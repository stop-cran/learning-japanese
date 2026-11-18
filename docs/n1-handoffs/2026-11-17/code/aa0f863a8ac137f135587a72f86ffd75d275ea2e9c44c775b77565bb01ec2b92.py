import unittest

import run_b134_reconciliation_checks as checks


class ReconciliationScope(unittest.TestCase):
    def test_accepts_exact_card_manifest_and_new_evidence(self):
        changes = checks.parse_changes(
            "M\0kanji/\u7d2b.md\0M\0manifest.json\0"
            "A\0docs/n1-sources/batch-134-reconciliation-001/dispositions.json\0".encode())
        self.assertEqual(len(checks.validate_scope(changes)), 3)

    def test_rejects_changes_outside_scope_and_destructive_operations(self):
        cases = [
            [], [("M", "words/\u7d2b.md")], [("M", "kanji/\u7d3a.md")],
            [("D", "kanji/\u7d2b.md")], [("T", "kanji/\u7d2b.md")],
            [("A", "manifest.json")], [("M", "docs/n1-sources/batch-134/source-receipt.json")],
            [("M", "docs/n1-sources/batch-134-reconciliation-001/existing.json")],
            [("A", "docs/n1-sources/batch-134-reconciliation-001/../source-receipt.json")],
            [("A", "docs/n1-sources/batch-134-reconciliation-001\\escape.json")],
            [("M", "manifest.json"), ("M", "manifest.json")],
        ]
        for changes in cases:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                checks.validate_scope(changes)

    def test_rejects_malformed_git_output_and_cli_before_running(self):
        for raw in (b"M\0manifest.json", b"M\0", b"R100\0old\0new\0"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                checks.parse_changes(raw)
        for mode, head, path in (
            ("author", checks.closure.CANDIDATE, checks.closure.HERE / "new"),
            ("working", "short", checks.closure.HERE / "new"),
            ("working", checks.closure.CANDIDATE, checks.closure.HERE / "review" / "new"),
        ):
            with self.subTest(mode=mode, head=head, path=path), self.assertRaises(ValueError):
                checks.main(mode, head, path)


if __name__ == "__main__":
    unittest.main()
