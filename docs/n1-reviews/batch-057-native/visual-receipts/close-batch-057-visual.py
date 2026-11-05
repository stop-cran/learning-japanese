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
native = reviews / "batch-057-native"
sources = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution338.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = "4d460d10add0b9c88d6514837e2806b1d9946c3a"
teaching = "acc397033503a38aa88506fc3ad966761793db72"
record_path = sources / "execution-338.json"
acceptance_path = reviews / "batch-057-native-acceptance.json"
p = load(c / "progress.json")
assert p["checkpoint"] == 337 and p["batch"] == "057"
if len(sys.argv) > 1 and sys.argv[1] == "finish":
    assert not git("status", "--porcelain")
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == head
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", head, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json")
    record = load(record_path)
    checkpoint = {
        "execution": 338, "batch": "057", "status": record["status"],
        "savedCommit": saved, "signature": "G", "record": str(record_path.relative_to(r)),
        "recordSha256": sha(record_path), "nextAction": record["nextAction"],
        "recordedAt": datetime.now().astimezone().isoformat(),
        "publishedAdditions": 83, "remainingAdditions": 1145,
        "publicationAttempted": False, "nativeRerun": False, "androidRerun": False,
        "strictInitialProcessContractAccepted": False,
    }
    p.update(checkpoint=338, status="continue",
             stage="batch-057-bounded-native-visual-reconciled-pending-combined-main-publication",
             blocker=None, nextAction=record["nextAction"])
    p["execution338StartingState"]["status"] = "signed-bounded-native-visual-checkpoint-complete"
    p["execution338CoordinatorCheckpoint"] = checkpoint
    p["batch057NativeVisualCheckpoint"] = checkpoint.copy()
    save(c / "progress.json", p)
    print(f"Checkpoint338 persisted: signed G {saved}; continue SAME057 combined-main acceptance next.")
    sys.exit(0)

assert git("rev-parse", "HEAD") == head
assert not git("status", "--porcelain", "--", "kanji", "words", "articles", "strokes", "manifest.json")
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json")
assert git("log", "-1", "--format=%G?") == "G"
android = c.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=android)
freeze = load(c / "batch-057-visual-freeze.json")
for name, h in freeze["files"].items():
    assert sha(r / name) == h
for name, h in freeze["originalReports"].items():
    assert sha(reviews / name) == h
archival = load(sources / "execution-337.json")
for row in archival["verification"]["indexedArtifacts"]:
    assert sha(r / row["path"]) == row["sha256"]
assert sha(r / archival["priorExecutionRecord"]) == archival["priorExecutionRecordSha256"]
assert sha(r / archival["parentRecovery"]) == archival["parentRecoverySha256"]

