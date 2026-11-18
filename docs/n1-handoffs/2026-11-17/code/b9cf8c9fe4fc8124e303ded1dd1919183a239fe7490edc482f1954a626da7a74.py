import unittest

import b127_external_sources as module


class SourceExtractionTests(unittest.TestCase):
    def test_complete_body_preserves_inline_reading_and_source_sections(self):
        raw = ('<html><title>\u5009 | \u6f22\u5b57\u30da\u30c7\u30a3\u30a2</title><body>'
               '<script>not source evidence</script><style>hidden css</style>'
               '<h2>Readings</h2><p><span>\u306b\u308f</span>\u304b</p>'
               '<h2>Other source section</h2><p>keep &amp; retain</p>'
               '<img alt="\u4eba"></body></html>').encode("utf-8")
        text, error = module.extract(raw, "https://www.kanjipedia.jp/kanji/0004231200")
        self.assertIsNone(error)
        self.assertIn("\u306b\u308f\u304b", text)
        self.assertIn("Other source section\nkeep & retain", text)
        self.assertIn("[image alt: \u4eba]", text)
        self.assertNotIn("not source evidence", text)
        self.assertNotIn("hidden css", text)

    def test_wrong_title_or_incomplete_body_is_not_supplied(self):
        for raw in (b"<html><title>Wrong</title><body>text</body></html>",
                    "<title>\u5009 \u30b3\u30c8\u30d0\u30f3\u30af</title><body>unfinished".encode("utf-8")):
            text, error = module.extract(raw, "https://kotobank.jp/word/example")
            self.assertIsNone(text)
            self.assertIsNotNone(error)

    def test_unknown_host_is_not_reinterpreted_as_dictionary(self):
        text, error = module.extract(b"<body>text</body>", "https://example.com/")
        self.assertIsNone(text)
        self.assertIn("Unsupported", error)


if __name__ == "__main__":
    unittest.main()
