"""Completion certificate for the Professional Certificate in Cybersecurity,
AI & Digital Resilience.

Issued only when the composite course grade meets the pass mark. The
certificate carries a verification code deterministically derived from the
achievement record and the student's persistent seed, so a facilitator can
re-derive it on the student's machine (`labctl certificate --verify <code>`)
and detect a hand-edited certificate. This is an integrity check for a local,
single-user classroom — not a cryptographic anti-forgery guarantee.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import html

from . import grade as grading
from . import paths, state
from .course import COURSE_MAP

PROGRAMME = "Professional Certificate in Cybersecurity, AI & Digital Resilience"
ISSUERS = "Kofi Annan International Peacekeeping Training Centre (KAIPTC) · Cyber1Defense Communication Ltd"


def _seed() -> int:
    return state.get_seed()


def _serial() -> str:
    h = hashlib.sha256(str(_seed()).encode()).hexdigest()[:6].upper()
    return f"CAIC-{_dt.date.today().year}-{h}"


def _grouped(code: str) -> str:
    return "-".join(code[i:i + 4] for i in range(0, len(code), 4))


def _code(rec: dict) -> str:
    """12-hex verification code over the canonical record + the student seed."""
    g = rec["grade"]
    canonical = "|".join(str(x) for x in (
        rec["serial"], rec["student"], rec["issued"],
        g["overall"], g["components"]["labs"]["pct"],
        g["components"]["quizzes"]["pct"], g["components"]["exam"]["pct"],
        _seed(),
    ))
    return _grouped(hashlib.sha256(canonical.encode()).hexdigest()[:12].upper())


def _modules_passed() -> list[dict]:
    """Gradable modules the student has completed (best score == max)."""
    from .manifest import discover_labs
    labs = {l.id: l for l in discover_labs()}
    out = []
    for mid, _day, title, _ in COURSE_MAP:
        lab = labs.get(mid)
        if lab and lab.max_points:
            done = state.lab_status(mid).get("best_score", 0) >= lab.max_points
            out.append({"id": mid, "title": title, "done": done})
    return out


def eligibility() -> dict:
    g = grading.compute()
    reasons = []
    c = g["components"]
    if not g["passed"]:
        if c["labs"]["pct"] < 100:
            reasons.append(f"complete the remaining labs ({c['labs']['got']}/{c['labs']['total']} points)")
        if c["quizzes"]["pct"] < 70:
            reasons.append(f"raise your quiz average ({c['quizzes']['pct']}%)")
        if c["exam"]["pct"] < 70:
            reasons.append(f"take/improve the final exam ({c['exam']['pct']}%)")
        if not reasons:
            reasons.append(f"reach {g['passMark']}% overall (currently {g['overall']}%)")
    return {"eligible": g["passed"], "grade": g, "reasons": reasons,
            "student": g["student"]}


def build(persist: bool = True) -> dict:
    """Assemble the certificate record (+ rendered HTML) if eligible."""
    elig = eligibility()
    if not elig["eligible"]:
        return {"eligible": False, "reasons": elig["reasons"], "grade": elig["grade"],
                "student": elig["student"]}
    serial = _serial()
    issued = (state.certificate_issue(serial)["issued"] if persist
              else _dt.date.today().isoformat())
    rec = {
        "serial": serial,
        "student": elig["student"] or "CAIC Participant",
        "programme": PROGRAMME,
        "issuers": ISSUERS,
        "issued": issued,
        "grade": elig["grade"],
        "modules": _modules_passed(),
    }
    rec["code"] = _code(rec)
    return {"eligible": True, "record": rec, "html": render_html(rec)}


def verify(code: str) -> dict:
    """Re-derive the code from this machine's record and compare."""
    b = build(persist=False)
    if not b["eligible"]:
        return {"ok": False, "reason": "no certificate has been earned on this machine yet"}
    want = b["record"]["code"]
    got = _grouped("".join(ch for ch in code.upper() if ch.isalnum()))
    return {"ok": got == want, "expected": want, "serial": b["record"]["serial"],
            "student": b["record"]["student"]}


# ───────────────────────────── rendering ────────────────────────────────

def render_html(rec: dict) -> str:
    e = html.escape
    g = rec["grade"]
    c = g["components"]
    mods = "".join(
        f'<li>{e(m["id"].upper())} — {e(m["title"])}</li>'
        for m in rec["modules"] if m["done"])
    issued_long = _dt.date.fromisoformat(rec["issued"]).strftime("%d %B %Y")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Certificate — {e(rec['student'])}</title>
