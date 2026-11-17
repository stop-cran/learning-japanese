import copy
import unittest

import b129_source_schema as schema
import verify_b129_sources as verifier
import verify_b126_sources as scan_helper


class B129SchemaTests(unittest.TestCase):
    def selection(self):
        index = {
            "X": {"kanji": "X", "sourceRow": 3, "statusAtFreeze": "pending",
                  "metadata": {"onyomi": ["A", "B"], "kunyomi": [], "meanings": ["silk"]}},
            "Y": {"kanji": "Y", "sourceRow": 5, "statusAtFreeze": "pending",
                  "metadata": {"onyomi": [], "kunyomi": ["C"], "meanings": ["rainbow"]}},
        }
        value = {"batch": "129", "base": "base",
                 "members": [{"kanji": "X", "row": 3}, {"kanji": "Y", "row": 5}]}
        return value, list(index.values()), index

    def scan(self):
        rows = [
            {"kanji": "A", "path": "kanji/A.md", "baselineGitBytesSha256": "a-bytes",
             "title": "unrelated", "meanings": ["cloth", "silk"]},
            {"kanji": "B", "path": "kanji/B.md", "baselineGitBytesSha256": "b-bytes",
             "title": "silk fabric", "meanings": ["cloth"]},
            {"kanji": "C", "path": "kanji/C.md", "baselineGitBytesSha256": "c-bytes",
             "title": "rock", "meanings": ["stone"]},
        ]
        recorded = {
            "base": "base", "kanji": "X", "tokenRegex": "[a-z]+",
            "literalKeywords": ["silk"], "expandedKeywords": ["fabric", "silk"],
            "matches": ["A", "B"],
            "rows": [
                {"kanji": "A", "path": "kanji/A.md", "baselineBytesSha256": "a-bytes",
                 "title": "unrelated", "completeMeanings": ["cloth", "silk"],
                 "matchedKeywords": ["silk"]},
                {"kanji": "B", "path": "kanji/B.md", "baselineBytesSha256": "b-bytes",
                 "title": "silk fabric", "completeMeanings": ["cloth"],
                 "matchedKeywords": ["fabric", "silk"]},
                {"kanji": "C", "path": "kanji/C.md", "baselineBytesSha256": "c-bytes",
                 "title": "rock", "completeMeanings": ["stone"], "matchedKeywords": []},
            ],
        }
        return recorded, rows

    def check_scan(self, recorded, rows, original=None):
        return verifier.verify_scan(recorded, rows, ["silk"], "silk", "base",
                                    scan_helper, original)

    def test_complete_ordered_membership_keeps_all_metadata(self):
        selection, rows, index = self.selection()
        self.assertEqual(
            [{"kanji": "X", "sourceRow": 3}, {"kanji": "Y", "sourceRow": 5}],
            schema.verify_selection(selection, rows, index, ["X", "Y"], "base"))
        for change in ("swap-members", "wrong-row", "drop-reading", "swap-source-rows"):
            selected, source_rows = copy.deepcopy(selection), copy.deepcopy(rows)
            if change == "swap-members":
                selected["members"].reverse()
            elif change == "wrong-row":
                selected["members"][1]["row"] = 6
            elif change == "drop-reading":
                source_rows[0]["metadata"]["onyomi"].pop()
            else:
                source_rows.reverse()
            with self.subTest(change=change), self.assertRaises(ValueError):
                schema.verify_selection(selected, source_rows, index, ["X", "Y"], "base")

    def test_scan_uses_secondary_meanings_and_actual_titles(self):
        recorded, rows = self.scan()
        proof = self.check_scan(recorded, rows)
        self.assertEqual(["A", "B"], proof["matches"])
        self.assertEqual(3, proof["scannedBaselineCards"])
        for field, value in (
            ("completeMeanings", ["cloth"]), ("matchedKeywords", []),
            ("baselineBytesSha256", "changed"),
        ):
            changed = copy.deepcopy(recorded)
            changed["rows"][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "does not reproduce"):
                self.check_scan(changed, rows)
        changed = copy.deepcopy(recorded)
        changed["rows"][1]["title"] = "cloth"
        with self.assertRaisesRegex(ValueError, "does not reproduce"):
            self.check_scan(changed, rows)

    def test_nonmatching_rows_and_match_order_cannot_be_discarded(self):
        recorded, rows = self.scan()
        for change in ("drop-nonmatch", "duplicate-nonmatch", "reorder", "wrong-matches"):
            changed = copy.deepcopy(recorded)
            if change == "drop-nonmatch":
                changed["rows"].pop()
            elif change == "duplicate-nonmatch":
                changed["rows"].append(changed["rows"][-1])
            elif change == "reorder":
                changed["rows"].reverse()
            else:
                changed["matches"].reverse()
            with self.subTest(change=change), self.assertRaisesRegex(ValueError, "does not reproduce"):
                self.check_scan(changed, rows)

    def test_literal_policy_and_previous_expansion_are_preserved(self):
        recorded, rows = self.scan()
        for field, value in (
            ("base", "wrong"), ("tokenRegex", ".*"), ("literalKeywords", []),
            ("expandedKeywords", ["fabric"]), ("expandedKeywords", ["silk", "fabric"]),
            ("expandedKeywords", ["fabric", "silk", "silk"]),
        ):
            changed = copy.deepcopy(recorded)
            changed[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.check_scan(changed, rows)
        original = copy.deepcopy(recorded)
        original["expandedKeywords"].append("textile")
        with self.assertRaisesRegex(ValueError, "drops earlier"):
            self.check_scan(recorded, rows, original)
        original = copy.deepcopy(recorded)
        original["kanji"] = "Y"
        with self.assertRaisesRegex(ValueError, "changes member"):
            self.check_scan(recorded, rows, original)
        self.assertEqual(["A", "B"], self.check_scan(recorded, rows, recorded)["matches"])


if __name__ == "__main__":
    unittest.main()
