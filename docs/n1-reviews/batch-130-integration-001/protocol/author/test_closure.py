import copy
import unittest
from closure_common import *


class ClosureTests(unittest.TestCase):
    def setUp(self):
        self.previous = json.loads(git("show", PARENT + ":" + LEDGER))

    def test_exact_extension_keeps_snapshot_accounting_and_limits(self):
        current = make_ledger(self.previous, "a" * 64, "b" * 64)
        self.assertEqual({key: current[key] for key in self.previous}, self.previous)
        self.assertEqual(current["activeReviewedSnapshot"], PARENT)
        self.assertEqual(current["integrationReview"]["runtimeCandidate"], RUNTIME)
        self.assertEqual(current["integrationReview"]["previousLimitsPreserved"], self.previous["limits"])
        self.assertFalse(current["integrationReview"]["currentControlMessageAdjudicationUsed"])

    def test_old_ledger_or_accounting_rewrite_is_rejected(self):
        for key, value in (("runtimeCandidate", RUNTIME), ("reviewedSnapshot", PARENT),
                           ("accounting", {}), ("limits", []), ("published", ["拍"])):
            with self.subTest(key=key):
                current = make_ledger(self.previous, "a" * 64, "b" * 64)
                current[key] = value
                with self.assertRaises(ValueError):
                    check_ledger(self.previous, current, "a" * 64, "b" * 64)

    def test_unscoped_blob_mode_or_new_path_is_rejected(self):
        before = {LEDGER: {"mode": "100644", "blob": "old"}, "kanji/拍.md": {"blob": "fixed"}}
        after = copy.deepcopy(before)
        after[LEDGER]["blob"] = "new"
        after[ARCHIVE + "/provenance.json"] = {"blob": "archive"}
        self.assertEqual(check_delta(before, after), {ARCHIVE + "/provenance.json"})
        for path, value in (("kanji/拍.md", {"blob": "changed"}), ("unscoped.txt", {"blob": "added"})):
            altered = {**after, path: value}
            with self.assertRaises(ValueError):
                check_delta(before, altered)
        after[LEDGER]["mode"] = "100755"
        with self.assertRaises(ValueError):
            check_delta(before, after)

    def test_old_snapshot_or_control_adjudication_cannot_be_relabelled(self):
        provenance = {
            "reviewedSnapshot": PARENT, "previousReviewedSnapshot": PREVIOUS, "parents": PARENTS,
            "runtimeCandidate": RUNTIME, "finalRuns": list(RUNS.values()),
            "reviewLineage": [
                {"family": family, "run": run, "session": family, "snapshot": PARENT,
                 "priorSnapshot": PREVIOUS, "rawVerdict": "CONFIRMED",
                 "rawAuditWasClean": True, "controlMessageAdjudicationApplied": False}
                for family, run in RUNS.items()],
        }
        validation = {"candidate": PARENT, "runtimeCandidate": RUNTIME, "reviewClosureSha256": "a" * 64}
        check_lineage(provenance, validation, "a" * 64)
        for field, value in (("snapshot", PREVIOUS), ("controlMessageAdjudicationApplied", True),
                             ("rawAuditWasClean", False)):
            changed = copy.deepcopy(provenance)
            changed["reviewLineage"][0][field] = value
            with self.assertRaises(ValueError):
                check_lineage(changed, validation, "a" * 64)
        with self.assertRaises(ValueError):
            check_lineage(provenance, validation, "b" * 64)


if __name__ == "__main__":
    guard = start_guard()
    try:
        result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ClosureTests))
    finally:
        write(HERE / "focused-test-memory-001.json", guard.finish())
    raise SystemExit(0 if result.wasSuccessful() else 1)
