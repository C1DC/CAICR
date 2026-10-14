**A SOC flagged a workstation for odd traffic — prove the compromise across three evidence sources.**  ·  Day 2 · ~2 h · 20 graded tasks

::: note | What this lab is
A Ghanaian institution's SOC flagged workstation **FIN-03** (`10.13.3.30`) for
strange outbound traffic. You investigate across three sources — the **live
subnet** (scan it with Nmap), a **packet capture** from the network tap (read it
in Wireshark), and a **netstat** taken on FIN-03 during live response — then
**correlate** them into one story and design the controls. You practise Nmap+NSE,
Wireshark stream-following, and host-evidence reading.
:::

## What's running

- **Four live targets on `10.13.3.0/24`** (launched for you): `.10` web server
  (unauthenticated admin console), `.20` fileserver (anonymous/cleartext FTP),
  `.30` FIN-03 — the infected SSH host, `.40` legacy RDP.
- **Evidence files (`assets/`, personalised to you):** `network-capture.pcap`,
  `netstat-FIN03.txt`.

## How to use this lab

**In the GUI (this page):**
1. Click **Start**. The four targets come up; wait for **● running**.
2. In the **Terminal** tab, work the mission — scan the range, open the capture,
   read the netstat.
3. Enter findings in the **Verify** panel → **Submit & grade**.
4. **Reset** rebuilds the subnet clean; **Stop** tears it down.

**Prefer the terminal?** `labctl start m3` → investigate → `labctl verify m3`.

::: warning | The guards — read before you start
- Scan and investigate **only** `10.13.3.0/24` — the IPs in the table above.
  Nmap against anything else is an offence under Act 1038.
- The C2 domain, the FTP credentials and the backdoor port are **randomised to
  you** — read *your* evidence and report *your* values.
- A capture filter decides what is *recorded*; a display filter decides what is
  *shown* — don't confuse them in Wireshark.
:::

## The mission — step by step

### Part 1 — Map & fingerprint with Nmap + NSE

```Terminal
nmap -sn 10.13.3.0/24                         # who is alive?
nmap -sV -p 21,22,80,443,3389 10.13.3.0/24    # service + version detection
nmap --script=http-title -p80 10.13.3.0/24    # find the unauth admin panel
nmap --script ftp-anon -p21 10.13.3.20        # is anonymous FTP allowed?
nmap -sV -p22 10.13.3.30                       # fingerprint FIN-03's SSH
```

Find the live hosts, the unauthenticated web panel, the exposed RDP port, the
SSH version on FIN-03, and whether the fileserver allows anonymous FTP.

### Part 2 — Follow the capture in Wireshark

```Terminal
wireshark assets/network-capture.pcap &
```

Recover two things: (1) the **C2 beacon** — filter `dns`; one host repeats the
same lookup at a fixed interval — note the **domain**, the **interval**, and the
**infected host IP**. (2) **Cleartext credentials** — right-click an FTP packet →
**Follow → TCP Stream** and read the **username and password** off the wire.

### Part 3 — Correlate the host evidence (netstat)

```Terminal
cat assets/netstat-FIN03.txt
```

Identify the **malware process** (it masquerades as a Windows service — read the
spelling carefully), the **backdoor port** it listens on, and the **external C2
IP** it is connected to. Make the correlation: *the beacon domain resolves to the
C2 IP in the netstat, and both belong to the same malicious process.*

### Part 4 — Conclude

Map the DNS C2 channel to a **MITRE ATT&CK** technique, then design four controls:
segmentation, DNS monitoring, killing cleartext FTP (SFTP/FTPS), and MFA +
firewalling on the exposed RDP.

## What you'll be graded on

The **Verify** panel has 20 checks across the three sources. Then write it up:

```Terminal
labctl verify m3
labctl worksheet m3    # traffic-analysis findings + control design
```

::: key | Tips
- "Same destination + fixed interval, round the clock" = a beacon, not a human.
- Read `svchost` vs `svch0st` character by character — masquerading defeats the
  hurried.
- A finding the scan, the capture *and* the netstat all support is proof; one
  source alone is only a lead.
:::
