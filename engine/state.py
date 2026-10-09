"""Per-student progress and running-lab tracking. JSON on disk, fault-tolerant."""
from __future__ import annotations

import datetime as _dt
import json

from . import paths


def _now() -> str:
    return _dt.datetime.now().isoformat(timespec="seconds")


def _load() -> dict:
    try:
        with paths.STATE_FILE.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            return _blank()
        data.setdefault("labs", {})
        data.setdefault("student", "")
        return data
    except (OSError, json.JSONDecodeError):
        return _blank()


def _blank() -> dict:
    return {"student": "", "labs": {}}


def _save(data: dict) -> None:
    paths.ensure_state_dir()
    try:
        tmp = paths.STATE_FILE.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)
        tmp.replace(paths.STATE_FILE)
    except OSError:
        pass  # non-fatal: progress tracking is best-effort


def _lab(data: dict, lab_id: str) -> dict:
    return data["labs"].setdefault(lab_id, {
        "started": None, "verified": {}, "best_score": 0, "max_points": 0,
    })


def set_student(name: str) -> None:
    data = _load()
    data["student"] = name
    _save(data)


def get_student() -> str:
    return _load().get("student", "")


def get_seed() -> int:
    """A stable per-student random seed; created and persisted on first use.
    Drives per-student lab randomization so answers can't be copied."""
    import secrets
    data = _load()
    seed = data.get("seed")
    if not isinstance(seed, int):
        seed = secrets.randbelow(2**31)
        data["seed"] = seed
        _save(data)
    return seed


def mark_started(lab_id: str) -> None:
    data = _load()
    _lab(data, lab_id)["started"] = _now()
    _save(data)


def mark_stopped(lab_id: str) -> None:
    data = _load()
    if lab_id in data["labs"]:
        data["labs"][lab_id]["started"] = None
        _save(data)


def record_result(lab_id: str, results: dict[str, bool], score: int, max_points: int) -> None:
    """results: check_id -> passed. Keeps the best score seen."""
    data = _load()
    entry = _lab(data, lab_id)
    entry["verified"] = {k: bool(v) for k, v in results.items()}
    entry["max_points"] = max_points
    entry["last_attempt"] = _now()
    if score >= entry.get("best_score", 0):
        entry["best_score"] = score
    _save(data)


def lab_status(lab_id: str) -> dict:
    return _load()["labs"].get(lab_id, {})


def record_quiz(quiz_id: str, score: int, total: int) -> None:
    """Persist a quiz/exam result, keeping the best score."""
    data = _load()
    qs = data.setdefault("quizzes", {})
    entry = qs.setdefault(quiz_id, {"best": 0, "total": total})
    entry["total"] = total
    entry["last"] = _now()
    if score >= entry.get("best", 0):
        entry["best"] = score
    _save(data)


def quiz_status(quiz_id: str) -> dict:
    return _load().get("quizzes", {}).get(quiz_id, {})


def certificate_issue(serial: str) -> dict:
    """Record the certificate issue date once, so the verification code is
    stable across re-prints. Returns the stored {serial, issued}."""
    data = _load()
    cert = data.get("certificate")
    if not isinstance(cert, dict) or not cert.get("issued"):
        cert = {"serial": serial, "issued": _dt.date.today().isoformat()}
        data["certificate"] = cert
        _save(data)
    return data["certificate"]


def certificate_status() -> dict:
    c = _load().get("certificate")
    return c if isinstance(c, dict) else {}


def is_complete(lab_id: str, max_points: int) -> bool:
    entry = lab_status(lab_id)
    return max_points > 0 and entry.get("best_score", 0) >= max_points


def all_progress() -> dict:
    return _load()


def clear_progress() -> bool:
    """Wipe this student's progress/state. Returns True if a file was removed."""
    try:
        if paths.STATE_FILE.exists():
            paths.STATE_FILE.unlink()
            return True
    except OSError:
        pass
    return False


def load_file(path) -> dict:
    """Load a state.json from an arbitrary path (for facilitator aggregation)."""
    import json as _json
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = _json.load(fh)
        return data if isinstance(data, dict) else {}
    except (OSError, _json.JSONDecodeError):
        return {}
