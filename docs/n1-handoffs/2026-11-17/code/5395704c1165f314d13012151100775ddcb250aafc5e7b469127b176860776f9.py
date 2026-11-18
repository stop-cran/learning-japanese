"""Immutable final ledger, directory existence/probe proof and guarded future lifecycle commands."""
import json
from pathlib import Path

from b131_review_v3_common import (
    DEFAULT_PREFLIGHT, HERE, IMMUTABLE_BINDINGS, RECORDS, TOOLS,
    freeze_json, frozen, require, sha, start_guard, write_frozen)
from verify_b131_preparation_003 import verify


def main():
    guard, _ = start_guard("B131003 final preparation seal")
    try:
        qualification = verify(guard)
        tools = [TOOLS / name for name in (
            "b131_review_v3_common.py", "b131_preflight_003.py", "build_b131_runset_003.py",
            "prepare_chain_b131_003.py", "b131_runtime_003.py", "b131_review_admission_003.py",
            "b131_lifecycle_process_004.py", "step_b131_neutral_005.py",
            "test_b131_preparation_003.py", "test_b131_preparation_004.py",
            "prepare_b131_validation_successor_004.py", "snapshot_b131_runset_subset_003.py",
            "b131_path_readiness_004.py", "test_b131_path_inventory_004.py",
            "verify_b131_preparation_003.py", "seal_b131_preparation_003.py", "prepare_b131_seal_successor_004.py", "seal_b131_preparation_004.py")]
        spec = json.loads(frozen(DEFAULT_PREFLIGHT))
        paths = [*tools, DEFAULT_PREFLIGHT, HERE / "Invoke-B131Review003.ps1"]
        paths += [HERE / name for name in (
            "audit-review.py", "review_chain.py", "check-run-context.py", "check-report-structure.py",
            "batch.json", "derivation-verification-002.json", "core-chain-compact-002.json",
            "tooling-derivation-003.json", "source-bindings-003.json", "path-readiness-003.json",
            "path-readiness-004.json",
            "runset-build-003.json", "test-controls-003.py", "test-controls-004.py",
            "partial-handoff-003.json", "validation-fixture-successor-004.json",
            "validation-001/result.json", "validation-002/result.json", "validation-002/output.log",
            "validation-paths-004/result.json", "validation-paths-004/output.log")]
        for run in spec["runs"].values():
            paths.extend(Path(run[name]) for name in ("prompt", "kickoff", "auditConfig"))
        bindings = []
        for path in paths:
            data = frozen(path)
            if path.suffix == ".py":
                compile(data.decode("utf-8-sig"), str(path), "exec")
            bindings.append({"path": str(path), "sha256": sha(data), "bytes": len(data)})
            guard.check()

        environment = "$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'; "
        common = (environment + "$receipt='" + str(RECORDS / "preparation-v3-command-")
                  + "'+[guid]::NewGuid().ToString('N'); python -B '"
                  + str(RECORDS / "guarded-test-v3.py") + "' $receipt python -B '"
                  + str(TOOLS / "run_b127_tool.py") + "' ")
        commands = {"verify": common + "'" + str(TOOLS / "verify_b131_preparation_003.py") + "'"}
        for action, argument in (("admit", "admissionRequest"), ("launch", "sessionId"),
                                 ("phase1", "sessionId"), ("final", "sessionId"),
                                 ("accept", "adjudication")):
            commands[action] = (common + "'" + str(TOOLS / "step_b131_neutral_005.py")
                                + "' 131 claude " + action + " $" + argument + " '"
                                + str(DEFAULT_PREFLIGHT) + "'")
        command_binding = freeze_json(HERE / "guarded-commands-004.json", {
            "commands": commands,
            "arguments": {
                "admissionRequest": "Absolute request JSON with exactly statusPath,rosterPath,observedAt, "
                                    "containing fresh full unfiltered app snapshots (<120seconds).",
                "sessionId": "Actual newly created003 app reviewer session ID, never a retired002 ID.",
                "adjudication": "Absolute frozen substantive003 adjudication JSON bound to current candidate, "
                                "run, report SHA and final SHA; not supplied/inferred by preparation."},
            "family": "Replace 131 claude with 131 gpt for the second fresh run, only after Claude003 acceptance.",
            "launch": "The launch command verifies/records an already app-launched fresh session; it does not "
                      "spawn a model. Use the exact frozen kickoff/model/long_context spec and a fresh admission.",
            "guard": "Direct commands set UTF8/no-bytecode and invoke pinned guarded-test-v3.py with a fresh UUID receipt. "
                     "Commands other than verify have NOT been executed. Admission/launch remain future decisions."})
        # Preserve the command-level admission and failure receipts without changing their originals.
        receipt_bindings = []
        for directory in (
            "preparation-v3-build-001", "preparation-v3-tests-001",
            "preparation-v3-subset-001", "preparation-v3-subset-002", "preparation-v3-tests-002",
            "preparation-v3-inventory-001", "preparation-v3-wrapper-001",
            "preparation-v3-seal-successor-001"):
            source = RECORDS / directory
            raw = (source / "receipt.json").read_bytes()
            receipt = json.loads(raw)
            output = (source / "output.log").read_bytes()
            require(receipt["logSha256"] == sha(output) and not receipt["memory"]["breach"]
                    and receipt["memory"]["freeRamBeforeBytes"] > 2 * 1024**3
                    and receipt["memory"]["minimumObservedFreeRamBytes"] > 1024**3
                    and receipt["cleanupError"] is None, "Resource receipt integrity differs")
            for name, data in (("receipt.json", raw), ("output.log", output)):
                receipt_bindings.append(write_frozen(HERE / "receipts" / directory / name, data))
        proof = freeze_json(HERE / "preparation-qualification-003.json", qualification)
        record = {
            "status": "VERIFIED_FRESH003_PREPARATION_ONLY", "qualification": proof,
            "files": bindings, "immutableInputs": [{"path": str(path), "sha256": digest}
                                                  for path, digest in IMMUTABLE_BINDINGS],
            "reportDirectories": qualification["protocol"]["reportDestinations"],
            "guardedCommands": command_binding, "commands": commands, "receipts": receipt_bindings,
            "changes": "Only fresh003 identities/lifecycle paths and explicit checked report parents. "
                       "Packet, source contract, core chain, review_chain caps and capacity forecast are unchanged. "
                       "Both report parents existed, were empty/non-ReadOnly and passed actual exclusive "
                       "create/readback/remove probes before the preflight was frozen.",
            "validation": qualification["tests"],
            "inventoryValidation": qualification["inventoryTests"],
            "activePathReadiness": qualification["activePathReadiness"],
            "deviations": "First32-case run preserved one synthetic fixture error (relocated HERE lacked batch.json); "
                          "test-only successor004 supplies that unchanged config. All32 controls reran and passed. "
                          "A helper syntax error was caught before freezing/execution; its command receipt is retained. "
                          "Original path inventory incorrectly said extension-002; corrected path-readiness004 "
                          "matches the actual frozen003 builder and explicitly supersedes only that metadata. "
                          "The original prompts/preflight/runtime files are preserved. Three metadata controls passed. "
                          "No runtime guard or immutable input was relaxed.",
            "commandDeliveryLimitation": "The optional frozen .ps1 wrapper was refused by the host's "
                "script execution policy and is INACTIVE. No policy was changed or bypassed. "
                "Use the ordinary direct guarded Python commands in guarded-commands-004.json; "
                "these are the same supported invocation path used throughout preparation.",
            "limits": qualification["limits"], "notPerformed": qualification["notPerformed"]}
        record["memory"] = guard.finish()
        require(not record["memory"]["breach"], "Final preparation seal RAM breach")
        binding = freeze_json(HERE / "preparation-handoff-004.json", record)
        print(json.dumps({"handoff": binding, "qualification": proof, "commands": command_binding,
                          "protocolFiles": [row for row in bindings if "prompts" in Path(row["path"]).parts],
                          "tools": [row for row in bindings if Path(row["path"]).parent == TOOLS],
                          "reportDirectories": record["reportDirectories"], "validation": record["validation"]}))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
