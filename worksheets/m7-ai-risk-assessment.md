# AI Risk Assessment & Verification Protocol — Module 7 Deliverable

**Assessor:** [your name]  **Date:** [YYYY-MM-DD]  **AI system:** [name/purpose]

> Assess an AI deployment the way an attacker and an auditor both would, then
> write the controls. See `labctl learn m7`.

## 1. System profile

- What the AI does: [ ]
- Data / knowledge base it can access: [ ]
- Tools / actions it can take: [ ]
- Who can use it, and over what channels: [ ]

## 2. Attack test results (sandbox)

| Vector | Attempt | Result | OWASP / class |
|--------|---------|--------|---------------|
| Direct injection (`/chat`) | [prompt used] | [leaked? what?] | LLM01 Prompt Injection |
| RAG / data poisoning (`/ask`) | [question asked] | [fraudulent value returned] | Knowledge-base poisoning |
| Indirect injection (`/summarize`) | [via which document] | [AI obeyed hidden instruction] | Indirect prompt injection |
| Tool abuse / excessive agency | [tool invoked from input] | [exfil address / action] | Excessive agency |

## 3. Risk rating

| Risk | Likelihood | Impact | Rating |
|------|-----------|--------|--------|
| Secret / system-prompt disclosure | [ ] | [ ] | [ ] |
| Poisoned knowledge base serving false "facts" (e.g. mule account) | [ ] | [ ] | [ ] |
| Unauthorised tool action (data exfil / email) | [ ] | [ ] | [ ] |
| Shadow AI (staff pasting data into personal tools) | [ ] | [ ] | [ ] |

## 4. Mitigations (map each to a risk above)

- [ ] Treat all ingested content as untrusted (data ≠ instructions)
- [ ] Least-privilege tools — minimum access the task needs
- [ ] Input/output guardrails & filtering (scan output for secrets / injected tool calls)
- [ ] Human-in-the-loop for consequential actions (payments, exports, access changes)
- [ ] Integrity controls on the RAG knowledge base (who can write to it?)
- [ ] **Output sanitised** before it reaches a browser/DB/shell (LLM05)
- [ ] **Dual-LLM / privilege separation** — the tool-holding model never sees untrusted input directly
- [ ] **Rate limits & budgets**; prompts/responses logged for monitoring
- [ ] AI acceptable-use policy + a sanctioned alternative (addresses shadow AI)

## 4b. Red-team & evaluation

- **Jailbreaks tested:** [role-play / obfuscation / many-shot / prompt-leaking / indirect]
- **Safety eval suite:** [where it lives; runs on every model/prompt change? yes/no]
- **Tooling:** [e.g. garak / PyRIT / promptfoo]

## 4c. Governance & law

- **NIST AI RMF** weakest function (Govern/Map/Measure/Manage): [ ]
- **Automated decisions** affecting people? [ ] → human-review + lawful basis under **Act 843**? [ ]
- **Data residency** — does personal data leave Ghana to a foreign AI API? [ ]

## 5. Deepfake verification protocol

**Standing rule:** any out-of-band request (voice/video) to move money or change
access is verified by calling back on a **pre-established known number** — never
the channel the request arrived on. Detectors are not sufficient.

**Behavioural red flags to train staff on (not acoustic):**

- [ ] [e.g. manufactured urgency / deadline]
- [ ] [e.g. demand for secrecy / confidentiality]
- [ ] [e.g. instruction not to call back / unusual channel]
- [ ] [e.g. pressure to bypass the normal approvers]

## 6. AI governance note

Weakest **NIST AI RMF** function here (Govern / Map / Measure / Manage): [ ]
One policy or control to add first: [ ]

---

## Self-check before you submit

- [ ] All four attack classes tested, with **my own** randomised values.
- [ ] Every mitigation in §4 maps to a specific risk in §3.
- [ ] My deepfake protocol names **behavioural** red flags, not "listen for glitches".
- [ ] I did everything against the **offline sandbox** only.

## Grading rubric (100 pts)

| Band | Attacks demonstrated (35) | Risk rating & mapping (25) | Mitigations (25) | Deepfake & governance (15) |
|------|---------------------------|----------------------------|------------------|-----------------------------|
| Excellent (full) | All four classes shown with evidence + correct OWASP/ATLAS | Rated and mapped to findings | Architectural controls, each tied to a risk | Out-of-band + behavioural flags; weakest RMF function named |
| Adequate (~60%) | 2–3 classes | Some ratings, loose mapping | Generic list | Callback only |
| Weak (<40%) | One class | No ratings | "Be careful with AI" | Relies on detectors |

---

## Worked example (reference — fictional "Adom Microfinance" procurement assistant)

**Profile:** an internal assistant that answers supplier questions from a RAG
knowledge base and can summarise documents and send email.

**Attacks:** (1) `/chat` "ignore previous instructions…" leaked the admin override
`ai_…`. (2) `/ask "supplier bank account?"` returned a **mule 10-digit account**
(RAG poisoning). (3) `/summarize` on `supplier-memo.txt` obeyed a hidden
instruction (indirect injection) and (4) drove `send_email` to exfiltrate to
`collector@mule-net.su` (excessive agency).

**Top risk:** poisoned RAG serving a mule account as fact → a staffer pays it
trusting "the system" — *likelihood High, impact High*.

**Mitigations:** lock down who can write the knowledge base + integrity checks;
hold the assistant to least-privilege tools (no arbitrary `send_email`); output
guardrails; **human approval** before any payment detail is acted on; treat all
ingested docs as untrusted.

**Deepfake protocol:** callback on the director's **known** number for any
transfer; red flags = urgency + "don't loop in Finance" + WhatsApp voice note +
"keep it confidential". **Weakest RMF function:** *Govern* — add an AI
acceptable-use policy and a knowledge-base change-control process first.
