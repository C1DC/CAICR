# Vulnerability Remediation Register & SOC Case Ticket — Module 4 Deliverable

**Analyst:** [your name]  **Date:** [YYYY-MM-DD]  **Authorised targets:** 10.13.4.10, 10.13.4.20

> Two deliverables from one investigation: a **remediation register** that
> prioritises by more than CVSS, and a **SOC case ticket** that correlates the
> alert feed into one incident. See `labctl learn m4`.

---

## Part A — Remediation Register

*Prioritise by severity **and** active exploitation (CISA KEV), exposure and
asset criticality — not CVSS alone.*

| # | Finding (from Nikto / scan / loot) | CVSS | In KEV? | Exposure | Asset criticality | Priority | Fix | Owner | Target date |
|---|------------------------------------|------|---------|----------|-------------------|----------|-----|-------|-------------|
| 1 | *Example:* config.php.bak leaks DB password | — | — | Internet | High | **High** | Delete file; rotate credential | IT | [ ] |
| 2 | [FILL IN] | | | | | | | | |
| 3 | [FILL IN] | | | | | | | | |
| 4 | [FILL IN] | | | | | | | | |
| 5 | [FILL IN] | | | | | | | | |

**Priority rule of thumb:** internet-facing + KEV + critical asset = do first,
even at a lower CVSS.

**Credential findings (from cracking):**

- Password storage scheme observed: [ ] — *why it is weak:* [ ]
- Accounts cracked (do **not** paste full plaintext in a shared doc — note count + strength): [ ]
- Single control that would make these cracks harmless: [ ]

---

## Part B — SOC Triage Case Ticket

**Ticket ref:** [ ]  **Analyst:** [your name]  **Opened:** [date/time]

| Field | Detail |
|-------|--------|
| Alert(s) involved | [rule IDs / descriptions] |
| Source IP (correlating indicator) | [ ] |
| Highest Wazuh rule level | [ ] |
| Correlation — the one-paragraph story | [how the alerts link: scan + brute force + success + escalation + persistence, all from one IP] |
| Classification | [True Positive / False Positive / Needs Investigation] |
| Did the attacker succeed? | [evidence — e.g. auth success after the failures] |
| Persistence established? | [e.g. root cron job → T1053.003] |
| ATT&CK techniques | [e.g. T1110 Brute Force, T1053 Scheduled Task/Job] |
| Containment action | [e.g. block IP, disable account, kill cron, rotate creds] |
| Escalated to | [Tier 2/3 / IR lead] |
| Status | [open / contained / closed] |

### Evidence timeline

[Key log lines in time order that justify the classification — the proof.]

---

## Self-check before you submit

- [ ] Every priority in Part A reflects **KEV + exposure + criticality**, not just CVSS.
- [ ] The cracked values are **my own** (randomised per student).
- [ ] Part B tells **one** story from the shared source IP, not a list of alerts.
- [ ] I stated plainly **whether the attacker got in** and **how they persisted**.
- [ ] I only touched 10.13.4.10 / 10.13.4.20 and the provided hashes.

## Grading rubric (100 pts)

| Band | Register & prioritisation (35) | Cracking & controls (25) | Correlation & "did it work?" (25) | Containment & ATT&CK (15) |
|------|-------------------------------|--------------------------|-----------------------------------|---------------------------|
| Excellent (full) | Findings prioritised by KEV+exposure+criticality, each with a fix/owner/date | Weakness named, cracks demonstrated, MFA/salting argued | One clear incident from the shared IP; success + persistence proven | Right containment steps; correct ATT&CK IDs |
| Adequate (~60%) | Mostly CVSS, some context | Cracks done, control argument thin | Alerts linked but story loose | Generic actions, partial ATT&CK |
| Weak (<40%) | CVSS-only list | "cracked some" with no reasoning | Alerts listed, not correlated | No containment / no ATT&CK |

---

## Worked example (reference — fictional "Adom Microfinance Ltd")

*Illustrative values — yours are randomised.*

**Part A (top items):** (1) `config.php.bak` leaks the live DB password —
internet-facing, High asset → **High**: delete, rotate credential (IT, this week).
(2) World-readable `/backup/db_dump.sql` with **unsalted-MD5** passwords —
Internet, High → **High**: remove, enforce salted bcrypt, force reset (IT).
(3) Exposed `/admin/` with weak auth — Internet, High → **High**: restrict + MFA.
(4) Outdated Apache modules (CVSS 7.5, **in KEV**) — **High** over an internal
CVSS 8.1 not in KEV: patch, then **verify**.

**Credentials:** storage = unsalted MD5 (identical passwords share a hash,
precomputed in seconds). Cracked: `admin` (a top-100 password) and `backup`
(`12345`); SSH `labuser` fell to Hydra. **One control makes all of this
harmless: phishing-resistant MFA.**

**Part B:** source IP **10.13.4.66** behind both the web scan and the SSH brute
force; highest rule level **12**. Story: scan (T1595) → dozens of failed SSH
logins (T1110) → **authentication SUCCESS** (rule 5715) from the same IP →
sudo-to-root → **new root cron job** (persistence, T1053.003). Classification:
**True Positive — intrusion succeeded and persisted.** Containment: block
10.13.4.66, disable `labuser`, remove the cron job, rotate all cracked creds,
escalate to IR lead. **BLUF:** *"An attacker brute-forced a weak SSH account, got
root and installed a cron backdoor — contain now; the host is owned."*
