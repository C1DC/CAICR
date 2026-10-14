# CAIC CyberLab — Curriculum Audit & Documentation

**Professional Certificate in Cybersecurity, AI & Digital Resilience**  
Kofi Annan International Peacekeeping Training Centre (KAIPTC) · Cyber1Defense Communication Ltd  
Five intensive days · 11 modules · *Generated 2026-10-13*

> **For external review.** This document is **auto-generated from the course repository** by `scripts/course_audit.py`. Every figure — word counts, topic lists, lab tasks, ATT&CK technique IDs, question counts — is read directly from the teaching files, lab manifests and assessment bank. It is not hand-written marketing; it can be regenerated and independently verified against the source at any time (see *How to verify* at the end).

---

## 1 · Summary

| Measure | Count |
|---------|-------|
| Modules (incl. Day-1 orientation) | 13 |
| Teaching lessons | 13 |
| Total lesson word count | ~79,545 words |
| In-lesson diagrams (SVG + ASCII) | 39 |
| Hands-on graded labs | 12 |
| Total graded lab tasks (checks) | 173 |
| Deliverable worksheet templates | 16 |
| Module knowledge-check quizzes | 11 (33 questions) |
| Final exam questions | 12 |
| Baseline diagnostic questions | 6 |

Every lab is **per-student randomised** (each student gets unique flags, credentials, IPs, accounts and figures), so answers cannot be copied and the labs are reusable across cohorts without leakage. All labs run on **isolated targets on the student's own machine** (addresses on `10.13.x.x`), never against third parties.

---

## 2 · Course at a Glance

| Module | Day | Title | Lesson | Lab (graded tasks) | Deliverables |
|--------|-----|-------|-------:|--------------------|--------------|
| **M0** | 1 | Orientation, Kali Linux & the Command Line | 5,913 w | — | — |
| **RT** | 1 | Red Team Primer — Your First Hack | 2,330 w | 10 tasks | 1 template(s) |
| **JS** | 1 | Web Attack Arena — OWASP Juice Shop | 1,423 w | 9 tasks | 1 template(s) |
| **M1** | 1 | Threat Landscape & Cyber Threat Intelligence | 5,617 w | 19 tasks | 1 template(s) |
| **M2** | 1 | Institutional Cyber Risk & Digital Resilience | 3,253 w | 17 tasks | 2 template(s) |
| **M3** | 2 | Network, Endpoint & Identity Security | 11,365 w | 16 tasks | 1 template(s) |
| **M4** | 2 | Vulnerability Management & SOC Operations | 8,744 w | 16 tasks | 1 template(s) |
| **M5** | 3 | Cyber Fraud, BEC & Mobile Money Security | 7,983 w | 13 tasks | 1 template(s) |
| **M6** | 3 | Digital Forensics & Incident Response | 7,803 w | 14 tasks | 2 template(s) |
| **M7** | 4 | AI Security, Deepfakes & Emerging Threats | 7,238 w | 12 tasks | 1 template(s) |
| **M8** | 4 | Data Protection, Privacy & Compliance | 6,301 w | 16 tasks | 2 template(s) |
| **M9** | 5 | Cyber Governance & Business Continuity | 5,324 w | 16 tasks | 2 template(s) |
| **M10** | 5 | Operation Cyber Resilience — Capstone | 6,251 w | 15 tasks | 1 template(s) |

---

## 3 · Module-by-Module Detail

### M0 — Orientation, Kali Linux & the Command Line
*Day 1*

**Format:** ~5,913-word lesson · 3 diagram(s) · 14 teaching callouts · 19 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- What Cybersecurity Really Is — for an Organisation
- Cybersecurity, AI & Digital Resilience — the Three Pillars
- Why This Course — What You and Your Organisation Gain
- The Language You Need
- How Attacks Really Happen — and the Tools Attackers Use
- How This Course Works
- Rules of Engagement — Read Carefully
- Your Workstation: Kali Linux
- The Command Line, and Why It Is Non-Negotiable
- The Linux Command Line — the Commands That Matter
- Hands-On: Your First Fifteen Minutes
- Safety Recap

*Plus learning aids in every lesson: Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** T1046

---

### RT — Red Team Primer — Your First Hack
*Day 1*

**Format:** ~2,330-word lesson · 1 diagram(s) · 7 teaching callouts · 1 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- Why We Start by Attacking
- Red, Blue & Purple — and Where "Ethical Hacking" Fits
- The Anatomy of an Attack
- Authorisation Is Everything
- Your First-Hack Toolkit
- The Worked Intrusion — "Operation First Blood"
- Flip It — How Each Step Is Stopped

*Plus learning aids in every lesson: Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** T1078

**Hands-on lab — Operation First Blood — Your First Live Intrusion**  
*Live isolated range on `10.13.2.0/24` · ~75 min · 10 graded tasks · tools: nmap, gobuster, curl, ssh, sudo*

> Break into a live internal server end to end — the real thing, on an isolated range you're authorised to attack. Scan it, discover a web service, loot a credential a careless admin left exposed, use it to get a foothold over SSH, capture the user flag, then exploit a sudo misconfiguration to escalate to root and capture the root flag. Finally, flip to defender: name what would have broken each step of the chain. This is the whole attacker lifecycle in 75 minutes.

