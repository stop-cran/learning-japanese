import copy
import unittest

import b134_revision_progress as progress
from common import json_bytes, sha
from test_b134_closure_progress import progress_fixture
from test_b134_revision_history import fixture as revision_fixture


def fixture():
    original, _, manifest, _, _ = progress_fixture()
    closure, resolution, claims = revision_fixture()
    closure["publicationChecks"] = {"uuidFindings": 0, "externalWindowFindings": 0}
    closure["limits"] = ["Synthetic authorized descendant fixture, not actual review."]
    closure["resolution"] = {"path": "resolution.json", "sha256": sha(json_bytes(resolution))}
    closure["recordedFileSha256"]["resolution.json"] = closure["resolution"]["sha256"]
    return original, closure, manifest, resolution, claims


class RevisionProgressTests(unittest.TestCase):
    def test_descendant_ledger_preserves_all_publication_and_historical_state(self):
        original, closure, manifest, resolution, claims = fixture()
        before = copy.deepcopy((original, closure, manifest, resolution, claims))
        ledger = progress.closed_progress(original, json_bytes(closure), manifest, resolution, claims)
        self.assertEqual((original, closure, manifest, resolution, claims), before)
        self.assertEqual(ledger["review"]["finalRuns"], closure["finalRuns"])
        self.assertEqual(ledger["review"]["confirmationRuns"], closure["confirmationRuns"])
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 271)
        self.assertEqual(ledger["accounting"]["undelivered"], 957)
        self.assertFalse(ledger["review"]["originalReviewerConfirmation"])
        self.assertFalse(ledger["runtimePublished"])

    def test_missing_confirmation_attribution_or_early_delivery_credit_rejected(self):
        original, closure, manifest, resolution, claims = fixture()
        raw = json_bytes(closure)
        ledger = progress.closed_progress(original, raw, manifest, resolution, claims)
        changes = (
            lambda item: item["review"].update(confirmationRuns=[]),
            lambda item: item["review"].update(authorizedDescendantConfirmations=False),
            lambda item: item.update(priorReviewedSnapshot=progress.history.REVISED),
            lambda item: item["accounting"].update(publishedPendingRecordsWithCards=272),
            lambda item: item.update(runtimePublished=True),
        )
        for change in changes:
            mutated = copy.deepcopy(ledger)
            change(mutated)
            with self.subTest(change=change), self.assertRaises(ValueError):
                progress.validate_progress(mutated, progress.history.REVISED, manifest, raw)


if __name__ == "__main__":
    unittest.main()
