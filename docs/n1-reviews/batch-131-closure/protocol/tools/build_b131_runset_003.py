"""Fresh003 preparation with real report directories; do not read retired reviewer observations."""
import json
from pathlib import Path

from b131_review_v3_common import (
    CORE, DEFAULT_PREFLIGHT, FORECAST, HERE, IMMUTABLE_BINDINGS, OLD_PREP, PACKET, TOOLS,
    freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen)
from b131_preflight_002 import verify_subset as verify_original_evidence
from b131_preflight_003 import path_inventory, validate_report_destination, verify_protocol


def once(text, before, after):
    require(text.count(before) == 1, "Successor anchor differs: " + before[:90])
    return text.replace(before, after)


def main():
    require(not HERE.exists(), "Preserve every003 output; use a successor after a failed partial build")
    guard, _ = start_guard("B131 fresh003 preparation")
    try:
        for path, digest in IMMUTABLE_BINDINGS:
            frozen(path, digest)
        verify_original_evidence(guard, initial=True)
        derivations = []

        def copy(source, destination, transform=None):
            raw = frozen(source)
            output = raw if transform is None else transform(raw.decode("utf-8").replace("\r\n", "\n")).encode("utf-8")
            if destination.suffix == ".py":
                compile(output.decode("utf-8"), str(destination), "exec")
            binding = write_frozen(destination, output)
            derivations.append({"source": str(source), "sourceSha256": sha(raw), "output": binding})
            guard.check()

        for name in ("batch.json", "derivation-verification-002.json", "review_chain.py",
                     "core-chain-compact-002.json", "check-report-structure.py", "check-run-context.py"):
            copy(OLD_PREP / name, HERE / name)
        freeze_json(HERE / "source-bindings-003.json", [
            {"path": str(path), "sha256": digest} for path, digest in IMMUTABLE_BINDINGS])

        def audit(text):
            text = text.replace("b131_review_v2_common", "b131_review_v3_common").replace(
                "b131_runtime_002", "b131_runtime_003")
            return once(text, "config, extension, phase1_text, phase2_text, original)",
                        "config, extension, phase1_text, phase2_text, original, require_fresh_report=not final)")
        copy(OLD_PREP / "audit-review.py", HERE / "audit-review.py", audit)

        def extension(text):
            text = text.replace("b131_review_v2_common", "b131_review_v3_common")
            text = text.replace("-extension-002", "-extension-003")
            anchor = '    args = parser.parse_args(argv)\n'
            text = once(text, anchor, anchor + '    require(args.run is not None, "Reuse the pinned core;003 only builds extensions")\n')
            anchor = "        else:\n            forecast = load_forecast()\n"
            return once(text, anchor, anchor + (
                "            from b131_review_v3_common import DEFAULT_PREFLIGHT\n"
                "            from b131_preflight_003 import validate_report_destination\n"
                "            specs = json.loads(frozen(DEFAULT_PREFLIGHT))['runs'].values()\n"
                "            validate_report_destination(next(spec for spec in specs if spec['run'] == args.run))\n"))
        copy(TOOLS / "prepare_chain_b131_002.py", TOOLS / "prepare_chain_b131_003.py", extension)

        def runtime(text):
            text = text.replace("b131_review_v2_common", "b131_review_v3_common")
            text = text.replace("prepare_chain_b131_002", "prepare_chain_b131_003")
            anchor = 'def validate_prepared_extension(config, chain, reply_text, phase2_text, phase1_audit_path):\n'
            return once(text, anchor, (
                "def validate_prepared_extension(config, chain, reply_text, phase2_text, phase1_audit_path,\n"
                "                                require_fresh_report=True):\n"
                "    from b131_preflight_003 import validate_report_destination\n"
                "    if require_fresh_report:\n"
                "        validate_report_destination(config)\n"))
        copy(TOOLS / "b131_runtime_002.py", TOOLS / "b131_runtime_003.py", runtime)

        def admission(text):
            text = text.replace("b131_review_v2_common", "b131_review_v3_common").replace(
                "b131_preflight_002", "b131_preflight_003")
            anchor = "def observe(argument, config, spec, record):\n"
            text = once(text, anchor, anchor + (
                "    from b131_preflight_003 import validate_report_destination\n"
                "    report_readiness = validate_report_destination(spec)\n"))
            anchor = '    record.update(status="ADMITTED_REVIEWER_STARTUP_ONLY", admitted=True,\n'
            return once(text, anchor,
                "    report_readiness = validate_report_destination(spec)\n"
                "    record['reportDestination'] = report_readiness\n" + anchor)
        copy(TOOLS / "b131_review_admission_002.py", TOOLS / "b131_review_admission_003.py", admission)

        def adapter(text):
            return text.replace("b131_review_v2_common", "b131_review_v3_common").replace(
                "preparation-v2-lifecycle-", "preparation-v3-lifecycle-")
        copy(TOOLS / "b131_lifecycle_process_003.py", TOOLS / "b131_lifecycle_process_004.py", adapter)

        def step(text):
            for before, after in (
                ("b131_review_v2_common", "b131_review_v3_common"),
                ("b131_lifecycle_process_003", "b131_lifecycle_process_004"),
                ("b131_review_admission_002", "b131_review_admission_003"),
                ("b131_runtime_002", "b131_runtime_003"),
                ("prepare_chain_b131_002.py", "prepare_chain_b131_003.py"),
                ("step_b131_neutral_004.py", "step_b131_neutral_005.py"),
                ("step_b131_neutral_001.py", "step_b131_neutral_005.py"),
                ("preflight-compact-002.json", "preflight-compact-003.json")):
                text = text.replace(before, after)
            anchor = '    spec = preflight["runs"][key]\n'
            return once(text, anchor, anchor + (
                "    if action in ('admit', 'launch', 'phase1'):\n"
                "        from b131_preflight_003 import validate_report_destination\n"
                "        validate_report_destination(spec)\n"))
        copy(TOOLS / "step_b131_neutral_004.py", TOOLS / "step_b131_neutral_005.py", step)

        def controls(text):
            for before, after in (
                ("b131_review_v2_common", "b131_review_v3_common"),
                ("b131_preflight_002", "b131_preflight_003"),
                ("b131_runtime_002", "b131_runtime_003"),
                ("prepare_chain_b131_002", "prepare_chain_b131_003"),
                ("b131_lifecycle_process_003.py", "b131_lifecycle_process_004.py"),
                ("preflight-compact-002.json", "preflight-compact-003.json")):
                text = text.replace(before, after)
            text = once(text, 'with patch.object(preflight, "compute_forecast", return_value=changed):',
                        'with patch("b131_preflight_002.compute_forecast", return_value=changed):')
            extra = '''
    def test_complete_two_phase_create_readback_and_final_audit(self):
        code, message_path, audit_path = self.build_synthetic_extension()
        self.assertEqual(code, 0)
        run = self.audit_config["run"]
        extension = json.loads(frozen(self.case / (run + "-extension.json")))
        message = frozen(message_path).decode("utf-8")
        report = self.case / "report-output" / "synthetic-report.md"
        report.parent.mkdir(parents=True)
        config = dict(self.audit_config, report=str(report))
        events = copy.deepcopy(self.events)
        events.append({"type": "user.message", "data": {
            "content": message, "source": "agent-" + config["coordinator"]}})
        counter = 0
        def call(name, args, returned):
            nonlocal counter
            counter += 1
            cid = "synthetic-final-" + str(counter)
            events.extend([
                {"type": "assistant.message", "data": {"model": "claude-fabricated",
                    "apiCallId": cid, "toolRequests": [
                        {"toolCallId": cid, "name": name, "arguments": args}]}},
                {"type": "tool.execution_complete", "data": {
                    "toolCallId": cid, "success": True, "result": {"content": returned}}}])
        for segment in extension["segments"]:
            call("view", {"path": segment["path"], "forceReadLargeFiles": True},
                 frozen(segment["path"]).decode("utf-8"))
        body = "synthetic undelivered report\\n"
        call("create", {"path": str(report), "file_text": body}, "fixture-only created")
        report.write_bytes(body.encode("utf-8"))
        call("view", {"path": str(report), "forceReadLargeFiles": True}, body)
        call("send_session_message", {"session_id": config["coordinator"], "message": "UNVERIFIED"},
             "fixture-only accepted")
        events.append({"type": "assistant.turn_end", "data": {}})
        freeze_json(self.case / (run + "-phase1.json"), {"auditDir": str(audit_path.parent)})
        with patch("b131_review_v3_common.HERE", self.case), patch.object(runtime, "HERE", self.case):
            result = AUDITOR.audit(events, config, self.chain, self.reference, extension,
                                   self.synthetic_list, message, final=True)
        self.assertEqual(result["status"], "FINAL_AUDIT_NEEDS_CLAIM_CHECK", result.get("breaches"))
        self.assertTrue(result["readbackVerified"])
        self.assertTrue(report.is_file())

'''
            return once(text, "\ndef main():\n", "\n" + extra + "\ndef main():\n")
        copy(TOOLS / "test_b131_compact_002.py", HERE / "test-controls-003.py", controls)
        freeze_json(HERE / "tooling-derivation-003.json", {
            "status": "FRESH_RUN_PATH_SUCCESSORS_ONLY", "derivations": derivations,
            "limits": "Read implementation and neutral prompt inputs only; no retired reviewer events, list, report or final opened."})

        old_preflight_path = OLD_PREP / "prompts/preflight-compact-002.json"
        old_preflight = json.loads(frozen(
            old_preflight_path, "b27accc6688abbeb77a0d318f5bbfc32cca22cd5ac00663d73e728a7004e916a"))
        neutral_spec = old_preflight["runs"]["claude"]
        neutral = frozen(neutral_spec["prompt"], neutral_spec["promptSha256"]).decode("utf-8")
        for name in ("review-claude-003", "review-gpt-003"):
            (HERE / "reports" / name).mkdir(parents=True)
        tool_names = (
            "common.py", "run_b127_tool.py", "b131_review_v2_common.py", "b131_review_v3_common.py",
            "b131_review_v2_derivations.py", "b131_capacity_002.py", "b131_preflight_002.py",
            "b131_preflight_003.py", "prepare_chain_b131_003.py", "b131_runtime_003.py",
            "b131_review_admission_003.py", "b131_lifecycle_process_004.py", "step_b131_neutral_005.py",
            "test_b131_preparation_003.py", "build_b131_runset_003.py")
        paths = [TOOLS / name for name in tool_names]
        paths += [HERE / name for name in (
            "batch.json", "derivation-verification-002.json", "review_chain.py",
            "core-chain-compact-002.json", "check-report-structure.py", "check-run-context.py",
            "audit-review.py", "source-bindings-003.json", "tooling-derivation-003.json", "test-controls-003.py")]
        paths += [path for path, _ in IMMUTABLE_BINDINGS]
        bindings = [{"path": str(path), "sha256": sha(frozen(path))} for path in paths]
        runs = {}
        for family in ("claude", "gpt"):
            run = "N1-B131-" + family.upper() + "-003"
            prompt = HERE / "prompts" / f"initial-{family}-003.txt"
            kickoff = HERE / "prompts" / f"kickoff-{family}-003.txt"
            report = HERE / "reports" / f"review-{family}-003" / f"initial-{family}-003.md"
            body = neutral.replace(neutral_spec["prompt"], str(prompt)).replace(
                neutral_spec["report"], str(report)).replace(neutral_spec["run"], run)
            # Only identity substrings outside replaced paths need switching for GPT.
            if family == "gpt":
                body = body.replace("-claude-", "-gpt-").replace("CLAUDE", "GPT")
            body = body.encode("utf-8")
            kickoff_bytes = neutral_spec["kickoffText"].replace(neutral_spec["prompt"], str(prompt)).encode("ascii")
            audit_path = HERE / "prompts" / f"audit-config-{run}.json"
            audit = json.loads(frozen(neutral_spec["auditConfig"]))
            audit.update(run=run, prompt=str(prompt), kickoff=str(kickoff), report=str(report),
                         expectedFamily=family, coreManifest=str(CORE),
                         reportStructureChecker=str(HERE / "check-report-structure.py"),
                         reportDestinationRequired="existing-empty-writable-directory-and-absent-report",
                         files=bindings + [{"path": str(prompt), "sha256": sha(body)},
                                           {"path": str(kickoff), "sha256": sha(kickoff_bytes)}])
            for path, raw in ((prompt, body), (kickoff, kickoff_bytes), (audit_path, json_bytes(audit))):
                write_frozen(path, raw)
            spec = {**old_preflight["runs"][family], "run": run, "prompt": str(prompt),
                    "promptSha256": sha(body), "kickoff": str(kickoff), "kickoffText": kickoff_bytes.decode("ascii"),
                    "auditConfig": str(audit_path), "report": str(report)}
            spec["launch"] = {**spec["launch"], "sessionName": f"B131 {family.upper()} independent review003"}
            runs[family] = spec
        draft = {**old_preflight, "runs": runs, "reportDirectory": str(HERE / "reports"),
                 "preparationVersion": "003", "sourceBindings": str(HERE / "source-bindings-003.json"),
                 "pathReadinessRule": "Every run has its own existing empty writable report parent before preflight freeze. "
                                      "Admission and pre-phase2 checks re-probe it; no implicit parent creation by reviewer."}
        proofs = verify_protocol(draft)
        inventory = path_inventory(draft)
        proof_binding = freeze_json(HERE / "path-readiness-003.json", {
            "status": "PASS", "reportDirectories": proofs["reportDestinations"], "reviewerPathInventory": inventory,
            "creationOrder": "Both report directories created and write-probed BEFORE preflight freezing."})
        draft["pathReadiness"] = proof_binding
        preflight = freeze_json(DEFAULT_PREFLIGHT, draft)
        memory = guard.finish()
        require(not memory["breach"], "Runset build RAM breach")
        result = freeze_json(HERE / "runset-build-003.json", {
            "status": "FRESH_PAIRED_RUNSET_NOT_ADMITTED", "preflight": preflight, "pathReadiness": proof_binding,
            "immutableInputs": [{"path": str(path), "sha256": digest} for path, digest in IMMUTABLE_BINDINGS],
            "memory": memory, "limits": "No reviewer admitted/launched/messaged; no teaching, commit, push or publication."})
        print(json.dumps({"build": result, "preflight": preflight, "paths": proof_binding}))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
