# KAIPTC CyberLab Learning Environment
## Version 1.0 — October 2026

The learning environment for the **Professional Certificate in Cybersecurity, AI
& Digital Resilience** — a 5-day intensive course run by KAIPTC (Kofi Annan
International Peacekeeping Training Centre), Accra, Ghana.

## The one thing to run

```
./start.sh
```

This launches the **CAIC CyberLab web application** — a single place where
students do everything: a dashboard, the full course, every deep lesson, the
hands-on **labs launched and graded from the browser**, a **live Kali terminal
in the browser** (a real shell over a PTY/WebSocket bridge), a researched **tool
reference** (what each industry tool is, how to use it, and its commands),
deliverable templates, a command reference, and progress tracking. It opens in
your browser automatically; press Ctrl-C to stop.

The live terminal runs a real shell as your user on this machine and is bound to
localhost — a single-user local workstation by design. Set `CAIC_NO_TERMINAL=1`
to disable it.

Under the hood it's a local web app (`labctl serve`) whose API drives the same
lab engine as the terminal, so the browser and `labctl` stay in sync.

---

It has **complementary parts**, all reachable from the web app or on their own:

| Part | What it is | Start here |
|------|------------|-----------|
| 🖥 **Web application** | The unified GUI — course, lessons, labs, tools, materials, commands. | `./start.sh` |
| 🐉 **Lab engine (`labctl`)** | The CLI that launches isolated labs and grades findings. | `STUDENT_GUIDE.md` |
| 📘 **Lessons reader** | Standalone offline browser reader for the deep lessons. | open `cyberlab-lessons.html` |
| 🎓 **Legacy courseware** | The original single-file quiz app. | open `cyberlab.html` |

For the hands-on labs in the terminal:

- **Students:** `STUDENT_GUIDE.md` — the one-page "how to use `labctl`".
- **Facilitators / developers:** `LAB_ENGINE.md` — architecture, the lab
  catalogue, authoring new labs, and classroom rollout.

Each module has three layers, all driven from `labctl`: **learn** (a deep
lesson), **do** (a hands-on lab, where one exists), and **produce** (a fillable
deliverable template). Read lessons in the terminal with `labctl learn`, or open
`cyberlab-lessons.html` in a browser for the same content with navigation and
search. Regenerate that file after editing lessons with
`python3 scripts/build_lessons_html.py`.

**Start everything with one command:**

```
./start.sh          # checks the backend, serves the frontend, opens your browser
./start.sh m3       # ...and also brings up lab m3's targets
./start.sh --prep   # ...and pre-builds all lab images first (needs internet once)
```

`start.sh` serves the browser pages at `http://127.0.0.1:8899` and prints the
lab commands; press Ctrl-C to stop. Prefer the pieces directly?

```
./labctl doctor     # check the machine is ready
./labctl prep       # build all lab images once (needs internet this one time)
./labctl list       # see the labs
./labctl start m3   # launch a lab
```

---

## Courseware Quick Start (No Installation Needed)

1. Open `cyberlab.html` in any modern web browser (Chrome, Firefox, Edge, Safari)
2. That's it — no server, no install, no internet required after opening

The platform runs entirely in the browser. Progress is saved automatically in the browser's local storage.

---

## What's Inside

| File / folder | Purpose |
|------|---------|
| `cyberlab.html` | The browser courseware (single file) |
| `cyberlab-lessons.html` | Browser reader for the deep lessons + templates (generated) |
| `lessons/` | Deep teaching lessons, one per module (read via `labctl learn`) |
| `worksheets/` | Fillable deliverable templates (`labctl worksheet`) |
| `labctl` + `engine/` | The practical lab engine (Python, stdlib only) |
| `labs/` | The hands-on labs (M1, M3–M7, M10) |
| `STUDENT_GUIDE.md` | One-page student guide to the labs |
| `LAB_ENGINE.md` | Engine architecture + facilitator/author guide |
| `scripts/setup.sh` | One-time machine setup (Docker + image pre-build) |
| `README.md` | This file |
| `ARCHITECTURE.md` | Courseware technical breakdown |
| `CLAUDE_AGENT_HANDOFF.md` | Notes for continuing the courseware |

---

## Platform Features

### For Learners
- **5-Day Guided Course** — All 10 modules with theory, Kali Linux labs, and quizzes
- **Interactive Terminal Labs** — Copy-paste-ready Kali commands with full explanations
- **13 Kali Tool References** — theHarvester, Nmap, Wireshark, Nikto, Hydra, John the Ripper, and more
- **Built-in Quizzes** — Per-module knowledge checks and a full course quiz
- **Progress Dashboard** — Visual completion tracking with day-by-day breakdown
- **Dark/Light Themes** — Matches your system theme; toggle manually

### For Facilitators
- **No Teacher Required** — Platform guides learners step-by-step
- **Offline Capable** — Works with no internet after the initial load (fonts load from Google Fonts on first open; subsequent opens work fully offline if the browser cached them)
- **No Account Needed** — Each learner opens the file; progress saves in their own browser
- **Persistent Progress** — Learners can close and reopen — their progress is remembered

---

## Kali Linux Tools Covered

| Tool | Module | Use Case |
|------|--------|----------|
| theHarvester | Day 1, M1 | OSINT / passive recon |
| dig | Day 1, M1 | DNS enumeration |
| whois | Day 1, M1 | Domain registration lookup |
| Nmap | Day 2, M3 | Network port scanning |
| Wireshark | Day 2, M3 | Packet capture & analysis |
| tcpdump | Day 2, M3 | CLI packet capture |
| Nikto | Day 3, M4 | Web vulnerability scanning |
| Hydra | Day 3, M4 | Password brute-force testing |
| John the Ripper | Day 3, M4 | Hash cracking |
| Wazuh | Day 3, M4 | SIEM alert triage |
| sha256sum | Day 4, M6 | Digital forensics / chain of custody |
| Autopsy | Day 4, M6 | Disk image forensic analysis |
| CyberChef | Day 4, M6 | Encoding/decoding / data analysis |

---

## Course Structure

| Day | Modules | Topics |
|-----|---------|--------|
| Day 1 | M1, M2 | Cybersecurity Fundamentals + AI in Cybersecurity |
| Day 2 | M3 | Network Security |
| Day 3 | M4 | Vulnerability Management & SIEM |
| Day 4 | M5, M6 | BEC / Email Forensics + Digital Forensics |
| Day 5 | M10 | CyberRange Capstone — All tools, 8 live injects |

---

## Facilitator Tips

1. **Pre-load in browsers before class** — Open `cyberlab.html` so fonts cache
2. **Each learner gets their own copy** — Progress is per-browser; share the file on a USB or local network share
3. **CyberRange day (Day 5)** — Platform provides the inject scenarios; learners use live Kali VMs alongside
4. **After training** — Learners keep the file as a permanent reference tool

---

## Technical Notes

- Single HTML file, approximately 120 KB
- No external dependencies at runtime (fonts load from Google Fonts on first open)
- Works in all modern browsers; tested in Chrome 120+, Firefox 121+, Edge 120+
- Progress stored in `localStorage` under key `cyberlab_state`
- To reset a learner's progress: open browser DevTools → Application → Local Storage → delete `cyberlab_state`

