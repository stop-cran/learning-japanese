"""All24 existing fabricated compact-002 controls plus report-path admission/preflight regressions."""
import copy
import io
import json
import stat
import unittest
from pathlib import Path
from unittest.mock import patch

from b131_review_v3_common import (
    DEFAULT_PREFLIGHT, HERE, TOOLS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen)
from b131_preflight_003 import path_inventory, validate_report_destination, verify_protocol


class ReportPaths(unittest.TestCase):
    def setUp(self):
        self.root = HERE / "validation-001" / "path-fixtures" / self._testMethodName
        self.config = json.loads(frozen(DEFAULT_PREFLIGHT))
        self.spec = self.config["runs"]["claude"]

    def invalid_specs(self):
        for kind in ("missing", "not-directory", "already-present"):
            report = self.root / kind / "parent" / "report.md"
            if kind == "not-directory":
                report.parent.parent.mkdir(parents=True)
                report.parent.write_bytes(b"synthetic file, not directory\n")
            elif kind == "already-present":
                report.parent.mkdir(parents=True)
                report.write_bytes(b"synthetic pre-existing file\n")
            yield kind, {**self.spec, "report": str(report)}

    def test_preflight_rejects_missing_parent_file_parent_and_existing_report(self):
        for kind, spec in self.invalid_specs():
            candidate = copy.deepcopy(self.config)
            candidate["runs"]["claude"] = spec
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                verify_protocol(candidate)

    def test_admission_rejects_bad_paths_before_reading_any_request(self):
        admission = load_module("b131003_admission_regressions", TOOLS / "b131_review_admission_003.py")
        for kind, spec in self.invalid_specs():
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, "report parent|Report parent|Report already"):
                admission.observe(self.root / "nonexistent-admission-request.json", {}, spec, {})
        self.assertFalse((self.root / "nonexistent-admission-request.json").exists())

    def test_created_report_parents_remain_empty_writable_without_report(self):
        for spec in self.config["runs"].values():
            proof = validate_report_destination(spec)
            self.assertTrue(proof["empty"] and proof["reportAbsent"] and not proof["directoryReadOnly"])
            self.assertEqual(list(Path(spec["report"]).parent.iterdir()), [])

    def test_readonly_report_parent_rejected(self):
        parent = self.root / "parent"
        parent.mkdir(parents=True)
        parent.chmod(stat.S_IREAD)
        try:
            with self.assertRaisesRegex(ValueError, "ReadOnly"):
                validate_report_destination({"report": str(parent / "report.md")})
        finally:
            parent.chmod(stat.S_IREAD | stat.S_IWRITE)

    def test_actual_write_denial_surfaces(self):
        parent = self.root / "parent"
        parent.mkdir(parents=True)
        with patch.object(Path, "open", side_effect=PermissionError("synthetic ACL denial")):
            with self.assertRaisesRegex(PermissionError, "ACL denial"):
                validate_report_destination({"report": str(parent / "report.md")})
        self.assertEqual(list(parent.iterdir()), [])

    def test_one_create_and_exact_readback_with_created_parent(self):
        parent = self.root / "parent"
        parent.mkdir(parents=True)
        report = parent / "synthetic-report.md"
        validate_report_destination({"report": str(report)})
        with report.open("x", encoding="utf-8", newline="\n") as stream:
            stream.write("synthetic one-create report\n")
        self.assertEqual(report.read_bytes(), b"synthetic one-create report\n")
        with self.assertRaisesRegex(ValueError, "already present"):
            validate_report_destination({"report": str(report)})

    def test_every_reviewer_path_has_existing_input_or_explicit_creation_owner(self):
        inventory = path_inventory(self.config)
        self.assertEqual(len(inventory), 2)
        for item in inventory:
            self.assertEqual(item["core"]["segments"], 66)
            self.assertTrue(item["reportCreate"]["exclusiveCreateReadbackDelete"] == "PASS")
            self.assertIn("before any phase2", item["extension"]["state"])
            self.assertEqual(item["reportReadback"]["path"], item["reportCreate"]["report"])


def main():
    root = HERE / "validation-001"
    require(not root.exists(), "Preserve previous validation")
    guard, _ = start_guard("B131003 complete focused validation")
    try:
        existing = load_module("b131003_existing_focused_controls", HERE / "test-controls-003.py")
        suite = unittest.TestSuite((
            unittest.defaultTestLoader.loadTestsFromTestCase(existing.Controls),
            unittest.defaultTestLoader.loadTestsFromTestCase(ReportPaths)))
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        text = stream.getvalue()
        write_frozen(root / "output.log", text.encode("utf-8"))
        memory = guard.finish()
        require(not memory["breach"], "Validation RAM breach")
        record = {"status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
                  "existingControls": 24, "newPathControls": 7, "newCompleteCreateReadbackControl": 1,
                  "failures": len(result.failures),
                  "errors": len(result.errors), "memory": memory,
                  "testTool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
                  "outputSha256": sha(text.encode("utf-8")),
                  "scope": "Fabricated undelivered events and new path fixtures only. No reviewer admitted, launched, "
                           "messaged, or actual quarantined events/list/report/final opened."}
        binding = freeze_json(root / "result.json", record)
        print(text)
        print(json.dumps({"result": binding, **record}))
        return 0 if result.wasSuccessful() else 1
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    raise SystemExit(main())
