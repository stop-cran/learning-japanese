"""Contract fixtures are structural tests, never approval of heard Japanese or pictures."""
import copy
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

import build_manifest
import check_content_budget as budget
import validate
import validate_listening as legacy
import validate_listening_tasks as tasks


REPO = Path(__file__).resolve().parent.parent
EXAMPLES = REPO / "docs" / "listening-task-examples"
FIXTURES = {
    "task-based": ("n5-task-open-window", "2cc6a18530ee43db05da4b652fd52e7b49756ca7cbe12d57669df2916e0de6e0"),
    "key-point": ("n5-task-rainy-class", "cb18354fbfe4f17fee38b3096f2659eaf5f00cc9b571ae1ba118d6713183f687"),
    "verbal-expression": ("n5-task-borrow-pencil", "8dfd632512947247a44f751c34106459e6cd301479e353fae8ab167573de9b3f"),
    "quick-response": ("n5-task-park-invitation", "e49baee157fb73aa58675e4d59da91dda1c9c8b0028fc2c4ad70ed9d9b1456a7"),
}


def example(kind="task-based"):
    return json.loads((EXAMPLES / f"{FIXTURES[kind][0]}.json").read_text(encoding="utf-8"))


def check(document, root=None):
    return tasks.validate_document(document, f"listening-tasks/{document['id']}.json", root)


