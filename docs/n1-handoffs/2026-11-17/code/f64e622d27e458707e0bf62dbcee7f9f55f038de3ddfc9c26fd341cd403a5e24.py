import copy
import unittest

import verify_b126_sources as helper
import verify_b127_sources as verifier


class BaselineScanTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"kanji": "A", "title": "shop", "meanings": ["store", "business"]},
            {"kanji": "B", "title": "put", "meanings": ["keep"]},
            {"kanji": "C", "title": "whole", "meanings": ["complete"]},
        ]
        self.meanings = ["granary", "storehouse"]
        self.original = {
            "baseCommit": verifier.BASE, "newKanji": verifier.MEMBER,
            "newSourceMeanings": self.meanings, "newTitle": "granary; storehouse",
            "literalGlossTokens": sorted(helper.tokens(self.meanings)),
            "caseFoldAndTokenPattern": "[a-z]+", "scannedBaselineCards": 3,
            "expandedSemanticKeywords": sorted(verifier.KEYWORDS),
            "rows": helper.matched_rows(self.rows, verifier.KEYWORDS), "matches": ["A"],
        }
        self.expanded = {
            **copy.deepcopy(self.original), "extends": "baseline-gloss-scan.json",
            "expandedSemanticKeywords": sorted(verifier.KEYWORDS | verifier.EXPANSION),
            "rows": helper.matched_rows(self.rows, verifier.KEYWORDS | verifier.EXPANSION),
            "matches": ["A", "B"],
        }

    def check(self):
        return verifier.verify_scans(self.original, self.expanded, self.rows, self.meanings, helper)

    def test_complete_scans_include_unmatched_rows(self):
        self.assertEqual(self.check()["expandedMatches"], ["A", "B"])

    def test_missing_unmatched_baseline_row_fails(self):
        self.original["rows"].pop()
        with self.assertRaisesRegex(ValueError, "baseline rows"):
            self.check()

    def test_false_secondary_match_fails(self):
        self.expanded["matches"].append("C")
        with self.assertRaisesRegex(ValueError, "baseline matches"):
            self.check()

    def test_omitted_supplemental_token_fails(self):
        self.expanded["expandedSemanticKeywords"].remove("prison")
        with self.assertRaisesRegex(ValueError, "token policy"):
            self.check()

    def test_changed_baseline_source_meaning_fails(self):
        self.original["rows"][0]["meanings"] = ["business"]
        with self.assertRaisesRegex(ValueError, "baseline rows"):
            self.check()


if __name__ == "__main__":
    unittest.main()
