# Shared CAIC CyberLab target image.
# One small Alpine image that can impersonate several "enterprise" hosts
# (web admin, unencrypted FTP, SSH, legacy RDP) selected at runtime via
# the SERVICE env var. Built ONCE per student machine, reused by every lab.
#
# These targets are intentionally exposed/misconfigured FOR TRAINING and are
# confined to a private Docker subnet. They are never reachable off-host.
FROM alpine:3.20

RUN apk add --no-cache \
        openssh \
        vsftpd \
        darkhttpd \
        bash \
    && ssh-keygen -A \
    # a deliberately weak lab account — demonstrates why creds/MFA matter
    && adduser -D -s /bin/ash labuser \
    && echo 'labuser:Password123' | chpasswd \
    && mkdir -p /var/ftp/pub \
    && echo 'Internal file drop — Q3 supplier invoices' > /var/ftp/pub/README.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
