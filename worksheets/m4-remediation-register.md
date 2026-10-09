# Vulnerability Remediation Register — Module 4 Deliverable

**Analyst:** [your name]  **Date:** [YYYY-MM-DD]  **Target:** [e.g. 10.13.4.10]

> Prioritise by more than CVSS: combine severity with **active exploitation
> (CISA KEV)**, **exposure** and **asset criticality**. See `labctl learn m4`.

| # | Finding (from Nikto/scan) | CVSS | In KEV? | Exposure | Asset criticality | Priority | Fix | Owner | Target date |
|---|---------------------------|------|---------|----------|-------------------|----------|-----|-------|-------------|
| 1 | *Example:* config.php.bak leaks DB creds | — | — | Internet | High | **High** | Remove file; rotate creds | IT | [ ] |
| 2 | [FILL IN] | | | | | | | | |
| 3 | [FILL IN] | | | | | | | | |
| 4 | [FILL IN] | | | | | | | | |

**Priority rule of thumb:** internet-facing + KEV + critical asset = do first,
even at a lower CVSS.

---

# SOC Triage Case Ticket — Module 4 Deliverable

**Ticket ref:** [ ]  **Analyst:** [your name]  **Opened:** [date/time]

| Field | Detail |
|-------|--------|
| Alert(s) involved | [rule IDs / descriptions] |
| Source IP | [ ] |
| Highest severity level | [ ] |
| Correlation | [how the alerts link into one story — same source IP?] |
| Classification | [True Positive / False Positive / Needs Investigation] |
| Did the attacker succeed? | [evidence — e.g. auth success after brute force] |
| ATT&CK | [e.g. T1110 Brute Force] |
| Action taken | [ ] |
| Escalated to | [ ] |
| Status | [open / contained / closed] |

## Evidence / notes

[Timeline and key log lines that justify the classification.]
