#!/bin/bash
# Script checks for the Red Team Primer lab. Called as: verify.sh <check_id>
# Exit 0 = pass. Read-only reachability checks against the private lab target.
CHECK="$1"

port_open() {  # host port
  timeout 3 bash -c "exec 3<>/dev/tcp/$1/$2" 2>/dev/null && { exec 3>&- ; return 0; } || return 1
}

case "$CHECK" in
  target_up)
    up=0
    port_open 10.13.2.10 80 && up=$((up+1))
    port_open 10.13.2.10 22 && up=$((up+1))
    echo "$up/2 services (web + ssh) reachable on 10.13.2.10"
    [ "$up" -eq 2 ]
    ;;
  *)
    echo "unknown script check: $CHECK"; exit 2 ;;
esac