Targets:
- `10.13.2.10` **intranet** — Volta internal server — web (:80) + SSH (:22). Your authorised target.

Graded tasks (10 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. The target's web and SSH services are reachable
2. Fingerprint the web service (nmap -sV -p80 10.13.2.10). What server software is it?
3. The web root hides a directory an admin forgot to move. What path is it? (robots.txt hints; gobuster confirms)
4. That directory leaks an ops handover note with SSH credentials. What is the SSH username?
5. And the SSH password in that note?
6. SSH in with those credentials (ssh webadmin@10.13.2.10). What flag is in user.txt in the home directory?
7. Run 'sudo -l'. It shows webadmin may run a shell as root with NO password. What is the privilege-escalation method?
8. Escalate to root (e.g. 'sudo /bin/ash') and read /root/root.txt. What is the root flag?
9. Which MITRE ATT&CK technique covers getting in with the leaked, legitimate credentials?
10. Name ONE control that would have broken this chain.

*Per-student randomised variables (3): root_flag, ssh_pass, user_flag.*

**Deliverable template(s):** `rt-first-hack-report.md`

---

### JS — Web Attack Arena — OWASP Juice Shop
*Day 1*

**Format:** ~1,423-word lesson · 1 diagram(s) · 3 teaching callouts · 1 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- Why the Web App Is the Front Door
- How SQL Injection Works
- Hands-On: Break In (follow along)
- Flip to Defender — The Fix

*Plus learning aids in every lesson: Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** T1190

**Hands-on lab — Web Attack Arena — Break Into OWASP Juice Shop**  
*Live isolated range on `10.13.8.0/24` · ~60 min · 9 graded tasks · tools: browser, curl, nmap, burpsuite*

> Hack a real, deliberately-vulnerable web application the way attackers hit institutional portals every day. OWASP Juice Shop is the world's most famous training target — a modern Angular + Node/Express single-page app riddled with the OWASP Top 10. Browse it, fingerprint its stack, find the hidden challenge scoreboard, then perform a classic SQL-injection login bypass to log in as the administrator without a password — the #1 way public web apps get breached (MITRE ATT&CK T1190). Finally, flip to defender and name the one-line code fix. The server is already running the moment you open the lab — no setup.

Targets:
- `10.13.8.10` **juice-shop** — OWASP Juice Shop web app — http://10.13.8.10:3000  (your authorised target)

Graded tasks (9 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. The Juice Shop web app is reachable on 10.13.8.10:3000
2. Open http://10.13.8.10:3000 in your browser. What is this vulnerable application called?
3. The app leaks its exact version through an admin REST endpoint. Find it: what version is running?
4. Juice Shop hides a challenge scoreboard that is not linked in the menu. What is its route/path?
5. On the Login page, inject SQL into the EMAIL field to log in as the first user WITHOUT a password. What payload works?
6. That bypass logs you in as the administrator. What is the admin account's email address?
7. What class of web vulnerability did the login bypass exploit? (use the OWASP Top 10 name)
8. Name the primary code-level fix that would have stopped this injection.
9. Which MITRE ATT&CK technique covers breaking in by exploiting an internet-facing web app like this?

**Deliverable template(s):** `js-webapp-pentest.md`

---

### M1 — Threat Landscape & Cyber Threat Intelligence
*Day 1*

**Format:** ~5,617-word lesson · 1 diagram(s) · 14 teaching callouts · 3 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- The Intelligence Problem
- Know Your Adversary — Threat-Actor Taxonomy
- The Four Frameworks Professionals Use
- Indicators, Intelligence Levels & Source Grading
- Passive Reconnaissance — Theory and Practice
- Email Authentication — SPF, DKIM, DMARC & BIMI
- Writing the Threat Brief
- The Lab & Assessment

*Plus learning aids in every lesson: Key takeaways, Check yourself, Glossary, Further reading.*

**Frameworks / technique IDs referenced:** T1055, T1589, T1590, T1590.002, T1591, T1593, T1596, T1597, T1598, T1598.001, TA0043

**Hands-on lab — Threat Intelligence & OSINT — Passive Reconnaissance**  
*Live isolated range on `10.13.1.0/24` · ~90 min · 19 graded tasks · tools: dig, whois, theHarvester*

> Run a full passive-reconnaissance profile of a target domain the way an attacker does before a phishing campaign: sweep its DNS, read its email-authentication posture, analyse its registration, harvest its OSINT footprint, and find the missing controls (DMARC, CAA) that leave it exposed. Map every finding to MITRE ATT&CK and write it into a threat brief.

Targets:
- `10.13.1.10` **labdns** — Authoritative DNS for lab-corp.com.gh — query every record type with dig

Graded tasks (19 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. The lab DNS server answers queries for lab-corp.com.gh
2. What IPv4 address does lab-corp.com.gh resolve to? (A record)
3. What IPv6 address does it publish? (AAAA record)
4. What is the mail server (MX) host?
5. What IP does that mail server resolve to?
6. From the SOA record, what is the authoritative name server?
7. Attempt a zone transfer (AXFR). Does the server allow it? (a serious misconfiguration)
8. The zone transfer leaks an internal admin host not published anywhere else. Name it.
9. What internal IP does that leaked admin host resolve to?
10. Run nmap against 10.13.1.10 — what service/software does it fingerprint on port 53?
11. The SPF record ends in a qualifier — what is it, and what does it mean?
12. A DKIM public key is published. At which selector?
13. Is a DMARC record published for lab-corp.com.gh?
14. Is a CAA record published (which would restrict who can issue TLS certs)?
15. Which single email-authentication control is missing and enables spoofing?
16. From the WHOIS export, in what YEAR was lab-corp.com.gh originally registered?
17. The WHOIS export flags a recently-registered look-alike domain. Name it.
18. In the OSINT report, how many employee email addresses were found?
19. Which MITRE ATT&CK technique covers gathering victim DNS/network info?

*Per-student randomised variables (5): hidden_host, hidden_ip, lookalike, mail_ip, reg_year.*

**Deliverable template(s):** `m1-threat-intelligence-brief.md`

---

### M2 — Institutional Cyber Risk & Digital Resilience
*Day 1*

**Format:** ~3,253-word lesson · 3 diagram(s) · 9 teaching callouts · 1 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- Risk Is a Decision Tool, Not a Feeling
- How Risk Assessment Actually Works
- The Four Treatments
- NIST CSF 2.0 — The Control Map Boards Answer To
- Resilience — RTO, RPO and the Link to Continuity
- Scenarios — Risk Owned, and Risk Ignored
- Running the Assessment in Practice
- Do It — the Sankofa Rural Bank case

*Plus learning aids in every lesson: Key takeaways, Check yourself, Glossary, Further reading.*

**Hands-on lab — Institutional Risk Assessment — Sankofa Rural Bank**  
*File-based evidence package (nothing to launch) · ~120 min · 17 graded tasks · tools: risk analysis, NIST CSF 2.0, FAIR*

> Work a real institution's case pack — its asset inventory, its incident history, an external pen-test, a FAIR loss estimate and a half-built draft risk register — and turn it into a prioritised, board-ready risk picture. You triage the crown jewels, score the exposure with evidence, catch the governance failures in the draft register, read the recovery (RTO/RPO) gap, and map controls to NIST CSF 2.0. This is the analytical core of the risk register and CSF profile you then write up as the deliverables.

Graded tasks (17 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. From the asset inventory, which single asset is the highest-criticality 'crown jewel'?
2. How many customer records does the pen-test say sit in the reporting DB with world-readable backups?
3. What CVSS score does the pen-test give the internet-facing VPN (no MFA) finding?
4. Is that VPN vulnerability listed in the CISA KEV catalogue (actively exploited)?
5. Internet-facing + in KEV + on a path to a critical asset — what remediation priority (High/Medium/Low)?
6. In the BEC near-miss, which NEW bank account did the 'supplier' email ask payment to go to?
7. What look-alike domain did that fraudulent email use?
8. Which single payment control would stop this fraud class every time?
9. What annual loss exposure (ALE, in GHS, most-likely) does the FAIR analysis give for the fraud risk?
10. What is the CURRENT recovery time (RTO, in hours) for the core banking system?
11. The board mandates a 4-hour RTO for core banking. Is the current RTO acceptable?
12. Which draft-register risk is being ACCEPTED with no named owner and no review date (negligent acceptance)?
13. Which risk has a Mitigate treatment but NO named owner at all?
14. Which risk has the highest residual rating because its control (desktop antivirus only) does not reduce likelihood or impact?
15. From the profile (no board agenda item, no named accountability, no approved policy), which CSF 2.0 function is weakest?
16. 'Daily review of a central alert feed' belongs to which CSF 2.0 function?
17. The board buys cyber insurance for the residual ransomware risk. Which of the four risk treatments is that?

*Per-student randomised variables (7): bec_account, core_rpo_current, core_rto_current, fraud_ale, lookalike, records_at_risk, vpn_cvss.*

**Deliverable template(s):** `m2-csf-profile.md`, `m2-cyber-risk-register.md`

---

### M3 — Network, Endpoint & Identity Security
*Day 2*

**Format:** ~11,365-word lesson · 5 diagram(s) · 23 teaching callouts · 24 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- A Network Is Conversations
- Nmap — Seeing What Is Exposed
- Active Enumeration — Making Services Talk
- Traffic Analysis — Reading What Is Said
- Man-in-the-Middle & Layer-2 Attacks
- Wireless Network Security
- Endpoint Evidence & Security — Interrogating the Host
- Password Attacks — Cracking Credentials
- Identity & Active Directory Attacks — How a Foothold Becomes a Catastrophe
- Defensive Architecture — Keeping Small Things Small
- Detecting It — the Blue-Team View
- Mapping the Chain to MITRE ATT&CK
- Scenarios — Why Flat Networks and Exposed Services Cost Millions
- The Worked Investigation (what the lab asks of you)

*Plus learning aids in every lesson: Common mistakes, Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** T1003, T1003.006, T1021, T1036, T1040, T1046, T1053, T1053.003, T1053.005, T1059, T1068, T1071, T1071.004, T1078, T1087, T1098.004, T1110, T1110.003, T1135, T1218, T1543, T1543.002, T1543.003, T1546.003, T1547, T1547.001, T1548, T1550.002, T1557, T1557.001, T1557.002, T1558, T1558.003, T1558.004, TA0003

**Hands-on lab — Network Compromise Investigation — Nmap, NSE & Wireshark**  
*Live isolated range on `10.13.3.0/24` · ~120 min · 16 graded tasks · tools: nmap, nmap NSE, wireshark, tcpdump, netstat*

> Work a live network-compromise case across three evidence sources: scan the subnet with Nmap and its scripting engine to find exposed services, follow a packet capture in Wireshark to recover a C2 beacon AND cleartext credentials, and correlate a netstat capture from the suspect host to identify the backdoor and the C2 infrastructure. Map the chain to MITRE ATT&CK and design the controls.

Targets:
- `10.13.3.1` **gateway** — Lab network gateway (your host side — not a target to report)
- `10.13.3.10` **web-admin** — Web server — unauthenticated admin console on :80
- `10.13.3.20` **fileserver** — Anonymous, unencrypted FTP on :21
- `10.13.3.30` **workstation** — SSH on :22 — the infected host (see the capture and netstat)
- `10.13.3.40` **legacy-host** — Exposed legacy remote-access (RDP) on :3389

Graded tasks (16 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. All four lab targets are reachable on the range
2. How many TARGET hosts are live on 10.13.3.0/24 (exclude the .1 gateway)?
3. Which host serves an unauthenticated web admin panel? Give its IP.
4. On which TCP port is the exposed legacy remote-access service?
5. Fingerprint the SSH host (10.13.3.30). What SSH software/version does nmap report?
6. Run the ftp-anon NSE script against the fileserver. Is anonymous FTP login allowed?
7. Which protocol on the fileserver transmits credentials in cleartext?
8. In network-capture.pcap, what domain is the infected host beaconing to?
9. What is the beaconing interval, in seconds?
10. Which internal IP is making those beacon queries?
11. Follow the FTP TCP stream in the capture. What USERNAME logged in?
12. And what PASSWORD was sent — in the clear?
13. In netstat-FIN03.txt, what process name is masquerading as a Windows service?
14. What TCP port is that malware LISTENING on as a backdoor?
15. What external C2 IP does the malware hold an ESTABLISHED connection to? (correlates with the beacon domain)
16. Which MITRE ATT&CK technique covers the DNS command-and-control channel?

*Per-student randomised variables (5): backdoor_port, c2_domain, c2_ip, ftp_pass, ftp_user.*

**Deliverable template(s):** `m3-traffic-analysis-findings.md`

---

### M4 — Vulnerability Management & SOC Operations
*Day 2*

**Format:** ~8,744-word lesson · 4 diagram(s) · 19 teaching callouts · 15 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- Vulnerability Management Is a Loop
- Scanning the Estate — Finding the Weaknesses
- Validating Findings — Exploitation
- Secure Credential Storage — and Why Controls Are Mandatory
- The SOC and Alert Triage
- Correlation — The Master Skill
- Detection Engineering — Catching It, Not Just Finding It
- Threat Hunting & Threat Intelligence
- Mapping the Chain to MITRE ATT&CK
- Scenarios — The Unpatched Flaw and the Weak Credential
- The Worked Investigation (what the lab asks of you)

*Plus learning aids in every lesson: Common mistakes, Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** T1053, T1053.003, T1053.005, T1078, T1110, T1110.001, T1110.002, T1110.003, T1190, T1548, T1595, T1595.002, TA0004

**Hands-on lab — Vulnerability Management & SOC Operations**  
*Live isolated range on `10.13.4.0/24` · ~150 min · 16 graded tasks · tools: nmap, nikto, gobuster, whatweb, hashcat, john, hydra, jq (Wazuh)*

> Run a full web assessment and a cracking chain, then triage the SOC: fingerprint and scan the web server (nmap/whatweb/nikto), brute-force hidden content (gobuster) to find a leaked database backup, crack its unsalted MD5 hashes (hashcat/john), demonstrate weak SSH credentials (Hydra), and correlate the Wazuh alert feed into one attack story with a remediation register and SOC ticket.

Targets:
- `10.13.4.10` **web** — Leaky Apache web server — scan, fuzz and loot
- `10.13.4.20` **ssh** — SSH host with a weak account — authorised Hydra demo target

Graded tasks (16 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. The web target (10.13.4.10) is serving
2. The SSH target (10.13.4.20) is listening
3. Fingerprint the web server — what server software is it?
4. Brute-force the web content. What administrative path is exposed?
5. A database backup was left world-readable under /backup/. Name the file.
6. A leftover config backup leaks the database password. What is it?
7. How are the passwords in db_dump.sql stored (the weakness)?
8. What is the stored hash for the 'admin' account?
9. Crack it. What is admin's plaintext password?
10. Crack the 'backup' service account's hash too. What is its password?
11. Hydra: what password works for 'labuser' over SSH?
12. In the Wazuh feed, which source IP is behind the brute force AND the web scan?
13. What is the highest Wazuh rule level (severity) firing?
14. Did the attacker ultimately succeed in logging in? (yes/no or the rule id)
15. After root access, how did the attacker establish persistence (ATT&CK technique or method)?
16. Which MITRE ATT&CK technique covers the SSH brute force?

*Per-student randomised variables (3): admin_hash, admin_pw, db_pass.*

**Deliverable template(s):** `m4-remediation-register.md`

---

### M5 — Cyber Fraud, BEC & Mobile Money Security
*Day 3*

**Format:** ~7,983-word lesson · 3 diagram(s) · 26 teaching callouts · 15 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- Fraud Is Deception, Not Malware
- Why It Works — The Psychology, Named
- Email Header Forensics
- Hardening Your Own Email — So You're Not the One Spoofed
- Attachment & Document Forensics
- Mobile Money — Ghana's Fraud Battleground
- Payment Systems & Fintech Security
- Follow the Money — Mules, Cash-Out and the Golden Hour
- The Control That Stops BEC
- Hands-On Practicals — Do These Yourself
- Scenarios — The Costliest Con in the World
- The Worked Investigation (what the lab asks of you)

*Plus learning aids in every lesson: Common mistakes, Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** T1566, T1566.002, T1656

**Hands-on lab — Business Email Compromise — Header & Attachment Forensics**  
*File-based evidence package (nothing to launch) · ~120 min · 13 graded tasks · tools: grep, exiftool, pdfinfo, dig, whois*

> Investigate a BEC thread end to end: compare the genuine supplier email against the spoofed reply, trace the spoof's headers and infrastructure, then run exiftool on the malicious attachment to expose the attacker's author name and authoring timezone — and prove premeditation. Build the evidence timeline and design the payment control that stops it.

Graded tasks (13 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. In the spoofed email, which header reveals the true envelope sender (where bounces go)?
2. What is the source IP of the server that actually sent the spoof?
3. Did SPF pass or fail on the SPOOFED email?
4. And in the GENUINE earlier email (genuine-quote.eml), did SPF pass or fail?
5. What look-alike domain does the spoof use in Reply-To / Return-Path?
6. What is the real supplier domain the attacker impersonates?
7. The spoof hijacks the real thread by reusing its PO number. What is it?
8. What NEW bank account number does the spoof ask payment to go to?
9. Run exiftool on remittance-advice.pdf. What AUTHOR is recorded in its metadata?
10. The attachment's Create Date carries a UTC offset inconsistent with a Ghanaian (+00:00) supplier. What offset?
11. Was the attachment created BEFORE the email was sent (evidence of premeditation)?
12. Name the payment control that would have stopped this fraud.
13. Which MITRE ATT&CK technique covers this phishing/impersonation?

*Per-student randomised variables (5): fraud_account, lookalike, pdf_author, pdf_tz, source_ip.*

**Deliverable template(s):** `m5-fraud-investigation-brief.md`

---

### M6 — Digital Forensics & Incident Response
*Day 3*

**Format:** ~7,803-word lesson · 3 diagram(s) · 22 teaching callouts · 15 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- The Forensic Foundation — Prove You Didn't Change the Evidence
- Order of Volatility — Collect the Perishable First
- The Incident-Response Lifecycle
- Disk Forensics
- Decoding Attacker Artefacts
- Memory Forensics — The Reward for Not Powering Off
- Network Forensics — Reading the Breach on the Wire (PCAP)
- Where the Evidence Lives — Windows DFIR Artefacts
- Timeline Reconstruction & Correlation
- Running the Response — Containment, Eradication, Recovery
- Mapping the Chain to MITRE ATT&CK
- Scenarios — When Response Makes It Better, or Worse
- Hands-On Practicals — Do These Yourself
- The Worked Investigation (what the lab asks of you)

*Plus learning aids in every lesson: Common mistakes, Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** T1036, T1048, T1053, T1053.005, T1059, T1059.001, T1070, T1070.006, T1071, T1204, T1204.002, T1555, T1566.001

**Hands-on lab — Digital Forensics & Incident Response — Disk, Memory & Timeline**  
*File-based evidence package (nothing to launch) · ~150 min · 14 graded tasks · tools: sha256sum, fls/icat/tsk_recover, strings, bulk_extractor, CyberChef, grep*

> Work a full IR evidence package across disk, memory and logs: prove integrity by hashing, recover a deleted credentials file from a disk image (Sleuthkit), carve the malware's command line, C2, in-memory credential and exfil address from a RAM dump (strings/bulk_extractor), decode an obfuscated dropper (CyberChef), and reconstruct the attack timeline from the auth log — then correlate it all.

Graded tasks (14 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. Evidence integrity verified (sha256sum -c passes)
2. What filesystem does the evidence image use?
3. Name the macro-enabled spreadsheet the user opened (the lure).
4. Recover the DELETED credentials file — what is the VPN password in it?
5. Decode suspicious_artifact.txt — what C2 domain does it reveal?
6. Carve memory.raw — what malicious executable (masquerading as a service) is running?
7. What C2 host does the in-memory PowerShell stager call? (it matches the decoded dropper)
8. A plaintext credential sits in memory — what is the VPN admin's password?
9. bulk_extractor pulls an exfiltration email address from memory. What is it?
10. How does the malware persist (a scheduled task is created in memory)? Name the method or ATT&CK id.
11. From auth.log, which source IP brute-forced SSH and then succeeded?
12. Which account did the attacker finally log in as (Accepted password)?
13. By order of volatility, which evidence must be collected FIRST?
14. Which MITRE ATT&CK technique covers the macro launching PowerShell?

*Per-student randomised variables (3): c2_domain, exfil_email, vpn_pass.*

**Deliverable template(s):** `m6-chain-of-custody.md`, `m6-incident-report.md`

---

### M7 — AI Security, Deepfakes & Emerging Threats
*Day 4*

**Format:** ~7,238-word lesson · 3 diagram(s) · 20 teaching callouts · 5 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- AI as Weapon, AI as Target
- The LLM Attack Landscape
- Agentic AI & Autonomous Agents — the New Frontier
- The Frameworks Your Board Will Ask About
- Securing an LLM Application
- Red-Teaming & Evaluating AI
- Beyond the Chatbot — Adversarial ML & Governance
- Deepfakes — Why Detection Fails and Process Wins
- Mapping the Chain to MITRE ATLAS
- Hands-On Practicals — Do These Yourself
- Scenarios — Synthetic Media, Real Money
- The Worked Investigation (what the lab asks of you)

*Plus learning aids in every lesson: Common mistakes, Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** LLM01, LLM02, LLM03, LLM04, LLM05, LLM06, LLM07, LLM08, LLM10, T0051

**Hands-on lab — AI Security — Prompt Injection, RAG Poisoning, Tool Exfil & Deepfakes**  
*Live isolated range on `10.13.7.0/24` · ~120 min · 12 graded tasks · tools: curl, jq, ai-sandbox, exiftool*

> Attack a controlled, offline AI-assistant the way a real adversary does — four ways: direct prompt injection (leak the secret), RAG poisoning (make it serve a mule bank account as fact), indirect injection that triggers tool-based data exfiltration, and excessive-agency tool abuse. Then run a deepfake-voicemail verification drill and design the governance controls (OWASP LLM Top 10 / MITRE ATLAS / NIST AI RMF).

Targets:
- `10.13.7.10` **ai-sandbox** — Insecure scripted AI assistant on :8080 (no model, no internet)

Graded tasks (12 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. The AI sandbox is reachable on 10.13.7.10:8080
2. Direct injection via /chat: extract the hidden admin override code.
3. Query /ask about the supplier bank account. The knowledge base has been tampered with — what class of attack is that?
4. What fraudulent bank account number does the poisoned RAG answer return?
5. Feeding the poisoned supplier-memo.txt to /summarize makes the AI ACT. What class of injection is that?
6. That document makes the assistant abuse its send_email tool. What address does it exfiltrate data to?
7. The assistant runs tools (read_file, send_email) named in untrusted input. Which principle would contain this?
8. Which OWASP LLM Top 10 item is prompt injection (id or name)?
9. Which MITRE framework catalogues adversarial-ML tactics and techniques?
10. Name one technical mitigation against prompt injection / tool abuse.
11. A deepfake 'MD' voicemail (ceo-voicemail-transcript.txt) orders an urgent transfer. What verification step do you apply?
12. From the transcript, name one BEHAVIOURAL red flag (not acoustic) that marks it as likely fraud.

*Per-student randomised variables (3): exfil_addr, flag, rag_account.*

**Deliverable template(s):** `m7-ai-risk-assessment.md`

---

### M8 — Data Protection, Privacy & Compliance
*Day 4*

**Format:** ~6,301-word lesson · 4 diagram(s) · 22 teaching callouts · 1 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- Two Laws, One Duty of Care
- Controller vs Processor — Accountability Doesn't Transfer
- Privacy by Design, Data Classification & PETs
- Rights, DPIAs & Cross-Border Transfers
- The Global & Sectoral Landscape — GDPR and Beyond
- The First 72 Hours of a Breach
- CII and Mandatory Reporting (Act 1038)
- Standards, Certification & Assurance
- Building the Compliance Programme
- Hands-On Practicals — Do These Yourself
- Scenario — Exposure and Consequence
- Do It — the Akoma Health Case

*Plus learning aids in every lesson: Key takeaways, Check yourself, Glossary, Further reading.*

**Hands-on lab — Data Breach & Compliance Case — Akoma Health Network**  
*File-based evidence package (nothing to launch) · ~120 min · 16 graded tasks · tools: Act 843, Act 1038, GDPR, DPIA, breach notification*

> A private health network has just discovered that a cloud export of patient data was left public and downloaded. Work the case the way a Data Protection Officer must in the first hours: classify the breach, fix controller/processor accountability, scope the data and the people affected, decide the notification obligations and timelines, and catch the compliance failures (retention, lawful basis, DPIA, the missing vendor DPA, lapsed registration). This is the analytical core of the breach assessment and compliance-gap register you then write up.

Graded tasks (16 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. Is this a reportable personal-data breach under Act 843? (yes/no)
2. Does the exposed data include sensitive / special-category data? What makes it sensitive?
3. How many patient records were in the exposed export?
4. How many external downloads do the access logs show during the exposure window?
5. Under Act 843, who is ACCOUNTABLE for this breach — Akoma (the hospital) or CloudMed (the cloud vendor)?
6. What is CloudMed's role under the Act?
7. What is the GDPR-benchmark time (hours) to notify the regulator once aware of a breach?
8. Which Ghanaian regulator oversees the PERSONAL-DATA breach?
9. Which authority handles the CYBER-incident reporting side (Act 1038)?
10. Given the high risk to individuals (health data, confirmed downloads), should the affected patients be notified directly? (yes/no)
11. Keeping records years past the documented need breaches which data-protection principle?
12. The lawful basis on file is 'consent', but it was bundled into a mandatory form patients couldn't decline. Is that consent valid?
13. What assessment was legally required before this large-scale sensitive processing, but was never done? (name it)
14. The contract with CloudMed is missing the written controller–processor agreement. Name it.
15. What is the first CONTAINMENT action on the exposed cloud bucket?
16. What potential DPC penalty (in GHS) does the case file cite for these failures?

*Per-student randomised variables (5): download_count, exposure_days, fine, records, retention_years.*

**Deliverable template(s):** `m8-breach-assessment.md`, `m8-compliance-gap-register.md`

---

### M9 — Cyber Governance & Business Continuity
*Day 5*

**Format:** ~5,324-word lesson · 4 diagram(s) · 16 teaching callouts · 1 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- Governance Is Direction and Assurance
- Security Frameworks & Program Maturity
- The Policy Hierarchy
- Metrics That Matter to a Board
- The Board-Reporting Discipline
- The Business Case — Risk in Money, and Cyber Insurance
- Business Continuity — Surviving and Recovering
- Crisis Command
- Operational Resilience — the Modern Frame
- An Analogy
- Hands-On Practicals — Do These Yourself
- Scenarios — Governance Decides the Outcome
- Do It — the Volta Pension Trust Case

*Plus learning aids in every lesson: Key takeaways, Check yourself, Glossary, Further reading.*

**Hands-on lab — Governance & Continuity Review — Volta Pension Trust**  
*File-based evidence package (nothing to launch) · ~90 min · 16 graded tasks · tools: NIST CSF 2.0, ISO 22301, BIA, three-lines model*

> A pension trust's board has called a governance and business-continuity review before its next meeting. Work the case the way a CISO briefing the board must: read the BIA to set recovery priorities, find the RTO/RPO gap on the service pensioners depend on, catch the governance failures (no board owner, a muddled policy hierarchy, vanity metrics, untested backups, no crisis command), and name the right answers. This is the analytical core of the executive risk memo and the recovery-priority table you then write up.

Graded tasks (16 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. How many members does the Trust serve (per the case pack)?
2. Which service must be recovered FIRST (shortest RTO, highest impact)?
3. What RTO (hours) has the board mandated for the benefits-payment system?
4. What is the CURRENT recovery time (RTO, hours) for the benefits-payment system?
5. Does the current RTO meet the board's mandate?
6. What financial impact per day of a benefits-payment outage does the case cite (GHS)?
7. Setting the risk appetite and approving the cyber policy is a GOVERNANCE or a MANAGEMENT activity?
8. Given no board agenda item, no accountable executive and a stale policy, which NIST CSF 2.0 function is weakest?
9. A document titled 'Password Policy' that lists the step-by-step enrolment is really which layer of the policy hierarchy?
10. The board pack reports 'number of attacks blocked: 4.2M'. Is that a useful board metric?
11. Name one metric the board SHOULD see instead.
12. Backups exist but were never ___ — the control that proves recovery actually works?
13. In the three-lines model, independent assurance is provided by which line (or which function)?
14. In a crisis, who owns and directs the decisions?
15. What must the crisis team keep as its audit trail (and later defence)?
16. A regulated institution reports the incident to which authority under Act 1038?

*Per-student randomised variables (7): bp_rpo_current, bp_rto_current, bp_rto_required, impact_per_day, members, pensioners, policy_age.*

**Deliverable template(s):** `m9-executive-risk-memo.md`, `m9-recovery-priority-table.md`

---

### M10 — Operation Cyber Resilience — Capstone
*Day 5*

**Format:** ~6,251-word lesson · 4 diagram(s) · 16 teaching callouts · 2 worked command/example blocks.

**Topics taught (the lesson's own chapters):**

- The Orchestra, Not the Instruments
- Incident Command — Running It Under Pressure
- Decision-Making Under Pressure
- Know Your Adversary — the Campaign Behind the Injects
- The Signature Correlation — One Campaign, Not Six Problems
- Running the Investigation
- The Minute-by-Minute Playbook
- Running the Response (by the playbook)
- Crisis Communications
- The After-Action Review & the 90-Day Roadmap
- How You're Scored — the Debrief Rubric
- Scenarios — Because This Is How Real Attacks Arrive
- The Worked Investigation (what the lab asks of you)
- Graduation — Your Path Forward

*Plus learning aids in every lesson: Common mistakes, Key takeaways, Check yourself, Glossary.*

**Frameworks / technique IDs referenced:** LLM01, T1041, T1046, T1048, T1078, T1486, T1565, T1566, T1567, T1656

**Hands-on lab — Operation Cyber Resilience — CyberRange Capstone**  
*Live isolated range on `10.13.10.0/24` · ~270 min · 15 graded tasks · tools: nmap, wireshark, jq, email forensics, ai-sandbox, all*

> One simulated crisis against a fictional Ghanaian institution, eight injects, every tool from the week. Investigate the live range and the evidence package, reconstruct the multi-vector attack end to end, and drive the response.

Targets:
- `10.13.10.10` **finance-portal** — Public finance portal (web)
- `10.13.10.20` **records-host** — Records platform (SSH) — the compromised foothold's neighbour
- `10.13.10.40` **ai-assistant** — Internal AI assistant (:8080)

Graded tasks (15 — the student is assessed on each; «your value» marks a per-student randomised answer):

1. The capstone range (web + SSH + AI) is live
2. T+00: what look-alike domain sent the payment-change email? (payment-change.eml)
3. What mule bank account does the BEC email demand payment to?
4. Query the bank's own AI assistant (10.13.10.40 /ask) about the supplier account. What account does its POISONED knowledge base return — and what does matching it to the email tell you?
5. T+20/T+40: which internal IP is the compromised foothold (privileged login + scanning)?
6. Recon the finance portal (10.13.10.10). What world-readable DB backup is exposed under /backup/?
7. Crack the 'admin' MD5 from that dump. What is the plaintext password?
8. From capstone-capture.pcap, what C2 domain is the foothold beaconing to?
9. T+120: what external IP is the data being exfiltrated to?
10. What is the highest Wazuh rule level across the inject sequence?
11. T+90: a synthetic executive voicemail orders a wire transfer. What do you do?
12. First containment action for the foothold 10.13.10.66?
13. Which MITRE ATT&CK technique covers the data exfiltration?
14. T+145: the database is offline (ransomware). Which ATT&CK technique?
15. T+160: the bank's own AI assistant was abused in this campaign. Name the technique/class.

*Per-student randomised variables (5): admin_hash, admin_pw, c2_domain, fraud_account, lookalike.*

**Deliverable template(s):** `m10-incident-dossier.md`

---

## 4 · Assessment & Certification

Assessment is **graded and weighted**, not attendance-based:

| Component | Weight | What it is |
|-----------|-------:|------------|
| Labs | 50% | the hands-on graded lab tasks above |
| Quizzes | 25% | 11 module knowledge-checks (33 questions) |
| Exam | 25% | a 12-question final exam |
| **Pass mark** | **70%** | composite; below this, no certificate |

- A **6-question baseline diagnostic** (ungraded) lets students self-place at the start.
- Quiz and exam **options are reshuffled per student**, and the correct answer is never sent to the browser — so answers cannot be shared.
- On reaching the pass mark, the platform issues a **branded completion certificate** carrying a serial and a verification code derived from the student's own record (so a tampered certificate fails verification).
- Progress, grading and the certificate are available in both the command-line tool (`labctl`) and the web application.

---

## 5 · Built-in Reference Compendium

A searchable in-platform reference, available to every student:

- **Frameworks Quick-Reference** — Kill Chain, ATT&CK, CSF 2.0, OWASP LLM Top 10, Pyramid of Pain & more
- **Ghana Cyber & Data Law** — Act 843 & Act 1038, DPC / CSA / CERT-GH, breach response
- **Master Glossary** — Every key term from the programme, A–Z

---

## 6 · Frameworks, Standards & Laws Taught

The programme teaches to recognised frameworks and the Ghanaian legal regime throughout:

- **Attack/defence models:** Cyber Kill Chain, MITRE ATT&CK (enterprise tactics & techniques), MITRE ATLAS (adversarial AI), the Diamond Model, the Pyramid of Pain.
- **Risk & governance:** NIST Cybersecurity Framework 2.0, NIST SP 800-30, ISO/IEC 27001 & 27005, ISO 31000, FAIR (risk quantification), the three-lines model, COBIT.
- **Incident & continuity:** NIST SP 800-61 (PICERL), RFC 3227 (order of volatility), ISO 22301 (business continuity), the 3-2-1 backup rule.
- **AI security & governance:** OWASP Top 10 for LLM Applications, NIST AI RMF, ISO/IEC 42001, the EU AI Act (risk tiers).
- **Email & fraud:** SPF, DKIM, DMARC; the Fraud Triangle; Cialdini's principles of influence.
- **Ghanaian & global law:** Data Protection Act 2012 (**Act 843**, DPC); Cybersecurity Act 2020 (**Act 1038**, CSA / CERT-GH, CII); Payment Systems & Services Act 2019 (**Act 987**); the EU **GDPR** as the global benchmark.

---

## 7 · How to Verify This Document

Nothing here needs to be taken on trust. An external reviewer can confirm every claim against the source:

1. **Regenerate this file:** `python3 scripts/course_audit.py` — it reads the live files and rewrites `COURSE_AUDIT.md`.
2. **Read any lesson:** `labctl learn m3` (terminal) or open `lessons/m3.md` / the web app's Course view — the chapters listed above are the lesson's own headings.
3. **Run any lab:** `labctl start m3` → investigate → `labctl verify m3` — the graded tasks listed above are the lab's own checks.
4. **Validate the whole suite:** `python3 scripts/dry_run.py` brings every lab up, solves it against the per-student answer key, and tears it down (expect *ALL LABS PASS*); `python3 -m unittest discover -s tests` runs the engine test suite.
5. **See the model answers:** `scripts/answer_key.py` writes the facilitator answer key for every lab and the assessment.

*This audit is generated from the repository and reflects its exact state on 2026-10-13.*
