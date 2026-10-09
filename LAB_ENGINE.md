# CAIC CyberLab Engine — Developer & Facilitator Guide

The practical half of the KAIPTC programme: a local, offline lab launcher that
runs on each student's Kali box. It brings up **isolated Docker targets** per
module, serves the mission briefing, and **grades the student's findings** — so
students "just launch and use", with real tools against real (but contained)
scenarios.

This is the companion to the passive courseware (`cyberlab.html`). The HTML
teaches; this engine makes them *do*.

---

## 1. Why this design

| Decision | Choice | Reason |
|----------|--------|--------|
| Engine language | **Python 3.11+ (stdlib only)** | Clean CLI, state, grading. No `pip install` on student machines — `tomllib` ships with Python. |
| Provisioning | **Bash hooks** (`verify.sh`, image `entrypoint.sh`) | Bash does what Bash is good at; Python orchestrates. |
| Targets | **Docker containers** on a private subnet | Seconds to launch, trivially reset, and **structurally isolated** — targets are reachable from the Kali host for scanning but have no `ports:` mapping, so nothing reaches the real LAN. |
| Manifests | **TOML** (`lab.toml`) | Comment-friendly, parsed by stdlib `tomllib`, validated on load. |

**Safety is built in, not bolted on.** `manifest.py` refuses to load any lab
whose subnet is not RFC1918 private. The targets can only be reached from the
host; they are never published outward. This is the CyberRange "never touch a
live system" rule enforced by the code, not just a slide.

> The engine never runs an attack tool for the student. It launches targets and
> checks findings. The learning is in running the scan/capture yourself.

---

## 2. Layout

```
CAIC_lab/
├── labctl                  # entrypoint students run (./labctl ...)
├── engine/                 # the engine (stdlib Python)
│   ├── cli.py              #   commands: list/info/start/status/verify/reset/stop/progress/doctor
│   ├── manifest.py         #   load + validate lab.toml  (enforces private subnet)
│   ├── dockerctl.py        #   docker compose wrapper + preflight
│   ├── verify.py           #   grading engine (answer + script checks)
│   ├── state.py            #   per-student progress (~/.local/share/caic-lab)
│   ├── paths.py  ui.py
├── labs/
│   ├── _base/              # shared vulnerable-target image (built once)
│   │   ├── Dockerfile  entrypoint.sh
│   ├── _template/          # copy this to start a new lab
│   └── m3-network/         # ← first complete lab (reference implementation)
│       ├── lab.toml  docker-compose.yml  briefing.md  verify.sh
│       └── assets/         # seeded evidence (PCAPs, disk images, .eml, hashes)
└── LAB_ENGINE.md
```

Per-student **progress** lives in `~/.local/share/caic-lab/state.json`, kept out
of the (possibly root-owned, read-only) install tree.

---

## 3. Student workflow

```
./labctl doctor          # one-time: is Docker + tooling ready?
./labctl list            # see all labs, their status and your progress
./labctl info m3         # read the mission briefing + target list
./labctl start m3        # bring up the isolated targets (builds image 1st time)
#   ... student runs nmap / wireshark / etc. against the listed IPs ...
./labctl verify m3       # submit findings → graded, progress saved
./labctl reset m3        # wipe targets back to a clean state
./labctl stop m3         # shut the lab down
./labctl progress        # overall course completion
```

`sudo` is only needed if the student's user isn't in the `docker` group
(`labctl doctor` tells them which).

---

## 4. Network scheme

Every lab gets its own `/24` under **`10.13.0.0/16`** (10.13 ≈ "lab"), third
octet = module number. This space is almost never used by default Docker, so it
won't collide on a fresh Kali.

| Lab | Subnet | Gateway | Targets |
|-----|--------|---------|---------|
| M3  | `10.13.3.0/24` | `.1` | `.10 .20 .30 .40` |
| M4  | `10.13.4.0/24` | `.1` | (web app, SSH target, …) |
| M5  | `10.13.5.0/24` | … | |
| …   | `10.13.<N>.0/24` | | |

