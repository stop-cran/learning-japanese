"""Negative cases for the additional batch 107 fee exception."""
import copy
import importlib.util
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("fee107", HERE / "audit-fee-followup.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class FeeExceptionTest(unittest.TestCase):
    def setUp(self):
        self.row = copy.deepcopy(audit.EXPECTED)
        self.old = ("---\nword: 勘定\ntitle: reckoning; bill\n"
                    "quiz_exclusions: [計算, 支払う, 給与, 払う, 代金]\n---\n\nOriginal body.\n")
        self.new = self.old.replace(self.row["beforeText"], self.row["afterText"])

    def test_exact_addition_is_accepted(self):
        audit.verify_exception(self.old, self.new, self.row)

    def test_changed_body_or_identity_is_rejected(self):
        for altered in (self.new + "Extra teaching.\n",
                        self.new.replace("reckoning; bill", "different")):
            with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
                audit.verify_exception(self.old, altered, self.row)

    def test_earlier_guard_removal_or_extra_guard_is_rejected(self):
        for altered in (self.new.replace("給与, 払う, 代金, 料金", "給与, 払う, 料金"),
                        self.new.replace("代金, 料金]", "代金, 料金, 他]")):
            with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
                audit.verify_exception(self.old, altered, self.row)

    def test_wrong_ledger_is_rejected(self):
        row = copy.deepcopy(self.row)
        row["otherArticles"] = ["words/代金.md"]
        with self.assertRaisesRegex(ValueError, "exact authorized delta"):
            audit.verify_exception(self.old, self.new, row)

    def test_unrelated_runtime_change_is_rejected(self):
        before = {"schemaVersion": 1, "contentVersion": "old", "files": {"a": "x", "b": "y"}}
        after = {"schemaVersion": 1, "contentVersion": "new", "files": {"a": "z", "b": "changed"}}
        with self.assertRaisesRegex(ValueError, "Changed baseline payload"):
            audit.prior.base.runtime_delta(before, after, set(), {"a"})

    def test_previous_evidence_must_not_change(self):
        audit.prior.verify_historical_changes(
            [("A", "docs/n1-reviews/batch-107-review-846/followup-850/new.json")], [])
        for changed, untracked in (
            ([("M", "docs/n1-reviews/batch-107-review-846/reconciliation-followup.json")], []),
            ([("A", "docs/n1-sources/extra.json")], []),
            ([], ["docs/n1-sources/extra.json"]),
        ):
            with self.assertRaises(ValueError):
                audit.prior.verify_historical_changes(changed, untracked)

    def test_report_and_serial_provenance_are_required(self):
        folder = HERE.parent / "followup-849"
        receipt = json.loads((folder / "confirmation-provenance.json").read_text(encoding="utf-8"))
        reports = {name: (folder / f"confirmation-{name}.md").read_bytes() for name in ("claude", "gpt")}
        audit.verify_reviewers(receipt, reports)
        altered = copy.deepcopy(receipt)
        altered["reviewers"]["gpt"]["overlapCount"] = 1
        with self.assertRaisesRegex(ValueError, "serial-read contract"):
            audit.verify_reviewers(altered, reports)
        altered = copy.deepcopy(receipt)
        altered["reviewers"]["gpt"]["reads"]["gitPointer"]["startedAt"] = "1900"
        with self.assertRaisesRegex(ValueError, "sessions overlapped"):
            audit.verify_reviewers(altered, reports)
        with self.assertRaisesRegex(ValueError, "report changed"):
            audit.verify_reviewers(receipt, {**reports, "claude": reports["claude"] + b" "})


if __name__ == "__main__":
    unittest.main()
