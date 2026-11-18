import copy
import gzip
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verify_b121_revision import CARD, STROKES, WORD, check_gate, check_metadata, check_runtime, sha, verify_sources


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
            with patch("verify_b121_revision.WS", root), patch("verify_b121_revision.INPUTS", pins):
                with patch("verify_b121_revision.git", return_value=complete):
                    result = verify_sources({"candidate": "initial"}, "revision", ["source.xml"], Guard())
                    self.assertEqual(result["dictionaryRecords"][0]["completeRecordsVerified"], 1)
                for omitted in (
                    b"<sense><stagr>reading</stagr><gloss>secondary</gloss></sense>",
                    b"<re_restr>word</re_restr>",
                ):
                    with self.subTest(omitted=omitted), patch(
                        "verify_b121_revision.git", return_value=complete.replace(omitted, b"")
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

    def test_preserve_readings_and_prior_guards_while_replacing_options(self):
        old = {"onyomi": ["\u30c8\u30af"], "kunyomi": [], "quizOnyomi": ["\u30c8\u30af"],
               "distractors": ["a", "b", "c"], "quiz_exclusions": ["old"]}
        new = {**old, "distractors": ["d", "e", "f"], "quiz_exclusions": ["old", *"\u5e78\u8ca1\u5049"]}
        check_metadata(old, new)
        for key, value in (("onyomi", []), ("kunyomi", ["new"]), ("quizOnyomi", []),
                           ("quiz_exclusions", list("\u5e78\u8ca1\u5049")),
                           ("distractors", ["d", "d", "f"]),
                           ("distractors", ["d", "e", "\u8ca1"])):
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                check_metadata(old, {**new, key: value})

    def test_gate_rejects_changed_evidence_and_weakened_memory_limits(self):
        log = b"manifest rebuilt"
        receipt = {
            "gate": "manifest-rebuild", "exitCode": 0, "cwd": "repo", "logSha256": sha(log),
            "manifestSha256": "manifest", "manifestReproducible": True,
            "memory": {"breach": None, "freeRamBeforeBytes": 3 * 1024**3,
                       "minimumObservedFreeRamBytes": 2 * 1024**3,
                       "abortThresholdBytes": 1024**3, "samplingIntervalSeconds": 0.25},
        }
        check_gate(receipt, log, "manifest-rebuild", "manifest", "repo")
        for key, value in (("exitCode", 1), ("cwd", "another-repo"), ("logSha256", "changed"),
                           ("manifestSha256", "changed"), ("manifestReproducible", False)):
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_gate({**receipt, key: value}, log, "manifest-rebuild", "manifest", "repo")
        for key, value in (("breach", "low RAM"), ("freeRamBeforeBytes", 2 * 1024**3),
                           ("minimumObservedFreeRamBytes", 1024**3),
                           ("abortThresholdBytes", 512 * 1024**2), ("samplingIntervalSeconds", 1)):
            changed = copy.deepcopy(receipt)
            changed["memory"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                check_gate(changed, log, "manifest-rebuild", "manifest", "repo")


if __name__ == "__main__":
    unittest.main()
