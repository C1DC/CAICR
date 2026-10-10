"""Filesystem locations. The engine is relocatable: everything is resolved
relative to the package, and per-student state lives under the user's home."""
from __future__ import annotations

import os
from pathlib import Path

# <root>/engine/paths.py  ->  ROOT = <root>
ROOT = Path(__file__).resolve().parent.parent
LABS_DIR = ROOT / "labs"
LESSONS_DIR = ROOT / "lessons"
WORKSHEETS_DIR = ROOT / "worksheets"
REFERENCE_DIR = ROOT / "reference"
ASSESSMENT_FILE = ROOT / "assessment" / "exams.toml"

# Per-student mutable state and work, kept out of the (possibly read-only,
# shared) install tree.
_XDG = os.environ.get("XDG_DATA_HOME")
STATE_DIR = Path(_XDG) / "caic-lab" if _XDG else Path.home() / ".local" / "share" / "caic-lab"
STATE_FILE = STATE_DIR / "state.json"

# Where a student's own filled-in worksheet copies go.
WORK_DIR = (STATE_DIR / "coursework" if _XDG else Path.home() / "caic-coursework")


def ensure_state_dir() -> None:
    try:
        STATE_DIR.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass


def lab_dir(lab_id: str) -> Path | None:
    """Return the directory for a lab id (e.g. 'm3'), matching a 'm3-*' folder."""
    if not LABS_DIR.is_dir():
        return None
    for d in sorted(LABS_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        # match 'm3' against 'm3-network'
        stem = d.name.split("-", 1)[0]
        if stem.lower() == lab_id.lower():
            return d
    return None
