# Fraud Investigation Brief (BEC) — Module 5 Deliverable

**Investigator:** [your name]  **Date:** [YYYY-MM-DD]
**Case ref:** [ ]  **Reported by:** [who flagged it]

> Prove the fraud from the email's *and the attachment's* own evidence, then fix
> the **process** that let it through. See `labctl learn m5`.

## 1. Summary (BLUF)

[One paragraph: what the email claimed, what it really was, whether money moved,
and the single most urgent action.]

## 2. Header forensics findings

| Field | Value found | What it proves |
|-------|-------------|----------------|
| From (display) | [ ] | (attacker-controlled — trust last) |
| Return-Path / envelope sender | [ ] | [look-alike domain?] |
| Reply-To | [ ] | [mismatch → replies go to attacker?] |
| Source IP (earliest Received) | [ ] | [whois: ISP / country] |
| SPF — spoof | [ ] | |
| SPF — genuine email (baseline) | [ ] | [the contrast is the proof] |
| DKIM / DMARC | [ ] | |

**Look-alike domain:** [ ]  **Impersonated real domain:** [ ]
**Reused PO number (thread hijack):** [ ]

## 3. Attachment forensics (exiftool / pdfinfo)

| Metadata field | Value | What it proves |
|----------------|-------|----------------|
| Author | [ ] | [handle, not a supplier name?] |
| Create Date (+ timezone offset) | [ ] | [offset inconsistent with Ghana +00:00?] |
| Email send date | [ ] | |
| Created **before** sent? | [ yes / no ] | [yes → **premeditation**] |

## 4. Evidence timeline

| Date / time | Event |
|-------------|-------|
| [ ] | Attachment created (PDF metadata) |
| [ ] | Look-alike domain registered (whois) |
| [ ] | Spoofed email sent/received |
| [ ] | [action taken / payment attempted] |

## 5. Fraudulent payment details (for bank recall)

- Requested account: [ ]  Bank: [ ]  Amount: [ ]
- Legitimate account on file: [ ]

## 6. Control failures & the fix

- **Failures:** [e.g. no dual-control callback on a known number before a bank-detail change]
- **Process fix:** [who initiates vs approves; mandatory out-of-band callback to a
  previously known number for any bank-detail change; thresholds; logging]
- **Harden our own domain:** our current DMARC policy is [none/quarantine/reject];
  target [p=reject] by [date] so our brand can't be spoofed at a counterparty.

## 6b. Recall & report (if money moved — the golden hour)

*In order, and in parallel where possible:*

- [ ] Called **our bank's fraud desk** to freeze/recall — time: [ ]
- [ ] **Receiving bank / telco** asked to freeze the account/wallet — ref: [ ]
- [ ] Reported to **CSA / CERT-GH** (Act 1038) — ref: [ ]
- [ ] **Bank of Ghana** notified (if a regulated obligation) — [ ]
- [ ] **Police Cybercrime Unit / EOCO** — case ref: [ ]
- [ ] Evidence preserved (emails with full headers, attachment, this brief)

**ATT&CK:** T1566 (Phishing) / T1656 (Impersonation).

---

## Self-check before you submit

- [ ] Every value is **my own** (randomised per student).
- [ ] I used the **genuine email as a baseline** and stated the SPF contrast.
- [ ] I ran exiftool and stated whether the file was **created before it was sent**.
- [ ] My fix is a **process** control (dual control + callback), not just "be careful".
- [ ] Payment details are precise enough for a **bank recall**.

## Grading rubric (100 pts)

| Band | Headers & origin (30) | Attachment & premeditation (25) | Timeline & recall detail (20) | Process fix & ATT&CK (25) |
|------|-----------------------|---------------------------------|-------------------------------|---------------------------|
| Excellent (full) | True origin traced; SPF contrast used as proof | Author + timezone + premeditation proven | Clear dated timeline; precise recall details | Dual-control callback specified; correct ATT&CK |
| Adequate (~60%) | Spoof identified, baseline not used | Metadata read, premeditation missed | Partial timeline | "Verify payments" — vague |
| Weak (<40%) | Trusts From:, no trace | Attachment ignored | No timeline | No process control |

---

## Worked example (reference — fictional "Adom Microfinance Ltd")

*Illustrative values — yours are randomised.*

**Summary:** A "supplier" email asked to redirect a ZS-20418 invoice payment to a
new account. It was a spoof; payment was halted before release.

**Headers:** `From:` showed *Zenith Supplies* but `Return-Path`/`Reply-To` used
**zenith-supplies.com** (look-alike of the real **zenithsupplies.com.gh**); source
IP **45.137.112.63** (whois: offshore hosting). Spoof **SPF fail / DKIM none /
DMARC fail**; the earlier genuine quote was **SPF pass** — the contrast is the
proof. Reused PO **ZS-20418** = thread hijack.

**Attachment:** `remittance-advice.pdf` → Author **k1ngpin**, Create Date
**2026-09-28 +07:00**, email sent **2026-10-06**. Created **8 days before** it was
sent, from a **+07:00** timezone → **premeditated fraud by a foreign author**.

**Recall:** fraudulent account 13-digit number at [bank]; legitimate account on
file differs — flagged to the bank's fraud desk.

**Fix:** dual control (initiator ≠ approver) + **mandatory callback to the
supplier's known number** for any bank-detail change; alert over GHS 10,000.
**ATT&CK:** T1566.002 / T1656. **BLUF:** *"A premeditated supplier-impersonation
fraud; one callback on our known number stops this and every future instance."*
