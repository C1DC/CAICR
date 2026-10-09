#!/usr/bin/env python3
"""Generate capstone-capture.pcap: the compromised foothold (10.13.10.66)
beaconing to a C2 domain, plus a burst toward the exfiltration IP. Valid
classic PCAP, pure stdlib, deterministic.
"""
from __future__ import annotations
import struct
from pathlib import Path

SRC = "10.13.10.66"       # attacker foothold
RESOLVER = "10.13.10.1"
EXFIL_IP = "185.220.101.44"
C2_DOMAIN = "cdn-sync.ddns-telemetry.net"
INTERVAL = 60


def ipb(ip): return bytes(int(o) for o in ip.split("."))


def csum(d):
    if len(d) % 2:
        d += b"\x00"
    s = sum((d[i] << 8) | d[i + 1] for i in range(0, len(d), 2))
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return (~s) & 0xFFFF


def dns_q(txid, qname):
    h = struct.pack(">HHHHHH", txid, 0x0100, 1, 0, 0, 0)
    q = b"".join(bytes([len(l)]) + l.encode() for l in qname.split(".")) + b"\x00"
    return h + q + struct.pack(">HH", 1, 1)


def udp(sp, dp, pl):
    return struct.pack(">HHHH", sp, dp, 8 + len(pl), 0) + pl


def ip4(src, dst, pl, ident):
    hdr = struct.pack(">BBHHHBBH4s4s", 0x45, 0, 20 + len(pl), ident, 0, 64, 17, 0,
                      ipb(src), ipb(dst))
    hdr = hdr[:10] + struct.pack(">H", csum(hdr)) + hdr[12:]
    return hdr + pl


def eth(pl):
    return bytes.fromhex("02420a0d0a01") + bytes.fromhex("0242ac0d0a42") + struct.pack(">H", 0x0800) + pl


def rec(ts, data):
    return struct.pack("<IIII", int(ts), int((ts % 1) * 1e6), len(data), len(data)) + data


def build():
    base = 1_760_000_000
    out = []
    txid = 0x2000
    # C2 beacons
    for i in range(5):
        txid += 1
        out.append(rec(base + i * INTERVAL,
                       eth(ip4(SRC, RESOLVER, udp(40000 + i, 53, dns_q(txid, C2_DOMAIN)), 0x300 + i))))
    # exfil burst: many large UDP packets to the external IP
    for i in range(12):
        payload = b"\x00" * 1400
        out.append(rec(base + 300 + i * 0.2,
                       eth(ip4(SRC, EXFIL_IP, udp(50000, 4444, payload), 0x400 + i))))
    out.sort(key=lambda r: struct.unpack("<I", r[:4])[0] * 1_000_000 + struct.unpack("<I", r[4:8])[0])
    gh = struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1)
    return gh + b"".join(out)


def main():
    out = Path(__file__).resolve().parent / "capstone-capture.pcap"
    out.write_bytes(build())
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"  C2 domain: {C2_DOMAIN}   exfil IP: {EXFIL_IP}   foothold: {SRC}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
