# M6 — Digital Forensics & Incident Response

**Scenario.** Workstation **FIN-03** is suspected in a ransomware incident. The
responder pulled a disk image before the machine was wiped. Your job: prove the
image is intact, reconstruct what happened, and recover what the user tried to
destroy — all while preserving chain of custody.

Evidence in `assets/`:
`evidence.img` (disk image) · `evidence.sha256` (recorded hash) ·
`suspicious_artifact.txt` (obfuscated string pulled from a Temp folder).

> **Golden rule.** Hash first, analyse second. Never work on original evidence
> without proving — mathematically — that you did not change it.

---

## 1. Prove integrity (chain of custody)

```
$ cd labs/m6-forensics/assets
$ sha256sum evidence.img                 # what is the hash?
$ sha256sum -c evidence.sha256           # does it match what was recorded?
```

## 2. Examine the image — Autopsy or Sleuthkit

GUI (the Autopsy workflow taught in class):
```
$ autopsy &        # then open http://localhost:9999/autopsy, create a case,
                   # add evidence.img as a disk image, run ingest modules
```

CLI (fast, same backend as Autopsy):
```
$ fsstat evidence.img                    # filesystem type + layout
$ fls evidence.img                       # list files (a '*' marks DELETED)
$ icat evidence.img 5                    # read a file by its inode number
$ tsk_recover evidence.img ./recovered   # carve back deleted files
```

Find:
- the **filesystem type**,
- the **macro-enabled spreadsheet** the user opened (the lure),
- the **deleted credentials file** — recover it and read the **VPN password**.

## 3. Decode the dropped artefact — CyberChef

Open `suspicious_artifact.txt`. It's obfuscated. In CyberChef build the recipe:

```
From Base64   →   URL Decode
```
(CLI alternative: `base64 -d suspicious_artifact.txt`, then URL-decode.)

What **C2 domain** does it reveal?

## 4. Think IR

- By **order of volatility**, what should have been collected *first* — before
  the disk image?
- Map the macro-runs-PowerShell behaviour to a **MITRE ATT&CK** technique.

---

## Grade yourself

```
$ labctl verify m6
```
