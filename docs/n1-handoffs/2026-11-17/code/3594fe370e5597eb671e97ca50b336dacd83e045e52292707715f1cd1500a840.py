import copy
import gzip
import tempfile
import unittest

from common import GUARD_SHA
from pathlib import Path
from unittest.mock import patch

from verify_b123_revision_v2 import CARD, STROKES, WORD, check_gate, check_metadata, check_runtime, sha, verify_sources


class RevisionTests(unittest.TestCase):
    def test_source_verification_rejects_omitted_sense_or_restriction(self):
        complete = (
            b"<JMdict><entry><ent_seq>1</ent_seq><k_ele><keb>word</keb></k_ele>"
            b"<r_ele><reb>reading</reb><re_restr>word</re_restr></r_ele>"
            b"<sense><gloss>first</gloss></sense>"
            b"<sense><stagr>reading</stagr><gloss>secondary</gloss></sense></entry></JMdict>"
        )
        class Guard:
            def check(self):
                pass

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            inputs = root / "control" / "inputs"
            inputs.mkdir(parents=True)
            compressed = gzip.compress(complete)
            (inputs / "fixture.gz").write_bytes(compressed)
            pins = {"jmdict": ("fixture.gz", sha(compressed), "entry", "ent_seq")}
            with patch("verify_b123_revision_v2.WS", root), patch("verify_b123_revision_v2.INPUTS", pins):
                with patch("verify_b123_revision_v2.git", return_value=complete):
                    result = verify_sources({"candidate": "initial"}, "revision", ["source.xml"], Guard())
                    self.assertEqual(result["dictionaryRecords"][0]["completeRecordsVerified"], 1)
                for omitted in (
                    b"<sense><stagr>reading</stagr><gloss>secondary</gloss></sense>",
                    b"<re_restr>word</re_restr>",
                ):
                    with self.subTest(omitted=omitted), patch(
                        "verify_b123_revision_v2.git", return_value=complete.replace(omitted, b"")
                    ), self.assertRaisesRegex(ValueError, "Incomplete or altered"):
                        verify_sources({"candidate": "initial"}, "revision", ["source.xml"], Guard())

    def test_only_wrapper_and_new_card_change_baseline_runtime(self):
        before = {"files": {WORD: "old", "kanji/existing.md": "preserved"}}
        after = {"files": {WORD: "new", "kanji/existing.md": "preserved", CARD: "card", STROKES: "stroke"}}
        check_runtime(before, after)
        for path, value in (("kanji/existing.md", "changed"), ("kanji/unrelated.md", "added")):
            changed = copy.deepcopy(after)
            changed["files"][path] = value
            with self.subTest(path=path), self.assertRaises(ValueError):
                check_runtime(before, changed)
        changed = copy.deepcopy(after)
        del changed["files"]["kanji/existing.md"]
        with self.assertRaises(ValueError):
            check_runtime(before, changed)

    def test_preserve_readings_and_prior_guards_while_preserving_options(self):
        old = {"onyomi": ["\u30cf\u30f3"], "kunyomi": [], "quizOnyomi": ["\u30cf\u30f3"],
               "distractors": ["a", "b", "c"], "quiz_exclusions": ["old"]}
        new = {**old, "distractors": ["a", "b", "c"], "quiz_exclusions": ["old", *"\u6a19\u7d00\u93e1\u69d8\u683c"]}
        check_metadata(old, new)
        for key, value in (("onyomi", []), ("kunyomi", ["new"]), ("quizOnyomi", []),
                           ("quiz_exclusions", list("\u6a19\u7d00\u93e1\u69d8\u683c")),
                           ("distractors", ["d", "e", "f"]),
                           ("distractors", ["d", "d", "f"]),
                           ("distractors", ["d", "e", "\u5e38"])):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                check_metadata(old, {**new, key: value})

    def test_gate_rejects_changed_evidence_and_weakened_memory_limits(self):
        log = b"manifest rebuilt"
        receipt = {
            "gate": "manifest-rebuild", "exitCode": 0, "cwd": "repo", "logSha256": sha(log),
            "manifestSha256": "manifest", "manifestReproducible": True,
            "childExitCodeAfterCleanup": 0, "waitTimeoutSeconds": 0.1,
            "runnerSha256": "runner", "guardSha256": GUARD_SHA, "logBytes": len(log),
            "memory": {"breach": None, "freeRamBeforeBytes": 3 * 1024**3,
                       "minimumObservedFreeRamBytes": 2 * 1024**3,
                       "abortThresholdBytes": 1024**3, "samplingIntervalSeconds": 0.25},
        }
        check_gate(receipt, log, "manifest-rebuild", "manifest", "repo", "runner")
        for key, value in (("exitCode", 1), ("cwd", "another-repo"), ("logSha256", "changed"),
                           ("manifestSha256", "changed"), ("manifestReproducible", False)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_gate({**receipt, key: value}, log, "manifest-rebuild", "manifest", "repo", "runner")
        for key, value in (("breach", "low RAM"), ("freeRamBeforeBytes", 2 * 1024**3),
                           ("minimumObservedFreeRamBytes", 1024**3 - 1),
                           ("abortThresholdBytes", 512 * 1024**2), ("samplingIntervalSeconds", 1)):
            changed = copy.deepcopy(receipt)
            changed["memory"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_gate(changed, log, "manifest-rebuild", "manifest", "repo", "runner")


if __name__ == "__main__":
    unittest.main()
