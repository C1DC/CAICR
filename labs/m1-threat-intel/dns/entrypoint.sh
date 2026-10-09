#!/bin/sh
# Render the zone from the per-student values (passed as env by the lab engine),
# with sensible defaults so the image also runs standalone.
: "${HIDDEN_HOST:=vpn-admin}"
: "${HIDDEN_IP:=10.20.0.7}"
: "${MAIL_IP:=41.210.15.21}"
sed -e "s/__HIDDEN_HOST__/${HIDDEN_HOST}/g" \
    -e "s/__HIDDEN_IP__/${HIDDEN_IP}/g" \
    -e "s/__MAIL_IP__/${MAIL_IP}/g" \
    /etc/bind/db.lab-corp.tmpl > /etc/bind/db.lab-corp
exec named -g -c /etc/bind/named.conf