def with_media(document, duration=1000):
    document["media"] = {
        "contentSha256": tasks.content_hash(document),
        "audio": {
            stage["id"]: {
                "path": f"task-audio/{stage['id']}.ogg", "sha256": "a" * 64, "durationMs": duration,
                "turns": [{"id": turn, "startMs": index * duration // len(stage["turns"]),
                           "endMs": (index + 1) * duration // len(stage["turns"])}
                          for index, turn in enumerate(stage["turns"])],
            } for stage in document["stages"]
        },
    }
    if "visual" in document:
        document["media"]["image"] = {"path": "task-images/scene.webp", "sha256": "b" * 64}
    return document


def declared_approval(document):
    document["approval"] = {
        "status": "approved", "contentSha256": tasks.content_hash(document),
        "mediaSha256": tasks.media_hash(document["media"]), "reviewedOn": "2026-10-24",
        "note": "Test-only declaration. No actual listening or visual approval.",
    }
    return document


def ogg_page(packets, sequence, flags, granule):
    lengths = b"".join(bytes([255]) * (len(packet) // 255) + bytes([len(packet) % 255]) for packet in packets)
    page = bytearray(b"OggS\x00" + bytes([flags]) + granule.to_bytes(8, "little")
                     + (1).to_bytes(4, "little") + sequence.to_bytes(4, "little")
                     + bytes(4) + bytes([len(lengths)]) + lengths + b"".join(packets))
    crc = 0
    for byte in page:
        crc ^= byte << 24
        for _ in range(8):
            crc = ((crc << 1) ^ (0x04C11DB7 if crc & 0x80000000 else 0)) & 0xFFFFFFFF
    page[22:26] = crc.to_bytes(4, "little")
    return bytes(page)


def opus(duration, channels=1):
    """Build isolated silence-container fixtures, not generated Japanese recordings."""
    preskip = 312
    head = b"OpusHead\x01" + bytes([channels]) + preskip.to_bytes(2, "little") + (48000).to_bytes(4, "little") + bytes(3)
    result = ogg_page([head], 0, 2, 0) + ogg_page([b"OpusTags" + bytes(8)], 1, 0, 0)
    samples = duration * 48 + preskip
    packets = (samples + 959) // 960
    sequence = 2
    for start in range(0, packets, 255):
        count = min(255, packets - start)
        last = start + count == packets
        result += ogg_page([b"\xf8\xff\xfe"] * count, sequence, 4 if last else 0,
                           samples if last else (start + count) * 960)
        sequence += 1
    return result


def image_bytes(width=2, height=2):
    buffer = io.BytesIO()
    Image.new("RGB", (width, height)).save(buffer, format="WEBP")
    return buffer.getvalue()


class TaskSchemaTests(unittest.TestCase):
    def test_all_adopted_examples_and_cross_language_hashes(self):
        for kind, (_, digest) in FIXTURES.items():
            with self.subTest(kind=kind):
                document = example(kind)
                self.assertFalse(check(document))
                self.assertEqual(digest, tasks.content_hash(document))
                self.assertFalse(check(with_media(document)))
                self.assertTrue(check(declared_approval(document)))

    def test_integer_only_canonical_content_and_entire_media(self):
        document = example()
        original = tasks.content_hash(document)
        reordered = dict(reversed(list(document.items())))
        reordered["speakers"] = [dict(reversed(list(speaker.items()))) for speaker in document["speakers"]]
        self.assertEqual(original, tasks.content_hash(reordered))
        document = declared_approval(with_media(document))
        self.assertEqual(original, tasks.content_hash(document))
        self.assertEqual("ae574b684a98954b2ddd605e2afc11eae2fc44cee60f381e8f239593c190b67b",
                         tasks.media_hash(document["media"]))
        changed = copy.deepcopy(document)
        changed["turns"].reverse()
        self.assertNotEqual(original, tasks.content_hash(changed))
        for value in (1.0, float("inf"), float("nan")):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "integers"):
                legacy.canonical_hash({"nested": [value]})
        document["media"]["audio"]["focus"]["durationMs"] = 1000.0
        with self.assertRaisesRegex(ValueError, "integers"):
            check(document)

    def test_explicit_unsupported_versions_and_types(self):
        for field, values in (
            ("schemaVersion", (0, 2, "1", True, 1.0, None)),
            ("policyVersion", (0, 2, "1", True, 1.0, None)),
            ("taskType", ("future", "dialogue", 1, [], None)),
        ):
            for value in values:
                document = example()
                document[field] = value
                with self.subTest(field=field, value=value), self.assertRaisesRegex(tasks.UnsupportedTaskError, "unsupported"):
                    check(document)

    def test_unknown_fields_at_every_supported_object_boundary(self):
        document = example("verbal-expression")
        document["vocabulary"] = [{"surface": "えんぴつ", "reading": "えんぴつ", "gloss": "pencil"}]
        declared_approval(with_media(document))
        selectors = (
            lambda d: d, lambda d: d["speakers"][0], lambda d: d["turns"][0],
            lambda d: d["stages"][0], lambda d: d["options"][0], lambda d: d["visual"],
            lambda d: d["vocabulary"][0], lambda d: d["media"], lambda d: d["media"]["image"],
            lambda d: d["media"]["audio"]["instruction"],
            lambda d: d["media"]["audio"]["instruction"]["turns"][0], lambda d: d["approval"],
        )
        for index, selector in enumerate(selectors):
            changed = copy.deepcopy(document)
            selector(changed)["future"] = "unknown"
            # Rebind the enclosing hashes so the unknown-field check is actually reached.
            changed["media"]["contentSha256"] = tasks.content_hash(changed)
            changed["approval"]["contentSha256"] = tasks.content_hash(changed)
            changed["approval"]["mediaSha256"] = tasks.media_hash(changed["media"])
            with self.subTest(boundary=index), self.assertRaisesRegex(ValueError, "unknown fields"):
                check(changed)

    def test_unused_narrator_is_allowed_but_characters_and_references_are_required(self):
        document = example("verbal-expression")
        for turn in document["turns"]:
            turn["speaker"] = "a"
        self.assertFalse(check(document))
        document["turns"][0]["speaker"] = "undeclared"
        with self.assertRaisesRegex(ValueError, "unknown turn speaker"):
            check(document)
        for turn in document["turns"]:
            turn["speaker"] = "n"
        with self.assertRaisesRegex(ValueError, "every character speaker"):
            check(document)

    def test_optional_vocabulary_word_must_be_omitted_not_null(self):
        document = example()
        document["vocabulary"] = [{"surface": "窓", "reading": "まど", "gloss": "window"}]
        self.assertFalse(check(document))
        document["vocabulary"][0]["word"] = None
        with self.assertRaisesRegex(ValueError, "vocabulary word"):
            check(document)

    def test_malformed_required_values_and_closed_references(self):
        mutations = (
            lambda d: d.update(jlpt=True), lambda d: d.update(jlpt=4),
            lambda d: d.update(id="Not-lowercase"), lambda d: d.update(exposureId=""),
            lambda d: d.update(kind=[]), lambda d: d.update(usage="practice"),
            lambda d: d.update(blueprint=None), lambda d: d.update(title=" " * 2000 + "x"),
            lambda d: d.update(topic="bad\ntext"), lambda d: d.update(explanation=""),
            lambda d: d["speakers"][0].update(role="host"),
            lambda d: d["speakers"][1].update(role="narrator"),
            lambda d: d["speakers"][1].update(voice="en-US-TestNeural"),
            lambda d: d["speakers"][1].update(voice="ja-JP-" + "A" * 2000 + "Neural"),
            lambda d: d["speakers"][0].update(ratePercent=True),
            lambda d: d["speakers"][0].update(ratePercent=-16),
            lambda d: d["speakers"][0].update(id=d["speakers"][1]["id"]),
            lambda d: d["turns"][0].update(speaker="missing"),
            lambda d: d["turns"][0].update(spokenText=None),
            lambda d: d["turns"][0].update(text="あ" * 501),
            lambda d: d["turns"].append({**d["turns"][0], "id": "unused"}),
            lambda d: d["turns"][0].update(id=d["turns"][1]["id"]),
            lambda d: d.update(answer=[]), lambda d: d.update(answer="missing"),
            lambda d: d.update(evidence=["focus"]),
            lambda d: d.update(evidence=["request", "request"]),
            lambda d: d.update(evidence=["absent"]),
            lambda d: d["stages"][0].update(turns=["absent"]),
            lambda d: d["stages"][0].update(turns=[]),
            lambda d: d["stages"][0].update(turns=["instruction", "instruction"]),
        )
        for index, mutate in enumerate(mutations):
            document = example()
            mutate(document)
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                check(document)
        document = example()
        for field in list(document):
            changed = copy.deepcopy(document)
            del changed[field]
            with self.subTest(missing=field), self.assertRaises(ValueError):
                tasks.validate_document(changed, f"listening-tasks/{document['id']}.json")
        with self.assertRaisesRegex(ValueError, "filename"):
            tasks.validate_document(document, "listening-tasks/other.json")

    def test_stage_topology_focus_and_spoken_option_numbering(self):
        mutations = (
            lambda d: d["stages"].reverse(),
            lambda d: d["stages"].pop(),
            lambda d: d["stages"][0].update(id=d["stages"][1]["id"]),
            lambda d: d["stages"][0].update(role="focus"),
            lambda d: d["stages"][0].update(optionId=d["answer"]),
            lambda d: d["options"].pop(),
            lambda d: d["options"].reverse(),
            lambda d: d["options"][0].update(number=True),
            lambda d: d["options"][0].update(number=0),
            lambda d: d["options"][1].update(id=d["options"][0]["id"]),
            lambda d: d["options"][1].update(label=d["options"][0]["label"]),
        )
        for kind in FIXTURES:
            for index, mutate in enumerate(mutations):
                document = example(kind)
                mutate(document)
                with self.subTest(kind=kind, mutation=index), self.assertRaises(ValueError):
                    check(document)
        document = example()
        document["stages"][3]["turns"] = ["instruction"]
        with self.assertRaisesRegex(ValueError, "focus-repeat"):
            check(document)
        for mutate in (
            lambda d: d["stages"][2].pop("optionId"),
            lambda d: d["stages"][2].update(optionId=d["options"][1]["id"]),
            lambda d: d["stages"][2]["turns"].append("utterance"),
            lambda d: d["turns"][2].update(text=d["options"][0]["label"]),
            lambda d: d["turns"][2].update(text="2。" + d["options"][0]["label"]),
        ):
            document = example("quick-response")
            mutate(document)
            with self.assertRaises(ValueError):
                check(document)
        document = example("quick-response")
        document["turns"][2]["spokenText"] = "いち。いいですね。行きましょう。"
        self.assertFalse(check(document))

    def test_visual_and_choice_mode_rules(self):
        visual = {"role": "required", "description": "An unselected numbered grid."}
        for kind in FIXTURES:
            for mode in ("text", "visual", "audio", None):
                document = example(kind)
                document["choiceMode"] = mode
                if kind in ("task-based", "key-point") and mode == "visual":
                    document["visual"] = visual
                valid = mode in (("text", "visual") if kind in ("task-based", "key-point") else ("audio",))
                with self.subTest(kind=kind, mode=mode):
                    if valid:
                        self.assertFalse(check(document))
                    else:
                        with self.assertRaises(ValueError):
                            check(document)
        for kind, picture in (("quick-response", visual), ("verbal-expression", None),
                              ("verbal-expression", {"role": "context", "description": "Scene."}),
                              ("task-based", None)):
            document = example(kind)
            if kind == "task-based":
                document["choiceMode"] = "visual"
            if picture is None:
                document.pop("visual", None)
            else:
                document["visual"] = picture
            with self.subTest(kind=kind, picture=picture), self.assertRaises(ValueError):
                check(document)

    def test_complete_media_and_explicit_pending_approval(self):
        self.assertFalse(check(example()))
        self.assertFalse(check(with_media(example())))
        mutations = (
            lambda d: d.update(media=None), lambda d: d.update(media={}),
            lambda d: d["media"].pop("audio"),
            lambda d: d["media"]["audio"].pop("focus"),
            lambda d: d["media"]["audio"].update(extra=d["media"]["audio"]["focus"]),
            lambda d: d["media"].update(image={"path": "task-images/scene.webp", "sha256": "b" * 64}),
            lambda d: d["media"]["audio"]["focus"].update(sha256="bad"),
            lambda d: d["media"]["audio"]["focus"].update(durationMs=249),
            lambda d: d["media"]["audio"]["focus"].update(durationMs=90001),
            lambda d: d["media"]["audio"]["focus"].update(durationMs=True),
            lambda d: d["media"]["audio"]["focus"].update(turns=[]),
            lambda d: d["media"]["audio"]["focus"]["turns"][0].update(id="instruction"),
            lambda d: d["media"]["audio"]["focus"]["turns"][0].update(startMs=True),
            lambda d: d["media"]["audio"]["focus"]["turns"][0].update(startMs=-1),
            lambda d: d["media"]["audio"]["focus"]["turns"][0].update(endMs=0),
            lambda d: d["media"]["audio"]["focus"]["turns"][0].update(endMs=1001),
            lambda d: d["media"]["audio"]["passage"]["turns"][1].update(startMs=0),
            lambda d: d.update(approval=None),
        )
        for index, mutate in enumerate(mutations):
            document = with_media(example())
            mutate(document)
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                check(document)
        document = with_media(example("verbal-expression"))
        del document["media"]["image"]
        with self.assertRaisesRegex(ValueError, "iff visual"):
            check(document)
        document = declared_approval(with_media(example()))
        del document["media"]
        with self.assertRaisesRegex(ValueError, "approval without media"):
            check(document)

    def test_every_media_change_invalidates_exact_output_approval(self):
        mutations = (
            lambda d: d.update(title="Changed"),
            lambda d: d["turns"][0].update(spokenText="別の説明です。"),
            lambda d: d["options"][0].update(rationale="Changed feedback"),
            lambda d: d["media"]["audio"]["choice-three"].update(path="task-audio/replacement.ogg"),
            lambda d: d["media"]["audio"]["choice-three"].update(sha256="f" * 64),
            lambda d: d["media"]["audio"]["choice-three"].update(durationMs=1001),
            lambda d: d["media"]["audio"]["choice-three"]["turns"][0].update(endMs=999),
            lambda d: d["media"]["image"].update(path="task-images/replacement.webp"),
            lambda d: d["media"]["image"].update(sha256="f" * 64),
            lambda d: d["approval"].update(status="pending"),
            lambda d: d["approval"].update(mediaSha256="f" * 64),
            lambda d: d["approval"].update(contentSha256="f" * 64),
            lambda d: d["approval"].update(reviewedOn="2026-02-30"),
            lambda d: d["approval"].update(note=""),
        )
        for index, mutate in enumerate(mutations):
            document = declared_approval(with_media(example("verbal-expression")))
            mutate(document)
            with self.subTest(mutation=index), self.assertRaises(ValueError):
                check(document)

    def test_shared_recording_counts_each_occurrence(self):
        document = with_media(example(), duration=37500)
        document["media"]["audio"]["repeat"] = copy.deepcopy(document["media"]["audio"]["focus"])
        self.assertFalse(check(document))
        document["media"]["audio"]["repeat"]["durationMs"] += 1
        with self.assertRaisesRegex(ValueError, "conflicting shared audio"):
            check(document)
        document = with_media(example(), duration=37501)
        with self.assertRaisesRegex(ValueError, "150000"):
            check(document)

    def test_safe_flat_media_paths(self):
        for path in ("audio/focus.ogg", "task-audio/../focus.ogg", "task-audio/sub/focus.ogg",
                     "task-audio\\focus.ogg", "task-audio/Focus.ogg", "task-audio/focus.ogg:stream",
                     "task-audio/focus.wav", "task-audio/focus .ogg"):
            document = with_media(example())
            document["media"]["audio"]["focus"]["path"] = path
            with self.subTest(path=path), self.assertRaises(ValueError):
                check(document)
        document = with_media(example("verbal-expression"))
        document["media"]["image"]["path"] = "images/scene.webp"
        with self.assertRaisesRegex(ValueError, "unsafe"):
            check(document)


class TaskFilesTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(dir=REPO)
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        return path

    def media_document(self, kind="task-based"):
        document = with_media(example(kind))
        audio = opus(1000)
        for clip in document["media"]["audio"].values():
            clip["sha256"] = hashlib.sha256(audio).hexdigest()
            self.write(clip["path"], audio)
        if "visual" in document:
            picture = image_bytes()
            document["media"]["image"]["sha256"] = hashlib.sha256(picture).hexdigest()
            self.write(document["media"]["image"]["path"], picture)
        return document

    def errors(self, identity_ledger=None):
        errors = []
        tasks.check_listening_tasks(lambda path, message: errors.append((path, message)), self.root, identity_ledger)
        return [message for _, message in errors]

    def test_real_file_integrity_and_declared_duration(self):
        document = self.media_document("verbal-expression")
        self.assertFalse(check(document, self.root))
        self.assertTrue(check(declared_approval(document), self.root))
        for data, message in ((opus(1300), "duration"), (b"invalid", "Ogg"),
                              (b"x" * (512 * 1024 + 1), "exceeds")):
            self.write("task-audio/instruction.ogg", data)
            document["media"]["audio"]["instruction"]["sha256"] = hashlib.sha256(data).hexdigest()
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                check(document, self.root)
        document = self.media_document()
        self.write("task-audio/instruction.ogg", b"replacement")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            check(document, self.root)
        (self.root / "task-audio" / "instruction.ogg").unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            check(document, self.root)

    def test_webp_decode_size_hash_and_required_file(self):
        document = self.media_document("verbal-expression")
        for picture, message in ((b"RIFF\x04\x00\x00\x00WEBP", None),
                                 (image_bytes(2049, 1), "1-2048"),
                                 (b"x" * (150 * 1024 + 1), "exceeds")):
            self.write("task-images/scene.webp", picture)
            document["media"]["image"]["sha256"] = hashlib.sha256(picture).hexdigest()
            with self.subTest(message=message), self.assertRaises((ValueError, OSError)):
                check(document, self.root)
        document = self.media_document("verbal-expression")
        self.write("task-images/scene.webp", b"replacement")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            check(document, self.root)
        (self.root / "task-images" / "scene.webp").unlink()
        with self.assertRaisesRegex(ValueError, "missing"):
            check(document, self.root)

    def test_word_references_are_existing_exact_flat_articles(self):
        document = example()
        document["vocabulary"] = [{"surface": "窓", "reading": "まど", "gloss": "window", "word": "窓"}]
        with self.assertRaisesRegex(ValueError, "missing word"):
            check(document, self.root)
        self.write("words/窓.md", "Window")
        self.assertFalse(check(document, self.root))
        for word in ("../窓", "folder\\窓", ".", "..", "C:window", "window?"):
            document["vocabulary"][0]["word"] = word
            with self.subTest(word=word), self.assertRaisesRegex(ValueError, "unsafe"):
                check(document, self.root)
        self.write("words/Window.md", "Window")
        document["vocabulary"][0]["word"] = "window"
        with self.assertRaisesRegex(ValueError, "missing word"):
            check(document, self.root)

    def test_catalog_disjointness_and_existing_identity_evidence(self):
        document = example()
        name = f"listening-tasks/{document['id']}.json"
        self.write(name, json.dumps(document))
        self.assertEqual([], self.errors({document["id"]: document["exposureId"]}))
        self.assertTrue(any("rebind" in error for error in self.errors({document["id"]: "old-story"})))
        self.write("docs/listening-task-sources.json", json.dumps({
            "identities": [{"id": document["id"], "exposureId": "old-story", "context": "Original context"}],
        }))
        self.assertTrue(any("rebind" in error for error in self.errors()))
        self.write(f"listening/{document['id']}.json", "{}")
        self.assertTrue(any("collides" in error for error in self.errors()))

    def test_catalog_reports_unsupported_orphans_and_nonflat_files(self):
        document = example()
        document["policyVersion"] = 2
        self.write(f"listening-tasks/{document['id']}.json", json.dumps(document))
        self.write("listening-tasks/nested/a.json", "{}")
        self.write("task-audio/orphan.ogg", b"not audio")
        self.write("task-images/nested/orphan.webp", b"not image")
        errors = self.errors()
        self.assertTrue(any("unsupported" in error for error in errors))
        self.assertTrue(any("flat JSON" in error for error in errors))
        self.assertTrue(any("no valid listening task" in error for error in errors))
        self.assertTrue(any("unsafe" in error for error in errors))

    def test_catalog_requires_regular_root_directories(self):
        self.write("listening-tasks", "{}")
        self.assertTrue(any("regular directory" in error for error in self.errors()))

    def test_validator_main_integrates_task_catalog(self):
        document = example()
        document["policyVersion"] = 2
        self.write(f"listening-tasks/{document['id']}.json", json.dumps(document))
        with patch.object(validate, "ROOT", self.root), patch.object(validate, "errors", []), \
                patch("sys.stdout", new_callable=io.StringIO) as output:
            self.assertEqual(1, validate.main())
        self.assertIn("unsupported listening task policyVersion", output.getvalue())

    def test_mixed_manifest_keeps_old_reader_wanted_maps_unchanged(self):
        for name, data in (("words/example.md", "legacy\r\nword"), ("listening/legacy.json", "{}"),
                           ("audio/legacy.ogg", b"legacy\r\naudio"), ("images/legacy.webp", b"image"),
                           ("curriculum/grammar.json", "{}")):
            self.write(name, data)
        before = build_manifest.build_manifest(self.root)
        for name, data in (("listening-tasks/example.json", '{"text":"日本語"}\r\n'),
                           ("task-audio/short.ogg", b"short\r\naudio"),
                           ("task-images/scene.webp", b"picture\r\n")):
            self.write(name, data)
        mixed = build_manifest.build_manifest(self.root)
        for key in ("files", "listening", "audio", "images", "curriculum"):
            self.assertEqual(before[key], mixed[key])
        self.assertEqual(1, mixed["schemaVersion"])
        self.assertNotEqual(before["contentVersion"], mixed["contentVersion"])
        for key, path, normalized in (
            ("listeningTasks", "listening-tasks/example.json", True),
            ("listeningTaskAudio", "task-audio/short.ogg", False),
            ("listeningTaskImages", "task-images/scene.webp", False),
        ):
            raw = (self.root / path).read_bytes()
            self.assertEqual({path: hashlib.sha256(raw.replace(b"\r\n", b"\n") if normalized else raw).hexdigest()},
                             mixed[key])
            self.write(path, raw.replace(b"\r\n", b"\n"))
            changed = build_manifest.build_manifest(self.root)
            self.assertEqual(normalized, changed["contentVersion"] == mixed["contentVersion"])
            self.write(path, raw)
        for folder in ("listening-tasks", "task-audio", "task-images"):
            for path in (self.root / folder).iterdir():
                path.unlink()
        self.assertEqual(before, build_manifest.build_manifest(self.root))

    def test_whole_tree_budget_counts_curriculum_and_all_new_folders(self):
        names = ["curriculum/grammar.json", "listening-tasks/example.json", "task-audio/short.ogg",
                 "task-images/scene.webp", "docs/ignored.txt"]
        for name in names:
            self.write(name, b"12345")
        result = budget.check(self.root, names + ["task-audio/short.ogg"])
        self.assertEqual(20, result["retainedBytes"])
        self.assertEqual(25, result["inflatedBytes"])
        self.assertEqual(10, result["listeningTaskMediaBytes"])
        self.assertEqual(11, result["entries"])
        for name, limit in ((names[0], 2 * 1024 * 1024), (names[1], 2 * 1024 * 1024),
                            (names[2], 512 * 1024), (names[3], 150 * 1024)):
            self.write(name, b"x" * (limit + 1))
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, "per-file"):
                budget.check(self.root, [name])
            self.write(name, b"12345")
        for constant, limit, message in (("MAX_RETAINED", 19, "retained/inflated"),
                                         ("MAX_INFLATED", 24, "retained/inflated"),
                                         ("MAX_ENTRIES", 10, "entry"),
                                         ("MAX_COMPRESSED", result["localZipBytes"] - 1, "compressed"),
                                         ("MAX_TASK_MEDIA", 9, "6 MiB")):
            with self.subTest(guard=constant), patch.object(budget, constant, limit), self.assertRaisesRegex(ValueError, message):
                budget.check(self.root, names)

    def test_combined_new_media_budget_counts_files_once_not_references(self):
        document = self.media_document()
        document["media"]["audio"]["repeat"] = copy.deepcopy(document["media"]["audio"]["focus"])
        (self.root / "task-audio" / "repeat.ogg").unlink()
        self.write(f"listening-tasks/{document['id']}.json", json.dumps(document))
        total = sum(path.stat().st_size for path in (self.root / "task-audio").glob("*.ogg"))
        with patch.object(tasks, "MAX_MEDIA_BYTES", total):
            self.assertEqual([], self.errors())
        with patch.object(tasks, "MAX_MEDIA_BYTES", total - 1):
            self.assertTrue(any("6 MiB" in error for error in self.errors()))


class SharedOpusTests(unittest.TestCase):
    def test_new_short_and_long_bounds_preserve_legacy_defaults(self):
        for duration in (250, 1000, 15000, 60000, 90000):
            data = opus(duration)
            with self.subTest(duration=duration):
                self.assertEqual(duration, legacy.opus_duration_ms(data, 250, 90000))
                if 15000 <= duration <= 60000:
                    self.assertEqual(duration, legacy.opus_duration_ms(data))
                else:
                    with self.assertRaises(ValueError):
                        legacy.opus_duration_ms(data)
        for duration in (249, 90001):
            with self.subTest(duration=duration), self.assertRaises(ValueError):
                legacy.opus_duration_ms(opus(duration), 250, 90000)

    def test_framing_crc_sequence_channels_and_trailing_bytes(self):
        data = opus(1000)
        crc_broken = bytearray(data)
        crc_broken[-1] ^= 1
        bad_sequence = data[:47] + ogg_page([b"OpusTags" + bytes(8)], 7, 0, 0) + data[91:]
        for malformed in (b"", data[:-1], data + b"x", bytes(crc_broken), opus(1000, channels=2), bad_sequence):
            with self.subTest(length=len(malformed)), self.assertRaises(ValueError):
                legacy.opus_duration_ms(malformed, 250, 90000)

    def test_existing_approved_legacy_passages_still_validate(self):
        paths = sorted((REPO / "listening").glob("*.json"))
        self.assertTrue(paths)
        for path in paths:
            document = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(path=path.name):
                self.assertTrue(legacy.validate_document(document, path.relative_to(REPO).as_posix(), REPO))


if __name__ == "__main__":
    unittest.main()
