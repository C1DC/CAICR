# Forensics Toolbox — DFIR Tools by Domain (Free & Paid)

A practitioner's catalogue of the digital-forensics & incident-response (DFIR)
tools used in the field, grouped by **what you're investigating** — disk, memory,
Windows, macOS, Linux, mobile (Android/iOS), email, network — plus **online
analysis services**, forensic **distributions**, and **practice data**. It pairs
with Module 6 (do the hands-on) and Module 5 (email).

**Cost legend:** **Free** = free / open-source · **Paid** = commercial licence ·
**Freemium** = usable free tier, paid for more. Links are domains; search the exact
project to confirm the current build and licence.

::: warning | The law comes before the tool
These tools are powerful and many can *acquire* data from devices. Use them **only**
on evidence you are **authorised** to examine — your own devices, a sanctioned lab,
or a case you are lawfully assigned. Imaging or extracting data from someone else's
phone, computer or account without authority is an offence under Ghana's
**Cybersecurity Act 2020 (Act 1038)** and breaches the **Data Protection Act (Act
843)**. Always: **work on a copy, hash it, keep chain of custody** (Module 6).
:::

---

## 1 · Acquisition & Imaging (make the forensic copy first)

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **FTK Imager** | Free | The field-standard imager (raw/E01); previews files; captures live RAM | exterro.com |
| **Guymager** | Free | Fast Linux GUI imager (raw/E01) with auto-verify | guymager.sourceforge.io |
| **dc3dd / dcfldd** | Free | CLI `dd` with built-in hashing & logging | github |
| **ewfacquire** (libewf) | Free | Scriptable E01 acquisition | github.com/libyal/libewf |
| **Magnet ACQUIRE** | Free | Disk & mobile acquisition (registration) | magnetforensics.com |
| **Belkasoft Acquisition Tool** | Free | Disk, mobile, cloud and RAM acquisition | belkasoft.com |
| **Paladin** (Sumuri) | Free | Bootable forensic imaging Linux (write-blocked) | sumuri.com |
| **Tableau write-blockers** | Paid | Hardware write-blockers for safe acquisition | opentext.com |

---

## 2 · Disk Forensics & All-in-One Suites

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **The Sleuth Kit (TSK)** | Free | The CLI engine: `fls`, `icat`, `fsstat`, `mactime` | sleuthkit.org |
| **Autopsy** | Free | The GUI over TSK — case, ingest modules, keyword search, timeline, reporting | autopsy.com |
| **PhotoRec / TestDisk** | Free | File carving & partition recovery (no filesystem needed) | cgsecurity.org |
| **bulk_extractor** | Free | Scan an image/blob and auto-carve emails, URLs, IPs, cards | github |
| **X-Ways Forensics** | Paid | Lightweight, extremely powerful examiner suite | x-ways.net |
| **Magnet AXIOM / AXIOM Cyber** | Paid | All-in-one: computer + mobile + cloud in one case | magnetforensics.com |
| **OpenText EnCase Forensic** | Paid | The long-standing courtroom suite | opentext.com |
| **Exterro FTK (Forensic Toolkit)** | Paid | Indexed, database-backed examiner suite | exterro.com |
| **Belkasoft X** | Paid | Computer + mobile + cloud suite | belkasoft.com |

---

## 3 · Memory Forensics (RAM)

**Acquire RAM first** (Module 6 — order of volatility), then analyse.

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **WinPmem / WinPMEM** | Free | Windows RAM acquisition | github.com/Velocidex |
| **Magnet RAM Capture** | Free | Simple Windows RAM capture | magnetforensics.com |
| **LiME** | Free | Linux Memory Extractor (kernel module) | github.com/504ensicsLabs |
| **AVML** (Microsoft) | Free | Portable Linux memory acquisition | github.com/microsoft/avml |
| **Volatility 3** (and 2) | Free | The standard memory-analysis framework (`pstree`, `netscan`, `cmdline`, `malfind`) | volatilityfoundation.org |
| **MemProcFS** | Free | Mount a memory image as a browsable filesystem | github.com/ufrisk |
| **Mandiant Redline** | Free | Host/memory IOC collection & triage | cloud.google.com/mandiant |

---

