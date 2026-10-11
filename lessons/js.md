# Web Attack Arena — Hacking a Real Web Application

**Day 1 · ~60 min · Hands-on against OWASP Juice Shop at `http://10.13.8.10:3000`.**

In the Red Team Primer you broke into a server over SSH. But most institutions
expose far more **web applications** than SSH servers — internet banking portals,
e-government services, fintech dashboards, customer logins. **The web app is the
front door, and it is the single most attacked surface on the internet.** In this
session you attack a real, deliberately-vulnerable web app exactly the way
criminals do, then learn the one-line fix.

Your target is **OWASP Juice Shop** — the Open Worldwide Application Security
Project's flagship training app and the world's most-used insecure web
application. It is a genuine modern stack (Angular front end, Node/Express back
end, a real database) seeded with the **OWASP Top 10** — the industry's canonical
list of the most critical web risks. It is **already running** for you; there is
nothing to "start".

::: outcome | By the end of this session you will be able to
1. Explain why **web applications** are the #1 attack surface, and name the **OWASP Top 10**.
2. Fingerprint a web app's technology stack from the browser and the command line.
3. Perform a **SQL-injection login bypass** — authenticate as admin with no password — and explain *why* it works.
4. Name the **remediation** (parameterised queries) and map the attack to **MITRE ATT&CK (T1190)**.
5. Investigate further challenges on Juice Shop's hidden scoreboard.
:::

## 1 · Why the Web App Is the Front Door

A web application takes input from anyone on the internet and turns it into
actions against your databases, files and other systems. That is enormous power
exposed to total strangers — and if any single input is trusted when it should
not be, an attacker walks straight in. No phishing, no malware; just a crafted
request to a public URL.

The security community tracks the most dangerous classes of web flaw in the
**OWASP Top 10**. The ones you will meet this week:

| OWASP 2021 | What it is | Where you meet it |
|------------|------------|-------------------|
| A01 Broken Access Control | Users reach things they shouldn't | Juice Shop, M4 |
| **A03 Injection (incl. SQL injection)** | Untrusted input becomes code/queries | **This lab** |
| A02 Cryptographic Failures | Sensitive data poorly protected | M5, M6 |
| A05 Security Misconfiguration | Defaults, exposed admin, verbose errors | RT, M4 |
| A07 Identification & Auth Failures | Weak login, no MFA, guessable tokens | RT, M3 |

::: ghana | Why this matters here
Every bank, fintech and government portal in Ghana is a web application exposed to
the world. SQL injection and broken access control have dumped real customer
databases across the region. The Cybersecurity Act, 2020 (Act 1038) makes
protecting these systems a legal duty — and the fixes are mostly cheap code
changes, if your developers know to make them.
:::

## 2 · How SQL Injection Works

When you log in, the app builds a database query from what you typed. A **naive**
app glues your input straight into the query text:

```figure A naive login query — and how one quote hijacks it
  YOU TYPE:  email = me@x.com          password = secret
  APP BUILDS: SELECT * FROM users WHERE email='me@x.com' AND password='secret'
                                              └── your input ──┘
  ───────────────────────────────────────────────────────────────────────────
  ATTACKER TYPES:  email = ' or 1=1--          password = anything
  APP BUILDS: SELECT * FROM users WHERE email='' or 1=1--' AND password='...'
                                           │      │    └── '--' comments out the rest
                                           │      └── 'or 1=1' is ALWAYS true
                                           └── the ' closes the string early
  RESULT: the WHERE is always true → DB returns the FIRST user → you are admin.
~~~svg~~~
<svg viewBox="0 0 520 170" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="11">
  <defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L6,3 L0,6 Z" fill="currentColor"/></marker></defs>
  <g fill="none" stroke="currentColor" stroke-width="1.4">
    <rect x="12"  y="26" width="150" height="40" rx="6"/>
    <rect x="200" y="20" width="150" height="52" rx="6"/>
    <rect x="388" y="26" width="120" height="40" rx="6"/>
    <path d="M162 46 H200" marker-end="url(#a)"/>
    <path d="M350 46 H388" marker-end="url(#a)"/>
    <rect x="200" y="112" width="150" height="40" rx="6" stroke="var(--gold,#ffcf6b)"/>
    <path d="M275 72 V112" marker-end="url(#a)" stroke="var(--gold,#ffcf6b)"/>
  </g>
  <g fill="currentColor" text-anchor="middle">
    <text x="87"  y="42">attacker input</text>
    <text x="87"  y="58" font-family="monospace">' or 1=1--</text>
    <text x="275" y="40">query built by</text>
    <text x="275" y="56">string concatenation</text>
    <text x="448" y="50">database</text>
    <text x="275" y="130" fill="var(--gold,#ffcf6b)">WHERE always true</text>
    <text x="275" y="146" fill="var(--gold,#ffcf6b)">→ returns admin row</text>
  </g>
</svg>
```

