import copy
import unittest

from b129_revision_pairs import PARENT, check_table


class FinitePairTests(unittest.TestCase):
    def setUp(self):
        self.row = {
            "pair": ["A", "B"], "claim": "claim", "guard": True,
            "strongestSecondary": "evidence", "targetLabelOnComparison": "first direction",
            "comparisonLabelOnTarget": "second direction", "disposition": "conservative",
            "guardDeclaration": "kanji/A.md:quiz_exclusions",
        }
        self.table = {"parent": PARENT, "totalPairs": 1, "newDirectGuards": 1,
                      "supportedNoncollisionPairs": [], "rows": [self.row]}
        self.cards = {"A": {"quiz_exclusions": ["B"], "distractors": ["C"]}}

    def check(self):
        return check_table(self.table, {("A", "B"): "claim"}, self.cards)

    def test_exact_guard_and_explicit_noncollision(self):
        self.check()
        self.row.update(guard=False, guardDeclaration=None)
        self.table.update(newDirectGuards=0, supportedNoncollisionPairs=[["A", "B"]])
        self.cards["A"]["quiz_exclusions"] = []
        self.check()

    def test_duplicate_or_unresolved_direction_rejected(self):
        self.table["rows"].append(copy.deepcopy(self.row))
        with self.assertRaises(ValueError):
            self.check()
        self.table["rows"].pop()
        self.row["comparisonLabelOnTarget"] = ""
        with self.assertRaises(ValueError):
            self.check()

    def test_unimplemented_guard_or_curated_collision_rejected(self):
        self.cards["A"]["quiz_exclusions"] = []
        with self.assertRaises(ValueError):
            self.check()
        self.cards["A"]["quiz_exclusions"] = ["B"]
        self.cards["A"]["distractors"] = ["B"]
        with self.assertRaises(ValueError):
            self.check()


if __name__ == "__main__":
    unittest.main()
