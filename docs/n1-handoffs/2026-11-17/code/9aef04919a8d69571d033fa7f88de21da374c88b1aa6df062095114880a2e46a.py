"""Guarded synthetic controls. No real reviewer/repository/network/signing operation.

Existing fixture Git shim supplies signature observations only on unsigned synthetic
commits. Full CLI entry smoke uses --help and fail-closed output scopes. Pipeline
tests explicitly substitute synthetic Git/accepted-prior/event-home seams; none of
these fixtures is an actual review/admission/signature.
"""
import contextlib
import copy
import datetime as dt
import io
import json
import os
import subprocess
import sys
import unittest
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
TOOLS = Path(r"C:\Users\stop-\n1-kanji-workspace\review-tools")
sys.path.insert(0, str(TOOLS))
import b134_integration_confirmation_v1 as tool
import b134_revision_proofs_v1 as proofs
import b134_integrated_v1 as base
from common import freeze_json, frozen, json_bytes, load_module, sha, start_guard, write_frozen
GATE_DRAFT = ROOT / "superseded" / "b134_revision_gates_v1.py"
gates = load_module("b134_superseded_revision_gates_fixture", GATE_DRAFT)


class Controls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard, _ = start_guard("B134 bounded confirmation synthetic controls")
        cls.area = ROOT / ("synthetic-" + uuid.uuid4().hex)
        cls.area.mkdir()
        cls.fixture = load_module("b134_confirmation_fixture", ROOT.parent / "integration-prep-001" / "test-integration.py")
        cls.fixture.ROOT = ROOT
        cls.repo = cls.area / "repo"
        cls.repo.mkdir()
        cls.git = cls.fixture.FixtureGit(cls.repo, cls.guard)
        cls.git("init", "--quiet")
        for key, value in (("user.name", "Synthetic owner"), ("user.email", base.OWNER),
                           ("user.signingkey", base.FINGERPRINT), ("commit.gpgsign", "false"),
                           ("core.autocrlf", "false"), ("core.longpaths", "true")):
            cls.git("config", key, value)
        cls.git("remote", "add", "origin", "https://github.com/stop-cran/learning-japanese.git")
        cls.old_card = b"synthetic old purple\n"
        cls.new_card = b"synthetic revised purple\n"
        cls.put(gates.CARD, cls.old_card)
        cls.put("words/\u7d2b.md", b"unchanged support\n")
        for path in ("kanji/\u6fc3.md", "kanji/\u98df.md"):
            cls.put(path, b"synthetic complete unchanged comparison\n")
        cls.put("docs/original-claims.json", b'{"originalObligations":29}\n')
        cls.put("tools/build_manifest.py", b"# synthetic builder unchanged\n")
        for name in base.HELPERS:
            cls.put("docs/n1-sources/batch-134/producers/" + name, ("# synthetic " + name).encode())
        cls.old_manifest = {"schemaVersion": 1, "contentVersion": "initial",
                            "files": {gates.CARD: sha(cls.old_card), **{f"kanji/fake-{i}.md": "0"*64 for i in range(8746)}}}
        cls.put("manifest.json", (json.dumps(cls.old_manifest, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode())
        cls.old = cls.commit("synthetic original")
        cls.put(gates.CARD, cls.new_card)
        cls.put("docs/n1-sources/batch-134/revision-evidence.txt",
                b"PRIVATE_OPPOSITE_REVIEW_RESULT must stay coordinator-only\n")
        new = copy.deepcopy(cls.old_manifest)
        new["files"][gates.CARD] = sha(cls.new_card)
        payload = {key: value for key, value in new.items() if key not in ("schemaVersion", "contentVersion")}
        new["contentVersion"] = sha(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())[:16]
        cls.new_manifest = (json.dumps(new, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode()
        cls.put("manifest.json", cls.new_manifest)
        cls.candidate = cls.commit("synthetic revision")
        cls.copies = cls.area / "tools"
        for name in ("b134_integration_confirmation_v1.py", "b134_revision_proofs_v1.py"):
            write_frozen(cls.copies / name, (TOOLS / name).read_bytes())
        write_frozen(cls.copies / "b134_revision_gates_v1.py", GATE_DRAFT.read_bytes())
        cls.patches = [
            patch.object(base, "REVIEWED", cls.old), patch.object(base, "REPO", cls.repo),
            patch.object(base, "SCRATCH", cls.area / "scratch"),
            patch.object(tool, "ROOT", cls.area), patch.object(gates, "ROOT", cls.area),
            patch.object(tool, "__file__", str(cls.copies / "b134_integration_confirmation_v1.py")),
            patch.object(gates, "__file__", str(cls.copies / "b134_revision_gates_v1.py")),
            patch.object(tool, "Git", lambda *args: cls.git), patch.object(gates, "Git", lambda *args: cls.git)]
        for item in cls.patches:
            item.start()
        for name in base.HELPERS:
            write_frozen(base.SCRATCH / name, ("# synthetic " + name).encode())
        cls.gate_refs = {}
        for mode in ("author", "committed"):
            cls.gate_refs[mode] = cls.gate_fixture(mode)
        cls.scope_ref, cls.gates_ref = cls.proof_fixture()
        cls.prior_report = write_frozen(cls.area / "own-report.md", b"# synthetic own report\n### F1: own claim\n")
        cls.prior_adjudication = write_frozen(cls.area / "own-adjudication.json", b'{"verdict":"NEEDS FIX","claim":"own"}\n')
        cls.prior_refs = {"report": cls.small(cls.prior_report), "adjudication": cls.small(cls.prior_adjudication)}
        prior_raw = b"".join(json.dumps(row).encode() + b"\n" for row in cls.prefix())
        write_frozen(cls.area / "prior-audit" / "events.jsonl", prior_raw)
        prior_audit = cls.small(freeze_json(cls.area / "prior-audit" / "audit.json", {"eventsSha256": sha(prior_raw)}))
        prior_final = cls.small(freeze_json(cls.area / "prior-final.json", {"audit": prior_audit}))
        cls.spec = {"schemaVersion": 1, "mode": "revision", "scope": tool.REVISION_SCOPE,
                    "family": "claude", "run": "N1-B134-CLAUDE-REVISION-001",
                    "session": tool.OWN["claude"], "candidate": cls.candidate,
                    "scopeProof": cls.scope_ref, "gateProof": cls.gates_ref, "prior": {"final": prior_final},
                    "neutralEvidence": {"exactDeltaReadCompletely": True, "noOppositeFamilyResults": True,
                        "addedEvidenceTreatment": "private-raw-neutral-hash-inventory",
                        "addedPaths": ["docs/n1-sources/batch-134/revision-evidence.txt"]},
                    "obligations": [{"id": "F1", "claim": "Own synthetic claim"},
                                    {"id": "C1", "claim": "Own synthetic boundary"}],
                    "additionalSources": []}
        cls.spec_path = cls.area / "spec.json"
        freeze_json(cls.spec_path, cls.spec)

    @classmethod
    def tearDownClass(cls):
        for item in reversed(cls.patches):
            item.stop()
        freeze_json(cls.area / "memory.json", cls.guard.finish())

    @staticmethod
    def small(item):
        return {key: item[key] for key in ("path", "sha256")}

    @classmethod
    def put(cls, name, raw):
        path = cls.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            path.chmod(0o644)
        path.write_bytes(raw)

    @classmethod
    def commit(cls, title):
        cls.git("add", "--all")
        cls.git("-c", "commit.gpgsign=false", "commit", "--quiet", "-m", title, "-m", base.TRAILER.decode())
        return cls.git("rev-parse", "HEAD").decode().strip()

    @classmethod
    def gate_fixture(cls, mode):
        folder = cls.area / ("gate-" + mode)
        helpers = {name: sha(frozen(base.SCRATCH / name)) for name in base.HELPERS}
        logs = {}
        for number, name in enumerate(base.ORDER):
            raw = b"SYNTHETIC gate; not actual host execution\n"
            write_frozen(folder / (name + ".log"), raw)
            receipt = {"gate": name, "exitCode": 0, "childExitCodeAfterCleanup": 0,
                       "cleanupError": None, "activeError": None, "memory": {"breach": None},
                       "guardSha256": base.GUARD_SHA, "command": base.expected_commands()[name],
                       "cwd": str(cls.repo), "base": base.BASE, "logSha256": sha(raw),
                       "runnerSha256": helpers["run_134_gates.py"], "commonHelperSha256": helpers["common_134.py"],
                       "boundedLauncherSha256": helpers["bounded_launch_134.py"], "waitTimeoutSeconds": .1,
                       "cleanupTimeoutSecondsPerStage": 10, "startedAt": f"{number:02d}", "completedAt": f"{number:02d}",
                       "manifestSha256": sha(cls.new_manifest) if name.startswith("manifest") else None,
                       "manifestReproducible": name == "manifest-rebuild"}
            item = freeze_json(folder / (name + ".json"), receipt)
            logs[name] = {"receiptSha256": item["sha256"], "logSha256": sha(raw)}
        result = {"status": "PASS_REVISION_GATES_ONLY", "mode": mode,
                  "head": cls.old if mode == "author" else cls.candidate,
                  "candidate": None if mode == "author" else cls.candidate, "priorSnapshot": cls.old,
                  "treeInventorySha256": gates.tree_digest(base.tree(cls.git, cls.candidate)),
                  "helperHashes": helpers, "checks": base.ORDER, "serial": True,
                  "manifestSha256": sha(cls.new_manifest), "producerSha256": sha(GATE_DRAFT.read_bytes()),
                  "commands": base.expected_commands(), "memory": {"breach": None}, "logs": logs}
        return cls.small(freeze_json(folder / "summary.json", result))

    @classmethod
    def proof_fixture(cls):
        memory = json.loads(frozen(ROOT.parent / "integration-prep-test-004" / "receipt.json"))["memory"]
        before, after = base.tree(cls.git, cls.old), base.tree(cls.git, cls.candidate)
        changed = {p: sha(base.blob(cls.git, cls.candidate, p)) for p in after if before.get(p) != after[p]}
        scope = {"batch": 134, "status": "PASS", "reviewed": cls.old, "commit": cls.candidate,
                 "lineageDepth": 1, "verifierSha256": proofs.PRODUCERS["scope"][1], "memory": memory,
                 "signedFiles": changed, "card": {"priorExclusions": 56, "exclusions": 58},
                 "unchangedComparisonCards": {p: sha(base.blob(cls.git, cls.candidate, p))
                                               for p in ("kanji/\u6fc3.md", "kanji/\u98df.md")},
                 "manifest": {"runtimeEntries": 8747}, "evidencePaths": sorted(after.keys() - before.keys()),
                 "bindings": {"snapshot/" + p: cls.small(write_frozen(cls.area / "scope" / "snapshot" / p,
                              base.blob(cls.git, cls.candidate, p))) for p in changed}}
        scope_ref = cls.small(freeze_json(cls.area / "scope" / "verification.json", scope))
        captured = {"scope-proof.json": cls.small(write_frozen(cls.area / "gate-proof" / "scope-proof.json",
                                                              frozen(scope_ref["path"])))}
        groups = {}
        for mode, old_mode in (("working", "author"), ("committed", "committed")):
            original = Path(cls.gate_refs[old_mode]["path"]).parent
            summary = json.loads(frozen(original / "summary.json"))
            summary["mode"] = mode
            row = cls.small(freeze_json(cls.area / "gate-proof" / mode / "summary.json", summary))
            captured[mode + "/summary.json"] = row
            bindings = []
            for name in base.ORDER:
                bindings.append({"gate": name, **summary["logs"][name]})
                for suffix in ("json", "log"):
                    label = f"{mode}/{name}.{suffix}"
                    captured[label] = cls.small(write_frozen(cls.area / "gate-proof" / label, frozen(original / f"{name}.{suffix}")))
            actual_inventory_order = ["lint", "quiz-safety", "linkplan", "reading-exposure",
                                      "unittest", "validate", "manifest", "manifest-rebuild", "budget", "vocabulary"]
            bindings.sort(key=lambda binding: actual_inventory_order.index(binding["gate"]))
            groups[mode] = {"summarySha256": row["sha256"], "quizWarnings": 51, "latentReadingPairs": 1, "gates": bindings}
        gates_ref = cls.small(freeze_json(cls.area / "gate-proof" / "verification.json", {
            "batch": 134, "status": "PASS", "candidate": cls.candidate,
            "verifierSha256": proofs.PRODUCERS["gates"][1], "sourceProof": scope_ref,
            "manifestSha256": sha(cls.new_manifest), "groups": groups, "evidence": captured, "memory": memory}))
        return scope_ref, gates_ref

    def test_01_revision_objects_manifest_and_gate_bindings(self):
        result = gates.verify_revision(self.git, self.candidate)
        self.assertEqual(result["runtimeEntries"], 8747)
        gates.verify_gates(self.git, self.candidate, self.gate_refs, sha(self.new_manifest))
        after = base.tree(self.git, self.candidate)
        wrong = {**after, "docs/original-claims.json": ("100644", "blob", "0"*40)}
        with self.assertRaises(ValueError):
            gates.verify_revision(self.git, staged=wrong, read=lambda p: (self.repo / p).read_bytes())
        wrong_refs = copy.deepcopy(self.gate_refs)
        wrong_refs["committed"]["sha256"] = "0"*64
        with self.assertRaises(ValueError):
            gates.verify_gates(self.git, self.candidate, wrong_refs, sha(self.new_manifest))
        self.assertEqual(proofs.verify(self.git, self.candidate, self.scope_ref, self.gates_ref)["runtimeEntries"], 8747)
        wrong_scope = {**self.scope_ref, "sha256": "0"*64}
        with self.assertRaises(ValueError):
            proofs.verify(self.git, self.candidate, wrong_scope, self.gates_ref)

    def test_02_real_cli_entry_help_and_scope_fail_closed(self):
        commands = [[sys.executable, "-B", str(TOOLS / name), *args] for name, args in (
            ("b134_integration_confirmation_v1.py", ["--help"]),
            *[("b134_integration_confirmation_v1.py", [action, "--help"]) for action in ("prepare", "admit", "final", "accept")],
            ("b134_integration_confirmation_v1.py", ["prepare", str(self.spec_path), str(self.area / "forbidden-out")]))]
        observations = []
        for command in commands:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       env={**os.environ, "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1"})
            try:
                while True:
                    try:
                        stdout, stderr = process.communicate(timeout=.1)
                        break
                    except subprocess.TimeoutExpired:
                        self.guard.check()
            finally:
                self.fixture.FixtureGit.stop(process)
            expected = 0 if "--help" in command else 1
            self.assertEqual(process.returncode, expected, stderr.decode("utf-8", "replace"))
            if expected:
                self.assertIn(b"NEW direct review output", stderr)
            observations.append({"command": command, "exitCode": process.returncode,
                                 "stdoutSha256": sha(stdout), "stderrSha256": sha(stderr)})
        freeze_json(self.area / "real-cli-smoke.json", observations)

    def test_03_exact_context_budget_compaction_and_model_rejections(self):
        rows = self.prefix()
        checked = tool.context(rows, "claude", tool.OWN["claude"], 20000)
        self.assertLessEqual(checked["forecast"], 700000)
        for changed in (
            rows + [{"type": "session.compaction_start", "data": {}}],
            [{**rows[0], "data": {**rows[0]["data"], "contextTier": "default"}}, *rows[1:]],
            [rows[0], {"type": "session.usage_record", "data": {"usage": {
                "model": "claude-opus-5.5", "responseModel": "claude-opus-5.5",
                "inputTokens": 690000, "maxPromptTokens": 952000}}}],
        ):
            with self.assertRaises(ValueError):
                tool.context(changed, "claude", tool.OWN["claude"], 20000)

    def test_04_unknown_semantics_extra_users_and_deliveries_rejected(self):
        prefix = self.prefix()
        with self.assertRaises(ValueError):
            tool.event_envelope(prefix, [{"type": "unrecognized.semantic_activity", "data": {}}],
                                "claude", tool.OWN["claude"])
        with self.assertRaises(ValueError):
            tool.event_envelope(prefix, [{"type": "assistant.turn_start", "data": {"agentMode": "autopilot"}}],
                                "claude", tool.OWN["claude"])

    def test_05_fresh_roster_requires_complete_idle_interactive(self):
        now = dt.datetime.now(dt.timezone.utc)
        roster = [{"id": tool.COORDINATOR}, {"id": tool.OWN["claude"]}]
        rows = [{"id": item["id"], "activity": {"status": "idle"}, "mode": "interactive"} for item in roster]
        rows[0]["activity"]["status"] = "busy"
        status = {"sessions": rows, "summary": {"total": 2}}
        observation = {"observedAt": now.isoformat(),
                       "status": self.small(freeze_json(self.area / "status.json", status)),
                       "roster": self.small(freeze_json(self.area / "roster.json", roster))}
        self.assertEqual(tool.roster_check(observation, tool.OWN["claude"], now), 2)
        with self.assertRaises(ValueError):
            tool.roster_check(observation, tool.OWN["claude"], now + dt.timedelta(seconds=121))
        wrong = copy.deepcopy(status); wrong["summary"]["total"] = 3
        observation["status"] = self.small(freeze_json(self.area / "bad-status.json", wrong))
        with self.assertRaises(ValueError):
            tool.roster_check(observation, tool.OWN["claude"], now)

    @staticmethod
    def prefix():
        return [{"type": "session.start", "data": {"sessionId": tool.OWN["claude"],
                  "selectedModel": "claude-opus-5.5", "contextTier": "long_context"}},
                {"type": "session.usage_record", "data": {"usage": {"model": "claude-opus-5.5",
                  "responseModel": "claude-opus-5.5", "inputTokens": 100000, "maxPromptTokens": 952000}}},
                   {"type": "assistant.turn_start", "data": {"agentMode": "interactive"}},
                   {"type": "assistant.message", "data": {"model": "claude-opus-5.5", "content": "Synthetic prior complete"}},
                   {"type": "assistant.turn_end", "data": {}}]

    def test_06_prepare_full_dossier_and_strict_actual_byte_pipeline(self):
        out = self.area / "prepared"
        previous = {"report": self.prior_refs["report"]}
        with patch.object(tool, "prior_evidence", return_value=(self.prior_refs, previous, {"verdict": "NEEDS FIX"})):
            self.assertEqual(tool.main(["prepare", str(self.spec_path), str(out)]), 0)
        record, config, spec, chain = tool.preflight(out / "preflight.json")
        self.assertEqual(record["priorRawVerdict"], "NEEDS FIX")
        rebuilt = tool.reconstruct(chain)
        self.assertEqual(rebuilt["snapshot/kanji/\u7d2b.md"], self.new_card)
        self.assertEqual(rebuilt["base/kanji/\u7d2b.md"], self.old_card)
        self.assertNotIn("gpt", " ".join(rebuilt))
        self.assertNotIn(b"PRIVATE_OPPOSITE_REVIEW_RESULT", b"".join(rebuilt.values()))
        self.assertIn(b"PRIVATE_OPPOSITE_REVIEW_RESULT", tool.read(record["preservation"]["privateCompleteObjectDelta"]))
        text = self.report_text(record, chain)
        report = Path(config["report"])
        home = self.area / "synthetic-home"
        live = home / ".copilot" / "session-state" / record["session"] / "events.jsonl"
        live.parent.mkdir(parents=True)
        live.write_bytes(b"".join(json.dumps(row).encode() + b"\n" for row in self.prefix()))
        now = dt.datetime.now(dt.timezone.utc)
        rows = [{"id": sid, "activity": {"status": "idle"}, "mode": "interactive"}
                for sid in (tool.COORDINATOR, record["session"])]
        observation = {"observedAt": now.isoformat(),
            "status": self.small(freeze_json(self.area / "pipeline-status.json", {"sessions": rows, "summary": {"total": 2}})),
            "roster": self.small(freeze_json(self.area / "pipeline-roster.json", [{"id": row["id"]} for row in rows]))}
        observation_path = self.area / "observation.json"
        freeze_json(observation_path, observation)
        admitted = self.area / "admitted"
        with patch.object(Path, "home", return_value=home), patch.object(
                tool, "prior_evidence", return_value=(self.prior_refs, previous, {"verdict": "NEEDS FIX"})):
            self.assertEqual(tool.main(["admit", str(out / "preflight.json"), str(observation_path), str(admitted)]), 0)
        admission = json.loads(frozen(admitted / "admission.json"))
        report.write_text(text, encoding="utf-8", newline="")
        events, _ = self.events(record, config, chain, text)
        raw = b"".join(json.dumps(row).encode() + b"\n" for row in events)
        audit, telemetry, structure = tool.audit_snapshot(raw, record, config, chain, admission)
        self.assertEqual(audit["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK")
        self.assertEqual(structure["dispositions"], {"F1": "RESOLVED", "C1": "DISPUTE ACCEPTED"})
        self.assertEqual(structure["confirmation"], "CONFIRMED")
        for mutation in ("returned-bytes", "extra-user", "bad-path", "late-kickoff", "bad-completion", "bad-readback"):
            altered = copy.deepcopy(events)
            if mutation == "returned-bytes":
                item = next(row for row in altered if row["type"] == "tool.execution_complete")
                item["data"]["result"]["content"] += "TRUNCATED"
            elif mutation == "extra-user":
                altered.append({"type": "user.message", "data": {"content": "", "source": "autopilot"}})
            elif mutation == "bad-path":
                call = next(row for row in altered if row["type"] == "assistant.message" and row["data"].get("toolRequests"))
                call["data"]["toolRequests"][0]["arguments"]["path"] += "-other"
            elif mutation == "late-kickoff":
                next(row for row in altered if row["type"] == "user.message")["timestamp"] = "2099-01-01T00:00:00Z"
            elif mutation == "bad-completion":
                for row in altered:
                    if row["type"] == "assistant.message":
                        for call in row["data"].get("toolRequests", []):
                            if call["name"] == "functions.send_session_message":
                                call["arguments"]["message"] = "CONFIRMED with qualifications"
                    if row["type"] == "tool.execution_start" and row["data"]["toolName"] == "send_session_message":
                        row["data"]["arguments"]["message"] = "CONFIRMED with qualifications"
            else:
                complete = [row for row in altered if row["type"] == "tool.execution_complete"]
                complete[-2]["data"]["result"]["content"] = text + "mismatch"
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                bad = b"".join(json.dumps(row).encode() + b"\n" for row in altered)
                tool.audit_snapshot(bad, record, config, chain, admission)
        for source in ("not-opened.md:1", "proof/preservation.json:999999", "proof/preservation.json:1,3"):
            changed = text.replace("proof/preservation.json:1", source)
            result = tool.check_structure(changed, record, chain, "CONFIRMED")
            self.assertEqual(result["status"], "FAIL")
        live.write_bytes(raw)
        final_dir, accept_dir = self.area / "final", self.area / "accepted"
        with patch.object(Path, "home", return_value=home):
            self.assertEqual(tool.main(["final", str(out / "preflight.json"),
                                        str(admitted / "admission.json"), str(final_dir)]), 0)
        final_ref = tool.ref(final_dir / "final.json")
        decision = {"final": final_ref, "report": tool.ref(report), "candidate": record["candidate"],
            "run": record["run"], "session": record["session"], "family": record["family"],
            "verdict": "CONFIRMED", "scope": record["scope"], "reportReadCompletely": True,
            "claimChecks": [{"claim": row["id"], "evidence": "synthetic own source", "disposition": "synthetic accepted"}
                            for row in spec["obligations"]], "limitsPreserved": ["Prior raw NEEDS FIX"],
            "acceptedNewFindings": [], "openClaimIds": [], "dispositions": structure["dispositions"]}
        decision_path = self.area / "decision.json"
        freeze_json(decision_path, decision)
        self.assertEqual(tool.main(["accept", str(final_dir / "final.json"), str(decision_path), str(accept_dir)]), 0)
        accepted = json.loads(frozen(accept_dir / "acceptance.json"))
        self.assertTrue(accepted["confirmationAccepted"])
        self.assertFalse(accepted["publicationAccepted"])
        self.assertEqual(accepted["priorRawVerdict"], "NEEDS FIX")
        self.assertEqual(accepted["mode"], "revision")
        # A revision confirmation is deliberately NOT a fresh/integration acceptance.
        with self.assertRaises(ValueError):
            base.accepted({"merge": self.candidate, "confirmations": {
                "claude": tool.ref(accept_dir / "acceptance.json"), "gpt": tool.ref(accept_dir / "acceptance.json")}})

    def test_07_exact_own_gpt_F1_F2_C1_C6_inventory(self):
        spec = copy.deepcopy(self.spec)
        spec.update(family="gpt", session=tool.OWN["gpt"], run="N1-B134-GPT-REVISION-001")
        spec["prior"]["review"] = {"family": "gpt", "session": tool.OWN["gpt"],
            "run": "N1-B134-GPT-FRESH-003", "snapshot": self.old, "acceptance": self.prior_refs["adjudication"]}
        spec["prior"]["preflight"] = {}
        required = ["F1", "F2"] + ["C" + str(i) for i in range(1, 7)]
        spec["obligations"] = [{"id": name, "claim": "Own explicit synthetic obligation"} for name in required]
        claims = {"acceptedFindings": ["F1", "F2"], "openClaimIds": ["F1", "F2"],
                  "coordinatorClaimIds": required[2:]}
        with patch.object(tool, "collect_replacement_record", return_value=(self.prior_refs, {}, claims)):
            self.assertEqual(tool.prior_evidence(spec)[2]["verdict"], "NEEDS FIX")
            spec["obligations"].pop()
            with self.assertRaises(ValueError):
                tool.prior_evidence(spec)
            spec["prior"]["review"]["family"] = "claude"
            with self.assertRaises(ValueError):
                tool.prior_evidence(spec)

    @staticmethod
    def report_text(record, chain):
        return f"""# B134 confirmation - {record['run']}
## Snapshot
Commit: {record['candidate']}
Model: claude-opus-5.5 long_context
## Scope
Chain: All {len(chain['segments'])} complete segments
Fetches: 0
## Dispositions
- F1 - RESOLVED - Own synthetic evidence
- C1 - DISPUTE ACCEPTED - Own synthetic boundary retained as a limit
## Verdicts
Correctness: CLEAN
Scoped coverage: CLEAN
Consistency and quiz safety: CLEAN
Comprehensibility: CLEAN
## Confirmation
Verdict: CONFIRMED
Basis: Exact bounded impact (proof/preservation.json:1).
## Findings
None.
## Optional
None.
## Limits
- L1: {record['scope']}
- L2: Earlier raw NEEDS FIX and native/device limits are preserved.
"""

    def events(self, record, config, chain, text):
        prefix = self.prefix()
        raw = b"".join(json.dumps(row).encode() + b"\n" for row in prefix)
        saved = self.small(write_frozen(self.area / ("prefix-" + uuid.uuid4().hex + ".jsonl"), raw))
        created = dt.datetime.now(dt.timezone.utc)
        admission = {"prefix": saved, "offset": len(raw), "createdAt": created.isoformat(),
                     "kickoff": frozen(config["kickoff"]).decode()}
        events = prefix + [{"type": "user.message", "timestamp": created.isoformat(),
                            "data": {"source": "agent-" + tool.COORDINATOR, "content": admission["kickoff"]}}]
        calls = [("view", {"path": config["prompt"], "forceReadLargeFiles": True}, frozen(config["prompt"]).decode())]
        calls += [("view", {"path": row["path"], "forceReadLargeFiles": True}, tool.read(row).decode()) for row in chain["segments"]]
        patch_text = "*** Begin Patch\n*** Add File: " + config["report"] + "\n" + "".join("+" + line + "\n" for line in text.splitlines()) + "*** End Patch\n"
        calls += [("apply_patch", patch_text, ""), ("view", {"path": config["report"], "forceReadLargeFiles": True}, text),
                  ("send_session_message", {"session_id": tool.COORDINATOR, "message": "CONFIRMED"}, "delivered")]
        for number, (name, args, returned) in enumerate(calls):
            cid = str(number)
            events += [
                {"type": "assistant.turn_start", "data": {"agentMode": "interactive"}},
                {"type": "session.usage_record", "data": self.prefix()[1]["data"]},
                {"type": "assistant.message", "data": {"model": "claude-opus-5.5", "apiCallId": "api-" + cid,
                    "toolRequests": [{"name": "functions." + name, "arguments": args, "toolCallId": cid}]}},
                {"type": "tool.execution_start", "data": {"toolCallId": cid, "toolName": name, "arguments": args}},
                {"type": "tool.execution_complete", "data": {"toolCallId": cid, "success": True, "result": {"content": returned}}},
                {"type": "assistant.turn_end", "data": {}}]
        return events, admission


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False).result
    if not result.wasSuccessful():
        raise SystemExit(1)
    success = freeze_json(ROOT / ("successful-controls-" + uuid.uuid4().hex + ".json"), {
        "syntheticOnly": True, "actualReviewerAdmission": False, "testsRun": result.testsRun,
        "fixture": str(Controls.area), "testSha256": sha(Path(__file__).read_bytes()),
        "selectedTools": {name: sha((Controls.copies / name).read_bytes())
                          for name in ("b134_integration_confirmation_v1.py", "b134_revision_proofs_v1.py")}})
    print(json.dumps(success))
