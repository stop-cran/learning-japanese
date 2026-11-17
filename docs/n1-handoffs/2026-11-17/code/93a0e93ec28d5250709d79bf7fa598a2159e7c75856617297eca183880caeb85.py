import copy
import unittest

from common import CHECKS, GUARD_SHA, sha
from verify_b123_revision import check_gate, check_summary


class B123RevisionBindings(unittest.TestCase):
    def test_summary_binds_observed_head_runner_and_exact_gate_set(self):
        config = {"base": "base", "candidate": "initial"}
        summary = {
            "batch": "123", "status": "PASS", "mode": "committed", "base": "base",
            "startingHead": "revision", "checks": list(CHECKS),
            "manifestSha256": "manifest", "runnerSha256": "runner",
        }
        check_summary(summary, config, "revision", "manifest", "runner")
        for key, value in (
            ("batch", "122"), ("startingHead", "initial"), ("runnerSha256", "other"),
            ("mode", "author"), ("base", "other"), ("status", "FAIL"),
            ("manifestSha256", "other"), ("checks", list(CHECKS)[:-1]),
            ("checks", [*CHECKS, CHECKS[0]]), ("parent", "other"),
            ("manifestReproducible", False),
        ):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                check_summary({**summary, key: value}, config, "revision", "manifest", "runner")
        unobserved = {**summary, "head": summary["startingHead"]}
        del unobserved["startingHead"]
        with self.assertRaises(KeyError):
            check_summary(unobserved, config, "revision", "manifest", "runner")

    def receipt(self, log):
        return {
            "gate": "manifest-rebuild", "exitCode": 0, "childExitCodeAfterCleanup": 0,
            "cwd": "repo", "logSha256": sha(log), "logBytes": len(log),
            "manifestSha256": "manifest", "manifestReproducible": True,
            "runnerSha256": "runner", "guardSha256": GUARD_SHA, "waitTimeoutSeconds": 0.1,
            "memory": {
                "breach": None, "freeRamBeforeBytes": 3 * 1024**3,
                "minimumObservedFreeRamBytes": 1024**3,
                "abortThresholdBytes": 1024**3, "samplingIntervalSeconds": 0.25,
            },
        }

    def test_rebuild_receipt_and_bounded_live_child_are_not_optional(self):
        log = b"manifest rebuilt"
        receipt = self.receipt(log)
        check_gate(receipt, log, "manifest-rebuild", "manifest", "repo", "runner")
        for key, value in (
            ("childExitCodeAfterCleanup", None), ("childExitCodeAfterCleanup", 1),
            ("waitTimeoutSeconds", 0), ("waitTimeoutSeconds", 0.2),
            ("runnerSha256", "other"), ("guardSha256", "other"),
            ("logBytes", len(log) + 1), ("manifestReproducible", False),
        ):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_gate({**receipt, key: value}, log, "manifest-rebuild",
                           "manifest", "repo", "runner")
        for key, value in (
            ("freeRamBeforeBytes", 2 * 1024**3),
            ("minimumObservedFreeRamBytes", 1024**3 - 1),
        ):
            changed = copy.deepcopy(receipt)
            changed["memory"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_gate(changed, log, "manifest-rebuild", "manifest", "repo", "runner")

    def test_reading_evidence_covers_the_target_and_source_only_readings(self):
        values = ["\u7bc4", "\u30cf\u30f3", "\u306e\u308a", "\u3059\u3059\u3080"]
        log = " ".join(values).encode("utf-8")
        receipt = {**self.receipt(log), "gate": "reading-exposure"}
        check_gate(receipt, log, "reading-exposure", "manifest", "repo", "runner")
        for omitted in values:
            altered = " ".join(v for v in values if v != omitted).encode("utf-8")
            changed = {**self.receipt(altered), "gate": "reading-exposure"}
            with self.subTest(omitted=omitted), self.assertRaises(ValueError):
                check_gate(changed, altered, "reading-exposure", "manifest", "repo", "runner")


if __name__ == "__main__":
    unittest.main()
