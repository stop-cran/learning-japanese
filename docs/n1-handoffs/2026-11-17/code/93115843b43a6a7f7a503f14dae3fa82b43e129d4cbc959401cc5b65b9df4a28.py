import copy
import json
import unittest

from verify_b132_gates import BASE, GUARD_SHA, ORDER, verify_reading_output, verify_summary


class B132GateEvidenceTests(unittest.TestCase):
    def fixture(self):
        memory = {"breach": None, "freeRamBeforeBytes": 2 * 1024**3 + 1,
                  "minimumObservedFreeRamBytes": 1024**3, "abortThresholdBytes": 1024**3,
                  "samplingIntervalSeconds": 0.25}
        admission = {"base": BASE, "head": "candidate", "mode": "committed", "memory": memory}
        summary = {"batch": 132, "base": BASE, "startingHead": "candidate", "mode": "committed",
                   "status": "PASS", "checks": list(ORDER), "serial": True, "manifestSha256": "manifest",
                   "runnerSha256": "runner", "commonHelperSha256": "common", "guardSha256": GUARD_SHA,
                   "waitTimeoutSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10, "finalMemory": memory}
        return admission, summary

    def test_summary_rejects_other_snapshot_reordered_gates_and_weaker_bounds(self):
        admission, summary = self.fixture()
        verify_summary(summary, admission, "committed", "candidate", "manifest", "runner", "common")
        for field, value in (("startingHead", BASE), ("checks", list(reversed(ORDER))),
                             ("manifestSha256", "other"), ("waitTimeoutSeconds", 10),
                             ("cleanupTimeoutSecondsPerStage", 20), ("serial", False)):
            altered = copy.deepcopy(summary)
            altered[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_summary(altered, admission, "committed", "candidate", "manifest", "runner", "common")
        changed = copy.deepcopy(admission)
        changed["memory"]["freeRamBeforeBytes"] = 2 * 1024**3
        with self.assertRaises(ValueError):
            verify_summary(summary, changed, "committed", "candidate", "manifest", "runner", "common")

    def test_reading_evidence_requires_explicit_keys_and_retains_latent_hits(self):
        keys = {"X": ["metadata", "supplemental"]}
        log = ("Explicit supplemental reading keys: " + json.dumps(keys)
               + "\n0 production hit(s)\n0 padded-session hit(s)\n3 latent collision(s)\n")
        self.assertEqual(verify_reading_output(log, keys), 3)
        for changed in (log.replace("supplemental", "omitted"),
                        log.replace("0 production", "1 production"),
                        log.replace("0 production", "10 production"),
                        log.replace("0 padded-session", "1 padded-session"),
                        log.replace("0 padded-session", "10 padded-session"),
                        log.replace("3 latent collision(s)", ""),
                        log + "3 latent collision(s)\n"):
            with self.subTest(log=changed), self.assertRaises(ValueError):
                verify_reading_output(changed, keys)


if __name__ == "__main__":
    unittest.main()
