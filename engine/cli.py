"""labctl command-line interface. `labctl <command> [lab]`."""
from __future__ import annotations

import argparse
import sys

from . import __version__, dockerctl, state, ui
from .course import COURSE_MAP
from .manifest import Lab, ManifestError, discover_labs, load_one


# ─────────────────────────────── helpers ────────────────────────────────

def _require_docker() -> bool:
    pf = dockerctl.preflight()
    if pf.ok:
        return True
    ui.error("Docker is not ready.")
    if not pf.docker_installed:
        ui.info("Install it:  sudo apt update && sudo apt install -y docker.io docker-compose-v2")
    elif pf.needs_sudo:
        ui.info("Your user can't reach the Docker daemon. Either:")
        ui.info("  • add yourself to the group:  sudo usermod -aG docker $USER   (then log out/in)")
        ui.info("  • or run labctl with sudo:     sudo labctl <command>")
    elif not pf.daemon_up:
        ui.info("Start the daemon:  sudo systemctl start docker")
        if pf.detail:
            ui.dim("  " + pf.detail)
    elif not pf.compose_v2:
        ui.info("Install compose v2:  sudo apt install -y docker-compose-v2")
    return False


def _status_word(lab: Lab) -> str:
    if not lab.has_targets:
        return f"{ui.CYAN}file-based{ui.RESET}"
    try:
        running = dockerctl.is_running(lab)
    except Exception:
        running = False
    if running:
        return f"{ui.GREEN}● running{ui.RESET}"
    return f"{ui.GREY}○ stopped{ui.RESET}"


def _progress_word(lab: Lab) -> str:
    entry = state.lab_status(lab.id)
    best = entry.get("best_score", 0)
    if lab.max_points and best >= lab.max_points:
        return f"{ui.GREEN}✔ complete{ui.RESET}"
    if best > 0:
        return f"{ui.YELLOW}{best}/{lab.max_points}{ui.RESET}"
    return f"{ui.GREY}—{ui.RESET}"


# ─────────────────────────────── commands ───────────────────────────────

def cmd_list(_args) -> int:
    labs = discover_labs()
    if not labs:
        ui.warn("No labs found under labs/.")
        return 1
    ui.banner("KAIPTC CAIC CyberLab — available labs")
    rows = []
    for lab in labs:
        rows.append([
            f"{ui.BOLD}{lab.id}{ui.RESET}",
            f"D{lab.day}",
            lab.title,
            ", ".join(lab.tools) or "—",
            _status_word(lab),
            _progress_word(lab),
        ])
    ui.table(rows, ["LAB", "DAY", "TITLE", "TOOLS", "TARGETS", "PROGRESS"])
    print()
    ui.dim("  labctl start <lab>   bring up the isolated targets + briefing")
    ui.dim("  labctl verify <lab>  submit your findings for grading")
    return 0


def cmd_info(args) -> int:
    lab = load_one(args.lab)
    ui.banner(f"{lab.module} — {lab.title}")
    ui.header("Briefing")
    if lab.objective:
        print(f"  {lab.objective}\n")
    if lab.briefing_file:
        print(lab.briefing_file.read_text(encoding="utf-8"))
    else:
        ui.dim("  (no briefing.md for this lab)")
    if lab.targets:
        ui.header("Targets (isolated — never scan outside this subnet)")
        ui.info(f"network {lab.network_name}  subnet {lab.subnet}")
        rows = [[t.name, t.ip, t.role] for t in lab.targets]
        ui.table(rows, ["HOST", "IP", "ROLE"])
    ui.header("When you're ready")
    print(f"  {ui.cmd('labctl start ' + lab.id)}")
    print(f"  {ui.cmd('labctl verify ' + lab.id)}")
    return 0


