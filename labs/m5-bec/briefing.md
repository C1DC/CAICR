**A "supplier" wants the bank account changed and paid today — prove it's fraud from the evidence.**  ·  Day 3 · ~2 h · 13 graded tasks · file-based (nothing to launch)

::: note | What this lab is
Finance officer Ama Boateng received what looks like a reply from your supplier
*Zenith Supplies*, asking her to change the bank account for an overdue invoice
and pay **today**. You have the **genuine earlier email**, the **suspicious
reply**, and its **attachment**. You prove whether it's fraud from the message's
own headers and the attachment's metadata, expose the attacker, build the
timeline, and design the control that stops it. You practise email header
forensics and `exiftool`.
:::

## What's running

This is a **file-based lab — there are no targets to launch.** The evidence is
prepared for you in the lab's `assets/` (personalised to you):
`genuine-quote.eml`, `invoice-change-request.eml`, `remittance-advice.pdf`.

## How to use this lab

**In the GUI (this page):**
1. Click **Start** once — it personalises your evidence (the status will show
   **file-based**; there are no containers).
2. In the **Terminal** tab, work the evidence with `grep`, `exiftool`, `pdfinfo`.
3. Enter findings in the **Verify** panel → **Submit & grade**.

**Prefer the terminal?** `labctl start m5` → investigate → `labctl verify m5`.

::: warning | The guards — read before you start
- This is a **documents** lab — no scanning, no network targets. Just read the
  evidence.
- The source IP, look-alike domain, fraudulent account, PDF author and timezone
  are **randomised to you** — report *your* values.
- Never "reply to verify" a bank-detail change — the attacker set the `Reply-To`.
  The lesson of this lab is a *process* control, not a clever tool.
:::

## The mission — step by step

### Part 1 — Compare the two emails

```Terminal
grep -iE '^(From|Return-Path|Reply-To|Received|Authentication|Date|Subject)' assets/genuine-quote.eml
grep -iE '^(From|Return-Path|Reply-To|Received|Authentication|Date|Subject)' assets/invoice-change-request.eml
```

Contrast them: did **SPF pass** on the genuine email and **fail** on the reply?
The `From:` display is identical, but the **Reply-To / Return-Path** domain is a
**look-alike** — spot it. The reply reuses the real **PO number** (thread
hijacking). Note the fraudulent **account number** in the body.

### Part 2 — Trace the infrastructure

```Terminal
# the connecting IP from the spoof's earliest Received header, then:
whois <that-ip>            # ISP / country (offline: note what a live lookup shows)
```

### Part 3 — Forensics on the attachment (exiftool)

```Terminal
exiftool assets/remittance-advice.pdf
pdfinfo  assets/remittance-advice.pdf
```

Find the **Author** handle, the **Create Date** and its **UTC offset** (does a
Ghanaian supplier author in `+07:00`?), and compare the create date to the email
date — the file was authored **days before** it was sent, which proves
**premeditation**.

### Part 4 — Timeline & conclusion

Assemble the timeline (attachment authored → look-alike domain used → spoof sent →
payment requested), map it to **MITRE ATT&CK**, and specify the **dual-control +
out-of-band callback** payment control that defeats BEC.

## What you'll be graded on

13 checks in the **Verify** panel across headers, infrastructure and attachment.
Then write the brief:

```Terminal
labctl verify m5
labctl worksheet m5    # fraud investigation brief
```

::: key | Tips
- Use the **genuine email as a baseline** — the SPF *contrast* is courtroom-grade
  proof.
- The attachment's metadata is the confession: author handle, foreign timezone,
  and **created before sent**.
- The fix is a *process*: callback on a **known** number before any bank-detail
  change.
:::
