import hashlib
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
reviews = r / "docs" / "n1-reviews"
sources = r / "docs" / "n1-sources"
native = reviews / "batch-053-native"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = "c3880ee222728c1209e988b0d0b6d6563c1bfc38"
assert git("rev-parse", "HEAD") == head
assert not git("status", "--porcelain", "--", "kanji", "words", "articles", "strokes", "manifest.json")
assert not git("status", "--porcelain", tree=c.parent / "kanji-cards-android")
target = reviews / "batch-053-native-acceptance.json"
assert not target.exists()
n = load(c / "batch-053-parent-native-recovery.json")
a = load(sources / "execution-292.json")
v = load(c / "batch-053-recovered-evidence-verification.json")
processes = [load(reviews / f"batch-053-visual-{label}-execution.json") for label in ["claude", "gpt"]]
assert [p["actualModels"] for p in processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
assert (reviews / "batch-053-visual-claude.md").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
for label, p in zip(["claude", "gpt"], processes):
    assert len(p["toolCalls"]) == 28 and p["imagePayloadsVerified"] == 21
    assert p["exitCode"] == 0 and not p["observedToolOverlaps"] and not p["unfinishedTools"]
    assert sha(reviews / f"batch-053-visual-{label}.md") == p["reportSha256"]
    assert sha(c / f"batch-053-visual-{label}.jsonl") == p["rawExecutionSha256"]
    for call in p["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
            assert image["sourceDimensions"] == [1080, 2400]
            assert image["returnedDimensions"] == [900, 2000]
            assert not image["exactFileBytesReturnedToModel"]
copies = list(v["evidenceCopies"])
for row in copies:
    assert sha(r / row["path"]) == row["sha256"] == sha(Path(row["source"]))
names = [
    "prepare-batch-053-visual.py", "run-batch-053-visual.ps1", "archive-batch-053-visual.py",
    "archive-batch-050-visual.py", "close-batch-053-visual.py",
]
for label in ["claude", "gpt"]:
    names += [f"batch-053-visual-{label}-{suffix}" for suffix in ["prompt.txt", "process.json", "usage.json", "stderr.txt"]]
for name in names:
    source = c / name
    dest = native / "receipts" / name
    assert not dest.exists()
    shutil.copyfile(source, dest)
    assert sha(source) == sha(dest)
    copies.append({"source": str(source), "path": str(dest.relative_to(r)),
                   "sha256": sha(dest), "bytes": dest.stat().st_size})
next_action = (
    "SAME053 native/visual evidence CLOSED; signed LOCAL evidence checkpoint only, NOT publication. "
    "Do not repeat accepted freshAndroid2923+1/native294attempt1/two ORIGINAL visual confirmations absent new concern. "
    "OriginalClaude38b9b66d thenGPT54a998a9 actualclaude-opus-5.5/gpt-6.1-sol exited serially:28/28serialviewcalls,"
    "0/0overlaps-failures-truncations,21distinctPNGpayloads EACH;1080x2400sources returned900x2000, bothbytesets preserved. "
    "AllninefacetsCLEAN each/no teachingfix; fourpriorClaudeoptional groupsnotadopted; stroke-label proximity optional app-only. "
    "Observed meaningwronglabels monkey/handle;dealwith/concave;sunken, NOT authored内肉病; no displayed ambiguity established. "
    "Bothactualreadingskunひのえ thenonヘイ inONEsession/grade3logs; meaningfeedback NOTpersistedbeforeBack. "
    "Firstunchanged nativeattempt2terminalcase0/no skips92.792s/fullproductionContentSyncONCE1065/5023/N185/"
    "ba2d74eac9ea12e1/problems0/epoch1/fullヘイひのえ/rawcurationsnormalizedへいひのえ/"
    "fivegeneratedreference-touchstrokes/ungradedtraceWellDrawn/recallmiss/persistedDrawgrade/"
    "two support reciprocalpairs/fourdirections+丙午->existing午/SystemBack/offline/16Paintprobes/fourstyles丙内肉病. "
    "Drawing geometry-only/modelunavailable, NOTMLKitrecognition/humansuccessfulrecall/negativegeometry/reverseorder/phone. "
    "35PNGs21distinct14hash-equivalentcopies/tableclipping/hiddencontentlimits retained. "
    "Original294discoverydenial and exactparentrecovery/ownedhelpercleanup/unowned5556untouched retained; "
    "fresh292source-copyXML/testimplementationhashes verified notrerun; original049HOST512MiBOOM/"
    "existing1GiB :core HOSTTest-onlyheadroom, native192m576m/noHOSTinit retained. "
    "Initial56/58calls32resources/TWOClaudeinternaloverlaps/oversizedjlptreadrecovered/"
    "GPTnine-vs-actualeightcomparisonwords correction preserved. "
    "NEXT bounded checkpoint latestorigin/main fetch/normalnonrewritingmerge, resolve surgically/independentlyreview "
    "substantive teachingconflicts; ALLcombined frozen-source/baseline/exact虎[酔っ払い]猿[馬鹿]guards/membership/"
    "readinglinks/strokefonts/currentPython/vocabulary/validator/freshmanifest/original18000entry42MiBcompressed/"
    "80MiBinflated56MiBretainedbudgets. Normalsigning/ownerfastforward/publicSHA/actualterminalgreenCI/"
    "EVERYimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFORE counting053delivery or054. "
    "No secondrunner/signingbypass/permissionworkaround. Preserve FULLlivehistory. Published79/1228,1149remaining;"
    "Androidf9b59a2+ required;physicalphone/generalrelease/whole-set outstanding."
)
limits = (
    "Bounded recovered native/Android and two ORIGINAL dependent visual confirmations only, not current-main/"
    "publication/physicalphone/generalrelease/whole-set acceptance. No teaching change/repeatedblindinitial/"
    "freshsource/native-speaker/modelbenchmark. Bothvisualfollowups28serialviewcalls,0overlap/failure/truncation,"
    "21actualPNGpayloads each;1080x2400source resized900x2000, bytes/hashes separate. Parent21directreads/"
    "14hash-equivalentcopies not extra independentreads; current coordinator directly inspected fontpairs/"
    "drawingfeedback/recallfeedback only, otherpixels retainparentprovenance plus bothreviewerreads. "
    "Boundedviewports/readingsrightedge or offsetleftcolumnclipped, NOTfullarticle/allcolumncertification. "
    "Meaningchoices actualmonkey/handle;dealwith/concave;sunken NOTauthored内肉病; no ambiguity established, "
    "not allpools/largerquiz certification. Meaningfeedback notpersistedbeforeBack; bothreadingsgrade3 and DrawNext"
    "persistence are fixture assertions in supplied actualrun, not reviewer-executed tests. "
    "Synthetic source/duequeues/twohistoricalmeaninglogs/noDrawstateseeded, notownerprogress. "
    "Trace downloadingmodelmessage then explicit unavailable/geometric-only: exactreference-touch/ungradedtrace/"
    "recallmiss/persistedlogs do NOTprove MLKitrecognition/humanrecallsuccess/negativegeometry/reverseorder/phone. "
    "Existing午viewedrouteonly/notfreshlycertified. Source-only冂notauthored/no newfallbackfaceclaim. "
    "Original294discoverydenial/exactparentrecovery/ownedhelperstopped/exacttempsabsent/unowned5556untouched retained. "
    "Actual292fresh3+1 source-copyXML/UTC/implementationhashes reverified, NOTrerun or052reuse. "
    "Original049HOST512MiBOOM and bounded1GiBHOSTcoreTest headroom remain HOST-only, "
    "native192m576m/font/archiveguards unchanged/noHOSTinit. Initial56/58calls/all32resources,Claude2internaloverlaps/"
    "oversizedjlptreadrecovered/GPTnine-vs-actualeightwordcount correction and alloriginalreports preserved. "
    "No teaching defect; fourpriorClaudeoptional groups notadopted; stroke-number proximity optional app rendering"
    "outsidekanji task, not newteaching defect. Python368/vocabulary inherited290 and source/baseline mechanical "
    "audit291; no claim freshly rerun here. Fresh evidence-only validator/manifest/budget recorded separately. "
    "Published79/1228,1149remaining;Androidf9b59a2+ required."
)
status = "native-visual-closed-pending-combined-publication"
visual = dict(n["parentVisual"])
visual.update(
    independentVisualConfirmationPending=False,
    independentReports=["batch-053-visual-claude.md", "batch-053-visual-gpt.md"],
    actualModels=["claude-opus-5.5", "gpt-6.1-sol"],
    actualToolCalls=[28, 28], overlappingStarts=[0, 0], assignedPngReturnsPerReviewer=[21, 21],
    imageTransportBoundary="1080x2400source ->900x2000returned; separately preserved bytes/hashes.",
)
acceptance = {
    "schemaVersion": 1, "execution": 295, "batch": "053", "status": status,
    "native": {k: val for k, val in n.items() if k not in ["parentVisual", "pending"]},
    "visual": visual, "android": a, "recoveryVerification": v,
    "originalReviewerVisualProcesses": processes, "evidenceCopies": copies,
    "dispositions": [
        {"claim": "Original bounded visual gate", "status": "resolved", "evidence": "Two original models each read same21distinctPNGs/threearticles/fixture210-380; no actionable teaching defect."},
        {"claim": "Initial textual metadata-based choice assessment proves actual curated choice delivery", "status": "withdrawn", "evidence": "Actual monkey/handle;dealwith/concave;sunken labels differ from内肉病. Both reviewers found one defensible answer; no appchange in scope."},
        {"claim": "Prior four Claude optional teaching groups", "status": "optional", "evidence": "Original dispositions preserved, not adopted, no new consequential claim."},
        {"claim": "Stroke-number2/3 proximity and table clipping", "status": "optional", "evidence": "Visible app-level polish/scope limitation, not demonstrated teaching defect. No unrelated UI change."},
    ],
    "findingComparison": {
        "sharedActionableDefects": [], "uniqueVerifiedDefects": [],
        "sharedObservations": ["Actual meaning choices differ from authored trio", "Four readable glyph styles", "Clipped tables", "Geometry-only drawing/recall miss", "Operational results supplied rather than reviewer-run"],
        "uniqueOptionalObservation": "Claude noted stroke-number2/3 proximity; GPT did not. Optional app rendering, not verified unique linguistic defect.",
        "boundary": "Equivalent observations compared across full reports including limits. Same scope/snapshot, no general model benchmark.",
    },
    "auditCorrections": [
        "Both visual reports accurately self-count28calls. GPT explicitly corrects original nine comparison words to actualeight; original initial report preserved.",
        "Claude now qualifies original metadata-based quiz audit: actual displayed labels monkey/handle;dealwith/concave;sunken are not authored内肉病; no ambiguity established.",
        "Report supplied signedHEAD/emptydiff statements verified by coordinator, not shell-disabled reviewers. Uncommitted contributor evidence only.",
    ],
    "published": False, "publishedAdditions": 79, "remainingAdditions": 1149,
    "limits": limits, "nextAction": next_action,
}
save(target, acceptance)
for path in [reviews / "batch-053-reconciliation.json", sources / "batch-053-review-source-audit.json", sources / "batch-053-progress.json"]:
    obj = load(path)
    obj["preNativeVisualClosure"] = {key: obj[key] for key in [
        "status", "stage", "limits", "nextAction", "nativeVisualAcceptancePending", "acceptanceBlocker", "pendingQualification"
    ] if key in obj}
    obj["status"] = status
    obj["nativeVisualAcceptancePending"] = False
    obj["nativeAcceptance"] = "docs/n1-reviews/batch-053-native-acceptance.json"
    obj["nativeVisualSupplement"] = {
        "execution": 295, "reports": visual["independentReports"], "actualModels": visual["actualModels"],
        "calls": [28, 28], "pngReturns": [21, 21], "overlaps": [0, 0], "testsRerun": False,
        "auditCorrections": acceptance["auditCorrections"],
    }
    if "pendingQualification" in obj:
        obj["pendingQualification"] = ["Latest-main/allcombined/signing/ownerpush/terminalCI/everyimmutablepublicZIPruntimehash/originalbudget/terminalreceipts."]
    if "quizAudit" in obj:
        obj["quizAudit"]["丙"]["nativeObservation"] = acceptance["auditCorrections"][1]
    obj["limits"] = limits
    obj["nextAction"] = next_action
    save(path, obj)
record = {
    "schemaVersion": 1, "execution": 295, "checkpoint": 295, "batch": "053", "status": "continue",
    "stage": "batch-053-native-visual-closed-pending-combined-publication",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "startingHead": head, "reviewedTeachingSnapshot": "3e37ebdac9af2880ceaa810ca34a7588d8c1d602",
    "nativeArchiveSnapshot": n["actualResult"]["route"]["contentSnapshot"], "androidHead": n["androidHead"],
    "scope": "Recovered evidence re-verification/original Claude then GPT visual confirmation; signed evidence-only checkpoint, no publication/054.",
    "acceptance": "docs/n1-reviews/batch-053-native-acceptance.json",
    "actualModels": visual["actualModels"], "originalVisualSessions": [p["sessionId"] for p in processes],
    "actualVisualToolCalls": [28, 28], "overlaps": [0, 0], "actualPngReturns": [21, 21],
    "sourceToReturnedDimensions": [[1080, 2400], [900, 2000]],
    "runtimeHashesVerified": 8287, "testsRerun": False, "nativeTerminalCaseCodes": [0, 0], "fresh292AndroidCases": 4,
    "evidenceCopies": len(copies), "auditCorrections": acceptance["auditCorrections"],
    "verificationHelperFailures": v["verificationHelperFailures"],
    "publishedAdditions": 79, "remainingAdditions": 1149,
    "lastPublishedCommit": "e16c95b3edc55975b7a2c7985bf730425baa2f83",
    "blocker": None, "limits": limits, "nextAction": next_action,
}
save(sources / "execution-295.json", record)
print(f"Reconciled native/visual gate: {len(copies)} exact copied evidence artifacts; two original models28calls/21PNGs/0overlaps each. No runtime edits/publication.")
