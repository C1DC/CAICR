"""Shared course metadata: the module map, the Kali tool reference, and the
command cheat-sheet. Used by both the CLI and the web app so there is one
source of truth."""
from __future__ import annotations

# (id, day, title, has_lab)
COURSE_MAP = [
    ("m0",  1, "Orientation, Kali Linux & the Command Line", False),
    ("rt",  1, "Red Team Primer — Your First Hack", True),
    ("m1",  1, "Threat Landscape & Cyber Threat Intelligence", True),
    ("m2",  1, "Institutional Cyber Risk & Digital Resilience", True),
    ("m3",  2, "Network, Endpoint & Identity Security", True),
    ("m4",  2, "Vulnerability Management & SOC Operations", True),
    ("m5",  3, "Cyber Fraud, BEC & Mobile Money Security", True),
    ("m6",  3, "Digital Forensics & Incident Response", True),
    ("m7",  4, "AI Security, Deepfakes & Emerging Threats", True),
    ("m8",  4, "Data Protection, Privacy & Compliance", True),
    ("m9",  5, "Cyber Governance & Business Continuity", True),
    ("m10", 5, "Operation Cyber Resilience — Capstone", True),
]

DAY_TITLES = {
    1: "Threat Landscape, Kali Linux & Institutional Risk",
    2: "Network Security & Vulnerability Operations",
    3: "Cyber Fraud Investigation & Digital Forensics",
    4: "AI Security, Privacy & Ghana Compliance",
    5: "Governance & Integrated Crisis Capstone",
}

