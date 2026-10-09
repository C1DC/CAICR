# M4 — Vulnerability Management & SOC Operations

**Scenario.** You are the security engineer *and* the SOC analyst for Acme
Payroll. A web server is exposed, a backup was left world-readable, and the SIEM
is lighting up. Assess the server, loot and crack what you find, prove the weak
credentials, and turn the alert flood into one clear incident.

Targets: `10.13.4.10` (web) · `10.13.4.20` (ssh). Evidence in `assets/`:
`lab-wordlist.txt`, `lab_hashes.txt`, `wazuh-alerts.json`.

> ⚠ Hydra, hashcat and John are run **only** against the lab targets and the
> provided hashes. Anywhere else is a criminal offence (Act 1038).

---

## Part 1 — Assess & fuzz the web server

```
$ nmap -sV -p80 10.13.4.10                 # server software + version
$ whatweb http://10.13.4.10                # web technology fingerprint
$ nikto -h http://10.13.4.10               # known issues, risky files, headers
$ gobuster dir -u http://10.13.4.10 -w /usr/share/wordlists/dirb/common.txt
$ curl http://10.13.4.10/backup/           # directory listing is ON...
$ curl http://10.13.4.10/config.php.bak    # ...and a config backup leaks creds
```

Find the exposed **admin path**, the **leaked database backup** under `/backup/`,
and the **database password** in the config backup.

## Part 2 — Loot & crack

Open `db_dump.sql`. The passwords are stored as **unsalted MD5** — the point of
the exercise. Extract the hashes and crack them offline:

```
$ curl -s http://10.13.4.10/backup/db_dump.sql     # read the dump
$ # put the 32-char hashes in hashes.txt, then:
$ hashcat -m 0 -a 0 hashes.txt assets/lab-wordlist.txt --potfile-disable
$ hashcat -m 0 hashes.txt --show
$ # or with John:
$ john --format=raw-md5 --wordlist=assets/lab-wordlist.txt hashes.txt ; john --show ...
```

Recover **admin**'s and the **backup** service account's plaintext passwords.
(In the real world you'd use `/usr/share/wordlists/rockyou.txt` — the lab ships a
tiny list so it cracks instantly offline.)

## Part 3 — Prove the weak SSH credential (Hydra)

```
$ hydra -l labuser -P assets/lab-wordlist.txt ssh://10.13.4.20
```

## Part 4 — Triage & correlate the SOC feed

```
$ jq -r '.[] | "\(.rule.level)\t\(.rule.description)"' assets/wazuh-alerts.json | sort -rn
$ jq -r '.[].data.srcip // empty' assets/wazuh-alerts.json | sort | uniq -c | sort -rn
$ jq '[.[].rule.level] | max' assets/wazuh-alerts.json
```

Reconstruct the chain from one source IP: **brute force → web scan → successful
login → sudo to root → persistence (cron) → exfiltration.** Identify the highest
severity, whether the attacker got in, and how they persisted.

## Part 5 — Deliver

In the worksheet, produce a **remediation register** (prioritise by CVSS + KEV +
exposure) and a **SOC triage ticket** for the correlated incident.

---

## Grade yourself

```
$ labctl verify m4
$ labctl worksheet m4
```
