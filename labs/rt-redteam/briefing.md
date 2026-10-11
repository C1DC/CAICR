**Break into a live server, end to end — recon, loot, foothold, root.**  ·  Day 1 · ~75 min · 10 graded tasks · live isolated range

::: note | What this lab is
Your first real hack. There's one internal server on an isolated range you're
**authorised** to attack. You'll scan it, find a web service, discover a
credential a careless admin left in the web root, use it to **log in over SSH**,
grab the **user flag**, then abuse a **sudo misconfiguration** to become **root**
and grab the **root flag** — the complete attacker lifecycle in one sitting. Then
you flip to defender and name what would have stopped each step.
:::

## What's running

- **One live target — `10.13.2.10`** (hostname *intranet*): a Volta internal
  server exposing **web on :80** and **SSH on :22**. It's launched for you.

## How to use this lab

**In the GUI (this page):**
1. Click **Start** and wait for **● running**.
2. Open the **Terminal** tab and work the mission below with `nmap`, `curl` /
   `gobuster`, and `ssh`.
3. Enter each finding in the **Verify** panel → **Submit & grade**.
4. **Reset** rebuilds the box clean; **Stop** when done.

**Prefer the terminal?** `labctl start rt` → hack → `labctl verify rt`.

::: warning | The one rule that makes you a professional, not a criminal
Attack **only** `10.13.2.10` — the single authorised target on `10.13.2.0/24`.
Pointing these same tools at anything else is a criminal offence under Ghana's
Cybersecurity Act 2020 (Act 1038). The flags and password are **randomised to
you**, so report *your* values, not a neighbour's.
:::

## The mission — step by step

1. **Recon.** `nmap -sV 10.13.2.10` — confirm the two services and fingerprint the
   **web server software**.
2. **Enumerate the web.** `curl http://10.13.2.10/robots.txt` (it hints a hidden
   folder), or `gobuster dir -u http://10.13.2.10 -w /usr/share/wordlists/dirb/common.txt`.
   Find the **hidden directory**.
3. **Loot.** Read the ops note in that folder — it leaks the **SSH username and
   password**.
4. **Foothold.** `ssh webadmin@10.13.2.10` with the leaked password → you're in.
   `cat user.txt` for the **user flag**.
5. **Escalate.** `sudo -l` → webadmin may run a shell as root with no password.
   `sudo /bin/ash` → you're **root**. `cat /root/root.txt` for the **root flag**.
6. **Flip to defender.** Name the **ATT&CK technique** for the credential login and
   **one control** that would have broken the chain.

## What you'll be graded on

The **Verify** panel has 10 checks across the whole chain. (No written deliverable
required to pass, but the *First-Hack Report* template, `labctl worksheet rt`,
turns what you did into a mini penetration-test report — the professional habit.)

```Terminal
labctl verify rt
labctl worksheet rt    # optional: write it up as a short pentest report
```

::: key | Why this is first
You'll spend the week *defending*. This lab shows you the attacker's view first —
because you cannot defend a chain you've never walked. Notice how **small** each
step is (a forgotten file, a reused password, one sudo line) and how they **chain**
into total compromise. Every later module exists to break one of these links.
:::
