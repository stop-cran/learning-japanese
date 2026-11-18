import copy
import unittest

from prepare_b124_confirmations_002 import neutralize


class FollowupIsolationTests(unittest.TestCase):
    def test_only_report_provenance_removed_from_source_receipt(self):
        original = {"confirmationBindings": {"claude": "private", "gpt": "private"},
                    "reusedSourceContract": {"selectors": ["all", "complete"], "sha256": "hash"},
                    "supplementalTargetSource": {"relevantText": "roominess"},
                    "limits": ["not exhaustive"]}
        before = copy.deepcopy(original)
        value, pointers = neutralize("source-receipt.json", original)
        self.assertEqual(original, before)
        self.assertEqual(value, {key: item for key, item in original.items() if key != "confirmationBindings"})
        self.assertEqual(pointers, ["/confirmationBindings"])

    def test_keeps_conservative_claims_labels_and_superseded_judgments(self):
        original = {"confirmationStatus": {"gpt": "held"}, "dispositions": [
            {"id": "Q1", "decision": "conservative-direct-guard", "candidateLabel": "exact, punctuation",
             "reviewFinding": False, "evidence": {"selectors": {"1": ["all"]}}}],
                    "supersededPriorJudgments": {"reason": "Conservative choice, not universal synonymy"}}
        before = copy.deepcopy(original)
        value, _ = neutralize("dispositions.json", original)
        self.assertEqual(original, before)
        self.assertEqual(value["dispositions"], original["dispositions"])
        self.assertEqual(value["supersededPriorJudgments"], original["supersededPriorJudgments"])

    def test_selection_keeps_exact_guards_and_membership(self):
        original = {"membership": [{"kanji": "x", "sourceRow": 986}], "directMeaningGuards": ["a", "b"],
                    "reconciliation": {"reviewResponses": {}, "rawConfirmationVerdicts": {},
                                       "reviewEvidenceAccepted": True, "confirmationAccepted": False,
                                       "additionalConservativeGuards": ["b"], "sourceReceiptSha256": "source",
                                       "supersededNoNewGuardClaims": ["Q1"]}}
        value, pointers = neutralize("selection-005.json", original)
        self.assertEqual(value["membership"], original["membership"])
        self.assertEqual(value["directMeaningGuards"], ["a", "b"])
        self.assertEqual(value["reconciliation"], {
            "additionalConservativeGuards": ["b"], "sourceReceiptSha256": "source",
            "supersededNoNewGuardClaims": ["Q1"]})
        self.assertEqual(len(pointers), 4)


if __name__ == "__main__":
    unittest.main()
