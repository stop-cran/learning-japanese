import copy
import json
import unittest

from common import CHECKS, frozen, json_bytes, sha
from finalize_b130_followup import (BASE, PREVIOUS, ROOT, SIGNER, SOURCES_SHA,
                                   check_archive, check_proofs)


class FollowupFinalizerTests(unittest.TestCase):
    def fixture(self):
        candidate = "e" * 40
        runtime_binding = {"path": "synthetic-runtime-proof", "sha256": "a" * 64}
        source_binding = {"path": "synthetic-source-reuse-proof", "sha256": "b" * 64}
        shared = {"batch": 130, "candidate": candidate, "parent": PREVIOUS, "base": BASE,
                  "reviewAccepted": False, "publicationAccepted": False, "memory": {"breach": None}}
        runtime = {**shared, "status": "PASS_RUNTIME_ONLY", "worktreeClean": True,
                   "signature": {"fingerprint": SIGNER, "ownerVerified": True},
                   "runtimeEntries": 8730, "runtimeChanged": ["kanji/拍.md"],
                   "cardMetadata": {"拍": {"addedGuards": ["響"]}}, "claimResolutionAccepted": False}
        sources = {**shared, "status": "PASS_SOURCE_REUSE_ONLY",
                   "previousSourceProof": {"path": str(ROOT / "revision-source-proof-001.json"),
                                           "sha256": SOURCES_SHA},
                   "newDictionaryScanPerformed": False, "comparisonCardsVerified": 28,
                   "previousVerifiedCounts": {"jmdict": 99, "kanjidic2": 31}}
        old = json.loads(frozen(ROOT / "revision-evidence-001" / "verification.json"))
        proof = {**shared, "status": "PASS_SECOND_RECONCILIATION_BINDINGS_ONLY",
                 "proofs": {"runtime": runtime_binding, "sourceReuse": source_binding},
                 "pairBindings": {"pairCount": 28, "authorOpenQuizHolds": [],
                                  "counts": {"guard": 8, "precaution": 17, "bounded-noncollision": 3}},
                 "priorEvidencePreserved": True,
                 "retainedQuizSafetyWarnings": old["retainedQuizSafetyWarnings"],
                 "gateSets": {mode: {"gates": [{"gate": gate} for gate in CHECKS]}
                              for mode in ("author", "committed")}}
        return candidate, proof, runtime, sources, runtime_binding, source_binding

    def test_exact_delta_without_inventing_new_source_scan(self):
        values = self.fixture()
        check_proofs(*values)
        for index, key, value in ((1, "reviewAccepted", True),
                                  (2, "runtimeChanged", ["kanji/拍.md", "kanji/耗.md"]),
                                  (3, "newDictionaryScanPerformed", True),
                                  (3, "candidate", PREVIOUS)):
            changed = copy.deepcopy(values)
            changed[index][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_proofs(*changed)
        changed = copy.deepcopy(values)
        changed[1]["gateSets"]["committed"]["gates"].pop()
        with self.assertRaises(ValueError):
            check_proofs(*changed)

    def test_archive_cannot_skip_historical_unverified_chain(self):
        candidate = "e" * 40
        provenance = {"reviewLineage": [
            {"run": "final", "chains": [{"path": "final-chain"}]},
            {"run": "historical-unverified", "chains": [{"path": "prior-chain"}]},
        ], "excludedInitialRuns": [{"run": "void", "chains": [{"path": "void-chain"}]}]}
        raw = json_bytes(provenance)
        rows = [{"run": row["run"], "path": chain["path"]}
                for row in provenance["reviewLineage"] + provenance["excludedInitialRuns"]
                for chain in row["chains"]]
        archive = {"status": "PASS", "candidate": candidate, "provenanceSha256": sha(raw), "chains": rows}
        check_archive(candidate, archive, provenance, raw)
        with self.assertRaises(ValueError):
            check_archive(candidate, {**archive, "chains": [rows[0], rows[2]]}, provenance, raw)


if __name__ == "__main__":
    unittest.main()
