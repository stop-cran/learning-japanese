"""Negative cases for the exact, additive batch 107 review exceptions."""
import copy
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "batch107_review_audit", Path(__file__).with_name("audit-reviewed-exceptions.py"))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class ReviewedExceptionTest(unittest.TestCase):
    def setUp(self):
        self.name = "words/勘定.md"
        self.row = {"article": self.name, **copy.deepcopy(audit.EXCEPTIONS[self.name])}
        self.old = ("---\nword: 勘定\ntitle: reckoning; bill\nquiz_exclusions: [計算]\n"
                    "---\n\nOriginal body.\n")
        self.new = self.old.replace(self.row["beforeText"], self.row["afterText"])

    def test_exact_addition_is_accepted(self):
        audit.verify_exception(self.old, self.new, self.row)

    def test_changed_body_or_identity_is_rejected(self):
        for altered in (self.new + "Extra teaching.\n",
                        self.new.replace("reckoning; bill", "different")):
            with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
                audit.verify_exception(self.old, altered, self.row)

    def test_removed_previous_guard_is_rejected(self):
        altered = self.new.replace("[計算, 支払う, 給与]", "[支払う, 給与]")
        with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
            audit.verify_exception(self.old, altered, self.row)

    def test_duplicate_or_unreviewed_guard_is_rejected(self):
        for altered in (self.new.replace("[計算, 支払う, 給与]", "[計算, 支払う, 給与, 支払う]"),
                        self.new.replace("[計算, 支払う, 給与]", "[計算, 支払う, 給与, 他]")):
            with self.assertRaisesRegex(ValueError, "exceeds recorded exact edits"):
                audit.verify_exception(self.old, altered, self.row)

    def test_changed_ledger_and_wrong_baseline_are_rejected(self):
        row = copy.deepcopy(self.row)
        row["after"] = ["支払う"]
        with self.assertRaisesRegex(ValueError, "authorized exact delta"):
            audit.verify_exception(self.old, self.new, row)
        with self.assertRaisesRegex(ValueError, "Previous exclusions differ"):
            audit.verify_exception(self.old.replace("[計算]", "[]"), self.new, self.row)

    def test_unrelated_runtime_change_is_rejected(self):
        before = {"schemaVersion": 1, "contentVersion": "old", "files": {"a": "x", "b": "y"}}
        after = {"schemaVersion": 1, "contentVersion": "new", "files": {"a": "z", "b": "changed"}}
        with self.assertRaisesRegex(ValueError, "Changed baseline payload"):
            audit.runtime_delta(before, after, set(), {"a"})

    def test_only_the_signed_historical_source_addition_is_allowed(self):
        allowed = [("A", audit.SIGNED_ADDITION)]
        audit.verify_source_changes(allowed, [])
        for changed, untracked in (
            (allowed + [("M", "docs/n1-sources/batch-107-runtime-draft.json")], []),
            ([("M", audit.SIGNED_ADDITION)], []),
            (allowed, ["docs/n1-sources/unreviewed.json"]),
        ):
            with self.assertRaisesRegex(ValueError, "Original source evidence"):
                audit.verify_source_changes(changed, untracked)


if __name__ == "__main__":
    unittest.main()
