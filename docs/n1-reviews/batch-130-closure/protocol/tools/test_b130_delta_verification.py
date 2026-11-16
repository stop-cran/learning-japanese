import ast
import copy
import json
import unittest

from common import TOOLS, frozen, sha
from prepare_b130_delta_runtime import SOURCE, SOURCE_SHA, derive
from verify_b130_source_reuse import PREVIOUS_PROOF, SOURCES_SHA, check_previous, check_reuse


class DeltaVerificationTests(unittest.TestCase):
    def setUp(self):
        source = frozen(TOOLS / SOURCE, SOURCE_SHA).decode("utf-8")
        self.text = derive(source)
        self.module = {"__name__": "delta_runtime_test"}
        exec(compile(self.text, "delta_runtime_test", "exec"), self.module)

    def test_only_one_runtime_card_and_insert_only_evidence(self):
        check = self.module["check_paths"]
        notes = self.module["NOTES"]
        changes = {"manifest.json": "M", "kanji/拍.md": "M", notes: "M",
                   self.module["PREFIX"] + "pair-dispositions-002.json": "A"}
        check(changes, {"kanji/拍.md"})
        for bad in ({**changes, "kanji/耗.md": "M"},
                    {**changes, self.module["PREFIX"] + "source-receipt.json": "M"},
                    {key: value for key, value in changes.items() if key != notes}):
            with self.assertRaises(ValueError):
                check(bad, {"kanji/拍.md"})

    def test_initial_review_snapshot_does_not_move_with_delta_parent(self):
        self.assertNotEqual(self.module["INITIAL"], self.module["PARENT"])
        original = ast.parse(frozen(TOOLS / SOURCE, SOURCE_SHA))
        revised = ast.parse(self.text)
        names = ("check_metadata", "check_runtime", "check_notes", "valid_initial_claims", "claim_boundary")
        for name in names:
            with self.subTest(name=name):
                old = next(node for node in original.body if isinstance(node, ast.FunctionDef) and node.name == name)
                new = next(node for node in revised.body if isinstance(node, ast.FunctionDef) and node.name == name)
                self.assertEqual(ast.dump(old), ast.dump(new))
        self.assertIn('final["candidate"] == INITIAL', self.text)

    def test_source_reuse_rejects_changed_or_missing_previously_verified_bytes(self):
        previous = json.loads(frozen(PREVIOUS_PROOF, SOURCES_SHA))
        self.assertIn("docs/n1-sources/batch-130-reconciliation/comparison-cards/響.md",
                      check_previous(previous))
        changed = copy.deepcopy(previous)
        changed["reviewAccepted"] = True
        with self.assertRaises(ValueError):
            check_previous(changed)
        before = {"a": b"complete record", "b": b"comparison"}
        expected = {name: sha(raw) for name, raw in before.items()}
        check_reuse(before, dict(before), expected)
        for after in ({"a": before["a"]}, {**before, "a": b"selected sense"}):
            with self.assertRaises(ValueError):
                check_reuse(before, after, expected)


if __name__ == "__main__":
    unittest.main()
