"""Local web application for the CAIC CyberLab.

A single place where students do everything — dashboard, course, lessons, labs
(launched and graded from the browser), tools, materials, worksheets and a
command reference. Stdlib only (http.server); binds to localhost.

The API wraps the same engine the CLI uses, so the browser and the terminal
stay perfectly in sync.
"""
from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from . import __version__, certificate, dockerctl, grade as grading, paths, quiz, reference, state, verify
from .course import COMMANDS, COURSE_MAP, DAY_TITLES, LINUX_COMMANDS, RESOURCES, TOOLS
from .manifest import ManifestError, discover_labs, load_one
from .mdhtml import md_to_html

WEBUI = paths.ROOT / "webui"

# In-memory async action tracking for start/stop/reset (so the UI never hangs).
_ACTIONS: dict[str, dict] = {}
_LOCK = threading.Lock()


# ─────────────────────────────── data builders ──────────────────────────

def _lab_by_id() -> dict:
    out = {}
    for lab in discover_labs():
        out[lab.id] = lab
    return out


def _module_rows() -> list[dict]:
    labs = _lab_by_id()
    rows = []
    for mid, day, title, has_lab in COURSE_MAP:
        lesson = paths.LESSONS_DIR / f"{mid}.md"
        worksheets = sorted(paths.WORKSHEETS_DIR.glob(f"{mid}-*.md"))
        lab = labs.get(mid)
        entry = state.lab_status(mid)
        best = entry.get("best_score", 0)
        maxp = lab.max_points if lab else 0
        rows.append({
            "id": mid, "day": day, "title": title,
            "hasLesson": lesson.is_file(),
            "hasLab": bool(lab),
            "hasWorksheets": bool(worksheets),
            "worksheets": [w.name for w in worksheets],
            "bestScore": best, "maxPoints": maxp,
            "complete": bool(maxp and best >= maxp),
        })
    return rows


def _lab_detail(lab) -> dict:
    if not lab.has_targets:
        # personalise a file-based lab's evidence when its page is opened
        from . import seed
        seed.prepare(lab, seed.compute(lab))
    entry = state.lab_status(lab.id)
    verified = entry.get("verified", {})
    return {
        "id": lab.id, "module": lab.module, "title": lab.title, "day": lab.day,
        "objective": lab.objective, "tools": lab.tools,
        "estMinutes": lab.estimated_minutes,
        "hasTargets": lab.has_targets, "subnet": lab.subnet,
        "briefingHtml": md_to_html(lab.briefing_file.read_text(encoding="utf-8"))
            if lab.briefing_file else "",
        "targets": [{"name": t.name, "ip": t.ip, "role": t.role} for t in lab.targets],
        "checks": [{"id": c.id, "prompt": c.prompt, "hint": c.hint,
                    "type": c.type, "points": c.points,
                    "passed": verified.get(c.id)} for c in lab.checks],
        "maxPoints": lab.max_points,
        "bestScore": entry.get("best_score", 0),
        "complete": bool(lab.max_points and entry.get("best_score", 0) >= lab.max_points),
    }


def _lab_runtime(lab) -> dict:
    with _LOCK:
        act = dict(_ACTIONS.get(lab.id, {}))
    running = False
    services = []
    if lab.has_targets:
        try:
            svcs = dockerctl.running_services(lab)
            running = len(svcs) > 0
            services = [s.get("Service", s.get("Name", "?")) for s in svcs]
        except Exception:
            pass
    entry = state.lab_status(lab.id)
    return {
        "id": lab.id, "hasTargets": lab.has_targets,
        "running": running, "services": services,
        "busy": act.get("busy", False), "op": act.get("op"),
        "error": act.get("error"),
        "bestScore": entry.get("best_score", 0), "maxPoints": lab.max_points,
        "complete": bool(lab.max_points and entry.get("best_score", 0) >= lab.max_points),
    }


def _assessment() -> dict:
    """Quiz/exam/diagnostic availability + the student's best scores, plus the
    composite grade. Correct answers are never included."""
    bank = quiz.load()
    module_ids = [m for m, _, _, _ in COURSE_MAP if m in bank]

    def _card(qid):
        q = bank.get(qid, {})
        st = state.quiz_status(qid)
        n = len(q.get("questions", []))
        best = min(st.get("best", 0), n)
        return {
            "id": qid, "title": q.get("title", qid),
            "questions": n, "best": best,
            "pct": round(100 * best / n) if n else 0,
            "attempted": bool(st),
            "graded": qid != "baseline",
        }

    return {
        "quizzes": [_card(m) for m in module_ids],
        "exam": _card("final") if "final" in bank else None,
        "baseline": _card("baseline") if "baseline" in bank else None,
        "grade": grading.compute(),
    }


