import copy
import json
import unittest

from common import sha
from finalize_b117_v2 import SOURCE_ROOT, require_sources


class RoundTwoBindingTests(unittest.TestCase):
    def setUp(self):
        self.index = {
            "batch": 117, "baseline": "base", "parent": "parent",
            "comparisonCards": {"peer": {}}, "characterSources": [{"source": "member"}],
            "kanjidic2": {"sha256": "kd", "completeRecords": 2},
            "jmdict": {"sha256": "jm", "completeEntries": 1, "exactWrittenQueries": {"word": ["id"]}},
            "pinnedInputs": {"KANJIDIC2": {"sha256": "raw-kd"}, "JMdict": {"sha256": "raw-jm"}},
        }
        self.raw = json.dumps(self.index).encode()
        self.first = {
            "candidate": "signed", "status": "PASS", "baseline": "base",
            "sourceEvidenceIndexSha256": sha(self.raw), "comparisonCardsVerified": 1,
            "memory": {"breach": None},
            "dictionaryRecords": [
                {"source": "KANJIDIC2", "extractionSha256": "kd", "completeRecordsVerified": 2,
                 "inputSha256": "raw-kd", "exactWrittenQueriesVerified": 0},
                {"source": "JMdict", "extractionSha256": "jm", "completeRecordsVerified": 1,
                 "inputSha256": "raw-jm", "exactWrittenQueriesVerified": 1},
            ],
        }
        self.second = {
            **copy.deepcopy(self.first), "batch": 117, "parent": "parent",
            "sourceEvidenceIndex": f"{SOURCE_ROOT}/reconciliation-002/source-evidence-index.json",
            "characterSourcesVerified": 1, "priorSourceEvidencePreserved": True,
            "scopeVerified": ["kanji/member.md", "manifest.json"],
        }

    def verify(self, first=None, second=None):
        require_sources("signed", "parent", ["member"],
                        self.first if first is None else first, self.raw,
                        self.second if second is None else second, self.raw)

    def test_rejects_stale_candidate_from_either_round(self):
        self.verify()
        with self.assertRaises(ValueError):
            self.verify(first={**self.first, "candidate": "old"})
        with self.assertRaises(ValueError):
            self.verify(second={**self.second, "candidate": "old"})

    def test_rejects_incomplete_or_duplicated_dictionary_families(self):
        for records in (
            self.second["dictionaryRecords"][:1],
            self.second["dictionaryRecords"] + self.second["dictionaryRecords"][:1],
            [self.second["dictionaryRecords"][0],
             {**self.second["dictionaryRecords"][1], "exactWrittenQueriesVerified": 0}],
        ):
            with self.subTest(records=records), self.assertRaises(ValueError):
                self.verify(second={**self.second, "dictionaryRecords": records})

    def test_rejects_wrong_ancestry_or_incomplete_scope_proof(self):
        for patch in (
            {"parent": "other"}, {"sourceEvidenceIndexSha256": "other"},
            {"characterSourcesVerified": 0}, {"comparisonCardsVerified": 0},
            {"priorSourceEvidencePreserved": False}, {"scopeVerified": ["manifest.json"]},
            {"memory": {"breach": True}},
        ):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                self.verify(second={**self.second, **patch})


if __name__ == "__main__":
    unittest.main()
