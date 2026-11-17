import unittest

from common import frozen
from prepare_b131_confirmation_engine_001 import SOURCE, SOURCE_SHA
from prepare_b131_confirmation_engine_002 import corrected_text


class B131ConfirmationProtocolTests(unittest.TestCase):
    def test_explicit_protocol_tests_and_exclusive_recovery_namespace(self):
        text = corrected_text(frozen(SOURCE, SOURCE_SHA).decode("utf-8"))
        compile(text, "confirm_b131_002.py", "exec")
        self.assertIn("'test-audit-confirm', 'test-confirm-structure'", text)
        self.assertIn('require(re.search(r"Ran [1-9][0-9]* tests"', text)
        self.assertNotIn('"discover"', text)
        self.assertEqual(2, text.count(' / "confirm-002"'))
        self.assertIn('WS / "scratch-116" / "confirm" / name', text)


if __name__ == "__main__":
    unittest.main()
