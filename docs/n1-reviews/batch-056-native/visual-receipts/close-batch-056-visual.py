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
native = reviews / "batch-056-native"
sources = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".execution328.tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = "6283ee5e6b90598cf92516ee6abf7cfa91d08e68"
teaching = "4dba935415312d39b1c2defdc05b938d37fe21f0"
execution_path = sources / "execution-328.json"
acceptance_path = reviews / "batch-056-native-acceptance.json"
p = load(c / "progress.json")
assert p["checkpoint"] == 327 and p["batch"] == "056"
if len(sys.argv) > 1 and sys.argv[1] == "finish":
    assert not git("status", "--porcelain")
    saved = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == head
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", head, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json")
    record = load(execution_path)
    checkpoint = {
        "execution": 328, "batch": "056", "status": record["status"],
        "savedCommit": saved, "signature": "G", "record": str(execution_path.relative_to(r)),
        "recordSha256": sha(execution_path), "nextAction": record["nextAction"],
        "recordedAt": datetime.now().astimezone().isoformat(),
        "publishedAdditions": 82, "remainingAdditions": 1146,
        "publicationAttempted": False, "nativeRerun": False, "androidRerun": False,
    }
    p.update(checkpoint=328, status="continue",
             stage="batch-056-native-original-visual-closed-pending-combined-main-publication",
             blocker=None, nextAction=record["nextAction"])
    p["execution328StartingState"]["status"] = "signed-native-visual-checkpoint-complete"
    p["execution328CoordinatorCheckpoint"] = checkpoint
    p["batch056NativeVisualCheckpoint"] = checkpoint.copy()
    save(c / "progress.json", p)
    issue = (
        f"Batch 056 advanced to a **signed local native/visual evidence checkpoint**, `{saved}`. "
        "**Not published; overall project incomplete.**\n\n"
        "The original Claude Opus 5.5 and GPT-6.1 Sol sessions completed dependent visual confirmation "
        "on the same frozen snapshot, with reviewer processes run serially: 33 view calls and 24 distinct "
        "screenshot payloads each. Both found no actionable teaching defect in 乏, 乏しい or 貧乏. "
        "Claude's raw audit records **one internal two-image overlap**; its original no-deviation, "
        "whole-article visibility, choice-identity and saved-grade overclaims are retained and explicitly "
        "corrected by the original reviewer in a three-call serial supplement. No blanket serial-tool "
        "or hidden-content certification is claimed. GPT recorded zero overlaps.\n\n"
        "All complete reports, actual model/session/process and returned-image evidence are preserved; "
        "reconciliation is `docs/n1-reviews/batch-056-native-acceptance.json`. "
        "The 54 source PNGs contain 24 distinct hashes; both reviewers received 900×2000 payloads from "
        "1080×2400 sources. Four production font rows show readable/distinguishable 乏/久/反/乃 and "
        "readable 丿/饉/飢饉; the actual fallback face remains unidentified. "
        "Table clipping and unshown article portions remain explicit limits, not whole-article acceptance. "
        "ともしい frequency/register remains UNVERIFIED and is not claimed or practiced.\n\n"
        "Accepted retry2's two native terminal-status-0 cases (117.405 s), full production sync once "
        "(1,068 kanji / 5,027 words / 88 N1, zero problems), both curated reading Good logs, "
        "offline reciprocal/System Back routes and four-stroke trace/recall-miss evidence were reverified, "
        "not rerun. Meaning feedback exits Back before persistence. Drawing Again follows recall-miss Next; "
        "reference-touch geometric-only tracing is not successful human recall or ML Kit recognition. "
        "Original 322/324 failures and 326 denial/parent exact-command recovery stay unchanged. "
        "Accepted Android 320's 3+1 evidence was reverified, not rerun. Validator, unchanged fresh manifest "
        "and original publishing budgets pass; no teaching/runtime/font/heap/guard changes.\n\n"
        "**Next bounded checkpoint:** latest-main non-rewriting integration and all combined-tree checks, "
        "normal signing, owner fast-forward push, exact remote SHA, terminal green CI and every immutable "
        "public ZIP runtime hash/budget gate before delivery or batch 057. Published remains "
        "**82/1,228; 1,146 remaining**. Android f9b59a2+ required; physical-phone/general-release and "
        "whole-set acceptance remain outstanding. Full control history preserved; no second runner."
    )
    (c / "execution-328-issue-body.txt").write_text(issue + "\n", encoding="utf-8")
    print(f"Checkpoint328 persisted: signed G {saved}; continue SAME056 combined-main acceptance next.")
    sys.exit(0)

