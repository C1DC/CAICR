#!/usr/bin/env python3
"""Create suspicious_artifact.txt — a two-layer-obfuscated C2 URL, the kind of
string found inside a dropper. The student decodes it in CyberChef
(From Base64 -> URL Decode) or on the CLI. Deterministic, pure stdlib.
"""
import base64
import os
import urllib.parse
from pathlib import Path

C2_URL = "http://" + os.environ.get("CAIC_C2_DOMAIN","beacon.sync-malware-c2.net") + "/gate.php?id=FIN03"

# Layer 1: URL-encode.  Layer 2: Base64.  (student reverses: Base64 -> URL)
layer1 = urllib.parse.quote(C2_URL, safe="")
artifact = base64.b64encode(layer1.encode()).decode()


def main() -> int:
    out = Path(__file__).resolve().parent / "suspicious_artifact.txt"
    out.write_text(artifact + "\n")
    print(f"wrote {out}")
    print(f"  CyberChef recipe : From Base64  ->  URL Decode")
    print(f"  decodes to       : {C2_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
