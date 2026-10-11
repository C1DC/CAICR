"""Regression tests for the CAIC CyberLab engine and lab artefacts.

Pure stdlib — run with:  python3 -m unittest discover -s tests
(or simply:  python3 tests/test_engine.py)

These do NOT need Docker or Sleuthkit; they check manifest loading, the grading
logic, and that each generated evidence artefact is well-formed.
"""
import base64
import struct
import sys
import tempfile
import unittest
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from engine import manifest, verify  # noqa: E402
from engine.manifest import Check, ManifestError  # noqa: E402


from engine import course  # noqa: E402

LESSON_IDS = [mid for mid, _, _, _ in course.COURSE_MAP]


class TestManifests(unittest.TestCase):
    def test_all_labs_discover_and_validate(self):
        labs = manifest.discover_labs()
        ids = {l.id for l in labs}
        self.assertEqual(ids, {"rt", "js", "m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10"})

    def test_every_lab_has_checks_and_points(self):
        for lab in manifest.discover_labs():
            self.assertTrue(lab.checks, f"{lab.id} has no checks")
            self.assertGreater(lab.max_points, 0, f"{lab.id} has 0 points")

    def test_subnets_are_private(self):
        import ipaddress
        for lab in manifest.discover_labs():
            if lab.subnet:
                self.assertTrue(ipaddress.ip_network(lab.subnet).is_private,
                                f"{lab.id} subnet not private")

    def test_non_private_subnet_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "lab.toml").write_text(
                '[lab]\nid="x"\ntitle="t"\n[network]\nsubnet="8.8.8.0/24"\n')
            with self.assertRaises(ManifestError):
                manifest.load_lab(p)

    def test_file_based_labs_have_no_compose(self):
        byid = {l.id: l for l in manifest.discover_labs()}
        self.assertFalse(byid["m2"].has_targets)
        self.assertFalse(byid["m8"].has_targets)
        self.assertFalse(byid["m9"].has_targets)
        self.assertFalse(byid["m5"].has_targets)
        self.assertFalse(byid["m6"].has_targets)
        self.assertTrue(byid["m3"].has_targets)


class TestGrading(unittest.TestCase):
    def test_numeric_tolerance(self):
        c = Check(id="n", prompt="", type="numeric", answer=4, tolerance=1)
        self.assertTrue(verify.grade_answer(c, "5").passed)
        self.assertTrue(verify.grade_answer(c, "3").passed)
        self.assertFalse(verify.grade_answer(c, "6").passed)
        self.assertFalse(verify.grade_answer(c, "notanumber").passed)

    def test_string_case_space_insensitive(self):
        c = Check(id="s", prompt="", type="string", answer="Return-Path")
        self.assertTrue(verify.grade_answer(c, "  return-path ").passed)
        self.assertFalse(verify.grade_answer(c, "From").passed)

    def test_string_any(self):
        c = Check(id="a", prompt="", type="string_any", accept=["ftp", "file transfer protocol"])
        self.assertTrue(verify.grade_answer(c, "FTP").passed)
        self.assertTrue(verify.grade_answer(c, "File Transfer Protocol").passed)
        self.assertFalse(verify.grade_answer(c, "ssh").passed)


