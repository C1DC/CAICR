#!/usr/bin/env bash
# One-time CAIC CyberLab setup for a student Kali machine.
# Installs Docker if missing, enables the service, puts the user in the docker
# group, then pre-builds every lab image so later launches work offline.
#
# Run from the lab root:   bash scripts/setup.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

say() { printf '\n\033[1;35m▶ %s\033[0m\n' "$*"; }
ok()  { printf '  \033[32m✔\033[0m %s\n' "$*"; }
warn(){ printf '  \033[33m!\033[0m %s\n' "$*"; }

say "CAIC CyberLab setup"

# 1. Docker
if ! command -v docker >/dev/null 2>&1; then
  say "Installing Docker (needs internet + sudo)"
  sudo apt-get update
  sudo apt-get install -y docker.io docker-compose-v2
  ok "Docker installed"
else
  ok "Docker already present: $(docker --version)"
fi

# 2. Service
if ! sudo systemctl is-active --quiet docker 2>/dev/null; then
  sudo systemctl enable --now docker || warn "could not start docker via systemctl"
fi
ok "Docker service running"

# 3. docker group
if ! id -nG "$USER" | tr ' ' '\n' | grep -qx docker; then
  say "Adding $USER to the docker group"
  sudo usermod -aG docker "$USER"
  warn "Log out and back in (or run: newgrp docker) for this to take effect."
  warn "Until then, prefix labctl with sudo."
else
  ok "$USER is in the docker group"
fi

# 4. Python check (needs 3.11+ for tomllib)
if python3 -c 'import sys,tomllib; assert sys.version_info>=(3,11)' 2>/dev/null; then
  ok "Python $(python3 -V | awk '{print $2}') OK"
else
  warn "Python 3.11+ with tomllib is required for labctl."
fi

# 5. Pre-build all lab images for offline use
say "Pre-building lab images (needs internet this one time)"
if docker info >/dev/null 2>&1; then
  ./labctl prep
else
  warn "Can't reach the Docker daemon as this user yet."
  warn "After re-login, run:  ./labctl prep"
fi

say "Setup complete"
ok "Students: read STUDENT_GUIDE.md, then run  ./labctl list"
