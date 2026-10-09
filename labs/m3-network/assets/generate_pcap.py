#!/usr/bin/env python3
"""Generate network-capture.pcap for the M3 Wireshark exercise.

Produces a small, valid classic-format PCAP of DNS traffic. One internal host
(10.13.3.30) beacons to a dynamic-DNS C2 domain every 30 seconds; a little
benign DNS is mixed in so the student has to filter. Deterministic output —
run it once to (re)create the capture. Pure stdlib.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

LINKTYPE_ETHERNET = 1
SRC_HOST = "10.13.3.30"     # infected workstation
RESOLVER = "10.13.3.1"      # lab resolver / gateway
C2_DOMAIN = "sync-telemetry.duckdns.org"
BEACON_INTERVAL = 30         # seconds


def ip_to_bytes(ip: str) -> bytes:
    return bytes(int(o) for o in ip.split("."))


def checksum16(data: bytes) -> int:
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
    total = (total >> 16) + (total & 0xFFFF)
    total += total >> 16
    return (~total) & 0xFFFF


def dns_query(txid: int, qname: str) -> bytes:
    header = struct.pack(">HHHHHH", txid, 0x0100, 1, 0, 0, 0)  # standard query, RD
    q = b"".join(bytes([len(lbl)]) + lbl.encode() for lbl in qname.split(".")) + b"\x00"
    q += struct.pack(">HH", 1, 1)  # type A, class IN
    return header + q


def udp(src_port: int, dst_port: int, payload: bytes) -> bytes:
    length = 8 + len(payload)
    return struct.pack(">HHHH", src_port, dst_port, length, 0) + payload  # csum 0 = unused


def ipv4(src: str, dst: str, payload: bytes, ident: int) -> bytes:
    ver_ihl, tos = 0x45, 0
    total = 20 + len(payload)
    ttl, proto = 64, 17  # UDP
    hdr = struct.pack(">BBHHHBBH4s4s", ver_ihl, tos, total, ident, 0,
                      ttl, proto, 0, ip_to_bytes(src), ip_to_bytes(dst))
    csum = checksum16(hdr)
    hdr = hdr[:10] + struct.pack(">H", csum) + hdr[12:]
    return hdr + payload


def ethernet(payload: bytes) -> bytes:
    dst_mac = bytes.fromhex("02420a1e0301")  # gateway-ish
    src_mac = bytes.fromhex("0242ac1e031e")
    return dst_mac + src_mac + struct.pack(">H", 0x0800) + payload


def frame(src, dst, sport, dport, dns_payload, ident) -> bytes:
    return ethernet(ipv4(src, dst, udp(sport, dport, dns_payload), ident))


def pcap_global_header() -> bytes:
    return struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, LINKTYPE_ETHERNET)


def pcap_record(ts: float, data: bytes) -> bytes:
    secs, usecs = int(ts), int((ts - int(ts)) * 1_000_000)
    return struct.pack("<IIII", secs, usecs, len(data), len(data)) + data


def build() -> bytes:
    base = 1_760_000_000  # fixed epoch so output is reproducible
    records = []
    txid = 0x1000

    # 5 beacons to the C2 domain, every BEACON_INTERVAL seconds
    for i in range(5):
        txid += 1
        ts = base + i * BEACON_INTERVAL
        pkt = frame(SRC_HOST, RESOLVER, 40000 + i, 53, dns_query(txid, C2_DOMAIN), 0x100 + i)
        records.append(pcap_record(ts, pkt))

    # benign noise interleaved (different host / normal domains)
    for off, host, dom in [(7, "10.13.3.11", "www.google.com"),
                           (52, "10.13.3.12", "kaiptc.com"),
                           (95, "10.13.3.11", "update.microsoft.com")]:
        txid += 1
        pkt = frame(host, RESOLVER, 51000, 53, dns_query(txid, dom), 0x200 + off)
        records.append(pcap_record(base + off, pkt))

    # sort by timestamp so Wireshark shows chronological order
    records.sort(key=lambda r: struct.unpack("<I", r[:4])[0] * 1_000_000
                 + struct.unpack("<I", r[4:8])[0])
    return pcap_global_header() + b"".join(records)


def main() -> int:
    out = Path(__file__).resolve().parent / "network-capture.pcap"
    out.write_bytes(build())
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"  C2 domain : {C2_DOMAIN}")
    print(f"  interval  : {BEACON_INTERVAL}s   infected host: {SRC_HOST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
