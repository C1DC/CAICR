# Installing the CAIC CyberLab — Student Guide

**Professional Certificate in Cybersecurity, AI & Digital Resilience**
KAIPTC · Cyber1Defense Communication Ltd

Repository: **https://github.com/C1DC/CAICR** *(private — you need the access token your facilitator gives you)*

Follow these steps on your **Kali Linux** machine. You do it **once**; after that
the whole course — lessons, labs and the live terminal — runs on your laptop.

---

## Before you start — quick checklist

- [ ] **Kali Linux** (the course is built for it).
- [ ] **Internet** — needed the first time only (to download the course and build the labs).
- [ ] **~10 GB free disk** for the lab images.
- [ ] **The access token** your facilitator gives you (because the repository is private).

---

## Step 1 — Install the basics (Docker + Git)

Open a terminal and run:

```bash
sudo apt update
sudo apt install -y git docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker "$USER"
```

Then **log out and back in** (or run `newgrp docker`) so Docker works without `sudo`.

## Step 2 — Get your access token

The repository is **private**, so you can't download it anonymously. Your
facilitator will give you a **read-only access token** (a long string that starts
with `github_pat_...` or `ghp_...`). Keep it handy for the next step — you paste it
*instead of a password*.

## Step 3 — Download (clone) the course

```bash
cd ~
git clone https://github.com/C1DC/CAICR.git
```

When it asks:
- **Username:** type `C1DC` (or whatever your facilitator says)
- **Password:** **paste the access token** (not a real password — the screen stays blank while you paste; press Enter)

*(Shortcut — one line, if your facilitator gave you the token to put in the link:)*
```bash
git clone https://<PASTE-TOKEN-HERE>@github.com/C1DC/CAICR.git
```

## Step 4 — One-time setup

```bash
cd CAICR
chmod +x labctl start.sh        # (only if you get a "permission denied")
./labctl doctor                 # checks Docker + tools are ready
./start.sh --prep               # builds & caches all lab images — needs internet, ~10–20 min
```

`./labctl doctor` should show green ticks. `--prep` only needs to run **once**;
after it finishes, the labs work **fully offline**.

## Step 5 — Launch the GUI

```bash
./start.sh
```

Your browser opens the **CAIC CyberLab** at **http://localhost:8899** — the
dashboard, every lesson, the hands-on labs (launched and graded in the browser),
the live Kali terminal, the tools reference and your progress. Press **Ctrl-C** in
the terminal to stop it.

---

## Using it day to day

```bash
cd ~/CAICR
./start.sh          # launch the web app   (Ctrl-C to stop)
```

Prefer the terminal? `./labctl list` shows every lab; `./labctl learn m1` reads a
lesson; `./labctl start m3` → investigate → `./labctl verify m3`.

## Getting updates later

```bash
cd ~/CAICR
git pull            # (paste your token again if asked)
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Cannot connect to the Docker daemon` | `sudo systemctl start docker`; make sure you logged out/in after Step 1 (or run `newgrp docker`). |
| `permission denied` on `./labctl` or `./start.sh` | `chmod +x labctl start.sh` |
| Browser didn't open | Go to **http://localhost:8899** manually. |
| Port 8899 already in use | `CAIC_PORT=8900 ./start.sh` then open http://localhost:8900 |
| Clone keeps asking for a password / says `403` | Your token is wrong or expired — get a fresh read-only token from your facilitator. |
| A lab won't start | `./labctl doctor` to diagnose; `./labctl reset m3` for a clean rebuild of that lab. |

**Safety rule (all week):** only ever scan or attack the lab targets on `10.13.x.x`.
Pointing any tool at anything else is illegal under Ghana's Cybersecurity Act 2020
(Act 1038).

---

## For the facilitator — how to hand out access

The repo is private, so students need credentials to clone it. Two options:

1. **Read-only token (GitHub):** on the **C1DC** account → Settings → Developer
   settings → **Fine-grained tokens** → *Repository access = only `CAICR`*,
   *Permissions → Contents = Read-only*. Share that token with the class. It can
   **only clone** (not push), and you can **rotate/revoke it after the course**.
   *(It is a shared secret — scope it to just `CAICR`, read-only, and expire it.)*
2. **Offline USB bundle (no token, no internet):** build the images on one machine
   and distribute the tarball — see **`OFFLINE_ROLLOUT.md`**. Best for rooms with
   no reliable internet; students never touch GitHub.
