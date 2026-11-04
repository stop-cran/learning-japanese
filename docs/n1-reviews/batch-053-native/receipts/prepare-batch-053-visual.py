import hashlib
import json
import shutil
import struct
import subprocess
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
a = c.parent / "kanji-cards-android"
reviews = r / "docs" / "n1-reviews"
native = reviews / "batch-053-native"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = "c3880ee222728c1209e988b0d0b6d6563c1bfc38"
assert git("rev-parse", "HEAD") == head
assert not git("status", "--porcelain")
assert not git("status", "--porcelain", tree=a)
assert git("rev-parse", "HEAD", tree=a) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
p = load(c / "progress.json")
assert p["checkpoint"] == 294 and p["batch"] == "053"
if "execution295StartingState" not in p:
    p["execution295StartingState"] = {
        "execution": 295, "startingHead": head,
        "startedAt": datetime.now().astimezone().isoformat(),
        "scope": "SAME053 recovered native evidence verification; original Claude then GPT dependent visual confirmations serially; signed LOCAL evidence checkpoint/owner issue only. No publication/054/second runner.",
        "status": "verifying-recovered-native-evidence",
        "authorizationAcquired": "Complete request1-13199 including final checkpoint and complete issue60 including123-129 tail acquired. Live full history preserved.",
    }
    save(c / "progress.json", p)
    save(c / "execution-295-starting-progress.json", p)
else:
    assert p["execution295StartingState"]["startingHead"] == head
    assert p["execution295StartingState"]["status"] == "verifying-recovered-native-evidence"
n = load(c / "batch-053-parent-native-recovery.json")
prep = load(r / "docs" / "n1-sources" / "batch-053-native-preparation.json")
for row in load(c / "batch-053-parent-native-provenance.json"):
    assert sha(Path(row["path"])) == row["sha256"], row
assert sha(Path(prep["archive"])) == prep["archiveSha256"] == n["archiveSha256"]
assert sha(Path(prep["fixture"])) == prep["fixtureSha256"] == n["fixtureSha256"]
apk = Path(prep["compilation"]["apks"][0]["frozenPath"])
assert sha(apk) == n["frozenTestApkSha256"]
for rel, expected in prep["originalFixtureHashesUnchanged"].items():
    assert sha(r / rel) == expected
for rel, expected in prep["originalInitialReportHashesUnchanged"].items():
    assert sha(r / rel) == expected
assert not git("diff", prep["reviewedTeachingSnapshot"], "HEAD", "--",
               "kanji", "words", "articles", "strokes", "manifest.json")
m = load(r / "manifest.json")
with zipfile.ZipFile(prep["archive"]) as z:
    prefix = "n1-batch-053/"
    manifests = [x for x in z.namelist() if x.endswith("/manifest.json")]
    assert manifests == [prefix + "manifest.json"]
    assert z.read(prefix + "manifest.json") == (r / "manifest.json").read_bytes()
    files = {}
    binary_sections = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    for section in ["files", "images", "scenes", "listening", "audio", "curriculum",
                    "listeningTasks", "listeningTaskAudio", "listeningTaskImages"]:
        for rel, expected in m.get(section, {}).items():
            assert rel not in files
            files[rel] = expected
            archived = z.read(prefix + rel)
            current = (r / rel).read_bytes()
            if section not in binary_sections:
                archived = archived.replace(b"\r\n", b"\n")
                current = current.replace(b"\r\n", b"\n")
            assert hashlib.sha256(archived).hexdigest() == expected, rel
            assert hashlib.sha256(current).hexdigest() == expected, rel
    assert len(files) == 8287 and len(z.infolist()) == 8309
