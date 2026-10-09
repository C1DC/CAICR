#!/usr/bin/env python3
"""Generate the M5 BEC evidence package (deterministic, pure stdlib):

  genuine-quote.eml          the REAL supplier's earlier email (clean auth)
  invoice-change-request.eml the SPOOFED bank-detail-change email (fails auth)
  remittance-advice.pdf      the malicious attachment — its metadata betrays
                             the attacker (author, authoring timezone, a
                             creation date BEFORE the email = premeditation)

The analyst compares the two emails, traces the spoof, and runs exiftool on the
PDF to expose the author and the authoring timezone.
"""
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEGIT = "zenithsupplies.com.gh"
# Per-student values from the lab engine (defaults keep it standalone).
LOOKALIKE = os.environ.get("CAIC_LOOKALIKE", "zenith-supplies.com")
SRC_IP = os.environ.get("CAIC_SOURCE_IP", "45.137.112.63")
FRAUD_ACCT = os.environ.get("CAIC_FRAUD_ACCOUNT", "1402300087654")
PDF_AUTHOR = os.environ.get("CAIC_PDF_AUTHOR", "k1ngpin")
PDF_TZ = os.environ.get("CAIC_PDF_TZ", "+07:00")          # exiftool-style offset
_TZ_PDF = PDF_TZ.replace(":", "'") + "'"                   # -> +07'00'

GENUINE = f"""\
Return-Path: <k.mensah@{LEGIT}>
Received: from mx.{LEGIT} (mx.{LEGIT} [102.89.33.10])
\tby mx.lab-institution.gov.gh (Postfix) with ESMTPS id 10AF2;
\tMon, 29 Sep 2026 10:12:00 +0000 (GMT)
Authentication-Results: mx.lab-institution.gov.gh;
\tspf=pass smtp.mailfrom=k.mensah@{LEGIT}; dkim=pass header.d={LEGIT};
\tdmarc=pass header.from={LEGIT}
Message-ID: <q3-quote-8841@{LEGIT}>
Date: Mon, 29 Sep 2026 10:11:58 +0000
From: "Kwame Mensah | Zenith Supplies" <k.mensah@{LEGIT}>
Reply-To: <k.mensah@{LEGIT}>
To: "Ama Boateng" <ama.boateng@lab-institution.gov.gh>
Subject: Q3 supply quote — PO ZS-20418

Dear Ama,

Please find our quote for PO ZS-20418. Our bank details are unchanged
(First National, acct 9021145530). Kind regards, Kwame.
"""

SPOOF = f"""\
Return-Path: <billing@{LOOKALIKE}>
Delivered-To: ama.boateng@lab-institution.gov.gh
Received: from mail.{LOOKALIKE} (unknown [{SRC_IP}])
\tby mx.lab-institution.gov.gh (Postfix) with ESMTPS id 5C3A1;
\tTue, 06 Oct 2026 08:42:09 +0000 (GMT)
Authentication-Results: mx.lab-institution.gov.gh;
\tspf=fail (sender IP is {SRC_IP}) smtp.mailfrom=billing@{LOOKALIKE};
\tdkim=none; dmarc=fail (p=none) header.from={LOOKALIKE}
Message-ID: <a71f9c23-fraud@{LOOKALIKE}>
Date: Tue, 06 Oct 2026 08:42:08 +0000
From: "Kwame Mensah | Zenith Supplies" <k.mensah@{LEGIT}>
Reply-To: <accounts@{LOOKALIKE}>
To: "Ama Boateng" <ama.boateng@lab-institution.gov.gh>
Subject: RE: Q3 supply quote — URGENT updated bank details for PO ZS-20418
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

Dear Ama,

Further to our quote, note our bank account has CHANGED due to an audit.
Please pay PO ZS-20418 to the new account below TODAY and confirm by email —
I am travelling and cannot take calls.

    Account name:   Zenith Supplies Ltd
    Bank:           First Atlantic Bank, Osu
    Account number: {FRAUD_ACCT}

See attached remittance advice. Regards, Kwame.
"""


def build_pdf() -> bytes:
    """Minimal but valid PDF with an /Info dict carrying planted metadata."""
    objs = []
    objs.append(b"<< /Type /Catalog /Pages 2 0 R >>")
    objs.append(b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
    objs.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 320 200] "
                b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>")
    stream = b"BT /F1 12 Tf 36 150 Td (Remittance Advice - pay to new account) Tj ET"
    objs.append(b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream))
    objs.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    # Object 6: the Info dictionary — the forensic goldmine
    objs.append(b"<< /Title (Remittance Advice) /Author (" + PDF_AUTHOR.encode() + b") "
                b"/Creator (Microsoft Office Word) /Producer (Skia/PDF m118) "
                b"/CreationDate (D:20260928090000" + _TZ_PDF.encode() + b") "
                b"/ModDate (D:20260928090000" + _TZ_PDF.encode() + b") >>")

    out = bytearray(b"%PDF-1.5\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, body in enumerate(objs, start=1):
        offsets.append(len(out))
        out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
    xref_pos = len(out)
    n = len(objs) + 1
    out += b"xref\n0 %d\n" % n
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += b"%010d 00000 n \n" % off
    out += (b"trailer\n<< /Size %d /Root 1 0 R /Info 6 0 R >>\nstartxref\n%d\n%%%%EOF\n"
            % (n, xref_pos))
    return bytes(out)


def main() -> int:
    (HERE / "genuine-quote.eml").write_text(GENUINE, encoding="utf-8")
    (HERE / "invoice-change-request.eml").write_text(SPOOF, encoding="utf-8")
    (HERE / "remittance-advice.pdf").write_bytes(build_pdf())
    # remove the superseded single-email generator's output name if present
    print("wrote genuine-quote.eml, invoice-change-request.eml, remittance-advice.pdf")
    print(f"  spoof source IP   : {SRC_IP}   look-alike: {LOOKALIKE}")
    print(f"  PDF author        : k1ngpin   authoring TZ: +07:00 (not Ghana)")
    print(f"  PDF created        : 2026-09-28  (8 days BEFORE the email — premeditation)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
