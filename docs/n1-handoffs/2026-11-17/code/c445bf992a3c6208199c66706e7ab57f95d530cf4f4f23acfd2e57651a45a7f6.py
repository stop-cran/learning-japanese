import ast
import copy
import unittest

from common import TOOLS, frozen, load_batch, load_module, review_dir
from prepare_b129_initial_replacement import (
    FAILED_RUN, SOURCE_SHA, binding, check_lineage, derive_text, read, replacement_prompt,
    verify_replacement,
)


class FirstConfirmationReplacementTests(unittest.TestCase):
    def setUp(self):
        self.records = review_dir(129)
        out = self.records / "confirm"
        self.source = read(binding(out / f"{FAILED_RUN}-spec.json"))
        self.spec = {**self.source, "run": "N1-B129-CLAUDE-REPLACEMENT-CONFIRM-004",
                     "session": "synthetic-fresh-session-not-launched",
                     "originalSession": self.source["session"],
                     "replayedFrom": binding(out / f"{FAILED_RUN}-spec.json"),
                     "unavailable": binding(out / f"{FAILED_RUN}-superseded.json")}
        self.config = load_batch(129)
        self.initial = read(self.source["acceptance"])
        self.launch = read(binding(self.records / f"{self.initial['run']}-launch.json"))
        self.failure = read(self.spec["unavailable"])
        self.audit, self.context = read(self.failure["audit"]), read(self.failure["context"])

    def check(self, **changes):
        values = {key: copy.deepcopy(getattr(self, key)) for key in
                  ("spec", "source", "config", "initial", "launch", "failure", "audit", "context")}
        for key, patch in changes.items():
            values[key].update(patch)
        check_lineage(**values)

    def test_initial_only_lineage_reproduces_actual_context_failure(self):
        self.check()
        bindings = verify_replacement(self.spec, self.config, self.initial, self.launch, self.records)
        self.assertIn(self.spec["unavailable"], bindings)
        self.assertNotIn("prior", self.spec)

    def test_rejects_reuse_misattribution_or_changed_snapshot(self):
        for patch in ({"session": self.source["session"]}, {"originalSession": "different"},
                      {"family": "gpt"}, {"candidate": "0" * 40}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                self.check(spec=patch)

    def test_rejects_changed_source_selection_or_invented_prior(self):
        for patch in ({"additionalSources": []}, {"revisedSources": []},
                      {"prior": {"confirmationAccepted": True}}):
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                self.check(spec=patch)

    def test_rejects_unaccepted_initial_or_laundered_failure(self):
        cases = ({"initial": {"reviewAccepted": False}},
                 {"failure": {"status": "UNLAUNCHED_CONTEXT_COMPACTION"}},
                 {"failure": {"reviewEvidenceAccepted": True}},
                 {"failure": {"confirmationAccepted": True}},
                 {"failure": {"reportWritten": True}},
                 {"failure": {"linguisticVerdict": "CONFIRMED"}},
                 {"audit": {"reviewerIdle": False}},
                 {"audit": {"writes": 1}},
                 {"audit": {"eventsSha256": "wrong"}},
                 {"context": {"status": "PASS"}},
                 {"context": {"compactions": []}})
        for patch in cases:
            with self.subTest(patch=patch), self.assertRaises(ValueError):
                self.check(**patch)

    def test_replacement_does_not_change_access_or_report_contracts(self):
        renderer = load_module("b129_first_replacement_test", self.records / "confirm" / "renderer.py")
        original = renderer.render_prompt(
            {"run": "synthetic", "scope": ["card"], "dispositionIds": ["F1"]},
            {"candidate": "signed", "freeze": "base", "originalReport": "original", "report": "output"},
            {"segments": [{"path": "segment"}]}, "prompt")
        changed = replacement_prompt(original)
        self.assertNotIn("your own", changed)
        self.assertIn("no accepted earlier confirmation", changed)
        self.assertEqual(original[original.index("ACCESS RULES"):original.index("TASKS")],
                         changed[changed.index("ACCESS RULES"):changed.index("TASKS")])
        self.assertEqual(original[original.index("REPORT CONTRACT"):],
                         changed[changed.index("REPORT CONTRACT"):changed.index("\nREPLACEMENT IDENTITY")])

    def test_derivation_leaves_nonbuilder_gates_identical(self):
        original = frozen(TOOLS / "confirm_b127.py", SOURCE_SHA).decode("utf-8")
        changed = derive_text(original)
        functions = lambda text: {node.name: ast.dump(node) for node in ast.parse(text).body
                                  if isinstance(node, ast.FunctionDef) and node.name != "build"}
        self.assertEqual(functions(original), functions(changed))
        compile(changed, "synthetic-replacement", "exec")
        with self.assertRaises(ValueError):
            derive_text(original.replace("Wrong original reviewer or freeze", "unknown wording"))


if __name__ == "__main__":
    unittest.main()
