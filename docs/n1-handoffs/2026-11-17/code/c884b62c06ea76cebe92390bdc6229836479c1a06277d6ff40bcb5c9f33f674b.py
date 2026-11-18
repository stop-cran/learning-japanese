"""Focused lifecycle, source-class, capacity and report-contract controls."""
import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from b134_common import CAPACITY_SHA, CORE_SHA, PACKET, frozen, sha, verify_core, verify_packet, write_frozen
from b134_capacity import PROFILES, load_forecast, phase2_gate
from review_chain_with_optional import optional_unit_map, validate_selection
from capacity011 import source_class


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HERE = Path(__file__).resolve().parent
structure = load_module("b134_structure_011", HERE / "check-report-structure-b134-011.py")
step = load_module("b134_step_011", HERE / "step-b134-011.py")


class LifecycleControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sums = verify_packet()
        cls.core = verify_core()
        cls.forecast = load_forecast()
        cls.reference = json.loads(frozen(PACKET / "eligibility-reference.json",
                                          cls.sums["eligibility-reference.json"]))
        cls.units = optional_unit_map(json.loads(frozen(
            PACKET / "evidence/kanjidic2-full-unit-index.json",
            cls.sums["evidence/kanjidic2-full-unit-index.json"])))

    def test_exact_frozen_core_and_measured_tier(self):
        self.assertEqual(len(self.core["sources"]), 90)
        self.assertEqual(len(self.core["segments"]), 64)
        self.assertEqual(self.forecast["chosenCaps"], {"D": 20, "E": 10})
        self.assertEqual(self.forecast["trials"][1]["startupForecast"], 686550)
        self.assertEqual(700000 - self.forecast["trials"][1]["startupForecast"], 13450)
        self.assertEqual(len(self.units), 88)

    def test_hash_bound_configs_and_reconciliation_proofs(self):
        for family in ("claude", "gpt"):
            spec, config = step.inputs(family, fresh_report=False)
            self.assertEqual(config["expectedFamily"], family)
            self.assertEqual(spec["launch"]["contextTier"], "long_context")
            self.assertEqual(config["reportStructureContract"], "report-structure-v1")
            self.assertTrue(any(row["path"] == config["reportStructureChecker"]
                                for row in config["files"]))
        for binding in step.PROOFS.values():
            proof = json.loads(frozen(binding["path"], binding["sha256"]))
            self.assertTrue(proof["status"].startswith("PASS"))

    def test_nested_extract_and_check_classification(self):
        self.assertEqual(source_class("reconciliation/evidence/native-紫-kotobank-extract.txt"),
                         ("extract", .446 * 1.10))
        self.assertEqual(source_class("reconciliation/checks/lint.log"),
                         ("checks", .522 * 1.10))
        self.assertEqual(source_class("checks/lint.log"),
                         ("checks", .522 * 1.10))

    def test_selection_caps_and_complete_optional_inventory(self):
        valid = validate_selection("D: none\nE: none\nO: none", self.reference, self.units)
        self.assertTrue(valid["valid"], valid["errors"])
        targets = set(self.reference["cards"][0]["quiz_exclusions"])
        distractors = set(self.reference["cards"][0]["distractors"])
        eligible = []
        for codepoint in range(0x4E00, 0x9FFF):
            char = chr(codepoint)
            if char not in targets | distractors | set(self.reference["newCards"]):
                eligible.append(char)
            if len(eligible) == 21:
                break
        d20 = "\n".join(f"D{i} {char} - 紫: synthetic overlap" for i, char in enumerate(eligible[:20], 1))
        self.assertTrue(validate_selection(d20 + "\nE: none\nO: none", self.reference, self.units)["valid"])
        d21 = d20 + f"\nD21 {eligible[20]} - 紫: synthetic overlap\nE: none\nO: none"
        self.assertFalse(validate_selection(d21, self.reference, self.units)["valid"])
        exclusions = self.reference["cards"][0]["quiz_exclusions"]
        e10 = "\n".join(f"E{i} {char} - synthetic reason" for i, char in enumerate(exclusions[:10], 1))
        self.assertTrue(validate_selection("D: none\n" + e10 + "\nO: none",
                                           self.reference, self.units)["valid"])
        e11 = e10 + f"\nE11 {exclusions[10]} - synthetic reason"
        self.assertFalse(validate_selection("D: none\n" + e11 + "\nO: none",
                                            self.reference, self.units)["valid"])
        all_units = list(self.units)
        o88 = "\n".join(f"O{i} {unit} - synthetic optional request"
                        for i, unit in enumerate(all_units, 1))
        self.assertTrue(validate_selection("D: none\nE: none\n" + o88,
                                           self.reference, self.units)["valid"])
        self.assertFalse(validate_selection(
            "D: none\nE: none\n" + o88 + f"\nO89 {all_units[0]} - duplicate",
            self.reference, self.units)["valid"])

    def test_exact_actual_phase_two_boundaries(self):
        for family, profile in PROFILES.items():
            events = [{"type": "session.start", "data": {
                "sessionId": "synthetic-session", "selectedModel": profile["selectedModel"],
                "contextTier": "long_context"}},
                {"type": "session.usage_record", "data": {"usage": {
                    "inputTokens": 1, "maxPromptTokens": profile["maxPromptTokens"],
                    "model": profile["selectedModel"], "responseModel": profile["selectedModel"]}}}]
            extension = 0
            boundary = (profile["prePhase2Gate"] - 7000 - extension - 30000)
            events[-1]["data"]["usage"]["inputTokens"] = boundary
            self.assertTrue(phase2_gate(events, self.forecast, extension, family,
                                        "synthetic-session")["sendPhase2Message"])
            events[-1]["data"]["usage"]["inputTokens"] = boundary + 1
            self.assertFalse(phase2_gate(events, self.forecast, extension, family,
                                         "synthetic-session")["sendPhase2Message"])
            events[-1]["data"]["usage"]["inputTokens"] = 1
            events.append({"type": "session.compaction_start", "data": {}})
            self.assertFalse(phase2_gate(events, self.forecast, extension, family,
                                         "synthetic-session")["sendPhase2Message"])

    def test_prompt_only_bootstrap_rejections(self):
        profile = PROFILES["claude"]
        with tempfile.TemporaryDirectory(prefix="b134-bootstrap-") as temp:
            home = Path(temp)
            prompt = home / "frozen-prompt.txt"
            prompt_bytes = "Synthetic prompt only.\n".encode()
            write_frozen(prompt, prompt_bytes)
            call_index = 0

            def fixture(mutator=None):
                nonlocal call_index
                call_index += 1
                session = f"synthetic-bootstrap-session-{call_index}"
                events_path = home / ".copilot" / "session-state" / session / "events.jsonl"
                rows = [
                    {"type": "session.start", "data": {"sessionId": session,
                     "selectedModel": profile["selectedModel"], "contextTier": "long_context"}},
                    {"type": "user.message", "data": {"content": "synthetic kickoff"}},
                    {"type": "session.usage_record", "data": {"usage": {
                        "inputTokens": 1000, "maxPromptTokens": profile["maxPromptTokens"],
                        "model": profile["selectedModel"], "responseModel": profile["selectedModel"]}}},
                    {"type": "assistant.message", "data": {"toolRequests": [{
                        "toolCallId": "bootstrap-call", "name": "view", "arguments": {
                            "path": str(prompt), "forceReadLargeFiles": True, "view_range": None}}]}},
                    {"type": "tool.execution_start", "data": {"toolCallId": "bootstrap-call",
                     "toolName": "view", "arguments": {"path": str(prompt),
                     "forceReadLargeFiles": True, "view_range": None}}},
                    {"type": "tool.execution_complete", "data": {"toolCallId": "bootstrap-call",
                     "success": True, "result": {"content": prompt_bytes.decode()}}},
                    {"type": "assistant.message", "data": {"content": step.BOOTSTRAP_RESPONSE}},
                    {"type": "assistant.turn_end", "data": {}},
                ]
                if mutator:
                    mutator(rows)
                write_frozen(events_path, b"".join(
                    (json.dumps(row, ensure_ascii=False) + "\n").encode() for row in rows))
                config = {"prompt": str(prompt), "contextProfile": profile,
                          "bootstrapResponseText": step.BOOTSTRAP_RESPONSE}
                spec = {"kickoffText": "synthetic kickoff",
                        "prompt": {"sha256": sha(prompt_bytes)}}
                with patch("pathlib.Path.home", return_value=home):
                    return step.prompt_only_events(session, spec, config)

            self.assertEqual(fixture()[2][-1]["type"], "assistant.turn_end")
            for mutate in (
                lambda rows: rows[0]["data"].update(contextTier=None),
                lambda rows: rows[0]["data"].update(selectedModel="auto"),
                lambda rows: rows[2]["data"]["usage"].update(maxPromptTokens=200000),
                lambda rows: rows.append({"type": "session.compaction_start", "data": {}}),
                lambda rows: rows.append({"type": "user.message", "data": {"content": "extra"}}),
            ):
                with self.assertRaises((ValueError, KeyError)):
                    fixture(mutate)

    def test_report_contract_and_d_e_citations(self):
        run = "N1-B134-CLAUDE-FRESH-002"
        report = f"""# B134 fresh independent review — {run}

## Overall verdict
Verdict: UNVERIFIED

## Facet verdicts
### Correctness
Verdict: UNVERIFIED
Basis: Synthetic test only.
### Scoped coverage
Verdict: UNVERIFIED
Basis: Synthetic test only.
### Consistency/quiz safety
Verdict: UNVERIFIED
Basis: Synthetic test only.
### Comprehensibility
Verdict: UNVERIFIED
Basis: Synthetic test only.

## Segments read
Core chain: 1-64; no re-views
Extension chain: 1; no re-views

## Phase-1 D/E lists
D: D1 甲
E: none
O: none
Missing entries: none

## D/E cards read
| ID | Character | Displayed title | Related new card(s) | Reason | Disposition |
| --- | --- | --- | --- | --- | --- |
| D1 | 甲 | synthetic title | 紫 | Potential overlap; cmp.md:1 | Harmless; cmp.md:1 |

## Per-card results
| Card | Correctness | Scoped coverage | Consistency/quiz safety | Comprehensibility | Evidence |
| --- | --- | --- | --- | --- | --- |
| 紫 | UNVERIFIED | UNVERIFIED | UNVERIFIED | UNVERIFIED | Synthetic test only |

## Findings
None.

## Optional points
None.

## Limits
- L1: Synthetic test only.
"""
        core = {"sources": [{"source": "core.md", "selectedLines": 1}]}
        extension = {"sources": [{"source": "cmp.md [D1]", "selectedLines": 2}]}
        reference = {"newCards": ["紫"]}
        phase1 = {"entries": [{"label": "D1", "character": "甲"}], "optional": []}
        phase2 = "extension-first-segment\nMissing entries: none"
        result = structure.check(report, run, core, extension, reference, phase1, phase2, "UNVERIFIED")
        self.assertEqual(result["status"], "PASS", result["errors"])
        bad = report.replace("Potential overlap; cmp.md:1", "Potential overlap")
        bad = bad.replace("Harmless; cmp.md:1", "Harmless")
        result = structure.check(bad, run, core, extension, reference, phase1, phase2, "UNVERIFIED")
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(any("citation" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
