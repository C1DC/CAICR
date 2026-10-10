# Sankofa Rural Bank — DRAFT Risk Register (for review)

*A junior colleague drafted this register. It has several problems a good risk
officer must catch before it goes to the board. Review it critically — the checks
in `labctl verify m2` ask you to find the governance failures.*

Scoring: Likelihood (L) and Impact (I) are 1–5; Rating = L × I (1–25).
**Inherent** = before controls; **Residual** = after the listed controls.

| # | Risk statement | Inherent L×I | Controls in place | Residual L×I | Treatment | Owner | Review |
|---|----------------|--------------|-------------------|--------------|-----------|-------|--------|
| **R1** | IF an attacker exploits the internet-facing VPN (no MFA) THEN staff accounts and FinCore are reached → data theft + fraud | 4×5 = 20 | MFA rollout planned; patch SLA; monitoring | 2×5 = 10 | Mitigate | Head of IT | 2026-02-15 |
| **R2** | IF ransomware encrypts FinCore AND the backups THEN multi-day outage + data loss | 3×5 = 15 | Desktop antivirus | 3×5 = 15 | Mitigate | Head of IT | 2026-02-28 |
| **R3** | IF a finance officer actions a spoofed supplier email THEN funds are wired to a mule account | 4×4 = 16 | Dual-control + callback-on-known-number policy | 2×4 = 8 | Mitigate | *(blank)* | 2026-02-20 |
| **R4** | IF an unencrypted laptop with customer PII is lost THEN confidentiality breach + DPC notification | 3×3 = 9 | Full-disk encryption; remote wipe | 1×3 = 3 | Mitigate | Ops Manager | 2026-03-10 |
| **R5** | IF the legacy reporting tool (cannot support MFA) is abused THEN report data is exposed | 2×4 = 8 | IP allow-list | 2×4 = 8 | **Accept** | *(blank)* | *(none)* |
| **R6** | IF the public website is defaced THEN minor reputational embarrassment | 1×2 = 2 | Managed hosting, WAF | 1×2 = 2 | Mitigate | IT | 2026-04-01 — flagged **HIGH PRIORITY** |

---

## Problems to look for (the review skills this tests)

- **Negligent acceptance** — a risk marked *Accept* with **no named owner and no
  review date**. Acceptance without accountability is negligence, and a regulator
  will treat it as such.
- **Missing owner** — a risk with a treatment but **no one accountable**. A
  register without owners is a wish list.
- **Ineffective control** — a control that does **not** reduce the residual score
  below the inherent score (e.g. "desktop antivirus" against a backup-encrypting
  ransomware risk). The control–residual link must be real.
- **Mis-prioritisation** — a **low-rated** risk flagged as a top priority, pulling
  attention away from what actually matters.

*(The last column and the blanks are deliberate. Your job is to spot them.)*
