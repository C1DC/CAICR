**Work a full evidence package — disk, memory and logs — and correlate it into one story.**  ·  Day 3 · ~2.5 h · 14 graded tasks · file-based (nothing to launch)

::: note | What this lab is
Workstation **FIN-03** is suspected in a ransomware incident. The responder
captured a **disk image**, a **RAM dump**, and the host's **auth log** before the
machine was wiped. You prove the evidence is intact (hashing), recover a deleted
file, carve the malware and its C2/credentials out of memory, decode an
obfuscated dropper, reconstruct the timeline from the logs, and **correlate** all
three sources. You practise Sleuthkit, `strings`/`bulk_extractor`, CyberChef and
log analysis.
:::

## What's running

This is a **file-based lab — there are no targets to launch.** The evidence is in
the lab's `assets/` (personalised to you): `evidence.img` + `evidence.sha256`
(disk), `memory.raw` (RAM), `auth.log` (host logs), `suspicious_artifact.txt` (an
obfuscated dropped string).

## How to use this lab

**In the GUI (this page):**
1. Click **Start** once to personalise your evidence (status: **file-based**; no
   containers).
2. In the **Terminal** tab, work the five phases in forensic order.
3. Enter findings in the **Verify** panel → **Submit & grade**.

**Prefer the terminal?** `labctl start m6` → investigate → `labctl verify m6`.

::: warning | The guards — read before you start
- **Golden rule: hash first, analyse second — work on copies, never originals.**
  The first graded check is that `sha256sum -c` still passes.
- The VPN password, C2 domain and exfil email are **randomised to you** — and the
  disk and memory copies of the VPN password are made to **match** so you can
  prove the correlation.
- This is analysis of captured evidence — no live hosts, nothing to attack.
:::

## The mission — step by step

### 1. Integrity & disk forensics

```Terminal
cd labs/m6-forensics/assets
sha256sum evidence.img ; sha256sum -c evidence.sha256   # prove integrity
fsstat evidence.img                                     # filesystem type
fls evidence.img                                        # list files (* = deleted)
icat evidence.img 6                                     # read the deleted file
```

Find the filesystem, the **macro-enabled lure** the user opened, and recover the
**deleted VPN credentials**.

### 2. Decode the dropper (CyberChef)

```Terminal
base64 -d suspicious_artifact.txt        # one layer; then URL-decode
```

Recover the **C2 domain** — you'll see it again in memory.

### 3. Memory triage (strings / bulk_extractor)

```Terminal
strings memory.raw | grep -iE 'svch0st|\.ps1|vpnadmin|schtasks'
bulk_extractor -o be_out memory.raw
cat be_out/url.txt ; cat be_out/email.txt
```

Carve out: the **malware** (masquerading as a service), the **C2 host** the
PowerShell stager calls (it matches the decoded dropper — your correlation), the
**in-memory VPN credential**, the **exfil email**, and the **persistence**
(scheduled task).

### 4. Reconstruct the timeline (logs)

```Terminal
grep -E 'Failed|Accepted|sudo|CRON' auth.log
```

Build the sequence: brute force → **successful login** → sudo to root →
persistence (cron). Identify the **source IP** and the **account** compromised.

### 5. Correlate & conclude

Tie the sources together (dropper C2 == memory C2; brute-force IP == attacker;
scheduled task in memory == cron line in log), note the **order of volatility**,
and map macro→PowerShell to **MITRE ATT&CK**.

## What you'll be graded on

14 checks in the **Verify** panel across integrity, disk, memory, logs and
correlation. Then produce the paperwork:

```Terminal
labctl verify m6
labctl worksheet m6    # chain-of-custody form + incident report
```

::: key | Tips
- "Deleted" ≠ gone — `icat`/`tsk_recover` bring the file back.
- Memory holds what disk never saw — the plaintext VPN password lives in RAM.
- The same VPN password on **disk and in RAM** is your correlation: a lead
  becomes proof when two independent sources agree.
:::
