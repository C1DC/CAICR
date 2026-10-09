"""Composite course grade: hands-on labs + module quizzes + final exam, weighted
and pass-gated. The baseline diagnostic is excluded (self-placement only)."""
from __future__ import annotations

from . import quiz, state
from .course import COURSE_MAP
from .manifest import discover_labs

WEIGHTS = {"labs": 0.50, "quizzes": 0.25, "exam": 0.25}
PASS_MARK = 0.70   # 70%


def _labs_fraction() -> tuple[float, int, int]:
    got = tot = 0
    for lab in discover_labs():
        if lab.max_points > 0:
            got += min(state.lab_status(lab.id).get("best_score", 0), lab.max_points)
            tot += lab.max_points
    return (got / tot if tot else 0.0), got, tot


def _quizzes_fraction() -> tuple[float, int, int]:
    bank = quiz.load()
    module_ids = [m for m, _, _, _ in COURSE_MAP if m in bank]
    got = tot = 0
    for qid in module_ids:
        n = len(bank[qid].get("questions", []))
        tot += n
        got += min(state.quiz_status(qid).get("best", 0), n)
    return (got / tot if tot else 0.0), got, tot


def _exam_fraction() -> tuple[float, int, int]:
    bank = quiz.load()
    n = len(bank.get("final", {}).get("questions", []))
    got = min(state.quiz_status("final").get("best", 0), n)
    return (got / n if n else 0.0), got, n


def compute() -> dict:
    labs_f, lg, lt = _labs_fraction()
    quiz_f, qg, qt = _quizzes_fraction()
    exam_f, eg, et = _exam_fraction()
    overall = (WEIGHTS["labs"] * labs_f + WEIGHTS["quizzes"] * quiz_f
               + WEIGHTS["exam"] * exam_f)
    return {
        "components": {
            "labs": {"weight": WEIGHTS["labs"], "pct": round(100 * labs_f), "got": lg, "total": lt},
            "quizzes": {"weight": WEIGHTS["quizzes"], "pct": round(100 * quiz_f), "got": qg, "total": qt},
            "exam": {"weight": WEIGHTS["exam"], "pct": round(100 * exam_f), "got": eg, "total": et},
        },
        "overall": round(100 * overall),
        "passMark": round(100 * PASS_MARK),
        "passed": overall >= PASS_MARK,
        "student": state.get_student(),
    }
