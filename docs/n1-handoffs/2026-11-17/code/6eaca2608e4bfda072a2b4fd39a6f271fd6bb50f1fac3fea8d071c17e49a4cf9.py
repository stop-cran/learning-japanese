"""Verify exact actual source bounds without admitting or messaging a reviewer."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import frozen, load_module, sha

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent


class CapacityHold(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(frozen(HERE / "capacity-decision-002.json"))
        cls.runtime = load_module("b134_capacity_hold_test_runtime",
                                  REVIEW / "authorization-runtime-004" / "b134_authorized_confirmation_v3.py")
        cls.tool = cls.runtime.legacy

    def test_exact_actual_prior_report_and_adjudication_bytes(self):
        for family in ("claude", "gpt"):
            record = self.data["families"][family]
            accepted = json.loads(self.tool.read(record["priorAcceptance"]))
            self.assertEqual(accepted["candidate"], self.data["reviewed"])
            self.assertEqual(accepted["mode"], "revision")
            self.assertTrue(accepted["confirmationAccepted"])
            for name in ("report", "adjudication"):
                item = record["priorSources"][name]
                self.assertEqual(item["ref"], accepted[name])
                self.assertEqual(item["bytes"], len(self.tool.read(item["ref"])))

    def test_lower_bound_excludes_every_not_yet_known_source(self):
        units = self.data["completeSourceUnits"]
        for family in ("claude", "gpt"):
            record = self.data["families"][family]
            base = units["articles/numbers-and-counters.md"]["bytes"] + units["counters/kumiexpressions.json"]["bytes"]
            minimal = base + record["priorSources"]["report"]["bytes"]
            required = minimal + units["signed-incoming.patch"]["bytes"]
            self.assertEqual(record["strictNecessaryUnitsOnly"]["completeSourceBytes"], minimal)
            self.assertEqual(record["withRequiredSignedIncomingPatch"]["completeSourceBytes"], required)
            self.assertEqual(sum(record["reserves"].values()), 49000)
            for key in ("strictNecessaryUnitsOnly", "withRequiredSignedIncomingPatch", "withOptionalOwnAdjudication"):
                bound = record[key]
                self.assertEqual(bound["forecast"], record["telemetry"]["lastInputTokens"]
                                 + bound["completeSourceBytes"] + 49000)
                self.assertEqual(bound["excess"], max(0, bound["forecast"] - bound["limit"]))
            self.assertEqual(len(record["exclusions"]), 6)

    def test_current_profile_and_zero_compaction_are_actual_not_fixture(self):
        _, _, capacity, _ = self.tool.modules()
        for family in ("claude", "gpt"):
            record = self.data["families"][family]
            live = (Path.home() / ".copilot" / "session-state" / record["session"] / "events.jsonl").read_bytes()
            measured = capacity.telemetry(self.tool.parse_events(live), {}, family, record["session"])
            self.assertEqual(measured, record["telemetry"])
            self.assertEqual(measured["status"], "PASS")
            self.assertEqual(measured["compactions"], [])
        self.assertEqual(capacity.STARTUP_GATE, 700000)

    def test_claude_is_unconditionally_held_even_without_patch_prompt_or_proof(self):
        record = self.data["families"]["claude"]
        self.assertEqual(record["strictNecessaryUnitsOnly"]["forecast"], 741095)
        self.assertEqual(record["strictNecessaryUnitsOnly"]["excess"], 1095)
        self.assertEqual(record["withRequiredSignedIncomingPatch"]["forecast"], 747479)
        _, raw, _ = self.runtime.selected.retained("claude")
        # Use the actual latest stream (not the earlier held confirmation) for
        # the original public gate: it must reject the measured lower bound.
        live = (Path.home() / ".copilot" / "session-state" / record["session"] / "events.jsonl").read_bytes()
        self.assertNotEqual(sha(live), sha(raw))
        with self.assertRaisesRegex(ValueError, "741095 > 740000"):
            self.tool.context(self.tool.parse_events(live), "claude", record["session"],
                              record["strictNecessaryUnitsOnly"]["completeSourceBytes"])

    def test_gpt_lower_bound_is_not_relabelled_actual_readiness(self):
        record = self.data["families"]["gpt"]
        self.assertEqual(record["withRequiredSignedIncomingPatch"]["forecast"], 545400)
        self.assertEqual(record["withRequiredSignedIncomingPatch"]["status"], "LOWER_BOUND_ONLY_NOT_READINESS")
        self.assertTrue(self.data["noAdmissionOrAcceptance"])
        self.assertTrue(self.data["noReviewerContact"])
        self.assertNotIn("candidate", self.data)


if __name__ == "__main__":
    unittest.main(verbosity=2)
