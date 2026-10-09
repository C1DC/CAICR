# Threat Intelligence Brief — Module 1 Deliverable

**Prepared by:** [your name]  **Date/time:** [YYYY-MM-DD HH:MM]
**Subject:** [e.g. Exposure assessment of lab-corp.com.gh]
**Classification:** [internal / restricted]

> A good brief separates **fact** from **assessment**, and every assessment
> carries a **confidence level** (low / medium / high). Never state a hypothesis
> as a fact. See `labctl learn m1`.

## 1. Bottom line up front (BLUF) — 2–3 sentences

[What a decision-maker must know first: the key finding and the recommended
immediate action.]

## 2. Verified indicators (facts)

| # | Indicator | Source / how verified | ATT&CK (if any) |
|---|-----------|------------------------|-----------------|
| 1 | *Example:* No DMARC record published for the domain | `dig TXT _dmarc.<domain>` → NXDOMAIN | T1590 |
| 2 | [FILL IN] | | |
| 3 | [FILL IN] | | |
| 4 | [FILL IN] | | |
| 5 | [FILL IN] | | |

## 3. Assessment (hypotheses — label confidence)

- [Finding] → *We assess …* **[confidence: low/med/high]** because [reasoning].
- [FILL IN]

## 4. Attacker's likely next step

[Given the exposure, what would an attacker do? e.g. spoof the domain to phish
the finance team, since SPF is weak and DMARC absent.]

## 5. Recommended immediate actions

1. [e.g. Publish a DMARC record with p=reject — free, blocks domain spoofing]
2. [ ]
3. [ ]

## 6. What we do NOT yet know

[Be explicit about gaps — this is what separates intelligence from guessing.]
