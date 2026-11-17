import json
import shutil
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

import deliver_b134 as delivery
from common import freeze_json, json_bytes, sha, write_frozen

REVIEWED, PUBLISHED, RECEIPT = "3" * 40, "a" * 40, "b" * 40


class Guard:
    def check(self):
        pass


class FakeGit:
    def __init__(self, replies):
        self.replies = replies

    def __call__(self, *args, include_stderr=False):
        return self.replies[args]


def ledger(**changes):
    value = {"batch": 134, "published": ["\u7d2b"], "runtimePublished": True,
             "status": "published-verified-with-disclosed-review-limits", "publication": {"commit": PUBLISHED},
             "accounting": {"publishedPendingRecordsWithCards": 272, "publishedN1Additions": 266,
                            "undelivered": 956, "overallN1TaskComplete": False}}
    for key, item in changes.items():
        (value["accounting"] if key in value["accounting"] else value)[key] = item
    return value


def manifest():
    return json_bytes({"contentVersion": "v1", "kanji": {"kanji/a.md": "1"}, "words": {"words/b.md": "2"}})


def served(folder, commit, files):
    folder.mkdir()
    root = f"learning-japanese-{commit[:7]}/"
    path = folder / f"zipball-{commit[:12]}.zip"
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(root, b"")
        archive.writestr(root + "kanji/", b"")
        for name, data in files.items():
            archive.writestr(root + name, data)
    raw = manifest()
    freeze_json(folder / "receipt.json", {
        "commit": commit, "pendingChecks": [], "memory": {"breach": False}, "sha256": sha(path.read_bytes()),
        "zipEntries": len(files) + 2, "manifestSha256": sha(raw), "contentVersion": "v1",
        "verifiedRuntimeHashes": 2, **{field: True for field in (
            "manifestEqual", "manifestBytesEqualGitBlob", "zipNamesEqualExportedTree",
            "allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed")}})
    return {"headSha": commit, "status": "completed", "conclusion": "success"}


def unlock(root):
    for path in Path(root).rglob("*"):
        path.chmod(stat.S_IWRITE | stat.S_IREAD)


