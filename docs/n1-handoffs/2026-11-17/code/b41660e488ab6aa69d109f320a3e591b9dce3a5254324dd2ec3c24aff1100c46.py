import unittest

from close_b124 import require_confirmation, require_intermediate


class ClosureAcceptanceTests(unittest.TestCase):
    def test_held_or_different_revision_cannot_close(self):
        candidate = "a" * 40
        accepted = {"candidate": candidate, "confirmationAccepted": True,
                    "verdict": "CONFIRMED", "openClaimIds": []}
        require_confirmation(accepted, candidate)
        for field, value in (("candidate", "b" * 40), ("confirmationAccepted", False),
                             ("verdict", "NEEDS FIX"), ("openClaimIds", ["unsettled-pair"])):
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_confirmation({**accepted, field: value}, candidate)

    def test_intermediate_is_unaccepted_evidence_on_an_earlier_revision(self):
        candidate = "a" * 40
        accepted = {"candidate": "b" * 40, "reviewEvidenceAccepted": True, "confirmationAccepted": False,
                    "verdict": "NEEDS FIX", "openClaimIds": ["F1"]}
        require_intermediate(accepted, candidate)
        for field, value in (("candidate", candidate), ("confirmationAccepted", True),
                             ("reviewEvidenceAccepted", False), ("openClaimIds", []),
                             ("verdict", "PASS")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                require_intermediate({**accepted, field: value}, candidate)



class BatchScopeTests(unittest.TestCase):
    def test_other_batch_is_refused_before_any_archive_write(self):
        from close_b124 import archive
        with self.assertRaisesRegex(ValueError, "limited to B124"):
            archive(123, "a" * 40, [], preflight_path=None)


if __name__ == "__main__":
    unittest.main()
