# M10 — Operation Cyber Resilience (Capstone)

**All ten modules. Every tool. One crisis.** A multi-vector attack is unfolding
against a fictional Ghanaian institution. Your team investigates the live range
and the evidence package, reconstructs the attack across eight injects, and
drives the response.

**Live range:** `10.13.10.10` finance portal · `10.13.10.20` records host ·
`10.13.10.40` AI assistant.
**Evidence (`assets/`):** `capstone-alerts.json` (the SIEM feed),
`payment-change.eml` (the BEC), `capstone-capture.pcap` (the network tap).

Four cells work in parallel: **Crisis Leadership · Technical Investigation ·
Fraud/Finance · Legal/Privacy/Comms.**

---

## The inject timeline

| Inject | Event | Where to look |
|--------|-------|---------------|
| T+00 | Supplier payment-change email (urgent) | `payment-change.eml` — header forensics |
| T+20 | Privileged account login from unusual IP, off-hours | `capstone-alerts.json` |
| T+40 | Internal host scanning the network (lateral movement) | alerts + `nmap` the range |
| T+65 | Vendor bank details changed 48h ago — near-miss transfer | email + finance review |
| T+90 | Synthetic executive **voicemail** orders a wire transfer | deepfake protocol |
| T+120 | **Data exfiltration** — large outbound to unknown IP | alerts + `capstone-capture.pcap` |
| T+145 | Critical **database offline** (ransomware trigger) | alerts |
| T+160 | AI assistant leaks data via an injected document | alerts |

## Work the evidence

```
# SIEM: rank by severity, find the foothold, trace the exfil destination
$ jq -r '.[] | "\(.inject)\t\(.rule.level)\t\(.rule.description)"' assets/capstone-alerts.json
$ jq -r '.[].data.srcip // empty' assets/capstone-alerts.json | sort | uniq -c
$ jq '[.[].rule.level] | max' assets/capstone-alerts.json

# Email: prove the BEC look-alike domain
$ grep -iE '^(From|Reply-To|Return-Path|Received|Authentication)' assets/payment-change.eml

# Network: find the C2 beacon and the exfil burst
$ wireshark assets/capstone-capture.pcap &        # filter: dns   then   ip.addr==185.220.101.44

# Live range: confirm what's exposed
$ nmap -sn 10.13.10.0/24
```

## Drive the response

- **T+90 deepfake:** what verification step before any transfer?
- **Containment:** first action on the foothold `10.13.10.66` — *without*
  destroying volatile evidence (do not power it off).
- Map the **exfiltration** and the **ransomware** to MITRE ATT&CK techniques.
- Leadership cell: declare severity, set recovery priorities (RTO/RPO), and
  decide the Act 1038 / Act 843 reporting questions for counsel.

---

## Grade yourself

```
$ labctl verify m10
```
