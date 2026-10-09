# Claude Agent Handoff Instructions
## KAIPTC CyberLab Learning Environment — Continuation Brief

**Project:** KAIPTC CyberLab v1.0
**Owner:** David Asante / Cyber1Defense Communication Ltd
**Status:** Core platform complete. Modules M7–M9 missing. Several enhancements requested.

---

## Context

This is a self-contained browser-based learning platform (`cyberlab.html`) for a 5-day cybersecurity training course at KAIPTC (Kofi Annan International Peacekeeping Training Centre), Accra, Ghana. It runs entirely in the browser with no server. Read `ARCHITECTURE.md` for the full technical breakdown and data schemas.

The platform currently has:
- Day 1: M1 (Cybersecurity Fundamentals + Kali labs), M2 (AI in Cybersecurity)
- Day 2: M3 (Network Security — Nmap/Wireshark/tcpdump)
- Day 3: M4 (Vulnerability Management & SIEM — Nikto/Wazuh/Hydra/John)
- Day 4: M5 (BEC & Email Forensics), M6 (Digital Forensics — sha256sum/Autopsy/CyberChef)
- Day 5: M10 (CyberRange Capstone — all tools, 8 injects)

**Missing:** M7, M8, M9 (Days 4–5 gap — Incident Response, Risk Management, Governance)

---

## Priority 1 — Add Missing Modules M7, M8, M9

Read the `cyberlab.html` file fully. Locate the `COURSE` array in the `<script>`. Add three new module objects following the exact schema in ARCHITECTURE.md.

### M7 — Incident Response (Day 4 or Day 5)
**Topic:** Incident Response & Threat Hunting
**Kali Tools:** `wazuh` (already in TOOLS), `tcpdump`
**Theory sections:**
- NIST SP 800-61 Rev.3 IR lifecycle (Preparation → Detection → Containment → Eradication → Recovery → Lessons Learned)
- IR team roles and RACI
- Evidence preservation and chain of custody
- Ghana Cybersecurity Act 2020 (Act 1038) reporting obligations — 72-hour notification requirement

**Lab missions:**
1. Triage a Wazuh alert: `sudo wazuh-control status` + query alerts JSON
2. Capture live traffic during incident: `tcpdump -i eth0 -w /evidence/capture.pcap`
3. Preserve evidence with hash: `sha256sum /evidence/capture.pcap > /evidence/capture.pcap.sha256`

**Quiz (4 questions):**
- NIST IR phases order
- What to do first when you detect a breach
- Ghana Act 1038 reporting window
- Difference between containment and eradication

---

### M8 — Risk Management (Day 4 or Day 5)
**Topic:** Cybersecurity Risk Management & Compliance
**Kali Tools:** None (conceptual module)
**Theory sections:**
- NIST CSF 2.0 six functions: Govern, Identify, Protect, Detect, Respond, Recover
- Risk = Likelihood × Impact matrix
- NIST AI RMF — Map, Measure, Manage, Govern
- Ghana Data Protection Act 2012 (Act 843) — DPC registration, data minimisation, consent
- NIST SP 800-53 control families overview

**Lab missions (conceptual — no Kali terminal):**
1. Complete a risk register for a fictional Ghanaian bank scenario
2. Map a scenario to NIST CSF 2.0 functions
3. Identify Act 843 violations in a case study

**Quiz (4 questions):**
- NIST CSF 2.0 new function vs. CSF 1.1
- Risk formula
- Act 843 data subject rights
- NIST AI RMF purpose

---

### M9 — Cybersecurity Governance & Strategy (Day 5 morning, before Capstone)
**Topic:** Security Governance, Policy & Leadership
**Kali Tools:** None (conceptual module)
**Theory sections:**
- Difference between governance and management
- CISO role and board reporting
- Security policy hierarchy: Policy → Standard → Procedure → Guideline
- ISO/IEC 27001:2022 overview — ISMS clauses
- Third-party and supply chain risk
- Building a security culture

**Lab missions (conceptual):**
1. Draft a 5-clause Acceptable Use Policy for a Ghanaian organisation
2. Identify governance gaps in a scenario (board has no cybersecurity agenda item)
3. Map an organisation to ISO 27001 control domains

**Quiz (4 questions):**
- Governance vs. management distinction
- Policy hierarchy order
- ISO 27001 certification body
- What a CISO should report to the board

---

## Priority 2 — Enhancments

### A. Cybersecurity Glossary View
Add a fifth view `'glossary'` with a searchable list of ~50 terms.

