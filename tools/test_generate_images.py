"""Paid-request recovery, immutable approved assets and reviewed catalog publication."""
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

from PIL import Image

import generate_images as gen


def png(size=(32, 32)):
    out = io.BytesIO()
    Image.new("RGB", size, (180, 80, 40)).save(out, "PNG")
    return out.getvalue()


class GenerateSceneTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.artifacts = self.root / "artifacts"
        (self.root / "words").mkdir()
        self.card = self.root / "words" / "a.md"
        self.card.write_bytes(b"---\nword: a\n---\nA reviewed card.\n")
        self.scene = {"id": "warmth", "sense": "Warmth", "image": "images/a.webp",
                      "description": "A warm scene.", "quizEligible": True, "prompt": "A sunlit cat."}
        self.entry = {"articleSha256": gen.digest(self.card.read_bytes()), "scenes": [self.scene]}
        self.plan = self.root / "plan.json"

    def write_plan(self):
        gen.write_json(self.plan, {"schemaVersion": 1, "words": {"a": self.entry}})

    def generate(self):
        gen.generate_scene("a", self.entry, self.scene, "Shared style.", self.artifacts, self.root)

    def test_conversion_rejects_invalid_input_before_a_runtime_asset_is_written(self):
        with patch.object(gen, "token", return_value="fixture"), patch.object(gen, "generate", return_value=png((32, 16))):
            with self.assertRaisesRegex(ValueError, "square PNG"):
                self.generate()
        self.assertFalse((self.root / "images" / "a.webp").exists())
        self.assertTrue((self.artifacts / "a.png").exists())
        self.assertEqual("downloaded", json.loads((self.artifacts / "a.json").read_text())["status"])

    def test_completed_and_interrupted_outputs_resume_without_another_paid_request(self):
        with patch.object(gen, "token", return_value="fixture"), patch.object(gen, "generate", return_value=png()) as api:
            self.generate()
            target = self.root / "images" / "a.webp"
            original = target.read_bytes()
            self.generate()
            receipt_path = self.artifacts / "a.json"
            receipt = json.loads(receipt_path.read_text())
            receipt["status"] = "downloaded"
            gen.write_json(receipt_path, receipt)
            self.generate()
            self.assertEqual("complete", json.loads(receipt_path.read_text())["status"])
            target.unlink()
            self.generate()
            self.assertEqual(1, api.call_count)
            self.assertEqual(original, target.read_bytes())
        target.write_bytes(b"unexpected replacement")
        with self.assertRaisesRegex(ValueError, "refusing regeneration"):
            self.generate()
        self.assertEqual(b"unexpected replacement", target.read_bytes())

    def test_uncertain_requests_and_unattributed_originals_are_not_blindly_regenerated(self):
        with patch.object(gen, "token", return_value="fixture"), patch.object(gen, "generate", side_effect=gen.GenerationFailure("Timeout")) as api:
            with self.assertRaises(gen.GenerationFailure):
                self.generate()
            with self.assertRaisesRegex(ValueError, "may have been billed"):
                self.generate()
            self.assertEqual(1, api.call_count)
        (self.artifacts / "a.json").unlink()
        (self.artifacts / "a.png").write_bytes(png())
        with self.assertRaisesRegex(ValueError, "no request receipt"):
            self.generate()

    def test_review_is_hash_pinned_and_applying_a_catalog_never_rewrites_the_word(self):
        original = self.card.read_bytes()
        with patch.object(gen, "token", return_value="fixture"), patch.object(gen, "generate", return_value=png()):
            self.generate()
        with self.assertRaisesRegex(ValueError, "visual review"):
            gen.apply_catalogs({"a": self.entry}, self.artifacts, self.root)
        self.assertFalse((self.root / "scenes").exists())
        image_hash = gen.digest((self.root / "images" / "a.webp").read_bytes())
        self.scene["advisoryReview"] = {"verdict": "ARTICLE_ONLY", "imageSha256": image_hash, "note": "Fixture review"}
        with self.assertRaisesRegex(ValueError, "cannot enable quizzes"):
            gen.apply_catalogs({"a": self.entry}, self.artifacts, self.root)
        self.scene["quizEligible"] = False
        gen.apply_catalogs({"a": self.entry}, self.artifacts, self.root)
        catalog = json.loads((self.root / "scenes" / "a.json").read_text())
        self.assertFalse(catalog["scenes"][0]["quizEligible"])
        self.assertNotIn("prompt", catalog["scenes"][0])
        self.assertEqual(original, self.card.read_bytes())
        self.write_plan()
        gen.read_plan(self.plan, self.root)

    def test_preflight_detects_stale_article_and_changed_approved_bytes(self):
        image = self.root / "images" / "a.webp"
        gen.write_atomic(image, gen.to_webp(png()))
        self.scene["existingSha256"] = gen.digest(image.read_bytes())
        self.write_plan()
        gen.read_plan(self.plan, self.root)
        image.write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "approved bytes changed"):
            gen.read_plan(self.plan, self.root)
        self.card.write_bytes(b"changed article")
        with self.assertRaisesRegex(ValueError, "card changed"):
            gen.read_plan(self.plan, self.root)

    def test_only_confirmed_rate_limits_are_automatically_retried(self):
        limited = urllib.error.HTTPError(gen.URL, 429, "Limited", {"Retry-After": "0"}, io.BytesIO())
        with patch.object(gen.urllib.request, "urlopen", side_effect=limited) as api, patch.object(gen.time, "sleep"):
            with self.assertRaises(gen.GenerationFailure) as failure:
                gen.generate("Prompt", {"Authorization": "fixture"})
            self.assertTrue(failure.exception.retry_safe)
            self.assertEqual(6, api.call_count)
        unavailable = urllib.error.HTTPError(gen.URL, 503, "Unavailable", {}, io.BytesIO())
        with patch.object(gen.urllib.request, "urlopen", side_effect=unavailable) as api:
            with self.assertRaises(gen.GenerationFailure) as failure:
                gen.generate("Prompt", {"Authorization": "fixture"})
            self.assertFalse(failure.exception.retry_safe)
            self.assertEqual(1, api.call_count)

    def test_rejection_keeps_bounded_provider_details_for_diagnosis(self):
        rejected = urllib.error.HTTPError(gen.URL, 400, "Rejected", {"apim-request-id": "fixture-id"},
                                         io.BytesIO(b'{"error":{"code":"fixture_rejection","message":"Reason"}}'))
        with patch.object(gen.urllib.request, "urlopen", side_effect=rejected):
            with self.assertRaisesRegex(gen.GenerationFailure, "fixture_rejection") as failure:
                gen.generate("Prompt", {"Authorization": "fixture"})
            self.assertIn("fixture-id", str(failure.exception))
            self.assertTrue(failure.exception.retry_safe)

    def test_authentication_refresh_uses_expiry_and_the_explicit_subscription(self):
        self.addCleanup(setattr, gen, "SUBSCRIPTION", gen.SUBSCRIPTION)
        gen.SUBSCRIPTION = "fixture-subscription"
        old_token, old_expiry = gen._access_token, gen._expires_at
        self.addCleanup(setattr, gen, "_access_token", old_token)
        self.addCleanup(setattr, gen, "_expires_at", old_expiry)
        gen._access_token, gen._expires_at = "almost-expired", 1100
        response = json.dumps({"accessToken": "refreshed", "expires_on": 5000})
        with patch.object(gen.time, "time", return_value=1000), patch.object(gen.subprocess, "check_output", return_value=response) as cli:
            self.assertEqual("refreshed", gen.token())
            self.assertEqual("refreshed", gen.token())
            self.assertEqual(1, cli.call_count)
            self.assertIn("--subscription", cli.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
