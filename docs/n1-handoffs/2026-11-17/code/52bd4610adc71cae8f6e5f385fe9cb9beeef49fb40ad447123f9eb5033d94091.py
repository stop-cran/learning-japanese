import copy
import unittest

from verify_b132_packet import BASE, MEMBERS, pair_coverage


class B132PairCoverageTests(unittest.TestCase):
    def fixture(self):
        card = {"title": "target", "distractors": ["A"], "quiz_exclusions": ["B"]}
        scan = {"rows": [None] * 1257, "matches": ["B"]}
        comparisons = {"A": ("first", "hash-a"), "B": ("second", "hash-b")}
        pairs = [{"pair": [MEMBERS[0], char], "comparisonTitle": title,
                  "baselineCardSha256": digest, "decision": "curated" if char == "A" else "guard",
                  "scanMatch": char == "B", "targetLabelOnComparison": "first direction",
                  "comparisonLabelOnTarget": "second direction"}
                 for char, (title, digest) in comparisons.items()]
        table = {"base": BASE, "members": [{"kanji": MEMBERS[0], "targetTitle": "target",
                                          "scanRows": 1257, "pairs": pairs}]}
        return table, card, scan, comparisons

    def test_requires_full_finite_membership_and_both_directions(self):
        table, card, scan, comparisons = self.fixture()
        self.assertEqual(pair_coverage(table, card, scan, comparisons), 2)
        for mutation in ("omit", "duplicate", "direction", "snapshot", "guard", "scan"):
            altered = copy.deepcopy(table)
            rows = altered["members"][0]["pairs"]
            if mutation == "omit":
                rows.pop()
            elif mutation == "duplicate":
                rows.append(rows[0])
            elif mutation == "direction":
                rows[0]["comparisonLabelOnTarget"] = " "
            elif mutation == "snapshot":
                rows[0]["baselineCardSha256"] = "other"
            elif mutation == "guard":
                rows[1]["decision"] = "distinct"
            else:
                rows[1]["scanMatch"] = False
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                pair_coverage(altered, card, scan, comparisons)


if __name__ == "__main__":
    unittest.main()
