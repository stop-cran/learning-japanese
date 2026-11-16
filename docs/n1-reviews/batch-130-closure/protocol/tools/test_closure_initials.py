import unittest

from closure_initials import require_structure_hold


class ExcludedInitialTests(unittest.TestCase):
    def fixture(self):
        ref = {"path": "artifact", "sha256": "a" * 64}
        mechanics = {"status": "HOLD", "run": "N1-B118-CLAUDE-001",
                     "session": "reviewer", "candidate": "b" * 40,
                     "structure": ref, "context": ref, "finalAudit": ref}
        held = {**mechanics, "status": "HOLD_STRUCTURE_FAILED", "batch": 118,
                "rawVerdict": "NEEDS FIX", "reviewAccepted": False}
        return held, mechanics, {"status": "FAIL", "errors": ["facet mismatch"],
                                "overall": "NEEDS FIX"}, {
            "status": "PASS", "compactions": []}

    def test_structure_hold_is_preserved_not_accepted(self):
        require_structure_hold(*self.fixture(), 118, "b" * 40)

    def test_changed_identity_or_success_cannot_be_quarantined_as_structure_hold(self):
        for field, value in (("reviewAccepted", True), ("batch", 117), ("candidate", "c" * 40),
                             ("run", "different"), ("session", "different"),
                             ("status", "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"),
                             ("structure", {"path": "other", "sha256": "a" * 64})):
            held, mechanics, structure, context = self.fixture()
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_structure_hold({**held, field: value}, mechanics, structure, context, 118, "b" * 40)

    def test_failed_context_is_not_mislabeled_structure_only(self):
        held, mechanics, structure, context = self.fixture()
        with self.assertRaises(ValueError):
            require_structure_hold(held, mechanics, structure,
                                   {**context, "status": "FAIL", "compactions": [1]}, 118, "b" * 40)


if __name__ == "__main__":
    unittest.main()