def _bootstrap() -> dict:
    mods = _module_rows()
    gradable = [m for m in mods if m["maxPoints"] > 0]
    done = sum(1 for m in gradable if m["complete"])
    return {
        "version": __version__,
        "student": state.get_student(),
        "dayTitles": DAY_TITLES,
        "modules": mods,
        "tools": TOOLS,
        "resources": RESOURCES,
        "commands": [{"group": g, "cmd": c, "desc": d} for g, c, d in COMMANDS],
        "linux": [{"group": g, "cmd": c, "desc": d} for g, c, d in LINUX_COMMANDS],
        "reference": reference.discover(),
        "grade": grading.compute(),
        "summary": {"labsComplete": done, "totalLabs": len(gradable),
                    "totalModules": len(mods),
                    "dockerOk": dockerctl.preflight().ok,
                    "terminal": os.environ.get("CAIC_NO_TERMINAL") != "1",
                    "classroomUrl": os.environ.get("CAIC_CLASSROOM", "")},
    }


def _run_lab_op(lab_id: str, op: str) -> None:
    """Background worker for start/stop/reset so HTTP returns immediately."""
    try:
        lab = load_one(lab_id)
        if op == "start":
            from . import seed
            vals = seed.compute(lab)
            seed.prepare(lab, vals)
            dockerctl.up(lab, env=seed.env_for(vals))
            dockerctl.wait_ready(lab)
            state.mark_started(lab.id)
        elif op == "stop":
            dockerctl.down(lab)
            state.mark_stopped(lab.id)
        elif op == "reset":
            dockerctl.restart(lab)
        with _LOCK:
            _ACTIONS[lab_id] = {"busy": False, "op": op, "error": None}
    except Exception as exc:  # noqa: BLE001 - surfaced to the UI
        with _LOCK:
            _ACTIONS[lab_id] = {"busy": False, "op": op, "error": str(exc)}


def _start_op(lab_id: str, op: str) -> dict:
    with _LOCK:
        if _ACTIONS.get(lab_id, {}).get("busy"):
            return {"busy": True, "op": _ACTIONS[lab_id]["op"]}
        _ACTIONS[lab_id] = {"busy": True, "op": op, "error": None}
    threading.Thread(target=_run_lab_op, args=(lab_id, op), daemon=True).start()
    return {"busy": True, "op": op}


def _grade(lab, answers: dict) -> dict:
    from . import seed
    vals = seed.compute(lab)
    seed.prepare(lab, vals)   # ensure on-disk evidence matches the grading
    results = []
    score = 0
    verified = {}
    for c in lab.checks:
        c = seed.resolved_check(c, vals)
        if c.type == "script":
            out = verify.run_script_check(lab, c)
        else:
            out = verify.grade_answer(c, str(answers.get(c.id, "")))
        verified[c.id] = out.passed
        score += c.points if out.passed else 0
        results.append({"id": c.id, "passed": out.passed,
                        "detail": out.detail, "hint": c.hint})
    state.record_result(lab.id, verified, score, lab.max_points)
    entry = state.lab_status(lab.id)
    return {"results": results, "score": score, "maxPoints": lab.max_points,
            "bestScore": entry.get("best_score", 0),
            "complete": bool(lab.max_points and entry.get("best_score", 0) >= lab.max_points)}


# ─────────────────────────────── HTTP handler ───────────────────────────

