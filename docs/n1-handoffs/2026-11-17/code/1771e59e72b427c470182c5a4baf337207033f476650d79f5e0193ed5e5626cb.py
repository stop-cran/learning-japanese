import json
import unittest

from common import json_bytes, sha
from prepare_b129_confirmations import neutral_pairs, response


class IsolationTests(unittest.TestCase):
    def test_pair_derivative_preserves_decision_and_evidence(self):
        source = {
            "rows": [{
                "pair": ["A", "B"], "guard": True, "sourceEvidence": {"quote": "positive"},
                "disposition": "Conservative. Preserve Claude's narrower shape-versus-lexical distinction.",
            }]
        }
        raw = json_bytes(source)
        actual = json.loads(neutral_pairs(raw))
        self.assertEqual(actual["rows"][0]["sourceEvidence"], source["rows"][0]["sourceEvidence"])
        self.assertTrue(actual["rows"][0]["guard"])
        self.assertEqual(actual["confirmationDerivative"]["signedSha256"], sha(raw))
        self.assertIn("Preserve the narrower shape-versus-lexical distinction.", actual["rows"][0]["disposition"])

    def test_unanticipated_other_family_reference_is_not_silently_removed(self):
        raw = json_bytes({"first": "Preserve Claude's narrower shape-versus-lexical distinction.",
                          "second": "GPT concluded something"})
        with self.assertRaises(ValueError):
            neutral_pairs(raw)

    def test_only_own_response_provenance_survives(self):
        raw = json_bytes({"originalRun": "N1-B129-GPT-001", "F1":
                          "Preserved Claude's lexical/shape distinction; uncertainty remains."})
        actual = json.loads(response("gpt", raw))
        self.assertEqual(actual["originalRun"], "N1-B129-GPT-001")
        self.assertIn("uncertainty remains.", actual["F1"])
        own = json_bytes({"originalRun": "N1-B129-CLAUDE-001", "O1": "Deferred, not accepted."})
        self.assertEqual(response("claude", own), own)


if __name__ == "__main__":
    unittest.main()
