# Cyber Risk Register — Module 2 Deliverable

**Institution:** [name]  **Prepared by:** [your name]  **Date:** [YYYY-MM-DD]
**Review cycle:** [e.g. quarterly]

> How to use this. Fill in at least **eight** risks. Write each as an IF/THEN
> statement in business terms. Score **Likelihood (L)** and **Impact (I)** 1–5.
> **Inherent** = score with no controls; **Residual** = score after the controls
> you list. Every risk needs a named **Owner**, a **Treatment** (Mitigate /
> Transfer / Avoid / Accept) and a **Review date**. See `labctl learn m2`.

Scoring key — Likelihood: 1 rare · 2 unlikely · 3 possible · 4 likely · 5 almost
certain. Impact: 1 negligible · 2 minor · 3 moderate · 4 major · 5 severe.
Rating = L × I (1–25).

| # | Risk statement (IF threat exploits vulnerability THEN business consequence) | Inherent L×I | Existing / planned controls | Residual L×I | Treatment | Owner | Review |
|---|------------------------------------------------------------------------------|-------------|------------------------------|--------------|-----------|-------|--------|
| 1 | *Example:* IF an attacker exploits our internet-facing unpatched VPN THEN citizen records are stolen and we face DPC penalties + loss of trust | 4×5 = 20 | Patch SLA, MFA on VPN, monitoring | 2×5 = 10 | Mitigate | Head of IT | 2026-01-15 |
| 2 | [FILL IN] | [ ]×[ ] | [ ] | [ ]×[ ] | [ ] | [ ] | [ ] |
| 3 | [FILL IN] | | | | | | |
| 4 | [FILL IN] | | | | | | |
| 5 | [FILL IN] | | | | | | |
| 6 | [FILL IN] | | | | | | |
| 7 | [FILL IN] | | | | | | |
| 8 | [FILL IN] | | | | | | |

## Top 3 risks by residual rating (what leadership must act on first)

1. [risk # and one line on the decision needed]
2. [ ]
3. [ ]

## Accepted risks (must have owner + review date)

- [risk # — why it is being accepted, by whom, review date] — *acceptance without
  accountability is negligence.*

## 90-day treatment backlog

| Action | Addresses risk # | Owner | Target date | Cost / effort |
|--------|------------------|-------|-------------|---------------|
| [FILL IN] | | | | |

## Quantify your top risk in money (FAIR)

Pick your #1 risk and turn it into an annual loss exposure a board can weigh
against a spend. **ALE = Loss Event Frequency × Loss Magnitude.**

- Risk chosen: [ ]
- Loss Event Frequency (how many successful events per year): [ ]
- Loss Magnitude per event (GHS): primary [funds/recovery] + secondary [fines/trust] = [ ]
- **Annual Loss Exposure (ALE) = GHS [ ]** (most likely), range GHS [ ] – [ ]
- Cost of the control that reduces it: GHS [ ] → **is the spend justified?** [yes/no, why]

> You can do this exercise on the **Sankofa Rural Bank** case (`labctl start m2`)
> or on your own institution.

---

## Worked example (reference — fictional "Adom Microfinance Ltd")

| # | Risk statement | Inherent L×I | Controls | Residual L×I | Treatment | Owner | Review |
|---|----------------|--------------|----------|--------------|-----------|-------|--------|
| 1 | IF an attacker exploits our internet-facing VPN (no MFA) THEN member records are stolen → DPC penalties + trust loss | 4×5=20 | Patch SLA, MFA, DNS monitoring | 2×5=10 | Mitigate | Head of IT | 2026-01-15 |
| 2 | IF a finance officer actions a spoofed supplier email THEN funds are wired to a mule account | 4×4=16 | Dual-control + callback on known number | 2×4=8 | Mitigate | CFO | 2026-01-31 |
| 3 | IF ransomware encrypts the core banking server AND backups THEN multi-day outage + data loss | 3×5=15 | 3-2-1 backups, monthly restore test, segmentation | 2×4=8 | Mitigate | Head of IT | 2026-02-15 |
| 4 | IF a laptop with member PII is lost unencrypted THEN confidentiality breach + notification | 3×3=9 | Full-disk encryption, remote wipe | 1×3=3 | Mitigate | Ops Manager | 2026-02-28 |

**Top 3 by residual:** #1 (fund the MFA rollout now), #2 (mandate callback before the next payment run), #3 (verify the restore test).

**Accepted risk:** #5 — legacy reporting tool cannot support MFA; compensating control = IP allow-list; accepted by **CFO**, review **2026-03-31**.

**90-day backlog:** MFA on VPN (IT, wk 2) · dual-control payment policy (CFO, wk 3) · first monthly restore test (IT, wk 4) · laptop encryption rollout (Ops, wk 8).
