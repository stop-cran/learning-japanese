"""Verify the corrected batch's combined tree under the live parent launcher."""
import ast
import base64
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
L = C / "logs" / "3752d263-e4d2-4db8-b0a5-0b4f9fecb966"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-094-combined-acceptance-687"
HEAD = "bb11dc2809b401e253fc6e5c1fe278077040558f"
MAIN = "48765e20846e1d6769c6ddc35146f6ce58deab57"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PRODUCTION = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "74b7e886a1afbd46"
STAGE = "batch-094-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME094 only: normally signed owner fast-forward publication and exact public acceptance "
    "next; read docs/n1-sources/execution-687.json and "
    "docs/n1-reviews/batch-094-combined-reconciliation-687.json. Fresh origin/main48765e20 "
    "already ancestor of bb11dc28; normal merge Already up to date, no runtime/teaching "
    "change. Combined687 full Python/validator/vocabulary/regenerated manifest/budget/"
    "frozen sources/full baseline/membership/links/readings/strokes/font provenance/all8438 "
    "runtime hashes and fresh RealContentTHREE+RareHanONE zero skips passed. Original678 "
    "blind two-family textual reviews,679 corrections,682 native/font/85captures,683 "
    "original-session rendered confirmations with original Claude overlap REJECTED and "
    "serial repair preserved,685 original-session direct-pair confirmations and686 exact "
    "corrected import/128 builder checks inherited, NOT fresh review/native. All consequential "
    "in-scope findings resolved; optional suggestions and original read/visual/process "
    "limitations retained. Exact corrected native686 productionContentSync ONCE:1117kanji/"
    "5070words/126N1/zeroProblems/RoomreadingEpoch1/version74b7e886a1afbd46; terminalcase0 "
    "no skips. Qualified TESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "No physicalphone/humanhandwriting/successfulMLKit/full-pool semantic certification. "
    "Before publication recheck freshmain/exactsignedheads/whollyclean; if main advanced "
    "normal nonrewriting merge/reconcile/regenerate/revalidate ACTUAL combinedtree and "
    "independently review substantive teaching changes. Normal ownerstop-cran token ONLY "
    "publicationchild, no global auth switch; normal fastforward, exactremoteSHA, terminalgreen "
    "relevantCI, EVERY immutable publicGithubZIP runtimeentryhash/manifest equality/original "
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath guards, "
    "durable authored/reviewed/integrated/publishedSHAs and verifiedownerissue before095. "
    "Local GitZIP/native686 is NOT publicGithubZIP acceptance. No forcepush/amend/signing"
    "bypass/heapguardincrease/productionappchange/redundantnative/reviewer/095/secondrunner. "
    "Parent19008 ownsrunner.lock: verify liveancestry/decodedlauncher/session/checkpoint/"
    "signedheads/whollyclean; NEVERchildacquire/delete/unlock. Approvedcontrol/committed "
    "sources/frozenworkspaceinputs only, no optional historicalsessionhelpers. Preserve/"
    "report/yield actualnewdenial/signinghang/uncertainownership. Published120/1228 and1108 "
    "remaining unchanged pending delivery; compatibleAndroidf9b59a2+ required; physicalphone/"
    "generalrelease/whole-set outstanding, projectincomplete."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(path.suffix + ".687.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    temp.replace(path)


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
    script = f"""
$id={os.getpid()};$chain=@()
while($id -gt 0 -and $chain.Count -lt 12){{
 $p=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(!$p){{break}}
 $chain+=@{{pid=[int]$p.ProcessId;parent=[int]$p.ParentProcessId;name=$p.Name;command=$p.CommandLine}}
 if($id -eq 19008){{break}}
 $id=$p.ParentProcessId
}}
$chain|ConvertTo-Json -Depth 4 -Compress
"""
    chain = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", script], encoding="utf-8"))
    assert chain[-1]["pid"] == 19008
    assert any(p["name"].lower() == "copilot.exe" and L.name in p["command"] for p in chain)
    encoded = chain[-1]["command"].split("-EncodedCommand ", 1)[1].split()[0]
    assert str(C / "runner.ps1") in base64.b64decode(encoded).decode("utf-16-le")
    launcher = (C / "runner.ps1").read_text(encoding="utf-8-sig")
    assert "$lock.Dispose()" in launcher
    assert "'runner.lock'), 'OpenOrCreate', 'ReadWrite', 'None'" in launcher
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    progress = load(C / "progress.json")
    assert (progress["checkpoint"], progress["batch"], progress["status"]) == (686, "094", "continue")
    return {
        "parentPid": 19008, "session": L.name, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
    }


def start():
    role = context()
    clean(R, HEAD)
    assert not (L / "progress-before-687.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-687.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution686CoordinatorCheckpoint"] == p["execution686CoordinatorCheckpoint"]
    state = {
        "execution": 687, "batch": "094", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME094 combined-current-main acceptance and normally signed LOCAL evidence only; publication next, no095/newnative/reviewer.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete issue and final686 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role, "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed evidence/frozen inputs only; no optional historical-session helpers.",
    }
    save(L / "starting-state-687.json", state)
    p["execution687StartingState"] = state
    p.update(stage="batch-094-combined-main-acceptance-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-687.json")
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    assert git("merge-base", MAIN, HEAD) == MAIN
    result = subprocess.run(["git", "--no-pager", "-C", str(R), "merge", "--no-edit", "origin/main"],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (L / "merge-687.txt").write_bytes(result.stdout)
    assert result.returncode == 0
    clean(R, HEAD)
    print("Combined acceptance started; current main already integrated, full history preserved.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    context()
    clean(R, HEAD)
    result = batch_audit(R, "094")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(gzip.decompress(jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    ledger = load(S / "batch-094-progress.json")
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    packets = []
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        expected = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt.gz" if i == 0 else "comparison-full-family-reading.txt.gz"
        compact = gzip.decompress((S / f"batch-094-{suffix}").read_bytes())
        assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact.decode("utf-8") + "</JMdict>")] == [
            canonical(e) for e in ET.fromstring(expected)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(S / packet["xml"]),
                        "freshFrozenExtractionMatches": True, "completeCompactSemanticEquality": True})
    assert sum(p["families"] for p in packets) == 125
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    count = 0
    for name in ["batch-094-kanjidic2.xml", "batch-094-comparison-kanjidic2.xml"]:
        for row in ET.parse(S / name).getroot().findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            count += 1
    assert count == 10
    exceptions = copy.deepcopy(load(S / "batch-094-correction-audit-684.json")["baselineMetadataExceptions"])
    baseline = load(S / "baseline-inventory.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/\u5c71.md":
                expected["distractors"] = ["\u5ddd", "\u51fa", "\u6728"]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and len(named) == 1232
    chars = {p.stem for p in (R / "kanji").glob("*.md")}
    base_manifest = json.loads(git("show", f"{MAIN}:manifest.json"))
    old = {Path(n).stem for n in base_manifest["files"] if n.startswith("kanji/")}
    assert chars - old == {"\u524a"} and not old - chars
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    for c in "\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50":
        assert metadata(R, f"kanji/{c}.md")["jlpt"] == 2
    current_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
    }
    assert current_counts == {"kanji": 1117, "words": 5070, "n1Labels": 126}
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if "\u524a" in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/\u524a\u308b.md", "words/\u524a\u9664.md"}
    pairs = {(c, row["article"]) for row in ledger["supportMappings"]
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 3
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    stroke = load(S / "batch-094-stroke-evidence.json")
    svg = (S / "batch-094-kanjivg.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "\u524a.json") == convert("\u524a", svg.decode("utf-8"))
    font = load(S / "batch-094-draft-font-audit.json")
    text = "".join((R / n).read_text(encoding="utf-8") for n in font["completeArticleScope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert set(han) - set(font["actualHan"]) == {"\u7e2e"}
    assert not set(font["actualHan"]) - set(han) and len(han) == 42
    assert all("\u7e2e" not in (R / n).read_text(encoding="utf-8").split("---", 2)[2]
               for n in font["completeArticleScope"])
    font_checks = []
    for row in font["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path) == row["sha256"]
        with TTFont(path) as face:
            cmap = face.getBestCmap()
        assert {c: ord(c) in cmap for c in font["actualHan"]} == row["actualPresence"]
        assert ord("\u7e2e") in cmap
        font_checks.append({"path": str(path), "sha256": row["sha256"],
                            "actualPresence": {c: ord(c) in cmap for c in han}})
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
    assert checked == 8438
    result.update(execution=687, latestMain=MAIN, upstreamAlreadyAncestor=True,
                  runtimeHashesVerified=checked, frozenInputHashesVerified=len(snapshot["inputs"]),
                  decompressedDictionaryHashesVerified=2, packets=packets,
                  completeRawCharacterRecordsVerified=count,
                  originalBaselineMetadataAndStrokesPreserved=counts,
                  baselineMetadataExceptions=exceptions, exactMembershipAccounted=True,
                  currentCounts=current_counts, publishedIssue60Additions=120,
                  acceptedUnpublishedIssue60Additions=["\u524a"],
                  requiredAllMappedPairs=3, directedLinksVerified=6,
                  pinnedStrokeGeometryExactlyRegenerated=True, scopedHan=han,
                  fontProvenanceReverified=True, fonts=font_checks,
                  fontScopeDiagnostic={
                      "initial687Comparison": "Stopped on stale 677 raw-Han set; no acceptance claimed.",
                      "inheritedNativeVisibleHan": 41, "currentRawArticleHan": 42,
                      "addedOnlyInNonrenderedExclusionMetadata": "\u7e2e",
                      "newMetadataCharacterCoveredByAllBundledFonts": True,
                      "teachingBodiesAndVisibleFontScopeUnchanged": True})
    save(L / "combined-source-audit-687.json", result)
    print("Combined source/baseline/link/reading/font/membership and all8438 hashes passed.", flush=True)


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
        with (L / f"{name}-687.txt").open("w", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-687.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    clean(R, HEAD)
    audit()


def inherited():
    text = load(V / "batch-094-reconciliation.json")
    rendered = load(V / "batch-094-rendered-reconciliation-683.json")
    correction = load(V / "batch-094-correction-reconciliation-685.json")
    closure = load(V / "batch-094-correction-reconciliation-686.json")
    native = load(S / "execution-682.json")
    corrected = load(S / "execution-686.json")
    assert text["textualReviewClosed"]
    assert all(f["status"] == "resolved" for f in text["findings"])
    assert closure["reconciliation"][0]["status"] == "resolved"
    assert correction["processAcceptance"]["allProcessesExited"]
    assert correction["processAcceptance"]["noToolOverlap"]
    assert rendered["processDisposition"]["originalOverlapNeverRelabeledCompliant"]
    assert rendered["processDisposition"]["originalClaude"].startswith("Rejected")
    process_checks = []
    for group in ["processes", "confirmations"]:
        previous = None
        for label in ["claude", "gpt"]:
            p = text[group][label]
            assert p["actualModels"] == ["claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
            assert p["exitCode"] == 0 and not p["observedToolOverlaps"]
            assert p["allAssignedRangesReturned"] and p["exactFullPacketReturnedInOneCall"]
            assert sha(V / p["report"]) == p["reportSha256"]
            prefix = "batch-094-initial-" if group == "processes" else "batch-094-confirm-679-"
            assert sha(V / (prefix + label + ".jsonl")) == p["rawExecutionSha256"]
            if previous:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(p["startedAt"])
            previous = p["completedAt"]
            process_checks.append({"group": group, "model": p["actualModels"][0], "session": p["sessionId"],
                                   "snapshot": p["snapshot"], "report": p["report"]})
    for names in [
        ["batch-094-rendered-683-claude-serial-repair", "batch-094-rendered-683-gpt"],
        ["batch-094-correction-685-claude", "batch-094-correction-685-gpt"],
    ]:
        previous = None
        for name in names:
            p = load(V / (name + "-execution.json"))
            label = "claude" if "claude" in name else "gpt"
            assert p["actualModels"] == ["claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
            assert p["acceptedExecution"] and p["exitCode"] == 0 and not p["observedToolOverlaps"]
            assert not p["unfinishedTools"] and p["dependentOriginalSession"] and not p["newBlindInitialReviewCredit"]
            assert p["sessionId"] == text["processes"][label]["sessionId"]
            assert sha(V / (name + ".md")) == p["reportSha256"]
            raw = gzip.decompress((V / (name + ".jsonl.gz")).read_bytes())
            assert hashlib.sha256(raw).hexdigest() == p["rawSha256"]
            for first, second in zip(p["toolCalls"], p["toolCalls"][1:]):
                assert first["completedAt"] <= second["startedAt"]
            if previous:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(p["startedAt"])
            previous = p["completedAt"]
            process_checks.append({"group": name, "model": p["actualModels"][0], "session": p["sessionId"],
                                   "snapshot": p["snapshot"], "report": name + ".md"})
    verified = 0
    for number in [683, 685, 686]:
        for row in load(S / f"execution-{number}.json")["receipts"]:
            path = R / row["archive"]
            assert sha(path) == row["archiveSha256"], path
            compressed = row.get("losslessGzip", False)
            assert compressed == (path.suffix == ".gz")
            raw = gzip.decompress(path.read_bytes()) if compressed else path.read_bytes()
            assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"], path
            verified += 1
    for row in load(R / native["artifactIndex"]):
        assert sha(R / row["path"]) == row["sha256"]
        verified += 1
    route = load(R / native["routeEvidence"])
    assert native["nativeExecution"]["passed"] and native["terminalPerCaseStatus"] == [0, 0]
    assert route["passed"] and route["onlySakuAndKezuruBothKindsPersistedGoodAndDone"]
    assert route["quizOnKeys"] == ["\u3055\u304f"] and route["quizKunKeys"] == ["\u3051\u305a\u308b"]
    assert route["fullKunyomi"] == ["\u3051\u305a.\u308b", "\u306f\u3064.\u308b", "\u305d.\u3050"]
    assert route["reciprocalLinkAndSystemBack"] and route["offline"]
    assert route["mappedReciprocalPairs"] == 3 and route["directedLinkTransitions"] == 6
    assert route["drawingTraceThenRecall"] and route["drawingGradeRecordedOnNext"]
    assert len(route["directGuardBuilderChecks"]) == 384
    for row in route["directGuardBuilderChecks"]:
        assert not any(o["word"] == row["excluded"] for o in row["options"])
    for number, total in [(682, 2), (686, 1)]:
        raw = (V / "batch-094-native" / f"execution-{number}" / "instrumentation.txt").read_text(encoding="utf-8-sig")
        assert len(re.findall(r"^INSTRUMENTATION_STATUS_CODE: 0\s*$", raw, re.M)) == total
        assert not re.search(r"INSTRUMENTATION_STATUS_CODE: -[234]|FAILURES|INSTRUMENTATION_FAILED", raw)
    assert corrected["nativeExecution"]["passed"] and corrected["nativeTestsPassed"] == 1
    assert corrected["nativeTestsSkipped"] == 0 and corrected["fullArchiveImportedOnce"]
    assert corrected["runtimeHashesVerified"] == 8438 and corrected["directGuardBuilderChecks"] == 128
    assert corrected["directGuardFindingDisposition"] == "resolved"
    actual = json.loads(
        gzip.decompress((V / "batch-094-native" / "execution-686" / "n1-094-correction-686.json.gz").read_bytes()))
    assert (actual["archiveRequests"], actual["importedKanji"], actual["importedWords"], actual["n1Cards"],
            actual["problems"], actual["acceptedReadingParserEpoch"], actual["contentVersion"]) == (
                1, 1117, 5070, 126, 0, 1, VERSION)
    assert not git("diff", actual["contentSnapshot"], HEAD, "--",
                   "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not git("diff", PRODUCTION, APP, "--", "core/src/main", "app/src/main", "gradle.properties", root=A)
    changed = git("-c", "core.quotepath=false", "diff", text["reviewedTeachingSnapshot"], HEAD,
                  "--name-only", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert set(changed.splitlines()) == {"words/\u524a\u308b.md", "manifest.json"}
    for name in text["reviewedRuntimeHashes"]:
        if name not in {"words/\u524a\u308b.md", "manifest.json"}:
            assert sha(R / name) == text["reviewedRuntimeHashes"][name]
    return {
        "initialReviewRecord": "docs/n1-reviews/batch-094-reconciliation.json",
        "renderedRecord": "docs/n1-reviews/batch-094-rendered-reconciliation-683.json",
        "correctionTextualRecord": "docs/n1-reviews/batch-094-correction-reconciliation-685.json",
        "correctedNativeRecord": "docs/n1-sources/execution-686.json",
        "latestFindingClosure": closure["reconciliation"], "processesReverified": process_checks,
        "receiptHashesReverified": verified, "originalClaude683OverlapRemainsRejected": True,
        "native682TerminalCaseStatuses": [0, 0], "native686TerminalCaseStatuses": [0],
        "correctedImportCounts": {k: actual[k] for k in [
            "archiveRequests", "importedKanji", "importedWords", "n1Cards", "problems", "acceptedReadingParserEpoch", "contentVersion"]},
        "correctedImportRuntimeEqualsCurrentTree": True, "newNativeOrReviewerRuns": 0,
        "optional": {"textual": text["optionalDispositions"], "rendered": rendered["optional"], "correction": correction["optional"]},
        "originalLimits": {"textual": text["limits"], "rendered": rendered["limits"],
                           "correction": correction["limits"], "native": native["limits"], "correctedNative": corrected["limits"]},
        "rerunDisposition": "No new concern; visible teaching, geometry, curation, fonts and production app unchanged. Corrected exact import686 inherited, not old682 import relabeled.",
    }


def record():
    context()
    clean(R, HEAD)
    tests = (L / "python-tests-687.txt").read_text(encoding="utf-8-sig")
    match = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert match and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-687.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    assert VERSION in (L / "manifest-687.txt").read_text(encoding="utf-8")
    vocabulary = (L / "vocabulary-687.txt").read_text(encoding="utf-8").strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-687.json")["exitCode"] == 0
    assert (L / "host-exit-687.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-687.txt").read_text(encoding="utf-8-sig")
    begin = datetime.fromisoformat((L / "host-start-687.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((L / "host-end-687.txt").read_text(encoding="utf-8-sig").strip())
    suites = []
    for module, task, cls, names in [
        ("core", "test", "RealContentTest", {
            "parsesRealContentRepoWhenPresent", "hotelBookingDoesNotAcceptTheSchoolClassReadingWhenRepoPresent",
            "completeMixedArchiveKeepsShortTaskAudioOutOfTheLegacyReaderWhenRepoPresent"}),
        ("app", "testDebugUnitTest", "RareHanTest", {"contentRareCharactersAreCoveredByBundledFont"}),
    ]:
        path = A / module / "build" / "test-results" / task / f"TEST-io.github.stopcran.kanji.core.{cls}.xml"
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == len(names)
        assert all(xml.attrib[k] == "0" for k in ["skipped", "errors", "failures"])
        assert {x.attrib["name"] for x in xml.findall("testcase")} == names
        assert not any(xml.findall(".//" + name) for name in ["skipped", "failure", "error"])
        stamp = datetime.fromisoformat(xml.attrib["timestamp"]).astimezone(timezone.utc)
        assert begin <= stamp <= end and path.stat().st_mtime >= begin.timestamp()
        suites.append({"path": str(path), "sha256": sha(path), "suite": xml.attrib,
                       "cases": [x.attrib for x in xml.findall("testcase")]})
    assert all((A / module / ".." / ".." / "learning-japanese").resolve() == R for module in ["app", "core"])
    source, inheritance = load(L / "combined-source-audit-687.json"), inherited()
    budget = ast.literal_eval((L / "budget-687.txt").read_text(encoding="utf-8"))
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    assert not D.exists()
    D.mkdir()
    paths = [
        *(L / name for name in ["starting-state-687.json", "combined-source-audit-687.json", "merge-687.txt",
          "python-tests-687.txt", "validate-687.txt", "manifest-687.txt", "vocabulary-687.txt", "budget-687.txt",
          "host-687.txt", "host-exit-687.txt", "host-command-687.json", "host-start-687.txt", "host-end-687.txt"]),
        *(L / f"{name}-exit-687.json" for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-094-host-687.ps1",
        C / "post-batch-094-687.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        A / "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    ]
    receipts = []
    for path in paths:
        raw = path.read_bytes()
        target = D / (path.name + (".gz" if path.suffix == ".txt" else ""))
        assert not target.exists(), target
        target.write_bytes(gzip.compress(raw, mtime=0) if path.suffix == ".txt" else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "archiveSha256": sha(target), "losslessGzip": path.suffix == ".txt"})
    evidence = {
        "schemaVersion": 1, "execution": 687, "batch": "094", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-687.json"), "combinedContentHead": HEAD,
        "latestMainIntegrated": MAIN, "normalMerge": True, "mergeResult": "Already up to date.",
        "newMergeCommit": False, "conflicts": [], "substantiveTeachingConflictEdits": [],
        "runtimeBytesUnchanged": True, "sourceAudit": source, "pythonTestsPassed": int(match[1]),
        "validatorErrors": 0, "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary,
        "manifestFresh": True, "contentVersion": VERSION, "localBudget": budget, "hostSuites": suites,
        "hostChecksFresh": True, "hostTestsExecuted": 4, "hostTestsSkipped": 0, "androidHead": APP,
        "unchangedProductionAndroid": PRODUCTION, "qualifiedTestOnlyAndroid": True,
        "inheritedAcceptance": inheritance, "receipts": receipts, "runtimeAccepted": True,
        "runtimePublished": False, "publicGithubZipAcceptance": False,
        "publishedAdditions": 120, "remainingAdditions": 1108, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": [
            "Local combined-tree acceptance only, not public delivery or fresh native/linguistic review.",
            "Vocabulary2122/2431 pilot consistency not full coverage; no unrelated coverage fix.",
            "125 complete family occurrences/121 distinct families; mechanical equality, not fresh linguistic rereview.",
            "41 unchanged visible Han inherited;42 raw Han includes new metadata-only exclusion character縮, cmap verified in all bundled fonts, no new visible glyph claim.",
            "Original683 overlap remains rejected; accepted serial repair and all original process/read/visual/fallbackface/injectedtrace/MLKit limitations retained.",
            "Qualified test-only Android not latestappmain; CI/publicZIP/publication/physicalphone/generalrelease/whole-set remain outstanding.",
        ],
    }
    save(S / "execution-687.json", evidence)
    review = {
        "schemaVersion": 1, "batch": "094", "execution": 687, "status": STAGE,
        "snapshot": HEAD, "contentVersion": VERSION, "newIndependentReviewers": 0,
        "inheritedRecords": {k: inheritance[k] for k in [
            "initialReviewRecord", "renderedRecord", "correctionTextualRecord", "correctedNativeRecord"]},
        "verdicts": {name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "comprehensibility": "CLEAN"}
                     for name in ["kanji/\u524a.md", "words/\u524a\u308b.md", "words/\u524a\u9664.md", "kanji/\u9664.md:41"]},
        "reconciliation": text_findings() + closure_findings(),
        "optional": inheritance["optional"], "limits": evidence["limits"],
        "originalLimits": inheritance["originalLimits"], "runtimeAccepted": True,
        "runtimePublished": False, "evidence": "docs/n1-sources/execution-687.json", "nextAction": NEXT,
    }
    save(V / "batch-094-combined-reconciliation-687.json", review)
    path = S / "batch-094-progress.json"
    ledger = load(path)
    fields = ["status", "nextAction", "reviewClosed", "runtimeAccepted", "runtimePublished", "pendingGates", "limits"]
    ledger["preCombined687State"] = {k: ledger.get(k) for k in fields}
    ledger.update(status=STAGE, reviewClosed=ledger["membership"], runtimeAccepted=True, runtimePublished=False,
                  combinedAcceptance="docs/n1-sources/execution-687.json", nextAction=NEXT)
    ledger["pendingGates"] = [
        "Fresh-main recheck, normal signed owner fastforward publication; if main advances merge/reconcile/regenerate/revalidate and independently review changed substantive teaching.",
        "Exact remote SHA, terminal green relevant CI, EVERY immutable public ZIP runtime entry/hash, manifest equality and unchanged entry/compressed/inflated/retained/per-file/path/media budgets; durable publication ledger and verified owner issue before095.",
        "Physicalphone/generalrelease/whole-set acceptance remains explicitly outstanding.",
    ]
    ledger["limits"] = evidence["limits"]
    save(path, ledger)
    print("Combined acceptance evidence archived; no runtime content changes or publication.")


def text_findings():
    return load(V / "batch-094-reconciliation.json")["findings"]


def closure_findings():
    return load(V / "batch-094-correction-reconciliation-686.json")["reconciliation"]


def finalize():
    context()
    head = git("rev-parse", "HEAD")
    assert head != HEAD
    clean(R, head)
    evidence = load(S / "execution-687.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["archiveSha256"]
    expected = {r["archive"] for r in evidence["receipts"]} | {
        "docs/n1-sources/execution-687.json", "docs/n1-sources/batch-094-progress.json",
        "docs/n1-reviews/batch-094-combined-reconciliation-687.json"}
    assert set(git("diff", "--name-only", HEAD, head).splitlines()) == expected
    assert not git("diff", HEAD, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    issue = load(C / "batch-094-687-issue-receipt.json")
    body = (C / "batch-094-687-issue-body.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body and head in body
    before = load(L / "progress-before-687.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 687, "checkpoint": 687, "batch": "094",
        "savedCommit": head, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-687.json",
        "reviewRecord": "docs/n1-reviews/batch-094-combined-reconciliation-687.json",
        "pythonTestsPassed": evidence["pythonTestsPassed"], "hostTestsExecuted": 4, "hostTestsSkipped": 0,
        "runtimeHashesVerified": 8438, "contentVersion": VERSION,
        "runtimeChangedThisExecution": False, "reviewClosed": ["\u524a"],
        "runtimeAccepted": True, "runtimePublished": False, "publicGithubZipAcceptance": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "independentReviewersLaunched": 0, "newNativeRuns": 0,
        "publishedAdditions": 120, "remainingAdditions": 1108, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": issue["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    p.update(checkpoint=687, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution687StartingState"]["status"] = "signed-local-combined-acceptance-checkpoint-complete"
    p["execution687CoordinatorCheckpoint"] = checkpoint
    p["batch094CombinedAcceptanceCheckpoint"] = checkpoint
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", p)
    final = load(C / "progress.json")
    assert all(final[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-687.json", checkpoint)
    print("Checkpoint687 persisted; all original historical values preserved; both worktrees clean.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"start": start, "audit": audit, "checks": checks, "record": record, "finalize": finalize}[sys.argv[1]]()
