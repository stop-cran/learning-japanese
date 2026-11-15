import copy
import unittest

from finalize_b120 import CARD, CANDIDATE, INITIAL, STROKES, WORD, verify_closure, verify_runtime


class ClosureTests(unittest.TestCase):
    def setUp(self):
        self.proof = {
            "reviewedSnapshot": CANDIDATE, "initialSnapshot": INITIAL, "publication": "PENDING",
            "excludedInitialRuns": [], "intermediateRuns": [], "reviewLineage": []
        }
        for family in ("claude", "gpt"):
            self.proof["reviewLineage"].extend([
                {"family": family, "role": "initial", "rawVerdict": "UNVERIFIED",
                 "snapshot": INITIAL, "finalAcceptance": False},
                {"family": family, "role": "final", "rawVerdict": "CONFIRMED",
                 "snapshot": CANDIDATE, "finalAcceptance": True,
                 "confirmationAcceptedOnSnapshot": True, "priorRun": None}
            ])

    def test_accepts_preserved_initials_and_exact_final_snapshot(self):
        verify_closure(self.proof)

    def test_rejects_unclosed_or_wrong_snapshot(self):
        for field, value in (("rawVerdict", "UNVERIFIED"), ("snapshot", INITIAL),
                             ("confirmationAcceptedOnSnapshot", False), ("family", "claude")):
            with self.subTest(field=field):
                proof = copy.deepcopy(self.proof)
                proof["reviewLineage"][3][field] = value
                with self.assertRaises(ValueError):
                    verify_closure(proof)

    def test_does_not_rebrand_the_initial(self):
        self.proof["reviewLineage"][0]["rawVerdict"] = "CLEAN"
        with self.assertRaises(ValueError):
            verify_closure(self.proof)

    def test_baseline_deletion_and_unrelated_change_fail(self):
        old = {f"words/base-{i}.md": "unchanged" for i in range(8699)}
        old[WORD] = "before"
        new = {**old, WORD: "wrapper", CARD: "card", STROKES: "strokes"}
        self.assertEqual(len(verify_runtime({"md": old}, {"md": new})), 8702)
        for changed in ({**new, "words/base-0.md": "changed"},
                        {key: value for key, value in new.items() if key != "words/base-0.md"}):
            with self.assertRaises(ValueError):
                verify_runtime({"md": old}, {"md": changed})


if __name__ == "__main__":
    unittest.main()
