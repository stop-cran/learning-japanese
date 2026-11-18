import copy
import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "revision_gates", Path(__file__).with_name("verify-b134-revision002-gates.py"))
gates = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gates)


class GateBindings(unittest.TestCase):
    def setUp(self):
        self.signed = {"kanji/card.md": "card", "manifest.json": "manifest",
                       "docs/n1-sources/evidence.json": "evidence"}
        self.summary = {
            "batch": 134, "status": "PASS", "mode": "working", "base": gates.BASE,
            "initialSnapshot": gates.CANDIDATE, "head": gates.REVIEWED,
            "reconciliationCommits": 1, "checks": gates.ORDER,
            "manifestReproducible": True, "manifestSha256": "manifest",
            "changedFiles": copy.deepcopy(self.signed), "wrapperSha256": gates.WRAPPER_SHA,
        }

    def verify(self, summary):
        gates.verify_summary(summary, "working", gates.REVIEWED, 1, "manifest", self.signed)

    def test_exact_working_receipt_passes(self):
        self.verify(self.summary)

    def test_rejects_stale_candidate_and_mismatched_execution(self):
        for key, value in (
            ("head", gates.CANDIDATE), ("mode", "committed"),
            ("reconciliationCommits", 0), ("manifestSha256", "previous"),
            ("checks", gates.ORDER[:-1]), ("manifestReproducible", False),
            ("wrapperSha256", "replacement"),
        ):
            with self.subTest(key=key):
                summary = {**self.summary, key: value}
                with self.assertRaises(ValueError):
                    self.verify(summary)

    def test_rejects_omitted_or_changed_signed_evidence(self):
        for changed in (
            {"kanji/card.md": "card", "manifest.json": "manifest"},
            {**self.signed, "kanji/card.md": "prior-card"},
        ):
            with self.assertRaises(ValueError):
                self.verify({**self.summary, "changedFiles": changed})


if __name__ == "__main__":
    unittest.main(verbosity=2)