The root cause: **the app could not tell your *data* from its *code*.** Fix that
distinction and the entire class of attack disappears — see §4.

## 3 · Hands-On: Break In (follow along)

Your target is live at `http://10.13.8.10:3000`. Attack **only** that address.

1. **Get on the app.** Open `http://10.13.8.10:3000` in the browser. Note what the
   app is called (top-left).
2. **Fingerprint the version.** This app hides its framework (no `X-Powered-By`
   header — good practice) but leaks its exact version through an admin endpoint:
   ```bash
   curl -s http://10.13.8.10:3000/rest/admin/application-version
   ```
   Version disclosure lets an attacker search for version-specific exploits.
3. **Find the hidden scoreboard.** It is not in the menu. Browse to
   `http://10.13.8.10:3000/#/score-board`, or open DevTools (F12) → Sources and
   search the JS bundle for `score-board`. This board tracks every challenge.
4. **SQL-injection login bypass.** Open **Login**. In the **Email** field type:
   ```
   ' or 1=1--
   ```
   Put anything in **Password**, submit. You are logged in as the first user —
   the **administrator**. Note the admin email in the account menu.
5. **Prove impact.** You now hold an admin session with no credentials. In a real
   portal that is full account takeover, or — with other injection payloads — the
   whole customer table.

::: case | This is not a toy
The "`' or 1=1--`" login bypass is one of the oldest tricks in security, and it
*still* breaches production systems in 2026 because developers keep building
queries by string concatenation. Automated tools (e.g. **sqlmap**) find and
exploit these at scale across thousands of sites a day.
:::

## 4 · Flip to Defender — The Fix

One idea fixes injection for good: **never let user input become code.** Use
**parameterised queries** (a.k.a. prepared statements), where the query structure
is fixed and the input is sent separately as data the database can never execute:

```Secure vs insecure (pseudocode)
  // INSECURE — input glued into the query text:
  db.query("SELECT * FROM users WHERE email='" + email + "'")

  // SECURE — parameterised; '?' is data, never code:
  db.query("SELECT * FROM users WHERE email = ?", [email])
```

Layered defences that back this up:

- **Input validation** — reject obviously malformed input early.
- **Least privilege on the DB account** — the app's DB user cannot drop tables.
- **A Web Application Firewall (WAF)** — catches common payloads (a safety net, not a fix).
- **Error handling** — never show raw database errors to the user; they leak structure.

Map it for your report: this is **A03 Injection** (OWASP) and **MITRE ATT&CK
T1190 — Exploit Public-Facing Application**.

## Key takeaways

- The **web application is the #1 attack surface** — it exposes powerful actions to strangers.
- **SQL injection** happens when input is concatenated into a query; `' or 1=1--` turns a login into an always-true condition and returns the admin row.
- The permanent fix is **parameterised queries / prepared statements** — separate code from data.
- The attack maps to **OWASP A03 Injection** and **MITRE ATT&CK T1190**; `sqlmap` automates it at scale.
- Juice Shop's hidden **scoreboard** holds 100+ challenges you can keep hunting.

## Check yourself

1. In `' or 1=1--`, what does each of the three parts (`'`, `or 1=1`, `--`) do?
2. Why does a parameterised query stop the attack even if the input still contains `' or 1=1--`?
3. Which OWASP Top 10 category and which MITRE ATT&CK technique does this attack map to?
4. Name two defence-in-depth controls that reduce injection risk *besides* fixing the code.

## Glossary

- **OWASP** — Open Worldwide Application Security Project; publishes the Top 10 web risks.
- **OWASP Top 10** — the canonical list of the most critical web application security risks.
- **SQL injection (SQLi)** — inserting SQL through an input so it alters the database query.
- **Login/authentication bypass** — logging in without valid credentials by abusing a flaw.
- **Parameterised query / prepared statement** — a query whose inputs are bound as data, never executed as code.
- **WAF** — Web Application Firewall; filters malicious HTTP requests.
- **Scoreboard** — Juice Shop's (hidden) tracker of solved challenges.
- **T1190** — MITRE ATT&CK technique: Exploit Public-Facing Application.
