import json
import unittest
from unittest.mock import patch

from b130_context_confirmation import ROOT, PARENT, REVIEWERS, check_lineage, derive_text, replacement_prompt
from common import TOOLS
from prepare_b130_fresh_admission import derive_text as derive_admission
import test_scoped_confirmation_admission as original_tests


def admission_namespace():
    source = (TOOLS / "scoped_confirmation_admission.py").read_text(encoding="utf-8")
    namespace = {"__name__": "fresh_admission_test"}
    exec(compile(derive_admission(source), "fresh_admission_test", "exec"), namespace)
    return namespace


class FreshContextConfirmationTests(unittest.TestCase):
    def test_existing_prompt_keeps_access_contract_without_false_authorship(self):
        text = (ROOT / "confirm" / "N1-B130-CLAUDE-CONFIRM-001-prompt.txt").read_text(encoding="utf-8")
        result = replacement_prompt(text)
        self.assertNotIn("your own", result)
        self.assertIn("never admitted or executed", result)
        self.assertIn("Original reviewer's initial report:", result)
        self.assertEqual(text[text.index("ACCESS RULES"):text.index("TASKS")],
                         result[result.index("ACCESS RULES"):result.index("TASKS")])

    def test_actual_prepared_lineage_rejects_changed_sources_or_impersonation(self):
        source = json.loads((ROOT / "confirm" / "N1-B130-CLAUDE-CONFIRM-001-spec.json").read_bytes())
        observation = json.loads((ROOT / "confirmation-capacity-observation-001.json").read_bytes())
        accepted = json.loads((ROOT / "N1-B130-CLAUDE-004-acceptance.json").read_bytes())
        launch = json.loads((ROOT / "N1-B130-CLAUDE-004-launch.json").read_bytes())
        spec = {**source, "run": "N1-B130-CLAUDE-CONFIRM-002", "session": "fresh-test-session",
                "originalSession": REVIEWERS["claude"], "replayedFrom": {"test": "old"},
                "contextObservation": {"test": "observation"}}
        config = {"batch": 130, "candidate": PARENT}
        check_lineage(spec, source, config, accepted, launch, observation)
        for field, value in (("session", source["session"]), ("revisedSources", []),
                             ("candidate", "0" * 40), ("originalSession", "different")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                check_lineage({**spec, field: value}, source, config, accepted, launch, observation)

    def test_derivation_preserves_nonbuilder_functions(self):
        source = (ROOT.parent.parent / "review-tools" / "confirm_b130_compact.py").read_text(encoding="utf-8")
        derived = derive_text(source)
        compile(derived, "test-derivation", "exec")
        self.assertIn("pre-admission-context-capacity", derived)

    def test_fresh_admission_rejects_missing_or_impersonated_origin(self):
        namespace = admission_namespace()
        for record in ({}, {"replacementReason": "pre-admission-context-capacity",
                            "session": "same", "originalSession": "same",
                            "replayedFrom": {"present": True}, "contextObservation": {"present": True}}):
            namespace["preflight"] = lambda _: (record, {})
            with self.subTest(record=record), self.assertRaises(ValueError):
                namespace["admit"](None, None)


class FreshAdmissionTests(original_tests.ConfirmationAdmissionTests):
    def setUp(self):
        self.assess = admission_namespace()["assess_confirmation_status"]
        replacement = patch.object(original_tests, "assess_confirmation_status", self.assess)
        replacement.start()
        self.addCleanup(replacement.stop)

    def test_original_reviewer_is_reused_while_unrelated_android_runs(self):
        status = self.status(original_tests.session(
            "android", "busy", project_repo="stop-cran/kanji-cards-android"))
        result = self.assess(status, "reviewer", original_tests.FLOOR + 1)
        self.assertTrue(result["statusAllowsAdmission"])
        self.assertTrue(result["reviewerSessionNameUnique"])
        self.assertNotIn("originalReviewer", result)
        self.assertEqual([row["id"] for row in result["unrelatedActiveSessions"]], ["android"])


if __name__ == "__main__":
    unittest.main()