# Kali / industry tool reference shown in the Tools & Materials view.
# Each entry: name, category, modules it appears in, a full description, how to
# use it, a handful of real commands, and practitioner tips.
TOOLS = [
    {"name": "Nmap", "cat": "Network Scanning", "modules": "M3, M4, M10",
     "desc": "The de-facto network mapper. It discovers live hosts, open ports, "
             "the service and version behind each port, and can fingerprint the "
             "operating system. The Nmap Scripting Engine (NSE) adds hundreds of "
             "checks for specific vulnerabilities and misconfigurations.",
     "usage": "Start broad (host discovery), then narrow to services on the hosts "
              "that matter. Save output as evidence. Authorised targets only.",
     "how": "Nmap sends crafted probe packets and reads the replies. A SYN scan sends "
            "a TCP SYN: a SYN-ACK back means the port is OPEN, a RST means CLOSED, and "
            "silence means FILTERED (a firewall dropped it). Version detection then "
            "talks to each open port and matches the banner against a database to name "
            "the software and version.",
     "workflow": [
        "Discover live hosts: `nmap -sn 10.13.3.0/24`.",
        "Enumerate services on the ones that matter: `nmap -sV -p- <host>`.",
        "Investigate a specific weakness with a targeted NSE script (e.g. ftp-anon).",
        "Save everything as evidence: add `-oA scanname`.",
        "Read the VERSION column — that's where the finding (old/unauth service) is."],
     "commands": [
        {"cmd": "nmap -sn 10.13.3.0/24", "desc": "Ping sweep — which hosts are alive (no port scan)."},
        {"cmd": "nmap -sV -p 1-1000 10.13.3.10", "desc": "Scan top 1000 ports with service/version detection."},
        {"cmd": "nmap -A 10.13.3.10", "desc": "Aggressive: OS guess, version, default scripts, traceroute."},
        {"cmd": "nmap --script vuln 10.13.3.10", "desc": "Run the NSE vulnerability-check scripts."},
        {"cmd": "nmap -oN scan.txt 10.13.3.0/24", "desc": "Save normal-format output to a file (evidence)."}],
     "tips": ["`-Pn` skips host discovery when ICMP is blocked.",
              "`-T4` speeds timing on a lab LAN; avoid on fragile networks.",
              "Scan your own estate monthly — find your open RDP before attackers do."]},

    {"name": "Wireshark", "cat": "Packet Analysis", "modules": "M3, M10",
     "desc": "The world's most used graphical protocol analyser. It reads live or "
             "captured traffic and decodes it layer by layer, so you can follow a "
             "conversation and judge whether it is normal or malicious.",
     "usage": "Open a .pcap, apply a DISPLAY filter to cut noise, then follow "
              "streams. Hunt for C2 beaconing (same destination, fixed interval), "
              "DNS anomalies and cleartext credentials.",
     "how": "Wireshark captures raw frames and dissects each one through every "
            "protocol layer, then reassembles related packets into conversations. "
            "A capture filter decides what is recorded (and is lost if omitted); a "
            "display filter is a non-destructive view over what you already captured.",
     "workflow": [
        "Open the capture; apply a display filter like `dns` to cut the noise.",
        "Spot the one host repeatedly resolving an odd domain — watch the time delta (a beacon is regular).",
        "Right-click a packet → Follow → TCP Stream to read a whole conversation (where cleartext creds fall out).",
        "Use Statistics → Conversations (sort by bytes) to find a big exfil, or Protocol Hierarchy for what's in the capture.",
        "Export objects / note the indicators for your report."],
     "commands": [
        {"cmd": "wireshark capture.pcap &", "desc": "Open a capture in the GUI."},
        {"cmd": "dns", "desc": "Display filter: show only DNS (spot beaconing)."},
        {"cmd": "ip.addr == 185.220.101.44", "desc": "Filter all traffic to/from one host."},
        {"cmd": "http.request or tls.handshake", "desc": "Web requests and TLS handshakes only."},
        {"cmd": "tcp.flags.syn == 1 and tcp.flags.ack == 0", "desc": "SYN packets — reveals port scans."}],
     "tips": ["Capture filters limit what is recorded; display filters limit what is shown.",
              "Right-click a packet → Follow → TCP Stream to read a full exchange.",
              "Statistics → Conversations ranks who talked to whom, by volume."]},

    {"name": "tcpdump", "cat": "Packet Capture", "modules": "M3",
     "desc": "The command-line packet capture tool — lightweight, scriptable, and "
             "available on almost every system, so it is what you reach for on a "
             "server with no GUI.",
     "usage": "Capture to a file on the box under investigation, then analyse the "
              ".pcap elsewhere (often in Wireshark).",
     "commands": [
        {"cmd": "tcpdump -i eth0 -w capture.pcap", "desc": "Capture all traffic on eth0 to a file."},
        {"cmd": "tcpdump -r capture.pcap 'udp port 53'", "desc": "Read a file, show only DNS."},
        {"cmd": "tcpdump -i eth0 'host 10.13.3.30'", "desc": "Live capture for one host only."},
        {"cmd": "tcpdump -nn -i eth0 'tcp port 80'", "desc": "HTTP traffic, no name resolution (faster)."}],
     "tips": ["`-w` writes raw packets; `-r` reads them back.",
              "`-nn` disables DNS and port-name lookups for speed and clarity."]},

    {"name": "theHarvester", "cat": "OSINT & Recon", "modules": "M1",
     "desc": "An open-source reconnaissance tool that gathers a domain's public "
             "footprint — email addresses, subdomains, hosts and IPs — from search "
             "engines, certificate-transparency logs and other public sources.",
     "usage": "Point it at a domain you are authorised to assess; the output is the "
              "raw material for a phishing target list — and for the defender, the "
              "list of who needs the most awareness training.",
     "commands": [
        {"cmd": "theHarvester -d example.com -b all", "desc": "Harvest from all available sources."},
        {"cmd": "theHarvester -d example.com -b bing,crtsh", "desc": "Use specific sources."},
        {"cmd": "theHarvester -d example.com -b all -f report.html", "desc": "Save an HTML report."}],
     "tips": ["Live sources need internet; this course ships a captured report for offline use.",
              "Pair with `dig`/`whois` to confirm and enrich what you find."]},

    {"name": "dig", "cat": "DNS & Domain Intel", "modules": "M1, M5",
     "desc": "The DNS lookup workhorse. It queries any record type directly and "
             "shows the authoritative answer — the same checks an attacker runs to "
             "plan a phishing campaign, and a defender runs to audit exposure.",
     "usage": "Query MX, TXT (SPF/DMARC), A and NS records of a domain; the absence "
              "of a DMARC record is one of the most important findings in Module 1.",
     "commands": [
        {"cmd": "dig example.com A +short", "desc": "The IPv4 address(es)."},
        {"cmd": "dig example.com MX +short", "desc": "The mail servers."},
        {"cmd": "dig example.com TXT +short", "desc": "TXT records — SPF lives here."},
        {"cmd": "dig _dmarc.example.com TXT +short", "desc": "The DMARC policy (or NXDOMAIN = none)."},
        {"cmd": "dig @10.13.1.10 example.com ANY", "desc": "Query a specific DNS server."}],
     "tips": ["`+short` trims the output to just the answer.",
              "`-all` (hard fail) is strong SPF; `~all` (soft fail) is weak."]},

    {"name": "whois", "cat": "DNS & Domain Intel", "modules": "M1, M5",
     "desc": "Looks up domain and IP registration data — registrar, creation date, "
             "owner, hosting network. A look-alike domain registered days before a "
             "fraudulent invoice is a decisive fraud signal.",
     "usage": "Run against a suspicious domain or the source IP from an email's "
              "Received chain to identify the hosting provider and country.",
     "commands": [
        {"cmd": "whois example.com", "desc": "Full domain registration record."},
        {"cmd": "whois example.com | grep -Ei 'creat|registr'", "desc": "Registration date and registrar."},
        {"cmd": "whois 45.137.112.63", "desc": "Who owns an IP address (ISP, country)."}],
     "tips": ["A brand-new registration date on a 'trusted supplier' domain is a red flag."]},

    {"name": "Nikto", "cat": "Web Vulnerability Scanning", "modules": "M4",
     "desc": "An open-source web-server scanner that checks for thousands of "
             "dangerous files, outdated server software, risky HTTP methods and "
             "missing security headers. Where Nmap finds the open port, Nikto "
             "investigates what is running on it.",
     "usage": "Point it at a web server you are authorised to test; triage its "
              "findings against CVSS, KEV and exposure (Module 4).",
     "commands": [
        {"cmd": "nikto -h http://10.13.4.10", "desc": "Basic scan of a web server."},
        {"cmd": "nikto -h http://10.13.4.10 -o report.txt", "desc": "Save the findings to a report."},
        {"cmd": "nikto -h http://10.13.4.10 -ssl", "desc": "Force an HTTPS scan."},
        {"cmd": "nikto -h http://10.13.4.10 -Tuning 123b", "desc": "Limit to specific test categories."}],
     "tips": ["Nikto is noisy and easily detected — it is for authorised assessment, not stealth.",
              "Always verify a Nikto finding by hand before reporting it."]},

    {"name": "Gobuster / ffuf", "cat": "Web Content Discovery", "modules": "M4 (extension)",
     "desc": "High-speed brute-forcers for hidden web content — directories, files "
             "and virtual hosts — and for DNS subdomains. ffuf is the modern, "
             "flexible fuzzer; Gobuster is the simple, fast classic.",
     "usage": "Use a wordlist to discover unlinked admin panels, backups and config "
              "files a scanner's crawl would miss.",
     "commands": [
        {"cmd": "gobuster dir -u http://10.13.4.10 -w /usr/share/wordlists/dirb/common.txt",
         "desc": "Brute-force directories and files."},
        {"cmd": "gobuster dns -d example.com -w subdomains.txt", "desc": "Discover subdomains."},
        {"cmd": "ffuf -u http://10.13.4.10/FUZZ -w common.txt", "desc": "Fuzz the FUZZ keyword with a wordlist."},
        {"cmd": "ffuf -u http://10.13.4.10/FUZZ -w list.txt -mc 200,301", "desc": "Match only given status codes."}],
     "tips": ["A good wordlist matters more than speed — SecLists is the standard collection.",
              "`-mc`/`-fc` match or filter by HTTP status to cut noise."]},

    {"name": "sqlmap", "cat": "Web Exploitation", "modules": "M4 (extension)",
     "desc": "The standard automated SQL-injection tool. It detects and exploits "
             "injectable parameters, and can enumerate databases, dump tables and "
             "even gain command execution — strictly on authorised targets.",
     "usage": "Feed it a URL or a captured request; let it fingerprint the DBMS, "
              "then enumerate only what the engagement authorises.",
     "commands": [
        {"cmd": "sqlmap -u 'http://site/item?id=1' --batch", "desc": "Test a parameter for SQL injection."},
        {"cmd": "sqlmap -u '...' --dbs", "desc": "Enumerate databases if injectable."},
        {"cmd": "sqlmap -r request.txt -p id", "desc": "Use a saved request, target the 'id' parameter."},
        {"cmd": "sqlmap -u '...' -D app -T users --dump", "desc": "Dump a specific table."}],
     "tips": ["`--batch` accepts defaults non-interactively.",
              "Immensely powerful and immensely illegal without written authorisation."]},

    {"name": "Hydra", "cat": "Credential Testing", "modules": "M4",
     "desc": "A fast online password-guessing tool supporting dozens of protocols "
             "(SSH, FTP, HTTP forms, RDP and more). It demonstrates why weak and "
             "reused passwords fail — and why MFA is mandatory.",
     "usage": "Against an AUTHORISED target only, supply a username (or list) and a "
              "wordlist; a 'password spray' tries one common password across many "
              "accounts to avoid lockouts.",
     "commands": [
        {"cmd": "hydra -l labuser -P wordlist.txt ssh://10.13.4.20", "desc": "Guess one user's SSH password."},
        {"cmd": "hydra -L users.txt -p 'Password123' ssh://10.13.4.20", "desc": "Password-spray one password across users."},
        {"cmd": "hydra -l admin -P list.txt 10.13.4.10 http-post-form \"/login:user=^USER^&pass=^PASS^:Invalid\"",
         "desc": "Attack a web login form."}],
     "tips": ["Online guessing is slow and noisy and triggers lockouts/alerts — that is the point of the demo.",
              "The real-world wordlist is /usr/share/wordlists/rockyou.txt."]},

    {"name": "John the Ripper", "cat": "Password Cracking", "modules": "M4",
     "desc": "The classic offline password-hash cracker. Given stolen hashes it "
             "computes guesses locally at high speed, with no network, lockout or "
             "rate limit — which is why a leaked hash database is a disaster and "
             "why hashes must be salted and slow.",
     "usage": "Identify the hash type, run a wordlist (optionally with mangling "
              "rules), then show the cracked results.",
     "commands": [
        {"cmd": "john --wordlist=rockyou.txt hashes.txt", "desc": "Dictionary attack on a hash file."},
        {"cmd": "john --show hashes.txt", "desc": "Display cracked passwords."},
        {"cmd": "john --wordlist=rockyou.txt --rules hashes.txt", "desc": "Apply word-mangling rules."},
        {"cmd": "john --format=raw-md5 hashes.txt", "desc": "Force a specific hash format."}],
     "tips": ["`unshadow /etc/passwd /etc/shadow > out` prepares Linux hashes for John.",
              "If John is slow, the fix is GPU power — see Hashcat."]},

    {"name": "Hashcat", "cat": "Password Cracking", "modules": "M4 (extension)",
     "desc": "The fastest password cracker, built for GPUs. It supports hundreds of "
             "hash types and attack modes (dictionary, rules, mask/brute-force) and "
             "is the industry standard for serious offline cracking.",
     "usage": "Choose the hash mode (`-m`) and attack mode (`-a`), then feed hashes "
              "and a wordlist or mask.",
     "commands": [
        {"cmd": "hashcat -m 0 -a 0 hashes.txt rockyou.txt", "desc": "MD5 (-m 0) dictionary attack (-a 0)."},
        {"cmd": "hashcat -m 1800 -a 0 hashes.txt rockyou.txt", "desc": "sha512crypt dictionary attack."},
        {"cmd": "hashcat -m 0 -a 3 hashes.txt '?l?l?l?l?d?d'", "desc": "Mask attack: 4 letters + 2 digits."},
        {"cmd": "hashcat --show -m 0 hashes.txt", "desc": "Show already-cracked results."}],
     "tips": ["`-m` is the hash type; the wiki/`--help` lists every mode.",
              "Mask attacks target known password patterns far faster than brute force."]},

    {"name": "Metasploit Framework", "cat": "Exploitation", "modules": "M4 (extension)",
     "desc": "The most widely used exploitation framework: a vast, maintained "
             "library of exploits, payloads and post-exploitation modules behind a "
             "single console. It is the reference tool for validating that a "
             "vulnerability is genuinely exploitable.",
     "usage": "In msfconsole, search for a module, set its options (RHOSTS, "
              "payload), and run — on authorised targets only.",
     "how": "Metasploit separates the exploit (the flaw it abuses) from the payload "
            "(what runs after) from the options (target, port, listener). You pick an "
            "exploit module, attach a payload (e.g. Meterpreter — an in-memory agent), "
            "set RHOSTS/LHOST, and run; a handler catches the resulting session for "
            "post-exploitation. The same model powers its scanner and post modules.",
     "workflow": [
        "`msfconsole -q`, then `search` for a module matching the service/CVE you found.",
        "`use <module>`; `show options` to see what it needs.",
        "`set RHOSTS <target>` (and payload/LHOST for exploits); `check` if supported.",
        "`run` — on confirmed-authorised targets only.",
        "On success, `sessions -i <id>` to interact; use post modules to gather evidence."],
     "commands": [
        {"cmd": "msfconsole -q", "desc": "Start the console (quiet)."},
        {"cmd": "search type:exploit apache", "desc": "Find modules by keyword."},
        {"cmd": "use exploit/...; set RHOSTS 10.13.4.10; run", "desc": "Select, configure and launch a module."},
        {"cmd": "sessions -l", "desc": "List active post-exploitation sessions."}],
     "tips": ["Pair with the Meterpreter payload for rich post-exploitation.",
              "`msfvenom` generates standalone payloads outside the console."]},

    {"name": "Netcat (nc)", "cat": "Networking Swiss-army knife", "modules": "M3 (extension)",
     "desc": "A tiny, universal tool that reads and writes raw TCP/UDP. It is used "
             "for banner-grabbing, port testing, simple file transfer and "
             "listeners — the duct tape of networking.",
     "usage": "Connect to a port to inspect a service, or listen on a port to "
              "receive a connection.",
     "commands": [
        {"cmd": "nc -nv 10.13.3.20 21", "desc": "Connect to a port and grab its banner."},
        {"cmd": "nc -lvnp 4444", "desc": "Listen on port 4444 for an inbound connection."},
        {"cmd": "nc -zv 10.13.3.10 1-1000", "desc": "Quick port check across a range."},
        {"cmd": "nc 10.13.3.10 80 < request.txt", "desc": "Send a raw request to a service."}],
     "tips": ["`ncat` (from Nmap) adds TLS and is more capable than classic nc.",
              "A listener + a reverse connection is the basis of many shells — authorised use only."]},

    {"name": "Autopsy / Sleuthkit", "cat": "Digital Forensics", "modules": "M6, M10",
     "desc": "Autopsy is the open-source graphical forensic platform used by law "
             "enforcement worldwide; Sleuthkit is its command-line engine. Together "
             "they ingest a disk image, list and recover files (including deleted "
             "ones), build timelines and search artefacts.",
     "usage": "Hash the image first, create a case, add the image, run ingest "
              "modules — or use the Sleuthkit CLI directly for speed.",
     "commands": [
        {"cmd": "fsstat evidence.img", "desc": "Filesystem type and layout."},
        {"cmd": "fls evidence.img", "desc": "List files; a '*' marks a deleted entry."},
        {"cmd": "icat evidence.img 5", "desc": "Read a file by its inode number."},
        {"cmd": "tsk_recover evidence.img ./recovered", "desc": "Carve deleted files out to a folder."},
        {"cmd": "autopsy &", "desc": "Launch the GUI (then open the shown local URL)."}],
     "tips": ["Always work on a hashed copy, never the original.",
              "`mactime`/`log2timeline` build the chronological 'super timeline'."]},

    {"name": "Volatility", "cat": "Memory Forensics", "modules": "M6 (demo)",
     "desc": "The standard framework for analysing RAM captures. Because it reads "
             "memory, it finds running processes, injected code, network "
             "connections and credentials that never touched disk — the reward for "
             "not powering a machine off.",
     "usage": "Point it at a memory image and run plugins for the artefacts you "
              "need (processes, network, injected code).",
     "commands": [
        {"cmd": "vol.py -f mem.raw windows.pslist", "desc": "List processes from a RAM image."},
        {"cmd": "vol.py -f mem.raw windows.netscan", "desc": "Recover network connections."},
        {"cmd": "vol.py -f mem.raw windows.malfind", "desc": "Find injected/hidden code."},
        {"cmd": "vol.py -f mem.raw windows.cmdline", "desc": "Command lines of running processes."}],
     "tips": ["Collect memory BEFORE disk — order of volatility (RFC 3227).",
              "Volatility 3 uses `windows.*`/`linux.*` plugin names."]},

    {"name": "CyberChef", "cat": "Data Analysis & Decode", "modules": "M6, M10",
     "desc": "The 'cyber swiss-army knife' — a browser tool for decoding, "
             "decrypting and transforming data by chaining operations into a "
             "'recipe'. Ideal for peeling the layers off an obfuscated artefact to "
             "reveal, say, a C2 URL. Works fully offline.",
     "usage": "Paste the artefact, drag operations into the recipe (e.g. From "
              "Base64 → URL Decode), and read the output. The same can be done on "
              "the CLI for simple cases.",
     "commands": [
        {"cmd": "From Base64  →  URL Decode", "desc": "A typical CyberChef recipe for a dropper string."},
        {"cmd": "base64 -d artifact.txt", "desc": "CLI equivalent of one Base64 layer."},
        {"cmd": "echo 'aGVsbG8=' | base64 -d", "desc": "Quick inline Base64 decode."},
        {"cmd": "xxd artifact.bin | head", "desc": "Inspect raw bytes to identify the encoding."}],
     "tips": ["'Magic' operation auto-detects likely encodings.",
              "Great for defanging/refanging IOCs when writing a report."]},

    {"name": "Wazuh (SIEM/XDR)", "cat": "Security Monitoring", "modules": "M4, M10",
     "desc": "An open-source SIEM and XDR platform used across Africa and beyond. "
             "It collects logs from endpoints, servers and network devices, applies "
             "detection rules (mapped to MITRE ATT&CK), and raises prioritised "
             "alerts for the SOC to triage.",
     "usage": "Analysts live in the alert view: sort by severity, add context, "
              "correlate related alerts by shared indicators, and classify each as "
              "true positive, false positive or needs-investigation.",
     "commands": [
        {"cmd": "jq -r '.[] | \"\\(.rule.level)\\t\\(.rule.description)\"' alerts.json | sort -rn",
         "desc": "Rank alerts by severity (as in the M4 lab feed)."},
        {"cmd": "jq -r '.[].data.srcip // empty' alerts.json | sort | uniq -c | sort -rn",
         "desc": "Find the busiest source IP across alerts (correlation)."},
        {"cmd": "jq '[.[].rule.level] | max' alerts.json", "desc": "The highest severity level firing."}],
     "tips": ["The skill is correlation — ten alerts are often one attack seen ten ways.",
              "This course triages a realistic alert feed rather than run the full stack."]},

    {"name": "Burp Suite", "cat": "Web App Testing", "modules": "M4 (extension)",
     "desc": "The industry-standard web-application testing proxy. It sits between "
             "the browser and the target, letting you intercept, inspect, modify "
             "and replay every HTTP request — the core workflow of web pentesting.",
     "usage": "Configure the browser to proxy through Burp, intercept a request, "
              "send it to Repeater to tamper and replay, or to Intruder to fuzz.",
     "commands": [
        {"cmd": "(Proxy → Intercept)", "desc": "Capture and edit requests in flight."},
        {"cmd": "(Repeater)", "desc": "Replay and tweak a single request repeatedly."},
        {"cmd": "(Intruder)", "desc": "Automated fuzzing/brute-forcing of parameters."},
        {"cmd": "(Decoder / Comparer)", "desc": "Encode/decode values and diff responses."}],
     "tips": ["The Community Edition is free; Professional adds the active scanner.",
              "Set the browser's CA trust to Burp's cert to intercept HTTPS."]},

    {"name": "aircrack-ng", "cat": "Wireless Security", "modules": "M3 (extension)",
     "desc": "A suite for assessing Wi-Fi security — capturing wireless traffic, "
             "capturing authentication handshakes, and testing the strength of "
             "WPA/WPA2 pre-shared keys offline.",
     "usage": "Put the adapter in monitor mode, capture a handshake, then test it "
              "against a wordlist — on networks you own or are authorised to test.",
     "commands": [
        {"cmd": "airmon-ng start wlan0", "desc": "Put the wireless adapter into monitor mode."},
        {"cmd": "airodump-ng wlan0mon", "desc": "Survey nearby networks and clients."},
        {"cmd": "airodump-ng -c 6 --bssid AA:BB:.. -w cap wlan0mon", "desc": "Capture a handshake on a channel."},
        {"cmd": "aircrack-ng -w rockyou.txt cap.cap", "desc": "Test the captured handshake against a wordlist."}],
     "tips": ["Requires a wireless adapter that supports monitor mode and injection.",
              "Testing a Wi-Fi network you do not own is an offence — authorisation first."]},

    {"name": "sha256sum & hashing", "cat": "Evidence Integrity", "modules": "M6, M10",
     "desc": "Cryptographic hashing produces a fixed fingerprint of a file; change "
             "one byte and the fingerprint changes completely. It is the "
             "mathematical backbone of evidence integrity and chain of custody.",
     "usage": "Hash evidence before and after handling and record it; verify later "
              "against the recorded value to prove nothing changed.",
     "commands": [
        {"cmd": "sha256sum evidence.img", "desc": "Compute the SHA-256 fingerprint."},
        {"cmd": "sha256sum evidence.img > evidence.sha256", "desc": "Record the hash to a manifest file."},
        {"cmd": "sha256sum -c evidence.sha256", "desc": "Verify the file still matches the record."},
        {"cmd": "md5sum / sha1sum file", "desc": "Other algorithms (SHA-256 is preferred today)."}],
     "tips": ["Prefer SHA-256 — MD5 and SHA-1 are broken for collision resistance.",
              "A matching before/after hash is what makes your findings defensible."]},

    # ── Powerful tools for the career ahead (deep "learn it here" entries) ──
    {"name": "Maltego", "cat": "OSINT & Link Analysis", "modules": "Extends M1 (OSINT)",
     "desc": "The industry-standard graph tool for open-source intelligence and link "
             "analysis. You start from one 'entity' (a person, domain, email, company, "
             "IP) and run 'transforms' that discover related entities, drawing the whole "
             "web of connections as a visual graph you can keep pivoting on.",
     "how": "Everything is an entity (a node) and a transform (an automated query that "
            "takes an entity and returns related ones — e.g. 'domain → DNS names', "
            "'email → breaches', 'person → social profiles'). Transforms call data "
            "sources (public records, DNS, breach data, your own) and plot the results, "
            "so one click fans out dozens of new leads you can transform again.",
     "usage": "Install the free Community Edition, register a free account, drop your "
              "starting entity on the graph, right-click it and run transforms, then "
              "pivot on whatever looks interesting. Investigate only what you're "
              "authorised to.",
     "workflow": [
        "Open Maltego CE and start a new graph.",
        "Drag an entity from the palette (e.g. Domain) and set it to your target, e.g. lab-corp.com.gh.",
        "Right-click → run a transform set (e.g. 'DNS from Domain', 'To Email addresses').",
        "New entities appear linked to the first — right-click those and transform again to go deeper.",
        "Select nodes to see properties; use the layout buttons to make the picture readable.",
        "Export the graph/report as your OSINT evidence."],
     "commands": [
        {"cmd": "(GUI tool — no CLI)", "desc": "Maltego is graph-driven; you work in its canvas."},
        {"cmd": "Right-click entity → Run Transform", "desc": "The core action: expand an entity into related ones."},
        {"cmd": "Machines → run a Machine", "desc": "Chain many transforms automatically (e.g. 'Footprint L1')."}],
     "tips": ["The free Community Edition is enough to learn the whole model.",
              "Think in 'entity → transform → new entities'; that loop is the entire tool.",
              "It visualises the same passive-recon you do by hand in M1 with dig/whois/theHarvester."],
     "install": "Download Maltego CE from maltego.com (also ships on Kali). Register a free Community account on first launch.",
     "learn": "docs.maltego.com"},

    {"name": "SpiderFoot", "cat": "OSINT Automation", "modules": "Extends M1 (OSINT)",
     "desc": "An automation engine that runs a target through 200+ OSINT data sources at "
             "once — DNS, WHOIS, breach data, certificates, dark-web mentions, open "
             "ports — and correlates everything into one searchable result set, through "
             "a clean web UI.",
     "how": "You give it a 'seed' (domain, IP, email, name). Its modules each query one "
            "data source; results from one module become inputs to others, so it "
            "spiders outward automatically and links findings (this IP → this domain → "
            "this breach) without you running each query by hand.",
     "usage": "Start the web server, open the UI, create a scan with your seed and a use "
              "case (e.g. 'Footprint' / 'Investigate'), run it, then browse the "
              "correlations and export.",
     "workflow": [
        "Run `spiderfoot -l 127.0.0.1:5001` and open the URL in a browser.",
        "New Scan → enter the target seed → pick a use case (Footprint for breadth).",
        "Start the scan and watch modules populate results live.",
        "Browse by data type (Emails, Hosts, Vulnerabilities…) or the correlation view.",
        "Export CSV/GEXF for your report."],
     "commands": [
        {"cmd": "spiderfoot -l 127.0.0.1:5001", "desc": "Start the web UI on localhost:5001."},
        {"cmd": "spiderfoot -s example.com -t DOMAIN_NAME", "desc": "Run a scan from the command line."},
        {"cmd": "spiderfoot -M", "desc": "List all available modules."}],
     "tips": ["Great first OSINT tool — the web UI makes the whole discipline visible.",
              "Turn off intrusive modules for purely passive recon.",
              "'Investigate' and 'Footprint' use cases are the two you'll start with."],
     "install": "Pre-installed on Kali, or: pip install spiderfoot / clone github.com/smicallef/spiderfoot.",
     "learn": "github.com/smicallef/spiderfoot"},

    {"name": "Recon-ng", "cat": "OSINT Framework", "modules": "Extends M1 (OSINT)",
     "desc": "A reconnaissance framework that feels like Metasploit but for OSINT: a "
             "modular console where you load modules, set options and run them, with all "
             "results stored in a workspace database you can report on.",
     "how": "Everything lives in a workspace (a SQLite DB). You add a 'seed' to a table "
            "(e.g. domains), load a module (e.g. hackertarget host lookup), set its "
            "source to that table, and run — results are written back to tables "
            "(hosts, contacts, credentials) that feed the next module.",
     "usage": "Create a workspace, add seeds, use the marketplace to install modules, "
              "load + run them, then generate a report.",
     "workflow": [
        "`recon-ng` → `workspaces create lab-corp`.",
        "`marketplace install all` (or install the specific modules you need).",
        "`db insert domains` → add lab-corp.com.gh.",
        "`modules load recon/domains-hosts/hackertarget` → `run`.",
        "`show hosts` to see results; `modules load reporting/html` → `run` for a report."],
     "commands": [
        {"cmd": "workspaces create <name>", "desc": "Isolate an investigation in its own DB."},
        {"cmd": "marketplace search / install", "desc": "Find and install modules."},
        {"cmd": "modules load <path> ; options set ; run", "desc": "The load → configure → run loop."},
        {"cmd": "show hosts / contacts", "desc": "View what's been gathered so far."}],
     "tips": ["If you know Metasploit's console, Recon-ng is instantly familiar.",
              "Some modules need free API keys (`keys add ...`); many work without.",
              "The workspace DB means you can stop and resume an investigation."],
     "install": "Pre-installed on Kali, or clone github.com/lanmaster53/recon-ng.",
     "learn": "github.com/lanmaster53/recon-ng/wiki"},

    {"name": "Shodan", "cat": "Attack-Surface Search", "modules": "Extends M1 (recon)",
     "desc": "A search engine for internet-connected devices. It continuously scans the "
             "whole internet and indexes what each IP exposes — banners, services, "
             "versions, certificates — so you can search for exposed assets the way "
             "Google searches web pages.",
     "how": "Shodan's scanners connect to ports across the internet and record the "
            "service banner each returns. You query that index with filters (port, "
            "product, country, org), and it returns the matching hosts — a defender's "
            "early-warning tool for finding their own exposed assets before attackers do.",
     "usage": "Use the website or the CLI with a free API key. VIEW ONLY — Shodan shows "
              "you what is already public; never connect to or attack anything you find "
              "that you don't own (Act 1038).",
     "workflow": [
        "Make a free account at shodan.io; copy your API key.",
        "`shodan init <API_KEY>` once.",
        "Search your OWN org's IP range / domain to see what you expose.",
        "Filter down (port:, product:, org:, country:GH) to find the risky exposures.",
        "Feed findings into your own asset inventory and remediation list."],
     "commands": [
        {"cmd": "shodan init <API_KEY>", "desc": "Store your API key once."},
        {"cmd": "shodan host 8.8.8.8", "desc": "Everything Shodan knows about one IP."},
        {"cmd": "shodan search \"port:3389 country:GH\"", "desc": "Find exposed RDP in a country (example)."},
        {"cmd": "shodan domain example.com", "desc": "Subdomains and exposed services for a domain."}],
     "tips": ["Use it to audit YOUR OWN exposure monthly — before someone else does.",
              "It only reports what's already public; looking is fine, touching is not.",
              "Censys is a close alternative with similar power."],
     "install": "Website: shodan.io. CLI: pip install shodan (needs a free API key).",
     "learn": "help.shodan.io"},

    {"name": "OWASP Amass", "cat": "Attack-Surface Mapping", "modules": "Extends M1/M3",
     "desc": "The leading open-source tool for mapping an organisation's external "
             "attack surface — especially subdomain discovery — by combining dozens of "
             "passive sources with optional active DNS techniques.",
     "how": "Passive mode asks many third-party data sources (certificate logs, search "
            "engines, DNS databases) for names under a domain and merges them. Active "
            "mode additionally resolves and brute-forces names and can attempt zone "
            "transfers — so you move from 'what others already know' to 'what actually "
            "resolves right now'.",
     "usage": "Start passive (no packets to the target), review the names, then go "
              "active only against assets you're authorised to test.",
     "workflow": [
        "`amass enum -passive -d example.com` to gather names quietly.",
        "Review the list — unexpected subdomains (vpn., dev., old.) are the gold.",
        "`amass enum -active -d example.com` (authorised targets) to confirm what resolves.",
        "`amass viz` to produce a graph of the discovered surface."],
     "commands": [
        {"cmd": "amass enum -passive -d example.com", "desc": "Passive subdomain discovery (quiet)."},
        {"cmd": "amass enum -active -d example.com", "desc": "Active resolution + brute force (authorised only)."},
        {"cmd": "amass intel -org 'Acme'", "desc": "Find domains/ranges belonging to an org."},
        {"cmd": "amass db -names -d example.com", "desc": "Show results stored from earlier runs."}],
     "tips": ["Passive first, always — it's recon nobody can see.",
              "Forgotten subdomains are the classic foothold; this is how you find yours.",
              "Pairs naturally with the DNS work you do in M1."],
     "install": "Pre-installed on Kali, or: github.com/owasp-amass/amass (releases).",
     "learn": "github.com/owasp-amass/amass"},

    {"name": "OWASP ZAP", "cat": "Web App Testing", "modules": "Extends M4 (web)",
     "desc": "The free, open-source web-application security scanner from OWASP — a "
             "full-featured alternative to Burp Suite. It acts as an intercepting proxy "
             "and can passively and actively scan a web app for vulnerabilities.",
     "how": "You browse the target through ZAP, which sits as a proxy between your "
            "browser and the app, recording every request/response. It passively flags "
            "issues as you browse, can 'spider' the app to map every page, and can "
            "'active-scan' by replaying requests with malicious payloads to confirm "
            "flaws like XSS and SQLi.",
     "usage": "Point your browser's proxy at ZAP (or use its built-in browser), browse "
              "the authorised app, let it spider, then run an active scan and triage the "
              "alerts.",
     "workflow": [
        "Launch ZAP → 'Automated Scan' with the target URL for a quick pass.",
        "Or: set your browser proxy to ZAP, browse the app so ZAP learns the pages.",
        "Right-click the site → Spider to map it; review passive alerts.",
        "Right-click → Active Scan to confirm injectable issues (authorised only).",
        "Work the Alerts tab by risk; export the report."],
     "commands": [
        {"cmd": "zaproxy", "desc": "Launch the ZAP GUI."},
        {"cmd": "zap.sh -quickurl http://target -quickout report.html", "desc": "Headless quick scan to a report."},
        {"cmd": "(GUI) Automated Scan", "desc": "Point-and-shoot scan of a URL."}],
     "tips": ["Free and beginner-friendly — the best way to learn proxy-based web testing.",
              "Passive scanning (just browsing through ZAP) is safe and surprisingly revealing.",
              "Only active-scan targets you own or are authorised to test."],
     "install": "Pre-installed on Kali (zaproxy), or download from zaproxy.org.",
     "learn": "zaproxy.org/docs"},

    {"name": "Ghidra", "cat": "Reverse Engineering", "modules": "Beyond M6 (malware RE)",
     "desc": "A free, powerful software reverse-engineering suite released by the NSA. "
             "It disassembles and decompiles binaries (malware, firmware, unknown "
             "executables) so you can read what they actually do — with a remarkably "
             "good C-like decompiler.",
     "how": "You import a binary; Ghidra analyses it, identifies functions, and produces "
            "both assembly and a readable decompiled C view side by side. You navigate "
            "the call graph, rename variables/functions as you understand them, and "
            "follow strings and imports to find the interesting behaviour (network "
            "calls, file writes, persistence).",
     "usage": "Create a project, import the sample, let auto-analysis run, then start "
              "from strings/imports and read the decompiler. Analyse malware only in an "
              "isolated VM.",
     "workflow": [
        "New Project → import the binary → let auto-analysis complete.",
        "Open the Symbol Tree / Strings window to find interesting anchors (URLs, 'CreateService').",
        "Double-click a string's reference to jump to the function that uses it.",
        "Read the Decompiler pane; rename functions/variables as meaning emerges.",
        "Trace from main() or from the suspicious API calls to understand the logic."],
     "commands": [
        {"cmd": "ghidraRun", "desc": "Launch Ghidra."},
        {"cmd": "(GUI) File → Import File", "desc": "Load a binary into a project."},
        {"cmd": "(GUI) Window → Decompiler", "desc": "The readable C-like view of a function."}],
     "tips": ["The decompiler makes RE approachable without years of assembly.",
              "ALWAYS reverse malware in an isolated, snapshotted VM with no network.",
              "Start from strings and imports — they point straight at the behaviour."],
     "install": "Download from ghidra-sre.org (needs a JDK). Also packaged on Kali.",
     "learn": "ghidra-sre.org"},

    {"name": "Suricata", "cat": "Intrusion Detection (IDS/IPS)", "modules": "Extends M3/M4 (detection)",
     "desc": "A high-performance open-source IDS/IPS and network-security-monitoring "
             "engine. It inspects live or captured traffic against rules and raises "
             "alerts — the engine behind the detection you design in M3/M4.",
     "how": "Suricata reads packets (from an interface or a pcap), reassembles flows, "
            "and matches them against signature rules (and protocol logic). A rule says "
            "'alert if a DNS query ends in .ddns.net from an internal host more than N "
            "times' — when traffic matches, it logs an alert (eve.json) you can ship to "
            "a SIEM.",
     "usage": "Run it over a pcap to test rules offline, or on an interface for live "
              "monitoring; write/enable rules for the behaviours you care about.",
     "workflow": [
        "Write or enable rules in /etc/suricata/rules (e.g. the C2-beacon rule from M3).",
        "Test against a capture: `suricata -r capture.pcap -l ./out`.",
        "Read ./out/eve.json (or fast.log) for the alerts that fired.",
        "Tune the rule (thresholds, allow-lists) to cut false positives.",
        "Deploy on a span/tap interface for live detection; forward eve.json to Wazuh/ELK."],
     "commands": [
        {"cmd": "suricata -r capture.pcap -l ./out", "desc": "Run rules against a saved capture."},
        {"cmd": "suricata -i eth0", "desc": "Live monitoring on an interface."},
        {"cmd": "suricata -T", "desc": "Test the configuration and rules for errors."},
        {"cmd": "jq . out/eve.json", "desc": "Read the JSON event/alert log."}],
     "tips": ["Testing rules against a pcap is the fastest way to learn detection engineering.",
              "Behaviour-based rules (a beacon pattern) beat single-IP rules — Pyramid of Pain.",
              "Snort is the close cousin with similar rule syntax."],
     "install": "Pre-installed on Kali, or: apt install suricata; rules via suricata-update.",
     "learn": "docs.suricata.io"},

    {"name": "Greenbone / OpenVAS", "cat": "Vulnerability Scanning", "modules": "Extends M4",
     "desc": "A full open-source vulnerability scanner (the Greenbone Community Edition, "
             "formerly OpenVAS). It probes hosts against a huge, updated feed of "
             "vulnerability tests and produces prioritised, CVSS-scored reports — the "
             "tool behind the 'discover' step of the M4 vulnerability-management loop.",
     "how": "A scanner engine runs tens of thousands of network vulnerability tests "
            "(NVTs) against each target — checking versions, configurations and known "
            "CVEs — and a manager stores the results, scores them with CVSS and renders "
            "reports. You drive it from a web UI (the Greenbone Security Assistant).",
     "usage": "Set up a scan target (authorised IPs), run a Full and Fast scan, then "
              "triage the report with the M4 model (CVSS + KEV + exposure).",
     "workflow": [
        "Open the Greenbone web UI; create a Target (your authorised IP range).",
        "Create a Task using the 'Full and Fast' scan config → start it.",
        "When done, open the report; sort findings by severity.",
        "Re-prioritise with context: internet-facing? in CISA KEV? critical asset? (M4).",
        "Export the report into your remediation register and re-scan after fixing (verify)."],
     "commands": [
        {"cmd": "gvm-setup / gvm-start", "desc": "Set up and start the Greenbone stack."},
        {"cmd": "(web UI) Scans → Tasks → New", "desc": "Create and launch a scan."},
        {"cmd": "(web UI) Scans → Reports", "desc": "Review CVSS-scored findings."}],
     "tips": ["Scanning finds the flaws; the skill (M4) is prioritising them by context.",
              "Credentialed scans find far more than unauthenticated ones.",
              "Only scan assets you own or are authorised to test."],
     "install": "Pre-installed on Kali (run `gvm-setup`), or Greenbone CE from greenbone.net.",
     "learn": "greenbone.net / docs.greenbone.net"},

    {"name": "YARA", "cat": "Malware Identification", "modules": "Beyond M6 (threat hunting)",
     "desc": "A pattern-matching tool that lets analysts write rules to identify and "
             "classify files (especially malware) by textual or binary patterns. "
             "'The pattern-matching Swiss army knife for malware researchers.'",
     "how": "You write a rule describing strings and/or byte sequences and a condition "
            "('any 2 of these strings', 'this header at offset 0'). YARA scans files or "
            "memory and flags anything whose content satisfies a rule — so one good rule "
            "catches a whole malware family across samples.",
     "usage": "Write or download rules, then scan files, directories or a memory image "
              "to hunt for known-bad patterns.",
     "workflow": [
        "Identify tell-tale strings/bytes in a known sample (e.g. its C2 URL, a mutex).",
        "Write a .yar rule: a `strings:` block + a `condition:`.",
        "Scan with `yara rule.yar suspicious/` across files or a memory dump.",
        "Refine the condition to avoid false positives, then share the rule with your team."],
     "commands": [
        {"cmd": "yara rule.yar /path/to/scan", "desc": "Scan files/dirs against a rule."},
        {"cmd": "yara -r rules/ samples/", "desc": "Recursively apply many rules."},
        {"cmd": "yara rule.yar 1234", "desc": "Scan a running process by PID (memory)."}],
     "tips": ["YARA rules turn 'I've seen this once' into 'we detect it everywhere'.",
              "Huge free rule sets exist (e.g. the YARA-Rules project) to learn from.",
              "Pairs with M6 memory forensics — scan memory.raw for known families."],
     "install": "Pre-installed on Kali, or: apt install yara / pip install yara-python.",
     "learn": "virustotal.github.io/yara"},

    {"name": "MISP", "cat": "Threat Intelligence Platform", "modules": "Extends M1 (CTI)",
     "desc": "The leading open-source Threat-Intelligence Platform. Institutions use it "
             "to store, structure and SHARE indicators of compromise (IPs, domains, "
             "hashes, TTPs) as 'events', and to feed those indicators automatically into "
             "their defences.",
     "how": "Analysts record an incident as an event containing attributes (the IOCs) "
            "and context (ATT&CK techniques, confidence). MISP correlates attributes "
            "across events (so you see 'this IP appears in three campaigns'), and "
            "communities share events with each other via synchronised feeds and an API "
            "that pushes IOCs to firewalls/SIEMs.",
     "usage": "Browse/search events, add your own with their IOCs and ATT&CK tags, and "
              "subscribe to trusted feeds; let correlations and the API do the rest.",
     "workflow": [
        "Log in to your MISP; search existing events for an indicator you're triaging.",
        "Create an Event for a new incident; add attributes (the IOCs) and galaxy tags (ATT&CK).",
        "Review auto-correlations linking your IOCs to other events.",
        "Publish/share with your community; export IOCs (STIX/CSV) or push via API to defences."],
     "commands": [
        {"cmd": "(web UI) Add Event → add Attributes", "desc": "Record an incident and its IOCs."},
        {"cmd": "(web UI) Galaxies", "desc": "Tag with ATT&CK techniques / threat actors."},
        {"cmd": "PyMISP (API)", "desc": "Automate IOC ingest/export into your tooling."}],
     "tips": ["This is what 'a threat-intel platform' in M1 actually looks like in practice.",
              "The value grows with sharing — join sector/CERT communities.",
              "Tag everything with ATT&CK so indicators carry behaviour, not just values."],
     "install": "Try the demo at misp-project.org; deploy via the official docker/VM images.",
     "learn": "misp-project.org"},

    {"name": "Gophish", "cat": "Phishing Simulation (authorised)", "modules": "Extends M5 (awareness)",
     "desc": "An open-source phishing-simulation framework used by security teams to run "
             "AUTHORISED phishing-awareness campaigns against their own staff and measure "
             "who clicks — turning M5's human-factor lessons into a measurable control.",
     "how": "You build a campaign from four pieces: a sending profile (SMTP), an email "
            "template, a landing page, and a target group. Gophish sends the emails, "
            "tracks opens/clicks/submissions via a unique link per recipient, and shows "
            "the results on a dashboard — so you can report the phishing-failure-rate "
            "metric from M9.",
     "usage": "Only ever against your OWN organisation with leadership sign-off. Build "
              "the four pieces, launch, and report the click/submit rates to drive "
              "training.",
     "workflow": [
        "Start gophish; log in to the admin UI.",
        "Create a Sending Profile (your test SMTP), an Email Template and a Landing Page.",
        "Import your staff list as a Users & Groups entry.",
        "Launch a Campaign; watch opens/clicks/credential-submits on the dashboard.",
        "Report the failure rate and feed it into awareness training (M5/M9)."],
     "commands": [
        {"cmd": "./gophish", "desc": "Start the server; open the admin UI (default :3333)."},
        {"cmd": "(web UI) Campaigns → New", "desc": "Assemble and launch a simulation."},
        {"cmd": "(web UI) Dashboard", "desc": "Opens / clicks / submitted-data per recipient."}],
     "tips": ["AUTHORISED internal use only — phishing your own staff needs written sign-off; anything else is illegal.",
              "The goal is a trend you drive DOWN over time, not to shame people.",
              "Pair with a short just-in-time training page for anyone who clicks."],
     "install": "Download the release binary from getgophish.com (single binary).",
     "learn": "docs.getgophish.com"},

    {"name": "BloodHound", "cat": "Active Directory Attack Paths", "modules": "Extends M3 (identity)",
     "desc": "A tool that maps the hidden attack paths inside an Active Directory domain "
             "as a graph, revealing how a foothold on one ordinary machine can reach "
             "Domain Admin through chains of permissions nobody designed on purpose — "
             "the M3 lateral-movement lesson made visible.",
     "how": "A collector (SharpHound) gathers AD data — users, groups, sessions, ACLs, "
            "local-admin rights — and BloodHound loads it into a graph database. It then "
            "answers questions like 'shortest path from this user to Domain Admins' by "
            "walking edges (MemberOf, AdminTo, HasSession, CanRDP), exposing the "
            "escalation routes defenders must cut.",
     "usage": "Run SharpHound (in an authorised AD/lab) to collect, import the data into "
              "BloodHound, and run the built-in queries to find and then CLOSE the paths.",
     "workflow": [
        "Collect with SharpHound in the authorised domain → produces JSON/zip.",
        "Import the zip into the BloodHound UI.",
        "Run a pre-built query, e.g. 'Shortest Paths to Domain Admins'.",
        "Trace an edge (why can this user admin that box?) — that's the misconfig to fix.",
        "Re-collect after remediation to confirm the path is gone."],
     "commands": [
        {"cmd": "SharpHound -c All", "desc": "Collect AD data (authorised domain only)."},
        {"cmd": "(UI) upload the collection zip", "desc": "Load the graph."},
        {"cmd": "(UI) Pre-Built Analytics Queries", "desc": "Find paths to high-value targets."}],
     "tips": ["Attackers use it to find paths; defenders use it to DELETE them — same tool.",
              "Tiering, LAPS and PAM (M3) are exactly what shorten these graphs.",
              "Only ever run the collector against a domain you're authorised to assess."],
     "install": "BloodHound Community Edition from specterops.io / github.com/SpecterOps/BloodHound.",
     "learn": "bloodhound.specterops.io"},

    {"name": "exiftool", "cat": "Metadata Forensics", "modules": "M5, M6",
     "desc": "The definitive tool for reading (and writing) embedded metadata in almost "
             "any file — photos, PDFs, Office documents. In an investigation it exposes "
             "who authored a file, with what software, and exactly when — the evidence "
             "that proves premeditation in M5.",
     "how": "Files carry hidden metadata fields (EXIF in images, XMP/DocProps in "
            "documents): Author, Create/Modify dates with timezone, GPS, camera/software. "
            "exiftool parses each container format and prints these fields, so a "
            "'Ghanaian supplier' document authored in a +07:00 timezone, days before it "
            "was emailed, gives the attacker away.",
     "usage": "Run it on any suspicious file and read the Author, Create Date (and its "
              "UTC offset), and Producer/Creator fields. Also use it to SCRUB metadata "
              "from files your own org publishes.",
     "workflow": [
        "`exiftool suspicious.pdf` — read every metadata field.",
        "Note Author, Create Date + timezone offset, Creator/Producer.",
        "Compare the create date to when the file was sent → premeditation (M5).",
        "To defend: `exiftool -all= file` strips metadata before you publish."],
     "commands": [
        {"cmd": "exiftool file.pdf", "desc": "Dump all metadata from a file."},
        {"cmd": "exiftool -Author -CreateDate file", "desc": "Read specific fields."},
        {"cmd": "exiftool -time:all -a -G1 file", "desc": "All timestamps with their groups/timezones."},
        {"cmd": "exiftool -all= file", "desc": "Strip all metadata (defensive scrubbing)."}],
     "tips": ["The attacker is careful with the email and careless with the attachment — read the file.",
              "'Created before sent' is the line that turns a dispute into proven fraud.",
              "Scrub metadata from documents your organisation puts online."],
     "install": "Pre-installed on Kali, or: apt install libimage-exiftool-perl.",
     "learn": "exiftool.org"},

    {"name": "bulk_extractor", "cat": "Forensic Carving", "modules": "M6",
     "desc": "A digital-forensics tool that scans a disk image, memory dump or any blob "
             "and automatically extracts useful features — email addresses, URLs, IPs, "
             "credit-card numbers — into tidy per-type files, without needing to "
             "understand the filesystem.",
     "how": "It reads the raw bytes in parallel and runs 'scanners' that recognise "
            "patterns (an email, a URL, a PAN) wherever they appear — including in "
            "deleted, fragmented or unallocated space the filesystem can't see — and "
            "writes each type to its own output file (url.txt, email.txt).",
     "usage": "Point it at an image or RAM dump; read the categorised output files to "
              "triage what indicators are present before deeper analysis.",
     "workflow": [
        "`bulk_extractor -o out memory.raw` to scan a RAM dump or disk image.",
        "Read out/url.txt for C2/exfil URLs, out/email.txt for exfil addresses.",
        "Cross-check hits against your other evidence (the M6 correlation step).",
        "Use the histograms to see the most frequent indicators quickly."],
     "commands": [
        {"cmd": "bulk_extractor -o out evidence.img", "desc": "Scan an image into categorised feature files."},
        {"cmd": "cat out/url.txt", "desc": "Extracted URLs (C2 / exfil candidates)."},
        {"cmd": "cat out/email.txt", "desc": "Extracted email addresses."}],
     "tips": ["It finds indicators even in unallocated space the filesystem has 'lost'.",
              "A perfect triage pass before slow, targeted analysis.",
              "Pairs with strings + Volatility in the M6 memory workflow."],
     "install": "Pre-installed on Kali, or: apt install bulk-extractor.",
     "learn": "github.com/simsong/bulk_extractor"},
]

