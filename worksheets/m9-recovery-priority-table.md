# Service Recovery Priority Table (BIA / RTO / RPO) — Module 9 Deliverable

**Institution:** [name]  **Prepared by:** [your name]  **Date:** [YYYY-MM-DD]

> For each critical service, agree how fast it must come back (**RTO**) and how
> much data you can afford to lose (**RPO**), then rank recovery order. These are
> business decisions, agreed with service owners — not IT guesses. See
> `labctl learn m9`.

| Priority | Critical service | Business impact if down | RTO (max downtime) | RPO (max data loss) | Depends on | Owner |
|----------|------------------|-------------------------|--------------------|--------------------|-----------|-------|
| 1 | *Example:* Core payment system | Revenue stops; customer harm; reputational | 1 hour | 5 min | Database, network | CFO / Head of IT |
| 2 | [FILL IN] | | | | | |
| 3 | [FILL IN] | | | | | |
| 4 | [FILL IN] | | | | | |
| 5 | [FILL IN] | | | | | |

## Recovery sequence rationale

[Why this order? Note dependencies — a service can't recover before the things it
relies on. Explain any trade-offs.]

## Backup posture check (per critical service)

| Service | Backup exists? | 3-2-1 (3 copies/2 media/1 offsite)? | Last **restore test** (date/result) |
|---------|----------------|-------------------------------------|-------------------------------------|
| [ ] | [ ] | [ ] | [ ] |

> A backup you have never restored is a hope, not a control. The restore-test
> column is the one leadership should check every quarter.
