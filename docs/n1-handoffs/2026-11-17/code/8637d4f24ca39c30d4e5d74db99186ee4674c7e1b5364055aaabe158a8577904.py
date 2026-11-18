import copy
import unittest

from b125_followup_lineage import FINALS, HISTORICAL, PRIOR_SNAPSHOT, check_history
from test_finalize_b125 import B125FinalizerTests


class FollowupClosureLineageTests(unittest.TestCase):
    def fixture(self):
        config, provenance, *_ = B125FinalizerTests().fixture()
        candidate = "c" * 40
        lineage = []
        for row in provenance["reviewLineage"]:
            if row["role"] == "initial":
                lineage.append(row)
                continue
            family = row["family"]
            lineage.extend([
                {**row, "run": HISTORICAL[family], "role": "intermediate",
                 "rawVerdict": "CONFIRMED" if family == "claude" else "UNVERIFIED",
                 "confirmationAcceptedOnSnapshot": family == "claude", "finalAcceptance": False},
                {**row, "run": FINALS[family], "snapshot": candidate, "priorRun": HISTORICAL[family]},
            ])
        provenance.update(reviewLineage=lineage, reviewedSnapshot=candidate,
                          intermediateRuns=list(HISTORICAL.values()), finalRuns=list(FINALS.values()))
        return config, provenance, candidate

    def test_acceptance_of_one_prior_snapshot_does_not_erase_the_other_hold(self):
        config, provenance, candidate = self.fixture()
        original = copy.deepcopy(provenance)
        check_history(provenance, config, candidate)
        self.assertEqual(provenance, original)
        for index, field, value in (
            (1, "confirmationAcceptedOnSnapshot", False),
            (4, "confirmationAcceptedOnSnapshot", True),
            (4, "rawVerdict", "CONFIRMED"),
            (1, "snapshot", candidate),
        ):
            changed = copy.deepcopy(provenance)
            changed["reviewLineage"][index][field] = value
            with self.subTest(field=field, index=index), self.assertRaises(ValueError):
                check_history(changed, config, candidate)

    def test_finals_cannot_skip_history_change_reviewer_or_reuse_prior_snapshot(self):
        config, provenance, candidate = self.fixture()
        for field, value in (("priorRun", None), ("session", "other"), ("snapshot", PRIOR_SNAPSHOT),
                             ("finalAcceptance", False), ("rawVerdict", "UNVERIFIED")):
            changed = copy.deepcopy(provenance)
            changed["reviewLineage"][2][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_history(changed, config, candidate)

    def test_missing_history_or_reclassified_void_cannot_close(self):
        config, provenance, candidate = self.fixture()
        changed = copy.deepcopy(provenance)
        changed["reviewLineage"].pop(4)
        with self.assertRaises(ValueError):
            check_history(changed, config, candidate)
        for field, value in (("reviewAccepted", True), ("finalAcceptance", True),
                             ("status", "ACCEPTED"), ("quarantineSha256", "different")):
            changed = copy.deepcopy(provenance)
            changed["excludedInitialRuns"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_history(changed, config, candidate)


if __name__ == "__main__":
    unittest.main()
