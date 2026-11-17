import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import record_b130_publication as recorder
from common import freeze_json, json_bytes, sha


class PublicationRetentionTests(unittest.TestCase):
    def fixture(self, root):
        commit, reviewed = "a" * 40, "b" * 40
        repo = root / "repo"
        members = [f"member-{index}" for index in range(3)]
        config = {
            "batch": 130, "repo": str(repo), "base": "c" * 40,
            "candidate": reviewed, "members": members,
        }
        closure = repo / "docs" / "n1-reviews" / "batch-130-closure"
        closure_raw = json_bytes({"recordedFileSha256": {}})
        freeze_json(closure / "provenance.json", json.loads(closure_raw))
        freeze_json(closure / "validation-provenance.json", {
            "candidate": reviewed, "reviewClosureSha256": sha(closure_raw),
            "recordedFileSha256": {},
        })
        limits = [
            "Bounded textual review only.",
            "No native-device acceptance.",
            "Latent reading collisions remain outside tested pools.",
            "Component glyphs missing from bundled fonts; no rendered fallback acceptance.",
            "Historical dictionary senses are not allocated to every spelling.",
            "Complete external captures remain local.",
        ]
        ledger = {
            "batch": 130, "status": "textual-review-closed-publication-pending",
            "membership": members, "published": [], "runtimePublished": False,
            "reviewedSnapshot": reviewed,
            "review": {"closureProvenanceSha256": sha(closure_raw)},
            "accounting": {
                "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 261,
                "publishedN1Additions": 255, "n2Placements": 6, "undelivered": 967,
                "reviewClosedPendingRecordsWithCards": 264, "notStarted": 964,
                "overallN1TaskComplete": False,
            },
            "limits": limits,
        }
        ledger_rel = "docs/n1-sources/batch-130-progress.json"
        ledger_path = repo / Path(ledger_rel)
        freeze_json(ledger_path, ledger)
        manifest = {
            "contentVersion": "fixture",
            "N1": {f"kanji/member-{index}.md": "d" * 64 for index in range(264)},
        }
        manifest_raw = json_bytes(manifest)
        source_index = [
            {"kanji": f"member-{index}", "statusAtFreeze": "pending"} for index in range(1228)
        ]
        ci = {
            "status": "completed", "conclusion": "success", "headSha": commit,
            "databaseId": 1, "url": "https://example.invalid/ci",
        }
        archive = {
            "commit": commit, "pendingChecks": [], "memory": {"breach": False},
            "manifestSha256": sha(manifest_raw), "contentVersion": "fixture",
            "verifiedRuntimeHashes": 264, "sha256": "e" * 64,
        }
        for field in (
            "manifestEqual", "manifestBytesEqualGitBlob", "zipNamesEqualExportedTree",
            "allPublishingBudgetsPassed", "contributorEvidenceExcluded",
            "perFileLimitsAndSafePathsPassed",
        ):
            archive[field] = True
        archive_path = root / "archive.json"
        freeze_json(archive_path, archive)
        narrative_path = root / "narrative.json"
        freeze_json(narrative_path, {"reviewIdentity": "Fixture review.", "changeSummary": "Fixture."})

        def fake_git(actual_config, *args):
            self.assertEqual(actual_config, config)
            responses = {
                ("ls-remote", "origin", "refs/heads/main"): f"{commit}\trefs/heads/main\n".encode(),
                ("show", f"{commit}:manifest.json"): manifest_raw,
                ("show", f"{reviewed}:manifest.json"): manifest_raw,
                ("show", f"{commit}:{ledger_rel}"): json_bytes(ledger),
                ("show", f"{commit}:docs/n1-sources/source-index.json"): json_bytes(source_index),
                ("diff", "--name-only", reviewed, commit): b"docs/closure.json\n",
            }
            return responses[args]

        def fake_api(command):
            self.assertEqual(command[0], "gh")
            args = command[1:]
            if args == ["api", "user"]:
                return json_bytes({"login": "stop-cran"})
            if args == ["api", f"repos/stop-cran/learning-japanese/commits/{commit}"]:
                return json_bytes({
                    "sha": commit, "commit": {"verification": {"verified": True}},
                    "author": {"login": "stop-cran"}, "committer": {"login": "stop-cran"},
                    "html_url": f"https://example.invalid/commit/{commit}",
                })
            if args == [
                "run", "view", "1", "--repo", "stop-cran/learning-japanese", "--json",
                "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt",
            ]:
                return json_bytes(ci)
            self.fail(f"Unexpected external command: {command}")

        return {
            "config": config, "commit": commit, "ledger": ledger, "ledgerPath": ledger_path,
            "limits": limits, "ci": ci, "archivePath": archive_path, "narrativePath": narrative_path,
            "git": fake_git, "api": fake_api,
            "publication": repo / "docs" / "n1-reviews" / "batch-130-publication",
        }

    def record(self, root, fixture):
        with patch.object(recorder, "WS", root), \
                patch.object(recorder, "load_batch", return_value=fixture["config"]), \
                patch.object(recorder, "clean") as clean, \
                patch.object(recorder, "git", side_effect=fixture["git"]), \
                patch.object(recorder.subprocess, "check_output", side_effect=fixture["api"]), \
                contextlib.redirect_stdout(io.StringIO()):
            recorder.main(130, fixture["commit"], "1", fixture["archivePath"], fixture["narrativePath"])
            clean.assert_called_once_with(fixture["config"], fixture["commit"])

    def test_receipt_and_progress_keep_every_review_limit_in_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = self.fixture(root)
            self.record(root, fixture)
            receipt = json.loads((fixture["publication"] / "provenance.json").read_bytes())
            ledger = json.loads(fixture["ledgerPath"].read_bytes())
            self.assertEqual(receipt["limits"][:-2], fixture["limits"])
            self.assertEqual(ledger["limits"], receipt["limits"])
            self.assertEqual(len(receipt["limits"]), len(fixture["limits"]) + 2)
            self.assertEqual(ledger["accounting"]["publishedPendingRecordsWithCards"], 264)
            self.assertEqual(ledger["accounting"]["undelivered"], 964)
            self.assertFalse(ledger["accounting"]["overallN1TaskComplete"])

    def test_failed_or_wrong_commit_ci_cannot_create_a_delivery_receipt(self):
        for changes in ({"conclusion": "failure"}, {"headSha": "f" * 40}):
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                fixture = self.fixture(root)
                fixture["ci"].update(changes)
                with self.assertRaisesRegex(ValueError, "CI has not succeeded"):
                    self.record(root, fixture)
                self.assertFalse(fixture["publication"].exists())
                self.assertEqual(json.loads(fixture["ledgerPath"].read_bytes()), fixture["ledger"])


if __name__ == "__main__":
    unittest.main()
