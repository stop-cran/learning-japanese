"""Verify the bounded combined tree; the parent launcher retains runner.lock."""
import ast
import copy
import gzip
import hashlib
import io
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
L = C / "logs" / "cc53eba8-ebd4-461a-804c-9a559cb61644"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
D = V / "batch-100-combined-acceptance-760"
HEAD = "b33b4553255ab17dc72c09e65888f6584aa8d79d"
MAIN = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
VERSION = "606c836e4be33ba9"
CHAR = "\u5275"
STAGE = "batch-100-combined-main-accepted-awaiting-owner-publication"
NEXT = (
    "SAME100 publication-only checkpoint next, no101. Read docs/n1-sources/execution-760.json "
    "and docs/n1-reviews/batch-100-combined-acceptance-760.json at signed LOCAL review-closed HEAD. "
    "Fresh origin/main716c610153234e8d2240dcf528de3ef83b654b27 already ancestor; "
    "nonrewriting merge Already up to date; no incoming/runtime/teaching changes. "
    "Fresh full Python tests/validate/regenerated manifest/vocabulary/budgets/frozen inputs/"
    "complete dictionary packets/full baseline/exact membership/all readings/pinned geometry/"
    "all mapped links/quiz declarations/font provenance and every compiled757 archive payload "
    "verified, version606c836e4be33ba9/all8453 runtime hashes. "
    "Qualified Android signedbf30cdead8515739bc0e671d57a54b9a3109dd46 unchanged. "
    "HOST756 three RealContentTest plus one RareHanTest/no skips and corrected native758 "
    "TWO named terminalcase0 successes inherited, not rerun: ContentSyncONCE/1123kanji/"
    "5073words/132N1/zero problems/both epochs1,2464direct/1760NONTRANSITIVEneighbor/"
    "2304preservedwordguards/64actualbuilderchoices,22sampledlabels. "
    "Original-session759 rendered confirmations closed serially with actual models "
    "claude-opus-5.5 then gpt-6.1-sol;17serialcalls/15images each/zerooverlaps; "
    "exact-byte Claude coverage addendum preserved, no fresh blind credit. "
    "N753-fallback-establish resolved semantically755/mechanically758/rendered759; "
    "eleven direct symmetric NONTRANSITIVE guards, default silkworm fallback; "
    "N1 TWOcurated剣倹 plusfallback because験N4; no mask/relevel/futurepool guarantee. "
    "Six full readings/order preserved, selectedソウ/つく.る, source-onlyショウ/"
    "けず.しける allocation explicitlyUNVERIFIED/unselected. F1/C1-establish/"
    "H1-initial resolved andH1-woundwithdrawn;創/初 conservative, not proven historical "
    "live failure/universal synonymy. OptionalO1-O4/wrapping nonblocking. "
    "No new word;創作N2/作るN5/13and5wordguards preserved; fiveallmappedpairs/"
    "tendirections/oneactivatedbaselinepair/threeexactreusedchanges; twelve pinned paths. "
    "21Han/fourproductionfamily readability inherited759; cmap is not readability/"
    "fallbackfaceproof. Reduced contact sheets not all46fullresolutionPNGs; "
    "Back/offline relies on758execution; injectedstrokes/seededdue/shapeonly notMLKit/"
    "humanmastery. API35emulator notphone. "
    "NEXT fresh main fetch; if advanced nonrewritingmerge/surgicalreconciliation/"
    "regenerate/revalidate actualcombinedtree/independent changedteaching review/"
    "applicableHOST-native-rendered reassessment. Then normally signed owner-command-scoped "
    "stop-cran fastforwardpush/noauthswitch/noforcepush/noamend, exactremoteSHA/"
    "terminalgreenCI/EVERYimmutableGitHubZIP runtimeentryhash/manifest equality/"
    "18000entries/42MiBcompressed80MiBinflated56MiBretained/perfilepathmedia/"
    "verifiedownerissue/durablepublication ledgers BEFORE101/countingdelivery. "
    "Published126/1228,remaining1102,lastpublished716c6101 unchanged until verified delivery. "
    "SixearlierN2placements保案派第策結 separate, neverduplicate/relevel. "
    "Physicalphone/generalrelease/whole-set outstanding. Parent5920 ownsrunner.lock: "
    "verifyliveancestry/decodedlauncher/exactsession/checkpoint/signedheads/whollyclean; "
    "NOchildacquire/delete/unlock/readprobe. Approvedcontrol/committedsource/frozeninputs "
    "only, not optionalhistoricalsessionhelpers. Preserve/report/yield actualnewdenial/"
    "signinghang/uncertainownership. No secondrunner/unreviewedpush/101."
)
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data, replace=False):
    assert replace or not path.exists(), path
    temp = path.with_suffix(path.suffix + ".760.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    os.replace(temp, path)
    assert load(path) == data


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(root), *args],
        encoding="utf-8").strip()


