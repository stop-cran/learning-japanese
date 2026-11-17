import copy
import json
import unittest
from pathlib import Path

from common import json_bytes, load_module, sha

assembler = load_module("b134_actual_integration_assembler",
                        Path(__file__).with_name("assemble-b134-integration-v2.py"))
c = assembler.contract


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.plan = {"merge": "a" * 40, "signedClosure": "b" * 40}
        self.previous = json_bytes({
            "status": "textual-review-closed-publication-pending",
            "accounting": {"publishedPendingRecordsWithCards": 271, "undelivered": 957},
            "nested": {"originalVerdict": "NEEDS FIX", "limits": ["Unchanged limit"]},
        })
        self.manifest = json_bytes({
            "contentVersion": "test-version",
            "files": {f"kanji/fixture-{i}.md": "0" * 64 for i in range(8747)},
        })
        self.confirmations = {
            family: {
                "run": f"N1-B134-{family.upper()}-INTEGRATION-001",
                **{key: (family + "-" + key).encode()
                   for key in ("acceptance", "report", "final", "adjudication")},
            }
            for family in ("claude", "gpt")
        }

    def build(self, evidence=None):
        return assembler.assemble(
            self.plan, json_bytes(self.plan), self.previous, self.manifest,
            self.confirmations, evidence or {})

    def test_exact_evidence_and_all_old_ledger_values_are_preserved(self):
        files, ledger_raw = self.build({"verification/example.json": b"real-binding"})
        ledger, previous = json.loads(ledger_raw), json.loads(self.previous)
        self.assertEqual({k: v for k, v in ledger.items() if k not in c.EXTENSION_KEYS}, previous)
        self.assertEqual(files["previous-progress.json"], self.previous)
        self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 271)
        c.inventory(files, ("provenance.json", "validation-provenance.json"))
        for value in self.confirmations.values():
            self.assertEqual(files[f"runs/{value['run']}/report.md"], value["report"])
        self.assertEqual(ledger["integrationReview"]["closureProvenanceSha256"],
                         sha(files["provenance.json"]))

    def test_reserved_paths_and_preexisting_integration_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "reserved archive paths"):
            self.build({"previous-progress.json": b"replacement"})
        value = json.loads(self.previous)
        value["activeReviewedSnapshot"] = "c" * 40
        self.previous = json_bytes(value)
        with self.assertRaisesRegex(ValueError, "already recorded"):
            self.build()

    def test_changed_report_or_delivery_credit_is_rejected(self):
        files, ledger_raw = self.build()
        ledger = json.loads(ledger_raw)
        modified = copy.deepcopy(ledger)
        modified["accounting"]["publishedPendingRecordsWithCards"] = 272
        with self.assertRaisesRegex(ValueError, "preserve every original value"):
            c.closure_data(self.plan, json.loads(self.previous), modified, files,
                           self.manifest, self.confirmations)
        changed = dict(files)
        changed["runs/N1-B134-GPT-INTEGRATION-001/report.md"] = b"changed"
        with self.assertRaisesRegex(ValueError, "Changed archive bytes"):
            c.closure_data(self.plan, json.loads(self.previous), ledger, changed,
                           self.manifest, self.confirmations)


if __name__ == "__main__":
    unittest.main()
