import json
import unittest

from b129_confirmation_presentation import (
    canonical, compact_xml, kd_projection, lexical_articles, named_section, pair_projection,
)


class PresentationTests(unittest.TestCase):
    def test_complete_xml_preserves_restrictions_and_secondary_senses(self):
        raw = b'<JMdict>\n <entry><ent_seq>1</ent_seq><sense><stagk>x</stagk><gloss>first</gloss></sense><sense><misc>archaic</misc><gloss>second</gloss></sense></entry>\n</JMdict>'
        result = compact_xml(raw)
        self.assertEqual(canonical(result), canonical(raw))
        self.assertIn(b"second", result)

    def test_reading_projection_retains_all_english_and_reading_attributes(self):
        raw = b'<kanjidic2><character><literal>X</literal><codepoint>x</codepoint><misc><grade>1</grade></misc><reading_meaning><rmgroup><reading r_type="ja_on" r_status="jy">A</reading><meaning>first</meaning><meaning m_lang="en">second</meaning><meaning m_lang="fr">un</meaning></rmgroup><nanori>N</nanori></reading_meaning></character></kanjidic2>'
        result, omitted = kd_projection(raw)
        for retained in (b"first", b"second", b'r_status="jy"', b"<nanori>N</nanori>", b"<grade>1</grade>"):
            self.assertIn(retained, result)
        self.assertEqual(omitted["X"], ["codepoint", "meaning:fr"])
        self.assertIn(b"meaning", raw)

    def test_article_selection_keeps_the_whole_dictionary_entry(self):
        raw = ('<title>X | \u30b3\u30c8\u30d0\u30f3\u30af</title><body>'
               '<article id="d" class="dictype daijisen"><p>first <b>sense</b></p>'
               '<p>second sense<img alt="unread glyph"></p><script>hidden</script>'
               '<a data-title="hidden <b>attribute</b>">visible</a></article>'
               '<article id="e" class="encyclopedia">unrelated</article></body>').encode()
        records, omitted = lexical_articles(raw, "https://kotobank.jp/word/X", "X")
        self.assertEqual(len(records), 1)
        self.assertIn("first sense", records[0]["text"])
        self.assertIn("second sense", records[0]["text"])
        self.assertIn("[image alt: unread glyph]", records[0]["text"])
        self.assertNotIn("hidden", records[0]["text"])
        self.assertNotIn("attribute", records[0]["text"])
        self.assertIn("visible", records[0]["text"])
        self.assertEqual(omitted, [{"id": "e", "class": "encyclopedia"}])

    def test_unclosed_article_fails_instead_of_truncating(self):
        raw = '<title>X | \u30b3\u30c8\u30d0\u30f3\u30af</title><article class="jitsu">first'.encode()
        with self.assertRaises(ValueError):
            lexical_articles(raw, "https://kotobank.jp/word/X", "X")

    def test_pair_projection_does_not_change_arguments_or_disposition(self):
        row = {"pair": ["A", "B"], "guard": False, "disposition": "uncertain",
               "strongestSecondary": "secondary", "completeJmdictFamilies": {"1": {"hash": "x"}},
               "comparison": {"rawSha256": "x", "title": "B"},
               "sourceEvidence": {"rawCaptureSha256": "x", "completeSelectedTextSha256": "y",
                                  "boundedExcerpt": "contrary evidence"}}
        result = pair_projection(json.dumps({"rows": [row]}).encode())["rows"][0]
        self.assertEqual(result["disposition"], "uncertain")
        self.assertFalse(result["guard"])
        self.assertEqual(result["sourceEvidence"]["boundedExcerpt"], "contrary evidence")
        self.assertEqual(result["completeJmdictFamilyIds"], ["1"])

    def test_named_section_includes_all_lines_until_the_next_section(self):
        raw = b'Weblio source section: Other\nx\nWeblio source section: Target\nfirst\nsecond\n\nWeblio source section: Next\ny\n'
        selected, bounds = named_section(raw, "Target")
        self.assertEqual(bounds, [3, 6])
        self.assertIn(b"first\nsecond\n", selected)
        self.assertNotIn(b"Next", selected)


if __name__ == "__main__":
    unittest.main()
