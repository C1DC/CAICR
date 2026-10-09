# Fraud Investigation Brief (BEC) — Module 5 Deliverable

**Investigator:** [your name]  **Date:** [YYYY-MM-DD]
**Case ref:** [ ]  **Reported by:** [who flagged it]

> Prove the fraud from the email's own evidence, then fix the *process* that let
> it through. See `labctl learn m5`.

## 1. Summary

[One paragraph: what the email claimed, what it really was, and whether money
moved.]

## 2. Header forensics findings

| Field | Value found | What it proves |
|-------|-------------|----------------|
| From (display) | [ ] | (attacker-controlled — trust last) |
| Return-Path / envelope sender | [ ] | [look-alike domain?] |
| Reply-To | [ ] | [mismatch → replies go to attacker?] |
| Source IP (earliest Received) | [ ] | [whois: ISP / country] |
| SPF result | [ ] | |
| DKIM result | [ ] | |
| DMARC result | [ ] | |

**Look-alike domain:** [ ]  **Impersonated real domain:** [ ]

## 3. Evidence timeline

| Time | Event |
|------|-------|
| [ ] | Look-alike domain registered |
| [ ] | Email received |
| [ ] | [action taken / payment attempted] |

## 4. Fraudulent payment details (for bank recall)

- Requested account: [ ]  Bank: [ ]  Amount: [ ]
- Legitimate account on file: [ ]

## 5. Control failures identified

- [e.g. No dual-control callback on a known number before changing bank details.]

## 6. Payment-verification control (the fix)

[Design the procedure: who initiates vs approves, mandatory out-of-band callback
to a previously known number for any bank-detail change, thresholds, logging.]

**ATT&CK:** T1566 (Phishing) / T1656 (Impersonation).
