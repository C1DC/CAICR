#!/usr/bin/env bash
# CAIC CyberLab — start the whole project with one command.
#
#   ./start.sh            launch the web application (dashboard, course, labs…)
#   ./start.sh m3         ...and also bring up lab m3's targets first
#   ./start.sh --prep     ...and pre-build all lab images first (needs internet)
#   ./start.sh --no-browser   don't auto-open a browser
#
# The web app is the single place students do everything; it also exposes an
# API that launches and grades the labs. Backend = the lab engine + Docker.
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PORT="${CAIC_PORT:-8899}"

LAB=""; PREP=0; NOBROWSER=""
for a in "$@"; do
  case "$a" in
    --prep) PREP=1 ;;
    --no-browser) NOBROWSER="--no-browser" ;;
    m[0-9]*|rt) LAB="$a" ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) printf "\033[33mignoring unknown argument: %s\033[0m\n" "$a" ;;
  esac
done

printf "\033[38;5;135m\033[1m"
cat <<'BANNER'
  ╔════════════════════════════════════════════╗
  ║   KAIPTC · CAIC CyberLab — starting up       ║
  ╚════════════════════════════════════════════╝
BANNER
printf "\033[0m"

if ! command -v python3 >/dev/null 2>&1; then
  printf "\033[33mPython 3 is required but not found.\033[0m\n"; exit 1
fi

if [ "$PREP" = "1" ]; then
  printf "\n\033[1mPre-building lab images (needs internet, one-time)…\033[0m\n"
  ./labctl prep || true
fi
if [ -n "$LAB" ]; then
  printf "\n\033[1mStarting lab %s…\033[0m\n" "$LAB"
  ./labctl start "$LAB" || true
fi

# Hand off to the web application (serves the UI + API, opens the browser,
# and stops cleanly on Ctrl-C).
exec ./labctl serve --port "$PORT" $NOBROWSER
