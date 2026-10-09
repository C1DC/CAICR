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
   → **sync-telemetry.duckdns.org**  _(also: duckdns.org)_
9. What is the beaconing interval, in seconds?
   → **30**
10. Which internal IP is making those beacon queries?
   → **10.13.3.30**
11. Follow the FTP TCP stream in the capture. What USERNAME logged in?
   → **backupsvc**
12. And what PASSWORD was sent — in the clear?
   → **Backup#2021**
13. In netstat-FIN03.txt, what process name is masquerading as a Windows service?
   → **svch0st**  _(also: svch0st (pid 3391), sv ch0st)_
14. What TCP port is that malware LISTENING on as a backdoor?
   → **4444**
15. What external C2 IP does the malware hold an ESTABLISHED connection to? (correlates with the beacon domain)
   → **185.220.101.44**
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
   → **Acme#2019**
7. How are the passwords in db_dump.sql stored (the weakness)?
   → **md5**  _(also: raw-md5, unsalted md5, raw md5, unsalted, md5 unsalted)_
8. What is the stored hash for the 'admin' account?
   → **5f4dcc3b5aa765d61d8327deb882cf99**
9. Crack it. What is admin's plaintext password?
   → **password**
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
   → **45.137.112.63**
3. Did SPF pass or fail on the SPOOFED email?
   → **fail**  _(also: failed, spf fail, spf=fail)_
4. And in the GENUINE earlier email (genuine-quote.eml), did SPF pass or fail?
   → **pass**  _(also: passed, spf=pass)_
5. What look-alike domain does the spoof use in Reply-To / Return-Path?
   → **zenith-supplies.com**
6. What is the real supplier domain the attacker impersonates?
   → **zenithsupplies.com.gh**
7. The spoof hijacks the real thread by reusing its PO number. What is it?
   → **ZS-20418**  _(also: zs-20418, 20418)_
8. What NEW bank account number does the spoof ask payment to go to?
   → **1402300087654**
9. Run exiftool on remittance-advice.pdf. What AUTHOR is recorded in its metadata?
   → **k1ngpin**  _(also: kingpin)_
10. The attachment's Create Date carries a UTC offset inconsistent with a Ghanaian (+00:00) supplier. What offset?
   → **+07:00**  _(also: +0700, +07, 7, +7, utc+7)_
11. Was the attachment created BEFORE the email was sent (evidence of premeditation)?
   → **yes**  _(also: before, y, created before, premeditated)_
12. Name the payment control that would have stopped this fraud.
   → **dual control**  _(also: dual-control, callback, call back, out-of-band verification, verbal verification, separation of duties, callback verification, out of band)_
13. Which MITRE ATT&CK technique covers this phishing/impersonation?
   → **T1566**  _(also: T1566.002, T1656)_

## M6 — Digital Forensics & Incident Response — Disk, Memory & Timeline
*Day 3 · 15 checks · 15 points · tools: sha256sum, fls/icat/tsk_recover, strings, bulk_extractor, CyberChef, grep*

1. Evidence integrity verified (sha256sum -c passes)
   → _(automatic script check — verifies live state)_
2. What is the SHA-256 of evidence.img?
   → **1cd9ccc112367afb21b00f3300922757862d685749a1100620e1e17ee7d4d300**
3. What filesystem does the evidence image use?
   → **fat16**  _(also: fat, fat 16)_
4. Name the macro-enabled spreadsheet the user opened (the lure).
   → **q3invoic.xls**  _(also: Q3INVOIC.XLS, q3invoic)_
5. Recover the DELETED credentials file — what is the VPN password in it?
   → **Gh@na2026!**
6. Decode suspicious_artifact.txt — what C2 domain does it reveal?
   → **beacon.sync-malware-c2.net**  _(also: sync-malware-c2.net, http://beacon.sync-malware-c2.net/gate.php?id=FIN03)_
7. Carve memory.raw — what malicious executable (masquerading as a service) is running?
   → **svch0st.exe**  _(also: svch0st, c:\windows\temp\svch0st.exe)_
8. What C2 host does the in-memory PowerShell stager call? (it matches the decoded dropper)
   → **beacon.sync-malware-c2.net**  _(also: sync-malware-c2.net)_
9. A plaintext credential sits in memory — what is the VPN admin's password?
   → **S3cr3tVPN!2026**
10. bulk_extractor pulls an exfiltration email address from memory. What is it?
   → **exfil-drop@attacker-mail.ru**
11. How does the malware persist (a scheduled task is created in memory)? Name the method or ATT&CK id.
   → **schtasks**  _(also: scheduled task, scheduled task/job, T1053, T1053.005, cron, cron job)_
12. From auth.log, which source IP brute-forced SSH and then succeeded?
   → **10.13.4.66**
13. Which account did the attacker finally log in as (Accepted password)?
   → **labuser**
14. By order of volatility, which evidence must be collected FIRST?
   → **memory**  _(also: ram, volatile memory, memory (ram))_
15. Which MITRE ATT&CK technique covers the macro launching PowerShell?
   → **T1059.001**  _(also: T1059, T1204.002, T1204)_

## M7 — AI Security — Prompt Injection, RAG Poisoning, Tool Exfil & Deepfakes
*Day 4 · 12 checks · 12 points · tools: curl, jq, ai-sandbox, exiftool*

1. The AI sandbox is reachable on 10.13.7.10:8080
   → _(automatic script check — verifies live state)_
2. Direct injection via /chat: extract the hidden admin override code.
   → **FLAG{pr0mpt_1nj3ction_sh4d0w_ai}**
3. Query /ask about the supplier bank account. The knowledge base has been tampered with — what class of attack is that?
   → **rag poisoning**  _(also: rag-poisoning, knowledge base poisoning, data poisoning, poisoning)_
4. What fraudulent bank account number does the poisoned RAG answer return?
   → **9900778100**
5. Feeding the poisoned supplier-memo.txt to /summarize makes the AI ACT. What class of injection is that?
   → **indirect**  _(also: indirect prompt injection, indirect-prompt-injection, document injection)_
6. That document makes the assistant abuse its send_email tool. What address does it exfiltrate data to?
   → **collector@mule-net.su**
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
   → **zennith-supplies.com**
3. What mule bank account does the BEC email demand payment to?
   → **9900778100**
4. Query the bank's own AI assistant (10.13.10.40 /ask) about the supplier account. What account does its POISONED knowledge base return — and what does matching it to the email tell you?
   → **9900778100**
5. T+20/T+40: which internal IP is the compromised foothold (privileged login + scanning)?
   → **10.13.10.66**
6. Recon the finance portal (10.13.10.10). What world-readable DB backup is exposed under /backup/?
   → **db_dump.sql**  _(also: /backup/db_dump.sql, backup/db_dump.sql)_
7. Crack the 'admin' MD5 from that dump. What is the plaintext password?
   → **password**
8. From capstone-capture.pcap, what C2 domain is the foothold beaconing to?
   → **cdn-sync.ddns-telemetry.net**  _(also: ddns-telemetry.net)_
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
