import ast
import unittest
from pathlib import Path

import prepare_b129_initial_replacement_v2 as current
import test_prepare_b129_initial_replacement as prior
from common import TOOLS, frozen
from prepare_b129_initial_replacement import SOURCE_SHA, binding


class FirstConfirmationReplacementV2Tests(prior.FirstConfirmationReplacementTests):
    def test_initial_only_lineage_reproduces_actual_context_failure(self):
        self.check()
        bindings = current.verify_replacement(
            self.spec, self.config, self.initial, self.launch, self.records)
        self.assertIn(self.spec["unavailable"], bindings)
        self.assertIn(binding(Path(current.__file__)), bindings)
        self.assertNotIn("prior", self.spec)

    def test_derivation_leaves_nonbuilder_gates_identical(self):
        original = frozen(TOOLS / "confirm_b127.py", SOURCE_SHA).decode("utf-8")
        changed = current.derive_text(original)
        functions = lambda text: {node.name: ast.dump(node) for node in ast.parse(text).body
                                  if isinstance(node, ast.FunctionDef) and node.name != "build"}
        self.assertEqual(functions(original), functions(changed))
        compile(changed, "synthetic-replacement", "exec")
        with self.assertRaises(ValueError):
            current.derive_text(original.replace("Wrong original reviewer or freeze", "unknown wording"))

    def test_crlf_and_lf_produce_the_same_derivative(self):
        original = frozen(TOOLS / "confirm_b127.py", SOURCE_SHA).decode("utf-8")
        lf = original.replace("\r\n", "\n")
        self.assertEqual(current.derive_text(lf), current.derive_text(lf.replace("\n", "\r\n")))


if __name__ == "__main__":
    unittest.main()
