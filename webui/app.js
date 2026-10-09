"use strict";
const $ = (s, r = document) => r.querySelector(s);
const view = $("#view");
let BOOT = null, POLL = null;
let TERM = null, TWS = null, TFIT = null, TRESIZE = null;

/* ---------- utilities ---------- */
async function api(path, opts) {
  const r = await fetch(path, opts);
  if (!r.ok) { let e; try { e = (await r.json()).error; } catch (_) {} throw new Error(e || ("HTTP " + r.status)); }
  return r.json();
}
const esc = s => (s == null ? "" : String(s)).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
function toast(msg) { const t = document.createElement("div"); t.className = "toast"; t.textContent = msg; document.body.appendChild(t); setTimeout(() => t.remove(), 2600); }
function copy(txt) { navigator.clipboard?.writeText(txt).then(() => toast("Copied")); }
function clearPoll() { if (POLL) { clearInterval(POLL); POLL = null; } }
function cleanupTerm() {
  if (TRESIZE) { window.removeEventListener("resize", TRESIZE); TRESIZE = null; }
  if (TWS) { try { TWS.close(); } catch (e) {} TWS = null; }
  if (TERM) { try { TERM.dispose(); } catch (e) {} TERM = null; }
  TFIT = null;
}

/* ---------- chrome ---------- */
function initTheme() { try { const t = localStorage.getItem("caic_theme"); if (t) document.documentElement.setAttribute("data-theme", t); } catch (e) {} }
$("#themeBtn").onclick = () => { const r = document.documentElement, t = r.getAttribute("data-theme") === "light" ? "dark" : "light"; r.setAttribute("data-theme", t); try { localStorage.setItem("caic_theme", t); } catch (e) {} };
$("#menuBtn").onclick = () => $("#app").classList.toggle("nav-open");
$("#who").onclick = () => { location.hash = "dashboard"; };
document.querySelectorAll(".rail-nav a").forEach(a => a.onclick = () => { location.hash = a.dataset.view; });

