# Authoritative-ish DNS for the M1 OSINT lab. dnsmasq serves a small lab zone
# so dig returns real answers with no internet. The zone deliberately has an
# SPF record but NO DMARC record — the finding the student must spot.
FROM alpine:3.20
RUN apk add --no-cache dnsmasq
COPY dnsmasq.conf /etc/dnsmasq.conf
EXPOSE 53/udp 53/tcp
ENTRYPOINT ["dnsmasq", "-k", "-C", "/etc/dnsmasq.conf"]
