# Incident Dossier & 90-Day Roadmap — Module 10 Capstone Deliverable

**Team / name:** [ ]  **Date:** [YYYY-MM-DD]  **Exercise:** Operation Cyber Resilience

> The capstone deliverable pulls the whole week together: prove the attack story
> from evidence, show the decisions you made, and set the recovery path. See
> `labctl learn m10`.

## 1. Executive summary (for leadership)

[What happened, business impact, current status — 4–5 sentences.]

## 2. The attack story (correlation)

[Narrative tying the eight injects into ONE campaign. Name the shared indicator
(e.g. the foothold IP) that links them.]

| Inject | Time | Event | Evidence | ATT&CK |
|--------|------|-------|----------|--------|
| T+00 | 09:00 | Supplier payment-change email | payment-change.eml | T1566 |
| T+20 | 09:20 | Privileged login, unusual IP | Wazuh alerts | T1078 |
| T+40 | 09:40 | Internal host scanning | Wazuh / Nmap | T1046 |
| T+65 | 10:05 | Vendor bank details changed 48h ago | email / finance | T1565 |
| T+90 | 10:30 | Synthetic executive voice transfer order | — | T1656 |
| T+120 | 11:00 | Data exfiltration to unknown IP | pcap / Wazuh | T1041 |
| T+145 | 11:25 | Critical database offline (ransomware) | Wazuh | T1486 |
| T+160 | 11:40 | AI assistant leaks data via injected doc | — | — |

Key indicators — Foothold IP: [ ]  C2 domain: [ ]  Exfil destination IP: [ ]
Look-alike domain: [ ]  Highest alert severity: [ ]

## 3. Decision log (your crisis audit trail)

| Time | Decision | Made by | Rationale |
|------|----------|---------|-----------|
| [ ] | [e.g. isolate foothold host — NOT power off] | [IC] | preserve evidence |
| [ ] | [refuse & verify voice-note transfer via callback] | | likely deepfake |
| [ ] | [declare severity: ___] | | |

## 4. Response summary (NIST lifecycle)

- Containment: [ ]
- Eradication: [ ]
- Recovery priorities (RTO/RPO): [ ]

## 5. Reporting obligations & crisis communications

- **Reporting:** [Act 1038 CSA/CERT-GH · Act 843 DPC — questions for counsel]
- **Stakeholders briefed:** [board · staff · customers · regulator · bank · press]
- **Holding statement / spokesperson:** [one voice, confirmed facts only]

## 5b. After-action review (hotwash)

- **What went well:** [ ]
- **What didn't:** [ ] *(blameless — systems, not scapegoats)*
- **True root cause (five whys past the symptom):** [ ]

## 6. 90-Day resilience roadmap

| # | Action | Addresses | Owner | Target | CSF function |
|---|--------|-----------|-------|--------|--------------|
| 1 | [FILL IN] | [inject/root cause] | | | [Govern/Identify/Protect/Detect/Respond/Recover] |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

## 7. Three lessons for the board

1. [ ]
2. [ ]
3. [ ]

---

## Self-check before you submit

- [ ] §2 tells **one** campaign story, not eight separate incidents.
- [ ] I proved the **signature correlation**: the BEC mule account == the AI's
      poisoned answer == tied to the foothold IP.
- [ ] My decision log shows **isolate (not power off)** and **callback-verify** the voice order.
- [ ] Every roadmap item maps to a **root cause** and a **CSF function**.
- [ ] I only touched 10.13.10.0/24.

## Grading rubric (100 pts)

| Band | Attack story & correlation (40) | Decisions & evidence (25) | Response & obligations (15) | Roadmap & board lessons (20) |
|------|----------------------------------|---------------------------|-----------------------------|------------------------------|
| Excellent (full) | All injects correlated into one campaign; signature link proven | Sound, timestamped, evidence-backed decisions | Correct NIST phases + Act 1038/843 considered | Prioritised, root-cause-linked, CSF-mapped |
| Adequate (~60%) | Most injects linked, signature link missed | Decisions made, thin rationale | Generic response | Generic actions |
| Weak (<40%) | Injects listed separately | Ad-hoc decisions, no log | Power-off / action the transfer | No roadmap |

---

## Worked example (reference — fictional "Adom Microfinance Ltd")

*Illustrative values — yours are randomised.*

**The story:** one adversary. A look-alike **zennith-supplies.com** email (T+00)
demanded payment to mule account **0123456789**; the bank's **AI assistant**,
asked about the supplier, returned the **same 0123456789** — its knowledge base
was **poisoned** (T+160). Meanwhile foothold **10.13.10.66** logged in with privilege
(T+20), scanned internally (T+40), beaconed to a dynamic-DNS C2, and exfiltrated to
**185.220.101.44** (T+120) before ransomware took the database (T+145). **The same
account appearing in the email and the AI proves it is one campaign.**

**Decisions (logged):** 11:02 **isolate** 10.13.10.66 (not power off) — preserve
RAM; 10:31 **refuse & callback-verify** the T+90 voice order on the MD's known
number (deepfake); 11:05 declare **High** severity; quarantine the poisoned AI KB.

**Response:** eradicate (reset cracked admin creds, remove persistence, clean KB);
recover ransomed DB from **offline** backup (RPO ≤ 24h, RTO ≤ 8h); assess CSA/DPC
notification. **Roadmap:** MFA everywhere (Protect) · DNS monitoring (Detect) ·
dual-control payments + callback (Protect/Govern) · AI KB change-control + least-
privilege tools (Govern) · monthly restore test (Recover).

**Board lessons:** (1) one callback would have stopped the fraud; (2) our own AI
was turned against us — govern it; (3) tested offline backups are what got us back.
