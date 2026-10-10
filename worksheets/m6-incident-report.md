# Incident Report (NIST SP 800-61) — Module 6 Deliverable

**Incident ref:** [ ]  **Author:** [your name]  **Date:** [YYYY-MM-DD]
**Severity:** [low / medium / high / critical]  **Status:** [open / contained / closed]

> Structure the report on the NIST lifecycle. State what you *know* vs what you
> *assess*. See `labctl learn m6`.

## 1. Executive summary (for leadership, non-technical)

[What happened, business impact, current status, what you need from leadership.]

## 2. Detection & analysis

- How detected: [ ]
- Scope — systems affected: [ ]  Data affected: [ ]  Users affected: [ ]
- Attacker still present? [yes/no/unknown]

## 3. Evidence manifest

| Item ID | Description | SHA-256 | Collected (date/by) |
|---------|-------------|---------|---------------------|
| [ ] | [ ] | [ ] | [ ] |

## 4. Attack timeline (reconstructed)

| Time | Event | Evidence source |
|------|-------|-----------------|
| [ ] | [first suspicious activity] | [ ] |
| [ ] | [persistence / access] | [ ] |
| [ ] | [exfiltration / impact] | [ ] |

## 5. Response actions

| Phase | Action taken | By | Date/time |
|-------|--------------|----|-----------|
| Containment | [isolate — NOT power off] | | |
| Eradication | [ ] | | |
| Recovery | [restore from verified clean backup] | | |

## 6. Root cause

[What made this possible — the underlying control gap, not just the symptom.]

## 7. Lessons learned / recommendations

1. [ ]
2. [ ]

**ATT&CK techniques observed:** [e.g. T1059.001 PowerShell, T1053 Scheduled Task]
**Reporting obligations considered:** [Act 1038 CSA / Act 843 DPC — confirm with counsel]

---

## Self-check before you submit

- [ ] The timeline is built from **evidence** (disk + memory + logs), each row sourced.
- [ ] I **correlated** across sources (e.g. the same VPN password on disk and in RAM).
- [ ] Containment says **isolate**, not power off.
- [ ] Root cause is the **control gap**, not just the symptom.
- [ ] I separated what I **know** from what I **assess**.

## Grading rubric (100 pts)

| Band | Detection & scope (20) | Evidence & integrity (20) | Timeline & correlation (35) | Response, root cause & ATT&CK (25) |
|------|------------------------|---------------------------|-----------------------------|-------------------------------------|
| Excellent (full) | Clear scope, attacker-present call | Manifest + matching hashes | Dated timeline across disk/memory/logs, correlated | Right phases; true root cause; correct ATT&CK & obligations |
| Adequate (~60%) | Partial scope | Hashes noted | Timeline from one source | Generic actions, shallow root cause |
| Weak (<40%) | Vague | No integrity proof | Events listed, not ordered/correlated | "Reinstall everything"; no ATT&CK |

## Worked example (reference — fictional "Adom Microfinance Ltd")

**Exec summary:** A finance workstation (FIN-03) was compromised via a
macro-enabled spreadsheet; the attacker gained VPN admin credentials and set
persistence. Contained same day; no confirmed data loss. *Need: funding for MFA
on VPN and email macro-blocking.*

**Timeline (correlated):** 09-28 attachment authored (PDF metadata) → 10-06
brute-force from **10.13.4.66** then `Accepted password` for **labuser**
(auth.log) → macro → PowerShell stager (memory) → `svch0st.exe` beaconing to C2
(memory + decoded artefact **agree**) → VPN password harvested (same value on
**disk and in RAM** — correlation) → `schtasks` persistence.

**Response:** contain = **isolate** FIN-03 (not power off), capture RAM then image
disk; eradicate = remove task, reset VPN/labuser creds, block C2 + source IP;
recover = rebuild from verified-clean backup, validate, reconnect.

**Root cause:** no MFA on VPN + macros allowed from email. **ATT&CK:** T1204.002,
T1059.001, T1036, T1053. **Obligations:** assess CSA (Act 1038) / DPC (Act 843)
notification with counsel.
