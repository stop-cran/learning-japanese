import copy
import datetime as dt
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import close_b134_v3 as closure
from common import frozen, sha

REQUEST_001 = closure.ROOT / "authorized-revision-resolution-001" / "closure-request.json"
OWN = b"close_b134_v3 under test"


def setUpModule():
    global BASE_REQUEST
    BASE_REQUEST = json.loads(frozen(REQUEST_001))


def request():
    value = copy.deepcopy(BASE_REQUEST)
    value["evidence"] += [
        {"archivePath": "protocol/b134_revision_progress.py", "path": "progress.py",
         "sha256": closure.PINS["b134_revision_progress.py"]},
        {"archivePath": "protocol/close_b134_v3.py", "path": "v3.py", "sha256": sha(OWN)},
    ]
    return value


class RequestChecks(unittest.TestCase):
    def check(self, value):
        with patch.object(closure, "read_ref", return_value=OWN):
            return closure.check_request(value, OWN)

    def test_pinned_request_passes(self):
        self.assertIn("protocol/close_b134_v3.py", self.check(request()))

    def test_unexpected_fields_are_rejected(self):
        value = request()
        del value["revision"]
        with self.assertRaisesRegex(ValueError, "Unexpected closure request fields"):
            self.check(value)

    def test_held_claude_acceptance_is_rejected(self):
        value = request()
        value["revision"]["confirmations"]["claude"]["sha256"] = closure.history.HELD_CLAUDE_SHA
        with self.assertRaisesRegex(ValueError, "held acceptance"):
            self.check(value)

    def test_reordered_or_missing_tokens_are_rejected(self):
        for mutate in (lambda t: t.pop("O1"), lambda t: t.update({"F1": t.pop("F1")})):
            value = request()
            mutate(value["revision"]["literalDispositionTokens"]["N1-B134-CLAUDE-REVISION-002"])
            with self.subTest(mutate=mutate), self.assertRaisesRegex(ValueError, "tokens differ"):
                self.check(value)

    def test_missing_or_changed_own_assembler_is_rejected(self):
        value = request()
        value["evidence"][-1]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "authorized-confirmation assembler"):
            self.check(value)


class RecordChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.revision = BASE_REQUEST["revision"]
        cls.items = dict(zip(closure.FAMILIES, BASE_REQUEST["reviews"]))
        cls.records = {family: closure.gather(family, cls.revision) for family in closure.FAMILIES}

    def mutated(self, family, mutate):
        records = copy.deepcopy(self.records[family])
        item = copy.deepcopy(self.items[family])
        mutate(records, item)
        return records, item

    def test_actual_confirmations_pass(self):
        for family in closure.FAMILIES:
            with self.subTest(family=family):
                records = self.records[family]
                closure.check_records(family, self.items[family], records)
                closure.check_tokens(family, self.revision["literalDispositionTokens"][closure.RUNS[family]],
                                     records["adjudication"], records["decision"], records["structure"],
                                     records["config"], records["spec"])

    def test_identity_and_authorization_mutations_are_rejected(self):
        cases = (
            ("own FRESH-003 reviewer", lambda r, i: i["spec"].update(session=closure.history.SESSIONS["gpt"])),
            ("run, session, family or snapshot", lambda r, i: r["acceptance"].update(run="N1-B134-CLAUDE-REVISION-003")),
            ("run, session, family or snapshot", lambda r, i: r["audit"].update(session=closure.COORDINATOR)),
            ("prospective authorization", lambda r, i: r["final"]["authorization"].update(sha256="0" * 64)),
            ("prospective authorization", lambda r, i: r["adjudication"].update(heldEvidenceTreatment="authorized")),
            ("producer differs", lambda r, i: r["final"].update(
                producer=closure.ref(closure.RT["rt4"], closure.RUNTIMES[0][1]))),
            ("context differs or compacted", lambda r, i: r["context"]["compactions"].append({})),
            ("report structure differs", lambda r, i: r["structure"].update(findings=1)),
            ("audit is incomplete", lambda r, i: r["audit"].update(chainRead=6)),
        )
        for message, mutate in cases:
            records, item = self.mutated("claude", mutate)
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                closure.check_records("claude", item, records)

    def test_token_mismatch_is_rejected(self):
        records, _ = self.mutated("gpt", lambda r, i: r["adjudication"]["dispositions"].update(C1="CHANGED-BY-TEST"))
        with self.assertRaisesRegex(ValueError, "tokens differ from the adjudicated report"):
            closure.check_tokens("gpt", self.revision["literalDispositionTokens"]["N1-B134-GPT-REVISION-002"],
                                 records["adjudication"], records["decision"], records["structure"],
                                 records["config"], records["spec"])


class DeliveryChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        records = closure.gather("claude", BASE_REQUEST["revision"])
        cls.admission = records["admission"]
        cls.events = frozen(records["paths"]["audit"].parent / "events.jsonl", records["audit"]["eventsSha256"])
        cls.prefix = frozen(cls.admission["prefix"]["path"], cls.admission["prefix"]["sha256"])
        cls.auth_raw = frozen(closure.AUTH["path"], closure.AUTH["sha256"])
        cls.auth_row = closure.authority(cls.auth_raw)

    def deliver(self, events=None, prefix=None, admission=None, auth_row=None):
        admission = admission or self.admission
        return closure.check_delivery(events or self.events, prefix or self.prefix, admission,
                                      admission["kickoff"], auth_row or self.auth_row)

    def suffix(self, mutate):
        rows = closure.parse(self.events[self.admission["offset"]:])
        mutate(rows)
        return self.prefix + "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows).encode()

    @staticmethod
    def user(rows):
        return next(row for row in rows if row["type"] == "user.message")

    def test_actual_delivery_passes(self):
        delivery, interaction = self.deliver()
        self.assertEqual(delivery["deliveredUserMessages"], 1)
        self.assertGreater(delivery["secondsAfterAuthorization"], 0)
        self.assertLessEqual(delivery["secondsAfterAdmission"], closure.ARRIVAL_SECONDS)
        self.assertTrue(closure.UUID.fullmatch(interaction))

    def test_missing_or_duplicate_delivery_is_rejected(self):
        for mutate in (lambda rows: rows.remove(self.user(rows)),
                       lambda rows: rows.append(copy.deepcopy(self.user(rows)))):
            with self.subTest(mutate=mutate), self.assertRaisesRegex(ValueError, "Exactly one delivered"):
                self.deliver(self.suffix(mutate))

    def test_wrong_mode_is_rejected(self):
        def turn(rows):
            after = rows[rows.index(self.user(rows)) + 1:]
            next(row for row in after if row["type"] == "assistant.turn_start")["data"]["agentMode"] = "autopilot"

        for message, mutate in (("wrong actual mode", lambda rows: self.user(rows)["data"].update(agentMode="autopilot")),
                                ("interactive mode", turn)):
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                self.deliver(self.suffix(mutate))

    def test_late_or_retroactive_delivery_is_rejected(self):
        late = {**self.admission, "createdAt": (closure.stamp(self.admission["createdAt"])
                                                - dt.timedelta(hours=1)).isoformat()}
        with self.assertRaisesRegex(ValueError, "admission window"):
            self.deliver(admission=late)
        future = {**self.auth_row, "timestamp": "2027-01-01T00:00:00.000Z"}
        with self.assertRaisesRegex(ValueError, "retroactively"):
            self.deliver(auth_row=future)

    def test_non_prefix_admission_is_rejected(self):
        changed = self.prefix[:-2] + (b"x" if self.prefix[-2:-1] != b"x" else b"y") + b"\n"
        with self.assertRaisesRegex(ValueError, "exact retained stream prefix"):
            self.deliver(prefix=changed)
        shifted = {**self.admission, "offset": self.admission["offset"] + 1}
        with self.assertRaisesRegex(ValueError, "exact retained stream prefix"):
            self.deliver(admission=shifted)

    def test_wrong_forwarding_is_rejected(self):
        source, changed = closure.SOURCE["id"], "0" * 8 + closure.SOURCE["id"][8:]
        cases = (
            ("not from this coordinator", lambda d: d.update(source="agent-other")),
            ("live user authorization", lambda d: d.update(
                transformedContent=d["transformedContent"].replace(source, changed))),
            ("live user authorization", lambda d: d.update(content=d["content"] + " ")),
        )
        for message, mutate in cases:
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                self.deliver(self.suffix(lambda rows: mutate(self.user(rows)["data"])))

    def test_authorization_event_is_the_received_one(self):
        self.assertEqual(self.auth_row["id"], closure.AUTH_EVENT)
        row = json.loads(self.auth_raw)
        row["id"] = "0" * 8 + row["id"][8:]
        with self.assertRaisesRegex(ValueError, "actual received authorization"):
            closure.authority(json.dumps(row).encode())


