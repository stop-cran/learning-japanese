import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
prefix = "batch-064-visual-409-claude"
process = load(C / f"{prefix}-process.json")
usage = load(C / f"{prefix}-usage.json")
raw = C / f"{prefix}.jsonl"
events = [json.loads(s) for s in raw.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
messages = [e["data"] for e in events if e["type"] == "assistant.message"]
models = sorted({m["model"] for m in messages if m.get("model")})
starts = [e for e in events if e["type"] == "tool.execution_start"]
ends = [e for e in events if e["type"] == "tool.execution_complete"]
terminal = [e for e in events if e["type"] == "result"]
assert process["exitCode"] == 0
assert models == [process["requestedModel"]] == [usage["currentModel"]] == ["claude-opus-5.5"]
assert process["sessionId"] == "28a561c9-9201-40a9-a3a1-c9e37c6d168a"
assert len(starts) == len(ends) == len(terminal) == 1
start, end = starts[0], ends[0]
assert start["data"]["toolName"] == "view"
assert start["data"]["arguments"] == {"path": str(C / "batch-064-visual-task.txt")}
assert start["data"]["toolCallId"] == end["data"]["toolCallId"]
assert not end["data"]["success"] and end["data"]["error"]["code"] == "denied"
assert terminal[0]["exitCode"] == 0 and terminal[0]["sessionId"] == process["sessionId"]
assert not terminal[0]["usage"]["codeChanges"]["filesModified"]
assert all(len(m.get("toolRequests", [])) <= 1 for m in messages)
assert not (C / "batch-064-visual-409-gpt.jsonl").exists()
freeze = load(C / "batch-064-visual-freeze.json")
for path, expected in (freeze["teachingHashes"] | freeze["originalReportHashes"]).items():
    assert sha(R / path) == expected, path
recovery = load(C / "batch-064-parent-shared-task-read-recovery.json")
for path, key in [
    (V / "batch-064-visual-claude.md", "originalReviewerReportSha256"),
    (V / "batch-064-visual-claude-execution.json", "originalReviewerExecutionRecordSha256"),
    (C / "batch-064-visual-claude.jsonl", "originalReviewerRawExecutionSha256"),
]:
    assert sha(path) == recovery[key], path
assert not subprocess.check_output(["git", "diff", "ff6eb7893344b806bf517ebd41bf19089bed5021",
                                    "--", "kanji", "words", "articles", "strokes", "manifest.json"], cwd=R)
report = V / f"{prefix}.md"
assert not report.exists()
report.write_text([m["content"] for m in messages if m.get("content")][-1] + "\n", encoding="utf-8")
failure = {
    "name": "view", "arguments": start["data"]["arguments"],
    "startedAt": start["timestamp"], "completedAt": end["timestamp"],
    "success": False, "error": end["data"]["error"], "returnedCharacters": 0,
}
audit = {
    **process, "actualModels": models, "availableTools": ["view"],
    "dependentFollowupNotBlindInitial": True, "reportSha256": sha(report),
    "rawExecutionLocation": str(raw), "rawExecutionSha256": sha(raw),
    "sharedTaskSha256": sha(C / "batch-064-visual-task.txt"),
    "controlArtifactHashes": {
        suffix: sha(C / (prefix + suffix))
        for suffix in ("-process.json", "-usage.json", "-prompt.txt", "-stderr.txt")
    },
    "requestsPerAssistantResponse": [len(m.get("toolRequests", [])) for m in messages],
    "toolCalls": [failure], "failedTools": [failure], "observedToolOverlaps": [],
    "multiToolResponses": [], "unfinishedTools": [], "imagePayloadsVerified": 0,
    "successfulFreshReads": 0, "missingRequiredText": [str(C / "batch-064-visual-task.txt"),
        str(V / "batch-064-visual-claude.md"), str(R / "kanji" / "偵.md"),
        str(R / "words" / "探偵.md")],
    "missingAssignedImages": 6, "processAndCoverageAccepted": False,
    "reviewerStoppedImmediatelyAfterDenial": True,
    "usage": usage, "usageBoundary": "Original-session cumulative counters, not incremental409 cost.",
    "terminalResults": [{"sessionId": terminal[0]["sessionId"], "exitCode": terminal[0]["exitCode"]}],
    "limits": "Process exit0 is not coverage acceptance. Parent408 successful coordinator read did not establish reviewer access. No successful fresh evidence, retry, substituted tool/path or GPT launch. Historical408 strict acceptance remains false.",
}
audit_path = V / f"{prefix}-execution.json"
assert not audit_path.exists()
audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipts = V / "batch-064-native" / "visual-409-receipts"
receipts.mkdir()
artifacts = []
for name in [
    "prepare-visual-409.py", "run-visual-409.ps1", "archive-visual-409-blocked.py",
    "batch-064-parent-shared-task-read-recovery.json",
    f"{prefix}-prompt.txt", f"{prefix}-process.json",
    "batch-064-visual-409-gpt-prompt.txt",
]:
    target = receipts / name
    shutil.copyfile(C / name, target)
    artifacts.append({"path": str(target.relative_to(R)), "sha256": sha(target),
                      "bytes": target.stat().st_size})
for name in ("copilot-help-409.txt", "copilot-config-help-409.txt"):
    target = receipts / name
    shutil.copyfile(C / "inputs" / name, target)
    artifacts.append({"path": str(target.relative_to(R)), "sha256": sha(target),
                      "bytes": target.stat().st_size})
next_action = (
    "SAME064 blocked at execution409 original Claude reviewer EXACT view of "
    r"C:\Users\stop-\n1-kanji-workspace\control\batch-064-visual-task.txt. "
    "Parent408 successful coordinator read did NOT resolve original reviewer access; preserve both "
    "denials and recovery separately. Approval-capable parent must resolve this exact original-session "
    "reviewer read without policy/config changes, path substitution or disguised retry. No further "
    "coordinator retries. After actual reviewer-access recovery, resume bounded original Claude "
    "missing-task/consequential-pixel confirmation, archive full exit/report/audit, THEN originalGPT "
    "1d30e91b-c5ed-4bd0-8d74-2177b9fbb0d7 full dependent visual strictly serial. "
    "Original408 28returned images/report immutable and strict coverage FALSE;409 one failed call, "
    "zero successful fresh reads/images, stopped immediately; GPT NOT launched. Kun-dash/all-paragraph "
    "visibility report claims remain unresolved, not teaching defects established. Retain402textual/"
    "404Android/406native without rerun absent new concern and406 nonempty-port qualification. "
    "Then latest-main integration/combined validation/normal signing/ownerfastforward/publicSHA/"
    "greenCI/every immutable public ZIP runtimehash/terminal receipts/ownerissue60 BEFOREdelivery/065. "
    "Published90/1228,1138remain/latest063d00bf868;local91 NOTdelivered. CompatibleAndroidf9b59a2+; "
    "physicalphone/generalrelease/whole-set outstanding. No second runner or permission workaround."
)
blocker = {
    "schemaVersion": 1, "execution": 409, "batch": "064", "kind": "execution-permission",
    "gate": "Original Claude bounded recovery confirmation: mandatory shared task view",
    "attempts": 1, "deniedTool": "view", "deniedArguments": failure["arguments"],
    "message": failure["error"]["message"], "errorCode": "denied",
    "startedAt": failure["startedAt"], "completedAt": failure["completedAt"],
    "reviewer": models[0], "reviewerSession": process["sessionId"],
    "originalReport": str(report.relative_to(R)), "executionRecord": str(audit_path.relative_to(R)),
    "processExitCode": 0, "strictProcessAndCoverageAccepted": False,
    "disposition": "Preserve/report/yield. Reviewer stopped immediately; no retry/substitution/GPT/native/publication. Parent408 read remains a coordinator-only success, not original reviewer access.",
    "safeNextAction": next_action,
}
record = {
    "schemaVersion": 1, "execution": 409, "checkpoint": 409, "batch": "064",
    "startingHead": process["evidenceHead"], "reviewedTeachingSnapshot": process["snapshot"],
    "status": "blocked-at-original-reviewer-task-read-after-parent-coordinator-only-recovery",
    "scope": "One bounded original-session dependent confirmation attempt and durable blocked archival checkpoint only.",
    "reviewer": {
        "model": models[0], "sessionId": process["sessionId"], "exitCode": 0,
        "startedAt": process["startedAt"], "completedAt": process["completedAt"],
        "toolCalls": 1, "successfulCalls": 0, "deniedCalls": 1, "images": 0,
        "overlaps": 0, "multiToolResponses": 0,
        "report": str(report.relative_to(R)), "reportSha256": sha(report),
        "executionRecord": str(audit_path.relative_to(R)), "executionRecordSha256": sha(audit_path),
        "rawExecution": str(raw), "rawExecutionSha256": sha(raw),
        "strictProcessAndCoverageAccepted": False,
    },
    "blocker": blocker, "archivedExecutionArtifacts": artifacts,
    "parent408RecoveryPreservedWithoutRetroactiveAcceptance": True,
    "original408ReportExecutionRawHashesVerifiedUnmodified": True,
    "originalInitialAndTextualReportHashesVerifiedUnmodified": True,
    "runtimeTeachingAndManifestUnchanged": True,
    "original402TextualClosurePreserved": True,
    "accepted404AndroidRetainedWithoutRerun": True,
    "native406TwoTerminalZeroCasesRetainedWithoutRerun": True,
    "secondReviewerLaunched": False, "independentVisualAcceptance": False,
    "coordinatorNewPixelReads": [
        "n1-064-kanji-no-kun.png", "n1-064-kanji-compound-boundary.png",
        "n1-064-detective-role-summary.png",
    ],
    "coordinatorObservation": "Three actual returned900x2000 images inspected. Visible偵 table has one on row and following no-kun prose; these frames do not establish the old claimed kun-dash cell. Role-summary screenshot shows lower prose/footer but clips leading component sentence. This is a report-evidence qualification, not an established teaching defect, full image-set review, independent two-family closure or phone acceptance.",
    "claimReconciliation": {
        "408-kun-dash-after-sideways-scroll": "unresolved; original reviewer has not confirmed or withdrawn; current three coordinator images do not establish it",
        "408-every-in-scope-paragraph-full-footer-visible": "unresolved; no new reviewer comparison completed",
    },
    "runtimePublished": False, "publishedAdditions": 90, "remainingAdditions": 1138,
    "lastPublishedCommit": "d00bf868466437d39b0330a383de8448686b502d",
    "nextAction": next_action,
    "limits": "No successful fresh reviewer reads or new review closure. No Android/native/Python-suite rerun, dictionary audit, main integration, runtime push,CI/ZIP delivery, physical-phone/general-release or whole-set acceptance. Historical source/process/406port and denial qualifications retained.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
for target, value in [(C / "execution-409-permission-blocker.json", blocker),
                      (receipts / "execution-409-permission-blocker.json", blocker),
                      (S / "execution-409.json", record)]:
    assert not target.exists()
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
p = C / "progress.json"
data = load(p)
assert data["checkpoint"] == 408 and data["batch"] == "064"
before = dict(data)
data.update(checkpoint=409, status="blocked",
            stage="batch-064-original-claude-shared-task-read-still-permission-blocked",
            blocker=blocker, nextAction=next_action)
data["execution409StartingState"]["status"] = "blocked-report-archived-no-second-reviewer"
data["execution409CoordinatorCheckpoint"] = record
for key, value in before.items():
    if key not in {"checkpoint", "status", "stage", "blocker", "nextAction", "execution409StartingState"}:
        assert data[key] == value, key
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Checkpoint409 blocked; original complete report and failure archived; history preserved; no GPT launch.")
