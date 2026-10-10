**All ten modules. Every tool. One crisis.**  ·  Day 5 · ~4.5 h · 15 graded tasks

::: note | What this lab is
A multi-vector attack is unfolding against a fictional Ghanaian institution. Your
team investigates the **live range** and the **evidence package**, reconstructs
the attack across **eight injects**, and drives the response — as both the
technical investigators and the decision-makers. The one skill being tested is
**correlation**: seeing the single adversary behind email, network and AI at once.
:::

## What's running

- **Live range on `10.13.10.0/24`** (launched for you): `.10` finance portal,
  `.20` records host, `.40` the bank's internal AI assistant.
- **Evidence package (`assets/`, personalised to you):** `capstone-alerts.json`
  (SIEM feed), `payment-change.eml` (the BEC), `capstone-capture.pcap` (the tap).
- **Four cells** work in parallel: Crisis Leadership · Technical Investigation ·
  Fraud/Finance · Legal/Privacy/Comms.

## How to use this lab

**In the GUI (this page):**
1. Click **Start**; wait for **● running** across the range.
2. In the **Terminal** tab, work the inject timeline and the evidence below.
3. Enter findings in the **Verify** panel → **Submit & grade**. This is your
   `labctl progress` finale.

**Prefer the terminal?** `labctl start m10` → investigate → `labctl verify m10`.

::: warning | The guards — read before you start
- Authorised scope is **`10.13.10.0/24` only**.
- The mule account, look-alike domain, C2 domain and admin password are
  **randomised to you** — and the lab makes the BEC account and the AI's poisoned
  account **identical**, so you can prove the correlation.
- Containment means **isolate, not power off** — preserve volatile evidence.
:::

## The inject timeline

| Inject | Event | Where to look |
|--------|-------|---------------|
| T+00 | Supplier payment-change email (urgent) | `payment-change.eml` — header forensics |
| T+20 | Privileged login, unusual IP, off-hours | `capstone-alerts.json` |
| T+40 | Internal host scanning (lateral movement) | alerts + `nmap` the range |
| T+65 | Vendor bank details changed 48h ago | email + finance review |
| T+90 | Synthetic executive **voicemail** orders a transfer | deepfake protocol |
| T+120 | **Data exfiltration** — large outbound to unknown IP | alerts + the capture |
| T+145 | Critical **database offline** (ransomware) | alerts |
| T+160 | AI assistant leaks data via an injected document | alerts |

## Work the evidence

```Terminal — one representative command per front
jq -r '.[].data.srcip // empty' assets/capstone-alerts.json | sort | uniq -c   # foothold IP
jq '[.[].rule.level] | max' assets/capstone-alerts.json                        # top severity
grep -iE '^(From|Reply-To|Return-Path)' assets/payment-change.eml              # BEC look-alike
wireshark assets/capstone-capture.pcap &     # filter: dns (C2) then the exfil burst
gobuster dir -u http://10.13.10.10 -w /usr/share/wordlists/dirb/common.txt     # leaked backup
curl http://10.13.10.40:8080/ask -d '{"question":"supplier bank account"}'     # poisoned AI
```

**The correlation that proves one campaign:** the mule account in the BEC email is
the **same** account the bank's own poisoned AI returns; the foothold IP recurs
across the SIEM injects; the C2 domain in the capture ties to the exfil IP.

## Drive the response

- **T+90 deepfake:** what verification step before any transfer?
- **Containment:** first action on the foothold `10.13.10.66` — *without*
  destroying volatile evidence.
- Map the **exfiltration** and the **ransomware** to MITRE ATT&CK.
- Leadership: declare severity, set RTO/RPO recovery priorities, and decide the
  Act 1038 / Act 843 reporting questions for counsel.

## What you'll be graded on

15 checks in the **Verify** panel spanning every inject and the response
decisions. Then assemble the capstone deliverable:

```Terminal
labctl verify m10
labctl worksheet m10   # incident dossier + 90-day resilience roadmap
```

::: key | Tips
- Don't triage the injects separately — they are **one campaign**; find the shared
  indicators (foothold IP, the shared mule account).
- "The system said so" is not verification when the AI itself was poisoned.
- Log every decision with a timestamp — in the debrief you're judged on the
  decision log as much as the findings.
:::
