import copy
import json
import unittest

from common import sha
from finalize_b117_v3 import SOURCE_ROOT, require_prior_sources, require_round3


class RoundThreeBindingTests(unittest.TestCase):
    def setUp(self):
        self.index = {
            "batch": 117, "parent": "parent", "comparisonCards": {"peer": {}, "job": {}},
            "characterSources": [{"source": "member"}, {"source": "pay"}],
            "existingTargetSourceRecords": [{"path": "existing"}],
            "kanjidic2": {"sha256": "kd", "completeRecords": 2},
            "jmdict": {"sha256": "jm", "completeEntries": 1, "exactWrittenQueries": {"word": ["id"]},
                       "counterpartCardCitedIds": ["id"]},
            "pinnedInputs": {"KANJIDIC2": {"sha256": "raw-kd"}, "JMdict": {"sha256": "raw-jm"}},
        }
        self.raw = json.dumps(self.index).encode()
        self.receipt = {
            "batch": 117, "parent": "parent", "sourceEvidence": {"indexSha256": sha(self.raw)},
            "addedGuards": {"member": ["peer"]}, "declinedComparisons": ["pay/job"],
        }
        self.proof = {
            "candidate": "signed", "parent": "parent", "batch": 117, "status": "PASS",
            "sourceEvidenceIndex": f"{SOURCE_ROOT}/reconciliation-003/source-evidence-index.json",
            "sourceEvidenceIndexSha256": sha(self.raw), "comparisonCardsVerified": 2,
            "characterSourcesVerified": 2, "existingTargetRecordsVerified": 1,
            "counterpartCardCitedIdsVerified": ["id"], "guardAppendsVerified": {"member": ["peer"]},
            "declinedComparisons": ["pay/job"], "priorSourceEvidencePreserved": True,
            "scopeVerified": ["kanji/member.md", "manifest.json"], "memory": {"breach": None},
            "dictionaryRecords": [
                {"source": "KANJIDIC2", "extractionSha256": "kd", "completeRecordsVerified": 2,
                 "inputSha256": "raw-kd", "exactWrittenQueriesVerified": 0},
                {"source": "JMdict", "extractionSha256": "jm", "completeRecordsVerified": 1,
                 "inputSha256": "raw-jm", "exactWrittenQueriesVerified": 1},
            ],
        }

    def verify(self, proof=None, receipt=None):
        require_round3("signed", "parent", self.proof if proof is None else proof, self.raw,
                       json.dumps(self.receipt if receipt is None else receipt).encode())

    def test_rejects_stale_or_incomplete_third_round(self):
        self.verify()
        for patch in (
            {"candidate": "parent"}, {"parent": "other"}, {"sourceEvidenceIndexSha256": "wrong"},
            {"comparisonCardsVerified": 1}, {"existingTargetRecordsVerified": 0},
            {"counterpartCardCitedIdsVerified": []}, {"guardAppendsVerified": {}},
            {"declinedComparisons": []}, {"priorSourceEvidencePreserved": False},
            {"scopeVerified": ["manifest.json"]}, {"memory": {"breach": True}},
        ):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                self.verify(proof={**self.proof, **patch})
        with self.assertRaises(ValueError):
            self.verify(receipt={**self.receipt, "sourceEvidence": {"indexSha256": "old"}})

    def test_rejects_missing_duplicate_or_wrong_dictionary_records(self):
        bad = copy.deepcopy(self.proof["dictionaryRecords"])
        bad[1]["inputSha256"] = "wrong"
        for records in (bad, self.proof["dictionaryRecords"][:1],
                        self.proof["dictionaryRecords"] * 2):
            with self.subTest(records=records), self.assertRaises(ValueError):
                self.verify(proof={**self.proof, "dictionaryRecords": records})

    def test_preserves_exact_earlier_tree_entries(self):
        before = b"100644 blob aa\told-one\0" + b"100644 blob bb\told-two\0"
        self.assertEqual(require_prior_sources(before, before + b"100644 blob cc\tnew\0"), 2)
        for after in (before.replace(b"aa", b"cc"), before.replace(b"100644", b"100755"),
                      before.replace(b"old-one", b"moved-one"), b"100644 blob aa\told-one\0"):
            with self.subTest(after=after), self.assertRaises(ValueError):
                require_prior_sources(before, after)


if __name__ == "__main__":
    unittest.main()
