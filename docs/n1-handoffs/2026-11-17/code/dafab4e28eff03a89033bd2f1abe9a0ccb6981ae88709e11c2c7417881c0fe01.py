import unittest

from verify_b123_followup_selection import check_queries


class FocusedQueries(unittest.TestCase):
    def receipt(self):
        return {"kanjidic2ExactLiterals": ["\u666e"],
                "jmdictExactWrittenQueries": ["\u666e\u304f", "\u666e\u53ca", "\u904d\u304f"],
                "files": dict.fromkeys(["comparison-\u666e.md", "jmdict-records.xml",
                                       "kanjidic2-records.xml"])}

    def test_rejects_broadened_or_duplicate_queries(self):
        for extra in ("\u666e", "\u666e\u304f"):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                receipt = self.receipt()
                receipt["jmdictExactWrittenQueries"].append(extra)
                check_queries(receipt)

    def test_rejects_extra_selection_route_or_unbound_file(self):
        for key, value in (("jmdictExplicitEntryIds", ["1497180"]),
                           ("files", {"comparison-\u666e.md": None})):
            with self.subTest(key=key), self.assertRaises(ValueError):
                receipt = self.receipt()
                receipt[key] = value
                check_queries(receipt)


if __name__ == "__main__":
    unittest.main()
