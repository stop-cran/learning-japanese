import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import record_b130_integration_publication_v2 as recorder
import test_record_b130_publication as fixtures


class DeliveryScopeTests(unittest.TestCase):
    def record(self, root, fixture):
        context = {
            "reviewedSnapshot": recorder.ACTIVE, "previousReviewedSnapshot": recorder.PREVIOUS,
            "parents": recorder.PARENTS, "runtime": recorder.RUNTIME, "finalRuns": recorder.FINAL_RUNS,
            "integrationClosure": {"path": recorder.INTEGRATION_CLOSURE},
            "originalClosure": {"path": recorder.ORIGINAL_CLOSURE},
            "limits": ["No served-ZIP or publication acceptance was granted by these textual reviews."],
        }
        with patch.object(recorder, "WS", root), \
                patch.object(recorder, "load_batch", return_value=fixture["config"]), \
                patch.object(recorder, "clean"), \
                patch.object(recorder, "git", side_effect=fixture["git"]), \
                patch.object(recorder, "api_output",
                             side_effect=lambda config, *args: fixture["api"](["gh", *args])), \
                patch.object(recorder, "select_reviewed_snapshot", return_value=context), \
                contextlib.redirect_stdout(io.StringIO()):
            recorder.main(130, fixture["commit"], "1", fixture["archivePath"], fixture["narrativePath"])

    def test_receipt_distinguishes_review_scope_from_completed_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = fixtures.PublicationRetentionTests().fixture(root)
            self.record(root, fixture)
            receipt = json.loads((fixture["publication"] / "provenance.json").read_bytes())
            ledger = json.loads(fixture["ledgerPath"].read_bytes())
            self.assertEqual(receipt["limits"][:len(fixture["limits"])], fixture["limits"])
            self.assertEqual(receipt["limits"][-3],
                             "Scope of the integrated-snapshot textual reviews, not later publication checks: "
                             "No served-ZIP or publication acceptance was granted by these textual reviews.")
            self.assertEqual(ledger["reviewedSnapshot"], fixture["ledger"]["reviewedSnapshot"])
            self.assertEqual(ledger["publication"]["reviewedSnapshot"], recorder.ACTIVE)
            self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 264)
            self.assertFalse(ledger["accounting"]["overallN1TaskComplete"])

    def test_failing_ci_still_prevents_publication_receipt_and_credit(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = fixtures.PublicationRetentionTests().fixture(root)
            fixture["ci"]["conclusion"] = "failure"
            with self.assertRaisesRegex(ValueError, "CI has not succeeded"):
                self.record(root, fixture)
            self.assertFalse(fixture["publication"].exists())
            self.assertEqual(json.loads(fixture["ledgerPath"].read_bytes()), fixture["ledger"])


if __name__ == "__main__":
    unittest.main()
