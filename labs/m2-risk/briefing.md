**Turn a rural bank's messy reality into a prioritised, board-ready risk picture.**  ·  Day 1 · ~2 h · 17 graded tasks · file-based (nothing to launch)

::: note | What this lab is
You are the incoming risk officer at **Sankofa Rural Bank**. You've been handed a
case pack — the asset inventory, a year of incidents and near-misses, an external
pen-test, a FAIR loss estimate, and a half-built draft risk register — and the
board meets next week. Your job is the *analytical core* of risk management: find
the crown jewels, score the exposure against real evidence, **catch the
governance failures in the draft register**, read the recovery gap, and map
controls to NIST CSF 2.0. Then you write it up as a register and a CSF profile.
This is how risk is actually done — no abstractions.
:::

## What's running

This is a **file-based lab — there are no systems to launch.** The case pack is
prepared for you in the lab's `assets/` (and **personalised to you** — your
numbers differ from your neighbour's):

- `casefile.md` — the institution profile, asset inventory, incidents, pen-test,
  FAIR estimate and BIA.
- `draft-risk-register.md` — a junior colleague's draft, with planted problems to
  catch.

## How to use this lab

**In the GUI (this page):**
1. Click **Start** once — it personalises your case pack (status: **file-based**).
2. Open the **Terminal** tab and read the pack:
   `cat casefile.md` and `cat draft-risk-register.md` (they're in the lab's
   `assets/`), or open them in any editor.
3. Answer the questions in the **Verify** panel → **Submit & grade**.
4. Then build the deliverables with `labctl worksheet m2`.

**Prefer the terminal?** `labctl start m2` → read the pack → `labctl verify m2`.

::: warning | The guards — read before you start
- This is an **analysis** exercise — there are no targets to scan and nothing to
  attack. The skill is judgement, not tooling.
- Your figures (records exposed, CVSS, the mule account, the FAIR exposure, the
  RTO) are **randomised to you** — read *your* case pack and answer *your* values.
- Every answer must **trace to evidence** in the pack. "It feels risky" is not an
  assessment; "R2's control doesn't reduce its residual score" is.
:::

## The mission — step by step

### 1. Triage the assets and the exposure
Read the profile and asset inventory: which asset is the **crown jewel**? Read the
pen-test: how many **records** are exposed, what **CVSS** does the VPN finding
carry, and is it **in CISA KEV**? Given it's internet-facing, in KEV and on a path
to a critical asset, what **priority** does it deserve?

### 2. The fraud near-miss
From the incident log, find the **mule account** and the **look-alike domain** the
BEC email used, and name the one payment **control** that defeats this fraud class.

### 3. Quantified exposure (FAIR)
Read the **annual loss exposure (ALE)** the FAIR analysis gives for the fraud risk.
This is how you turn "that feels bad" into a number a board can weigh against a
spend.

### 4. Recovery capability (BIA)
Read the **current RTO** for core banking and decide whether it meets the board's
**4-hour** mandate.

### 5. Critique the draft register
Find the three governance failures: the risk **accepted with no owner and no
review date** (negligent acceptance), the risk with a treatment but **no owner**,
and the risk whose **control doesn't reduce its residual score** (and so tops the
residual ranking).

### 6. Map to NIST CSF 2.0
Which **function is weakest** given the board/governance gaps? Which function does
**daily alert review** belong to? And which **treatment** is "buy cyber insurance"?

## What you'll be graded on

The **Verify** panel has 17 checks across the steps above. Then produce the two
board deliverables:

```Terminal
labctl verify m2
labctl worksheet m2    # cyber risk register + NIST CSF 2.0 profile
```

::: key | Tips
- **Context beats CVSS:** internet-facing + in KEV + reaches a crown jewel = do
  it first, even at a lower score.
- A control only counts if the **residual** is genuinely lower than the
  **inherent** — otherwise it's theatre.
- Every **Accept** needs a **named owner and a review date**, or it's negligence.
- Fixing **GOVERN** (board ownership) is what unlocks the budget for everything
  else.
:::
