import gzip
import hashlib
import json
import shutil
import subprocess
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
ANDROID = CONTROL.parent / "kanji-cards-android"
LOGS = CONTROL / "logs" / "e2498e2d-1fe6-4764-a8cf-a46f0b83535d"
ATTEMPT = CONTROL / "artifacts" / "batch-078-native-attempt-1"
DESTINATION = ROOT / "docs" / "n1-reviews" / "batch-078-native" / "attempt-1"
HEAD = "02c617480a1537feef611c12d51865ace7406caf"
NEXT = (
    "SAME078 bounded dependent visual confirmations ONLY, then persist/yield; no publication,079 "
    "or second runner. Read docs\\n1-sources\\execution-526.json and "
    "docs\\n1-reviews\\batch-078-native\\attempt-1: fresh native BOTH cases terminal0, zero skips; "
    "full signed7fb6c463 archive imported through production ContentSync ONCE, "
    "1090kanji5046words110N1/version8e06edf2b0857b26/zeroProblems/acceptedepoch1. "
    "Full+Lite full/curatedジョウ,emptykun,soleじょう key; selection/meaning/soleon completion/"
    "fourstroke injected trace then give-up recall/articles/all2pairs4directions/systemBack/offline passed. "
    "All27Han/fourproductionfamilies/108individual+4wholewordrasters/threeComposepanels passed; "
    "author directly inspected all24 byte-distinct PNGs accounting for43 originals. "
    "Exact冖/几fallback readable and 冗/元/兄/見 distinguishable; no actual visual defect established. "
    "Horizontal table scroll clips different edges in different captures, not data loss. "
    "Model unavailable offline; tracing uses stroke-shape fallback, not handwriting recognition. "
    "Owned emulator5580 parent27716/QEMU11132 stopped; unrelated owner5556 untouched. "
    "Do not rerun native/HOST3+1 or recompile without a new concern. Two serial original-family "
    "visual confirmations ClaudeOpus5.5/GPT6.1Sol still REQUIRED, original sessions where possible; "
    "same frozen teaching and exact new screenshots, no overlapping reviewers or heavywork. "
    "Preserve actual model identities, complete reports, supplied-versus-fresh evidence and all "
    "read-depth limits. Textual closure523, HOST3+1zero-skips524 valid; ZEROnew078wordarticle. "
    "8360runtimehashes/localfullarchive8382entries/originalbudgets verified unchanged526. "
    "No heap/guard changes; HOST-only2GiBinit NEVER enters native builds. Use committed source "
    "packets/approvedcontrolinputs/durablecontrolhelpers, not optional historical session-state recipes. "
    "Preserve FULL history and actual denials/OOM/review/read-depth/phone limitations. Later currentmain "
    "non-rewriting integration/revalidation/normal signing/ownerfastforward/greenCI/EVERYimmutableZIP"
    "hash/originalbudgets/verifiedownerissue60 still mandatory. No unreviewedpush/authoragents/"
    "secondrunner/signingretry/permissionworkaround. Preserve/report/yield on actualnewdenials. "
    "Published104/1228,remaining1124; local105th addition notpublished. CompatibleAndroidf9b59a2+; "
    "physicalphone/generalrelease/whole-set outstanding. Overallproject incomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, cwd=ROOT):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=cwd).decode("utf-8").strip()


if __name__ == "__main__":
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", cwd=ANDROID)
    assert git("rev-parse", "HEAD", cwd=ANDROID) == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    result = load(ATTEMPT / "execution.json")
    assert result == load(CONTROL / "batch-078-native-attempt-1-execution.json")
    assert result["passed"] and result["nativeExecuted"] and result["failure"] is None
    assert result["ownedHelperStopped"] and result["ownedQemuStopped"] and result["stopAdbExitCode"] == 0
    assert result["terminalSuccessCases"] == 2 and len(result["terminalCases"]) == 2
    assert {case["class"].split(".")[-1] for case in result["terminalCases"]} == {
        "N1Batch078GlyphTest", "N1Batch078ArticleTest"
    }
    assert all(case["status"] == 0 for case in result["terminalCases"])
    raw = (ATTEMPT / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert "OK (2 tests)" in raw and raw.count("INSTRUMENTATION_STATUS_CODE: 0") == 2
    assert not any(f"INSTRUMENTATION_STATUS_CODE: {code}" in raw for code in (-2, -3, -4))
    route = load(ATTEMPT / "n1-078-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1 and route["problems"] == 0
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"]) == (1090, 5046, 110)
    assert route["contentVersion"] == "8e06edf2b0857b26" and route["acceptedReadingParserEpoch"] == 1
    for key in ("fullOnyomi", "liteQuizOnyomi", "fullProjectionOnyomi", "fullProjectionQuizOnyomi"):
        assert route[key] == ["ジョウ"]
    for key in ("fullKunyomi", "quizKunKeys", "liteQuizKunyomi", "fullProjectionKunyomi", "fullProjectionQuizKunyomi"):
        assert route[key] == []
    assert route["quizOnKeys"] == ["じょう"]
    assert route["mappedReciprocalPairs"] == 2 and route["directedLinkTransitions"] == 4
    assert route["touchInjectedReferenceStrokes"] == 4 and route["offline"] and not route["phoneEvidence"]
    for key in ("reciprocalLinkAndSystemBack", "meaningQuestionAndFeedback",
                "soleCuratedOnPersistedGoodAndDoneNoKun", "drawingTraceThenRecall", "drawingGradeRecordedOnNext"):
        assert route[key] is True
    raster = load(ATTEMPT / "n1-078-font-raster.json")
    assert raster["individualGlyphProbes"] == 108 and raster["wholeWordRasterProbes"] == 4
    assert raster["panels"] == 3 and len(raster["rows"]) == 112 and raster["sdk"] == 35
    fixture = load(ROOT / "docs" / "n1-sources" / "batch-078-native-fixture-verification.json")
    for font in ("Gothic", "Mincho", "Textbook", "Brush"):
        rows = [row for row in raster["rows"] if row["font"] == font]
        assert {row["character"] for row in rows if "character" in row} == set(fixture["plannedGlyphs"])
        assert all(row["hasGlyph"] for row in rows if "character" in row)
        assert len({row["nativePaintRasterSha256"] for row in rows if "character" in row}) == 27
        assert [row["renderedCharactersNonblank"] for row in rows if "word" in row] == [2]
    for path, expected in (
        (Path(fixture["archive"]), fixture["archiveSha256"]),
        (Path(fixture["fixture"]), fixture["fixtureSha256"]),
        (Path(result["testApk"]), result["testApkSha256"]),
        (Path(result["appApk"]), result["appApkSha256"]),
    ):
        assert sha(path) == expected
    manifest_path = ROOT / "manifest.json"
    assert sha(manifest_path) == "2a2cb1b76b3e07d39da62c414b5845f12f8c1c77f6a11b3335091a43ce14ca65"
    manifest = load(manifest_path)
    entries = {}
    for section, value in manifest.items():
        if isinstance(value, dict):
            for name, digest in value.items():
                assert name not in entries
                entries[name] = (section, digest)
    assert len(entries) == 8360
    assert not git("diff", HEAD, "--", *{
        name.split("/")[0] for name in entries
    }, "manifest.json")
    with zipfile.ZipFile(fixture["archive"]) as archive:
        infos = archive.infolist()
        assert len(infos) == 8382
        prefix = next(info.filename[:-len("manifest.json")] for info in infos if info.filename.endswith("/manifest.json"))
        assert archive.read(prefix + "manifest.json") == manifest_path.read_bytes()
        retained = len(archive.read(prefix + "manifest.json"))
        for name, (section, expected) in entries.items():
            path = ROOT.joinpath(*name.split("/"))
            data = path.read_bytes()
            archived_data = archive.read(prefix + name)
            binary = section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
            canonical = data if binary else data.replace(b"\r\n", b"\n")
            archived_canonical = archived_data if binary else archived_data.replace(b"\r\n", b"\n")
            assert hashlib.sha256(canonical).hexdigest() == expected, name
            assert hashlib.sha256(archived_canonical).hexdigest() == expected, name
            assert archived_canonical == canonical, name
            retained += len(archived_data)
        inflated = sum(info.file_size for info in infos)
    assert retained == 44138361 and inflated == 44406699
    assert Path(fixture["archive"]).stat().st_size == 30344420
    assert retained <= 56 * 1024**2 and inflated <= 80 * 1024**2
    assert len(infos) <= 18000 and Path(fixture["archive"]).stat().st_size <= 42 * 1024**2
    observations = load(CONTROL / "batch-078-native-visual-observations.json")
    groups = defaultdict(list)
    for path in sorted(ATTEMPT.glob("*.png")):
        groups[sha(path)].append(path.name)
    assert sum(map(len, groups.values())) == 43 and len(groups) == 24
    assert len(observations["inspectedRepresentatives"]) == 24
    assert {sha(ATTEMPT / name) for name in observations["inspectedRepresentatives"]} == set(groups)
    assert not DESTINATION.exists()
    DESTINATION.mkdir()
    archived = []
    for path in sorted(ATTEMPT.iterdir()):
        assert path.is_file()
        destination = DESTINATION / path.name
        if path.name.endswith(".txt"):
            destination = destination.with_suffix(".txt.gz")
            destination.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
            assert gzip.decompress(destination.read_bytes()) == path.read_bytes()
            archived.append({"path": str(destination.relative_to(ROOT)), "sha256": sha(destination),
                             "decompressedSha256": sha(path)})
        else:
            shutil.copyfile(path, destination)
            assert sha(path) == sha(destination)
            archived.append({"path": str(destination.relative_to(ROOT)), "sha256": sha(destination)})
    save(DESTINATION / "visual-observations.json", observations)
    save(DESTINATION / "screenshot-groups.json", [
        {"sha256": digest, "originals": names} for digest, names in groups.items()
    ])
    receipts = DESTINATION / "execution-receipts"
    receipts.mkdir()
    for path in (CONTROL / "execution-526.py", CONTROL / "run-526-native.ps1", Path(__file__)):
        shutil.copyfile(path, receipts / path.name)
        archived.append({"path": str((receipts / path.name).relative_to(ROOT)), "sha256": sha(path)})
    record = {
        **load(CONTROL / "progress.json")["execution526StartingState"],
        "schemaVersion": 1, "checkpoint": 526, "status": "continue",
        "stage": "native-passed-awaiting-independent-visual-confirmations",
        "completedAt": datetime.now(timezone.utc).isoformat(),
        "nativeExecution": result, "articleRoute": route,
        "glyphInspection": {
            "individualProbes": 108, "wholeWordRasters": 4, "scopedHan": 27, "fonts": 4,
            "panels": 3, "fontScale": raster["fontScale"], "originalPngs": 43,
            "distinctPngs": 24, "authorDirectlyInspectedDistinctPngs": 24,
            "observations": str((DESTINATION / "visual-observations.json").relative_to(ROOT)),
            "independentVisualConfirmations": "pending",
        },
        "archivedArtifacts": archived,
        "preservationAudit": {
            "runtimePayloadHashesVerified": 8360, "manifestBytesUnchanged": True,
            "contentVersion": manifest["contentVersion"], "zipEntries": len(infos),
            "compressedBytes": Path(fixture["archive"]).stat().st_size,
            "inflatedBytes": inflated, "retainedBytes": retained, "originalBudgetsPassed": True,
            "androidWorktreeClean": True, "temporaryNativeSourceOrAssetInstalled": False,
            "runtimeOrTeachingEdited": False,
        },
        "independentReviewersLaunched": 0, "publishedAdditions": 104, "remainingAdditions": 1124,
        "lastPublishedCommit": "d7170f11e271a8de47bd2fd152e7196b96bff189",
        "runtimePublished": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
        "diagnostics": [
            "The first evidence-recording attempt stopped before writing contributor artifacts: it incorrectly applied raw-byte hashing to CRLF text worktree files. Corrected to the repository's existing section-specific manifest hashing (text CRLF normalization, binary raw bytes), verified both worktree and frozen archive, and counted retained bytes from the archive including its manifest. No content/native fixture or acceptance guard changed."
        ],
        "limits": observations["limits"] + " Exact archive is the frozen local signed snapshot, not fresh immutable public ZIP acceptance. All prior source/review/process/denial/OOM/read-depth limits retained. No native/HOST recompile or HOST regression rerun.",
    }
    save(ROOT / "docs" / "n1-sources" / "execution-526.json", record)
    print("Native evidence preserved: both terminal0, 43 PNGs/24 distinct inspected, 8360 runtime hashes unchanged.")
