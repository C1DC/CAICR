#!/bin/bash
# Script checks for this lab:  verify.sh <check_id>   (exit 0 = pass)
CHECK="$1"
case "$CHECK" in
  example_script)
    echo "describe what passed/failed"
    true
    ;;
  *) echo "unknown script check: $CHECK"; exit 2 ;;
esac
