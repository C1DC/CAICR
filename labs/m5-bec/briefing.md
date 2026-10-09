# M5 — Business Email Compromise: Header Forensics

**Scenario.** Ama Boateng, a finance officer, received an email that appears to
be from your supplier *Zenith Supplies Ltd*, asking her to change the bank
account for an overdue invoice and pay it **today**. Something feels off. Before
anyone moves money, prove whether this email is genuine.

The raw message is in `assets/invoice-change-request.eml`.

> The `From:` display can say anything. The truth is in the headers — the
> delivery path, the envelope sender, and the authentication results.

---

## Read the headers

```
$ cd labs/m5-bec/assets

$ cat invoice-change-request.eml | less          # read the whole thing

$ grep -iE '^(From|Return-Path|Reply-To|Received|Authentication|Received-SPF):' \
      invoice-change-request.eml
```

Work through these questions (you'll submit them in `labctl verify m5`):

1. **Envelope sender** — which header shows where bounces really go, regardless
   of the friendly `From:` name?
2. **Source IP** — in the `Received:` chain, the *earliest* hop records the IP
   that actually connected. What is it?
3. **SPF** — did the sending IP pass or fail SPF for the supplier's domain?
4. **Look-alike domain** — the `Reply-To` / `Return-Path` use a domain that is
   *almost* the supplier's. Spot the difference.
5. **Real domain** — what genuine domain is being impersonated in `From:`?
6. **The ask** — what new account number is the attacker trying to redirect
   payment to?

### In a live SOC (not needed to pass — offline here)

You would confirm the domains with:
```
$ dig TXT zenithsupplies.com.gh        # is there an SPF record? a DMARC one?
$ dig TXT _dmarc.zenithsupplies.com.gh
$ whois zenith-supplies.com            # when was the look-alike registered?
```
A look-alike domain registered days before the email is a strong fraud signal.

---

## Then think like a defender

- Which single **payment control** would have caught this before the money left?
- Map the initial access to a **MITRE ATT&CK** technique ID.

---

## Grade yourself

```
$ labctl verify m5
```
