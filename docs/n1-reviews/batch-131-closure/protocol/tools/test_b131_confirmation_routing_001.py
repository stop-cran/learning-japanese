import copy
import datetime
import json
import unittest
import b131_confirmation_routing_001 as routing
from common import frozen
from prepare_b131_confirmation_engine_001 import SOURCE, SOURCE_SHA, derive_text


class B131ConfirmationRoutingTests(unittest.TestCase):
    def test_exact_accepted_initial_namespaces_and_reviewer_identity(self):
        for family, expected in routing.INITIALS.items():
            root = routing.initial_directory(family)
            path = root / (expected["run"] + "-acceptance.json")
            accepted = json.loads(frozen(path, expected["acceptanceSha256"]))
            launch = json.loads(frozen(root / (expected["run"] + "-launch.json")))
            config = {"batch": 131, "candidate": routing.PARENT}
            spec = {"batch": 131, "family": family, "session": expected["session"],
                    "acceptance": {"path": str(path), "sha256": expected["acceptanceSha256"]}}
            routing.check_lineage(spec, accepted, launch, config)
            for change in ({"session": "other-reviewer"}, {"batch": 130},
                           {"acceptance": {**spec["acceptance"], "path": str(routing.ROOT / path.name)}}):
                with self.subTest(family=family, change=change), self.assertRaises(ValueError):
                    routing.check_lineage({**spec, **change}, accepted, launch, config)
            with self.assertRaises(ValueError):
                routing.check_lineage(spec, {**accepted, "reviewAccepted": False}, launch, config)
            with self.assertRaises(ValueError):
                routing.check_lineage(spec, {**accepted, "run": "N1-B131-GPT-003"}, launch, config)

    def test_derived_engine_binds_both_context_paths_and_preserves_auditor_rules(self):
        source = frozen(SOURCE, SOURCE_SHA).decode("utf-8")
        derived = derive_text(source)
        self.assertIn('initial_launch(spec, accepted, config)', derived)
        self.assertIn('check_context(events, config["expectedFamily"])', derived)
        self.assertIn('check_context(audit_path.parent / "events.jsonl", config["expectedFamily"])', derived)
        self.assertNotIn("b130_compact_common", derived)
        self.assertNotIn("b127_lifecycle_process", derived)
        self.assertIn('audit["writes"] == audit["readbacks"] == 1', derived)
        self.assertIn('audit["chainRead"] == audit["chainRequired"]', derived)
        with self.assertRaises(ValueError):
            derive_text(source.replace('accepted.get("reviewAccepted")', 'accepted.get("accepted")')
                        .replace('report.exists()', 'report.is_file()'))

    def test_family_specific_checkers_reject_wrong_exact_profile_and_compaction(self):
        from b131_capacity_003 import PROFILES, telemetry
        forecast = {"bootstrapTokens": 80000, "coreTokens": 400000}
        for family, profile in PROFILES.items():
            events = [
                {"type": "session.start", "data": {"selectedModel": profile["selectedModel"],
                                                   "contextTier": "long_context"}},
                {"type": "session.usage_record", "data": {"usage": {
                    "inputTokens": 300000, "maxPromptTokens": profile["maxPromptTokens"],
                    "model": profile["selectedModel"]}}},
            ]
            self.assertEqual("PASS", telemetry(events, forecast, family)["status"])
            other = "gpt" if family == "claude" else "claude"
            self.assertEqual("HOLD", telemetry(events, forecast, other)["status"])
            compacted = events + [{"type": "session.compaction_start", "data": {}}]
            self.assertEqual("HOLD", telemetry(compacted, forecast, family)["status"])

    def test_full_roster_and_chain_capacity_are_required_before_delivery(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        status = {"summary": {"total": 2}, "sessions": [
            {"id": routing.COORDINATOR, "name": "Coordinator", "activity": {"status": "busy"}},
            {"id": "reviewer", "name": "Original reviewer", "activity": {"status": "idle"}},
        ]}
        roster = [{"id": routing.COORDINATOR}, {"id": "reviewer"}]
        routing.check_roster(status, roster, "reviewer", now, now)
        for state in ("busy", "unknown"):
            bad = copy.deepcopy(status)
            bad["sessions"][1]["activity"]["status"] = state
            with self.subTest(state=state), self.assertRaises(ValueError):
                routing.check_roster(bad, roster, "reviewer", now, now)
        with self.assertRaises(ValueError):
            routing.check_roster(status, roster[:1], "reviewer", now, now)
        with self.assertRaises(ValueError):
            routing.check_roster(status, roster, "reviewer", now - datetime.timedelta(seconds=120), now)
        context = {"status": "PASS", "exactProfile": {"lastInputTokens": 554904}}
        self.assertLessEqual(routing.capacity_check(context, {"segments": [{"bytes": 100000}]})["projectedPeak"],
                             700000)
        with self.assertRaises(ValueError):
            routing.capacity_check(context, {"segments": [{"bytes": 200000}]})


if __name__ == "__main__":
    unittest.main()
