import hashlib
import json
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
reviews = r / "docs" / "n1-reviews"
native = reviews / "batch-055-native"
sources = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = "c4fc279c44541b3d99ddaa56ca5d1ce0452e9026"
assert git("rev-parse", "HEAD") == head
assert not git("status", "--porcelain", "--", "kanji", "words", "articles", "strokes", "manifest.json")
assert not git("diff", "a532c4d436726e6eeb46ff78cc3dc1a039d6f19e", "--", "kanji", "words", "articles", "strokes", "manifest.json")
android = c.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=android)
processes = [load(reviews / f"batch-055-visual-{label}-execution.json") for label in ("claude", "gpt")]
assert [p["actualModels"] for p in processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
assert (reviews / "batch-055-visual-claude.md").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
for label, p in zip(("claude", "gpt"), processes):
    assert p["exitCode"] == 0 and not p["observedToolOverlaps"] and not p["unfinishedTools"]
    assert len(p["toolCalls"]) == 27 and p["imagePayloadsVerified"] == 20
    assert p["expectedPngMembershipReturned"]
    assert sha(reviews / f"batch-055-visual-{label}.md") == p["reportSha256"]
    assert sha(c / f"batch-055-visual-{label}.jsonl") == p["rawExecutionSha256"]
    for call in p["toolCalls"]:
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
index = load(native / "artifact-index.json")
indexed = []
for section in ("sourceArtifacts", "coordinatorReturnedImages"):
    for row in index[section]:
        assert sha(r / row["path"]) == row["sha256"]
        indexed.append(row["path"])
assert len(index["coordinatorReturnedImages"]) == 20
pngs = list((native / "attempt-1").glob("*.png"))
assert len(pngs) == 37 and len({sha(p) for p in pngs}) == 20
raw_native = (native / "attempt-1" / "instrumentation.txt").read_text(encoding="utf-8")
assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0$", raw_native, re.M)) == 2
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw_native, re.M) == ["1", "0", "1", "0"]
assert "Time: 85.809" in raw_native and "OK (2 tests)" in raw_native
route = load(native / "attempt-1" / "n1-055-article-route.json")
assert all(route[k] for k in (
    "passed", "reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
    "curatedOnQuestionAndPersistedGrade", "drawingTraceThenRecall", "drawingGradeRecordedOnNext", "offline",
))
assert not route["phoneEvidence"] and route["archiveRequests"] == 1
assert [route[k] for k in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1067, 5025, 87, 0, 1]
assert route["contentVersion"] == "66fa8fda924b856d"
assert route["fullOnyomi"] == ["ジョウ", "ショウ"] and route["fullKunyomi"] == ["すく.う", "たす.ける"]
assert route["quizOnKeys"] == ["じょう"] and route["quizKunKeys"] == []
rasters = load(native / "attempt-1" / "n1-055-font-raster.json")["rows"]
assert len(rasters) == 16 and all(row["hasGlyph"] for row in rasters)
for char in "丞蒸乗水":
    rows = [row for row in rasters if row["character"] == char]
    assert len(rows) == 4 and len({row["nativePaintRasterSha256"] for row in rows}) == 4
initial = load(reviews / "batch-055-reconciliation.json")
for label, p in zip(("claude", "gpt"), initial["reviewProcesses"]):
    assert sha(reviews / f"batch-055-initial-{label}.md") == p["reportSha256"]
