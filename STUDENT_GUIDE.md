# CAIC CyberLab — Student Quick Start

Welcome. This is your hands-on lab. Everything runs **on your own Kali machine**,
offline, against safe practice targets. You use the real tools (Nmap, Wireshark,
Nikto, Hydra, John, Autopsy, CyberChef, dig) — the lab just sets up the targets
and checks your answers.

---

## Start here: one command

Open a terminal in the lab folder and run:

```
./start.sh
```

This opens the CyberLab home page in your browser (lessons + courseware) and
gets the labs ready. Leave it running; press Ctrl-C when you're done.

## The command you drive the labs with: `labctl`

Everything hands-on runs through `labctl`. In the lab folder:

```
./labctl list
```

You'll see every lab, whether its targets are running, and your progress.

### Learn, then do

Every module has a full teaching lesson you read in the terminal — plain-language
explanation, a real Ghana example, common mistakes, and a self-check quiz:

```
./labctl learn                  # the course map — all 10 modules
./labctl learn m3               # read module 3's full lesson
```

Read the lesson first, then launch the matching lab and do it for real.

**Brand new? Start with the orientation** — it explains how the course works,
the rules of engagement, and gives you a complete Linux command-line primer:

```
./labctl learn m0
```

### Produce the deliverable

Each module has a professional template — a risk register, a chain-of-custody
form, a board memo, an incident dossier. Get your own copy to fill in:

```
./labctl worksheet          # which modules have templates
./labctl worksheet m2       # copy module 2's templates into your work folder
```

Your copies go to `~/caic-coursework/` and are never overwritten, so your edits
are safe. Fill in the `[...]` placeholders in any editor.

### A lab, start to finish

```
./labctl whoami Your Name       # once — puts your name on your progress
./labctl learn m3               # read the lesson for the module
./labctl info m3                # read the mission + see the target IPs
./labctl start m3               # bring the targets up (wait for "ready")
#   ... now do the work in your own terminal: nmap, wireshark, etc. ...
./labctl verify m3              # type in what you found — it grades you
./labctl reset m3               # start the targets over, clean
./labctl stop m3                # shut the lab down when you're done
```

`./labctl progress` shows how far through the course you are.

### Quizzes, the exam and your certificate

Hands-on labs are half your grade. The rest comes from the module quizzes and
the final exam:

```
./labctl diagnostic             # optional baseline self-check (not graded)
./labctl quiz m3                # a short knowledge check for a module
./labctl exam                   # the final exam (counts for 25%)
./labctl grade                  # your composite grade: labs 50 / quizzes 25 / exam 25
./labctl certificate            # generate your certificate once you pass (70%)
```

Quiz and exam options are reshuffled for every student, so answers can't be
shared. When you reach **70% overall**, `./labctl certificate` writes a branded
certificate (open it and Print → Save as PDF). You can do all of this in the web
app too — open the **Assessment** page with `./labctl serve`.

---

## The golden safety rule

Every lab tells you its target IPs (they look like `10.13.x.x`). **Only ever
scan or attack those IPs.** They live inside an isolated network on your own
machine and cannot reach the real internet or your college/work network. Using
these tools against anything else is against the law (Ghana Cybersecurity Act
2020, Act 1038) and will remove you from the programme.

---

## The labs

| Lab | What you practise |
|-----|-------------------|
| `m1` | OSINT & DNS recon — find a domain's weak email security (`dig`) |
| `m3` | Network scanning + traffic analysis (`nmap`, Wireshark) |
| `m4` | Vulnerability scanning + password attacks + SIEM triage (`nikto`, `hydra`, `john`) |
| `m5` | Business Email Compromise — trace a spoofed email's headers |
| `m6` | Digital forensics — disk image, deleted-file recovery, decoding (`autopsy`, `fls`, CyberChef) |
| `m7` | AI security — break a vulnerable AI assistant with prompt injection |
| `m10` | Capstone — a full multi-stage attack, all tools, one crisis |

---

## If something doesn't work

```
./labctl doctor        # checks Docker and your tools are ready
```

- **"Docker is not ready"** — ask your facilitator; you may need to run
  `sudo labctl ...` or be added to the `docker` group.
- **Targets won't start / "subnet collides"** — tell your facilitator; another
  Docker network is using that address range.
- **Start over completely** — `./labctl reset-progress` wipes your scores.

Your progress is saved automatically on your own machine. You can close the
terminal and come back any time.
