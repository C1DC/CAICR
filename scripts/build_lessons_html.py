#!/usr/bin/env python3
"""Build cyberlab-lessons.html — a single-file, offline browser reader for the
deep course lessons and deliverable templates.

Source of truth is lessons/*.md and worksheets/*.md; run this whenever they
change:  python3 scripts/build_lessons_html.py

Pure stdlib. Produces one self-contained HTML file (no external fetch), so it
works from file:// with no server, exactly like cyberlab.html.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from engine.mdhtml import md_to_html  # noqa: E402

LESSONS = ROOT / "lessons"
WORKSHEETS = ROOT / "worksheets"
OUT = ROOT / "cyberlab-lessons.html"

MODULES = [
    ("m0", 1), ("m1", 1), ("m2", 1), ("m3", 2), ("m4", 2), ("m5", 3),
    ("m6", 3), ("m7", 4), ("m8", 4), ("m9", 5), ("m10", 5),
]


# ─────────────────────────────── assemble ───────────────────────────────

def build() -> str:
    data = {}
    for mid, day in MODULES:
        lf = LESSONS / f"{mid}.md"
        if not lf.is_file():
            continue
        md = lf.read_text(encoding="utf-8")
        title = md.splitlines()[0].lstrip("# ").strip()
        lesson_html = md_to_html(md)
        sheets = []
        for ws in sorted(WORKSHEETS.glob(f"{mid}-*.md")):
            sheets.append({"name": ws.name, "html": md_to_html(ws.read_text(encoding="utf-8"))})
        data[mid] = {"day": day, "title": title, "lesson": lesson_html, "sheets": sheets}

    payload = json.dumps(data, ensure_ascii=False)
    return PAGE.replace("/*__DATA__*/", payload)


PAGE = r"""<!doctype html>
<html lang="en" data-theme="dark">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>KAIPTC CAIC CyberLab — Lessons</title>
<style>
:root{
  --bg:#0e0b16; --surface:#17132233; --surface2:#1d1830; --border:#2e2740;
  --kali:#9b6dff; --kali-lt:#c3a6ff; --gold:#ffcf6b; --teal:#5fd3c6;
  --fg:#ece8f5; --fg-mid:#b9b2cf; --fg-dim:#7d7595; --green:#57d98a;
  color-scheme:dark;
}
:root:not([data-theme="dark"]) @media (prefers-color-scheme: light){}
:root[data-theme="light"]{
  --bg:#f6f4fb; --surface:#ffffff; --surface2:#efeaf8; --border:#e0d9f0;
  --kali:#6f3fe0; --kali-lt:#8a5cf0; --gold:#b9811a; --teal:#1f9c8e;
  --fg:#241d38; --fg-mid:#4d4466; --fg-dim:#7a7191; --green:#1f9d57;
  color-scheme:light;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
header{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:12px;
  padding:12px 18px;background:linear-gradient(90deg,#1a1230,#241a3f);
  border-bottom:1px solid var(--border);}
header .brand{font-weight:700;color:var(--kali-lt);letter-spacing:.3px}
header .brand b{color:var(--gold)}
header .spacer{flex:1}
button.theme{background:var(--surface2);color:var(--fg);border:1px solid var(--border);
  border-radius:8px;padding:6px 12px;cursor:pointer;font-size:14px}
.layout{display:flex;max-width:1180px;margin:0 auto;min-height:calc(100vh - 54px)}
nav{width:290px;flex:0 0 290px;border-right:1px solid var(--border);padding:16px 10px;}
nav input{width:100%;padding:9px 11px;margin-bottom:10px;background:var(--surface2);
  border:1px solid var(--border);border-radius:8px;color:var(--fg);font-size:14px}
.day-h{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:var(--fg-dim);
  margin:14px 10px 4px}
nav a{display:block;padding:8px 11px;border-radius:8px;color:var(--fg-mid);
  text-decoration:none;font-size:14.5px;cursor:pointer}
nav a:hover{background:var(--surface2);color:var(--fg)}
nav a.active{background:var(--kali);color:#fff;font-weight:600}
nav a .mid{color:var(--gold);font-weight:700;margin-right:6px}
nav a.active .mid{color:#fff}
main{flex:1;min-width:0;padding:26px 34px 80px}
article{max-width:780px}
h1{font-size:27px;line-height:1.25;color:var(--kali-lt);margin:.2em 0 .6em}
h2{font-size:21px;color:var(--gold);margin:1.5em 0 .4em;padding-top:.3em}
h3{font-size:17px;color:var(--teal);margin:1.2em 0 .3em}
p{margin:.6em 0}
code{background:var(--surface2);color:var(--green);padding:1px 6px;border-radius:5px;
  font:14px/1.5 "SFMono-Regular",Consolas,"Liberation Mono",monospace}
pre{background:#0b0814;border:1px solid var(--border);border-left:3px solid var(--kali);
  border-radius:8px;padding:14px 16px;overflow:auto}
pre code{background:none;color:var(--green);padding:0}
blockquote{margin:1em 0;padding:10px 16px;border-left:3px solid var(--gold);
  background:var(--surface2);border-radius:0 8px 8px 0;color:var(--fg-mid)}
ul,ol{margin:.5em 0;padding-left:1.4em}
li{margin:.25em 0}
hr{border:none;border-top:1px solid var(--border);margin:1.6em 0}
table{border-collapse:collapse;width:100%;margin:1em 0;font-size:14.5px;display:block;overflow:auto}
th,td{border:1px solid var(--border);padding:7px 10px;text-align:left;vertical-align:top}
th{background:var(--surface2);color:var(--fg)}
details{margin:1.2em 0;border:1px solid var(--border);border-radius:8px;background:var(--surface2)}
details>summary{cursor:pointer;padding:11px 14px;font-weight:600;color:var(--gold)}
details[open]>summary{border-bottom:1px solid var(--border)}
details .body{padding:4px 16px 12px}
.hint{color:var(--fg-dim);font-size:13.5px;margin-top:10px}
@media(max-width:820px){
  .layout{flex-direction:column}
  nav{width:auto;flex:none;border-right:none;border-bottom:1px solid var(--border)}
  main{padding:20px 16px 60px}
}
</style>
</head>
<body>
<header>
  <span class="brand">KAIPTC CAIC CyberLab · <b>Lessons</b></span>
  <span class="spacer"></span>
  <button class="theme" onclick="toggleTheme()">◐ Theme</button>
</header>
<div class="layout">
  <nav>
    <input id="search" placeholder="Search modules…" oninput="filter(this.value)">
    <div id="navlist"></div>
  </nav>
  <main><article id="content"></article>
    <p class="hint">Terminal version: <code>labctl learn m1</code> ·
       Deliverable template: <code>labctl worksheet m1</code></p>
  </main>
</div>
<script>
const DATA = /*__DATA__*/;
const DAYS={1:"Day 1",2:"Day 2",3:"Day 3",4:"Day 4",5:"Day 5"};
function buildNav(){
  const order=Object.keys(DATA);
  let lastDay=null,h="";
  for(const mid of order){
    const d=DATA[mid];
    if(d.day!==lastDay){h+=`<div class="day-h">${DAYS[d.day]||("Day "+d.day)}</div>`;lastDay=d.day;}
    const label=d.title.replace(/^Module\s+\d+\s*[—-]\s*/,"");
    h+=`<a data-mid="${mid}" onclick="show('${mid}')"><span class="mid">${mid.toUpperCase()}</span>${label}</a>`;
  }
  document.getElementById('navlist').innerHTML=h;
}
function show(mid){
  const d=DATA[mid]; if(!d) return;
  let h=d.lesson;
  if(d.sheets&&d.sheets.length){
    for(const s of d.sheets){
      h+=`<details><summary>📝 Deliverable template — ${s.name}</summary><div class="body">${s.html}</div></details>`;
    }
  }
  document.getElementById('content').innerHTML=h;
  document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('active',a.dataset.mid===mid));
  window.scrollTo(0,0);
  try{localStorage.setItem('caic_last',mid);}catch(e){}
  if(location.hash!=='#'+mid) history.replaceState(null,'','#'+mid);
}
function filter(q){
  q=q.toLowerCase();
  document.querySelectorAll('nav a').forEach(a=>{
    const d=DATA[a.dataset.mid];
    const hay=(d.title+' '+d.lesson).toLowerCase();
    a.style.display=hay.includes(q)?'block':'none';
  });
}
function toggleTheme(){
  const r=document.documentElement;
  const t=r.getAttribute('data-theme')==='light'?'dark':'light';
  r.setAttribute('data-theme',t);
  try{localStorage.setItem('caic_theme',t);}catch(e){}
}
(function init(){
  try{const t=localStorage.getItem('caic_theme');if(t)document.documentElement.setAttribute('data-theme',t);}catch(e){}
  buildNav();
  let start=(location.hash||'').replace('#','');
  if(!DATA[start]){try{start=localStorage.getItem('caic_last');}catch(e){}}
  if(!DATA[start]) start=Object.keys(DATA)[0];
  show(start);
})();
</script>
</body>
</html>
"""


def main() -> int:
    OUT.write_text(build(), encoding="utf-8")
    kb = OUT.stat().st_size / 1024
    print(f"wrote {OUT} ({kb:.0f} KB) — {len(MODULES)} modules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
