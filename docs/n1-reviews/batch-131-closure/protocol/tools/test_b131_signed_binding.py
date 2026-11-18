import copy
import json
import unittest
from unittest.mock import patch

import b131_base_binding_v2 as bridge
from common import sha


def encoded(value):
    return json.dumps(value, sort_keys=True).encode("utf-8")


class SignedBindingTests(unittest.TestCase):
    def setUp(self):
        self.candidate = "d" * 40
        self.calls = []
        entries = [
            (f"100644 blob {'a' * 40}\tkanji/{chr(0x4e00 + index)}.md").encode("utf-8")
            for index in range(1254)
        ]
        tree = b"\0".join(entries) + b"\0"
        scans = {
            f"scans/{index}.json": encoded({"base": bridge.SOURCE_BASE, "matches": []})
            for index in range(6)
        }
        record = {
            "originalSourceBase": bridge.SOURCE_BASE,
            "candidateBase": bridge.CANDIDATE_BASE,
            "coordinatorProofSha256": bridge.INCOMING_PROOF_SHA,
            "baselineKanjiTreeSha256": sha(b"\n".join(entries) + b"\n"),
            "baselineKanjiEntries": 1254,
            "originalScans": {path: sha(raw) for path, raw in scans.items()},
        }
        self.observed = encoded(record)
        self.proof = {
            "status": "PASS_WORD_ONLY_BASELINE_ADAPTATION",
            "originalBase": bridge.SOURCE_BASE,
            "incomingBase": bridge.CANDIDATE_BASE,
            "membershipPreservedByExactTreeEquality": True,
            "memory": {"breach": False},
        }
        self.responses = {
            ("show", "-s", "--format=%P", self.candidate): bridge.CANDIDATE_BASE.encode() + b"\n",
            ("show", self.candidate + ":" + bridge.PREFIX + "base-adaptation.json"): self.observed,
            ("show", self.candidate + ":" + bridge.PREFIX + "selection.json"):
                encoded({"base": bridge.SOURCE_BASE}),
            ("ls-tree", "-rz", bridge.SOURCE_BASE, "--", "kanji"): tree,
            ("ls-tree", "-rz", bridge.CANDIDATE_BASE, "--", "kanji"): tree,
        }
        for path, raw in scans.items():
            self.responses[("show", self.candidate + ":" + bridge.PREFIX + path)] = raw
        for path in ("docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json"):
            for commit in (bridge.SOURCE_BASE, bridge.CANDIDATE_BASE, self.candidate):
                self.responses[("show", commit + ":" + path)] = encoded({"source": path})

    def git(self, *args):
        self.calls.append(args)
        return self.responses[args]

    def frozen(self, path, expected):
        if path.name == "author-base-adaptation-observed-001.json":
            self.assertEqual(expected, bridge.OBSERVED_SHA)
            return self.observed
        self.assertEqual(path.name, "incoming-main-verification-001.json")
        self.assertEqual(expected, bridge.INCOMING_PROOF_SHA)
        return encoded(self.proof)

    def verify(self):
        with patch.object(bridge, "frozen", side_effect=self.frozen):
            return bridge.verify_signed_binding(self.git, self.candidate)

    def test_signed_blobs_preserve_both_bases_and_exact_scan_inventory(self):
        result = self.verify()
        self.assertEqual(result["sourceBase"], bridge.SOURCE_BASE)
        self.assertEqual(result["candidateBase"], bridge.CANDIDATE_BASE)
        self.assertEqual(result["candidate"], self.candidate)
        self.assertEqual(result["baselineKanjiEntries"], 1254)
        self.assertEqual(len(result["originalScans"]), 6)
        self.assertEqual(result["signedAdaptationSha256"], sha(self.observed))
        signed_reads = [args[1] for args in self.calls if args[0] == "show" and len(args) == 2]
        for path in result["originalScans"]:
            self.assertIn(self.candidate + ":" + bridge.PREFIX + path, signed_reads)

    def test_wrong_parent_or_changed_signed_adaptation_is_rejected(self):
        for key, changed, message in (
            (("show", "-s", "--format=%P", self.candidate), bridge.SOURCE_BASE.encode(), "direct child"),
            (("show", self.candidate + ":" + bridge.PREFIX + "base-adaptation.json"),
             self.observed + b"\n", "Signed adaptation differs"),
        ):
            original = self.responses[key]
            with self.subTest(key=key):
                self.responses[key] = changed
                with self.assertRaisesRegex(ValueError, message):
                    self.verify()
                self.responses[key] = original

    def test_relabelled_selection_or_changed_signed_scan_is_rejected(self):
        for name, changed, message in (
            ("selection.json", encoded({"base": bridge.CANDIDATE_BASE}), "selection was relabelled"),
            ("scans/0.json", encoded({"base": bridge.CANDIDATE_BASE, "matches": []}), "bytes changed"),
        ):
            key = ("show", self.candidate + ":" + bridge.PREFIX + name)
            original = self.responses[key]
            with self.subTest(name=name):
                self.responses[key] = changed
                with self.assertRaisesRegex(ValueError, message):
                    self.verify()
                self.responses[key] = original

    def test_source_index_drift_is_rejected_at_each_later_commit(self):
        path = "docs/n1-sources/source-index.json"
        for commit in (bridge.CANDIDATE_BASE, self.candidate):
            key = ("show", commit + ":" + path)
            original = self.responses[key]
            with self.subTest(commit=commit):
                self.responses[key] += b"\n"
                with self.assertRaisesRegex(ValueError, "Source baseline changed"):
                    self.verify()
                self.responses[key] = original

    def test_unaccepted_or_mismatched_incoming_proof_is_rejected(self):
        original = copy.deepcopy(self.proof)
        for field, value in (
            ("status", "PREPARATION_ONLY"),
            ("originalBase", bridge.CANDIDATE_BASE),
            ("incomingBase", bridge.SOURCE_BASE),
            ("membershipPreservedByExactTreeEquality", False),
            ("memory", {"breach": True}),
        ):
            with self.subTest(field=field):
                self.proof = dict(original, **{field: value})
                with self.assertRaisesRegex(ValueError, "Incoming baseline proof differs"):
                    self.verify()


if __name__ == "__main__":
    unittest.main()
