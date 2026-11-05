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
reviews = r / "docs/n1-reviews"
native = reviews / "batch-058-native"
sources = r / "docs/n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
head = "9468bac2169909be53ef87bda5cffdbb79646040"
teaching = "58b53fd31b6d55baba32c049fba62ac739feb004"
record_path = sources / "execution-348.json"
acceptance_path = reviews / "batch-058-native-acceptance.json"


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution348.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


p = load(c / "progress.json")
assert p["checkpoint"] == 347 and p["batch"] == "058"
if len(sys.argv) > 1 and sys.argv[1] == "finish":
    assert not git("status", "--porcelain")
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == head
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", head, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json")
    record = load(record_path)
    checkpoint = {
        "execution": 348, "batch": "058", "status": record["status"],
        "savedCommit": saved, "signature": "G", "record": str(record_path.relative_to(r)),
        "recordSha256": sha(record_path), "nextAction": record["nextAction"],
        "recordedAt": datetime.now().astimezone().isoformat(),
        "publishedAdditions": 84, "remainingAdditions": 1144,
        "publicationAttempted": False, "nativeRerun": False, "androidRerun": False,
        "strictInitialProcessContractAccepted": False, "strictVisualProcessContractAccepted": True,
    }
    p.update(checkpoint=348, status="continue",
             stage="batch-058-bounded-native-visual-reconciled-pending-combined-main-publication",
             blocker=None, nextAction=record["nextAction"])
    p["execution348StartingState"]["status"] = "signed-bounded-native-visual-checkpoint-complete"
    p["execution348CoordinatorCheckpoint"] = checkpoint
    p["batch058NativeVisualCheckpoint"] = checkpoint.copy()
    save(c / "progress.json", p)
    print(f"Checkpoint348 persisted: signed G {saved}; continue SAME058 combined-main acceptance next.")
    sys.exit(0)

assert git("rev-parse", "HEAD") == head and git("log", "-1", "--format=%G?") == "G"
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json")
assert not git("status", "--porcelain", "--", "kanji", "words", "articles", "strokes", "manifest.json")
android = c.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=android)
freeze = load(c / "batch-058-visual-freeze.json")
for name, h in freeze["files"].items():
    assert sha(r / name) == h
for name, h in freeze["originalReports"].items():
    assert sha(reviews / name) == h
index = r / freeze["nativeArtifactIndex"]
assert sha(index) == freeze["nativeArtifactIndexSha256"]
for row in load(index)["files"]:
    assert sha(r / row["path"]) == row["sha256"]
pngs = list((native / "attempt-1").glob("*.png"))
assert len(pngs) == 43 and len({sha(x) for x in pngs}) == 25
processes = [load(reviews / f"batch-058-visual-{label}-execution.json") for label in ("claude", "gpt")]
assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
assert (reviews / "batch-058-visual-claude.md").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
assert (reviews / "batch-058-visual-claude-execution.json").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
for label, process, model in zip(("claude", "gpt"), processes, ("claude-opus-5.5", "gpt-6.1-sol")):
    assert process["actualModels"] == [model] == [process["usage"]["currentModel"]]
    assert process["exitCode"] == 0 and not process["unfinishedTools"] and not process["observedToolOverlaps"]
    assert len(process["toolCalls"]) == 36 and process["imagePayloadsVerified"] == 25
    assert process["expectedPngMembershipReturned"]
    assert process["requestsPerAssistantResponse"] == [1] * 36 + [0]
    assert sha(reviews / f"batch-058-visual-{label}.md") == process["reportSha256"]
    assert sha(c / f"batch-058-visual-{label}.jsonl") == process["rawExecutionSha256"]
    assert len(process["configurationEvidence"]) == 1
    disabled = process["configurationEvidence"][0]["message"]
    assert "Disabled tools:" in disabled and "powershell" in disabled and "task" in disabled
    assert process["toolModelEvidence"] == [{"model": model}]
    assert process["terminalResults"] == [{"sessionId": process["sessionId"], "exitCode": 0}]
    for call in process["toolCalls"]:
        assert call["name"] == "view" and call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
            assert image["sourceDimensions"] == [1080, 2400] and image["returnedDimensions"] == [900, 2000]
        else:
            assert call["exactRequestedTextContainedInResult"]
    paths = {Path(x["arguments"]["path"]) for x in process["toolCalls"]}
    assert {r / f for f in list(freeze["files"])[:5]}.issubset(paths)
    assert reviews / f"batch-058-initial-{label}.md" in paths
    assert reviews / f"batch-058-confirmation-{label}.md" in paths
    fixture_calls = [x["arguments"]["view_range"] for x in process["toolCalls"]
                     if x["arguments"]["path"].endswith("N1Batch058NativeTest.kt")]
    assert fixture_calls == [[57, 139], [150, 242], [249, 432]]