## 4 · Windows Forensics (artefacts, registry, event logs, triage)

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **Eric Zimmerman's Tools (EZ Tools)** | Free | The essential set: **MFTECmd, Registry Explorer, EvtxECmd, Timeline Explorer, PECmd (prefetch), AmcacheParser, JLECmd, LECmd, SrumECmd** | ericzimmerman.github.io |
| **KAPE** (Kroll) | Free | Targeted triage collection + parsing at speed | kroll.com/kape |
| **Chainsaw** | Free | Hunt EVTX logs with Sigma rules, fast | github.com/WithSecureLabs |
| **Hayabusa** | Free | EVTX threat hunting & timelining (Sigma) | github.com/Yamato-Security |
| **RegRipper** | Free | Registry-hive parsing to readable output | github.com/keydet89 |
| **Sysinternals** (Autoruns, Process Explorer, Procmon) | Free | Live triage: autostarts, process tree, live activity | learn.microsoft.com/sysinternals |
| **Velociraptor** | Free | Fleet-wide endpoint hunting & artefact collection (DFIR at scale) | docs.velociraptor.app |
| **Hindsight** | Free | Browser-history forensics (Chrome/Edge) | github.com/obsidianforensics |

---

## 5 · macOS Forensics

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **mac_apt** | Free | macOS Artifact Parsing Tool — broad artefact extraction | github.com/ydkhatri |
| **AutoMacTC** | Free | Automated macOS triage collector | github.com/CrowdStrike |
| **APOLLO** | Free | Pattern-of-life timeline from macOS/iOS databases | github.com/mac4n6 |
| **UnifiedLogReader** | Free | Parse the macOS/iOS Unified Logs | github.com/ydkhatri |
| **Objective-See (KnockKnock, BlockBlock, LuLu)** | Free | Persistence, malware & firewall tools for macOS | objective-see.org |
| **Magnet AXIOM / X-Ways / FTK** | Paid | Full macOS (APFS) support in the commercial suites | — |

---

