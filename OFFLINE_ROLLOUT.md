# CAIC CyberLab — Offline / USB Rollout Checklist

How to prepare a classroom of student Kali machines that will run **with no
internet**. The labs are designed to be fully offline *after* a one-time,
internet-connected preparation of the images.

---

## A. On the prep machine (once, with internet)

- [ ] Clone/copy the project and open a terminal in it.
- [ ] `./labctl doctor` — confirm Docker + Compose + Python 3.11+ are present.
- [ ] `./labctl prep` — builds and caches all lab images (pulls base images and
      packages; this is the only step that needs internet).
- [ ] `python3 scripts/dry_run.py` — confirms every lab grades 100%
      ("ALL LABS PASS"). Fix anything that fails before class.
- [ ] `python3 scripts/answer_key.py` — refresh `FACILITATOR_ANSWER_KEY.md`.
- [ ] `bash scripts/package.sh` — produces `dist/`:
      - `caic-lab-images.tar.gz` (the built Docker images)
      - `caic-cyberlab.tar.gz` (the project)
      - `INSTALL-OFFLINE.txt` (per-machine steps)
- [ ] Copy the whole `dist/` folder to a **USB stick** (or a local file share).

> Image bundle size is roughly a few hundred MB — it carries Debian/Alpine/httpd/
> python base layers so student machines need nothing from the internet.

---

## B. On each student machine (offline)

Machine requirements: Kali/Debian Linux, **Docker**, **Python 3.11+**. If a
machine lacks Docker *and* has no internet, install Docker from an offline Debian
package mirror first.

- [ ] Copy `caic-cyberlab.tar.gz` and `caic-lab-images.tar.gz` from the USB.
- [ ] Unpack the project:
      `mkdir -p ~/CAIC_lab && tar -xzf caic-cyberlab.tar.gz -C ~/CAIC_lab`
- [ ] Load the images (no internet):
      `docker load -i caic-lab-images.tar.gz`
- [ ] Put the user in the docker group (or plan to use `sudo labctl`):
      `sudo usermod -aG docker $USER` then log out/in.
- [ ] Verify: `cd ~/CAIC_lab && ./labctl doctor` (green ticks).
- [ ] Smoke test: `./labctl start m1` → `./labctl stop m1` (targets come up/down).

(Steps B are also written to `dist/INSTALL-OFFLINE.txt` by the packaging script.)

---

## C. Classroom-day checklist

- [ ] Each machine: `./start.sh` opens the app in the browser.
- [ ] Project the facilitator run-of-show (`FACILITATOR_GUIDE.md`).
- [ ] Keep `FACILITATOR_ANSWER_KEY.md` to hand (facilitator only).
- [ ] Hand each student the one-page `STUDENT_HANDOUT.md` (print it).
- [ ] Reinforce the rule of engagement: **only `10.13.x.x` lab targets** (Act 1038).

---

## D. After the course

- [ ] Collect each student's progress for grading: copy their
      `~/.local/share/caic-lab/state.json` (rename per student), then on one
      machine run `./labctl report <folder-of-json-files>` for a class matrix.
- [ ] To reset a machine for the next cohort: `./labctl reset-progress` and
      `./labctl stop` (stops any running labs).

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `labctl doctor` says Docker unreachable | start Docker (`sudo systemctl start docker`) or add user to `docker` group |
| `docker load` fails | ensure you copied the full `.tar.gz`; `docker load -i <file>` |
| Lab "subnet overlaps" error | another Docker network uses that `/24`; edit `[network] subnet` in that lab's `lab.toml` |
| A lab won't grade a `script` check | it checks live state — make sure the lab is started first |
| Student tools missing (nmap, etc.) | they ship with Kali; on plain Debian install the course toolset from an offline mirror |
