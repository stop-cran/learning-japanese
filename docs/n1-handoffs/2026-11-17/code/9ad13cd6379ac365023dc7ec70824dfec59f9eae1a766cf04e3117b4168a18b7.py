import unittest

from snapshot_b129_noose import CHARACTER, URL, extract_noose


class ExactCompoundTests(unittest.TestCase):
    def test_complete_compound_source_is_retained(self):
        raw = (f"<html><title>{CHARACTER}(reading) - \u30b3\u30c8\u30d0\u30f3\u30af</title>"
               "<body><p>first sense</p><p>secondary discrepancy</p></body></html>").encode()
        text, error = extract_noose(raw, {"requestUrl": URL, "finalUrl": URL + "-491940"})
        self.assertIsNone(error)
        self.assertIn("first sense\nsecondary discrepancy", text)

    def test_single_constituent_or_other_redirect_is_rejected(self):
        capture = {"requestUrl": URL, "finalUrl": URL + "-491940"}
        raw = (f"<html><title>{CHARACTER[1]}(reading) - \u30b3\u30c8\u30d0\u30f3\u30af</title>"
               "<body>wrong headword</body></html>").encode()
        with self.assertRaises(ValueError):
            extract_noose(raw, capture)
        capture["finalUrl"] = "https://example.com/word"
        with self.assertRaises(ValueError):
            extract_noose(raw, capture)


if __name__ == "__main__":
    unittest.main()