assert git("rev-parse", "HEAD") == head
assert not git("status", "--porcelain", "--", "kanji", "words", "articles", "strokes", "manifest.json")
assert not git("diff", teaching, "--", "kanji", "words", "articles", "strokes", "manifest.json")
android = c.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=android)
labels = ("claude", "gpt", "claude-clarification")
processes = [load(reviews / f"batch-056-visual-{label}-execution.json") for label in labels]
assert [x["actualModels"] for x in processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"], ["claude-opus-5.5"]]
for first, second in zip(processes, processes[1:]):
    assert datetime.fromisoformat(first["completedAt"]) < datetime.fromisoformat(second["startedAt"])
assert (reviews / "batch-056-visual-claude.md").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
for label, process, count, images, overlaps in zip(labels, processes, (33, 33, 3), (24, 24, 2), (1, 0, 0)):
    assert process["exitCode"] == 0 and not process["unfinishedTools"]
    assert len(process["toolCalls"]) == count and process["imagePayloadsVerified"] == images
    assert len(process["observedToolOverlaps"]) == overlaps and process["expectedPngMembershipReturned"]
    assert sha(reviews / f"batch-056-visual-{label}.md") == process["reportSha256"]
    assert sha(c / f"batch-056-visual-{label}.jsonl") == process["rawExecutionSha256"]
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
pngs = list((native / "attempt-3-retry2").glob("*.png"))
assert len(pngs) == 54 and len({sha(x) for x in pngs}) == 24
index = load(native / "execution-326-artifact-index.json")
for row in index["files"]:
    assert sha(r / row["path"]) == row["sha256"]
assert len(index["files"]) == 63
original327 = load(sources / "execution-327.json")
assert sha(sources / "execution-326.json") == original327["originalNativeRecordSha256"]
assert sha(r / original327["parentCleanupRecoveryArchive"]) == original327["parentCleanupRecoveryArchiveSha256"]
raw = (native / "attempt-3-retry2" / "instrumentation.txt").read_text(encoding="utf-8")
assert re.findall(r"^INSTRUMENTATION_STATUS_CODE: (-?\d+)$", raw, re.M) == ["1", "0", "1", "0"]
assert "Time: 117.405" in raw and "OK (2 tests)" in raw
route = load(native / "attempt-3-retry2" / "n1-056-article-route.json")
assert route["passed"] and route["archiveRequests"] == 1 and not route["phoneEvidence"]
assert [route[x] for x in ("importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch")] == [1068, 5027, 88, 0, 1]
assert route["contentVersion"] == "cb85043f73a606f3"
assert route["fullOnyomi"] == ["ボウ"] and route["fullKunyomi"] == ["とぼ.しい", "とも.しい"]
assert route["quizOnKeys"] == ["ぼう"] and route["quizKunKeys"] == ["とぼしい"]
assert all(route[x] for x in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                            "bothCuratedQuestionsAndPersistedGrades", "drawingTraceThenRecall",
                            "drawingGradeRecordedOnNext", "offline"))
initial = load(reviews / "batch-056-reconciliation.json")
for label, row in zip(("claude", "gpt"), initial["reviewProcesses"]):
    assert sha(reviews / f"batch-056-initial-{label}.md") == row["reportSha256"]
a = load(sources / "execution-320.json")
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
    result = subprocess.run(["python", "-B", *args], cwd=r, text=True, encoding="utf-8", capture_output=True)
    check = {"command": ["python", "-B", *args], "exitCode": result.returncode,
             "stdout": result.stdout, "stderr": result.stderr}
    checks.append(check)
    assert result.returncode == 0, check
assert not git("diff", "--", "manifest.json")
receipts = native / "visual-receipts"
receipts.mkdir()
names = [
    "start-execution-328.py", "batch-056-visual-task.txt", "run-batch-056-visual.ps1",
    "run-batch-056-visual-claude-clarification.ps1", "archive-batch-056-visual.py", "close-batch-056-visual.py",
]
for label in labels:
    names += [f"batch-056-visual-{label}-{suffix}" for suffix in ("process.json", "usage.json", "stderr.txt")]
copied = []
for name in names:
    source, dest = c / name, receipts / name
    shutil.copyfile(source, dest)
    assert sha(source) == sha(dest)
    copied.append({"path": str(dest.relative_to(r)), "sha256": sha(dest)})