def cmd_start(args) -> int:
    lab = load_one(args.lab)
    if not lab.has_targets:
        # File-based lab: no containers, just point the student at the evidence.
        from . import seed
        vals = seed.compute(lab)
        seed.prepare(lab, vals)   # personalise the evidence files for this student
        ui.header(f"{lab.module}: {lab.title}")
        ui.ok("This is a file-based lab — no targets to launch.")
        if vals:
            ui.info("Evidence personalised for you — your answers differ from others'.")
        assets = lab.directory / "assets"
        if assets.is_dir():
            files = [p for p in sorted(assets.iterdir())
                     if p.is_file() and not p.name.startswith(".")
                     and not p.name.endswith(".py")]
            if files:
                ui.info("Evidence provided:")
                for p in files:
                    print(f"      {ui.GREEN}{p.relative_to(lab.directory)}{ui.RESET}")
        state.mark_started(lab.id)
        print(f"\n  Read the mission:  {ui.cmd('labctl info ' + lab.id)}")
        print(f"  Grade your work:   {ui.cmd('labctl verify ' + lab.id)}")
        return 0
    if not _require_docker():
        return 2
    from . import seed
    vals = seed.compute(lab)
    seed.prepare(lab, vals)   # render assets/*.tmpl + run generators for this student
    ui.header(f"Starting {lab.module}: {lab.title}")
    ui.info(f"Bringing up isolated targets on {lab.subnet} (project {lab.project})…")
    if vals:
        ui.info("Targets personalised for you — your flags/answers differ from others'.")
    try:
        dockerctl.up(lab, env=seed.env_for(vals))
    except dockerctl.DockerError as exc:
        ui.error(str(exc))
        return 2
    state.mark_started(lab.id)
    svcs = dockerctl.running_services(lab)
    ui.ok(f"{len(svcs)} target(s) up.")
    # Wait until the services actually accept connections (avoids a confusing
    # first verify while a container is still booting its app).
    if lab.ready:
        ui.info("Waiting for services to accept connections…")
        all_ready, down = dockerctl.wait_ready(lab)
        if all_ready:
            ui.ok("All services ready.")
        else:
            ui.warn(f"Still starting: {', '.join(down)} — give it a few more seconds.")
    if lab.targets:
        rows = [[t.name, t.ip, t.role] for t in lab.targets]
        ui.table(rows, ["HOST", "IP", "ROLE"])
    print()
    ui.warn("SAFETY: only scan/attack the IPs above. Nothing else is authorised.")
    print(f"\n  Read the mission:  {ui.cmd('labctl info ' + lab.id)}")
    print(f"  Grade your work:   {ui.cmd('labctl verify ' + lab.id)}")
    print(f"  Clean reset:       {ui.cmd('labctl reset ' + lab.id)}")
    return 0


def cmd_status(args) -> int:
    labs = [load_one(args.lab)] if args.lab else discover_labs()
    if any(l.has_targets for l in labs) and not _require_docker():
        return 2
    rows = []
    for lab in labs:
        if not lab.has_targets:
            rows.append([f"{ui.BOLD}{lab.id}{ui.RESET}", _status_word(lab), "—", "—"])
            continue
        svcs = dockerctl.running_services(lab)
        names = ", ".join(sorted(s.get("Service", s.get("Name", "?")) for s in svcs)) or "—"
        rows.append([f"{ui.BOLD}{lab.id}{ui.RESET}", _status_word(lab),
                     str(len(svcs)), names])
    ui.header("Lab target status")
    ui.table(rows, ["LAB", "STATE", "UP", "SERVICES"])
    return 0


def cmd_verify(args) -> int:
    from . import verify
    lab = load_one(args.lab)
    running = False
    if lab.has_targets:
        try:
            running = dockerctl.is_running(lab)
        except Exception:
            running = False
    if lab.has_targets and not running and any(c.type == "script" for c in lab.checks):
        ui.warn(f"Targets for {lab.id} are not running — start them first: labctl start {lab.id}")
    verify.interactive(lab)
    return 0


def cmd_reset(args) -> int:
    lab = load_one(args.lab)
    if not lab.has_targets:
        ui.info(f"{lab.id} is file-based — nothing to reset (evidence is read-only).")
        return 0
    if not _require_docker():
        return 2
    ui.header(f"Resetting {lab.module} to a clean state")
    try:
        dockerctl.restart(lab)
    except dockerctl.DockerError as exc:
        ui.error(str(exc))
        return 2
    ui.ok("Targets destroyed and rebuilt fresh.")
    return 0


