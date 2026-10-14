"""Facilitator classroom — student submissions, aggregation, and a dashboard.

Every student runs the lab on their OWN machine, so their scores live in their own
state.json. To let a facilitator see the class, scores must be *moved*. Two models,
both stdlib-only, offline/LAN, no external service:

  1. Collect & view   — student: `labctl submit` writes a signed score file;
                        facilitator gathers the files and runs
                        `labctl report <dir> --html board.html`.
  2. Live classroom   — facilitator: `labctl classroom` runs a LAN server + live
                        dashboard; student: `labctl submit --to http://<ip>:7000`.

Integrity: each submission carries a `sig` derived from the machine's per-student
seed + the raw scores, so casual tampering is detectable and a submission is tied
to that machine's seed. It is NOT tamper-proof against someone with the source — for
assured scores a facilitator uses the live server and/or watches `labctl verify`.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import re
from pathlib import Path

from . import grade, paths, quiz, state
from .course import COURSE_MAP
from .manifest import discover_labs


# ───────────────────────────── scoring helpers ──────────────────────────────

def _lab_maxpts() -> dict:
    return {l.id: l.max_points for l in discover_labs()}


def _lab_ids() -> list:
    return [l.id for l in discover_labs()]


def grade_from(data: dict, maxpts: dict | None = None, bank: dict | None = None) -> dict:
    """Recompute the composite grade from a progress/submission dict (so the
    facilitator never trusts a 'grade' field a student could edit)."""
    maxpts = maxpts if maxpts is not None else _lab_maxpts()
    bank = bank if bank is not None else quiz.load()
    labs = data.get("labs", {}) or {}
    lg = lt = 0
    for lid, mp in maxpts.items():
        if mp > 0:
            lt += mp
            lg += min(int(labs.get(lid, {}).get("best_score", 0) or 0), mp)
    labs_f = lg / lt if lt else 0.0

    quizzes = data.get("quizzes", {}) or {}
    module_ids = [m for m, _, _, _ in COURSE_MAP if m in bank]
    qg = qt = 0
    for qid in module_ids:
        n = len(bank[qid].get("questions", []))
        qt += n
        qg += min(int(quizzes.get(qid, {}).get("best", 0) or 0), n)
    quiz_f = qg / qt if qt else 0.0

    en = len(bank.get("final", {}).get("questions", []))
    eg = min(int(quizzes.get("final", {}).get("best", 0) or 0), en)
    exam_f = eg / en if en else 0.0

    overall = (grade.WEIGHTS["labs"] * labs_f + grade.WEIGHTS["quizzes"] * quiz_f
               + grade.WEIGHTS["exam"] * exam_f)
    return {
        "labs": {"got": lg, "total": lt, "pct": round(100 * labs_f)},
        "quizzes": {"got": qg, "total": qt, "pct": round(100 * quiz_f)},
        "exam": {"got": eg, "total": en, "pct": round(100 * exam_f)},
        "overall": round(100 * overall),
        "passed": overall >= grade.PASS_MARK,
    }


def _sig(data: dict) -> str:
    """A 12-hex check code over the per-student seed + the raw scores."""
    labs = {k: int(v.get("best_score", 0) or 0) for k, v in sorted((data.get("labs") or {}).items())}
    quizzes = {k: int(v.get("best", 0) or 0) for k, v in sorted((data.get("quizzes") or {}).items())}
    canonical = json.dumps(
        {"seed": data.get("seed"), "student": data.get("student", ""),
         "labs": labs, "quizzes": quizzes}, sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()[:12].upper()


def build_submission() -> dict:
    """The student's own machine: package progress into a signed submission."""
    data = state.all_progress()
    sub = {
        "kind": "caic-submission",
        "version": 1,
        "student": data.get("student", "") or "(unnamed)",
        "seed": data.get("seed"),
        "generated": _dt.datetime.now().isoformat(timespec="seconds"),
        "labs": {k: {"best_score": int(v.get("best_score", 0) or 0),
                     "max_points": int(v.get("max_points", 0) or 0)}
                 for k, v in (data.get("labs") or {}).items()},
        "quizzes": {k: {"best": int(v.get("best", 0) or 0), "total": int(v.get("total", 0) or 0)}
                    for k, v in (data.get("quizzes") or {}).items()},
    }
    sub["grade"] = grade_from(data)
    sub["sig"] = _sig(data)
    return sub


