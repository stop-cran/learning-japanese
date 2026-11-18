import copy
import unittest
from contextlib import ExitStack
from unittest.mock import patch

import record_b130_integration_publication as recorder
from common import json_bytes, sha


class IntegrationPublicationTests(unittest.TestCase):
    def archive(self):
        blobs = {"report.md": b"confirmed", "proof.json": b"verified"}
        closure = {"recordedFileSha256": {"report.md": sha(blobs["report.md"])}}
        blobs["provenance.json"] = json_bytes(closure)
        validation = {
            "candidate": recorder.ACTIVE,
            "reviewClosureSha256": sha(blobs["provenance.json"]),
            "recordedFileSha256": {"proof.json": sha(blobs["proof.json"])},
        }
        blobs["validation-provenance.json"] = json_bytes(validation)
        return blobs

    def test_archive_rejects_changed_missing_extra_and_cyclic_evidence(self):
        blobs = self.archive()
        closure_sha = sha(blobs["provenance.json"])
        validation_sha = sha(blobs["validation-provenance.json"])
        recorder.verify_archive(blobs, recorder.ACTIVE, closure_sha, validation_sha)
        for kind in ("changed", "missing", "extra", "cycle", "wrong-candidate"):
            with self.subTest(kind=kind):
                changed = dict(blobs)
                if kind == "changed":
                    changed["report.md"] = b"not confirmed"
                elif kind == "missing":
                    del changed["proof.json"]
                elif kind == "extra":
                    changed["unlisted.json"] = b"unexpected"
                elif kind == "cycle":
                    changed["provenance.json"] = json_bytes({
                        "recordedFileSha256": {"provenance.json": closure_sha},
                    })
                with self.assertRaises(ValueError):
                    recorder.verify_archive(
                        changed, recorder.PREVIOUS if kind == "wrong-candidate" else recorder.ACTIVE,
                        closure_sha, validation_sha)

    def test_extension_preserves_every_existing_path_and_mode(self):
        before = {
            recorder.LEDGER: ("100644", "blob", "a"),
            "kanji/example.md": ("100644", "blob", "b"),
            "docs/previous-proof.json": ("100644", "blob", "c"),
        }
        after = dict(before)
        after[recorder.LEDGER] = ("100644", "blob", "d")
        added = recorder.INTEGRATION_CLOSURE + "/provenance.json"
        after[added] = ("100644", "blob", "e")
        self.assertEqual(recorder.check_extension(before, after), {added})
        for kind in ("runtime", "old-proof", "mode", "removed", "unrelated-doc", "symlink"):
            with self.subTest(kind=kind):
                changed = dict(after)
                if kind == "runtime":
                    changed["kanji/example.md"] = ("100644", "blob", "f")
                elif kind == "old-proof":
                    changed["docs/previous-proof.json"] = ("100644", "blob", "f")
                elif kind == "mode":
                    changed["kanji/example.md"] = ("100755", "blob", "b")
                elif kind == "removed":
                    del changed["docs/previous-proof.json"]
                elif kind == "unrelated-doc":
                    changed["docs/unrelated.json"] = ("100644", "blob", "f")
                else:
                    changed[added] = ("120000", "blob", "e")
                with self.assertRaises(ValueError):
                    recorder.check_extension(before, changed)

    def fixture(self):
        manifest = json_bytes({"contentVersion": "fixture", "files": {"kanji/example.md": "a" * 64}})
        runtime = {"manifestSha256": sha(manifest), "contentVersion": "fixture", "runtimeEntries": 1}
        previous = {
            "reviewedSnapshot": recorder.PREVIOUS, "published": [],
            "review": {"closureProvenanceSha256": "b" * 64},
            "limits": ["Original limits remain."],
        }
        blobs = {
            "original-progress.json": json_bytes(previous),
            "claude.md": b"Claude bounded confirmation",
            "gpt.md": b"GPT bounded confirmation",
        }
        blobs["provenance.json"] = json_bytes({
            "recordedFileSha256": {name: sha(raw) for name, raw in blobs.items()},
        })
        blobs["validation-provenance.json"] = json_bytes({
            "candidate": recorder.ACTIVE, "reviewClosureSha256": sha(blobs["provenance.json"]),
            "recordedFileSha256": {},
        })
        ledger = {
            **copy.deepcopy(previous), "activeReviewedSnapshot": recorder.ACTIVE,
            "integrationReview": {
                "status": "closed-with-disclosed-limits", "reviewedSnapshot": recorder.ACTIVE,
                "previousReviewedSnapshot": recorder.PREVIOUS, "parents": recorder.PARENTS,
                "runtimeCandidate": runtime, "finalRuns": recorder.FINAL_RUNS,
                "closurePath": recorder.INTEGRATION_CLOSURE,
                "closureProvenanceSha256": sha(blobs["provenance.json"]),
                "validationProvenanceSha256": sha(blobs["validation-provenance.json"]),
                "limits": ["Integration impact only."],
            },
        }
        before = {recorder.LEDGER: ("100644", "blob", "a"),
                  "docs/old-proof.json": ("100644", "blob", "b")}
        after = {**before, recorder.LEDGER: ("100644", "blob", "c")}
        after.update({recorder.INTEGRATION_CLOSURE + "/" + name: ("100644", "blob", name)
                      for name in blobs})
        responses = {
            ("show", f"{recorder.PARENTS[0]}:{recorder.LEDGER}"): json_bytes(previous),
            ("show", f"{recorder.ACTIVE}:manifest.json"): manifest,
        }
        patches = {
            "RUNTIME": runtime,
            "git": lambda config, *args: responses[args],
            "original_lineage": lambda *args: previous["review"]["closureProvenanceSha256"],
            "owner_signature": lambda *args: None,
            "tracked_tree": lambda config, commit: before if commit == recorder.ACTIVE else after,
            "tree": lambda *args: "unchanged-original-closure",
            "archive_blobs": lambda *args: blobs,
            "accepted_confirmations": lambda *args: {
                "claude": sha(blobs["claude.md"]), "gpt": sha(blobs["gpt.md"]),
            },
        }
        return manifest, ledger, patches

    def select(self, manifest, ledger, patches):
        with ExitStack() as stack:
            for name, value in patches.items():
                stack.enter_context(patch.object(recorder, name, value))
            return recorder.select_reviewed_snapshot({}, "c" * 40, ledger, manifest)

    def test_snapshot_selection_preserves_old_metadata_and_rejects_stale_context(self):
        manifest, ledger, patches = self.fixture()
        saved = copy.deepcopy(ledger)
        context = self.select(manifest, ledger, patches)
        self.assertEqual(context["reviewedSnapshot"], recorder.ACTIVE)
        self.assertEqual(ledger, saved)
        for kind in ("old-metadata", "active-snapshot", "parents", "manifest", "report"):
            with self.subTest(kind=kind):
                manifest, ledger, patches = self.fixture()
                if kind == "old-metadata":
                    ledger["limits"] = []
                elif kind == "active-snapshot":
                    ledger["activeReviewedSnapshot"] = recorder.PREVIOUS
                elif kind == "parents":
                    ledger["integrationReview"]["parents"] = list(reversed(recorder.PARENTS))
                elif kind == "manifest":
                    manifest += b"\n"
                else:
                    patches["accepted_confirmations"] = lambda *args: {"missing": "f" * 64}
                with self.assertRaises(ValueError):
                    self.select(manifest, ledger, patches)


if __name__ == "__main__":
    unittest.main()
