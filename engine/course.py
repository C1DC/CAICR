"""Shared course metadata: the module map, the Kali tool reference, and the
command cheat-sheet. Used by both the CLI and the web app so there is one
source of truth."""
from __future__ import annotations

# (id, day, title, has_lab)
COURSE_MAP = [
    ("m0",  1, "Orientation, Kali Linux & the Command Line", False),
    ("m1",  1, "Threat Landscape & Cyber Threat Intelligence", True),
    ("m2",  1, "Institutional Cyber Risk & Digital Resilience", False),
    ("m3",  2, "Network, Endpoint & Identity Security", True),
    ("m4",  2, "Vulnerability Management & SOC Operations", True),
    ("m5",  3, "Cyber Fraud, BEC & Mobile Money Security", True),
    ("m6",  3, "Digital Forensics & Incident Response", True),
    ("m7",  4, "AI Security, Deepfakes & Emerging Threats", True),
    ("m8",  4, "Data Protection, Privacy & Compliance", False),
    ("m9",  5, "Cyber Governance & Business Continuity", False),
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
