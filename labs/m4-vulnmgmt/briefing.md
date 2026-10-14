**Assess a leaky web server, loot and crack what you find, then turn the alert flood into one incident.**  ·  Day 2 · ~2.5 h · 20 graded tasks

::: note | What this lab is
You are the security engineer *and* the SOC analyst for Acme Payroll. A web
server is exposed, a database backup was left world-readable, and the SIEM is
lighting up. You assess the server (Nmap/whatweb/Nikto/gobuster), **loot** a
leaked backup and **crack** its unsalted-MD5 hashes (hashcat/John), prove a weak
SSH credential (Hydra), and triage a realistic **Wazuh** alert feed into one
correlated incident. The attacks are taught so you understand why the controls
(salting, MFA, correlation) are non-negotiable.
:::

## What's running

- **Two live targets:** `10.13.4.10` (leaky Apache web server), `10.13.4.20`
  (SSH host with a weak account — the authorised Hydra target).
- **Evidence files (`assets/`):** `lab-wordlist.txt`, `wazuh-alerts.json`, and the
  looted `db_dump.sql` / `config.php.bak` you pull from the web server.

## How to use this lab

**In the GUI (this page):**
1. Click **Start**; wait for **● running** on both targets.
2. In the **Terminal** tab, work the five parts below.
3. Enter findings in the **Verify** panel → **Submit & grade**.
4. **Reset** / **Stop** as needed.

**Prefer the terminal?** `labctl start m4` → investigate → `labctl verify m4`.

::: warning | The guards — read before you start
- Hydra, hashcat and John are run **only** against `10.13.4.10` / `10.13.4.20`
  and the **provided** hashes. Using them anywhere else is a criminal offence
  (Act 1038).
- The admin password (and its MD5 hash) and the DB password are **randomised to
  you** — crack and report *your own* values.
- These cracks are deliberately trivial (a tiny wordlist, unsalted MD5) so you
  *see* why the real controls matter — this is not how you'd attack production.
:::

## The mission — step by step

### Part 1 — Assess & fuzz the web server

```Terminal
nmap -sV -p80 10.13.4.10                 # server software + version
whatweb http://10.13.4.10                # web technology fingerprint
nikto -h http://10.13.4.10               # risky files, stale software, headers
gobuster dir -u http://10.13.4.10 -w /usr/share/wordlists/dirb/common.txt
curl http://10.13.4.10/backup/           # directory listing is ON…
curl http://10.13.4.10/config.php.bak    # …and a config backup leaks the DB password
```

### Part 2 — Loot & crack

The dump stores passwords as **unsalted MD5** (the point of the exercise):

```Terminal
curl -s http://10.13.4.10/backup/db_dump.sql     # read the dump
# put the 32-char hashes in hashes.txt, then crack offline:
hashcat -m 0 -a 0 hashes.txt assets/lab-wordlist.txt --potfile-disable
hashcat -m 0 hashes.txt --show
# or:  john --format=raw-md5 --wordlist=assets/lab-wordlist.txt hashes.txt
```

Recover **admin**'s and the **backup** account's plaintext passwords.

### Part 3 — Prove the weak SSH credential (Hydra)

```Terminal
hydra -l labuser -P assets/lab-wordlist.txt ssh://10.13.4.20
```

### Part 4 — Triage & correlate the SOC feed

```Terminal
jq -r '.[] | "\(.rule.level)\t\(.rule.description)"' assets/wazuh-alerts.json | sort -rn
jq -r '.[].data.srcip // empty' assets/wazuh-alerts.json | sort | uniq -c | sort -rn
jq '[.[].rule.level] | max' assets/wazuh-alerts.json
```

Reconstruct the chain from **one source IP**: brute force → web scan → successful
login → sudo to root → persistence (cron). Find the highest severity, whether the
attacker got in, and how they persisted.

### Part 5 — Deliver

Produce a **remediation register** (prioritise by CVSS + KEV + exposure) and a
**SOC triage ticket** for the correlated incident.

## What you'll be graded on

20 checks in the **Verify** panel — assessment, cracking, triage, and applying the toolkit. Then:

```Terminal
labctl verify m4
labctl worksheet m4    # remediation register + SOC case ticket
```

::: key | Tips
- Prioritise by **context**, not CVSS alone: internet-facing + in KEV + critical
  asset wins, even at a lower score.
- Ten alerts from one IP are **one incident**, not ten — correlation is the skill.
- The one control that makes every cracked password harmless: **MFA**.
:::
