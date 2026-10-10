# Master Glossary

Every key term from the programme in one place. Terms are grouped A–Z; the module
where each is taught in depth is noted where useful. Use your reader's search
(the web app's search box, or `/term` in `less`) to jump to one.

---

## A

- **Actionability** — the test of good intelligence: does it change a decision? *(M1)*
- **Alignment (DMARC)** — the authenticated sending domain matching the visible `From:`; what actually catches display-name spoofing. *(M1, M5)*
- **APT (Advanced Persistent Threat)** — a well-resourced, persistent actor, usually nation-state. *(M1)*
- **Authentication / Authorisation** — proving *who* you are / deciding *what* you may do. *(M3)*
- **Authenticity** — assurance a message/entity is genuinely what it claims. *(M1)*
- **Autopsy / Sleuthkit** — the GUI / command-line toolkit for disk forensics. *(M6)*

## B

- **Backdoor** — a hidden listening port/service an attacker uses to return. *(M3)*
- **BEC (Business Email Compromise)** — fraud by email impersonation; usually no malware. *(M5)*
- **Beaconing** — malware's regular, fixed-interval check-ins with its controller. *(M3)*
- **BLUF (Bottom Line Up Front)** — put the decision/conclusion first in a brief. *(M1)*
- **bulk_extractor** — carves URLs, emails, IPs and more from a disk/RAM image. *(M6)*

## C

- **C2 (Command & Control)** — the channel malware uses to receive orders. *(M3)*
- **CERT-GH** — Ghana's national cyber incident-response team, under the CSA. *(M8)*
- **Chain of custody** — the documented handling history that makes evidence defensible. *(M6)*
- **CIA(A)(C)** — Confidentiality, Integrity, Availability (+ Authenticity, + Continuity). *(M1)*
- **CII (Critical Information Infrastructure)** — systems designated critical under Act 1038. *(M8)*
- **Cialdini's principles** — authority, urgency/scarcity, social proof, liking, reciprocity. *(M5)*
- **CISA KEV** — catalogue of vulnerabilities **known to be actively exploited**. *(M4)*
- **Containment** — stopping the spread of an incident *without destroying evidence*. *(M6)*
- **Controller / Processor** — decides why/how data is used / processes it on the controller's behalf. *(M8)*
- **Correlation** — linking separate events by a shared indicator into one incident. *(M4, M10)*
- **CSA (Cyber Security Authority)** — Ghana's cybersecurity regulator (Act 1038). *(M8)*
- **CVE / CVSS** — a vulnerability's catalogue id / its 0–10 severity score. *(M4)*
- **CyberChef** — an offline tool for building multi-step decode recipes. *(M6)*

## D

- **DKIM** — a cryptographic signature proving an email was not altered in transit. *(M1, M5)*
- **DMARC** — the published policy (and alignment) tying SPF/DKIM to the visible sender. *(M1, M5)*
- **Deepfake** — AI-generated synthetic video or audio. *(M7)*
- **Defence in depth** — layered controls so one failure is not fatal. *(M3)*
- **Diamond Model** — intrusion analysis across Adversary–Capability–Infrastructure–Victim. *(M1)*
- **Dual control** — no single person both initiates and approves a payment. *(M5)*

## E

- **EPSS** — predicted probability a CVE will be exploited in the next 30 days. *(M4)*
- **Eradication** — removing the attacker: close the vector, reset creds, kill persistence. *(M6)*
- **Excessive agency** — an AI with more tool access/autonomy than it safely needs. *(M7)*
- **exiftool** — reads a file's embedded metadata (author, dates, timezone). *(M5, M6)*

## F

- **FAIR** — a model expressing cyber risk in money (loss frequency × magnitude). *(M2)*
- **Fraud Triangle** — fraud needs pressure + opportunity + rationalisation. *(M5)*

## G

- **GDPR** — the EU data-protection regulation; the global benchmark. *(M8)*
- **gobuster** — brute-forces hidden web paths/content against a wordlist. *(M4)*
- **GOVERN** — the central NIST CSF 2.0 function; board accountability for cyber. *(M2, M9)*
- **Governance vs management** — setting direction & demanding assurance / running it day to day. *(M9)*

## H

- **Hash (SHA-256)** — a file's one-way cryptographic fingerprint; proves integrity. *(M0, M6)*
- **Hashcat / John the Ripper** — offline password-hash crackers (GPU / CPU). *(M4)*
- **Hydra** — online password guesser against a live service (SSH, web). *(M4)*

## I

- **IOC / IOA** — Indicator of Compromise (an artefact) / of Attack (a behaviour). *(M1)*
- **Image (forensic)** — a bit-for-bit copy of storage you analyse instead of the original. *(M6)*
- **Indirect prompt injection** — a malicious instruction hidden inside content an AI ingests. *(M7)*
- **Inherent / Residual risk** — exposure before / after controls. *(M2)*
- **Inject** — a scripted event introduced during an exercise. *(M10)*
- **inode** — a file's internal id within a filesystem. *(M6)*

## J–L

- **jq** — a command-line JSON processor; used to triage the Wazuh alert feed. *(M4)*
- **Jitter** — deliberate random variation in beacon timing, to evade detection. *(M3)*
- **Kill Chain** — Lockheed Martin's seven-stage model of an intrusion. *(M1)*
- **LISTEN / ESTABLISHED** — a socket awaiting connections / an active connection. *(M3)*
- **LLM01** — Prompt Injection; the top OWASP risk for LLM applications. *(M7)*
- **Locard's exchange principle** — every contact leaves a trace. *(M6)*

## M

- **Masquerading (T1036)** — malware named to impersonate a trusted process (e.g. `svch0st`). *(M3, M6)*
- **MFA** — multi-factor authentication; SMS OTP is weakest, FIDO2/passkeys strongest. *(M3)*
- **MITRE ATT&CK / ATLAS** — catalogues of adversary techniques for IT / for AI-ML systems. *(M1, M7)*
- **MTTD / MTTR** — mean time to detect / to respond. *(M4)*
- **Minimisation / Retention** — collect only what's needed / keep only as long as needed. *(M8)*

## N

- **NIST AI RMF** — AI governance framework: Govern, Map, Measure, Manage. *(M7)*
- **NIST CSF 2.0** — Govern, Identify, Protect, Detect, Respond, Recover. *(M2, M9)*
- **NIST SP 800-30 / 800-61** — risk-assessment guide / incident-response lifecycle. *(M2, M6)*
- **Nmap / NSE** — the network scanner / its scripting engine for targeted checks. *(M3)*

## O

- **Order of volatility (RFC 3227)** — collect the most perishable evidence (RAM) first. *(M6)*
- **OSI / TCP-IP** — the layer models that locate where an attack and its control live. *(M3)*
- **Out-of-band verification** — confirming via a separate, pre-established trusted channel. *(M5, M7)*
- **OWASP LLM Top 10** — the application-security checklist for LLM systems. *(M7)*

## P

- **PAM (Privileged Access Management)** — just-in-time, vaulted, recorded admin access. *(M3)*
- **Password spray** — trying one common password across many accounts to dodge lockout. *(M4)*
- **PICERL** — Prepare, Identify, Contain, Eradicate, Recover, Lessons-learned. *(M6)*
- **Policy hierarchy** — Policy → Standard → Procedure → Guideline. *(M9)*
- **Premeditation** — proof a fraud was prepared in advance (e.g. file created before sent). *(M5)*
- **Prompt injection** — overriding an AI's instructions via crafted input. *(M7)*
- **Pyramid of Pain** — how much detecting an indicator hurts the attacker; aim for TTPs. *(M1)*

## R

- **RAG / data poisoning** — tampering with an AI's knowledge base so it serves false "facts". *(M7)*
- **Ransomware** — malware that encrypts data for extortion; ATT&CK T1486. *(M6, M10)*
- **Risk appetite / tolerance** — risk the organisation will take / acceptable variation on one risk. *(M2)*
- **RTO / RPO** — maximum acceptable downtime / data loss per critical service. *(M2, M9)*

## S

- **Segmentation** — dividing a network so a breach in one zone can't reach another. *(M3)*
- **Shadow AI** — unsanctioned use of AI tools with corporate data. *(M7)*
- **SIEM / SOAR** — alert aggregation & rules / automated response. *(M4)*
- **SIM swap** — hijacking a phone number to steal its SMS one-time codes. *(M5)*
- **SOC (Security Operations Centre)** — the team watching alerts (Tiers 1/2/3). *(M4)*
- **SPF** — checks whether a sending server is authorised to send for a domain. *(M1, M5)*
- **SS7** — legacy telecom signalling with interception weaknesses behind some MoMo fraud. *(M5)*
- **strings** — extracts human-readable text from a binary or memory image. *(M0, M6)*

## T

- **Thread hijack** — reusing a real PO number / quoting a genuine email to ride existing trust. *(M5)*
- **Threat / Vulnerability** — the actor or event / the weakness it exploits. *(M1, M2)*
- **Triage** — classifying each alert True Positive / False Positive / needs-investigation. *(M4)*
- **TTPs** — Tactics, Techniques & Procedures; the durable top of the Pyramid of Pain. *(M1)*

## U–Z

- **Unsalted MD5** — a fast, broken password-storage scheme (`-m 0` in hashcat). *(M4)*
- **Vishing** — voice phishing (e.g. "confirm your MoMo PIN"). *(M5)*
- **Wazuh** — the SIEM whose JSON alert feed you triage with `jq`. *(M4)*
- **Wireshark / tcpdump** — the packet analyser / command-line capture tool. *(M3)*
- **Zero Trust** — never trust, always verify; assume the attacker is already inside. *(M3)*
- **3-2-1 rule** — 3 backup copies, 2 media types, 1 offsite/offline. *(M6)*
