# Executive Cyber Risk Memo — Module 9 Deliverable

**To:** [Board / Executive Committee]  **From:** [your name, role]
**Date:** [YYYY-MM-DD]  **Re:** [subject]  **Length target: ONE page.**

> Write for decision-makers, not engineers. Lead with the decision you need.
> Use business language and the board metrics — not CVE numbers. See
> `labctl learn m9`.

## Decision required

[State in one or two sentences exactly what you are asking the board to decide,
approve or fund.]

## Situation (3–4 sentences)

[What is happening / the risk, in business terms — money, trust, legal, safety,
continuity.]

## Where we stand — the metrics that matter

| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| MFA adoption (% accounts) | [ ] | [ ] | [↑/↓/→] |
| Patch compliance (critical, within SLA) | [ ] | [ ] | [ ] |
| Mean Time to Detect (MTTD) | [ ] | [ ] | [ ] |
| Mean Time to Respond (MTTR) | [ ] | [ ] | [ ] |
| Phishing-sim failure rate | [ ] | [ ] | [ ] |
| Last verified backup restore | [date/result] | [ ] | [ ] |

## Options & recommendation

| Option | Cost / effort | Risk reduction | Recommend? |
|--------|---------------|----------------|------------|
| [A] | [ ] | [ ] | [✔/—] |
| [B] | [ ] | [ ] | [ ] |

**Recommendation:** [one clear sentence.]

## If we do nothing

[The residual risk the board is choosing to accept — named owner, review date.]

---

## Worked example (reference — fictional "Adom Microfinance Ltd")

**To:** Board Risk Committee **From:** CISO **Re:** Fund MFA + payment-verification before Q1 close

**Decision required:** approve GHS 180,000 to deploy MFA on all remote access and a dual-control payment-verification process this quarter.

**Situation:** BEC against West African microfinance is rising; our VPN has no MFA and payments need no second-person callback. A single compromised credential or spoofed supplier email could cause a six-figure loss and DPC-reportable breach.

| Metric | Current | Target |
|--------|---------|--------|
| MFA adoption | 22% | 100% |
| Last verified backup restore | none (untested) | monthly pass |
| Phishing-sim failure rate | 31% | <10% |

**Recommendation:** approve both controls now — together they address our two highest residual risks (M2 #1 and #2) for < one-tenth of a plausible single-incident loss.

**If we do nothing:** the board accepts a high-likelihood, high-impact fraud/breach risk — owner CFO, review at Q1 close.
