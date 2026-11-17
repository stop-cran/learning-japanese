"""Seal neutral preparation artifacts, actual execution evidence and coordinator instructions."""
import json
from pathlib import Path

from b131_neutral_common_001 import (
    BASE, CANDIDATE, HERE, PACKET, RECORDS, RUNNER, TOOLS, WS,
    freeze_json, frozen, require, sha, start_guard, write_frozen)
from verify_b131_preparation_001 import main as verify

ASSIGNMENT = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b131-review-preparation-kickoff.txt")
ASSIGNMENT_SHA = "7c4c374eca769ab6ecf573b5b0f6b3f403b848ae6673c26f06895e1da7e41ccc"
ADMISSION_SHA = "0189d080261527e400c16d17ead812aa640948424b1809adec1606df1416b7b7"


def main():
    require(not (HERE / "preparation-artifact-bindings-001.json").exists(), "Preserve final preparation seal")
    guard, _ = start_guard("B131 preparation evidence and handoff seal")
    try:
        assignment_raw = ASSIGNMENT.read_bytes()
        require(sha(assignment_raw) == ASSIGNMENT_SHA, "Frozen assignment changed")
        assignment = write_frozen(HERE / "assignment-captured-001.txt", assignment_raw)
        admission_raw = frozen(RECORDS / "review-preparation-admission-001.json", ADMISSION_SHA)
        admission = write_frozen(HERE / "preparation-admission-captured-001.json", admission_raw)
        executions = []
        for directory in sorted(RECORDS.glob("preparation-*")):
            receipt_path = directory / "receipt.json"
            if not directory.is_dir() or not receipt_path.exists():
                continue
            raw_receipt = receipt_path.read_bytes()
            receipt = json.loads(raw_receipt)
            raw_log = (directory / "output.log").read_bytes()
            require(receipt["runnerSha256"] == RUNNER["sha256"]
                    and receipt["logSha256"] == sha(raw_log)
                    and receipt["waitTimeoutSeconds"] <= 0.1
                    and receipt["cleanupTimeoutSecondsPerStage"] <= 10
                    and receipt["cleanupError"] is None and not receipt["memory"]["breach"],
                    "Preparation execution differs or breached its resource contract")
            capture = HERE / "execution-evidence" / directory.name
            executions.append({
                "source": str(directory), "exitCode": receipt["exitCode"],
                "receipt": write_frozen(capture / "receipt.json", raw_receipt),
                "log": write_frozen(capture / "output.log", raw_log)})
            guard.check()
        failures = [r for r in executions if r["exitCode"] != 0]
        # The synthetic expected-refusal child is separately labelled, not a failed preparation.
        require(all(Path(row["source"]).name in {
            "preparation-validation-001", "preparation-lifecycle-cf2c9755db0f474dbdceb11939d672b1"}
                    for row in failures), "Unexplained preparation failure")
        preflight_path = HERE / "prompts" / "preflight-compact-003.json"
        preflight = json.loads(frozen(preflight_path))
        chain = json.loads(frozen(HERE / "core-chain-compact-001.json"))
        guidance = f"""B131 preparation-only coordinator handoff

Candidate {CANDIDATE}; direct parent {BASE}.
No reviewer is admitted or launched. No content/teaching edit, commit, push or publication occurred.
Use ONLY prompts/preflight-compact-003.json and review-tools/step_b131_neutral_003.py.
Older 001/002 lifecycle/preflight files are preserved preparation predecessors, not launch instructions.
The actual frozen prompt text is initial-claude-002.txt / initial-gpt-002.txt.
The run IDs remain N1-B131-CLAUDE-001 / N1-B131-GPT-001; neither has run.

All shell commands below are guidance, NOT executed reviewer operations:

$env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'
$ws='C:\\Users\\stop-\\n1-kanji-workspace'
$guard="$ws\\scratch-131\\review\\guarded-test-v3.py"
$adapter="$ws\\review-tools\\run_b127_tool.py"
$step="$ws\\review-tools\\step_b131_neutral_003.py"
$prep="$ws\\scratch-131\\review\\preparation-001"
$preflight="$prep\\prompts\\preflight-compact-003.json"

Safe next read-only verification, with NEW absent output names:
python -B $guard "$ws\\scratch-131\\review\\preparation-coordinator-check-001" python -B $adapter "$ws\\review-tools\\verify_b131_preparation_001.py" "$prep\\coordinator-verification-001.json"

Before any reviewer: obtain fresh FULL, UNFILTERED get_sessions_status and list_sessions_and_chats
snapshots; save exact tool outputs to NEW local files. No omitted idle, archived, unrelated or
unknown rows. Roster may retain its tool preamble; the parser locates its JSON array.
Create a new request JSON with exactly:
{{"statusPath":"<absolute exact status JSON path>","rosterPath":"<absolute exact roster output path>","observedAt":"<actual RFC3339 observation time with timezone>"}}
The requester must use actual observation time, not file-copy time. The admission enforces matching
full IDs/counts, no duplicates, age under120s, no unknown/active session except coordinator, no
duplicate reviewer name, no prior run artifacts, signed clean candidate, all five actual proofs,
packet bytes and >2GiB free RAM. It is an observation, not a reservation.

Admission command (do not execute until fresh actual observations exist):
python -B $guard "$ws\\scratch-131\\review\\preparation-claude-admit-001" python -B $adapter $step 131 claude admit "<absolute NEW request.json>" $preflight

Only after admission, the coordinator may use app create_session with the EXACT kickoffText
and launch settings from preflight.runs.claude. Never invent/truncate the kickoff, enable
extra tools or grant inherited B113 permissions. One active reviewer, interactive, long_context,
model claude-opus-5.5. Startup must be checked within120s of admission. Capture actual desktop
session identity separately from the runtime CLI session-state ID; lifecycle arguments below
require the actual runtime ID whose events.jsonl exists, not a guessed desktop ID.
No launch is performed or requested by this preparation handoff.

Future lifecycle commands (each output directory must be NEW and absent):
python -B $guard "$ws\\scratch-131\\review\\preparation-claude-launch-audit-001" python -B $adapter $step 131 claude launch "<actual runtime session ID>" $preflight
python -B $guard "$ws\\scratch-131\\review\\preparation-claude-phase1-audit-001" python -B $adapter $step 131 claude phase1 "<same actual runtime session ID>" $preflight

phase1 must report readyForPhase2=true after full execution and context checks. It mechanically
builds only that reviewer's D/E extension. Send the ENTIRE frozen
$prep\\N1-B131-CLAUDE-001-phase2-message.txt as ONE exact coordinator message:
line1 is the extension first-segment path; line2 is Missing entries: none, OR Missing entries:
followed by every missing request line verbatim. Sending only line1 voids the pass.
No substitutes, selection hints, later-added candidates or unrequested material.

python -B $guard "$ws\\scratch-131\\review\\preparation-claude-final-audit-001" python -B $adapter $step 131 claude final "<same actual runtime session ID>" $preflight

Final mechanics, actual family, exact full phase messages, ordered complete reads, one report
creation/readback, zero fetches, exact completion enum, report structure and no-compaction
context must all pass. Mechanical status is NOT content acceptance. The coordinator must
adjudicate all claims, notes, source citations and evidence issues explicitly before a frozen
adjudication binds candidate/run/report and finalSha256, claimsAdjudicated=true, verdict and
acceptedFindings. Do not execute accept against a placeholder or unadjudicated report.
python -B $guard "$ws\\scratch-131\\review\\preparation-claude-accept-001" python -B $adapter $step 131 claude accept "<actual frozen substantive adjudication.json>" $preflight

Only after the first run's accepted bounded evidence and fresh complete app/RAM admission:
repeat the process for gpt, using its untouched kickoffText and gpt-6.1-sol long_context,
fresh session, and entirely independent D/E choices. Never put the first report, selections,
findings or author pair/source conclusions in the second initial packet.

Required core: {len(chain['segments'])} serial complete segments, all below16000 bytes;
{len(chain['sources'])} full sources; total {sum(s['bytes'] for s in chain['segments'])} segment bytes.
No token-budget/compaction guarantee is inferred from size. Actual context audit remains mandatory.
If any gate fails: preserve raw execution, mark HOLD/VOID as applicable, quarantine observations,
do not fix the report, send hints, relax a gate or silently retry a reviewer.

Preparation limitations: complete source records and mechanical checks only; not linguistic/native/
rendered/device, arbitrary/custom/multiple-borrow, Kotlin, review acceptance or publication.
Font scope is209 finite code points, NOT all text of179 legacy articles. Five points are absent
in all3 bundled cmaps; no rendered fallback is claimed. Published membership stays264/1228,
964 remaining; no B131 delivery is credited.
"""
        write_frozen(HERE / "coordinator-guidance-001.txt", guidance.encode("utf-8"))
        for name in ("validation-001", "validation-002"):
            empty = HERE / name / "fixture-temporary"
            if empty.exists():
                require(not any(empty.iterdir()), "Unexpected remaining synthetic fixture output")
                empty.rmdir()
        tools = [
            "inspect_b131_neutral_inputs_001.py", "b131_neutral_common_001.py",
            "build_b131_neutral_packet_001.py", "b131_review_admission_001.py",
            "b131_lifecycle_process_001.py", "b131_lifecycle_process_002.py",
            "derive_b131_review_tooling_001.py", "prepare_chain_b131_001.py",
            "step_b131_neutral_001.py", "step_b131_neutral_002.py", "step_b131_neutral_003.py",
            "b131_prompt_primitives_001.py", "build_b131_review_prompts_001.py",
            "revise_b131_protocol_controls_002.py", "bind_b131_lifecycle_io_003.py",
            "test_b131_neutral_preparation_001.py", "test_b131_neutral_preparation_002.py",
            "test_b131_neutral_preparation_003.py", "test_b131_lifecycle_io_003.py",
            "verify_b131_preparation_001.py", "finalize_b131_preparation_001.py"]
        paths = sorted([p for p in HERE.rglob("*") if p.is_file()], key=str)
        paths += [TOOLS / name for name in tools]
        paths.append(PACKET / "SHA256SUMS.json")
        manifest = freeze_json(HERE / "preparation-artifact-bindings-001.json", {
            "batch": 131, "candidate": CANDIDATE, "base": BASE,
            "files": [{"path": str(path), "sha256": sha(frozen(path))} for path in paths],
            "packetScope": "Packet member hashes are complete under the separately bound SHA256SUMS.json.",
            "currentExecution": "The sealing command's own outer receipt is completed after this child exits; "
                                "it remains in preparation-finalize-001, not retrospectively frozen here.",
            "assignment": assignment, "admission": admission,
            "executions": executions, "preparationFailures": failures})
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Preparation seal RAM breach")
    verification = verify(HERE / "final-preparation-verification-001.json")
    handoff = freeze_json(HERE / "preparation-handoff-001.json", {
        "status": "VERIFIED_PREPARATION_ONLY", "batch": 131, "candidate": CANDIDATE, "base": BASE,
        "packetManifest": {"path": str(PACKET / "SHA256SUMS.json"),
                           "sha256": sha(frozen(PACKET / "SHA256SUMS.json"))},
        "sourceContract": {"path": str(HERE / "source-contract.json"),
                           "sha256": sha(frozen(HERE / "source-contract.json"))},
        "preflight": {"path": str(preflight_path), "sha256": sha(frozen(preflight_path))},
        "lifecycle": {"path": str(TOOLS / "step_b131_neutral_003.py"),
                      "sha256": sha(frozen(TOOLS / "step_b131_neutral_003.py"))},
        "artifactManifest": manifest, "verification": verification,
        "validation": {"path": str(HERE / "validation-003" / "result.json"),
                       "sha256": sha(frozen(HERE / "validation-003" / "result.json")), "tests": 85},
        "guidance": {"path": str(HERE / "coordinator-guidance-001.txt"),
                     "sha256": sha(frozen(HERE / "coordinator-guidance-001.txt"))},
        "core": {"path": str(HERE / "core-chain-compact-001.json"),
                 "sha256": sha(frozen(HERE / "core-chain-compact-001.json")),
                 "segments": len(chain["segments"]), "sources": len(chain["sources"]),
                 "maxSegmentBytes": max(s["bytes"] for s in chain["segments"]),
                 "totalSegmentBytes": sum(s["bytes"] for s in chain["segments"])},
        "runs": {key: {"run": spec["run"], "prompt": spec["prompt"],
                       "promptSha256": spec["promptSha256"], "auditConfig": spec["auditConfig"]}
                 for key, spec in preflight["runs"].items()},
        "preparationCorrections": ["First validation preserved: two inherited fixtures did not match "
                                  "stronger explicit B131 controls; no production gate relaxed.",
                                  "Actual lifecycle adapter IO boundary corrected before any reviewer; "
                                  "synthetic success and expected-refusal subprocesses passed."],
        "memory": memory,
        "limits": "No reviewer admitted/launched; no independent content review, native/device acceptance "
                  "or B131 delivery. Candidate checkout and every pre-existing frozen artifact unchanged."})
    print(json.dumps(handoff))


if __name__ == "__main__":
    main()
