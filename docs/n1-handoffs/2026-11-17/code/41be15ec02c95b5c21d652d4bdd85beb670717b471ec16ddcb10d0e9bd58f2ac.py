"""Focused fabricated capacity/profile/path/subprocess controls plus all25 inherited source controls."""
import copy
import io
import json
import stat
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

from b131_review_v4_common import (
    DEFAULT_PREFLIGHT, HERE, TOOLS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen)
import b131_capacity_003 as capacity
import b131_preflight_004 as preflight

ROOT = HERE / "validation-004"


def events_for(family, tokens=300000):
    profile = capacity.PROFILES[family]
    return [{"type": "session.start", "data": {
        "contextTier": "long_context", "selectedModel": profile["selectedModel"]}},
        {"type": "session.usage_record", "data": {"usage": {
            "inputTokens": tokens, "maxPromptTokens": profile["maxPromptTokens"],
            "model": profile["selectedModel"], "responseModel": profile["selectedModel"]}}}]


class CapacityControls(unittest.TestCase):
    def setUp(self):
        self.forecast = capacity.load_forecast()
        self.root = ROOT / "profile-fixtures" / self._testMethodName
        self.config = json.loads(frozen(DEFAULT_PREFLIGHT))
        self.spec = self.config["runs"]["gpt"]
        self.cost = capacity.extension_tokens(1000, 2000, 2, 1)

    def test_both_supported_exact_context_profiles(self):
        for family in capacity.PROFILES:
            with self.subTest(family=family):
                result = capacity.telemetry(events_for(family), self.forecast, family)
                self.assertEqual(result["status"], "PASS")
                self.assertEqual(result["forecastPhase1Tokens"], 526615)

    def test_limits_below_minimum_mixed_invalid_and_unknown_hold(self):
        for family, spec in capacity.PROFILES.items():
            for value in (spec["maxPromptTokens"] - 1, None, True, 922000.0, "922000", 0,
                          spec["maxPromptTokens"] + 1):
                rows = events_for(family)
                rows[1]["data"]["usage"]["maxPromptTokens"] = value
                with self.subTest(family=family, value=value):
                    self.assertEqual(capacity.telemetry(rows, self.forecast, family)["status"], "HOLD")
            rows = events_for(family)
            extra = copy.deepcopy(rows[1])
            extra["data"]["usage"]["maxPromptTokens"] = 922000 if family == "claude" else 952000
            self.assertEqual(capacity.telemetry(rows + [extra], self.forecast, family)["status"], "HOLD")

    def test_bad_tokens_model_context_and_compaction_hold(self):
        for family in capacity.PROFILES:
            for value in (None, True, -1, "300000", 1.2, 1000000):
                rows = events_for(family)
                rows[1]["data"]["usage"]["inputTokens"] = value
                self.assertEqual(capacity.telemetry(rows, self.forecast, family)["status"], "HOLD")
            for field, value in (("selectedModel", "unknown"), ("contextTier", "standard")):
                rows = events_for(family)
                rows[0]["data"][field] = value
                self.assertEqual(capacity.telemetry(rows, self.forecast, family)["status"], "HOLD")
            for kind in ("session.compaction_start", "session.compaction_complete"):
                rows = events_for(family) + [{"type": kind, "data": {}}]
                result = capacity.phase2_gate(rows, self.forecast, self.cost, family)
                self.assertFalse(result["sendPhase2Message"])
                self.assertEqual(result["telemetry"]["compactions"], [kind])
            rows = events_for(family)
            rows[1]["data"]["usage"]["responseModel"] = "gpt-other" if family == "claude" else "claude-other"
            self.assertEqual(capacity.telemetry(rows, self.forecast, family)["status"], "HOLD")
            for rows in ([], events_for(family)[1:], events_for(family) * 2,
                         events_for(family) + [{"type": "session.usage_record", "data": {"usage": []}}]):
                self.assertEqual(capacity.telemetry(rows, self.forecast, family)["status"], "HOLD")

    def test_both_exact_gate_boundaries_and_one_token_over(self):
        for family, profile in capacity.PROFILES.items():
            last = profile["prePhase2Gate"] - 7000 - self.cost["tokens"] - 30000
            passed = capacity.phase2_gate(events_for(family, last), self.forecast, self.cost, family)
            self.assertTrue(passed["sendPhase2Message"])
            self.assertEqual(passed["projectedPeak"], profile["prePhase2Gate"])
            held = capacity.phase2_gate(events_for(family, last + 1), self.forecast, self.cost, family)
            self.assertFalse(held["sendPhase2Message"])
        self.assertEqual(capacity.PROFILES["gpt"]["prePhase2Gate"], 710000)
        self.assertLessEqual(710000, int(.8 * 922000))

    def test_omitted_dictionary_and_header_costs_rejected(self):
        for key in ("supplementalDictionaryBytes", "headerAllowanceTokens", "supplementalRecords"):
            altered = dict(self.cost, **{key: 0})
            if key == "headerAllowanceTokens":
                altered["tokens"] = altered["sourceTokens"]
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "altered or omitted"):
                capacity.phase2_gate(events_for("gpt"), self.forecast, altered, "gpt")

    def test_neutral_telemetry_and_startup_forecast_remain_conservative(self):
        neutral = capacity.verify_neutral_telemetry()
        self.assertEqual(neutral["measuredCoreTokens"], 273135)
        self.assertEqual(neutral["actualPeakInputTokens"], 322200)
        self.assertEqual(self.forecast["bootstrapTokens"] + self.forecast["coreTokens"], 526615)
        self.assertEqual(self.forecast["projectedWorstCasePeak"], 698784)
        self.assertLessEqual(self.forecast["projectedWorstCasePeak"], 700000)

    def test_changed_profile_or_sequential_prerequisite_rejected(self):
        cfg = json.loads(frozen(self.spec["auditConfig"]))
        cfg["contextProfile"] = capacity.PROFILES["claude"]
        with self.assertRaisesRegex(ValueError, "profile differs"):
            capacity.validate_capacity_config(cfg)
        altered = copy.deepcopy(self.config)
        altered["sequentialPrerequisite"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "prerequisite"):
            preflight.verify_prerequisite(altered)

    def test_report_parent_bad_paths_fail_preflight_and_admission_before_request(self):
        admission = load_module("b131004_admission_path_test", TOOLS / "b131_review_admission_004.py")
        for kind in ("missing", "not-directory", "preexisting"):
            report = self.root / kind / "parent" / "report.md"
            if kind == "not-directory":
                report.parent.parent.mkdir(parents=True)
                report.parent.write_bytes(b"fixture file")
            elif kind == "preexisting":
                report.parent.mkdir(parents=True)
                report.write_bytes(b"fixture report")
            spec = {**self.spec, "report": str(report)}
            candidate = copy.deepcopy(self.config)
            candidate["runs"]["gpt"] = spec
            with self.subTest(kind=kind):
                with self.assertRaises(ValueError):
                    preflight.verify_protocol(candidate)
                with self.assertRaisesRegex(ValueError, "report parent|Report parent|Report already"):
                    admission.observe(self.root / "no-request.json", {}, spec, {})

    def test_readonly_and_actual_write_denial_fail_and_real_parent_probe_passes(self):
        parent = self.root / "parent"
        parent.mkdir(parents=True)
        spec = {"report": str(parent / "report.md")}
        parent.chmod(stat.S_IREAD)
        try:
            with self.assertRaisesRegex(ValueError, "ReadOnly"):
                preflight.validate_report_destination(spec)
        finally:
            parent.chmod(stat.S_IREAD | stat.S_IWRITE)
        with patch.object(Path, "open", side_effect=PermissionError("fixture ACL denied")):
            with self.assertRaises(PermissionError):
                preflight.validate_report_destination(spec)
        self.assertEqual(list(parent.iterdir()), [])
        self.assertEqual(preflight.validate_report_destination(self.spec)["exclusiveCreateReadbackDelete"], "PASS")

    def test_actual_inventory_suffix_and_preserved_coordinator_fixes(self):
        inventory = preflight.path_inventory(self.config)
        builder = frozen(TOOLS / "prepare_chain_b131_004.py").decode("utf-8")
        self.assertIn('f"b131-{args.run}-extension-004"', builder)
        self.assertTrue(inventory["extensionDirectory"].endswith("-extension-004"))
        helper = frozen(TOOLS / "b131_lifecycle_process_006.py").decode("utf-8")
        self.assertIn('"PYTHONPATH": str(TOOLS)', helper)
        step = frozen(TOOLS / "step_b131_neutral_007.py").decode("utf-8")
        self.assertIn('f"{run}-context-{path.parent.name}.json"', step)
        self.assertIn('f"{run}-structure-{path.parent.name}.json"', step)

    def test_real_context_checker_child_imports_both_profiles_and_hold(self):
        adapter = load_module("b131004_real_child_context", TOOLS / "b131_lifecycle_process_006.py")
        for family in capacity.PROFILES:
            for compacted in (False, True):
                rows = events_for(family) + ([{"type": "session.compaction_start", "data": {}}] if compacted else [])
                path = self.root / f"{family}-{compacted}.jsonl"
                write_frozen(path, b"".join((json.dumps(row) + "\n").encode() for row in rows))
                code, out, err = adapter.python(HERE / "check-run-context.py", path)
                self.assertEqual(code, 1 if compacted else 0, err)
                self.assertEqual(json.loads(out)["status"], "FAIL" if compacted else "PASS")

    def test_full_serial_roster_resource_admission_shape_is_preserved(self):
        admission = load_module("b131004_roster_test", TOOLS / "b131_review_admission_004.py")
        now = datetime.now(timezone.utc)
        coordinator = admission.COORDINATOR
        rows = [{"id": coordinator, "name": "coordinator", "activity": {"status": "busy"}},
                {"id": "fabricated-idle-session", "name": "fabricated", "activity": {"status": "idle"}}]
        roster = [{"id": row["id"]} for row in rows]
        status = {"sessions": rows, "summary": {"total": 2}}
        args = (status, roster, "fresh004", now, now)
        self.assertEqual(admission.validate_roster(*args), 2)
        for value in ("busy", "unknown"):
            altered = copy.deepcopy(status)
            altered["sessions"][1]["activity"]["status"] = value
            with self.assertRaises(ValueError):
                admission.validate_roster(altered, roster, "fresh004", now, now)
        with self.assertRaises(ValueError):
            admission.validate_roster(status, roster[:1], "fresh004", now, now)
        with self.assertRaises(ValueError):
            admission.validate_roster(status, roster, "fresh004", now, now - timedelta(seconds=120))


