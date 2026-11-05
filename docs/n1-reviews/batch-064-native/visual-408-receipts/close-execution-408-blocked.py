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
audit = load(V / "batch-064-visual-claude-execution.json")
freeze = load(C / "batch-064-visual-freeze.json")
assert audit["actualModels"] == ["claude-opus-5.5"] and audit["exitCode"] == 0
assert audit["sessionId"] == "28a561c9-9201-40a9-a3a1-c9e37c6d168a"
assert len(audit["failedTools"]) == 1 and not audit["processAndCoverageAccepted"]
assert not audit["observedToolOverlaps"] and not audit["multiToolResponses"]
assert len(audit["toolCalls"]) == 41 and audit["imagePayloadsVerified"] == 28
assert not (C / "batch-064-visual-gpt.jsonl").exists()
failure = audit["failedTools"][0]
assert failure["name"] == "view" and failure["error"]["code"] == "denied"
assert failure["arguments"] == {"path": str(C / "batch-064-visual-task.txt")}
for path, expected in (freeze["teachingHashes"] | freeze["originalReportHashes"]).items():
    assert sha(R / path) == expected, path
for call in audit["toolCalls"]:
    if "imagePayload" in call:
        image = call["imagePayload"]
        assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
        assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
    elif call["success"]:
        assert call["exactRequestedTextContainedInResult"] and not call["truncationOrLimitMarker"]
assert not subprocess.check_output(["git", "diff", "ff6eb7893344b806bf517ebd41bf19089bed5021", "--",
                                    "kanji", "words", "articles", "strokes", "manifest.json"], cwd=R)
receipts = V / "batch-064-native" / "visual-408-receipts"
receipts.mkdir(exist_ok=True)
artifacts = []
for name in [
    "start-execution-408.py", "prepare-batch-064-visual-408.py",
    "run-batch-064-visual-408.ps1", "archive-batch-064-visual-408.py",
    "close-execution-408-blocked.py", "batch-064-visual-task.txt",
    "batch-064-visual-freeze.json", "batch-064-visual-claude-prompt.txt",
    "batch-064-visual-gpt-prompt.txt", "batch-064-visual-claude-process.json",
]:
    target = receipts / name
    assert not target.exists()
    shutil.copyfile(C / name, target)
    artifacts.append({"path": str(target.relative_to(R)), "sha256": sha(target),
                      "bytes": target.stat().st_size})
