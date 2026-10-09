# M3 — Network Compromise Investigation

**Scenario.** A mid-sized Ghanaian institution suspects one of its internal
workstations is compromised. You have been given access to an isolated copy of
the affected subnet (`10.13.3.0/24`) and a packet capture pulled from the
network tap. Map the network, find what shouldn't be exposed, then prove which
host is talking to an attacker's command-and-control (C2) server.

> ⚠ **CyberRange rule.** Scan and investigate **only** `10.13.3.0/24`. These
> targets live on a private Docker network and never leave your machine. Using
> these tools on any other network is outside the authorised lab.

---

## Part 1 — Map the subnet with Nmap

```
$ nmap -sn 10.13.3.0/24                 # which hosts are alive?
$ nmap -sV -p 21,22,80,443,3389 10.13.3.0/24   # what services + versions?
$ nmap --script=http-title -p80 10.13.3.0/24   # grab web page titles
$ nmap -oN m3_scan.txt 10.13.3.0/24            # save your evidence
```

Questions to answer (you'll submit these in `labctl verify m3`):
- How many **target** hosts are live? (don't count the `.1` gateway — that's your own host side)
- Which host serves an **unauthenticated** web admin panel?
- Which host exposes a **legacy remote-access** service, and on what port?
- Which service transmits credentials in **cleartext**?

---

## Part 2 — Find the C2 beacon with Wireshark

Open the capture that shipped with this lab:

```
$ wireshark assets/network-capture.pcap &
```

In Wireshark, apply the display filter `dns`. Most malware talks to its C2 over
DNS. Look for one internal host repeating the **same lookup at a fixed
interval** — that regular "heartbeat" is beaconing.

- What **domain** is the infected host beaconing to?
- What is the **interval** between beacons, in seconds?

(CLI alternative, if you prefer tcpdump:)

```
$ tcpdump -r assets/network-capture.pcap -n 'udp port 53'
```

---

## Part 3 — Map to MITRE ATT&CK

Translate the beaconing behaviour to an ATT&CK technique ID (Command and
Control → Application Layer Protocol). Then, in your head or notes, list four
controls that would have caught or stopped this: network segmentation, DNS
monitoring, MFA on the exposed RDP, and a firewall rule closing 3389.

---

## Grade yourself

```
$ labctl verify m3
```
