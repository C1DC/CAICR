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

## 5. Reporting obligations considered

[Act 1038 CSA / Act 843 DPC questions — to confirm with counsel.]

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
