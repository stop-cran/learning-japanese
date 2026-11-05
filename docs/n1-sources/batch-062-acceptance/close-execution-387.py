import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
HEAD = "da3a602a8eaf12190c7baf4048d02d86fe20a048"
TEACHING = "38ab6072d2041325142c54cf54be5d126928eb31"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, cwd=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd, text=True, encoding="utf-8").strip()


def audit():
    assert git("branch", "--show-current") == "content/n1-kanji"
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    android = C.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", cwd=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", cwd=android)
    freeze = load(C / "batch-062-visual-freeze.json")
    for path, digest in freeze["files"].items():
        assert sha(R / path) == digest, path
    for row in freeze["nativeFiles"]:
        assert sha(R / row["path"]) == row["sha256"]
    assert freeze["sharedTaskSha256"] == sha(C / "batch-062-visual-task.txt")
    processes = []
    for family, model, session, count in (
        ("claude", "claude-opus-5.5", "1d12b838-18c9-407a-b065-fc6e8fe44480", 28),
        ("gpt", "gpt-6.1-sol", "38b783dc-e2cf-4226-8786-e207effbde13", 27),
    ):
        prefix = f"batch-062-visual-{family}"
        record = load(V / f"{prefix}-execution.json")
        assert record["actualModels"] == [model] == [record["usage"]["currentModel"]]
        assert record["sessionId"] == session and record["exitCode"] == 0
        assert record["processAndCoverageAccepted"] and record["availableTools"] == ["view"]
        assert not record["observedToolOverlaps"] and not record["multiToolResponses"]
        assert not record["unfinishedTools"] and not record["missingRequiredText"]
        assert len(record["toolCalls"]) == count and record["imagePayloadsVerified"] == 17
        assert record["sharedTaskSha256"] == freeze["sharedTaskSha256"]
        assert sha(V / f"{prefix}.md") == record["reportSha256"]
        assert sha(C / f"{prefix}.jsonl") == record["rawExecutionSha256"]
        assert all(sha(C / (prefix + suffix)) == digest for suffix, digest in record["controlArtifactHashes"].items())
        config = [x["message"] for x in record["configurationEvidence"] if x.get("infoType") == "configuration"]
        assert len(config) == 1 and all(x in config[0] for x in ("powershell", "task", "web_fetch"))
        editing_tools = ("edit", "create") if family == "claude" else ("apply_patch",)
        assert all(x in config[0] for x in editing_tools)
        for call in record["toolCalls"]:
            assert call["name"] == "view" and call["success"] and not call["truncationOrLimitMarker"]
            if "imagePayload" in call:
                image = call["imagePayload"]
                assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
                assert image["sourceDimensions"] == [1080, 2400]
                assert image["returnedDimensions"] == [900, 2000]
            else:
                assert call["exactRequestedTextContainedInResult"]
                assert call["requestedRange"][1] - call["requestedRange"][0] + 1 <= 140
        processes.append(record)
    began = datetime.fromisoformat(processes[1]["startedAt"])
    assert datetime.fromisoformat(processes[0]["completedAt"]) < began
    assert (V / "batch-062-visual-claude-execution.json").stat().st_mtime < began.timestamp()
    assert (V / "batch-062-visual-claude.md").stat().st_mtime < began.timestamp()
    log = (V / "batch-062-native" / "attempt-1" / "instrumentation.txt").read_text(encoding="utf-8")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", log, re.M) == ["1", "0", "1", "0"]
    assert "Time: 96.065" in log and "OK (2 tests)" in log
    route = load(V / "batch-062-native" / "attempt-1" / "n1-062-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1 and not route["phoneEvidence"]
    assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1074, 5032, 94, 0, 1]
    assert route["contentVersion"] == "545c56b5d4b4e8ef"
    assert route["fullOnyomi"] == ["ホウ"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["ほう"] and route["quizKunKeys"] == []
    pngs = list((V / "batch-062-native" / "attempt-1").glob("*.png"))
    assert len(pngs) == 37 and len({sha(p) for p in pngs}) == 17
    return freeze, processes


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    freeze, processes = audit()
    p = load(C / "progress.json")
    before = load(C / "execution-387-precheckpoint-progress.json")
    assert p["checkpoint"] == 386 and p["batch"] == "062"
    assert all(p[k] == v for k, v in before.items())
    assert set(p) - set(before) == {"execution387StartingState"}
    record_path = S / "execution-387.json"
    if sys.argv[1] == "finish":
        saved = git("rev-parse", "HEAD")
        assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
        assert not git("status", "--porcelain")
        record = load(record_path)
        checkpoint = {
            "execution": 387, "batch": "062", "savedCommit": saved, "signature": "G",
            "status": record["status"], "record": str(record_path.relative_to(R)),
            "recordSha256": sha(record_path), "nextAction": record["nextAction"],
            "recordedAt": datetime.now().astimezone().isoformat(),
            "publishedAdditions": 88, "remainingAdditions": 1140,
            "publicationAttempted": False, "nativeRerun": False, "androidRerun": False,
            "strictHistoricalProcessContractAccepted": False,
        }
        p.update(checkpoint=387, status="continue", stage=record["status"], blocker=None, nextAction=record["nextAction"])
        p["execution387StartingState"]["status"] = "signed-bounded-native-visual-checkpoint-complete"
        p["execution387CoordinatorCheckpoint"] = checkpoint
        p["batch062NativeVisualCheckpoint"] = checkpoint.copy()
        save(C / "progress.json", p)
        verification = {
            **checkpoint, "dedicatedWorktreesClean": True, "runtimeUnchanged": True,
            "originalNativeArtifactsVerified": len(freeze["nativeFiles"]),
            "actualModels": [x["actualModels"][0] for x in processes],
            "serialViewCalls": [len(x["toolCalls"]) for x in processes],
            "actualImagePayloadsArchived": 34, "distinctSourceImageHashes": 17,
            "historicalRecordsCompared": len(before), "fullHistoricalProgressPreserved": True,
            "wholeProjectComplete": False,
        }
        save(C / "execution-387-final-verification.json", verification)
        print(f"Checkpoint387 persisted: signed G {saved}; continue SAME062 combined-main acceptance next.")
        return
    assert sys.argv[1] == "stage" and not record_path.exists()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    next_action = (
        "SAME062 bounded native/visual acceptance reconciled at signed checkpoint387; teaching unchanged"
        "38ab6072. Read docs/n1-sources/execution-387.json and docs/n1-reviews/batch-062-native-acceptance.json. "
        "Original Claude1d12b838/GPT38b783dc dependent visual turns actual claude-opus-5.5/gpt-6.1-sol "
        "terminalexit0/28+27serialviews/zerooverlaps/onecallperresponse/17distinctPNGseach/"
        "34actual900x2000payloadsarchived/firstreport+auditBEFOREsecondlaunch. "
        "Both three-facet bounded verdicts CLEAN/no actionable content defect; seventeenhashgroups cover37PNGs. "
        "Fourfontrows俸棒奉借付人亻木給糸合/俸給 readable/distinct; actualfallbackfaceUNVERIFIED; "
        "table horizontalcrops/unseenviewports explicit. Meaning actualfallbacktiger/salary;stipend/mosquito/"
        "hill;knoll and readingホウ/チョウ/オウ/ヨウ unambiguous. MeaningBackBEFORENext notnewpersistedgrade; "
        "OnGood/noKunlog/DrawAgain separatelyasserted. Accepted384Android3+1/native386bothterminal0 "
        "retainedwithoutredundantrerun. Source/publiclookup limits/Claude062-P1/P2historicalviolations/"
        "fiveoptionalnotadopted preserved; dependentremediation NOTretroactivestrictinitialacceptance. "
        "NEXTboundedgate latestorigin/main fetch/normalnonrewritingmerge/accountallchanges, "
        "combinedsource-baseline-membership-reading-link-font-stroke/Python/vocab/validator/freshmanifest/"
        "original18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets; changedsubstantiveteaching "
        "needsoriginalreviewers. Normal signing then ownerfastforward/publicSHA/terminalgreenCI/"
        "everyimmutablepublicZIPruntimehash/budgets/terminalreceipts/ownerissue60 BEFOREdelivery or063. "
        "Do not rerun acceptedAndroid/native absent changedruntime/newconcern; no newblindinitials/"
        "063/secondrunner/concurrentheavywork/supervisorchanges. Actualpermissiondenial/signingwait: "
        "preserveexactcommand/error/report/yield,no retry/workaround. Original383denial and049hostOOM/"
        "qualifiedhost-only1GiB setting remain historical; no guest/appheap or archiveguardchanges. "
        "PreserveFULLlivehistory. Published88/1228,1140remain/89necessarysupportwords; localdraft89/90"
        "NOTdelivered. CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
        "Overallproject incomplete."
    )
    acceptance = {
        "schemaVersion": 1, "execution": 387, "batch": "062",
        "status": "batch-062-bounded-native-visual-reconciled-pending-combined-main-publication",
        "teachingSnapshot": TEACHING, "evidenceHead": HEAD,
        "nativeExecution": "docs/n1-sources/execution-386.json",
        "nativeAssertionsPassed": True, "independentVisualAcceptance": True,
        "boundedNativeAcceptance": True, "batchPublicationAcceptance": False,
        "strictHistoricalProcessContractAccepted": False,
        "reports": [{"family": family, "report": f"batch-062-visual-{family}.md",
                     "executionRecord": f"batch-062-visual-{family}-execution.json",
                     "actualModel": x["actualModels"][0], "sessionId": x["sessionId"],
                     "reportSha256": x["reportSha256"], "viewCalls": len(x["toolCalls"]),
                     "imagePayloads": x["imagePayloadsVerified"], "exitCode": x["exitCode"]}
                    for family, x in zip(("claude", "gpt"), processes)],
        "serialExitAndCompleteArchiveBeforeSecondLaunch": True,
        "sourcePngCount": 37, "distinctSourceImageHashes": 17, "actualModelVisiblePayloads": 34,
        "imageBoundary": "Sources1080x2400; both models received900x2000. All exact returned payloads archived, not source-byte-identical.",
        "verdicts": {name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"}
                     for name in ("kanji/俸.md", "words/俸給.md", "kanji/給.md:added line40 and coupled navigation")},
        "findings": [],
        "reconciliation": [
            {"status": "resolved", "facet": "bounded-native-visual",
             "claim": "No new actionable defect established; both models inspected all17distinct images, full three-file text, exact fixture ranges and terminal/route receipts.",
             "evidence": "Actual source glyphs, exposed prose, complete meaning/reading tasks and explicit drawing qualifications agree with unchanged teaching. Exact hashes and process audits independently verified."},
            {"status": "optional", "facet": "inherited-editorial-suggestions",
             "claim": "Five original Claude suggestions remain optional and not adopted; GPT offers none. No new actionable defect."},
            {"status": "resolved", "facet": "report-interpretation",
             "claim": "Claude's 'None of them could reasonably be accepted' follows a list including the correct salary option; interpreted as the three wrong alternatives, not a finding that salary is wrong.",
             "evidence": "Its same sentence and report identify correct salary feedback; GPT and coordinator actual meaning-question pixels independently confirm only salary; stipend is correct."},
            {"status": "unresolved", "facet": "strict-historical-process-acceptance",
             "claim": "Original062-P1/P2 violations remain historical. Bounded textual remediation and new compliant dependent visual turns are not retroactive strict initial-process acceptance.",
             "blockingBoundary": "No actionable current teaching/native defect; strict historical acceptance not claimed. Preserve coordinator/owner process adjudication and original reports."},
        ],
        "meaningOptions": ["tiger", "salary; stipend", "mosquito", "hill; knoll"],
        "onOptions": ["ホウ", "チョウ", "オウ", "ヨウ"],
        "persistenceBoundary": "Meaning feedback Back beforeNext is not new persisted grade. OnGood/noKunlog/DrawAgain separately asserted.",
        "glyphConclusion": "Four rows readable/distinguishable俸棒奉借付人亻木給糸合/俸給; actual fallback face UNVERIFIED.",
        "limits": "Dependent original-session confirmations, not new blind initials or fresh42family/upstream audits. Visible emulator viewports only, horizontal table crops/unseen article portions UNVERIFIED. Duplicate image hashes verified by coordinator, not reviewers. Supplied native run, reference-touch trace/recallmiss not MLKit or correct human recall. Physical-phone/general-release/current-main/publication/whole-set outstanding.",
        "runtimeChanged": False, "androidRerun": False, "nativeRerun": False,
        "publicationAttempted": False, "publishedAdditions": 88, "remainingAdditions": 1140,
        "nextAction": next_action,
    }
    save(V / "batch-062-native-acceptance.json", acceptance)
    receipts = V / "batch-062-native" / "execution-receipts"
    artifacts = [
        "prepare-execution-387.py", "run-execution-387-visual.ps1", "archive-execution-387-visual.py",
        "close-execution-387.py", "batch-062-visual-task.txt", "batch-062-visual-freeze.json",
        "copilot-help-execution-387.txt", "copilot-model-settings-execution-387.txt",
        "batch-062-visual-claude-prompt.txt", "batch-062-visual-gpt-prompt.txt",
    ]
    copied = []
    for name in artifacts:
        target = receipts / name
        assert not target.exists()
        shutil.copyfile(C / name, target)
        copied.append({"path": str(target.relative_to(R)), "sha256": sha(target)})
    checks = []
    for args in (["tools\\validate.py"], ["tools\\build_manifest.py"], ["tools\\check_content_budget.py"]):
        run = subprocess.run(["python", "-B", *args], cwd=R, capture_output=True, text=True, encoding="utf-8")
        log_path = receipts / ("execution-387-" + Path(args[0]).stem + ".txt")
        log_path.write_text(run.stdout + run.stderr, encoding="utf-8")
        checks.append({"command": ["python", "-B", *args], "exitCode": run.returncode,
                       "log": str(log_path.relative_to(R)), "sha256": sha(log_path)})
        assert run.returncode == 0, run.stdout + run.stderr
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    ledger_path = S / "batch-062-progress.json"
    ledger = load(ledger_path)
    ledger["status"] = acceptance["status"]
    ledger["nativeVisualConfirmation"] = {
        "execution": 387, "acceptance": "docs/n1-reviews/batch-062-native-acceptance.json",
        "acceptanceSha256": sha(V / "batch-062-native-acceptance.json"),
        "independentVisualAcceptance": True, "boundedNativeAcceptance": True,
        "runtimePublished": False, "strictHistoricalProcessContractAccepted": False,
        "actualModels": [x["actualModels"][0] for x in processes],
        "nextAction": next_action,
    }
    save(ledger_path, ledger)
    save(record_path, {
        "schemaVersion": 1, "execution": 387, "batch": "062", "status": acceptance["status"],
        "recordedAt": datetime.now().astimezone().isoformat(), "startingHead": HEAD,
        "scope": p["execution387StartingState"]["scope"],
        "reviewedTeachingSnapshot": TEACHING,
        "acceptance": "docs/n1-reviews/batch-062-native-acceptance.json",
        "acceptanceSha256": sha(V / "batch-062-native-acceptance.json"),
        "originalNativeArtifactsVerified": len(freeze["nativeFiles"]),
        "allFrozenTeachingAndOriginalReportsUnmodified": True,
        "freshChecks": checks, "archivedExecutionArtifacts": copied,
        "archivalAuditCorrection": "First local audit stopped before any acceptance/ledger output because it incorrectly required Claude edit/create tool names in the GPT configuration. Exact evidence shows GPT apply_patch disabled instead. Corrected model-specific disabled-edit assertion; both actual reviewers had view only. No reviewer/native rerun or permission change.",
        "android384AndNative386RetainedWithoutRerun": True,
        "independentVisualAcceptance": True, "boundedNativeAcceptance": True,
        "strictHistoricalProcessContractAccepted": False,
        "runtimeChanged": False, "runtimePublished": False, "publicationAttempted": False,
        "publishedAdditions": 88, "remainingAdditions": 1140,
        "limits": acceptance["limits"], "nextAction": next_action,
    })
    print("Both complete dependent reports reconciled; exact source/returned bytes and serial process audited. Fresh validator/manifest/budget pass; runtime unchanged. Ready for normal signed local evidence commit.")


if __name__ == "__main__":
    main()
