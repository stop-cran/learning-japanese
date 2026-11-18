import copy
import unittest
from unittest.mock import patch

import b133_closure_origins as origins
import b133_closure_records_v2 as records
import record_b133_publication_v2 as recorder
from test_b133_closure_records import ReconciliationControls
from test_record_b133_publication import PublicationControls, fixture


class ExistingPublicationControls(PublicationControls):
    def setUp(self):
        context = patch("test_record_b133_publication.recorder", recorder)
        context.start()
        self.addCleanup(context.stop)


class ExistingLedgerControls(ReconciliationControls):
    def setUp(self):
        context = patch("test_b133_closure_records.records", records)
        context.start()
        self.addCleanup(context.stop)


def actual_lineage_fixture():
    closure, _, _ = fixture()
    initial = closure["reviewLineage"]
    for row in initial:
        row["run"] = "N1-B133-" + row["family"].upper() + "-001"
        row["session"] = origins.ORIGINAL if row["family"] == "claude" else "gpt-original"
    closure["reviewedSnapshot"] = origins.REVISION
    closure["intermediateRuns"] = []
    closure["finalRuns"] = []
    for row in list(initial):
        middle = copy.deepcopy(row)
        number = "001" if row["family"] == "claude" else "002"
        middle.update(run="N1-B133-" + row["family"].upper() + "-CONFIRM-" + number,
                      role="confirmation", snapshot="a" * 40, confirmation="CONFIRMED")
        closure["reviewLineage"].append(middle)
        closure["intermediateRuns"].append(middle["run"])
        final = copy.deepcopy(middle)
        final.update(run="N1-B133-" + row["family"].upper() + "-CONFIRM-003",
                     snapshot=origins.REVISION)
        if row["family"] == "claude":
            final.update(session=origins.FRESH, originalSession=origins.ORIGINAL,
                         reviewerOrigin="fresh-context-replacement",
                         replacementReason="pre-admission-context-capacity")
            for key, digest in (("contextObservation", origins.OBSERVATION),
                                ("priorFinal", origins.PRIOR_FINAL), ("priorAdjudication", "d" * 64)):
                final[key] = {"path": "origin/" + key, "sha256": digest}
                closure["recordedFileSha256"][final[key]["path"]] = digest
            final["priorAdjudication"]["originalSha256"] = origins.PRIOR_ADJUDICATION
        closure["reviewLineage"].append(final)
        closure["finalRuns"].append(final["run"])
    closure["nonAcceptedReviews"] = []
    for run in ("N1-B133-GPT-CONFIRM-001", "N1-B133-CLAUDE-CONFIRM-002"):
        row = {"run": run, "reviewAccepted": False, "confirmation": "UNVERIFIED"}
        for field in ("report", "final", "adjudication", "context", "structure", "audit-summary"):
            row[field] = {"path": run + "/" + field, "sha256": "e" * 64}
            closure["recordedFileSha256"][row[field]["path"]] = "e" * 64
        closure["nonAcceptedReviews"].append(row)
    return closure


class OriginAndHistoryControls(unittest.TestCase):
    def test_only_disclosed_pinned_continuation_can_replace_original(self):
        closure = actual_lineage_fixture()
        recorder.validate_reviews(closure, origins.REVISION)
        for key, wrong in (
            ("session", "another-session"), ("originalSession", "someone-else"),
            ("reviewerOrigin", "original"), ("replacementReason", "convenience"),
            ("contextObservation", {"path": "origin/contextObservation", "sha256": "0" * 64}),
            ("priorAdjudication", {"path": "origin/priorAdjudication", "sha256": "d" * 64,
                                   "originalSha256": "0" * 64}),
        ):
            altered = copy.deepcopy(closure)
            final = next(row for row in altered["reviewLineage"]
                         if row["run"] == "N1-B133-CLAUDE-CONFIRM-003")
            final[key] = wrong
            with self.subTest(key=key), self.assertRaises((ValueError, KeyError)):
                recorder.validate_reviews(altered, origins.REVISION)

    def test_held_or_superseded_reviews_cannot_be_omitted_or_promoted(self):
        closure = actual_lineage_fixture()
        for change in (
            lambda value: value["nonAcceptedReviews"].pop(),
            lambda value: value["nonAcceptedReviews"][0].update(reviewAccepted=True),
            lambda value: value["nonAcceptedReviews"][0]["adjudication"].update(sha256="0" * 64),
            lambda value: value.update(intermediateRuns=[]),
            lambda value: value.update(finalRuns=value["intermediateRuns"]),
        ):
            altered = copy.deepcopy(closure)
            change(altered)
            with self.assertRaises(ValueError):
                recorder.validate_reviews(altered, origins.REVISION)


if __name__ == "__main__":
    unittest.main()
