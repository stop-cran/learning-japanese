import unittest

from verify_b119_followup import verify_pair_change

CARD = """---
kanji: 妥
title: appropriate; settled
onyomi: [ダ]
quiz_exclusions: [安, 円]
---
# 妥

Preserved teaching.

## Notes

- [円](円.md) has a peaceful adjective sense.

Metadata: preserved.
"""
GUARDED = CARD.replace("[安, 円]", "[安, 円, 丸]")
CORRECTED = GUARDED.replace("- [円](円.md)", "- [丸](丸.md) and [円](円.md)")


class DirectPairTests(unittest.TestCase):
    def test_accepts_only_guard_and_qualified_comparison_change(self):
        self.assertEqual(verify_pair_change(CARD, GUARDED)["changedBodyPassages"], 0)
        self.assertEqual(verify_pair_change(CARD, CORRECTED)["changedBodyPassages"], 1)

    def test_rejects_missing_pair_lost_guard_metadata_and_unrelated_teaching(self):
        for revised in (
            CARD, GUARDED.replace("[安, 円, 丸]", "[円, 丸]"),
            GUARDED.replace("[ダ]", "[タ]"),
            CORRECTED.replace("Preserved teaching.", "Changed teaching."),
            CORRECTED.replace("Metadata: preserved.", "Metadata: changed."),
        ):
            with self.subTest(revised=revised), self.assertRaises(ValueError):
                verify_pair_change(CARD, revised)


if __name__ == "__main__":
    unittest.main()
