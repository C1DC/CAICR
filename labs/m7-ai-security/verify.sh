#!/bin/bash
# Script checks for M7:  verify.sh <check_id>   (exit 0 = pass)
CHECK="$1"
case "$CHECK" in
  sandbox_up)
    if curl -sf -m 3 http://10.13.7.10:8080/ >/dev/null 2>&1; then
      echo "AI sandbox responding on :8080"; exit 0
    fi
    echo "sandbox down — run: labctl start m7"; exit 1 ;;
  *) echo "unknown script check: $CHECK"; exit 2 ;;
esac
