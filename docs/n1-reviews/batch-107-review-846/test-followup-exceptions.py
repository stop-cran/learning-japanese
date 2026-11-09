"""Negative cases for the additional batch 107 payment exceptions."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("followup107", HERE / "audit-followup-exceptions.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class FollowupExceptionTest(unittest.TestCase):
    def setUp(self):
        self.row = copy.deepcopy(audit.EXPECTED)
        self.old = ("---\nword: 勘定\ntitle: reckoning; bill\n"
                    "quiz_exclusions: [計算, 支払う, 給与]\n---\n\nOriginal body.\n")
        self.new = self.old.replace(self.row["beforeText"], self.row["afterText"])

    def test_exact_additions_are_accepted(self):
        audit.verify_exception(self.old, self.new, self.row)

    def test_changed_body_or_identity_is_rejected(self):
        for altered in (self.new + "Extra teaching.\n",
                        self.new.replace("reckoning; bill", "different")):
            with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
                audit.verify_exception(self.old, altered, self.row)

    def test_removing_an_earlier_guard_is_rejected(self):
        altered = self.new.replace("計算, 支払う, 給与, 払う, 代金", "計算, 給与, 払う, 代金")
        with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
            audit.verify_exception(self.old, altered, self.row)

    def test_unreviewed_or_duplicate_guard_is_rejected(self):
        for altered in (self.new.replace("払う, 代金]", "払う, 代金, 料金]"),
                        self.new.replace("払う, 代金]", "払う, 代金, 払う]")):
            with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
                audit.verify_exception(self.old, altered, self.row)

    def test_wrong_ledger_is_rejected(self):
        row = copy.deepcopy(self.row)
        row["otherArticles"] = ["words/料金.md"]
        with self.assertRaisesRegex(ValueError, "exact authorized delta"):
            audit.verify_exception(self.old, self.new, row)

    def test_unrelated_runtime_change_is_rejected(self):
        before = {"schemaVersion": 1, "contentVersion": "old", "files": {"a": "x", "b": "y"}}
        after = {"schemaVersion": 1, "contentVersion": "new", "files": {"a": "z", "b": "changed"}}
        with self.assertRaisesRegex(ValueError, "Changed baseline payload"):
            audit.base.runtime_delta(before, after, set(), {"a"})

    def test_previous_evidence_must_not_change(self):
        audit.verify_historical_changes([("A", "docs/n1-reviews/batch-107-review-846/new.json")], [])
        for changed, untracked in (
            ([("M", "docs/n1-reviews/batch-107-review-846/reconciliation.json")], []),
            ([("A", "docs/n1-sources/extra.json")], []),
            ([], ["docs/n1-sources/extra.json"]),
        ):
            with self.assertRaises(ValueError):
                audit.verify_historical_changes(changed, untracked)

    def test_additional_source_bytes_and_provenance_are_required(self):
        raw = (HERE / "followup-payment-jmdict.xml").read_bytes()
        receipt = json.loads((HERE / "followup-payment-jmdict-provenance.json").read_text(encoding="utf-8"))
        audit.verify_additional_source(raw, receipt)
        for altered_raw, altered_receipt in (
            (raw + b" ", receipt),
            (raw, {**receipt, "entryIds": ["1411790"]}),
            (raw, {**receipt, "compressedSourceSha256": "wrong"}),
        ):
            with self.assertRaises(ValueError):
                audit.verify_additional_source(altered_raw, altered_receipt)


if __name__ == "__main__":
    unittest.main()
