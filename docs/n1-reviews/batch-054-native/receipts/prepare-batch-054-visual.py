import hashlib
import json
import struct
import subprocess
import zipfile
from datetime import datetime
from pathlib import Path

c = Path(__file__).resolve().parent
r = c.parent / "learning-japanese"
reviews = r / "docs" / "n1-reviews"
native = reviews / "batch-054-native"
sources = r / "docs" / "n1-sources"
load = lambda p: json.loads(p.read_text(encoding="utf-8-sig"))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args, tree=r):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=tree, text=True, encoding="utf-8").strip()


head = "73593c32886b12443c6da65b9b6c2e393ba01ace"
assert git("rev-parse", "HEAD") == head and not git("status", "--porcelain")
assert git("log", "-1", "--format=%G?") == "G"
android = c.parent / "kanji-cards-android"
assert git("rev-parse", "HEAD", tree=android) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
assert not git("status", "--porcelain", tree=android)
p = load(c / "progress.json")
assert p["checkpoint"] == 303 and p["batch"] == "054"
assert "execution304StartingState" not in p
state = {
    "execution": 304, "batch": "054", "startingHead": head,
    "startedAt": datetime.now().astimezone().isoformat(),
    "scope": "SAME054 original Claude then GPT dependent native visual confirmations and normally signed LOCAL evidence checkpoint only; no publication,055,accepted tests/blind initial reruns or second runner.",
    "status": "starting-original-visual-confirmations",
    "acquisition": "Complete authorized request through actual EOF12173/final303 checkpoint acquired before action;1-9290 inherited via compaction,9291-12173 currently returned and430-438 boundary recovered. BeyondEOF12291/12441 calls returned errors, not evidence. Complete approved issue inherited; applicable current repository/scoped instructions, dedicated clean signed heads and scoped live history inspected. Full live history preserved.",
}
p["execution304StartingState"] = state
save(c / "progress.json", p)
save(c / "execution-304-starting-progress.json", p)
n = load(sources / "execution-303.json")
prep = load(sources / "batch-054-native-preparation.json")
assert not git("diff", n["reviewedTeachingSnapshot"], "HEAD", "--",
               "kanji", "words", "articles", "strokes", "manifest.json")
for rel, expected in {**prep["originalFixtureHashesUnchanged"], **n["originalInitialReportHashesUnchanged"]}.items():
    assert sha(r / rel) == expected, rel
assert sha(native / "N1Batch054NativeTest.kt") == n["nativeExecution"]["fixtureSha256"]
assert sha(native / "artifact-index.json") == n["artifactIndexSha256"]
assert sha(native / "coordinator-observations.json") == n["coordinatorObservationsSha256"]
index = load(native / "artifact-index.json")
for section in ["sourceArtifacts", "returnedPayloads"]:
    if section in index:
        for row in index[section]:
            assert sha(r / row["path"]) == row["sha256"]
log = (native / "attempt-1" / "instrumentation.txt").read_text(encoding="utf-8")
assert log.count("INSTRUMENTATION_STATUS_CODE: 0") == 2
assert "OK (2 tests)" in log and "Time: 118.893" in log
assert "INSTRUMENTATION_STATUS_CODE: -2" not in log and "INSTRUMENTATION_STATUS_CODE: -3" not in log
assert sha(native / "attempt-1" / "instrumentation.txt") == n["rawLogSha256"]
route = load(native / "attempt-1" / "n1-054-article-route.json")
for key, value in {
    "archiveRequests": 1, "importedKanji": 1066, "importedWords": 5024,
    "problems": 0, "n1Cards": 86, "acceptedReadingParserEpoch": 1,
    "fullOnyomi": ["ショ", "ソ", "ショウ"], "fullKunyomi": ["か.つ"],
    "quizOnKeys": [], "quizKunKeys": ["かつ"], "contentVersion": "fa89fc674144b377",
    "passed": True, "offline": True,
}.items():
    assert route[key] == value, key
