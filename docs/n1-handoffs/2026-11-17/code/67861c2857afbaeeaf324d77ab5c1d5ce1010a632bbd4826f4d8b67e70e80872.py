import copy
import itertools
import unittest

from prepare_b131_source_facts import CANDIDATE_BASE, MEMBERS, SOURCE_BASE
from verify_b131_gate_evidence_v2 import memory_ok
from verify_b131_packet_evidence_v2 import pair_coverage


class AdmissionEvidenceTests(unittest.TestCase):
    def test_exact_memory_admission_and_abort_boundaries(self):
        memory = {
            "breach": None, "freeRamBeforeBytes": 2 * 1024**3 + 1,
            "minimumObservedFreeRamBytes": 1024**3, "abortThresholdBytes": 1024**3,
            "samplingIntervalSeconds": 0.25,
        }
        memory_ok(memory)
        for field, value in (
            ("freeRamBeforeBytes", 2 * 1024**3),
            ("minimumObservedFreeRamBytes", 1024**3 - 1),
            ("samplingIntervalSeconds", 1),
            ("breach", {"freeRam": 1}),
        ):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "memory contract"):
                memory_ok(dict(memory, **{field: value}))

    def fixture(self):
        cards, scans, members = {}, {}, []
        for char in MEMBERS:
            cards[char] = {"title": char, "quiz_exclusions": [], "distractors": ["X"]}
            scans[char] = ({"matches": ["X"]}, {"matches": ["X"]}, "scan-hash")
            members.append({
                "kanji": char, "targetTitle": char, "scanFile": f"scans-002/{char}.json",
                "scanSha256": "scan-hash", "scanRows": 1254,
                "originalScanBase": SOURCE_BASE, "candidateBase": CANDIDATE_BASE,
                "pairs": [{"pair": [char, "X"], "comparisonTitle": "comparison",
                           "baselineCardSha256": "card-hash", "decision": "curated", "scanMatch": True,
                           "targetLabelOnComparison": "first direction", "comparisonLabelOnTarget": "second direction"}],
            })
        members += [{"newMemberPair": list(pair), "decision": "distinct", "bothDirections": "different senses"}
                    for pair in itertools.combinations(MEMBERS, 2)]
        return {"base": CANDIDATE_BASE, "members": members}, cards, scans, {"X": ("comparison", "card-hash")}

    def test_finite_pairs_require_both_directions_and_every_scan_match(self):
        disposition, cards, scans, comparisons = self.fixture()
        self.assertEqual(pair_coverage(disposition, cards, scans, comparisons), (3, 3))
        for mutation in ("omit-row", "duplicate-row", "missing-direction", "wrong-scan", "wrong-exclusion"):
            altered, changed_cards = copy.deepcopy(disposition), copy.deepcopy(cards)
            member = altered["members"][0]
            if mutation == "omit-row":
                member["pairs"].clear()
            elif mutation == "duplicate-row":
                member["pairs"].append(member["pairs"][0])
            elif mutation == "missing-direction":
                member["pairs"][0]["comparisonLabelOnTarget"] = ""
            elif mutation == "wrong-scan":
                member["originalScanBase"] = CANDIDATE_BASE
            else:
                changed_cards[MEMBERS[0]]["quiz_exclusions"] = ["X"]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                pair_coverage(altered, changed_cards, scans, comparisons)

    def test_new_member_pairs_cannot_be_omitted(self):
        disposition, cards, scans, comparisons = self.fixture()
        disposition["members"].pop()
        with self.assertRaisesRegex(ValueError, "member-pair inventory"):
            pair_coverage(disposition, cards, scans, comparisons)


if __name__ == "__main__":
    unittest.main()
