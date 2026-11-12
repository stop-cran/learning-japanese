import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import build_manifest
from validate_reading import load_package, validate_document, word_ids

ROOT = Path(__file__).resolve().parent.parent


def fixture():
    return {
        "schemaVersion": 1,
        "id": "reading-fixture-peach",
        "jlpt": 5,
        "title": "A small peach",
        "japaneseTitle": "小さい桃",
        "levelRationale": "Parser fixture only. Not the Momotaro pilot.",
        "provenance": {
            "originalTitle": "小さい桃",
            "adaptation": {"label": "Original example", "basis": "original"},
            "credits": ["Parser fixture only."],
            "rights": {"status": "original-wording", "note": "Original fixture wording."},
            "distribution": {"reviewed": [], "note": "No jurisdiction has been reviewed."},
        },
        "sections": [{
            "id": "river",
            "text": "小さい桃があります。",
            "vocabulary": [{
                "start": 3, "end": 4, "text": "桃", "reading": "もも",
                "headword": "桃", "gloss": "peach", "word": "桃",
            }],
        }],
        "questions": [{
            "id": "where",
            "tier": 1,
            "prompt": "Where is the peach?",
            "options": [{"id": "house", "text": "At a house"}, {"id": "mountain", "text": "On a mountain"}],
            "correctOptionId": "house",
            "explanation": "The fixture does not state a place.",
            "evidence": [{"sectionId": "river", "start": 0, "end": 2}],
        }],
    }


class ReadingTests(unittest.TestCase):
    def test_pilot_matches_the_authoring_band(self):
        path = ROOT / "reading" / "momotaro-n5.json"
        document = load_package(path)
        validate_document(document, "reading/momotaro-n5.json", known_words=word_ids(ROOT), literary=True)
        self.assertEqual(sum(len(section["text"]) for section in document["sections"]), 575)
        self.assertEqual(document["provenance"]["distribution"]["reviewed"], [])

    def test_schema_accepts_a_short_fixture_and_rejects_bad_packages(self):
        validate_document(fixture(), "reading/reading-fixture-peach.json", known_words={"桃"})
        mutations = [
            lambda d: d.update(extra=True),
            lambda d: d["sections"][0].update(translation=None),
            lambda d: d["sections"][0]["vocabulary"][0].update(end=3),
            lambda d: d["sections"][0]["vocabulary"][0].update(word="missing-card"),
            lambda d: d["provenance"].update(consulted=[{
                "originalTitle": "桃太郎", "author": "Author", "edition": "Edition",
                "sourceUrl": "https://example.test/card", "accessed": "2026-11-12", "role": "wording-source",
            }]),
            lambda d: d["questions"][0].update(correctOptionId="missing"),
            lambda d: d["questions"][0].update(prompt="She says 「ない文」."),
        ]
        for mutation in mutations:
            data = fixture()
            mutation(data)
            with self.assertRaises(ValueError):
                validate_document(data, "reading/reading-fixture-peach.json", known_words={"桃"})
        short = fixture()
        with self.assertRaises(ValueError):
            validate_document(short, "reading/reading-fixture-peach.json", literary=True)

    def test_default_manifest_does_not_publish_reading(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "reading").mkdir()
            (root / "reading-images").mkdir()
            before = build_manifest.build_manifest(root)
            (root / "reading" / "example.json").write_bytes("{\"id\": \"example\"}\r\n".encode("utf-8"))
            image = root / "reading-images" / "example.webp"
            image.write_bytes(b"webp\r\n")
            after = build_manifest.build_manifest(root)
            self.assertNotIn("reading", after)
            self.assertNotIn("readingImages", after)
            self.assertEqual(before["contentVersion"], after["contentVersion"])
            published = build_manifest.build_manifest(root, publish_reading=True)
            self.assertEqual(published["reading"]["reading/example.json"], hashlib.sha256(b"{\"id\": \"example\"}\n").hexdigest())
            self.assertEqual(published["readingImages"]["reading-images/example.webp"], hashlib.sha256(b"webp\r\n").hexdigest())
            self.assertNotEqual(published["contentVersion"], before["contentVersion"])


if __name__ == "__main__":
    unittest.main()
