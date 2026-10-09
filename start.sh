#!/usr/bin/env bash
# CAIC CyberLab — start the whole project with one command.
#
#   ./start.sh            check the backend, serve the frontend, open the browser
#   ./start.sh m3         ...and also bring up lab m3's targets
#   ./start.sh --prep     ...and pre-build all lab images first (needs internet)
#
# Frontend = the browser pages (index / lessons / courseware), served locally.
# Backend  = the lab engine (labctl) + its Docker targets, brought up per lab.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PORT="${CAIC_PORT:-8899}"
HOSTB="127.0.0.1"

k="\033[38;5;135m"; g="\033[32m"; y="\033[33m"; d="\033[90m"; b="\033[1m"; r="\033[0m"
say(){ printf "\n${k}${b}▶ %s${r}\n" "$*"; }
ok(){ printf "  ${g}✔${r} %s\n" "$*"; }
info(){ printf "  ${d}%s${r}\n" "$*"; }

LAB=""; DO_PREP=0
for a in "$@"; do
  case "$a" in
    --prep) DO_PREP=1 ;;
    m[0-9]*) LAB="$a" ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) printf "${y}ignoring unknown argument: %s${r}\n" "$a" ;;
  esac
done

printf "${k}${b}"
cat <<'BANNER'
  ╔══════════════════════════════════════════╗
  ║   KAIPTC · CAIC CyberLab — starting up     ║
  ╚══════════════════════════════════════════╝
BANNER
printf "${r}"

# 1. Backend readiness ------------------------------------------------------
say "Checking the backend (lab engine + Docker)"
if ! command -v python3 >/dev/null 2>&1; then
  printf "${y}Python 3 is required but not found.${r}\n"; exit 1
fi
./labctl doctor || info "Some checks failed — browser content still works; labs need Docker."

if [ "$DO_PREP" = "1" ]; then
  say "Pre-building lab images (one-time, needs internet)"
  ./labctl prep || info "prep hit an issue — you can retry later with ./labctl prep"
fi

# 2. Optional: bring up a lab ----------------------------------------------
if [ -n "$LAB" ]; then
  say "Starting lab $LAB"
  ./labctl start "$LAB" || info "could not start $LAB (is Docker running?)"
fi

# 3. Frontend: local web server --------------------------------------------
say "Serving the frontend"
# find a free port starting at $PORT
for try in $(seq 0 9); do
  CAND=$((PORT + try))
  if ! { exec 3<>"/dev/tcp/$HOSTB/$CAND"; } 2>/dev/null; then PORT=$CAND; break; fi
  exec 3>&- 2>/dev/null || true
done

python3 -m http.server "$PORT" --bind "$HOSTB" --directory "$ROOT" >/dev/null 2>&1 &
SERVER_PID=$!

cleanup(){
  printf "\n"; say "Shutting down"
  kill "$SERVER_PID" 2>/dev/null && ok "web server stopped"
  if [ -n "$LAB" ]; then
    ./labctl stop "$LAB" >/dev/null 2>&1 && ok "lab $LAB stopped"
  fi
  info "Docker targets for other labs (if any) keep running — ./labctl stop to end them."
  exit 0
}
trap cleanup INT TERM

# wait until it actually answers (no sleep; poll)
URL="http://$HOSTB:$PORT/index.html"
UP=0
for i in $(seq 1 50); do
  if curl -sf -o /dev/null "$URL" 2>/dev/null; then UP=1; break; fi
  curl -s -o /dev/null "$URL" 2>/dev/null || true   # tiny delay via curl connect attempt
done
[ "$UP" = "1" ] && ok "web server up on port $PORT" || info "server may still be starting"

# 4. Open the browser -------------------------------------------------------
if [ -n "${DISPLAY:-}${WAYLAND_DISPLAY:-}" ]; then
  for opener in xdg-open sensible-browser firefox; do
    if command -v "$opener" >/dev/null 2>&1; then "$opener" "$URL" >/dev/null 2>&1 & break; fi
  done
  ok "opened your browser"
else
  info "no graphical display detected — open the URL below in a browser"
fi

# 5. Summary + keep running -------------------------------------------------
say "CAIC CyberLab is running"
printf "  ${b}Frontend:${r}  %s\n" "$URL"
printf "  ${b}Labs:${r}      ${g}./labctl learn${r}   then   ${g}./labctl start m3${r}\n"
printf "  ${d}Press Ctrl-C to stop the web server.${r}\n\n"

wait "$SERVER_PID"
