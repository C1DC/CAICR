"""Local web application for the CAIC CyberLab.

A single place where students do everything — dashboard, course, lessons, labs
(launched and graded from the browser), tools, materials, worksheets and a
command reference. Stdlib only (http.server); binds to localhost.

The API wraps the same engine the CLI uses, so the browser and the terminal
stay perfectly in sync.
"""
from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from . import __version__, dockerctl, paths, state, verify
from .course import COMMANDS, COURSE_MAP, DAY_TITLES, TOOLS
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


def _bootstrap() -> dict:
    mods = _module_rows()
    done = sum(1 for m in mods if m["complete"])
    return {
        "version": __version__,
        "student": state.get_student(),
        "dayTitles": DAY_TITLES,
        "modules": mods,
        "tools": TOOLS,
        "commands": [{"group": g, "cmd": c, "desc": d} for g, c, d in COMMANDS],
        "summary": {"labsComplete": done, "totalModules": len(mods),
                    "dockerOk": dockerctl.preflight().ok},
    }


def _run_lab_op(lab_id: str, op: str) -> None:
    """Background worker for start/stop/reset so HTTP returns immediately."""
    try:
        lab = load_one(lab_id)
        if op == "start":
            dockerctl.up(lab)
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
    results = []
    score = 0
    verified = {}
    for c in lab.checks:
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
        self.end_headers()
        self.wfile.write(data)

    # -- routing --
    def do_GET(self):
        p = urlparse(self.path).path
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