archive = c / "artifacts" / "n1-batch-054-b9575007-envelope.zip"
assert sha(archive) == n["nativeExecution"]["archiveSha256"]
assert sha(Path(n["nativeExecution"]["testApk"])) == n["nativeExecution"]["testApkSha256"]
m = load(r / "manifest.json")
with zipfile.ZipFile(archive) as z:
    manifests = [x for x in z.namelist() if x.endswith("/manifest.json")]
    assert len(manifests) == 1
    prefix = manifests[0][:-len("manifest.json")]
    assert z.read(manifests[0]) == (r / "manifest.json").read_bytes()
    files = {}
    for section in ["files", "images", "scenes", "listening", "audio", "curriculum",
                    "listeningTasks", "listeningTaskAudio", "listeningTaskImages"]:
        for rel, expected in m.get(section, {}).items():
            assert rel not in files
            files[rel] = expected
            frozen, current = z.read(prefix + rel), (r / rel).read_bytes()
            if section not in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}:
                frozen, current = frozen.replace(b"\r\n", b"\n"), current.replace(b"\r\n", b"\n")
            assert hashlib.sha256(frozen).hexdigest() == hashlib.sha256(current).hexdigest() == expected
    assert len(files) == 8290 and len(z.infolist()) == 8312
observations = load(native / "coordinator-observations.json")
scope = []
for step in observations["directlyViewedPngSteps"]:
    path = native / "attempt-1" / f"n1-054-{step}.png"
    assert struct.unpack(">II", path.read_bytes()[16:24]) == (1080, 2400)
    scope.append({"path": str(path), "sha256": sha(path)})