log = Path(n["actualResult"]["log"])
assert sha(log) == n["actualResult"]["logSha256"]
text = log.read_text(encoding="utf-8-sig")
assert text.count("INSTRUMENTATION_STATUS_CODE: 0") == 2
assert text.count("INSTRUMENTATION_STATUS_CODE: 1") == 2
assert "OK (2 tests)" in text and "Time: 92.792" in text
assert not any(x in text for x in ["INSTRUMENTATION_STATUS_CODE: -2", "FAILURES", "INSTRUMENTATION_STATUS_CODE: -3"])
android = load(r / "docs" / "n1-sources" / "execution-292.json")
assert sha(Path(android["log"])) == android["logSha256"]
for row in android["tests"]:
    for path in [Path(row["sourcePath"]), r / row["artifactPath"]]:
        assert sha(path) == row["sha256"]
        suite = ET.parse(path).getroot()
        assert int(suite.attrib["tests"]) == row["tests"]
        assert all(int(suite.attrib[k]) == 0 for k in ["failures", "errors", "skipped"])
        assert suite.attrib["timestamp"] == row["timestamp"]
        assert sorted(x.attrib["name"] for x in suite.findall("testcase")) == sorted(row["caseNames"])
    assert sha(a / row["testImplementation"]) == row["testImplementationSha256"]
assert sha(c / "batch-049-host-integration-heap.init.gradle") == android["hostInitSha256"]
for rel in [
    r"app\src\androidTest\java\io\github\stopcran\kanji\ui\N1Batch053NativeTest.kt",
    r"app\src\androidTest\assets\n1-batch-053-93c55a2c-envelope.zip",
]:
    assert not (a / rel).exists()
copies = []


def copy(source, destination):
    assert not destination.exists(), destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    assert sha(source) == sha(destination)
    copies.append({"source": str(source), "path": str(destination.relative_to(r)),
                   "sha256": sha(destination), "bytes": destination.stat().st_size})


index = load(Path(n["artifactIndex"]))
assert len(index) == 39
pngs = {}
for row in index:
    source = Path(row["path"])
    assert sha(source) == row["sha256"]
    dest = native / "attempt-1" / source.name
    copy(source, dest)
    if source.suffix == ".png":
        assert struct.unpack(">II", source.read_bytes()[16:24]) == (1080, 2400)
        pngs[source.name] = row["sha256"]
assert len(pngs) == 35 and len(set(pngs.values())) == 21
scope = []
for group in n["parentVisual"]["viewportGroups"]:
    for name in group["files"]:
        assert pngs[name] == group["sha256"].lower()
    name = group["files"][0]
    scope.append({"path": str(native / "attempt-1" / name), "sha256": pngs[name]})
assert len(scope) == 21 and len({x["sha256"] for x in scope}) == 21
route = load(native / "attempt-1" / "n1-053-article-route.json")
for key, value in {
    "archiveRequests": 1, "importedKanji": 1065, "importedWords": 5023,
    "n1Cards": 85, "problems": 0, "acceptedReadingParserEpoch": 1,
    "fullOnyomi": ["ヘイ"], "fullKunyomi": ["ひのえ"],
    "quizOnKeys": ["へい"], "quizKunKeys": ["ひのえ"],
    "contentSnapshot": prep["contentSnapshot"], "contentVersion": "ba2d74eac9ea12e1",
    "passed": True, "reciprocalLinkAndSystemBack": True, "bothCuratedKindsAndPersistedGrades": True,
    "drawingGradeRecordedOnNext": True, "touchInjectedReferenceStrokes": 5, "offline": True,
}.items():
    assert route[key] == value, key
rasters = load(native / "attempt-1" / "n1-053-font-raster.json")["rows"]
assert len(rasters) == 16 and all(x["hasGlyph"] for x in rasters)
for char in ["丙", "内", "肉", "病"]:
    rows = [x for x in rasters if x["character"] == char]
    assert len(rows) == 4 and len({x["nativePaintRasterSha256"] for x in rows}) == 4
receipt_names = [
    "batch-053-parent-native-recovery.json", "batch-053-parent-native-provenance.json",
    "batch-053-parent-native-attempt-1-artifact-index.json", "batch-053-parent-native-device-readiness.json",
    "batch-053-parent-checkpoint-recovery.json", "execution-294-permission-blocker.json",
    "batch-049-parent-android-host-memory-recovery.json", "batch-049-host-integration-heap.init.gradle",
]
for name in receipt_names:
    copy(c / name, native / "receipts" / name)