class AssemblyGuards(unittest.TestCase):
    def test_runtime_ancestry_is_statically_pinned(self):
        self.assertEqual(len(closure.runtime_ancestry()), len(closure.RUNTIMES))
        reader = closure.original.read_review

        def strip(path, digest=None):
            raw = reader(path, digest)
            return raw.replace(closure.RUNTIMES[1][1].encode(), b"0" * 64) if digest == closure.RUNTIMES[0][1] else raw

        with patch.object(closure.original, "read_review", side_effect=strip), \
                self.assertRaisesRegex(ValueError, "ancestry pin differs"):
            closure.runtime_ancestry()

    def test_failed_attempts_bind_their_actual_reasons(self):
        rows, _ = closure.non_accepted_attempts()
        self.assertEqual([row["status"] for row in rows],
                         ["SUPERSEDED_PREPARATION_NOT_REVIEW"] * 2 + ["FAILED_ATTEMPT_NOT_ACCEPTED"] * 3)
        changed = list(closure.ATTEMPTS)
        changed[2] = changed[2][:4] + ("ValueError: something else",) + changed[2][5:]
        with patch.object(closure, "ATTEMPTS", tuple(changed)), \
                self.assertRaisesRegex(ValueError, "Failed attempt reason differs"):
            closure.non_accepted_attempts()

    def test_unknown_identity_is_reported(self):
        known, unknown = closure.AUTH_EVENT, "12345678-1234-4234-8234-123456789abc"
        files = {"a.json": json.dumps([known, unknown]).encode()}
        self.assertEqual(closure.uuid_findings(files, {known}), [{"file": "a.json", "uuid": unknown}])

    def test_main_routes_reader_and_restores_it_after_failure(self):
        output = closure.HERE / "closure-v3-unit-test-never-created"

        def stop(mode, request_path, out, report_path, own):
            self.assertIs(closure.original.read_review, closure.v2.read_review)
            self.assertEqual((mode, out, own), ("dry", output, OWN))
            raise RuntimeError("controlled assembly failure")

        with patch.object(closure, "frozen", return_value=OWN), \
                patch.object(closure, "assemble", side_effect=stop):
            with self.assertRaisesRegex(RuntimeError, "controlled assembly failure"):
                closure.main("dry", Path("request.json"), output)
        self.assertIs(closure.original.read_review, closure.v2.original_reader)
        self.assertFalse(output.exists())

    def test_existing_or_misplaced_output_is_rejected(self):
        for output in (closure.ROOT, closure.HERE.parent / "elsewhere"):
            with self.subTest(output=output), patch.object(closure, "assemble") as assemble, \
                    self.assertRaisesRegex(ValueError, "Preserve existing|Unexpected closure destination"):
                closure.main("dry", Path("request.json"), output)
            assemble.assert_not_called()


if __name__ == "__main__":
    unittest.main(verbosity=2)
