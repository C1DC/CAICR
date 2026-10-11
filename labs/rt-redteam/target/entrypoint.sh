#!/bin/bash
# Personalise this student's target from the lab engine's env, then start
# SSH (background) and the web server (foreground, keeps the container up).
set -e
: "${CAIC_SSH_PASS:=Spring2024!}"
: "${CAIC_USER_FLAG:=FLAG{user_demo}}"
: "${CAIC_ROOT_FLAG:=FLAG{root_demo}}"
U=webadmin

# the leaked, legitimate credential (randomised per student)
echo "$U:$CAIC_SSH_PASS" | chpasswd

# user flag in webadmin's home
printf '%s\n' "$CAIC_USER_FLAG" > /home/$U/user.txt
chown "$U:$U" /home/$U/user.txt
chmod 600 /home/$U/user.txt
# a friendly nudge on login
printf '\nWell done — you have a foothold. The flag is in user.txt.\nNow try: sudo -l\n\n' > /home/$U/.profile
chown "$U:$U" /home/$U/.profile

# root flag, root-only
printf '%s\n' "$CAIC_ROOT_FLAG" > /root/root.txt
chmod 600 /root/root.txt

# the privilege-escalation misconfiguration: webadmin may run a root shell
# with no password (a very common real-world sudo mistake)
echo "$U ALL=(root) NOPASSWD: /bin/ash" > /etc/sudoers.d/webadmin
chmod 440 /etc/sudoers.d/webadmin

# web content — including the ops note the admin left in the web root
mkdir -p /www/backup
cat > /www/index.html <<'HTML'
<!doctype html><html><head><title>Volta Internal Portal</title></head>
<body style="font-family:sans-serif">
<h1>Volta Internal Portal</h1>
<p>Authorised staff only · build 1.3</p>
<!-- TODO: move the ops backup folder out of the web root before go-live -->
</body></html>
HTML
cat > /www/robots.txt <<'ROBOTS'
User-agent: *
Disallow: /backup/
ROBOTS
cat > /www/backup/notes.txt <<NOTES
Volta IT — ops handover notes (INTERNAL, DO NOT PUBLISH)
--------------------------------------------------------
Host:     this server (intranet)
SSH user: $U
SSH pass: $CAIC_SSH_PASS

Reminder: rotate this password and move these notes off the web root
before go-live. (We never did.)
NOTES

echo "[intranet] SSH on :22 (user $U) and web on :80 starting"
/usr/sbin/sshd -e
exec darkhttpd /www --port 80 --index index.html
