# Data Breach Assessment — Module 8 Deliverable

**Prepared by:** [your name]  **Date:** [YYYY-MM-DD]  **Incident ref:** [ ]

> Work the first-72-hours order: **contain → scope → triage notification →
> counsel.** This assessment informs — it does not replace — legal advice. See
> `labctl learn m8`.

## 1. What happened

[Plain description of the breach.]

## 2. Classification

- Breach type: [ransomware / phishing / BEC / cloud misconfiguration / other]
- Data involved: [ ]  **Sensitive?** [health / biometric / financial / criminal — yes/no]
- Volume: [approx. number of records / individuals]
- Was data **exfiltrated** (left your control), or only exposed/encrypted? [ ]

## 3. Our role under Act 843

- Are we the **data controller** or **processor** for this data? [ ]
- (Remember: using a cloud vendor does **not** transfer your accountability.)

## 4. Containment & scoping actions taken

| Action | Date/time | By |
|--------|-----------|----|
| [e.g. removed public access / isolated host] | | |
| [preserved logs & evidence] | | |

## 5. Notification triage

| Question | Answer / status |
|----------|-----------------|
| Did personal data leave our control? | [ ] |
| Is the data sensitive? | [ ] |
| Are we (or is this) CII under Act 1038? | [ ] |
| Does this likely trigger DPC notification? | [confirm with counsel] |
| Do affected individuals likely need to be told? | [confirm with counsel] |

## 6. Questions for legal counsel (before any external communication)

1. [ ]
2. [ ]

## 7. Immediate remediation

[What stops this recurring — the control gap to close.]

---

## Worked example (reference — fictional hospital cloud exposure)

- **What happened:** a cloud repository of patient records was left publicly readable; access logs show 3 external downloads over 9 days.
- **Classification:** cloud misconfiguration → **confirmed exfiltration** (downloads observed). Data = **sensitive** (health). ~4,200 individuals.
- **Our role:** **data controller** (the vendor who ran the cloud is our processor — accountability stays with us).
- **Containment taken:** public access removed 11:20; access logs and bucket config preserved; snapshot hashed.
- **Notification triage:** personal + sensitive data left our control → DPC notification **likely required**; affected individuals **likely must be told** — *confirm timing/wording with counsel*.
- **Questions for counsel:** 1) Does the 9-day exposure + downloads trigger mandatory DPC notification now? 2) Individual-notification wording? 3) Any CII reporting duty to the CSA?
- **Immediate remediation:** enforce "private by default" bucket policy; add cloud-config monitoring; DPIA for the patient-records system.
