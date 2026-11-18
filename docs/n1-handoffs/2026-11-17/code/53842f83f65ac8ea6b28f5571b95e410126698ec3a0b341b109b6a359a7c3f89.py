import copy
import gzip
import json
import unittest
from unittest import mock

from close_b134 import (
    CANDIDATE, HELD_RUN, HELD_SESSION, HOLD_PATH, HOLD_SHA, REVIEWED, add_replacement,
    require_fresh_inventory, retain_bootstrap, retain_launch_hold, retained_chain, verify_audited_chain,
)
from common import WS, frozen, json_bytes, sha


def chain_fixture():
    paths = [r"C:\review\one.txt", r"C:\review\two.txt"]
    data = {paths[0]: b"native extract and colocated public data\n", paths[1]: b"public data\n"}
    rows = [{
        "index": i, "path": path, "sha256": sha(data[path]), "bytes": len(data[path]),
        "parts": [{"source": source, "sha256": sha(data[path]), "a": 1, "b": 1}],
    } for i, (path, source) in enumerate(zip(paths, (
        "reconciliation/evidence/native-example-extract.txt", "snapshot/kanji/example.md")), 1)]
    return {"segments": rows}, data


class FinalClosureControls(unittest.TestCase):
    def test_failed_launch_is_retained_without_publishing_raw_host_events(self):
        files = {}
        entry, local = retain_launch_hold(files)
        self.assertEqual(set(files), {"history/fresh-002-launch-hold.json"})
        self.assertEqual(files["history/fresh-002-launch-hold.json"], frozen(HOLD_PATH, HOLD_SHA))
        self.assertEqual(entry["quarantine"]["sha256"], HOLD_SHA)
        self.assertEqual(entry["session"], HELD_SESSION)
        self.assertFalse(entry["reviewAccepted"])
        self.assertFalse(entry["reportPresent"])
        self.assertEqual(len(local), 2)
        self.assertTrue(local[0]["path"].endswith("events.jsonl"))
        self.assertNotIn("verdict", entry)

    def test_failed_launch_cannot_be_substituted_for_a_fresh_review(self):
        for session, run in ((HELD_SESSION, "N1-B134-CLAUDE-FRESH-003"),
                             ("new-session", HELD_RUN)):
            spec = {"snapshot": REVIEWED, "session": session, "run": run}
            with self.subTest(session=session, run=run), self.assertRaises(ValueError):
                add_replacement({}, {"spec": spec}, None)

    def bootstrap_fixture(self, snapshot=None, response="PROMPT READ; WAITING FOR COORDINATOR CORE RELEASE."):
        spec = {"run": "N1-B134-CLAUDE-FRESH-002", "session": "reviewer", "snapshot": "3" * 40}
        config_ref = {"path": r"C:\review\config.json", "sha256": "a" * 64}
        config = {
            "bootstrapRecordPath": r"C:\review\bootstrap.json",
            "coreAuthorizationPath": r"C:\review\authorization.json",
            "prompt": r"C:\review\prompt.txt",
            "base": CANDIDATE,
            "contextProfile": {"selectedModel": "claude-opus-5.5", "maxPromptTokens": 952000},
            "bootstrapResponseText": response,
        }
        if snapshot is None:
            snapshot = b"".join((json.dumps(event) + "\n").encode("utf-8") for event in (
                {"type": "assistant.message", "data": {"toolRequests": [{"name": "view"}]}},
                {"type": "assistant.turn_end"},
                {"type": "assistant.message", "data": {"content": response}},
                {"type": "assistant.turn_end"},
                {"type": "session.usage_checkpoint"},
            ))
        events = [json.loads(line) for line in snapshot.decode("utf-8").splitlines()]
        shared = {"run": spec["run"], "sessionId": spec["session"], "candidate": spec["snapshot"],
                  "base": CANDIDATE, "configSha256": config_ref["sha256"], **config["contextProfile"],
                  "contextTier": "long_context",
                  "compactionEvents": [], "eventSnapshotPath": r"C:\review\bootstrap-events.jsonl",
                  "eventSnapshotSha256": sha(snapshot)}
        bootstrap = {
            **shared, "status": "PROMPT_ONLY_BOOTSTRAP_PASS", "kickoffSha256": "b" * 64,
            "promptSha256": sha(b"prompt"), "eventSnapshotBytes": len(snapshot), "eventCount": len(events),
            "eventSnapshotLastType": events[-1]["type"],
        }
        authorization = {**shared, "status": "CORE_RELEASE_AUTHORIZED",
                         "bootstrapRecordPath": config["bootstrapRecordPath"]}
        return spec, config, config_ref, bootstrap, authorization, snapshot

    def retain_fixture(self, fixture, final_events=None):
        spec, config, config_ref, bootstrap, authorization, snapshot = fixture
        bootstrap_raw = json_bytes(bootstrap)
        authorization = {**authorization, "bootstrapRecordSha256": sha(bootstrap_raw)}
        data = {
            config["bootstrapRecordPath"]: bootstrap_raw,
            config["coreAuthorizationPath"]: json_bytes(authorization),
            config["prompt"]: b"prompt", bootstrap["eventSnapshotPath"]: snapshot,
        }

        def read(path, digest=None):
            raw = data[str(path)]
            if digest is not None and sha(raw) != digest:
                raise ValueError("fixture digest mismatch")
            return raw

        files = {}
        with mock.patch("close_b134.read_review", side_effect=read):
            entries, local = retain_bootstrap(
                files, "reviews/fresh/", spec, config, config_ref,
                {"kickoffSha256": "b" * 64},
                snapshot + b"later execution\n" if final_events is None else final_events)
        return files, entries, local

    def test_bootstrap_authorization_is_archived_but_raw_events_remain_local(self):
        fixture = self.bootstrap_fixture()
        files, entries, local = self.retain_fixture(fixture)
        self.assertEqual(set(files), {"reviews/fresh/bootstrap.json",
                                      "reviews/fresh/core-authorization.json"})
        self.assertEqual(entries["bootstrap"]["sha256"], sha(files["reviews/fresh/bootstrap.json"]))
        self.assertEqual(local["sha256"], sha(fixture[-1]))
        self.assertEqual(local["bytes"], len(fixture[-1]))

    def test_complete_real_meter_event_shapes_are_retained_without_truncation(self):
        for family, digest in (
            ("claude", "0332c7aa374ddaec83912b8b243a6cfed0aa1cf736bff5de00ffb9b0b0872924"),
            ("gpt", "75947d76dc4b6136ee30f1e9100b3867b94fb6fd2092d6a52a472e0bc0871dab"),
        ):
            with self.subTest(family=family):
                snapshot = frozen(WS / "scratch-134" / "review"
                                  / f"meter-011-{family}-bootstrap-001" / "events.jsonl", digest)
                events = [json.loads(line) for line in snapshot.decode("utf-8").splitlines()]
                response, = [event["data"]["content"] for event in events
                             if event["type"] == "assistant.message"
                             and not event["data"].get("toolRequests")]
                _, _, local = self.retain_fixture(self.bootstrap_fixture(snapshot, response))
                self.assertEqual(local["sha256"], digest)
                self.assertEqual(local["bytes"], len(snapshot))

    def test_incomplete_or_duplicate_prompt_response_cannot_enter_closure(self):
        fixture = self.bootstrap_fixture()
        events = [json.loads(line) for line in fixture[-1].decode("utf-8").splitlines()]
        for invalid in (events[:3], events + [events[2], events[3]]):
            snapshot = b"".join((json.dumps(event) + "\n").encode("utf-8") for event in invalid)
            with self.assertRaises(ValueError):
                self.retain_fixture(self.bootstrap_fixture(snapshot))
        fixture[1]["bootstrapResponseText"] = "unexpected response"
        with self.assertRaises(ValueError):
            self.retain_fixture(fixture)

    def test_foreign_or_unexecuted_bootstrap_cannot_enter_closure(self):
        mutations = (
            lambda b, a: a.update(status="HOLD"),
            lambda b, a: b.update(sessionId="another-reviewer"),
            lambda b, a: a.update(configSha256="c" * 64),
            lambda b, a: a.update(selectedModel="gpt-6.1-sol"),
            lambda b, a: b.update(base="e" * 40),
            lambda b, a: a.update(compactionEvents=["compacted"]),
            lambda b, a: a.update(eventSnapshotPath=r"C:\review\other-events.jsonl"),
            lambda b, a: b.update(promptSha256="d" * 64),
            lambda b, a: b.update(eventSnapshotBytes=1),
            lambda b, a: b.update(eventSnapshotLastType="assistant.turn_end"),
        )
        for index, mutate in enumerate(mutations):
            fixture = self.bootstrap_fixture()
            mutate(fixture[3], fixture[4])
            with self.subTest(index=index), self.assertRaises(ValueError):
                self.retain_fixture(fixture)
        with self.assertRaises(ValueError):
            self.retain_fixture(self.bootstrap_fixture(), final_events=b"unrelated execution\n")

    def test_native_reconciliation_segment_remains_local_with_original_manifest(self):
        manifest, data = chain_fixture()
        before = copy.deepcopy((manifest, data))
        raw = json_bytes(manifest)
        files, retention = retained_chain(raw, data)
        self.assertEqual((manifest, data), before)
        self.assertEqual(files["manifest.json"], raw)
        self.assertNotIn("one.txt.gz", files)
        self.assertEqual(gzip.decompress(files["two.txt.gz"]), data[r"C:\review\two.txt"])
        self.assertEqual(retention["archivedSegmentIndices"], [2])
        self.assertEqual([row["index"] for row in retention["localOnlySegments"]], [1])
        self.assertEqual(json.loads(files["retention.json"]), retention)
        data[r"C:\review\two.txt"] = b"changed\n"
        with self.assertRaises(ValueError):
            retained_chain(raw, data)

    def test_report_only_optional_claim_cannot_disappear_from_resolution(self):
        report = b"### F1: Finding\n### O1: Optional point\n"
        claims = {"acceptedFindings": ["F1"], "openClaimIds": [], "coordinatorClaimIds": []}
        with self.assertRaises(ValueError):
            require_fresh_inventory(report, claims)
        claims["coordinatorClaimIds"] = ["O1"]
        require_fresh_inventory(report, claims)

    def test_equal_counts_cannot_substitute_other_chain_reads(self):
        manifest, data = chain_fixture()
        audit = {"calls": [
            {"id": str(i), "role": f"extension-{i}", "path": row["path"], "success": True}
            for i, row in enumerate(manifest["segments"], 1)]}
        events = [{
            "type": "tool.execution_complete",
            "data": {"toolCallId": str(i), "success": True,
                     "result": {"content": data[row["path"]].decode("utf-8")}},
        } for i, row in enumerate(manifest["segments"], 1)]
        verify_audited_chain(manifest, audit, events, "extension")
        mutations = (
            lambda m, a, e: m["segments"][0].update(path=r"C:\review\unread.txt"),
            lambda m, a, e: a["calls"].reverse(),
            lambda m, a, e: e[0]["data"]["result"].update(content="changed"),
            lambda m, a, e: e.append(copy.deepcopy(e[0])),
            lambda m, a, e: e[0]["data"].update(success=False),
            lambda m, a, e: m["segments"].pop(),
        )
        for index, mutate in enumerate(mutations):
            changed = copy.deepcopy((manifest, audit, events))
            mutate(*changed)
            with self.subTest(index=index), self.assertRaises(ValueError):
                verify_audited_chain(*changed, "extension")


if __name__ == "__main__":
    unittest.main()
