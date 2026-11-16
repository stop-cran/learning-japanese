import copy
import datetime
import json
import os
import shutil
import stat
import tempfile
import unittest
from pathlib import Path

import verify_b128_reconciliation as v
from common import git, load_batch, sha

CONFIG = load_batch(128)
REPO = Path(CONFIG["repo"])
OWNER = git(CONFIG, "show", "-s", "--format=%an", v.PARENT).decode("utf-8").strip()
OTHER_HEAD = "1" * 40


class Guard:
    def check(self):
        pass


def staged(path):
    return git(CONFIG, "show", f":{path}")


def parent(path):
    return git(CONFIG, "show", f"{v.PARENT}:{path}")


def remove(path):
    for root, _, files in os.walk(path):
        for name in files:
            os.chmod(Path(root) / name, stat.S_IREAD | stat.S_IWRITE)
    shutil.rmtree(path)


def dump(path, value):
    data = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    Path(path).write_bytes(data)
    return sha(data)


class Temporary(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(remove, self.tmp)


class GateTests(Temporary):
    def setUp(self):
        super().setUp()
        self.dir = self.tmp / "gates"
        self.dir.mkdir()
        for path in v.AUTHOR_GATES.iterdir():
            (self.dir / path.name).write_bytes(path.read_bytes())
        admission = self.load("admission.json")
        admission.update(head=OTHER_HEAD, mode="committed")
        dump(self.dir / "admission.json", admission)
        self.summary_sha = self.edit_summary(lambda value: value.update(mode="committed", startingHead=OTHER_HEAD))

    def load(self, name):
        return json.loads((self.dir / name).read_bytes())

    def edit_summary(self, change):
        summary = self.load("summary.json")
        change(summary)
        return dump(self.dir / "summary.json", summary)

    def edit_receipt(self, gate, change):
        receipt = self.load(f"{gate}.json")
        change(receipt)
        digest = dump(self.dir / f"{gate}.json", receipt)
        self.summary_sha = self.edit_summary(lambda value: value["logs"][gate].update(receiptSha256=digest))

    def edit_log(self, gate, data):
        (self.dir / f"{gate}.log").write_bytes(data)
        self.edit_receipt(gate, lambda value: value.update(logSha256=sha(data), logBytes=len(data)))
        self.summary_sha = self.edit_summary(lambda value: value["logs"][gate].update(logSha256=sha(data)))

    def verify(self, head=OTHER_HEAD, not_before=None):
        return v.verify_gates("committed", self.dir, self.summary_sha, head, REPO, Guard(), not_before)

    def test_committed_copy_passes(self):
        row, latest = self.verify()
        self.assertEqual([item["gate"] for item in row["gates"]], v.GATES)
        self.assertEqual(row["head"], OTHER_HEAD)
        self.assertIsNotNone(latest)

    def test_wrong_head_fails(self):
        with self.assertRaisesRegex(ValueError, "Wrong gate summary"):
            self.verify(head="2" * 40)

    def test_gates_before_successor_fail(self):
        end = v.time(self.load("manifest-rebuild.json")["completedAt"])
        with self.assertRaisesRegex(ValueError, "out of order"):
            self.verify(not_before=end + datetime.timedelta(seconds=1))

    def test_nonzero_exit_fails(self):
        self.edit_receipt("unittest", lambda value: value.update(exitCode=1))
        with self.assertRaisesRegex(ValueError, "Failed, weakened"):
            self.verify()

    def test_weakened_command_fails(self):
        self.edit_receipt("lint", lambda value: value["command"].remove("--no-jmdict"))
        with self.assertRaisesRegex(ValueError, "Failed, weakened"):
            self.verify()

    def test_memory_breach_fails(self):
        self.edit_receipt("budget", lambda value: value["memory"].update(breach="low RAM"))
        with self.assertRaisesRegex(ValueError, "Failed, weakened"):
            self.verify()

    def test_consistently_hashed_failing_log_fails(self):
        self.edit_log("unittest", b"Ran 431 tests in 1.0s\r\n\r\nFAILED (failures=1)\r\n")
        with self.assertRaisesRegex(ValueError, "Gate output differs: unittest"):
            self.verify()

    def test_extra_file_fails(self):
        (self.dir / "extra.log").write_bytes(b"")
        with self.assertRaisesRegex(ValueError, "Gate files differ"):
            self.verify()


class ContentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.table = json.loads(staged(v.PREFIX + "pair-dispositions.json"))
        cls.old = v.metadata(parent(v.CARD))
        cls.new = v.metadata(staged(v.CARD))
        cls.cards = {char: v.metadata(staged(v.PREFIX + f"comparison-cards/{char}.md")) for char in v.OTHERS}
        cls.kanjidic = staged(v.PREFIX + "kanjidic2-complete-records.xml")
        cls.identities = {
            "jmdict": {source["ent_seq"] for row in cls.table["claims"] for source in row["sources"]
                       if "ent_seq" in source},
            "kanjidic2": set(v.OTHERS + v.MEMBER),
        }

    def claims(self, table=None, new=None, cards=None):
        v.check_claims(table or self.table, self.old, new or self.new, cards or self.cards, self.identities,
                       self.kanjidic)

    def mutated(self, index, change):
        table = copy.deepcopy(self.table)
        change(table["claims"][index])
        return table

    def test_claims_pass(self):
        self.claims()

    def test_unguarded_claim_marked_guarded_fails(self):
        with self.assertRaisesRegex(ValueError, "Disposition"):
            self.claims(self.mutated(1, lambda row: row.update(decision="conservative-direct-guard")))

    def test_guarded_claim_marked_unguarded_fails(self):
        with self.assertRaisesRegex(ValueError, "Disposition"):
            self.claims(self.mutated(11, lambda row: row.update(decision="no-guard")))

    def test_changed_meanings_fail(self):
        with self.assertRaisesRegex(ValueError, "Character meanings"):
            self.claims(self.mutated(2, lambda row: row["completeCharacterEnglishMeanings"].append("extra")))

    def test_uncaptured_family_fails(self):
        with self.assertRaisesRegex(ValueError, "Uncaptured family"):
            self.claims(self.mutated(3, lambda row: row["sources"].append(
                {"file": "jmdict-complete-records.xml", "ent_seq": "0"})))

    def test_missing_character_source_fails(self):
        def drop(row):
            row["sources"] = [item for item in row["sources"] if item["file"] != "kanjidic2-complete-records.xml"]
        with self.assertRaisesRegex(ValueError, "Incomplete source binding"):
            self.claims(self.mutated(4, drop))

    def test_open_claim_fails(self):
        table = copy.deepcopy(self.table)
        table["openUnguardedClaims"] = ["Q2"]
        with self.assertRaisesRegex(ValueError, "Claim table summary"):
            self.claims(table)

    def test_comparison_endpoint_change_fails(self):
        cards = copy.deepcopy(self.cards)
        cards[v.OTHERS[0]]["quiz_exclusions"] = [v.MEMBER]
        with self.assertRaisesRegex(ValueError, "Disposition"):
            self.claims(cards=cards)

    def test_metadata_guards_and_options(self):
        v.check_metadata(self.old, self.new)
        for change in (lambda meta: meta["quiz_exclusions"].remove("\u90ca"),
                       lambda meta: meta.update(distractors=["\u53e3", "\u53f3", "\u77f3"]),
                       lambda meta: meta.update(title="mouth")):
            new = copy.deepcopy(self.new)
            change(new)
            with self.assertRaises(ValueError):
                v.check_metadata(self.old, new)

    def test_extra_body_edit_fails(self):
        v.check_edits(parent(v.CARD), staged(v.CARD), v.CARD_EDITS, "card")
        with self.assertRaisesRegex(ValueError, "Unexpected card edit"):
            v.check_edits(parent(v.CARD), staged(v.CARD) + b"extra\r\n", v.CARD_EDITS, "card")

    def test_failing_logs(self):
        for gate, text in (("lint", b"kanji checked: 1, words checked: 1\r\n0 error(s), 1 warning(s)\r\n"),
                           ("validate", b"2 error(s)\r\n"),
                           ("linkplan", v.LINKPLAN.replace("problems: 0", "problems: 1").encode()),
                           ("manifest", b"manifest.json: 8717 files version 31aa657d61cdfe9e\r\n")):
            with self.assertRaisesRegex(ValueError, f"Gate output differs: {gate}"):
                v.check_log(gate, text)


class HandoffTests(Temporary):
    def setUp(self):
        super().setUp()
        self.dir = self.tmp / "handoff"
        self.dir.mkdir()
        self.path = self.dir / "handoff.json"
        self.signature = git(CONFIG, "show", "-s", "--format=%H%n%P%n%an%n%ae%n%cn%n%ce%n%G?%n%GF%n%GP%n%B",
                             v.PARENT)
        identity = f"{OWNER} <{v.EMAIL}>"
        packet = REPO / v.PREFIX
        self.handoff = {
            "mode": "handoff", "successor": v.PARENT, "parent": v.PARENT, "publishedBase": v.BASE, "clean": True,
            "author": identity, "committer": identity, "signatureStatus": "G",
            "signingFingerprint": v.FINGERPRINT, "primaryFingerprint": v.FINGERPRINT,
            "signatureEvidence": str(self.dir / "identity-signature.log"), "worktree": str(REPO),
            "membership": [{"kanji": v.MEMBER, "sourceRow": 159}],
            "runtimeChangesFromParent": [v.CARD, "manifest.json"],
            "supportWordAndGeometryRawBytesPreserved": True,
            "addedDirectGuards": v.ADDED_GUARDS, "totalDirectGuards": 17,
            "authorGates": {"directory": str(v.AUTHOR_GATES), "summarySha256": v.AUTHOR_GATES_SHA},
            "committedGates": {"directory": str(v.COMMITTED_GATES), "summarySha256": "0" * 64,
                               "checks": v.GATES},
            "preservation": {"directory": str(v.COMMITTED_PRESERVATION), "summarySha256": "0" * 64,
                             "runtimeCount": v.RUNTIME_ENTRIES, "unchangedFromParent": v.RUNTIME_ENTRIES - 1},
            "packet": str(packet), "packetInventorySha256": v.PACKET_FILES_SHA,
            "bindings": {name: {"path": str(packet / name), "sha256": "0" * 64} for name in v.BINDINGS},
            "manifestSha256": v.MANIFEST_SHA, "contentVersion": v.CONTENT_VERSION,
            "noOpenUnguardedClaims": True, "limits": ["a", "b", "c", "d", "e"],
            "publishedAccountingUnchanged": {"delivered": 257, "remaining": 971, "localDrafts": 1},
        }
        self.receipt = {"mode": "handoff", "memory": {"breach": None}, "childPid": 1, "childExitCode": 0,
                        "waitTimeoutSeconds": 0.1, "cleanupTimeoutSecondsPerStage": 10, "activeError": None,
                        "cleanupError": None, "producerSha256": v.PRODUCER_SHAS["finish_reconciliation.py"]}

    def check(self, signature=None):
        (self.dir / "identity-signature.log").write_bytes(signature or self.signature)
        (self.dir / "operation.log").write_bytes(b"gpg: Good signature\n")
        dump(self.dir / "execution-receipt.json", self.receipt)
        dump(self.path, self.handoff)
        v.check_handoff(self.handoff, self.path, v.PARENT, OWNER, REPO, CONFIG)

    def test_handoff_passes(self):
        self.check()

    def test_unverified_signature_fails(self):
        self.handoff["signatureStatus"] = "U"
        with self.assertRaisesRegex(ValueError, "Handoff fields differ"):
            self.check()

    def test_changed_accounting_fails(self):
        self.handoff["publishedAccountingUnchanged"]["delivered"] = 258
        with self.assertRaisesRegex(ValueError, "Handoff fields differ"):
            self.check()

    def test_other_gate_directory_fails(self):
        self.handoff["committedGates"]["directory"] = str(v.AUTHOR_GATES)
        with self.assertRaisesRegex(ValueError, "Handoff fields differ"):
            self.check()

    def test_rebound_packet_fails(self):
        self.handoff["bindings"]["response-a.md"]["path"] = str(self.tmp / "response-a.md")
        with self.assertRaisesRegex(ValueError, "binding inventory"):
            self.check()

    def test_altered_signature_evidence_fails(self):
        with self.assertRaisesRegex(ValueError, "Signature evidence differs"):
            self.check(self.signature.replace(b"\nG\n", b"\nU\n"))

    def test_failed_handoff_execution_fails(self):
        self.receipt["activeError"] = "Deadline reached"
        with self.assertRaisesRegex(ValueError, "Handoff execution differs"):
            self.check()

    def test_extra_file_fails(self):
        (self.dir / "result.json").write_bytes(b"{}")
        with self.assertRaisesRegex(ValueError, "Handoff directory differs"):
            self.check()


if __name__ == "__main__":
    unittest.main()
