import copy
import json
import unittest

from b130_context_confirmation import ROOT, binding
from b130_followup_lineage import PRIOR_SHA, require_followup_identity
from common import TOOLS, frozen, load_batch
from prepare_b130_followup_engine import derive_admission, derive_engine


class FollowupTests(unittest.TestCase):
    def fixture(self, family):
        run = f"N1-B130-{family.upper()}-CONFIRM-002"
        origin_path = ROOT / "confirm" / f"{run}-spec.json"
        origin = json.loads(frozen(origin_path))
        initial = json.loads(frozen(origin["acceptance"]["path"], origin["acceptance"]["sha256"]))
        launch = json.loads(frozen(ROOT / f"{initial['run']}-launch.json"))
        spec = {
            "batch": 130, "run": run[:-3] + "003", "family": family,
            "session": origin["session"], "originalSession": origin["originalSession"],
            "candidate": "1" * 40, "acceptance": origin["acceptance"],
            "reviewerOrigin": binding(origin_path),
            "prior": {"path": str(ROOT / "confirm" / f"{run}-acceptance.json"),
                      "sha256": PRIOR_SHA[family]},
            "basis": "accepted-confirmation" if family == "claude" else "held-confirmation",
            "priorVerdict": "CONFIRMED" if family == "claude" else "UNVERIFIED",
            "openClaimIds": [] if family == "claude" else ["D18"],
        }
        return spec, initial, launch

    def test_actual_confirmed_and_unverified_history_is_usable_without_relabelling(self):
        for family in PRIOR_SHA:
            spec, initial, launch = self.fixture(family)
            before = copy.deepcopy(spec)
            origin = require_followup_identity(spec, initial, launch, ROOT)
            self.assertEqual(spec, before)
            self.assertNotEqual(origin["session"], launch["session"])

    def test_changed_reviewer_erased_hold_or_skipped_prior_is_rejected(self):
        spec, initial, launch = self.fixture("gpt")
        for field, value in (("session", launch["session"]), ("openClaimIds", []),
                             ("basis", "accepted-confirmation"), ("run", "N1-B130-GPT-CONFIRM-004"),
                             ("prior", {"path": "wrong", "sha256": PRIOR_SHA["gpt"]})):
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_followup_identity({**spec, field: value}, initial, launch, ROOT)

    def test_derived_engines_retain_shared_state_and_audit_checks(self):
        engine = derive_engine(frozen(TOOLS / "confirm_followup.py").decode("utf-8"))
        admission = derive_admission(frozen(TOOLS / "b130_fresh_confirmation_admission.py").decode("utf-8"))
        compile(engine, "confirm_b130_followup.py", "exec")
        compile(admission, "b130_followup_admission.py", "exec")
        import ast
        functions = lambda text: {node.name: ast.dump(node) for node in ast.parse(text).body
                                  if isinstance(node, ast.FunctionDef)}
        original = functions(frozen(TOOLS / "confirm_followup.py").decode("utf-8"))
        actual = functions(engine)
        for name in ("require_prior_state", "verify_prior", "render_followup_prompt"):
            self.assertEqual(actual[name], original[name])
        self.assertIn("from confirm_b130_fresh_context import binding, clean, final, revision_diff", engine)
        self.assertIn("require_followup_preflight(record, config)", admission)


if __name__ == "__main__":
    unittest.main()
