"""Bounded batch090 combined acceptance; runner.lock belongs to the live parent."""
import ast
import copy
import gzip
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
L = C / "logs" / "e13bc447-6efd-4a7d-b640-0e5dadd40fd1"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-090-combined-acceptance-643"
HEAD = "3f1530421f967983dc1a588b23c6b8ca88436d8f"
MAIN = "ebfd48dc911f32be0eeb9426db2f2d35a9084044"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "ceee0f79a6d394df"
STAGE = "batch-090-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME090 normal signed owner fast-forward publication and exact public acceptance next; NO091. "
    "Read docs/n1-sources/execution-643.json and docs/n1-reviews/batch-090-combined-acceptance-643. "
    "Fresh origin/main ebfd48dc already ancestor of reviewed3f153042; normal nonrewriting merge "
    "Already up to date; no substantive teaching/runtime change. Fresh fullPython/validator/"
    "vocabulary consistency/manifestfreshness/budget/source/fullbaseline/exactmembership/all3readings/"
    "5allmappedpairs10directions/1directguard/pinned2strokes/18Hanfontprovenance and actual sibling "
    "RealContentTest3+RareHanTest1 zero skips required and recorded in643. 8429runtimehashes/"
    "versionceee0f79a6d394df;1113kanji5069words122N1labels127namedmembers. Original638 blind "
    "ClaudeOpus5.5/GPT6.1Sol,641native bothterminalcase0 and642 original-session dependentvisuals "
    "reverified NOT rerun. Original read/provenance limits preserved; Claude used compacted same-session "
    "notes for first4visualsheets, not equal fresh-read claim. Fullarchive40bc5a55 productionContentSync"
    "ONCE/zeroProblems/Roomepoch1; exactly onとう/kunかたな Good/done; rawトウ/かたな/そり retained "
    "in full/Lite sourceorder; sourceonlyそり excluded without invented jukujikunrazor allocation. "
    "Actual N1/All options 刀sword;blade versus乃thereupon;possessiveno/凹concave;sunken/"
    "凸convex;protruding all3available/zerofallback; not futurecustompool certification. "
    "Bothnewarticles plus ONLYfourchangedreusedpassages/5pairs10directions/1direct日本刀-刀guard/"
    "SystemBack/offline/2injectedstrokes/trace-recallgiveup, NOT humanhandwriting/MLKit/phone. "
    "All18Han/fourComposefonts including刀versus力 visible; fallbackfaceunknown;76Painthashprobes "
    "NOT separatelyviewedPNGs; contact sheets downscaled. TraditionalJapaneseSwordnoun, neutralmuseum/"
    "photosentences, lexical日本modifier+sword, bothにほんとう/にっぽんとう withoutfrequencyranking/"
    "universalsoundchange/shape rule. Existing刀N3/剃刀N2/鋭いguard preserved. TESTONLYAndroid1c1b7bf4 "
    "retains unchangedproductionf9b59a2, NOTlatestappmain. Beforepush fetchfreshmain; ifadvanced "
    "normallymerge/reconcile/regenerate/revalidate and independentlyreview substantive teaching. "
    "Normalsigning/ownerstop-cran processscopedtoken/normalfastforward only; noamend/forcepush/"
    "globalauthswitch. Verify exactremoteSHA/terminalgreen relevantCI/EVERYruntimeentryhash and "
    "manifestequality in EXACTimmutableGitHubZIP/original18000entries42MiBcompressed80MiBinflated"
    "56MiBretained/perfile-media-safepathguards. Persist authored/reviewed/integrated/publishedSHAs/"
    "ledgers/counts/verifiedownerissue60 BEFORE091. Published116/1228,1112remaining/latestpublic"
    "ebfd48dc unchanged until verifieddelivery. Physicalphone/generalrelease/whole-set outstanding; "
    "projectincomplete. Keep original source/review/process/denial/OOM/readdepth/downscale/pool/font/"
    "phone limits and optionaldispositions. Parent19008 ownsrunner.lock; verify liveancestry/"
    "decodedlauncher/currentrunnersession/checkpoint/exactsignedheads/whollycleanworktrees; "
    "NEVERchildacquire/delete/unlock. Approvedcontrol/committedsources/frozenworkspaceinputs only, "
    "no optionalhistoricalsessionhelpers. Preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. No091/newnative/reviewer absent new concern, productionappchange, "
    "heap/guardincrease or unreviewedpush."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".643.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == value
    tmp.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain=v1", "--untracked-files=all", root=root)


