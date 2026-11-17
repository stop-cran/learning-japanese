import unittest

from verify_b120_correction_v2 import verify_pair_change


CARD = "---\nkanji: 逮\ntitle: arrest; chase\nquiz_exclusions: [捕, 凌]\n---\n"
BODY = "# Meaning\nTeaching.\n\n## Notes\n\n- Existing note.\n\nMetadata: sources.\n"
GUARD = CARD.replace("[捕, 凌]", "[捕, 凌, 押]")
NOTE = "- [押](押.md) has a separately sourced seizing sense.\n"


class PairChangeTests(unittest.TestCase):
    def test_guard_alone_or_one_inserted_note(self):
        self.assertEqual(verify_pair_change(CARD + BODY, GUARD + BODY)["changedBodyPassages"], 0)
        revised = (GUARD + BODY).replace("Metadata:", NOTE + "Metadata:")
        self.assertEqual(verify_pair_change(CARD + BODY, revised)["changedBodyPassages"], 1)

    def test_actual_crlf_markdown_uses_the_same_preservation_rules(self):
        before = (CARD + BODY).replace("\n", "\r\n")
        after = (GUARD + BODY).replace("Metadata:", NOTE + "Metadata:").replace("\n", "\r\n")
        self.assertEqual(verify_pair_change(before, after)["changedBodyPassages"], 1)

    def test_metadata_old_guard_and_unrelated_teaching_must_remain(self):
        for revised in ((GUARD + BODY).replace("arrest; chase", "push"),
                        (GUARD + BODY).replace("[捕, 凌, 押]", "[凌, 押]"),
                        (GUARD + BODY).replace("Teaching.", "Changed teaching."),
                        (GUARD + BODY).replace("- Existing note.", NOTE.strip()),
                        (GUARD + BODY).replace("Metadata:", NOTE + NOTE + "Metadata:")):
            with self.subTest(revised=revised), self.assertRaises(ValueError):
                verify_pair_change(CARD + BODY, revised)


if __name__ == "__main__":
    unittest.main()
