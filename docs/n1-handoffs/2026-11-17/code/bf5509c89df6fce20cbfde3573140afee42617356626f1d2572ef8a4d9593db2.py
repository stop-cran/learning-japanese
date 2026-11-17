import copy
import json
import unittest

from b130_context_confirmation import binding
from b130_integration_lineage import (ACCEPTANCE_SHA, CANDIDATE, PREVIOUS, RUNS,
                                     check_capacity, require_followup_identity)
from common import frozen
from verify_b130_integration_runtime import ROOT


class IntegrationLineageTests(unittest.TestCase):
    def test_actual_accepted_lineage_and_reject_wrong_snapshot_or_session(self):
        for family in RUNS:
            previous = json.loads(frozen(ROOT / "confirm" / f"{PREVIOUS[family]}-spec.json"))
            spec = {**previous, "candidate": CANDIDATE, "run": RUNS[family],
                    "basis": "accepted-confirmation", "priorVerdict": "CONFIRMED", "openClaimIds": [],
                    "prior": {"path": str(ROOT / "confirm" / f"{PREVIOUS[family]}-acceptance.json"),
                              "sha256": ACCEPTANCE_SHA[family]}}
            initial = json.loads(frozen(spec["acceptance"]["path"], spec["acceptance"]["sha256"]))
            launch = json.loads(frozen(ROOT / f"{initial['run']}-launch.json"))
            require_followup_identity(spec, initial, launch, ROOT)
            for key, value in (("candidate", previous["candidate"]), ("session", spec["originalSession"]),
                               ("prior", previous["prior"]), ("basis", "held-confirmation")):
                with self.subTest(family=family, key=key), self.assertRaises(ValueError):
                    require_followup_identity({**spec, key: value}, initial, launch, ROOT)

    def test_capacity_rejects_new_events_oversize_or_exhausted_context(self):
        observation = json.loads(frozen(ROOT / "integration-capacity-observation-001.json"))
        row = next(row for row in observation["reviewers"] if row["family"] == "claude")
        check_capacity(observation, "claude", row["session"], row["eventsSha256"], 110000)
        with self.assertRaises(ValueError):
            check_capacity(observation, "claude", row["session"], "0" * 64, 110000)
        with self.assertRaises(ValueError):
            check_capacity(observation, "claude", row["session"], row["eventsSha256"], 120001)
        changed = copy.deepcopy(observation)
        next(row for row in changed["reviewers"] if row["family"] == "claude")["lastUsage"]["inputTokens"] = 700001
        with self.assertRaises(ValueError):
            check_capacity(changed, "claude", row["session"], row["eventsSha256"], 110000)


if __name__ == "__main__":
    unittest.main()
