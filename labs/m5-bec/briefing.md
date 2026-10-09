# M5 — BEC Investigation: Headers, Thread & Attachment

**Scenario.** Finance officer Ama Boateng received what looks like a reply from
your supplier *Zenith Supplies*, asking her to change the bank account for an
overdue invoice and pay **today**. You have the **genuine earlier email**, the
**suspicious reply**, and its **attachment**. Prove whether this is fraud, expose
the attacker, and design the control that stops it.

Evidence in `assets/`: `genuine-quote.eml`, `invoice-change-request.eml`,
`remittance-advice.pdf`.

---

## Part 1 — Compare the two emails

```
$ grep -iE '^(From|Return-Path|Reply-To|Received|Authentication|Date|Subject)' \
      assets/genuine-quote.eml
$ grep -iE '^(From|Return-Path|Reply-To|Received|Authentication|Date|Subject)' \
      assets/invoice-change-request.eml
```

Contrast them:
- Did **SPF pass** on the genuine email? Did it **fail** on the reply?
- The `From:` display is identical, but the **Reply-To / Return-Path** domain
  differs — spot the look-alike.
- The reply reuses the real **PO number** and subject to look like a thread reply
  (thread hijacking). Note the fraudulent **account number** in the body.

## Part 2 — Trace the infrastructure

```
$ # the connecting IP from the spoof's earliest Received header
$ whois 45.137.112.63        # (offline: note what a live lookup would reveal)
$ dig TXT zenith-supplies.com    # (offline here; in the field, check SPF/age)
```

## Part 3 — Forensics on the attachment (exiftool)

The attachment is where attackers get careless — document metadata records who
authored it, with what tool, and *when*:

```
$ exiftool assets/remittance-advice.pdf
$ pdfinfo  assets/remittance-advice.pdf
```

Find the **Author** name, the **Create Date** and its **UTC offset** (does a
"Ghanaian supplier" author documents in a `+07:00` timezone?), and compare the
creation date to the email date — the attachment was authored **days before**
the email, which proves premeditation.

## Part 4 — Timeline & conclusion

Assemble the evidence timeline (attachment authored → look-alike domain used →
spoof sent → payment requested), map it to **MITRE ATT&CK**, and specify the
**dual-control + out-of-band callback** payment control that defeats BEC.

---

## Grade yourself, then write the brief

```
$ labctl verify m5
$ labctl worksheet m5
```
