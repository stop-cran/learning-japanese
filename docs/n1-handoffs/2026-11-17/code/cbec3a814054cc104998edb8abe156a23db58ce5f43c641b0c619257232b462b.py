"""Actual immutable report through real original and repaired CLI, plus citation rejections."""
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIFECYCLE = ROOT.parent / "fresh-independent-002" / "lifecycle-011"
PROTOCOL = LIFECYCLE / "protocol-014"
sys.path[:0] = [str(PROTOCOL), r"C:\Users\stop-\n1-kanji-workspace\review-tools"]
from common import freeze_json, frozen, load_module, require, sha, start_guard, write_frozen

CONFIG = LIFECYCLE / "audit-configs-020" / "audit-claude-fresh-003.json"
CONFIG_SHA = "05688385b07d0b00a9a98077014a26aae23a6e06713c7ddb29e78855a3d12d22"
REPORT_SHA = "844961d7d05d23ebb0ee43b819b3c79e1105bdcf07d77cdf739ecba0bf80d2fe"
HOLD = LIFECYCLE / "N1-B134-CLAUDE-FRESH-003-final-hold-76012e64cadc4f0d989fde7a5f83cee6.json"
HOLD_SHA = "9b50c4a5bc689c0059f210b8c42ff288edbfd623e9a4ee42eecd7735bd428800"


class CheckerControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard, _ = start_guard("B134 actual report checker regression")
        cls.config = json.loads(frozen(CONFIG, CONFIG_SHA))
        cls.hold = json.loads(frozen(HOLD, HOLD_SHA))
        cls.report = Path(cls.config["report"])
        cls.raw = frozen(cls.report, REPORT_SHA)
        phase = json.loads(frozen(LIFECYCLE / (cls.config["run"] + "-phase1.json")))
        cls.args = [
            "--core-manifest", cls.config["coreManifest"],
            "--extension", str(LIFECYCLE / (cls.config["run"] + "-extension.json")),
            "--reference", cls.config["reference"], "--phase1-list", str(Path(phase["auditDir"]) / "phase1-list.txt"),
            "--phase2-message", str(LIFECYCLE / (cls.config["run"] + "-phase2-message.txt")),
            "--audit", cls.hold["audit"]["path"], "--run", cls.config["run"]]
        frozen(cls.hold["audit"]["path"], cls.hold["audit"]["sha256"])
        cls.checker = load_module("b134_test_checker_repair", ROOT / "checker-entry.py")
        cls.results = {}

    @classmethod
    def tearDownClass(cls):
        require(frozen(cls.report, REPORT_SHA) == cls.raw, "Original report changed")
        memory = cls.guard.finish()
        require(not memory["breach"], "Regression RAM breach")
        freeze_json(ROOT / "validation.json", {
            "status": "PASS", "reportSha256": REPORT_SHA, "configSha256": CONFIG_SHA,
            "failedFinalSha256": HOLD_SHA, "audit": cls.hold["audit"],
            "results": cls.results, "memory": memory,
            "limits": "Mechanical report contract only; no semantic adjudication or reviewer contact."})

    def cli(self, name, checker, report):
        command = [sys.executable, "-B", str(checker), "--report", str(report), *self.args]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
                                        "PYTHONPATH": os.pathsep.join((str(PROTOCOL),
                                             r"C:\Users\stop-\n1-kanji-workspace\review-tools"))})
        try:
            while True:
                try:
                    stdout, stderr = process.communicate(timeout=.1)
                    break
                except subprocess.TimeoutExpired:
                    self.guard.check()
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=10)
        self.assertEqual(stderr, b"", stderr.decode("utf-8", "replace"))
        value = json.loads(stdout)
        write_frozen(ROOT / (name + "-stdout.json"), stdout)
        write_frozen(ROOT / (name + "-stderr.log"), stderr)
        self.results[name] = {"exitCode": process.returncode, "status": value["status"],
                              "errors": value["errors"], "stdoutSha256": sha(stdout)}
        return process.returncode, value

    def mutated(self, name, citation):
        lines = self.raw.decode("utf-8").splitlines()
        in_de = False
        for number, line in enumerate(lines):
            if line == "## D/E cards read":
                in_de = True
            elif in_de and line.startswith("## "):
                break
            elif in_de and line.startswith("| D1 |"):
                cells = line.split("|")
                cells[5] += " (" + citation + ") "
                lines[number] = "|".join(cells)
                path = ROOT / (name + ".md")
                write_frozen(path, ("\n".join(lines) + "\n").encode())
                return path
        raise AssertionError("Actual first D/E row not found")

    def test_01_original_defect_is_reproduced(self):
        code, result = self.cli("original", PROTOCOL / "check-report-structure-b134-014.py", self.report)
        self.assertEqual(code, 1)
        self.assertTrue(result["errors"])
        self.assertTrue(all(error.startswith("D/E row ") for error in result["errors"]))

    def test_02_actual_report_passes_real_repaired_cli(self):
        code, result = self.cli("repaired", ROOT / "checker-entry.py", self.report)
        self.assertEqual(code, 0)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["deRows"], 15)
        self.assertEqual(result["findings"], 1)
        self.assertEqual(result["optionalPoints"], 3)

    def test_03_parentheses_backticks_and_known_names(self):
        sources = {"repo/kanji/x.md": 10, "REVIEW.md": 20}
        found = self.checker.inline_references(
            ["(`repo/kanji/x.md:1-4`), prose (01-extract.txt:1); (REVIEW.md:2)."], sources)
        self.assertEqual(found, ["repo/kanji/x.md:1-4", "REVIEW.md:2"])
        original = self.checker.load_checker()
        errors = []
        original.citations("; ".join(found), sources, errors, "row")
        self.assertEqual(errors, [])

    def test_04_unknown_qualified_path_rejected_even_with_valid_citation(self):
        report = self.mutated("invalid-path", "repo/kanji/__NOT_OPENED__.md:1")
        code, result = self.cli("invalid-path", ROOT / "checker-entry.py", report)
        self.assertEqual(code, 1)
        self.assertTrue(any("not in the reviewer's chains" in error for error in result["errors"]))

    def test_05_out_of_range_rejected_even_with_valid_citation(self):
        # Select only the actual row's path, without reading its semantic prose.
        original = self.raw.decode("utf-8")
        start = original.index("## D/E cards read")
        match = __import__("re").search(r"(repo/kanji/[^ :;|()]+\.md):\d+", original[start:])
        self.assertIsNotNone(match)
        report = self.mutated("invalid-range", match[1] + ":999999")
        code, result = self.cli("invalid-range", ROOT / "checker-entry.py", report)
        self.assertEqual(code, 1)
        self.assertTrue(any("outside source lines" in error for error in result["errors"]))

    def test_06_short_only_missing_and_strict_fo_grammar_unchanged(self):
        repaired = self.checker.load_checker()
        self.assertEqual(self.checker.inline_references(["(01-extract.txt:1)"], {}), [])
        for value in ("repo/not-opened.md:1", "repo/card.md:99", "repo/card.md:1,3", "repo/card.md:3-1"):
            errors = []
            repaired.citations(value, {"repo/card.md": 5}, errors, "strict")
            self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
