import hashlib
import json
import shutil
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
reviews = r / "docs" / "n1-reviews"
sources = r / "docs" / "n1-sources"
native = reviews / "batch-054-native"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = "73593c32886b12443c6da65b9b6c2e393ba01ace"
assert git("rev-parse", "HEAD") == head
assert not git("status", "--porcelain", "--", "kanji", "words", "articles", "strokes", "manifest.json")
android = c.parent / "kanji-cards-android"
assert not git("status", "--porcelain", tree=android)
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
target = reviews / "batch-054-native-acceptance.json"
assert not target.exists()
n = load(sources / "execution-303.json")
a = load(sources / "execution-301.json")
v = load(c / "batch-054-recovered-evidence-verification.json")
processes = [load(reviews / f"batch-054-visual-{label}-execution.json") for label in ["claude", "gpt"]]
assert [p["actualModels"] for p in processes] == [["claude-opus-5.5"], ["gpt-6.1-sol"]]
assert datetime.fromisoformat(processes[0]["completedAt"]) < datetime.fromisoformat(processes[1]["startedAt"])
assert (reviews / "batch-054-visual-claude.md").stat().st_mtime < datetime.fromisoformat(processes[1]["startedAt"]).timestamp()
for label, p in zip(["claude", "gpt"], processes):
    assert len(p["toolCalls"]) == 24 and p["imagePayloadsVerified"] == 18
    assert p["exitCode"] == 0 and not p["observedToolOverlaps"] and not p["unfinishedTools"]
    assert sha(reviews / f"batch-054-visual-{label}.md") == p["reportSha256"]
    raw = c / f"batch-054-visual-{label}.jsonl"
    assert sha(raw) == p["rawExecutionSha256"]
    events = [json.loads(s) for s in raw.read_text(encoding="utf-8-sig").splitlines() if s.strip()]
    results = [e for e in events if e["type"] == "result"]
    assert len(results) == 1 and results[0]["sessionId"] == p["sessionId"] and results[0]["exitCode"] == 0
    assert not results[0]["usage"]["codeChanges"]["filesModified"]
    for call in p["toolCalls"]:
        assert call["success"] and not call["truncationOrLimitMarker"]
        if "imagePayload" in call:
            image = call["imagePayload"]
            assert sha(r / image["returnedPayloadCopy"]) == image["sha256"]
            assert sha(Path(call["arguments"]["path"])) == image["sourceSha256"]
            assert image["sourceDimensions"] == [1080, 2400]
            assert image["returnedDimensions"] == [900, 2000]
            assert not image["exactFileBytesReturnedToModel"]
index = load(native / "artifact-index.json")
for section in ["sourceArtifacts", "coordinatorReturnedImages"]:
    for row in index[section]:
        assert sha(r / row["path"]) == row["sha256"]
assert len(index["coordinatorReturnedImages"]) == 18
rasters = load(native / "attempt-1" / "n1-054-font-raster.json")["rows"]
assert len(rasters) == 20 and all(row["hasGlyph"] for row in rasters)
for char, count in {"且": 4, "目": 4, "日": 4, "助": 4, "苟": 1}.items():
    rows = [row for row in rasters if row["character"] == char]
    assert len(rows) == 4 and len({row["nativePaintRasterSha256"] for row in rows}) == count
assert sha(Path(a["log"])) == a["logSha256"]
for row in a["tests"]:
    for path in [Path(row["sourcePath"]), r / row["artifactPath"]]:
        assert sha(path) == row["sha256"]
        suite = ET.parse(path).getroot()
        assert int(suite.attrib["tests"]) == row["tests"]
        assert all(int(suite.attrib[key]) == 0 for key in ["failures", "errors", "skipped"])
        assert suite.attrib["timestamp"] == row["timestamp"]
        assert sorted(x.attrib["name"] for x in suite.findall("testcase")) == sorted(row["caseNames"])
    assert sha(android / row["testImplementation"]) == row["testImplementationSha256"]
assert sha(c / "batch-049-host-integration-heap.init.gradle") == a["hostInitSha256"]
prep = load(sources / "batch-054-native-preparation.json")
for rel, expected in {**prep["originalFixtureHashesUnchanged"], **n["originalInitialReportHashesUnchanged"]}.items():
    assert sha(r / rel) == expected
