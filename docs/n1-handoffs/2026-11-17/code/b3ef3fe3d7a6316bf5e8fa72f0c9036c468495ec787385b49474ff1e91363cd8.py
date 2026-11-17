import unittest
from unittest.mock import patch

from replacement_lineage import require_followup_identity, verify_origin


class ContinuingReplacementTests(unittest.TestCase):
    def test_original_identity_is_unchanged(self):
        self.assertIsNone(require_followup_identity({"session": "original"}, {}, {"session": "original"}, None))
        with self.assertRaises(ValueError):
            require_followup_identity({"session": "other"}, {}, {"session": "original"}, None)
        with self.assertRaises(ValueError):
            require_followup_identity({"session": "original", "reviewerOrigin": {}},
                                      {}, {"session": "original"}, None)

    def test_followup_requires_verified_origin(self):
        spec = {"session": "replacement", "reviewerOrigin": {"path": "origin", "sha256": "hash"}}
        with patch("replacement_lineage.verify_origin", return_value={"run": "origin"}) as verify:
            self.assertEqual(require_followup_identity(spec, {}, {"session": "original"}, "records"),
                             {"run": "origin"})
            verify.assert_called_once_with(spec, {}, {"session": "original"}, "records")

    def test_unrelated_origin_is_rejected_before_any_acceptance(self):
        spec = {"session": "replacement", "family": "claude", "batch": 117,
                "acceptance": {"sha256": "initial"}, "reviewerOrigin": {}}
        origin = {"session": "replacement", "originalSession": "original",
                  "family": "claude", "batch": 117, "acceptance": spec["acceptance"]}
        for changed in ({"session": "other"}, {"originalSession": "other"},
                        {"family": "gpt"}, {"batch": 118}, {"acceptance": {"sha256": "other"}}):
            with self.subTest(changed=changed), patch("replacement_lineage.read", return_value={**origin, **changed}):
                with self.assertRaises(ValueError):
                    verify_origin(spec, {}, {"session": "original"}, None)


if __name__ == "__main__":
    unittest.main()