labels = ("claude", "gpt", "claude-clarification")
processes = [load(reviews / f"batch-057-visual-{label}-execution.json") for label in labels]
assert [x["actualModels"] for x in processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"], ["claude-opus-5.5"]]
for first, second in zip(processes, processes[1:]):
    assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
assert (reviews / "batch-057-visual-claude.md").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
assert (reviews / "batch-057-visual-gpt.md").stat().st_mtime < datetime.fromisoformat(processes[2]["startedAt"]).timestamp()
configuration_correction = []
for label, process, count, images, overlaps in zip(labels, processes, (32, 32, 3), (23, 23, 2), (1, 0, 0)):
    assert process["exitCode"] == 0 and not process["unfinishedTools"]
    assert len(process["toolCalls"]) == count and process["imagePayloadsVerified"] == images
    assert len(process["observedToolOverlaps"]) == overlaps and process["expectedPngMembershipReturned"]
    assert sha(reviews / f"batch-057-visual-{label}.md") == process["reportSha256"]
    raw_path = c / f"batch-057-visual-{label}.jsonl"
    assert sha(raw_path) == process["rawExecutionSha256"]
    for call in process["toolCalls"]:
        assert call["name"] == "view" and call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
            assert image["sourceDimensions"] == [1080, 2400]
            assert image["returnedDimensions"] == [900, 2000]
            assert not image["exactFileBytesReturnedToModel"]
        else:
            assert call["exactRequestedTextContainedInResult"]
    events = [json.loads(s) for s in raw_path.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
    configurations = [e["data"] for e in events if e["type"] == "session.info"
                      and e["data"].get("infoType") == "configuration"]
    assert len(configurations) == 1 and "Disabled tools:" in configurations[0]["message"]
    assert "powershell" in configurations[0]["message"] and "task" in configurations[0]["message"]
    actual_models = sorted({e["data"]["model"] for e in events if e["type"] == "session.tools_updated"})
    assert actual_models == process["actualModels"]
    configuration_correction.append({
        "executionRecord": f"batch-057-visual-{label}-execution.json",
        "executionRecordSha256": sha(reviews / f"batch-057-visual-{label}-execution.json"),
        "actualConfigurationEvidence": configurations, "actualToolModel": actual_models,
        "actualTask": process["toolCalls"][0]["arguments"]["path"],
        "actualTaskSha256": sha(Path(process["toolCalls"][0]["arguments"]["path"])),
    })
correction_path = reviews / "batch-057-visual-configuration-evidence.json"
assert not correction_path.exists()
save(correction_path, {
    "schemaVersion": 1, "execution": 338,
    "kind": "Additive archive-helper event-selector correction; original execution records unchanged.",
    "detail": "Helper selected system.message, but actual configuration event type is session.info. Empty original configurationEvidence arrays were archive filtering omissions, not absence of CLI allowlist enforcement. Actual raw events below; all actual executed tools were view. No rerun or claim of retroactive process compliance.",
    "records": configuration_correction,
})
pngs = list((native / "attempt-1").glob("*.png"))
assert len(pngs) == 43 and len({sha(x) for x in pngs}) == 23
raw = (native / "attempt-1" / "instrumentation.txt").read_text(encoding="utf-8")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw, re.M) == ["1", "0", "1", "0"]
assert "Time: 99.132" in raw and "OK (2 tests)" in raw
route = load(native / "attempt-1" / "n1-057-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1 and not route["phoneEvidence"]
assert [route[x] for x in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1069, 5028, 89, 0, 1]
assert route["contentVersion"] == "47f11f7f539a1d55"
assert route["fullOnyomi"] == ["キ"] and route["fullKunyomi"] == ["くわだ.てる", "たくら.む"]
assert route["quizOnKeys"] == ["き"] and route["quizKunKeys"] == ["くわだてる"]
assert all(route[x] for x in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                            "bothCuratedQuestionsAndPersistedGrades", "drawingTraceThenRecall",
                            "drawingGradeRecordedOnNext", "offline"))
a = load(sources / "execution-334.json")
assert sha(Path(a["log"])) == a["logSha256"]
for row in a["tests"]:
    for path in (Path(row["sourcePath"]), r / row["artifactPath"]):
        assert sha(path) == row["sha256"]
        suite = ET.parse(path).getroot()
        assert int(suite.attrib["tests"]) == row["tests"]
        assert all(int(suite.attrib[k]) == 0 for k in ("failures", "errors", "skipped"))
        assert suite.attrib["timestamp"] == row["timestamp"]
        assert sorted(x.attrib["name"] for x in suite.findall("testcase")) == sorted(row["caseNames"])
    assert sha(android / row["testImplementation"]) == row["testImplementationSha256"]
assert sha(c / "batch-049-host-integration-heap.init.gradle") == a["hostInitSha256"]

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
    "batch-057-visual-task.txt", "batch-057-visual-freeze.json",
    "batch-057-visual-claude-clarification-task.txt", "run-batch-057-visual.ps1",
    "run-batch-057-visual-claude-clarification.ps1", "archive-batch-057-visual.py",
    "close-batch-057-visual.py", "copilot-help-execution-338.txt", "copilot-model-settings-execution-338.txt",
]
for label in labels:
    names += [f"batch-057-visual-{label}-{suffix}" for suffix in ("process.json", "usage.json", "stderr.txt")]
copied = []
for name in names:
    source, dest = c / name, receipts / name
    shutil.copyfile(source, dest)
    assert sha(source) == sha(dest)
    copied.append({"path": str(dest.relative_to(r)), "sha256": sha(dest)})
