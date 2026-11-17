import copy
import unittest

from prepare_b124_confirmations import neutralize


class NeutralSourceTests(unittest.TestCase):
    def test_receipt_retains_all_source_and_selector_information(self):
        original = {"immutableInputs": {"report": "private"}, "reviewReportBindings": {"other": "private"},
                    "dictionaryInputs": {"complete": ["a", "b"]}, "files": {"source.xml": {"sha256": "hash"}},
                    "limits": ["not exhaustive"]}
        before = copy.deepcopy(original)
        value, removed = neutralize("source-receipt.json", original)
        self.assertEqual(original, before)
        self.assertEqual(value, {key: item for key, item in original.items()
                                 if key not in ("immutableInputs", "reviewReportBindings")})
        self.assertEqual(len(removed), 2)

    def test_pair_claims_and_exact_queries_are_not_rewritten(self):
        rows = [{"id": "Q1", "decision": "no-new-guard", "strongestOverlap": "wealth",
                 "limits": ["uncertain"], "sources": ["complete.xml"]}]
        original = {"sourceBindings": {"reviewReports": {"other": "private"}, "xml": "hash"},
                    "dispositions": rows}
        value, _ = neutralize("dispositions.json", original)
        self.assertEqual(value["dispositions"], rows)
        self.assertEqual(value["sourceBindings"], {"xml": "hash"})
        selection = {"claimInventory": [{"id": "Q1", "kanji": "x", "reviewRows": ["other F1"]}],
                     "exactJmdictQueriesByClaim": {"Q1": ["one", "two"]}}
        selected, _ = neutralize("selection.json", selection)
        self.assertEqual(selected["claimInventory"], [{"id": "Q1", "kanji": "x"}])
        self.assertEqual(selected["exactJmdictQueriesByClaim"], selection["exactJmdictQueriesByClaim"])


if __name__ == "__main__":
    unittest.main()
