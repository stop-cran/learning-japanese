import copy
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from common import freeze_json, load_module

HERE = Path(__file__).parent
module = load_module("revision_input_v2", HERE / "assemble-b134-revision-input-v2.py")
old_tests = load_module("revision_input_v1_tests", HERE / "test-assemble-b134-revision-input.py")
old_tests.module = module


class LiteralDispositionTests(old_tests.RevisionInputTests):
    def test_actual_entry_rejects_held_acceptance_before_any_assembly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            request = root / "request.json"
            output = root / "must-not-exist"
            freeze_json(request, {
                "claude": {"path": "held", "sha256":
                           "18eb73b8484e457d748f7abe64b44ddfed47a25121ae6682320bc4eedf09057c"},
                "gpt": {"path": "not-read", "sha256": "0" * 64},
            })
            with patch.object(module, "ROOT", root), self.assertRaisesRegex(ValueError, "held pre-authorization"):
                module.main(request, output)
            self.assertFalse(output.exists())

    def test_claude_editorial_decline_preserves_both_original_and_new_evidence(self):
        values = old_tests.fixture("claude")
        values[5]["dispositions"]["F1"] = "DECLINE ACCEPTED"
        before = copy.deepcopy(values)
        result = module.confirmation_dispositions(*values)
        self.assertEqual(values, before)
        self.assertEqual(result[0]["status"], "withdrawn")
        self.assertEqual(result[0]["reason"], values[2]["decisions"][0]["reason"])
        with self.assertRaises(ValueError):
            module.prior.confirmation_dispositions(*values)

    def test_decline_exception_does_not_relax_other_obligations(self):
        for family, identity, token in (
            ("claude", "F1", "DECLINE REJECTED"), ("claude", "F1", "UNVERIFIED"),
            ("claude", "F1", "RESOLVED"), ("claude", "O1", "DISPUTE ACCEPTED"),
            ("gpt", "F1", "DECLINE ACCEPTED"), ("gpt", "F2", "DISPUTE ACCEPTED"),
            ("gpt", "C1", "DECLINE ACCEPTED"),
        ):
            with self.subTest(family=family, identity=identity, token=token):
                values = old_tests.fixture(family)
                values[5]["dispositions"][identity] = token
                with self.assertRaises(ValueError):
                    module.confirmation_dispositions(*values)


if __name__ == "__main__":
    unittest.main()