def aggregate(files: list) -> dict:
    """Facilitator: fold a list of submission/state files into a class view."""
    maxpts = _lab_maxpts()
    bank = quiz.load()
    lab_ids = _lab_ids()
    rows = []
    for f in files:
        data = state.load_file(f)
        if not isinstance(data, dict) or not data:
            continue
        who = (data.get("student") or Path(f).stem or "(unnamed)").strip()
        g = grade_from(data, maxpts, bank)
        labs = {lid: int((data.get("labs", {}).get(lid, {}) or {}).get("best_score", 0) or 0)
                for lid in lab_ids}
        sig_ok = (data.get("sig") == _sig(data)) if data.get("sig") else None
        rows.append({
            "student": who, "labs": labs, "grade": g,
            "generated": data.get("generated", ""),
            "sigOk": sig_ok,
        })
    rows.sort(key=lambda r: (-r["grade"]["overall"], r["student"].lower()))
    n = len(rows)
    passed = sum(1 for r in rows if r["grade"]["passed"])
    avg = round(sum(r["grade"]["overall"] for r in rows) / n) if n else 0
    labs_done = sum(
        sum(1 for lid in lab_ids if maxpts.get(lid, 0) and r["labs"].get(lid, 0) >= maxpts[lid])
        for r in rows)
    return {
        "labIds": lab_ids,
        "maxpts": maxpts,
        "rows": rows,
        "stats": {"n": n, "passed": passed, "avg": avg,
                  "passMark": round(100 * grade.PASS_MARK),
                  "labsDoneTotal": labs_done, "labsPossible": n * sum(1 for v in maxpts.values() if v)},
        "updated": _dt.datetime.now().isoformat(timespec="seconds"),
    }


# ───────────────────────────── dashboard HTML ───────────────────────────────

_PAGE = r"""<!doctype html><html lang="en" data-theme="dark"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>CAIC CyberLab — Facilitator Dashboard</title>
<style>
:root{--bg:#0e0b16;--panel:#17132a;--panel2:#1d1830;--border:#2e2740;--kali:#9b6dff;
--kali-lt:#c3a6ff;--gold:#ffcf6b;--teal:#5fd3c6;--fg:#ece8f5;--fg-dim:#7d7595;--green:#57d98a;--red:#ff6b7a;color-scheme:dark;}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]){--bg:#f6f4fb;--panel:#fff;--panel2:#efeaf8;--border:#e0d9f0;--fg:#241d38;--fg-dim:#7a7191;--kali-lt:#6f3fe0;--gold:#b9811a;--teal:#1f9c8e;--green:#1f9d57;color-scheme:light;}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
header{display:flex;align-items:center;gap:12px;padding:14px 20px;background:linear-gradient(90deg,#1a1230,#241a3f);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:5}
header b{color:var(--gold)}header .brand{font-weight:700;color:var(--kali-lt)}
header .spacer{flex:1}header .meta{font-size:12.5px;color:var(--fg-dim)}
.wrap{max-width:1180px;margin:0 auto;padding:20px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-bottom:20px}
.stat{background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:14px 16px}
.stat .big{font-size:30px;font-weight:700}.stat .lbl{font-size:12px;color:var(--fg-dim);text-transform:uppercase;letter-spacing:.5px}
table{border-collapse:collapse;width:100%;background:var(--panel);border:1px solid var(--border);border-radius:12px;overflow:hidden;font-size:13.5px}
th,td{padding:8px 10px;text-align:center;border-bottom:1px solid var(--border)}
th{background:var(--panel2);color:var(--fg-dim);text-transform:uppercase;font-size:11px;letter-spacing:.5px;position:sticky;top:56px}
td.name{text-align:left;font-weight:600;white-space:nowrap}
tr:hover td{background:var(--panel2)}
.cell-done{color:var(--green);font-weight:700}.cell-part{color:var(--gold)}.cell-none{color:var(--fg-dim)}
.pill{display:inline-block;padding:2px 9px;border-radius:999px;font-size:12px;font-weight:700}
.pass{background:rgba(87,217,138,.16);color:var(--green)}.fail{background:rgba(255,107,122,.16);color:var(--red)}
.grade{font-weight:700}.warn{color:var(--red);font-size:11px}
.empty{padding:40px;text-align:center;color:var(--fg-dim)}
.foot{margin-top:16px;font-size:12px;color:var(--fg-dim)}
</style></head><body>
<header><span class="brand">KAIPTC · CAIC CyberLab — <b>Facilitator Dashboard</b></span>
<span class="spacer"></span><span class="meta" id="meta"></span></header>
<div class="wrap">
  <div class="stats" id="stats"></div>
  <div id="board"></div>
  <div class="foot" id="foot"></div>
</div>
<script>
function esc(s){return String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function render(D){
  if(!D||!D.rows){document.getElementById('board').innerHTML='<div class="empty">No submissions yet.</div>';return;}
  const s=D.stats;
  document.getElementById('stats').innerHTML=
    `<div class="stat"><div class="big">${s.n}</div><div class="lbl">Students</div></div>`+
    `<div class="stat"><div class="big" style="color:var(--green)">${s.passed}</div><div class="lbl">Passed (&ge;${s.passMark}%)</div></div>`+
    `<div class="stat"><div class="big" style="color:var(--gold)">${s.avg}%</div><div class="lbl">Class average</div></div>`+
    `<div class="stat"><div class="big" style="color:var(--kali-lt)">${s.labsDoneTotal}</div><div class="lbl">Labs completed</div></div>`;
  const ids=D.labIds;
  let h='<div style="overflow:auto"><table><thead><tr><th class="name">Student</th><th>Grade</th><th>Status</th>'+
    ids.map(i=>`<th>${i.toUpperCase()}</th>`).join('')+'</tr></thead><tbody>';
  for(const r of D.rows){
    const g=r.grade;
    const cells=ids.map(i=>{const v=r.labs[i]||0;const mp=D.maxpts[i]||0;
      if(mp&&v>=mp)return '<td class="cell-done">&#10003;</td>';
      if(v>0)return `<td class="cell-part">${v}</td>`;
      return '<td class="cell-none">&middot;</td>';}).join('');
    const sig=r.sigOk===false?' <span class="warn" title="score signature mismatch — verify">&#9888;</span>':'';
    h+=`<tr><td class="name">${esc(r.student)}${sig}</td>`+
       `<td class="grade">${g.overall}%</td>`+
       `<td><span class="pill ${g.passed?'pass':'fail'}">${g.passed?'PASS':'—'}</span></td>`+cells+'</tr>';
  }
  h+='</tbody></table></div>';
  document.getElementById('board').innerHTML=h;
  document.getElementById('meta').textContent='updated '+(D.updated||'');
  document.getElementById('foot').textContent='Grade = labs 50% · quizzes 25% · exam 25%. '+
    '⚠ = score signature mismatch (confirm with labctl verify). '+ids.length+' labs.';
}
/*__BOOT__*/
</script></body></html>"""