class TestArtefacts(unittest.TestCase):
    LABS = ROOT / "labs"

    def _prepare(self, mid):
        """Generate a lab's (possibly randomized) assets for this test run."""
        from engine import seed, manifest
        lab = manifest.load_one(mid)
        seed.prepare(lab, seed.compute(lab))
        return lab

    def test_m3_pcap_is_valid(self):
        self._prepare("m3")
        data = (self.LABS / "m3-network/assets/network-capture.pcap").read_bytes()
        magic = struct.unpack("<I", data[:4])[0]
        self.assertEqual(magic, 0xA1B2C3D4, "pcap magic wrong")
        self.assertIn(b"USER ", data, "FTP credentials missing from capture")
        self.assertIn(b"\x00\x01\x00\x01", data[:0] + data, "no DNS query in capture")

    def test_m6_image_is_fat16(self):
        self._prepare("m6")
        img = (self.LABS / "m6-forensics/assets/evidence.img").read_bytes()
        self.assertEqual(img[510:512], b"\x55\xAA", "boot signature missing")
        self.assertIn(b"FAT16", img[0:64], "FAT16 id missing from BPB")

    def test_m6_hash_manifest_matches_image(self):
        import hashlib
        self._prepare("m6")
        base = self.LABS / "m6-forensics/assets"
        img = (base / "evidence.img").read_bytes()
        recorded = (base / "evidence.sha256").read_text().split()[0]
        self.assertEqual(hashlib.sha256(img).hexdigest(), recorded)

    def test_m6_artifact_decodes_to_c2(self):
        self._prepare("m6")
        txt = (self.LABS / "m6-forensics/assets/suspicious_artifact.txt").read_text().strip()
        decoded = urllib.parse.unquote(base64.b64decode(txt).decode())
        self.assertIn("http", decoded)
        self.assertIn("/gate.php", decoded)

    def test_m5_email_has_spoof_indicators(self):
        self._prepare("m5")
        eml = (self.LABS / "m5-bec/assets/invoice-change-request.eml").read_text()
        self.assertIn("spf=fail", eml)
        self.assertIn("zenith", eml.lower())           # a zenith look-alike is present
        self.assertIn("Reply-To:", eml)

    def test_answers_in_manifests_are_gradable(self):
        """Every string/numeric check's own answer should grade as correct,
        after resolving any per-student randomized placeholders."""
        from engine import seed
        for lab in manifest.discover_labs():
            vals = seed.compute(lab)
            for c in lab.checks:
                c = seed.resolved_check(c, vals)
                if c.type in ("string", "numeric") and c.answer:
                    out = verify.grade_answer(c, str(c.answer))
                    self.assertTrue(out.passed, f"{lab.id}:{c.id} answer not self-consistent")

    def test_randomization_is_per_student(self):
        """Two different seeds must yield different values for a randomized lab."""
        from engine import seed, state
        lab = manifest.load_one("m1")
        self.assertTrue(lab.randomize, "m1 should be randomized")
        orig = state.get_seed
        try:
            state.get_seed = lambda: 1001
            a = seed.compute(lab)
            state.get_seed = lambda: 2002
            b = seed.compute(lab)
        finally:
            state.get_seed = orig
        self.assertNotEqual(a, b)
        self.assertIn("hidden_host", a)


