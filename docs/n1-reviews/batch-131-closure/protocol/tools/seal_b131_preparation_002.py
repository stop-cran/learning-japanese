"""Exclusive immutable handoff for completed preparation only, with every requested file binding."""
import json
from pathlib import Path

from b131_review_v2_common import (
    CANDIDATE, FORECAST, HERE, PACKET, RECORDS, RUNNER, TOOLS, freeze_json, frozen, require, sha,
    start_guard, write_frozen)
from verify_b131_preparation_002 import verify


def main():
    guard, _ = start_guard("B131002 final preparation handoff seal")
    try:
        qualification = verify(guard)
        tools = [
            "b131_review_v2_common.py", "b131_review_v2_derivations.py", "build_b131_review_packet_002.py",
            "prepare_b131_v2_chain_engine.py", "prepare_chain_b131_002.py",
            "b131_capacity_002.py", "forecast_b131_capacity_002.py", "b131_preflight_002.py",
            "seal_b131_partial_002.py", "b131_runtime_002.py", "build_b131_protocol_002.py",
            "prepare_b131_protocol_successor_003.py", "build_b131_protocol_003.py",
            "b131_review_admission_002.py", "b131_lifecycle_process_003.py", "step_b131_neutral_004.py",
            "test_b131_compact_002.py", "verify_b131_preparation_002.py", "seal_b131_preparation_002.py"]
        paths = {
            "packet": [PACKET / "SHA256SUMS.json", PACKET / "packet.json", PACKET / "REVIEW.md",
                       *(PACKET / "evidence" / name for name in (
                           "kanjidic2-review-projection.xml", "jmdict-review-core.xml",
                           "title-index-delta.txt", "jmdict-extension-index.json"))],
            "preparation": [HERE / name for name in (
                "packet-build-002.json", "derivation-verification-002.json", "chain-engine-derivation-002.json",
                "core-chain-compact-002.json", "core-chain-compact-002-preflight.json",
                "capacity-forecast-compact-002.json", "tooling-derivation-002.json", "partial-handoff-002.json")],
            "protocol": [HERE / "prompts" / name for name in (
                "initial-claude-002.txt", "initial-gpt-002.txt", "kickoff-claude-002.txt", "kickoff-gpt-002.txt",
                "audit-config-N1-B131-CLAUDE-002.json", "audit-config-N1-B131-GPT-002.json",
                "template-compact-002.txt", "preflight-compact-002.json")],
            "localTools": [HERE / name for name in (
                "review_chain.py", "audit-review.py", "check-report-structure.py", "check-run-context.py")],
            "tools": [TOOLS / name for name in tools],
            "validation": [HERE / "validation-001" / name for name in ("result.json", "output.log")],
            "receipts": [RECORDS / directory / "receipt.json" for directory in (
                "preparation-v2-packet-001", "preparation-v2-chain-001", "preparation-v2-forecast-001",
                "preparation-v2-subset-001", "preparation-v2-protocol-001",
                "preparation-v2-protocol-002", "preparation-v2-tests-001")]}
        bindings = {}
        for group, files in paths.items():
            bindings[group] = []
            for path in files:
                data = frozen(path) if group != "receipts" else path.read_bytes()
                original_path = path
                if group == "receipts":
                    receipt = json.loads(data)
                    output_log = (path.parent / "output.log").read_bytes()
                    require(receipt["runnerSha256"] == RUNNER["sha256"]
                            and receipt["logSha256"] == sha(output_log)
                            and receipt["memory"]["freeRamBeforeBytes"] > 2 * 1024**3
                            and receipt["memory"]["minimumObservedFreeRamBytes"] > 1024**3
                            and not receipt["memory"]["breach"] and receipt["cleanupError"] is None
                            and receipt["childExitCodeAfterCleanup"] == receipt["exitCode"],
                            "Command receipt, resource admission or cleanup differs")
                    path = HERE / "receipts" / original_path.parent.name / "receipt.json"
                    write_frozen(path, data)
                    log_binding = write_frozen(path.parent / "output.log", output_log)
                    bindings[group].append({**log_binding, "originalPath": str(original_path.parent / "output.log")})
                if path.suffix == ".py":
                    compile(data.decode("utf-8-sig"), str(path), "exec")
                bindings[group].append({"path": str(path), "sha256": sha(data), "bytes": len(data),
                                        **({"originalPath": str(original_path)} if group == "receipts" else {})})
                guard.check()
        forecast = json.loads(frozen(FORECAST))
        record = {
            "status": "VERIFIED_CAPACITY_GATED_PREPARATION_ONLY", "candidate": CANDIDATE,
            "qualification": qualification, "files": bindings,
            "capacity": {key: forecast[key] for key in (
                "coreTokens", "bootstrapTokens", "reportMessageAllowance", "chosenCaps",
                "projectedWorstCasePeak", "startupGate", "prePhase2Gate", "worstCaseMethod")},
            "capTrials": [{"D": row["D"], "E": row["E"], "projectedPeak": row["projectedWorstCasePeak"],
                           "passes": row["passes"]} for row in forecast["trials"]],
            "evidencePreservation": "Every selected D/E character receives its actual article if present plus "
                "every complete omitted exact-keb JMdict family from the frozen874-record union, "
                "deduplicated against core/other selected records in original union order. Complete record "
                "bytes are checked. Missing articles and absent exact-keb matches are disclosed without substitutes. "
                "Worst-case and actual runtime costs include these bytes and explicit headers.",
            "deviations": [
                "JMdict core has exactly615 records and249780 record-line bytes; XML root framing adds19 "
                "bytes, so complete file249799. No tuning or semantic mismatch.",
                "259 per-ent_seq complete remainder XML assets plus a mechanical exact-keb index were added "
                "to the immutable packet to support later independent selected evidence without packet mutation.",
                "Worst-case ranks additive combined article-plus-dictionary costs within disjoint D/E "
                "eligibility classes, overcounting shared families conservatively. Largest passing capD25/E10.",
                "Initial protocol adaptation failed on a CRLF/LF code anchor before prompts existed. "
                "Frozen failure/outputs preserved. New003 builder normalized implementation line endings, "
                "reusing prior outputs only when equal after newline normalization. No gate was relaxed."],
            "safeNextCommand": (
                "$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'; "
                "$receipt='" + str(RECORDS / "preparation-v2-reverify-") + "'+[guid]::NewGuid().ToString('N'); "
                "python -B " + str(RECORDS / "guarded-test-v3.py") + " $receipt python -B "
                + str(TOOLS / "run_b127_tool.py") + " " + str(TOOLS / "verify_b131_preparation_002.py")),
            "futureLifecycle": {
                "tool": str(TOOLS / "step_b131_neutral_004.py"),
                "preflight": str(HERE / "prompts/preflight-compact-002.json"),
                "limits": "Not executed/admitted here. Any future authorized reviewer requires new full unfiltered "
                "status/roster snapshots and >2GiB admission; do not reuse preparation/old admissions. "
                "Only the new002 runs and tools apply. Phase1 rechecks actual no-compaction context and "
                "the selected extension before allowing any phase2 message. A HOLD sends no phase2."},
            "notDone": ["No reviewer admitted/launched", "No linguistic review or pair disposition",
                        "No quarantined reviewer observations/selections accessed",
                        "No teaching edits, commits, pushes or publication"],
            "limitations": "Forecast is not a guarantee. Source omissions/unread retained evidence are disclosed "
                "in the neutral packet/prompts; dependent judgments remain UNVERIFIED. "
                "Independent review and substantive claim adjudication are future work."}
        record["memory"] = guard.finish()
        require(not record["memory"]["breach"], "Final preparation handoff RAM breach")
        qualification_binding = freeze_json(HERE / "preflight-verified-compact-002.json", qualification)
        record["verifiedPreflight"] = qualification_binding
        binding = freeze_json(HERE / "preparation-handoff-002.json", record)
        print(json.dumps({"handoff": binding, "verifiedPreflight": qualification_binding,
                          "capacity": record["capacity"], "protocol": bindings["protocol"],
                          "newTools": bindings["tools"], "validation": bindings["validation"]}, ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
