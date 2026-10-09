#!/bin/bash
# Script checks for M4:  verify.sh <check_id>   (exit 0 = pass)
# Read-only reachability checks against the lab targets only.
CHECK="$1"

port_open() { timeout 2 bash -c "exec 3<>/dev/tcp/$1/$2" 2>/dev/null && { exec 3>&-; return 0; } || return 1; }

case "$CHECK" in
  web_up)
    if port_open 10.13.4.10 80; then echo "web target serving on :80"; exit 0; fi
    echo "web target down — run: labctl start m4"; exit 1 ;;
  ssh_up)
    if port_open 10.13.4.20 22; then echo "SSH target listening on :22"; exit 0; fi
    echo "SSH target down — run: labctl start m4"; exit 1 ;;
  *) echo "unknown script check: $CHECK"; exit 2 ;;
esac
