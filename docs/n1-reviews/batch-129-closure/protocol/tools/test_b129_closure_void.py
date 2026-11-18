import json
import unittest

from b129_closure_void import bounded_void
from common import WS, frozen, sha


class VoidAuditTests(unittest.TestCase):
    def test_actual_void_audit_retains_numeric_user_message_count(self):
        root = WS / "scratch-129" / "review" / "confirm"
        failure = json.loads(frozen(root / "N1-B129-CLAUDE-CONFIRM-003-superseded.json"))
        raw = frozen(failure["audit"]["path"], failure["audit"]["sha256"])
        audit = json.loads(raw)
        result = bounded_void(audit, sha(raw))
        self.assertEqual(result["unexpectedUserMessagesCount"], audit["unexpectedUserMessages"])
        self.assertEqual(result["chainRead"], 63)
        self.assertFalse(result["confirmationAccepted"])
        self.assertNotIn("calls", result)

    def test_invalid_count_is_rejected(self):
        audit = {"status": "VOID", "reviewerIdle": True, "writes": 0, "readbacks": 0,
                 "messages": ["UNVERIFIED"], "unexpectedUserMessages": -1}
        with self.assertRaises(ValueError):
            bounded_void(audit, "a" * 64)


if __name__ == "__main__":
    unittest.main()
