# Red Team Primer — Your First Hack

**Day 1 · After Orientation · ~1.5 hours · Hands-on lab: `labctl start rt`**

You are about to break into a server. Not read about it — *do* it: scan a live
machine, find the way in, steal a credential someone left lying around, log in,
and take over the whole box as root. In about an hour, with the same tools
professionals use, you will run a complete intrusion from the outside to full
control. That is not a stunt — it is the fastest way to understand everything
that follows this week, because **you cannot defend an attack you have never
walked through yourself.**

This module is the attacker's half of the story, told honestly and up front. The
rest of the programme is the defender's answer to it. By the end of today's first
lab you will have *felt* how a real compromise happens — how small each step is,
and how mercilessly they chain — and you will never look at "a forgotten backup
file" or "a reused password" the same way again.

::: outcome | By the end of this module you will be able to
1. Explain the **attacker's mindset** and why defenders must learn it first.
2. Distinguish **red, blue and purple** teams and where **penetration testing / ethical hacking** fits.
3. Walk the **anatomy of an attack** — recon → access → foothold → privilege escalation → objectives — and map it to the Cyber Kill Chain.
4. State the **non-negotiable ethics**: authorisation, scope, rules of engagement, and the law (Act 1038).
5. Run a **full live intrusion** with `nmap`, `gobuster`/`curl`, `ssh` and `sudo` — recon, loot a leaked credential, get a foothold, capture the user flag, escalate to **root**, capture the root flag.
6. **Flip to defender** and name the single control that breaks each link of the chain.
:::

### Session structure

| Time | Content |
|------|---------|
| 0:00 – 0:15 | Why we start by attacking; the attacker mindset; red/blue/purple |
| 0:15 – 0:30 | The anatomy of an attack + authorisation, scope and the law |
| 0:30 – 0:40 | The first-hack toolkit (nmap, gobuster/curl, ssh, sudo -l) |
| 0:40 – 1:20 | Lab: `labctl start rt` — Operation First Blood (recon → root) |
| 1:20 – 1:30 | Flip to defender: how each step is stopped (the rest of the week) |

::: note | Before you begin
**Mindset:** today you play the attacker — *inside a cage*. Everything is on an
isolated range on your own machine.
**Lab requirement:** a Kali terminal with `nmap`, `gobuster`, `curl`, `ssh`, and Docker running.
**Assessment:** the lab (`labctl verify rt`) is graded; the optional *First-Hack Report* (`labctl worksheet rt`) is the professional write-up.
**The rule:** the only authorised target is `10.13.2.10`. Nothing else, ever.
:::

---

## 1 · Why We Start by Attacking

Most courses open with definitions. We open with a break-in, for one reason:
**defence is a response to attack, so the attack has to be real to you first.**
When you have personally turned a forgotten file into a root shell, three things
change for good:

- You stop seeing controls as bureaucracy and start seeing them as the specific
  thing that would have stopped *you*.
- You develop the attacker's habit of **thinking in chains** — not "is this one
  thing dangerous?" but "what does this let me reach *next*?"
- You gain the confidence to investigate, because the tools are no longer
  mysterious.

The whole week is the defender's reply to this one hour. Keep that frame: today
you learn the punch so that for the next four days you can learn the block.

---

## 2 · Red, Blue & Purple — and Where "Ethical Hacking" Fits

Security work has colours:

- **Red team** — plays the attacker. Finds the ways in, proves what's exploitable,
  thinks like the adversary. **Penetration testing** and **ethical hacking** live
  here: authorised, scoped attacks that find the holes *before* criminals do.
- **Blue team** — defends. Builds the controls, watches the alerts (the SOC,
  Module 4), responds to incidents (Module 6). This is where most of you will work.
- **Purple team** — the loop between them: red attacks, blue detects and fixes, red
  tries again. The point was never red *versus* blue; it's red *improving* blue.

::: key | The ethical hacker's distinction
The only thing separating a penetration tester from a criminal is **authorisation**
— written permission, a defined scope, and rules of engagement. Same tools, same
techniques; one has a signed contract and one has a prison sentence. Hold that
line and the entire discipline is open to you.
:::

---

## 3 · The Anatomy of an Attack

Real intrusions are not one magic exploit; they are a **chain** of ordinary steps,
each enabling the next. The model you'll use all week is the **Cyber Kill Chain**
(Module 1 goes deep); here it is as the attacker actually moves:

