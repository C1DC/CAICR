# CAIC CyberLab — Student Handout

**Professional Certificate in Cybersecurity, AI & Digital Resilience**
KAIPTC · Cyber1Defense Communication Ltd

Keep this one page beside you all week.

---

## Start the day

```
./start.sh
```
Opens the CyberLab app in your browser. Or use the terminal directly with
`labctl` (below). Set your name once: `./labctl whoami Your Name`.

## The rhythm for every module

1. **Learn** — read the lesson: app **Course** tab, or `./labctl learn m3`.
2. **Do** — run the lab: `./labctl start m3`, work the tasks, then
   `./labctl verify m3` to be graded.
3. **Produce** — get the deliverable template: `./labctl worksheet m3`
   (your copies go to `~/caic-coursework/`).

Press **Ctrl‑K** in the app to jump to any module, lab, tool or command.

## The commands you'll use

| Command | What it does |
|---------|--------------|
| `./labctl learn` | List all modules; `learn m3` reads one lesson |
| `./labctl start m3` | Bring up a lab's isolated targets |
| `./labctl info m3` | The mission briefing + target IPs |
| `./labctl verify m3` | Submit your findings, get graded |
| `./labctl reset m3` | Rebuild a lab clean |
| `./labctl stop m3` | Shut a lab down |
| `./labctl worksheet m3` | Get the deliverable template |
| `./labctl progress` | How far you've come |
| `./labctl doctor` | Check your machine is ready |

New here? Start with **`./labctl learn m0`** — the orientation + Linux
command-line primer.

## The five days

| Day | Modules |
|-----|---------|
| 1 | m0 Orientation · **m1** Threat Intel (lab) · m2 Risk register |
| 2 | **m3** Network (lab) · **m4** Vuln & SOC (lab) |
| 3 | **m5** BEC (lab) · **m6** Forensics (lab) |
| 4 | **m7** AI Security (lab) · m8 Privacy & Compliance |
| 5 | m9 Governance · **m10** Capstone (lab) |

## ⚠ The one rule you never break

Every lab tells you its target IPs — they look like **`10.13.x.x`** and live only
on your own machine. **Scan or attack ONLY those IPs.** Using these tools against
any other network, website or phone is a criminal offence under the Ghana
Cybersecurity Act 2020 (Act 1038) and will remove you from the programme.

## Stuck?

- `./labctl doctor` first.
- Targets won't start → tell your facilitator (Docker may need `sudo` or the
  `docker` group).
- Lost your place → the app Dashboard shows "Jump back in".
- Start a lab over → `./labctl reset m3`.

Your progress is saved automatically on this machine. Close and come back any
time.
