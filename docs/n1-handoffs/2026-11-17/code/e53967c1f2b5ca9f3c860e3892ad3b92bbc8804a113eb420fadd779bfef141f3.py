import copy
import json
import unittest

from common import sha
from finalize_b117_v4 import ROOT, require_round4
import test_verify_b117_round4 as focused_tests
from verify_b117_round4 import PARENT


class FourthRoundBindingTests(unittest.TestCase):
    def setUp(self):
        fixture = focused_tests.FocusedRegressionContractTests()
        fixture.setUp()
        models = {"reading_options.py": "options", "reading_exposure.py": "exposure", "n1lib.py": "parse"}
        fixture.result["models"] = models
        self.index = {
            "batch": 117, "parent": PARENT, "comparisonCards": {c: {} for c in ("銀", "語", "休")},
            "characterSources": [{"source": "維"}], "models": {k: {"sha256": v} for k, v in models.items()},
            "kanjidic2": {"sha256": "kd", "completeRecords": 5},
            "jmdict": {"sha256": "jm", "completeEntries": 27, "exactWrittenQueries": {"銀": ["id"]}},
            "pinnedInputs": {"KANJIDIC2": {"sha256": "raw-kd"}, "JMdict": {"sha256": "raw-jm"}},
        }
        self.raw_index = json.dumps(self.index).encode()
        self.receipt = {
            "batch": 117, "parent": PARENT, "sourceEvidence": {"indexSha256": sha(self.raw_index)},
            "validation": {"focusedCheck": {"sha256": "check"}},
        }
        self.proof = {
            "status": "PASS", "batch": 117, "candidate": "signed", "parent": PARENT,
            "sourceEvidenceIndex": f"{ROOT}/source-evidence-index.json",
            "sourceEvidenceIndexSha256": sha(self.raw_index),
            "manifestSha256": sha(b"manifest"), "targetSha256": sha(b"target"),
            "comparisonCardsVerified": 3, "characterSourcesVerified": 1,
            "modelSnapshotsVerified": models, "focusedCheck": fixture.result,
            "focusedTool": {"sha256": "check"}, "priorSourceEvidencePreserved": True,
            "scopeVerified": ["kanji/維.md", "manifest.json"], "memory": {"breach": None},
            "dictionaryRecords": [
                {"source": "KANJIDIC2", "inputSha256": "raw-kd", "extractionSha256": "kd",
                 "completeRecordsVerified": 5, "exactWrittenQueriesVerified": 0},
                {"source": "JMdict", "inputSha256": "raw-jm", "extractionSha256": "jm",
                 "completeRecordsVerified": 27, "exactWrittenQueriesVerified": 1},
            ],
        }

    def verify(self, proof):
        require_round4("signed", proof, self.raw_index, json.dumps(self.receipt).encode(), b"manifest", b"target")

    def test_rejects_stale_snapshot_source_or_model(self):
        self.verify(self.proof)
        for patch in (
            {"candidate": PARENT}, {"parent": "wrong"}, {"sourceEvidenceIndexSha256": "wrong"},
            {"manifestSha256": "wrong"}, {"targetSha256": "wrong"}, {"comparisonCardsVerified": 2},
            {"modelSnapshotsVerified": {}}, {"priorSourceEvidencePreserved": False},
            {"focusedTool": {"sha256": "different"}}, {"dictionaryRecords": []},
            {"scopeVerified": ["manifest.json"]},
        ):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                self.verify({**self.proof, **patch})

    def test_rejects_missing_or_regressed_focused_pool(self):
        for patch in ({"yuiReachable": True}, {"seedsChecked": 100}, {"fallback": {"3": ["ゆい"]}}):
            proof = copy.deepcopy(self.proof)
            proof["focusedCheck"]["pools"]["Starter+target+由"].update(patch)
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                self.verify(proof)


if __name__ == "__main__":
    unittest.main()