class TestLessons(unittest.TestCase):
    LESSONS = ROOT / "lessons"

    def test_every_course_module_has_a_lesson(self):
        for mid in LESSON_IDS:
            self.assertTrue((self.LESSONS / f"{mid}.md").is_file(),
                            f"lessons/{mid}.md missing")

    def test_lessons_render_without_error(self):
        import io
        import contextlib
        from engine import mdrender
        for mid in LESSON_IDS:
            md = (self.LESSONS / f"{mid}.md").read_text(encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mdrender.render(md)
            self.assertGreater(len(buf.getvalue()), 500, f"{mid} rendered too short")

    def test_lessons_have_core_sections(self):
        for mid in LESSON_IDS:
            text = (self.LESSONS / f"{mid}.md").read_text(encoding="utf-8")
            for heading in ("Key takeaways", "Check yourself", "Glossary"):
                self.assertIn(heading, text, f"{mid} missing '{heading}'")

    def test_figure_block_renders_in_both_engines(self):
        import io, contextlib
        from engine import mdrender
        from engine.mdhtml import md_to_html
        md = ("```figure The Kill Chain\n"
              "Recon -> Deliver -> C2\n"
              "~~~svg~~~\n"
              '<svg viewBox="0 0 10 10"><rect width="10" height="10"/></svg>\n'
              "```\n")
        h = md_to_html(md)
        self.assertIn("<figure class='fig'>", h)
        self.assertIn("<svg", h)              # raw SVG passed through
        self.assertNotIn("&lt;svg", h)        # not escaped
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mdrender.render(md)
        t = buf.getvalue()
        self.assertIn("Recon -> Deliver -> C2", t)   # ASCII shown
        self.assertNotIn("<svg", t)                  # SVG hidden in terminal

    def test_lesson_svg_figures_are_well_formed(self):
        """Every inline SVG diagram in the lessons parses as well-formed XML."""
        import re, xml.etree.ElementTree as ET
        for mid in LESSON_IDS:
            text = (self.LESSONS / f"{mid}.md").read_text(encoding="utf-8")
            self.assertEqual(text.count("<svg"), text.count("</svg>"),
                             f"{mid}: unbalanced <svg> tags")
            for m in re.finditer(r"<svg.*?</svg>", text, re.S):
                try:
                    ET.fromstring(m.group(0))
                except ET.ParseError as e:
                    self.fail(f"{mid}: malformed SVG — {e}")


class TestWorksheets(unittest.TestCase):
    WS = ROOT / "worksheets"

    def test_worksheets_exist_for_every_module(self):
        for n in range(1, 11):
            found = list(self.WS.glob(f"m{n}-*.md"))
            self.assertTrue(found, f"no worksheet for m{n}")

    def test_worksheets_render_without_error(self):
        import io
        import contextlib
        from engine import mdrender
        for p in self.WS.glob("m*.md"):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mdrender.render(p.read_text(encoding="utf-8"))
            self.assertGreater(len(buf.getvalue()), 200, f"{p.name} rendered too short")


class TestLessonsHtml(unittest.TestCase):
    def test_md_to_html_converter(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "blh", ROOT / "scripts" / "build_lessons_html.py")
        blh = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(blh)
        out = blh.md_to_html("# T\n\n**bold** and `code`\n\n- a\n- b\n\n```\nx=1\n```\n")
        self.assertIn("<h1>T</h1>", out)
        self.assertIn("<strong>bold</strong>", out)
        self.assertIn("<code>code</code>", out)
        self.assertIn("<ul>", out)
        self.assertIn("<pre><code>", out)
        self.assertNotIn("**", out)

    def test_generated_html_has_all_modules(self):
        f = ROOT / "cyberlab-lessons.html"
        if not f.is_file():
            self.skipTest("cyberlab-lessons.html not built")
        import json
        import re
        html = f.read_text(encoding="utf-8")
        self.assertNotIn("/*__DATA__*/", html)
        m = re.search(r"const DATA = (\{.*?\});\s*\nconst DAYS", html, re.S)
        data = json.loads(m.group(1))
        self.assertTrue({f"m{n}" for n in range(1, 11)}.issubset(set(data)))
        self.assertIn("m0", data)


class TestWebApp(unittest.TestCase):
    def test_course_data(self):
        # m0 orientation + rt red-team primer + js web-attack arena + m1..m10
        self.assertEqual(len(course.COURSE_MAP), 13)
        self.assertEqual(course.COURSE_MAP[0][0], "m0")
        self.assertEqual(course.COURSE_MAP[1][0], "rt")
        self.assertEqual(course.COURSE_MAP[2][0], "js")
        self.assertTrue(course.TOOLS and course.COMMANDS)

    def test_resources_well_formed(self):
        res = course.RESOURCES
        self.assertGreaterEqual(len(res), 30, "expected a substantial resource list")
        names = set()
        for r in res:
            for key in ("name", "cat", "url", "desc"):
                self.assertIn(key, r, f"resource missing '{key}': {r.get('name')}")
                self.assertTrue(str(r[key]).strip(), f"empty '{key}' in {r.get('name')}")
            self.assertTrue(r["url"].startswith("https://"), f"{r['name']} url not https")
            self.assertNotIn(r["name"], names, f"duplicate resource {r['name']}")
            names.add(r["name"])
        # must be surfaced to the browser
        from engine import webapp
        boot = webapp._bootstrap()
        self.assertEqual(len(boot["resources"]), len(res))

    def test_module_rows_and_bootstrap(self):
        from engine import webapp
        rows = webapp._module_rows()
        for r in rows:
            self.assertIn("id", r); self.assertIn("complete", r)
        self.assertEqual(len(rows), len(course.COURSE_MAP))
        boot = webapp._bootstrap()
        self.assertEqual(len(boot["modules"]), len(course.COURSE_MAP))
        self.assertTrue(boot["tools"] and boot["commands"])
        self.assertIn("summary", boot)

    def test_lab_detail_never_leaks_answers(self):
        """The browser must receive prompts/hints but NEVER expected answers."""
        from engine import webapp
        from engine.manifest import load_one
        for mid in ("m1", "m4", "m6"):
            d = webapp._lab_detail(load_one(mid))
            for c in d["checks"]:
                self.assertNotIn("answer", c)
                self.assertNotIn("accept", c)

    def test_webui_assets_present(self):
        for f in ("index.html", "app.js", "styles.css"):
            self.assertTrue((ROOT / "webui" / f).is_file(), f"webui/{f} missing")

    def test_tools_are_richly_documented(self):
        self.assertGreaterEqual(len(course.TOOLS), 15)
        for t in course.TOOLS:
            for k in ("name", "cat", "desc", "usage", "commands"):
                self.assertIn(k, t, f"tool {t.get('name')} missing '{k}'")
            self.assertTrue(t["commands"], f"tool {t['name']} has no commands")
            for c in t["commands"]:
                self.assertIn("cmd", c); self.assertIn("desc", c)


class TestTerminal(unittest.TestCase):
    def test_webterm_imports_and_vendor_present(self):
        from engine import webterm  # noqa: F401
        for f in ("xterm.js", "xterm.css", "xterm-addon-fit.js"):
            self.assertTrue((ROOT / "webui" / "vendor" / f).is_file(),
                            f"vendor/{f} missing")

    def test_ws_frame_roundtrip(self):
        """The WebSocket codec must decode a masked client frame correctly."""
        import os
        import struct
        from engine import webterm

        class FakeSock:
            def __init__(self, data): self.buf = data
            def recv(self, n):
                chunk = self.buf[:n]; self.buf = self.buf[n:]; return chunk

        payload = b'{"t":"data","d":"x"}'
        mask = os.urandom(4)
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        frame = bytes([0x81, 0x80 | len(payload)]) + mask + masked
        op, got = webterm._read_frame(FakeSock(frame))
        self.assertEqual(op, 0x1)
        self.assertEqual(got, payload)


class TestReference(unittest.TestCase):
    def test_topics_discover(self):
        from engine import reference
        ids = {t["id"] for t in reference.discover()}
        self.assertEqual(ids, {"frameworks", "ghana-law", "glossary"})

    def test_topics_render_in_both_engines(self):
        import io, contextlib
        from engine import reference, mdrender
        from engine.mdhtml import md_to_html
        for t in reference.discover():
            md = reference.load(t["id"])
            self.assertTrue(md and len(md) > 400, f"{t['id']} too short")
            self.assertIn("<", md_to_html(md))               # HTML renders
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                mdrender.render(md)
            self.assertGreater(len(buf.getvalue()), 400, f"{t['id']} terminal render short")

    def test_missing_topic_returns_none(self):
        from engine import reference
        self.assertIsNone(reference.load("does-not-exist"))


class TestAssessment(unittest.TestCase):
    def setUp(self):
        # Redirect per-student state to a throwaway file so grading these
        # quizzes never pollutes a real student's recorded progress.
        from engine import paths
        self._tmp = tempfile.TemporaryDirectory()
        self._orig = paths.STATE_FILE
        paths.STATE_FILE = Path(self._tmp.name) / "state.json"

    def tearDown(self):
        from engine import paths
        paths.STATE_FILE = self._orig
        self._tmp.cleanup()

    def test_bank_loads(self):
        from engine import quiz
        bank = quiz.load()
        for qid in ("m1", "m10", "final", "baseline"):
            self.assertIn(qid, bank)
            self.assertTrue(bank[qid].get("questions"))

    def test_every_question_self_grades(self):
        """Answering each quiz with the correct (shuffled) options scores 100%."""
        from engine import quiz
        bank = quiz.load()
        for qid, q in bank.items():
            items = quiz.present(qid)
            answers = []
            for i, it in enumerate(items):
                correct_orig = q["questions"][i]["answer"]
                answers.append(it["_order"].index(correct_orig))
            res = quiz.grade(qid, answers)
            self.assertEqual(res["score"], res["total"], f"{qid} did not self-grade 100%")

    def test_grade_structure(self):
        from engine import grade
        g = grade.compute()
        self.assertEqual(set(g["components"]), {"labs", "quizzes", "exam"})
        self.assertIn("passed", g)
        self.assertEqual(sum(c["weight"] for c in g["components"].values()), 1.0)

    def _pass_everything(self):
        from engine import state, quiz
        from engine.manifest import discover_labs
        state.set_student("Test Student")
        for lab in discover_labs():
            if lab.max_points:
                state.record_result(lab.id, {}, lab.max_points, lab.max_points)
        for qid, q in quiz.load().items():
            if qid != "baseline":
                n = len(q["questions"]); state.record_quiz(qid, n, n)

    def test_certificate_locked_until_pass(self):
        from engine import certificate
        b = certificate.build()
        self.assertFalse(b["eligible"])
        self.assertTrue(b["reasons"])

    def test_certificate_earned_and_verifiable(self):
        from engine import certificate
        self._pass_everything()
        b = certificate.build()
        self.assertTrue(b["eligible"])
        code = b["record"]["code"]
        self.assertEqual(certificate.build()["record"]["code"], code)  # stable
        self.assertTrue(certificate.verify(code)["ok"])
        self.assertFalse(certificate.verify("0000-0000-0000")["ok"])
        self.assertIn("Test Student", b["html"])
        self.assertIn(code, b["html"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
