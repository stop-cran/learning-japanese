import copy
import unittest

from common import sha
from finalize_b124 import RESPONSE_PATHS, RUNTIME_PROOF_SHA, SIGNER
from verify_b124_response_correction import (
    ADMISSION_SHA, BRIEF_SHA, CLOSED, PARENT, R2_HANDOFF_SHA, check_delta, check_handoff,
)

CANDIDATE = "c" * 40
BASE = "b" * 40
FILES = {path: path.encode() for path in RESPONSE_PATHS}
FILES["manifest.json"] = b"{}"
PRIOR = {"manifest.json": b"{}"}
TREES = {"kanji": "k" * 40, "strokes": "s" * 40, "words": "w" * 40}
ADDENDUM = {"schemaVersion": 1}


def handoff():
    return {
        "commit": {"sha": CANDIDATE, "parent": PARENT, "publishedBase": BASE, "signatureVerified": True,
                   "signingKeyFingerprint": SIGNER, "worktreeClean": True, "push": False, "amended": False},
        "fileInventory": {"count": 2, "exactPaths": sorted(RESPONSE_PATHS), "files": [
            {"path": path, "bytes": len(FILES[path]), "sha256": sha(FILES[path])} for path in sorted(RESPONSE_PATHS)]},
        "correctionBindings": {"addendum": {"bindings": copy.deepcopy(ADDENDUM)}},
        "preservedHistory": {
            "verifiedR2Proof": {"sha256": RUNTIME_PROOF_SHA},
            "priorR2Handoff": {"sha256": R2_HANDOFF_SHA, "candidate": PARENT},
            "assignmentBrief": {"sha256": BRIEF_SHA}, "freshAdmission": {"sha256": ADMISSION_SHA},
            "unchangedSourceAndRuntimeFiles": [
                {"path": "manifest.json", "sha256": sha(b"{}"), "sameAsSignedParent": True}],
        },
        "runtimeByteEquality": {"trees": {name: {"gitTree": value, "parentGitTree": value, "byteIdentical": True}
                                          for name, value in TREES.items()}},
        "newGateRuns": {"authoring": [], "committed": [], "priorR2RunsReusedAsEvidence": False},
        "publication": dict(CLOSED),
    }


def run(value, prior=PRIOR, trees=TREES):
    check_handoff(value, CANDIDATE, BASE, FILES.__getitem__, prior.__getitem__,
                  lambda rev, name: trees[name], ADDENDUM)


class DocumentationDeltaTests(unittest.TestCase):
    def test_exact_additive_documents_only(self):
        valid = [["A", path] for path in sorted(RESPONSE_PATHS)]
        check_delta(valid)
        for changed in (
            valid[:-1], valid + [["M", "manifest.json"]], valid + [["M", "kanji/x.md"]],
            [["M", valid[0][1]], valid[1]], [valid[0], valid[0]],
            [valid[0], ["A", "docs/n1-sources/unrelated.json"]],
        ):
            with self.subTest(delta=changed), self.assertRaises(ValueError):
                check_delta(changed)


class HandoffBindingTests(unittest.TestCase):
    def test_valid_handoff(self):
        run(handoff())

    def test_rejects_relabeled_handoff(self):
        def mutate(path, value):
            item = handoff()
            target = item
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value
            return item

        for path, value in (
            (("commit", "sha"), "d" * 40), (("commit", "parent"), BASE), (("commit", "amended"), True),
            (("commit", "push"), True), (("commit", "signingKeyFingerprint"), "0" * 40),
            (("fileInventory", "count"), 3), (("correctionBindings", "addendum", "bindings"), {"schemaVersion": 2}),
            (("preservedHistory", "verifiedR2Proof", "sha256"), "0" * 64),
            (("preservedHistory", "priorR2Handoff", "candidate"), CANDIDATE),
            (("newGateRuns", "committed"), [{"name": "unit"}]),
            (("newGateRuns", "priorR2RunsReusedAsEvidence"), True), (("publication", "published"), True),
        ):
            with self.subTest(path=path), self.assertRaises(ValueError):
                run(mutate(path, value))

    def test_rejects_inventory_hash_and_changed_preserved_bytes(self):
        item = handoff()
        item["fileInventory"]["files"][0]["sha256"] = "0" * 64
        with self.assertRaises(ValueError):
            run(item)
        with self.assertRaises(ValueError):
            run(handoff(), prior={"manifest.json": b"[]"})

    def test_rejects_changed_or_missing_runtime_tree(self):
        with self.assertRaises(ValueError):
            run(handoff(), trees={**TREES, "kanji": "x" * 40})
        item = handoff()
        del item["runtimeByteEquality"]["trees"]["words"]
        with self.assertRaises(ValueError):
            run(item)


if __name__ == "__main__":
    unittest.main()
