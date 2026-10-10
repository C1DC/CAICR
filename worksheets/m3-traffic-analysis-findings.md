# Traffic Analysis Findings & Control Design — Module 3 Deliverable

**Analyst:** [your name]  **Date:** [YYYY-MM-DD]  **Authorised scope:** 10.13.3.0/24

> You are the on-call analyst at a Ghanaian financial institution. A host is
> suspected of compromise. Work the three evidence sources — the Nmap scan, the
> packet capture and the host's netstat dump — then design the controls that
> close each proven gap. Everything here must be supported by evidence you can
> point to. See `labctl learn m3`; submit with your findings filled in.

---

## 1. Host & service inventory (Nmap)

*Scan the range, fingerprint the services, and flag what should not be exposed.*

| Host IP | Open ports / services (with version) | Exposure concern |
|---------|--------------------------------------|------------------|
| [ ] | | [e.g. unauthenticated admin panel] |
| [ ] | | [e.g. anonymous + cleartext FTP] |
| [ ] | | [e.g. SSH — note the version] |
| [ ] | | [e.g. exposed legacy RDP] |

**Commands I ran (evidence):** `[e.g. nmap -sn …; nmap -sV -p … ; nmap --script ftp-anon …]`

## 2. Network behaviour (Wireshark / tcpdump)

| Finding | Value (from my evidence) | How I know |
|---------|--------------------------|------------|
| Infected / beaconing host IP | [ ] | [source IP of the repeated queries] |
| C2 domain | [ ] | [DNS filter in the capture] |
| Beacon interval (seconds) | [ ] | [timestamp delta between queries] |
| Why this is a beacon, not normal traffic | [ ] | [fixed interval, round-the-clock, dynamic-DNS] |
| Cleartext credential captured — username | [ ] | [Follow TCP Stream on the FTP session] |
| Cleartext credential captured — password | [ ] | [same stream, after USER] |

## 3. Endpoint evidence (netstat from the suspect host)

| Finding | Value | How I know |
|---------|-------|------------|
| Masquerading process name | [ ] | [read the spelling carefully vs svchost] |
| Backdoor port (LISTEN) | [ ] | [the odd high port it listens on] |
| External C2 IP (ESTABLISHED) | [ ] | [foreign address owned by that process] |
| Correlation check: does the C2 IP match the beacon domain's infrastructure? | [ yes / no ] | [this is what turns a hunch into proof] |

## 4. Attack narrative mapped to MITRE ATT&CK

*One or two sentences per stage — tell the story the evidence supports.*

| Stage | What happened here | ATT&CK ID |
|-------|--------------------|-----------|
| Reconnaissance | [ ] | T1046 |
| Initial access / credentials | [ ] | T1078 / T1040 |
| Defense evasion | [ ] | T1036 |
| Command & control | [ ] | T1071.004 |

## 5. Control design (map each proven gap to a fix, with priority)

| # | Finding (from §1–§3) | Recommended control | Priority (H/M/L) | Owner |
|---|----------------------|---------------------|------------------|-------|
| 1 | [e.g. RDP 3389 exposed] | [e.g. close port / VPN + MFA] | H | IT |
| 2 | [FILL IN] | [e.g. network segmentation] | | |
| 3 | [FILL IN] | [e.g. DNS monitoring/logging] | | |
| 4 | [FILL IN] | [e.g. replace FTP with SFTP] | | |

## 6. One-line summary for leadership (BLUF)

> [Business impact of what's exposed + the single most urgent fix, in plain
> language a non-technical director can act on.]

---

## Self-check before you submit

- [ ] Every value in §2–§3 is **my own** (randomised per student) — not copied.
- [ ] My C2 IP (§3) and C2 domain (§2) are **correlated** — I state whether they match.
- [ ] Each control in §5 traces to a specific finding in §1–§3.
- [ ] I named the **layer** and the **ATT&CK ID** for each stage.
- [ ] I scanned **only** 10.13.3.0/24.

## Grading rubric (how your facilitator marks this — 100 pts)

| Band | Inventory & scan (25) | Behaviour & creds (25) | Endpoint & correlation (25) | Controls & BLUF (25) |
|------|-----------------------|------------------------|-----------------------------|----------------------|
| Excellent (full) | All hosts + versions, every exposure named | Beacon + interval + both credentials, reasoned | Process, port, IP — **and** C2 correlation proven | Each gap → right control, prioritised; crisp BLUF |
| Adequate (~60%) | Most hosts, exposures partly named | Beacon found, creds partial | Process + port, no correlation | Generic controls, weak prioritisation |
| Weak (<40%) | Hosts only, no versions | "Looks suspicious", no evidence | Single source, no story | Controls not tied to findings |

---

## Worked example (reference — fictional "Adom Microfinance Ltd")

*Illustrative values — yours are randomised. This shows the standard expected.*

**§1 Inventory:** `10.20.5.10` HTTP 80 — *unauthenticated "Admin Console"*;
`10.20.5.20` FTP 21 — *anonymous login allowed (code 230), cleartext*;
`10.20.5.30` SSH 22 — *OpenSSH 9.7*; `10.20.5.40` RDP 3389 — *legacy, internet-reachable*.

**§2 Behaviour:** host `10.20.5.30` resolves `cdn-update.ddns.net` every **~30 s**
all night → **beacon** (fixed interval, dynamic-DNS, round-the-clock).
FTP stream yields `USER backupsvc` / `PASS S3rv!ce-2bf9` in the clear.

**§3 Endpoint:** process **`svch0st.exe`** (zero, not *o*) PID 3391 — LISTEN on
**4444** (backdoor) and ESTABLISHED to **203.0.113.47:443** (C2). The C2 IP
matches the address `cdn-update.ddns.net` resolves to — **correlation proven**.

**§4 Narrative:** scanned (T1046) → anonymous FTP + sniffed credentials
(T1078/T1040) → implant masquerading as svchost (T1036) → DNS beacon C2 (T1071.004).

**§5 Controls:** (1) close RDP, move to VPN+MFA — **H**, IT; (2) **segment** the
network so finance ≠ general LAN — **H**, IT; (3) **DNS logging + alert** on
dynamic-DNS beacons — **H**, SOC; (4) replace FTP with **SFTP**, rotate the
leaked credential — **M**, IT.

**§6 BLUF:** *"An internal workstation is actively controlled by an attacker over
a hidden channel, and our file server hands out credentials in plain text. Fund
network segmentation and DNS monitoring now; the exposure is live."*
