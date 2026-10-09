# Authoritative DNS for the M1 recon lab — real BIND9. The zone is rendered at
# container start from per-student values (env), and is deliberately
# misconfigured with `allow-transfer { any; }` so a zone transfer (AXFR) leaks
# the whole zone — including a hidden internal host unique to each student.
# It also omits DMARC and CAA on purpose. Training target only.
FROM debian:12-slim
RUN apt-get update && apt-get install -y --no-install-recommends bind9 bind9-utils dnsutils \
    && rm -rf /var/lib/apt/lists/*
COPY named.conf /etc/bind/named.conf
COPY db.lab-corp.tmpl /etc/bind/db.lab-corp.tmpl
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
EXPOSE 53/udp 53/tcp
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