def cmd_stop(args) -> int:
    labs = [load_one(args.lab)] if args.lab else discover_labs()
    labs = [l for l in labs if l.has_targets]
    if not labs:
        ui.info("No container-based labs to stop.")
        return 0
    if not _require_docker():
        return 2
    for lab in labs:
        try:
            if dockerctl.is_running(lab):
                dockerctl.down(lab)
                state.mark_stopped(lab.id)
                ui.ok(f"{lab.id} stopped.")
        except dockerctl.DockerError as exc:
            ui.error(f"{lab.id}: {exc}")
    return 0


def cmd_progress(_args) -> int:
    labs = discover_labs()
    who = state.get_student() or "(unnamed student)"
    ui.banner(f"Progress — {who}")
    done = 0
    rows = []
    for lab in labs:
        entry = state.lab_status(lab.id)
        best = entry.get("best_score", 0)
        complete = lab.max_points and best >= lab.max_points
        done += 1 if complete else 0
        rows.append([f"{ui.BOLD}{lab.id}{ui.RESET}", f"D{lab.day}", lab.title,
                     _progress_word(lab), entry.get("last_attempt", "—") or "—"])
    ui.table(rows, ["LAB", "DAY", "TITLE", "SCORE", "LAST ATTEMPT"])
    print()
    total = len(labs)
    pct = round(100 * done / total) if total else 0
    ui.info(f"{done}/{total} labs complete ({pct}%).")
    # Composite course grade (labs + quizzes + exam).
    try:
        from . import grade as grading
        g = grading.compute()
        c = g["components"]
        print()
        ui.dim(f"  Course grade: labs {c['labs']['pct']}% · "
               f"quizzes {c['quizzes']['pct']}% · exam {c['exam']['pct']}% "
               f"→ overall {g['overall']}% (pass {g['passMark']}%)")
        ui.dim("  Full breakdown: labctl grade")
    except Exception:
        pass
    return 0


def cmd_doctor(_args) -> int:
    ui.banner("labctl doctor — environment check")
    pf = dockerctl.preflight()
    (ui.ok if pf.docker_installed else ui.fail)("docker binary present")
    (ui.ok if pf.daemon_up else ui.fail)(
        "docker daemon reachable" + (f" ({pf.detail})" if pf.detail else ""))
    (ui.ok if pf.compose_v2 else ui.fail)("docker compose v2 present")
    if pf.needs_sudo:
        ui.warn("Add your user to the 'docker' group or run labctl with sudo.")
    labs = discover_labs()
    ui.info(f"{len(labs)} lab(s) discovered and valid.")
    import shutil
    for t in ("nmap", "wireshark", "tcpdump", "nikto", "hydra", "john", "autopsy"):
        (ui.ok if shutil.which(t) else ui.warn)(
            f"{t} " + ("found" if shutil.which(t) else "not on PATH (install if the lab needs it)"))
    return 0 if pf.ok else 1


def cmd_whoami(args) -> int:
    if args.name:
        state.set_student(" ".join(args.name))
        ui.ok(f"Student name set to: {state.get_student()}")
    else:
        ui.info(f"Student: {state.get_student() or '(not set — labctl whoami <your name>)'}")
    return 0