<style>
  @page {{ size: A4 landscape; margin: 0; }}
  :root {{ --brand:#6d3fe0; --ink:#1a1530; --gold:#b4821a; --mut:#5c5570; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:#2a2440; font-family:Georgia,"Times New Roman",serif;
    color:var(--ink); display:flex; justify-content:center; padding:26px; }}
  .sheet {{ width:1040px; min-height:720px; background:#fdfcff; position:relative;
    padding:56px 64px; border:2px solid var(--brand);
    box-shadow:0 18px 60px rgba(0,0,0,.45); }}
  .sheet::before {{ content:""; position:absolute; inset:14px; border:1px solid var(--gold);
    pointer-events:none; }}
  .top {{ display:flex; justify-content:space-between; align-items:flex-start; }}
  .mark {{ width:60px; height:60px; border-radius:12px; background:var(--brand); color:#fff;
    display:grid; place-items:center; font-family:Arial,sans-serif; font-weight:800;
    font-size:19px; letter-spacing:1px; }}
  .issuer {{ text-align:right; font-size:12.5px; color:var(--mut); max-width:420px; line-height:1.5; }}
  .eyebrow {{ text-align:center; margin-top:30px; letter-spacing:4px; text-transform:uppercase;
    font-family:Arial,sans-serif; font-size:12px; color:var(--mut); }}
  h1 {{ text-align:center; font-size:34px; margin:6px 0 2px; color:var(--brand);
    letter-spacing:.5px; }}
  .sub {{ text-align:center; font-size:14px; color:var(--mut); }}
  .awarded {{ text-align:center; margin-top:34px; font-size:14px; color:var(--mut); }}
  .name {{ text-align:center; font-size:40px; margin:6px 0 4px; color:var(--ink);
    border-bottom:2px solid var(--gold); display:inline-block; padding:0 26px 6px; }}
  .namewrap {{ text-align:center; }}
  .body {{ text-align:center; max-width:720px; margin:22px auto 0; font-size:14.5px;
    line-height:1.7; color:#332c48; }}
  .grade {{ display:flex; justify-content:center; gap:26px; margin:24px 0 6px;
    font-family:Arial,sans-serif; }}
  .gi {{ text-align:center; }} .gi b {{ display:block; font-size:22px; color:var(--brand); }}
  .gi span {{ font-size:11px; letter-spacing:1px; text-transform:uppercase; color:var(--mut); }}
  .mods {{ columns:2; max-width:640px; margin:12px auto 0; font-size:12px; color:var(--mut);
    font-family:Arial,sans-serif; }}
  .mods li {{ margin:2px 0; }}
  .foot {{ display:flex; justify-content:space-between; align-items:flex-end; margin-top:40px; }}
  .sig {{ text-align:center; font-family:Arial,sans-serif; }}
  .sig .line {{ width:220px; border-top:1.5px solid var(--ink); margin-bottom:5px; }}
  .sig small {{ color:var(--mut); font-size:11px; }}
  .verify {{ text-align:center; font-family:"Courier New",monospace; font-size:11px; color:var(--mut); }}
  .verify b {{ font-size:14px; color:var(--ink); letter-spacing:1px; }}
  @media print {{ body {{ background:#fff; padding:0; }} .sheet {{ box-shadow:none; }} }}
</style></head>
<body><div class="sheet">
  <div class="top">
    <div class="mark">C1D</div>
    <div class="issuer"><strong>Awarded by</strong><br>{e(rec['issuers'])}<br>
      <em>CSA (Ghana) Tier-1 accredited training</em></div>
  </div>
  <div class="eyebrow">Certificate of Completion</div>
  <h1>Cybersecurity, AI &amp; Digital Resilience</h1>
  <div class="sub">{e(rec['programme'])}</div>
  <div class="awarded">This is to certify that</div>
  <div class="namewrap"><div class="name">{e(rec['student'])}</div></div>
  <div class="body">has successfully completed the five-day intensive programme — including the
    hands-on practical labs, module knowledge checks and the final examination — meeting the
    {g['passMark']}% certification standard across all assessed components.</div>
  <div class="grade">
    <div class="gi"><b>{g['overall']}%</b><span>Overall</span></div>
    <div class="gi"><b>{c['labs']['pct']}%</b><span>Labs</span></div>
    <div class="gi"><b>{c['quizzes']['pct']}%</b><span>Quizzes</span></div>
    <div class="gi"><b>{c['exam']['pct']}%</b><span>Final Exam</span></div>
  </div>
  <ul class="mods">{mods}</ul>
  <div class="foot">
    <div class="sig"><div class="line"></div><strong>Lead Facilitator</strong><br>
      <small>Cyber1Defense Communication Ltd</small></div>
    <div class="verify">Serial <b>{e(rec['serial'])}</b><br>
      Verification code<br><b>{e(rec['code'])}</b><br>Issued {e(issued_long)}</div>
    <div class="sig"><div class="line"></div><strong>Programme Director</strong><br>
      <small>KAIPTC</small></div>
  </div>
</div></body></html>"""
