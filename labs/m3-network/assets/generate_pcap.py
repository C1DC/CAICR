#!/usr/bin/env python3
"""Generate network-capture.pcap for the M3 investigation.

Two things to find in one capture:
  1. DNS C2 beaconing — the infected workstation (10.13.3.30) queries a
     dynamic-DNS C2 domain every 30 seconds.
  2. A cleartext FTP login — an admin (10.13.3.50) logs into the fileserver
     (10.13.3.20) over plain FTP, so the username and password are visible to
     anyone who follows the TCP stream.

Valid classic PCAP, pure stdlib, deterministic output.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

LINK = 1  # Ethernet
C2_DOMAIN = "sync-telemetry.duckdns.org"
INFECTED = "10.13.3.30"
RESOLVER = "10.13.3.1"
BEACON_INTERVAL = 30
FTP_CLIENT = "10.13.3.50"
FTP_SERVER = "10.13.3.20"
FTP_USER = "backupsvc"
FTP_PASS = "Backup#2021"


def ipb(ip): return bytes(int(o) for o in ip.split("."))


def csum(d: bytes) -> int:
    if len(d) % 2:
        d += b"\x00"
    s = sum((d[i] << 8) | d[i + 1] for i in range(0, len(d), 2))
    s = (s >> 16) + (s & 0xFFFF)
    s += s >> 16
    return (~s) & 0xFFFF


def ip4(src, dst, payload, ident, proto):
    hdr = struct.pack(">BBHHHBBH4s4s", 0x45, 0, 20 + len(payload), ident, 0, 64, proto, 0,
                      ipb(src), ipb(dst))
    hdr = hdr[:10] + struct.pack(">H", csum(hdr)) + hdr[12:]
    return hdr + payload


def eth(payload):
    return (bytes.fromhex("02420a0d0301") + bytes.fromhex("0242ac0d0330")
            + struct.pack(">H", 0x0800) + payload)


def udp(sp, dp, pl):
    return struct.pack(">HHHH", sp, dp, 8 + len(pl), 0) + pl


def dns_q(txid, qname):
    h = struct.pack(">HHHHHH", txid, 0x0100, 1, 0, 0, 0)
    q = b"".join(bytes([len(x)]) + x.encode() for x in qname.split(".")) + b"\x00"
    return h + q + struct.pack(">HH", 1, 1)


def tcp(src, dst, sp, dp, seq, ack, flags, payload=b""):
    off_flags = (5 << 12) | flags
    hdr = struct.pack(">HHIIHHHH", sp, dp, seq, ack, off_flags, 64240, 0, 0)
    pseudo = ipb(src) + ipb(dst) + struct.pack(">BBH", 0, 6, len(hdr) + len(payload))
    chk = csum(pseudo + hdr + payload)
    hdr = hdr[:16] + struct.pack(">H", chk) + hdr[18:]
    return ip4(src, dst, hdr + payload, 0, 6)


def rec(ts, data):
    return struct.pack("<IIII", int(ts), int((ts % 1) * 1e6), len(data), len(data)) + data


def build():
    base = 1_760_000_000
    out = []

    # --- DNS C2 beacons from the infected host (every 30s) ---
    txid = 0x1000
    for i in range(5):
        txid += 1
        out.append(rec(base + i * BEACON_INTERVAL,
                       eth(ip4(INFECTED, RESOLVER, udp(40000 + i, 53, dns_q(txid, C2_DOMAIN)), 0x100 + i, 17))))
    # a little benign DNS noise
    for off, host, dom in [(7, "10.13.3.11", "www.google.com"), (52, "10.13.3.12", "kaiptc.com")]:
        txid += 1
        out.append(rec(base + off,
                       eth(ip4(host, RESOLVER, udp(51000, 53, dns_q(txid, dom)), 0x200 + off, 17))))

    # --- cleartext FTP login (handshake then USER/PASS in the clear) ---
    c, s = FTP_CLIENT, FTP_SERVER
    cp, sp = 51972, 21
    t = base + 100
    cseq, sseq = 1000, 5000
    # 3-way handshake
    out.append(rec(t, eth(tcp(c, s, cp, sp, cseq, 0, 0x02))))                       # SYN
    out.append(rec(t + 0.01, eth(tcp(s, c, sp, cp, sseq, cseq + 1, 0x12))))         # SYN-ACK
    out.append(rec(t + 0.02, eth(tcp(c, s, cp, sp, cseq + 1, sseq + 1, 0x10))))     # ACK
    cseq += 1; sseq += 1
    conv = [
        (s, "220 lab-corp FTP service (vsftpd 3.0.5) ready.\r\n"),
        (c, f"USER {FTP_USER}\r\n"),
        (s, "331 Please specify the password.\r\n"),
        (c, f"PASS {FTP_PASS}\r\n"),
        (s, "230 Login successful.\r\n"),
        (c, "SYST\r\n"),
        (s, "215 UNIX Type: L8\r\n"),
    ]
    tt = t + 0.03
    for who, msg in conv:
        payload = msg.encode()
        if who == c:
            out.append(rec(tt, eth(tcp(c, s, cp, sp, cseq, sseq, 0x18, payload))))   # PSH-ACK
            cseq += len(payload)
        else:
            out.append(rec(tt, eth(tcp(s, c, sp, cp, sseq, cseq, 0x18, payload))))
            sseq += len(payload)
        tt += 0.05

    out.sort(key=lambda r: struct.unpack("<I", r[:4])[0] * 1_000_000 + struct.unpack("<I", r[4:8])[0])
    gh = struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, LINK)
    return gh + b"".join(out)


def main():
    out = Path(__file__).resolve().parent / "network-capture.pcap"
    out.write_bytes(build())
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"  C2 domain : {C2_DOMAIN}   beacon interval: {BEACON_INTERVAL}s   infected: {INFECTED}")
    print(f"  FTP creds : {FTP_USER} / {FTP_PASS}  ({FTP_CLIENT} -> {FTP_SERVER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
