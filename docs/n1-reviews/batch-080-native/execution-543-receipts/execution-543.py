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
ANDROID = CONTROL.parent / "kanji-cards-android"
LOGS = CONTROL / "logs" / "4d6594cd-479f-4796-871c-9b0e50f053c4"
BASE = "4033c82b7c1e7b690ccb2c9b510e04820fe1ba1a"
NATIVE = ROOT / "docs" / "n1-reviews" / "batch-080-native"
ATTEMPT = CONTROL / "artifacts" / "batch-080-native-attempt-1"
EVIDENCE = ROOT / "docs" / "n1-sources" / "execution-543.json"
NEXT = (
    "SAME080 two SERIAL original-family independent VISUAL confirmations only, then "
    "persist/yield before integration/publication/081. Use signed native evidence at "
    "execution543 savedCommit and docs\\n1-sources\\execution-543.json, actual original "
    "attempt-1 PNGs, visual-inspection-execution-543.json and image-index-execution-543.json. "
    "Original ClaudeOpus5.5 session a3b94466-63e4-4403-a67d-3249751e5a1b and GPT6.1Sol "
    "session27fb4006-7e5d-4d5c-aabb-c8316fb8f334 where possible; actual catalog/model/process "
    "evidence and complete reports required, at mostONE active reviewer, no edits to frozen "
    "snapshot during reviews. Fresh543 native TWO named cases terminal0/no skips on owned "
    "read-only API35 emulator-5580 parent11976/qemu1240, both stopped; owner5556 untouched. "
    "Production ContentSync exact full signed0d2c9aee envelope ONCE:1092kanji5048words112N1/"
    "contentVersion4572f7b1d0d95059/zeroProblems/acceptedepoch1. Full+Lite full readings "
    "ゴ,コ / さ.える,こお.る,ひ.える intact; explicit no on quiz and sole selected "
    "さ.える/offeredさえる/good log and one-question Done asserted. Complete冴/冴える, "
    "onepair/twodirections/SystemBack/N1selection/meaning/sevenstroke reference trace then "
    "giveuprecall/offline passed.49originalPNGs/26distinctbytegroups directly coordinator "
    "viewed; all30Han/fourproductionfamilies in three Compose panels including actual "
    "冫/冱/氵 fallback readable;120individual+4wholeword Paint assertion/hash records "
    "not124PNGreads or fallback-face proof. Table horizontal states collectively show "
    "labels/explanations, no single-frameallcolumns claim. Offline handwritingmodel "
    "unavailable; injected trace/shape-only comparison/giveuprecall NOT recognition, "
    "humanmemory or phone. Inherit fresh540HOST3+1/no skips and successful541 native compile "
    "without rerun absent new concern; HOST-only2GiBinit NEVER native, no app/guestheap/"
    "archiveguard change. Preserve source/lookup/citation/read-depth/review/process/denial/"
    "OOM/viewport/MLKit/phone/generalrelease/whole-set limits. Durablecontrol helpers and "
    "committedpackets/approvedinputs only; optional historical session recipes skipped. "
    "No secondrunner/authoragent/concurrentheavywork/unreviewedpush/signingretry/"
    "permissionworkaround. Actual new denial or signinghang preserve/report/yield. "
    "Later combined-currentmain non-rewritingintegration/revalidation/normalsigning/"
    "ownerfastforward/publicSHA/terminalgreenCI/EVERYimmutableZIP runtimehash/original "
    "budgets/terminalreceipts/ownerissue60 mandatory before081. Published106/1228,remaining1122/"
    "latest079b120125ae5cdbfe9f3bcb1b0a7ae8a61e422ec8d; draft107 NOT delivered. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=ROOT):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 542 and progress["batch"] == "080"
    assert progress["status"] == "continue"
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=ANDROID)
    backup = LOGS / "progress-before-543.json"
    assert not backup.exists()
    shutil.copyfile(CONTROL / "progress.json", backup)
    request = LOGS / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["checkpoint"] == 542
    starting = {
        "execution": 543, "batch": "080", "startingHead": BASE,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME080 native execution and durable local checkpoint only; no reviewer, publication,081 or second runner.",
        "authorization": {
            "requestSha256": sha(request), "bytes": request.stat().st_size,
            "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint parsed; operative contract, complete issue and final checkpoint inspected. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": str(CONTROL / "authoring-artifact-path-notes.txt"),
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "manifestSha256": sha(ROOT / "manifest.json"),
        "status": "native-execution-in-progress",
    }
    save(LOGS / "starting-state-543.json", starting)
    progress["execution543StartingState"] = starting
    progress.update(stage="batch-080-native-execution-in-progress", blocker=None)
    save(CONTROL / "progress.json", progress)
    persisted = load(CONTROL / "progress.json")
    original = load(backup)
    assert all(persisted[k] == v for k, v in original.items() if k not in {"stage", "blocker"})
    print("Native execution scope persisted; complete original history retained.")


def record():
    starting = load(LOGS / "starting-state-543.json")
    native = load(CONTROL / "batch-080-native-attempt-1-execution.json")
    visual = load(CONTROL / "batch-080-native-visual-inspection.json")
    preparation = load(ROOT / "docs" / "n1-sources" / "batch-080-native-fixture-verification.json")
    assert git("rev-parse", "HEAD") == BASE
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=ANDROID)
    assert native["passed"] and native["failure"] is None and native["adbExitCode"] == 0
    assert native["terminalSuccessCases"] == 2 and len(native["terminalCases"]) == 2
    assert {(c["class"].split(".")[-1], c["test"], c["status"]) for c in native["terminalCases"]} == {
        ("N1Batch080GlyphTest", "clarityLookalikesAndIceWaterFallbacksAcrossFourProductionFamilies", 0),
        ("N1Batch080ArticleTest", "fullSingleImportOfflineClarityOneReciprocalPairCuratedKunDrawingAndSystemBack", 0),
    }
    assert native["ownedHelperStopped"] and native["ownedQemuStopped"] and native["stopAdbExitCode"] == 0
    assert native["parentEmulatorPid"] == 11976 and native["qemuPid"] == 1240
    assert not any(native[k] for k in ("hostHeapInitUsed", "guestOrAppHeapChanged", "guardsChanged"))
    assert sha(ROOT / "manifest.json") == starting["manifestSha256"]
    route = load(ATTEMPT / "n1-080-article-route.json")
    raster = load(ATTEMPT / "n1-080-font-raster.json")
    assert route["passed"] and route["offline"] and route["archiveRequests"] == 1
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"], route["problems"]) == (1092, 5048, 112, 0)
    assert route["acceptedReadingParserEpoch"] == 1 and not route["phoneEvidence"]
    assert route["contentSnapshot"] == preparation["contentSnapshot"]
    assert route["contentVersion"] == preparation["contentVersion"] == "4572f7b1d0d95059"
    for key in ("fullOnyomi", "fullProjectionOnyomi"):
        assert route[key] == ["ゴ", "コ"]
    for key in ("fullKunyomi", "fullProjectionKunyomi"):
        assert route[key] == ["さ.える", "こお.る", "ひ.える"]
    for key in ("quizOnKeys", "liteQuizOnyomi", "fullProjectionQuizOnyomi"):
        assert route[key] == []
    for key in ("liteQuizKunyomi", "fullProjectionQuizKunyomi"):
        assert route[key] == ["さ.える"]
    assert route["quizKunKeys"] == ["さえる"]
    assert route["touchInjectedReferenceStrokes"] == 7
    assert route["mappedReciprocalPairs"] == 1 and route["directedLinkTransitions"] == 2
    for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedKunPersistedGoodAndDone", "drawingTraceThenRecall", "drawingGradeRecordedOnNext"):
        assert route[key], key
    assert (len(raster["rows"]), raster["individualGlyphProbes"], raster["wholeWordRasterProbes"], raster["panels"]) == (124, 120, 4, 3)
    expected_glyphs = set(preparation["plannedGlyphs"])
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        rows = [r for r in raster["rows"] if r["font"] == font]
        assert {r["character"] for r in rows if "character" in r} == expected_glyphs
        assert all(r["hasGlyph"] for r in rows if "character" in r)
        assert {r["word"] for r in rows if "word" in r} == {"冴える"}
    groups = defaultdict(list)
    for path in sorted(ATTEMPT.glob("*.png")):
        groups[sha(path)].append(path.name)
    assert sum(map(len, groups.values())) == 49 and len(groups) == 26
    assert {names[0] for names in groups.values()} == set(visual["inspectedRepresentatives"])
    index = {
        "originalPngCount": 49, "distinctByteGroups": 26, "inspectionMethod": visual["method"],
        "groups": [{"sha256": digest, "directlyViewedRepresentative": names[0], "originals": names}
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
        assert verified == 8366
        assert len(archive.infolist()) == preparation["zipEntries"] < 18000
        assert Path(preparation["archive"]).stat().st_size < 42 * 1024**2
        assert sum(i.file_size for i in archive.infolist()) == preparation["inflatedBytes"] < 80 * 1024**2
        assert retained == preparation["retainedBytes"] < 56 * 1024**2
    target = NATIVE / "attempt-1"
    assert not target.exists()
    shutil.copytree(ATTEMPT, target)
    copied = []
    for path in sorted(ATTEMPT.iterdir()):
        if path.is_file():
            destination = target / path.name
            assert sha(path) == sha(destination)
            copied.append({"path": str(destination.relative_to(ROOT)), "sha256": sha(destination),
                           "bytes": destination.stat().st_size})
    for name in ("emulator-stdout.txt", "adb-operations.txt"):
        path = target / name
        raw = path.read_bytes()
        compressed = target / (name[:-4] + ".raw.txt.gz")
        compressed.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(compressed.read_bytes()) == raw
        if len(raw) > 16000:
            lines = raw.decode("utf-8-sig").splitlines()
            path.write_text(
                "Exact raw bytes retained in " + compressed.name + "\n"
                + "\n".join(lines[:12]) + "\n[Middle omitted; exact gzip retained.]\n"
                + "\n".join(lines[-20:]) + "\n", encoding="utf-8")
        for row in copied:
            if row["path"] == str(path.relative_to(ROOT)):
                row["originalSha256"] = row["sha256"]
                row.update(sha256=sha(path), bytes=path.stat().st_size,
                           compressedRaw=str(compressed.relative_to(ROOT)),
                           compressedRawSha256=sha(compressed))
    receipts = NATIVE / "execution-543-receipts"
    receipts.mkdir()
    for path in (Path(__file__), CONTROL / "run-543-native.ps1", CONTROL / "post-execution-543.ps1"):
        destination = receipts / path.name
        shutil.copyfile(path, destination)
        assert sha(path) == sha(destination)
    save(NATIVE / "visual-inspection-execution-543.json", visual)
    save(NATIVE / "image-index-execution-543.json", index)
    evidence = {
        **starting, "schemaVersion": 1, "checkpoint": 543, "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmations",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "nativeExecution": native, "articleRoute": route,
        "nativeRasterRecords": {"rows": 124, "individualGlyphProbes": 120,
                               "wholeWordRasterProbes": 4, "panels": 3,
                               "path": str((target / "n1-080-font-raster.json").relative_to(ROOT)),
                               "sha256": sha(target / "n1-080-font-raster.json")},
        "visualInspection": visual, "imageIndex": index, "archivedReceipts": copied,
        "rawAttemptsAndOriginalPngBytesPreserved": True,
        "productionSingleArchiveImport": True, "exactRuntimeHashesVerified": verified,
        "originalArchiveBudgetsReverified": True, "runtimeUnchanged": True,
        "runtimePublished": False, "independentVisualReviewersLaunched": 0,
        "inheritedTextualReview": "df0bab41616b2d8db5c03c2ebfc32aa213a75c80",
        "inheritedFreshHostChecks": "execution540 RealContentTest THREE + RareHanTest ONE, no skips; no rerun",
        "inheritedNativeCompile": "execution541 BUILD SUCCESSFUL in 1m17s; execution542 hash/receipt verification; no rebuild",
        "originalReviewerSessions": {
            "claude-opus-5.5": "a3b94466-63e4-4403-a67d-3249751e5a1b",
            "gpt-6.1-sol": "27fb4006-7e5d-4d5c-aabb-c8316fb8f334",
        },
        "otherOwnerEmulator": "Preexisting emulator5556/PIDs10668+18200 remained connected; all mutating adb operations explicitly addressed owned5580 only.",
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": "b120125ae5cdbfe9f3bcb1b0a7ae8a61e422ec8d",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "nextAction": NEXT, "limits": visual["limits"],
    }
    save(EVIDENCE, evidence)
    ledger_path = ROOT / "docs" / "n1-sources" / "batch-080-progress.json"
    ledger = load(ledger_path)
    assert "preNative543AcceptanceState" not in ledger
    ledger["preNative543AcceptanceState"] = {
        k: ledger[k] for k in ("status", "nextAction", "limits", "fontDisposition")
    }
    ledger.update(
        status=evidence["stage"], nextAction=NEXT, limits=visual["limits"],
        fontDisposition="Fresh543 native 30Han/four families/three actual Compose PNGs incl. 冫/冱/氵. Coordinator viewed; two-family independent visual confirmation and phone acceptance outstanding.",
        nativeEvidence="docs/n1-sources/execution-543.json",
        nativeExecutionCases=2, independentVisualAcceptance=False,
    )
    save(ledger_path, ledger)
    print(json.dumps({"terminalCases": 2, "originalPNGs": 49, "directlyViewedDistinctPNGs": 26,
                      "runtimeHashesVerified": verified, "stage": evidence["stage"]}, indent=2))


def issue_body():
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=ANDROID)
    assert git("rev-parse", "HEAD^") == BASE and git("log", "-1", "--format=%G?") == "G"
    head = git("rev-parse", "HEAD")
    body = (
        "Batch 080 (冴): native checkpoint **passed locally**, preserved in normally signed "
        f"`{head}`; **not published**.\n\n"
        "Both named API35 native cases returned terminal status 0 (no skips). The exact full "
        "`0d2c9aee` archive went through production ContentSync once: 1,092 kanji, 5,048 words, "
        "112 N1 cards, zero problems, contentVersion `4572f7b1d0d95059`. Full source readings "
        "remain intact; explicit empty on selection and sole kun `さえる` were verified in "
        "Full/Lite projections, quiz completion and the saved log. Complete 冴/冴える articles, "
        "both reciprocal directions, System Back, N1 selection/meaning, seven-stroke reference "
        "trace and give-up recall/offline routes passed.\n\n"
        "Preserved 49 original PNGs (26 distinct byte groups directly viewed by the coordinator), "
        "three four-family font panels covering all 30 scoped Han including 冫/冱/氵, and "
        "120 individual + four whole-word Paint records. Owned read-only emulator-5580 "
        "(parent11976/QEMU1240) stopped; existing owner emulator5556 untouched. No rebuild, "
        "guest/app heap change or archive-guard change. Offline handwriting recognition was "
        "unavailable: injected reference traces/shape comparison are not MLKit or human-recall proof. "
        "Table columns require horizontal scrolling; no single-frame all-columns claim.\n\n"
        "Next checkpoint: two serial original-family independent visual confirmations on this "
        "frozen snapshot, then integration/publication gates. Prior textual/host/compile/source "
        "limitations remain. Published additions stay **106/1,228; 1,122 remain**; local draft107 "
        "is not delivered. Compatible curated-reading client required. Physical-phone, "
        "general-release and whole-set acceptance remain outstanding.\n\n"
        "Evidence: `docs/n1-sources/execution-543.json` and "
        "`docs/n1-reviews/batch-080-native/attempt-1/`. Durable control helpers used; "
        "optional historical session helpers skipped. No new permission denial."
    )
    (LOGS / "issue-body-543.txt").write_text(body, encoding="utf-8")
    print(head)


def checkpoint():
    progress = load(CONTROL / "progress.json")
    original = load(LOGS / "progress-before-543.json")
    evidence = load(EVIDENCE)
    receipt = load(LOGS / "issue-response-543.json")
    body = (LOGS / "issue-body-543.txt").read_bytes().decode("utf-8")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    assert "issues/60#issuecomment-" in receipt["html_url"]
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=ANDROID)
    assert git("rev-parse", "HEAD") != BASE and git("merge-base", BASE, "HEAD") == BASE
    assert git("log", "-1", "--format=%G?") == "G"
    assert sha(ROOT / "manifest.json") == evidence["manifestSha256"]
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    for row in evidence["archivedReceipts"]:
        assert sha(ROOT / row["path"]) == row["sha256"], row["path"]
        if "compressedRaw" in row:
            compressed = ROOT / row["compressedRaw"]
            assert sha(compressed) == row["compressedRawSha256"]
            assert hashlib.sha256(gzip.decompress(compressed.read_bytes())).hexdigest() == row["originalSha256"]
    result = {
        "schemaVersion": 1, "execution": 543, "checkpoint": 543, "batch": "080",
        "savedCommit": git("rev-parse", "HEAD"), "signature": "G", "status": "continue",
        "stage": evidence["stage"], "evidence": str(EVIDENCE.relative_to(ROOT)),
        "evidenceSha256": sha(EVIDENCE), "nativeCasesExecuted": 2,
        "terminalSuccessCases": 2, "skipped": 0, "nativePassed": True,
        "emulatorSerial": "emulator-5580", "parentEmulatorPid": 11976, "qemuPid": 1240,
        "ownedHelperAndQemuStopped": True, "otherOwnerEmulatorUntouched": True,
        "originalPngCount": 49, "distinctPngGroupsDirectlyInspected": 26,
        "scopeGlyphs": 30, "productionFontFamilies": 4, "actualComposePanels": 3,
        "individualNativePaintAssertions": 120, "wholeWordNativePaintAssertions": 4,
        "independentVisualReviewersLaunched": 0, "independentVisualAcceptance": False,
        "runtimePayloadHashesVerified": 8366, "contentVersion": evidence["contentVersion"],
        "runtimeBytesUnchanged": True, "dedicatedWorktreesClean": True, "runtimePublished": False,
        "publishedAdditions": 106, "remainingAdditions": 1122,
        "lastPublishedCommit": evidence["lastPublishedCommit"],
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextBatchStarted": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "originalRootKeyCountCompared": len(original),
        "allOriginalHistoricalRootKeysPreservedExactly": True,
        "changedRootFields": ["checkpoint", "status", "stage", "nextAction", "blocker"],
    }
    assert progress["checkpoint"] == 542 and progress["batch"] == "080"
    progress.update(checkpoint=543, status="continue", stage=evidence["stage"], nextAction=NEXT, blocker=None)
    progress["execution543CoordinatorCheckpoint"] = result
    progress["batch080Native"] = result
    allowed = set(result["changedRootFields"])
    assert all(progress[k] == v for k, v in original.items() if k not in allowed)
    save(CONTROL / "progress.json", progress)
    persisted = load(CONTROL / "progress.json")
    assert all(persisted[k] == v for k, v in original.items() if k not in allowed)
    save(LOGS / "coordinator-checkpoint-543.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    globals()[sys.argv[1]]()
