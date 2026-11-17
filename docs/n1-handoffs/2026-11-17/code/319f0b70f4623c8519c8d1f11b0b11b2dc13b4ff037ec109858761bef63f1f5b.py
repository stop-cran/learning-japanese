import json
import unittest

from common import WS
from prepare_b127_confirmations import neutral_receipt, response_is_isolated, shared_is_neutral
from test_verify_b127_reconciliation import ReconciliationTests
from verify_b127_reconciliation import PREFIX


class IsolationTests(unittest.TestCase):
    def test_receipt_derivative_preserves_all_source_fields(self):
        source = json.loads((WS / "b127-worktree" / PREFIX / "source-receipt.json").read_bytes())
        result = neutral_receipt(source)
        self.assertIn("admissionBindings", source)
        self.assertNotIn("admissionBindings", result)
        self.assertEqual({k: v for k, v in result.items() if k != "derivation"},
                         {k: v for k, v in source.items() if k != "admissionBindings"})
        self.assertTrue(shared_is_neutral(json.dumps(result, ensure_ascii=False).encode()))
        self.assertFalse(shared_is_neutral(json.dumps(source, ensure_ascii=False).encode()))

    def test_other_family_and_verdict_leaks_are_rejected(self):
        for family, other in (("claude", "GPT"), ("gpt", "Claude")):
            self.assertTrue(response_is_isolated(family, f"{family}: own report".encode()))
            self.assertFalse(response_is_isolated(family, f"{other} approved this".encode()))
        self.assertFalse(shared_is_neutral(b"Prior verdict was CONFIRMED"))

    def test_actual_family_responses_are_isolated(self):
        for family in ("claude", "gpt"):
            raw = (WS / "b127-worktree" / PREFIX / f"{family}-author-response.md").read_bytes()
            self.assertTrue(response_is_isolated(family, raw))


if __name__ == "__main__":
    unittest.main(verbosity=2)