# Linux / Kali command reference (group, command, description). Mirrors the
# Day-1 orientation lesson (m0) so students also find it under the Commands view.
LINUX_COMMANDS = [
    ("Identity & help", "whoami", "Print your current username."),
    ("Identity & help", "id", "Your user id and groups (shows sudo/root power)."),
    ("Identity & help", "hostname", "The machine's name."),
    ("Identity & help", "uname -a", "Kernel and architecture of the system."),
    ("Identity & help", "man <cmd>", "Open a command's full manual (q to quit, / to search)."),
    ("Identity & help", "<cmd> --help", "Quick option summary for a command."),
    ("Identity & help", "apropos <word>", "Find commands related to a keyword."),
    ("Navigation", "pwd", "Print the working directory — where you are."),
    ("Navigation", "ls -la", "List all files in detail, including hidden ones."),
    ("Navigation", "ls -lh", "List with human-readable sizes (K, M, G)."),
    ("Navigation", "cd /etc", "Change to a directory (absolute path)."),
    ("Navigation", "cd ..", "Go up one level;  cd ~ home;  cd - previous."),
    ("Navigation", "tree -L 2", "Show a directory tree, two levels deep."),
    ("Reading files", "cat file", "Print a whole file."),
    ("Reading files", "less file", "Page through a large file (q quit, / search)."),
    ("Reading files", "head -n 20 file", "First 20 lines;  tail -n 20 the last 20."),
    ("Reading files", "tail -f /var/log/auth.log", "Follow a log live as it grows (vital in IR)."),
    ("Reading files", "file evidence.img", "Identify what a file really is."),
    ("Reading files", "strings binary", "Pull readable text out of a binary."),
    ("Reading files", "xxd file | head", "Raw hex view — forensics staple."),
    ("Files & dirs", "mkdir -p a/b/c", "Create nested directories in one go."),
    ("Files & dirs", "touch file", "Create an empty file / update its timestamp."),
    ("Files & dirs", "cp -r src dst", "Copy recursively (work on copies of evidence)."),
    ("Files & dirs", "mv a b", "Move or rename."),
    ("Files & dirs", "rm -rf dir", "Delete a folder and all of it — irreversible, careful."),
    ("Finding things", "find /home -name '*.pcap'", "Find files by name anywhere under a path."),
    ("Finding things", "find . -type f -mtime -1", "Files modified in the last day (IR triage)."),
    ("Finding things", "which nmap", "Where a command lives on disk."),
    ("Finding things", "grep -r 'password' /etc 2>/dev/null", "Search file contents recursively."),
    ("Pipes & redirection", "cmd1 | cmd2", "Send one command's output into the next."),
    ("Pipes & redirection", "cmd > out.txt", "Write output to a file;  >> appends."),
    ("Pipes & redirection", "cmd 2>/dev/null", "Discard error output."),
    ("Pipes & redirection", "cmd | tee out.txt", "Show on screen AND save to a file."),
    ("Text processing", "grep -i 'error' log", "Case-insensitive search;  -v invert;  -c count."),
    ("Text processing", "grep -E 'T10[0-9]{2}' f", "Extended-regex search (e.g. ATT&CK IDs)."),
    ("Text processing", "cut -d',' -f1,3 data.csv", "Pull columns from delimited text."),
    ("Text processing", "sort f | uniq -c | sort -rn", "Count values, most-frequent first (the analyst one-liner)."),
    ("Text processing", "awk '{print $1}' access.log", "Extract a column from a log."),
    ("Permissions", "chmod +x labctl", "Make a file executable."),
    ("Permissions", "chmod 600 id_rsa", "Owner-only (private keys must be 600)."),
    ("Permissions", "chown user:group file", "Change owner/group (usually needs sudo)."),
    ("Privilege", "sudo <cmd>", "Run one command as root."),
    ("Privilege", "sudo -l", "What you're allowed to run as root."),
    ("Processes", "ps aux", "Every running process."),
    ("Processes", "ps aux | grep ssh", "Is a given process running?"),
    ("Processes", "top", "Live process/resource monitor (q to quit)."),
    ("Processes", "kill -9 <pid>", "Force-stop a process (last resort)."),
    ("Networking", "ip a", "Your network interfaces and IP addresses."),
    ("Networking", "ping -c 4 10.13.3.10", "Is a host reachable? (4 packets)."),
    ("Networking", "ss -tulpn", "Listening TCP/UDP ports and their processes."),
    ("Networking", "dig example.com MX", "Query DNS records."),
    ("Networking", "curl -I https://site", "Fetch just the HTTP response headers."),
    ("Networking", "nc -lvnp 4444", "Netcat: listen on a port."),
    ("Packages", "sudo apt update && sudo apt install -y nmap", "Refresh and install a package."),
    ("Packages", "apt search forensic", "Search for packages."),
    ("Archives & integrity", "tar -czf a.tgz dir/", "Create a compressed archive;  -xzf extracts."),
    ("Archives & integrity", "base64 -d file", "Decode Base64 (e.g. an obfuscated artefact)."),
    ("Archives & integrity", "sha256sum file", "Fingerprint a file;  -c verifies against a manifest."),
    ("System & disk", "df -h", "Disk space per filesystem."),
    ("System & disk", "du -sh *", "Size of each item here;  free -h shows memory."),
    ("Shortcuts", "history / !! / Ctrl-R", "Command history / repeat last / reverse-search."),
    ("Shortcuts", "Tab", "Auto-complete commands and paths."),
    ("Shortcuts", "Ctrl-C / Ctrl-L", "Cancel the running command / clear the screen."),
]

