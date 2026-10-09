# M3 — Network Compromise Investigation

**Scenario.** A Ghanaian institution's SOC flagged workstation **FIN-03**
(`10.13.3.30`) for odd outbound traffic. You have three evidence sources: the
live subnet, a packet capture from the network tap, and a `netstat` taken on
FIN-03 during live response. Map the network, prove the compromise, and recover
what the attacker exposed — then design the controls.

Targets: `10.13.3.10` web · `10.13.3.20` FTP · `10.13.3.30` FIN-03 (SSH) ·
`10.13.3.40` legacy RDP. Evidence in `assets/`: `network-capture.pcap`,
`netstat-FIN03.txt`.

> ⚠ **CyberRange rule.** Scan and investigate **only** `10.13.3.0/24`.

---

## Part 1 — Map & fingerprint with Nmap + NSE

```
$ nmap -sn 10.13.3.0/24                         # who is alive?
$ nmap -sV -p 21,22,80,443,3389 10.13.3.0/24    # service + version detection
$ nmap --script=http-title -p80 10.13.3.0/24    # find the unauth admin panel
$ nmap --script ftp-anon -p21 10.13.3.20        # is anonymous FTP allowed?
$ nmap -sV -p22 10.13.3.30                       # fingerprint FIN-03's SSH
```

Find: the live hosts, the unauthenticated web panel, the exposed RDP port, the
SSH version on FIN-03, and whether the fileserver allows **anonymous FTP** (an
NSE script tells you directly).

## Part 2 — Follow the capture in Wireshark

```
$ wireshark assets/network-capture.pcap &
```

Two things to recover:

1. **The C2 beacon** — apply the display filter `dns`. One host repeats the same
   lookup at a fixed interval. Find the **domain**, the **interval**, and the
   **infected host's IP**.
2. **Cleartext credentials** — the capture also contains a plain-FTP login.
   Right-click an FTP packet → **Follow → TCP Stream** (or
   `tcpdump -r assets/network-capture.pcap -A`). Read the **username and
   password** straight off the wire — the reason cleartext FTP is a finding.

## Part 3 — Correlate the host evidence (netstat)

```
$ cat assets/netstat-FIN03.txt
```

Identify the **malware process** (it is masquerading as a Windows service — look
closely at the spelling), the **backdoor port** it listens on, and the **external
C2 IP** it is connected to. Then make the correlation that turns three artefacts
into one story: *the beacon domain from the capture resolves to the C2 IP in the
netstat, and both belong to the same malicious process.*

## Part 4 — Conclude

- Map the C2 channel to a **MITRE ATT&CK** technique.
- In the worksheet, design four controls: network segmentation, DNS monitoring,
  killing cleartext FTP (FTPS/SFTP), and MFA + firewalling on the exposed RDP.

---

## Grade yourself, then write it up

```
$ labctl verify m3
$ labctl worksheet m3
```
