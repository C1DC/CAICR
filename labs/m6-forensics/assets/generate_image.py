#!/usr/bin/env python3
"""Build evidence.img — a small, valid FAT16 disk image for the M6 forensics
lab, using pure stdlib (no mount, no mtools, no root).

The image root directory holds:
  * Q3_Supplier_Invoice.xlsm  — the macro-enabled lure the user opened
  * README.txt                — benign
  * vpn_creds.txt (DELETED)   — recoverable with Autopsy / tsk_recover / icat

Sleuthkit reads it directly (fls / icat / tsk_recover), so Autopsy ingests it
as a normal disk image. Deterministic output -> stable SHA-256.
"""
from __future__ import annotations

import struct
import os
from pathlib import Path

BPS = 512          # bytes per sector
SPC = 1            # sectors per cluster
RESERVED = 1       # reserved sectors (just the boot sector)
NUM_FATS = 2
ROOT_ENTRIES = 512
TOTAL_SECTORS = 12288   # 6 MiB -> forces FAT16 cluster count
MEDIA = 0xF8
VOLID = 0x43414943      # "CAIC"
LABEL = b"CAIC EVID  "  # 11 bytes

ROOT_DIR_SECTORS = (ROOT_ENTRIES * 32 + BPS - 1) // BPS  # 32


def _fat_size() -> int:
    """Iteratively size the FAT so the layout is self-consistent."""
    fsz = 1
    while True:
        data_sectors = TOTAL_SECTORS - RESERVED - NUM_FATS * fsz - ROOT_DIR_SECTORS
        clusters = data_sectors // SPC
        need = ((clusters + 2) * 2 + BPS - 1) // BPS
        if need <= fsz:
            return fsz
        fsz = need


FAT_SIZE = _fat_size()
DATA_START_SECTOR = RESERVED + NUM_FATS * FAT_SIZE + ROOT_DIR_SECTORS


def boot_sector() -> bytes:
    b = bytearray(BPS)
    b[0:3] = b"\xEB\x3C\x90"
    b[3:11] = b"MSDOS5.0"
    struct.pack_into("<H", b, 11, BPS)
    b[13] = SPC
    struct.pack_into("<H", b, 14, RESERVED)
    b[16] = NUM_FATS
    struct.pack_into("<H", b, 17, ROOT_ENTRIES)
    struct.pack_into("<H", b, 19, TOTAL_SECTORS if TOTAL_SECTORS < 65536 else 0)
    b[21] = MEDIA
    struct.pack_into("<H", b, 22, FAT_SIZE)
    struct.pack_into("<H", b, 24, 32)      # sectors per track
    struct.pack_into("<H", b, 26, 64)      # heads
    struct.pack_into("<I", b, 28, 0)       # hidden sectors
    struct.pack_into("<I", b, 32, TOTAL_SECTORS if TOTAL_SECTORS >= 65536 else 0)
    b[36] = 0x80                           # drive number
    b[38] = 0x29                           # extended boot signature
    struct.pack_into("<I", b, 39, VOLID)
    b[43:54] = LABEL
    b[54:62] = b"FAT16   "
    b[510:512] = b"\x55\xAA"
    return bytes(b)


def dir_entry(name83: str, first_cluster: int, size: int,
              attr: int = 0x20, deleted: bool = False) -> bytes:
    name, _, ext = name83.partition(".")
    raw = (name.upper()[:8].ljust(8) + ext.upper()[:3].ljust(3)).encode("ascii")
    e = bytearray(32)
    e[0:11] = raw
    if deleted:
        e[0] = 0xE5                       # deletion marker (data left intact)
    e[11] = attr
    # fixed timestamp: 2026-10-04 02:15:00
    struct.pack_into("<H", e, 14, (2 << 11) | (15 << 5) | 0)      # create time
    struct.pack_into("<H", e, 16, ((2026 - 1980) << 9) | (10 << 5) | 4)  # create date
    struct.pack_into("<H", e, 18, ((2026 - 1980) << 9) | (10 << 5) | 4)  # access date
    struct.pack_into("<H", e, 22, (2 << 11) | (15 << 5) | 0)     # write time
    struct.pack_into("<H", e, 24, ((2026 - 1980) << 9) | (10 << 5) | 4)  # write date
    struct.pack_into("<H", e, 26, first_cluster & 0xFFFF)
    struct.pack_into("<I", e, 28, size)
    return bytes(e)


def build() -> bytes:
    # 8.3-clean names so Autopsy / fls display them exactly (no LFN needed)
    files = [
        ("README.TXT", b"Workstation FIN-03. If found, return to ICT.\r\n", False),
        ("Q3INVOIC.XLS",
         b"[macro-enabled workbook - disguised .xls]\r\n"
         b"Workbook_Open -> cmd /c powershell -enc <base64>\r\n"
         b"This document executed a macro when the user opened it.\r\n", False),
        ("VPNKEYS.TXT",
         ("corporate VPN\r\nuser: vpnadmin\r\npass: " + os.environ.get("CAIC_VPN_PASS","Gh@na2026!") + "\r\nserver: 10.8.0.1\r\n").encode(),
         True),   # deleted but recoverable
    ]

    # allocate clusters sequentially
    clusters_per: list[int] = []
    for _name, data, _d in files:
        clusters_per.append(max(1, (len(data) + BPS * SPC - 1) // (BPS * SPC)))

    data_region = bytearray()
    entries = []
    cluster = 2
    for (name, data, deleted), ncl in zip(files, clusters_per):
        first = cluster
        chunk = bytearray(ncl * BPS * SPC)
        chunk[0:len(data)] = data
        data_region += chunk
        entries.append((name, first, len(data), deleted, ncl))
        cluster += ncl

    # FAT: entry0/1 reserved, then a chain per (live) file
    total_entries = (FAT_SIZE * BPS) // 2
    fat = [0] * total_entries
    fat[0] = 0xFFF8
    fat[1] = 0xFFFF
    for _name, first, _sz, deleted, ncl in entries:
        if deleted:
            continue  # freed on delete (entries stay 0) — data still on disk
        for k in range(ncl):
            c = first + k
            fat[c] = 0xFFFF if k == ncl - 1 else c + 1
    fat_bytes = b"".join(struct.pack("<H", v & 0xFFFF) for v in fat)

    # root directory
    root = bytearray()
    root += dir_entry(LABEL.decode().strip() or "CAIC", 0, 0, attr=0x08)  # volume label
    for name, first, sz, deleted, _ncl in entries:
        root += dir_entry(name, first, sz, deleted=deleted)
    root = root.ljust(ROOT_DIR_SECTORS * BPS, b"\x00")

    # assemble: boot | FAT1 | FAT2 | root | data (padded to TOTAL_SECTORS)
    img = bytearray()
    img += boot_sector()
    img += fat_bytes
    img += fat_bytes
    img += root
    img += data_region
    img = img.ljust(TOTAL_SECTORS * BPS, b"\x00")
    return bytes(img)


def main() -> int:
    out = Path(__file__).resolve().parent / "evidence.img"
    img = build()
    out.write_bytes(img)
    import hashlib
    h = hashlib.sha256(img).hexdigest()
    print(f"wrote {out} ({len(img)} bytes, FAT16, fat_size={FAT_SIZE} sectors)")
    print(f"  data starts at sector {DATA_START_SECTOR}")
    print(f"  sha256: {h}")
    # write a hash manifest for `sha256sum -c`
    (out.parent / "evidence.sha256").write_text(f"{h}  evidence.img\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
