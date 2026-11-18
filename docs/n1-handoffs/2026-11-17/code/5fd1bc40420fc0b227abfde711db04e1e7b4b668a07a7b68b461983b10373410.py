"""Bind the observed B132 support schema without changing preservation checks."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-132" / "review"
frozen(TOOLS / "prepare_b131_source_verifier.py",
       "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5")
from prepare_b131_source_verifier import derive

SUPPORT_FUNCTION = '''
def verify_support_inventory(declaring, selection):
    require(declaring == SUPPORTS, "Complete declared-support inventory differs")
    pairs = [[char, word] for char in MEMBERS for word in SUPPORTS[char]]
    require(selection["supports"] == pairs and selection["proseException"] is None,
            "Reciprocal pair inventory or prose-exception scope differs")
    return pairs

'''

SUPPORT_TESTS = '''
class SupportInventoryTests(unittest.TestCase):
    def test_exact_declared_support_and_reciprocal_pair_are_required(self):
        support = {"\\u5893": ["\\u5893"]}
        selection = {"supports": [["\\u5893", "\\u5893"]], "proseException": None}
        self.assertEqual(selection["supports"], verify_support_inventory(support, selection))
        for declared in ({}, {"\\u5893": []}, {"\\u5893": ["\\u5893", "extra"]},
                         {"\\u5893": ["\\u5893"], "other": ["other"]}):
            with self.subTest(declared=declared), self.assertRaises(ValueError):
                verify_support_inventory(declared, selection)

    def test_pair_omission_duplication_and_unapproved_prose_changes_fail(self):
        support = {"\\u5893": ["\\u5893"]}
        for pairs, exception in (
            ([], None), ([["\\u5893", "extra"]], None),
            ([["\\u5893", "\\u5893"], ["\\u5893", "\\u5893"]], None),
            ([["\\u5893", "\\u5893"]], "unexpected prose change"),
        ):
            with self.subTest(pairs=pairs, exception=exception), self.assertRaises(ValueError):
                verify_support_inventory(support, {"supports": pairs, "proseException": exception})

'''


def main():
    record = HERE / "payload-verifier-derivation-002.json"
    outputs = ("verify_b132_payload_v2.py", "test_verify_b132_payload_v2.py")
    require(not record.exists() and all(not (TOOLS / name).exists() for name in outputs),
            "Preserve existing derivation outputs")
    guard, _ = start_guard("B132 observed support schema")
    try:
        verifier = derive(
            "verify_b132_payload.py",
            "e1adf7af0f426a965c2bbb614a1c5c9aadc0428431b6fe11d83d1019e35a86e0",
            outputs[0], [
                ('def main(proof_path, expected_sha, output):',
                 SUPPORT_FUNCTION + '\ndef main(proof_path, expected_sha, output):'),
                ('        require(declaring == SUPPORTS == selection["allDeclaredSupportArticles"],\n'
                 '                "Complete declared-support inventory differs")\n'
                 '        pairs = [[char, word] for char in MEMBERS for word in SUPPORTS[char]]\n'
                 '        require(selection["requiredReciprocalPairs"] == pairs, "Reciprocal pair inventory differs")',
                 '        verify_support_inventory(declaring, selection)'),
                ("verify_b132_payload.py", "verify_b132_payload_v2.py"),
            ])
        tests = derive(
            "test_verify_b132_payload.py",
            "214c8f2b5ee67da5c7a87ba4da2d11184135c75f3b2e2ba7f50b94c9a908bc2e",
            outputs[1], [
                ("from verify_b132_payload import runtime_entries, verify_metadata, verify_runtime_delta",
                 "from verify_b132_payload_v2 import (\n"
                 "    runtime_entries, verify_metadata, verify_runtime_delta, verify_support_inventory)")
            ])
        tests_path = TOOLS / "test_b132_support_inventory.py"
        require(not tests_path.exists(), "Preserve support-schema tests")
        from common import write_frozen
        test_source = ("import unittest\nfrom verify_b132_payload_v2 import verify_support_inventory\n"
                       + SUPPORT_TESTS + '\nif __name__ == "__main__":\n    unittest.main()\n')
        compile(test_source, str(tests_path), "exec")
        support_tests = write_frozen(tests_path, test_source.encode("utf-8"))
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(record, {
        "batch": 132, "status": "PREPARATION_ONLY", "verifier": verifier,
        "retainedTests": tests, "supportSchemaTests": support_tests,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "memory": memory,
        "reason": "The inspected B132 producer writes supports as reciprocal pairs and "
                  "proseException as null, not B131's two named support inventories.",
        "invariant": "Every runtime word declaration must still equal the exact selected support "
                     "inventory. Its reciprocal pairs must match exactly, with no prose exception. "
                     "All original runtime, signature, metadata, wrapper and geometry checks remain.",
        "limits": "Candidate-independent preparation. The original verifier and derivation remain "
                  "unchanged. No candidate, source, gate, semantic or publication acceptance.",
    })))


if __name__ == "__main__":
    main()
