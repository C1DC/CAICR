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

# Kali tool reference shown in the Tools & Materials view.
TOOLS = [
    {"name": "theHarvester", "cat": "OSINT & Recon", "modules": "M1",
     "purpose": "Gather domain intelligence — emails, hosts, IPs — from public sources."},
    {"name": "dig", "cat": "DNS & Domain Intel", "modules": "M1, M5",
     "purpose": "Query DNS records (MX, TXT/SPF/DMARC, A, NS) — the checks attackers run before phishing."},
    {"name": "whois", "cat": "DNS & Domain Intel", "modules": "M1, M5",
     "purpose": "Look up domain registration — age and owner reveal look-alike/impersonation domains."},
    {"name": "Nmap", "cat": "Network Scanning", "modules": "M3, M4, M10",
     "purpose": "Discover live hosts, open ports, services and OS fingerprints."},
    {"name": "Wireshark", "cat": "Packet Analysis", "modules": "M3, M10",
     "purpose": "Inspect traffic; spot suspicious DNS, C2 beaconing and cleartext credentials."},
    {"name": "tcpdump", "cat": "Packet Capture", "modules": "M3",
     "purpose": "Command-line capture and quick filtering of network traffic."},
    {"name": "Nikto", "cat": "Web Vulnerability Scan", "modules": "M4",
     "purpose": "Scan web servers for misconfigurations, risky files and outdated software."},
    {"name": "Hydra", "cat": "Credential Testing", "modules": "M4",
     "purpose": "Demonstrate online password guessing against authorised lab targets."},
    {"name": "John the Ripper", "cat": "Password Analysis", "modules": "M4",
     "purpose": "Crack sample hashes offline to show why password policy and MFA matter."},
    {"name": "Wazuh (triage)", "cat": "Security Monitoring", "modules": "M4, M10",
     "purpose": "Triage and correlate SIEM alerts into a single attack story."},
    {"name": "Autopsy / Sleuthkit", "cat": "Digital Forensics", "modules": "M6, M10",
     "purpose": "Examine disk images — list files, recover deleted data, build a timeline."},
    {"name": "CyberChef", "cat": "Data Analysis & Decode", "modules": "M6, M10",
     "purpose": "Decode and transform obfuscated artefacts (Base64, URL, hex) offline."},
    {"name": "sha256sum", "cat": "Evidence Integrity", "modules": "M6, M10",
     "purpose": "Hash evidence before/after handling to prove integrity (chain of custody)."},
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