assert len(prep["originalFixtureHashesUnchanged"]) == 70
assert not git("diff", n["reviewedTeachingSnapshot"], "--", "kanji", "words", "articles", "strokes", "manifest.json")
copies = []
names = [
    "prepare-batch-054-visual.py", "run-batch-054-visual.ps1", "archive-batch-054-visual.py",
    "archive-batch-050-visual.py", "close-batch-054-visual.py",
    "batch-054-recovered-evidence-verification.json",
    "execution-304-copilot-help.txt", "execution-304-config-help.txt",
    "execution-304-commands-help.txt", "execution-304-settings-help.txt",
]
for label in ["claude", "gpt"]:
    names += [f"batch-054-visual-{label}-{suffix}" for suffix in ["prompt.txt", "process.json", "usage.json", "stderr.txt"]]
for name in names:
    source = c / name
    dest = native / "receipts" / name
    assert not dest.exists()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    assert sha(source) == sha(dest)
    copies.append({"source": str(source), "path": str(dest.relative_to(r)),
                   "sha256": sha(dest), "bytes": dest.stat().st_size})
next_action = (
    "SAME054 native/visual evidence CLOSED; signed LOCAL evidence checkpoint only, NOT publication. "
    "Do not repeat accepted301Android3+1/native303attempt1/compiled302fixture/two ORIGINAL visual confirmations/"
    "blind initials absent new concern. OriginalClaude1bed2f69 thenGPT572484bf actualclaude-opus-5.5/gpt-6.1-sol "
    "exited serially:24/24serialviewcalls,0/0overlaps-failures-truncations,18distinctPNGpayloads EACH; "
    "1080x2400sources returned900x2000, bothbytesets preserved. Both allfacetsCLEAN for且/且つ/no teachingfix. "
    "FivepriorClaudeoptional groupsnotadopted; horizontal-table wrapping optional app-only. "
    "Actualmeaningfallback Japanese cedar/chicken/mosquito NOTauthored目日助; one defensible answer. "
    "Curatedkunまつたつかえでかつ/correctかつ/persistedGood; fullfeedbacklookup NOTpracticekeys. "
    "Native303two terminalcase0/no skips118.893s/fullproductionContentSyncONCE1066kanji5024words86N1/"
    "fa89fc674144b377/problems0/epoch1/schema1en-ja/fullorderedショソショウ/か.つ LiteANDFull/"
    "on[]kun[か.つ]/normalizedかつ. Fivegeneratedreference-touchstrokes/ungradedtrace/modelunavailablegeometry-only/"
    "recallmiss/persistedDrawgrade/one supportreciprocalpairtwodirections/SystemBack/offline/"
    "20Paintprobes/fourstyles且目日助/readable苟single sharedfallback faceunknown. "
    "Drawing NOTMLKitrecognition/humansuccessfulrecall/negativegeometry/reverseorder/phone. "
    "32sourcePNGs18distinct14hash-equivalentcopies/tableclipping/hiddencontentlimits retained. "
    "OriginalClaude56calls/ONEinternaloverlap andGPT55calls/zero/32resources each preserved. "
    "Comparative register UNVERIFIEDandOMITTED; allrawreadings/oneかつsupport/ninedirectguards/"
    "noinferredwordlevel retained. 70originalfixtures/twoinitialreports/8290current-frozenruntimehashes unchanged. "
    "Owned303helperstopped/exacttempsabsent/unowned5556untouched/Androidclean; native192m576m unchanged/"
    "requested2048auto2560MB/MemTotal2532900kB. Original049HOST512MiBOOM/existing1GiB :core HOSTTest-only "
    "qualification NOTguestauthorization. NEXT bounded checkpoint fresh latestorigin/main fetch/normalnonrewritingmerge, "
    "resolve surgically/independentlyreview substantive teachingconflicts; ALLcombined frozen-source/baseline/"
    "exact虎[酔っ払い]猿[馬鹿]guards/membership/readinglinks/strokefonts/currentPython/vocabulary/validator/"
    "freshmanifest/original18000entry42MiBcompressed80MiBinflated56MiBretainedbudgets. "
    "Normalsigning/ownerfastforward/publicSHA/actualterminalgreenCI/EVERYimmutablepublicZIPruntimehash/"
    "terminalreceipts/ownerissue60 BEFORE counting054delivery or055. Actualpermissiondenial/signingwait "
    "preserveexactcommand-error/report/yield,no retry/workaround. No secondrunner; preserve FULLlivehistory. "
    "Published80/1228,1148remaining;Androidf9b59a2+ required;physicalphone/generalrelease/whole-set outstanding."
)
limits = (
    "Bounded native/Android re-verification and two ORIGINAL dependent visual confirmations only, not current-main/"
    "publication/physicalphone/generalrelease/whole-set acceptance. No teaching change/repeatedblindinitial/"
    "freshsource/native-speaker/modelbenchmark. Bothvisualfollowups24serialviewcalls/0overlap-failure-truncation/"
    "18actualPNGpayloads each;1080x2400source resized900x2000, bytes/hashes separate. "
    "Original30318directreads/14hash-equivalentcopies not extra independentreads; current coordinator directly "
    "inspected fontpairs/drawingfeedback/recallfeedback only, otherpixels retain303andbothreviewer provenance. "
    "Tableleftlabels orrightqualifications clipped; archaicこうしょwraps/source-onlytails clipped, "
    "NOTeverycell/fullarticle/allcolumns certification. Actualmeaningchoices cedar/chicken/mosquito "
    "NOTauthored目日助; oneanswer defensible, not allpools/largerquiz certification. Meaningfeedback "
    "notpersistedbeforeBack; readingGood/DrawNext persistence are actualfixture assertions, not reviewer-executedtests. "
    "Synthetic source/duequeues/twohistoricalmeaninglogs/noDrawstateseeded, notownerprogress. "
    "Trace downloadingmodelmessage then explicit unavailable/geometric-only: exactreference-touch/ungradedtrace/"
    "recallmiss/persistedlogs NOTMLKitrecognition/humanrecallsuccess/negativegeometry/reverseorder/phone. "
    "苟readable sharedfallback actualfaceunknown, not fourbundleddesigns; only threebundledcmaps establishedabsent, "
    "not Gothicfaceabsence. Original303ownedhelperstopped/exacttempsabsent/unowned5556untouched retained. "
    "Fresh3013+1 source-copyXML/UTC/testimplementation hashes reverified NOTrerun. Original049HOST512MiBOOM/"
    "bounded1GiBHOSTcoreTest headroom remain HOST-only, native192m576m/font/archiveguards unchanged. "
    "OriginalinitialClaude56calls/oneinternaloverlap andGPT55calls/zero/all32resources and fiveClaudeoptional "
    "suggestions preserved. Comparative register UNVERIFIEDandOMITTED. Python368/vocabulary inherited299; "
    "source/baseline mechanicalaudit300 inherited, not freshly rerun here. Evidence-onlyvalidator/manifest/budget "
    "recorded separately. Published80/1228,1148remaining;Androidf9b59a2+required."
)
corrections = [
    "Claude's 'four fonts lacking苟' is overbroad wording: absence was audited in THREE bundled font cmaps only. Gothic/system fallback face is unidentified; four readable rows and a single shared raster are established. Original report preserved unchanged.",
    "Claude's near-identical/pixel-identical-content observations do not revise byte counts: all18 assigned PNG source hashes differ; overlapping content is not independent context evidence. There are32source captures/18distincthashes/14additional hash-equivalentcopies.",
    "Claude's every-cell wording is bounded by the same report's exceptions and Limits: clippedlabels/qualificationtails mean no every-cell/full-table certification. GPT and coordinator retain that explicit limit.",
    "Metadata-based initial choice audit is qualified by actual delivered cedar/chicken/mosquito fallback labels, not authored目日助. Both reviewers found one defensible answer; no changed-pool/all-pools certification.",
]
status = "native-visual-closed-pending-combined-publication"
acceptance = {
    "schemaVersion": 1, "execution": 304, "batch": "054", "status": status,
    "reviewedTeachingSnapshot": n["reviewedTeachingSnapshot"],
    "nativeEvidence": {"path": "docs/n1-sources/execution-303.json", "sha256": sha(sources / "execution-303.json")},
    "androidEvidence": {"path": "docs/n1-sources/execution-301.json", "sha256": sha(sources / "execution-301.json")},
    "nativeFixture": {"path": "docs/n1-reviews/batch-054-native/N1Batch054NativeTest.kt", "sha256": n["nativeExecution"]["fixtureSha256"]},
    "mechanicalVerification": v, "originalReviewerVisualProcesses": processes,
    "evidenceCopies": copies, "actualModels": [p["actualModels"][0] for p in processes],
    "actualCalls": [24, 24], "actualPngReturns": [18, 18], "overlaps": [0, 0],
    "terminalNativeCaseCodes": [0, 0], "nativeDurationSeconds": 118.893,
    "fresh301AndroidCasesReverified": 4, "testsRerun": False, "runtimeUnchanged": True,
    "dispositions": [
        {"claim": "Original bounded visual gate", "status": "resolved", "evidence": "Two original actual models each read same18PNGs/two completearticles/fixture210-380, with allfacetsCLEAN and no actionable teachingdefect."},
        {"claim": "Actual 苟 fallback/readability", "status": "resolved", "evidence": "Readable in four production rows and article; one shared raster/faceunidentified. Bounded API35/defaultscale evidence only."},
        {"claim": "Five original Claude optional groups", "status": "optional", "evidence": "Not adopted; no consequential unresolved positive claim."},
        {"claim": "Horizontal table layout", "status": "optional", "evidence": "Visible sideways-scrollhint; original report and clipped-cell limitation retained. Unrelated UI changes out ofscope."},
        {"claim": "Comparative register", "status": "unresolved", "evidence": "UNVERIFIED and excluded from teaching, not a consequential asserted claim or formal-only ban."},
    ],
    "findingComparison": {
        "sharedActionableDefects": [], "uniqueVerifiedDefects": [],
        "sharedObservations": ["Readable shared苟fallback", "Actual fallbacklabels differ from authoredtrio", "Clippedtables", "Geometry-onlydrawing/recallmiss", "Operationalresults supplied not reviewer-run"],
        "optional": "Claude suggests table wrapping as app-only polish; GPT records clipping in Limits. Equivalent observation, not unique substantive discovery.",
        "boundary": "Equivalent observations compared across complete reports including limits. Same bounded scope/snapshot, no general model benchmark.",
    },
    "auditCorrections": corrections, "published": False, "publishedAdditions": 80,
    "remainingAdditions": 1148, "limits": limits, "nextAction": next_action,
}
save(target, acceptance)
for path in [reviews / "batch-054-reconciliation.json", sources / "batch-054-review-source-audit.json", sources / "batch-054-progress.json"]:
    obj = load(path)
    obj["preNativeVisualClosure"] = {key: obj[key] for key in ["status", "limits", "nextAction"] if key in obj}
    obj["status"] = status
    obj["nativeVisualAcceptancePending"] = False
    obj["nativeAcceptance"] = "docs/n1-reviews/batch-054-native-acceptance.json"
    obj["nativeVisualSupplement"] = {
        "execution": 304, "reports": ["batch-054-visual-claude.md", "batch-054-visual-gpt.md"],
        "actualModels": acceptance["actualModels"], "calls": [24, 24], "pngReturns": [18, 18],
        "overlaps": [0, 0], "testsRerun": False, "auditCorrections": corrections,
    }
    obj["limits"] = limits
    obj["nextAction"] = next_action
    save(path, obj)