def preflight(label, head=HEAD):
    assert not os.environ.get("GH_TOKEN") and not os.environ.get("GITHUB_TOKEN")
    subprocess.run(["pwsh", "-NoProfile", "-NonInteractive", "-File",
                    str(C / "preflight-760.ps1"), "-ExpectedHead", head,
                    "-ReceiptName", f"preflight-760-{label}.json"], check=True)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("merge-base", MAIN, head) == MAIN


def runtime():
    from build_manifest import build_manifest, sha256
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R) and manifest["contentVersion"] == VERSION
    preparation = load(S / "execution-757.json")["preparation"]
    path = Path(preparation["archive"])
    assert path.is_relative_to(C) and sha(path.read_bytes()) == preparation["archiveSha256"]
    binary_sections = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) and len(names) <= 18000
        assert all(not n.startswith(("/", "\\")) and "\\" not in n and ":" not in n
                   and ".." not in PurePosixPath(n).parts for n in names)
        manifests = [n for n in names if n == "manifest.json" or n.endswith("/manifest.json")]
        assert len(manifests) == 1
        prefix = manifests[0][:-len("manifest.json")]
        assert json.loads(archive.read(manifests[0])) == manifest
        count = retained = media = 0
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, digest in entries.items():
                local = (R / name).read_bytes()
                archived = archive.read(prefix + name)
                assert (sha(local) if section in binary_sections else sha256(R / name)) == digest
                if section not in binary_sections:
                    local = local.replace(b"\r\n", b"\n")
                    archived = archived.replace(b"\r\n", b"\n")
                assert archived == local and sha(archived) == digest, name
                original_size = archive.getinfo(prefix + name).file_size
                limit = (150 * 1024 if section in {"images", "listeningTaskImages"} else
                         512 * 1024 if section in {"audio", "listeningTaskAudio"} else 2 * 1024**2)
                assert original_size <= limit
                retained += original_size
                if section in {"listeningTaskAudio", "listeningTaskImages"}:
                    media += original_size
                count += 1
        retained += archive.getinfo(manifests[0]).file_size
        inflated = sum(info.file_size for info in archive.infolist())
        assert count == 8453 and path.stat().st_size <= 42 * 1024**2
        assert inflated <= 80 * 1024**2 and retained <= 56 * 1024**2 and media <= 20 * 1024**2
    return {"runtimeHashesVerified": count, "contentVersion": VERSION,
            "manifestSha256": sha((R / "manifest.json").read_bytes()),
            "manifestFresh": True, "compiled757ArchiveSha256": preparation["archiveSha256"],
            "everyNativeArchivePayloadEqual": True, "runtimeChanged": False,
            "compiledArchiveEntries": len(names), "compiledArchiveCompressedBytes": path.stat().st_size,
            "compiledArchiveInflatedBytes": inflated, "compiledArchiveRetainedBytes": retained,
            "compiledArchiveTaskMediaBytes": media, "safePathsAndPerFileMediaGuards": True}


