# Facilitator Dashboard — Seeing the Class & Collecting Real Scores

Every student installs the lab from GitHub and runs it **on their own machine**, so
their progress (labs graded by `labctl verify`, quizzes, exam) is saved locally in
their own `state.json`. There is no shared database by default — which is correct
for an offline, self-contained teaching tool. To see the whole class, the scores
have to be **moved** to you. There are two supported ways; pick whichever fits the
room.

---

## Model A — Collect & view (offline, works anywhere)

No network needed. Students export a score file; you gather them and open a dashboard.

**Each student, at the end (or any checkpoint):**
```bash
labctl submit                 # writes caic-submit-<name>.json in the current folder
```
They hand you that file — USB stick, a shared folder, email, or a Git drop. (The
file is small JSON and carries a **verification code** tied to their machine's seed.)

**You, the facilitator:** put all the collected `*.json` files in one folder, then:
```bash
labctl report ./submissions                      # a scoreboard in the terminal
labctl report ./submissions --html board.html    # ...and a browser dashboard
labctl report ./submissions --html board.html --open   # ...and open it
```

`board.html` is a self-contained page: a ranked roster with each student's
**composite grade, PASS/—, and a tick/score per lab**, plus class stats (students,
passed, average, labs completed). Open it on any machine — no server required.

> You can also just collect each student's `state.json` (it lives in their
> `~/.local/state/caic-cyberlab/` by default) and point `labctl report` at those —
> `submit` simply packages the same data in a tidy, signed form.

---

## Model B — Live classroom dashboard (on the room's LAN)

For real-time scores during the session. **You** run a small server on your laptop;
students submit to it over the classroom network and your dashboard updates live.

**You, the facilitator (once):**
```bash
labctl classroom            # starts the server + prints your invite line
# e.g.  Dashboard:  http://10.0.0.5:7000/
```
Open that URL in your browser — it refreshes every few seconds as submissions
arrive. Submissions are saved in `./classroom-submissions/` (latest wins per
student).

**Each student:**
```bash
labctl submit --to http://10.0.0.5:7000        # use the IP your invite line shows
# or set it once:
export CAIC_CLASSROOM=http://10.0.0.5:7000
labctl submit                                   # now just this, any time
```
They can submit repeatedly as they complete more — the board always shows their
latest. (Students need network line-of-sight to your laptop; the classroom Wi-Fi/
LAN is enough. It is a facilitator-run, LAN-only tool — nothing leaves the room.)

---

## How the grade is computed

The dashboard shows the same **composite grade** students see in `labctl grade`:

| Component | Weight |
|-----------|-------:|
| Hands-on labs (`labctl verify`) | 50% |
| Module quizzes | 25% |
| Final exam | 25% |

**Pass mark 70%.** The facilitator side **re-computes** the grade from the raw
lab/quiz scores in each file — it never trusts a `grade` field a student could edit.

---

## "Are the scores real?" — integrity & its limits

- Each submission carries a **`sig`** derived from the machine's per-student **seed**
  plus the raw scores. The dashboard flags a **⚠** if a file's signature doesn't
  match its contents — i.e. it was edited by hand.
- Lab answers are **randomised per student** (the seed), so a student cannot submit a
  classmate's lab answers and pass — `labctl verify` grades against *their own* key.
- **Honest limit:** this is an open-source teaching tool, so a determined student
  with the source could craft a consistent fake. The signature stops *casual*
  tampering, not a motivated cheat. For **assured** scores:
  1. use **Model B** (live submission as work is completed, with you in the room), and/or
  2. spot-check by watching a student run **`labctl verify <lab>`** on their machine,
     and/or
  3. have the exam/quizzes done in a supervised window.

Treat the dashboard as a **real-time picture of class progress** (its main value),
and confirm final certification scores by observation for anyone it matters for.

---

## Quick reference

| Who | Command | Does |
|-----|---------|------|
| Student | `labctl submit` | write a signed score file to hand in |
| Student | `labctl submit --to <url>` | send scores to the live classroom server |
| Facilitator | `labctl report <dir>` | terminal scoreboard from collected files |
| Facilitator | `labctl report <dir> --html board.html --open` | browser dashboard |
| Facilitator | `labctl classroom` | live LAN dashboard students submit to |
| Anyone | `labctl grade` | the composite grade on this machine |
| Facilitator | `labctl report` + `FACILITATOR_ANSWER_KEY.md` | scores + the answer key |