next_action = (
    "SAME057 bounded native/ORIGINAL two-family visual confirmation reconciled; signed LOCAL evidence checkpoint only, "
    "NOT runtime publication or strict initial-process acceptance. No accepted334Android3+1/native336/initialreview/"
    "visual rerun absent new concern. OriginalClaude9afffb68 actualclaude-opus-5.5 thenGPT94ee22aa actualgpt-6.1-sol "
    "processes exited0SERIAL:32calls/23distinctPNGpayloads EACH; ClaudeONEinternaltwoimageoverlap retained, GPTzero; "
    "Claude3callserial supplement reread overlap pair and corrected static-backlink inference. Original52internal "
    "overlaps/noncompliance and onevisualoverlap NOTerased; strict original/visual process contract NOTclaimed. "
    "Allcomplete reports/audits/actualreturnedpayloads preserved. No actionable teaching defect or teaching edit. "
    "43sourcePNGs23distinct/20hash-equivalentcopies;1080x2400sources returned900x2000, bothbytesets preserved. "
    "Fourfontrows企全危休 distinguishable/人止業企業企てるreadable; Textbookfinalるwrap visible, actualfallbackfaceunknown. "
    "Complementaryreadingtableviews have croppedcells; hiddencontent/everycell/fullarticlerendering NOTcertified. "
    "Native336actual2case0/no skips99.132s/fullContentSyncONCE1069kanji5028words89N1/47f11f7f539a1d55/"
    "problems0/epoch1/LiteANDfullorderedキ/くわだ.てる,たくら.む/curatedきくわだてる/twopairsfourdirections/"
    "SystemBack/offline/meaningfeedbackBackwithoutpersist/bothcuratedGood/sixreference-touchstrokes/"
    "ungradedtrace/recallmiss/persistedDrawAgain. NOTMLKit/correcthumanrecall/phone. Original336denial and "
    "parentEXACTcleanupverificationexit0 unchanged. NEXT bounded checkpoint latestorigin/main fetch/normal "
    "nonrewritingmerge, surgicalconflicts/reviewsubstantiveteaching; ALLcombined frozen-source/baseline/"
    "exactmembership/originalguards/readings/links/strokes/fonts/currentPython/vocabulary/validator/"
    "freshmanifest/18000entries42MiBcompressed80MiBinflated56MiBretainedbudgets/normalsigning/ownerfastforward/"
    "exactremoteSHA/terminalgreenCI/EVERYimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 "
    "BEFOREdelivery or058. Actualpermissiondenial/signingwait preserveexactcommand-error/report/yield, "
    "no retry/workaround. Preserve FULLlivehistory, nosecondrunner. Published83/1228,1145remaining latest056"
    "e8dc74eba6a783552f069593c6fc1d3849986293;Androidf9b59a2+required;physicalphone/generalrelease/whole-set"
    "outstanding;overallincomplete."
)
limits = (
    "Dependent bounded visuals, not new blind initials/fresh194family or upstream dictionary/native-speaker/"
    "model benchmark/reviewer-run tests. Original Claude52internaloverlapstarts and false serial self-claim "
    "remain historical noncompliance; current visualONEoverlap is a real further deviation. Claude honestly "
    "disclosed it and3callzerooverlap supplement reread the two affected images, correcting static navigation "
    "inference; no retroactive strict contract acceptance or claim that all full reviews were serial. "
    "Reviewer PROCESSES serial,32/32/3calls and23/23/2actualPNGpayloads. Allrequestedrangesreturned; "
    "byte consistency is not comprehension. 43sourcePNGs23distincthashes/20equivalentcopies; "
    "1080x2400to900x2000 transport. Coordinator directly viewed9unique PNGs this execution only; "
    "other pixel claims retain reviewer provenance. Horizontal table cropping/hiddencontent/everycell/"
    "wholearticle rendering UNVERIFIED, not blanket acceptance. Actualfallbackfaceunidentified. "
    "Actualmeaningchoices tiger/riceplant/plan;undertake/mosquito, not authored危休全. Meaningfeedback "
    "notpersistedbeforeBack; bothcuratedGood andDrawAgainNext actualfixtureassertions. Reference-touch/"
    "ungradedtrace/modelunavailablegeometry-only/recallmiss NOTMLKit/correcthumanrecall/negativegeometry/"
    "reverseorder. Original336denial/parentrecovery retained; no native/Android rerun. Originaloptional "
    "groups remainunadopted; mixed practice/grading wording optional existing app observation only. "
    "Freshvalidator/unchangedmanifest/originalbudgets repeated to capture complete output; fullPython/"
    "vocabulary/source/baseline integration checks NOTfreshlyrunhere, required next onactualcombinedmain. "
    "Initial unsupported copilot config help model command returned unknown-key error (no setting modified); "
    "supported copilot help config then supplied actual catalog. Archive config event-selector omission "
    "preserved and corrected additively, not reviewer/tool failure. No runtime/font/heap/archiveguard "
    "changes/publication/058/secondrunner. Compatiblef9b59a2+required; physicalphone/generalrelease/whole-setoutstanding."
)
acceptance = {
    "schemaVersion": 1, "execution": 338, "batch": "057",
    "status": "bounded-native-original-visual-reconciled-pending-combined-main-publication",
    "frozenSnapshot": head, "reviewedTeachingSnapshot": teaching, "teachingDiff": "empty",
    "visualReports": [f"batch-057-visual-{label}.md" for label in labels],
    "visualProcessRecords": [f"batch-057-visual-{label}-execution.json" for label in labels],
    "models": ["claude-opus-5.5", "gpt-6.1-sol"], "reviewerProcessesSerial": True,
    "observedInternalOverlaps": [1, 0, 0], "actualCalls": [32, 32, 3],
    "strictInitialProcessContractAccepted": False, "strictVisualProcessContractAccepted": False,
    "reconciliation": [
        {"claim": "No new actionable teaching defect in bounded visible scope", "disposition": "resolved", "teachingChange": False, "allArticleFacets": "CLEAN only within retained textual and bounded viewport scope"},
        {"claim": "057-F1 practical ambiguity", "disposition": "resolved", "detail": "Modern one-ichidan-verb sentence unchanged; original historical-versus-synchronic disagreement remains explicit. No new etymology."},
        {"claim": "One Claude visual two-image overlap after original52overlap history", "disposition": "partially resolved", "detail": "Both affected PNGs reread in3callzerooverlap original-session supplement. Original reports and both noncompliance histories immutable; process acceptance is not established by agreement."},
        {"claim": "Static backlink screenshot establishes navigation sequence", "disposition": "withdrawn", "detail": "Claude original-session supplement limits pixels to displayed destination. Sequence and persistence rely separately on actual fixture/asserted native execution."},
        {"claim": "Full-article/every-cell rendering acceptance", "disposition": "unresolved", "deliveredPositiveClaim": False, "detail": "UNVERIFIED outside actual inspected viewports; complementary views support bounded reading-table distinctions, not hidden-content certification."},
        {"claim": "Original optional groups and mixed practice/grading app wording", "disposition": "optional", "adopted": False, "detail": "No new exclusion, example, historical expansion or out-of-scope app change. Existing practice-only and model-unavailable messages explicitly limit drawing conclusions."},
    ],
    "nativeResult": route, "terminalNativeCase0": 2, "nativeDurationSeconds": 99.132,
    "sourcePngs": 43, "distinctSourcePngHashes": 23, "hashEquivalentCopies": 20,
    "modelVisibleImagesPerReview": [23, 23, 2], "coordinatorNewDistinctDirectImageReads": 9,
    "freshNativeRun": False, "freshAndroidRun": False, "verified337IndexedNativeArtifacts": 52,
    "acceptedAndroid": "docs\\n1-sources\\execution-334.json",
    "originalNative": "docs\\n1-sources\\execution-336.json",
    "archivalParentRecovery": "docs\\n1-sources\\execution-337.json",
    "originalInitialAndConfirmationReportHashesPreserved": True,
    "configurationEvidenceCorrection": str(correction_path.relative_to(r)),
    "checks": checks, "receiptFiles": copied,
    "publicationAttempted": False, "publishedAdditions": 83, "remainingAdditions": 1145,
    "limits": limits, "nextAction": next_action,
}
assert not acceptance_path.exists() and not record_path.exists()
save(acceptance_path, acceptance)
record = {
    "schemaVersion": 1, "execution": 338, "batch": "057", "status": acceptance["status"],
    "recordedAt": datetime.now().astimezone().isoformat(), "startingHead": head,
    "scope": p["execution338StartingState"]["scope"],
    "acceptanceRecord": str(acceptance_path.relative_to(r)), "acceptanceRecordSha256": sha(acceptance_path),
    "visualProcesses": [
        {"model": x["actualModels"][0], "sessionId": x["sessionId"], "startedAt": x["startedAt"],
         "completedAt": x["completedAt"], "exitCode": x["exitCode"], "calls": len(x["toolCalls"]),
         "internalOverlaps": len(x["observedToolOverlaps"]), "pngPayloads": x["imagePayloadsVerified"],
         "reportSha256": x["reportSha256"]} for x in processes
    ],
    "checks": checks, "nativeRerun": False, "androidRerun": False, "runtimeUnchanged": True,
    "strictInitialProcessContractAccepted": False, "strictVisualProcessContractAccepted": False,
    "publicationAttempted": False, "publishedAdditions": 83, "remainingAdditions": 1145,
    "limits": limits, "nextAction": next_action,
}
save(record_path, record)
p["execution338StartingState"]["status"] = "bounded-visual-reconciliation-ready-for-normal-signing"
p["execution338VisualCheckpoint"] = {
    "record": str(record_path.relative_to(r)), "recordSha256": sha(record_path),
    "status": "verified-ready-for-normal-signing", "nextAction": next_action,
}
save(c / "progress.json", p)
print("SAME057 bounded visuals reconciled; exact reports/audits/payloads preserved; ready for normally signed local checkpoint.")