```figure The attack chain — small steps that compound into total control
  RECON ─► ENUMERATE ─► GET ACCESS ─► FOOTHOLD ─► PRIVILEGE ESC ─► OBJECTIVES
  find the   what's      a way in     a shell as   become root/    loot, persist,
  target     exposed?    (creds/flaw) a user       admin           exfiltrate
~~~svg~~~
<svg viewBox="0 0 660 150" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">
  <defs><marker id="rt-a" markerWidth="9" markerHeight="9" refX="6" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="currentColor"/></marker></defs>
  <g text-anchor="middle" font-size="9.5">
    <rect x="8"   y="40" width="92" height="40" rx="6" fill="var(--teal,#2bb6a8)" fill-opacity="0.14" stroke="currentColor"/><text x="54" y="58" fill="currentColor" font-weight="bold">RECON</text><text x="54" y="72" fill="currentColor" opacity="0.8">find target</text>
    <rect x="116" y="40" width="98" height="40" rx="6" fill="var(--teal,#2bb6a8)" fill-opacity="0.14" stroke="currentColor"/><text x="165" y="58" fill="currentColor" font-weight="bold">ENUMERATE</text><text x="165" y="72" fill="currentColor" opacity="0.8">what's exposed?</text>
    <rect x="230" y="40" width="104" height="40" rx="6" fill="var(--gold,#e0a93b)" fill-opacity="0.16" stroke="currentColor"/><text x="282" y="58" fill="currentColor" font-weight="bold">GET ACCESS</text><text x="282" y="72" fill="currentColor" opacity="0.8">creds / flaw</text>
    <rect x="350" y="40" width="96" height="40" rx="6" fill="var(--gold,#e0a93b)" fill-opacity="0.16" stroke="currentColor"/><text x="398" y="58" fill="currentColor" font-weight="bold">FOOTHOLD</text><text x="398" y="72" fill="currentColor" opacity="0.8">shell as user</text>
    <rect x="462" y="40" width="104" height="40" rx="6" fill="var(--red,#ff6b7a)" fill-opacity="0.18" stroke="currentColor"/><text x="514" y="58" fill="currentColor" font-weight="bold">PRIV ESC</text><text x="514" y="72" fill="currentColor" opacity="0.8">become root</text>
    <rect x="582" y="40" width="70" height="40" rx="6" fill="var(--red,#ff6b7a)" fill-opacity="0.22" stroke="currentColor"/><text x="617" y="58" fill="currentColor" font-weight="bold">LOOT</text><text x="617" y="72" fill="currentColor" opacity="0.8">objectives</text>
  </g>
  <g stroke="currentColor" fill="none" stroke-width="1.4">
    <line x1="100" y1="60" x2="114" y2="60" marker-end="url(#rt-a)"/>
    <line x1="214" y1="60" x2="228" y2="60" marker-end="url(#rt-a)"/>
    <line x1="334" y1="60" x2="348" y2="60" marker-end="url(#rt-a)"/>
    <line x1="446" y1="60" x2="460" y2="60" marker-end="url(#rt-a)"/>
    <line x1="566" y1="60" x2="580" y2="60" marker-end="url(#rt-a)"/>
  </g>
  <text x="330" y="112" text-anchor="middle" font-size="9" fill="currentColor" font-style="italic" opacity="0.85">your lab today runs this whole chain — and each link has a defence you'll learn this week</text>
</svg>
```

Notice: nothing here requires a Hollywood zero-day. The intrusion you're about to
run uses a **forgotten file**, a **reused password**, and **one careless sudo
line** — and that is exactly how most real breaches actually happen.

---

## 4 · Authorisation Is Everything

This is the most important section in the module. The techniques you learn are
genuinely powerful, and the law treats them seriously.

::: warning | The line you never cross
Running these tools against a system you do **not own** or have **written
authorisation** to test is a criminal offence under Ghana's **Cybersecurity Act
2020 (Act 1038)** — with real penalties. A professional engagement always has:
- **Authorisation** — signed permission from someone who owns the system.
- **Scope** — exactly which IPs/apps are in bounds, and which are off-limits.
- **Rules of engagement** — when you can test, what you must not do (no
  destruction, no real customer data), and who to call if something breaks.
In this course, your entire authorised scope is the lab targets on `10.13.x.x` —
today, exactly `10.13.2.10`. There is no "just testing" exception.
:::

Everything you do should be **documented** as you go — the professional output of
a red-team engagement is a *report* (your `labctl worksheet rt`), not a trophy.

---

## 5 · Your First-Hack Toolkit

Four tools, each of which you'll meet again in depth this week:

```Terminal — the whole chain, in commands
# 1. RECON — what's alive and what's running?
nmap -sV 10.13.2.10

# 2. ENUMERATE the web — find what isn't linked
curl http://10.13.2.10/robots.txt
gobuster dir -u http://10.13.2.10 -w /usr/share/wordlists/dirb/common.txt

# 3. LOOT — read the file the admin forgot to move
curl http://10.13.2.10/backup/notes.txt

# 4. FOOTHOLD — log in with the leaked credential
ssh webadmin@10.13.2.10        # then:  cat user.txt

# 5. PRIVILEGE ESCALATION — abuse the sudo misconfiguration
sudo -l                        # shows a NOPASSWD shell
sudo /bin/ash                  # now root:  cat /root/root.txt
```

- **nmap** (Module 3) — the scanner: which ports are open, what software behind them.
- **gobuster / curl** (Module 4) — find hidden web content nobody linked to.
- **ssh** — log in with the credential you looted.
- **`sudo -l`** — the first thing you check on any foothold: *what can this user do
  as root?* A `NOPASSWD` entry for a shell is a free ride to root.

