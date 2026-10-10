**A hospital's patient data was left public and downloaded — run the first hours as its Data Protection Officer.**  ·  Day 4 · ~2 h · 16 graded tasks · file-based (nothing to launch)

::: note | What this lab is
You are the **Data Protection Officer** at **Akoma Health Network**. A cloud export
of patient records — including diagnoses and Ghana Card numbers — was left public
and downloaded from foreign IPs. The board meets this afternoon. Your job is the
analytical core of breach response and compliance: **classify** the breach, fix
**controller/processor** accountability, **scope** the data and the people
affected, decide the **notification** obligations and timelines, and catch the
**compliance failures** (retention, invalid consent, the missing DPIA, the missing
vendor DPA, the lapsed registration). Then you write it up.
:::

## What's running

This is a **file-based lab — there are no systems to launch.** The case pack is in
the lab's `assets/`, **personalised to you** (your numbers differ from your
neighbour's): `casefile.md` — the institution, the incident, the compliance review
and the regulatory frame.

## How to use this lab

**In the GUI (this page):**
1. Click **Start** once — it personalises your case pack (status: **file-based**).
2. Open the **Terminal** tab and read the pack: `cat casefile.md` (in the lab's
   `assets/`), or open it in any editor.
3. Answer the questions in the **Verify** panel → **Submit & grade**.
4. Then build the deliverables with `labctl worksheet m8`.

**Prefer the terminal?** `labctl start m8` → read the pack → `labctl verify m8`.

::: warning | The guards — read before you start
- This is a **decisions** exercise — there is nothing to scan or attack. The skill
  is judgement under the law.
- Your figures (records exposed, downloads, retention years, potential fine) are
  **randomised to you** — read *your* pack and answer *your* values.
- Breach timelines and thresholds in the real world are confirmed with **counsel**
  and the **current DPC/CSA directives** — this lab teaches the reasoning, not a
  substitute for legal advice.
:::

## The mission — step by step

1. **Classify.** Is this a reportable personal-data breach? Does it involve
   **sensitive** data? How many **records** and how many **downloads**?
2. **Accountability.** Under Act 843, who is accountable — **Akoma (controller)**
   or **CloudMed (processor)**? Outsourcing the task never outsources the duty.
3. **Notify.** The **72-hour** benchmark; the **DPC** (personal data) vs **CSA /
   CERT-GH** (cyber); and whether the **patients** must be told directly.
4. **Compliance failures.** Name the breached **retention** principle, why the
   **consent** is invalid, the missing **DPIA**, and the missing **DPA**.
5. **Contain.** The first action on the exposed bucket, and the **potential
   penalty** the case cites.

## What you'll be graded on

The **Verify** panel has 16 checks across the steps above. Then produce the two
board deliverables:

```Terminal
labctl verify m8
labctl worksheet m8    # data-breach assessment + compliance-gap register
```

::: key | Tips
- **Outsourcing the processing never outsources the accountability** — the
  controller answers to the DPC, not the cloud vendor.
- **Contain first** (remove public access, preserve the logs), *then* scope and
  notify — and brief **counsel before any public statement**.
- "We had consent" fails if the consent wasn't **freely given**; bundled, forced
  consent is no consent.
:::