a = load(sources / "execution-310.json")
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
    command = ["python", "-B", *args]
    result = subprocess.run(command, cwd=r, text=True, encoding="utf-8", capture_output=True)
    check = {"command": command, "exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}
    checks.append(check)
    assert result.returncode == 0, check
assert not git("diff", "--", "manifest.json")
receipts = native / "receipts"
receipts.mkdir()
copied = []
names = [
    "batch-055-visual-task.txt", "run-batch-055-visual.ps1", "archive-batch-055-visual.py",
    "close-batch-055-visual.py", "start-execution-314.py",
    "copilot-help-execution-314.txt", "copilot-config-execution-314.txt",
]
for label in ("claude", "gpt"):
    names += [f"batch-055-visual-{label}-{suffix}" for suffix in ("process.json", "usage.json", "stderr.txt")]
for name in names:
    source, dest = c / name, receipts / name
    shutil.copyfile(source, dest)
    assert sha(source) == sha(dest)
    copied.append({"path": str(dest.relative_to(r)), "sha256": sha(dest)})
next_action = (
    "SAME055 native/visual evidence CLOSED; signed LOCAL evidence checkpoint only, NOT publication. "
    "Do not repeat accepted310Android3+1/native312attempt1/compiled311fixture/two ORIGINAL visual confirmations/"
    "blind initials absent a new concern. OriginalClaude4617b82e thenGPT6aba3514 actualclaude-opus-5.5/gpt-6.1-sol "
    "exited serially:27/27serialviewcalls,0/0overlaps-failures-truncations,20distinctPNGpayloads EACH; "
    "1080x2400sources returned900x2000, bothbytesets preserved. Both allfacetsCLEAN for丞/丞相/no teachingfix. "
    "FourpriorClaudeoptional suggestionsnotadopted; horizontal-table clippedReadingcolumn optional app-only. "
    "Actualmeaningfallback yuzucitrus/carp/monme3.75g NOTauthored蒸乗水; one defensible answer. "
    "Curatedonジョウジュウホウオウ/correctジョウ/persistedGood; fullfeedbacklookup NOTpracticekeys. "
    "Native312two terminalcase0/no skips85.809s/fullproductionContentSyncONCE1067kanji5025words87N1/"
    "66fa8fda924b856d/problems0/epoch1/fullorderedジョウショウ/すく.うたす.ける LiteANDFull/"
    "on[ジョウ]kun[]/normalizedじょう. Sixgeneratedreference-touchstrokes/ungradedtrace/modelunavailablegeometry-only/"
    "recallmiss/persistedDrawAgain/one supportreciprocalpairtwodirections/SystemBack/offline/"
    "16Paintprobes/fourstyles丞蒸乗水readable-distinguishable/actualfallbackfaceunknown. "
    "Drawing NOTMLKitrecognition/humansuccessfulrecall/negativegeometry/reverseorder/phone. "
    "37sourcePNGs20distinct17hash-equivalentcopies/tableclipping/hiddencontentlimits retained. "
    "OriginalClaude42calls/TWOinternaloverlaps andGPT44calls/zero/26resources each preserved. "
    "Olderwholewordしょうじょうconstituentallocation UNVERIFIEDandOMITTED; allrawreadings/oneじょうしょうsupport/"
    "threedirectguards/noinferredwordlevel/sixstrokes一1grade9 retained. Original312denial retained; parent EXACT"
    "compound shell1 due stoppedPIDsabsent, notpermission/nativefailure/exit0; separatecleanworktrees/ownedPIDsabsentverified. "
    "Owned312helperstopped/exacttempsabsent/unowned5556untouched/Androidclean; native192m576m unchanged/"
    "requested2048auto2560MB/MemTotal2532900kB. Original049HOST512MiBOOM/existing1GiB :core HOSTTest-only "
    "qualification NOTguestauthorization. NEXT bounded checkpoint fresh latestorigin/main fetch/normalnonrewritingmerge, "
    "resolve surgically/independentlyreview substantive teachingconflicts; ALLcombined frozen-source/baseline/"
    "membership/exactoriginalguards/readings/links/strokefonts/currentPython/vocabulary/validator/"
    "freshmanifest/original18000entry42MiBcompressed80MiBinflated56MiBretainedbudgets. "
    "Normalsigning/ownerfastforward/publicSHA/actualterminalgreenCI/EVERYimmutablepublicZIPruntimehash/"
    "terminalreceipts/ownerissue60 BEFORE counting055delivery or056. Actualpermissiondenial/signingwait "
    "preserveexactcommand-error/report/yield,no retry/workaround. No secondrunner; preserve FULLlivehistory. "
    "Published81/1228,1147remaining;Androidf9b59a2+ required;physicalphone/generalrelease/whole-set outstanding."
)
limits = (
    "Bounded native/Android re-verification and two ORIGINAL dependent visual confirmations only, not current-main/"
    "publication/physicalphone/generalrelease/whole-set acceptance. No teaching change/repeatedblindinitial/"
    "freshsource/native-speaker/modelbenchmark. Bothvisualfollowups27serialviewcalls/0overlap-failure-truncation/"
    "20actualPNGpayloads each;1080x2400source resized900x2000, bytes/hashes separate. "
    "Original31220directreads/17hash-equivalentcopies not extra independentreads; current coordinator directly "
    "inspected fontpairs/drawingfeedback/kanjicuration only, otherpixels retain312andbothreviewer provenance. "
    "Tableleftlabels orrightqualifications clipped; たす.ける can appear as す.ける at shiftedoffset, "
    "NOTeverycell/fullarticle/allcolumns certification. Sideways-scrollinstruction available; no teachingfix "
    "or unsupported appredesign. Wordexample edge/wrapping retained. Actualmeaningchoices yuzucitrus/carp/"
    "monme NOTauthored蒸乗水; oneanswer defensible, not allpools/largerquiz certification. Meaningfeedback "
    "notpersistedbeforeBack; readingGood/DrawAgainNext persistence are actualfixture assertions, not reviewer-executedtests. "
    "Synthetic source/duequeues/twohistoricalmeaninglogs/noDrawstateseeded, notownerprogress. "
    "Trace downloadingmodelmessage then explicit unavailable/geometric-only: exactreference-touch/ungradedtrace/"
    "recallmiss/persistedlogs NOTMLKitrecognition/humanrecallsuccess/negativegeometry/reverseorder/phone. "
    "Readable fourfontrows do not identify actualfallbackfaces. Original312denial/parent exact shell1 dueabsentPIDs "
    "preserved, no new cleanup/device action. Fresh3103+1 source-copyXML/UTC/testimplementation hashes reverified "
    "NOTrerun. Original049HOST512MiBOOM/bounded1GiBHOSTcoreTest headroom remain HOST-only, "
    "native192m576m/font/archiveguards unchanged. OriginalinitialClaude42calls/TWOinternaloverlaps "
    "andGPT44calls/zero/all26resources and fourClaudeoptional suggestions preserved. "
    "Olderwholewordしょうじょうconstituentallocation UNVERIFIEDandOMITTED. Python368/vocabulary inherited308; "
    "source/baseline mechanicalaudit309 inherited, not freshly rerun here. Evidence-onlyvalidator/manifest/budget "
    "freshly persisted here, repeated once after successful unredirected shell validation to retain exact command output. "
    "Published81/1228,1147remaining;Androidf9b59a2+required."
)
acceptance = {
    "schemaVersion": 1, "execution": 314, "batch": "055",
    "status": "native-and-original-two-family-visual-evidence-closed-pending-combined-main-publication",
    "frozenSnapshot": head,
    "reviewedTeachingSnapshot": "a532c4d436726e6eeb46ff78cc3dc1a039d6f19e",
    "teachingDiff": "empty", "models": [p["actualModels"][0] for p in processes],
    "visualReports": ["batch-055-visual-claude.md", "batch-055-visual-gpt.md"],
    "visualProcessRecords": ["batch-055-visual-claude-execution.json", "batch-055-visual-gpt-execution.json"],
    "reconciliation": [
        {"claim": "No new actionable teaching defect in either original dependent visual confirmation", "disposition": "resolved", "teachingChange": False, "allArticleFacets": "CLEAN within bounded scope"},
        {"claim": "Readings table clips the leading part of labels at some horizontal offsets", "disposition": "optional", "remedy": "Potential app-only layout improvement; preserve full correct teaching and sideways-scroll affordance. No every-cell or full-article acceptance claimed."},
        {"claim": "Four original Claude optional expansions", "disposition": "optional", "adopted": False, "detail": "Historical 大臣 sense2 clarification; 宰相 mention; standalone 丞 office; 承 look-alike. No new consequential omission established."},
        {"claim": "Older whole-word しょうじょう constituent allocation", "disposition": "unresolved", "deliveredPositiveClaim": False, "detail": "UNVERIFIED and explicitly omitted from positive allocation teaching/practice; whole-word recognition note preserved."},
    ],
    "nativeResult": route, "terminalNativeCase0": 2, "nativeDurationSeconds": 85.809,
    "sourcePngs": 37, "distinctSourcePngHashes": 20,
    "modelVisibleImagesPerReviewer": [20, 20], "coordinatorNewDirectImageReads": 3,
    "freshNativeRun": False, "freshAndroidRun": False,
    "inheritedAndroidRecord": "docs\\n1-sources\\execution-310.json",
    "inheritedNativeRecord": "docs\\n1-sources\\execution-312.json",
    "nativeArchiveRecord": "docs\\n1-sources\\execution-313.json",
    "parentCleanupRecord": "docs\\n1-reviews\\batch-055-native\\parent-cleanup-recovery.json",
    "verifiedIndexedArtifactCount": len(indexed),
    "originalInitialReportHashesPreserved": True,
    "checks": checks, "receiptFiles": copied,
    "publicationAttempted": False, "publishedAdditions": 81, "remainingAdditions": 1147,
    "limits": limits, "nextAction": next_action,
}
target = reviews / "batch-055-native-acceptance.json"
assert not target.exists()
save(target, acceptance)
record = {
    "schemaVersion": 1, "execution": 314, "batch": "055",
    "status": acceptance["status"], "recordedAt": datetime.now().astimezone().isoformat(),
    "startingHead": head, "reviewedTeachingSnapshot": acceptance["reviewedTeachingSnapshot"],
    "scope": "SAME055 ORIGINAL serial visual confirmations/evidence closure only; no native/Android rerun, publication,056 or second runner.",
    "acceptanceRecord": str(target.relative_to(r)), "acceptanceRecordSha256": sha(target),
    "visualProcesses": [
        {"model": p["actualModels"][0], "sessionId": p["sessionId"], "startedAt": p["startedAt"],
         "completedAt": p["completedAt"], "exitCode": p["exitCode"],
         "calls": len(p["toolCalls"]), "internalOverlaps": len(p["observedToolOverlaps"]),
         "pngPayloads": p["imagePayloadsVerified"], "reportSha256": p["reportSha256"]}
        for p in processes
    ],
    "nativeTerminalCase0": 2, "nativeRerun": False, "androidRerun": False,
    "checks": checks, "runtimeUnchanged": True, "publicationAttempted": False,
    "publishedAdditions": 81, "remainingAdditions": 1147,
    "limits": limits, "nextAction": next_action,
}
execution = sources / "execution-314.json"
assert not execution.exists()
save(execution, record)
progress = load(c / "progress.json")
assert progress["checkpoint"] == 313
progress["execution314StartingState"]["status"] = "visual-confirmations-closed-evidence-ready-for-normal-signing"
progress["execution314VisualCheckpoint"] = {
    "record": str(execution.relative_to(r)), "recordSha256": sha(execution),
    "status": "verified-ready-for-normal-signing", "nextAction": next_action,
}
save(c / "progress.json", progress)
print("Closed SAME055 original serial native visual confirmations; no teaching change. Ready for normal signed LOCAL checkpoint.")
