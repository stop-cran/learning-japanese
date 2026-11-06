import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOGS = CONTROL / "logs" / "f4e4a05d-996c-4922-8780-cd7ddac62e21"
FOLDER = ROOT / "docs" / "n1-reviews" / "batch-077-native"
SOURCES = ROOT / "docs" / "n1-sources"
APK = CONTROL / "artifacts" / "n1-batch-077-native-test.apk"
HEAD = "46dff1466ac9f3cf64b54e197c05088414939896"
NEXT = (
    "SAME077 execute compiled control\\artifacts\\n1-batch-077-native-test.apk ONLY after fresh "
    "device/5580/5581 local+remote connection/PID ownership inspection. Read docs\\n1-sources\\"
    "execution-517.json and batch-077-native-preparation.json. Established read-only API35 "
    "N3_Acceptance_20261029 emulator-5580, hostGPU/Vulkan-disabled2048MiB/two-core flags; record "
    "actual owned parent/QEMU and stop only owned helper. Batch0405584override NOT inherited. "
    "No HOST-only2GiBinit for native; no heap/guard increases. Both N1Batch077GlyphTest and "
    "N1Batch077ArticleTest require terminal0, zero skips and actual PNG inspection; compilation "
    "is not acceptance. Full signed46dff146 Git archive via production ContentSync ONCE:1089kanji"
    "5046words109N1,version2944928c13e2165a,problems0,epoch1. Full+Lite raw and curatedボウ/おか.す; "
    "actualぼう/おかす each Good/Done2correct without duplicate question/log. Complete冒/冒す, "
    "exact changed冒険 component paragraph and険 meaning paragraph plus actual冂/阝 facts, "
    "all3mappedpairs6directions; selection/meaning/readings/nine-stroke reference-touch/"
    "ungradedtrace/recallAgain/articles/SystemBack/offline. Cover all39 rawscopedHan across"
    "4productionfamilies in two bounded panels plus focused冒/日/目/官/冂/阜/阝/険/犯/侵 and冒険/冒す "
    "panel; two wholewordrasters per family. Historical draft38 retained: reviewed metadata-only"
    "攻 exclusion adds the39th rawHan, not new learner prose; cmaps unchanged, pending冂/阝. "
    "Cmapabsence NOTglyphfailure; hashes NOTreadability/fallbackface. Then two SERIAL different-"
    "family original-session visual confirmations where possible. Fresh516HOST3+1 retained; "
    "no redundant rerun. No teachingchanges/publication/078 this checkpoint. Later currentmain"
    "normalmerge/revalidation/normalsigning/ownerfastforward/greenCI/EVERYimmutableZIPhash/"
    "originalbudgets/ownerissue60receipt remain. No unreviewedpush/signingretry/"
    "permissionworkaround/authoragents/secondrunner. Preserve FULLlivehistory, source recipes, "
    "originalreports and reviewedbaseline虎/猿/丘/山exceptions; original denials/OOMs/failedlookups/"
    "readdepthlimits remain. Published103/1228,remaining1125; necessarysupportsNOTN1vocabulary. "
    "CompatibleAndroidf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding. "
    "Overall project incomplete."
)
LIMITS = (
    "Preparation/compilation only; no emulator, native execution, PNG inspection or independent "
    "visual acceptance. Static projections/offsets and raster hashes do not establish visibility/"
    "readability or fallback face. Reference-touch trace is not human handwriting/MLKit evidence. "
    "Fresh516 HOST3+1 remains distinct; HOST-only2GiBinit NEVER enters native builds. No guest/app "
    "heap/archiveguard changes, teaching/app edits, reviewer or publication. Historical denials/"
    "OOMs/failed lookups/read-depth limitations retained. Physical-phone/general-release/whole-set "
    "acceptance remains outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".execution517.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    assert load(path) == value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


def unchanged():
    assert not git("diff", HEAD, "--", "kanji", "words", "strokes", "articles", "manifest.json")
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not git("status", "--porcelain", cwd=ANDROID)


def evidence():
    unchanged()
    preparation = load(CONTROL / "batch-077-native-fixture-verification.json")
    assert sha(Path(preparation["fixture"])) == preparation["fixtureSha256"]
    assert sha(Path(preparation["archive"])) == preparation["archiveSha256"]
    raw_log = LOGS / "native-compile.txt"
    text = raw_log.read_text(encoding="utf-8-sig")
    assert (LOGS / "native-compile-exit.txt").read_text().strip() == "0"
    assert "BUILD SUCCESSFUL" in text
    with zipfile.ZipFile(APK) as archive:
        assert hashlib.sha256(archive.read("assets/" + Path(preparation["archive"]).name)).hexdigest() == preparation["archiveSha256"]
        dex = [archive.read(n) for n in archive.namelist() if re.fullmatch(r"classes\d*\.dex", n)]
        for kind in ("Glyph", "Article"):
            assert any(f"Lio/github/stopcran/kanji/ui/N1Batch077{kind}Test;".encode() in b for b in dex)
            assert not any(f"Lio/github/stopcran/kanji/ui/N1Batch076{kind}Test;".encode() in b for b in dex)
        for method in (
            "bravingRiskLookalikesAndRadicalFallbacksAcrossFourProductionFamilies",
            "fullSingleImportOfflineBravingRiskThreeReciprocalPairsBothReadingsDrawingAndSystemBack",
        ):
            assert any(method.encode() in b for b in dex)
    (FOLDER / "compile.txt").write_text(
        "\n".join(line.rstrip() for line in text.splitlines()) + "\n", encoding="utf-8")
    (FOLDER / "compile-raw.txt.gz").write_bytes(gzip.compress(raw_log.read_bytes(), mtime=0))
    for kind in ("start", "end", "exit"):
        shutil.copyfile(LOGS / f"native-compile-{kind}.txt", FOLDER / f"compile-{kind}.txt")
    receipts = FOLDER / "preparation-receipts"
    receipts.mkdir(exist_ok=True)
    for name in ("prepare-batch-077-native.py", "run-517-native-compile.ps1", "checkpoint-517.py"):
        shutil.copyfile(CONTROL / name, receipts / name)
    checks = []
    for name, expected in (("validate", "0 error(s)"), ("manifest", "version 2944928c13e2165a")):
        source = LOGS / f"{name}-517.txt"
        content = source.read_text(encoding="utf-8-sig")
        assert expected in content
        target = FOLDER / f"{name}.txt"
        target.write_text(content.replace("\r\n", "\n"), encoding="utf-8")
        checks.append({"check": name, "exitCode": 0, "log": str(target.relative_to(ROOT)), "sha256": sha(target)})
    inherited = load(SOURCES / "execution-516.json")
    for item in inherited["tests"]:
        assert sha(ROOT / item["archivedPath"]) == item["sha256"]
        assert item["failures"] == item["errors"] == item["skipped"] == "0"
    preparation["nextAction"] = NEXT
    preparation["limits"] = LIMITS
    save(SOURCES / "batch-077-native-preparation.json", preparation)
    record = {
        "schemaVersion": 1, "execution": 517, "batch": "077", "status": "native-compiled-pending-execution",
        "startingHead": HEAD, "reviewedTeachingSnapshot": preparation["reviewedTeachingSnapshot"],
        "authorization": load(CONTROL / "progress.json")["execution517StartingState"]["authorization"],
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "originMainFreshFetch": git("rev-parse", "origin/main"),
        "preparation": "docs\\n1-sources\\batch-077-native-preparation.json",
        "preparationSha256": sha(SOURCES / "batch-077-native-preparation.json"),
        "contentVersion": preparation["contentVersion"], "expectedCounts": preparation["expectedCounts"],
        "compilation": {
            "exitCode": 0, "status": "compiled-not-executed",
            "startedAt": (LOGS / "native-compile-start.txt").read_text().strip(),
            "endedAt": (LOGS / "native-compile-end.txt").read_text().strip(),
            "result": next(line for line in text.splitlines() if line.startswith("BUILD SUCCESSFUL")),
            "command": ".\\gradlew.bat :app:assembleDebugAndroidTest --no-daemon --no-parallel --max-workers=1 '-Pkotlin.compiler.execution.strategy=in-process'",
            "log": str((FOLDER / "compile.txt").relative_to(ROOT)),
            "logSha256": sha(FOLDER / "compile.txt"), "rawLog": str(raw_log), "rawLogSha256": sha(raw_log),
            "apk": str(APK), "apkSha256": sha(APK), "apkBytes": APK.stat().st_size,
            "packagedExactFullArchiveVerified": True, "bothClassesAndMethodsVerified": True,
            "old076DescriptorsAbsent": True, "temporaryAndroidSourceAndAssetRemoved": True,
            "androidWhollyClean": True, "hostTestInitScriptUsed": False,
            "nativeOrEmulatorStarted": False,
            "JAVA_HOME": r"C:\Program Files\Eclipse Adoptium\jdk-17.0.20.101-hotspot",
            "ANDROID_HOME": r"C:\Users\stop-\AppData\Local\Android\Sdk",
        },
        "checks": checks, "fixtureSha256": preparation["fixtureSha256"],
        "archiveSha256": preparation["archiveSha256"],
        "selectorAudit": {
            "staticSelectors": len(preparation["staticMarkdownSelectors"]),
            "completeArticleProjections": 2, "changedReusedPassages": 2,
            "readingLabelsAndExplanations": 4,
            "mappedReciprocalPairs": 3, "mappedDirectedTransitions": 6,
            "staticOnlyNotActualVisualCoverage": True,
            "exactLedgerDirectedLinksAndPairsVerified": True,
        },
        "inventoryReconciliation": preparation["inventoryReconciliation"],
        "currentScopedHan": 39, "plannedNativePaintProbes": 156, "plannedWholeWordRasterProbes": 8,
        "accepted516AndroidRetainedWithoutRerun": True, "inheritedArchivedXmlHashesReverified": True,
        "textualReconciliationSha256": sha(ROOT / "docs" / "n1-reviews" / "batch-077-reconciliation.json"),
        "runtimeEditsMade": False, "nativeExecuted": False, "nativeAcceptance": False,
        "independentVisualAcceptance": False, "reviewersLaunched": 0, "publicationAttempted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "diagnostics": [
            "Preparation stopped before artifact writes on an assumed directedLinks key; corrected to derive exact six directions from actual allMappedReciprocalPairs.",
            "An exact fixture string assertion caught its missing leading clause; corrected before artifacts were written.",
            "Actual post-review inventory caught metadata-only 攻, absent from historical38; audited39 against unchanged fonts and included all39 in planned probes. No historical audit rewritten.",
            "Stale-token assertion initially rejected legitimate ケン in unchanged冒険's compound explanation; narrowed to old target metadata list, preserving exact reused prose.",
            "Staged whitespace check caught a Gradle log trailing space before signing was invoked. Normalized the readable log; exact original bytes remain in compile-raw.txt.gz and control.",
        ],
        "publishedAdditions": 103, "remainingAdditions": 1125, "nextAction": NEXT, "limits": LIMITS,
    }
    record["artifacts"] = [
        {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(FOLDER.rglob("*")) if path.is_file()
    ] + [{"path": str((SOURCES / "batch-077-native-preparation.json").relative_to(ROOT)),
          "bytes": (SOURCES / "batch-077-native-preparation.json").stat().st_size,
          "sha256": sha(SOURCES / "batch-077-native-preparation.json")}]
    save(SOURCES / "execution-517.json", record)
    print("Native preparation/compile evidence archived; no native execution or publication.")


def checkpoint():
    unchanged()
    assert not git("status", "--porcelain")
    assert git("log", "-1", "--format=%G?") == "G"
    record = load(SOURCES / "execution-517.json")
    for item in record["artifacts"]:
        assert sha(ROOT / item["path"]) == item["sha256"]
    p = load(CONTROL / "progress.json")
    original = load(LOGS / "progress-before-517.json")
    receipt = {
        "execution": 517, "checkpoint": 517, "batch": "077", "savedCommit": git("rev-parse", "HEAD"),
        "signature": "G", "record": "docs\\n1-sources\\execution-517.json",
        "recordSha256": sha(SOURCES / "execution-517.json"), "status": "continue",
        "stage": "batch-077-native-compiled-pending-execution",
        "runtimePublished": False, "nativeExecuted": False, "dedicatedWorktreesClean": True,
        "currentScopedHan": 39, "allOriginalHistoricalRootKeysPreserved": True,
        "originalRootKeysCompared": len(original), "nextAction": NEXT,
    }
    p["execution517CoordinatorCheckpoint"] = receipt
    p["batch077NativePreparationCheckpoint"] = receipt.copy()
    p.update(checkpoint=517, status="continue", stage=receipt["stage"], nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(CONTROL / "progress.json", p)
    body = (
        "Batch 077 native preparation/compile checkpoint (not native acceptance or publication): "
        f"signed local `{receipt['savedCommit']}`; teaching/runtime bytes and manifest "
        "`2944928c13e2165a` unchanged. The two-case native test APK compiled with one worker; "
        "its embedded full signed46dff146 Git archive preserves all8,358 runtime hashes and original "
        "budgets (8,380ZIP entries;30,342,183 compressed /44,403,012 inflated /44,134,674 retained bytes). "
        "Fixture plans production ContentSync once,1089kanji/5046words/109N1, Full+Lite "
        "ボウ/おか.す and actualぼう/おかす, complete冒/冒す plus changed冒険/険, "
        "all3mappedpairs6directions, nine-stroke reference-touch, SystemBack/offline. "
        "Current raw scope is39Han: historical38 plus metadata-only攻 from the reviewed exclusion; "
        "156glyph+8word raster probes across4productionfamilies planned, pending actual冂/阝 rendering. "
        "Historical38 audit retained. Android temporary test source/asset removed; dedicated trees clean. "
        "Fresh516 HOST3+1 evidence retained without redundant rerun. No emulator/native/visual/reviewer "
        "or publication performed here. Next: fresh device/5580/5581/PID ownership preflight, then compiled "
        "native cases with terminal0/no skips and actual PNG inspection, followed by two serial "
        "different-family visual confirmations; later combined-main/signing/CI/immutableZIP gates remain. "
        "Published103/1228,remaining1125. CompatibleAndroidf9b59a2+ required; supports are not an N1 "
        "vocabulary delivery; phone/generalrelease/whole-set outstanding. "
        "All historical evidence/denials/OOMs/guards preserved; optional external helpers not accessed. "
        "Evidence: `docs/n1-sources/execution-517.json` and `batch-077-native-preparation.json`."
    )
    (LOGS / "issue-517-body.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("checkpoint", "savedCommit", "stage", "originalRootKeysCompared")}, indent=2))


if sys.argv[1] == "evidence":
    evidence()
elif sys.argv[1] == "checkpoint":
    checkpoint()
else:
    raise ValueError(sys.argv[1])
