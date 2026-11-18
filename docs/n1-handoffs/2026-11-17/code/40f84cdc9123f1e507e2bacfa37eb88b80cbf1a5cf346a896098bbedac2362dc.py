import ast
import copy
import json
import sys
import unittest

from b130_delta_pairs import check_responses, check_table
from common import TOOLS, WS, frozen
from prepare_b130_delta_gates import derive


class DeltaEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.repo = WS / "b130-worktree"
        self.packet = self.repo / "docs" / "n1-sources" / "batch-130-reconciliation"
        self.source = lambda name: (self.packet / name).read_bytes()
        self.previous = self.source("pair-dispositions-001.json")
        self.table = json.loads(self.source("pair-dispositions-002.json"))
        self.receipt = json.loads(self.source("source-receipt.json"))
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        self.metadata = {char: parse((self.repo / "kanji" / (char + ".md")).read_text(
            encoding="utf-8").replace("\r\n", "\n"))[0] for char in ("塀", "拍", "耗")}

    def test_exact_observed_pair_delta_and_retained_family_history(self):
        proof = check_table(self.previous, self.table, self.metadata, self.receipt)
        self.assertFalse(proof["semanticAcceptance"])
        self.assertEqual(set(check_responses(self.source, self.source("pair-dispositions-002.json"))),
                         {"claude", "gpt"})
        changed = copy.deepcopy(self.table)
        changed["rows"][0]["qualification"] += " changed"
        with self.assertRaises(ValueError):
            check_table(self.previous, changed, self.metadata, self.receipt)
        changed = copy.deepcopy(self.metadata)
        changed["拍"]["quiz_exclusions"].remove("響")
        with self.assertRaises(ValueError):
            check_table(self.previous, self.table, changed, self.receipt)

    def test_gate_derivation_preserves_commands_and_full_verification(self):
        original = frozen(TOOLS / "b130_revision_gates.py").decode("utf-8")
        text = derive(original)
        compile(text, "delta_gate_test", "exec")
        for name in ("commands", "verify"):
            old = next(node for node in ast.parse(original).body
                       if isinstance(node, ast.FunctionDef) and node.name == name)
            new = next(node for node in ast.parse(text).body
                       if isinstance(node, ast.FunctionDef) and node.name == name)
            self.assertEqual(ast.dump(old), ast.dump(new))


if __name__ == "__main__":
    unittest.main()
