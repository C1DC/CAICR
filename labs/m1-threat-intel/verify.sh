#!/bin/bash
# Script checks for M1:  verify.sh <check_id>   (exit 0 = pass)
# Read-only DNS lookups against the lab resolver only.
CHECK="$1"
DNS=10.13.1.10

case "$CHECK" in
  dns_up)
    ans=$(dig +short @"$DNS" lab-corp.com.gh A 2>/dev/null | head -1)
    if [ "$ans" = "41.210.15.20" ]; then
      echo "lab DNS responding (lab-corp.com.gh -> $ans)"
      exit 0
    fi
    echo "lab DNS not answering — run: labctl start m1"
    exit 1
    ;;
  *) echo "unknown script check: $CHECK"; exit 2 ;;
esac
