"""Knowledge-check quizzes, the final exam, and the baseline diagnostic.

Loaded from assessment/exams.toml. Each question's options are shuffled
per-student (via the seed) so the correct answer's position can't be shared.
The correct answer is never sent to the browser; grading maps the student's
chosen option back to the original correct one.
"""
from __future__ import annotations

import random
import tomllib

from . import paths, state, ui


def load() -> dict:
    if not paths.ASSESSMENT_FILE.is_file():
        return {}
    with paths.ASSESSMENT_FILE.open("rb") as fh:
        return tomllib.load(fh)


def _shuffled(quiz_id: str, qi: int, n: int) -> list[int]:
    """A per-student permutation of option indices for one question."""
    order = list(range(n))
    random.Random(f"{state.get_seed()}:{quiz_id}:{qi}").shuffle(order)
    return order


def present(quiz_id: str) -> list[dict]:
    """Questions with options shuffled for this student; NO correct answer.
    Each item carries the permutation so grading can map choices back."""
    quiz = load().get(quiz_id)
    if not quiz:
        return []
    out = []
    for qi, q in enumerate(quiz.get("questions", [])):
        opts = q["options"]
        order = _shuffled(quiz_id, qi, len(opts))
        out.append({
            "q": q["q"],
            "options": [opts[i] for i in order],
            "_order": order,              # shown index -> original index
            "explain": q.get("explain", ""),
        })
    return out


def grade(quiz_id: str, answers: list[int]) -> dict:
    """answers: the shown-option index chosen for each question (or -1)."""
    quiz = load().get(quiz_id, {})
    questions = quiz.get("questions", [])
    results, score = [], 0
    for qi, q in enumerate(questions):
        order = _shuffled(quiz_id, qi, len(q["options"]))
        chosen = answers[qi] if qi < len(answers) else -1
        chosen_original = order[chosen] if 0 <= chosen < len(order) else -1
        correct = chosen_original == q["answer"]
        score += 1 if correct else 0
        results.append({
            "correct": correct,
            "correctOption": q["options"][q["answer"]],
            "explain": q.get("explain", ""),
        })
    total = len(questions)
    graded = quiz_id != "baseline"   # the diagnostic is self-placement only
    if graded and total:
        state.record_quiz(quiz_id, score, total)
    return {"score": score, "total": total, "results": results, "graded": graded}


def interactive(quiz_id: str) -> None:
    quiz = load().get(quiz_id)
    if not quiz:
        ui.error(f"no quiz '{quiz_id}' (try: labctl quiz)")
        return
    items = present(quiz_id)
    ui.banner(f"{quiz.get('title', quiz_id)}")
    if quiz_id == "baseline":
        ui.dim("  Baseline diagnostic — not graded; for your own placement.\n")
    answers = []
    for i, it in enumerate(items):
        print(f"\n  {ui.BOLD}[{i+1}/{len(items)}] {it['q']}{ui.RESET}")
        for j, opt in enumerate(it["options"]):
            print(f"      {ui.CYAN}{chr(97+j)}{ui.RESET}) {opt}")
        try:
            raw = input(f"  {ui.CYAN}answer (a-{chr(96+len(it['options']))}, q to quit)>{ui.RESET} ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(); ui.warn("Quiz aborted — nothing recorded."); return
        if raw == "q":
            ui.warn("Stopped — nothing recorded."); return
        answers.append(ord(raw[0]) - 97 if raw and raw[0].isalpha() else -1)
    res = grade(quiz_id, answers)
    print()
    for i, r in enumerate(res["results"]):
        if r["correct"]:
            ui.ok(f"Q{i+1} correct")
        else:
            ui.fail(f"Q{i+1} — correct answer: {r['correctOption']}")
            if r["explain"]:
                ui.dim(f"      {r['explain']}")
    pct = round(100 * res["score"] / res["total"]) if res["total"] else 0
    bar = ui.GREEN + "█" * int(pct / 5) + ui.GREY + "░" * (20 - int(pct / 5)) + ui.RESET
    print(f"\n  Score: {bar} {res['score']}/{res['total']} ({pct}%)")
    if res["graded"]:
        ui.info("Recorded. See your overall grade with: labctl grade")
