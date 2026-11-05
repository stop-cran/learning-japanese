import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
reviews = r / "docs" / "n1-reviews"
native = reviews / "batch-059-native"
sources = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution358.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = "b4173065b2b78d697e41279777c177a8d92e58c5"
teaching = "769293c824dc41abb9386e76c4dd5f8c676e48e0"
record_path = sources / "execution-358.json"
acceptance_path = reviews / "batch-059-native-acceptance.json"
p = load(c / "progress.json")
assert p["checkpoint"] == 357 and p["batch"] == "059"
if len(sys.argv) > 1 and sys.argv[1] == "finish":
    assert not git("status", "--porcelain")
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == head
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", head, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json")
    record = load(record_path)
    checkpoint = {
        "execution": 358, "batch": "059", "status": record["status"],
        "savedCommit": saved, "signature": "G", "record": str(record_path.relative_to(r)),
        "recordSha256": sha(record_path), "nextAction": record["nextAction"],
        "recordedAt": datetime.now().astimezone().isoformat(),
        "publishedAdditions": 85, "remainingAdditions": 1143,
        "publicationAttempted": False, "nativeRerun": False, "androidRerun": False,
        "strictHistoricalProcessContractAccepted": False,
    }
    p.update(checkpoint=358, status="continue",
             stage="batch-059-bounded-native-visual-reconciled-pending-combined-main-publication",
             blocker=None, nextAction=record["nextAction"])
    p["execution358StartingState"]["status"] = "signed-bounded-native-visual-checkpoint-complete"
    p["execution358CoordinatorCheckpoint"] = checkpoint
    p["batch059NativeVisualCheckpoint"] = checkpoint.copy()
    before = load(c / "execution-358-starting-progress.json")
    assert all(p[k] == v for k, v in before.items() if k not in (
        "checkpoint", "status", "stage", "blocker", "nextAction",
    ))
    save(c / "progress.json", p)
    print(f"Checkpoint358 persisted: signed G {saved}; continue SAME059 combined-main acceptance next.")
    sys.exit(0)

assert not record_path.exists() and not acceptance_path.exists()
assert git("rev-parse", "HEAD") == head and git("log", "-1", "--format=%G?") == "G"
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json")
android = c.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=android)
freeze = load(c / "batch-059-visual-freeze.json")
for section in ("files", "teachingFiles"):
    for name, h in freeze[section].items():
        assert sha(r / name) == h
for name, h in freeze["originalReports"].items():
    assert sha(reviews / name) == h
index = load(native / "execution-357-artifact-index.json")
for row in index["files"]:
    assert sha(r / row["path"]) == row["sha256"]
