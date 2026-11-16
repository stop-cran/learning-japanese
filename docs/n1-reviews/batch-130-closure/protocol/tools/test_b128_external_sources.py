import unittest

import b128_external_sources as module


class SourceIdentityTests(unittest.TestCase):
    def test_new_character_preserves_complete_body_and_inline_reading(self):
        raw = ('<html><title>\u501f | \u6f22\u5b57\u30da\u30c7\u30a3\u30a2</title><body>'
               '<script>not evidence</script><h2>Reading</h2>'
               '<p><span>\u304b</span>\u308a\u308b</p><h2>Secondary sense</h2>'
               '<p>keep &amp; retain</p><img alt="\u4eba"></body></html>').encode("utf-8")
        text, error = module.extract(raw, "https://www.kanjipedia.jp/kanji/example", ["\u501f"])
        self.assertIsNone(error)
        self.assertIn("\u304b\u308a\u308b", text)
        self.assertIn("Secondary sense\nkeep & retain", text)
        self.assertIn("[image alt: \u4eba]", text)
        self.assertNotIn("not evidence", text)

    def test_old_batch_character_is_not_accepted_for_new_card(self):
        raw = ('<title>\u5009 | \u30b3\u30c8\u30d0\u30f3\u30af</title>'
               '<body>complete but unrelated source</body>').encode("utf-8")
        text, error = module.extract(raw, "https://kotobank.jp/word/example", ["\u501f"])
        self.assertIsNone(text)
        self.assertIn("matching character", error)

    def test_missing_or_malformed_character_identity_is_explicitly_unsupplied(self):
        raw = ('<title>\u501f | \u30b3\u30c8\u30d0\u30f3\u30af</title>'
               '<body>text</body>').encode("utf-8")
        for characters in ([], [""], [None], ["two"]):
            with self.subTest(characters=characters):
                text, error = module.extract(raw, "https://kotobank.jp/word/example", characters)
                self.assertIsNone(text)
                self.assertIn("single-character", error)

    def test_numeric_entity_title_matches_bound_character(self):
        raw = ('<title>&#20511; | \u30b3\u30c8\u30d0\u30f3\u30af</title>'
               '<body>complete text</body>').encode("utf-8")
        text, error = module.extract(raw, "https://kotobank.jp/word/example", ["\u501f"])
        self.assertIsNone(error)
        self.assertIn("complete text", text)


if __name__ == "__main__":
    unittest.main()
