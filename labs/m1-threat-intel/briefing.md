# M1 — Threat Intelligence & OSINT: DNS Recon

**Scenario.** Before attackers phish an organisation, they study it from the
outside — no packets sent to the target's own servers, just public DNS and
open-source intelligence. You will do exactly that against **lab-corp.com.gh**
and decide how exposed it is to email spoofing.

A lab DNS server (`10.13.1.10`) answers authoritatively for the zone. An OSINT
report sits in `assets/osint-report.txt`.

> This is *passive* recon against a lab-only domain. The same `dig` queries run
> against a real domain are how an attacker plans a phishing campaign — and how
> a defender audits their own exposure.

---

## 1. Enumerate DNS

```
$ dig @10.13.1.10 lab-corp.com.gh        A      # where does the domain point?
$ dig @10.13.1.10 lab-corp.com.gh        MX     # who handles its mail?
$ dig @10.13.1.10 mail.lab-corp.com.gh   A +short
$ dig @10.13.1.10 lab-corp.com.gh        TXT    # SPF lives here
$ dig @10.13.1.10 _dmarc.lab-corp.com.gh TXT    # ...and DMARC should live here
```

Answer:
- the **MX host** and the **IP** it resolves to,
- the **SPF qualifier** at the end of the TXT record (`-all` = hard fail,
  `~all` = soft fail — which is weaker?),
- whether a **DMARC** record exists at all.

## 2. Read the OSINT footprint

```
$ cat assets/osint-report.txt
```
How many employee email addresses are exposed? Which role accounts (finance@,
helpdesk@) make the easiest phishing targets?

*(In a live engagement you'd gather this with `theHarvester -d <domain> -b all`
and `whois <domain>` — both need internet, so the report is captured for you
here.)*

## 3. Judge the exposure

- SPF is published but ends in `~all`, and **no DMARC policy exists**. Explain,
  in one line, why that combination lets an attacker spoof this domain and have
  the mail still land in inboxes.
- Which single control closes this gap?
- Map your recon to a **MITRE ATT&CK** reconnaissance technique.

---

## Grade yourself

```
$ labctl verify m1
```
