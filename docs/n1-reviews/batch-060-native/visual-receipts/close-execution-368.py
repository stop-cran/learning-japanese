import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
V = R / "docs" / "n1-reviews"
S = R / "docs" / "n1-sources"
N = V / "batch-060-native"
START = "8f9bad077f40cac9a31523a27d192accc59dcd0d"
TEACHING = "ea1dac1a6fd2c452db9cf602442e1f287ff95c67"
STATUS = "bounded-native-visual-reconciled-pending-combined-main-publication"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution368.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=R):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


def audit():
    assert not git("diff", TEACHING, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    android = C.parent / "kanji-cards-android"
    assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", tree=android)
    freeze = load(C / "batch-060-visual-freeze.json")
    index_path = N / "execution-367-artifact-index.json"
    assert sha(index_path) == freeze["artifactIndexSha256"]
    index = load(index_path)
    for row in index["files"]:
        assert sha(R / row["path"]) == row["sha256"]
        assert (R / row["path"]).stat().st_size == row["bytes"]
    pngs = list((N / "attempt-1").glob("*.png"))
    assert len(pngs) == 36 and len({sha(x) for x in pngs}) == 19
    native = load(S / "execution-367.json")
    assert native["nativeAssertionsPassed"] and not native["independentVisualAcceptance"]
    raw = (N / "attempt-1" / "instrumentation.txt").read_text(encoding="utf-8")
    assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw, re.M) == ["1", "0", "1", "0"]
    assert "Time: 88.09" in raw and "OK (2 tests)" in raw
    route = load(N / "attempt-1" / "n1-060-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1 and not route["phoneEvidence"]
    assert [route[x] for x in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1072, 5031, 92, 0, 1]
    assert route["contentVersion"] == "dbf047f0c2e6cd56"
    assert route["fullOnyomi"] == ["テイ", "チン"] and route["fullKunyomi"] == []
    assert route["quizOnKeys"] == ["てい"] and route["quizKunKeys"] == []
    assert route["touchInjectedReferenceStrokes"] == 9
    assert all(route[x] for x in (
        "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
        "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
        "drawingGradeRecordedOnNext", "offline",
    ))
    android_evidence = load(S / "execution-365.json")
    for row in android_evidence["archivedArtifacts"]:
        assert sha(R / row["path"]) == row["sha256"]
    for row in android_evidence["recovery"]["tests"]:
        for path in (Path(row["sourcePath"]), Path(row["artifactPath"])):
            assert sha(path) == row["sha256"]
            suite = ET.parse(path).getroot()
            assert int(suite.attrib["tests"]) == row["tests"]
            assert all(int(suite.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
            assert suite.attrib["timestamp"] == row["timestamp"]
            assert sorted(x.attrib["name"] for x in suite.findall("testcase")) == sorted(row["caseNames"])
    for row in android_evidence["provenance"]:
        assert sha(Path(row["path"])) == row["sha256"]
    original = load(V / "batch-060-initial-review-checkpoint.json")
    assert not original["strictInitialInternalSerializationAccepted"]
    for row in original["reviewProcesses"]:
        prefix = "batch-060-" + row["label"]
        for suffix, key in (
            (".md", "reportSha256"), ("-execution.json", "executionRecordSha256"),
            ("-coverage.json", "coverageRecordSha256"),
        ):
            assert sha(V / (prefix + suffix)) == row[key]
        assert sha(C / (prefix + ".jsonl")) == row["rawExecutionSha256"]
    assert sha(V / "batch-060-reconciliation.json") == android_evidence["reconciliationSha256"]
    labels = ("claude", "gpt", "claude-glyph")
    processes = [load(V / f"batch-060-visual-{label}-execution.json") for label in labels]
    assert [x["actualModels"] for x in processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"], ["claude-opus-5.5"]]
    assert [len(x["toolCalls"]) for x in processes] == [29, 28, 1]
    assert [x["imagePayloadsVerified"] for x in processes] == [19, 19, 1]
    for prior, following, label in zip(processes, processes[1:], labels):
        assert datetime.fromisoformat(prior["completedAt"]) < datetime.fromisoformat(following["startedAt"])
        for suffix in (".md", "-execution.json"):
            assert (V / f"batch-060-visual-{label}{suffix}").stat().st_mtime < datetime.fromisoformat(following["startedAt"]).timestamp()
    for label, process in zip(labels, processes):
        assert process["exitCode"] == 0 and not process["unfinishedTools"]
        assert not process["observedToolOverlaps"] and not process["multiToolResponses"]
        assert max(process["requestsPerAssistantResponse"]) == 1
        assert process["expectedPngMembershipReturned"]
        assert sha(V / f"batch-060-visual-{label}.md") == process["reportSha256"]
        assert sha(C / f"batch-060-visual-{label}.jsonl") == process["rawExecutionSha256"]
        assert process["usage"]["currentModel"] == process["actualModels"][0]
        disabled = "\n".join(x["message"] for x in process["configurationEvidence"])
        assert all(x in disabled for x in ("powershell", "task", "web_fetch", "write_agent"))
        for call in process["toolCalls"]:
            assert call["name"] == "view" and call["success"] and not call["truncationOrLimitMarker"]
            if "imagePayload" in call:
                image = call["imagePayload"]
                assert sha(R / image["returnedPayloadCopy"]) == image["sha256"]
                assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
                assert image["sourceDimensions"] == [1080, 2400] and image["returnedDimensions"] == [900, 2000]
                assert not image["exactFileBytesReturnedToModel"]
            else:
                assert call["exactRequestedTextContainedInResult"]
    return index, processes


def main():
    progress = load(C / "progress.json")
    before = load(C / "execution-368-starting-progress.json")
    record_path = S / "execution-368.json"
    acceptance_path = V / "batch-060-native-acceptance.json"
    assert progress["checkpoint"] == 367 and progress["batch"] == "060"
    index, processes = audit()
    if sys.argv[1] == "finish":
        saved = git("rev-parse", "HEAD")
        assert git("rev-parse", "HEAD^") == START
        assert git("log", "-1", "--format=%G?") == "G"
        assert not git("status", "--porcelain")
        assert not git("diff", START, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json")
        record = load(record_path)
        checkpoint = {
            "schemaVersion": 1, "execution": 368, "batch": "060", "status": STATUS,
            "savedCommit": saved, "signature": "G", "record": str(record_path.relative_to(R)),
            "recordSha256": sha(record_path), "nextAction": record["nextAction"],
            "recordedAt": datetime.now().astimezone().isoformat(),
            "publishedAdditions": 86, "remainingAdditions": 1142,
            "publicationAttempted": False, "nativeRerun": False, "androidRerun": False,
            "boundedIndependentVisualAcceptance": True,
            "strictHistoricalProcessContractAccepted": False,
        }
        progress.update(
            checkpoint=368, status="continue",
            stage="batch-060-bounded-native-visual-reconciled-pending-combined-main-publication",
            blocker=None, nextAction=record["nextAction"],
        )
        progress["execution368StartingState"]["status"] = "signed-bounded-native-visual-checkpoint-complete"
        progress["execution368CoordinatorCheckpoint"] = checkpoint
        progress["batch060NativeVisualCheckpoint"] = checkpoint.copy()
        mutable = {"checkpoint", "status", "stage", "blocker", "nextAction"}
        assert all(progress[k] == v for k, v in before.items() if k not in mutable)
        save(C / "progress.json", progress)
        verification = {
            **checkpoint, "checkpoint": 368, "dedicatedWorktreesClean": True,
            "runtimeUnchanged": True, "historicalRecordsCompared": len(before) - len(mutable),
            "fullHistoricalProgressPreserved": True, "nativeArtifactHashesReverified": len(index["files"]),
            "actualReturnedImagePayloadsVerified": 39, "reviewerProcessesExited": True,
            "wholeProjectComplete": False, "changedPaths": load(C / "execution-368-staged-inventory.json"),
        }
        save(C / "execution-368-final-verification.json", verification)
        print(f"Checkpoint368 persisted: signed G {saved}; continue SAME060 combined-main acceptance next.")
        return
    assert sys.argv[1] == "stage"
    assert git("rev-parse", "HEAD") == START and git("log", "-1", "--format=%G?") == "G"
    assert not record_path.exists() and not acceptance_path.exists()
    checks = []
    for args in (["tools\\validate.py"], ["tools\\build_manifest.py"], ["tools\\check_content_budget.py"]):
        result = subprocess.run(["python", "-X", "utf8", "-B", *args], cwd=R, text=True, encoding="utf-8", capture_output=True)
        check = {"command": ["python", "-X", "utf8", "-B", *args], "exitCode": result.returncode,
                 "stdout": result.stdout, "stderr": result.stderr}
        checks.append(check)
        assert result.returncode == 0, check
    assert not git("diff", "--", "manifest.json")
    receipts = N / "visual-receipts"
    receipts.mkdir()
    names = [
        "batch-060-visual-task.txt", "batch-060-visual-freeze.json",
        "batch-060-visual-claude-glyph-task.txt", "run-batch-060-visual.ps1",
        "run-batch-060-visual-claude-glyph.ps1", "archive-batch-060-visual.py",
        "prepare-execution-368.py", "close-execution-368.py",
    ]
    for label in ("claude", "gpt", "claude-glyph"):
        names += [f"batch-060-visual-{label}-{suffix}" for suffix in ("process.json", "usage.json", "stderr.txt")]
    copied = []
    for name in names:
        source, destination = C / name, receipts / name
        shutil.copyfile(source, destination)
        assert sha(source) == sha(destination)
        copied.append({"path": str(destination.relative_to(R)), "sha256": sha(destination)})
    next_action = (
        "SAME060 bounded native/ORIGINAL two-family visual confirmation reconciled; signed LOCAL evidence checkpoint368 "
        "only, NOT runtime publication or retroactive strict historical process acceptance. OriginalClaude34dbb43d "
        "actualclaude-opus-5.5 THEN originalGPT8130aa10 actualgpt-6.1-sol exited0SERIAL:29/28viewcalls respectively, "
        "19distinctPNGpayloads EACH, ZEROoverlaps/multitoolresponses. Claude complete report+audit archived BEFORE "
        "GPTlaunch. OriginalClaude single-image glyph-report clarification then exited0/ONEview; GPT completearchive "
        "preceded it. All39actual900x2000modelpayloads separately archived from1080x2400sources.36sourcePNGs/"
        "19distinct/17equivalent. Both no new actionable teaching/visible-task defect, all4boundedteachingscopes "
        "threefacetsCLEAN;停native route NOTexercised. Fourfontrows亭停京享高 distinct/亠亻冖丁小子口料料亭 "
        "readable/no blankboxes; fallbackfaceunknown. Tablescroll/croppedoffscreenlabels not everytablepixel/"
        "inaccessibility certification. Actualmeaningchoicesmulberry/enjoy;receivebenefits/pavilion;restaurantbuilding/"
        "firefly, actualonchoicesヘイテイキョウバイ; fullfeedbackテイチン lookupNOTextraquizkey. "
        "Originalreports/363textualclosure/Claude060-P1/P2 historicalnoncompliance preserved; supervisedlexical "
        "remediation and dependentvisuals NOTretroactivestrictinitialacceptance. Accepted365freshAndroid3+1 and367 "
        "native2case0/noskips88.09s/fullContentSyncONCE1072kanji5031words92N1/dbf047f0c2e6cd56/problems0/epoch1/"
        "Full+Liteorderedテイチン/emptykun/curatedてい/no-kun/twopairsfourdirections/SystemBack/offline/meaningBack"
        "withoutNext/solecuratedOnGood/ninereference-touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain "
        "retained without rerun. NOTMLKit/correcthumanrecall/phone. Original364permissiondenial and049HOST512MiBOOM/"
        "qualifiedhost-only1GiBinit unchanged. NEXT bounded checkpoint latestorigin/main fetch/normalnonrewritingmerge, "
        "surgicalconflicts/reviewsubstantiveteaching; ALLcombined frozen-source/baseline/exactmembership/originalguards/"
        "readings/links/strokes/fonts/currentPython/vocabulary/validator/freshmanifest/18000entries42MiBcompressed"
        "80MiBinflated56MiBretainedbudgets/normalsigning/ownerfastforward/exactremoteSHA/terminalgreenCI/EVERY"
        "immutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFOREdelivery or061. No accepted365Android/"
        "367native/initialreview/visual rerun absent new concern. Actualpermissiondenial/signingwait preserveexact"
        "command-error/report/yield, no retry/workaround. Preserve FULLlivehistory/no061/secondrunner/concurrentheavywork/"
        "supervisorchanges. Published86/1228,1142remaining latest05948d7110f unchanged; compatibleAndroidf9b59a2+ required; "
        "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
    )
    acceptance = {
        "schemaVersion": 1, "execution": 368, "batch": "060", "status": STATUS,
        "snapshot": START, "reviewedTeachingSnapshot": TEACHING,
        "nativeEvidence": "n1-sources/execution-367.json", "nativeEvidenceSha256": sha(S / "execution-367.json"),
        "textualReconciliation": "batch-060-reconciliation.json",
        "textualReconciliationSha256": sha(V / "batch-060-reconciliation.json"),
        "reviewers": [{
            "model": process["actualModels"][0], "sessionId": process["sessionId"],
            "report": f"batch-060-visual-{label}.md", "reportSha256": process["reportSha256"],
            "execution": f"batch-060-visual-{label}-execution.json",
            "executionSha256": sha(V / f"batch-060-visual-{label}-execution.json"),
            "toolCalls": len(process["toolCalls"]), "imagePayloads": process["imagePayloadsVerified"],
            "overlaps": 0, "multiToolResponses": 0, "exitCode": 0,
            "startedAt": process["startedAt"], "completedAt": process["completedAt"],
            "freshScope": "Own initial report, complete亭/料亭/料/停, fixture54-148/150-270/271-430,19distinctPNGpayloads; Claude also own latest supervised lexical confirmation." if label != "claude-glyph" else "Exactly one font-pairs PNG; original visual report's other judgments and limits inherited unchanged.",
        } for label, process in zip(("claude", "gpt", "claude-glyph"), processes)],
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"}
            for name in ("kanji/亭.md", "words/料亭.md", "kanji/料.md:added-link", "kanji/停.md:added-link-text-only")
        },
        "findings": [], "newActionableDefects": [],
        "reportingGap": {
            "status": "resolved", "kind": "omitted-specific-glyph-observations",
            "evidence": "Original Claude visual report retained19reads but omitted specific four-font observations. One-image original-session clarification explicitly confirms every assigned glyph in all four rows. Original report unchanged.",
        },
        "optional": [
            {"origin": "claude", "status": "optional", "claim": "Drawing stroke label9 sits near the hook.", "disposition": "Nonblocking app-rendering observation; no established teaching or glyph defect and no unrelated UI change."},
            {"origin": "claude", "status": "optional", "claim": "Food-example and place-particle captures show the same visible content.", "disposition": "Overlapping viewport coverage, not byte equivalence: their source hashes are different. No additional independent scene/coverage claim."},
        ],
        "coordinatorAdjudication": [
            "Both reviews retain inherited textual correctness/coverage with new bounded screenshot comprehension evidence. No new actionable defect established; no teaching edits.",
            "亭/料亭 and料addedlink are visually sampled. 停addedlink is textually reviewed only; no native route proof claimed.",
            "Claude's original completeチンrow wording is bounded to the visible example text. The left reading label is clipped; no whole-row/table certification.",
            "Glyph clarification closes a report omission only, not a linguistic fix, new blind review or historical process repair.",
            "Static links/screenshots do not prove taps or persistence. Independently reverified367 raw terminal results and fixture/route establish those operational facts.",
            "Actual meaning choices differ from authored wrong-choice trio. All displayed choices and reading feedback inspected, no ambiguous answer established.",
            "Original060-P1/P2 remain partially resolved: supervised remediation complete but original strict process violations irreversible.",
        ],
        "glyphObservation": "Fourproductionfontrows亭停京享高 distinct; actual亠亻冖丁小子口料料亭 readable/no blankboxes. Textbook thinner/lowercontrast but readable; fallbackfaceunknown.",
        "pngAccounting": {
            "sourceFiles": 36, "distinctSourceHashes": 19, "equivalentCopies": 17,
            "sourceDimensions": [1080, 2400], "returnedDimensions": [900, 2000],
            "actualReturnedPayloadCopies": 39, "exactSourceBytesReturned": False,
        },
        "nativeAssertionsPassed": True, "boundedIndependentVisualAcceptance": True,
        "strictHistoricalProcessContractAccepted": False, "wholeArticlePixelCoverage": False,
        "physicalPhoneAcceptance": False, "generalReleaseAcceptance": False,
        "publicationAttempted": False, "wholeSetAcceptance": False,
        "limits": "Dependent original-session visual confirmation, not new blind initial or fresh upstream dictionary review. Supplied operations hash/XML/log-verified by coordinator, not reviewer-executed. Drawing reference-touch trace/recallmiss not MLKit or successful human recall. Unseen cells/pixels,停native route and unidentified fallback face remain limits. Cumulative usage is not current-turn cost. Historical process noncompliance remains explicit.",
    }
    save(acceptance_path, acceptance)
    record = {
        "schemaVersion": 1, "execution": 368, "batch": "060", "status": STATUS,
        "startingHead": START, "startingSignature": "G", "reviewedTeachingSnapshot": TEACHING,
        "scope": progress["execution368StartingState"]["scope"],
        "authorization": progress["execution368StartingState"]["authorization"],
        "recordedAt": datetime.now().astimezone().isoformat(),
        "acceptance": str(acceptance_path.relative_to(R)), "acceptanceSha256": sha(acceptance_path),
        "nativeArtifactHashesReverified": len(index["files"]),
        "originalReportsAndReconciliationReverified": True, "freshAndroidNamedCasesReverified": 4,
        "freshAndroidSkipped": 0, "nativeTerminalCaseStatusesReverified": [0, 0],
        "nativeRerun": False, "androidRerun": False, "teachingChanged": False,
        "reviewerProcessesSerialAndExited": True, "firstReportAndAuditArchivedBeforeSecond": True,
        "newVisualOverlaps": 0, "newVisualMultiToolResponses": 0,
        "sourcePngCount": 36, "distinctPngCount": 19, "actualModelPayloadCopiesVerified": 39,
        "coordinatorDirectImageReadsThisExecution": [
            "n1-060-font-pairs.png", "n1-060-meaning-question.png", "n1-060-kanji-curation.png",
        ],
        "historicalProcessNoncompliancePreserved": True, "validation": checks,
        "archivedExecutionReceipts": copied, "runtimeUnchanged": True, "manifestUnchanged": True,
        "publicationAttempted": False, "publishedAdditions": 86, "remainingAdditions": 1142,
        "nextAction": next_action, "limits": acceptance["limits"],
    }
    save(record_path, record)
    batch_path = S / "batch-060-progress.json"
    batch = load(batch_path)
    assert batch["status"] == "native-assertions-passed-pending-independent-visual"
    batch.update(
        status=STATUS, nextAction=next_action, nativeVisualCheckpoint="execution-368.json",
        nativeVisualAcceptance={
            "record": str(acceptance_path.relative_to(R)), "sha256": sha(acceptance_path),
            "boundedIndependentVisualAcceptance": True, "strictHistoricalProcessContractAccepted": False,
            "sourceScreenshots": 36, "distinctScreenshots": 19, "actualModelPayloadCopies": 39,
            "nativeOrAndroidRerun": False, "publicationAttempted": False,
        },
        independentReview="Original two-family textual review and bounded native visual supplements closed. All four bounded teaching scopes CLEAN in three facets;停native route unexercised. Original060-P1/P2 remain historical noncompliance, not retroactive strict initial acceptance.",
        limits=acceptance["limits"] + " Combined-main batch acceptance, CI, immutable public archive and publication remain pending.",
    )
    for mapping in batch["supportMappings"]:
        mapping["status"] = "textual-and-bounded-native-visual-review-closed-pending-integration-and-publication"
    save(batch_path, batch)
    stage = [str(x.relative_to(R)) for x in (
        record_path, acceptance_path, batch_path, R / "docs" / "n1-authoring-notes.md",
        V / "batch-060-copilot-help-execution-368.txt", V / "batch-060-copilot-model-catalog-execution-368.txt",
    )]
    for label in ("claude", "gpt", "claude-glyph"):
        stage += [str((V / f"batch-060-visual-{label}{suffix}").relative_to(R)) for suffix in (".md", "-execution.json")]
        stage += [str(x.relative_to(R)) for x in sorted((N / f"visual-{label}-returned").iterdir())]
    stage += [row["path"] for row in copied]
    save(C / "execution-368-staged-inventory.json", stage)
    subprocess.run(["git", "add", "--", *stage], cwd=R, check=True)
    assert set(filter(None, git("diff", "--cached", "--name-only", "-z").split("\0"))) == {x.replace("\\", "/") for x in stage}
    assert not git("diff", "--cached", "--check")
    print(f"Verified and staged {len(stage)} evidence files; runtime unchanged. Normal signed commit required.")


if __name__ == "__main__":
    main()
