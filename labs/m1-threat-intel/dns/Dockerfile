# Authoritative DNS for the M1 recon lab — real BIND9, the industry-standard
# server students meet in the field. The zone is deliberately misconfigured with
# `allow-transfer { any; }`, so a zone transfer (AXFR) leaks the whole zone —
# including a hidden internal host not published anywhere else. It also omits
# DMARC and CAA on purpose. Training target only.
FROM debian:12-slim
RUN apt-get update && apt-get install -y --no-install-recommends bind9 bind9-utils dnsutils \
    && rm -rf /var/lib/apt/lists/*
COPY named.conf /etc/bind/named.conf
COPY db.lab-corp /etc/bind/db.lab-corp
EXPOSE 53/udp 53/tcp
# Foreground, authoritative only.
ENTRYPOINT ["named", "-g", "-c", "/etc/bind/named.conf"]
