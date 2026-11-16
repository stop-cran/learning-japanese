import copy
import json
import sys
import unittest

from common import WS, sha
from verify_b131_revision_evidence_001 import (
    PREFIX, REPO, SCRATCH, additive_body, check_gate_context, pair_checks)

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse


class EvidenceTests(unittest.TestCase):
    def test_additive_prose_preserves_existing_text(self):
        before = b"quiz_exclusions: [a]\r\n---\r\nold note\r\n\r\nMetadata: original\r\n"
        after = b"quiz_exclusions: [a, b]\r\n---\r\nold note\r\n- qualified addition\r\n\r\nMetadata: original\r\n"
        self.assertIn("qualified addition", additive_body(before, after))
        for changed in (after.replace(b"old note", b"rewritten"),
                        after.replace(b"Metadata: original", b"Metadata: changed")):
            with self.assertRaises(ValueError):
                additive_body(before, changed)

    def test_pair_coverage_directions_and_real_labels(self):
        packet = REPO / PREFIX
        table = json.loads((packet / "pair-dispositions-001.json").read_bytes())
        receipt = json.loads((packet / "source-receipt.json").read_bytes())
        parse_card = lambda raw: parse(raw.decode("utf-8").replace("\r\n", "\n"))[0]
        chars = {row["pair"][0] for row in table["rows"]}
        cards = {ch: parse_card((REPO / "kanji" / (ch + ".md")).read_bytes()) for ch in chars}
        others = {row["pair"][1] for row in table["rows"]}
        comparison = {}
        for ch in others:
            raw = (packet / "comparison-cards" / (ch + ".md")).read_bytes()
            comparison[ch] = (parse_card(raw), raw)
        self.assertEqual(sum(map(len, pair_checks(table, cards, receipt, comparison).values())), 16)
        bad = copy.deepcopy(table)
        bad["rows"].pop()
        with self.assertRaises(ValueError):
            pair_checks(bad, cards, receipt, comparison)
        for key, value in (("targetLabelOnComparison", ""), ("displayedLabels", ["wrong", "title"]),
                           ("directExclusionOnNewEndpoint", False), ("openQuizHold", True)):
            bad = copy.deepcopy(table)
            bad["rows"][0][key] = value
            with self.assertRaises(ValueError):
                pair_checks(bad, cards, receipt, comparison)

    def test_gate_scope_and_implementation_cannot_be_substituted(self):
        directory = SCRATCH / "reconciliation-001" / "author-gates-001"
        summary, admission = [json.loads((directory / name).read_bytes())
                              for name in ("summary.json", "admission.json")]
        wrapper = sha((SCRATCH / "r131_gates.py").read_bytes())
        implementation = sha((SCRATCH / "run_b131_gates.py").read_bytes())
        args = ("author", "not-used-for-author", summary["manifestSha256"], wrapper, implementation)
        check_gate_context(summary, admission, *args)
        for key, value in (("publishedBase", "wrong"), ("startingHead", "wrong"), ("serial", False)):
            bad = copy.deepcopy(summary)
            bad[key] = value
            with self.assertRaises(ValueError):
                check_gate_context(bad, admission, *args)
        with self.assertRaises(ValueError):
            check_gate_context(summary, admission, *args[:-1], "wrong-implementation")


if __name__ == "__main__":
    unittest.main()
