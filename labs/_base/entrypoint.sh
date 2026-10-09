#!/bin/bash
# Start the service named by $SERVICE in the foreground so the container stays
# up. Each lab target container sets SERVICE to one of: web ftp ssh rdp.
set -e
SERVICE="${SERVICE:-web}"
HOSTLABEL="${HOSTLABEL:-target}"

log() { echo "[$HOSTLABEL/$SERVICE] $*"; }

case "$SERVICE" in
  web)
    # Unauthenticated "admin panel" — a classic finding for nmap http-title.
    mkdir -p /www
    cat > /www/index.html <<HTML
<!doctype html><html><head><title>${WEB_TITLE:-Acme Payroll Admin Console}</title></head>
<body><h1>${WEB_TITLE:-Acme Payroll Admin Console}</h1>
<p>Status: ONLINE. No authentication configured.</p>
<p>Build 2.1.4 — contact ict@lab-corp.local</p></body></html>
HTML
    log "serving admin panel on :80"
    exec darkhttpd /www --port 80 --index index.html
    ;;

  ftp)
    # Anonymous, unencrypted FTP — cleartext, no TLS.
    cat > /etc/vsftpd/vsftpd.conf <<CONF
listen=YES
anonymous_enable=YES
local_enable=YES
write_enable=NO
anon_root=/var/ftp
dirmessage_enable=YES
xferlog_enable=YES
seccomp_sandbox=NO
ftpd_banner=lab-corp FTP (vsftpd) — anonymous access permitted
CONF
    log "serving anonymous FTP on :21"
    exec vsftpd /etc/vsftpd/vsftpd.conf
    ;;

  ssh)
    log "serving SSH on :22 (lab account labuser:Password123)"
    exec /usr/sbin/sshd -D -e
    ;;

  rdp)
    # No real RDP server in Alpine; present an open 3389 with a banner so the
    # port shows up in discovery as an exposed remote-access service.
    log "presenting legacy remote-access port :3389"
    while true; do
      echo -e "RDP-Service\r" | busybox nc -l -p 3389 >/dev/null 2>&1 || sleep 1
    done
    ;;

  *)
    log "unknown SERVICE '$SERVICE'"; exit 1 ;;
esac