# labctl command cheat-sheet (group, command, description).
COMMANDS = [
    ("Learn", "labctl learn", "List all modules — lesson, lab and deliverable status."),
    ("Learn", "labctl learn m3", "Read a module's full teaching lesson."),
    ("Labs", "labctl list", "List all labs with their status and your progress."),
    ("Labs", "labctl info m3", "Show a lab's briefing and target IPs."),
    ("Labs", "labctl start m3", "Bring up a lab's isolated targets (waits until ready)."),
    ("Labs", "labctl status", "Show which lab targets are currently running."),
    ("Labs", "labctl verify m3", "Submit your findings and get graded."),
    ("Labs", "labctl reset m3", "Destroy and rebuild a lab clean."),
    ("Labs", "labctl stop m3", "Stop a lab's targets (or all)."),
    ("Deliverables", "labctl worksheet", "List the deliverable templates."),
    ("Deliverables", "labctl worksheet m2", "Copy a module's templates to your work folder."),
    ("Progress", "labctl progress", "Show your overall course completion."),
    ("Progress", "labctl whoami Your Name", "Set your name for progress tracking."),
    ("Setup", "labctl doctor", "Check Docker and tools are ready."),
    ("Setup", "labctl prep", "Pre-build all lab images for offline use (run once)."),
]
