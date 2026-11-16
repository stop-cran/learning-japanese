"""Freeze identity-only paired B131 initial prompts and explicit auditing contracts."""
import json
from pathlib import Path

from b131_neutral_common_001 import (
    BASE, CANDIDATE, COORDINATOR, HERE, PACKET, PROOFS, RECORDS, SNAP, TOOLS, WS,
    freeze_json, frozen, json_bytes, load_batch, require, sha, start_guard,
    verify_packet, write_frozen)
from b131_prompt_primitives_001 import (
    B116_CHAIN, B116_CHAIN_SHA, B116_PACKET, SOURCE, SOURCE_SHA, render, template, values)


def main():
    require(not (HERE / "prompts").exists(), "Preserve initial prompts")
    guard, _ = start_guard("B131 paired initial prompt construction")
    try:
        config = load_batch(131)
        root, sums, packet_sha = verify_packet(config, guard)
        chain_path = HERE / "core-chain-compact-001.json"
        chain = json.loads(frozen(chain_path))
        preflight = json.loads(frozen(HERE / "core-chain-compact-001-preflight.json"))
        require(preflight["packetManifestSha256"] == packet_sha
                and preflight["chainManifestSha256"] == sha(frozen(chain_path)), "Core chain binding differs")
        source = frozen(SOURCE, SOURCE_SHA).decode("utf-8")
        b116_chain = json.loads(frozen(B116_CHAIN, B116_CHAIN_SHA))
        b116 = values(B116_PACKET, b116_chain, "N1-B116-GPT-004", SOURCE,
                      WS / "reports-116" / "initial-gpt-004.md", extra_reads="")
        text, replacements = template(source, b116)
        require(render(text, b116) == source, "Accepted-template render equality failed")
        anchor = "PHASE 1 (selection). Read all {{SEGMENTS}} core segments in full. Then select:"
        require(text.count(anchor) == 1, "Complete-core gate anchor differs")
        text = text.replace(anchor,
            "PHASE 1 (selection). Read all {{SEGMENTS}} core segments in full.\n\n"
            "PHASE-1 SEND GATE: Before sending any selection, verify that every numbered core "
            "segment through segment {{SEGMENTS}} and its END OF CHAIN terminator was read. "
            "The title indices are not the end of the core: curated articles and all six complete "
            "external-source extracts must also be read. Follow NEXT SEGMENT until the terminator. "
            "Missing phase-1 coverage cannot be repaired in phase 2.\n\nThen select:")
        text = text.replace("repo\\docs\\content-format.md lines 1-139 only",
                            "repo\\docs\\content-format.md in full")
        text = text.replace(
            "or compatibility with installed APK 5c000bd (predates quiz_exclusions). JVM/emulator work remains on hold.",
            "or compatibility with any installed APK. JVM/emulator work remains out of scope.")
        anchor = "B. The neutral title index,"
        require(text.count(anchor) == 1, "Title-index anchor differs")
        text = text.replace(anchor,
            "Also read the complete four baseline word snapshots, evidence\\font-cmap.json "
            "(actual bounded final cmaps), evidence\\xml-presentation.json (complete canonical-equal "
            "record representation), and evidence\\baseline-title-index.txt in full. The latter "
            "contains every one of the 1254 baseline cards, without proposed pair selections. "
            "State its complete read, line count and first/last lines in Segments read. The "
            "same-commit index below additionally includes the three new cards.\n"
            "B. The neutral title index,")
        require("5c000bd" not in text, "Stale device identifier survived")
        reports = HERE / "reports"
        prompts = HERE / "prompts"
        tools = [
            "common.py", "run_b127_tool.py", "verify_b127_sources.py", "verify_b131_sources.py",
            "b131_source_schema.py", "b131_base_binding_v2.py", "source_query_union.py",
            "b131_neutral_common_001.py", "b131_review_admission_001.py",
            "b131_lifecycle_process_001.py", "prepare_chain_b131_001.py", "step_b131_neutral_001.py",
            "build_b131_review_prompts_001.py", "b131_prompt_primitives_001.py"]
        paths = [*(TOOLS / name for name in tools),
                 *(HERE / name for name in (
                     "review_chain.py", "audit-review.py", "check-report-structure.py",
                     "check-run-context.py", "test-review-chain.py", "test-report-structure.py",
                     "test-review-audit.py", "tooling-derivation.json", "batch.json",
                     "source-contract.json", "packet-build.json", "core-chain-compact-001.json",
                     "core-chain-compact-001-preflight.json")),
                 Path(RECORDS / "guarded-test-v3.py"),
                 root / "SHA256SUMS.json", root / "eligibility-reference.json",
                 root / SNAP / "manifest.json"]
        bindings = [{"path": str(p), "sha256": sha(frozen(p))} for p in paths]
        outputs, runs = {}, {}
        for key, label in (("claude", "CLAUDE"), ("gpt", "GPT")):
            run = f"N1-B131-{label}-001"
            prompt = prompts / f"initial-{key}-001.txt"
            kickoff = prompts / f"kickoff-{key}-001.txt"
            report = reports / f"initial-{key}-001.md"
            rendered = render(text, values(root, chain, run, prompt, report)).encode("utf-8")
            kickoff_bytes = (
                'Original user request: "Please find and inspect work items at stop-cran/learning-japanese '
                'related to creating N1 kanji cards. The work is ~30% complete. Fetch latest changes, find '
                'and read related repo work items, gather the context, plan the outstanding work and do it."\n\n'
                'Assigned slice: independent content review only. The frozen prompt supplies the exact '
                'snapshot, scope and access rules.\n\n'
                f"Read {prompt} using one view call with forceReadLargeFiles: true and no view_range, then "
                "follow its instructions. No other tool call may precede that read.").encode("ascii")
            audit_path = prompts / f"audit-config-{run}.json"
            audit = {
                "run": run, "batch": 131, "candidate": CANDIDATE, "base": BASE,
                "kickoff": str(kickoff), "prompt": str(prompt), "report": str(report),
                "coordinator": COORDINATOR, "expectedFamily": key, "coreManifest": str(chain_path),
                "reference": str(root / "eligibility-reference.json"),
                "completionContract": "entire-message-enum-v1",
                "completionContractScope": "coordinator-tool-message-only",
                "reportStructureContract": "report-structure-v1",
                "reportStructureChecker": str(HERE / "check-report-structure.py"),
                "maxWebFetches": 0,
                "files": bindings + [
                    {"path": str(prompt), "sha256": sha(rendered)},
                    {"path": str(kickoff), "sha256": sha(kickoff_bytes)}]}
            outputs[prompt], outputs[kickoff], outputs[audit_path] = rendered, kickoff_bytes, json_bytes(audit)
            runs[key] = {
                "run": run, "prompt": str(prompt), "promptSha256": sha(rendered),
                "kickoff": str(kickoff), "kickoffText": kickoff_bytes.decode("ascii"),
                "auditConfig": str(audit_path), "report": str(report),
                "launch": {"mode": "interactive", "model": (
                    "claude-opus-5.5" if key == "claude" else "gpt-6.1-sol"),
                    "contextTier": "long_context", "freshSession": True,
                    "sessionName": f"B131 {label} independent review 001"}}
        require(outputs[prompts / "initial-claude-001.txt"].replace(
            b"CLAUDE", b"GPT").replace(b"-claude-", b"-gpt-")
            == outputs[prompts / "initial-gpt-001.txt"], "Initial prompts differ beyond identity")
        for path, raw in outputs.items():
            require(not any(term in raw.lower() for term in (b"b130", b"scratch-130", b"batch-130")),
                    "Residual predecessor identity in initial inputs")
            write_frozen(path, raw)
        write_frozen(prompts / "template-compact-001.txt", text.encode("utf-8"))
        freeze_json(prompts / "preflight-compact-001.json", {
            "batch": 131, "candidate": CANDIDATE, "base": BASE, "packetManifestSha256": packet_sha,
            "coreChainSha256": sha(frozen(chain_path)), "order": ["claude", "gpt"],
            "runs": runs, "reportDirectory": str(reports),
            "template": {"source": str(SOURCE), "sourceSha256": SOURCE_SHA,
                         "b116RenderEqualsSource": True, "replacements": replacements},
            "blindness": "Both initial prompts are byte-identical after identity normalization. "
                         "No author or earlier-review findings or selected D/E answers are present.",
            "phase2Delivery": "Send the entire frozen phase2-message.txt as one exact message, including "
                              "its missing-entry line(s); never send only the first-segment path.",
            "readBudget": {"coreSegments": len(chain["segments"]),
                           "maxSegmentBytesExclusive": 16000,
                           "totalCoreSegmentBytes": sum(s["bytes"] for s in chain["segments"]),
                           "contextAcceptance": "Actual long_context >200000 prompt-token records and "
                                                "no compaction at any point; size is not acceptance."},
            "limits": "Preparation only, not current reviewer admission or launch permission."})
        print(json.dumps({"status": "PAIRED_PROMPTS_PREPARED", "segments": len(chain["segments"]),
                          "runs": {key: value["promptSha256"] for key, value in runs.items()}}))
    finally:
        require(not guard.finish()["breach"], "Prompt construction RAM breach")


if __name__ == "__main__":
    main()
