import json
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

from common import sha
from confirm_v3 import verify_prior

SESSION = "reviewer-session"


class FollowupLineageTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix="n1-confirm-v3-")
        self.addCleanup(self.cleanup)
        self.root = Path(self.directory.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "--quiet")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.freeze_commit = self.commit("freeze")
        self.prior_commit = self.commit("prior")
        self.new_commit = self.commit("new")
        self.records = self.root / "review"
        (self.records / "confirm").mkdir(parents=True)
        self.config = {"repo": str(self.repo), "candidate": self.freeze_commit}
        report = self.write("initial.md", "# initial\n### F1: x\n")
        self.initial = self.write("N1-B9-CLAUDE-001-acceptance.json", {
            "run": "N1-B9-CLAUDE-001", "reviewAccepted": True, "candidate": self.freeze_commit,
            "report": report})
        self.write("N1-B9-CLAUDE-001-launch.json", {"session": SESSION})
        self.write("confirm/N1-B9-CLAUDE-CONFIRM-001-spec.json",
                   {"acceptance": self.initial, "session": SESSION})
        self.prior_report = self.write("confirm/prior.md", "# prior\r\n### F1: gap\r\n## Optional\r\nNone.\r\n")
        self.final = self.write("confirm/N1-B9-CLAUDE-CONFIRM-001-final.json", {
            "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION", "run": "N1-B9-CLAUDE-CONFIRM-001",
            "candidate": self.prior_commit, "confirmation": "NEEDS FIX", "report": self.prior_report})
        self.adjudication = self.write("confirm/adjudication.json", {"verdict": "NEEDS FIX"})

    def cleanup(self):
        for path in self.root.rglob("*"):
            if path.is_file():
                path.chmod(stat.S_IWRITE | stat.S_IREAD)
        self.directory.cleanup()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, stderr=subprocess.PIPE)

    def commit(self, text):
        (self.repo / "card.md").write_text(text + "\n", encoding="utf-8")
        self.git("add", "--all")
        self.git("-c", "core.hooksPath=NUL", "commit", "--quiet", "--no-gpg-sign", "-m", text)
        return self.git("rev-parse", "HEAD").decode().strip()

    def write(self, name, value):
        path = self.records / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.chmod(stat.S_IWRITE | stat.S_IREAD)
            path.unlink()
        raw = value.encode("utf-8") if isinstance(value, str) else json.dumps(value).encode("utf-8")
        path.write_bytes(raw)
        path.chmod(stat.S_IREAD)
        return {"path": str(path), "sha256": sha(raw)}

    def spec(self, prior_changes=None, **changes):
        prior = {"run": "N1-B9-CLAUDE-CONFIRM-001", "family": "claude", "session": SESSION,
                 "candidate": self.prior_commit, "verdict": "NEEDS FIX", "reviewEvidenceAccepted": True,
                 "confirmationAccepted": False, "acceptedNewFindings": ["F1"], "openClaimIds": ["F1"],
                 "report": self.prior_report, "final": self.final, "adjudication": self.adjudication,
                 **(prior_changes or {})}
        base = {"batch": 9, "run": "N1-B9-CLAUDE-CONFIRM-002", "family": "claude", "session": SESSION,
                "candidate": self.new_commit, "basis": "confirmation", "acceptance": self.initial,
                "prior": self.write("confirm/N1-B9-CLAUDE-CONFIRM-001-acceptance.json", prior)}
        return {**base, **changes}

    def test_accepted_needs_fix_is_a_followup_basis(self):
        _, prior, report = verify_prior(self.spec(), self.config, self.records)
        self.assertEqual(prior["candidate"], self.prior_commit)
        self.assertIn(b"### F1: gap", report)

    def test_lineage_violations_are_rejected(self):
        cases = {
            "other reviewer": ({}, {"session": "other-session"}),
            "earlier run": ({}, {"run": "N1-B9-CLAUDE-CONFIRM-001"}),
            "accepted prior": ({"confirmationAccepted": True}, {}),
            "unaccepted finding": ({"acceptedNewFindings": []}, {}),
            "relabeled held verdict": ({}, {"basis": "held-confirmation", "priorVerdict": "CONFIRMED",
                                            "openClaimIds": ["F1"]}),
            "same candidate": ({}, {"candidate": self.prior_commit}),
        }
        for label, (prior, changes) in cases.items():
            with self.subTest(label), self.assertRaises(ValueError):
                verify_prior(self.spec(prior, **changes), self.config, self.records)

    def test_non_descendant_revision_is_rejected(self):
        self.git("checkout", "--quiet", "-b", "side", self.freeze_commit)
        side = self.commit("side")
        with self.assertRaises(subprocess.CalledProcessError):
            verify_prior(self.spec(candidate=side), self.config, self.records)


if __name__ == "__main__":
    unittest.main()
