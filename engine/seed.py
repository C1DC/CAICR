"""Per-student lab randomization.

Each student gets a stable random seed (stored in their state). A lab's optional
[randomize] block declares variables; this module turns (seed, lab, spec) into
deterministic per-student values, so no two students share the same flag, hidden
host, C2 domain, mule account, etc. — which makes the labs usable for real,
copy-proof assessment and reusable across cohorts.

Values flow two ways at `labctl start`:
  * host-side: assets/*.tmpl are rendered to their stripped names, substituting
    __VARNAME__ tokens;
  * container-side: values are passed as CAIC_<VARNAME> env vars that the
    compose files forward into services, whose entrypoints render from them.

At grade time, check `answer`/`accept` values containing {{varname}} are resolved
against the same deterministic values.
"""
from __future__ import annotations

import dataclasses
import random
import re
import string

from . import state

_TOKEN = re.compile(r"\{\{(\w+)\}\}")

_HOSTNAMES = ["vpn-admin", "backup-01", "jenkins", "db-replica", "fileshare",
              "ad-backup", "gitlab", "monitoring", "staging-web", "print-srv",
              "mail-relay", "sap-test", "citrix", "pbx"]


def _rng(lab_id: str) -> random.Random:
    return random.Random(f"{state.get_seed()}::{lab_id}")


def _one(rng: random.Random, spec: dict):
    kind = spec.get("kind", "choice")
    if kind == "flag":
        body = "".join(rng.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        return "FLAG{" + str(spec.get("prefix", "")) + body + "}"
    if kind == "choice":
        return str(rng.choice(spec["choices"]))
    if kind == "hostname":
        return rng.choice(spec.get("choices", _HOSTNAMES))
    if kind == "ip_private":
        return f"10.{rng.randint(20, 99)}.{rng.randint(0, 250)}.{rng.randint(2, 250)}"
    if kind == "ip_public":
        return (f"{rng.choice([41, 45, 102, 154, 196, 197])}."
                f"{rng.randint(1, 250)}.{rng.randint(1, 250)}.{rng.randint(2, 250)}")
    if kind == "int_range":
        return str(rng.randint(int(spec["min"]), int(spec["max"])))
    if kind == "digits":
        n = int(spec.get("length", 10))
        return "".join(rng.choice(string.digits) for _ in range(n))
    if kind == "password":
        words = spec.get("choices", ["Falcon", "Harmattan", "Volta", "Ashanti", "Kente", "Baobab"])
        return f"{rng.choice(words)}{rng.randint(10, 99)}!"
    return str(spec.get("default", ""))


def compute(lab) -> dict:
    """Deterministic {var: value} for this student + lab (empty if not randomized).
    Two passes: primitives first, then derived values (md5/sha256 of another var)."""
    import hashlib
    spec = getattr(lab, "randomize", None) or {}
    if not spec:
        return {}
    rng = _rng(lab.id)
    vals, derived = {}, []
    for var in sorted(spec):
        if spec[var].get("kind") in ("md5", "sha256"):
            derived.append(var)
        else:
            vals[var] = _one(rng, spec[var])
    for var in derived:
        s = spec[var]
        src = str(vals.get(s.get("of", ""), ""))
        algo = hashlib.md5 if s["kind"] == "md5" else hashlib.sha256
        vals[var] = algo(src.encode()).hexdigest()
    return vals


def resolve(text, vals: dict):
    if not isinstance(text, str) or not vals:
        return text
    return _TOKEN.sub(lambda m: str(vals.get(m.group(1), m.group(0))), text)


def resolved_check(check, vals: dict):
    """Return a copy of a Check with {{...}} resolved in answer/accept."""
    if not vals:
        return check
    return dataclasses.replace(
        check,
        answer=resolve(check.answer, vals),
        accept=[resolve(a, vals) for a in check.accept],
    )


def env_for(vals: dict) -> dict:
    """CAIC_<VAR> environment variables for docker compose substitution."""
    return {f"CAIC_{k.upper()}": str(v) for k, v in vals.items()}


def run_generators(lab, vals: dict) -> None:
    """Run the lab's declared generator scripts (for binary assets like PCAPs)
    with the per-student values in the environment as CAIC_<VAR>."""
    import os
    import subprocess
    import sys
    scripts = getattr(lab, "generators", None) or []
    if not scripts:
        return
    env = os.environ.copy()
    env.update(env_for(vals))
    for rel in scripts:
        script = lab.directory / rel
        if script.is_file():
            subprocess.run([sys.executable, str(script)], cwd=str(lab.directory),
                           env=env, capture_output=True, text=True)


def prepare(lab, vals: dict) -> None:
    """Everything to personalise a lab's on-disk assets before launch."""
    render_assets(lab, vals)
    run_generators(lab, vals)


def render_assets(lab, vals: dict) -> None:
    """Render assets/*.tmpl -> stripped name, substituting __VAR__ tokens."""
    if not vals:
        return
    adir = lab.directory / "assets"
    if not adir.is_dir():
        return
    for tmpl in adir.rglob("*.tmpl"):
        text = tmpl.read_text(encoding="utf-8")
        for k, v in vals.items():
            text = text.replace(f"__{k.upper()}__", str(v))
        tmpl.with_suffix("").write_text(text, encoding="utf-8")
