"""Offline accounting/protocol tests; synthetic declarations are never real approval."""
import copy
from datetime import date
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
from xml.sax.saxutils import escape

import requests

import listening_task_budget as budget
import render_listening_tasks as renderer
import validate_listening_tasks as tasks
from test_listening_tasks import example, image_bytes, ogg_page, opus


class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.raw = Mock()
        self.raw.post.return_value.status_code = 200
        self.endpoint = "https://fixture.cognitiveservices.azure.com/tts/cognitiveservices/v1"

    def session(self, phase="preview"):
        return budget.BudgetSession(self.raw, self.root, self.endpoint, "fixture-plan", phase, lambda: None)

    def test_failed_attempts_retries_and_restarts_share_exact_ceiling(self):
        body = "<speak>一</speak>"
        units = 2 * len(body)
        budget.authorize(self.root, "fixture-plan", "complete", 2 * units, "1", "15", "Synthetic test only")
        self.raw.post.side_effect = [OSError("connection lost after send"), Mock(status_code=200)]
        with budget.run_lock(self.root):
            with self.assertRaisesRegex(OSError, "connection lost"):
                self.session().post(self.endpoint, data=body.encode("utf-8"))
            self.session("complete").post(self.endpoint, data=body)
            with self.assertRaisesRegex(ValueError, "ceiling"):
                self.session().post(self.endpoint, data=body)
        self.assertEqual(2, self.raw.post.call_count)
        self.assertEqual([units, units], [attempt["units"] for attempt in budget.read_json(self.root / "spend.json")["attempts"]])

    def test_money_ceiling_and_scope_are_enforced_before_post(self):
        budget.authorize(self.root, "fixture-plan", "preview", 10000, "0.0001", "15", "Synthetic test only")
        with self.assertRaisesRegex(ValueError, "Only previews"):
            self.session("complete")
        with budget.run_lock(self.root), self.assertRaisesRegex(ValueError, "ceiling"):
            self.session().post(self.endpoint, data="<speak>test</speak>")
        self.raw.post.assert_not_called()

    def test_deferred_audition_requires_complete_authorization(self):
        with self.assertRaisesRegex(ValueError, "complete private-generation"):
            budget.authorize(self.root, "fixture-plan", "preview", 10000, "1", "15",
                             "Synthetic fixture", defer_preview_approval=True)
        self.assertFalse((self.root / "authorization.json").exists())

    def test_missing_or_rewritten_accounting_cannot_reset_a_run(self):
        budget.authorize(self.root, "fixture-plan", "complete", 10000, "1", "15", "Synthetic test only")
        with self.assertRaisesRegex(ValueError, "already exists"):
            budget.authorize(self.root, "fixture-plan", "complete", 20000, "2", "15", "Not a renewal")
        auth = budget.read_json(self.root / "authorization.json")
        auth["maxRequestUnits"] += 1
        budget.write_json(self.root / "authorization.json", auth)
        with self.assertRaisesRegex(ValueError, "Authorization changed"):
            self.session()
        (self.root / "spend.json").unlink()
        with self.assertRaises(FileNotFoundError):
            self.session()
        self.raw.post.assert_not_called()

    def test_concurrent_run_and_wrong_endpoint_are_rejected(self):
        budget.authorize(self.root, "fixture-plan", "complete", 10000, "1", "15", "Synthetic test only")
        with budget.run_lock(self.root):
            with self.assertRaisesRegex(ValueError, "locked"), budget.run_lock(self.root):
                self.fail("Second writer entered")
            with self.assertRaisesRegex(ValueError, "planned TTS endpoint"):
                self.session().post("https://other.invalid", data="test")
        self.assertFalse((self.root / "operation.lock").exists())
        self.raw.post.assert_not_called()

    def test_requests_redirects_cannot_replay_an_authenticated_post_outside_accounting(self):
        body = "<speak>一</speak>"
        units = 2 * len(body)
        for code in (307, 308):
            with self.subTest(status=code), requests.Session() as raw:
                raw.trust_env = False
                root = self.root / str(code)
                root.mkdir()
                budget.authorize(root, "fixture-plan", "complete", units, "1", "15", "Synthetic transport only")
                attempts = []

                def transport(request, **kwargs):
                    attempts.append(request)
                    response = requests.Response()
                    response.status_code = code if len(attempts) == 1 else 200
                    response.headers["Location"] = self.endpoint + "/redirect"
                    response._content = b""
                    response.request = request
                    return response

                session = budget.BudgetSession(raw, root, self.endpoint, "fixture-plan", "preview", lambda: None)
                with budget.run_lock(root), patch.object(requests.adapters.HTTPAdapter, "send", side_effect=transport) as send:
                    with self.assertRaisesRegex(ValueError, "redirect blocked"):
                        session.post(self.endpoint, data=body.encode("utf-8"),
                                     headers={"Authorization": "Bearer synthetic-test-token"}, allow_redirects=True)
                self.assertEqual(1, send.call_count)
                self.assertEqual([units], [item["units"] for item in budget.read_json(root / "spend.json")["attempts"]])