/* ---------- command palette (Ctrl-K) ---------- */
let PAL = null, PAL_SEL = 0, PAL_FILTERED = [];
function paletteItems() {
  const items = [
    { t: "Dashboard", s: "Home", ic: "▣", go: () => location.hash = "dashboard" },
    { t: "All Labs", s: "Hands-on", ic: "⌘", go: () => location.hash = "labs" },
    { t: "Live Terminal", s: "Real Kali shell", ic: "▶_", go: () => location.hash = "terminal" },
    { t: "Tools & Materials", s: "Reference", ic: "◉", go: () => location.hash = "materials" },
    { t: "Commands", s: "Cheat-sheet", ic: "⌨", go: () => location.hash = "commands" },
    { t: "Progress", s: "Your scores", ic: "▤", go: () => location.hash = "progress" },
  ];
  BOOT.modules.forEach(m => {
    items.push({ t: m.id.toUpperCase() + " — " + m.title, s: "Lesson · Day " + m.day, ic: "◈", k: "lesson", go: () => location.hash = "course/" + m.id });
    if (m.hasLab) items.push({ t: "Lab " + m.id.toUpperCase() + " — " + m.title, s: "Launch & verify", ic: "⌘", k: "lab", go: () => location.hash = "labs/" + m.id });
  });
  (BOOT.tools || []).forEach(t => items.push({
    t: t.name, s: t.cat + " · tool", ic: "◉", k: "tool",
    go: () => { location.hash = "materials"; setTimeout(() => { const el = [...document.querySelectorAll(".toolrow summary")].find(s => s.textContent.trim().startsWith(t.name)); if (el) { el.parentElement.open = true; el.scrollIntoView({ block: "center" }); } }, 140); }
  }));
  (BOOT.commands || []).forEach(c => items.push({ t: c.cmd, s: c.desc, ic: "⌨", k: "copy", go: () => copy(c.cmd) }));
  return items;
}
function openPalette() {
  if (PAL) return;
  const all = paletteItems();
  const back = document.createElement("div");
  back.className = "pal-back";
  back.innerHTML = `<div class="pal"><input placeholder="Search modules, labs, tools, commands…" autocomplete="off" spellcheck="false"><div class="pal-list"></div></div>`;
  document.body.appendChild(back); PAL = back;
  const input = back.querySelector("input"), list = back.querySelector(".pal-list");
  const render = q => {
    q = q.trim().toLowerCase();
    PAL_FILTERED = (q ? all.filter(i => (i.t + " " + i.s).toLowerCase().includes(q)) : all).slice(0, 60);
    PAL_SEL = 0;
    list.innerHTML = PAL_FILTERED.length
      ? PAL_FILTERED.map((i, idx) => `<div class="pal-item ${idx === 0 ? "sel" : ""}" data-i="${idx}"><div class="pi-ic">${i.ic}</div><div style="min-width:0"><div class="pi-t">${esc(i.t)}</div><div class="pi-s">${esc(i.s)}</div></div>${i.k ? `<div class="pi-k">${i.k}</div>` : ""}</div>`).join("")
      : `<div class="pal-empty">No matches</div>`;
    list.querySelectorAll(".pal-item").forEach(el => { el.onmouseenter = () => select(+el.dataset.i); el.onclick = () => run(+el.dataset.i); });
  };
  const select = i => { PAL_SEL = i; list.querySelectorAll(".pal-item").forEach((el, idx) => el.classList.toggle("sel", idx === i)); const s = list.querySelector(".pal-item.sel"); if (s) s.scrollIntoView({ block: "nearest" }); };
  const run = i => { const it = PAL_FILTERED[i]; closePalette(); if (it) it.go(); };
  input.addEventListener("input", () => render(input.value));
  input.addEventListener("keydown", e => {
    if (e.key === "ArrowDown") { e.preventDefault(); select(Math.min(PAL_SEL + 1, PAL_FILTERED.length - 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); select(Math.max(PAL_SEL - 1, 0)); }
    else if (e.key === "Enter") { e.preventDefault(); run(PAL_SEL); }
    else if (e.key === "Escape") closePalette();
  });
  back.addEventListener("click", e => { if (e.target === back) closePalette(); });
  render(""); input.focus();
}
function closePalette() { if (PAL) { PAL.remove(); PAL = null; } }
$("#searchBtn").onclick = openPalette;
document.addEventListener("keydown", e => {
  if ((e.ctrlKey || e.metaKey) && (e.key === "k" || e.key === "K")) {
    // Let the live terminal keep Ctrl-K (kill-line) when it has focus.
    const inTerm = !PAL && document.activeElement && document.activeElement.closest && document.activeElement.closest("#termwrap");
    if (inTerm) return;
    e.preventDefault(); PAL ? closePalette() : openPalette();
  }
});

function updateChrome() {
  $("#who").textContent = BOOT.student ? "👤 " + BOOT.student : "Set your name →";
  const p = $("#dockerPill");
  p.textContent = "Docker: " + (BOOT.summary.dockerOk ? "ready" : "not ready");
  p.className = "pill " + (BOOT.summary.dockerOk ? "ok" : "bad");
}
function setActive(v) { document.querySelectorAll(".rail-nav a").forEach(a => a.classList.toggle("active", a.dataset.view === v)); }
function crumb(parts) { $("#crumb").innerHTML = parts.map((p, i) => i < parts.length - 1 && p.href ? `<a href="${p.href}">${esc(p.t)}</a>` : `<span>${esc(p.t)}</span>`).join('<span class="sep">/</span>'); }

/* ---------- module helpers ---------- */
const modById = id => BOOT.modules.find(m => m.id === id);
function modBadges(m) {
  let b = "";
  if (m.complete) b += `<span class="badge b-done">✓ ${m.bestScore}/${m.maxPoints}</span> `;
  else if (m.bestScore) b += `<span class="badge b-busy">${m.bestScore}/${m.maxPoints}</span> `;
  if (m.hasLab) b += `<span class="badge b-run" style="background:none;border:1px solid var(--border2);color:var(--fg-mid)">lab</span> `;
  if (m.hasWorksheets) b += `<span class="badge b-file" style="background:none;border:1px solid var(--border2);color:var(--fg-mid)">deliverable</span> `;
  return b;
}

/* ---------- views ---------- */
function vDashboard() {
  setActive("dashboard"); crumb([{ t: "Dashboard" }]);
  const done = BOOT.summary.labsComplete, total = BOOT.summary.totalLabs;
  const pct = total ? Math.round(100 * done / total) : 0;
  const anyProgress = BOOT.modules.some(m => m.bestScore > 0);
  const next = !anyProgress ? (modById("m0") || BOOT.modules[0])
    : (BOOT.modules.find(m => m.hasLab && !m.complete) || BOOT.modules[0]);
  const days = [...new Set(BOOT.modules.map(m => m.day))].sort();
  const termOk = BOOT.summary.terminal !== false;
  view.innerHTML = `
  <div class="hero">
    <div class="row wrap" style="justify-content:space-between;align-items:center;gap:24px">
      <div style="flex:1;min-width:260px">
        <div class="dim" style="letter-spacing:2px;font-size:11.5px;text-transform:uppercase">Professional Certificate in Cybersecurity, AI &amp; Digital Resilience</div>
        <h1>Welcome${BOOT.student ? ", " + esc(BOOT.student) : ""}</h1>
        <p class="muted" style="max-width:520px">Your course, labs, lessons, tools and deliverables — all in one place, on this machine. Press <span class="kbd">Ctrl K</span> to jump anywhere.</p>
        <div class="row" style="margin-top:10px">
          <input id="nameIn" type="text" placeholder="Enter your name" value="${esc(BOOT.student)}"
            style="background:var(--bg);border:1px solid var(--border2);border-radius:9px;padding:9px 12px;color:var(--fg);font-size:14px">
          <button class="btn sec" id="nameSave">Save</button>
        </div>
      </div>
      <div class="ring" style="--p:${pct}"><div class="hole"><div style="text-align:center"><b>${pct}%</b><br><span>${done}/${total} labs</span></div></div></div>
    </div>
  </div>

  <div class="section-title">Jump back in</div>
  <div class="quick">
    <a id="qResume"><span class="ic">▶</span> ${anyProgress ? "Next lab" : "Start orientation"}: <strong style="margin-left:4px">${next.id.toUpperCase()}</strong></a>
    ${termOk ? `<a onclick="location.hash='terminal'"><span class="ic">▶_</span> Open live terminal</a>` : ""}
    <a onclick="location.hash='labs'"><span class="ic">⌘</span> All labs</a>
    <a onclick="location.hash='materials'"><span class="ic">◉</span> Tools reference</a>
  </div>

  <div class="section-title">Your five days</div>
  <div class="card">
    ${days.map(d => {
      const mods = BOOT.modules.filter(m => m.day === d);
      const grad = mods.filter(m => m.maxPoints > 0);
      const dn = grad.filter(m => m.complete).length;
      const dp = grad.length ? Math.round(100 * dn / grad.length) : 0;
      return `<div class="dayrow">
        <div class="daynum">D${d}</div>
        <div style="flex:1;min-width:0">
          <div class="row" style="justify-content:space-between"><strong style="font-size:14px">${esc(BOOT.dayTitles[d] || ("Day " + d))}</strong>
            <span class="dim" style="font-size:12.5px">${grad.length ? dn + "/" + grad.length + " labs" : mods.length + " sessions"}</span></div>
          <div class="bar"><i style="width:${dp}%"></i></div>
        </div>
        <a class="ghost" data-day="${d}">Open</a>
      </div>`;
    }).join("")}
  </div>`;
  $("#nameSave").onclick = saveName;
  $("#nameIn").addEventListener("keydown", e => { if (e.key === "Enter") saveName(); });
  $("#qResume").onclick = () => { location.hash = (next.hasLab ? "labs/" : "course/") + next.id; };
  view.querySelectorAll("[data-day]").forEach(c => c.onclick = () => { location.hash = "course"; });
}
async function saveName() {
  const name = $("#nameIn").value.trim();
  try { const r = await api("/api/student", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ name }) }); BOOT.student = r.student; updateChrome(); toast("Saved"); } catch (e) { toast(e.message); }
}