If a subnet ever collides on a machine, `labctl start` surfaces the Docker
error; change the `[network] subnet` in that lab's `lab.toml`.

---

## 5. Authoring a new lab (≈ 20 minutes)

1. `cp -r labs/_template labs/m4-vulnmgmt`
2. Edit `lab.toml` — id, module, day, title, tools, subnet (`10.13.4.0/24`),
   targets, and the `[[check]]` list (this *is* the grading).
3. Edit `docker-compose.yml` — your targets on that subnet. Reuse
   `image: caic-target:1.0` where a generic service fits; add a service-specific
   image only when you need one (e.g. a real vulnerable web app for Nikto).
4. Write `briefing.md` — scenario, the commands to run, the questions.
5. Drop any seeded evidence into `assets/` (PCAP, disk image, `.eml`, hashes).
   Prefer a `generate_*.py` that builds the artifact deterministically.
6. Optional `verify.sh` for automated (`type = "script"`) checks.
7. `./labctl doctor` (confirms the lab parses) → `./labctl start m4`.

### Check types

| `type` | Student enters | Graded by |
|--------|----------------|-----------|
| `numeric` | a number | `== answer` within `tolerance` |
| `string` | text | case/space-insensitive exact match to `answer` |
| `string_any` | text | matches any value in `accept` |
| `script` | *(nothing)* | `verify.sh <check_id>` exit code (0 = pass) |

Use `string_any` generously so sensible variant answers are accepted; always
give a `hint` that names the tool/command.

---

## 6. Build-out roadmap (labs still to author)

Status so far:

| Lab | Module | Kind | Status |
|-----|--------|------|--------|
| **M1** | Threat Intel / OSINT | Docker (dnsmasq lab zone) + OSINT report | ✅ **done** |
| **M3** | Network — Nmap + Wireshark | Docker (4 targets) + PCAP | ✅ **done** |
| **M4** | Vuln Mgmt & SOC | Docker (Nikto web + Hydra SSH) + John hashes + Wazuh alerts | ✅ **done** |
| **M5** | BEC / Email forensics | file-based (`.eml`) | ✅ **done** |
| **M6** | Digital forensics | file-based (FAT16 image + artefact) | ✅ **done** |
| **M7** | AI security | Docker (scripted prompt-injection sandbox) | ✅ **done** |
| **M10** | Capstone | Docker (3-target range) + 8-inject evidence package | ✅ **done** |

**All practical labs are built and validated.** The remaining modules — M2
(institutional risk register), M8 (Ghana Act 843/1038 compliance) and M9
(governance & board reporting) — are conceptual/leadership deliverables that
belong in the courseware and document templates, not in a Docker range.

> **Design note — Wazuh.** M4 teaches SIEM *triage*, not Wazuh installation. A
> full Wazuh stack (indexer + manager + dashboard) needs multiple GB of RAM per
> student and is impractical on classroom laptops, so the alerts are shipped as
> a realistic `wazuh-alerts.json` the student triages with `jq`. If a central
> instructor Wazuh server is ever available, point the lab at it instead.

Each lab is self-contained under `labs/m<N>-<slug>/`; generators under
`assets/` rebuild every artefact deterministically (PCAP, `.eml`, disk image,
encoded artefacts), so the whole evidence set is reproducible and reviewable.

M2, M8, M9 are conceptual (risk register, Ghana Act 843/1038, governance) — they
fit the courseware or document deliverables rather than Docker targets.

---

## 7. Install (the project dir is root-owned)

This was built in a staging copy. To put it in place:

```
sudo cp -r /home/kali/CAIC_lab/{labctl,engine,labs,LAB_ENGINE.md} /opt/kaiptc/CAIC_lab/
sudo chown -R $USER:$USER /opt/kaiptc/CAIC_lab
cd /opt/kaiptc/CAIC_lab && ./labctl doctor
```

For classroom rollout, ship the whole `CAIC_lab/` folder (USB or share). On
each machine: install Docker, then `./labctl start m3` builds the target image
once (needs internet that first time) and every launch after is offline.
