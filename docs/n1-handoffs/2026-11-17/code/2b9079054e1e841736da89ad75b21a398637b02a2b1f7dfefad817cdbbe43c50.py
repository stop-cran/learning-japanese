import unittest

from verify_b123_revision_v3 import CARD, PREFIX, check_delta, check_followup_metadata


class FollowupTests(unittest.TestCase):
    def test_only_appended_pu_guard_with_preserved_metadata(self):
        before = {"title": "model; standard", "onyomi": ["ハン"], "kunyomi": [],
                  "distractors": ["車", "書", "達"], "quiz_exclusions": list("標紀鏡様格")}
        after = {**before, "quiz_exclusions": [*before["quiz_exclusions"], "普"]}
        check_followup_metadata(before, after)
        for changed in (
            {**after, "title": "widespread"},
            {**after, "quiz_exclusions": [*after["quiz_exclusions"], "測"]},
            {**after, "quiz_exclusions": ["普", *before["quiz_exclusions"]]},
            before,
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                check_followup_metadata(before, changed)

    def test_old_sources_and_other_cards_cannot_change(self):
        valid = f"M\t{CARD}\nM\tmanifest.json\nA\t{PREFIX}query-manifest.json\n"
        self.assertEqual(check_delta(valid), [PREFIX + "query-manifest.json"])
        for changed in (
            valid + "M\tdocs/n1-sources/batch-123/reconciliation-001/pair-dispositions.json\n",
            valid + "M\tkanji/普.md\n",
            valid.replace("A\t", "M\t"),
            valid.replace("M\tmanifest.json\n", ""),
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                check_delta(changed)


if __name__ == "__main__":
    unittest.main()
