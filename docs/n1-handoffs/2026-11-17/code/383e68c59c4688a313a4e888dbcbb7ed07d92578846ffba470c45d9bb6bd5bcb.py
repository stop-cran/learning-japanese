import copy
import itertools
import unittest

from verify_b133_packet import BASE, MEMBERS, pair_coverage


class B133FinitePairTests(unittest.TestCase):
    def fixture(self):
        comparisons = {"A": ("alpha", "hashA"), "B": ("beta", "hashB")}
        cards, scans, items = {}, {}, []
        for char in MEMBERS:
            cards[char] = {"title": char, "quiz_exclusions": ["A"], "distractors": ["B"]}
            scans[char] = {"rows": [None] * 1258, "matches": ["A"]}
            items.append({"kanji": char, "targetTitle": char, "scanRows": 1258, "pairs": [
                {"pair": [char, other], "comparisonTitle": comparisons[other][0],
                 "baselineCardSha256": comparisons[other][1],
                 "decision": "guard" if other == "A" else "curated", "scanMatch": other == "A",
                 "additionalSourceDrivenComparison": other == "B",
                 "targetLabelOnComparison": "first direction", "comparisonLabelOnTarget": "second direction"}
                for other in comparisons
            ]})
        disposition = {"base": BASE, "members": items, "newMemberPairs": [
            {"pair": list(pair), "decision": "distinct", "bothDirections": "distinct both ways"}
            for pair in itertools.combinations(MEMBERS, 2)]}
        return disposition, cards, scans, comparisons, {"B"}

    def test_requires_complete_unique_snapshot_bound_bidirectional_pairs(self):
        fixture = self.fixture()
        self.assertEqual(pair_coverage(*fixture), (6, 3))
        for change in ("drop", "duplicate", "wrong-hash", "no-direction", "scan-flag", "additional-flag",
                       "new-pair-drop", "new-direction"):
            altered = copy.deepcopy(fixture)
            rows = altered[0]["members"][0]["pairs"]
            if change == "drop":
                rows.pop(0)
            elif change == "duplicate":
                rows.append(copy.deepcopy(rows[0]))
            elif change == "wrong-hash":
                rows[0]["baselineCardSha256"] = "other"
            elif change == "no-direction":
                rows[0]["targetLabelOnComparison"] = " "
            elif change == "scan-flag":
                rows[0]["scanMatch"] = False
            elif change == "additional-flag":
                rows[1]["additionalSourceDrivenComparison"] = False
            elif change == "new-pair-drop":
                altered[0]["newMemberPairs"].pop()
            else:
                altered[0]["newMemberPairs"][0]["bothDirections"] = ""
            with self.subTest(change=change), self.assertRaises(ValueError):
                pair_coverage(*altered)

    def test_new_guards_are_direct_and_symmetric_not_transitive(self):
        fixture = self.fixture()
        disposition, cards = fixture[:2]
        for row in disposition["newMemberPairs"][:2]:
            row["decision"] = "guard"
            left, right = row["pair"]
            cards[left]["quiz_exclusions"].append(right)
            cards[right]["quiz_exclusions"].append(left)
        self.assertEqual(pair_coverage(*fixture), (6, 3))
        altered = copy.deepcopy(fixture)
        altered[1][MEMBERS[1]]["quiz_exclusions"].remove(MEMBERS[0])
        with self.assertRaises(ValueError):
            pair_coverage(*altered)
        cards[MEMBERS[1]]["quiz_exclusions"].append(MEMBERS[2])
        with self.assertRaises(ValueError):
            pair_coverage(*fixture)


if __name__ == "__main__":
    unittest.main()