class DeliveryControls(unittest.TestCase):
    def test_changed_paths_are_limited_to_ledger_and_batch_folder(self):
        delivery.allowed([delivery.PROGRESS, delivery.CLOSURE + "provenance.json"], delivery.CLOSURE)
        for paths in ([], ["manifest.json"], [delivery.PUBLICATION + "x.json"],
                      [delivery.CLOSURE[:-1] + "-other/x.json"]):
            with self.subTest(paths=paths), self.assertRaises(ValueError):
                delivery.allowed(paths, delivery.CLOSURE)

    def test_published_ledger_requires_exact_new_credit(self):
        delivery.published_ledger(ledger(), PUBLISHED)
        for changes in ({"publishedPendingRecordsWithCards": 271}, {"undelivered": 957},
                        {"overallN1TaskComplete": 0}, {"publishedN1Additions": 266.0},
                        {"runtimePublished": False}, {"published": []}):
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                delivery.published_ledger(ledger(**changes), PUBLISHED)
        with self.assertRaises(ValueError):
            delivery.published_ledger(ledger(), RECEIPT)

    def test_identity_requires_owner_signature_parent_and_trailer(self):
        row = ("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", PUBLISHED)
        body = ("show", "-s", "--format=%B", PUBLISHED)
        good = f"{REVIEWED}|G|{delivery.FINGERPRINT}|{delivery.OWNER}|{delivery.OWNER}\n".encode()
        delivery.identity(FakeGit({row: good, body: b"T\n\n" + delivery.TRAILER}), PUBLISHED, REVIEWED)
        for reply, message in ((good.replace(b"|G|", b"|U|"), delivery.TRAILER),
                               (good.replace(REVIEWED.encode(), PUBLISHED.encode()), delivery.TRAILER),
                               (good.replace(delivery.OWNER.encode(), b"romanko@example.com", 1), delivery.TRAILER),
                               (good, b"no trailer")):
            with self.subTest(reply=reply), self.assertRaises(ValueError):
                delivery.identity(FakeGit({row: reply, body: message}), PUBLISHED, REVIEWED)

    def test_served_tree_equality_detects_any_byte_name_or_flag_change(self):
        root = Path(tempfile.mkdtemp())
        try:
            files = {"kanji/a.md": b"a", "words/b.md": b"b"}
            ci = served(root / "one", PUBLISHED, files)
            before, _ = delivery.entries(root / "one", PUBLISHED, manifest(), ci, Guard())
            for name, change in (("same", files), ("byte", {**files, "words/b.md": b"c"}),
                                 ("extra", {**files, "docs/r.json": b"{}"})):
                after, _ = delivery.entries(root / name, RECEIPT, manifest(),
                                            served(root / name, RECEIPT, change), Guard())
                result = delivery.compare(before, after)
                self.assertEqual(result["contentEqual"] and result["namesEqual"], name == "same")
            self.assertEqual(delivery.compare(before, after)["onlyInReceipt"], ["docs/r.json"])
            (root / "one" / f"zipball-{PUBLISHED[:12]}.zip").chmod(stat.S_IWRITE | stat.S_IREAD)
            with (root / "one" / f"zipball-{PUBLISHED[:12]}.zip").open("ab") as stream:
                stream.write(b"x")
            with self.assertRaises(ValueError):
                delivery.entries(root / "one", PUBLISHED, manifest(), ci, Guard())
            with self.assertRaises(ValueError):
                delivery.entries(root / "same", RECEIPT, manifest(), {**ci, "headSha": RECEIPT,
                                                                       "conclusion": "failure"}, Guard())
        finally:
            unlock(root)
            shutil.rmtree(root)

    def test_gate_summary_and_logs_must_bind_exact_closure(self):
        root = Path(tempfile.mkdtemp())
        try:
            closure_raw = json_bytes({"recordedFileSha256": {"a.json": "0" * 64}})
            logs = {}
            folder = root / "gates"
            for name in delivery.ORDER:
                logs[name] = {"receiptSha256": write_frozen(folder / f"{name}.json", b"{}")["sha256"],
                              "logSha256": write_frozen(folder / f"{name}.log", name.encode())["sha256"]}
            summary = {"batch": 134, "status": "PASS", "mode": "closure", "head": REVIEWED,
                       "base": delivery.BASE, "initialSnapshot": "ba80afffc20a72d31be68b355b6f90aab36a5726",
                       "reviewedSnapshot": REVIEWED, "manifestReproducible": True,
                       "manifestSha256": sha(manifest()), "closureProvenanceSha256": sha(closure_raw),
                       "closureFiles": 2, "checks": delivery.ORDER, "logs": logs}
            freeze_json(folder / "summary.json", summary)
            with mock.patch.object(delivery, "HERE", root):
                delivery.gate(folder / "summary.json", "closure", REVIEWED, REVIEWED, manifest(), closure_raw)
                for args in (("committed", REVIEWED, PUBLISHED, manifest(), closure_raw),
                             ("closure", REVIEWED, REVIEWED, manifest() + b" ", closure_raw),
                             ("closure", REVIEWED, REVIEWED, manifest(), closure_raw + b" ")):
                    with self.subTest(args=args[0]), self.assertRaises(ValueError):
                        delivery.gate(folder / "summary.json", *args)
                log = folder / "unittest.log"
                log.chmod(stat.S_IWRITE | stat.S_IREAD)
                log.write_bytes(b"changed")
                log.chmod(stat.S_IREAD)
                with self.assertRaises(ValueError):
                    delivery.gate(folder / "summary.json", "closure", REVIEWED, REVIEWED, manifest(), closure_raw)
        finally:
            unlock(root)
            shutil.rmtree(root)

    def test_cli_requires_exact_mode_arity(self):
        self.assertIs(delivery.dispatch(["push", "closure", REVIEWED, PUBLISHED, "g", "c"])[0], delivery.push)
        self.assertIs(delivery.dispatch(["push", "receipt", REVIEWED, RECEIPT])[0], delivery.push)
        self.assertIs(delivery.dispatch(["equal", PUBLISHED, RECEIPT, "p", "r", "c"])[0], delivery.equal)
        for argv in ([], ["push", "closure", REVIEWED, PUBLISHED], ["push", "receipt", REVIEWED, RECEIPT, "g", "c"],
                     ["sign", "closure"], ["checkpoint", PUBLISHED, RECEIPT], ["publish", "x"]):
            with self.subTest(argv=argv), self.assertRaises(SystemExit):
                delivery.dispatch(argv)

    def test_checkpoint_body_reports_served_equality(self):
        body = delivery.checkpoint_body("B134 base", "https://r", "https://c", 9123)
        self.assertTrue(body.startswith("B134 base\n\n"))
        self.assertIn("[publication receipt](https://r)", body)
        self.assertIn("**9,123 served entries**", body)


if __name__ == "__main__":
    unittest.main()
