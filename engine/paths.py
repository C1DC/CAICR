"""Filesystem locations. The engine is relocatable: everything is resolved
relative to the package, and per-student state lives under the user's home."""
from __future__ import annotations

import os
from pathlib import Path

# <root>/engine/paths.py  ->  ROOT = <root>
ROOT = Path(__file__).resolve().parent.parent
LABS_DIR = ROOT / "labs"

# Per-student mutable state (progress, which labs are running).
# Kept out of the (possibly read-only, root-owned) install tree.
_XDG = os.environ.get("XDG_DATA_HOME")
STATE_DIR = Path(_XDG) / "caic-lab" if _XDG else Path.home() / ".local" / "share" / "caic-lab"
STATE_FILE = STATE_DIR / "state.json"


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
