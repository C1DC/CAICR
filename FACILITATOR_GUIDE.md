# CAIC CyberLab — Facilitator Run-of-Show

**Professional Certificate in Cybersecurity, AI & Digital Resilience**
KAIPTC · Cyber1Defense Communication Ltd · 5 intensive days

This is the delivery playbook: what to run, when, and how to unblock students.
Model answers for every lab are in **`FACILITATOR_ANSWER_KEY.md`** (regenerate
with `python3 scripts/answer_key.py`). Validate the whole suite before class with
`python3 scripts/dry_run.py` (expect "ALL LABS PASS").

---

## The teaching rhythm (every module)

1. **Teach** the lesson (10–20 min) — students read it in the app (Course view)
   or you project `labctl learn m<N>`; it's chaptered, use the TOC to pace.
2. **Demo** the first command live on your screen.
3. **Do** — students run the lab (`labctl start m<N>` → work → `labctl verify
   m<N>`) or complete the leadership worksheet (`labctl worksheet m<N>`).
4. **Debrief** — walk the answer key; draw out the "why" and the Ghana cases.

Each student drives everything from one command, `labctl`, or the browser app
(`./start.sh`). Progress saves per-machine; `labctl progress` shows completion.

---

## Day 1 — Threat Landscape, Kali & Institutional Risk

### 09:00 Orientation (`labctl learn m0`) — 45 min
- Cover the rules of engagement (only `10.13.x.x`, Act 1038) and walk the Linux
  command-line primer. Have everyone run the "first fifteen minutes" block.
- **Check the room is ready:** `labctl doctor` on every machine (green ticks).

### 09:45 M1 — Threat Intelligence & OSINT  *(lab, 19 checks)*
- Teach §1–6 of the lesson; demo `dig` and the AXFR zone transfer.
- Students: `labctl start m1` → work the practicum → `labctl verify m1`.
- **The "aha":** the AXFR zone transfer leaking `vpn-admin` (10.20.0.7).
- Deliverable: threat brief (`labctl worksheet m1`).
- **Common stumbles:** querying the real internet instead of `@10.13.1.10`;
  missing that *no DMARC* = spoofable; typing the full DKIM key instead of the
  selector `default`.

### 13:00 M2 — Institutional Risk  *(leadership worksheet)*
- Teach the IF/THEN risk statement, 5×5 + FAIR, the four treatments, CSF 2.0.
- Students build the **risk register** + **CSF profile** (`labctl worksheet m2`);
  show the worked "Adom Microfinance" example at the foot of each template.
- **Common stumble:** risks with no named owner / no review date.

---

## Day 2 — Network Security & Vulnerability Operations

### 09:00 M3 — Network Compromise  *(lab, 16 checks)*
- Demo `nmap -sn` then `nmap -sV`; show Wireshark **Follow TCP Stream**.
- Students: `labctl start m3`; three evidence sources (scan + pcap + netstat).
- **The "aha":** the C2 domain in the pcap resolves to the C2 IP in the netstat,
  and the FTP username/password are readable in the clear.
- **Common stumbles:** counting the `.1` gateway as a target; not following the
  TCP stream to find the FTP creds.

### 13:00 M4 — Vulnerability Mgmt & SOC  *(lab, 16 checks)*
- Demo gobuster, then the hash-cracking chain (hashcat/John).
- Students: `labctl start m4`; fuzz → loot the leaked DB dump → crack → triage
  the Wazuh feed with `jq`.
- **The "aha":** the leaked `db_dump.sql` with unsalted MD5s that crack instantly.
- **Common stumbles:** chasing CVSS alone (teach KEV/EPSS + exposure); not
  correlating the Wazuh alerts by source IP.

---

## Day 3 — Cyber Fraud & Digital Forensics

### 09:00 M5 — BEC & Fraud  *(lab, 13 checks)*
- Demo reading headers with `grep`, then `exiftool` on the attachment.
- Students: `labctl start m5`; compare the two emails, trace the spoof, run
  exiftool on the PDF.
