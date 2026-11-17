import copy
import unittest
from pathlib import Path
from unittest.mock import patch

import confirm_b132 as module


class ActualConfirmationTests(unittest.TestCase):
    def test_capacity_uses_live_tokens_and_all_bytes(self):
        observed = {"status": "PASS", "family": "claude", "lastInputTokens": 300000}
        chain = {"segments": [{"bytes": 200000}, {"bytes": 100000}]}
        result = module.capacity(observed, chain, 10000)
        self.assertEqual(result["projectedPeak"], 652000)
        for value in (dict(observed, lastInputTokens=400000), dict(observed, status="HOLD")):
            with self.assertRaises(ValueError):
                module.capacity(value, chain, 10000)

    def test_original_bindings_and_claim_ids(self):
        for family, ids in (("claude", ["O1", "O2"]), ("gpt", ["Q1", "Q2"])):
            refs, report, actual = module.initial(family, module.INITIALS[family]["session"])
            self.assertEqual(actual, ids)
            self.assertTrue(report)
            self.assertIn("report", refs)
            with self.assertRaises(ValueError):
                module.initial(family, module.INITIALS["gpt" if family == "claude" else "claude"]["session"])

    def test_renderer_preserves_actual_initial_status(self):
        spec = {"family": "gpt", "run": "N1-B132-GPT-CONFIRM-001", "candidate": "a" * 40,
                "scope": ["\u5893"], "dispositionIds": ["Q1", "Q2"],
                "basis": "adjudicated-initial", "priorVerdict": "UNVERIFIED"}
        text = module.render(spec, {"path": "own-report.md"},
                             {"segments": [{"path": "first.txt"}]}, Path("prompt.txt"), Path("report.md"))
        self.assertIn(b"methodologically accepted as UNVERIFIED", text)
        self.assertNotIn(b"and held for open claims", text)
        self.assertIn(b"- Q1 -", text)
        self.assertIn(b"- Q2 -", text)

    def test_context_rejects_compaction_and_changed_model(self):
        events = [
            {"type": "session.start", "data": {"selectedModel": "gpt-6.1-sol", "contextTier": "long_context"}},
            {"type": "session.usage_record", "data": {"usage": {
                "inputTokens": 100, "maxPromptTokens": 922000, "responseModel": "gpt-6.1-sol"}}},
        ]
        import json
        encode = lambda rows: ("\n".join(json.dumps(row) for row in rows) + "\n").encode()
        self.assertEqual(module.context(encode(events), "gpt")["status"], "PASS")
        changed = copy.deepcopy(events)
        changed[1]["data"]["usage"]["responseModel"] = "claude-opus-5.5"
        for rows in (changed, events + [{"type": "session.compaction_start", "data": {}}]):
            with self.assertRaises(ValueError):
                module.context(encode(rows), "gpt")

    def test_build_rejects_substituted_reviewer_before_writing(self):
        spec = {"family": "gpt", "run": "N1-B132-GPT-CONFIRM-001", "candidate": "a" * 40,
                "session": module.INITIALS["claude"]["session"]}
        import json
        with patch.object(module, "frozen", return_value=json.dumps(spec).encode()):
            with self.assertRaisesRegex(ValueError, "original reviewer"):
                module.build(Path("synthetic.json"))


if __name__ == "__main__":
    unittest.main()