next_action = (
    "SAME056 native and ORIGINAL two-family bounded visual confirmation closed; signed LOCAL evidence checkpoint only, "
    "NOT publication. Do not rerun accepted320Android3+1/native326retry2/initialreviews/visuals absent a new concern. "
    "OriginalClaude1d0d537e actualclaude-opus-5.5 thenGPT51bbf606 actualgpt-6.1-sol processes exited serially:33calls/"
    "24distinctPNGpayloads EACH; ClaudeONEinternaltwoimageoverlap retained, GPTzero; originalClaude3callserial "
    "clarification withdrew no-deviation/fullarticlevisibility/speculative之identity/incorrectgrades claims. "
    "Allreports/audits preserved; no teachingfix. 54sourcePNGs24distinct/30hash-equivalentcopies;1080x2400sources "
    "returned900x2000, bothbytesets preserved. Fourfontrows乏久反乃 distinguishable/丿饉飢饉readable; fallbackfaceunknown. "
    "Tableclipping/hiddencontent UNVERIFIED, notfullarticle/everycellcertification. ともしいfrequency/register "
    "UNVERIFIEDnotclaimed/notpractice; original3optionalnotadopted. Native326actual2case0/no skips117.405s/"
    "productionContentSyncONCE1068kanji5027words88N1/cb85043f73a606f3/problems0/epoch1/LiteANDfullorderedボウ/"
    "とぼ.しいとも.しい/curatedぼうとぼしい/twopairsfourdirections/SystemBack/offline/meaningfeedbackBackwithoutpersist/"
    "bothcuratedGood/fourreference-touchstrokes/ungradedtrace/recallmiss/persistedDrawAgain. NOTMLKit/"
    "correcthumanrecall/negativegeometry/reverseorder/phone. Original322twofailures/324glyph0article-2/326denial "
    "andparentEXACTcleanupverificationexit0 unchanged. Original049HOST512MiBOOM/existing1GiBHOSTcoreTest-only/"
    "native192m576m unchanged. NEXT bounded checkpoint fresh latestorigin/main fetch/normalnonrewritingmerge, "
    "surgicalconflicts/reviewsubstantiveteaching; ALLcombined frozen-source/baseline/exactmembership/originalguards/"
    "readings/links/strokes/fonts/currentPython/vocabulary/validator/freshmanifest/18000entries42MiBcompressed"
    "80MiBinflated56MiBretainedbudgets/normalsigning/ownerfastforward/exactremoteSHA/terminalgreenCI/"
    "EVERYimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFOREdelivery or057. Actualpermissiondenial/"
    "signingwait preserveexactcommand-error/report/yield,no retry/workaround. Preserve FULLlivehistory, nosecondrunner. "
    "Published82/1228,1146remaining latest0559b5e9fd9f596801eb78078ab14e4c4b35973479d;Androidf9b59a2+required;"
    "physicalphone/generalrelease/whole-setoutstanding;overallincomplete."
)
limits = (
    "Dependent bounded visuals, not blind initial/fresh dictionary/native-speaker/model benchmark/reviewer-run tests. "
    "Claude's ONE initial internal overlap is a real process deviation; zero-overlap clarification does not erase it. "
    "No reviewer processes overlapped. Original complete report retained with original-session correction supplement. "
    "All33/33/3calls returned,24/24/2actualPNGpayloads,1080x2400to900x2000. 54sourcePNGs24distincthashes; "
    "30equivalentcopies not independent visual reads. Coordinator directly viewed fontpairs/kanjikun/drawingfeedback "
    "only this execution; otherpixel claims retain bothreviewers' provenance. Hidden/clipped content/everycell/"
    "fullarticle rendering UNVERIFIED, no blanket acceptance. ともしいfrequency/register UNVERIFIEDnotclaimed. "
    "Actualmeaningchoices scarce;lacking/whale/handle;dealwith/thereupon;possessiveno includeauthored乃, "
    "notestablished之. Meaningfeedback notpersistedbeforeBack; bothcuratedGood andDrawAgainNext actualfixtureassertions. "
    "Reference-touch/ungradedtrace/modelunavailablegeometry-only/recallmiss NOTMLKit/correcthumanrecall/"
    "negativegeometry/reverseorder. Fallbackfaceunidentified; nativeAPI35notphone. Originalfailures/denial/"
    "parentrecovery retained; no native/Android rerun. Originalthreeoptional remainunadopted. Freshvalidator/"
    "manifest/budget repeated for persisted commandoutput after initial successful shellvalidation. FullPython/"
    "vocabulary/source/baseline integration checks NOTfreshlyrunhere; required next onactualcombinedmain. "
    "No teaching/runtime/font/heap/archiveguard changes, publication/057/secondrunner. "
    "Compatiblef9b59a2+required;physicalphone/generalrelease/whole-setoutstanding."
)
acceptance = {
    "schemaVersion": 1, "execution": 328, "batch": "056",
    "status": "native-and-original-two-family-bounded-visual-closed-pending-combined-main-publication",
    "frozenSnapshot": head, "reviewedTeachingSnapshot": teaching, "teachingDiff": "empty",
    "visualReports": [f"batch-056-visual-{label}.md" for label in labels],
    "visualProcessRecords": [f"batch-056-visual-{label}-execution.json" for label in labels],
    "models": ["claude-opus-5.5", "gpt-6.1-sol"], "reviewerProcessesSerial": True,
    "observedInternalOverlaps": [1, 0, 0], "actualCalls": [33, 33, 3],
    "reconciliation": [
        {"claim": "No new actionable teaching defect on bounded visible scope", "disposition": "resolved", "teachingChange": False, "allArticleFacets": "CLEAN within textual and bounded viewport scope"},
        {"claim": "Claude no-deviations report versus actual two-image overlap", "disposition": "resolved", "detail": "Original-session supplement withdraws universal serial claim. Original overlap retained, not erased by serial rereads."},
        {"claim": "Claude full-article/every-row visibility", "disposition": "withdrawn", "detail": "Universal rendering conclusion UNVERIFIED; hidden and clipped portions excluded from bounded acceptance."},
        {"claim": "Claude speculative choice identity and saved grades", "disposition": "resolved", "detail": "乃 not established之; meaning exits Back without persistence; BOTH reading Good logs and drawing Again after Next. Original inaccuracies and supplement retained."},
        {"claim": "Horizontal table clipping and mixed practice/grading app wording", "disposition": "optional", "detail": "Existing app presentation observation; no new teaching defect, no out-of-scope app change or complete viewport certification."},
        {"claim": "Three original Claude optional suggestions", "disposition": "optional", "adopted": False, "detail": "貧乏/悪い guard; unverified Nに乏しい expansion; short/small upper-slant wording."},
        {"claim": "ともしい frequency/register", "disposition": "unresolved", "deliveredPositiveClaim": False, "detail": "UNVERIFIED; no frequency/register claim or quiz practice for this recognition-only reading."},
    ],
    "nativeResult": route, "terminalNativeCase0": 2, "nativeDurationSeconds": 117.405,
    "sourcePngs": 54, "distinctSourcePngHashes": 24, "hashEquivalentCopies": 30,
    "modelVisibleImagesPerReview": [24, 24, 2], "coordinatorNewDirectImageReads": 3,
    "freshNativeRun": False, "freshAndroidRun": False, "verified326IndexedArtifacts": 63,
    "acceptedAndroid": "docs\\n1-sources\\execution-320.json",
    "originalNative": "docs\\n1-sources\\execution-326.json",
    "archivalParentRecovery": "docs\\n1-sources\\execution-327.json",
    "originalInitialReportHashesPreserved": True,
    "checks": checks, "receiptFiles": copied,
    "catalogEvidence": [
        {"path": str(c / name), "sha256": sha(c / name)}
        for name in ("copilot-help-execution-328.txt", "copilot-config-execution-328.txt")
    ],
    "publicationAttempted": False, "publishedAdditions": 82, "remainingAdditions": 1146,
    "limits": limits, "nextAction": next_action,
}
assert not acceptance_path.exists() and not execution_path.exists()
save(acceptance_path, acceptance)
record = {
    "schemaVersion": 1, "execution": 328, "batch": "056", "status": acceptance["status"],
    "recordedAt": datetime.now().astimezone().isoformat(), "startingHead": head,
    "scope": p["execution328StartingState"]["scope"],
    "acceptanceRecord": str(acceptance_path.relative_to(r)), "acceptanceRecordSha256": sha(acceptance_path),
    "visualProcesses": [
        {"model": x["actualModels"][0], "sessionId": x["sessionId"], "startedAt": x["startedAt"],
         "completedAt": x["completedAt"], "exitCode": x["exitCode"], "calls": len(x["toolCalls"]),
         "internalOverlaps": len(x["observedToolOverlaps"]), "pngPayloads": x["imagePayloadsVerified"],
         "reportSha256": x["reportSha256"]} for x in processes
    ],
    "checks": checks, "nativeRerun": False, "androidRerun": False, "runtimeUnchanged": True,
    "publicationAttempted": False, "publishedAdditions": 82, "remainingAdditions": 1146,
    "limits": limits, "nextAction": next_action,
}
save(execution_path, record)
p["execution328StartingState"]["status"] = "visual-confirmations-reconciled-ready-for-normal-signing"
p["execution328VisualCheckpoint"] = {
    "record": str(execution_path.relative_to(r)), "recordSha256": sha(execution_path),
    "status": "verified-ready-for-normal-signing", "nextAction": next_action,
}
save(c / "progress.json", p)
print("SAME056 original bounded visuals reconciled; exact reports/audits/images preserved; ready for normally signed local checkpoint.")