function vCourse() {
  setActive("course"); crumb([{ t: "Course" }]);
  const days = [...new Set(BOOT.modules.map(m => m.day))].sort();
  view.innerHTML = days.map(d => `
    <div class="section-title">Day ${d} — ${esc(BOOT.dayTitles[d] || "")}</div>
    <div class="grid cards-2">
      ${BOOT.modules.filter(m => m.day === d).map(m => `
        <div class="card click" data-mid="${m.id}">
          <div class="row" style="justify-content:space-between;align-items:flex-start">
            <div><strong>${m.id.toUpperCase()}</strong> — ${esc(m.title)}</div>
          </div>
          <div style="margin-top:10px">${modBadges(m) || '<span class="dim">lesson</span>'}</div>
        </div>`).join("")}
    </div>`).join("");
  view.querySelectorAll("[data-mid]").forEach(c => c.onclick = () => { location.hash = "course/" + c.dataset.mid; });
}

async function vModule(mid) {
  const m = modById(mid); if (!m) { location.hash = "course"; return; }
  setActive("course"); crumb([{ t: "Course", href: "#course" }, { t: m.id.toUpperCase() }]);
  view.innerHTML = `<div class="loading">Loading ${esc(m.id.toUpperCase())}…</div>`;
  let lesson = { html: "<p class='dim'>No lesson for this module.</p>", title: m.title };
  try { lesson = await api("/api/lesson/" + mid); } catch (e) {}
  let sheets = { sheets: [] };
  if (m.hasWorksheets) { try { sheets = await api("/api/worksheets/" + mid); } catch (e) {} }
  view.innerHTML = `
    <div class="row wrap" style="justify-content:space-between;margin-bottom:6px">
      <div></div>
      ${m.hasLab ? `<button class="btn" id="toLab">⌘ Open the ${m.id.toUpperCase()} lab →</button>` : ""}
    </div>
    <div class="content">${lesson.html}</div>
    ${sheets.sheets.length ? `<div class="section-title">Deliverable templates</div>
      ${sheets.sheets.map(s => `<details><summary>📝 ${esc(s.name)}</summary><div class="inner content">${s.html}</div></details>`).join("")}
      <p class="dim">Get editable copies in your terminal: <code>labctl worksheet ${mid}</code></p>` : ""}
    <div class="section-title">My notes</div>
    <div class="notes panel">
      <textarea id="noteBox" placeholder="Jot your findings, commands, and answers for ${mid.toUpperCase()} here — saved automatically in this browser."></textarea>
      <div class="row" style="justify-content:space-between;margin-top:8px">
        <span class="dim" id="noteState">Saved locally on this device.</span>
        <button class="ghost" id="noteClear">Clear</button>
      </div>
    </div>`;
  if (m.hasLab) $("#toLab").onclick = () => { location.hash = "labs/" + mid; };
  const box = $("#noteBox"), key = "caic_notes_" + mid, st = $("#noteState");
  try { box.value = localStorage.getItem(key) || ""; } catch (e) {}
  let tmr = null;
  box.addEventListener("input", () => {
    st.className = "dim"; st.textContent = "Saving…";
    clearTimeout(tmr);
    tmr = setTimeout(() => { try { localStorage.setItem(key, box.value); st.className = "saved"; st.textContent = "✓ Saved"; } catch (e) { st.textContent = "Could not save"; } }, 400);
  });
  $("#noteClear").onclick = () => { box.value = ""; try { localStorage.removeItem(key); } catch (e) {} st.textContent = "Cleared."; };
}

