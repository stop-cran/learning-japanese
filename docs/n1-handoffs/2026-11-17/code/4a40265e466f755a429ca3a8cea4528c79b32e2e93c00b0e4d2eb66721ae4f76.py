import copy
import sys
import unittest

from verify_b129_evidence import ORDER, verify_execution, verify_pair_member, verify_query_map


class EvidenceTests(unittest.TestCase):
    def test_query_map_requires_all_matching_predicates(self):
        raw = b"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>XY</keb></k_ele>" \
              b"<r_ele><reb>reading</reb></r_ele></entry></JMdict>"
        selection = {"mode": "union", "queries": ["contains-keb:X", "exact-reb:reading", "exact-keb:missing"]}
        recorded = {"1": ["contains:X", "exact-reading:reading"]}
        verify_query_map(raw, selection, recorded)
        with self.assertRaises(ValueError):
            verify_query_map(raw, selection, {"1": ["contains:X"]})
        with self.assertRaises(ValueError):
            verify_query_map(raw, selection, {"1": recorded["1"] + ["exact-keb:missing"]})

    def test_pairs_require_guard_and_both_snapshot_labels(self):
        card = {"title": "target", "quiz_exclusions": ["B"], "distractors": []}
        scan = {"matches": ["B"]}
        item = {"kanji": "A", "targetTitle": "target", "pairs": [{
            "pair": ["A", "B"], "decision": "guard", "comparisonTitle": "comparison",
            "baselineCardSha256": "hash", "scanMatch": True,
            "targetLabelOnComparison": "forward", "comparisonLabelOnTarget": "reverse"}]}
        verify_pair_member(item, card, scan, {"B": ("comparison", "hash")})
        changed = copy.deepcopy(item)
        changed["pairs"][0]["decision"] = "distinct"
        with self.assertRaises(ValueError):
            verify_pair_member(changed, card, scan, {"B": ("comparison", "hash")})
        with self.assertRaises(ValueError):
            verify_pair_member(item, card, scan, {"B": ("stale title", "hash")})

    def test_gate_execution_rejects_overlap_and_command_drift(self):
        commands = {name: [name] for name in ORDER}
        receipts = {name: {
            "startedAt": f"2026-11-16T07:{index:02d}:00+00:00",
            "completedAt": f"2026-11-16T07:{index:02d}:10+00:00",
            "command": [sys.executable, "-B", name], "commonHelperSha256": "hash",
            "cleanupTimeoutSecondsPerStage": 10, "activeError": None, "cleanupError": None,
        } for index, name in enumerate(ORDER)}
        verify_execution(receipts, commands, "hash")
        overlap = copy.deepcopy(receipts)
        overlap[ORDER[1]]["startedAt"] = receipts[ORDER[0]]["startedAt"]
        with self.assertRaises(ValueError):
            verify_execution(overlap, commands, "hash")
        drift = copy.deepcopy(receipts)
        drift["lint"]["command"].append("--skip")
        with self.assertRaises(ValueError):
            verify_execution(drift, commands, "hash")


if __name__ == "__main__":
    unittest.main()
