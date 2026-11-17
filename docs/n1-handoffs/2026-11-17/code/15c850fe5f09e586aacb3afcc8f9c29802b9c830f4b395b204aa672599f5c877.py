import copy
import json
import sys
import unittest

from verify_b133_gates import (
    BASE, GUARD_SHA, ORDER, commands, verify_execution, verify_launcher,
    verify_reading_output, verify_runtime_maps, verify_summary)


class B133GateEvidenceTests(unittest.TestCase):
    def memory(self):
        return {"breach": None, "freeRamBeforeBytes": 2 * 1024**3 + 1,
                "minimumObservedFreeRamBytes": 1024**3, "abortThresholdBytes": 1024**3,
                "samplingIntervalSeconds": 0.25}

    def test_summary_binds_snapshot_launcher_order_and_bounds(self):
        admission = {"base": BASE, "head": "candidate", "mode": "committed", "memory": self.memory()}
        summary = {"batch": 133, "base": BASE, "startingHead": "candidate", "mode": "committed",
                   "status": "PASS", "checks": list(ORDER), "serial": True, "manifestSha256": "manifest",
                   "runnerSha256": "runner", "commonHelperSha256": "common",
                   "boundedLauncherSha256": "launcher", "guardSha256": GUARD_SHA,
                   "waitTimeoutSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10,
                   "finalMemory": self.memory()}
        args = ("committed", "candidate", "manifest", "runner", "common", "launcher")
        verify_summary(summary, admission, *args)
        for field, value in (("startingHead", BASE), ("checks", list(reversed(ORDER))),
                             ("manifestSha256", "other"), ("boundedLauncherSha256", "other"),
                             ("waitTimeoutSeconds", 10), ("cleanupTimeoutSecondsPerStage", 20),
                             ("serial", False)):
            changed = copy.deepcopy(summary)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_summary(changed, admission, *args)
        admission["memory"]["freeRamBeforeBytes"] = 2 * 1024**3
        with self.assertRaises(ValueError):
            verify_summary(summary, admission, *args)

    def test_execution_requires_exact_bounded_commands_and_serial_intervals(self):
        expected = commands()
        receipts = {
            name: {"startedAt": f"2026-11-17T00:00:{i * 2:02d}+00:00",
                   "completedAt": f"2026-11-17T00:00:{i * 2 + 1:02d}+00:00",
                   "command": [sys.executable, "-B", *map(str, expected[name])],
                   "commonHelperSha256": "common", "cleanupTimeoutSecondsPerStage": 10,
                   "activeError": None, "cleanupError": None}
            for i, name in enumerate(ORDER)
        }
        verify_execution(receipts, expected, "common")
        for field, value in (("command", receipts["quiz-safety"]["command"][:2]
                             + receipts["quiz-safety"]["command"][3:]),
                             ("startedAt", receipts["lint"]["startedAt"]),
                             ("cleanupError", "failed")):
            changed = copy.deepcopy(receipts)
            changed["quiz-safety"][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_execution(changed, expected, "common")

    def test_inner_launcher_memory_and_binding_are_required(self):
        receipts = {name: {"boundedLauncherSha256": "launcher"} for name in ORDER}
        line = "B133 bounded launcher memory: " + json.dumps(self.memory()) + "\n"
        logs = {name: line for name in ORDER}
        verify_launcher(receipts, logs, "launcher")
        bad_memory = self.memory()
        bad_memory["breach"] = "threshold"
        for value in ("", line + line, "B133 bounded launcher memory: " + json.dumps(bad_memory)):
            changed = dict(logs, lint=value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                verify_launcher(receipts, changed, "launcher")
        receipts["lint"]["boundedLauncherSha256"] = "other"
        with self.assertRaises(ValueError):
            verify_launcher(receipts, logs, "launcher")

    def test_reading_evidence_rejects_nonzero_or_missing_hits(self):
        keys = {"X": ["metadata", "supplemental"]}
        log = ("Explicit supplemental reading keys: " + json.dumps(keys)
               + "\n0 production hit(s)\n0 padded-session hit(s)\n1 latent collision(s)\n")
        self.assertEqual(verify_reading_output(log, keys), 1)
        for changed in (log.replace("supplemental", "omitted"),
                        log.replace("0 production", "10 production"),
                        log.replace("0 padded-session", "10 padded-session"),
                        log.replace("1 latent collision(s)", "")):
            with self.subTest(log=changed), self.assertRaises(ValueError):
                verify_reading_output(changed, keys)

    def test_files_only_map_cannot_stand_in_for_complete_runtime(self):
        manifest = {"files": {"kanji/A.md": "a"}, "audio": {"audio/A.mp3": "b"},
                    "scenes": {"scenes/A.json": "c"}, "contentVersion": "version"}
        full = {"kanji/A.md": "a", "audio/A.mp3": "b", "scenes/A.json": "c"}
        self.assertEqual(verify_runtime_maps(manifest, manifest["files"], full), full)
        for changed in (manifest["files"], {**full, "audio/A.mp3": "wrong"},
                        {**full, "unlisted": "d"}):
            with self.subTest(full=changed), self.assertRaises(ValueError):
                verify_runtime_maps(manifest, manifest["files"], changed)
        with self.assertRaises(ValueError):
            verify_runtime_maps(manifest, full, full)
        duplicate = copy.deepcopy(manifest)
        duplicate["scenes"]["kanji/A.md"] = "a"
        with self.assertRaises(ValueError):
            verify_runtime_maps(duplicate, manifest["files"], full)


if __name__ == "__main__":
    unittest.main()
