import unittest

from common import review_dir
from step_v2 import main


class PreflightSelectionTests(unittest.TestCase):
    def test_rejects_preflight_outside_frozen_prompts(self):
        with self.assertRaisesRegex(ValueError, "frozen prompts record"):
            main("118", "claude", "admit", "unused.json", str(review_dir("118") / "preflight.json"))

    def test_rejects_missing_attempt_preflight(self):
        with self.assertRaises(Exception):
            main("118", "claude", "admit", "unused.json", str(review_dir("118") / "prompts" / "preflight-claude-009.json"))


if __name__ == "__main__":
    unittest.main()