raw = (native / "attempt-1/instrumentation.txt").read_text(encoding="utf-8")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw, re.M) == ["1", "0", "1", "0"]
assert "Time: 102.361" in raw and "OK (2 tests)" in raw
route = load(native / "attempt-1/n1-058-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1 and not route["phoneEvidence"]
assert [route[x] for x in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1070, 5029, 90, 0, 1]
assert route["contentVersion"] == "5e8f3e7e39ea187a"
assert route["fullOnyomi"] == ["キュウ"] and route["fullKunyomi"] == ["おか"]
assert route["quizOnKeys"] == ["きゅう"] and route["quizKunKeys"] == ["おか"]
assert all(route[x] for x in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                            "bothCuratedQuestionsAndPersistedGrades", "drawingTraceThenRecall",
                            "drawingGradeRecordedOnNext", "offline"))
a = load(sources / "execution-345.json")
for row in a["archivedArtifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
for row in a["recovery"]["tests"]:
    archived = reviews / "batch-058-android" / Path(row["artifactPath"]).name
    assert sha(archived) == row["sha256"]
    suite = ET.parse(archived).getroot()
    assert int(suite.attrib["tests"]) == row["tests"]
    assert all(int(suite.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
    assert sorted(x.attrib["name"] for x in suite.findall("testcase")) == sorted(row["caseNames"])
for row in a["provenance"]:
    assert sha(Path(row["path"])) == row["sha256"]
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
names = ["batch-058-visual-task.txt", "batch-058-visual-freeze.json", "run-batch-058-visual.ps1",
         "prepare-batch-058-visual.py", "archive-batch-058-visual.py", "close-batch-058-visual.py",
         "execution-348-copilot-help.txt", "execution-348-model-catalog.txt"]
for label in ("claude", "gpt"):
    names += [f"batch-058-visual-{label}-{suffix}" for suffix in ("process.json", "usage.json", "stderr.txt")]
copied = []
for name in names:
    source, dest = c / name, receipts / name
    text = source.read_text(encoding="utf-8-sig").replace("\r\n", "\n").rstrip()
    dest.write_text(text + ("\n" if text else ""), encoding="utf-8")
    copied.append({"path": str(dest.relative_to(r)), "sha256": sha(dest), "sourceSha256": sha(source),
                   "normalization": "UTF-8 LF, trailing blank lines removed for Git; original control bytes preserved."})
next_action = (
    "SAME058 bounded native/ORIGINAL two-family visual confirmation reconciled; signed LOCAL evidence checkpoint348 only, "
    "NOT runtime publication or retroactive strict initial-process acceptance. No accepted345Android3+1/native347/initialreview/"
    "visual rerun absent new concern. OriginalClaude527ad6ad actualclaude-opus-5.5 THEN originalGPT843ee44f actualgpt-6.1-sol "
    "processes exited0SERIAL; first complete report+audit archived before secondlaunch. EACH36viewcalls/25distinctactualPNGpayloads/"
    "exactlyONEcallperresponse/ZEROoverlaps/allassignedtext+rangesreturned. OriginalClaude3initialoverlaps/tworesponses remain "
    "historicalNONCOMPLIANCE; boundedremediationNOTretroactiveacceptance. Reports/audits/source+returnedimages preserved. "
    "No actionable teaching defect/teachingedit. 43sourcePNGs25distinct/18hash-equivalentcopies;1080x2400sources returned900x2000. "
    "Coordinator8directimages thisexecution; otherpixelclaims reviewerprovenance. Fourfontrows丘兵近共 distinct and一砂山/丘/砂丘 "
    "readable/noboxes;fallbackfaceUNIDENTIFIED. Horizontalreadingtablecropping/hiddencontent/everycell/wholearticlerendering "
    "UNVERIFIED, not blanketapproval. Meaningactualchoices chrysanthemum/hillknoll/pigpork/turtletortoise,notauthored兵近共; "
    "BackbeforemeaningNextnopersist; BOTHcuratedGoodpersisted. Fivegeneratedreferencetouchstrokes/ungradedtrace/modelunavailable/"
    "geometry-only/recallmiss/persistedDrawAgain;NOTMLKit/correcthumanrecall. Accepted347two terminalcase0/102.361s/"
    "fullContentSyncONCE1070kanji5029words90N1/5e8f3e7e39ea187a/problems0/epoch1/full+Liteキュウおか/"
    "curatedきゅうおか/THREEpairsSIXdirections/offline retained. Original344denial/parentrecovery and049HOST512MiBOOM/"
    "qualifiedhost-only1GiBinit preserved. NEXTboundedcheckpoint latestorigin/main fetch/normalnonrewritingmerge, "
    "surgicalconflicts/reviewsubstantiveteaching; ALLcombined frozen-source/baseline/exactmembership/readings/links/"
    "strokes/fonts/currentPython/vocabulary/validator/freshmanifest/18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/"
    "normalsigning/ownerfastforward/exactremoteSHA/terminalgreenCI/EVERYimmutablepublicZIPruntimehash/terminalreceipts/"
    "ownerissue60 BEFOREdelivery or059. Actualpermissiondenial/signingwait: preserveexactcommand-error/report/yield, "
    "no retry/workaround. Preserve FULLlivehistory, nosecondrunner orconcurrentheavywork. Published84/1228,1144remain/"
    "latest057c064f0c749bdc93bc1f86dbd01cec19212991bd7;compatibleAndroidf9b59a2+required;physicalphone/generalrelease/"
    "whole-setoutstanding;overallprojectINCOMPLETE."
)
limits = (
    "Dependent bounded visuals in ORIGINAL sessions, not new blind initials/fresh68family/upstream dictionary/native-speaker/"
    "model benchmark/reviewer-run tests. InitialClaude3overlapstarts/tworesponses retained as historical noncompliance; "
    "strictinitialprocessacceptance false. Current36/36calls each one per response/zero overlaps, serial terminal0 processes, "
    "25/25distinct actual PNG payloads; bytes/ranges do not certify comprehension. 43sourcePNGs25distinct/18copies, "
    "1080x2400sources returned900x2000. Coordinator directly viewed8PNGs thisexecution only. Horizontal table leftlabels "
    "cropped in shiftedview; unseen cells/wholearticles UNVERIFIED. Different typeface alone no defect; fallbackface notidentified. "
    "Actualmeaningfallbacklabels differ from authored lookalikes; meaningfeedbackBack notpersisted. BothcuratedGood and "
    "DrawAgainNext persistent fixtureassertions; generatedreference-touch/ungradedtrace/modelunavailablegeometry-only/recallmiss "
    "NOTMLKit/correcthumanrecall/negativegeometry/reverseorder. OriginalClaudeoptionals remain optional/unadopted; app "
    "practice-versus-grading wording observation optional, no established new content defect. No teaching/app/font/heap/"
    "archiveguard changes or Android/native rerun/publication/059. Freshvalidator/unchangedmanifest/originalbudgets only; "
    "fullPython/vocabulary/source/baseline/currentmain gates next. Original344permissiondenial/parentrecovery and049host "
    "qualification unchanged. CompatibleAndroidf9b59a2+required;physicalphone/generalrelease/whole-setoutstanding."
)
acceptance = {
    "schemaVersion": 1, "execution": 348, "batch": "058",
    "status": "bounded-native-original-visual-reconciled-pending-combined-main-publication",
    "snapshot": head, "reviewedTeachingSnapshot": teaching,
    "nativeAssertionsPassed": True, "boundedIndependentVisualConfirmation": True,
    "strictInitialProcessContractAccepted": False, "strictVisualProcessContractAccepted": True,
    "reviewProcessesSerial": True, "internalVisualToolOverlaps": [0, 0],
    "sourcePngCount": 43, "distinctPngCount": 25, "equivalentCopies": 18,
    "visualReports": [{"report": f"batch-058-visual-{label}.md", "reportSha256": process["reportSha256"],
                      "audit": f"batch-058-visual-{label}-execution.json",
                      "auditSha256": sha(reviews / f"batch-058-visual-{label}-execution.json"),
                      "model": process["actualModels"][0], "sessionId": process["sessionId"]}
                     for label, process in zip(("claude", "gpt"), processes)],
    "findings": [], "optional": load(reviews / "batch-058-reconciliation.json")["optional"],
    "drawingWordingObservation": {"status": "optional", "source": "visual-claude",
                                 "disposition": "Existing app wording mixes practice-only and shape-assessment language; not an established batch teaching defect. No app change authorized here."},
    "coordinatorDirectImageReads": ["font-pairs", "meaning-question", "drawing-feedback", "kanji-curation",
                                    "kanji-landform-boundaries", "dune-components-readings", "hill-house-example", "system-back-sand"],
    "nativeRecord": "docs/n1-sources/execution-347.json", "nativeRecordSha256": sha(sources / "execution-347.json"),
    "nativeArtifactIndexSha256": sha(index),
    "acceptedAndroidRecord": "docs/n1-sources/execution-345.json",
    "acceptedAndroidRecordSha256": sha(sources / "execution-345.json"),
    "allFiveArticlesThreeFacetsCleanWithinReviewedScope": True,
    "unseenTableCellsAndWholeArticleRendering": "UNVERIFIED",
    "fallbackFace": "UNVERIFIED", "phoneAcceptance": "outstanding",
    "nativeRerun": False, "androidRerun": False, "runtimePublished": False,
    "checks": checks, "archivedExecutionReceipts": copied, "limits": limits, "nextAction": next_action,
}
assert not acceptance_path.exists() and not record_path.exists()
save(acceptance_path, acceptance)
record = {
    "schemaVersion": 1, "execution": 348, "batch": "058", "status": acceptance["status"],
    "recordedAt": datetime.now().astimezone().isoformat(), "startingHead": head,
    "scope": p["execution348StartingState"]["scope"],
    "acceptanceRecord": str(acceptance_path.relative_to(r)), "acceptanceRecordSha256": sha(acceptance_path),
    "visualProcesses": [{"model": x["actualModels"][0], "sessionId": x["sessionId"],
                         "startedAt": x["startedAt"], "completedAt": x["completedAt"], "exitCode": x["exitCode"],
                         "calls": len(x["toolCalls"]), "internalOverlaps": len(x["observedToolOverlaps"]),
                         "pngPayloads": x["imagePayloadsVerified"], "reportSha256": x["reportSha256"]} for x in processes],
    "checks": checks, "nativeRerun": False, "androidRerun": False, "runtimeUnchanged": True,
    "strictInitialProcessContractAccepted": False, "strictVisualProcessContractAccepted": True,
    "publicationAttempted": False, "publishedAdditions": 84, "remainingAdditions": 1144,
    "limits": limits, "nextAction": next_action,
}
save(record_path, record)
batch_path = sources / "batch-058-progress.json"
batch = load(batch_path)
batch.update(status=acceptance["status"], nextAction=next_action,
             nativeVisualCheckpoint="execution-348.json",
             nativeAcceptance="docs/n1-reviews/batch-058-native-acceptance.json",
             nativeVisualLimits=limits)
save(batch_path, batch)
print("Closed bounded visual evidence: both36calls/25PNGs/zerooverlaps, serial exits; current validator/manifest/budgets passed.")
