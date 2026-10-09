#!/usr/bin/env python3
"""Clean-room dry run: for every lab, start it (if it has targets), feed the
model answers to `labctl verify`, record the score, and stop it. Confirms the
whole suite grades 100% from the manifests — a classroom-readiness / regression
check.

  python3 scripts/dry_run.py
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from answer_key import answers_for, load_labs  # noqa: E402

LABCTL = str(ROOT / "labctl")


def run(args, inp=None, timeout=300):
    return subprocess.run([LABCTL, *args], input=inp, capture_output=True,
                          text=True, cwd=str(ROOT), timeout=timeout)


def main() -> int:
    rows = []
    ok_all = True
    for folder, data in load_labs():
        lab = data["lab"]
        lid = lab["id"]
        has_targets = (ROOT / "labs" / folder / "docker-compose.yml").is_file()
        if has_targets:
            r = run(["start", lid], timeout=400)
            if r.returncode != 0:
                rows.append((lid, "START FAIL", r.stderr.strip()[:50])); ok_all = False
                continue
            time.sleep(2)  # settle
        answers = "\n".join(answers_for(data)) + "\n"
        v = run(["verify", lid], inp=answers, timeout=120)
        m = re.search(r"(\d+)/(\d+)\s*\((\d+)%\)", v.stdout)
        if m and m.group(1) == m.group(2):
            rows.append((lid, f"{m.group(1)}/{m.group(2)}", "PASS"))
        else:
            score = m.group(0) if m else "no score"
            rows.append((lid, score, "FAIL")); ok_all = False
        if has_targets:
            run(["stop", lid], timeout=120)
    print("\n=== DRY RUN RESULTS ===")
    for lid, score, status in rows:
        mark = "✔" if status == "PASS" else "✘"
        print(f"  {mark} {lid:4} {score:>8}  {status}")
    print("=======================")
    print("ALL LABS PASS" if ok_all else "SOME LABS FAILED")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
