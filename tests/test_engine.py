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


class TestManifests(unittest.TestCase):
    def test_all_labs_discover_and_validate(self):
        labs = manifest.discover_labs()
        ids = {l.id for l in labs}
        self.assertEqual(ids, {"m1", "m3", "m4", "m5", "m6", "m7", "m10"})

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

    def test_m3_pcap_is_valid(self):
        data = (self.LABS / "m3-network/assets/network-capture.pcap").read_bytes()
        magic = struct.unpack("<I", data[:4])[0]
        self.assertEqual(magic, 0xA1B2C3D4, "pcap magic wrong")
        self.assertIn(b"sync-telemetry", data, "C2 domain missing from capture")

    def test_m6_image_is_fat16(self):
        img = (self.LABS / "m6-forensics/assets/evidence.img").read_bytes()
        self.assertEqual(img[510:512], b"\x55\xAA", "boot signature missing")
        self.assertIn(b"FAT16", img[0:64], "FAT16 id missing from BPB")

    def test_m6_hash_manifest_matches_image(self):
        import hashlib
        base = self.LABS / "m6-forensics/assets"
        img = (base / "evidence.img").read_bytes()
        recorded = (base / "evidence.sha256").read_text().split()[0]
        self.assertEqual(hashlib.sha256(img).hexdigest(), recorded)

    def test_m6_artifact_decodes_to_c2(self):
        txt = (self.LABS / "m6-forensics/assets/suspicious_artifact.txt").read_text().strip()
        decoded = urllib.parse.unquote(base64.b64decode(txt).decode())
        self.assertIn("sync-malware-c2.net", decoded)

    def test_m5_email_has_spoof_indicators(self):
        eml = (self.LABS / "m5-bec/assets/invoice-change-request.eml").read_text()
        self.assertIn("zenith-supplies.com", eml)      # look-alike
        self.assertIn("spf=fail", eml)

    def test_answers_in_manifests_are_gradable(self):
        """Every string/numeric check's own answer should grade as correct."""
        for lab in manifest.discover_labs():
            for c in lab.checks:
                if c.type in ("string", "numeric") and c.answer is not None:
                    out = verify.grade_answer(c, str(c.answer))
                    self.assertTrue(out.passed, f"{lab.id}:{c.id} answer not self-consistent")


if __name__ == "__main__":
    unittest.main(verbosity=2)
