#!/bin/bash
# Script checks for M6:  verify.sh <check_id>   (exit 0 = pass)
# Read-only — confirms the evidence is intact (chain of custody).
CHECK="$1"
HERE="$(cd "$(dirname "$0")" && pwd)"

case "$CHECK" in
  integrity)
    cd "$HERE/assets" || { echo "assets/ missing"; exit 2; }
    if sha256sum -c evidence.sha256 >/dev/null 2>&1; then
      echo "evidence.img matches the recorded hash — integrity intact"
      exit 0
    fi
    echo "HASH MISMATCH — evidence may be altered"
    exit 1
    ;;
  *)
    echo "unknown script check: $CHECK"; exit 2 ;;
esac
