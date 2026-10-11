# First-Hack Report (Mini Penetration Test) — Red Team Primer Deliverable

**Tester:** [your name]  **Date:** [YYYY-MM-DD]  **Authorised scope:** 10.13.2.10 only

> A real red-team engagement ends in a **report**, not a trophy. Write up your
> intrusion the way a professional pentester would: what you found, how you
> chained it, the evidence, and — most importantly — how to fix it. See
> `labctl learn rt`.

## 1. Engagement summary (BLUF)

[2–3 sentences: you achieved full compromise (root) of 10.13.2.10 starting from an
exposed web service; the root cause and the single most urgent fix.]

## 2. The attack chain (how you got in)

| Step | What you did | Evidence / finding |
|------|--------------|--------------------|
| Recon | `nmap -sV 10.13.2.10` | open services + web server software: [ ] |
| Enumerate | robots.txt / gobuster | hidden path: [ ] |
| Loot | read the leaked note | SSH user: [ ]  (password captured — do **not** paste it in a shared report) |
| Foothold | `ssh webadmin@10.13.2.10` | user flag: [ ] |
| Privilege escalation | `sudo -l` → `sudo /bin/ash` | method: [ ] · root flag: [ ] |

## 3. Findings & severity

| # | Finding | Severity | Why it matters |
|---|---------|----------|----------------|
| 1 | Backup/notes left in the web root | High | leaks live credentials to anyone |
| 2 | [FILL IN — credential in cleartext] | | |
| 3 | [FILL IN — SSH password auth, no MFA] | | |
| 4 | [FILL IN — NOPASSWD sudo to a shell] | High | instant root from any foothold |

## 4. ATT&CK mapping

- Initial access via leaked valid credentials: **T1078**
- Privilege escalation via sudo: **T1548 / T1548.003**
- (Recon/enumeration: T1595 · T1046)

## 5. Remediation (break the chain)

*One fix per finding — the attacker needs every link; you only need to break one.*

1. [e.g. remove the backup from the web root; rotate the exposed credential]
2. [e.g. enforce MFA / key-based SSH, disable password auth]
3. [e.g. remove the NOPASSWD sudo entry; apply least privilege]
4. [e.g. monitor/alert on the SSH login + sudo-to-root]

---

## Self-check before you submit

- [ ] My flags and password are **my own** (randomised per student).
- [ ] The chain reads step-by-step — each step enabled the next.
- [ ] Every finding has a **severity** and a **specific fix**.
- [ ] I only touched 10.13.2.10.

## Grading rubric (100 pts)

| Band | Chain reconstructed (40) | Findings & severity (30) | Remediation & ATT&CK (30) |
|------|--------------------------|--------------------------|---------------------------|
| Excellent | Full recon→root chain with evidence at each step | Each finding rated and justified | A real fix per link + correct ATT&CK |
| Adequate (~60%) | Got root, chain partly shown | Findings listed, thin severity | Generic fixes |
| Weak (<40%) | Flags only, no chain | No severity | No remediation |

---

## Worked example (reference — illustrative values, yours are randomised)

**BLUF:** Full root compromise of 10.13.2.10 from an unauthenticated web service in
minutes; root cause = a credential left in the web root plus a NOPASSWD sudo
shell. Fix MFA and the sudo entry today.

**Chain:** nmap → web (darkhttpd) + SSH open → robots.txt → `/backup/notes.txt`
leaked `webadmin` + password → `ssh webadmin@…` → `user.txt` flag → `sudo -l`
showed `NOPASSWD: /bin/ash` → `sudo /bin/ash` → root → `/root/root.txt` flag.

**Top fixes:** remove backups from the web root + rotate the credential (H);
enforce MFA / key-based SSH (H); remove the NOPASSWD sudo rule (H); alert on
sudo-to-root. **ATT&CK:** T1078 (valid accounts), T1548.003 (sudo).
