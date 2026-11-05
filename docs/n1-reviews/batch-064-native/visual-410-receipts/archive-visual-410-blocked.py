import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources" / "execution-410.json"
P = C / "progress.json"
load = lambda path: json.loads(path.read_text(encoding="utf-8-sig"))
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
git = lambda *args: subprocess.check_output(["git", *args], cwd=R, text=True).strip()
data = load(P)

if len(sys.argv) > 1:
    assert sys.argv[1] == "finish" and data["checkpoint"] == 410 and data["status"] == "blocked"
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    receipt = load(C / "execution-410-issue-receipt.json")
    assert receipt["localCommit"] == head and receipt["author"] == "stop-cran" and receipt["bodyVerified"]
    record = load(S)
    record.update(savedCommit=head, signature="G", record=str(S.relative_to(R)),
                  recordSha256=sha(S), issueUpdate=receipt["url"], dedicatedContentClean=True,
                  checkpointRecordedAt=datetime.now(timezone.utc).isoformat())
    data["execution410CoordinatorCheckpoint"] = record
    data["execution410IssueReceipt"] = receipt
    data["blocker"].update(savedCommit=head, signature="G", issueUpdate=receipt["url"])
    data["execution410StartingState"]["status"] = "signed-blocked-checkpoint-complete"
    P.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Checkpoint410 signed receipt persisted; no runtime publication.")
    sys.exit(0)

assert data["checkpoint"] == 409 and data["batch"] == "064"
prefix = "batch-064-visual-410-claude"
process = load(C / f"{prefix}-process.json")
usage = load(C / f"{prefix}-usage.json")
raw = C / f"{prefix}.jsonl"
events = [json.loads(line) for line in raw.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
messages = [e["data"] for e in events if e["type"] == "assistant.message"]
starts = [e for e in events if e["type"] == "tool.execution_start"]
ends = [e for e in events if e["type"] == "tool.execution_complete"]
terminal = [e for e in events if e["type"] == "result"]
models = sorted({m["model"] for m in messages if m.get("model")})
assert process["exitCode"] == 0 and len(starts) == len(ends) == len(terminal) == 1
assert models == [usage["currentModel"]] == [process["requestedModel"]] == ["claude-opus-5.5"]
assert process["sessionId"] == "28a561c9-9201-40a9-a3a1-c9e37c6d168a"
start, end = starts[0], ends[0]
assert start["data"]["toolName"] == "view"
assert start["data"]["arguments"] == {"path": str(C / "batch-064-visual-task.txt")}
assert start["data"]["toolCallId"] == end["data"]["toolCallId"]
assert not end["data"]["success"] and end["data"]["error"]["code"] == "denied"
assert terminal[0]["exitCode"] == 0 and terminal[0]["sessionId"] == process["sessionId"]
assert not terminal[0]["usage"]["codeChanges"]["filesModified"]
assert all(len(m.get("toolRequests", [])) <= 1 for m in messages)
assert not (C / "batch-064-visual-410-gpt.jsonl").exists()
freeze = load(C / "batch-064-visual-freeze.json")
for path, expected in (freeze["teachingHashes"] | freeze["originalReportHashes"]).items():
    assert sha(R / path) == expected, path
assert sha(C / "batch-064-visual-task.txt") == freeze["sharedTaskSha256"]
historical = {}
for name in ("batch-064-visual-claude", "batch-064-visual-409-claude"):
    audit = load(V / f"{name}-execution.json")
    assert sha(V / f"{name}.md") == audit["reportSha256"]
    assert sha(Path(audit["rawExecutionLocation"])) == audit["rawExecutionSha256"]
    assert not audit["processAndCoverageAccepted"]
    historical[name] = {
        "reportSha256": sha(V / f"{name}.md"),
        "executionSha256": sha(V / f"{name}-execution.json"),
        "rawSha256": audit["rawExecutionSha256"],
        "strictAcceptance": False,
    }
assert not git("diff", "ff6eb7893344b806bf517ebd41bf19089bed5021", "--",
               "kanji", "words", "articles", "strokes", "manifest.json")
app = C.parent / "kanji-cards-android"
assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=app)
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
    "sharedTaskSha256": freeze["sharedTaskSha256"],
    "requestsPerAssistantResponse": [len(m.get("toolRequests", [])) for m in messages],
    "toolCalls": [failure], "failedTools": [failure], "observedToolOverlaps": [],
    "multiToolResponses": [], "unfinishedTools": [], "imagePayloadsVerified": 0,
    "successfulFreshReads": 0, "missingAssignedImages": 6,
    "processAndCoverageAccepted": False, "reviewerStoppedImmediatelyAfterDenial": True,
    "usage": usage, "usageBoundary": "Cumulative original-session metrics, not incremental410 effort.",
    "terminalResults": [{"sessionId": terminal[0]["sessionId"], "exitCode": terminal[0]["exitCode"]}],
    "limits": "Exit0 is not coverage acceptance. One newly user-authorized exact-path attempt denied; zero successful fresh reads/images. No substitute tool/path, policy changes, further retry or GPT launch. Historical408/409 strict acceptance remains false.",
}
audit_path = V / f"{prefix}-execution.json"
assert not audit_path.exists()
audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
receipts = V / "batch-064-native" / "visual-410-receipts"
receipts.mkdir()
artifacts = []
for source in [
    C / "prepare-visual-410.py", C / "run-visual-410.ps1", Path(__file__),
    C / "batch-064-user-authorized-reviewer-retry.json",
    C / f"{prefix}-prompt.txt", C / f"{prefix}-process.json",
    C / f"{prefix}-usage.json", C / f"{prefix}-stderr.txt",
    C / "batch-064-visual-410-gpt-prompt.txt",
    C / "inputs" / "copilot-help-410.txt",
    C / "inputs" / "copilot-config-help-410.txt",
]:
    target = receipts / source.name
    shutil.copyfile(source, target)
    artifacts.append({"path": str(target.relative_to(R)), "sha256": sha(target),
                      "bytes": target.stat().st_size})
