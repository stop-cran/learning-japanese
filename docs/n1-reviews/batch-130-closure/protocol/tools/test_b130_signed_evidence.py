import copy
import json
import unittest

from b130_signed_evidence import (BASE, FINAL_VERIFIER_SHA, MEMBERS, PREFIX, RESIDUAL, SUPPORTS,
                                  receipt_outputs, verify_final_proof, verify_progress, verify_reading_keys)


class SignedEvidenceTests(unittest.TestCase):
    def test_signed_new_pairs_require_all_three_written_rationales(self):
        from verify_b130_evidence_v3 import new_pair_sets
        a, b, c = MEMBERS
        items = [{"newMemberPair": pair, "decision": "distinct", "bothDirections": "Both labels differ."}
                 for pair in ([a, b], [a, c], [b, c])]
        guards, curated = new_pair_sets(items)
        self.assertTrue(all(not values for values in [*guards.values(), *curated.values()]))
        for value in (True, False, "", " "):
            bad = copy.deepcopy(items)
            bad[0]["bothDirections"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                new_pair_sets(bad)
        with self.assertRaises(ValueError):
            new_pair_sets(items[:-1])

    def test_receipt_requires_unambiguous_output_binding(self):
        self.assertEqual(receipt_outputs({"outputs": {"x": 1}}), {"x": 1})
        self.assertEqual(receipt_outputs({"finalAdditionalOutput": 2}), {RESIDUAL: 2})
        for value in ({}, {"outputs": {}, "finalAdditionalOutput": {}}):
            with self.assertRaises(ValueError):
                receipt_outputs(value)

    def test_final_proof_binds_candidate_and_original_source_proof(self):
        proof = {"batch": 130, "base": BASE, "candidate": "candidate", "status": "PASS",
                 "memory": {"breach": None}, "sourceProof": {"sha256": "source"},
                 "verifierSha256": FINAL_VERIFIER_SHA, "signedInputs": {PREFIX + RESIDUAL: "hash"}}
        verify_final_proof(proof, "source", "candidate")
        for key, value in (("candidate", "other"), ("verifierSha256", "other"), ("signedInputs", {}),
                           ("sourceProof", {"sha256": "other"}), ("memory", {"breach": True})):
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify_final_proof({**proof, key: value}, "source", "candidate")

    def test_json_reading_keys_bind_exact_producer_and_log(self):
        raw = b'extras = json.loads((PACKET / "reading-keys.json").read_text(encoding="utf-8"))["testedKeys"]'
        keys = {char: ["x", "y"] for char in MEMBERS}
        data = json.dumps({"testedKeys": keys}).encode()
        log = ("Explicit supplemental reading keys: " + json.dumps(keys, ensure_ascii=False) + "\n").encode()
        self.assertEqual(verify_reading_keys(raw, data, log, {MEMBERS[0]: ["x"]}), keys)
        for producer, source, output in (
            (raw.replace(b"reading-keys.json", b"different.json"), data, log),
            (raw, data, log + log),
            (raw, data, b"Explicit supplemental reading keys: {}\n"),
            (raw, json.dumps({"testedKeys": {MEMBERS[0]: ["x"]}}).encode(), log),
        ):
            with self.assertRaises(ValueError):
                verify_reading_keys(producer, source, output, {MEMBERS[0]: ["x"]})

    def test_progress_never_counts_unpublished_cards(self):
        facts = {"wordProseExceptions": [], "pairDispositions": "pair-dispositions-002.json",
                 "expectedJmdictFamilies": 519}
        payload = {"manifestSha256": "hash", "contentVersion": "version"}
        progress = {"batch": 130, "base": BASE, "status": "local-unreviewed-author-candidate",
                    "members": MEMBERS, "sourceRows": [191, 419, 879], "publishedDelivered": 261,
                    "frozenTotal": 1228, "undelivered": 967, "localUnpublishedDrafts": 3,
                    "deliveryNotIncremented": True,
                    "supports": [[char, word] for char in MEMBERS for word in SUPPORTS[char]],
                    "proseException": None, "manifestSha256": "hash", "contentVersion": "version",
                    "activePairTable": "batch-130/pair-dispositions-002.json", "completeJmdictFamilies": 519}
        verify_progress(progress, facts, payload)
        for key, value in (("publishedDelivered", 264), ("deliveryNotIncremented", False),
                           ("status", "published"), ("manifestSha256", "wrong"),
                           ("proseException", "unreviewed rewrite")):
            changed = copy.deepcopy(progress)
            changed[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                verify_progress(changed, facts, payload)


if __name__ == "__main__":
    unittest.main()
