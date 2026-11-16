import copy
import json
import unittest

from common import frozen, json_bytes
from finalize_b130 import (CANDIDATE, PROOF_SHA, ROOT, check_archive, check_proofs,
                           execution_files, read_binding)


class FinalizerTests(unittest.TestCase):
    def setUp(self):
        self.proof = json.loads(frozen(ROOT / "revision-evidence-001" / "verification.json",
                                      PROOF_SHA))
        self.runtime = read_binding(self.proof["proofs"]["runtime"])[1]
        self.sources = read_binding(self.proof["proofs"]["sources"])[1]

    def test_exact_signed_proofs_and_nonsemantic_boundaries(self):
        check_proofs(self.proof, self.runtime, self.sources)
        for index, field, value in ((0, "reviewAccepted", True), (1, "candidate", "0" * 40),
                                    (2, "publicationAccepted", True)):
            values = copy.deepcopy([self.proof, self.runtime, self.sources])
            values[index][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_proofs(*values)
        changed = copy.deepcopy(self.proof)
        changed["gateSets"]["committed"]["gates"].pop()
        with self.assertRaises(ValueError):
            check_proofs(changed, self.runtime, self.sources)

    def test_archive_must_cover_excluded_as_well_as_accepted_chains(self):
        provenance = {"reviewLineage": [{"run": "accepted", "chains": [{"path": "a"}]}],
                      "excludedInitialRuns": [{"run": "excluded", "chains": [{"path": "b"}]}]}
        raw = json_bytes(provenance)
        from common import sha
        archive = {"status": "PASS", "candidate": CANDIDATE, "provenanceSha256": sha(raw),
                   "chains": [{"run": "accepted", "path": "a"}, {"run": "excluded", "path": "b"}]}
        check_archive(archive, provenance, raw)
        for rows in (archive["chains"][:1], archive["chains"] * 2):
            with self.assertRaises(ValueError):
                check_archive({**archive, "chains": rows}, provenance, raw)

    def test_preserved_failed_execution_cannot_be_relabelled_successful(self):
        path = ROOT / "fresh-claude-adjudication-execution-002"
        self.assertEqual(set(execution_files(path, 1)), {"receipt.json", "output.log"})
        with self.assertRaises(ValueError):
            execution_files(path, 0)


if __name__ == "__main__":
    unittest.main()
