"""Additional synthetic controls; no real reviewer records, selections or writes."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import patch
from b134_common import HERE, PROTOCOL, CORE, CORE_SHA, PACKET, SUMS_SHA, frozen, sha, start_guard, write_frozen
from b134_capacity import load_forecast, phase2_gate, startup_bound, telemetry
from review_chain_with_optional import validate_selection


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PROTOCOL / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


FIXTURE = module("b134_extra_fixtures", "test-synthetic-protocol-b134-001.py")
AUDIT = FIXTURE.AUDIT
STEP = FIXTURE.STEP


class Focused(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = json.loads(frozen(HERE / "audit-configs-001" / "audit-gpt-001.json"))
        cls.core = json.loads(frozen(CORE, CORE_SHA))
        sums = json.loads(frozen(PACKET / "SHA256SUMS.json", SUMS_SHA))
        cls.reference = json.loads(frozen(PACKET / "eligibility-reference.json", sums["eligibility-reference.json"]))
        cls.events = FIXTURE.events_for(cls.config, cls.core)
        cls.forecast = load_forecast()

    def base(self, events):
        return AUDIT.audit_base(events, self.config, self.core, self.reference)

    def test_exact_complete_returned_ranges(self):
        self.assertEqual(self.base(self.events)["status"], "PHASE1_READY")
        for mutation in ("range", "truncated", "failed", "executed-arguments"):
            events = copy.deepcopy(self.events)
            request = events[5]["data"]["toolRequests"][0]
            self.assertEqual(request["name"], "view")
            if mutation == "range":
                request["arguments"]["view_range"] = [1, 2]
            elif mutation == "truncated":
                events[6]["data"]["result"]["content"] = "truncated synthetic return"
            elif mutation == "failed":
                events[6]["data"]["success"] = False
            else:
                events.insert(6, {"type": "tool.execution_start", "data": {
                    "toolCallId": request["toolCallId"], "toolName": "view",
                    "arguments": {"path": "wrong synthetic path"}}})
            with self.subTest(mutation=mutation):
                result = self.base(events)
                self.assertEqual(result["status"], "VOID")
                self.assertTrue(result["breaches"])

    def test_read_order_and_out_of_scope_tools(self):
        events = copy.deepcopy(self.events)
        first = self.core["segments"][1]
        events[5]["data"]["toolRequests"][0]["arguments"]["path"] = first["path"]
        events[6]["data"]["result"]["content"] = frozen(first["path"]).decode()
        self.assertEqual(self.base(events)["status"], "VOID")
        for tool in ("powershell", "rg", "web_fetch", "web_search", "multi_tool_use.parallel", "create_session"):
            events = copy.deepcopy(self.events)
            events[5]["data"]["toolRequests"][0]["name"] = tool
            with self.subTest(tool=tool):
                self.assertEqual(self.base(events)["status"], "VOID")

    def test_multiple_calls_provenance_and_gap(self):
        events = copy.deepcopy(self.events)
        events[5]["data"]["toolRequests"].append(copy.deepcopy(events[5]["data"]["toolRequests"][0]))
        self.assertEqual(self.base(events)["status"], "VOID")
        events = copy.deepcopy(self.events)
        events[1]["data"]["source"] = "agent-not-the-coordinator"
        self.assertEqual(self.base(events)["status"], "VOID")
        events = copy.deepcopy(self.events)
        events[-1:-1] = [
            {"type": "assistant.message", "data": {"model": "gpt-fixture", "apiCallId": "gap",
                "toolRequests": [{"toolCallId": "gap", "name": "view",
                                  "arguments": {"path": self.core["segments"][0]["path"]}}]}},
            {"type": "tool.execution_complete", "data": {"toolCallId": "gap", "success": True,
                "result": {"content": frozen(self.core["segments"][0]["path"]).decode()}}}]
        self.assertEqual(self.base(events)["status"], "VOID")

    def test_all_card_eligibility_and_caps(self):
        valid = validate_selection("D: none\nE: none\nO: none", self.reference)
        self.assertTrue(valid["valid"])
        for row in self.reference["cards"]:
            for char in row["distractors"] + row["quiz_exclusions"]:
                self.assertFalse(validate_selection(f"D1 {char} - 琴: synthetic overlap\nE: none",
                                                    self.reference)["valid"])
        fake = {"newCards": ["甲"], "otherRequiredCards": [],
                "cards": [{"distractors": [], "quiz_exclusions": []}]}
        lines = [f"D{i + 1} {chr(0x5000 + i)} - 甲: fixture" for i in range(26)]
        self.assertFalse(validate_selection("\n".join(lines + ["E: none", "O: none"]), fake)["valid"])
        self.assertTrue(validate_selection("\n".join(lines[:25] + ["E: none", "O: none"]), fake)["valid"])

    def test_safe_precompaction_headroom(self):
        preflight = json.loads(frozen(HERE / "audit-configs-001" / "preflight.json"))
        for family in ("claude", "gpt"):
            estimate = preflight["runs"][family]["startupEstimate"]
            self.assertEqual(estimate["status"], "PASS_ESTIMATE")
            self.assertEqual(estimate["limit"], 700000)
            self.assertLessEqual(estimate["estimatedUpper"], estimate["limit"])
            self.assertEqual(STEP.inputs(family)[1]["expectedFamily"], family)
        for family, token_value, model, nominal in (
                ("claude", 720000, "claude-opus-5.5", 952000),
                ("gpt", 690000, "gpt-6.1-sol", 922000)):
            events = [{"type": "session.start", "data": {"selectedModel": model, "contextTier": "long_context"}},
                      {"type": "session.usage_record", "data": {"usage": {
                          "inputTokens": token_value, "maxPromptTokens": nominal,
                          "model": family + "-fixture", "responseModel": family + "-fixture"}}}]
            gate = phase2_gate(events, self.forecast, 1, family)
            self.assertFalse(gate["sendPhase2Message"])
            self.assertLess(gate["limit"], nominal)
        with self.assertRaises(ValueError):
            phase2_gate(self.events, self.forecast,
                        self.forecast["maximumExtensionTokens"] + 1, "gpt")

    def test_model_context_absence_and_mismatch(self):
        for change in ("missing-usage", "wrong-context", "wrong-model", "wrong-limit", "mixed-family"):
            events = copy.deepcopy(self.events)
            if change == "missing-usage":
                events = [e for e in events if e["type"] != "session.usage_record"]
            elif change == "wrong-context":
                events[0]["data"]["contextTier"] = "default"
            elif change == "wrong-model":
                events[0]["data"]["selectedModel"] = "gpt-not-selected"
            elif change == "wrong-limit":
                events[2]["data"]["usage"]["maxPromptTokens"] = 1000000
            else:
                events[2]["data"]["usage"]["responseModel"] = "claude-fixture"
            with self.subTest(change=change):
                self.assertEqual(telemetry(events, self.forecast, "gpt")["status"], "HOLD")

    def test_claude_phase1_positive_same_blinded_contract(self):
        config = json.loads(frozen(HERE / "audit-configs-001" / "audit-claude-001.json"))
        events = FIXTURE.events_for(config, self.core)
        events[0]["data"]["selectedModel"] = "claude-opus-5.5"
        events[2]["data"]["usage"].update(model="claude-fixture", responseModel="claude-fixture",
                                           maxPromptTokens=952000)
        for event in events:
            if event["type"] == "assistant.message":
                event["data"]["model"] = "claude-fixture"
        result = AUDIT.audit(events, config, self.core, self.reference)
        self.assertEqual(result["status"], "PHASE1_READY", result["breaches"])

    def test_actual_coordinator_packet_proof_is_pinned(self):
        self.assertEqual(STEP.PROOFS["packet-verification-001/verification.json"],
                         "fb95e655419fe9ecc0465ac565fb309397fb8843c22362b08cf5a1feda4d478a")
        proof = json.loads(frozen(STEP.ROOT / "packet-verification-001" / "verification.json",
                                  STEP.PROOFS["packet-verification-001/verification.json"]))
        self.assertEqual(proof["status"], "PASS")
        self.assertEqual(proof["candidate"], self.config["candidate"])
        self.assertEqual(proof["base"], self.config["base"])
        self.assertEqual(proof["verifiedJmdictFamilies"], 399)
        self.assertEqual(proof["verifiedKanjidicRecords"], 59)


if __name__ == "__main__":
    guard, _ = start_guard("B134 focused protocol controls")
    try:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Focused))
        if not result.wasSuccessful():
            raise SystemExit(1)
    finally:
        if guard.finish()["breach"]:
            raise RuntimeError("Focused controls RAM breach")
