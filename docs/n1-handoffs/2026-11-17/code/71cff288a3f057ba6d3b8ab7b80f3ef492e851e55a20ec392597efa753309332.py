import copy
import json
import unittest

from b130_context_confirmation import ROOT
from b130_delta_closure_support import FINALS, additional_history, ledger_acceptance
from b130_followup_closure_history_v2 import (
    EXCLUDED, HISTORICAL, PREVIOUS, check_history, historical_confirmations,
)
from b130_fresh_closure_history import confirmation_origins
from common import frozen, load_batch, sha
from confirm_b130_fresh_context import preflight
from verify_b130_delta_evidence import CANDIDATE


class ActualDeltaClosureTests(unittest.TestCase):
    def fixture(self):
        config = load_batch(130)
        prior = historical_confirmations()
        finals, lineage = [], []
        for family, run in FINALS.items():
            initial = json.loads(frozen(ROOT / f"N1-B130-{family.upper()}-004-acceptance.json"))
            previous = next(row for row in prior if row["family"] == family)
            final = json.loads(frozen(ROOT / "confirm" / f"{run}-acceptance.json"))
            record, _ = preflight(ROOT / "confirm" / f"{run}-preflight.json")
            finals.append(ledger_acceptance(final, record))
            for role, row, prior_run in (("initial", initial, None),
                                         ("intermediate", previous, None),
                                         ("final", final, previous["run"])):
                lineage.append({
                    "run": row["run"], "family": family, "session": json.loads(frozen(row["final"]["path"], row["final"]["sha256"]))["session"],
                    "snapshot": row["candidate"], "rawVerdict": row["verdict"],
                    "role": role, "priorRun": prior_run, "finalAcceptance": role == "final",
                    "confirmationAcceptedOnSnapshot": row.get("confirmationAccepted", False),
                })
        excluded = []
        for run, status in EXCLUDED.items():
            raw = frozen(ROOT / f"{run}-hold.json")
            held = json.loads(raw)
            excluded.append({"run": run, "status": status, "session": held["session"],
                             "snapshot": config["candidate"], "holdSha256": sha(raw),
                             "reviewAccepted": False, "finalAcceptance": False})
        prepared, origins = confirmation_origins(prior, PREVIOUS)
        followups, controls = additional_history(finals)
        provenance = {
            "batch": 130, "base": config["base"], "members": config["members"],
            "initialSnapshot": config["candidate"], "reviewedSnapshot": CANDIDATE,
            "publication": "PENDING", "intermediateRuns": list(HISTORICAL.values()),
            "finalRuns": list(FINALS.values()), "preparedOnlyConfirmationRuns": prepared,
            "confirmationOrigins": origins, "reviewLineage": lineage, "excludedInitialRuns": excluded,
            "preparedOnlyFollowups": followups, "runtimeControlAdjudications": controls,
        }
        return provenance, CANDIDATE, config, finals

    def test_actual_mixed_finals_and_all_six_outcomes(self):
        args = self.fixture()
        before = copy.deepcopy(args)
        history = check_history(*args)
        self.assertEqual(len(history["gpt"]["openClaimIds"]), 24)
        self.assertEqual(args, before)

    def test_historical_unverified_cannot_be_relabelled(self):
        provenance, candidate, config, finals = self.fixture()
        previous = next(row for row in provenance["reviewLineage"]
                        if row["family"] == "gpt" and row["role"] == "intermediate")
        previous["rawVerdict"] = "CONFIRMED"
        with self.assertRaises(ValueError):
            check_history(provenance, candidate, config, finals)

    def test_unused_preparation_and_original_control_holds_cannot_disappear(self):
        original, candidate, config, finals = self.fixture()
        for key in ("preparedOnlyFollowups", "runtimeControlAdjudications"):
            with self.subTest(key=key):
                provenance = copy.deepcopy(original)
                provenance[key] = []
                with self.assertRaises(ValueError):
                    check_history(provenance, candidate, config, finals)
        provenance = copy.deepcopy(original)
        provenance["runtimeControlAdjudications"][0]["rawStatus"] = "PASS"
        with self.assertRaises(ValueError):
            check_history(provenance, candidate, config, finals)

    def test_unused_claude003_cannot_replace_actual004(self):
        provenance, candidate, config, finals = self.fixture()
        provenance["finalRuns"][0] = "N1-B130-CLAUDE-CONFIRM-003"
        with self.assertRaises(ValueError):
            check_history(provenance, candidate, config, finals)


if __name__ == "__main__":
    unittest.main()