def dashboard_html(agg: dict | None, live: bool = False) -> str:
    if live:
        boot = ("async function tick(){try{const r=await fetch('/api/scores');render(await r.json());}"
                "catch(e){}}tick();setInterval(tick,5000);")
    else:
        boot = "render(" + json.dumps(agg or {}) + ");"
    return _PAGE.replace("/*__BOOT__*/", boot)


# ───────────────────────────── live server ──────────────────────────────────

def serve(host: str, port: int, subdir):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    sub = Path(subdir)
    sub.mkdir(parents=True, exist_ok=True)

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):  # quiet
            pass

        def _send(self, code, body, ctype):
            if isinstance(body, str):
                body = body.encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                return self._send(200, dashboard_html(None, live=True), "text/html; charset=utf-8")
            if self.path.startswith("/api/scores"):
                files = sorted(sub.glob("*.json"))
                return self._send(200, json.dumps(aggregate(files)), "application/json")
            self._send(404, "not found", "text/plain")

        def do_POST(self):
            if not self.path.startswith("/api/submit"):
                return self._send(404, "not found", "text/plain")
            try:
                length = int(self.headers.get("Content-Length", "0") or 0)
                raw = self.rfile.read(length)
                obj = json.loads(raw)
                if not isinstance(obj, dict):
                    raise ValueError
            except Exception:  # noqa: BLE001
                return self._send(400, '{"error":"bad submission"}', "application/json")
            name = re.sub(r"[^A-Za-z0-9_.-]", "_", (obj.get("student") or "anon"))[:48] or "anon"
            try:
                (sub / f"{name}.json").write_text(json.dumps(obj), encoding="utf-8")
            except OSError:
                return self._send(500, '{"error":"write failed"}', "application/json")
            self._send(200, '{"ok":true}', "application/json")

    return ThreadingHTTPServer((host, port), Handler), sub


def post_submission(url: str, sub: dict, timeout: float = 6.0) -> None:
    """Student side: POST a submission to a classroom server (raises on failure)."""
    import urllib.request
    endpoint = url.rstrip("/")
    if not endpoint.endswith("/api/submit"):
        endpoint += "/api/submit"
    req = urllib.request.Request(
        endpoint, data=json.dumps(sub).encode("utf-8"),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (LAN, user-provided)
        resp.read()
