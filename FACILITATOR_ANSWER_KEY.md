# CAIC CyberLab — Facilitator Answer Key

> **Facilitator-only.** Model answers for every lab, generated from the
> manifests (`python3 scripts/answer_key.py`). Do not distribute to students.

## M1 — Threat Intelligence & OSINT — Passive Reconnaissance
*Day 1 · 19 checks · 19 points · tools: dig, whois, theHarvester*

1. The lab DNS server answers queries for lab-corp.com.gh
   → _(automatic script check — verifies live state)_
2. What IPv4 address does lab-corp.com.gh resolve to? (A record)
   → **41.210.15.20**
3. What IPv6 address does it publish? (AAAA record)
   → **2001:db8:ac10:f15::20**
4. What is the mail server (MX) host?
   → **mail.lab-corp.com.gh**  _(also: mail.lab-corp.com.gh.)_
5. What IP does that mail server resolve to?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
6. From the SOA record, what is the authoritative name server?
   → **ns1.lab-corp.com.gh**  _(also: ns1.lab-corp.com.gh.)_
7. Attempt a zone transfer (AXFR). Does the server allow it? (a serious misconfiguration)
   → **yes**  _(also: allowed, successful, it works, transfer allowed, y)_
8. The zone transfer leaks an internal admin host not published anywhere else. Name it.
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
9. What internal IP does that leaked admin host resolve to?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
10. Run nmap against 10.13.1.10 — what service/software does it fingerprint on port 53?
   → **bind**  _(also: isc bind, domain, dns, bind9, named)_
11. The SPF record ends in a qualifier — what is it, and what does it mean?
   → **~all**  _(also: softfail, soft fail, ~all softfail, tilde all)_
12. A DKIM public key is published. At which selector?
   → **default**  _(also: default._domainkey, default._domainkey.lab-corp.com.gh)_
13. Is a DMARC record published for lab-corp.com.gh?
   → **no**  _(also: none, no dmarc, absent, not published, nxdomain, missing)_
14. Is a CAA record published (which would restrict who can issue TLS certs)?
   → **no**  _(also: none, absent, not published, missing, no caa)_
15. Which single email-authentication control is missing and enables spoofing?
   → **dmarc**
16. From the WHOIS export, in what YEAR was lab-corp.com.gh originally registered?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
17. The WHOIS export flags a recently-registered look-alike domain. Name it.
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
18. In the OSINT report, how many employee email addresses were found?
   → **5**
19. Which MITRE ATT&CK technique covers gathering victim DNS/network info?
   → **T1590**  _(also: T1590.002, T1589, T1598)_

## M3 — Network Compromise Investigation — Nmap, NSE & Wireshark
*Day 2 · 16 checks · 16 points · tools: nmap, nmap NSE, wireshark, tcpdump, netstat*

1. All four lab targets are reachable on the range
   → _(automatic script check — verifies live state)_
2. How many TARGET hosts are live on 10.13.3.0/24 (exclude the .1 gateway)?
   → **4**
3. Which host serves an unauthenticated web admin panel? Give its IP.
   → **10.13.3.10**
4. On which TCP port is the exposed legacy remote-access service?
   → **3389**
5. Fingerprint the SSH host (10.13.3.30). What SSH software/version does nmap report?
   → **openssh**  _(also: openssh 9.7, 9.7, openssh 9, openssh 9.7 (protocol 2.0))_
6. Run the ftp-anon NSE script against the fileserver. Is anonymous FTP login allowed?
   → **yes**  _(also: allowed, anonymous allowed, anonymous ftp login allowed, y, 230)_
7. Which protocol on the fileserver transmits credentials in cleartext?
   → **ftp**  _(also: ftp (21), file transfer protocol)_
8. In network-capture.pcap, what domain is the infected host beaconing to?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
9. What is the beaconing interval, in seconds?
   → **30**
10. Which internal IP is making those beacon queries?
   → **10.13.3.30**
