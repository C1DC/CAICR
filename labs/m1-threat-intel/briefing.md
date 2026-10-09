# M1 — Passive Reconnaissance Practicum

**Scenario.** Before attackers phish an organisation they profile it from the
outside — no packets to the target's own servers, just public DNS and OSINT. You
will do exactly that against **lab-corp.com.gh** and judge how exposed it is to
email spoofing, then write it up as a threat brief.

A lab DNS server (`10.13.1.10`) answers authoritatively for the zone. A WHOIS
export and an OSINT report are in `assets/`.

> This is *passive* recon against a lab-only domain. The same `dig`/`whois`
> queries run against a real domain are how an attacker plans a campaign — and
> how a defender audits their own exposure. Only ever query the lab targets.

---

## Part 1 — Sweep the DNS

```
$ dig @10.13.1.10 lab-corp.com.gh        A +short      # IPv4
$ dig @10.13.1.10 lab-corp.com.gh        AAAA +short   # IPv6
$ dig @10.13.1.10 lab-corp.com.gh        MX +short     # mail servers
$ dig @10.13.1.10 mail.lab-corp.com.gh   A +short      # the mail server's IP
$ dig @10.13.1.10 lab-corp.com.gh        SOA +short    # authoritative NS + admin
$ dig @10.13.1.10 lab-corp.com.gh        TXT +short    # SPF lives here
$ dig @10.13.1.10 default._domainkey.lab-corp.com.gh TXT   # DKIM key
$ dig @10.13.1.10 _dmarc.lab-corp.com.gh TXT           # DMARC policy?
$ dig @10.13.1.10 lab-corp.com.gh        CAA           # cert-issuance control?
```

Record what each returns. Then read the **email-authentication posture**:
- the **SPF** qualifier (`-all` hard vs `~all` soft);
- whether **DKIM** is published, and at which selector;
- whether **DMARC** exists at all (an `NXDOMAIN` means *no policy*);
- whether **CAA** exists (an empty answer means *any* CA may issue certificates).

## Part 1b — Fingerprint the server & attempt a zone transfer

The DNS server is real **BIND9**. Fingerprint it and test for the single most
damaging DNS misconfiguration — an open **zone transfer (AXFR)**:

```
$ nmap -sV -p53 10.13.1.10                     # what server software is this?
$ dig AXFR @10.13.1.10 lab-corp.com.gh         # dump the ENTIRE zone if allowed
$ dnsrecon -n 10.13.1.10 -d lab-corp.com.gh -a # dnsrecon's AXFR + enumeration
```

If the transfer succeeds, you get **every record at once** — including internal
hosts that were never meant to be public. Find the internal admin host and its
private IP. This is exactly how real breaches begin: a forgotten
`allow-transfer { any; }` hands an attacker the whole network map.

## Part 2 — Investigate the registration (WHOIS)

```
$ cat assets/whois-lab-corp.txt
```
Note the **creation date** (how old is the domain?), the name servers, and the
**look-alike domain** the export flags — registered days ago, on free email and
free DNS. That pattern is classic BEC pre-staging.

## Part 3 — Read the OSINT footprint

```
$ cat assets/osint-report.txt
```
How many employee emails are exposed? Which subdomains (vpn, dev, mail) widen the
attack surface?

## Part 4 — Judge the exposure & map to ATT&CK

- SPF is `~all`, DKIM is present, but **no DMARC** → explain in one line why the
  domain is still spoofable (hint: policy + alignment).
- Map your reconnaissance to a **MITRE ATT&CK** Reconnaissance technique (TA0043).

---

## Grade yourself, then write the brief

```
$ labctl verify m1
$ labctl worksheet m1     # the threat-brief template
```
