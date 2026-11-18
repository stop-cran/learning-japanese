import json
import unittest

from common import sha
from finalize_b117 import require_source_proof


class SourceBindingTests(unittest.TestCase):
    def test_rejects_stale_or_incomplete_extraction_proofs(self):
        index = {
            "baseline": "base", "comparisonCards": {"紀": {}},
            "kanjidic2": {"sha256": "kd", "completeRecords": 1},
            "jmdict": {"sha256": "jm", "completeEntries": 2},
            "pinnedInputs": {"KANJIDIC2": {"sha256": "raw-kd"}, "JMdict": {"sha256": "raw-jm"}},
        }
        raw = json.dumps(index).encode()
        proof = {
            "status": "PASS", "sourceEvidenceIndexSha256": sha(raw), "baseline": "base",
            "comparisonCardsVerified": 1, "memory": {"breach": None},
            "dictionaryRecords": [
                {"source": "KANJIDIC2", "extractionSha256": "kd", "completeRecordsVerified": 1,
                 "inputSha256": "raw-kd"},
                {"source": "JMdict", "extractionSha256": "jm", "completeRecordsVerified": 2,
                 "inputSha256": "raw-jm"},
            ],
        }
        require_source_proof(proof, raw)
        for changed in (
            {**proof, "sourceEvidenceIndexSha256": "old"},
            {**proof, "comparisonCardsVerified": 0},
            {**proof, "dictionaryRecords": proof["dictionaryRecords"][:1]},
            {**proof, "baseline": "other"},
            {**proof, "memory": {"breach": True}},
        ):
            with self.subTest(changed=changed), self.assertRaises(ValueError):
                require_source_proof(changed, raw)


if __name__ == "__main__":
    unittest.main()
