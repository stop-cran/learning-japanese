"""Synthetic Git/ZIP integration controls. Never opens or invokes Git in b134-worktree.

Synthetic commits are UNSIGNED; a narrow metadata shim supplies signature observations
while retaining real parents, blobs, modes and graph traversal. Network/signing calls
are intercepted, never executed. All repos and fixtures stay below this scratch root.
"""
import copy
import contextlib
import datetime
import hashlib
import json
import io
import os
import stat
import subprocess
import sys
import unittest
import uuid
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
TOOLS = Path(r"C:\Users\stop-\n1-kanji-workspace\review-tools")
sys.path.insert(0, str(TOOLS))
import b134_integrated_v1 as c
import deliver_b134_integration_v1 as d
import run_b134_integration_gates_v1 as gates
import verify_b134_integration_closure_v1 as verifier
import record_b134_integration_publication_v1 as recorder
from common import freeze_json, frozen, json_bytes, sha, start_guard, write_frozen
from verify_b134_payload import runtime_entries


class FixtureGit:
    def __init__(self, repo, guard):
        self.repo, self.guard = repo, guard
        self.cleanup = SimpleNamespace(stop_child=self.stop)
        self.calls = []

    @staticmethod
    def stop(process):
        if process and process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=10)

    def __call__(self, *args, include_stderr=False):
        assert self.repo.is_relative_to(ROOT), "Synthetic Git escaped"
        assert not any(arg in args for arg in ("push", "fetch", "-S")), "Prohibited real effect in test"
        self.calls.append(args)
        process = subprocess.Popen(
            ["git", "--no-pager", "-c", "core.quotepath=false", *args], cwd=self.repo,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env={**os.environ, "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull})
        try:
            while True:
                try:
                    out, err = process.communicate(timeout=.1)
                    break
                except subprocess.TimeoutExpired:
                    self.guard.check()
        finally:
            self.stop(process)
        if process.returncode:
            raise ValueError(f"Synthetic git failed {args}: {err.decode('utf-8', 'replace')}")
        if args[:3] == ("show", "-s", "--format=%P|%G?|%GF|%ae|%ce"):
            fields = out.decode().strip().split("|")
            fields[1:3] = ["G", c.FINGERPRINT]
            out = ("|".join(fields) + "\n").encode()
        return out + err if include_stderr else out


class IntegrationControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard, _ = start_guard("B134 synthetic integration fixtures")
        cls.area = ROOT / ("synthetic-" + uuid.uuid4().hex)
        cls.area.mkdir()
        cls.repo = cls.area / "repo"
        cls.repo.mkdir()
        cls.git = FixtureGit(cls.repo, cls.guard)
        cls.git("init", "--quiet")
        for key, value in (("user.name", "Synthetic owner"), ("user.email", c.OWNER),
                           ("user.signingkey", c.FINGERPRINT), ("commit.gpgsign", "false"),
                           ("core.autocrlf", "false"), ("core.longpaths", "true")):
            cls.git("config", key, value)
        cls.git("remote", "add", "origin", "https://github.com/stop-cran/learning-japanese.git")
        cls.put("articles/numbers-and-counters.md", b"old article\n")
        cls.put("counters/kumiexpressions.json", b'{"value":"old"}\n')
        cls.put("kanji/test.md", b"original card\n")
        cls.put("tools/build_manifest.py", b"# synthetic unchanged builder\n")
        for name in c.HELPERS:
            cls.put(f"docs/n1-sources/batch-134/producers/{name}", ("# synthetic " + name).encode())
        index = [{"kanji": value, "statusAtFreeze": "pending"} for value in
                 [*("synthetic-" + str(i) for i in range(271)), "\u7d2b",
                  *("missing-" + str(i) for i in range(956))]]
        cls.put("docs/n1-sources/source-index.json", json_bytes(index))
        cls.base_manifest = {"schemaVersion": 1, "contentVersion": "baseline",
                             "files": {"articles/numbers-and-counters.md": sha(b"old article\n"),
                                       "counters/kumiexpressions.json": sha(b'{"value":"old"}\n'),
                                       "kanji/\u7d2b.md": "0"*64,
                                       **{f"kanji/synthetic-{i}.md": "0"*64 for i in range(8744)}}}
        cls.put("manifest.json", json_bytes(cls.base_manifest))
        cls.base = cls.commit("baseline")
        cls.put("kanji/test.md", b"reviewed purple fixture\n")
        cls.reviewed = cls.commit("reviewed")
        cls.old_ledger = {"batch": 134, "reviewedSnapshot": cls.reviewed,
                           "status": "textual-review-closed-publication-pending", "published": [],
                           "runtimePublished": False, "limits": ["Original native/device limits retained."],
                           "accounting": {"publishedPendingRecordsWithCards": 271, "publishedN1Additions": 265,
                                          "undelivered": 957, "overallN1TaskComplete": False}}
        cls.put(c.PROGRESS, json_bytes(cls.old_ledger))
        cls.put(c.CLOSURE + "evidence.md", b"original report preserved\n")
        cls.put(c.CLOSURE + "provenance.json", json_bytes({
            "recordedFileSha256": {"evidence.md": sha(b"original report preserved\n")}}))
        cls.closure = cls.commit("original closure")
        cls.git("checkout", "--quiet", "--detach", cls.base)
        cls.incoming_content = {"articles/numbers-and-counters.md": b"concurrent article\n",
                                "counters/kumiexpressions.json": b'{"value":"incoming"}\n'}
        for path, raw in cls.incoming_content.items():
            cls.put(path, raw)
        cls.combined_manifest = c.expected_manifest(cls.base_manifest, cls.incoming_content)
        cls.put("manifest.json", cls.combined_manifest)
        cls.incoming = cls.commit("incoming")
        cls.git("checkout", "--quiet", "--detach", cls.closure)
        cls.git("merge", "--no-commit", "--no-ff", cls.incoming)
        cls.merged = cls.commit("merge")
        cls.patches = [
            patch.object(c, "BASE", cls.base), patch.object(c, "REVIEWED", cls.reviewed),
            patch.object(c, "INCOMING", cls.incoming), patch.object(c, "REPO", cls.repo),
            patch.object(c, "SCRATCH", cls.area / "scratch"), patch.object(c, "REVIEW", cls.area),
            patch.object(gates, "BASE", cls.base),
            patch.object(c, "lineage", lambda git, rev: None),
            patch.object(c, "validate_progress", lambda *args: {"delivered": 272, "remaining": 956}),
            patch.object(d, "Git", lambda *args: cls.git),
            patch.object(gates, "Git", lambda *args: cls.git),
            patch.object(verifier, "Git", lambda *args: cls.git),
            patch.object(recorder, "Git", lambda *args: cls.git),
        ]
        for item in cls.patches:
            item.start()
        cls.copies = cls.area / "copied-tools"
        for name in c.TOOLS:
            write_frozen(cls.copies / name, (TOOLS / name).read_bytes())
        for module, name in ((c, "b134_integrated_v1.py"), (gates, "run_b134_integration_gates_v1.py"),
                             (d, "deliver_b134_integration_v1.py"),
                             (recorder, "record_b134_integration_publication_v1.py")):
            item = patch.object(module, "__file__", str(cls.copies / name))
            item.start(); cls.patches.append(item)
        for name in c.HELPERS:
            write_frozen(c.SCRATCH / name, ("# synthetic " + name).encode())
        cls.plan = {"schemaVersion": 1, "batch": 134, "reviewedSnapshot": cls.reviewed,
                    "signedClosure": cls.closure, "merge": cls.merged, "incoming": cls.incoming,
                    "originalGates": {"closure": {}, "committed": {}},
                    "mergeGates": {"merge": {}, "committed-merge": {}},
                    "confirmations": {}, "toolInventory": {}}
        cls.confirmations = cls.make_confirmations()
        cls.archive, cls.integration_ledger = cls.make_archive()
        for path, raw in cls.archive.items():
            cls.put(c.INTEGRATION + path, raw)
        cls.put(c.PROGRESS, json_bytes(cls.integration_ledger))
        cls.integrated = cls.commit("integration closure")
        cls.plan["toolInventory"] = cls.ref(freeze_json(cls.area / "tool-inventory.json", {
            "files": {name: sha(frozen(cls.copies / name)) for name in c.TOOLS}}))
        for mode in ("closure", "committed"):
            cls.plan["originalGates"][mode] = cls.ref(freeze_json(
                cls.area / f"original-{mode}.json", {"synthetic": "inherited verifier intercepted"}))
        for mode in ("merge", "committed-merge"):
            cls.plan["mergeGates"][mode] = cls.make_gates(mode, cls.closure if mode == "merge" else cls.merged,
                                                        c.tree(cls.git, cls.merged))
        cls.plan_path = cls.area / "plan.json"
        freeze_json(cls.plan_path, cls.plan)
        cls.pre_closure = cls.make_gates("closure", cls.merged, c.tree(cls.git, cls.integrated))
        cls.post_closure = cls.make_gates("committed-closure", cls.integrated, c.tree(cls.git, cls.integrated))

    @classmethod
    def tearDownClass(cls):
        for item in reversed(cls.patches):
            item.stop()
        memory = cls.guard.finish()
        assert not memory["breach"]
        freeze_json(cls.area / "memory.json", memory)

    @classmethod
    def put(cls, name, raw):
        path = cls.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.chmod(stat.S_IREAD | stat.S_IWRITE)
        path.write_bytes(raw)

    @classmethod
    def commit(cls, title):
        cls.git("add", "--all")
        cls.git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", title, "-m", c.TRAILER.decode())
        return cls.git("rev-parse", "HEAD").decode().strip()

    @staticmethod
    def ref(value):
        return {key: value[key] for key in ("path", "sha256")}

    @classmethod
    def make_gates(cls, mode, head, entries):
        folder = cls.area / ("gate-" + mode + "-" + uuid.uuid4().hex)
        helpers = {name: sha(frozen(c.SCRATCH / name)) for name in c.HELPERS}
        commands, logs = c.expected_commands(), {}
        for number, name in enumerate(c.ORDER):
            log = write_frozen(folder / (name + ".log"), b"Synthetic gate observation; command NOT executed.\n")
            receipt = {"gate": name, "exitCode": 0, "childExitCodeAfterCleanup": 0,
                       "cleanupError": None, "activeError": None, "memory": {"breach": None},
                       "logSha256": log["sha256"], "base": cls.base, "cwd": str(cls.repo),
                       "command": commands[name], "runnerSha256": helpers["run_134_gates.py"],
                       "commonHelperSha256": helpers["common_134.py"],
                       "boundedLauncherSha256": helpers["bounded_launch_134.py"],
                       "guardSha256": c.GUARD_SHA, "waitTimeoutSeconds": .1,
                       "cleanupTimeoutSecondsPerStage": 10,
                       "startedAt": f"2026-01-01T00:00:{number:02d}+00:00",
                       "completedAt": f"2026-01-01T00:00:{number:02d}+00:00",
                       "manifestSha256": sha(cls.combined_manifest) if name.startswith("manifest") else None,
                       "manifestReproducible": name == "manifest-rebuild"}
            item = freeze_json(folder / (name + ".json"), receipt)
            logs[name] = {"receiptSha256": item["sha256"], "logSha256": log["sha256"]}
        return cls.ref(freeze_json(folder / "summary.json", {
            "batch": 134, "mode": mode, "head": head, "signedClosure": cls.closure,
            "merge": None if mode == "merge" else cls.merged, "incoming": cls.incoming,
            "reviewedSnapshot": cls.reviewed, "base": cls.base, "checks": c.ORDER, "serial": True,
            "commands": commands, "helperHashes": helpers, "treeInventorySha256": gates.tree_digest(entries),
            "manifestSha256": sha(cls.combined_manifest), "manifestReproducible": True,
            "memory": {"breach": None}, "producerSha256": sha(frozen(cls.copies / "run_b134_integration_gates_v1.py")),
            "logs": logs, "status": "PASS"}))

    @classmethod
    def make_confirmations(cls):
        for family in ("claude", "gpt"):
            folder = cls.area / family
            run = "N1-B134-" + family.upper() + "-INTEGRATION-001"
            session = "synthetic-" + family
            report = write_frozen(folder / "report.md", b"synthetic confirmation\n")
            report = {key: report[key] for key in ("path", "sha256")}
            final = {"batch": 134, "candidate": cls.merged, "session": session, "run": run,
                     "status": "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION", "report": report}
            adjudication = {"candidate": cls.merged, "session": session, "run": run, "report": report,
                            "verdict": "CONFIRMED", "acceptedNewFindings": [], "openClaimIds": [],
                            "rawAuditWasClean": True, "controlAdjudicationApplied": False}
            refs = {}
            for name, value in (("final", final), ("adjudication", adjudication)):
                ref = freeze_json(folder / (name + ".json"), value)
                refs[name] = {key: ref[key] for key in ("path", "sha256")}
            acceptance = {"batch": 134, "run": run, "family": family, "session": session,
                          "candidate": cls.merged, "verdict": "CONFIRMED",
                          "confirmationAccepted": True, "reviewEvidenceAccepted": True,
                          "acceptedNewFindings": [], "openClaimIds": [], "report": report, **refs}
            ref = freeze_json(folder / "acceptance.json", acceptance)
            cls.plan["confirmations"][family] = {key: ref[key] for key in ("path", "sha256")}
        return c.accepted(cls.plan)

    @classmethod
    def make_archive(cls):
        runtime = {"manifestSha256": sha(cls.combined_manifest),
                   "contentVersion": json.loads(cls.combined_manifest)["contentVersion"], "runtimeEntries": 8747}
        files = {"previous-progress.json": json_bytes(cls.old_ledger), ".gitattributes": b"* -text\n"}
        runs = []
        for family, evidence in cls.confirmations.items():
            runs.append(evidence["run"])
            for key in ("acceptance", "report", "final", "adjudication"):
                files[f"runs/{evidence['run']}/{key}.{'md' if key == 'report' else 'json'}"] = evidence[key]
        provenance = {"batch": 134, "reviewedSnapshot": cls.merged, "previousReviewedSnapshot": cls.reviewed,
                      "parents": [cls.closure, cls.incoming], "runtimeCandidate": runtime, "finalRuns": runs,
                      "publication": "PENDING", "deliveryCredit": 0, "limits": ["Integration impact only."],
                      "recordedFileSha256": {name: sha(raw) for name, raw in files.items()}}
        files["provenance.json"] = json_bytes(provenance)
        files["validation-provenance.json"] = json_bytes({
            "candidate": cls.merged, "reviewClosureSha256": sha(files["provenance.json"]),
            "recordedFileSha256": {}})
        review = {"reviewedSnapshot": cls.merged, "previousReviewedSnapshot": cls.reviewed,
                  "parents": [cls.closure, cls.incoming], "status": "closed-with-disclosed-limits",
                  "runtimeCandidate": runtime, "finalRuns": runs, "closurePath": c.INTEGRATION.rstrip("/"),
                  "closureProvenanceSha256": sha(files["provenance.json"]),
                  "validationProvenanceSha256": sha(files["validation-provenance.json"]),
                  "limits": provenance["limits"]}
        return files, {**copy.deepcopy(cls.old_ledger), "activeReviewedSnapshot": cls.merged, "integrationReview": review}

    def test_exact_signed_merge_graph_and_runtime_delta(self):
        result = c.merge(self.git, self.closure, self.merged)
        self.assertEqual(result["runtimeEntries"], 8747)
        self.assertEqual(result["manifestSha256"], sha(self.combined_manifest))
        with self.assertRaises(ValueError):
            c.merge(self.git, self.closure, self.integrated)

    def test_merge_object_and_manifest_mutations(self):
        staged = c.tree(self.git, self.merged)
        for name in ("kanji/test.md", c.CLOSURE + "evidence.md", c.PROGRESS):
            changed = {**staged, name: ("100644", "blob", "0"*40)}
            with self.subTest(path=name), self.assertRaises(ValueError):
                c.merge(self.git, self.closure, staged=changed, manifest=self.combined_manifest)
        with self.assertRaises(ValueError):
            c.merge(self.git, self.closure, staged=staged, manifest=self.combined_manifest + b" ")
        with self.assertRaises(ValueError):
            c.identity(self.git, self.merged, [self.incoming, self.closure])

    def test_actual_integration_closure_and_additive_ledger(self):
        result = c.verify_closure(self.git, self.plan, self.integrated)
        self.assertEqual(result["activeReviewedSnapshot"], self.merged)
        self.assertEqual(result["archiveFiles"], len(self.archive))

    def test_existing_tree_modes_archives_and_membership_are_preserved(self):
        before, after = c.tree(self.git, self.merged), c.tree(self.git, self.integrated)
        for change in (
            {**after, "kanji/test.md": ("100644", "blob", "1"*40)},
            {k: v for k, v in after.items() if k != c.CLOSURE + "evidence.md"},
            {**after, c.INTEGRATION + "bad-link": ("120000", "blob", "1"*40)},
            {**after, "docs/unrelated.md": ("100644", "blob", "1"*40)},
        ):
            with self.assertRaises(ValueError):
                c.extension(before, change)

    def test_closure_rejects_credit_old_value_changes_and_unbound_reports(self):
        for mutate in (
            lambda x: x["accounting"].update(undelivered=956),
            lambda x: x.update(runtimePublished=True),
            lambda x: x["integrationReview"].update(reviewedSnapshot=self.reviewed),
            lambda x: x["integrationReview"].update(finalRuns=["invented"]),
        ):
            ledger = copy.deepcopy(self.integration_ledger)
            mutate(ledger)
            with self.assertRaises(ValueError):
                c.closure_data(self.plan, self.old_ledger, ledger, self.archive,
                               self.combined_manifest, self.confirmations)
        changed = dict(self.archive)
        changed["extra.jsonl"] = b"private raw"
        with self.assertRaises(ValueError):
            c.closure_data(self.plan, self.old_ledger, self.integration_ledger, changed,
                           self.combined_manifest, self.confirmations)

    def test_acceptances_require_distinct_families_hashes_and_snapshot(self):
        for family in ("claude", "gpt"):
            plan = copy.deepcopy(self.plan)
            plan["confirmations"][family]["sha256"] = "0"*64
            with self.assertRaises(ValueError):
                c.accepted(plan)
        plan = copy.deepcopy(self.plan)
        plan["merge"] = self.reviewed
        with self.assertRaises(ValueError):
            c.accepted(plan)

    def test_paths_reject_absolute_traversal_and_aliases(self):
        for name in ("../x", "/x", "C:\\x", "a\\x", "a//b", "a/./b", "a/../b", "x:stream"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                c.relative(name)

    def test_pending_and_committed_modes_match_same_exact_tree(self):
        self.git("checkout", "--quiet", "--detach", self.merged)
        context, digest = gates.validate_tree("committed-merge", self.git, self.repo, self.closure,
                                               self.merged, self.merged, None, self.guard)
        self.assertEqual(digest, gates.tree_digest(c.tree(self.git, self.merged)))
        self.put("kanji/test.md", b"unstaged change\n")
        with self.assertRaises(ValueError):
            gates.validate_tree("committed-merge", self.git, self.repo, self.closure,
                                self.merged, self.merged, None, self.guard)
        self.git("restore", "--", "kanji/test.md")
        self.git("checkout", "--quiet", "--detach", self.integrated)

    def test_signature_metadata_must_not_be_weakened(self):
        original = self.git
        def unsigned(*args):
            raw = original(*args)
            return raw.replace(b"|G|", b"|N|") if "--format=%P|%G?|%GF|%ae|%ce" in args else raw
        with self.assertRaises(ValueError):
            c.identity(unsigned, self.merged, [self.closure, self.incoming])

    def test_delivery_cli_exact_arity_and_invalid_modes(self):
        self.assertIs(d.dispatch(["push", "receipt", "p", "r", "out"])[0], d.push)
        self.assertIs(d.dispatch(["push", "closure", "p", "i", "pre", "post", "out"])[0], d.push)
        self.assertIs(d.dispatch(["equal", *["x"]*7])[0], d.equal)
        self.assertIs(d.dispatch(["checkpoint", *["x"]*7])[0], d.checkpoint)
        for args in ([], ["push", "closure", "p", "i", "out"], ["equal", *["x"]*8]):
            with self.assertRaises(ValueError):
                d.dispatch(args)

    def test_remote_advance_and_nonancestor_rejected_before_push(self):
        def remote(*args):
            return (self.incoming + "\trefs/heads/main\n").encode()
        d.remote_head(remote, self.incoming)
        with self.assertRaises(ValueError):
            d.remote_head(remote, self.base)
        with self.assertRaises(ValueError):
            self.git("merge-base", "--is-ancestor", self.integrated, self.incoming)

    def test_publication_ledger_only_advances_exact_credit(self):
        before = copy.deepcopy(self.integration_ledger)
        proof = {"limits": ["Preserved limits."], "publishedCommitUrl": "https://example.invalid/commit"}
        after = copy.deepcopy(before)
        after.update(status=d.STATUS, published=["\u7d2b"], runtimePublished=True, limits=proof["limits"])
        after["accounting"].update(publishedPendingRecordsWithCards=272, publishedN1Additions=266, undelivered=956)
        after["publication"] = {"commit": self.integrated, "url": proof["publishedCommitUrl"],
                                "receipt": "../n1-reviews/batch-134-integration-publication-001/provenance.json"}
        d.published_ledger(before, after, self.integrated, proof)
        for mutate in (
            lambda x: x["integrationReview"].update(previousReviewedSnapshot=self.base),
            lambda x: x["accounting"].update(undelivered=955),
            lambda x: x["accounting"].update(overallN1TaskComplete=True),
        ):
            wrong = copy.deepcopy(after); mutate(wrong)
            with self.assertRaises(ValueError):
                d.published_ledger(before, wrong, self.integrated, proof)

    def test_all_new_tools_parse_without_running(self):
        import ast
        for name in c.TOOLS:
            ast.parse((TOOLS / name).read_bytes(), filename=name)

    def test_gate_command_producer_log_and_tree_bindings(self):
        ref = self.plan["mergeGates"]["committed-merge"]
        c.gate_ref(ref, "committed-merge", self.closure, self.merged, self.merged, sha(self.combined_manifest))
        with patch.object(d.linear, "gate", return_value=b"synthetic inherited gates"):
            c.plan_gates(self.git, self.plan)
        for field, value in (("base", self.incoming), ("producerSha256", "0"*64),
                             ("commands", {name: ["python", "-c", "pass"] for name in c.ORDER})):
            changed = json.loads(frozen(ref["path"]))
            changed[field] = value
            new_ref = self.ref(freeze_json(self.area / ("bad-" + uuid.uuid4().hex + ".json"), changed))
            with self.assertRaises(ValueError):
                c.gate_ref(new_ref, "committed-merge", self.closure, self.merged,
                           self.merged, sha(self.combined_manifest))
        plan = copy.deepcopy(self.plan)
        changed = json.loads(frozen(ref["path"]))
        changed["treeInventorySha256"] = "0"*64
        # Keep unchanged per-gate evidence in its original folder.
        bad_path = Path(ref["path"]).with_name("bad-tree.json")
        plan["mergeGates"]["committed-merge"] = self.ref(freeze_json(bad_path, changed))
        with patch.object(d.linear, "gate", return_value=b"synthetic inherited gates"), self.assertRaises(ValueError):
            c.plan_gates(self.git, plan)

    def test_frozen_plan_checks_complete_source_inventory(self):
        self.assertEqual(c.load_plan(self.plan_path)[0], self.plan)
        wrong = copy.deepcopy(self.plan)
        wrong["incoming"] = self.base
        path = self.area / ("bad-plan-" + uuid.uuid4().hex + ".json")
        freeze_json(path, wrong)
        with self.assertRaises(ValueError):
            c.load_plan(path)

    def test_four_gate_modes_real_controllers_with_simulated_gate_children(self):
        def fake_gate(name, folder, expected):
            # Execute only the new gate-controller wiring; inherited gate subprocesses
            # are NOT run against the minimal synthetic repository.
            write_frozen(folder / (name + ".log"), b"synthetic child\n")
            freeze_json(folder / (name + ".json"), {"synthetic": True})
            return sha(self.combined_manifest) if name == "manifest" else expected
        runner = SimpleNamespace(REPO=self.repo,
                                 CHECKS={name: args[3:] for name, args in c.expected_commands().items()},
                                 run_gate=fake_gate)
        with patch.object(gates, "load_module", return_value=runner), \
                patch.object(d.linear, "gate", return_value=b"synthetic inherited gates"), \
                contextlib.redirect_stdout(io.StringIO()):
            self.git("checkout", "--quiet", "--detach", self.closure)
            self.git("merge", "--no-commit", "--no-ff", self.incoming)
            gates.main("merge", self.closure, "-", self.closure, "-",
                       str(self.area / ("actual-mode-merge-" + uuid.uuid4().hex)))
            self.git("merge", "--abort")
            self.git("checkout", "--quiet", "--detach", self.merged)
            gates.main("committed-merge", self.closure, self.merged, self.merged, "-",
                       str(self.area / ("actual-mode-committed-merge-" + uuid.uuid4().hex)))
            for path, raw in self.archive.items():
                self.put(c.INTEGRATION + path, raw)
            self.put(c.PROGRESS, json_bytes(self.integration_ledger))
            gates.main("closure", self.closure, self.merged, self.merged, str(self.plan_path),
                       str(self.area / ("actual-mode-closure-" + uuid.uuid4().hex)))
            self.git("add", "--all")
            # The exact pending tree is identical to an already-created unsigned fixture I.
            self.git("checkout", "--quiet", "--detach", self.integrated)
            gates.main("committed-closure", self.closure, self.merged, self.integrated, str(self.plan_path),
                       str(self.area / ("actual-mode-committed-closure-" + uuid.uuid4().hex)))

    def test_recorder_receipt_sign_push_zip_equality_and_checkpoint_pipeline(self):
        self.git("checkout", "--quiet", "--detach", self.integrated)
        manifest = self.combined_manifest
        first_zip = self.area / "published-zip"
        first_archive = self.zip_fixture(first_zip, self.integrated)
        narrative = self.area / "narrative.json"
        freeze_json(narrative, {"reviewIdentity": "Synthetic only.", "changeSummary": "No actual publication."})
        closure_ci = self.ci_fixture(self.integrated)
        out = self.area / "record-output"
        remote = {"head": self.integrated}
        comments = []
        commands = []
        def api(git, *args):
            if args[:2] == ("run", "view"):
                return json_bytes(self.ci_fixture(remote["head"]))
            if args[0] == "api" and args[1].startswith("repos/") and "/commits/" in args[1]:
                commit = args[1].split("/")[-1]
                return json_bytes({"sha": commit, "commit": {"verification": {"verified": True}},
                                   "author": {"login": "stop-cran"}, "committer": {"login": "stop-cran"},
                                   "html_url": "https://example.invalid/commit/" + commit})
            if args[0] == "api" and "issues/60/comments?" in args[1]:
                return json_bytes(comments)
            if args[:3] == ("api", "--method", "POST"):
                request = json.loads(frozen(args[-1]))
                row = {"id": 1, "body": request["body"], "user": {"login": "stop-cran"}}
                comments.append(row)
                return json_bytes(row)
            if args[0] == "api" and args[1].endswith("issues/comments/1"):
                return json_bytes(comments[0])
            raise AssertionError("Unexpected synthetic API: " + repr(args))
        def remote_head(git, expected):
            c.require(remote["head"] == expected, "Synthetic remote advanced")
        def command(git, args, env=None, timeout=None, log=None):
            commands.append(args)
            self.assertFalse(any(value.startswith("--force") for value in args))
            if "commit" in args:
                self.assertIn("-S", args)
                self.assertEqual(timeout, 75)
                log.write(b"Unsigned synthetic commit; signature observation simulated.\n")
                self.commit("receipt simulated signature")
            elif "push" in args:
                self.assertEqual(args[-2:], ["origin", "HEAD:refs/heads/main"])
                remote["head"] = self.git("rev-parse", "HEAD").decode().strip()
            else:
                raise AssertionError(args)
            return b"synthetic\n"
        with patch.object(d, "api", side_effect=api), patch.object(d, "remote_head", side_effect=remote_head), \
                patch.object(d, "command", side_effect=command), patch.object(d, "owner_env", return_value={}), \
                patch.object(d.linear, "gate", return_value=b"synthetic inherited gates"), \
                contextlib.redirect_stdout(io.StringIO()):
            recorder.record(str(self.plan_path), self.integrated, str(closure_ci["databaseId"]),
                            str(first_zip / "receipt.json"), str(narrative),
                            self.pre_closure["path"], self.post_closure["path"], str(out))
            proof_path = self.repo / c.PUBLICATION / "provenance.json"
            proof = json.loads(frozen(proof_path))
            self.assertEqual(proof["planSha256"], sha(frozen(self.plan_path)))
            d.sign("receipt", str(self.plan_path), self.integrated, str(self.area / "sign-output"))
            receipt = self.git("rev-parse", "HEAD").decode().strip()
            self.assertNotEqual(receipt, self.integrated)
            d.receipt_tree(self.git, self.plan, self.integrated, receipt, sha(frozen(self.plan_path)))
            remote["head"] = self.incoming
            self.git("checkout", "--quiet", "--detach", self.integrated)
            d.push("closure", str(self.plan_path), self.integrated,
                   self.pre_closure["path"], self.post_closure["path"], str(self.area / "push-i"))
            self.git("checkout", "--quiet", "--detach", receipt)
            d.push("receipt", str(self.plan_path), receipt, None, None, str(self.area / "push-r"))
            self.assertEqual(remote["head"], receipt)
            second_zip = self.area / "receipt-zip"
            self.zip_fixture(second_zip, receipt)
            ci_path = self.area / "receipt-ci.json"
            freeze_json(ci_path, self.ci_fixture(receipt))
            equal_out = self.area / "equal-output"
            d.equal(str(self.plan_path), self.integrated, receipt, str(first_zip), str(second_zip),
                    str(ci_path), str(equal_out))
            request = out / "issue60-request.json"
            d.checkpoint(str(self.plan_path), self.integrated, receipt, str(ci_path),
                         str(equal_out / "equality.json"), str(request), str(self.area / "checkpoint"))
            self.assertEqual(len(comments), 1)
            self.assertEqual(len(commands), 3)
            # Repeated checkpoint is idempotent and only verifies the identical owner comment.
            d.checkpoint(str(self.plan_path), self.integrated, receipt, str(ci_path),
                         str(equal_out / "equality.json"), str(request), str(self.area / "checkpoint-readback"))
            self.assertEqual(len(comments), 1)
        self.git("checkout", "--quiet", "--detach", self.integrated)

    @classmethod
    def ci_fixture(cls, commit):
        return {"databaseId": 123, "headSha": commit, "workflowName": "Validate content",
                "status": "completed", "conclusion": "success", "url": "https://example.invalid/ci/123"}

    @classmethod
    def zip_fixture(cls, folder, commit):
        folder.mkdir()
        path = folder / f"zipball-{commit[:12]}.zip"
        with zipfile.ZipFile(path, "w") as archive:
            root = "synthetic-" + commit[:7] + "/"
            archive.writestr(root, b"")
            # Full-sized synthetic served-tree shape, not real runtime content validation.
            for number in range(8750):
                archive.writestr(root + f"entry-{number}.txt", b"fixture\n")
        path.chmod(stat.S_IREAD)
        receipt = {"commit": commit, "pendingChecks": [], "memory": {"breach": None},
                   "sha256": sha(frozen(path)), "manifestSha256": sha(cls.combined_manifest),
                   "contentVersion": json.loads(cls.combined_manifest)["contentVersion"],
                   "verifiedRuntimeHashes": 8747, "zipEntries": 8751}
        for key in ("manifestEqual", "manifestBytesEqualGitBlob", "zipNamesEqualExportedTree",
                    "allPublishingBudgetsPassed", "contributorEvidenceExcluded", "perFileLimitsAndSafePathsPassed"):
            receipt[key] = True
        freeze_json(folder / "receipt.json", receipt)
        return receipt


if __name__ == "__main__":
    unittest.main(verbosity=2)