Nav button label: `📖 Glossary`

Terms to include (add definitions):
OSINT, Threat Intelligence, IOC, TTPs, MITRE ATT&CK, Lateral Movement, Persistence, Exfiltration, C2, Phishing, Spear Phishing, BEC, Vishing, Pretexting, Social Engineering, SQL Injection, XSS, CSRF, CVE, CVSS, Zero-Day, Patch, Vulnerability, Exploit, Payload, Malware, Ransomware, Rootkit, Keylogger, Botnet, DDoS, MitM, ARP Spoofing, DNS Poisoning, SIEM, SOAR, EDR, XDR, Firewall, IDS, IPS, WAF, VPN, Zero Trust, MFA, PKI, TLS, Hashing, Salt, Digital Signature, Non-repudiation, Chain of Custody, Forensic Image, Incident Response, Playbook, RACI, Tabletop Exercise, Purple Team, Red Team, Blue Team, Penetration Test, CTF.

Add a search/filter input at the top. Filter terms in real time as user types.

---

### B. Facilitator Export
Add a button on the Dashboard view: **"Export Progress (JSON)"**

Clicking it creates and downloads a JSON file:
```json
{
  "exportDate": "2026-10-08",
  "completedMods": ["M1", "M2", "M3"],
  "quizScores": { "M1": 3, "M3": 4 },
  "totalModules": 10,
  "percentComplete": 30
}
```

This lets facilitators collect progress files from learners and compare manually.

For download, use this pattern (works in artifact sandbox):
```javascript
const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url; a.download = 'cyberlab_progress.json'; a.click();
URL.revokeObjectURL(url);
```

---

### C. Completion Certificate
When all 10 modules are complete, show a "Course Complete" banner on the Dashboard with a **"Print Certificate"** button.

The certificate should render as a styled `<div>` in the page that the learner can screenshot, containing:
- KAIPTC logo text (no image needed — styled text)
- Learner's name (prompt them to enter it on first completion)
- Course name: "Professional Certificate in Cybersecurity, AI & Digital Resilience"
- Completion date
- Facilitator name: "David Asante, Cyber1Defense Communication Ltd"

Note: `window.print()` is disabled in the artifact sandbox. Render the certificate as a visible in-page element styled to look like a certificate. The learner screenshots it.

---

### D. Inline Emoji Icons for Concepts
In `renderModule()`, the concept grid currently uses plain emoji. Replace with SVG icons for a more polished look. Use inline SVG only (no external icon libraries — the CDN allowlist is restricted).

---

## Technical Constraints for Claude Agent

1. **Single HTML file** — Keep everything in one `cyberlab.html`. No separate JS/CSS files.
2. **No external libraries beyond** `fonts.googleapis.com` — The artifact CSP blocks other CDN resources unless loaded from cdnjs.cloudflare.com, cdn.jsdelivr.net, unpkg.com, or code.jquery.com via `<script src>` only.
3. **No `window.print()`** — It does nothing in the artifact sandbox.
4. **No `alert()` / `confirm()` / `prompt()`** — Use in-page UI instead.
5. **No fetch to external URLs** — Only relative file fetches work in the sandbox.
6. **localStorage may throw** — Always wrap in try/catch.
7. **Test at ~400px width** — Must be fully responsive on mobile.
8. **Publish the updated file as an Artifact** — Use the Artifact tool with the same URL to update in place.

---

## How to Hand Off to Claude Agent

Copy this entire prompt and paste it to a new Claude session, then attach `cyberlab.html`:

---

**PASTE THIS TO CLAUDE AGENT:**

> I have a single-file HTML learning platform for a 5-day cybersecurity course at KAIPTC in Ghana. The file is `cyberlab.html`. I need you to:
>
> 1. Read the full file
> 2. Add three missing modules (M7 Incident Response, M8 Risk Management, M9 Governance) following the exact schema in the COURSE array — see the CLAUDE_AGENT_HANDOFF.md in this ZIP for full content specs
> 3. Add a Glossary view with ~50 searchable cybersecurity terms
> 4. Add a JSON export button on the Dashboard
> 5. Add a completion certificate display when all 10 modules are done
> 6. Publish the result as an updated Artifact
> 7. Also give me the updated HTML file to download
>
> Technical constraints: single HTML file, no external libraries except Google Fonts, no window.print(), no alert/confirm/prompt, mobile-responsive, localStorage wrapped in try/catch.
>
> Read ARCHITECTURE.md for the full schema and component reference.

---

**End of handoff instructions.**

