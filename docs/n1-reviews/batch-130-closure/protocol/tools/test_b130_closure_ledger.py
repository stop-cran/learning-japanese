import copy
import json
import unittest

from b130_closure_ledger import (BASE, EXCLUDED, GPT_OPEN, MEMBERS, PARENT, REVIEWERS,
                                ROOT, check_history, make_ledger)
from common import WS, frozen, load_batch, sha
from record_b130_publication import delivery_accounting


class ClosureLedgerTests(unittest.TestCase):
    def setUp(self):
        self.config = load_batch(130)
        self.old = json.loads((WS / "b130-worktree" / "docs" / "n1-sources"
                               / "batch-130-progress.json").read_bytes())
        # Synthetic confirmations exercise the helper, not actual review acceptance.
        self.candidate = "1" * 40
        self.finals, rows = [], []
        for family, session in REVIEWERS.items():
            run = f"N1-B130-{family.upper()}-CONFIRM-001"
            self.finals.append({
                "batch": 130, "run": run, "family": family, "candidate": self.candidate,
                "verdict": "CONFIRMED", "confirmationAccepted": True, "openClaimIds": [],
            })
            rows.extend([
                {"run": f"N1-B130-{family.upper()}-004", "family": family, "session": session,
                 "role": "initial", "snapshot": PARENT, "rawVerdict": "NEEDS FIX",
                 "priorRun": None, "finalAcceptance": False, "confirmationAcceptedOnSnapshot": False},
                {"run": run, "family": family, "session": session, "role": "final",
                 "snapshot": self.candidate, "rawVerdict": "CONFIRMED", "priorRun": None,
                 "finalAcceptance": True, "confirmationAcceptedOnSnapshot": True},
            ])
        excluded = []
        for run in EXCLUDED:
            raw = frozen(ROOT / f"{run}-hold.json")
            held = json.loads(raw)
            excluded.append({
                "run": run, "status": held["status"], "session": held["session"],
                "snapshot": held["candidate"], "holdSha256": sha(raw),
                "reviewAccepted": False, "finalAcceptance": False,
            })
        self.provenance = {
            "batch": 130, "initialSnapshot": PARENT, "reviewedSnapshot": self.candidate,
            "base": BASE, "members": list(MEMBERS), "publication": "PENDING",
            "finalRuns": [row["run"] for row in self.finals],
            "intermediateRuns": [], "reviewLineage": rows, "excludedInitialRuns": excluded,
        }
        self.runtime = {
            "batch": 130, "status": "PASS_RUNTIME_ONLY", "candidate": self.candidate,
            "parent": PARENT, "base": BASE, "runtimeEntries": 8730,
            "reviewAccepted": False, "publicationAccepted": False,
            "claimResolutionAccepted": False,
            "initialOpenClaimIds": {"claude": [], "gpt": list(GPT_OPEN)},
            "manifestSha256": "a" * 64, "contentVersion": "b" * 16,
            "memory": {"breach": False},
        }

    def ledger(self):
        return make_ledger(self.old, self.config, self.provenance, "c" * 64,
                           self.runtime, self.finals)

    def test_actual_schema_and_history_preserve_delivery_and_initial_questions(self):
        before = copy.deepcopy((self.old, self.runtime, self.provenance, self.finals))
        ledger = self.ledger()
        self.assertEqual((self.old, self.runtime, self.provenance, self.finals), before)
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 261)
        self.assertEqual(ledger["accounting"]["undelivered"], 967)
        self.assertFalse(ledger["runtimePublished"])
        self.assertFalse(ledger["accounting"]["overallN1TaskComplete"])
        self.assertEqual(ledger["published"], [])
        self.assertEqual(ledger["review"]["initialHistory"]["gpt"]["openClaimIds"], GPT_OPEN)
        self.assertEqual(ledger["originalAuthorWarnings"], self.old["warnings"])
        self.assertEqual(delivery_accounting(ledger), {
            "delivered": 264, "n1Additions": 258, "n2Placements": 6, "remaining": 964,
        })

    def test_missing_open_or_wrong_snapshot_confirmation_cannot_close(self):
        for field, value in (("openClaimIds", ["D2"]), ("confirmationAccepted", False),
                             ("candidate", PARENT), ("verdict", "NEEDS FIX"), ("family", "claude")):
            with self.subTest(field=field):
                finals = copy.deepcopy(self.finals)
                finals[1][field] = value
                with self.assertRaises(ValueError):
                    check_history(self.provenance, self.candidate, self.config, finals)
        with self.assertRaises(ValueError):
            check_history(self.provenance, self.candidate, self.config, self.finals[:1])

    def test_relabelled_initial_reviewer_or_new_history_cannot_close(self):
        for index, field, value in ((0, "rawVerdict", "CLEAN"), (0, "finalAcceptance", True),
                                    (1, "session", REVIEWERS["gpt"]), (1, "priorRun", "prior")):
            with self.subTest(index=index, field=field):
                provenance = copy.deepcopy(self.provenance)
                provenance["reviewLineage"][index][field] = value
                with self.assertRaises(ValueError):
                    check_history(provenance, self.candidate, self.config, self.finals)
        self.provenance["intermediateRuns"] = ["prior"]
        with self.assertRaises(ValueError):
            self.ledger()

    def test_omitted_duplicate_or_promoted_excluded_initial_cannot_close(self):
        for index in range(3):
            for change in ("omit", "duplicate", "accept", "binding"):
                with self.subTest(index=index, change=change):
                    provenance = copy.deepcopy(self.provenance)
                    rows = provenance["excludedInitialRuns"]
                    if change == "omit":
                        rows.pop(index)
                    elif change == "duplicate":
                        rows[index] = rows[(index + 1) % 3]
                    elif change == "accept":
                        rows[index]["reviewAccepted"] = True
                    else:
                        rows[index]["holdSha256"] = "0" * 64
                    with self.assertRaises(ValueError):
                        check_history(provenance, self.candidate, self.config, self.finals)

    def test_runtime_checks_cannot_erase_questions_or_increment_delivery(self):
        for field, value in (("claimResolutionAccepted", True),
                             ("initialOpenClaimIds", {"claude": [], "gpt": []}),
                             ("publicationAccepted", True)):
            with self.subTest(field=field):
                runtime = copy.deepcopy(self.runtime)
                runtime[field] = value
                with self.assertRaises(ValueError):
                    make_ledger(self.old, self.config, self.provenance, "c" * 64,
                                runtime, self.finals)
        self.old["publishedDelivered"] = 264
        with self.assertRaises(ValueError):
            self.ledger()


if __name__ == "__main__":
    unittest.main()