---

## 6 · The Worked Intrusion — "Operation First Blood"

`labctl start rt` brings up one internal server at **`10.13.2.10`** exposing web
and SSH. Walk the chain:

1. **Recon** — `nmap -sV 10.13.2.10`: two services (web :80, SSH :22); note the web
   **server software**.
2. **Enumerate** — `robots.txt` hints a hidden folder; `gobuster` confirms the
   **`/backup/`** directory the admin forgot to move out of the web root.
3. **Loot** — `/backup/notes.txt` is an ops handover note leaking the **SSH
   username and password**.
4. **Foothold** — `ssh webadmin@10.13.2.10` with that password; `cat user.txt` for
   the **user flag**.
5. **Privilege escalation** — `sudo -l` reveals webadmin may run a root shell with
   no password; `sudo /bin/ash` makes you **root**; `cat /root/root.txt` for the
   **root flag**.
6. **Report** — map the login to ATT&CK and name the controls (next section), then
   capture it in the First-Hack Report.

::: warning | Your flags and password are unique
The SSH password and both flags are **randomised per student**, so report *your*
values — `labctl verify rt` grades against your own answer key, and a classmate's
flag will fail.
:::

---

## 7 · Flip It — How Each Step Is Stopped

Now the point of the whole exercise. Re-run the chain as a defender and watch it
fall apart at *every* link — each fix is a module this week:

| Attacker step | What enabled it | The control that breaks it (module) |
|---------------|-----------------|-------------------------------------|
| Recon found the open services | Unknown/over-exposed surface | Scan your own estate; least exposure, host firewall (M3) |
| `/backup/` was reachable | A file left in the web root | Secure config, don't expose backups (M4) |
| The note leaked a credential | Secrets stored in the clear | Secrets management; never write passwords down (M4/M5) |
| The SSH login worked | A password alone was enough | **Phishing-resistant MFA**; key-based SSH (M3) |
| `sudo /bin/ash` gave root | A `NOPASSWD` sudo misconfig | **Least privilege**; audited, minimal sudo (M3) |
| You read the flags / could exfiltrate | Flat trust once inside | Segmentation, monitoring, DLP (M3/M4/M6) |

::: key | The lesson of First Blood
No single mistake here was catastrophic on its own — a forgotten file, a reused
password, one sudo line. The **catastrophe was the chain.** Defence is the
discipline of breaking *any one link*, because the attacker needs them all and you
only need to hold one. That is what the rest of this week teaches you to do.
:::

---

## Key takeaways

::: key | Carry these out of the Red Team Primer
- **You defend what you've attacked.** Walking an intrusion makes every later
  control concrete.
- **Red attacks, blue defends, purple is the loop** — and the only thing that makes
  hacking *ethical* is **authorisation + scope + rules of engagement** (Act 1038).
- Attacks are **chains**: recon → enumerate → access → foothold → privilege
  escalation → objectives. Hollywood zero-days are rare; forgotten files, reused
  passwords and sudo misconfigs are the norm.
- On any foothold, **`sudo -l` first** — a `NOPASSWD` shell is instant root.
- The defender wins by **breaking one link**: least exposure, no leaked secrets,
  MFA, least-privilege sudo, segmentation and monitoring — the whole week ahead.
:::

## Check yourself

1. **What is the only real difference between a penetration tester and a
   criminal using the same tools?**
   → **Authorisation** — written permission, a defined scope and rules of
   engagement. Without it, it's a crime under Act 1038.

2. **You've just landed a shell as an ordinary user. What's the first command you
   run, and why?**
   → `sudo -l` — to see what that user may run as root. A `NOPASSWD` entry for a
   shell (or many other binaries) is an instant path to root.

3. **In the lab, the SSH login simply worked with the looted password. Name the
   single control that would have stopped that step.**
   → Phishing-resistant **MFA** (or key-based SSH with passwords disabled) — a
   stolen password alone would no longer be enough.

4. **Why do we say the breach was "the chain, not the mistake"?**
   → Each step was individually minor; it was the *combination* (exposed file →
   leaked creds → password login → sudo misconfig) that led to full compromise.
   Breaking any one link stops the whole attack.

## Glossary

- **Red / blue / purple team** — attack / defend / the loop that improves defence.
- **Penetration testing / ethical hacking** — authorised, scoped attacks to find holes first.
- **Authorisation / scope / rules of engagement** — permission / what's in bounds / how you may test.
- **Recon / enumeration** — finding the target / mapping what it exposes.
- **Foothold** — your first shell/access inside the target.
- **Privilege escalation** — going from a normal user to root/admin.
- **Flag** — a token (e.g. `FLAG{…}`) proving you reached a point, as in a CTF.
- **`sudo -l`** — lists what the current user may run via sudo; a key priv-esc check.
- **Cyber Kill Chain** — the staged model of an intrusion (Module 1).
