#!/usr/bin/env python3
"""Generate FACILITATOR_ANSWER_KEY.md from the lab manifests, and expose the
model answers for the automated dry-run. Always in sync with lab.toml.

  python3 scripts/answer_key.py          # (re)write FACILITATOR_ANSWER_KEY.md

FACILITATOR-ONLY material — it contains every lab's answers.
"""
from __future__ import annotations

import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABS = ROOT / "labs"
OUT = ROOT / "FACILITATOR_ANSWER_KEY.md"


def load_labs():
    labs = []
    for d in sorted(LABS.iterdir()):
        if d.name.startswith("_") or not (d / "lab.toml").is_file():
            continue
        with (d / "lab.toml").open("rb") as fh:
            data = tomllib.load(fh)
        labs.append((d.name, data))
    labs.sort(key=lambda x: (x[1]["lab"].get("day", 0), x[1]["lab"]["id"]))
    return labs


def model_answer(c: dict):
    """The canonical answer to feed the grader (None for script checks)."""
    t = c.get("type", "string")
    if t == "script":
        return None
    if t in ("string", "numeric"):
        return str(c.get("answer", ""))
    if t == "string_any":
        acc = c.get("accept", [])
        return str(acc[0]) if acc else ""
    return ""


def answers_for(data: dict) -> list[str]:
    """Ordered model answers for the non-script checks (dry-run input)."""
    return [model_answer(c) for c in data.get("check", []) if c.get("type") != "script"]


def build_md() -> str:
    out = ["# CAIC CyberLab — Facilitator Answer Key",
           "",
           "> **Facilitator-only.** Model answers for every lab, generated from the",
           "> manifests (`python3 scripts/answer_key.py`). Do not distribute to students.",
           ""]
    for folder, data in load_labs():
        lab = data["lab"]
        checks = data.get("check", [])
        maxp = sum(int(c.get("points", 1)) for c in checks)
        out.append(f"## {lab['module']} — {lab['title']}")
        out.append(f"*Day {lab.get('day','?')} · {len(checks)} checks · {maxp} points · "
                   f"tools: {', '.join(lab.get('tools', [])) or '—'}*")
        out.append("")
        for i, c in enumerate(checks, 1):
            t = c.get("type", "string")
            raw = str(c.get("answer", "")) + "".join(str(x) for x in c.get("accept", []))
            if t == "script":
                ans = "_(automatic script check — verifies live state)_"
            elif "{{" in raw:
                ans = "**«randomized per student»** — grade on the student's own machine (`labctl verify`)"
            elif t == "string_any":
                acc = c.get("accept", [])
                ans = "**" + str(acc[0]) + "**" + (f"  _(also: {', '.join(map(str, acc[1:]))})_" if len(acc) > 1 else "")
            else:
                ans = "**" + str(c.get("answer", "")) + "**"
            out.append(f"{i}. {c.get('prompt','').strip()}")
            out.append(f"   → {ans}")
        out.append("")
    out += build_quiz_md()
    return "\n".join(out)


def build_quiz_md() -> list[str]:
    """Correct answers for the quizzes and final exam. Options are reshuffled
    per student in the app, so these are keyed by the answer *text*, not a/b/c/d."""
    bank_file = ROOT / "assessment" / "exams.toml"
    if not bank_file.is_file():
        return []
    with bank_file.open("rb") as fh:
        bank = tomllib.load(fh)
    out = ["---", "",
           "# Assessment answer key (quizzes & final exam)",
           "",
           "> Options are **shuffled per student**, so answers are given by text, not letter.",
           "> The baseline diagnostic is self-placement and is not graded.",
           ""]
    order = [k for k in ("baseline",) if k in bank]
    order += [k for k in bank if k not in ("baseline", "final")]
    order += [k for k in ("final",) if k in bank]
    for qid in order:
        quiz = bank[qid]
        qs = quiz.get("questions", [])
        out.append(f"## {quiz.get('title', qid)}  _(`{qid}` · {len(qs)} questions)_")
        out.append("")
        for i, q in enumerate(qs, 1):
            ans = q["options"][q["answer"]]
            out.append(f"{i}. {q['q'].strip()}")
            out.append(f"   → **{ans}**")
            if q.get("explain"):
                out.append(f"   _{q['explain'].strip()}_")
        out.append("")
    return out


def main() -> int:
    OUT.write_text(build_md(), encoding="utf-8")
    n = len(load_labs())
    print(f"wrote {OUT} ({n} labs + assessment answers)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
