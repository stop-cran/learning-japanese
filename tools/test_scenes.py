"""Scene catalogs, unique ownership, and backward-compatible manifest versions."""
import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_manifest
import validate
from validate_scenes import check_scenes, read_catalog


class SceneTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ("words", "images", "scenes"):
            (self.root / folder).mkdir()
        root_patch = patch.object(validate, "ROOT", self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        errors_patch = patch.object(validate, "errors", [])
        errors_patch.start()
        self.addCleanup(errors_patch.stop)
        self.path = self.root / "scenes" / "a.json"
        self.data = {
            "schemaVersion": 1, "word": "a",
            "scenes": [
                {"id": "warmth", "sense": "Warmth", "image": "images/a.webp", "description": "A scene", "quizEligible": True},
                {"id": "diagram", "sense": "Diagram", "image": "images/b.webp", "description": "Labels", "quizEligible": False},
            ],
        }
        self.words = {"a": {"image": "images/a.webp", "image_scene": "A scene"}}
        for name in ("a", "b"):
            (self.root / "images" / f"{name}.webp").write_bytes(b"RIFF\x08\x00\x00\x00WEBP" + name.encode() * 4)

    def write(self, data=None):
        self.path.write_text(json.dumps(self.data if data is None else data), encoding="utf-8")

    def check(self):
        references = check_scenes(validate.err, self.root, self.words, validate.check_image_file)
        legacy = {word: data["image"] for word, data in self.words.items() if "image" in data}
        validate.check_images(legacy, references)
        return references

    def test_legacy_and_catalog_share_owner_and_article_only_assets_are_not_orphans(self):
        self.write()
        self.assertEqual({"a": ["images/a.webp", "images/b.webp"]}, self.check())
        self.assertEqual([], validate.errors)
        self.words["a"] = {}
        self.data["scenes"][0]["quizEligible"] = False
        self.write()
        self.check()
        self.assertEqual([], validate.errors)

    def test_bad_or_ineligible_legacy_fallback_is_rejected(self):
        for change in ({"quizEligible": False}, {"description": "Changed"}, {"image": "images/c.webp"}):
            with self.subTest(change=change):
                data = copy.deepcopy(self.data)
                data["scenes"][0].update(change)
                self.write(data)
                validate.errors.clear()
                self.check()
                self.assertTrue(any("legacy image must match" in error for error in validate.errors), validate.errors)

    def test_strict_fields_and_unique_scene_identity(self):
        cases = [
            {"quizEligible": value} for value in ("true", None, 1, [], {})
        ] + [{"id": "diagram"}, {"image": "images/b.webp"}, {"id": "bad id"}, {"sense": " "},
             {"image": "images/sub/a.webp"}, {"description": 3}]
        for change in cases:
            with self.subTest(change=change):
                data = copy.deepcopy(self.data)
                data["scenes"][0].update(change)
                self.write(data)
                with self.assertRaises(ValueError):
                    read_catalog(self.path)
        data = copy.deepcopy(self.data)
        del data["scenes"][0]["quizEligible"]
        self.write(data)
        with self.assertRaisesRegex(ValueError, "explicit boolean"):
            read_catalog(self.path)

    def test_missing_word_asset_and_cross_word_ownership_are_reported(self):
        self.write()
        self.words.clear()
        self.check()
        self.assertTrue(any("word 'a' is missing" in error for error in validate.errors))
        self.words = {"a": {}, "b": {"image": "images/a.webp"}}
        validate.errors.clear()
        (self.root / "images" / "b.webp").unlink()
        self.check()
        self.assertTrue(any("does not exist" in error for error in validate.errors))
        self.assertTrue(any("also used by" in error for error in validate.errors))

    def test_separate_text_hash_map_changes_version_only_when_scene_content_changes(self):
        (self.root / "words" / "a.md").write_bytes(b"word\r\n")
        before = build_manifest.build_manifest(self.root)
        old_payload = {"files": before["files"], "images": before["images"]}
        old_version = hashlib.sha256(json.dumps(old_payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
        self.assertEqual(old_version, before["contentVersion"])
        self.assertNotIn("scenes", before)
        self.write()
        added = build_manifest.build_manifest(self.root)
        self.assertNotIn("scenes/a.json", added["files"])
        self.assertEqual(build_manifest.sha256(self.path), added["scenes"]["scenes/a.json"])
        self.assertNotEqual(before["contentVersion"], added["contentVersion"])
        self.data["scenes"][1]["quizEligible"] = True
        self.write()
        changed = build_manifest.build_manifest(self.root)
        self.assertEqual(added["files"], changed["files"])
        self.assertEqual(added["images"], changed["images"])
        self.assertNotEqual(added["contentVersion"], changed["contentVersion"])
        self.path.write_bytes(self.path.read_bytes() + b"\r\n")
        crlf = build_manifest.build_manifest(self.root)
        self.path.write_bytes(self.path.read_bytes().replace(b"\r\n", b"\n"))
        self.assertEqual(crlf, build_manifest.build_manifest(self.root))


if __name__ == "__main__":
    unittest.main()
