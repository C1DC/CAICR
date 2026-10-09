#!/usr/bin/env python3
"""Generate the BEC evidence for M5: a spoofed supplier email with full,
internally-consistent headers a student can trace. Deterministic, pure stdlib.

The story: a finance officer at a fictional Ghanaian institution receives an
email that looks like it is from their real supplier (zenithsupplies.com.gh),
asking to change the bank account for an outstanding invoice. The headers show
it actually came from a look-alike domain on a foreign VPS, and failed SPF,
DKIM and DMARC.
"""
from pathlib import Path

LEGIT_DOMAIN = "zenithsupplies.com.gh"       # the real supplier
LOOKALIKE = "zenith-supplies.com"            # attacker's look-alike (hyphenated)
SOURCE_IP = "45.137.112.63"                  # connecting server (foreign VPS)
RECV_MX = "mx.lab-institution.gov.gh"        # victim's mail gateway
FRAUD_ACCOUNT = "1402300087654"
FRAUD_BANK = "First Atlantic Bank, Osu branch"

EML = f"""\
Return-Path: <billing@{LOOKALIKE}>
Delivered-To: ama.boateng@lab-institution.gov.gh
Received: from {RECV_MX} (localhost [127.0.0.1])
\tby {RECV_MX} with LMTP id 8fA2 for <ama.boateng@lab-institution.gov.gh>;
\tTue, 06 Oct 2026 08:42:11 +0000 (GMT)
Received: from mail.{LOOKALIKE} (unknown [{SOURCE_IP}])
\tby {RECV_MX} (Postfix) with ESMTPS id 5C3A1;
\tTue, 06 Oct 2026 08:42:09 +0000 (GMT)
Authentication-Results: {RECV_MX};
\tspf=fail (sender IP is {SOURCE_IP}) smtp.mailfrom=billing@{LOOKALIKE};
\tdkim=none (no signature);
\tdmarc=fail (p=none) header.from={LOOKALIKE}
Received-SPF: fail ({LEGIT_DOMAIN}: {SOURCE_IP} is not permitted to send)
Message-ID: <a71f9c23-fraud@{LOOKALIKE}>
Date: Tue, 06 Oct 2026 08:42:08 +0000
From: "Kwame Mensah | Zenith Supplies" <k.mensah@{LEGIT_DOMAIN}>
Reply-To: <accounts@{LOOKALIKE}>
To: "Ama Boateng" <ama.boateng@lab-institution.gov.gh>
Subject: URGENT: Updated bank details for Invoice ZS-20418
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

Dear Ama,

I hope you are well. Due to an audit on our old corporate account, please
note that all payments must now go to our NEW bank account with immediate
effect. Kindly update your records before processing Invoice ZS-20418.

    Account name:   Zenith Supplies Ltd
    Bank:           {FRAUD_BANK}
    Account number: {FRAUD_ACCOUNT}

As this invoice is already overdue, please treat it as a priority and confirm
once the transfer has been made today. I am travelling and may be slow to
answer calls, so email is best.

Best regards,
Kwame Mensah
Accounts Receivable, Zenith Supplies Ltd
"""


def main() -> int:
    out = Path(__file__).resolve().parent / "invoice-change-request.eml"
    out.write_text(EML, encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    print(f"  look-alike domain : {LOOKALIKE}  (real: {LEGIT_DOMAIN})")
    print(f"  source IP         : {SOURCE_IP}   SPF/DKIM/DMARC: fail/none/fail")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
