# Web Attack Arena — Break Into OWASP Juice Shop

**Day 1 · ~60 min · Your authorised target: `http://10.13.8.10:3000` only.**

This is the **arena**: a real, deliberately-vulnerable web application that is
**already running** the moment the lab opens — no setup, no "host is down". It is
**OWASP Juice Shop**, the world's standard web-pentest training app (a modern
Angular + Node/Express single-page shop). You will attack it exactly the way
criminals hit bank portals, e-gov sites and fintech dashboards every day, then
learn the fix. Full teaching walkthrough: `labctl learn js`.

::: warning | Rules of engagement
Attack **only** `10.13.8.10:3000`. It is isolated on a private range
(`10.13.8.0/24`) on this machine — it is not on the internet and not on your LAN.
Pointing these techniques at any other site is a crime under the Cybersecurity
Act, 2020 (Act 1038).
:::

## How to use this lab (GUI)

1. In the web app, open the **Labs** view → **Web Attack Arena**. The target is
   already **up** (it starts with the lab environment). The status dot is green.
2. Click **Open target** (or browse to `http://10.13.8.10:3000` yourself). The
   shop loads. Dismiss the welcome/cookie banners.
3. Work the mission below. Type each answer into the **check** boxes and press
   **Verify** to grade. You can verify as many times as you like.
4. Stuck on a check? Click its **Hint**.

> Terminal equivalent: `labctl start js` · `labctl info js` · `labctl verify js`.
> (The arena normally auto-starts; `labctl start js` is only needed if you stopped it.)

## The mission

**Recon — get on the app and fingerprint it**

1. Browse to `http://10.13.8.10:3000`. Read the page — what is the app **called**?
2. Fingerprint the version. Well-run apps hide their stack (notice there is **no**
   `X-Powered-By` header here — good hardening). But this one leaks its exact
   version through an admin REST endpoint:
   ```bash
   curl -s http://10.13.8.10:3000/rest/admin/application-version
   ```
   Knowing the exact version lets an attacker look up version-specific exploits.
3. Find the **hidden challenge scoreboard**. It is not in the menu — Juice Shop
   dares you to discover it. Try the route `/#/score-board`, or open your
   browser's DevTools (F12) → Sources and search the JavaScript bundle for
   `score-board`. The scoreboard tracks every challenge you solve.

**Exploit — log in as the administrator with no password (SQL injection)**

4. Go to the **Login** page (top-right account icon → Login).
5. In the **Email** field, type a SQL-injection payload instead of an email:
   ```
   ' or 1=1--
   ```
   Put *anything* in the password field. Submit.
6. You are now logged in — as the **first user in the database, the admin**. Note
   the account's email address (shown in the account menu). *What just happened:*
   the login query was built by gluing your input straight into SQL. Your `'`
   closed the string, `or 1=1` made the WHERE clause always true, and `--`
   commented out the password check. The database returned the first row — admin.

**Flip to defender — name the fix**

7. What **class** of vulnerability was this (OWASP Top 10 name)?
8. What is the one-line **code fix** that makes it impossible?
9. Which **MITRE ATT&CK** technique describes breaking in through a public web app?

::: key | Why this matters for your institution
This exact bug — untrusted input concatenated into a query — is still one of the
top causes of real breaches of banking, government and fintech web apps. One
injection can dump an entire customer database or bypass authentication. The fix
is cheap (parameterised queries); the breach is not.
:::

## Going further (optional, ungraded)

Juice Shop has **100+ challenges** on that scoreboard — XSS, broken access
control, JWT forgery, sensitive-data exposure, and more. Everything you find
feeds the OWASP Top 10 you will meet again in Module 4 (Vulnerability Management)
and Module 7 (AI Security). Hunt a few more and watch the scoreboard light up.

## Deliverable

Write it up with `labctl worksheet js` — a short web-app pentest finding:
the injection, the evidence, the impact, and the remediation.
