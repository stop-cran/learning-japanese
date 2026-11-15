import unittest

from prepare_b123_confirmations_003 import check_isolation


class FollowupIsolationTests(unittest.TestCase):
    def test_shared_sources_cannot_disclose_either_reviewer(self):
        check_isolation(b"Independent source-based nine-pair decisions.\n")
        for raw in (b"GPT says this is fixed.\n", b"initial-claude-001.md\n"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                check_isolation(raw)

    def test_responses_may_name_only_their_own_reviewer(self):
        check_isolation(b"Claude follow-up response.\n", "claude")
        check_isolation(b"GPT follow-up response.\n", "gpt")
        for family, raw in (("claude", b"GPT was unverified.\n"),
                            ("gpt", b"Claude confirmed.\n")):
            with self.subTest(family=family), self.assertRaises(ValueError):
                check_isolation(raw, family)

    def test_line_framing_is_not_silently_rewritten(self):
        with self.assertRaises(ValueError):
            check_isolation(b"Missing final newline")


if __name__ == "__main__":
    unittest.main()
