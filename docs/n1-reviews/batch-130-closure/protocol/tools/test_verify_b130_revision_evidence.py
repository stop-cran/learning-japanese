import copy
import json
import unittest

from verify_b130_revision_evidence import PREFIX, REPO, ROOT, check_inventory, check_progress, pairs


class SignedEvidenceBoundaryTests(unittest.TestCase):
    def read(self, name):
        return json.loads((REPO / name).read_bytes())

    def test_exact_packet_and_immutable_predecessor_cannot_be_narrowed(self):
        current = self.read(PREFIX + "evidence-inventory-002.json")
        prior = self.read(PREFIX + "evidence-inventory.json")
        changed = json.loads((ROOT / "revision-handoff-capture-001" / "changed-files.json").read_bytes())["files"]
        check_inventory(current, prior, changed)
        with self.assertRaises(ValueError):
            check_inventory(current, prior, changed[:-5])
        bad = copy.deepcopy(current)
        bad["files"][next(iter(prior["files"]))] = "0" * 64
        with self.assertRaises(ValueError):
            check_inventory(bad, prior, changed)

    def test_progress_preserves_actual_open_history_and_unpublished_accounting(self):
        progress = self.read("docs/n1-sources/batch-130-progress-reconciliation-002.json")
        runtime = json.loads((ROOT / "revision-runtime-proof-001.json").read_bytes())
        proof = pairs.verify(lambda name: (REPO / PREFIX / name).read_bytes(),
                             lambda char: (REPO / "kanji" / (char + ".md")).read_bytes())
        warnings = self.read("docs/n1-sources/batch-130-progress.json")["warnings"]["quizSafetyWarnings"]
        check_progress(progress, runtime, proof, progress["newEvidenceInventorySha256"], warnings)
        for field, value in (("publishedDelivered", 264), ("historicalOpenQuestionsPreserved", 0),
                             ("historicalAndRareSpellingAllocationResolved", True),
                             ("status", "published"), ("manifestSha256", "0" * 64)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_progress({**progress, field: value}, runtime, proof,
                               progress["newEvidenceInventorySha256"], warnings)


if __name__ == "__main__":
    unittest.main()
