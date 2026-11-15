import subprocess
import tempfile
import unittest
from pathlib import Path

from confirm_v2 import revision_diff


class ConfirmationDiffTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="n1-confirm-diff-")
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git("init", "--quiet")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.autocrlf", "false")
        for path, text in {
            "kanji/card.md": "Original lesson\n",
            "words/word.md": "Original link\n",
            "manifest.json": "{}\n",
            "docs/receipt.json": "{}\n",
        }.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
        self.commit()
        self.config = {"repo": str(self.root),
                       "candidate": self.git("rev-parse", "HEAD").decode().strip()}

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.PIPE)

    def commit(self):
        self.git("add", "--all")
        self.git("-c", "core.hooksPath=NUL", "commit", "--quiet", "--no-gpg-sign", "-m", "fixture")
        return self.git("rev-parse", "HEAD").decode().strip()

    def test_runtime_delta_does_not_leak_other_reviewer_findings(self):
        (self.root / "kanji" / "card.md").write_text("Corrected lesson\n", encoding="utf-8")
        (self.root / "words" / "word.md").write_text("Corrected link\n", encoding="utf-8")
        (self.root / "manifest.json").write_text('{"generated": true}\n', encoding="utf-8")
        (self.root / "docs" / "receipt.json").write_text(
            '{"otherReviewer": "PRIVATE_FINDING"}\n', encoding="utf-8")
        (self.root / "docs" / "new-report.md").write_text("OTHER_REPORT\n", encoding="utf-8")
        delta, omitted = revision_diff(self.config, self.commit())
        self.assertIn(b"+Corrected lesson", delta)
        self.assertIn(b"+Corrected link", delta)
        self.assertNotIn(b"PRIVATE_FINDING", delta)
        self.assertNotIn(b"OTHER_REPORT", delta)
        self.assertNotIn(b"generated", delta)
        self.assertEqual(set(omitted),
                         {"manifest.json", "docs/receipt.json", "docs/new-report.md"})

    def test_contributor_only_revision_is_not_a_card_confirmation(self):
        (self.root / "docs" / "receipt.json").write_text('{"new": true}\n', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "No non-contributor revision"):
            revision_diff(self.config, self.commit())


if __name__ == "__main__":
    unittest.main()
