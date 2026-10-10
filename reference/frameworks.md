# Frameworks Quick-Reference

The models you are expected to speak in — on the job, in an exam, and to a board.
Each card is the structure plus the one-line "why it matters". For the full
treatment, see the module noted on each.

::: note | How to use this
These are *lenses*, not checklists. A strong analyst names several at once:
*where* in the intrusion (Kill Chain), *which* technique (ATT&CK), *how* to pivot
(Diamond), *how durable* the indicator (Pyramid of Pain), and *who* is accountable
(CSF). Introduced in **Module 1**; governance frameworks in **Modules 2 & 9**; AI
frameworks in **Module 7**.
:::

---

## The five security properties — CIA(A)(C)

Everything in security reduces to protecting these. Name the one that is
threatened *before* you assess anything. *(Module 1)*

| Property | Meaning | Example breach |
|----------|---------|----------------|
| **Confidentiality** | Only authorised parties can read it | Customer database exfiltrated |
| **Integrity** | Data is accurate and untampered | A payment account number silently changed |
| **Availability** | Usable when needed | DDoS takes mobile banking offline |
| **Authenticity** | An entity/message is genuinely what it claims | A forged "CEO" email authorises a transfer |
| **Business continuity** | The organisation can sustain/restore operations | Ransomware encrypts servers *and* backups |

---

## The Cyber Kill Chain (Lockheed Martin)

Seven sequential stages; the adversary must complete every one, so **disrupting
any stage breaks the chain — and the earlier, the cheaper.** *(Module 1)*

1. **Reconnaissance** — gather target info (passive; run it on yourself first)
2. **Weaponization** — build the weapon (malicious doc, exploit)
3. **Delivery** — the weapon reaches the target (richest detection signal)
4. **Exploitation** — it executes (macro runs, credential submitted)
5. **Installation** — persistence established
6. **Command & Control (C2)** — the implant calls home
7. **Actions on Objectives** — exfiltration, ransomware, fraud

---

## MITRE ATT&CK — the 14 enterprise tactics

Tactics are the adversary's *why* (`TA####`); techniques are the *how* (`T####`,
with sub-techniques like `T1566.002`). This is the shared vocabulary of modern
defence. *(Module 1; used in every lab)*

| Tactic | ID | Tactic | ID |
|--------|----|--------|----|
| Reconnaissance | TA0043 | Credential Access | TA0006 |
| Resource Development | TA0042 | Discovery | TA0007 |
| Initial Access | TA0001 | Lateral Movement | TA0008 |
| Execution | TA0002 | Collection | TA0009 |
| Persistence | TA0003 | Command & Control | TA0011 |
| Privilege Escalation | TA0004 | Exfiltration | TA0010 |
| Defense Evasion | TA0005 | Impact | TA0040 |

**Techniques you meet in this course:** T1566 Phishing · T1598 Phishing for Info ·
T1046 Network Service Discovery · T1071.004 C2 over DNS · T1036 Masquerading ·
T1110 Brute Force · T1053 Scheduled Task/Job · T1059.001 PowerShell · T1078 Valid
Accounts · T1041 Exfiltration over C2 · T1486 Data Encrypted for Impact · T1656
Impersonation.

::: key | MITRE ATLAS — ATT&CK for AI
When the target is an AI/ML system, the equivalent catalogue of adversary
tactics is **MITRE ATLAS** (evasion, poisoning, model extraction, prompt
injection). *(Module 7)*
:::

---

## The Diamond Model (Caltagirone, Pendergast & Betz)

Every intrusion event has four linked vertices; pivot from any one to find the
others. *(Module 1)*

**Adversary** ◄──► **Capability** (their tooling) · **Infrastructure** (their
C2/domains) · **Victim** (you). Find a C2 domain (infrastructure) and you can
pivot to other victims using it, or to the capability it serves.

---

## The Pyramid of Pain (David Bianco)

How much it *hurts the attacker* when you detect/block at each level. Aim high.
*(Module 1)*

| Level | Indicator | Pain to attacker |
|-------|-----------|------------------|
| bottom | Hash values | Trivial — recompile |
| | IP addresses | Easy — rotate |
| | Domain names | Simple — re-register |
| | Network/host artefacts | Annoying |
| | Tools | Challenging |
| **top** | **TTPs** (how they operate) | **Maximum — forces re-training** |

---

## NIST Cybersecurity Framework 2.0 (2024)

Six functions; **GOVERN** (new in 2.0) sits at the centre — cybersecurity is now
explicitly a **board accountability**. Build a current/target *profile* against
each. *(Modules 2 & 9)*

**GOVERN** (strategy, policy, risk appetite) · **IDENTIFY** (assets, risks) ·
**PROTECT** (safeguards: MFA, patching, training) · **DETECT** (SIEM, alerts) ·
**RESPOND** (tested plan) · **RECOVER** (tested backups, improvement).

---

## Risk management — the vocabulary

*(Module 2)* **Inherent risk** (before controls) → **Residual risk** (after); the
gap is your controls' value. **Risk appetite** (how much you'll take) vs
**tolerance** (variation allowed). Four treatments: **Mitigate · Transfer · Avoid
· Accept** (accept only with a named owner + review date). Quantify big decisions
with **FAIR** (loss exposure in money). Standards: **NIST SP 800-30**, **ISO
27005**, **ISO 31000**.

---

## Incident response — NIST SP 800-61 / PICERL

The lifecycle that keeps a panicked response from destroying evidence. *(Module
6; applied in 8 & 10)*

**P**reparation → **I**dentification/Detection → **C**ontainment (isolate, don't
power off) → **E**radication → **R**ecovery (verified-clean backups) → **L**essons
learned. Collect evidence by the **order of volatility (RFC 3227): memory → network
→ disk → archival.** Backups follow **3-2-1** (3 copies, 2 media, 1 offline),
tested monthly.

---

## OWASP Top 10 for LLM Applications (2025)

The application-security checklist for anything you build on an LLM. *(Module 7)*

| ID | Risk | ID | Risk |
|----|------|----|------|
| LLM01 | Prompt Injection | LLM06 | Excessive Agency |
| LLM02 | Sensitive Information Disclosure | LLM07 | System Prompt Leakage |
| LLM03 | Supply Chain | LLM08 | Vector & Embedding Weaknesses |
| LLM04 | Data & Model Poisoning | LLM09 | Misinformation |
| LLM05 | Improper Output Handling | LLM10 | Unbounded Consumption |

::: key | The AI governance pair
Govern AI with the **NIST AI RMF** — four functions: **Govern, Map, Measure,
Manage** (the AI parallel to the CSF). The management-system standard is **ISO/IEC
42001**. *(Module 7)*
:::

---

## Diamond vs Kill Chain vs ATT&CK — when to reach for which

- **Kill Chain** — *where* in the intrusion are we? (stage → which control)
- **ATT&CK** — *what* exactly did they do? (precise, shareable technique IDs)
- **Diamond** — *how* do I pivot from one artefact to the rest of the campaign?
- **Pyramid of Pain** — *how durable* is the indicator I'm about to block?

A professional report uses all four together.
