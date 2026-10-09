# KAIPTC CyberLab — Architecture Reference
## For Developers and Claude Agent Continuation

---

## Overview

Single-file HTML SPA (Single Page Application). No build step, no server, no framework. All state in `localStorage`. All UI rendered by JavaScript DOM manipulation.

---

## File Structure (Inside cyberlab.html)

```
cyberlab.html
├── <title> + Google Fonts <link>
├── <style>          — All CSS (tokens, layout, components)
└── <script>         — All JavaScript (data, state, UI engine)
    ├── COURSE data   — 5 days × modules × labs × quizzes
    ├── TOOLS data    — 13 Kali tool reference entries
    ├── state object  — currentDay, currentMod, completedMods, view, theme
    ├── persistence   — loadState() / saveState() via localStorage
    ├── render()      — Master render dispatcher
    ├── renderModule() — Learn view renderer
    ├── renderTools()  — Tool reference renderer
    ├── renderQuiz()   — Quiz engine
    ├── renderDashboard() — Progress view
    └── init()        — Bootstrap + event binding
```

---

## CSS Architecture

### Color Tokens (`:root`)
```css
--bg, --surface, --surface2, --border   /* backgrounds */
--navy, --kali, --kali-mid, --kali-lt   /* brand purples */
--gold, --gold-lt                        /* accent gold */
--teal                                   /* secondary accent */
--green, --green-dk                      /* terminal / success */
--red, --amber                           /* danger / warning */
--fg, --fg-mid, --fg-dim                 /* text hierarchy */
```

### Theme Strategy
- Default: dark (`:root` defines dark values, `color-scheme: dark`)
- Light override via `@media (prefers-color-scheme: light)` + `[data-theme="light"]`
- Toggle writes `data-theme` to `<html>` element and saves to state

### Key Component Classes
| Class | Purpose |
|-------|---------|
| `.sidebar` | Left nav — collapsible on mobile |
| `.content` | Right panel — main scroll area |
| `.terminal` | Dark terminal box with green monospace text |
| `.lab-card` | Mission card with numbered steps |
| `.tool-card` | Kali tool reference card |
| `.quiz-opt` | Quiz option button (correct/wrong states) |
| `.mod-complete` | Green check badge for completed modules |
| `.day-band` | Day header in sidebar |

---

## JavaScript Data Model

### COURSE Array
```javascript
const COURSE = [
  {
    day: 1,
    title: "...",
    modules: [
      {
        id: "M1",
        title: "...",
        kaliTools: ["nmap", "dig"],   // shown as badges
        theory: [
          { heading: "...", body: "..." }
        ],
        concepts: [
          { icon: "🔒", title: "...", desc: "..." }
        ],
        labs: [
          {
            title: "...",
            objective: "...",
            steps: ["...", "..."],
            commands: [
              { cmd: "nmap -sV target", note: "Explanation..." }
            ]
          }
        ],
        quiz: [
          {
            q: "Question text",
            opts: ["A", "B", "C", "D"],
            ans: 0,          // index of correct answer
            explain: "..."
          }
        ]
      }
    ]
  }
]
```

### TOOLS Array
```javascript
const TOOLS = [
  {
    name: "nmap",
    category: "Network Scanning",
    desc: "...",
    install: "sudo apt install nmap",
    commands: [
      { cmd: "nmap -sV -p 1-1000 target", desc: "Version scan top ports" }
    ],
    tips: ["...", "..."]
  }
]
```

### State Object
```javascript
let state = {
  currentDay: 0,          // index into COURSE array
  currentMod: 0,          // index into day.modules array
  completedMods: [],      // array of "M1", "M3" etc (serialized Set)
  view: 'module',         // 'module' | 'tools' | 'quiz' | 'dashboard'
  quizMod: null,          // module ID for active quiz, or 'all'
  theme: 'auto'           // 'auto' | 'light' | 'dark'
}
```

### localStorage Key
`cyberlab_state` — JSON-serialized state (completedMods as Array)

---

## Render Flow

```
User action (click)
  → update state
  → saveState()
  → render()
    → switch(state.view)
      → renderModule(day, mod)   writes to #content
      → renderTools()
      → renderQuiz(modId)
      → renderDashboard()
```

---

## Adding Content (For Claude Agent)

### Add a New Module to an Existing Day
1. Find the day object in `COURSE`
2. Push a new module object into `day.modules[]`
3. Follow the schema above exactly

### Add a New Kali Tool
1. Push a new entry into `TOOLS[]`
2. Reference it by name in any module's `kaliTools: []` array

### Add a New View
1. Add a nav button in the sidebar HTML (`renderSidebar()`)
2. Add a `case 'viewname':` in the `render()` switch
3. Write a `renderMyView()` function

### Add Learner Comparison / Multi-User
- Current: single-user localStorage
- To compare: export state as JSON → facilitator collects → compare in a separate "facilitator view"
- Or: add a `facilitatorCode` field; learners enter it; data posts to a simple webhook/sheet

---

## Known Limitations / Future Work

| Feature | Status | Notes |
|---------|--------|-------|
| Modules M7, M8, M9 | Missing | Need content for Incident Response, Risk Management, Governance |
| Facilitator dashboard | Missing | Aggregate progress view across learners |
| Export/print certificate | Missing | PDF generation on completion |
| Glossary | Missing | 50-term cybersecurity glossary |
| Progress comparison | Missing | Side-by-side learner stats |
| Offline fonts | Missing | Inline Google Fonts as base64 for full offline |
| Audio narration | Missing | Text-to-speech per section |
| Video embeds | Missing | YouTube/local video per module |