next_action = (
    "SAME064 blocked at execution410: newly user-authorized ONE original-Claude exact "
    r"view of C:\Users\stop-\n1-kanji-workspace\control\batch-064-visual-task.txt "
    "was denied again. No more coordinator retries, alternative paths/tools, permission/config changes "
    "or coordinator-only read proxies. An approval-capable environment must resolve this exact "
    "original-session reviewer access before another explicitly authorized attempt. Preserve408/409/410 "
    "original reports/denials; strict coverage remains FALSE; both kun-dash and every-paragraph/full-footer "
    "claims unresolved. After actual access recovery, originalClaude bounded task/pixel confirmation "
    "and full report/process archive BEFORE originalGPT1d30e91b-c5ed-4bd0-8d74-2177b9fbb0d7 "
    "full dependent visual strictly serial. Retain402textual/404Android/406native without rerun absent "
    "new concern, including406nonempty-port qualification/future fresh fullportguard. Then latestmain "
    "normalintegration/combinedchecks/originalbudgets/normalsigning/ownerfastforward/publicSHA/"
    "terminalgreenCI/everyimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFOREdelivery/065. "
    "Published90/1228,1138remain/latest063d00bf868;local91 NOTdelivered. CompatibleAndroidf9b59a2+; "
    "physicalphone/generalrelease/whole-set outstanding. No second runner or permission workaround."
)
blocker = {
    "schemaVersion": 1, "execution": 410, "batch": "064", "kind": "execution-permission",
    "gate": "Newly user-authorized original Claude exact shared-task read retry",
    "attempts": 1, "deniedTool": "view", "deniedArguments": failure["arguments"],
    "message": failure["error"]["message"], "errorCode": "denied",
    "startedAt": failure["startedAt"], "completedAt": failure["completedAt"],
    "reviewer": models[0], "reviewerSession": process["sessionId"], "processExitCode": 0,
    "strictProcessAndCoverageAccepted": False, "permissionResolved": False,
    "safeNextAction": next_action,
}
record = {
    "schemaVersion": 1, "execution": 410, "checkpoint": 410, "batch": "064",
    "startingHead": process["evidenceHead"], "reviewedTeachingSnapshot": process["snapshot"],
    "status": "blocked-after-one-newly-user-authorized-exact-reviewer-read",
    "authorization": load(C / "batch-064-user-authorized-reviewer-retry.json"),
    "reviewer": audit, "report": str(report.relative_to(R)),
    "executionRecord": str(audit_path.relative_to(R)), "executionRecordSha256": sha(audit_path),
    "blocker": blocker, "archivedExecutionArtifacts": artifacts,
    "historical408And409VerifiedUnchanged": historical,
    "originalInitialAndTextualReportsVerifiedUnchanged": True,
    "runtimeTeachingAndManifestUnchanged": True, "dedicatedAndroidClean": True,
    "original402TextualClosurePreserved": True, "accepted404AndroidRetainedWithoutRerun": True,
    "native406RetainedWithoutRerun": True, "secondReviewerLaunched": False,
    "independentVisualAcceptance": False,
    "claimReconciliation": {"408-kun-dash-after-sideways-scroll": "unresolved",
                            "408-every-in-scope-paragraph-full-footer-visible": "unresolved"},
    "runtimePublished": False, "publishedAdditions": 90, "remainingAdditions": 1138,
    "lastPublishedCommit": data["lastPublishedCommit"], "nextAction": next_action,
    "limits": "No successful fresh reviewer evidence, new lexical/visual/native/Android acceptance, latest-main integration, runtime push, CI/ZIP delivery, physical-phone/general-release or whole-set acceptance. No permission workarounds. Inherited source/read-depth/citation/process/port limits retained.",
    "recordedAt": datetime.now(timezone.utc).isoformat(),
}
for target, value in [(C / "execution-410-permission-blocker.json", blocker),
                      (receipts / "execution-410-permission-blocker.json", blocker), (S, record)]:
    assert not target.exists()
    target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
before = dict(data)
data.update(checkpoint=410, status="blocked",
            stage="batch-064-newly-authorized-original-reviewer-read-still-denied",
            blocker=blocker, nextAction=next_action)
data["execution410CoordinatorCheckpoint"] = record
for key, value in before.items():
    if key not in {"checkpoint", "status", "stage", "blocker", "nextAction"}:
        assert data[key] == value, key
P.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Checkpoint410 blocked; complete report/audit archived; history preserved; no GPT launch.")