save(sources / "execution-304.json", {
    "schemaVersion": 1, "execution": 304, "checkpoint": 304, "batch": "054", "status": "continue",
    "stage": "batch-054-native-visual-closed-pending-combined-publication",
    "recordedAt": datetime.now().astimezone().isoformat(),
    "startingHead": head, "reviewedTeachingSnapshot": n["reviewedTeachingSnapshot"],
    "nativeArchiveSnapshot": n["nativeExecution"]["contentSnapshot"],
    "scope": "Original Claude then GPT bounded dependent visual confirmations and normally signed LOCAL evidence checkpoint; no publication/055.",
    "acceptance": "docs/n1-reviews/batch-054-native-acceptance.json",
    "actualModels": acceptance["actualModels"], "originalVisualSessions": [p["sessionId"] for p in processes],
    "actualVisualToolCalls": [24, 24], "overlaps": [0, 0], "actualPngReturns": [18, 18],
    "sourceToReturnedDimensions": [[1080, 2400], [900, 2000]],
    "runtimeHashesVerified": 8290, "testsRerun": False, "nativeTerminalCaseCodes": [0, 0],
    "fresh301AndroidCasesReverified": 4, "originalNativeFixturesUnchanged": 70,
    "evidenceCopies": len(copies), "auditCorrections": corrections,
    "toolDiscoveryLimits": "Current CLI --help/confighelp/settingshelp acquired; help model is unsupported and returned1. Current settingshelp advertises bothrequestedmodels; actual successful resumed execution/sessionId/model verified. No unrelated settings inspected/changed.",
    "publishedAdditions": 80, "remainingAdditions": 1148,
    "lastPublishedCommit": "672266d5fffae425e608cdfa5a631ac147d1d08c",
    "blocker": None, "limits": limits, "nextAction": next_action,
})
print(f"Closed bounded native/visual gate: {len(copies)} receipts, actual24serialcalls/18PNGs each, no runtime changes/publication.")
