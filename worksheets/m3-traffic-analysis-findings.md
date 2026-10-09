# Traffic Analysis Findings & Control Design — Module 3 Deliverable

**Analyst:** [your name]  **Date:** [YYYY-MM-DD]  **Network:** [e.g. 10.13.3.0/24]

> Record what you found on the network and the capture, then design the controls
> that close each gap. See `labctl learn m3`.

## 1. Host & service inventory (Nmap)

| Host IP | Open ports / services | Concern |
|---------|-----------------------|---------|
| [ ] | [ ] | [e.g. unauth admin panel / cleartext FTP / exposed RDP] |
| [ ] | | |
| [ ] | | |

## 2. Suspicious traffic (Wireshark / tcpdump)

- Infected host IP: [ ]
- C2 domain observed: [ ]
- Beacon interval: [ ] seconds — *why this looks like beaconing:* [ ]
- Other indicators: [ ]

**ATT&CK:** T1046 (Network Service Discovery), T1071 (Application Layer Protocol).

## 3. Control design (map each gap to a fix, with priority)

| # | Finding | Recommended control | Priority (H/M/L) | Owner |
|---|---------|---------------------|------------------|-------|
| 1 | *Example:* RDP 3389 exposed | Close port / VPN + MFA | H | IT |
| 2 | [FILL IN] | [e.g. network segmentation] | | |
| 3 | [FILL IN] | [e.g. DNS monitoring] | | |
| 4 | [FILL IN] | | | |

## 4. One-line summary for leadership

[Business impact of what's exposed, and the single most urgent fix.]
