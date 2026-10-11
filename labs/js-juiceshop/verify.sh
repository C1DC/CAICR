#!/bin/bash
# Script checks for the Web Attack Arena (OWASP Juice Shop). verify.sh <check_id>
# Exit 0 = pass. Read-only reachability check against the private lab target.
CHECK="$1"

port_open() {  # host port
  timeout 3 bash -c "exec 3<>/dev/tcp/$1/$2" 2>/dev/null && { exec 3>&- ; return 0; } || return 1
}

case "$CHECK" in
  target_up)
    if port_open 10.13.8.10 3000; then
      echo "Juice Shop reachable on http://10.13.8.10:3000"
      exit 0
    fi
    echo "10.13.8.10:3000 is not reachable — is the arena up?  (labctl start js)"
    exit 1
    ;;
  *)
    echo "unknown script check: $CHECK"; exit 2 ;;
esac
