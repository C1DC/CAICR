"""Grade a student's findings for a lab.

Two kinds of checks:
  - answer checks  (numeric / string / string_any): the student submits what
    they found; the engine compares it to the expected value.
  - script checks  (type='script'): verify.sh in the lab decides pass/fail,
    e.g. "does a capture file exist", "is the vulnerable service still up".

The engine deliberately does NOT run the attacking tool for the student — it
only confirms the finding. The learning is in doing the scan/capture itself.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass

from . import seed, state, ui
from .manifest import Check, Lab


@dataclass
class Outcome:
    check: Check
    passed: bool
    detail: str = ""


def _norm(s: str) -> str:
    return " ".join(str(s).strip().lower().split())


def grade_answer(check: Check, answer: str) -> Outcome:
    a = answer.strip()
    if check.type == "numeric":
        try:
            got = float(a.replace(",", ""))
        except ValueError:
            return Outcome(check, False, "not a number")
        exp = float(check.answer)
        if abs(got - exp) <= check.tolerance:
            return Outcome(check, True)
        return Outcome(check, False, "value does not match")
    if check.type == "string":
        return Outcome(check, _norm(a) == _norm(str(check.answer)))
    if check.type == "string_any":
        accepted = {_norm(x) for x in (check.accept or [check.answer])}
        return Outcome(check, _norm(a) in accepted)
    return Outcome(check, False, "unsupported answer type")


def run_script_check(lab: Lab, check: Check) -> Outcome:
    """Run verify.sh <check_id>; exit 0 = pass. stdout last line = detail."""
    if lab.verify_script is None:
        return Outcome(check, False, "no verify.sh provided")
    r = subprocess.run(["bash", str(lab.verify_script), check.id],
                       capture_output=True, text=True, cwd=str(lab.directory))
    detail = (r.stdout or r.stderr or "").strip().splitlines()
    return Outcome(check, r.returncode == 0, detail[-1] if detail else "")


def interactive(lab: Lab) -> None:
    """Prompt the student through each check, grade, and persist the result."""
    if not lab.checks:
        ui.warn("This lab has no verification checks defined yet.")
        return

    ui.header(f"Verify — {lab.module}: {lab.title}")
    ui.dim("  Enter what you found. Type 's' to skip a check, 'q' to quit.\n")

    vals = seed.compute(lab)
    seed.prepare(lab, vals)   # ensure on-disk evidence matches the grading
    results: dict[str, bool] = {}
    score = 0
    for i, check in enumerate(lab.checks, 1):
        check = seed.resolved_check(check, vals)
        if check.type == "script":
            out = run_script_check(lab, check)
            label = f"[{i}/{len(lab.checks)}] {check.prompt}"
            if out.passed:
                ui.ok(f"{label}  {ui.GREY}{out.detail}{ui.RESET}")
            else:
                ui.fail(f"{label}  {ui.GREY}{out.detail}{ui.RESET}")
            results[check.id] = out.passed
            score += check.points if out.passed else 0
            continue

        print(f"\n  {ui.BOLD}[{i}/{len(lab.checks)}] {check.prompt}{ui.RESET}")
        try:
            ans = input(f"  {ui.CYAN}answer>{ui.RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            ui.warn("Verification aborted — nothing recorded.")
            return
        if ans.lower() == "q":
            ui.warn("Stopped. Partial progress not saved.")
            return
        if ans.lower() == "s" or ans == "":
            ui.dim("    skipped")
            results[check.id] = False
            continue
        out = grade_answer(check, ans)
        if out.passed:
            ui.ok("correct")
            score += check.points
        else:
            msg = f"not quite ({out.detail})" if out.detail else "not quite"
            ui.fail(msg)
            if check.hint:
                ui.dim(f"    hint: {check.hint}")
        results[check.id] = out.passed

    state.record_result(lab.id, results, score, lab.max_points)

    print()
    pct = round(100 * score / lab.max_points) if lab.max_points else 0
    bar_full = int(pct / 5)
    bar = ui.GREEN + "█" * bar_full + ui.GREY + "░" * (20 - bar_full) + ui.RESET
    tone = ui.GREEN if pct == 100 else ui.YELLOW if pct >= 60 else ui.RED
    print(f"  Score: {bar} {tone}{score}/{lab.max_points}  ({pct}%){ui.RESET}")
    if pct == 100:
        ui.ok(f"{lab.module} complete — well done.")
    else:
        ui.info("Re-run `labctl verify " + lab.id + "` after investigating further.")
