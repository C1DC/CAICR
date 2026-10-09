# M6 — Digital Forensics & IR: Disk, Memory & Timeline

**Scenario.** Workstation **FIN-03** is suspected in a ransomware incident. The
responder captured a disk image, a RAM dump, and the host's auth log before the
machine was wiped. Prove the evidence is intact, then reconstruct what happened
across all three sources and correlate them into one story.

Evidence in `assets/`: `evidence.img` + `evidence.sha256` (disk), `memory.raw`
(RAM), `auth.log` (host logs), `suspicious_artifact.txt` (a dropped, obfuscated
string).

> **Golden rule.** Hash first, analyse second. Work on copies, never originals.

---

## 1. Integrity & disk forensics

```
$ cd labs/m6-forensics/assets
$ sha256sum evidence.img ; sha256sum -c evidence.sha256   # prove integrity
$ fsstat evidence.img                                     # filesystem type
$ fls evidence.img                                        # list files (* = deleted)
$ icat evidence.img 6                                     # read the deleted file
$ tsk_recover evidence.img ./recovered                    # or carve it out
```
Find the filesystem, the **macro-enabled lure** the user opened, and recover the
**deleted VPN credentials**.

## 2. Decode the dropper (CyberChef)

```
$ base64 -d suspicious_artifact.txt        # one layer; then URL-decode
```
Recover the **C2 domain**. Remember it — you'll see it again in memory.

## 3. Memory triage (strings / bulk_extractor)

You don't have a Volatility profile for this capture, so triage by carving:

```
$ strings memory.raw | grep -iE 'svch0st|\.ps1|vpnadmin|schtasks'
$ bulk_extractor -o be_out memory.raw      # feature extraction
$ cat be_out/url.txt ; cat be_out/email.txt
```
Carve out: the **malicious executable** (masquerading as a service), the **C2
host** the PowerShell stager calls (it should match the decoded dropper — that's
your correlation), the **in-memory plaintext VPN credential**, the **exfil email
address**, and how the malware **persists** (a scheduled task).

## 4. Reconstruct the timeline (logs)

```
$ grep -E 'Failed|Accepted|sudo|CRON' auth.log
```
Build the sequence: brute force → **successful login** → sudo to root →
persistence (cron). Identify the **source IP** and the **account** that was
compromised.

## 5. Correlate & conclude

Tie the three sources together: the dropper's C2 == the memory C2; the brute-force
IP in the log == the attacker; the scheduled task in memory == the cron line in
the log. Note the **order of volatility** (why memory is collected first) and map
the macro→PowerShell execution to **MITRE ATT&CK**. Produce the evidence manifest,
chain-of-custody form and incident report in the worksheet.

---

## Grade yourself

```
$ labctl verify m6
$ labctl worksheet m6
```
