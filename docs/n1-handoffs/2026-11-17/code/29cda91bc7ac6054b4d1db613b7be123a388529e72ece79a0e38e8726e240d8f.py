import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from close_v4 import require_historical_confirmation
from common import WS, frozen
from confirm_followup_evidence_v1 import selected_revision_diff


class EvidenceDeltaIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="n1-evidence-delta-")
        self.root = Path(self.directory.name)
        self.addCleanup(self.directory.cleanup)
        self.git("init", "--quiet")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        (self.root / "kanji").mkdir()
        (self.root / "kanji" / "card.md").write_text("original teaching\n", encoding="utf-8")
        (self.root / "manifest.json").write_text("{}\n", encoding="utf-8")
        self.base = self.commit("fixture baseline")
        (self.root / "docs").mkdir()
        (self.root / "docs" / "evidence.json").write_text('{"bounded":true}\n', encoding="utf-8")
        self.docs = self.commit("fixture evidence")
        self.config = {"repo": str(self.root), "candidate": self.base}

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.PIPE)

    def commit(self, message):
        self.git("add", "--all")
        self.git("-c", "core.hooksPath=NUL", "commit", "--quiet", "--no-gpg-sign", "-m", message)
        return self.git("rev-parse", "HEAD").decode().strip()

    def test_real_git_docs_delta_and_both_runtime_boundaries(self):
        note, omitted = selected_revision_diff(self.config, self.docs, {"evidenceOnly": True})
        self.assertEqual(omitted, ["docs/evidence.json"])
        self.assertIn(self.base.encode(), note)
        self.assertIn(self.docs.encode(), note)
        with self.assertRaisesRegex(ValueError, "No non-contributor"):
            selected_revision_diff(self.config, self.docs, {})
        (self.root / "manifest.json").write_text('{"changed":true}\n', encoding="utf-8")
        manifest = self.commit("fixture manifest")
        with self.assertRaisesRegex(ValueError, "documentation-only"):
            selected_revision_diff(self.config, manifest, {"evidenceOnly": True})
        (self.root / "kanji" / "card.md").write_text("changed teaching\n", encoding="utf-8")
        runtime = self.commit("fixture teaching")
        config = {**self.config, "candidate": manifest}
        with self.assertRaisesRegex(ValueError, "documentation-only"):
            selected_revision_diff(config, runtime, {"evidenceOnly": True})
        patch, _ = selected_revision_diff(config, runtime, {})
        self.assertIn(b"+changed teaching", patch)


class HistoricalSnapshotIntegrationTests(unittest.TestCase):
    def test_real_accepted_and_held_confirmations_are_not_relabelled(self):
        records = WS / "scratch-125" / "review" / "confirm"
        for family, verdict, accepted, claims in (
            ("CLAUDE", "CONFIRMED", True, []),
            ("GPT", "UNVERIFIED", False, ["S1"]),
        ):
            with self.subTest(family=family):
                path = records / f"N1-B125-{family}-CONFIRM-001-acceptance.json"
                raw = frozen(path)
                prior = json.loads(raw)
                self.assertEqual((prior["verdict"], prior["confirmationAccepted"], prior["openClaimIds"]),
                                 (verdict, accepted, claims))
                require_historical_confirmation(prior, "c" * 40)
                with self.assertRaises(ValueError):
                    require_historical_confirmation(prior, prior["candidate"])
                self.assertEqual(frozen(path), raw)


if __name__ == "__main__":
    unittest.main()
