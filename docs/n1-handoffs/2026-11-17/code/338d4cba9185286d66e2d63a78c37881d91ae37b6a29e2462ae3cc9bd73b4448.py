import unittest

from prepare_b128_confirmations import (NOTES_HEADING, neutral_receipt, notes_delta, response_is_isolated,
                                        shared_is_neutral)

DELTA = ("diff --git a/docs/n1-authoring-notes.md b/docs/n1-authoring-notes.md\n"
         "--- a/docs/n1-authoring-notes.md\n+++ b/docs/n1-authoring-notes.md\n"
         "@@ -83,0 +84,2 @@ delivered.\n" + NOTES_HEADING + "\n+\n")


class NeutralityTests(unittest.TestCase):
    def test_ordinary_prose_is_shareable(self):
        self.assertTrue(shared_is_neutral("it is not a clean opposite; confirmed by records".encode()))

    def test_verdicts_and_families_leak(self):
        for text in ("Facet: CLEAN", "NEEDS FIX", "UNVERIFIED", "CONFIRMED", "Claude", "gpt-5", "Opus"):
            self.assertFalse(shared_is_neutral(text.encode()), text)

    def test_response_isolation(self):
        self.assertTrue(response_is_isolated("claude", b"Response to Claude F1"))
        self.assertFalse(response_is_isolated("claude", b"Claude and GPT"))
        self.assertFalse(response_is_isolated("gpt", b"no family"))

    def test_receipt_omits_only_admission(self):
        receipt = {"recordCounts": {"jmdict": 50}, "admissionBindings": {"claude": 1}}
        result = neutral_receipt(receipt)
        self.assertEqual(set(result), {"recordCounts", "derivation"})
        self.assertEqual(result["recordCounts"], receipt["recordCounts"])
        self.assertIn("admissionBindings", receipt)


class NotesDeltaTests(unittest.TestCase):
    def test_single_insertion(self):
        self.assertEqual(notes_delta(DELTA.encode()), DELTA.encode())

    def test_rejects_removal_extra_hunk_or_wrong_section(self):
        for bad in (DELTA + "-old\n", DELTA + "@@ -90,0 +93,1 @@\n+x\n",
                    DELTA.replace(NOTES_HEADING, "+### Batch 127")):
            with self.assertRaises(ValueError):
                notes_delta(bad.encode())


if __name__ == "__main__":
    unittest.main()
