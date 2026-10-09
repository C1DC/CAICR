"""Load and validate lab manifests (lab.toml). Zero-dependency: uses tomllib."""
from __future__ import annotations

import ipaddress
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from . import paths


class ManifestError(Exception):
    """Raised when a lab.toml is missing required fields or is malformed."""


@dataclass
class Target:
    name: str
    ip: str
    role: str = ""


@dataclass
class Check:
    id: str
    prompt: str
    type: str           # 'numeric' | 'string' | 'string_any' | 'script'
    answer: object = None       # expected value (not used for 'script')
    hint: str = ""
    points: int = 1
    tolerance: int = 0          # numeric: allowed +/- deviation
    accept: list[str] = field(default_factory=list)  # string_any: accepted values


@dataclass
class Lab:
    id: str
    module: str
    title: str
    day: int
    tools: list[str]
    objective: str
    estimated_minutes: int
    network_name: str
    subnet: str
    directory: Path
    compose_file: Path
    briefing_file: Path | None
    verify_script: Path | None
    targets: list[Target]
    checks: list[Check]
    ready: list[str]   # "ip:port" endpoints to probe before a lab is "ready"
    randomize: dict    # per-student randomization spec (empty = static lab)
    generators: list   # scripts to run at start (binary assets), with CAIC_* env

    @property
    def project(self) -> str:
        """docker compose project name — namespaced so labs never collide."""
        return f"caic_{self.id}".lower()

    @property
    def max_points(self) -> int:
        return sum(c.points for c in self.checks)

    @property
    def has_targets(self) -> bool:
        """File-based labs (forensics, email) ship evidence but launch no
        containers. They have no docker-compose.yml."""
        return self.compose_file.is_file()


def _require(d: dict, key: str, where: str):
    if key not in d:
        raise ManifestError(f"{where}: missing required key '{key}'")
    return d[key]


def load_lab(directory: Path) -> Lab:
    toml_path = directory / "lab.toml"
    if not toml_path.is_file():
        raise ManifestError(f"{directory.name}: no lab.toml found")
    try:
        with toml_path.open("rb") as fh:
            data = tomllib.load(fh)
    except tomllib.TOMLDecodeError as exc:
        raise ManifestError(f"{directory.name}/lab.toml: {exc}") from exc

    lab = _require(data, "lab", directory.name)
    net = data.get("network", {})

    subnet = net.get("subnet", "")
    if subnet:
        _validate_isolated_subnet(subnet, directory.name)

    compose = directory / data.get("compose", "docker-compose.yml")
    briefing = directory / lab.get("briefing", "briefing.md")
    verify_sh = directory / "verify.sh"

    targets = [
        Target(name=_require(t, "name", f"{directory.name}:target"),
               ip=t.get("ip", ""), role=t.get("role", ""))
        for t in data.get("targets", [])
    ]

    checks = []
    for c in data.get("check", []):
        cid = _require(c, "id", f"{directory.name}:check")
        ctype = c.get("type", "string")
        if ctype not in ("numeric", "string", "string_any", "script"):
            raise ManifestError(f"{directory.name}: check '{cid}' has unknown type '{ctype}'")
        checks.append(Check(
            id=cid,
            prompt=_require(c, "prompt", f"{directory.name}:check:{cid}"),
            type=ctype,
            answer=c.get("answer"),
            hint=c.get("hint", ""),
            points=int(c.get("points", 1)),
            tolerance=int(c.get("tolerance", 0)),
            accept=[str(x) for x in c.get("accept", [])],
        ))

    return Lab(
        id=str(_require(lab, "id", directory.name)).lower(),
        module=str(lab.get("module", lab.get("id", "?")).upper()),
        title=str(_require(lab, "title", directory.name)),
        day=int(lab.get("day", 0)),
        tools=[str(x) for x in lab.get("tools", [])],
        objective=str(lab.get("objective", "")),
        estimated_minutes=int(lab.get("estimated_minutes", 0)),
        network_name=str(net.get("name", f"caic_{lab.get('id','x')}")),
        subnet=subnet,
        directory=directory,
        compose_file=compose,
        briefing_file=briefing if briefing.is_file() else None,
        verify_script=verify_sh if verify_sh.is_file() else None,
        targets=targets,
        checks=checks,
        ready=[str(x) for x in net.get("ready", [])],
        randomize=data.get("randomize", {}) or {},
        generators=[str(x) for x in (data.get("generators") or lab.get("generators", []))],
    )


def _validate_isolated_subnet(subnet: str, where: str) -> None:
    """Safety guardrail: lab subnets MUST be private (RFC1918). This is what
    structurally keeps the CyberRange off the real network."""
    try:
        net = ipaddress.ip_network(subnet, strict=False)
    except ValueError as exc:
        raise ManifestError(f"{where}: invalid subnet '{subnet}': {exc}") from exc
    if not net.is_private:
        raise ManifestError(
            f"{where}: subnet '{subnet}' is NOT private — labs must stay on "
            f"RFC1918 space (10/8, 172.16/12, 192.168/16). Refusing to load."
        )


def discover_labs() -> list[Lab]:
    """Load every valid lab under labs/, sorted by day then id."""
    found: list[Lab] = []
    if not paths.LABS_DIR.is_dir():
        return found
    for d in sorted(paths.LABS_DIR.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        if not (d / "lab.toml").is_file():
            continue
        found.append(load_lab(d))
    found.sort(key=lambda l: (l.day, l.id))
    return found


def load_one(lab_id: str) -> Lab:
    d = paths.lab_dir(lab_id)
    if d is None:
        raise ManifestError(f"no lab named '{lab_id}' (try: labctl list)")
    return load_lab(d)
