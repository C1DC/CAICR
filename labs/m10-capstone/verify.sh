#!/bin/bash
# Script checks for M10:  verify.sh <check_id>   (exit 0 = pass)
CHECK="$1"
port_open() { timeout 2 bash -c "exec 3<>/dev/tcp/$1/$2" 2>/dev/null && { exec 3>&-; return 0; } || return 1; }

case "$CHECK" in
  range_up)
    up=0
    port_open 10.13.10.10 80   && up=$((up+1))
    port_open 10.13.10.20 22   && up=$((up+1))
    port_open 10.13.10.40 8080 && up=$((up+1))
    echo "$up/3 capstone services reachable"
    [ "$up" -eq 3 ]
    ;;
  *) echo "unknown script check: $CHECK"; exit 2 ;;
esac
