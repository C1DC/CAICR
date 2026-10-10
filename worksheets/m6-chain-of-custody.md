# Chain of Custody Form — Module 6 Deliverable

**Case ref:** [ ]  **Examiner:** [your name]  **Organisation:** [ ]

> Chain of custody is what makes your findings defensible. Every time evidence
> changes hands or is acted on, add a row. Never leave a gap. See
> `labctl learn m6`.

## Evidence item

| Field | Detail |
|-------|--------|
| Item ID | [e.g. EVID-001] |
| Description | [e.g. disk image evidence.img from workstation FIN-03] |
| Source | [where/what it came from] |
| Date/time collected | [YYYY-MM-DD HH:MM TZ] |
| Collected by | [name] |
| Acquisition method | [e.g. forensic image, write-blocked] |
| **SHA-256 at acquisition** | [paste full hash] |

## Integrity verification

| Checkpoint | Date/time | SHA-256 | Matches acquisition? | By |
|------------|-----------|---------|----------------------|----|
| Before analysis | [ ] | [ ] | [yes/no] | [ ] |
| After analysis | [ ] | [ ] | [yes/no] | [ ] |

## Custody log (one row per transfer or action)

| # | Date/time | Released by | Received by | Purpose / action | Storage location |
|---|-----------|-------------|-------------|------------------|------------------|
| 1 | [ ] | [ ] | [ ] | Acquisition | [ ] |
| 2 | [ ] | [ ] | [ ] | [analysis] | [ ] |
| 3 | [ ] | | | | |

## Attestation

I certify that the above record is accurate and the evidence was handled without
unauthorised alteration.

Signature: ______________________   Name: [ ]   Date: [ ]

---

## Self-check before you submit

- [ ] The acquisition hash is recorded, and **before/after** hashes both **match**.
- [ ] Every transfer or action has a custody row — **no gaps** in the chain.
- [ ] I analysed a **copy/image**, never the original.
- [ ] Times carry a **timezone**; names are real, not "me".

## Worked example (reference — fictional "Adom Microfinance Ltd")

| Field | Detail |
|-------|--------|
| Item ID | EVID-001 |
| Description | Forensic image `evidence.img` from workstation **FIN-03** |
| Date/time collected | 2026-10-07 09:14 GMT |
| Collected by | A. Mensah (IR analyst) |
| Acquisition method | Bit-for-bit image, write-blocked |
| SHA-256 at acquisition | `9f2c…` (full 64-hex) |

**Integrity:** before analysis `9f2c…` ✓ matches; after analysis `9f2c…` ✓ matches.
**Custody log:** (1) 09:14 acquired by A. Mensah → evidence safe; (2) 10:02
released to A. Mensah for analysis on the **copy** → returned 12:30; (3) 12:35
sealed, stored in the locked evidence cabinet. *No gaps — the record is
defensible.*
