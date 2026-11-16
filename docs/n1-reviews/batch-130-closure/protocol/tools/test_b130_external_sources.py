import unittest

from b130_external_sources import extract_capture


class B130SourceTests(unittest.TestCase):
    def test_numeric_kanjipedia_url_requires_matching_cited_identity(self):
        raw = "<html><title>\u8017 | \u6f22\u5b57\u30da\u30c7\u30a3\u30a2</title><body>first<p>last</p></body></html>".encode()
        capture = {"requestUrl": "https://www.kanjipedia.jp/kanji/0006729100",
                   "finalUrl": "https://www.kanjipedia.jp/kanji/0006729100",
                   "citedBy": [{"card": "snapshot/kanji/\u8017.md"}]}
        text, problem = extract_capture(raw, capture)
        self.assertIsNone(problem)
        self.assertIn("first", text)
        self.assertIn("last", text)
        for citations in ([], [{"card": "snapshot/kanji/\u62cd.md"}],
                          [{"card": "outside/\u8017.md"}],
                          [{"card": "snapshot/kanji/\u8017.md"}, {"card": "snapshot/kanji/\u62cd.md"}]):
            with self.subTest(citations=citations):
                result, error = extract_capture(raw, {**capture, "citedBy": citations})
                self.assertIsNone(result)
                self.assertTrue(error)

    def test_cross_card_kotobank_still_uses_url_headword(self):
        raw = "<html><title>\u6728 \u30b3\u30c8\u30d0\u30f3\u30af</title><body>whole body</body></html>".encode()
        capture = {"requestUrl": "https://kotobank.jp/word/\u6728",
                   "finalUrl": "https://kotobank.jp/word/\u6728",
                   "citedBy": [{"card": "snapshot/kanji/\u8017.md"}]}
        text, problem = extract_capture(raw, capture)
        self.assertIsNone(problem)
        self.assertIn("whole body", text)


if __name__ == "__main__":
    unittest.main()
