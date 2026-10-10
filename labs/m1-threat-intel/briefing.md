**Passive reconnaissance against a target domain — the way an attacker profiles you before they phish.**  ·  Day 1 · ~90 min · 19 graded tasks

::: note | What this lab is
Before criminals phish an organisation they profile it from the *outside* — no
packets to its own servers, just public DNS and open-source intelligence. In this
lab you do exactly that against a fictional company, **lab-corp.com.gh**, judge how
exposed it is to email spoofing, and write it up as a threat brief. You practise
`dig`, `whois` and OSINT reading, and you learn to read a domain's SPF/DKIM/DMARC
posture the way a defender audits their own.
:::

## What's running

- **One live target — `labdns` at `10.13.1.10`:** a real BIND9 server that is
  authoritative for `lab-corp.com.gh`. It is launched *for* you; you query it, you
  don't configure it.
- **Evidence files (in the lab's `assets/`, personalised to you):** a WHOIS export
  (`whois-lab-corp.txt`) and an OSINT report (`osint-report.txt`).

## How to use this lab

**In the GUI (this page):**
1. Click **Start**. The DNS target comes up; wait until the status shows
   **● running** and the target IP `10.13.1.10` appears in the table above.
2. Open the **Terminal** tab (a real Kali shell on this machine) and work the
   mission below — run `dig`/`whois`/`theHarvester` against the target.
3. Type each finding into the **Verify** panel and click **Submit & grade**.
4. Use **Reset** for a clean DNS server, **Stop** when you're done.

**Prefer the terminal?** `labctl start m1` → investigate → `labctl verify m1`.

::: warning | The guards — read before you start
- Query **only** `10.13.1.10` and the `lab-corp.com.gh` zone it serves. Pointing
  `dig`/`whois`/`theHarvester` at a real domain you don't own is reconnaissance for
  an attack and an offence under the **Cybersecurity Act 2020 (Act 1038)**.
- This is **passive** recon — you read public records, you don't exploit anything.
- Your WHOIS/OSINT evidence is **randomised to you**; report *your* values —
  a classmate's answers will not match.
:::

## The mission — step by step

### Part 1 — Sweep the DNS

```Terminal — query every record type
dig @10.13.1.10 lab-corp.com.gh        A +short      # IPv4
dig @10.13.1.10 lab-corp.com.gh        MX +short     # mail servers
dig @10.13.1.10 lab-corp.com.gh        SOA +short    # authoritative NS + admin
dig @10.13.1.10 lab-corp.com.gh        TXT +short    # SPF lives here
dig @10.13.1.10 default._domainkey.lab-corp.com.gh TXT   # DKIM key
dig @10.13.1.10 _dmarc.lab-corp.com.gh TXT           # DMARC policy?
dig @10.13.1.10 lab-corp.com.gh        CAA           # cert-issuance control?
```

Read the **email-authentication posture**: the SPF qualifier (`-all` hard vs
`~all` soft), whether DKIM is published, whether DMARC exists at all (an
`NXDOMAIN` means *no policy*), and whether CAA exists.

### Part 1b — Fingerprint the server & try a zone transfer

```Terminal — the single most damaging DNS misconfiguration
nmap -sV -p53 10.13.1.10                     # what server software is this?
dig AXFR @10.13.1.10 lab-corp.com.gh         # dump the ENTIRE zone if allowed
```

If the transfer succeeds you get **every record at once** — including internal
hosts never meant to be public. Find the hidden admin host and its private IP.

### Part 2 — Investigate the registration (WHOIS)

```Terminal
cat assets/whois-lab-corp.txt
```

Note the **creation date**, the name servers, and the **look-alike domain** the
export flags — registered days ago on free email/DNS. Classic BEC pre-staging.

### Part 3 — Read the OSINT footprint

```Terminal
cat assets/osint-report.txt
```

How many employee emails are exposed? Which subdomains (vpn, dev, mail) widen the
attack surface?

### Part 4 — Judge the exposure & map to ATT&CK

Explain in one line why the domain is still spoofable even with SPF+DKIM (hint:
policy + alignment), and map your recon to a **MITRE ATT&CK** Reconnaissance
technique (TA0043).

## What you'll be graded on

The **Verify** panel has 19 checks drawn from the parts above. Then turn your
findings into the professional deliverable:

```Terminal
labctl verify m1       # grade your findings
labctl worksheet m1    # the threat-brief template to fill in
```

::: key | Tips
- Trust the **SOA**, not `dig +short NS`, for the authoritative name server.
- "No DMARC" is itself the finding — an `NXDOMAIN` on `_dmarc` is why the domain
  can be spoofed despite SPF/DKIM.
- The zone transfer is the money shot: if `AXFR` works, read the whole zone for
  the hidden host.
:::