def start():
    state = load(C / "progress.json")
    assert state == load(L / "checkpoint-full.json")
    assert (state["checkpoint"], state["batch"], state["status"]) == (759, "100", "continue")
    request = (L / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    a, b = embedded["execution759CoordinatorCheckpoint"], state["execution759CoordinatorCheckpoint"]
    assert a.keys() == b.keys()
    assert all(v == b[k] for k, v in a.items() if k != "recordedAt")
    assert datetime.fromisoformat(a["recordedAt"]) == datetime.fromisoformat(b["recordedAt"])
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain", "--untracked-files=all")
    assert git("rev-parse", "origin/main") == MAIN and git("merge-base", MAIN, HEAD) == MAIN
    role = load(L / "preflight-760.json")
    assert role["sessionId"] == L.name and role["liveParentPid"] == 5920 and not role["lockTouched"]
    save(L / "progress-before-760.json", state)
    starting = {
        "execution": 760, "batch": "100", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME100 combined-current-main acceptance and normally signed LOCAL checkpoint only; no publication/native rerun/reviewer/101.",
        "request": {"sha256": sha(request), "bytes": len(request), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request decoded and complete checkpoint parsed; operative contract, entire approved issue and final759 directly inspected. Historical middle parsed, not freshly semantically rereviewed."},
        "runnerPreflight": role, "runtime": runtime(),
        "artifactPathPreflight": "Approved committed source/evidence, frozen workspace inputs and durable control helpers only; optional historical-session recipes not accessed.",
        "actualNewPermissionDenials": [],
    }
    save(L / "starting-state-760.json", starting)
    after = copy.deepcopy(state)
    after["execution760StartingState"] = starting
    after.update(stage="batch-100-combined-main-acceptance-in-progress",
                 nextAction=starting["scope"], blocker=None)
    assert all(after[k] == v for k, v in state.items() if k not in {"stage", "nextAction", "blocker"})
    assert load(C / "progress.json") == state
    save(C / "progress.json", after, replace=True)
    print("SAME100 starting scope persisted; complete request parsed and full history preserved.", flush=True)


def canonical(e):
    return e.tag, tuple(sorted(e.attrib.items())), (e.text or "").strip(), tuple(canonical(c) for c in e)


def source_audit():
    from audit_n1_batch import audit
    from audit_n1_pilot import metadata
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert, KANJIVG_REVISION
    result = audit(R, "100")
    ledger = load(S / "batch-100-progress.json")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
        inputs[name] = raw
    jm = inputs["n1-implementation-JMdict_e.gz"]
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    packets = []
    compact_names = ["batch-100-full-family-reading.txt.gz", "batch-100-comparison-full-family-reading.txt.gz",
                     "batch-100-correction-full-family-reading.txt.gz", "batch-100-fallback-754-full-family-reading.txt.gz"]
    packet_rows = list(ledger["dictionaryPackets"])
    if not any(row["xml"] == "batch-100-fallback-754-jmdict.xml" for row in packet_rows):
        packet_rows.append({"selection": "batch-100-fallback-754-selection.json",
                            "xml": "batch-100-fallback-754-jmdict.xml"})
    assert len(packet_rows) == len(compact_names) == 4
    for packet, compact in zip(packet_rows, compact_names):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        assert [canonical(ET.fromstring(line)) for line in gzip.decompress(
            (S / compact).read_bytes()).decode("utf-8").splitlines()] == [
                canonical(e) for e in ET.fromstring(raw)]
        packets.append({"xml": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    frozen_kd = {e.findtext("literal"): canonical(e) for e in ET.fromstring(kd).findall("character")}
    records = {}
    for name in ["batch-100-kanjidic2.xml", "batch-100-comparison-kanjidic2.xml",
                 "batch-100-correction-kanjidic2.xml", "batch-100-fallback-754-kanjidic2.xml.gz"]:
        raw = (S / name).read_bytes()
        root = ET.fromstring(gzip.decompress(raw) if name.endswith(".gz") else raw)
        for e in root.findall("character"):
            char = e.findtext("literal")
            assert canonical(e) == frozen_kd[char]
            records[char] = canonical(e)
    meta = metadata(R, f"kanji/{CHAR}.md")
    expected = copy.deepcopy(load(S / "batch-100-authoring-plan.json")["proposedMetadata"])
    expected["quiz_exclusions"] += list("\u8a2d\u521d\u6a39")
    assert meta == ledger["proposedMetadata"] == expected
    assert meta["quiz_exclusions"] == list("\u4f5c\u9020\u59cb\u5143\u539f\u672c\u7dd2\u7523\u8a2d\u521d\u6a39")
    guards = ledger["quizAudit"][CHAR]["directExclusions"]
    assert [row["kanji"] for row in guards] == meta["quiz_exclusions"]
    for row in guards + ledger["quizAudit"][CHAR]["meaningDecisions"]:
        assert metadata(R, f"kanji/{row['kanji']}.md")["title"] == row["label"]
    assert not set(meta["distractors"]) & set(meta["quiz_exclusions"])
    previous_audit = load(S / "batch-100-draft-audit.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in load(S / "baseline-inventory.json")["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            baseline_meta = copy.deepcopy(info["metadata"])
            if name in previous_audit["baselineMetadataExceptions"]:
                baseline_meta["quiz_exclusions"] = previous_audit["baselineMetadataExceptions"][name]
            if name in previous_audit["baselineKanjiDistractorException"]:
                baseline_meta["distractors"] = previous_audit["baselineKanjiDistractorException"][name]
            assert metadata(R, name) == baseline_meta, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha((R / name).read_bytes()) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and named[110] == CHAR
    chars = {p.stem for p in (R / "kanji").glob("*.md")}
    before_manifest = json.loads(git("show", f"{MAIN}:manifest.json"))
    old_chars = {Path(p).stem for p in before_manifest["files"] if p.startswith("kanji/")}
    assert chars - old_chars == {CHAR} and not old_chars - chars
    assert metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in "\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50")
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/\u5275\u4f5c.md"}
    plan = load(S / "batch-100-authoring-plan.json")
    pairs = {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert pairs == {(row["kanji"], row["article"]) for row in plan["supportMappings"]}
    assert len(pairs) == 5
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / f"kanji/{char}.md").read_text(encoding="utf-8")
    for name, level, n in [("words/\u5275\u4f5c.md", 2, 13), ("words/\u4f5c\u308b.md", 5, 5)]:
        m = metadata(R, name)
        assert m["jlpt"] == level and len(m["quiz_exclusions"]) == n
        assert m["quiz_exclusions"] == ledger["wordQuizAudit"]["preservedOriginalExclusions"][name]
    svg = (S / "batch-100-kanjivg.svg").read_bytes()
    proof = load(S / "batch-100-stroke-evidence.json")
    assert sha(svg) == proof["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == proof["gitBlob"]
    assert svg == (C / "inputs" / "n1-05275-70a0b7ae.svg").read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = load(R / "strokes" / f"{CHAR}.json")
    assert geometry == convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 12
    assert all(s["id"] == i and len(s["points"]) == 16 and
               all(len(p) == 2 and all(math.isfinite(v) for v in p) for p in s["points"])
               for i, s in enumerate(geometry["strokes"], 1))
    text = (R / "kanji" / f"{CHAR}.md").read_text(encoding="utf-8")
    text += "".join(row["after"] for row in ledger["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert len(han) == 21
    fonts = []
    for row in load(S / "batch-100-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap]})
    result.update(execution=760, frozenInputsVerified=len(inputs), packets=packets,
                  completeRawCharacterRecordsVerified=len(records),
                  originalBaselineMetadataAndStrokesPreserved=counts,
                  exactNewMember=CHAR, allMappedPairs=5, directedLinksVerified=10,
                  directKanjiGuardPairs=11, wordExclusionsPreserved=[13, 5],
                  pinnedGeometryExactlyRegenerated=True, generatedStrokes=12,
                  actualHan=han, fonts=fonts, actualHanCount=21,
                  currentCounts={"kanji": len(chars), "words": len(list((R / "words").glob("*.md"))),
                                 "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in chars),
                                 "namedSourceMembersPresent": len(chars & set(named))},
                  sourceOnlyLexicalAllocation="UNVERIFIED/unselected, no fresh linguistic claim",
                  runtime=runtime(), freshLinguisticOrNativeEvidence=False)
    assert result["currentCounts"] == {"kanji": 1123, "words": 5073, "n1Labels": 132,
                                      "namedSourceMembersPresent": 137}
    save(L / "combined-source-audit-760.json", result)
    print("Fresh frozen sources/full baseline/membership/readings/quiz/links/strokes/font provenance audit passed.", flush=True)


def checks():
    preflight("checks")
    merged = subprocess.run(["git", "-C", str(R), "merge", "--no-edit", "origin/main"],
                            capture_output=True, text=True, encoding="utf-8")
    save(L / "main-integration-760.json", {
        "command": ["git", "merge", "--no-edit", "origin/main"], "exitCode": merged.returncode,
        "stdout": merged.stdout, "stderr": merged.stderr, "main": MAIN, "head": HEAD})
    assert merged.returncode == 0 and git("rev-parse", "HEAD") == HEAD
    assert not git("diff", HEAD + "...origin/main", "--name-only")
    for name, args in [
        ("python-tests", ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"]),
        ("validate", ["tools\\validate.py"]), ("manifest", ["tools\\build_manifest.py"]),
        ("vocabulary", ["tools\\grammar_vocabulary.py", "check"]),
        ("budget", ["tools\\check_content_budget.py"]),
        ("batch-audit", ["tools\\audit_n1_batch.py", "--batch", "100"]),
    ]:
        command = [sys.executable, "-X", "utf8", "-B", *args]
        with (L / f"{name}-760.txt").open("x", encoding="utf-8") as output:
            result = subprocess.run(command, cwd=R, stdout=output, stderr=subprocess.STDOUT)
        save(L / f"{name}-exit-760.json", {"command": command, "exitCode": result.returncode})
        assert result.returncode == 0, name
        print(name, "passed", flush=True)
    preflight("after-python")
    source_audit()


def inherit():
    initial = load(V / "batch-100-reconciliation.json")
    semantic = load(V / "batch-100-fallback-confirmation-755-reconciliation.json")
    rendered = load(V / "batch-100-rendered-759-reconciliation.json")
    host = load(S / "execution-756.json")
    native = load(S / "execution-758.json")
    assert initial["serialReviewerProcessesVerified"] and initial["allInternalToolsSerial"]
    assert initial["allAssignedRangesReturned"] and initial["initialReviewsComplete"]
    assert rendered["independentRenderedReviewClosed"] and not rendered["freshBlindReviewCredit"]
    assert rendered["serialProcessesAndInternalToolsVerified"] and rendered["findings"] == []
    assert semantic["status"] == "resolved" and semantic["bothReviewersAgreeNoOtherActionableSampledAmbiguity"]
    receipt_hashes = 0
    for assignments in (initial["processes"], initial["confirmations"],
                        semantic["confirmations"], rendered["confirmations"]):
        previous = None
        for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
            row = assignments[label]
            assert row["actualModels"] == [model] and row["exitCode"] == 0
            assert row["sessionId"] == initial["processes"][label]["sessionId"]
            if previous:
                assert datetime.fromisoformat(previous) < datetime.fromisoformat(row["startedAt"])
            previous = row["completedAt"]
            assert sha((V / row["report"]).read_bytes()) == row["reportSha256"]
            raw_name = row.get("rawExecution", row["report"].replace(".md", ".jsonl"))
            raw_path = V / raw_name
            if not raw_path.exists():
                raw_path = raw_path.with_suffix(raw_path.suffix + ".gz")
            raw = raw_path.read_bytes()
            if raw_path.suffix == ".gz":
                raw = gzip.decompress(raw)
            assert sha(raw) == row["rawExecutionSha256"]
            detail = load(V / row["execution"])
            assert detail["exitCode"] == 0 and not detail["observedToolOverlaps"]
            assert not detail.get("unfinishedTools", [])
            assert row.get("observedToolOverlaps", row.get("internalToolOverlaps", 0)) == 0
            receipt_hashes += 3
    addendum = load(V / "batch-100-rendered-759-claude-coverage-addendum.json")
    assert addendum["exactRawWholeFileBytesEqual"] and addendum["allAssignedResourcesReturned"]
    assert addendum["originalExecutionSha256"] == sha(
        (V / "batch-100-rendered-759-claude-execution.json").read_bytes())
    provenance = load(V / "batch-100-rendered-759-provenance.json")
    for row in provenance["images"]:
        path = Path(row["path"])
        assert path.is_relative_to(R) and sha(path.read_bytes()) == row["sha256"]
        receipt_hashes += 1
    for row in load(R / native["artifactIndex"]):
        path = R / row["archive"]
        assert sha(path.read_bytes()) == row["sha256"]
        raw = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
        assert sha(raw) == row["sourceSha256"]
        receipt_hashes += 1
    assert host["qualifiedAndroidHead"] == APP and host["totalTests"] == 4
    assert all(host[k] == 0 for k in ("failures", "errors", "skipped"))
    assert host["allTestsFreshAfterCommandStart"]
    for row in host["tests"]:
        path = R / row["archive"]
        assert sha(path.read_bytes()) == row["sha256"]
        xml = ET.parse(path).getroot()
        assert int(xml.attrib["tests"]) == row["tests"]
        assert all(xml.attrib[k] == "0" for k in ("skipped", "errors", "failures"))
        assert {t.attrib["name"] for t in xml.findall("testcase")} == set(row["caseNames"])
        assert Path(row["fixtureRoot"]) == R
        assert (Path(row["moduleWorkingDirectory"]) / ".." / ".." / "learning-japanese").resolve() == R
        assert sha((R / row["testSourceArchive"]).read_bytes()) == row["testSourceSha256"]
        receipt_hashes += 2
    assert native["qualifiedAndroidHead"] == APP and native["nativeMechanicalChecksPassed"]
    assert native["nativeAttempt"]["terminalSuccessCases"] == 2
    assert native["nativeAttempt"]["ownedHelperStopped"] and native["nativeAttempt"]["ownedQemuStopped"]
    raw_dir = V / "batch-100-native-758" / "native"
    text = gzip.decompress((raw_dir / "instrumentation.txt.gz").read_bytes()).decode("utf-8-sig")
    assert text.count("INSTRUMENTATION_STATUS_CODE: 0") == 2 and "OK (2 tests)" in text
    for name in (
        "N1Batch100Glyph757Test", "N1Batch100Article757Test",
        "creationLookalikesAndAllTwentyOneHanAcrossFourProductionFamilies",
        "fullSingleImportCreationDirectGuardsTwoCuratedKeysFivePairsTwelveStrokesOfflineAndBack",
    ):
        assert name in text
    assert all(f"INSTRUMENTATION_STATUS_CODE: {n}" not in text for n in (-2, -3, -4))
    route = json.loads(gzip.decompress((raw_dir / "n1-100-article-route.json.gz").read_bytes()))
    assert route["passed"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"],
            route["acceptedReadingParserEpoch"], route["acceptedMeaningParserEpoch"]) == (1123, 5073, 132, 0, 1, 1)
    assert route["contentVersion"] == VERSION
    assert route["kanjiQuizExclusions"] == list("\u4f5c\u9020\u59cb\u5143\u539f\u672c\u7dd2\u7523\u8a2d\u521d\u6a39")
    assert route["quizOnKeys"] == ["\u305d\u3046"] and route["quizKunKeys"] == ["\u3064\u304f\u308b"]
    assert route["touchInjectedReferenceStrokes"] == 12
    assert route["offline"] and route["reciprocalLinkAndSystemBack"]
    assert route["twoCuratedKeysPersistedGoodAndDone"]
    assert len(route["kanjiDirectGuardChecks"]) == native["kanjiDirectGuardChecks"] == 2464
    assert native["nontransitiveNeighborChecks"] == 1760 and native["preservedWordGuardChecks"] == 2304
    assert len(route["productionBuilderN1AndAllExactChoices"]) == native["productionChoiceChecks"] == 64
    labels = {(o["kanji"], o["title"]) for row in route["productionBuilderN1AndAllExactChoices"]
              for o in row["options"]}
    assert len(labels) == 22 and ("\u6a39", "tree; establish") not in labels
    assert ("\u8695", "silkworm") in {(o["kanji"], o["title"]) for o in route["exactDefaultMeaningOptions"]}
    assert route["actualN1CuratedAvailable"] == 2 and route["actualN1FallbackOptions"] == 1
    assert not git("diff", native["archiveContentSnapshot"], HEAD, "--", "manifest.json")
    assert not git("diff", host["testedContentHead"], HEAD, "--", "manifest.json")
    for key in ("F1", "C1-establish", "H1-initial", "N753-fallback-establish"):
        assert rendered["reconciliation"][key]["status"] == "resolved"
    assert rendered["reconciliation"]["H1-wound"]["status"] == "withdrawn"
    return {
        "initialRecord": "docs/n1-reviews/batch-100-reconciliation.json",
        "semanticRecord": "docs/n1-reviews/batch-100-fallback-confirmation-755-reconciliation.json",
        "hostRecord": "docs/n1-sources/execution-756.json",
        "nativeRecord": "docs/n1-sources/execution-758.json",
        "renderedRecord": "docs/n1-reviews/batch-100-rendered-759-reconciliation.json",
        "receiptHashesReverified": receipt_hashes, "hostTests": 4, "hostSkipped": 0,
        "nativeTerminalCaseSuccesses": 2, "nativeFailuresOrSkips": 0,
        "kanjiDirectGuardChecks": 2464, "nontransitiveNeighborChecks": 1760,
        "preservedWordGuardChecks": 2304, "productionBuilderChoices": 64,
        "sampledLabels": 22, "actualN1CuratedAvailable": 2, "actualN1FallbackOptions": 1,
        "newHostRuns": 0, "newNativeRuns": 0, "newReviewers": 0, "newBlindReviewCredit": False,
        "justification": "No incoming changes; every runtime payload and manifest plus qualified Android HEAD exactly identical to756/758/759. No redundant heavy rerun or changed-teaching review needed.",
        "sourceOnlyReadingLimits": rendered["sourceOnlyReadingLimits"],
        "limits": rendered["limits"],
    }


def record():
    preflight("record")
    text = (L / "python-tests-760.txt").read_text(encoding="utf-8")
    count = int(re.search(r"^Ran (\d+) tests in ", text, re.M)[1])
    assert count == 377 and re.search(r"^OK$", text, re.M) and "skipped=" not in text
    assert (L / "validate-760.txt").read_text(encoding="utf-8").strip() == "0 error(s)"
    for name in ("python-tests", "validate", "manifest", "vocabulary", "budget", "batch-audit"):
        assert load(L / f"{name}-exit-760.json")["exitCode"] == 0
    from check_content_budget import MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED
    assert (MAX_ENTRIES, MAX_COMPRESSED, MAX_INFLATED, MAX_RETAINED) == (
        18000, 42 * 1024**2, 80 * 1024**2, 56 * 1024**2)
    budget = ast.literal_eval((L / "budget-760.txt").read_text(encoding="utf-8"))
    for key, limit in [("entries", MAX_ENTRIES), ("localZipBytes", MAX_COMPRESSED),
                       ("inflatedBytes", MAX_INFLATED), ("retainedBytes", MAX_RETAINED)]:
        assert budget[key] <= limit
    inherited = inherit()
    D.mkdir()
    receipts = []
    sources = [*sorted(L.glob("*-760.txt")), *sorted(L.glob("*-760.json")),
               *sorted(L.glob("preflight-760*.json")), Path(__file__), C / "preflight-760.ps1",
               C / "post-batch-100-combined-760.ps1",
               C / "runner-lock-role-notes.txt", C / "authoring-artifact-path-notes.txt"]
    for path in dict.fromkeys(sources):
        if path.name == "progress-before-760.json":
            continue
        raw = path.read_bytes()
        compressed = path.suffix == ".txt"
        target = D / (path.name + (".gz" if compressed else ".txt" if path.suffix == ".ps1" else ""))
        assert not target.exists(), target
        target.write_bytes(gzip.compress(raw, mtime=0) if compressed else raw)
        assert (gzip.decompress(target.read_bytes()) if compressed else target.read_bytes()) == raw
        receipts.append({"source": str(path), "archive": target.relative_to(R).as_posix(),
                         "sourceSha256": sha(raw), "archiveSha256": sha(target.read_bytes()),
                         "losslessGzip": compressed})
    evidence = {
        "schemaVersion": 1, "execution": 760, "batch": "100", "stage": STAGE,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "startingState": load(L / "starting-state-760.json"),
        "combinedTestedSnapshot": HEAD, "integratedMain": MAIN, "qualifiedAndroidHead": APP,
        "mainAlreadyAncestor": True, "incomingChanges": [], "substantiveTeachingChanged": False,
        "runtime": runtime(), "checks": {
            "pythonTests": count, "validatorErrors": 0, "manifestFresh": True,
            "vocabulary": (L / "vocabulary-760.txt").read_text(encoding="utf-8").strip(),
            "vocabularyLimit": "Existing pilot coverage2122/2431 is reported, not silently closed or represented as full coverage.",
            "localArchiveBudgets": budget, "freshPythonExecution": True,
            "inheritedAndroidTests": 4, "androidSkipped": 0, "freshAndroidExecution": False,
            "actualResolvedContentRoot": str(R)},
        "sourceAudit": load(L / "combined-source-audit-760.json"),
        "inheritedAcceptance": inherited, "receipts": receipts,
        "reviewClosed": [CHAR], "published": [], "runtimeAccepted": True,
        "runtimeAcceptanceScope": "Local bounded compatible-client owner testing, not public delivery/general release.",
        "runtimePublished": False, "actionableRemainingFindings": 0,
        "consequentialUnresolvedUnqualifiedTeachingClaims": 0,
        "explicitlyUnverifiedSourceOnlyReadings": ["\u30b7\u30e7\u30a6", "\u3051\u305a.\u3057\u3051\u308b"],
        "changedGuardSemanticReviewClosed": True, "independentRenderedReviewClosed": True,
        "newBlindReviewCredit": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "limits": [
            "Compatible kanji-exclusion-aware and curated-reading client required; old clients ignore both fields.",
            "Direct symmetric nontransitive guards and sampled22labels/64choices, not exhaustive future semantics.",
            "HOST756/native758/original-session confirmations759 inherited, not fresh runs or fresh blind review.",
            "Source-onlyショウ/けず.しける allocation remains explicitlyUNVERIFIED/unselected; full metadata preserved.",
            "Reduced contact sheets not full-resolution reads of every PNG; actual fallback face unidentified.",
            "Injected reference strokes/seeded due states/shape-only drawing are not MLKit or human mastery evidence.",
            "Physical-phone/general-release and whole-set acceptance outstanding.",
            "Fresh-main check/normal owner fast-forward/terminal CI/every immutable public ZIP hash and budgets/verified issue remain pending before publication or101.",
        ],
        "nextAction": NEXT,
    }
    save(S / "execution-760.json", evidence)
    save(V / "batch-100-combined-acceptance-760.json", evidence)
    ledger_path = S / "batch-100-progress.json"
    ledger = load(ledger_path)
    assert "preCombinedAcceptance760" not in ledger
    ledger["preCombinedAcceptance760"] = {
        k: copy.deepcopy(ledger.get(k)) for k in
        ("status", "reviewClosed", "limits", "nextAction", "pendingGates", "runtimeAccepted")}
    ledger.update(status=STAGE, reviewClosed=[CHAR], published=[], runtimeAccepted=True,
                  runtimePublished=False, limits=evidence["limits"], nextAction=NEXT)
    ledger["combinedAcceptance760"] = {
        "evidence": "docs/n1-sources/execution-760.json",
        "reviewRecord": "docs/n1-reviews/batch-100-combined-acceptance-760.json",
        "contentVersion": VERSION, "mainAlreadyAncestor": True, "incomingChanges": [],
        "freshPythonTests": count, "inheritedHostTests": 4, "inheritedHostSkipped": 0,
        "inheritedNativeTerminalSuccesses": 2, "native758StillExact": True,
        "semantic755AndRendered759Closed": True, "runtimeAccepted": True, "runtimePublished": False,
        "historicalLimitDisposition": "Earlier pending/draft states preserved as historical; superseded only for bounded current compatible-client local acceptance."}
    ledger["pendingGates"] = [
        "Fresh main fetch; if advanced nonrewriting merge/reconcile/regenerate/revalidate actual combined tree and independently review changed teaching/reassess native scope.",
        "Normal signed owner fast-forward, exact remote SHA, terminal green CI, every immutable GitHub ZIP entry/hash under unchanged guards and verified owner issue/durable publication checkpoint before101."]
    save(ledger_path, ledger, replace=True)
    print("Combined-current-main local acceptance archived; no runtime edit or publication.", flush=True)


def finish():
    head = git("rev-parse", "HEAD")
    preflight("final", head)
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    evidence = load(S / "execution-760.json")
    assert evidence == load(V / "batch-100-combined-acceptance-760.json")
    expected = {row["archive"] for row in evidence["receipts"]} | {
        "docs/n1-sources/execution-760.json", "docs/n1-reviews/batch-100-combined-acceptance-760.json",
        "docs/n1-sources/batch-100-progress.json"}
    assert set(git("diff", "--name-only", HEAD, head).splitlines()) == expected
    for row in evidence["receipts"]:
        assert sha((R / row["archive"]).read_bytes()) == row["archiveSha256"]
    assert runtime() == evidence["runtime"]
    inherit()
    posted, comment = load(L / "issue-760-posted.json"), load(L / "issue-760-reread.json")
    bodypath = C / "batch-100-combined-760-issue-body.txt"
    body = bodypath.read_bytes().decode("utf-8")
    assert comment["user"]["login"] == posted["author"] == "stop-cran"
    assert comment["body"] == body and head in body and sha(bodypath.read_bytes()) == posted["bodySha256"]
    assert comment["html_url"] == posted["url"]
    before, state = load(L / "progress-before-760.json"), load(C / "progress.json")
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(state[k] == v for k, v in before.items() if k not in changed)
    checkpoint = {
        "schemaVersion": 1, "execution": 760, "checkpoint": 760, "batch": "100",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "savedCommit": head,
        "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-760.json",
        "reviewRecord": "docs/n1-reviews/batch-100-combined-acceptance-760.json",
        "combinedTestedSnapshot": HEAD, "integratedMain": MAIN, "qualifiedAndroidHead": APP,
        **runtime(), "freshPythonTests": 377, "inheritedHostTests": 4, "inheritedHostSkipped": 0,
        "native758StillExact": True, "inheritedNativeTerminalSuccesses": 2,
        "freshHostOrNativeExecuted": False, "newReviewers": 0, "incomingChanges": [],
        "changedGuardSemanticReviewClosed": True, "independentRenderedReviewClosed": True,
        "reviewClosed": [CHAR], "published": [], "runtimeAccepted": True,
        "runtimeAcceptanceScope": evidence["runtimeAcceptanceScope"], "runtimePublished": False,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": comment["html_url"], "ownerIssueAuthorAndExactBodyVerified": True,
        "nextAction": f"SAME100 signed LOCAL review-closed HEAD{head}. " + NEXT,
        "historicalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "blocker": None,
    }
    after = copy.deepcopy(state)
    assert "execution760CoordinatorCheckpoint" not in after
    after["execution760CoordinatorCheckpoint"] = checkpoint
    for key in changed:
        after[key] = checkpoint[key]
    assert all(after[k] == v for k, v in before.items() if k not in changed)
    save(L / "checkpoint-760-summary.json", checkpoint)
    assert load(C / "progress.json") == state
    save(C / "progress.json", after, replace=True)
    print(json.dumps({"checkpoint": 760, "status": "continue", "savedCommit": head,
                      "historicalRootKeysCompared": len(before),
                      "allOriginalHistoricalValuesPreserved": True}), flush=True)


if __name__ == "__main__":
    {"start": start, "checks": checks, "record": record, "finish": finish}[sys.argv[1]]()
