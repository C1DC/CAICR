# Ghana Cyber & Data Law — At a Glance

The two laws every practitioner in Ghana must know, the regulators behind them,
and what they require in practice. This is an orientation, **not legal advice** —
confirm current obligations and timelines with qualified counsel and the current
CSA/DPC directives. *(Full treatment in Module 8; governance in Module 9.)*

::: warning | The one rule that protects your career
Scanning, probing or attacking any system you do not **own** or have **written
authorisation** to test is a criminal offence under the **Cybersecurity Act 2020
(Act 1038)** — regardless of good intentions. In this course the only authorised
targets are the lab addresses on `10.13.x.x`. When in doubt, stop and ask.
:::

---

## The two laws

| | **Data Protection Act 2012 (Act 843)** | **Cybersecurity Act 2020 (Act 1038)** |
|---|---|---|
| Governs | Personal data | Cybersecurity |
| Regulator | **Data Protection Commission (DPC)** | **Cyber Security Authority (CSA)** |
| Applies to you if | You hold data about identifiable people (customers, citizens, staff) | You operate systems/services, especially designated critical ones |
| Headline duty | Protect personal data; register; be accountable | Secure systems; report incidents; be licensed where required |
| National team | — | **CERT-GH** (incident coordination, under the CSA) |

---

## Act 843 — Data Protection

**The principles.** Process data **lawfully** and for a stated **purpose**;
collect only what you need (**minimisation**); keep it **accurate** and
**secure**; keep it only as long as needed (**retention**); and be
**accountable** for all of it.

**Controller vs processor.**

- **Controller** — decides *why and how* data is processed (your institution).
  Carries the **primary legal liability**.
- **Processor** — processes it on the controller's behalf (cloud vendor, payroll
  bureau, outsourced IT).

::: key | Outsourcing the task never outsources the accountability
If your cloud vendor (a processor) misconfigures storage and leaks your
customers' data, **you** — the controller — answer to the DPC and to the data
subjects. This is the single most common misunderstanding among institutions
moving to the cloud.
:::

**Sensitive data** — health, biometrics, financial records, criminal history —
demands heightened protection and makes any breach far more serious.

**Registration.** If you hold personal data in Ghana you are almost certainly a
**data controller** and must register with the DPC. "We're too small to matter"
is not a legal position.

---

## Act 1038 — Cybersecurity

- Created the **Cyber Security Authority (CSA)**; established **CERT-GH**.
- **Licenses** cybersecurity service providers and professionals.
- Designates **Critical Information Infrastructure (CII)** — sectors whose
  disruption would harm national security, the economy or public safety
  (finance, energy, telecoms, health, government).
- Imposes **mandatory incident reporting** to the CSA/CERT-GH for CII operators —
  with timelines and formats you confirm against *current* CSA directives.
- Criminalises **unauthorised access, interception and interference** — the legal
  basis for the authorisation rule above.

::: key | Reporting is also a defensive act
Reporting an incident lets the CSA issue sector-wide warnings — which is exactly
what organised-crime groups are counting on you *not* to do. Silence protects the
attacker, not you.
:::

---

## The global benchmark — GDPR

Even when the EU **GDPR** does not directly bind you, clients, partners and
regulators increasingly assume its expectations:

- a **72-hour** breach-notification norm (to the regulator, once aware);
- **data-subject rights**: access, rectification, erasure, portability;
- **Data Protection Impact Assessments (DPIAs)** for high-risk processing;
- privacy **by design and by default**;
- fines up to **4% of global turnover**.

Enforcement (British Airways, Marriott) turned on *inadequate protection* —
regulators punish the failure to protect, not merely the fact of being attacked.

---

## Breach response — the first 72 hours

*(Module 8)* A disciplined order:

1. **Contain first, investigate second** — stop active access while *preserving
   evidence* (isolate, don't power off).
2. **Scope it** — what data, which systems, how many people, is the attacker still
   present?
3. **Triage notification** — scope and data **sensitivity** drive the obligation.
4. **Engage legal counsel** *before* any external communication.

::: warning | Do not communicate before counsel
The most damaging early move is a public statement that later proves wrong. Brief
qualified counsel before notifying regulators, customers or the press, and
confirm the *current* Act 843 notification obligation with them.
:::

---

## Who to contact

- **Personal-data breach / privacy** → Data Protection Commission (DPC) — dataprotection.org.gh
- **Cyber incident / CII** → Cyber Security Authority (CSA) & CERT-GH — csa.gov.gh
- **Financial fraud (BEC/MoMo)** → your bank's fraud desk **and** the above, immediately, to attempt recall.

*Always confirm current reporting timelines and thresholds with counsel and the
regulators' current directives.*
