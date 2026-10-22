import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import build_manifest
from check_content_budget import check
from validate_listening import content_hash, validate_document


def passage():
    return {
        "schemaVersion": 1, "id": "example", "jlpt": 5, "kind": "monologue",
        "title": "A message", "topic": "routine", "levelRationale": "Short basic sentences.",
        "speakers": [{"id": "a", "voice": "ja-JP-NanamiNeural", "ratePercent": -10}],
        "turns": [{"id": "one", "speaker": "a", "text": "こんにちは。", "translation": "Hello."}],
        "questions": [{
            "id": f"q-{number}", "mainPoint": number == 0, "prompt": f"Question {number}?",
            "options": [{"id": f"a-{option}", "label": f"Choice {option}", "rationale": "Fixture rationale."}
                        for option in range(4)],
            "answer": "a-0", "evidence": ["one"], "explanation": "Fixture explanation.",
        } for number in range(3)],
    }


class ListeningTests(unittest.TestCase):
    def test_pending_and_exact_approval_bindings(self):
        data = passage()
        self.assertFalse(validate_document(data, "listening/example.json"))
        digest = content_hash(data)
        data["audio"] = {"path": "audio/example.ogg", "sha256": "a" * 64, "contentSha256": digest,
                         "durationMs": 20000, "turns": [{"id": "one", "startMs": 250, "endMs": 19500}]}
        self.assertFalse(validate_document(data, "listening/example.json"))
        data["audioReview"] = {"status": "approved", "audioSha256": "a" * 64,
                               "contentSha256": digest, "reviewedOn": "2026-10-22", "note": "Test declaration only."}
        self.assertTrue(validate_document(data, "listening/example.json"))
        for change in ("question", "audio", "timing"):
            with self.subTest(change=change):
                changed = copy.deepcopy(data)
                if change == "question":
                    changed["questions"][0]["options"][0]["label"] = "Changed tested fact"
                elif change == "audio":
                    changed["audio"]["sha256"] = "b" * 64
                else:
                    changed["audio"]["turns"][0]["endMs"] = 20001
                with self.assertRaises(ValueError):
                    validate_document(changed, "listening/example.json")

    def test_strict_n5_questions_and_evidence(self):
        for mutation in (
            lambda d: d.update(jlpt=True), lambda d: d.update(jlpt=4),
            lambda d: d["questions"][1].update(mainPoint=True),
            lambda d: d["questions"][0].update(answer="missing"),
            lambda d: d["questions"][0].update(evidence=["absent"]),
            lambda d: d["questions"][0]["options"][1].update(label="Choice 0"),
            lambda d: d["turns"][0].update(speaker="missing"),
            lambda d: d.update(image="images/../unsafe.webp"),
        ):
            data = passage()
            mutation(data)
            with self.assertRaises(ValueError):
                validate_document(data, "listening/example.json")

    def test_manifest_separates_binary_audio_and_binds_content_version(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "listening").mkdir()
            (root / "audio").mkdir()
            before = build_manifest.build_manifest(root)
            (root / "listening" / "example.json").write_text(json.dumps(passage()), encoding="utf-8")
            audio = root / "audio" / "example.ogg"
            audio.write_bytes(b"binary\r\ncontent")
            added = build_manifest.build_manifest(root)
            self.assertEqual({}, added["files"])
            self.assertIn("listening/example.json", added["listening"])
            self.assertEqual(hashlib.sha256(audio.read_bytes()).hexdigest(), added["audio"]["audio/example.ogg"])
            self.assertNotEqual(before["contentVersion"], added["contentVersion"])
            audio.write_bytes(b"binary\ncontent")
            self.assertNotEqual(added["contentVersion"], build_manifest.build_manifest(root)["contentVersion"])

    def test_complete_archive_budget_includes_skipped_files_and_audio_envelope(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "audio").mkdir()
            (root / "docs").mkdir()
            (root / "audio" / "a.ogg").write_bytes(b"audio")
            (root / "docs" / "ignored.txt").write_bytes(b"ignored documentation")
            budget = check(root, ["audio/a.ogg", "docs/ignored.txt"])
            self.assertEqual(5, budget["retainedBytes"])
            self.assertEqual(26, budget["inflatedBytes"])
            (root / "audio" / "a.ogg").write_bytes(b"x" * (512 * 1024 + 1))
            with self.assertRaisesRegex(ValueError, "per-file"):
                check(root, ["audio/a.ogg"])


if __name__ == "__main__":
    unittest.main()