class Handler(BaseHTTPRequestHandler):
    server_version = "CAIC-CyberLab"

    def log_message(self, *a):  # quiet
        pass

    # -- helpers --
    def _json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _html(self, body, code=200):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _err(self, msg, code=400):
        self._json({"error": msg}, code)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length", 0) or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}

    def _static(self, path: str):
        # map "/" -> index.html; prevent path traversal
        rel = path.lstrip("/") or "index.html"
        target = (WEBUI / rel).resolve()
        if WEBUI.resolve() not in target.parents and target != WEBUI.resolve() / rel:
            if not str(target).startswith(str(WEBUI.resolve())):
                return self._err("forbidden", 403)
        if not target.is_file():
            return self._err("not found", 404)
        ctype = {"html": "text/html", "css": "text/css", "js": "application/javascript",
                 "svg": "image/svg+xml", "json": "application/json",
                 "ico": "image/x-icon"}.get(target.suffix.lstrip("."), "application/octet-stream")
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype + ("; charset=utf-8" if ctype.startswith("text") or ctype.endswith("javascript") else ""))
        self.send_header("Content-Length", str(len(data)))
        # Never let the browser cache the app shell/JS/CSS, so a `git pull` +
        # restart always serves the latest UI (no hard-refresh needed).
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(data)

    # -- routing --
    def do_GET(self):
        p = urlparse(self.path).path
        # Real browser terminal: upgrade this GET to a WebSocket <-> PTY bridge.
        if p == "/ws/terminal":
            from . import webterm
            if webterm.is_upgrade(self):
                try:
                    webterm.handle(self)
                except Exception:
                    pass
                return
            return self._err("expected websocket upgrade", 400)
        try:
            if p == "/api/bootstrap":
                return self._json(_bootstrap())
            if p.startswith("/api/lesson/"):
                mid = p.rsplit("/", 1)[-1]
                f = paths.LESSONS_DIR / f"{mid}.md"
                if not f.is_file():
                    return self._err("no lesson", 404)
                md = f.read_text(encoding="utf-8")
                return self._json({"id": mid, "title": md.splitlines()[0].lstrip("# ").strip(),
                                   "html": md_to_html(md)})
            if p.startswith("/api/worksheets/"):
                mid = p.rsplit("/", 1)[-1]
                sheets = [{"name": w.name, "html": md_to_html(w.read_text(encoding="utf-8"))}
                          for w in sorted(paths.WORKSHEETS_DIR.glob(f"{mid}-*.md"))]
                return self._json({"id": mid, "sheets": sheets})
            if p == "/api/reference":
                return self._json({"topics": reference.discover()})
            if p.startswith("/api/reference/"):
                tid = p.rsplit("/", 1)[-1]
                md = reference.load(tid)
                if md is None:
                    return self._err("no such reference topic", 404)
                title = next((t["title"] for t in reference.discover() if t["id"] == tid), tid)
                return self._json({"id": tid, "title": title, "html": md_to_html(md)})
            if p.startswith("/api/lab/") and p.endswith("/status"):
                lab = load_one(p.split("/")[3])
                return self._json(_lab_runtime(lab))
            if p.startswith("/api/lab/"):
                lab = load_one(p.split("/")[3])
                detail = _lab_detail(lab)
                detail["runtime"] = _lab_runtime(lab)
                return self._json(detail)
            if p == "/api/progress":
                return self._json({"modules": _module_rows(), "student": state.get_student()})
            if p == "/api/assessment":
                return self._json(_assessment())
            if p == "/api/grade":
                return self._json(grading.compute())
            if p == "/api/submission":
                from . import classroom
                return self._json(classroom.build_submission())
            if p == "/api/certificate":
                b = certificate.build()
                b.pop("html", None)   # the SPA fetches the printable page separately
                return self._json(b)
            if p == "/certificate.html":
                b = certificate.build()
                if b["eligible"]:
                    return self._html(b["html"])
                reasons = "".join(f"<li>{r}</li>" for r in b.get("reasons", []))
                return self._html(
                    "<!doctype html><meta charset=utf-8><title>Certificate</title>"
                    "<body style='font-family:system-ui;max-width:640px;margin:60px auto;"
                    "padding:0 20px;color:#1a1530'><h1>Not earned yet</h1>"
                    f"<p>You're at {b['grade']['overall']}% overall; the pass mark is "
                    f"{b['grade']['passMark']}%.</p><p>To earn your certificate:</p>"
                    f"<ul>{reasons}</ul>"
                    "<p><a href='/#assessment'>← Back to the assessment</a></p></body>",
                    code=403)
            if p.startswith("/api/quiz/"):
                qid = p.rsplit("/", 1)[-1]
                items = quiz.present(qid)
                if not items:
                    return self._err("no such quiz", 404)
                # strip the server-side permutation — the browser only sees options
                for it in items:
                    it.pop("_order", None)
                    it.pop("explain", None)
                meta = quiz.load().get(qid, {})
                return self._json({"id": qid, "title": meta.get("title", qid),
                                   "graded": qid != "baseline", "questions": items})
            if p.startswith("/api/"):
                return self._err("unknown endpoint", 404)
            return self._static(p)
        except ManifestError as exc:
            self._err(str(exc), 404)
        except Exception as exc:  # noqa: BLE001
            self._err(str(exc), 500)

    def do_POST(self):
        p = urlparse(self.path).path
        try:
            if p == "/api/student":
                name = str(self._body().get("name", "")).strip()
                state.set_student(name)
                return self._json({"student": state.get_student()})
            if p == "/api/submit":
                from . import classroom
                url = str(self._body().get("url", "")).strip()
                if not url:
                    return self._err("a classroom URL is required", 400)
                try:
                    classroom.post_submission(url, classroom.build_submission())
                except Exception as exc:  # noqa: BLE001
                    return self._err(f"could not reach {url}: {exc}", 502)
                return self._json({"ok": True, "url": url})
            if p.startswith("/api/quiz/"):
                qid = p.rsplit("/", 1)[-1]
                answers = self._body().get("answers", [])
                if not isinstance(answers, list):
                    return self._err("answers must be a list", 400)
                res = quiz.grade(qid, [int(a) if a is not None else -1 for a in answers])
                if not res["total"]:
                    return self._err("no such quiz", 404)
                res["grade"] = grading.compute()
                return self._json(res)
            if p.startswith("/api/lab/"):
                parts = p.split("/")
                lab_id, action = parts[3], parts[4] if len(parts) > 4 else ""
                lab = load_one(lab_id)
                if action in ("start", "stop", "reset"):
                    if not lab.has_targets:
                        return self._err("this lab has no targets to control", 400)
                    return self._json(_start_op(lab_id, action))
                if action == "verify":
                    answers = self._body().get("answers", {})
                    return self._json(_grade(lab, answers))
            return self._err("unknown endpoint", 404)
        except ManifestError as exc:
            self._err(str(exc), 404)
        except Exception as exc:  # noqa: BLE001
            self._err(str(exc), 500)


def serve(host: str = "127.0.0.1", port: int = 8899) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer((host, port), Handler)
    return httpd
