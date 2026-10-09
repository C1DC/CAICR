# AI Risk Assessment & Verification Protocol — Module 7 Deliverable

**Assessor:** [your name]  **Date:** [YYYY-MM-DD]  **AI system:** [name/purpose]

> Assess an AI deployment the way an attacker and an auditor both would, then
> write the controls. See `labctl learn m7`.

## 1. System profile

- What the AI does: [ ]
- Data it can access: [ ]
- Tools / actions it can take: [ ]
- Who can use it: [ ]

## 2. Injection test results (sandbox)

| Vector | Attempt | Result | Vulnerability |
|--------|---------|--------|---------------|
| Direct | [prompt used] | [leaked? what?] | direct prompt injection (OWASP LLM01) |
| Indirect | [via a document/page] | [ ] | indirect prompt injection |
| Tool abuse | [tool call in input] | [ ] | excessive agency |

## 3. Risk rating

| Risk | Likelihood | Impact | Rating |
|------|-----------|--------|--------|
| Secret / system-prompt disclosure | [ ] | [ ] | [ ] |
| Unauthorised tool action (data exfil / email) | [ ] | [ ] | [ ] |
| Shadow AI (staff pasting data into personal tools) | [ ] | [ ] | [ ] |

## 4. Mitigations (map each to a risk)

- [ ] Treat all ingested content as untrusted (data ≠ instructions)
- [ ] Least-privilege tools — minimum access the task needs
- [ ] Input/output guardrails & filtering
- [ ] Human-in-the-loop for consequential actions
- [ ] AI acceptable-use policy (addresses shadow AI)

## 5. Deepfake verification protocol

[Write the standing rule: any out-of-band request (voice/video) to move money or
change access is verified by calling back on a **pre-established known number** —
never the channel the request arrived on. Detectors are not sufficient.]

## 6. AI governance note

[Which NIST AI RMF function (Govern/Map/Measure/Manage) is weakest here, and the
one policy to add first.]