next_action = (
    "SAME064 blocked at execution408 original-Claude view of "
    r"C:\Users\stop-\n1-kanji-workspace\control\batch-064-visual-task.txt. "
    "Approval-capable parent should resolve EXACT denied read without permission/configuration changes, "
    "path substitution or disguised retry. Preserve original first report/execution/28returned images "
    "and failed task-read; no retroactive strict acceptance. First reviewer exited0 but strict coverage "
    "false; GPT visual process NOT launched. After parent recovery, bounded original-session confirmation "
    "of missing task evidence and consequential visual claims, archive exit/report before originalGPT "
    "1d30e91b-c5ed-4bd0-8d74-2177b9fbb0d7 visual follow-up, strictly serial. No fresh blind initials, "
    "native/accepted404Android rerun absent new concern,065 or second runner. Then all current-main "
    "integration/signing/combined validation/ownerfastforward/publicSHA/greenCI/every publicZIP runtimehash "
    "and issue60 gates. Published90/1228,1138remain; local91 NOTdelivered. CompatibleAndroidf9b59a2+; "
    "physicalphone/generalrelease/whole-set outstanding."
)
blocker = {
    "schemaVersion": 1, "execution": 408, "batch": "064", "kind": "execution-permission",
    "gate": "Original-session Claude dependent native visual confirmation: required shared task view",
    "attempts": 1, "deniedTool": failure["name"], "deniedArguments": failure["arguments"],
    "message": failure["error"]["message"], "errorCode": failure["error"]["code"],
    "startedAt": failure["startedAt"], "completedAt": failure["completedAt"],
    "reviewer": "claude-opus-5.5",
    "reviewerSession": audit["sessionId"],
    "originalReport": "docs/n1-reviews/batch-064-visual-claude.md",
    "originalExecution": "docs/n1-reviews/batch-064-visual-claude-execution.json",
    "processExitCode": 0, "strictProcessAndCoverageAccepted": False,
    "disposition": "Preserve/report/yield. No denied-read retry, alternate path, permission change, second reviewer or publication. Reviewer independently continued from prompt already supplied; coordinator discovered denial after exit and has not accepted it.",
    "safeNextAction": next_action,
}
record = {
    "schemaVersion": 1, "execution": 408, "checkpoint": 408, "batch": "064",
    "startingHead": freeze["evidenceHead"], "reviewedTeachingSnapshot": freeze["teachingSnapshot"],
    "status": "blocked-at-original-claude-shared-task-view",
    "scope": "Partial original-session visual confirmation, exact evidence archival and signed local blocked checkpoint only.",
    "reviewer": {
        "model": audit["actualModels"][0], "sessionId": audit["sessionId"],
        "startedAt": audit["startedAt"], "completedAt": audit["completedAt"],
        "exitCode": audit["exitCode"], "toolCalls": len(audit["toolCalls"]),
        "successfulCalls": 40, "deniedCalls": 1, "overlaps": 0, "multiToolResponses": 0,
        "completeTeachingReads": 4, "fixtureRanges": [[54,143],[150,285],[286,453],[499,550]],
        "completeOwnReportsRead": 2, "completeTerminalLogAndRouteRead": True,
        "assignedPngNamesReturned": 28, "distinctSourceImageHashes": 28,
        "sourceDimensions": [1080,2400], "returnedDimensions": [900,2000],
        "report": "docs/n1-reviews/batch-064-visual-claude.md",
        "reportSha256": audit["reportSha256"],
        "executionRecord": "docs/n1-reviews/batch-064-visual-claude-execution.json",
        "executionRecordSha256": sha(V / "batch-064-visual-claude-execution.json"),
        "rawExecution": audit["rawExecutionLocation"], "rawExecutionSha256": audit["rawExecutionSha256"],
        "strictProcessAndCoverageAccepted": False,
        "reportedNoActionableContentDefect": True,
        "qualification": "Dependent original session, not fresh blind initial. Own original/textual reports read. Task content supplied in prompt but separate mandatory task read denied. Raw report preserved, not treated as independently reconciled visual acceptance. Usage cumulative across original session.",
    },
    "blocker": blocker, "archivedExecutionArtifacts": artifacts,
    "originalReportsAndTeachingHashesPreserved": True,
    "verifiedIndexed406Artifacts": 68,
    "original402TextualClosurePreserved": True,
    "accepted404AndroidRetainedWithoutRerun": True,
    "native406TwoTerminalZeroCasesRetainedWithoutRerun": True,
    "secondReviewerLaunched": False, "independentVisualAcceptance": False,
    "runtimeEditsMade": False, "runtimePublished": False,
    "publishedAdditions": 90, "remainingAdditions": 1138,
    "lastPublishedCommit": "d00bf868466437d39b0330a383de8448686b502d",
    "operationalObservations": [
        "One live-JSONL status probe encountered an incomplete final JSON line while the process was writing; no raw output changed. Completed JSONL later parsed successfully.",
        "Initial archival parser assumed every tool completion has result. Denied completion has error instead; parser updated to preserve exact failed call and mark strict acceptance false.",
        "First parser invocation had already saved the complete report with Windows CRLF. Resume verified normalized report text matches raw final response; original report bytes preserved.",
        "No denied operation retried. No owner token supplied to reviewer; no permissions/configuration changes.",
    ],
    "nextAction": next_action,
    "limits": "One partial visual follow-up only, not two-family visual closure or publication. Reviewer supplied-content and actual view returns distinguished. Its claims of full paragraph visibility and a kun dash/table location have not been independently reconciled by coordinator; no new coordinator image inspection. Source/reading/quiz judgments inherited. No physical-phone/general-release/whole-set acceptance. Original406 denial/parent cleanup connection qualification preserved.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
for target, value in [(C / "execution-408-permission-blocker.json", blocker),
                      (receipts / "execution-408-permission-blocker.json", blocker),
                      (S / "execution-408.json", record)]:
    assert not target.exists()
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
p = C / "progress.json"
data = load(p)
assert data["checkpoint"] == 407 and data["batch"] == "064"
before = dict(data)
data["checkpoint"] = 408
data["status"] = "blocked"
data["stage"] = "batch-064-visual-shared-task-read-permission-blocked"
data["blocker"] = blocker
data["nextAction"] = next_action
data["execution408StartingState"]["status"] = "blocked-first-visual-report-preserved-no-second-reviewer"
data["execution408CoordinatorCheckpoint"] = record
data["batch064VisualBlockedCheckpoint"] = record
for key, value in before.items():
    if key not in {"checkpoint","status","stage","blocker","nextAction","execution408StartingState"}:
        assert data[key] == value, key
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Checkpoint408 blocked saved with full history; 28 returned payloads and exact first report archived. No GPT launch.")
