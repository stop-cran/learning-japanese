import copy
import unittest

from common import CHECKS
from finalize_b124 import (
    FINALS, HELD, INITIALS, PARENT, RESPONSE_PATHS, RUNTIME_PROOF_SHA, SIGNER,
    check_documentation, check_history, check_proofs, make_ledger,
)
from record_publication import delivery_accounting


class B124FinalizationTests(unittest.TestCase):
    def fixture(self):
        config = {"candidate": "a" * 40, "base": "b" * 40, "members": ["\u88d5"]}
        candidate = "c" * 40
        lineage = []
        for family in INITIALS:
            base = {"family": family, "session": family, "priorRun": None,
                    "confirmationAcceptedOnSnapshot": False, "finalAcceptance": False}
            lineage.extend([
                {**base, "run": INITIALS[family], "role": "initial", "snapshot": config["candidate"],
                 "rawVerdict": "NEEDS FIX"},
                {**base, "run": HELD[family], "role": "intermediate", "snapshot": PARENT,
                 "rawVerdict": "CONFIRMED" if family == "claude" else "UNVERIFIED"},
                {**base, "run": FINALS[family], "role": "final", "snapshot": candidate,
                 "rawVerdict": "CONFIRMED", "confirmationAcceptedOnSnapshot": True,
                 "finalAcceptance": True, "priorRun": HELD[family]},
            ])
        provenance = {"reviewedSnapshot": candidate, "initialSnapshot": config["candidate"],
                      "base": config["base"], "publication": "PENDING", "members": config["members"],
                      "excludedInitialRuns": [], "finalRuns": list(FINALS.values()),
                      "intermediateRuns": list(HELD.values()), "reviewLineage": lineage}
        common = {"status": "PASS", "initial": config["candidate"], "base": config["base"],
                  "metadataStrokesSupportAndHistoricalEvidencePreserved": True,
                  "sourceMembersPublishedBeforeBatch": 253, "sourceMembersInCandidate": 254,
                  "runtimeEntries": 8710, "signature": {"fingerprint": SIGNER, "ownerVerified": True},
                  "worktreeClean": True, "memory": {"breach": None},
                  "gateSets": {mode: {"gates": [{"gate": name} for name in CHECKS]}
                               for mode in ("author", "committed")}, "signedArtifacts": {},
                  "contentVersion": "version", "manifestSha256": "hash"}
        first = {**copy.deepcopy(common), "candidate": PARENT}
        current = {**copy.deepcopy(common), "candidate": candidate, "parent": PARENT}
        return config, candidate, provenance, first, current

    def test_requires_exact_original_family_lineage_and_preserves_held_verdicts(self):
        config, candidate, provenance, *_ = self.fixture()
        check_history(provenance, candidate, config)
        for index, key, value in (
            (0, "rawVerdict", "CLEAN"), (1, "rawVerdict", "UNVERIFIED"),
            (1, "confirmationAcceptedOnSnapshot", True), (4, "rawVerdict", "CONFIRMED"),
            (2, "session", "replacement"), (2, "snapshot", PARENT), (2, "priorRun", None),
            (5, "run", "N1-B124-GPT-CONFIRM-003"), (5, "finalAcceptance", False),
        ):
            changed = copy.deepcopy(provenance)
            changed["reviewLineage"][index][key] = value
            with self.subTest(index=index, key=key), self.assertRaises(ValueError):
                check_history(changed, candidate, config)

    def test_rejects_missing_or_duplicate_historical_runs(self):
        config, candidate, provenance, *_ = self.fixture()
        for rows in (provenance["reviewLineage"][1:],
                     provenance["reviewLineage"] + [provenance["reviewLineage"][0]]):
            with self.assertRaises(ValueError):
                check_history({**provenance, "reviewLineage": rows}, candidate, config)

    def test_requires_both_proofs_and_all_four_gate_sets(self):
        config, candidate, _, first, current = self.fixture()
        check_proofs(first, current, candidate, config)
        for key, value in (("parent", "wrong"), ("sourceMembersPublishedBeforeBatch", 254),
                           ("memory", {"breach": "low RAM"}), ("gateSets", {"committed": {"gates": []}})):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_proofs(first, {**current, key: value}, candidate, config)
        changed = copy.deepcopy(first)
        changed["gateSets"]["author"]["gates"].pop()
        with self.assertRaises(ValueError):
            check_proofs(changed, current, candidate, config)

    def test_closed_ledger_still_does_not_claim_delivery(self):
        config, candidate, provenance, first, current = self.fixture()
        documentation = {"signedArtifacts": {path: "hash" for path in RESPONSE_PATHS}}
        ledger = make_ledger(config, candidate, provenance, "closure", first, current, documentation)
        self.assertEqual(ledger["published"], [])
        self.assertFalse(ledger["runtimePublished"])
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 253)
        self.assertEqual(ledger["accounting"]["undelivered"], 975)
        self.assertEqual(ledger["review"]["intermediateRuns"], list(HELD.values()))
        self.assertIn("held", ledger["review"]["identity"])
        self.assertEqual(delivery_accounting(ledger),
                         {"delivered": 254, "n1Additions": 248, "n2Placements": 6, "remaining": 974})

    def test_documentation_successor_cannot_mask_a_runtime_or_source_change(self):
        config, _, _, _, current = self.fixture()
        candidate = "d" * 40
        proof = {"status": "PASS", "candidate": candidate, "parent": current["candidate"],
                 "initial": config["candidate"], "base": config["base"],
                 "runtimeAndPriorEvidenceUnchanged": True, "runtimeProofSha256": RUNTIME_PROOF_SHA,
                 "manifestSha256": current["manifestSha256"],
                 "signedArtifacts": {path: "hash" for path in RESPONSE_PATHS},
                 "signature": {"fingerprint": SIGNER, "ownerVerified": True},
                 "worktreeClean": True, "memory": {"breach": None}}
        check_documentation(proof, candidate, current, config)
        for key, value in (("parent", PARENT), ("runtimeAndPriorEvidenceUnchanged", False),
                           ("manifestSha256", "changed"), ("signedArtifacts", {"kanji/x.md": "hash"})):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_documentation({**proof, key: value}, candidate, current, config)


if __name__ == "__main__":
    unittest.main()