copy(log, native / "receipts" / log.name)
verification = {
    "execution": 295, "batch": "053", "verifiedAt": datetime.now().astimezone().isoformat(),
    "startingHead": head, "sameVisualScope": scope, "evidenceCopies": copies,
    "verifiedRuntimeHashes": len(files), "nativeTerminalCase0": 2, "nativeDurationSeconds": 92.792,
    "nativeRerun": False, "androidRerun": False, "fresh292NamedCases": 4,
    "pngs": 35, "distinctPngs": 21, "hashEquivalentCopies": 14,
    "paintProbes": 16, "fourRasterStylesEach": True, "originalFixturesAndInitialReportsUnchanged": True,
    "verificationHelperFailures": [
        "First helper stopped at an incorrect unprefixed-manifest ZIP assumption before any evidence copy/review; actual frozen envelope has n1-batch-053/ prefix. Corrected exact prefix, archive bytes unchanged.",
        "Read-only shape probe used implicit cp1252 for manifest and failed Unicode decode after printing ZIP prefix. Helper uses explicit UTF-8; no source changes or permission denial.",
        "Second helper stopped before copies at byte-hash versus canonical text hash mismatch. Inspected build_manifest.py: textual sections normalize CRLF, four binary sections hash exact bytes; applied existing contract across all nine sections, not hash/guard weakening. Frozen ZIP/current manifest bytes unchanged.",
    ],
    "boundary": "Exact receipts/source-copy XML/implementation/archive/APK/runtime/PNG hashes reverified. Parent operational21directreads and owned-helper cleanup are historical parent evidence, not a fresh native run or current coordinator visual inspection. Temporary source/asset absent and Android clean.",
}
save(c / "batch-053-recovered-evidence-verification.json", verification)
save(native / "receipts" / "batch-053-recovered-evidence-verification.json", verification)
for label, model, session in [
    ("claude", "claude-opus-5.5", "38b9b66d-5342-4caa-97f3-37c3a0731882"),
    ("gpt", "gpt-6.1-sol", "54a998a9-f1f9-4eba-a126-85dc39357dd0"),
]:
    prompt = f"""You are original {model}, same session {session}.
SAME053 bounded ORIGINAL-session dependent visual confirmation, NOT a repeated blind initial.
Frozen signed HEAD {head}; teaching unchanged from original reviewed3e37ebdac9af2880ceaa810ca34a7588d8c1d602 and native envelope93c55a2c17bd61123e2a5bacf1ff47a5c2ad48cf. Actual teaching diff is EMPTY. Only uncommitted contributor evidence copies/new prompts exist; no teaching/runtime/production changes.
Use ONLY SERIAL view calls: exactly ONE tool call per response, await completion. NEVER parallelize even text reads.
Read this task and YOUR COMPLETE original report, not the other reviewer's:
{reviews / f"batch-053-initial-{label}.md"}
Read complete current teaching in three separate calls:
{r / "kanji" / "丙.md"}
{r / "words" / "丙.md"}
{r / "words" / "丙午.md"}
Read unchanged disposable native fixture ranges210-320 and321-380 separately:
{native / "N1Batch053NativeTest.kt"}
Actually view EACH of these21distinct accepted attempt1 PNG viewports singly, ONE PER RESPONSE:
""" + "\n".join(x["path"] for x in scope) + """
These are21distinct views from35PNGs;14other captures hash-identical, NOT extra independent reads. Names do not establish which text is visible; inspect actual pixels and do not certify hidden columns.
Check 丙内肉病 readability/distinction in four production font rows;16Paintprobes/four distinct rasterstyles percharacter supplied. No authored冂/no new fallback-face claim.
Check five strokes/canonical radical一1/modern topbar+内-like mnemonic explicitlyNOTetymology/historicalexplanationsdiffer. Fullヘイ/ひのえ/bothcurated normalizedへい/ひのえ; rankclass versus quantitythree and contextualbelowstandard. Tenstems/twelvebranches/sixtyorderedcycle, thirdstem/seventhbranch, 丙午term43/1906-1966-2026/alternateへいご/historicaldateconversionlimits/no personalpredictions.
Check visible whole learner task, actual meaning alternatives/feedback and bothon+kun questions/feedback, trace/feedback/recallmiss, reciprocaltwo supportpairs/fourroutes/SystemBack/丙午->existing午route. Existing午unchanged/notfreshteachingcertification.
Supplied operational results, NOT tests run by reviewer: unchanged fixture firstactual nativeattempt two terminalcase0/no skips92.792s/adbexit0; exactfullGit envelope through productionContentSyncONCE1065kanji5023words85N1/problems0/parserEpoch1/schema1en-ja/ba2d74eac9ea12e1/fullヘイひのえ/bothnormalizedkeys. Synthetic disposable source1meaningdue/2readingdue/1newdrawing; otherN1postponed/twohistoricalmeaninglogs unlockdrawing/noDrawstateseeded/notownerprogress. Meaningcorrectfeedback NOTpersistedbeforeBack; both readinggrade3 logs asserted in ONEsession/nofixedshuffle (actualkun thenon), other legitimatekind excluded from wrongchoices. Fivegeneratedreference-touchstrokes/ungradedtraceWellDrawn/recallI don't remember/persistedDrawgrade onNext/offline reciprocalBack. ActualAPI35owned5580read-onlyhostGPU/Vulkan-disabledhelper stopped/exacttempsremoved/Androidclean/unowned5556untouched.192m576mguestappheapsunchanged/no nativeHOSTinit. Fresh292Android3+1/source-copyXMLhashes reverified, NOTrerun. Original049512MiBHOSTTestOOM/existing1GiB :core HOSTTest-onlyheadroom retained, NOTguestapp/nativeauthorization.
Original294device-port discovery denied once beforeexecution; parent EXACTcommand approved/passed and freshallconnectionsguard immediatelybeforeownedhelper; denial retained/not workaround.
Visual limits: initialtable rightedgeclipped/offsetreading leftcolumnclipped; boundedviewports NOTfullarticle/allcolumns. Trace firstuse downloadingmodelmessage; subsequentfeedback handwritingmodelunavailable/geometric-only. Touchreference/trace/recallMISS/persistedlogs do NOTprove MLKitrecognition/realhuman successfulrecall/negativegeometry/reverseorder/physicalphone/generalrelease/whole-setacceptance. Source1080x2400 mayreturnresized900x2000; do NOTclaim exactoriginalbytes/dimensions without evidence.
Initials actual56/58calls32resources each; ClaudeTWOinternaloverlaps/oversizedjlptreadrejectedthenassigned1-32recovered; GPTzerooverlaps/failures and selfcountninecomparisonwords versus ACTUALeight corrected inledger. Alloriginalreports retained. No teachingdefect/consequentialunresolvedclaim initially; fourClaudeoptionalgroupsnotadopted. This supplied-evidence dependent visualfollowup is not blind, freshsource retrieval/native-speaker certification/modelbenchmark or reviewer-executedtests.
Return complete Snapshot/Scope/Verdicts(each article correctness/scopedcoverage/comprehensibility)/Findings/Optional/Limits. Enumerate actualPNGreads/textranges and processdeviations honestly. No findingquota. Distinguish inherited textualjudgments from newlyvisible screenshots and supplied operational evidence. No edits/shell/delegation/search/retries/tools beyondview. Physicalphone/generalrelease/currentmain/publication/whole-set remainunperformed. Return FINALREPORT, nottask_complete. ONE toolcall perresponse.
"""
    target = c / f"batch-053-visual-{label}-prompt.txt"
    assert not target.exists()
    target.write_text(prompt, encoding="utf-8")
print("Verified exact native/Android/frozen evidence; archived39artifacts; prepared21distinct-view original-session prompts. No test rerun.")
