import unittest

from prepare_b125_confirmations import (exclusions, lf_derivative, neutral_summary, response_is_isolated,
                                        shared_is_neutral)


class IsolationTests(unittest.TestCase):
    def test_shared_evidence_rejects_family_and_verdict_markers(self):
        self.assertTrue(shared_is_neutral("Kanji Pedia 凌 ②おかす".encode("utf-8")))
        for text in ("see claude-response-002.md", "GPT F1", "verdict NEEDS FIX", "CONFIRMED"):
            self.assertFalse(shared_is_neutral(text.encode("utf-8")), text)

    def test_family_response_may_name_only_itself(self):
        self.assertTrue(response_is_isolated("claude", b"# Revised response to Claude-001\n"))
        self.assertFalse(response_is_isolated("claude", b"accepted GPT F1 evidence\n"))
        self.assertFalse(response_is_isolated("gpt", b"the Claude E5 attribution\n"))

    def test_summary_drops_family_responses_and_sense_transcriptions(self):
        proof = {key: key for key in ("batch", "candidate", "parent", "originalCandidate", "signature",
                                      "addedDirectGuards", "dispositionsSha256", "sourceReceiptSha256",
                                      "manifestSha256", "contentVersion", "runtimeEntries", "gates",
                                      "integrityReceipts")}
        proof.update(changedFiles=["kanji/侵.md", "x/claude-response-002.md", "x/gpt-response-002.md"],
                     captures=[{"character": "侵", "url": "u", "sha256": "h", "bytes": 1,
                                "verifiedSenses": ["②"]}],
                     responses={"claude": "a", "gpt": "b"}, observations={"x": 1})
        summary = neutral_summary(proof)
        self.assertEqual(summary["changedFiles"], ["kanji/侵.md"])
        self.assertEqual(summary["captures"], [{"character": "侵", "url": "u", "sha256": "h", "bytes": 1}])
        self.assertNotIn("responses", summary)
        self.assertNotIn("observations", summary)
        self.assertTrue(shared_is_neutral((repr(summary)).encode("utf-8")))


class InputTests(unittest.TestCase):
    def test_lf_derivative_is_exactly_reversible(self):
        raw = "<html>\r\n侵</html>".encode("utf-8")
        self.assertEqual(lf_derivative(raw)[:-1], raw)
        self.assertEqual(lf_derivative(raw)[-1:], b"\n")
        with self.assertRaises(Exception):
            lf_derivative(raw + b"\n")

    def test_exclusions_read_front_matter_lists(self):
        card = "---\ndistractors: [寝, 進, 掃]\nquiz_exclusions: [犯, 凌, 占]\n---\nbody\n".encode("utf-8")
        self.assertEqual(exclusions(card), ("犯凌占", "寝進掃"))
        self.assertEqual(exclusions(card.replace(b"\n", b"\r\n")), ("犯凌占", "寝進掃"))


if __name__ == "__main__":
    unittest.main()
