#!/bin/bash
# Script-based checks for M3. Called as:  verify.sh <check_id>
# Exit 0 = pass, non-zero = fail. Last stdout line is shown to the student.
#
# These only READ state (reachability of the lab targets). They never attack
# anything and never touch hosts outside the private lab subnet.
CHECK="$1"

targets=(10.13.3.10 10.13.3.20 10.13.3.30 10.13.3.40)

port_open() {  # host port
  timeout 2 bash -c "exec 3<>/dev/tcp/$1/$2" 2>/dev/null && { exec 3>&- ; return 0; } || return 1
}

case "$CHECK" in
  targets_live)
    up=0
    port_open 10.13.3.10 80   && up=$((up+1))
    port_open 10.13.3.20 21   && up=$((up+1))
    port_open 10.13.3.30 22   && up=$((up+1))
    port_open 10.13.3.40 3389 && up=$((up+1))
    echo "$up/4 lab targets reachable"
    [ "$up" -eq 4 ]
    ;;
  *)
    echo "unknown script check: $CHECK"
    exit 2
    ;;
esac
