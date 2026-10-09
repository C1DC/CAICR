# M4 — Vulnerability Management & SOC Operations

**Scenario.** You run vulnerability assessment and SOC triage for an
organisation. A web server is exposed, staff passwords are weak, and your SIEM
is lighting up. Find what's wrong, prove why it matters, and turn a pile of
alerts into one clear attack story.

Targets: `10.13.4.10` (web) · `10.13.4.20` (ssh).
Evidence in `assets/`: `lab_hashes.txt`, `lab-wordlist.txt`, `wazuh-alerts.json`.

> **Boundary.** Hydra and John are run **only** against the lab targets and the
> provided hash file. Using them anywhere else is a criminal offence (Act 1038).

---

## 1. Web vulnerability scan — Nikto

```
$ nikto -h http://10.13.4.10
$ curl http://10.13.4.10/robots.txt        # what paths does it give away?
$ curl http://10.13.4.10/config.php.bak    # what leaked here?
```
Find the sensitive **admin path** and the **backup file** that exposes database
credentials. (Think CVSS + exposure + exploitability when you prioritise.)

## 2. Why weak passwords lose — Hydra & John

```
# online guessing against the SSH service (authorised target only)
$ hydra -l labuser -P assets/lab-wordlist.txt ssh://10.13.4.20

# offline cracking of stolen hashes
$ john --wordlist=assets/lab-wordlist.txt assets/lab_hashes.txt
$ john --show assets/lab_hashes.txt
```
What password does Hydra find for `labuser`? What is `admin`'s cracked password?
*(In the real world you'd use `/usr/share/wordlists/rockyou.txt` — the lab ships
a tiny list so it runs instantly offline.)*

## 3. SIEM triage — Wazuh alerts

The alert feed your SIEM would show is in `assets/wazuh-alerts.json`. Triage it:

```
$ jq -r '.[] | "\(.rule.level)\t\(.rule.description)"' assets/wazuh-alerts.json | sort -rn
$ jq -r '.[].data.srcip // empty' assets/wazuh-alerts.json | sort | uniq -c
$ jq '[.[].rule.level] | max' assets/wazuh-alerts.json
```
Answer:
- the **highest severity level** firing,
- the **source IP** behind both the brute force and the web scan,
- whether the attacker **ultimately got in** (find the success event from that
  same IP, after the failures) — this is the correlation that turns noise into
  an incident.

Then map the SSH brute force to a **MITRE ATT&CK** technique.

---

## Grade yourself

```
$ labctl verify m4
```
