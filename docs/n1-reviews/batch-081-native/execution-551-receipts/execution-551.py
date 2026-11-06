import hashlib
import gzip
import json
import shutil
import subprocess
import sys
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
LOGS = CONTROL / "logs" / "239df77c-7bf3-488c-bb17-2b6fbfbb1248"
HEAD = "739832b4ff3a00203ef345e1c03e77574d1545a0"
ANDROID = CONTROL.parent / "kanji-cards-android"
NATIVE = ROOT / "docs" / "n1-reviews" / "batch-081-native"
ATTEMPT = CONTROL / "artifacts" / "batch-081-native-attempt-1"
EVIDENCE = ROOT / "docs" / "n1-sources" / "execution-551.json"
NEXT = (
    "SAME081 two SERIAL original-family independent VISUAL confirmations ONLY, then persist/yield "
    "before integration/publication/082. Use signed execution551 native evidence, docs/n1-sources/"
    "execution-551.json, batch-081-native/attempt-1 original PNGs, visual-inspection-execution-551.json "
    "and image-index-execution-551.json. Original ClaudeOpus5.5 session5d197613-b9f7-4815-aa0f-25098fbf6825 "
    "and GPT6.1Sol session44f703a8-cc19-4e68-bd98-8fa94688e781 where possible; actual catalog/model/"
    "process evidence and complete original reports required, at most ONE active reviewer and "
    "no edits to frozen snapshot during reviews. Fresh551 BOTH native named cases terminal0/no skips "
    "on owned read-only API35 emulator5580 parent18020/qemu28948 stopped; owner5556 untouched. "
    "Production ContentSync exact full signed95a87783 archive ONCE:1093kanji5049words113N1/"
    "contentVersionf1dd5d8b9d2ff535/zeroProblems/acceptedepoch1. Full+Lite retain onヤ/kunい.る "
    "in order, selected onヤ and explicit empty kun, sole offeredや/good log/one-questionDone. "
    "Complete冶/冶金 plus exact added金bullet/twopairs/fourdirections/SystemBack/N1selection/"
    "meaning/sevenstroke injected trace then giveuprecall/offline passed.45originalPNGs/"
    "25distinctbytegroups inspected via five coordinator contact sheets at half resolution; "
    "three actual font panels additionally viewed at original resolution. All29Han/fourfamilies "
    "including冫/氵 fallback readable;116individual+4wholeword Paint records not120PNGreads or "
    "fallback-face proof. Table horizontal states collectively show labels/explanation; no "
    "single-frame-all-columns claim. Offline handwritingmodel unavailable; reference injection/"
    "shape-only/giveup recall NOT recognition/humanmemory/phone. Inherit textual closureb7bf953d, "
    "fresh549HOST3+1/no skips and550compile honestly; no rerun absent new concern. Preserve "
    "all source/lookup/citation/read-depth/review/process/denial/OOM/viewport/MLKit/phone/baseline "
    "limitations and FULL live history. Durablecontrolhelpers/approvedworkspaceinputs/committed "
    "packets only; optional historical session recipes skipped. HOST-only2GiBinit NEVER native; "
    "no app/guestheap/archiveguard increase. Later combined-currentmain non-rewritingintegration/"
    "revalidation/normalsigning/ownerfastforward/publicSHA/terminalgreenCI/EVERYimmutableZIP "
    "runtimehash/originalbudgets/verifiedownerissue60 mandatory. No unreviewedpush/nextbatch/"
    "secondrunner. Actualnewdenial or signinghang preserve/report/yield without retry/workaround. "
    "Published107/1228,remaining1121; local108th addition not delivered. CompatibleAndroidf9b59a2+ "
    "required; physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT).decode("utf-8").strip()


def start():
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 550
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 550 and progress["batch"] == "081"
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    before = LOGS / "progress-before-551.json"
    assert not before.exists()
    save(before, progress)
    record = {
        "schemaVersion": 1, "execution": 551, "batch": "081", "startingHead": HEAD,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME081 native execution and actual PNG inspection only; no reviewer, publication,082 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed; operative contract, complete issue and final550 inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": str(CONTROL / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "native-execution-preparing",
        "manifestSha256": sha(ROOT / "manifest.json"),
    }
    progress["execution551StartingState"] = record
    progress["stage"] = "native-execution-in-progress"
    save(CONTROL / "progress.json", progress)
    save(LOGS / "starting-state-551.json", record)
    print("Starting scope persisted; complete request parsed; full live history preserved.")


def record():
    starting = load(LOGS / "starting-state-551.json")
    native = load(CONTROL / "batch-081-native-attempt-1-execution.json")
    visual = load(CONTROL / "batch-081-native-visual-inspection.json")
    preparation = load(ROOT / "docs" / "n1-sources" / "batch-081-native-fixture-verification.json")
    assert git("rev-parse", "HEAD") == HEAD and not git("status", "--porcelain")
    assert not subprocess.check_output(["git", "-C", str(ANDROID), "status", "--porcelain"])
    assert native["passed"] and native["failure"] is None and native["adbExitCode"] == 0
    assert native["terminalSuccessCases"] == 2 and len(native["terminalCases"]) == 2
    assert {(c["class"].split(".")[-1], c["test"], c["status"]) for c in native["terminalCases"]} == {
        ("N1Batch081GlyphTest", "smeltingLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies", 0),
        ("N1Batch081ArticleTest", "fullSingleImportOfflineSmeltingTwoReciprocalPairsCuratedOnDrawingAndSystemBack", 0),
    }
    assert native["ownedHelperStopped"] and native["ownedQemuStopped"] and native["stopAdbExitCode"] == 0
    assert (native["parentEmulatorPid"], native["qemuPid"]) == (18020, 28948)
    assert not any(native[k] for k in ("hostHeapInitUsed", "guestOrAppHeapChanged", "guardsChanged"))
    route = load(ATTEMPT / "n1-081-article-route.json")
    raster = load(ATTEMPT / "n1-081-font-raster.json")
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"]) == (1093, 5049, 113, 0)
    assert route["acceptedReadingParserEpoch"] == 1 and not route["phoneEvidence"]
    assert route["contentSnapshot"] == preparation["contentSnapshot"]
    assert route["contentVersion"] == preparation["contentVersion"] == "f1dd5d8b9d2ff535"
    for key in ("fullOnyomi", "fullProjectionOnyomi", "liteQuizOnyomi", "fullProjectionQuizOnyomi"):
        assert route[key] == ["ヤ"]
    for key in ("fullKunyomi", "fullProjectionKunyomi"):
        assert route[key] == ["い.る"]
    for key in ("quizKunKeys", "liteQuizKunyomi", "fullProjectionQuizKunyomi"):
        assert route[key] == []
    assert route["quizOnKeys"] == ["や"]
    assert route["touchInjectedReferenceStrokes"] == 7
    assert route["mappedReciprocalPairs"] == 2 and route["directedLinkTransitions"] == 4
    for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedOnPersistedGoodAndDone", "drawingTraceThenRecall", "drawingGradeRecordedOnNext"):
        assert route[key], key
    assert (len(raster["rows"]), raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (120, 116, 4, 3)
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        rows = [r for r in raster["rows"] if r["font"] == font]
        assert {r["character"] for r in rows if "character" in r} == set(preparation["plannedGlyphs"])
        assert all(r["hasGlyph"] for r in rows if "character" in r)
        assert {r["word"] for r in rows if "word" in r} == {"冶金"}
    groups = defaultdict(list)
    for path in sorted(ATTEMPT.glob("*.png")):
        groups[sha(path)].append(path.name)
    assert sum(map(len, groups.values())) == 45 and len(groups) == 25
    index = {
        "originalPngCount": 45, "distinctByteGroups": 25, "inspectionMethod": visual["method"],
        "groups": [{"sha256": digest, "contactSheetRepresentative": names[0], "originals": names}
                   for digest, names in groups.items()],
    }
    manifest = load(ROOT / "manifest.json")
    assert sha(Path(native["testApk"])) == native["testApkSha256"]
    assert sha(Path(native["appApk"])) == native["appApkSha256"]
    verified = 0
    with zipfile.ZipFile(preparation["archive"]) as archive:
        assert sha(Path(preparation["archive"])) == preparation["archiveSha256"] == native["archiveSha256"]
        manifest_name, = (n for n in archive.namelist() if n.endswith("/manifest.json") or n == "manifest.json")
        prefix = manifest_name[:-len("manifest.json")]
        assert json.loads(archive.read(manifest_name)) == manifest
        retained = len(archive.read(manifest_name))
        for section, entries in manifest.items():
            if not isinstance(entries, dict):
                continue
            for name, expected in entries.items():
                raw = archive.read(prefix + name)
                binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                normalized = raw if binary else raw.replace(b"\r\n", b"\n")
                current = (ROOT / name).read_bytes()
                assert normalized == (current if binary else current.replace(b"\r\n", b"\n")), name
                assert hashlib.sha256(normalized).hexdigest() == expected, name
                verified += 1
                retained += len(raw)
        assert verified == 8369
        assert len(archive.infolist()) == preparation["zipEntries"] < 18000
        assert Path(preparation["archive"]).stat().st_size < 42 * 1024**2
        assert sum(i.file_size for i in archive.infolist()) == preparation["inflatedBytes"] < 80 * 1024**2
        assert retained == preparation["retainedBytes"] < 56 * 1024**2
    target = NATIVE / "attempt-1"
    assert not target.exists()
    shutil.copytree(ATTEMPT, target)
    copied = []
    for path in sorted(target.iterdir()):
        assert sha(path) == sha(ATTEMPT / path.name)
        copied.append({"path": str(path.relative_to(ROOT)), "sha256": sha(path), "bytes": path.stat().st_size})
    raw_log = target / "adb-operations.txt"
    raw = raw_log.read_bytes()
    compressed = target / "adb-operations.raw.txt.gz"
    compressed.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(compressed.read_bytes()) == raw
    lines = raw.decode("utf-8-sig").splitlines()
    raw_log.write_text("Exact original bytes retained in adb-operations.raw.txt.gz\n"
                       + "\n".join(lines[:12]) + "\n[Middle omitted; exact gzip retained.]\n"
                       + "\n".join(lines[-20:]) + "\n", encoding="utf-8")
    for row in copied:
        if row["path"] == str(raw_log.relative_to(ROOT)):
            row.update(originalSha256=row["sha256"], sha256=sha(raw_log), bytes=raw_log.stat().st_size,
                       compressedRaw=str(compressed.relative_to(ROOT)), compressedRawSha256=sha(compressed))
    receipts = NATIVE / "execution-551-receipts"
    receipts.mkdir()
    for path in (Path(__file__), CONTROL / "run-551-native.ps1", CONTROL / "post-551-issue.ps1"):
        shutil.copyfile(path, receipts / path.name)
    inspection = NATIVE / "inspection-execution-551"
    shutil.copytree(CONTROL / "artifacts" / "batch-081-native-inspection", inspection)
    save(NATIVE / "visual-inspection-execution-551.json", visual)
    save(NATIVE / "image-index-execution-551.json", index)
    evidence = {
        **starting, "schemaVersion": 1, "checkpoint": 551, "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmations",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "manifestSha256": sha(ROOT / "manifest.json"),
        "nativeExecution": native, "articleRoute": route,
        "nativeRasterRecords": {"rows": 120, "individualGlyphProbes": 116, "wholeWordRasterProbes": 4,
                               "panels": 3, "path": str((target / "n1-081-font-raster.json").relative_to(ROOT)),
                               "sha256": sha(target / "n1-081-font-raster.json")},
        "visualInspection": visual, "imageIndex": index, "archivedReceipts": copied,
        "rawAttemptsAndOriginalPngBytesPreserved": True,
        "productionSingleArchiveImport": True, "exactRuntimeHashesVerified": verified,
        "originalArchiveBudgetsReverified": True, "runtimeUnchanged": True,
        "runtimePublished": False, "independentVisualReviewersLaunched": 0,
        "contentVersion": route["contentVersion"],
        "inheritedTextualReview": "b7bf953d137251f179a57128bb84bd70a37737c8",
        "inheritedFreshHostChecks": "execution549 RealContentTest THREE + RareHanTest ONE, no skips; no rerun",
        "inheritedNativeCompile": "execution550 compiled frozen test APK; no rebuild",
        "originalReviewerSessions": {
            "claude-opus-5.5": "5d197613-b9f7-4815-aa0f-25098fbf6825",
            "gpt-6.1-sol": "44f703a8-cc19-4e68-bd98-8fa94688e781",
        },
        "otherOwnerEmulator": "Preexisting emulator5556/PIDs10668+18200 remained connected; all mutating adb operations explicitly addressed owned5580 only.",
        "publishedAdditions": 107, "remainingAdditions": 1121,
        "lastPublishedCommit": "a7b119ed36adf7a3a92bba03700bc1c51f812bef",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT, "limits": visual["limits"],
    }
    save(EVIDENCE, evidence)
    ledger_path = ROOT / "docs" / "n1-sources" / "batch-081-progress.json"
    ledger = load(ledger_path)
    assert "preNative551AcceptanceState" not in ledger
    ledger["preNative551AcceptanceState"] = {
        k: ledger[k] for k in ("status", "nextAction", "limits", "fontDisposition") if k in ledger
    }
    ledger.update(
        status=evidence["stage"], nextAction=NEXT, limits=visual["limits"],
        fontDisposition="Fresh551 native29Han/fourfamilies/three original Compose PNGs incl. 冫/氵 readable. Coordinator contact-sheet inspection; independent two-family visual confirmation and phone acceptance outstanding.",
        nativeEvidence="docs/n1-sources/execution-551.json",
        nativeExecutionCases=2, independentVisualAcceptance=False,
    )
    save(ledger_path, ledger)
    print("Native evidence archived: 2 terminal-zero cases; 45 PNGs/25 groups; 8369 runtime hashes.")


def checkpoint():
    original = load(LOGS / "progress-before-551.json")
    progress = load(CONTROL / "progress.json")
    evidence = load(EVIDENCE)
    receipt = load(LOGS / "issue-response-551.json")
    body = (LOGS / "issue-body-551.txt").read_text(encoding="utf-8")
    assert receipt["user"]["login"] == "stop-cran"
    assert receipt["body"].replace("\r\n", "\n").rstrip() == body.rstrip()
    assert "issues/60#issuecomment-" in receipt["html_url"]
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert not subprocess.check_output(["git", "-C", str(ANDROID), "status", "--porcelain"])
    assert sha(ROOT / "manifest.json") == evidence["manifestSha256"]
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for row in evidence["archivedReceipts"]:
        assert sha(ROOT / row["path"]) == row["sha256"], row["path"]
        if "compressedRaw" in row:
            compressed = ROOT / row["compressedRaw"]
            assert sha(compressed) == row["compressedRawSha256"]
            assert hashlib.sha256(gzip.decompress(compressed.read_bytes())).hexdigest() == row["originalSha256"]
    result = {
        "schemaVersion": 1, "execution": 551, "checkpoint": 551, "batch": "081",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": evidence["stage"], "evidence": str(EVIDENCE.relative_to(ROOT)),
        "evidenceSha256": sha(EVIDENCE), "nativeCasesExecuted": 2, "terminalSuccessCases": 2,
        "skipped": 0, "nativePassed": True, "emulatorSerial": "emulator-5580",
        "parentEmulatorPid": 18020, "qemuPid": 28948, "ownedHelperAndQemuStopped": True,
        "otherOwnerEmulatorUntouched": True, "originalPngCount": 45,
        "distinctPngGroupsInspectedViaContactSheets": 25, "originalFontPanelsDirectlyViewed": 3,
        "scopeGlyphs": 29, "productionFontFamilies": 4,
        "individualNativePaintAssertions": 116, "wholeWordNativePaintAssertions": 4,
        "independentVisualReviewersLaunched": 0, "independentVisualAcceptance": False,
        "runtimePayloadHashesVerified": 8369, "contentVersion": evidence["contentVersion"],
        "runtimeBytesUnchanged": True, "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 107, "remainingAdditions": 1121,
        "lastPublishedCommit": evidence["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "originalRootKeyCountCompared": len(original),
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "changedRootFields": ["checkpoint", "status", "stage", "nextAction", "blocker"],
    }
    assert progress["checkpoint"] == 550 and progress["batch"] == "081"
    progress.update(checkpoint=551, status="continue", stage=evidence["stage"], nextAction=NEXT, blocker=None)
    progress["execution551CoordinatorCheckpoint"] = result
    progress["batch081NativeExecution551"] = result
    allowed = set(result["changedRootFields"])
    assert all(progress[k] == v for k, v in original.items() if k not in allowed)
    save(CONTROL / "progress.json", progress)
    persisted = load(CONTROL / "progress.json")
    assert all(persisted[k] == v for k, v in original.items() if k not in allowed)
    save(LOGS / "coordinator-checkpoint-551.json", result)
    print(json.dumps({k: result[k] for k in ("checkpoint", "status", "stage", "savedCommit", "issueUpdate",
                                             "originalRootKeyCountCompared", "allOriginalHistoricalRootKeysPreservedExactly")}, indent=2))


def checks():
    evidence = load(EVIDENCE)
    receipts = NATIVE / "execution-551-receipts"
    for path in (Path(__file__), CONTROL / "run-551-native.ps1", CONTROL / "post-551-issue.ps1"):
        shutil.copyfile(path, receipts / path.name)
    for name in ("validate-551.txt", "manifest-551.txt"):
        source = LOGS / name
        destination = receipts / name
        shutil.copyfile(source, destination)
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    evidence.update(
        validatorErrors=0, manifestFresh=True, manifestBytesUnchanged=True,
        runtimeBytesUnchanged=True, freshOriginMain=git("rev-parse", "origin/main"),
        validationReceipts=[
            {"path": str(path.relative_to(ROOT)), "sha256": sha(path)}
            for path in sorted(receipts.iterdir())
        ],
    )
    save(EVIDENCE, evidence)
    print("Validation and durable helper receipts sealed; runtime unchanged.")


def clean_logs():
    evidence = load(EVIDENCE)
    target = NATIVE / "attempt-1"
    for row in evidence["archivedReceipts"]:
        path = ROOT / row["path"]
        if path.name not in {"adb-operations.txt", "emulator-stdout.txt"}:
            continue
        raw = path.read_bytes()
        if "compressedRaw" not in row:
            compressed = target / (path.stem + ".raw.txt.gz")
            compressed.write_bytes(gzip.compress(raw, mtime=0))
            assert gzip.decompress(compressed.read_bytes()) == raw
            row.update(originalSha256=sha(path), compressedRaw=str(compressed.relative_to(ROOT)),
                       compressedRawSha256=sha(compressed))
        normalized = "\n".join(line.rstrip() for line in raw.decode("utf-8-sig").splitlines()).rstrip() + "\n"
        path.write_text(normalized, encoding="utf-8")
        row.update(sha256=sha(path), bytes=path.stat().st_size)
    evidence["logNormalization"] = "Readable adb summary/emulator stdout strip trailing whitespace; complete original bytes retained in exact raw gzip files. Original attempt folder and all PNG bytes unmodified."
    save(EVIDENCE, evidence)
    print("Readable log whitespace normalized; exact original bytes preserved in gzip.")


if __name__ == "__main__":
    {"start": start, "record": record, "checks": checks, "clean_logs": clean_logs, "checkpoint": checkpoint}[sys.argv[1]]()
