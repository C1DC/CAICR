"""Thin wrapper around `docker compose` for a single lab. stdlib only."""
from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass

from .manifest import Lab


class DockerError(Exception):
    pass


@dataclass
class Preflight:
    docker_installed: bool
    daemon_up: bool
    compose_v2: bool
    needs_sudo: bool
    detail: str = ""

    @property
    def ok(self) -> bool:
        return self.docker_installed and self.daemon_up and self.compose_v2


def preflight() -> Preflight:
    if shutil.which("docker") is None:
        return Preflight(False, False, False, False, "docker binary not found on PATH")
    # daemon reachable as current user?
    r = subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"],
                       capture_output=True, text=True)
    daemon_up = r.returncode == 0
    needs_sudo = False
    detail = ""
    if not daemon_up:
        err = (r.stderr or "").lower()
        if "permission denied" in err or "dial unix" in err:
            needs_sudo = True
            detail = "cannot talk to docker daemon as this user"
        else:
            detail = (r.stderr or "docker daemon not reachable").strip().splitlines()[-1] if r.stderr else "daemon down"
    # compose v2?
    rc = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True)
    compose_v2 = rc.returncode == 0
    return Preflight(True, daemon_up, compose_v2, needs_sudo, detail)


def _compose(lab: Lab, *args: str, capture: bool = False,
             env: dict | None = None) -> subprocess.CompletedProcess:
    import os
    cmd = [
        "docker", "compose",
        "-p", lab.project,
        "-f", str(lab.compose_file),
        *args,
    ]
    runenv = None
    if env:
        runenv = os.environ.copy()
        runenv.update(env)
    return subprocess.run(cmd, capture_output=capture, text=True,
                          cwd=str(lab.directory), env=runenv)


def build(lab: Lab) -> None:
    """Build this lab's images (pulling base layers). Used by `labctl prep`."""
    r = _compose(lab, "build")
    if r.returncode != 0:
        raise DockerError(f"compose build failed for {lab.id} (exit {r.returncode})")


def up(lab: Lab, env: dict | None = None) -> None:
    r = _compose(lab, "up", "-d", "--remove-orphans", capture=True, env=env)
    if r.returncode != 0:
        err = (r.stderr or "").strip()
        if "overlaps" in err.lower() or "pool" in err.lower():
            raise DockerError(
                f"subnet {lab.subnet} collides with an existing Docker network. "
                f"Edit [network] subnet in {lab.directory.name}/lab.toml to a free "
                f"10.13.x.0/24, then retry.")
        last = err.splitlines()[-1] if err else f"exit {r.returncode}"
        raise DockerError(f"compose up failed for {lab.id}: {last}")


def wait_ready(lab: Lab, timeout: float = 30.0) -> tuple[bool, list[str]]:
    """Poll the lab's declared ready endpoints (ip:port) until all accept TCP
    connections or timeout. Returns (all_ready, still_down)."""
    import socket
    import time
    endpoints = [e for e in lab.ready if ":" in e]
    if not endpoints:
        return True, []
    deadline = time.monotonic() + timeout
    down = list(endpoints)
    while time.monotonic() < deadline and down:
        still = []
        for ep in down:
            host, _, port = ep.rpartition(":")
            try:
                with socket.create_connection((host, int(port)), timeout=1.5):
                    pass
            except OSError:
                still.append(ep)
        down = still
        if down:
            time.sleep(1.0)
    return (not down), down


def down(lab: Lab, destroy_volumes: bool = False) -> None:
    args = ["down", "--remove-orphans"]
    if destroy_volumes:
        args.append("-v")
    r = _compose(lab, *args)
    if r.returncode != 0:
        raise DockerError(f"compose down failed for {lab.id} (exit {r.returncode})")


def restart(lab: Lab) -> None:
    """Hard reset: tear down (incl. volumes) and bring up clean."""
    down(lab, destroy_volumes=True)
    up(lab)


def is_running(lab: Lab) -> bool:
    return len(running_services(lab)) > 0


def running_services(lab: Lab) -> list[dict]:
    """Return list of running compose services as dicts (name, state, ...)."""
    r = _compose(lab, "ps", "--format", "json", capture=True)
    if r.returncode != 0 or not r.stdout.strip():
        return []
    out = []
    for line in r.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        # compose may emit a single JSON array instead of one-per-line
        if isinstance(obj, list):
            out.extend(obj)
        else:
            out.append(obj)
    return [s for s in out if str(s.get("State", "")).lower() in ("running", "up")]