class FakeEngine:
    SAMPLE_RATE, SAMPLE_WIDTH = 24000, 2

    def __init__(self):
        self.cache = {}
        self.login = Mock(return_value=lambda: "synthetic-token-not-used")

    def pipeline_hash(self):
        return "synthetic-offline-engine"

    def resolve_endpoint(self, resource):
        return f"https://{resource}.cognitiveservices.azure.com/tts/cognitiveservices/v1"

    def make_token_provider(self, **kwargs):
        return self.login(**kwargs)

    def _silence(self, milliseconds):
        return bytes(milliseconds * 48)

    def _wrap_wav(self, pcm):
        return pcm

    def cached_pcm(self, text, token, session, voice, rate, directory, force):
        key = (text, voice, rate)
        if key not in self.cache:
            session.post(self.ENDPOINT, data=f'<speak><voice name="{voice}">{escape(text)}</voice></speak>'.encode())
            self.cache[key] = bytes(4800)
        return self.cache[key]


def fake_ffmpeg(engine, arguments, data=None):
    if data is not None:
        Path(arguments[-1]).write_bytes(opus(round(len(data) / 48)))
        return b""
    path = Path(arguments[arguments.index("-i") + 1])
    return bytes(tasks.opus_duration_ms(path.read_bytes(), 250, 90000) * 48)


class RendererTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.content, self.run = self.base / "content", self.base / "private-run"
        self.content.mkdir()
        (self.content / "words").mkdir()
        (self.content / "words" / "fixture.md").write_text("Synthetic word fixture", encoding="utf-8")
        self.engine, self.raw = FakeEngine(), Mock()
        self.raw.post.return_value.status_code = 200
        self.sources, self.images, self.previews = [], {}, []
        profiles = set()
        for kind in tasks.STAGE_ROLES:
            document = example(kind)
            document["vocabulary"] = [{"surface": "test", "reading": "test", "gloss": "fixture", "word": "fixture"}]
            source = self.content / f"{document['id']}.json"
            budget.write_json(source, document)
            self.sources.append(source)
            speakers = {speaker["id"]: speaker for speaker in document["speakers"]}
            for turn in document["turns"]:
                speaker = speakers[turn["speaker"]]
                profile = (speaker["voice"], speaker["ratePercent"])
                if profile not in profiles:
                    profiles.add(profile)
                    self.previews.append(f"{document['id']}:{turn['id']}")
            if "visual" in document:
                path = self.base / f"{document['id']}.webp"
                path.write_bytes(image_bytes())
                self.images[document["id"]] = path
        self.patch = patch.object(renderer, "ffmpeg", side_effect=fake_ffmpeg)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.create_plan()

    def create_plan(self):
        renderer.create_plan(self.run, self.content, self.sources, self.images, self.previews,
                             self.engine, "fixture", "synthetic-subscription")

    def authorize(self, scope="complete"):
        plan = renderer.load_plan(self.run, self.engine)
        budget.authorize(self.run, tasks.canonical_hash(plan), scope, 100000, "10", "15", "Synthetic fixture; no HTTP service")

    def render(self, phase):
        renderer.render(self.run, self.engine, "fixture", "synthetic-subscription", phase, self.raw)

    def complete(self):
        self.authorize()
        self.render("preview")
        renderer.approve_preview(self.run, self.engine, "Synthetic fixture declaration, not real listening", date.today().isoformat())
        self.render("complete")

    def test_no_authorization_or_preview_acceptance_means_no_login_or_complete_render(self):
        with self.assertRaises(FileNotFoundError):
            self.render("preview")
        self.engine.login.assert_not_called()
        self.authorize()
        with self.assertRaises(FileNotFoundError):
            self.render("complete")
        self.engine.login.assert_not_called()
        with self.assertRaisesRegex(ValueError, "Resource/subscription"):
            renderer.render(self.run, self.engine, "other", "synthetic-subscription", "preview", self.raw)
        self.raw.post.assert_not_called()

    def test_all_four_protocols_repeat_reuse_and_no_implicit_output_approval(self):
        self.complete()
        plan = renderer.load_plan(self.run, self.engine)
        for entry in plan["tasks"]:
            with self.subTest(task=entry["document"]["taskType"]):
                document = renderer.verified_package(self.run, plan, entry["document"]["id"], self.engine)
                self.assertFalse(renderer.validate_output(document, self.run, plan))
                self.assertNotIn("approval", document)
                stages = document["stages"]
                for stage in stages:
                    self.assertEqual(stage["turns"], [turn["id"] for turn in document["media"]["audio"][stage["id"]]["turns"]])
                if document["taskType"] in ("task-based", "key-point"):
                    self.assertEqual(document["media"]["audio"][stages[1]["id"]], document["media"]["audio"][stages[3]["id"]])
                with self.assertRaisesRegex(ValueError, "missing word article"):
                    tasks.validate_document(document, renderer.logical_path(document), self.run)
        before = self.raw.post.call_count
        self.render("complete")
        self.assertEqual(before, self.raw.post.call_count)
        self.assertIn("not C/D native playback", (self.run / "complete-review.html").read_text(encoding="utf-8"))

    def test_n4_schema_survives_frozen_render_and_explicitly_approved_export(self):
        self.run = self.base / "n4-private-run"
        sources = []
        for source in self.sources:
            document = budget.read_json(source)
            identifier = document["id"].replace("n5-", "n4-", 1)
            document.update(id=identifier, exposureId=identifier, schemaVersion=2, jlpt=4,
                            blueprint="n4-section-v1")
            target = self.content / f"{identifier}.json"
            budget.write_json(target, document)
            sources.append(target)
        self.sources = sources
        self.images = {key.replace("n5-", "n4-", 1): value for key, value in self.images.items()}
        self.previews = [value.replace("n5-", "n4-", 1) for value in self.previews]
        self.create_plan()
        self.complete()
        for source in self.sources:
            identifier = source.stem
            with self.assertRaises(FileNotFoundError):
                renderer.export(self.run, self.engine, [identifier])
            renderer.approve_task(self.run, self.engine, identifier, "Synthetic N4 schema fixture; no actual media acceptance",
                                  date.today().isoformat(), listened=True, visual=True, native=True, phone=True)
        renderer.export(self.run, self.engine, [source.stem for source in self.sources])
        for source in self.sources:
            published = budget.read_json(self.content / "listening-tasks" / source.name)
            self.assertEqual((2, 4, "n4-section-v1"),
                             (published["schemaVersion"], published["jlpt"], published["blueprint"]))
            self.assertTrue(tasks.validate_document(published, renderer.logical_path(published), self.content))

    def test_explicit_deferred_audition_generates_private_outputs_but_cannot_approve_or_export(self):
        plan = renderer.load_plan(self.run, self.engine)
        budget.authorize(self.run, tasks.canonical_hash(plan), "complete", 100000, "10", "15",
                         "Synthetic explicit full-generation authorization", defer_preview_approval=True)
        with self.assertRaises(FileNotFoundError):
            self.render("complete")
        self.engine.login.assert_not_called()
        self.render("preview")
        self.render("complete")
        self.assertFalse((self.run / "preview-approval.json").exists())
        for entry in plan["tasks"]:
            identifier = entry["document"]["id"]
            document = renderer.verified_package(self.run, plan, identifier, self.engine)
            self.assertNotIn("approval", document)
            with self.assertRaises(FileNotFoundError):
                renderer.approve_task(self.run, self.engine, identifier, "Not real approval", date.today().isoformat(),
                                      listened=True, visual=True, native=True, phone=True)
            with self.assertRaises(FileNotFoundError):
                renderer.export(self.run, self.engine, [identifier])
        self.assertFalse((self.content / "listening-tasks").exists())

    def test_task_occurrence_limit_counts_repeated_focus(self):
        self.authorize()
        with patch.object(self.engine, "cached_pcm", return_value=bytes(40_000 * 48)):
            self.render("preview")
            renderer.approve_preview(self.run, self.engine, "Synthetic timing fixture only", date.today().isoformat())
            with self.assertRaisesRegex(ValueError, "total stage occurrence duration"):
                self.render("complete")
        self.assertFalse((self.run / "packages" / f"{self.sources[0].stem}.json").exists())

    def test_changed_source_picture_and_plan_stop_before_any_further_request(self):
        self.authorize()
        document = budget.read_json(self.sources[0])
        document["options"][0]["rationale"] += " Changed."
        budget.write_json(self.sources[0], document)
        with self.assertRaisesRegex(ValueError, "Frozen learning package"):
            self.render("preview")
        self.raw.post.assert_not_called()
        plan = budget.read_json(self.run / "plan.json")
        original_hash = tasks.canonical_hash(plan)
        plan["tasks"][0]["document"] = document
        plan["tasks"][0]["contentSha256"] = tasks.content_hash(document)
        budget.write_json(self.run / "plan.json", plan)
        with self.assertRaisesRegex(ValueError, "plan changed"):
            renderer.require_same_plan(self.run, self.engine, original_hash)
        next(iter(self.images.values())).write_bytes(image_bytes(3, 3))
        with self.assertRaisesRegex(ValueError, "Frozen picture"):
            renderer.load_plan(self.run, self.engine)

    def test_corrupt_audio_and_changed_numbering_invalidate_the_output(self):
        self.complete()
        plan = renderer.load_plan(self.run, self.engine)
        entry = plan["tasks"][-1]
        identifier = entry["document"]["id"]
        output_path = self.run / "packages" / f"{identifier}.json"
        document = budget.read_json(output_path)
        modified = copy.deepcopy(document)
        modified["options"][0]["label"] = "Changed choice"
        budget.write_json(output_path, modified)
        with self.assertRaisesRegex(ValueError, "learning package changed"):
            renderer.verified_package(self.run, plan, identifier, self.engine)
        budget.write_json(output_path, document)
        clip = next(iter(document["media"]["audio"].values()))
        (self.run / clip["path"]).write_bytes(opus(2000))
        with self.assertRaisesRegex(ValueError, "audio hash changed"):
            renderer.verified_package(self.run, plan, identifier, self.engine)

    def test_export_requires_all_actual_declarations_and_preserves_immutable_approval(self):
        self.complete()
        identifier = budget.read_json(self.sources[0])["id"]
        with self.assertRaises(FileNotFoundError):
            renderer.export(self.run, self.engine, [identifier])
        with self.assertRaisesRegex(ValueError, "physical-phone"):
            renderer.approve_task(self.run, self.engine, identifier, "Synthetic fixture", date.today().isoformat(),
                                  listened=True, visual=True, native=True, phone=False)
        renderer.approve_task(self.run, self.engine, identifier, "Synthetic fixture; NOT actual listener approval",
                              date.today().isoformat(), listened=True, visual=True, native=True, phone=True)
        original = budget.read_json(self.run / "packages" / f"{identifier}.json")
        self.render("complete")
        self.assertEqual(original, budget.read_json(self.run / "packages" / f"{identifier}.json"))
        renderer.export(self.run, self.engine, [identifier])
        published = budget.read_json(self.content / "listening-tasks" / f"{identifier}.json")
        self.assertEqual(original, published)
        self.assertTrue(tasks.validate_document(published, renderer.logical_path(published), self.content))
        published["exposureId"] = "different-story"
        budget.write_json(self.content / "listening-tasks" / f"{identifier}.json", published)
        with self.assertRaisesRegex(ValueError, "never rebind"):
            renderer.export(self.run, self.engine, [identifier], replace=True)

    def test_fresh_reviewed_revision_exports_reencoded_speech_without_overwriting_old_assets(self):
        self.complete()
        identifier = self.sources[0].stem
        renderer.approve_task(self.run, self.engine, identifier, "Synthetic fixture, not listener approval",
                              date.today().isoformat(), listened=True, visual=True, native=True, phone=True)
        renderer.export(self.run, self.engine, [identifier])
        published = budget.read_json(self.content / "listening-tasks" / f"{identifier}.json")
        old_assets = {clip["path"]: (self.content / clip["path"]).read_bytes() for clip in published["media"]["audio"].values()}
        draft = budget.read_json(self.sources[0])
        draft["options"][0]["rationale"] += " Revised feedback."
        budget.write_json(self.sources[0], draft)
        self.run = self.base / "revised-run"

        def reencoded(engine, arguments, data=None):
            result = fake_ffmpeg(engine, arguments, data)
            if data is not None:
                path = Path(arguments[-1])
                vendor = b"different-encoder-run"
                old = ogg_page([b"OpusTags" + bytes(8)], 1, 0, 0)
                new = ogg_page([b"OpusTags" + len(vendor).to_bytes(4, "little") + vendor + bytes(4)], 1, 0, 0)
                path.write_bytes(path.read_bytes().replace(old, new))
            return result

        with patch.object(renderer, "ffmpeg", side_effect=reencoded):
            self.create_plan()
            self.complete()
            renderer.approve_task(self.run, self.engine, identifier, "Synthetic revised fixture, not listener approval",
                                  date.today().isoformat(), listened=True, visual=True, native=True, phone=True)
            renderer.export(self.run, self.engine, [identifier], replace=True)
        revised = budget.read_json(self.content / "listening-tasks" / f"{identifier}.json")
        self.assertNotEqual(published["media"]["audio"], revised["media"]["audio"])
        self.assertEqual(draft["options"], revised["options"])
        self.assertTrue(all(clip["path"] not in old_assets for clip in revised["media"]["audio"].values()))
        for path, data in old_assets.items():
            self.assertEqual(data, (self.content / path).read_bytes())


if __name__ == "__main__":
    unittest.main()