assert len(scope) == 18 and len({row["sha256"] for row in scope}) == 18
save(c / "batch-054-recovered-evidence-verification.json", {
    "execution": 304, "sameVisualScope": scope, "runtimeHashesVerified": 8290,
    "nativeTerminalCase0": 2, "nativeDurationSeconds": 118.893,
    "nativeRerun": False, "androidRerun": False, "originalFixturesUnchanged": 70,
    "originalInitialReportsUnchanged": 2,
    "limits": "Mechanical current/frozen payload and evidence verification, not fresh linguistic review or native run. Original303 direct18image provenance retained; current coordinator image reads recorded separately.",
})
for label, model, session in [
    ("claude", "claude-opus-5.5", "1bed2f69-6d63-4a81-91f7-05f664ff3030"),
    ("gpt", "gpt-6.1-sol", "572484bf-b4d8-4206-94b6-d046f9157dc7"),
]:
    prompt = f"""You are original {model}, same session {session}.
SAME054 bounded ORIGINAL-session dependent visual confirmation, NOT new blind initials.
Frozen signed HEAD {head}; teaching unchanged from original reviewed4fb51498f6912169499456031380ce2353373397. Exact compiled302fixture and full signedb957500752f3f62f5228706db9f1ea6d4a17d0ed envelope. Actual teaching diff EMPTY, verified by coordinator. Contributor evidence only may be uncommitted.
Use ONLY SERIAL view calls: exactly ONE tool call per response; await completion. NEVER parallelize even text reads.
Read this task and YOUR COMPLETE original report, not the other reviewer's:
{reviews / f"batch-054-initial-{label}.md"}
Read complete current teaching in two separate calls:
{r / "kanji" / "且.md"}
{r / "words" / "且つ.md"}
Read exact unchanged compiled native fixture ranges210-300 and301-380 separately:
{native / "N1Batch054NativeTest.kt"}
Actually view EACH of these18distinct accepted attempt1 PNG viewports singly, ONE PER RESPONSE:
""" + "\n".join(row["path"] for row in scope) + """
These are18distinct views from32sourcePNGs/14hash-identicaladditionalcaptures, NOT32independentreads. Inspect actual pixels, not names. Source1080x2400 mayreturnresized900x2000; report transport limits.
Check 且目日助苟 readability/distinction in four production font rows. Supplied20Paintprobes and four distinct rasterstyles for且目日助; 苟single sharedfallback style in allfour, faceunidentified. Cmapabsence NOTactualglyphfailure, nofourbundled苟claim.
Check five strokes/canonical一1/modernshape mnemonic NOTetymology; fullorderedショ/ソ/ショウ/か.つ with on[]kun[か.つ], selectedkunkeyかつ. ショrecognition-only archaic苟且こうしょ, source-onlyソ/ショウ, separatewholeword苟且かりそめ notindividualソallocation. One且つかつsupport/onepairtwodirections/ninedirectguards/noinferredwordlevel. Comparative register claim remains UNVERIFIEDandOMITTED, noformal-onlyban. Attestedlectureandconditionexamples/English/kana/i-adjectiveおもしろく/finalなin必要かつ十分な/noun; twoframesnotuniversalrule. Additive/parallel-actions/notunrestrictedEnglishnoun-listingand/substitutionboundaries.
Check complete visible learner tasks: actualmeaningwronglabels Japanese cedar/chicken/mosquito, NOTauthored目日助; curatedkunまつ/たつ/かえで/かつ, correctかつ and suppliedpersistedGood. Fulllookupmetadata showninfeedback NOTexcludedonpracticekeys. Fivegeneratedreference-touchstrokes/ungradedtrace/modelunavailable geometric-onlyfeedback/recallmiss/persistedDraw onNext; noMLKitrecognition orhuman successfulrecall/negativegeometry/reverseorder evidence.
Supplied operational results, NOT tests run by reviewer: unchanged302fixture native303attempt1 two terminalcase0/no skips118.893s/adbexit0; fullproductionContentSyncONCE1066kanji5024words86N1/problems0/parserEpoch1/schema1en-ja/fa89fc674144b377. Full ANDLite orderedreadings/curation assertionspassed. All8290current/frozenruntimehashes/8312ZIPentries/originalbudgetsverified. Syntheticdisposablesource/otherN1postponed/twohistoricalmeaninglogs unlockdrawing/noDrawstateseeded/notownerprogress. Meaningfeedback NOTpersistedbeforeBack; readingGood/drawingNextpersisted asserted.
Offline onepair/twodirections/SystemBack/nativeAPI35defaultfontscale1. Requested2048MB auto2560MB/MemTotal2532900kB; actual192m576mguestappheapsunchanged. Owned5580helperPIDs21572/18312stopped; unowned5556untouched/Androidclean/no temporarysourceassets installed303. Original049HOST512MiBOOM/existing1GiB :core HOSTTest-onlyheadroom retained, NOTguest/nativeheapauthorization. Fresh301Android3+1 accepted/reverified, NOTrerun.
Visual limits: readings tablewiderthanviewport; oppositehorizontaloffsets clipleftlabels/rightqualification, archaicこうしょwrapsafterし/source-onlylabels partlyclipped. Bounded screenshots NOTeverycell/allcolumns/fullarticlecertification. Lecturebulletreachesrightedge. Tracefirstuse downloadingmodelmessage then explicitunavailable/geometric-only. No enlargedtext/otherAPI/physicalphone/generalrelease/whole-setacceptance.
Originalblindinitials actualClaude56calls/ONEinternaloverlap andGPT55calls/zero,32assignedresources each/no failedtruncatedreads. Originalreports and fiveClaudeoptional suggestions unchanged/unadopted. This supplied-evidence dependentfollowup is not blind, freshsource retrieval/native-speaker certification/modelbenchmark/reviewer-executedtests. Do not invent defectquota or overclaim unread tablecells.
Return complete Snapshot/Scope/Verdicts(each article correctness/scopedcoverage/comprehensibility)/Findings/Optional/Limits. Enumerate actualPNGreads/textranges/processdeviations honestly. Separate inheritedtextualjudgments/newlyvisiblepixels/suppliedoperationalresults. No edits/shell/delegation/search/retries/tools beyondview. Currentmain/publication/phone/generalrelease/whole-set remainunperformed. Return FINALREPORT, nottask_complete. ONE toolcall perresponse.
"""
    target = c / f"batch-054-visual-{label}-prompt.txt"
    assert not target.exists()
    target.write_text(prompt, encoding="utf-8")
print("Starting scope saved; exact8290runtime hashes/native evidence verified; original-session18view prompts prepared.")
