# Operation First Blood — the vulnerable internal server for the Red Team Primer.
# One Alpine box exposing web (:80) + SSH (:22), with a deliberately leaked
# credential and a sudo misconfiguration, so students can run a full intrusion
# chain (recon -> loot -> foothold -> privilege escalation) end to end.
#
# Intentionally vulnerable FOR TRAINING. Confined to a private Docker subnet;
# never reachable off-host. Per-student secrets come from CAIC_* env at runtime.
FROM alpine:3.20

RUN apk add --no-cache openssh darkhttpd bash sudo \
    && ssh-keygen -A \
    && adduser -D -s /bin/ash webadmin

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
