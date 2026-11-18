import unittest

from b129_external_sources import extract_capture


class CitedIdentityTests(unittest.TestCase):
    def capture(self):
        return {"requestUrl": "https://kotobank.jp/word/%E7%B6%BF",
                "finalUrl": "https://kotobank.jp/word/%E7%B6%BF",
                "citedBy": [{"card": "snapshot/kanji/\u7d79.md"}]}

    def test_comparison_source_uses_its_own_headword(self):
        raw = "<html><title>\u7dbf - \u30b3\u30c8\u30d0\u30f3\u30af</title><body><p>complete source</p></body></html>".encode()
        text, error = extract_capture(raw, self.capture())
        self.assertIsNone(error)
        self.assertIn("complete source", text)

    def test_wrong_headword_response_is_rejected(self):
        raw = "<html><title>\u7d79 - \u30b3\u30c8\u30d0\u30f3\u30af</title><body><p>different source</p></body></html>".encode()
        text, error = extract_capture(raw, self.capture())
        self.assertIsNone(text)
        self.assertIn("matching character", error)

    def test_non_character_url_is_not_guessed(self):
        capture = self.capture()
        capture["requestUrl"] = "https://kotobank.jp/word/unknown"
        self.assertIsNone(extract_capture(b"unused", capture)[0])


if __name__ == "__main__":
    unittest.main()