async function vLabs() {
  setActive("labs"); crumb([{ t: "Labs" }]);
  const labMods = BOOT.modules.filter(m => m.hasLab);
  view.innerHTML = `<p class="muted">Launch isolated practice targets and get graded — all from here. Targets run only on your machine.</p>
    <div class="grid cards-2" id="labGrid">${labMods.map(m => `
      <div class="card click" data-mid="${m.id}">
        <div class="row" style="justify-content:space-between">
          <strong>${m.id.toUpperCase()} — ${esc(m.title)}</strong>
          <span class="badge b-stop" id="st-${m.id}">…</span>
        </div>
        <div class="dim" style="margin-top:8px">Day ${m.day}</div>
      </div>`).join("")}</div>`;
  view.querySelectorAll("[data-mid]").forEach(c => c.onclick = () => { location.hash = "labs/" + c.dataset.mid; });
  // lazy status badges
  labMods.forEach(async m => {
    try { const s = await api("/api/lab/" + m.id + "/status"); const el = $("#st-" + m.id);
      if (s.complete) { el.className = "badge b-done"; el.textContent = "✓ complete"; }
      else if (s.busy) { el.className = "badge b-busy"; el.textContent = s.op + "…"; }
      else if (!s.hasTargets) { el.className = "badge b-file"; el.textContent = "file-based"; }
      else if (s.running) { el.className = "badge b-run"; el.textContent = "● running"; }
      else { el.className = "badge b-stop"; el.textContent = "○ stopped"; }
    } catch (e) {}
  });
}

