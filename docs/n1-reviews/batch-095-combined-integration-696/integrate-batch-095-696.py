"""Preserve batch 095 while checking the actual non-rewriting main integration."""
import base64
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
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "a5e4986a-d4a8-49b0-893f-70922ec19530"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
HEAD = "515666e98b11e79a2d5a4bc116717f110d7769e3"
MAIN = "da374717b6f8a53430c9583e9b5371004e1f7719"
BASE = "d6a261903f269d6223afc067815b02c595da41a3"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
STAGE = "combined-main-automated-checked-awaiting-changed-teaching-review-and-import"
NEXT = (
    "SAME095 only: finish combined-main acceptance at signed merge d5a6823c "
    "(parents515666e9+da374717), contentVersion3eebfff0fdad5e28/all8441hashes. "
    "Read docs/n1-sources/execution-696.json and "
    "docs/n1-reviews/batch-095-combined-integration-696.json. "
    "Fresh696 all372Python/validate/regeneratedmanifest/vocabularypilot2122of2431/"
    "unchangedbudgets/fullfrozendictionaries/fullbaseline/readings/strokes/allmappedlinks/"
    "fontprovenance and FOURAndroidRealContentTHREE+RareHanONE/no skips passed. "
    "Only manifest conflict was regenerated; incoming eleven teaching files and source "
    "packet preserved exactly from da374717, all four batch095runtime files exactly "
    "from515666e9. No overlapping teaching conflict. Incoming substantive 子/"
    "nominal-ending amendments include priorN1words柚/帽子/冊子: upstream has one "
    "independent reviewer with model unavailable, NOT batch095 two-family credit. "
    "Perform bounded independent changed-passage confirmation in original Claude "
    "ede78c28-e889-47b5-be0b-21533da61551 THEN GPT "
    "ee7498e0-d3ad-46bf-bbc9-82761892cab0 on SAME frozen combined snapshot. "
    "Use exact before/after incoming11files, surrounding actual articles, "
    "docs/ko-nominal-endings-sources.json and mandatory precise source evidence; "
    "no cross-report contamination, at mostONE reviewer and serial tools, verify actual "
    "models/process exits/fullreports/limits; reconcile by evidence and fix/reconfirm "
    "only actionable defects. Use installed actualCLI catalog at execution time. "
    "Original691blind/694native/695rendered records remain inherited with all limits; "
    "originalClaude695overlap remains REJECTED, accepted smallest serialrepair separate. "
    "All32batch095Han/fourfonts/60PNG and teaching/geometry/reading/quizmetadata unchanged, "
    "so no manufactured glyph/route rerun requirement. BUT exact combined manifest "
    "DIFFERS from native694version463619d79972e9f2: obtain bounded new full combined "
    "archive through productionContentSync ONCE, assert1118kanji5071words127N1/"
    "zeroProblems/acceptedRoomversion3eebfff0fdad5e28+readingepoch1 and preserved "
    "full/Liteボウ/[] explicitボウ/[] plus THREEdirectguards and links. "
    "Do NOT relabel old fullarchivecc748347/native694 as new combined import. "
    "Keep old fixture/hash immutable; new clearly named fixture/evidence, no guards/heap "
    "changes. Freshport/device/PID5580/5581ownership for ownedreadonlyAPI35 emulator "
    "N3_Acceptance_20261029 emulator5580 hostGPU/-Vulkan/2048MiB/2cores; stop onlyownedhelper. "
    "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, NOT latestappmain. "
    "Then normal signed reviewclosed/combinedacceptance evidence; freshmain recheck "
    "and nonrewriting merge/revalidate if advanced; ownerfastforward to origin/main "
    "only after ALLgates. Verify exactremoteSHA/terminalgreenCI/EVERYimmutablepublicZIP"
    "runtimeentryhash/manifest equality/original18000entries42MiBcompressed80MiBinflated"
    "56MiBretained/perfile-media-safepath/verifiedownerissue. LocalZIP not publicacceptance. "
    "Parent19008 ownsrunner.lock: verifyliveancestry/session/checkpoint/exactsignedheads/"
    "whollyclean, NOchildacquire/delete/unlock. Approvedcontrol/committedpackets only, "
    "no optionalhistoricalsessionhelpers. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. No runtimepublication/096/secondrunner at696. "
    "Published121of1228/1107remaining unchanged; physicalphone/generalrelease/whole-set "
    "outstanding, no phone/humanhandwriting/MLKit/fullpool certification."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".696.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, expected):
    assert git("rev-parse", "HEAD", root=root) == expected
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
    assert sha(C / "runner.ps1") == "f83fec8ee5ade731adbd00bfbfc48df8d2bd673afd12d0d4118fb17e4d66e9af"
    progress = load(C / "progress.json")
    assert (progress["checkpoint"], progress["batch"], progress["status"]) == (695, "095", "continue")
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    return {
        "parentPid": 19008, "session": L.name, "decodedLauncherMatches": True,
        "launcherSha256": sha(C / "runner.ps1"), "parentLockTouched": False,
        "ancestry": [{k: p[k] for k in ("pid", "parent", "name")} for p in chain],
    }


def start():
    role = context()
    clean(R, HEAD)
    assert not (L / "progress-before-696.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-696.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution695CoordinatorCheckpoint"] == p["execution695CoordinatorCheckpoint"]
    state = {
        "execution": 696, "batch": "095", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME095 non-rewriting current-main integration and combined automated checks; signed LOCAL checkpoint only, no publication/096.",
        "request": {
            "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire file loaded and embedded checkpoint decoded. Operative contract, complete issue and final695 inspected directly; historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": role, "actualNewPermissionDenials": [],
        "artifactPathPreflight": "Approved control and committed sources/frozen inputs only; no optional historical-session helper access.",
    }
    save(L / "starting-state-696.json", state)
    p["execution696StartingState"] = state
    p.update(stage="batch-095-current-main-integration-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    before = load(L / "progress-before-696.json")
    assert all(p[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    assert git("merge-base", HEAD, MAIN) == BASE
    incoming = git("-c", "core.quotepath=false", "diff", "--name-only", BASE, MAIN).splitlines()
    authored = git("-c", "core.quotepath=false", "diff", "--name-only", BASE, HEAD).splitlines()
    assert set(incoming) & set(authored) == {"manifest.json"}
    save(L / "integration-scope-696.json", {
        "before": HEAD, "main": MAIN, "commonBase": BASE, "incomingPaths": incoming,
        "authoredPaths": authored, "overlap": ["manifest.json"],
        "incomingSourceRecord": "docs/ko-nominal-endings-sources.json",
        "incomingIndependentReview": "One upstream independent reviewer; actual model unavailable. Not credited as batch095 two-family review.",
        "mergeConflictPolicy": "Preserve exact disjoint teaching bytes from each parent; regenerate manifest, never choose a stale side.",
    })
    print("Starting state persisted; exact disjoint scope verified; parent lock untouched.", flush=True)


def integrated_head():
    receipt = load(L / "merge-signed-head-696.json")
    head = receipt["head"]
    clean(R, head)
    assert git("show", "-s", "--format=%P", head).split() == [HEAD, MAIN]
    return head


def freeze():
    context()
    head = git("rev-parse", "HEAD")
    clean(R, head)
    assert git("show", "-s", "--format=%P", head).split() == [HEAD, MAIN]
    composed = integration()
    composed.pop("beforeManifest")
    composed.pop("currentManifest")
    save(L / "merge-signed-head-696.json", {
        "head": head, "signature": "G", "parents": [HEAD, MAIN],
        "mergeConflictPaths": ["manifest.json"], "resolution": "Regenerated with tools/build_manifest.py",
        "exactComposition": composed, "runtimeAccepted": False, "runtimePublished": False,
    })
    print("Signed integrated snapshot:", head, composed["contentVersion"], flush=True)


def integration():
    from build_manifest import build_manifest, sha256

    before = json.loads(git("show", f"{HEAD}:manifest.json"))
    base = json.loads(git("show", f"{BASE}:manifest.json"))
    main = json.loads(git("show", f"{MAIN}:manifest.json"))
    current = build_manifest(R)
    expected = copy.deepcopy(before)
    changes = []
    for section, entries in main.items():
        if not isinstance(entries, dict):
            continue
        assert section in base and section in before
        assert entries.keys() == base[section].keys()
        for name, value in entries.items():
            if value != base[section][name]:
                assert before[section][name] == base[section][name], name
                assert sha256(R / name) == value, name
                expected[section][name] = value
                changes.append(name)
    expected["contentVersion"] = current["contentVersion"]
    assert current == expected == load(R / "manifest.json")
    assert len(changes) == 11
    assert not git("diff", MAIN, "--", *changes, "docs/ko-nominal-endings-sources.json")
    incoming = load(L / "integration-scope-696.json")["incomingPaths"]
    authored_runtime = [n for n in before["files"] if base["files"].get(n) != before["files"][n]]
    assert set(authored_runtime) == {"kanji/\u5256.md", "kanji/\u89e3.md", "words/\u89e3\u5256.md", "strokes/\u5256.json"}
    assert not set(changes) & set(authored_runtime)
    assert not git("diff", HEAD, "--", *authored_runtime)
    actual = git("-c", "core.quotepath=false", "diff", "--name-only", HEAD).splitlines()
    assert set(actual) == set(incoming)
    for section, entries in current.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                found = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert found == digest, name
    return {
        "beforeManifest": before, "currentManifest": current,
        "incomingRuntimePaths": changes, "batch095RuntimePaths": authored_runtime,
        "contentVersion": current["contentVersion"], "oldNativeContentVersion": before["contentVersion"],
        "runtimeHashesVerified": sum(len(e) for e in current.values() if isinstance(e, dict)),
        "disjointTeachingPreservedExactly": True, "incomingMetadataPreserved": True,
        "oldNativeArchiveEqualsCombinedTree": False,
    }


def audit():
    from audit_n1_pilot import metadata
    import audit_n1_batch
    from extract_n1_jmdict import extract
    from generate_strokes import convert
    from build_manifest import sha256
    from fontTools.ttLib import TTFont

    context()
    head = integrated_head()
    merged = integration()
    original_delta = audit_n1_batch.runtime_delta

    def composed_delta(before, after, additions, changed):
        original_delta(before, merged["beforeManifest"], additions, changed)
        assert after == merged["currentManifest"]

    audit_n1_batch.runtime_delta = composed_delta
    try:
        result = audit_n1_batch.audit(R, "095")
    finally:
        audit_n1_batch.runtime_delta = original_delta
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        path = C / "inputs" / name
        assert path.stat().st_size == info["bytes"] and sha(path) == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert hashlib.sha256(gzip.decompress(jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(kd).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    ledger = load(S / "batch-095-progress.json")
    packets = []
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        expected = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt.gz" if i == 0 else "comparison-full-family-reading.txt.gz"
        compact = gzip.decompress((S / f"batch-095-{suffix}").read_bytes())
        assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact.decode("utf-8") + "</JMdict>")] == [
            canonical(e) for e in ET.fromstring(expected)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(S / packet["xml"]),
                        "freshFrozenExtractionMatches": True, "completeCompactSemanticEquality": True})
    assert sum(p["families"] for p in packets) == 37
    records = {e.findtext("literal"): e for e in ET.fromstring(kd).findall("character")}
    count = 0
    for name in ["batch-095-kanjidic2.xml", "batch-095-comparison-kanjidic2.xml"]:
        for row in ET.parse(S / name).getroot().findall("character"):
            assert canonical(row) == canonical(records[row.findtext("literal")])
            count += 1
    assert count == 7
    exceptions = load(S / "batch-095-draft-audit.json")["baselineMetadataExceptions"]
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in load(S / "baseline-inventory.json")["files"].items():
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
            assert sha(R / name) == info["sha256"]
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and len(named) == 1232
    chars = {p.stem for p in (R / "kanji").glob("*.md")}
    old = {Path(n).stem for n in merged["beforeManifest"]["files"] if n.startswith("kanji/")}
    assert chars == old and metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    for char in "\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50":
        assert metadata(R, f"kanji/{char}.md")["jlpt"] == 2
    current_counts = {
        "kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
        "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
    }
    assert current_counts == {"kanji": 1118, "words": 5071, "n1Labels": 127}
    pairs = {(c, row["article"]) for row in ledger["supportMappings"]
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 2
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
    assert metadata(R, "words/\u89e3\u5256.md")["quiz_exclusions"] == ["\u5206\u6790", "\u5206\u89e3", "\u691c\u67fb"]
    svg = (S / "batch-095-kanjivg.svg").read_bytes()
    stroke = load(S / "batch-095-stroke-evidence.json")
    assert hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert sha256(R / "tools" / "generate_strokes.py") == stroke["converterNormalizedSha256"]
    assert load(R / "strokes" / "\u5256.json") == convert("\u5256", svg.decode("utf-8"))
    font = load(S / "batch-095-draft-font-audit.json")
    text = "".join((R / name).read_text(encoding="utf-8") for name in font["completeArticleScope"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert han == font["actualHan"] and len(han) == 32
    for row in font["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path) == row["sha256"]
        with TTFont(path) as face:
            cmap = face.getBestCmap()
        assert {c: ord(c) in cmap for c in han} == row["actualPresence"]
    assert merged["runtimeHashesVerified"] == 8441
    merged.pop("beforeManifest")
    merged.pop("currentManifest")
    result.update(
        execution=696, combinedContentHead=head, integratedMain=MAIN,
        exactComposedDelta=merged, frozenInputHashesVerified=len(snapshot["inputs"]),
        packets=packets, completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        currentCounts=current_counts, allMappedReciprocalPairs=2, directedLinksVerified=4,
        activatedBaselinePairs=0, pinnedStrokeGeometryExactlyRegenerated=True,
        scopedHan=han, fontProvenanceReverified=True,
        limits="Mechanical combined audit with explicit disjoint upstream delta; not new linguistic/native/publication acceptance.",
    )
    result["exactBaseRuntimePreservedOutsideRecordedChanges"] = False
    result["exactBaseRuntimePreservedOutsideBatchAndIncomingChanges"] = True
    result["unmergedBatchDeltaSeparatelyVerified"] = True
    save(L / "combined-source-audit-696.json", result)
    print("Combined frozen sources/baseline/readings/links/strokes/fonts and 8441 hashes passed.", flush=True)


def checks():
    context()
    integrated_head()
    for name, arguments in [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]),
        ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
    ]:
        command = [sys.executable, "-X", "utf8", "-B", *arguments]
        with (L / f"{name}-696.txt").open("w", encoding="utf-8") as output:
            completed = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-696.json", {"command": command, "exitCode": completed.returncode})
        assert completed.returncode == 0, name
        print(name, "passed", flush=True)
    audit()


def preflight():
    context()
    integrated_head()
    assert load(C / "progress.json")["stage"] == "batch-095-current-main-integration-in-progress"
    print("Exact signed heads, wholly clean worktrees and live parent ancestry verified; lock untouched.")


def inherited():
    textual = load(V / "batch-095-reconciliation.json")
    rendered = load(V / "batch-095-rendered-reconciliation-695.json")
    native = load(S / "execution-694.json")
    assert textual["textualReviewClosed"] and not textual["findings"]
    assert rendered["actionableRemainingFindings"] == 0
    assert rendered["consequentialUnresolvedInScopeClaims"] == 0
    assert rendered["processDisposition"]["originalOverlapNeverRelabeledCompliant"]
    for name, value in textual["reviewedRuntimeHashes"].items():
        if name != "manifest.json":
            assert sha(R / name) == value, name
    previous = None
    for label in ["claude", "gpt"]:
        process = textual["processes"][label]
        assert process["actualModels"] == ["claude-opus-5.5" if label == "claude" else "gpt-6.1-sol"]
        assert process["exitCode"] == 0 and not process["observedToolOverlaps"]
        assert process["allAssignedRangesReturned"] and process["exactFullPacketReturnedInOneCall"]
        assert sha(V / process["report"]) == process["reportSha256"]
        raw = V / f"batch-095-initial-{label}.jsonl"
        assert sha(raw) == process["rawExecutionSha256"]
        if previous:
            assert datetime.fromisoformat(previous) < datetime.fromisoformat(process["startedAt"])
        previous = process["completedAt"]
    receipts_checked = 0
    for row in load(S / "execution-695.json")["receipts"]:
        path = R / row["archive"]
        assert sha(path) == row["archiveSha256"]
        raw = gzip.decompress(path.read_bytes()) if row.get("losslessGzip") else path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row["sourceSha256"]
        receipts_checked += 1
    for name in ["claude-serial-repair", "gpt"]:
        record = load(V / f"batch-095-rendered-695-{name}-execution.json")
        assert record["acceptedExecution"] and record["exitCode"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
    assert native["terminalPerCaseStatus"] == [0, 0] and native["nativeTestsSkipped"] == 0
    assert native["fullArchiveImportedOnce"] and native["contentVersion"] == "463619d79972e9f2"
    route = load(R / native["routeEvidence"])
    assert (route["archiveRequests"], route["importedKanji"], route["importedWords"],
            route["n1Cards"], route["problems"], route["acceptedReadingParserEpoch"]) == (1, 1118, 5071, 127, 0, 1)
    assert route["onlyOnBouNoKunPersistedGoodAndDone"] and route["offline"]
    assert route["reciprocalLinkAndSystemBack"] and route["drawingTraceThenRecall"]
    assert len(route["productionBuilderN1AndAllExactChoices"]) == 64
    assert len(route["directGuardBuilderChecks"]) == 384
    for row in load(R / native["artifactIndex"]):
        assert sha(R / row["path"]) == row["sha256"]
        receipts_checked += 1
    assert not git("diff", "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", APP,
                   "--", "core/src/main", "app/src/main", "gradle.properties", root=A)
    return {
        "initialRecord": "docs/n1-reviews/batch-095-reconciliation.json",
        "nativeRecord": "docs/n1-sources/execution-694.json",
        "renderedRecord": "docs/n1-reviews/batch-095-rendered-reconciliation-695.json",
        "receiptHashesReverified": receipts_checked,
        "originalClaude695OverlapRemainsRejected": True,
        "acceptedSerialRepairPreserved": True,
        "originalTeachingAndStrokesUnchanged": True,
        "native694ContentVersion": native["contentVersion"],
        "native694EqualsCombinedManifest": False,
        "newNativeRuns": 0, "newReviewers": 0,
        "originalLimits": {"textual": textual["limits"], "native": native["limits"], "rendered": rendered["limits"]},
        "incomingTeachingReview": "Pending bounded two-family changed-passage confirmation; upstream single independent review/model unavailable preserved as evidence, not substituted.",
        "changedNativeScope": "Only exact merged full-archive production ContentSync import/version/metadata assertions require new evidence. Batch095 visible teaching/fonts/strokes/reading/quiz metadata unchanged; inherited interaction/glyph evidence retained with original limits.",
    }


def record():
    context()
    head = integrated_head()
    assert not git("diff", "--check")
    tests = (L / "python-tests-696.txt").read_text(encoding="utf-8-sig")
    matched = re.search(r"^Ran (\d+) tests in ", tests, re.M)
    assert matched and re.search(r"^OK$", tests, re.M) and "skipped=" not in tests
    assert (L / "validate-696.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    vocabulary = (L / "vocabulary-696.txt").read_text(encoding="utf-8").strip()
    assert vocabulary == "Vocabulary coverage: 2122/2431 reviewed prompts; stage=pilot"
    for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]:
        assert load(L / f"{name}-exit-696.json")["exitCode"] == 0
    assert (L / "host-exit-696.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "host-696.txt").read_text(encoding="utf-8-sig")
    begin = datetime.fromisoformat((L / "host-start-696.txt").read_text(encoding="utf-8-sig").strip())
    end = datetime.fromisoformat((L / "host-end-696.txt").read_text(encoding="utf-8-sig").strip())
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
    budget = ast.literal_eval((L / "budget-696.txt").read_text(encoding="utf-8"))
    assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
    assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
    inheritance = inherited()
    source = load(L / "combined-source-audit-696.json")
    assert not source["exactBaseRuntimePreservedOutsideRecordedChanges"]
    assert source["exactBaseRuntimePreservedOutsideBatchAndIncomingChanges"]
    directory = V / "batch-095-combined-integration-696"
    assert not directory.exists()
    directory.mkdir()
    paths = [
        *(L / name for name in ["starting-state-696.json", "combined-source-audit-696.json",
          "integration-scope-696.json", "merge-696.txt", "merge-signed-head-696.json",
          "premerge-validate-696.txt", "python-tests-696.txt", "validate-696.txt",
          "manifest-696.txt", "vocabulary-696.txt", "budget-696.txt", "host-696.txt",
          "host-exit-696.txt", "host-command-696.json", "host-start-696.txt", "host-end-696.txt"]),
        *(L / f"{name}-exit-696.json" for name in ["python-tests", "validate", "manifest", "budget", "vocabulary"]),
        *(Path(row["path"]) for row in suites), Path(__file__), C / "run-batch-095-host-696.ps1",
        C / "post-batch-095-integration-696.ps1", C / "batch-065-host-integration-heap.init.gradle",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/RealContentTest.kt",
        A / "core/src/test/kotlin/io/github/stopcran/kanji/core/PublishableContentFixture.kt",
        A / "app/src/test/java/io/github/stopcran/kanji/core/RareHanTest.kt",
    ]
    receipts = []
    for path in paths:
        raw = path.read_bytes()
        compressed = path.suffix == ".txt"
        target = directory / (path.name + (".gz" if compressed else ""))
        assert not target.exists(), target
        target.write_bytes(gzip.compress(raw, mtime=0) if compressed else raw)
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(path), "archiveSha256": sha(target), "losslessGzip": compressed})
    evidence = {
        "schemaVersion": 1, "execution": 696, "batch": "095", "status": "continue", "stage": STAGE,
        "startingState": load(L / "starting-state-696.json"), "combinedContentHead": head,
        "latestMainIntegrated": MAIN, "normalNonRewritingMerge": True, "mergeParents": [HEAD, MAIN],
        "conflicts": ["manifest.json"], "resolution": "Regenerated with tools/build_manifest.py",
        "substantiveTeachingConflictEdits": [], "incomingTeachingPreservedExactly": True,
        "batch095TeachingPreservedExactly": True, "incomingSubstantiveChangedPassages": 11,
        "sourceAudit": source, "pythonTestsPassed": int(matched[1]), "validatorErrors": 0,
        "vocabularyConsistencyPassed": True, "vocabularyCoverage": vocabulary, "manifestFresh": True,
        "contentVersion": source["contentVersion"], "runtimeHashesVerified": 8441, "localBudget": budget,
        "hostSuites": suites, "hostChecksFresh": True, "hostTestsExecuted": 4, "hostTestsSkipped": 0,
        "androidHead": APP, "qualifiedTestOnlyAndroid": True,
        "unchangedProductionAndroid": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
        "inheritedEvidence": inheritance, "receipts": receipts,
        "changedTeachingTwoFamilyConfirmation": "pending", "exactCombinedNativeImport": "pending",
        "runtimeChangedByMainIntegration": True, "batch095RuntimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False, "publicGithubZipAcceptance": False,
        "publishedAdditions": 121, "remainingAdditions": 1107, "lastPublishedCommit": BASE,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "newReviewers": 0, "newNativeRuns": 0, "nextAction": NEXT,
        "limits": [
            "Combined automated/source acceptance only; upstream substantive changed teaching and exact new native import gates remain before full batch acceptance/publication.",
            "Upstream one independent review has unavailable model; not silently relabeled two-family review.",
            "Native694 fullarchivecc748347/version463619d79972e9f2 remains historical; it is not the new merged3eebfff0fdad5e28 import.",
            "All batch095 visible teaching,32Han/fourfonts/60PNGs/geometry/reading/quiz metadata unchanged; original native/rendered scope and all limits retained, not new phone/humanhandwriting/MLKit/fullpool acceptance.",
            "Vocabulary2122/2431 pilot consistency only, not full coverage; no unrelated fixes.",
            "Source byte equivalence and metadata preservation are mechanical evidence, not a fresh linguistic review.",
            "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2; not latestappmain.",
            "Local GitZIP budget not immutable publicGithubZIP/CI/publication; physicalphone/generalrelease/whole-set outstanding.",
        ],
    }
    save(S / "execution-696.json", evidence)
    save(V / "batch-095-combined-integration-696.json", {
        "schemaVersion": 1, "batch": "095", "execution": 696, "status": STAGE, "snapshot": head,
        "contentVersion": source["contentVersion"], "newIndependentReviewers": 0,
        "newLinguisticVerdicts": None,
        "originalBatchReviewRecord": inheritance["initialRecord"],
        "originalRenderedRecord": inheritance["renderedRecord"],
        "incomingScope": source["exactComposedDelta"]["incomingRuntimePaths"],
        "incomingReviewEvidence": "docs/ko-nominal-endings-sources.json",
        "incomingTwoFamilyChangedPassageConfirmation": "pending",
        "originalClaude695OverlapRemainsRejected": True,
        "batch095TeachingUnchanged": True, "exactCombinedNativeImport": "pending",
        "runtimeAccepted": False, "runtimePublished": False, "limits": evidence["limits"],
        "evidence": "docs/n1-sources/execution-696.json", "nextAction": NEXT,
    })
    path = S / "batch-095-progress.json"
    ledger = load(path)
    prior = {k: ledger.get(k) for k in ["status", "nextAction", "pendingGates"]}
    ledger["preIntegration696State"] = prior
    ledger.update(status=STAGE, nextAction=NEXT)
    ledger["combinedIntegration696"] = {
        "head": head, "main": MAIN, "evidence": "docs/n1-sources/execution-696.json",
        "automatedChecksPassed": True, "incomingChangedTeachingReview": "pending",
        "exactCombinedNativeImport": "pending", "runtimeAccepted": False, "runtimePublished": False,
        "historicalRecordsUnchanged": True,
    }
    ledger["pendingGates"] = [
        "Two-family bounded review of eleven incoming substantive teaching diffs, preserving upstream evidence/metadata/bytes; original sessions serially where possible.",
        "Exact merged3eebfff0fdad5e28 full archive productionContentSync ONCE/acceptedRoomversion+epoch/counts; old native694 not relabeled.",
        "Full combined acceptance/normal signing/freshmainrecheck/ownerfastforward/terminalgreenCI/EVERYimmutablepublicZIPhash/unchangedbudgets/verifiedownerissue before096.",
        "Physicalphone/generalrelease/whole-set acceptance remains explicitly outstanding.",
    ]
    save(path, ledger)
    print("Combined integration evidence archived; teaching review/import/publication remain pending.", flush=True)


def finalize():
    context()
    head = git("rev-parse", "HEAD")
    clean(R, head)
    merge = load(L / "merge-signed-head-696.json")["head"]
    assert git("rev-parse", "HEAD^") == merge
    evidence = load(S / "execution-696.json")
    for row in evidence["receipts"]:
        assert sha(R / row["archive"]) == row["archiveSha256"]
    expected = {row["archive"] for row in evidence["receipts"]} | {
        "docs/n1-sources/execution-696.json", "docs/n1-sources/batch-095-progress.json",
        "docs/n1-reviews/batch-095-combined-integration-696.json"}
    assert set(git("-c", "core.quotepath=false", "diff", "--name-only", merge, head).splitlines()) == expected
    assert not git("diff", merge, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    issue = load(C / "batch-095-integration-696-issue-receipt.json")
    body = (C / "batch-095-integration-696-issue-body.txt").read_bytes().decode("utf-8")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == body and head in body
    before = load(L / "progress-before-696.json")
    progress = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[k] == value for k, value in before.items() if k not in allowed)
    checkpoint = {
        "schemaVersion": 1, "execution": 696, "checkpoint": 696, "batch": "095",
        "savedCommit": head, "signature": "G", "integratedMerge": merge, "integratedMain": MAIN,
        "status": "continue", "stage": STAGE, "evidence": "docs/n1-sources/execution-696.json",
        "reviewRecord": "docs/n1-reviews/batch-095-combined-integration-696.json",
        "pythonTestsPassed": evidence["pythonTestsPassed"], "hostTestsExecuted": 4, "hostTestsSkipped": 0,
        "runtimeHashesVerified": 8441, "contentVersion": evidence["contentVersion"],
        "incomingSubstantiveChangedPassages": 11, "changedTeachingConfirmation": "pending",
        "exactCombinedNativeImport": "pending", "batch095RuntimeChanged": False,
        "runtimeAccepted": False, "runtimePublished": False, "publicGithubZipAcceptance": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False, "newIndependentReviewers": 0, "newNativeRuns": 0,
        "publishedAdditions": 121, "remainingAdditions": 1107, "lastPublishedCommit": BASE,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "issueUpdate": issue["html_url"],
        "ownerAuthorAndBodyVerified": True, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalRootValuesPreservedExactly": True, "nextAction": NEXT,
    }
    progress.update(checkpoint=696, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    progress["execution696StartingState"]["status"] = "signed-local-combined-integration-checkpoint-complete"
    progress["execution696CoordinatorCheckpoint"] = checkpoint
    progress["batch095CombinedIntegrationCheckpoint"] = checkpoint
    assert all(progress[k] == value for k, value in before.items() if k not in allowed)
    save(C / "progress.json", progress)
    reread = load(C / "progress.json")
    assert all(reread[k] == value for k, value in before.items() if k not in allowed)
    assert reread["checkpoint"] == 696 and reread["status"] == "continue"
    save(L / "checkpoint-696.json", checkpoint)
    print("Checkpoint696 persisted; all original historical values preserved, both worktrees clean.", flush=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    {"start": start, "freeze": freeze, "audit": audit, "checks": checks,
     "preflight": preflight, "record": record, "finalize": finalize}[sys.argv[1]]()