## 6 · Linux / Unix Forensics

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **UAC** (Unix-like Artifacts Collector) | Free | Live-response triage collection on Linux/macOS/ESXi/*nix | github.com/tclahr/uac |
| **CyLR / Catscale** | Free | Fast artefact collectors for *nix/Windows | github |
| **The Sleuth Kit / Autopsy** | Free | ext4/XFS filesystem analysis | sleuthkit.org |
| **Volatility (Linux profiles)** | Free | Linux memory analysis (with LiME/AVML captures) | volatilityfoundation.org |
| **chkrootkit / rkhunter** | Free | Rootkit detection on a live/mounted system | chkrootkit.org |
| **Loki / THOR Lite** (Nextron) | Free | IOC & YARA scanner for compromise assessment | nextron-systems.com |
| **Built-ins** (`auditd`/`ausearch`, `journalctl`, `last`, `/proc`, bash history) | Free | The native evidence sources (Module 3 §7.2) | — |

---

## 7 · Mobile Forensics — Android & iOS

The commercial suites dominate device **extraction** (especially modern locked
phones); the open-source tools excel at **parsing and analysis** of what you
extract (and at spyware checks).

**Commercial (extraction + analysis):**

| Tool | Cost | Focus | Site |
|------|------|-------|------|
| **Cellebrite UFED / Inseyets / Physical Analyzer** | Paid | Industry leader; broad device extraction & analysis | cellebrite.com |
| **Magnet Graykey** | Paid | iOS/Android extraction (incl. locked devices) | magnetforensics.com |
| **MSAB XRY / XAMN** | Paid | Methodical extraction + analysis | msab.com |
| **Oxygen Forensic Detective** | Paid | Mobile + cloud + app data | oxygenforensics.com |
| **Elcomsoft iOS Forensic Toolkit / Phone Breaker** | Paid | iOS-focused extraction & cloud (iCloud) | elcomsoft.com |
| **MOBILedit Forensic** | Paid | Accessible mobile extraction suite | mobiledit.com |

**Free / open-source (acquisition helpers + parsing + spyware):**

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **ALEAPP** | Free | Android Logs, Events And Protobuf Parser — parse an Android extraction | github.com/abrignoni/ALEAPP |
| **iLEAPP** | Free | iOS Logs, Events And Plists Parser — parse an iOS extraction | github.com/abrignoni/iLEAPP |
| **MVT (Mobile Verification Toolkit)** | Free | Amnesty International's spyware/Pegasus check for iOS & Android | mvt.re |
| **Andriller** | Free | Android logical acquisition + decoders | andriller.com |
| **ADB** (Android Debug Bridge) | Free | Logical acquisition / `adb backup` / logcat | developer.android.com |
| **libimobiledevice** | Free | iOS device comms; `idevicebackup2` for backups | libimobiledevice.org |
| **APOLLO** | Free | Pattern-of-life timeline across iOS databases | github.com/mac4n6 |

::: key | Mobile reality check
Modern phones are **encrypted by default**, so *extraction* from a locked, up-to-date
device often needs the commercial tools (Cellebrite/Graykey/XRY). But once you have
a backup or an extraction, **iLEAPP/ALEAPP** parse it for free into a readable
report, and **MVT** checks for spyware — a powerful free workflow for consented or
lawfully-acquired data.
:::

---

## 8 · Email Forensics

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **Mozilla Thunderbird** | Free | Open and read mailboxes (MBOX/EML/IMAP) for review | thunderbird.net |
| **libpff / pffexport** | Free | Parse Outlook **PST/OST** archives | github.com/libyal/libpff |
| **readpst** (pst-utils) | Free | Convert PST to MBOX/EML | — |
| **msgconvert** | Free | Convert Outlook `.msg` to `.eml` | metacpan.org |
| **emldump / oledump** (D. Stevens) | Free | Pull parts/attachments out of EML/MSG safely | blog.didierstevens.com |
| **MxToolbox / Google Messageheader** | Free (online) | Paste headers → delivery path + SPF/DKIM/DMARC | mxtoolbox.com |
| **Aid4Mail** | Paid | Email forensics, migration & search at scale | aid4mail.com |
| **MailXaminer** (SysTools) | Paid | Dedicated email-examination suite | systoolsgroup.com |
| **Intella** (Vound) | Paid | E-discovery & email investigation | vound-software.com |

*(Reading headers, defanging links and checking attachments is Module 5 §3.)*

---

## 9 · Network Forensics (PCAP)

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **Wireshark / tshark** | Free | The protocol analyser; Follow Stream, Export Objects | wireshark.org |
| **NetworkMiner** | Freemium | Forensics-friendly pcap parse: hosts, files, creds, images | netresec.com |
| **Zeek** | Free | Turn a pcap into rich logs (conn/dns/http/files) | zeek.org |
| **Suricata** | Free | Run IDS rules over a pcap to label known-bad | suricata.io |
| **Arkime** (ex-Moloch) | Free | Large-scale full-packet-capture indexing & search | arkime.com |
| **Brim / Zui** | Free | Desktop app to query pcap/Zeek logs | zui.brimdata.io |
| **tcpdump** | Free | CLI capture on servers | tcpdump.org |

*(The IR workflow is Module 6 §7.)*

---

## 10 · Malware Analysis & Reverse Engineering

| Tool | Cost | What it does | Site |
|------|------|--------------|------|
| **Ghidra** (NSA) | Free | Full-featured disassembler/decompiler | ghidra-sre.org |
| **Cutter / radare2 / rizin** | Free | Open reverse-engineering framework + GUI | cutter.re |
| **x64dbg** | Free | Windows user-mode debugger | x64dbg.com |
| **IDA Free / IDA Pro** | Freemium/Paid | The classic disassembler | hex-rays.com |
| **PEStudio / PE-bear / Detect It Easy (DIE)** | Free | Static triage of Windows executables | — |
| **CAPA** (Mandiant) | Free | Identify a binary's capabilities from patterns | github.com/mandiant/capa |
| **YARA** | Free | Pattern-match/classify files & memory | virustotal.github.io/yara |
| **oletools / olevba** | Free | Dump & flag Office macros without opening them | github.com/decalage2 |
| **pdf-parser / peepdf** | Free | Analyse malicious PDFs | blog.didierstevens.com |
| **REMnux** | Free | A whole Linux distro of malware-analysis tools | remnux.org |
| **FLARE-VM** | Free | A Windows malware-analysis environment | github.com/mandiant/flare-vm |

---

## 11 · Online Analysis Services (free web pages — no install)

Fast, browser-based analysis. **Never upload confidential/personal data** to public
services (Act 843), and **never visit live malicious URLs** — submit, don't browse.

| Service | Cost | Use it to | Site |
|---------|------|-----------|------|
| **VirusTotal** | Freemium | Scan a file/URL/hash vs 70+ engines; pivot indicators | virustotal.com |
| **Hybrid Analysis** | Free | Automated malware sandbox report | hybrid-analysis.com |
| **Any.Run** | Freemium | Interactive sandbox — watch malware run live | any.run |
| **Recorded Future Triage** | Free | Fast automated malware sandbox | tria.ge |
| **Joe Sandbox (Community)** | Freemium | Deep sandbox analysis | joesandbox.com |
| **urlscan.io** | Free | Sandbox-visit a URL: screenshot, IOCs, contacted domains | urlscan.io |
| **CyberChef** | Free | Decode/decrypt/deobfuscate; EXIF; extract URLs — offline-capable | gchq.github.io/CyberChef |
| **CIRCL hashlookup** | Free | Is this hash a known-good (NSRL) or known-bad file? | hashlookup.circl.lu |
| **MalwareBazaar / ThreatFox / URLhaus** (abuse.ch) | Free | Look up a sample/IOC/URL by hash or indicator | abuse.ch |
| **AbuseIPDB / GreyNoise / Talos** | Freemium | IP/domain reputation; "targeted vs internet-noise" | abuseipdb.com |
| **Jeffrey's Image Metadata Viewer** | Free | Read a photo's EXIF/GPS metadata online | exif.tools |
| **unfurl** (Ryan Benson) | Free | Break a URL/token into its meaning | dfir.blog/unfurl |
| **EpochConverter / DCode** | Free | Convert timestamps between formats | epochconverter.com |
| **jwt.io** | Free | Decode & inspect a JSON Web Token | jwt.io |
| **crt.sh** | Free | Certificate-transparency search → subdomains | crt.sh |

---

## 12 · Forensic Distributions & IR Platforms

| Platform | Cost | What it is | Site |
|----------|------|------------|------|
| **SANS SIFT Workstation** | Free | The classic DFIR Linux toolkit | sans.org/tools/sift-workstation |
| **REMnux** | Free | Malware-analysis Linux distro | remnux.org |
| **CAINE** | Free | Italian forensic live distro | caine-live.net |
| **Tsurugi Linux** | Free | DFIR/OSINT/malware distro | tsurugi-linux.org |
| **Kali Linux** | Free | The offensive + DFIR distro (this course's platform) | kali.org |
| **TheHive + Cortex** | Free | Incident-response case management + analyzers | strangebee.com |
| **DFIR IRIS** | Free | Collaborative incident-response case management | dfir-iris.org |
| **Timesketch** (Google) | Free | Collaborative forensic timeline analysis | timesketch.org |
| **MISP** | Free | Threat-intelligence sharing platform | misp-project.org |
| **Velociraptor** | Free | Endpoint visibility, hunting & collection | velociraptor.app |

---

## 13 · Practice Data & Keeping Current

**Practice evidence (safe, legal to analyse):**

- **malware-traffic-analysis.net** — real annotated malware PCAPs with exercises.
- **NIST CFReDS** (cfreds.nist.gov) — reference disk images & scenarios.
- **Digital Corpora** (digitalcorpora.org) — disk, memory & network datasets.
- **CyberDefenders** (cyberdefenders.org) — full DFIR/blue-team challenges.
- **Volatility sample images** — public memory dumps to practise on.
- **DFIR CTF images** — Ali Hadi's challenges, DFIR Madness, aboutDFIR's test-image list.

**Keep current & go deeper:**

- **aboutDFIR.com** — a maintained directory of tools, training and resources.
- **forensicfocus.com** — news, articles and community.
- **DFIR Diva** (dfirdiva.com) — curated *free* training.
- **This Week in 4n6** (thisweekin4n6.com) — the weekly DFIR roundup.
- **SANS DFIR posters & cheat-sheets** (sans.org/posters) — Windows/memory/smartphone.
- **NIST SP 800-86** (forensic techniques into IR) and **ISO/IEC 27037** (acquisition) — the standards.

::: key | The free stack can take you a long way
A capable examiner can work most cases on **Autopsy + Sleuth Kit + Volatility +
Wireshark + the EZ Tools + iLEAPP/ALEAPP + CyberChef + VirusTotal** — all free. The
paid suites add scale, locked-mobile extraction, indexing and court-ready workflow;
reach for them when the case (or the courtroom) demands it, not by default.
:::
