import copy
import io
import unittest

from verify_b126_sources import (
    BASE, EXPANSION, KEYWORDS, MEMBER, STOPWORDS, matched_rows, scan_baseline,
    single_headword_glosses, tokens, verify_scans,
)


class Guard:
    def check(self):
        pass


class BaselineScanTests(unittest.TestCase):
    def test_preserves_all_english_groups_and_scans_title_polysemy(self):
        raw = b"""<kanjidic2><character><literal>X</literal><reading_meaning>
        <rmgroup><meaning>unrelated</meaning><meaning m_lang="fr">shade</meaning></rmgroup>
        <rmgroup><meaning>cover</meaning></rmgroup></reading_meaning></character>
        <character><literal>Y</literal></character></kanjidic2>"""
        rows = scan_baseline(io.BytesIO(raw), {
            "Y": {"kanji": "Y", "title": "umbrella"},
            "X": {"kanji": "X", "title": "rest"},
        }, Guard())
        self.assertEqual(["X", "Y"], [row["kanji"] for row in rows])
        self.assertEqual(["unrelated", "cover"], rows[0]["meanings"])
        self.assertEqual([["cover"], ["umbrella"]],
                         [row["matchedWords"] for row in matched_rows(rows, KEYWORDS)])

    def test_missing_or_duplicate_baseline_character_fails(self):
        for raw, message in (
            (b"<kanjidic2/>", "Missing baseline"),
            (b"<kanjidic2><character><literal>X</literal></character>"
             b"<character><literal>X</literal></character></kanjidic2>", "Duplicate baseline"),
        ):
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                scan_baseline(io.BytesIO(raw), {"X": {"title": "cover"}}, Guard())

    def test_whole_compound_does_not_supply_single_headword_glosses(self):
        raw = (f"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>{MEMBER}</keb></k_ele>"
               "<sense><gloss>umbrella</gloss></sense><sense><gloss>cap</gloss></sense></entry>"
               f"<entry><ent_seq>2</ent_seq><k_ele><keb>{MEMBER}X</keb></k_ele>"
               "<sense><gloss>affiliation</gloss></sense></entry></JMdict>").encode()
        self.assertEqual((["1"], ["umbrella", "cap"]), single_headword_glosses(raw))

    def test_scan_reproduction_rejects_changed_policy_rows_or_source_binding(self):
        jm = (f"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>{MEMBER}</keb></k_ele>"
              "<sense><gloss>umbrella or a cap</gloss></sense></entry></JMdict>").encode()
        rows = [{"kanji": "X", "title": "cap", "meanings": ["unrelated"],
                 "path": "kanji/X.md", "baselineRawSha256": "raw-hash"}]
        expanded_tokens = (tokens(["umbrella or a cap"]) - STOPWORDS) | KEYWORDS | EXPANSION
        first, second = matched_rows(rows, KEYWORDS), matched_rows(rows, expanded_tokens)
        original = {
            "baseCommit": BASE, "newKanji": MEMBER, "newSourceMeanings": ["umbrella"],
            "newTitle": "umbrella; parasol", "literalGlossTokens": ["umbrella"],
            "expandedSemanticKeywords": sorted(KEYWORDS), "caseFoldAndTokenPattern": "[a-z]+",
            "scannedBaselineCards": 1, "matches": [], "rows": first,
        }
        expanded = {
            "baseCommit": BASE, "newKanji": MEMBER,
            "extends": {"file": "baseline-gloss-scan.json", "sha256": "scan-hash"},
            "singleCharacterJmdictEntries": ["1"], "allSingleCharacterJmdictGlosses": ["umbrella or a cap"],
            "sourceMeanings": ["umbrella"], "omittedFunctionTokens": sorted(STOPWORDS),
            "scanTokens": sorted(expanded_tokens), "scannedBaselineCards": 1, "matches": ["X"],
            "rows": second,
        }
        self.assertEqual(["X"], verify_scans(
            original, expanded, rows, ["umbrella"], jm, "scan-hash")["expandedMatches"])
        for field, value in (
            ("matches", []), ("rows", []), ("scannedBaselineCards", 0),
            ("scanTokens", ["umbrella"]), ("allSingleCharacterJmdictGlosses", ["umbrella"]),
            ("extends", {"file": "baseline-gloss-scan.json", "sha256": "different"}),
        ):
            changed = copy.deepcopy(expanded)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_scans(original, changed, rows, ["umbrella"], jm, "scan-hash")
        changed = copy.deepcopy(original)
        changed["rows"][0]["baselineRawSha256"] = "different"
        with self.assertRaisesRegex(ValueError, "does not reproduce"):
            verify_scans(changed, expanded, rows, ["umbrella"], jm, "scan-hash")


if __name__ == "__main__":
    unittest.main()