def context():
    assert not os.environ.get("GH_TOKEN")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["status"], runner["sessionId"]) == (19008, "running", L.name)
    script = r"""
$ids=@();$p=$PID;$owned=$false
while($p -gt 0){
    $r=Get-CimInstance Win32_Process -Filter "ProcessId=$p"
    if(-not $r){break}
    $ids+=$r.ProcessId
    if($r.ProcessId -eq 19008){
        $command=$r.CommandLine
        if($command -match '-EncodedCommand ([A-Za-z0-9+/=]+)'){
            $command=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($Matches[1]))
        }
        $owned=$command.Contains('C:\Users\stop-\n1-kanji-workspace\control\runner.ps1')
        break
    }
    $p=$r.ParentProcessId
}
@{ids=$ids;owned=$owned}|ConvertTo-Json
"""
    ancestry = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert ancestry["owned"] and 19008 in ancestry["ids"], ancestry
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    return ancestry


def start():
    ancestry = context()
    clean(R, HEAD)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (
        642, "090", "continue", "visual-review-closed-awaiting-combined-acceptance")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["execution642CoordinatorCheckpoint"]["checkpoint"] == 642
    assert not (L / "progress-before-643.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-643.json")
    state = {
        "execution": 643, "batch": "090", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME090 current-main integration and combined acceptance, signed LOCAL evidence only; no publication/091 or new native/reviewer absent changed teaching/new concern.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded; operative contract, complete issue and final642 directly inspected. Historical middle parsed, not freshly semantically re-reviewed. Initial full remaining-output request exceeded tool output limit; exact final checkpoint read separately."},
        "runnerLockRole": "Live parent19008 ancestry, decoded runner.ps1 command and current runner session verified; no child lock acquisition/delete/unlock.",
        "ancestry": ancestry,
        "artifactPathPreflight": "Approved control helpers, frozen workspace inputs and committed source/review evidence only; no optional historical-session artifact accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-643.json", state)
    p["execution643StartingState"] = state
    p.update(stage="batch-090-combined-main-integration-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-643.json")
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    print("Starting scope persisted with full history; parent lock untouched.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    context()
    clean(R, HEAD)
    assert git("merge-base", MAIN, HEAD) == MAIN
    result = batch_audit(R, "090")
    ledger, prior = load(S / "batch-090-progress.json"), load(S / "batch-090-draft-audit.json")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(gzip.decompress(jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    packets = []
    for packet in ledger["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        expected = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / packet["xml"]).read_bytes()
        packets.append({"path": packet["xml"], "families": len(ids),
                        "freshFrozenExtractionMatches": True, "sha256": sha(S / packet["xml"])})
    assert sum(p["families"] for p in packets) == 207
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    occurrences = 0
    for name in ["batch-090-kanjidic2.xml", "batch-090-comparison-kanjidic2.xml"]:
        for row in ET.parse(S / name).getroot().findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            occurrences += 1
    assert occurrences == 8
    baseline = load(S / "baseline-inventory.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in prior["baselineMetadataExceptions"]:
                expected["quiz_exclusions"] = prior["baselineMetadataExceptions"][name]
            if name in prior["baselineKanjiDistractorException"]:
                expected["distractors"] = prior["baselineKanjiDistractorException"][name]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and len(named) == 1232
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    chars = {path.stem for path in (R / "kanji").glob("*.md")}
    separate, nonmembers = set("保案派第策結"), set("坊的誰身阪")
    assert len(published) == 116 and chars - old == published | separate | nonmembers | {"刀"}
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in separate)
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    actual_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
        "namedSourceMembersPresent": len(chars & set(named)),
    }
    assert actual_counts == {"kanji": 1113, "words": 5069, "n1Labels": 122,
                             "namedSourceMembersPresent": 127}
    assert {f"words/{p.name}" for p in (R / "words").glob("*.md")
            if "刀" in metadata(R, f"words/{p.name}")["kanji"]} == {
                "words/刀.md", "words/剃刀.md", "words/日本刀.md"}
    assert "jlpt" not in metadata(R, "words/日本刀.md")
    assert metadata(R, "words/刀.md")["jlpt"] == 3
    assert metadata(R, "words/剃刀.md")["jlpt"] == 2
    assert "鋭い" in metadata(R, "words/剃刀.md")["quiz_exclusions"]
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"]
                 if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert len(all_pairs) == 5
    for char, word in all_pairs:
        assert f"(../{word})" in (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
        assert f"(../kanji/{char}.md)" in (R / word).read_text(encoding="utf-8")
    guards = {tuple(sorted((row["word"], other)))
              for row in ledger["wordQuizAudit"]["directExclusions"] for other in row["exclude"]}
    assert guards == {tuple(sorted(("日本刀", "刀")))}
    for c in ["力", "切"]:
        row = metadata(R, f"kanji/{c}.md")
        assert len(row["distractors"]) == 3 and "刀" not in row["distractors"]
    assert not [c for c in chars if c != "刀"
                and "刀" in metadata(R, f"kanji/{c}.md").get("distractors", [])]
    stroke = load(S / "batch-090-stroke-evidence.json")
    svg = (S / "batch-090-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "刀.json") == convert("刀", svg.decode("utf-8"))
    assert stroke["dictionaryStrokeCount"] == stroke["sourceStrokePaths"] == 2
    font = load(S / "batch-090-draft-font-audit.json")
    text = "".join((R / n).read_text(encoding="utf-8") for n in font["completeNewArticleScope"])
    text += "".join(row["after"] for row in ledger["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert han == font["actualHan"] and len(han) == 18
    for row in font["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path) == row["sha256"]
        with TTFont(path) as face:
            cmap = face.getBestCmap()
        assert {c: ord(c) in cmap for c in han} == row["actualPresence"]
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json") and manifest["contentVersion"] == VERSION
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8429
    result.update(
        execution=643, latestMain=MAIN, preIntegrationHead=HEAD, upstreamAlreadyAncestor=True,
        runtimeHashesVerified=checked, frozenInputsVerified=len(snapshot["inputs"]),
        decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterOccurrencesVerified=occurrences,
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=prior["baselineMetadataExceptions"],
        baselineKanjiDistractorException=prior["baselineKanjiDistractorException"],
        exactMembershipAccounted=True, currentCounts=actual_counts,
        publishedIssue60Additions=116, acceptedUnpublishedIssue60Additions=["刀"],
        separateEarlierLevelSourceMembers=sorted(separate), separateNonmemberAdditions=sorted(nonmembers),
        remainingIssue60Acceptance=1112, sixEarlierPlacementsCountedAsIssue60Accepted=False,
        requiredAllMappedPairs=5, directedLinksVerified=10, directWordExclusionPairs=1,
        pinnedStrokeGeometryExactlyRegenerated=True, scopedHan=han, fontProvenanceReverified=True,
        runtimePublished=False,
        limits="Mechanical source/baseline/link/reading/hash/font provenance audit, not fresh linguistic/native review. Original reviewer/native limitations retained.",
    )
    save(L / "combined-source-audit-643.json", result)
    print("Combined source audit passed; all8429 runtime hashes and exact membership verified.")


def checks():
    context()
    clean(R, HEAD)
    for name, args in [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]:
        command = [sys.executable, "-X", "utf8", "-B", *args]
        with (L / f"{name}-643.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-643.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-090-reconciliation.json")
    visual = load(V / "batch-090-visual-reconciliation-642.json")
    assert text["textualReviewClosed"] and text["findings"] == []
    assert text["actionableRemainingTeachingFindings"] == 0
    assert text["consequentialUnresolvedTeachingFindings"] == 0
    assert visual["findings"] == [] and visual["serialReviewerProcessesExited"]
    assert visual["eachReviewerImagesDecoded"] == 14 and visual["allToolViewsSerial"]
    for name, expected in text["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    for records, is_visual in [(text["processes"], False), (visual["processes"], True)]:
        previous = None
        for label, process in records.items():
            assert process["actualModels"] == [
                "claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
            assert process["exitCode"] == 0 and not process["observedToolOverlaps"]
            if is_visual:
                assert process["allAssignedResourcesSuccessfullyReturned"]
                assert process["sessionId"] == text["processes"][label]["sessionId"]
                assert not process["unfinishedTools"] and not process["missingResources"]
                assert len(process["toolCalls"]) == 16
                prefix = V / f"batch-090-visual-642-{label}"
                assert sha(prefix.with_suffix(".md")) == process["reportSha256"]
                assert hashlib.sha256(gzip.decompress(
                    prefix.with_suffix(".jsonl.gz").read_bytes())).hexdigest() == process["rawSha256"]
            else:
                assert process["allAssignedRangesReturned"]
                assert sha(V / process["report"]) == process["reportSha256"]
                assert sha(V / f"batch-090-initial-{label}.jsonl") == process["rawExecutionSha256"]
            if previous is not None:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
            previous = process["completedAt"]
    receipts_verified = 0
    for number in [641, 642]:
        for row in load(S / f"execution-{number}.json")["receipts"]:
            path = R / row["archive"]
            assert sha(path) == row["archiveSha256"], path
            data = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
            assert hashlib.sha256(data).hexdigest() == row["sourceSha256"], path
            receipts_verified += 1
    native = load(S / "execution-641.json")
    execution = native["executionReceipt"]
    assert execution["passed"] and execution["terminalSuccessCases"] == 2
    assert execution["ownedHelperStopped"] and execution["ownedQemuStopped"]
    route = native["nativeRoute"]
    assert {k: route[k] for k in ["archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems"]} == {
        "archiveRequests": 1, "importedKanji": 1113, "importedWords": 5069, "n1Cards": 122, "problems": 0}
    assert route["contentVersion"] == VERSION and route["acceptedReadingParserEpoch"] == 1
    for field in ["fullOnyomi", "fullProjectionOnyomi", "fullProjectionQuizOnyomi", "liteQuizOnyomi"]:
        assert route[field] == ["トウ"]
    assert route["fullKunyomi"] == route["fullProjectionKunyomi"] == ["かたな", "そり"]
    assert route["liteQuizKunyomi"] == route["fullProjectionQuizKunyomi"] == ["かたな"]
    assert route["quizOnKeys"] == ["とう"] and route["quizKunKeys"] == ["かたな"]
    assert route["bothCuratedKindsPersistedGoodAndDone"]
    assert route["touchInjectedReferenceStrokes"] == 2 and route["completeArticleProjections"] == 2
    assert route["mappedReciprocalPairs"] == 5 and route["directedLinkTransitions"] == 10
    assert route["directWordGuardCount"] == 1 and route["changedReusedArticles"] == 4
    assert route["offline"] and route["reciprocalLinkAndSystemBack"]
    for pool in ["N1", "All"]:
        choices = route["productionBuilderN1AndAllExactChoices"][pool]
        assert choices["availableCuratedCount"] == 3 and choices["fallbackOptions"] == 0
        assert {o["kanji"] for o in choices["options"]} == set("刀乃凸凹")
    for snapshot in [text["reviewedTeachingSnapshot"], route["contentSnapshot"]]:
        assert not git("diff", snapshot, HEAD, "--",
                       "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", PRODUCTION, APP, "--", "core/src/main", "app/src/main",
                   "gradle.properties", root=A)
    return {
        "initialReviewReports": text["processes"], "nativeTerminalCaseStatuses": [0, 0],
        "archiveReceiptsReverified": receipts_verified, "newNativeOrReviewerRuns": 0,
        "nativeRuntimeMatchesCurrentCombinedTree": True, "nativeRoute": route,
        "nativeEvidence": "docs/n1-sources/execution-641.json",
        "visualEvidence": "docs/n1-reviews/batch-090-visual-reconciliation-642.json",
        "inheritedSourceTextLimits": text["limits"], "inheritedVisualLimits": visual["limits"],
        "visualDispositions": visual["dispositions"],
        "rerunDisposition": "Current main already included; teaching/runtime/app production/font bytes unchanged. Existing native and original dependent visuals remain applicable; no new concern established.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-643.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-643.txt").read_text().strip() == "0 error(s)"
    assert VERSION in (L / "manifest-643.txt").read_text()
    vocabulary = (L / "vocabulary-643.txt").read_text().strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-643.json")["exitCode"] == 0
    assert (L / "host-exit-643.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-643.txt").read_text(encoding="utf-8-sig")
    started = datetime.fromisoformat((L / "host-start-643.txt").read_text().strip())
    ended = datetime.fromisoformat((L / "host-end-643.txt").read_text().strip())
    suites = []
    for relative, names in [
        ("core\\build\\test-results\\test\\TEST-io.github.stopcran.kanji.core.RealContentTest.xml",
         {"parsesRealContentRepoWhenPresent", "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
          "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent"}),
        ("app\\build\\test-results\\testDebugUnitTest\\TEST-io.github.stopcran.kanji.core.RareHanTest.xml",
         {"contentRareCharactersAreCoveredByBundledFont"}),
    ]:
        path = A / relative
        xml = ET.parse(path).getroot()
        assert xml.attrib["tests"] == str(len(names))
        assert all(xml.attrib[k] == "0" for k in ["skipped", "errors", "failures"])
        assert {x.attrib["name"] for x in xml.findall("testcase")} == names
        assert not any(xml.findall(".//" + name) for name in ["skipped", "failure", "error"])
        stamp = datetime.fromisoformat(xml.attrib["timestamp"]).astimezone(timezone.utc)
        assert started <= stamp <= ended and path.stat().st_mtime >= started.timestamp()
        suites.append({"path": str(path), "sha256": sha(path), "suite": xml.attrib,
                       "cases": [x.attrib for x in xml.findall("testcase")]})
    assert all((A / module / ".." / ".." / "learning-japanese").resolve() == R for module in ["app", "core"])
    source, inheritance = load(L / "combined-source-audit-643.json"), inherited()
    budget = ast.literal_eval((L / "budget-643.txt").read_text())
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    assert not D.exists()
    D.mkdir()
    receipts = []
    paths = [
        *(L / name for name in ["starting-state-643.json", "combined-source-audit-643.json", "merge-643.txt",
          "python-tests-643.txt", "validate-643.txt", "manifest-643.txt", "vocabulary-643.txt", "budget-643.txt",
          "host-643.txt", "host-exit-643.txt", "host-command-643.json", "host-start-643.txt", "host-end-643.txt",
          "runner-ancestry-643.json"]),
        *(L / f"{name}-exit-643.json" for name in ["python-tests", "validate", "manifest", "vocabulary", "budget"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-090-combined-host-643.ps1",
        C / "post-batch-090-combined-643.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
        A / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "RealContentTest.kt",
        A / "core" / "src" / "test" / "kotlin" / "io" / "github" / "stopcran" / "kanji" / "core" / "PublishableContentFixture.kt",
        A / "app" / "src" / "test" / "java" / "io" / "github" / "stopcran" / "kanji" / "core" / "RareHanTest.kt",
    ]
    for path in paths:
        target = D / (path.name + ".gz" if path.suffix == ".txt" else path.name)
        assert not target.exists(), target
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "sha256": sha(target),
                         "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 643, "batch": "090", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-643.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "normalMerge": True,
        "upstreamAlreadyAncestor": True, "mergeResult": "Already up to date.", "newMergeCommit": False,
        "conflicts": [], "substantiveTeachingConflictEdits": [], "batchTeachingUnchanged": True,
        "runtimeBytesUnchanged": True, "sourceAudit": source, "pythonTestsPassed": int(match[1]),
        "validatorErrors": 0, "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary,
        "manifestFresh": True, "contentVersion": VERSION, "localBudget": budget, "hostSuites": suites,
        "hostChecksFresh": True, "hostTestsExecuted": 4, "androidHead": APP,
        "productionAndroidBytesUnchanged": True, "inheritedAcceptance": inheritance, "receipts": receipts,
        "runtimeAccepted": True, "runtimePublished": False, "publishedAdditions": 116,
        "remainingAdditions": 1112, "lastPublishedCommit": MAIN, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Local combined-tree acceptance only, not publication or fresh linguistic/native review. Existing vocabulary pilot2122/2431 is consistency, not full coverage. Original source/process/read-depth/denial/OOM/downscale/pool/font/MLKit/phone limitations and optional dispositions preserved. Physical phone/general release/whole set outstanding.",
    }
    save(S / "execution-643.json", evidence)
    path = S / "batch-090-progress.json"
    ledger = load(path)
    ledger["preCombined643State"] = {
        k: ledger.get(k) for k in ["status", "nextAction", "reviewClosed", "runtimeAccepted", "runtimePublished"]}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True,
                  runtimePublished=False, combinedAcceptance="docs/n1-sources/execution-643.json", nextAction=NEXT)
    save(path, ledger)
    body = (
        "**Batch090 checkpoint643: combined current-main acceptance passed locally; publication next.** "
        f"Fresh main `{MAIN}` is already an ancestor of reviewed `{HEAD}`; normal non-rewriting merge "
        "returned 'Already up to date'. No conflict, artificial merge or teaching/runtime edit.\n\n"
        f"Fresh {match[1]} Python tests, validator0errors, vocabulary consistency (`{vocabulary}`), "
        "regenerated manifest/all8429runtimehashes/version`ceee0f79a6d394df`, frozen inputs/decompressed"
        "dictionary hashes/207completelexicalfamilies/8rawcharacters, original985kanji4942words985strokes "
        "with recorded exceptions, exactmembership/all3rawreadings/2curatedkeys, fiveallmappedpairs/"
        "tendirections/onedirect日本刀-刀guard, regenerated pinnedtwostrokes and18Han/fontprovenance "
        "passed. Actual1113kanji5069words122N1labels127namedmembers. Fresh actual-sibling RealContentTest3+"
        "RareHanTest1 passed, zero skips/errors/failures; explicitJDK17/SDK/oneworker/in-processKotlin/"
        "existingapproved2GiBHOSTinit. TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, notlatestappmain; "
        "no app/guestheap change.\n\n"
        "Original638 blind ClaudeOpus5.5/GPT6.1Sol and642 dependent original-session visuals reverified, "
        "NOT rerun; Claude compacted same-session notes for first4visualsheets retained. Native641 "
        "bothterminalcase0/fullarchive40bc5a55 productionContentSyncONCE/zeroProblems/acceptedepoch1 "
        "unchanged. Exactly onとう/kunかたな Good/done; rawトウ/かたな/そり retained in sourceorder/"
        "full-Lite; sourceonlyそり not inferred fromjukujikunrazor. ActualN1/All options sword;blade "
        "versus乃/凹/凸/all3curatedavailable/zerofallback, notfuturecustompool certification. Botharticles "
        "and ONLYfourchangedreusedpassages/SystemBack/offline/twoinjectedstrokes/trace-recallgiveup. "
        "All18Han/fourComposefonts including刀versus力 visible; contact sheets downscaled, fallbackface"
        "unidentified,76Painthashes NOT76viewedPNGs. Not humanhandwriting/MLKit/phone. TraditionalJapanese"
        "Swordnoun, neutralmuseum/photosentences, lexical日本modifier+sword, bothにほんとう/にっぽんとう "
        "withoutfrequencyranking/universalsoundchange/shape rule. Existing刀N3/剃刀N2/鋭いguard preserved. "
        "Original limitations retained.\n\n"
        f"Local budget: {budget['entries']:,}entries/{budget['retainedBytes']:,}retained/"
        f"{budget['inflatedBytes']:,}inflated/{budget['localZipBytes']:,}compressed bytes. "
        "Original18000entries/42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath guards "
        "unchanged. Evidence:`docs/n1-sources/execution-643.json` and "
        "`docs/n1-reviews/batch-090-combined-acceptance-643`.\n\n"
        "**Next bounded checkpoint: freshmain recheck, normal signed owner fast-forward publication, "
        "exactremoteSHA/terminalgreenCI/EVERYimmutablepublicZIP runtimehash and originalbudgets, durable"
        "publication and verifiedownerissue receipt BEFORE091.** No push/091 here. Published116/1228, "
        "1112remaining unchanged. Compatiblef9b59a2+ required; physicalphone/generalrelease/whole-set "
        "outstanding; projectincomplete. Liveparent19008 ancestry/session/decodedlauncher verified; "
        "runner.lock untouched. No optionalhistoricalsessionhelper or actualnewpermissiondenial.\n"
    )
    (L / "issue-body-643.txt").write_text(body, encoding="utf-8", newline="\n")
    print("Combined acceptance and lossless evidence archived; ready for signed LOCAL checkpoint.")


def finish():
    context()
    saved = git("rev-parse", "HEAD")
    clean(R, saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    evidence = load(S / "execution-643.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["sha256"]
        raw = (R / row["archive"]).read_bytes()
        if row["losslessGzip"]:
            raw = gzip.decompress(raw)
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
    receipt = load(L / "issue-verified-643.json")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"] == (L / "issue-body-643.txt").read_bytes().decode("utf-8")
    before, p = load(L / "progress-before-643.json"), load(C / "progress.json")
    assert p["checkpoint"] == 642 and p["batch"] == "090"
    row = {
        "schemaVersion": 1, "execution": 643, "checkpoint": 643, "batch": "090",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-643.json", "evidenceSha256": sha(S / "execution-643.json"),
        "combinedContentHead": HEAD, "latestMainIntegrated": MAIN, "upstreamAlreadyAncestor": True,
        "runtimeHashesVerified": 8429, "contentVersion": VERSION,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "freshHostTestsPassed": 4, "hostSkips": 0,
        "runtimeAccepted": True, "runtimePublished": False, "runtimeBytesUnchanged": True,
        "newNativeOrReviewerRuns": 0, "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 116, "remainingAdditions": 1112, "lastPublishedCommit": MAIN,
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "issueUpdate": receipt["html_url"], "ownerIssueAuthorAndBodyVerified": True,
        "issueReceiptSha256": sha(L / "issue-verified-643.json"), "nextAction": NEXT, "blocker": None,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p.update(checkpoint=643, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution643CoordinatorCheckpoint"] = row
    p["batch090CombinedAcceptanceCheckpoint"] = row
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    save(L / "checkpoint-verification-643.json", row)
    print(f"Checkpoint643 persisted at signed {saved}; full history preserved. SAME090 publication next; no091.")


if __name__ == "__main__":
    {"start": start, "audit": audit, "checks": checks, "record": record, "finish": finish}[sys.argv[1]]()