prior = load(sources / "execution-357.json")
assert sha(native / "execution-357-artifact-index.json") == prior["artifactIndexSha256"]
assert prior["nativeAssertionsPassed"] and not prior["independentVisualAcceptance"]
raw = (native / "attempt-1" / "instrumentation.txt").read_text(encoding="utf-8")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw, re.M) == ["1", "0", "1", "0"]
assert "Time: 101.725" in raw and "OK (2 tests)" in raw
route = load(native / "attempt-1" / "n1-059-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1 and not route["phoneEvidence"]
assert [route[x] for x in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1071, 5030, 91, 0, 1]
assert route["contentVersion"] == "1f1ad78479e9c1f4"
assert route["fullOnyomi"] == ["キョウ", "コウ"] and route["fullKunyomi"] == ["う.ける"]
assert route["quizOnKeys"] == ["きょう"] and route["quizKunKeys"] == []
assert all(route[x] for x in (
    "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
    "soleCuratedOnQuestionAndPersistedGradeNoKun", "drawingTraceThenRecall",
    "drawingGradeRecordedOnNext", "offline",
))
a = load(sources / "execution-355.json")
for row in a["archivedArtifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
for row in a["recovery"]["tests"]:
    for path in (Path(row["sourcePath"]), Path(row["artifactPath"])):
        assert sha(path) == row["sha256"]
        suite = ET.parse(path).getroot()
        assert int(suite.attrib["tests"]) == row["tests"]
        assert all(int(suite.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
        assert suite.attrib["timestamp"] == row["timestamp"]
        assert sorted(x.attrib["name"] for x in suite.findall("testcase")) == sorted(row["caseNames"])
for row in a["provenance"]:
    assert sha(Path(row["path"])) == row["sha256"]

processes = [load(reviews / f"batch-059-visual-{label}-execution.json") for label in ("claude", "gpt")]
assert [x["actualModels"] for x in processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
assert (reviews / "batch-059-visual-claude.md").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
assert (reviews / "batch-059-visual-claude-execution.json").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
for label, process in zip(("claude", "gpt"), processes):
    assert process["exitCode"] == 0 and not process["unfinishedTools"]
    assert len(process["toolCalls"]) == 29 and process["imagePayloadsVerified"] == 20
    assert not process["observedToolOverlaps"] and not process["multiToolResponses"]
    assert max(process["requestsPerAssistantResponse"]) == 1 and process["expectedPngMembershipReturned"]
    assert sha(reviews / f"batch-059-visual-{label}.md") == process["reportSha256"]
    assert sha(c / f"batch-059-visual-{label}.jsonl") == process["rawExecutionSha256"]
    assert len(process["configurationEvidence"]) == 1
    disabled = process["configurationEvidence"][0]["message"]
    assert "powershell" in disabled and "task" in disabled and "web_fetch" in disabled
    for call in process["toolCalls"]:
        assert call["name"] == "view" and call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
            assert image["sourceDimensions"] == [1080, 2400] and image["returnedDimensions"] == [900, 2000]
            assert not image["exactFileBytesReturnedToModel"]
        else:
            assert call["exactRequestedTextContainedInResult"]
pngs = list((native / "attempt-1").glob("*.png"))
assert len(pngs) == 35 and len({sha(x) for x in pngs}) == 20
checks = []
for args in (["tools\\validate.py"], ["tools\\build_manifest.py"], ["tools\\check_content_budget.py"]):
    result = subprocess.run(["python", "-X", "utf8", "-B", *args], cwd=r, text=True, encoding="utf-8", capture_output=True)
    check = {"command": ["python", "-X", "utf8", "-B", *args], "exitCode": result.returncode,
             "stdout": result.stdout, "stderr": result.stderr}
    checks.append(check)
    assert result.returncode == 0, check
assert not git("diff", "--", "manifest.json")
receipts = native / "visual-receipts"
receipts.mkdir()
names = [
    "batch-059-visual-task.txt", "batch-059-visual-freeze.json",
    "run-batch-059-visual.ps1", "archive-batch-059-visual.py", "close-batch-059-visual.py",
    "execution-358-start.py", "copilot-help-execution-358.txt", "copilot-model-settings-execution-358.txt",
]
for label in ("claude", "gpt"):
    names += [f"batch-059-visual-{label}-{suffix}" for suffix in ("process.json", "usage.json", "stderr.txt")]
copied = []
for name in names:
    source, dest = c / name, receipts / name
    if name.startswith("copilot-"):
        dest.write_text(source.read_text(encoding="utf-8-sig").rstrip() + "\n", encoding="utf-8")
    else:
        shutil.copyfile(source, dest)
        assert sha(source) == sha(dest)
    copied.append({"path": str(dest.relative_to(r)), "sha256": sha(dest),
                   "sourceSha256": sha(source),
                   "normalization": "CLI capture only: UTF-8 LF, no BOM, one terminal newline." if name.startswith("copilot-") else "none"})
next_action = (
    "SAME059 bounded native/ORIGINAL two-family visual confirmation reconciled; signed LOCAL evidence checkpoint358 "
    "only, NOT runtime publication or retroactive strict historical process acceptance. OriginalClaude57374784 actual"
    "claude-opus-5.5 thenGPT345c7cb4 actualgpt-6.1-sol exited0SERIAL:29viewcalls/20distinctPNGpayloads EACH, ZERO"
    "overlaps or multi-tool responses; Claude complete report+audit archived BEFORE GPTlaunch. Both no new actionable"
    "teaching/visible-task defect;059-F1 resolved. Original reports/353textualclosure/Claudehistoricalconfirmation"
    "overlap remain immutable; supplement NOTrepair. 35sourcePNGs20distinct15equivalent;1080x2400sources and actual"
    "900x2000modelpayloads separately preserved. Fourfontrows享京厚高 distinct/亠厂子口受享受 readable/no boxes; "
    "fallbackfaceunknown. Recognitionexample visible but leftreadinglabel cropped; no complete-table/every-pixel "
    "certification. Staticlinks do NOTprove routes; accepted357actual2case0/noskips101.725s/fullContentSyncONCE"
    "1071kanji5030words91N1/1f1ad78479e9c1f4/problems0/epoch1/Full+Liteorderedキョウコウ/う.ける/"
    "curatedきょう/no-kun/twopairsfourdirections/SystemBack/offline/meaningBackwithoutNext/"
    "solecuratedOnGood/eightreference-touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain retained "
    "without rerun. NOTMLKit/correcthumanrecall/phone. Accepted355freshAndroid3+1 retained; original354denial "
    "and049HOST512MiBOOM/samequalifiedhost-only1GiBinit unchanged. NEXT bounded checkpoint latestorigin/main "
    "fetch/normalnonrewritingmerge, surgicalconflicts/reviewsubstantiveteaching; ALLcombined frozen-source/baseline/"
    "exactmembership/originalguards/readings/links/strokes/fonts/currentPython/vocabulary/validator/freshmanifest/"
    "18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normalsigning/ownerfastforward/exactremoteSHA/"
    "terminalgreenCI/EVERYimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFOREdelivery or060. "
    "No accepted355Android/357native/initialreview/visual rerun absent new concern. Actualpermissiondenial/"
    "signingwait preserveexactcommand-error/report/yield, no retry/workaround. Preserve FULLlivehistory/"
    "no060/secondrunner/concurrentheavywork/supervisorchanges. Published85/1228,1143remaining latest058"
    "633f6002 unchanged; compatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
    "Overallproject incomplete."
)
acceptance = {
    "schemaVersion": 1, "execution": 358, "batch": "059",
    "status": "bounded-native-visual-reconciled-pending-combined-main-publication",
    "snapshot": head, "reviewedTeachingSnapshot": teaching,
    "nativeEvidence": "n1-sources/execution-357.json",
    "nativeEvidenceSha256": sha(sources / "execution-357.json"),
    "textualReconciliation": "batch-059-reconciliation.json",
    "textualReconciliationSha256": sha(reviews / "batch-059-reconciliation.json"),
    "reviewers": [{
        "model": x["actualModels"][0], "sessionId": x["sessionId"],
        "report": f"batch-059-visual-{label}.md", "reportSha256": x["reportSha256"],
        "execution": f"batch-059-visual-{label}-execution.json",
        "executionSha256": sha(reviews / f"batch-059-visual-{label}-execution.json"),
        "toolCalls": 29, "imagePayloads": 20, "overlaps": 0, "multiToolResponses": 0,
        "startedAt": x["startedAt"], "completedAt": x["completedAt"], "exitCode": 0,
        "freshScope": "Own original+confirmation reports; complete享/享受/受; fixture54-142,150-270,271-430;20distinctPNGpayloads.",
    } for label, x in zip(("claude", "gpt"), processes)],
    "verdicts": {
        name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"}
        for name in ("kanji/享.md", "words/享受.md", "kanji/受.md:added享受link-and-coupled-behavior")
    },
    "findings": [{"id": "059-F1", "status": "resolved", "discovery": "Original Claude only; unchanged attribution.",
                  "evidence": "Corrected recognition-spelling example text visible in shifted reading table; source meaning inherited from353."}],
    "newActionableDefects": [],
    "optional": "Original Claude optional高contrast/artuse/source-line expansion remain optional; GPTnone. No expansion made.",
    "coordinatorAdjudication": [
        "Both20-image reviews establish bounded readability, not every article/table pixel.",
        "Claude's 'row fully visible' is bounded to its example text; the left reading label is visibly clipped. No whole-row/table certification.",
        "Claude's Android acceptance limit is reviewer non-execution, not reversal of accepted355 operational results.",
        "Static visible links do not independently prove four transitions or Back; accepted357 fixture/results establish those operational facts.",
        "Meaning fallback choices differ from authored distractors: suspicious;uncanny/pig;pork/enjoy;receive benefits/grain-bearing head. Unique correct answer visible.",
        "Onchoicesキュウ/ボウ/リュウ/キョウ; feedback fullキョウ/コウ/うける is lookup, not extra practice keys.",
        "Earlier Claude confirmation overlap persists; current zero-overlap reviews do not retroactively satisfy historical strict process compliance.",
    ],
    "glyphObservation": "Fourproductionfontrows享京厚高 distinct/亠厂子口受享受 readable/no replacement boxes; fallback face unknown.",
    "pngAccounting": {"sourceFiles": 35, "distinctSourceHashes": 20, "equivalentCopies": 15,
                      "sourceDimensions": [1080, 2400], "returnedDimensions": [900, 2000],
                      "actualReturnedPayloadCopies": 40, "exactSourceBytesReturned": False},
    "nativeAssertionsPassed": True, "boundedIndependentVisualAcceptance": True,
    "strictHistoricalProcessContractAccepted": False, "wholeArticlePixelCoverage": False,
    "physicalPhoneAcceptance": False, "generalReleaseAcceptance": False,
    "publicationAttempted": False, "wholeSetAcceptance": False,
    "limits": "Dependent original-session visual confirmation, not new blind initial or fresh upstream dictionary review. Supplied operations independently hash/XML/log-verified by coordinator, not reviewer-executed. Drawing reference-touch trace/recallmiss not MLKit or successful human recall. Unseen cells/pixels and unidentified fallback face remain limits. Cumulative usage is not current-turn cost. Historical process noncompliance remains explicit.",
}
save(acceptance_path, acceptance)
record = {
    "schemaVersion": 1, "execution": 358, "batch": "059", "status": acceptance["status"],
    "startingHead": head, "startingSignature": "G", "reviewedTeachingSnapshot": teaching,
    "scope": p["execution358StartingState"]["scope"],
    "authorization": p["execution358StartingState"]["authorization"],
    "recordedAt": datetime.now().astimezone().isoformat(),
    "acceptance": str(acceptance_path.relative_to(r)), "acceptanceSha256": sha(acceptance_path),
    "nativeArtifactHashesReverified": len(index["files"]), "originalReportsReverified": freeze["originalReports"],
    "freshAndroidNamedCasesReverified": 4, "freshAndroidSkipped": 0,
    "nativeTerminalCaseStatusesReverified": [0, 0],
    "nativeRerun": False, "androidRerun": False, "teachingChanged": False,
    "reviewerProcessesSerialAndExited": True, "firstReportAndAuditArchivedBeforeSecond": True,
    "newVisualOverlaps": 0, "newVisualMultiToolResponses": 0,
    "sourcePngCount": 35, "distinctPngCount": 20, "actualModelPayloadCopiesVerified": 40,
    "coordinatorDirectImageReadsThisExecution": [
        "n1-059-kanji-curation.png", "n1-059-font-pairs.png",
        "n1-059-meaning-question.png", "n1-059-drawing-feedback.png",
    ],
    "historicalProcessNoncompliancePreserved": True,
    "validation": checks, "archivedExecutionReceipts": copied,
    "runtimeUnchanged": True, "manifestUnchanged": True,
    "publicationAttempted": False, "publishedAdditions": 85, "remainingAdditions": 1143,
    "nextAction": next_action, "limits": acceptance["limits"],
}
save(record_path, record)
batch_path = sources / "batch-059-progress.json"
batch = load(batch_path)
assert batch["status"] == "native-assertions-passed-pending-independent-visual"
batch.update(
    status=acceptance["status"], nextAction=next_action,
    nativeVisualCheckpoint="execution-358.json",
    nativeVisualAcceptance={
        "record": str(acceptance_path.relative_to(r)), "sha256": sha(acceptance_path),
        "boundedIndependentVisualAcceptance": True, "strictHistoricalProcessContractAccepted": False,
        "sourceScreenshots": 35, "distinctScreenshots": 20, "actualModelPayloadCopies": 40,
        "nativeOrAndroidRerun": False, "publicationAttempted": False,
    },
)
save(batch_path, batch)
stage = [str(x.relative_to(r)) for x in (record_path, acceptance_path, batch_path, r / "docs" / "n1-authoring-notes.md")]
for label in ("claude", "gpt"):
    stage += [str((reviews / f"batch-059-visual-{label}{suffix}").relative_to(r)) for suffix in (".md", "-execution.json")]
    stage += [str(x.relative_to(r)) for x in sorted((native / f"visual-{label}-returned").iterdir())]
stage += [row["path"] for row in copied]
save(c / "execution-358-staged-inventory.json", stage)
subprocess.run(["git", "add", "--", *stage], cwd=r, check=True)
assert set(filter(None, git("diff", "--cached", "--name-only", "-z").split("\0"))) == {x.replace("\\", "/") for x in stage}
assert not git("diff", "--cached", "--check")
print(f"Verified and staged {len(stage)} evidence files; runtime unchanged. Normal signed commit required.")