async function vLab(id) {
  setActive("labs"); crumb([{ t: "Labs", href: "#labs" }, { t: id.toUpperCase() }]);
  view.innerHTML = `<div class="loading">Loading ${esc(id.toUpperCase())}…</div>`;
  let d; try { d = await api("/api/lab/" + id); } catch (e) { view.innerHTML = `<div class="card">${esc(e.message)}</div>`; return; }
  const targetsHtml = d.targets.length ? `<table class="targets"><thead><tr><th>Host</th><th>IP</th><th>Role</th></tr></thead><tbody>
    ${d.targets.map(t => `<tr><td>${esc(t.name)}</td><td class="ipcode">${esc(t.ip)}</td><td class="muted">${esc(t.role)}</td></tr>`).join("")}</tbody></table>` : "";
  const checksHtml = d.checks.map((c, i) => `
    <div class="check" id="chk-${c.id}" data-type="${c.type}">
      <div class="q">${i + 1}. ${esc(c.prompt)}</div>
      ${c.type === "script" ? `<div class="dim">Automatic check — run the lab, then press Verify.</div>`
        : `<input type="text" id="in-${c.id}" placeholder="your answer" autocomplete="off">`}
      ${c.hint ? `<a class="hintbtn" data-h="${c.id}">Show hint</a><div class="hint" id="hint-${c.id}" style="display:none">💡 ${esc(c.hint)}</div>` : ""}
    </div>`).join("");

  view.innerHTML = `
  <div class="split">
    <div>
      <div class="safety">⚠ Scan or attack <strong>only</strong> the target IPs listed here (on <code>${esc(d.subnet || "your machine")}</code>). Using these tools elsewhere is illegal (Act 1038).</div>
      ${d.hasTargets ? `<div class="section-title">Targets</div>${targetsHtml}` : `<div class="section-title">Evidence</div><p class="muted">File-based lab — the materials are in the lab folder's <code>assets/</code>. No targets to launch.</p>`}
      <div class="section-title">Briefing</div>
      <div class="content">${d.briefingHtml || "<p class='dim'>No briefing.</p>"}</div>
    </div>
    <div>
      <div class="panel" id="ctrl">
        <h3>${d.module} control</h3>
        <div id="statusLine" class="row" style="margin-bottom:10px"><span class="badge b-stop">…</span></div>
        ${d.hasTargets ? `<div class="row wrap">
          <button class="btn" id="btnStart">▶ Start</button>
          <button class="btn sec" id="btnStop">■ Stop</button>
          <button class="btn sec" id="btnReset">↻ Reset</button></div>
          <div id="svcList" class="dim" style="margin-top:10px;font-size:12.5px"></div>` : `<div class="dim">No targets — go straight to Verify when you've worked the evidence.</div>`}
      </div>
      <div class="panel" style="margin-top:16px">
        <h3>Verify your findings</h3>
        ${checksHtml || "<div class='dim'>No checks for this lab.</div>"}
        <div class="scorebar"><div class="bar"><i id="scoreFill" style="width:${d.maxPoints ? Math.round(100 * d.bestScore / d.maxPoints) : 0}%"></i></div>
          <strong id="scoreTxt">${d.bestScore}/${d.maxPoints}</strong></div>
        <button class="btn" id="btnVerify" style="width:100%">Submit &amp; grade</button>
      </div>
      <div class="panel" style="margin-top:16px">
        <h3>Prefer the terminal?</h3>
        <div class="cmdline"><code>labctl start ${id}</code><button data-c="labctl start ${id}">copy</button></div>
        <div class="cmdline"><code>labctl verify ${id}</code><button data-c="labctl verify ${id}">copy</button></div>
      </div>
    </div>
  </div>`;

  view.querySelectorAll(".hintbtn").forEach(a => a.onclick = () => { const h = $("#hint-" + a.dataset.h); h.style.display = h.style.display === "none" ? "block" : "none"; });
  view.querySelectorAll(".cmdline button").forEach(b => b.onclick = () => copy(b.dataset.c));
  if (d.hasTargets) {
    $("#btnStart").onclick = () => labOp(id, "start");
    $("#btnStop").onclick = () => labOp(id, "stop");
    $("#btnReset").onclick = () => labOp(id, "reset");
  }
  $("#btnVerify").onclick = () => verifyLab(id, d);
  renderRuntime(await api("/api/lab/" + id + "/status"));
  if (d.hasTargets) startPoll(id);
}

function renderRuntime(s) {
  const line = $("#statusLine"); if (!line) return;
  let badge;
  if (s.busy) badge = `<span class="badge b-busy"><span class="spin"></span> ${s.op}…</span>`;
  else if (!s.hasTargets) badge = `<span class="badge b-file">file-based</span>`;
  else if (s.running) badge = `<span class="badge b-run">● running</span>`;
  else badge = `<span class="badge b-stop">○ stopped</span>`;
  if (s.complete) badge += ` <span class="badge b-done">✓ complete</span>`;
  line.innerHTML = badge + (s.error ? ` <span class="dim" style="color:var(--red)">${esc(s.error)}</span>` : "");
  const sv = $("#svcList"); if (sv) sv.textContent = s.services && s.services.length ? "Up: " + s.services.join(", ") : "";
  const bs = $("#btnStart"), bt = $("#btnStop"), br = $("#btnReset");
  if (bs) { bs.disabled = s.busy || s.running; bt.disabled = s.busy || !s.running; br.disabled = s.busy; }
}
async function labOp(id, op) {
  try { await api("/api/lab/" + id + "/" + op, { method: "POST" }); toast(op === "start" ? "Starting targets…" : op === "stop" ? "Stopping…" : "Resetting…"); renderRuntime({ hasTargets: true, busy: true, op }); startPoll(id); }
  catch (e) { toast(e.message); }
}
function startPoll(id) {
  clearPoll();
  POLL = setInterval(async () => {
    try { const s = await api("/api/lab/" + id + "/status"); renderRuntime(s); if (!s.busy) { /* keep light polling while running */ if (!s.running) clearPoll(); } }
    catch (e) { clearPoll(); }
  }, 2000);
}
async function verifyLab(id, d) {
  const answers = {};
  d.checks.forEach(c => { const el = $("#in-" + c.id); if (el) answers[c.id] = el.value; });
  const btn = $("#btnVerify"); btn.disabled = true; btn.textContent = "Grading…";
  try {
    const r = await api("/api/lab/" + id + "/verify", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ answers }) });
    r.results.forEach(res => {
      const box = $("#chk-" + res.id); if (!box) return;
      box.classList.remove("pass", "fail"); box.classList.add(res.passed ? "pass" : "fail");
      let ico = box.querySelector(".result-ico"); if (!ico) { ico = document.createElement("span"); ico.className = "result-ico"; box.querySelector(".q").appendChild(ico); }
      ico.textContent = res.passed ? "✓" : "✗"; ico.style.color = res.passed ? "var(--green)" : "var(--red)";
    });
    const pct = d.maxPoints ? Math.round(100 * r.score / d.maxPoints) : 0;
    $("#scoreFill").style.width = pct + "%"; $("#scoreTxt").textContent = r.score + "/" + r.maxPoints;
    toast(r.complete ? "✓ Lab complete — well done!" : `Scored ${r.score}/${r.maxPoints}`);
    // refresh progress in BOOT
    const mm = modById(id); if (mm) { mm.bestScore = r.bestScore; mm.complete = r.complete; }
    refreshSummary();
  } catch (e) { toast(e.message); }
  btn.disabled = false; btn.textContent = "Submit & grade";
}

function vTerminal() {
  setActive("terminal"); crumb([{ t: "Terminal" }]);
  if (BOOT.summary && BOOT.summary.terminal === false) {
    view.innerHTML = `<div class="card">The live terminal is disabled on this installation.</div>`;
    return;
  }
  if (typeof Terminal === "undefined") {
    view.innerHTML = `<div class="card">Terminal component failed to load (vendor/xterm.js).</div>`;
    return;
  }
  view.innerHTML = `
    <div class="row wrap" style="justify-content:space-between;margin-bottom:10px">
      <div><strong>Live Kali terminal</strong> <span class="dim">— a real shell on this machine, in the lab folder.</span></div>
      <div class="row"><span class="badge b-stop" id="termStatus">connecting…</span>
        <button class="ghost" id="termReconnect">Reconnect</button></div>
    </div>
    <div class="safety">⚠ This is your real machine, with your real privileges. The rules still apply: only scan or attack the <code>10.13.x.x</code> lab targets.</div>
    <div id="termwrap"></div>
    <p class="dim">New here? Run <code>./labctl learn m0</code> for the command-line primer, or <code>./labctl list</code> to see the labs.</p>`;
  connectTerminal();
  $("#termReconnect").onclick = () => { cleanupTerm(); connectTerminal(); };
}
function connectTerminal() {
  const wrap = $("#termwrap"); if (!wrap) return;
  wrap.innerHTML = "";
  const term = new Terminal({
    cursorBlink: true, fontSize: 14, scrollback: 5000,
    fontFamily: 'SFMono-Regular,Consolas,"Liberation Mono",monospace',
    theme: { background: "#0a0812", foreground: "#e6e2f5", cursor: "#9b6dff",
             selectionBackground: "#3a3158" },
  });
  const fit = new FitAddon.FitAddon();
  term.loadAddon(fit); term.open(wrap); try { fit.fit(); } catch (e) {}
  TERM = term; TFIT = fit;
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const ws = new WebSocket(proto + "://" + location.host + "/ws/terminal");
  ws.binaryType = "arraybuffer"; TWS = ws;
  const status = $("#termStatus");
  const sendResize = () => { if (ws.readyState === 1) ws.send(JSON.stringify({ t: "resize", cols: term.cols, rows: term.rows })); };
  ws.onopen = () => { if (status) { status.className = "badge b-run"; status.textContent = "● connected"; } sendResize(); term.focus(); };
  ws.onmessage = e => { if (typeof e.data === "string") term.write(e.data); else term.write(new Uint8Array(e.data)); };
  ws.onclose = () => { if (status) { status.className = "badge b-stop"; status.textContent = "○ disconnected"; } try { term.write("\r\n\x1b[90m[session ended — press Reconnect]\x1b[0m\r\n"); } catch (e) {} };
  ws.onerror = () => { if (status) { status.className = "badge b-busy"; status.textContent = "error"; } };
  term.onData(d => { if (ws.readyState === 1) ws.send(JSON.stringify({ t: "data", d })); });
  TRESIZE = () => { try { fit.fit(); sendResize(); } catch (e) {} };
  window.addEventListener("resize", TRESIZE);
}

function toolDetail(t) {
  const cmds = (t.commands || []).map(c =>
    `<div class="cmdline"><code>${esc(c.cmd)}</code><span class="dim" style="flex:2">${esc(c.desc)}</span><button data-c="${esc(c.cmd)}">copy</button></div>`).join("");
  const tips = (t.tips || []).map(x => `<li>${esc(x)}</li>`).join("");
  return `<div class="tool-detail">
    <p>${esc(t.desc || "")}</p>
    ${t.usage ? `<h4>How to use it</h4><p class="muted">${esc(t.usage)}</p>` : ""}
    ${cmds ? `<h4>Key commands</h4>${cmds}` : ""}
    ${tips ? `<h4>Practitioner tips</h4><ul>${tips}</ul>` : ""}
    ${t.modules ? `<p class="dim" style="margin-top:10px">Used in: ${esc(t.modules)}</p>` : ""}
  </div>`;
}
function vMaterials() {
  setActive("materials"); crumb([{ t: "Tools & Materials" }]);
  const cats = [...new Set(BOOT.tools.map(t => t.cat))];
  view.innerHTML = `
  <p class="muted">The real toolkit — what each tool is, how to use it, and the commands that matter. Everything here you can run right now in the <a onclick="location.hash='terminal'">Terminal</a>.</p>
  <input id="toolSearch" placeholder="Search tools (name, category, command)…"
    style="width:100%;padding:10px 13px;margin:6px 0 14px;background:var(--panel2);border:1px solid var(--border2);border-radius:9px;color:var(--fg);font-size:14px">
  <div id="toolList">
    ${BOOT.tools.map(t => `
      <details class="toolrow" data-hay="${esc((t.name + " " + t.cat + " " + (t.desc||"") + " " + (t.commands||[]).map(c=>c.cmd).join(" ")).toLowerCase())}">
        <summary><strong>${esc(t.name)}</strong><span class="tool-cat">${esc(t.cat)}</span></summary>
        <div class="inner">${toolDetail(t)}</div>
      </details>`).join("")}
  </div>

  <div class="section-title">Deliverable templates</div>
  <div class="grid cards-3">
    ${BOOT.modules.filter(m => m.hasWorksheets).map(m => `<div class="card click" data-mid="${m.id}">
      <strong>${m.id.toUpperCase()}</strong><div class="dim" style="font-size:13px;margin-top:4px">${m.worksheets.length} template(s)</div>
      <div class="muted" style="font-size:12.5px;margin-top:6px">${m.worksheets.map(esc).join("<br>")}</div></div>`).join("")}
  </div>
  <p class="dim">Open a template in the Course view, or copy editable files with <code>labctl worksheet m2</code>.</p>`;
  view.querySelectorAll(".cmdline button").forEach(b => b.onclick = () => copy(b.dataset.c));
  view.querySelectorAll("[data-mid]").forEach(c => c.onclick = () => { location.hash = "course/" + c.dataset.mid; });
  const search = $("#toolSearch");
  if (search) search.oninput = () => {
    const q = search.value.toLowerCase();
    view.querySelectorAll(".toolrow").forEach(r => { r.style.display = r.dataset.hay.includes(q) ? "block" : "none"; });
  };
}

function vCommands() {
  setActive("commands"); crumb([{ t: "Commands" }]);
  const groups = [...new Set(BOOT.commands.map(c => c.group))];
  view.innerHTML = `<p class="muted">Everything the lab is also drivable from your terminal. Click a command to copy it.</p>` +
    groups.map(g => `<div class="section-title">${esc(g)}</div>
      ${BOOT.commands.filter(c => c.group === g).map(c => `
        <div class="cmdline"><code>${esc(c.cmd)}</code><span class="dim" style="flex:2">${esc(c.desc)}</span><button data-c="${esc(c.cmd)}">copy</button></div>`).join("")}`).join("");
  view.querySelectorAll(".cmdline button").forEach(b => b.onclick = () => copy(b.dataset.c));
}

function vProgress() {
  setActive("progress"); crumb([{ t: "Progress" }]);
  view.innerHTML = `
  <div class="row" style="gap:26px;margin-bottom:10px">
    <div class="stat"><span class="n">${BOOT.summary.labsComplete}/${BOOT.summary.totalLabs}</span><span class="l">labs completed</span></div>
    <div class="stat"><span class="n">${BOOT.student ? esc(BOOT.student) : "—"}</span><span class="l">student</span></div>
  </div>
  <div class="card" style="padding:0;overflow:auto"><table>
    <thead><tr><th>Module</th><th>Day</th><th>Title</th><th>Score</th><th>Status</th></tr></thead><tbody>
    ${BOOT.modules.map(m => `<tr>
      <td><strong>${m.id.toUpperCase()}</strong></td><td>${m.day}</td><td class="muted">${esc(m.title)}</td>
      <td>${m.maxPoints ? m.bestScore + "/" + m.maxPoints : "—"}</td>
      <td>${m.complete ? '<span class="badge b-done">✓ complete</span>' : m.bestScore ? '<span class="badge b-busy">in progress</span>' : '<span class="dim">—</span>'}</td>
    </tr>`).join("")}
    </tbody></table></div>`;
}

/* ---------- refresh summary after grading ---------- */
function refreshSummary() {
  BOOT.summary.labsComplete = BOOT.modules.filter(m => m.complete).length;
}

/* ---------- router ---------- */
function parseHash() { const h = (location.hash || "#dashboard").slice(1).split("/"); return { v: h[0] || "dashboard", arg: h[1] }; }
async function route() {
  clearPoll();
  cleanupTerm();
  $("#app").classList.remove("nav-open");
  const { v, arg } = parseHash();
  try {
    if (v === "dashboard") return vDashboard();
    if (v === "course") return arg ? vModule(arg) : vCourse();
    if (v === "labs") return arg ? vLab(arg) : vLabs();
    if (v === "terminal") return vTerminal();
    if (v === "materials") return vMaterials();
    if (v === "commands") return vCommands();
    if (v === "progress") return vProgress();
    vDashboard();
  } catch (e) { view.innerHTML = `<div class="card">${esc(e.message)}</div>`; }
}
window.addEventListener("hashchange", route);

/* ---------- boot ---------- */
(async function () {
  initTheme();
  try { BOOT = await api("/api/bootstrap"); } catch (e) { view.innerHTML = `<div class="card">Could not reach the lab backend: ${esc(e.message)}<br><span class="dim">Start it with <code>./start.sh</code> or <code>labctl serve</code>.</span></div>`; return; }
  updateChrome();
  if (!location.hash) location.hash = "dashboard";
  route();
})();
