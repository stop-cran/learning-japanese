import unittest
from unittest.mock import Mock

from common import frozen
from prepare_b125_evidence_followup import SOURCE, SOURCE_SHA, derive


class EvidenceOnlyFollowupTests(unittest.TestCase):
    def setUp(self):
        self.namespace = {"__name__": "fixture"}
        exec(compile(derive(frozen(SOURCE, SOURCE_SHA)), "derived-followup", "exec"), self.namespace)
        self.git = self.namespace["git"] = Mock()
        self.original = self.namespace["revision_diff"] = Mock(return_value=(b"real patch\n", ["docs/a"]))
        self.select = self.namespace["selected_revision_diff"]
        self.config = {"candidate": "a" * 40}
        self.candidate = "b" * 40

    def test_runtime_path_remains_the_existing_strict_path(self):
        self.assertEqual(self.select(self.config, self.candidate, {}), (b"real patch\n", ["docs/a"]))
        self.original.assert_called_once_with(self.config, self.candidate)
        self.git.assert_not_called()

    def test_docs_only_requires_explicit_opt_in_and_returns_honest_note(self):
        self.git.side_effect = [b"docs/new-evidence.json\0docs/response.md\0", b""]
        note, omitted = self.select(self.config, self.candidate, {"evidenceOnly": True})
        self.assertEqual(omitted, ["docs/new-evidence.json", "docs/response.md"])
        self.assertIn(b"no runtime patch", note)
        self.assertIn(b"All runtime and manifest bytes are unchanged", note)
        self.assertNotIn(b"response.md", note)
        self.original.assert_not_called()
        self.assertEqual(self.git.call_args.args[-2:], (".", ":(exclude)docs"))

    def test_non_boolean_opt_in_is_rejected(self):
        for value in ("true", 1, None):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "explicit boolean"):
                self.select(self.config, self.candidate, {"evidenceOnly": value})

    def test_empty_or_runtime_or_manifest_delta_is_rejected(self):
        for names in (b"", b"manifest.json\0docs/a\0", b"kanji/card.md\0", b"tools/app.py\0"):
            self.git.side_effect = [names, b""]
            with self.subTest(names=names), self.assertRaisesRegex(ValueError, "documentation-only"):
                self.select(self.config, self.candidate, {"evidenceOnly": True})

    def test_second_git_check_cannot_hide_runtime_bytes(self):
        self.git.side_effect = [b"docs/a\0", b"unexpected runtime diff"]
        with self.assertRaisesRegex(ValueError, "runtime or manifest"):
            self.select(self.config, self.candidate, {"evidenceOnly": True})

    def test_prior_accepted_and_held_states_remain_distinct(self):
        require_prior = self.namespace["require_prior_state"]
        accepted = {"reviewEvidenceAccepted": True, "confirmationAccepted": True,
                    "verdict": "CONFIRMED", "openClaimIds": [], "acceptedNewFindings": []}
        require_prior({"basis": "accepted-confirmation", "priorVerdict": "CONFIRMED",
                       "openClaimIds": []}, accepted, [])
        held = {**accepted, "confirmationAccepted": False, "verdict": "UNVERIFIED",
                "openClaimIds": ["S1"]}
        require_prior({"basis": "held-confirmation", "priorVerdict": "UNVERIFIED",
                       "openClaimIds": ["S1"]}, held, [])
        with self.assertRaises(ValueError):
            require_prior({"basis": "accepted-confirmation", "priorVerdict": "CONFIRMED",
                           "openClaimIds": []}, held, [])


if __name__ == "__main__":
    unittest.main()
