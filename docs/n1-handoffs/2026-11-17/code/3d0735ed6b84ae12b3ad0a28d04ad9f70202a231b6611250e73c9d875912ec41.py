import copy
import json
import sys
import unittest

from verify_b134_gates import (
    BASE, GUARD_SHA, LATENT_LINE, ORDER, OWNER, READING_KEYS, commands, verify_execution,
    verify_launcher, verify_preservation, verify_quiz, verify_reading, verify_reading_source,
    verify_summary)


class B134GateEvidenceTests(unittest.TestCase):
    def memory(self):
        return {"breach": None, "freeRamBeforeBytes": 2 * 1024**3 + 1,
                "minimumObservedFreeRamBytes": 1024**3, "abortThresholdBytes": 1024**3,
                "samplingIntervalSeconds": 0.25}

    def test_summary_binds_snapshot_launcher_order_and_bounds(self):
        admission = {"base": BASE, "head": "candidate", "mode": "committed", "memory": self.memory()}
        summary = {"batch": 134, "base": BASE, "startingHead": "candidate", "mode": "committed",
                   "status": "PASS", "checks": list(ORDER), "serial": True, "manifestSha256": "manifest",
                   "runnerSha256": "runner", "commonHelperSha256": "common",
                   "boundedLauncherSha256": "launcher", "guardSha256": GUARD_SHA,
                   "waitTimeoutSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10,
                   "finalMemory": self.memory()}
        args = ("committed", "candidate", "manifest", "runner", "common", "launcher")
        verify_summary(summary, admission, *args)
        for field, value in (("batch", 133), ("startingHead", BASE), ("checks", list(reversed(ORDER))),
                             ("manifestSha256", "other"), ("boundedLauncherSha256", "other"),
                             ("serial", False)):
            changed = copy.deepcopy(summary)
            changed[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_summary(changed, admission, *args)

    def test_execution_requires_b134_launcher_commands(self):
        expected = commands()
        self.assertTrue(all(str(v[0]).endswith("bounded_launch_134.py") for v in expected.values()))
        self.assertTrue(str(expected["reading-exposure"][1]).endswith("check_reading_134.py"))
        receipts = {
            name: {"startedAt": f"2026-11-17T00:00:{i * 2:02d}+00:00",
                   "completedAt": f"2026-11-17T00:00:{i * 2 + 1:02d}+00:00",
                   "command": [sys.executable, "-B", *map(str, expected[name])],
                   "commonHelperSha256": "common", "cleanupTimeoutSecondsPerStage": 10,
                   "activeError": None, "cleanupError": None}
            for i, name in enumerate(ORDER)
        }
        verify_execution(receipts, expected, "common")
        changed = copy.deepcopy(receipts)
        changed["lint"]["command"][-1] = "\u5305"
        with self.assertRaises(ValueError):
            verify_execution(changed, expected, "common")

    def test_launcher_memory_line_is_b134(self):
        receipts = {name: {"boundedLauncherSha256": "launcher"} for name in ORDER}
        line = "B134 bounded launcher memory: " + json.dumps(self.memory()) + "\n"
        verify_launcher(receipts, {name: line for name in ORDER}, "launcher")
        with self.assertRaises(ValueError):
            verify_launcher(receipts, {name: line.replace("B134", "B133") for name in ORDER}, "launcher")

    def test_quiz_warnings_must_match_exact_count_and_kind(self):
        warn = "WARN  X (x): exclusion Y is not mentioned in Notes"
        superseded = "0 error(s), 2 warning(s)\n" + warn + "\n" + warn + "\n"
        self.assertEqual(verify_quiz(superseded, 2), 2)
        self.assertEqual(verify_quiz("0 error(s), 0 warning(s)\n", 0), 0)
        for log, count in ((superseded, 0), ("0 error(s), 0 warning(s)\n" + warn, 0),
                           ("1 error(s), 0 warning(s)\n", 0),
                           (superseded.replace("Notes\n", "Usage\n", 1), 2)):
            with self.subTest(log=log), self.assertRaises(ValueError):
                verify_quiz(log, count)

    def test_reading_requires_signed_keys_and_single_latent_disclosure(self):
        log = ("Explicit supplemental reading keys: " + json.dumps(READING_KEYS) + "\n" + LATENT_LINE
               + "\n0 production hit(s)\n0 padded-session hit(s)\n1 latent collision(s)\n")
        self.assertEqual(verify_reading(log, READING_KEYS), 1)
        for changed in (log.replace(LATENT_LINE, ""), log.replace("0 production", "1 production"),
                        log.replace("1 latent", "2 latent")):
            with self.subTest(log=changed), self.assertRaises(ValueError):
                verify_reading(changed, READING_KEYS)
        with self.assertRaises(ValueError):
            verify_reading(log, {"\u7d2b": READING_KEYS["\u7d2b"][:-1]})

    def test_reading_source_must_read_local_packet_copy(self):
        source = (b'packet = HERE / "source-002"\n'
                  b'for node in ET.parse(packet / "jmdict-complete-families.xml").getroot():\n    pass\n'
                  b'extras = json.loads((packet / "reading-keys.json").read_bytes())["testedKeys"]\n')
        verify_reading_source(source)
        for old, new in ((b'"source-002"', b'"source-001"'), (b".read_bytes()", b".read_text()"),
                         (b"ET.parse(packet", b"ET.parse(other")):
            with self.subTest(old=old), self.assertRaises(ValueError):
                verify_reading_source(source.replace(old, new))

    def test_preservation_scope_and_non_files_groups(self):
        baseline = {"contentVersion": "a", "files": {"words/\u7d2b.md": "w0", "kanji/A.md": "k"},
                    "audio": {"audio/x.mp3": "x"}}
        manifest = {"contentVersion": "b",
                    "files": {"words/\u7d2b.md": "w1", "kanji/A.md": "k", "kanji/\u7d2b.md": "n",
                              "strokes/\u7d2b.json": "s"}, "audio": {"audio/x.mp3": "x"}}
        memory = self.memory()
        summary = {"status": "PASS", "mode": "committed", "head": "c", "base": BASE, "clean": True,
                   "ownerSignature": copy.deepcopy(OWNER), "manifestSha256": "m", "contentVersion": "b",
                   "producerSha256": "p", "evidenceInventorySha256": "i", "memory": memory,
                   "added": ["kanji/\u7d2b.md", "strokes/\u7d2b.json"], "removed": [],
                   "changed": ["words/\u7d2b.md"], "baselineRuntimeCount": 2, "candidateRuntimeCount": 4,
                   "allCandidateRuntimeHashesChecked": 4, "allOtherRuntimeEntriesUnchanged": 1}
        args = (manifest, baseline, "c", "m", "p", "i")
        result = verify_preservation(summary, memory, manifest["files"], *args)
        self.assertEqual(result["unchangedNonFilesGroups"], {"audio": 1})
        with self.assertRaises(ValueError):
            verify_preservation(summary, memory, {**manifest["files"], "kanji/A.md": "z"}, *args)
        for field, value in (("allOtherRuntimeEntriesUnchanged", 2), ("producerSha256", "q"),
                             ("ownerSignature", {**OWNER, "status": "U"})):
            changed = dict(summary, **{field: value})
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_preservation(changed, memory, manifest["files"], *args)
        altered = copy.deepcopy(manifest)
        altered["audio"]["audio/x.mp3"] = "y"
        with self.assertRaises(ValueError):
            verify_preservation(summary, memory, altered["files"], altered, baseline, "c", "m", "p", "i")


if __name__ == "__main__":
    unittest.main()