11. Follow the FTP TCP stream in the capture. What USERNAME logged in?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
12. And what PASSWORD was sent — in the clear?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
13. In netstat-FIN03.txt, what process name is masquerading as a Windows service?
   → **svch0st**  _(also: svch0st (pid 3391), sv ch0st)_
14. What TCP port is that malware LISTENING on as a backdoor?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
15. What external C2 IP does the malware hold an ESTABLISHED connection to? (correlates with the beacon domain)
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
16. Which MITRE ATT&CK technique covers the DNS command-and-control channel?
   → **T1071**  _(also: T1071.004)_

## M4 — Vulnerability Management & SOC Operations
*Day 2 · 16 checks · 16 points · tools: nmap, nikto, gobuster, whatweb, hashcat, john, hydra, jq (Wazuh)*

1. The web target (10.13.4.10) is serving
   → _(automatic script check — verifies live state)_
2. The SSH target (10.13.4.20) is listening
   → _(automatic script check — verifies live state)_
3. Fingerprint the web server — what server software is it?
   → **apache**  _(also: apache httpd, httpd)_
4. Brute-force the web content. What administrative path is exposed?
   → **/admin/**  _(also: /admin, admin, admin/)_
5. A database backup was left world-readable under /backup/. Name the file.
   → **db_dump.sql**  _(also: /backup/db_dump.sql, backup/db_dump.sql)_
6. A leftover config backup leaks the database password. What is it?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
7. How are the passwords in db_dump.sql stored (the weakness)?
   → **md5**  _(also: raw-md5, unsalted md5, raw md5, unsalted, md5 unsalted)_
8. What is the stored hash for the 'admin' account?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
9. Crack it. What is admin's plaintext password?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
10. Crack the 'backup' service account's hash too. What is its password?
   → **12345**
11. Hydra: what password works for 'labuser' over SSH?
   → **Password123**
12. In the Wazuh feed, which source IP is behind the brute force AND the web scan?
   → **10.13.4.66**
13. What is the highest Wazuh rule level (severity) firing?
   → **12**
14. Did the attacker ultimately succeed in logging in? (yes/no or the rule id)
   → **yes**  _(also: 5715, authentication success, successful login, success)_
15. After root access, how did the attacker establish persistence (ATT&CK technique or method)?
   → **T1053**  _(also: T1053.003, cron, cron job, scheduled task, scheduled task/job)_
16. Which MITRE ATT&CK technique covers the SSH brute force?
   → **T1110**  _(also: T1110.001, T1110.003)_

## M5 — Business Email Compromise — Header & Attachment Forensics
*Day 3 · 13 checks · 13 points · tools: grep, exiftool, pdfinfo, dig, whois*

1. In the spoofed email, which header reveals the true envelope sender (where bounces go)?
   → **return-path**  _(also: return path, return-path:)_
2. What is the source IP of the server that actually sent the spoof?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
3. Did SPF pass or fail on the SPOOFED email?
   → **fail**  _(also: failed, spf fail, spf=fail)_
4. And in the GENUINE earlier email (genuine-quote.eml), did SPF pass or fail?
   → **pass**  _(also: passed, spf=pass)_
5. What look-alike domain does the spoof use in Reply-To / Return-Path?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
6. What is the real supplier domain the attacker impersonates?
   → **zenithsupplies.com.gh**
7. The spoof hijacks the real thread by reusing its PO number. What is it?
   → **ZS-20418**  _(also: zs-20418, 20418)_
8. What NEW bank account number does the spoof ask payment to go to?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
9. Run exiftool on remittance-advice.pdf. What AUTHOR is recorded in its metadata?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
10. The attachment's Create Date carries a UTC offset inconsistent with a Ghanaian (+00:00) supplier. What offset?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
11. Was the attachment created BEFORE the email was sent (evidence of premeditation)?
   → **yes**  _(also: before, y, created before, premeditated)_
12. Name the payment control that would have stopped this fraud.
   → **dual control**  _(also: dual-control, callback, call back, out-of-band verification, verbal verification, separation of duties, callback verification, out of band)_
13. Which MITRE ATT&CK technique covers this phishing/impersonation?
   → **T1566**  _(also: T1566.002, T1656)_

## M6 — Digital Forensics & Incident Response — Disk, Memory & Timeline
*Day 3 · 14 checks · 14 points · tools: sha256sum, fls/icat/tsk_recover, strings, bulk_extractor, CyberChef, grep*

1. Evidence integrity verified (sha256sum -c passes)
   → _(automatic script check — verifies live state)_
2. What filesystem does the evidence image use?
   → **fat16**  _(also: fat, fat 16)_
3. Name the macro-enabled spreadsheet the user opened (the lure).
   → **q3invoic.xls**  _(also: Q3INVOIC.XLS, q3invoic)_
4. Recover the DELETED credentials file — what is the VPN password in it?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
5. Decode suspicious_artifact.txt — what C2 domain does it reveal?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
6. Carve memory.raw — what malicious executable (masquerading as a service) is running?
   → **svch0st.exe**  _(also: svch0st, c:\windows\temp\svch0st.exe)_
7. What C2 host does the in-memory PowerShell stager call? (it matches the decoded dropper)
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
8. A plaintext credential sits in memory — what is the VPN admin's password?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
9. bulk_extractor pulls an exfiltration email address from memory. What is it?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
10. How does the malware persist (a scheduled task is created in memory)? Name the method or ATT&CK id.
   → **schtasks**  _(also: scheduled task, scheduled task/job, T1053, T1053.005, cron, cron job)_
11. From auth.log, which source IP brute-forced SSH and then succeeded?
   → **10.13.4.66**
12. Which account did the attacker finally log in as (Accepted password)?
   → **labuser**
13. By order of volatility, which evidence must be collected FIRST?
   → **memory**  _(also: ram, volatile memory, memory (ram))_
14. Which MITRE ATT&CK technique covers the macro launching PowerShell?
   → **T1059.001**  _(also: T1059, T1204.002, T1204)_

## M7 — AI Security — Prompt Injection, RAG Poisoning, Tool Exfil & Deepfakes
*Day 4 · 12 checks · 12 points · tools: curl, jq, ai-sandbox, exiftool*

1. The AI sandbox is reachable on 10.13.7.10:8080
   → _(automatic script check — verifies live state)_
2. Direct injection via /chat: extract the hidden admin override code.
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
3. Query /ask about the supplier bank account. The knowledge base has been tampered with — what class of attack is that?
   → **rag poisoning**  _(also: rag-poisoning, knowledge base poisoning, data poisoning, poisoning)_
4. What fraudulent bank account number does the poisoned RAG answer return?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
5. Feeding the poisoned supplier-memo.txt to /summarize makes the AI ACT. What class of injection is that?
   → **indirect**  _(also: indirect prompt injection, indirect-prompt-injection, document injection)_
6. That document makes the assistant abuse its send_email tool. What address does it exfiltrate data to?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
7. The assistant runs tools (read_file, send_email) named in untrusted input. Which principle would contain this?
   → **least privilege**  _(also: least-privilege, principle of least privilege, tool permissioning, limit tool permissions, privilege separation, restrict tools, sandboxing tools)_
8. Which OWASP LLM Top 10 item is prompt injection (id or name)?
   → **LLM01**  _(also: LLM01:2025, prompt injection, llm01 prompt injection)_
9. Which MITRE framework catalogues adversarial-ML tactics and techniques?
   → **atlas**  _(also: mitre atlas)_
10. Name one technical mitigation against prompt injection / tool abuse.
   → **input validation**  _(also: input filtering, output filtering, treat content as untrusted, do not trust external content, privilege separation, human in the loop, human-in-the-loop, guardrails, content sanitisation, content sanitization, least privilege, allowlist, least-privilege)_
11. A deepfake 'MD' voicemail (ceo-voicemail-transcript.txt) orders an urgent transfer. What verification step do you apply?
   → **callback**  _(also: call back, independent channel, out-of-band, out of band, call a known number, pre-established number, verify on a known number, independent callback, call back on a known number, dual control)_
12. From the transcript, name one BEHAVIOURAL red flag (not acoustic) that marks it as likely fraud.
   → **urgency**  _(also: urgent, deadline, don't call back, dont call back, no callback, bypass approvers, bypass approval, skip approvers, confidential, secrecy, don't loop in approvers, out-of-band channel, whatsapp)_

## M10 — Operation Cyber Resilience — CyberRange Capstone
*Day 5 · 15 checks · 15 points · tools: nmap, wireshark, jq, email forensics, ai-sandbox, all*

1. The capstone range (web + SSH + AI) is live
   → _(automatic script check — verifies live state)_
2. T+00: what look-alike domain sent the payment-change email? (payment-change.eml)
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
3. What mule bank account does the BEC email demand payment to?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
4. Query the bank's own AI assistant (10.13.10.40 /ask) about the supplier account. What account does its POISONED knowledge base return — and what does matching it to the email tell you?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
5. T+20/T+40: which internal IP is the compromised foothold (privileged login + scanning)?
   → **10.13.10.66**
6. Recon the finance portal (10.13.10.10). What world-readable DB backup is exposed under /backup/?
   → **db_dump.sql**  _(also: /backup/db_dump.sql, backup/db_dump.sql)_
7. Crack the 'admin' MD5 from that dump. What is the plaintext password?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
8. From capstone-capture.pcap, what C2 domain is the foothold beaconing to?
   → **«randomized per student»** — grade on the student's own machine (`labctl verify`)
9. T+120: what external IP is the data being exfiltrated to?
   → **185.220.101.44**
10. What is the highest Wazuh rule level across the inject sequence?
   → **12**
11. T+90: a synthetic executive voicemail orders a wire transfer. What do you do?
   → **callback**  _(also: call back, independent channel, out-of-band, out of band, verify on a known number, pre-established number, independent callback, refuse and verify)_
12. First containment action for the foothold 10.13.10.66?
   → **isolate**  _(also: isolate the host, contain, quarantine, network isolation, disconnect, segment off, isolate host)_
13. Which MITRE ATT&CK technique covers the data exfiltration?
   → **T1041**  _(also: T1567, T1048)_
14. T+145: the database is offline (ransomware). Which ATT&CK technique?
   → **T1486**  _(also: data encrypted for impact)_
15. T+160: the bank's own AI assistant was abused in this campaign. Name the technique/class.
   → **prompt injection**  _(also: rag poisoning, rag-poisoning, indirect prompt injection, llm01, knowledge base poisoning, data poisoning)_

---

# Assessment answer key (quizzes & final exam)

> Options are **shuffled per student**, so answers are given by text, not letter.
> The baseline diagnostic is self-placement and is not graded.

## Baseline Diagnostic (ungraded — self-placement)  _(`baseline` · 6 questions)_

1. What does the 'C' in the CIA triad stand for?
   → **Confidentiality**
   _Confidentiality — only authorised parties can read the data._
2. MFA stands for:
   → **Multi-Factor Authentication**
   _An extra factor beyond the password._
3. Phishing is primarily an attack on:
   → **People (social engineering)**
   _It manipulates people into acting._
4. A 'patch' is:
   → **A software fix for a vulnerability**
   _Patches close known vulnerabilities._
5. Ransomware typically:
   → **Encrypts your files and demands payment**
   _It denies availability and extorts payment._
6. Which is a strong authentication practice?
   → **Using MFA and unique passwords**
   _Unique passwords + MFA._

## Orientation & the Linux command line  _(`m0` · 3 questions)_

1. Which one-liner lists the most frequent source IPs in a log's first column?
   → **awk '{print $1}' access.log | sort | uniq -c | sort -rn**
   _sort | uniq -c | sort -rn is the analyst's 'what's most common?' pattern._
2. A private SSH key shows permissions -rw------- (600). Is that correct?
   → **Yes — a private key must be readable only by its owner**
   _SSH refuses a private key other users can read; 600 (owner-only) is required._
3. A colleague asks you to 'quickly scan' a partner company's website. The correct response is:
   → **Refuse without the partner's written authorisation**
   _Scanning a third party without written authorisation is an offence under Act 1038._

## Threat Landscape & Cyber Threat Intelligence  _(`m1` · 3 questions)_

1. A domain publishes SPF ending in ~all and has no DMARC record. It is:
   → **Highly exposed to spoofing**
   _~all soft-fails forged mail (still delivered) and no DMARC means no policy/alignment — spoofable._
2. On the Pyramid of Pain, which indicator hurts the attacker MOST when you block it?
   → **The attacker's TTPs**
   _TTPs are hardest to change; hashes/IPs are trivially rotated._
3. Which is PASSIVE reconnaissance?
   → **dig MX against the target's domain**
   _dig reads public DNS and never touches the target's systems; the others are active._

## Institutional Cyber Risk & Resilience  _(`m2` · 3 questions)_

1. You buy cyber insurance for a risk. Which treatment is that?
   → **Transfer**
   _Insurance transfers financial cost (not the operational/reputational harm)._
2. What makes a risk-register entry's acceptance defensible rather than negligent?
   → **A named owner and a review date**
   _Acceptance without a named owner and review date is negligence._
3. Which NIST CSF 2.0 function was added in 2.0 and signals board accountability?
   → **Govern**
   _GOVERN makes cybersecurity a board-level duty._

## Network, Endpoint & Identity Security  _(`m3` · 3 questions)_

1. A host contacts the same external domain every 60 seconds all night. This is characteristic of:
   → **C2 beaconing**
   _Fixed-interval regularity is the beaconing tell; real traffic is bursty._
2. Target 2013's catastrophe spread because of which architectural failure?
   → **A flat network (no segmentation)**
   _The vendor segment could reach the payment systems — segmentation would have contained it._
3. Why is SMS-based MFA weaker than a FIDO2 security key?
   → **It's defeated by SIM-swap and phishing**
   _SIM-swap/phishing defeat SMS OTP; FIDO2 is phishing-resistant._

## Vulnerability Management & SOC Operations  _(`m4` · 3 questions)_

1. Which do you remediate first?
   → **CVSS 6.8 on your public payment portal, listed in CISA KEV**
   _Internet-facing + critical asset + actively exploited (KEV) beats raw score._
2. Hydra vs John the Ripper — the core difference is:
   → **Hydra guesses against a live service; John cracks stolen hashes offline**
   _Online guessing (Hydra) vs offline hash cracking (John); John has no lockout._
3. Failed logins, a port scan and a successful login — all from one IP. How many incidents?
   → **One — correlate by source IP**
   _Correlation turns scattered alerts into one intrusion._

## Cyber Fraud, BEC & Mobile Money  _(`m5` · 3 questions)_

1. The single control that most reliably stops BEC payment fraud is:
   → **Dual control + out-of-band callback on a KNOWN number**
   _Verify any bank-detail change via an independently known channel; never the email's number._
2. An email's From: shows your real supplier, but Reply-To is a different hyphenated domain. This is:
   → **A spoof routing replies to the attacker**
   _Display forged for trust; replies silently go to the look-alike domain._
3. Why doesn't an SMS OTP protect a MoMo wallet against SIM-swap?
   → **The attacker has taken over the number itself**
   _SIM-swap hijacks the number, so the OTP is delivered to the attacker._

## Digital Forensics & Incident Response  _(`m6` · 3 questions)_

1. You reach a compromised server still running. The right first move is to:
   → **Isolate it from the network and capture memory first**
   _Powering off destroys volatile memory evidence; isolate, then collect by order of volatility._
2. Matching SHA-256 hashes before and after analysis prove:
   → **The evidence was not altered (integrity)**
   _A matching hash is mathematical proof of integrity — the basis of chain of custody._
3. The 3-2-1 backup rule means:
   → **3 copies, 2 media types, 1 offsite/offline**
   _One offline/offsite copy is what survives ransomware that encrypts online backups._

## AI Security, Deepfakes & Emerging Threats  _(`m7` · 3 questions)_

1. A document you ask an AI to summarise makes it email data to an attacker. This is:
   → **Indirect prompt injection + excessive agency**
   _The instruction rode inside ingested content and the AI used a tool it shouldn't have._
2. Against a deepfake 'CEO' voicemail demanding an urgent transfer, the reliable defence is:
   → **Out-of-band callback on a pre-established number**
   _Detectors are unreliable; verify via an independent known channel._
3. Which OWASP list ranks prompt injection as its top risk (LLM01)?
   → **OWASP LLM Top 10**
   _Prompt injection is LLM01 in the OWASP Top 10 for LLM applications._

## Data Protection, Privacy & Compliance  _(`m8` · 3 questions)_

1. A cloud vendor misconfigures storage and leaks your customers' data. Who is accountable under Act 843?
   → **You — the data controller**
   _Outsourcing processing does not outsource accountability; you remain the controller._
2. In the first 72 hours of a breach, the first action is to:
   → **Contain active access (while preserving evidence)**
   _Contain first, investigate second, then triage notification with counsel._
3. The GDPR breach-notification norm Ghanaian institutions are increasingly expected to meet is:
   → **72 hours to the regulator once aware**
   _72 hours to the regulator is the benchmark expectation._

## Cyber Governance & Business Continuity  _(`m9` · 3 questions)_

1. Approving the cybersecurity budget and risk appetite is a function of:
   → **Governance (the board)**
   _Governance sets direction and demands assurance; management executes._
2. Why is the backup RESTORE test more important than the backup itself?
   → **A backup you've never restored may not work — only a verified restore proves DR**
   _An untested backup is a hope; the verified restore is the real control._
3. RTO and RPO are, respectively:
   → **Max acceptable downtime; max acceptable data loss**
   _RTO = how fast you must be back; RPO = how much data you can afford to lose._

## Operation Cyber Resilience (Capstone)  _(`m10` · 3 questions)_

1. Several injects all involve one internal IP. What does that tell you?
   → **It's one campaign — correlate by the shared foothold IP**
   _A shared indicator ties scattered events into a single intrusion._
2. You contain the compromised foothold host. You should:
   → **Isolate it from the network (preserve evidence)**
   _Isolate to stop spread without destroying volatile evidence._
3. A mid-incident voice note 'from the CEO' orders an urgent transfer. You:
   → **Verify out-of-band on a known number first**
   _Likely a deepfake; verify out-of-band before any payment._

## Final Exam — whole programme  _(`final` · 12 questions)_

1. No DMARC record on a domain means:
   → **It is effectively spoofable**
   _No policy/alignment to reject forged mail._
2. The highest-value indicator to detect on the Pyramid of Pain is:
   → **TTPs**
   _TTPs cost the attacker the most to change._
3. Target 2013 spread because the network was:
   → **Flat / unsegmented**
   _Segmentation would have contained the vendor-account foothold._
4. Prioritise remediation by:
   → **CVSS + KEV + exposure + asset criticality**
   _Context and active exploitation beat raw score._
5. The control that stops BEC payment fraud:
   → **Dual control + out-of-band callback**
   _Verify changes via an independently known channel._
6. First move on a running compromised host:
   → **Isolate + capture memory**
   _Order of volatility — memory first; never power off._
7. Under Act 843, if your processor leaks data, who is accountable?
   → **You, the controller**
   _Accountability stays with the controller._
8. Prompt injection is which OWASP LLM risk?
   → **LLM01**
   _LLM01 — the top risk._
9. Governance vs management: setting risk appetite is:
   → **Governance**
   _The board governs; teams manage._
10. RPO measures:
   → **Max acceptable data loss**
   _RTO is downtime; RPO is data loss._
11. The 3-2-1 rule requires at least one copy that is:
   → **Offline/offsite**
   _An offline copy survives ransomware._
12. A deepfake voicemail ordering a transfer is defeated by:
   → **Out-of-band callback verification**
   _Verify via a pre-established independent channel._
