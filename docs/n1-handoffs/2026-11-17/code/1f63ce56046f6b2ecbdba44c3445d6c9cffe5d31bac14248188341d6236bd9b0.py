import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import verify_b119_revision as verifier
from common import write_frozen


class RevisionPreservationTests(unittest.TestCase):
    def test_each_target_keeps_metadata_and_old_guards(self):
        from common import git, load_batch
        config = load_batch(119)
        for character in verifier.SUPPORT:
            before = git(config, "show", f"{config['candidate']}:kanji/{character}.md").decode("utf-8")
            old, _ = verifier.parse(before)
            old_line = "quiz_exclusions: [" + ", ".join(old["quiz_exclusions"]) + "]"
            new_line = old_line[:-1] + ", " + ", ".join(sorted(verifier.REQUIRED[character])) + "]"
            revised = before.replace(old_line, new_line)
            unnamed, named = (("the upper strokes", "the 爪-shaped upper component") if character == "妥"
                              else ("the layered strokes on the right", "the 盾-shaped component on the right"))
            revised = revised.replace(unnamed, named)
            with self.subTest(character=character, case="valid"):
                self.assertEqual(verifier.verify_card(before, revised, verifier.REQUIRED[character]),
                                 verifier.REQUIRED[character])
            for invalid in (before, revised.replace("jlpt: 1", "jlpt: 2"),
                            revised.replace("## Meaning and origin", "## Unsupported replacement"),
                            revised.replace(old["quiz_exclusions"][0] + ", ", "", 1),
                            revised.replace(named, unnamed),
                            revised.replace("mnemonic, not etymology", "historical origin"),
                            revised.replace("## Common words", "## New teaching section")):
                with self.subTest(character=character, case="metadata-or-guard"):
                    with self.assertRaises(ValueError):
                        verifier.verify_card(before, invalid, verifier.REQUIRED[character])

    def test_both_targets_supplemental_readings_are_required(self):
        all_readings = " ".join(text for c, readings in verifier.READINGS.items() for text in (c, *readings))
        for omitted in ("", "したがう", "おだやか"):
            with self.subTest(omitted=omitted), tempfile.TemporaryDirectory() as temp:
                directory = Path(temp)
                text = all_readings.replace(omitted, "") if omitted else all_readings
                log = write_frozen(directory / "reading-exposure.log", text.encode("utf-8"))
                write_frozen(directory / "reading-exposure.json", json.dumps({
                    "gate": "reading-exposure", "exitCode": 0, "logSha256": log["sha256"],
                    "memory": {"breach": None, "freeRamBeforeBytes": 3 * 1024 ** 3,
                               "minimumObservedFreeRamBytes": 2 * 1024 ** 3},
                }).encode())
                try:
                    with patch.object(verifier, "CHECKS", ("reading-exposure",)):
                        if omitted:
                            with self.assertRaises(ValueError):
                                verifier.verify_gates(directory, b"manifest", {}, Mock())
                        else:
                            self.assertEqual(len(verifier.verify_gates(directory, b"manifest", {}, Mock())), 1)
                finally:
                    for path in directory.iterdir():
                        path.chmod(0o644)

    def test_complete_jmdict_and_modern_membership_bindings(self):
        from common import WS, load_batch
        directory = WS / "scratch-119" / "review" / "reconciliation-001"
        receipt = json.loads((directory / "source-extraction.json").read_bytes())
        config = load_batch(119)
        result = verifier.verify_supplemental_sources(config, verifier.INTERMEDIATE, directory, receipt, Mock())
        self.assertEqual(result["completeJmdictRecordsVerified"], len(receipt["jmdictEntryIds"]))
        self.assertEqual(result["sourceRows"], [225, 345])
        for invalid in ({**receipt, "jmdictInputSha256": "0" * 64},
                        {**receipt, "jmdictEntryIds": receipt["jmdictEntryIds"][:-1]}):
            with self.subTest(receipt=invalid["jmdictInputSha256"], entries=len(invalid["jmdictEntryIds"])):
                with self.assertRaises(ValueError):
                    verifier.verify_supplemental_sources(config, verifier.INTERMEDIATE, directory, invalid, Mock())


if __name__ == "__main__":
    unittest.main()