def main():
    require(not ROOT.exists(), "Preserve all previous validation; use a successor after failure")
    guard, _ = start_guard("B131 GPT004 fabricated focused controls")
    try:
        existing = load_module("b131004_source_controls", HERE / "test-controls-004.py")

        class RealStructureChecker(existing.Controls):
            def test_full_extension_chain_coverage_and_sha_rejection(self):
                code, message_path, audit_path = self.build_synthetic_extension()
                self.assertEqual(code, 0)
                run = self.audit_config["run"]
                chain = json.loads(frozen(self.case / f"{run}-extension.json"))
                for kind in ("missing-source", "missing-part", "changed-sha"):
                    changed = copy.deepcopy(chain)
                    if kind == "missing-source":
                        changed["sources"].pop()
                    elif kind == "missing-part":
                        changed["segments"][0]["parts"].pop()
                    else:
                        changed["segments"][0]["sha256"] = "0" * 64
                    with patch.object(existing.runtime, "HERE", self.case):
                        with self.subTest(kind=kind), self.assertRaises(ValueError):
                            existing.runtime.validate_prepared_extension(
                                self.audit_config, changed, self.synthetic_list,
                                frozen(message_path).decode("utf-8"), audit_path)

            def test_real_structure_checker_subprocess_imports(self):
                code, message_path, audit_path = self.build_synthetic_extension()
                self.assertEqual(code, 0)
                report = self.case / "synthetic-structure-report.md"
                write_frozen(report, b"# Fabricated structure rejection fixture\n")
                run = self.audit_config["run"]
                adapter = load_module("b131004_real_child_structure", TOOLS / "b131_lifecycle_process_006.py")
                code, out, err = adapter.python(
                    HERE / "check-report-structure.py", "--report", report, "--core-manifest",
                    self.audit_config["coreManifest"], "--extension", self.case / f"{run}-extension.json",
                    "--reference", self.audit_config["reference"], "--phase1-list", audit_path.parent / "phase1-list.txt",
                    "--phase2-message", message_path, "--audit", audit_path, "--run", run)
                self.assertEqual(code, 1, err)
                self.assertEqual(json.loads(out)["status"], "FAIL")

        suite = unittest.TestSuite((
            unittest.defaultTestLoader.loadTestsFromTestCase(RealStructureChecker),
            unittest.defaultTestLoader.loadTestsFromTestCase(CapacityControls)))
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
        text = stream.getvalue()
        write_frozen(ROOT / "output.log", text.encode("utf-8"))
        memory = guard.finish()
        require(not memory["breach"], "Validation RAM breach")
        proof = freeze_json(ROOT / "result.json", {
            "status": "PASS" if result.wasSuccessful() else "FAIL", "tests": result.testsRun,
            "failures": len(result.failures), "errors": len(result.errors), "memory": memory,
            "testTool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
            "outputSha256": sha(text.encode("utf-8")),
            "scope": "Fabricated undelivered events and mechanical selections only. No reviewer observations "
                     "or real admission/launch/resume; no source/forecast changes."})
        print(text)
        print(json.dumps(proof))
        return 0 if result.wasSuccessful() else 1
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    raise SystemExit(main())
