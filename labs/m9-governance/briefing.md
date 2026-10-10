**Brief a pension trust's board: set recovery priorities and name the governance gaps.**  ·  Day 5 · ~1.5 h · 16 graded tasks · file-based (nothing to launch)

::: note | What this lab is
You are briefing the board of **Volta Pension Trust** — a fund that pays monthly
benefits to pensioners who depend on the money. The board has called a governance
and business-continuity review. Your job is the analytical core of a CISO's board
brief: read the **BIA** to decide what gets recovered first, find the **RTO/RPO
gap** on the service pensioners rely on, and **catch the governance failures** — no
board owner, a muddled policy hierarchy, vanity metrics, untested backups, no
crisis command. Then you write the executive memo and the recovery-priority table.
:::

## What's running

This is a **file-based lab — there are no systems to launch.** The case pack is in
the lab's `assets/`, **personalised to you**: `casefile.md` — the institution, the
BIA table, the current board pack (to critique) and the regulatory frame.

## How to use this lab

**In the GUI (this page):**
1. Click **Start** once — it personalises your case pack (status: **file-based**).
2. Open the **Terminal** tab and read it: `cat casefile.md` (in the lab's
   `assets/`), or open it in any editor.
3. Answer the questions in the **Verify** panel → **Submit & grade**.
4. Then build the deliverables with `labctl worksheet m9`.

**Prefer the terminal?** `labctl start m9` → read the pack → `labctl verify m9`.

::: warning | The guards — read before you start
- This is a **governance/decisions** exercise — nothing to scan or attack.
- Your figures (members, RTOs, impact) are **randomised to you** — answer *your*
  values.
- Think like the board: **evidence, not reassurance.** "Trust me, we're fine" is
  not governance.
:::

## The mission — step by step

1. **Recovery priorities.** From the BIA, which service is recovered **first**, and
   does its **current RTO** meet the **board mandate**? What is the daily **impact**?
2. **Governance.** Is setting risk appetite **governance or management**? Which CSF
   2.0 function is **weakest**? Is a step-by-step "Password Policy" actually a
   **procedure**?
3. **Metrics.** Is "4.2M attacks blocked" a useful board metric — and what should
   they see **instead**?
4. **Continuity.** What were the backups never subjected to? (the control that
   proves recovery works)
5. **Crisis & assurance.** Who provides the **third line** of assurance? Who owns
   decisions in a crisis, and what **log** do they keep? Who do you **report** to
   under Act 1038?

## What you'll be graded on

The **Verify** panel has 16 checks across the steps above. Then produce the two
board deliverables:

```Terminal
labctl verify m9
labctl worksheet m9    # executive cyber-risk memo + recovery-priority table
```

::: key | Tips
- **Governance sets direction and demands assurance; management executes** — don't
  confuse the two.
- A backup you have **never restored** is a hope, not a control — the restore test
  belongs in every board pack.
- Report **decision-useful** metrics (MTTD/MTTR, patch %, MFA %, restore test),
  never vanity numbers.
:::