def cmd_learn(args) -> int:
    from . import mdrender, paths
    if not args.module:
        ui.banner("CAIC CyberLab — course lessons")
        rows = []
        for mid, day, title, has_lab in COURSE_MAP:
            lesson = paths.LESSONS_DIR / f"{mid}.md"
            avail = f"{ui.GREEN}✔{ui.RESET}" if lesson.is_file() else f"{ui.GREY}—{ui.RESET}"
            lab = f"{ui.CYAN}start {mid}{ui.RESET}" if has_lab else f"{ui.GREY}—{ui.RESET}"
            has_ws = any(paths.WORKSHEETS_DIR.glob(f"{mid}-*.md"))
            ws = f"{ui.GREEN}✔{ui.RESET}" if has_ws else f"{ui.GREY}—{ui.RESET}"
            rows.append([f"{ui.BOLD}{mid}{ui.RESET}", f"D{day}", title, avail, lab, ws])
        ui.table(rows, ["MOD", "DAY", "TITLE", "LESSON", "LAB", "DELIV."])
        print()
        ui.dim("  labctl learn m1       read a module's full lesson")
        ui.dim("  labctl worksheet m2   get a module's deliverable template")
        return 0
    mid = args.module.lower()
    lesson = paths.LESSONS_DIR / f"{mid}.md"
    if not lesson.is_file():
        ui.error(f"no lesson for '{mid}' yet (try: labctl learn)")
        return 1
    mdrender.render(lesson.read_text(encoding="utf-8"))
    print()
    has_lab = next((hl for m, _, _, hl in COURSE_MAP if m == mid), False)
    if has_lab:
        ui.info(f"Now do it for real:  {ui.cmd('labctl start ' + mid)}")
    return 0


def cmd_worksheet(args) -> int:
    """List deliverable templates, or copy a module's templates into the
    student's own working folder so they can fill them in."""
    import shutil
    from . import paths
    wd = paths.WORKSHEETS_DIR
    if not wd.is_dir():
        ui.error("no worksheets/ directory found")
        return 1
    all_sheets = sorted(wd.glob("m*.md"))
    if not args.module:
        ui.banner("CAIC CyberLab — deliverable templates")
        by_mod: dict[str, list[str]] = {}
        for p in all_sheets:
            mid = p.name.split("-", 1)[0]
            by_mod.setdefault(mid, []).append(p.name)
        rows = [[f"{ui.BOLD}{m}{ui.RESET}", ", ".join(n)] for m, n in
                sorted(by_mod.items(), key=lambda kv: int(kv[0][1:]))]
        ui.table(rows, ["MODULE", "TEMPLATES"])
        print()
        ui.dim("  labctl worksheet m2   copy a module's templates to your work folder")
        return 0
    mid = args.module.lower()
    sheets = [p for p in all_sheets if p.name.split("-", 1)[0] == mid]
    if not sheets:
        ui.error(f"no worksheet for '{mid}' (try: labctl worksheet)")
        return 1
    try:
        paths.WORK_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        ui.error(f"cannot create work folder: {exc}")
        return 2
    ui.header(f"Templates for {mid.upper()} → {paths.WORK_DIR}")
    for src in sheets:
        dest = paths.WORK_DIR / src.name
        if dest.exists():
            ui.warn(f"{src.name} already in your work folder — left as-is (your edits kept)")
        else:
            shutil.copy2(src, dest)
            ui.ok(f"copied {src.name}")
    ui.info("Open them in any editor and fill in the [...] placeholders.")
    print(f"  {ui.cmd('cd ' + str(paths.WORK_DIR))}")
    return 0


