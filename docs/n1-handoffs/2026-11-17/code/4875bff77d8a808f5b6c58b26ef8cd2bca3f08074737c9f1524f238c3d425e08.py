import copy
import unittest

import b132_source_schema as schema
import verify_b126_sources as helper


class B132SourceSchemaTests(unittest.TestCase):
    def test_ordered_membership_requires_complete_frozen_metadata(self):
        index = {
            "X": {"kanji": "X", "sourceRow": 3, "metadata": {"onyomi": ["A", "B"]}},
            "Y": {"kanji": "Y", "sourceRow": 5, "metadata": {"kunyomi": ["C"]}},
        }
        selection = {"batch": 132, "base": "base", "members": ["X", "Y"]}
        rows = list(index.values())
        self.assertEqual(
            [{"kanji": "X", "sourceRow": 3}, {"kanji": "Y", "sourceRow": 5}],
            schema.verify_selection(selection, rows, index, ["X", "Y"], "base"))
        for change in ("batch-string", "wrong-base", "reorder-members", "wrong-row",
                       "drop-reading", "reorder-rows"):
            selected, changed = copy.deepcopy(selection), copy.deepcopy(rows)
            if change == "batch-string":
                selected["batch"] = "132"
            elif change == "wrong-base":
                selected["base"] = "wrong"
            elif change == "reorder-members":
                selected["members"].reverse()
            elif change == "wrong-row":
                changed[0]["sourceRow"] = 4
            elif change == "drop-reading":
                changed[0]["metadata"]["onyomi"].pop()
            else:
                changed.reverse()
            with self.subTest(change=change), self.assertRaises(ValueError):
                schema.verify_selection(selected, changed, index, ["X", "Y"], "base")

    def fixture(self):
        rows = [
            {"kanji": "A", "path": "kanji/A.md", "baselineWorkingBytesSha256": "a-crlf",
             "baselineNormalizedSha256": "a-lf", "title": "other", "meanings": ["cloth", "silk"]},
            {"kanji": "B", "path": "kanji/B.md", "baselineWorkingBytesSha256": "b-lf",
             "baselineNormalizedSha256": "b-lf", "title": "silk fabric", "meanings": ["cloth"]},
            {"kanji": "C", "path": "kanji/C.md", "baselineWorkingBytesSha256": "c-lf",
             "baselineNormalizedSha256": "c-lf", "title": "rock", "meanings": ["stone"]},
        ]
        recorded = {
            "base": "base", "kanji": "X", "tokenRegex": "[a-z]+",
            "literalKeywords": ["silk"], "expandedKeywords": ["fabric", "silk"],
            "matches": ["A", "B"],
            "rows": [
                {"kanji": "A", "path": "kanji/A.md", "baselineWorkingBytesSha256": "a-crlf",
                 "baselineNormalizedSha256": "a-lf", "title": "other",
                 "completeMeanings": ["cloth", "silk"], "matchedKeywords": ["silk"]},
                {"kanji": "B", "path": "kanji/B.md", "baselineWorkingBytesSha256": "b-lf",
                 "baselineNormalizedSha256": "b-lf", "title": "silk fabric",
                 "completeMeanings": ["cloth"], "matchedKeywords": ["fabric", "silk"]},
                {"kanji": "C", "path": "kanji/C.md", "baselineWorkingBytesSha256": "c-lf",
                 "baselineNormalizedSha256": "c-lf", "title": "rock",
                 "completeMeanings": ["stone"], "matchedKeywords": []},
            ],
        }
        return recorded, rows

    def check(self, recorded, rows, original=None):
        return schema.verify_scan(recorded, rows, ["silk"], "silk", "base", helper, original)

    def test_secondary_meanings_titles_and_distinct_byte_hashes(self):
        recorded, rows = self.fixture()
        self.assertEqual(["A", "B"], self.check(recorded, rows)["matches"])
        for field, value in (
            ("baselineWorkingBytesSha256", "a-lf"), ("baselineNormalizedSha256", "a-crlf"),
            ("completeMeanings", ["cloth"]), ("title", "invented"), ("matchedKeywords", []),
        ):
            changed = copy.deepcopy(recorded)
            changed["rows"][0][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "does not reproduce"):
                self.check(changed, rows)

    def test_nonmatches_and_order_remain_required(self):
        recorded, rows = self.fixture()
        for change in ("drop-nonmatch", "duplicate-row", "reorder", "wrong-matches"):
            changed = copy.deepcopy(recorded)
            if change == "drop-nonmatch":
                changed["rows"].pop()
            elif change == "duplicate-row":
                changed["rows"].append(changed["rows"][-1])
            elif change == "reorder":
                changed["rows"].reverse()
            else:
                changed["matches"].reverse()
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.check(changed, rows)

    def test_expansion_cannot_drop_literal_or_previous_keywords(self):
        recorded, rows = self.fixture()
        for field, value in (
            ("base", "wrong"), ("tokenRegex", ".*"), ("literalKeywords", []),
            ("expandedKeywords", ["fabric"]), ("expandedKeywords", ["silk", "fabric"]),
            ("expandedKeywords", ["fabric", "silk", "silk"]),
        ):
            changed = copy.deepcopy(recorded)
            changed[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.check(changed, rows)
        original = copy.deepcopy(recorded)
        original["expandedKeywords"].append("textile")
        with self.assertRaisesRegex(ValueError, "drops earlier"):
            self.check(recorded, rows, original)
        original = copy.deepcopy(recorded)
        original["kanji"] = "Y"
        with self.assertRaisesRegex(ValueError, "changes member"):
            self.check(recorded, rows, original)
        self.assertEqual(3, self.check(recorded, rows, recorded)["scannedBaselineCards"])


if __name__ == "__main__":
    unittest.main()
