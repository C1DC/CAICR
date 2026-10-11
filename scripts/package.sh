#!/usr/bin/env bash
# Build a distributable CAIC CyberLab bundle for OFFLINE classroom rollout.
#
# Run this ONCE on a prepped, internet-connected machine (after `labctl prep`):
#   bash scripts/package.sh
#
# It produces, under dist/:
#   caic-lab-images.tar.gz   every lab Docker image incl. the OWASP Juice Shop
#                            arena (so student machines need no internet to run)
#   caic-cyberlab.tar.gz     the project (code, lessons, labs, worksheets, docs)
#   INSTALL-OFFLINE.txt      copy-paste install steps for each student machine
#
# Copy dist/ to a USB stick and carry it to the offline machines.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
DIST="$ROOT/dist"
mkdir -p "$DIST"

# Every image the labs launch, including the RT intrusion target and the
# always-on OWASP Juice Shop web-attack arena. Keep in sync with labs/*/.
IMAGES=(caic-target:1.0 caic-labdns:1.0 caic-m4web:1.0 caic-aisandbox:1.0 \
        caic-rtweb:1.0 bkimminich/juice-shop:v20.2.0)

say() { printf '\n\033[1;35m▶ %s\033[0m\n' "$*"; }
ok()  { printf '  \033[32m✔\033[0m %s\n' "$*"; }
warn(){ printf '  \033[33m!\033[0m %s\n' "$*"; }

say "Checking the lab images are built"
missing=0
for img in "${IMAGES[@]}"; do
  if docker image inspect "$img" >/dev/null 2>&1; then ok "$img"; else warn "MISSING: $img"; missing=1; fi
done
if [ "$missing" = "1" ]; then
  warn "Run './labctl prep' (needs internet) first, then re-run this script."; exit 1
fi

say "Exporting Docker images (this is the big one)"
docker save "${IMAGES[@]}" | gzip > "$DIST/caic-lab-images.tar.gz"
ok "wrote caic-lab-images.tar.gz ($(du -h "$DIST/caic-lab-images.tar.gz" | cut -f1))"

say "Packaging the project"
tar --exclude='./.git' --exclude='./dist' --exclude='*/__pycache__' \
    --exclude='*.pyc' --exclude='*/recovered' --exclude='*/rec' \
    --exclude='*/be_out' --exclude='*.john.pot' \
    -czf "$DIST/caic-cyberlab.tar.gz" -C "$ROOT" .
ok "wrote caic-cyberlab.tar.gz ($(du -h "$DIST/caic-cyberlab.tar.gz" | cut -f1))"

cat > "$DIST/INSTALL-OFFLINE.txt" <<'TXT'
CAIC CyberLab — offline install (per student machine)
=====================================================
Requirements on the machine: Kali/Debian Linux, Docker, Python 3.11+.
(If Docker is absent and you also have no internet, install it from your
offline Debian package mirror first.)

1. Copy both tarballs from the USB to the machine, e.g. into ~/ :
       cp /media/usb/caic-cyberlab.tar.gz  ~/
       cp /media/usb/caic-lab-images.tar.gz ~/

2. Unpack the project:
       mkdir -p ~/CAIC_lab && tar -xzf ~/caic-cyberlab.tar.gz -C ~/CAIC_lab

3. Load the pre-built lab images into Docker (no internet needed):
       docker load -i ~/caic-lab-images.tar.gz

4. Verify and go:
       cd ~/CAIC_lab
       ./labctl doctor        # expect green ticks
       ./start.sh             # opens the app; or ./labctl list

Notes
- If Docker needs root: add the user to the 'docker' group
  (sudo usermod -aG docker $USER; then log out/in) or run labctl with sudo.
- Everything runs locally and offline. Lab targets live on 10.13.x.x and never
  touch the real network.
TXT
ok "wrote INSTALL-OFFLINE.txt"

say "Bundle ready in dist/"
ls -lh "$DIST"
ok "Carry dist/ to the offline machines. See OFFLINE_ROLLOUT.md for the full checklist."