def cmd_serve(args) -> int:
    """Launch the unified web application (dashboard, course, labs, materials)."""
    import webbrowser
    from . import webapp
    host = "127.0.0.1"
    port = args.port
    httpd = None
    for cand in range(port, port + 12):
        try:
            httpd = webapp.serve(host, cand)
            port = cand
            break
        except OSError:
            continue
    if httpd is None:
        ui.error(f"could not bind a port near {args.port}")
        return 2
    url = f"http://{host}:{port}/"
    ui.banner("CAIC CyberLab — web application")
    ui.ok(f"running at {ui.BOLD}{url}{ui.RESET}")
    pf = dockerctl.preflight()
    (ui.ok if pf.ok else ui.warn)(
        "Docker ready — labs can launch from the browser" if pf.ok
        else "Docker not ready — course/lessons work; labs need Docker (labctl doctor)")
    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    ui.dim("  Press Ctrl-C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print()
        ui.info("stopping web server…")
    finally:
        httpd.server_close()   # release the port in this same thread
    return 0


def cmd_quiz(args) -> int:
    from . import quiz
    bank = quiz.load()
    if not args.module:
        ui.banner("Knowledge-check quizzes")
        rows = []
        for mid, day, title, _ in COURSE_MAP:
            if mid not in bank:
                continue
            st = state.quiz_status(mid)
            n = len(bank[mid].get("questions", []))
            score = f"{st.get('best', 0)}/{n}" if st else f"{ui.GREY}—{ui.RESET}"
            rows.append([f"{ui.BOLD}{mid}{ui.RESET}", f"D{day}", bank[mid].get("title", title), score])
        ui.table(rows, ["QUIZ", "DAY", "TITLE", "BEST"])
        print()
        ui.dim("  labctl quiz m1    take a module quiz")
        ui.dim("  labctl exam       the final exam    ·    labctl diagnostic   baseline")
        return 0
    quiz.interactive(args.module.lower())
    return 0


def cmd_exam(_args) -> int:
    from . import quiz
    quiz.interactive("final")
    return 0


def cmd_diagnostic(_args) -> int:
    from . import quiz
    quiz.interactive("baseline")
    return 0


def cmd_grade(_args) -> int:
    from . import grade
    g = grade.compute()
    ui.banner(f"Course grade — {g['student'] or '(unnamed)'}")
    rows = []
    for name, c in g["components"].items():
        rows.append([name.capitalize(), f"{int(c['weight']*100)}%",
                     f"{c['got']}/{c['total']}", f"{c['pct']}%"])
    ui.table(rows, ["COMPONENT", "WEIGHT", "RAW", "SCORE"])
    print()
    pct = g["overall"]
    bar = ui.GREEN + "█" * int(pct / 5) + ui.GREY + "░" * (20 - int(pct / 5)) + ui.RESET
    tone = ui.GREEN if g["passed"] else ui.YELLOW
    print(f"  Overall: {bar} {tone}{pct}%{ui.RESET}  (pass mark {g['passMark']}%)")
    if g["passed"]:
        ui.ok("PASS — you have met the certification threshold.")
    else:
        ui.info("Keep going — complete more labs, quizzes and the final exam.")
    return 0


def cmd_prep(args) -> int:
    """Build every lab image up front, so later launches work fully offline.
    Run this ONCE on each machine while internet is available."""
    if not _require_docker():
        return 2
    labs = [load_one(args.lab)] if args.lab else discover_labs()
    container_labs = [l for l in labs if l.has_targets]
    ui.banner("labctl prep — building all lab images for offline use")
    ui.info(f"{len(container_labs)} container-based lab(s) to build. This needs "
            f"internet the first time; afterwards launches are offline.")
    failed = []
    for lab in container_labs:
        ui.header(f"{lab.module}: {lab.title}")
        try:
            dockerctl.build(lab)
            ui.ok(f"{lab.id} images built.")
        except dockerctl.DockerError as exc:
            ui.fail(str(exc))
            failed.append(lab.id)
    print()
    if failed:
        ui.error(f"build failed for: {', '.join(failed)}")
        return 1
    ui.ok("All lab images are built and cached. You can now run offline.")
    return 0


def cmd_reset_progress(args) -> int:
    if not args.yes:
        ui.warn("This erases YOUR saved progress and scores for every lab.")
        try:
            ans = input("  Type 'yes' to confirm: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print(); return 1
        if ans != "yes":
            ui.info("Cancelled — nothing changed.")
            return 0
    if state.clear_progress():
        ui.ok("Progress cleared. Fresh start.")
    else:
        ui.info("No saved progress to clear.")
    return 0


def cmd_report(args) -> int:
    """Facilitator view: aggregate collected student state.json files.
    Point it at a directory containing one or more *.json progress files."""
    import pathlib
    labs = discover_labs()
    lab_ids = [l.id for l in labs]
    maxpts = {l.id: l.max_points for l in labs}
    d = pathlib.Path(args.dir)
    files = sorted(d.glob("*.json")) if d.is_dir() else ([d] if d.is_file() else [])
    if not files:
        ui.error(f"no .json progress files found at {args.dir}")
        return 1
    ui.banner(f"Facilitator report — {len(files)} submission(s)")
    rows = []
    for f in files:
        data = state.load_file(f)
        who = data.get("student") or f.stem
        labs_done = data.get("labs", {})
        done = sum(1 for lid in lab_ids
                   if maxpts.get(lid, 0) and labs_done.get(lid, {}).get("best_score", 0) >= maxpts[lid])
        cells = []
        for lid in lab_ids:
            best = labs_done.get(lid, {}).get("best_score", 0)
            mp = maxpts.get(lid, 0)
            if mp and best >= mp:
                cells.append(f"{ui.GREEN}✔{ui.RESET}")
            elif best > 0:
                cells.append(f"{ui.YELLOW}{best}{ui.RESET}")
            else:
                cells.append(f"{ui.GREY}·{ui.RESET}")
        rows.append([who, f"{done}/{len(lab_ids)}"] + cells)
    ui.table(rows, ["STUDENT", "DONE"] + [l.upper() for l in lab_ids])
    return 0


# ─────────────────────────────── parser ────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="labctl",
        description="KAIPTC CAIC CyberLab — launch and grade isolated hands-on labs.")
    p.add_argument("--version", action="version", version=f"labctl {__version__}")
    sub = p.add_subparsers(dest="command", metavar="<command>")

    def add(name, fn, help_, lab="optional"):
        sp = sub.add_parser(name, help=help_)
        if lab == "required":
            sp.add_argument("lab", help="lab id, e.g. m3")
        elif lab == "optional":
            sp.add_argument("lab", nargs="?", help="lab id (default: all)")
        sp.set_defaults(func=fn)
        return sp

    add("list", cmd_list, "list all labs and their status", lab="none")
    learn = add("learn", cmd_learn, "read a module's full teaching lesson", lab="none")
    learn.add_argument("module", nargs="?", help="module id, e.g. m1 (omit to list)")
    ws = add("worksheet", cmd_worksheet, "get a module's deliverable template(s)", lab="none")
    ws.add_argument("module", nargs="?", help="module id, e.g. m2 (omit to list)")
    qz = add("quiz", cmd_quiz, "take a module knowledge-check quiz", lab="none")
    qz.add_argument("module", nargs="?", help="module id, e.g. m1 (omit to list)")
    add("exam", cmd_exam, "sit the final exam", lab="none")
    add("diagnostic", cmd_diagnostic, "take the (ungraded) baseline diagnostic", lab="none")
    add("grade", cmd_grade, "show your composite course grade + pass status", lab="none")
    add("info", cmd_info, "show a lab's briefing and targets", lab="required")
    add("start", cmd_start, "bring up a lab's isolated targets", lab="required")
    add("status", cmd_status, "show which lab targets are running")
    add("verify", cmd_verify, "submit findings and get graded", lab="required")
    add("reset", cmd_reset, "destroy and rebuild a lab clean", lab="required")
    add("stop", cmd_stop, "stop a lab's targets (or all)")
    srv = add("serve", cmd_serve, "launch the unified web application", lab="none")
    srv.add_argument("--port", type=int, default=8899, help="port (default 8899)")
    srv.add_argument("--no-browser", action="store_true", help="don't open a browser")
    add("prep", cmd_prep, "pre-build all lab images for offline use (run once)")
    add("progress", cmd_progress, "show your overall course progress", lab="none")
    add("doctor", cmd_doctor, "check docker + tools are ready", lab="none")
    who = add("whoami", cmd_whoami, "show/set your student name", lab="none")
    who.add_argument("name", nargs="*", help="set your name")
    rp = add("reset-progress", cmd_reset_progress, "erase your saved scores", lab="none")
    rp.add_argument("--yes", action="store_true", help="skip the confirmation prompt")
    rep = add("report", cmd_report, "facilitator: aggregate student progress files", lab="none")
    rep.add_argument("dir", help="directory of collected *.json progress files")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 0
    try:
        return args.func(args)
    except ManifestError as exc:
        ui.error(str(exc))
        return 1
    except KeyboardInterrupt:
        print()
        return 130


if __name__ == "__main__":
    sys.exit(main())