- **The "aha":** the PDF's `+07:00` authoring timezone and pre-dated creation —
  the attacker left metadata behind.
- Deliverable: fraud investigation brief + evidence timeline.

### 13:00 M6 — Digital Forensics & IR  *(lab, 15 checks)*
- Demo `sha256sum -c`, `fls`/`icat`, and memory carving with `strings` /
  `bulk_extractor`.
- Students: `labctl start m6`; disk + memory + logs, correlated.
- **The "aha":** the decoded dropper's C2 == the C2 carved from memory.
- **Common stumble:** the order-of-volatility point — *never power off; isolate*.

---

## Day 4 — AI Security, Privacy & Compliance

### 09:00 M7 — AI Security & Deepfakes  *(lab, 12 checks)*
- Demo a direct `/chat` injection; then the poisoned-document exfil.
- Students: `labctl start m7`; four vectors (injection, RAG poisoning, tool
  exfil, excessive agency) + the deepfake voicemail drill.
- **The "aha":** the AI's *poisoned knowledge base* returns a mule account as fact.
- Deliverable: AI risk assessment + verification protocol.

### 13:00 M8 — Privacy & Compliance  *(leadership worksheet)*
- Teach Act 843/1038, controller vs processor, GDPR benchmark, first-72-hours.
- Students complete the **breach assessment** + **compliance gap register**.
- **Common stumble:** "the cloud vendor is responsible" — accountability stays
  with the controller.

---

## Day 5 — Governance & Integrated Crisis Capstone

### 09:00 M9 — Governance & Business Continuity  *(leadership worksheet)*
- Teach governance vs management, board metrics, BIA/RTO/RPO, crisis command.
- Students write the **board cyber-risk memo** + **recovery priority table**.

### 10:30 M10 — Operation Cyber Resilience  *(capstone lab, 15 checks)*
- The full morning's crisis. Put students in four cells (Leadership, Technical,
  Fraud/Finance, Legal/Comms). `labctl start m10`.
- They work the live range **and** the evidence package, correlating one campaign
  (the mule account recurs in the BEC email *and* the poisoned AI; the foothold IP
  recurs across injects; the C2 domain ties to the exfil IP).
- Deliverable: incident dossier + 90-day roadmap + executive briefing.
- Close with each cell presenting; grade against the answer key + the dossier.

---

## Two tracks, one room

- **Technical Practitioner track** — executes every lab command and submits the
  `labctl verify` findings.
- **Institutional Leadership track** — observes the technical output and focuses
  on the worksheets (risk register, breach assessment, board memo). They still
  *read* the lab briefings and interpret the findings; they need not type the
  attack commands.

## If something breaks

- `labctl doctor` — the first diagnostic (Docker, tools, labs valid).
- Targets won't start → check Docker is running; `labctl reset m<N>` for a clean
  rebuild; a "subnet overlaps" error means another Docker network uses that
  range (edit `[network] subnet` in that lab's `lab.toml`).
- A student's scores are tangled → `labctl reset-progress`.
- Collect progress for grading → copy each student's
  `~/.local/share/caic-lab/state.json` and run `labctl report <folder>`.

---

## Assessment & certification

Three weighted components make the final grade: **labs 50% · quizzes 25% ·
exam 25%**, pass mark **70%** (`labctl grade`, or the Assessment page in the
web app).

- Quiz and exam options are **reshuffled per student** from the seed, so answers
  can't be copied. Correct answers (keyed by text, not letter) are in the second
  half of `FACILITATOR_ANSWER_KEY.md`.
- `labctl diagnostic` is an ungraded baseline — have students run it on Day 1 to
  self-place; it doesn't affect the grade.
- At 70% a student runs `labctl certificate` to produce a branded certificate
  (HTML → Print → Save as PDF) carrying a serial and verification code.
- To authenticate a certificate, run `labctl certificate --verify <code>` **on
  that student's machine** — the code is re-derived from their recorded
  achievement and seed, so a hand-edited certificate fails the check. This is an
  integrity check for the classroom, not a cryptographic anti-forgery guarantee.
