import copy
import unittest

import b134_closure_progress as progress
from common import json_bytes, sha
from test_b134_review_history import REVIEWED, fixture


def progress_fixture():
    closure, resolution, claims = fixture()
    closure["publicationChecks"] = {"uuidFindings": 0, "externalWindowFindings": 0}
    closure["limits"] = ["Synthetic fixture, not actual review or publication approval."]
    closure["resolution"] = {"path": "resolution.json", "sha256": sha(json_bytes(resolution))}
    closure["recordedFileSha256"]["resolution.json"] = closure["resolution"]["sha256"]
    original = {
        "batch": progress.BATCH, "base": progress.BASE, "members": progress.MEMBERS,
        "sourceRows": [831], "supports": [[progress.MEMBERS[0], progress.MEMBERS[0]]],
        "status": "local-unreviewed-authoring-candidate",
        "runtimePublished": False, "reviewClosed": [], "published": [],
        "accounting": {
            **progress.COUNTS, "localUnreviewedDrafts": 1, "overallN1TaskComplete": False,
        },
        "authorWarnings": {"finalQuizSafety": "Original warning, not a current gate assertion."},
    }
    manifest = json_bytes({"contentVersion": "fixture"})
    return original, closure, manifest, resolution, claims


class ClosureProgressControls(unittest.TestCase):
    def test_closed_ledger_preserves_delivery_and_original_history(self):
        original, closure, manifest, resolution, claims = progress_fixture()
        before = copy.deepcopy((original, closure, resolution, claims))
        raw = json_bytes(closure)
        ledger = progress.closed_progress(original, raw, manifest, resolution, claims)
        self.assertEqual((original, closure, resolution, claims), before)
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 271)
        self.assertEqual(ledger["accounting"]["undelivered"], 957)
        self.assertEqual(ledger["accounting"]["reviewClosedPendingRecordsWithCards"], 272)
        self.assertEqual(ledger["published"], [])
        self.assertFalse(ledger["runtimePublished"])
        self.assertFalse(ledger["review"]["originalReviewerConfirmation"])
        self.assertEqual(ledger["originalAuthorWarnings"], original["authorWarnings"])
        self.assertEqual(progress.validate_progress(ledger, REVIEWED, manifest, raw)["delivered"], 272)

    def test_missing_claim_or_failed_publication_scan_prevents_closure(self):
        mutations = (
            lambda c, r: r["dispositions"].pop(),
            lambda c, r: r.update(remainingConsequentialClaims=["D1"]),
            lambda c, r: c["publicationChecks"].update(externalWindowFindings=1),
            lambda c, r: c["publicationChecks"].update(uuidFindings=1),
            lambda c, r: c.update(limits=[]),
            lambda c, r: c.update(originalReviewerConfirmation=True),
            lambda c, r: c["resolution"].update(sha256="0" * 64),
        )
        for index, mutate in enumerate(mutations):
            original, closure, manifest, resolution, claims = progress_fixture()
            mutate(closure, resolution)
            with self.subTest(index=index), self.assertRaises(ValueError):
                progress.closed_progress(original, json_bytes(closure), manifest, resolution, claims)

    def test_premature_credit_stale_manifest_and_false_confirmation_are_rejected(self):
        original, closure, manifest, resolution, claims = progress_fixture()
        raw = json_bytes(closure)
        ledger = progress.closed_progress(original, raw, manifest, resolution, claims)
        mutations = (
            lambda v: v.update(runtimePublished=True),
            lambda v: v.update(published=progress.MEMBERS),
            lambda v: v["accounting"].update(publishedPendingRecordsWithCards=272),
            lambda v: v["accounting"].update(undelivered=956),
            lambda v: v["accounting"].update(overallN1TaskComplete=True),
            lambda v: v["review"].update(originalReviewerConfirmation=True),
            lambda v: v["review"].update(closureProvenanceSha256="0" * 64),
            lambda v: v.update(contentVersion="stale"),
            lambda v: v.update(manifestSha256="0" * 64),
        )
        for index, mutate in enumerate(mutations):
            altered = copy.deepcopy(ledger)
            mutate(altered)
            with self.subTest(index=index), self.assertRaises(ValueError):
                progress.validate_progress(altered, REVIEWED, manifest, raw)
        original["accounting"]["publishedPendingRecordsWithCards"] = 272
        with self.assertRaises(ValueError):
            progress.closed_progress(original, raw, manifest, resolution, claims)


if __name__ == "__main__":
    unittest.main()
