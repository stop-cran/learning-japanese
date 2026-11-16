import json
import unittest

from b129_confirmation_presentation import canonical
from common import WS, frozen, load_batch, load_module, sha


class CompactReviewTests(unittest.TestCase):
    def setUp(self):
        self.root = WS / "scratch-130" / "review"
        self.proof = json.loads(frozen(self.root / "compact-review-packet-preflight-001.json"))
        self.adapter = load_module("b130_compact_adapter_test", WS / "review-tools" / "b130_compact_common.py")

    def test_complete_record_infosets_and_unrelated_bytes_are_preserved(self):
        source = WS / "review-packets" / "batch-130-ce1b5c89"
        packet, sums, digest = self.adapter.verify_packet(load_batch(130))
        original = json.loads(frozen(source / "SHA256SUMS.json"))
        self.assertEqual(digest, self.proof["packetManifest"]["sha256"])
        self.assertEqual(set(sums) - set(original), {"evidence/xml-presentation.json"})
        for relative in self.proof["dictionaries"]:
            before, after = frozen(source / relative), frozen(packet / relative)
            self.assertEqual(canonical(before), canonical(after))
            self.assertLess(len(after.splitlines()), len(before.splitlines()) // 10)
        changed = {name for name in original if original[name] != sums[name]}
        self.assertEqual(changed, set(self.proof["changedFiles"]))
        old_packet, new_packet = (json.loads(frozen(path / "packet.json")) for path in (source, packet))
        self.assertEqual(new_packet.pop("dictionaryPresentation"), "evidence/xml-presentation.json")
        self.assertEqual(old_packet, new_packet)

    def test_context_held_initial_has_no_acceptance_and_is_not_in_packet(self):
        hold = json.loads(frozen(self.root / "N1-B130-CLAUDE-001-hold.json"))
        self.assertFalse(hold["reviewAccepted"])
        self.assertFalse(hold["finalAcceptance"])
        self.assertFalse((self.root / "N1-B130-CLAUDE-001-acceptance.json").exists())
        packet, sums, _ = self.adapter.verify_packet(load_batch(130))
        self.assertNotIn(hold["report"]["sha256"], sums.values())
        self.assertNotIn(sha(frozen(self.root / "N1-B130-CLAUDE-001-hold.json")), sums.values())
        self.assertNotIn("heldReview", json.loads(frozen(packet / "packet.json")))

    def test_adapter_rejects_another_batch(self):
        with self.assertRaisesRegex(ValueError, "limited to B130"):
            self.adapter.packet_dir({"batch": 129, "candidate": "a" * 40})


if __name__ == "__main__":
    unittest.main()
