import copy
import difflib
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

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "fba96d45-7b95-46df-9ccf-c5222c8b627e"
HEAD = "fe3ec10b34e5b26fd286d7a79b33b6b6a03afda6"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
PROD = "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
VERSION = "bfe65483a821fc13"
WORK = C / "batch-091-native-revision-654"
FOLDER = R / "docs" / "n1-reviews" / "batch-091-native" / "execution-654"
ARCHIVE = C / "artifacts" / "n1-batch-091-fe3ec10b-revision-envelope.zip"
VERIFICATION = C / "batch-091-native-revision-verification-654.json"
BEFORE = L / "progress-before-654.json"
STAGE = "revised-version-native-passed-awaiting-rendered-confirmation-and-combined-acceptance"
NEXT = (
    "SAME091 only: read docs/n1-sources/execution-654.json and its exact revised-version native "
    "receipts/PNG inspection. Current bfe65483a821fc13 imported through production ContentSync ONCE "
    "from full archive fe3ec10b:1114kanji/5070words/123N1/zeroProblems/Room epoch1. One selected "
    "ArticleTest terminal0/no skips; exact revised mnemonic rendered/captured, both articles, "
    "one mapped pair/two directions/forefront/SystemBack/offline/meaning/onlykunHa/drawing route "
    "retained. GlyphTest NOT rerun; inherit650 fonts/old captures honestly. Next obtain smallest "
    "serial original-session dependent confirmation of the NEW mnemonic PNG, no broad source/"
    "review loops or new blind credit; V1 textual confirmation653 remains resolved. Then perform "
    "current-main normal merge and all combined-tree acceptance gates before any owner fast-forward "
    "publication, terminal green CI and every immutable public ZIP runtime hash/budget check. "
    "No runtimepublication/092/newrunner. Qualified test-only Android1c1b7bf4 retains production"
    "f9b59a2, NOT latest appmain; injectedtrace/giveup NOT human handwriting/successfulMLKit. "
    "Parent19008 owns runner.lock: verify live ancestry/exact session/decoded launcher/"
    "checkpoint/signedheads/whollyclean; NO child reacquire/delete/unlock. Approved control/"
    "committed evidence only, no optional historicalsessionhelpers. Preserve/report/yield actual "
    "new denial/signinghang/uncertain ownership. All original source/baseline/link/reading/"
    "twofamily/native/normal-signing/currentmain/CI/archive18000entries42MiBcompressed80MiBinflated"
    "56MiBretained/perfile-media-safepath/ownerissue gates remain. Published117/1228,1111remaining; "
    "physicalphone/generalrelease/whole-set outstanding."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def clean(head=HEAD):
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    assert not git("diff", PROD, APP, "--", "app/src/main", "core/src/main", "gradle.properties", root=A)


def persist(state):
    temp = C / "progress.654.tmp"
    assert not temp.exists()
    save(temp, state)
    assert load(temp) == state
    temp.replace(C / "progress.json")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest and manifest["contentVersion"] == VERSION
    count = 0
    for kind, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                path = R.joinpath(*name.split("/"))
                media = kind in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                assert (sha(path) if media else sha256(path)) == digest, name
                count += 1
    assert count == 8432
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json")
    return manifest


def ownership():
    command = r"""
$ErrorActionPreference='Stop'
$c='C:\Users\stop-\n1-kanji-workspace\control'
$r=Get-Content "$c\runner.json" -Raw | ConvertFrom-Json
if($r.pid -ne 19008 -or $r.status -ne 'running' -or $r.sessionId -ne 'fba96d45-7b95-46df-9ccf-c5222c8b627e'){throw 'Parent context uncertain'}
$n=$PID; $chain=@()
while($n -gt 0){
 $p=Get-CimInstance Win32_Process -Filter "ProcessId=$n"
 if(-not $p){break}
 $chain+=$p | Select-Object ProcessId,ParentProcessId,Name
 if($n -eq $r.pid){break}
 $n=$p.ParentProcessId
}
if($n -ne $r.pid){throw 'Parent ancestry uncertain'}
$p=Get-CimInstance Win32_Process -Filter "ProcessId=$($r.pid)"
$m=[regex]::Match($p.CommandLine,'-EncodedCommand\s+(\S+)')
if(-not $m.Success){throw 'Launcher command uncertain'}
$decoded=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($m.Groups[1].Value))
if($decoded -notlike "*$c\runner.ps1*"){throw 'Launcher mismatch'}
@{parentRunnerPid=$r.pid;sessionId=$r.sessionId;parentAncestryVerified=$true;launcherCommandMatches=$true;parentLockAccessAttempted=$false;ancestry=$chain} | ConvertTo-Json -Depth 6
"""
    raw = subprocess.check_output(["pwsh", "-NoProfile", "-Command", command], encoding="utf-8")
    role = json.loads(raw)
    assert role["parentAncestryVerified"] and role["launcherCommandMatches"]
    return role


def start():
    clean()
    role = ownership()
    state = load(C / "progress.json")
    assert (state["checkpoint"], state["status"], state["batch"]) == (653, "continue", "091")
    assert state["stage"] == "two-family-mnemonic-confirmed-awaiting-revised-native-and-combined-acceptance"
    assert state["execution653CoordinatorCheckpoint"]["savedCommit"] == HEAD
    assert not BEFORE.exists()
    shutil.copyfile(C / "progress.json", BEFORE)
    request = L / "request.txt"
    raw = request.read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert checkpoint["execution653CoordinatorCheckpoint"]["savedCommit"] == HEAD
    runtime()
    save(L / "native-revision-runner-role.json", role)
    state["execution654StartingState"] = {
        "execution": 654, "batch": "091", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": git("rev-parse", "origin/main"),
        "scope": "SAME091 revised-version full-import/native article confirmation; signed LOCAL evidence only, no publication/092.",
        "request": {"sha256": sha(request), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed before acting; operative contract, complete issue and final653 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved control and committed evidence only; no optional historical session helpers accessed.",
        "actualNewPermissionDenials": [],
    }
    state.update(stage="batch-091-revised-native-confirmation-in-progress",
                 nextAction="SAME091 prepare/compile revised full archive and exact mnemonic selector, run existing ArticleTest only, inspect new rendering, save signed local evidence; all original gates retained.")
    persist(state)
    print("Starting654 persisted; all live historical keys retained.", flush=True)


def prepare():
    clean()
    ownership()
    manifest = runtime()
    assert not WORK.exists() and not VERIFICATION.exists() and not ARCHIVE.exists()
    WORK.mkdir()
    old = R / "docs" / "n1-reviews" / "batch-091-native" / "N1Batch091NativeTest.kt"
    fixture = WORK / old.name
    old_evidence = load(C / "batch-091-native-fixture-verification.json")
    assert sha(old) == old_evidence["fixtureSha256"]
    source = old.read_text(encoding="utf-8")
    article = (R / "kanji" / "\u5203.md").read_text(encoding="utf-8")
    paragraph = next(p for p in article.split("\n\n") if p.startswith("**Modern-shape mnemonic"))
    plain = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", paragraph).replace("**", "")
    selector = json.dumps(plain, ensure_ascii=False)
    before = next(line for line in source.splitlines() if '), "kanji-04")' in line)
    after = '            show(articleBullet(' + selector + '), "kanji-04")'
    assert source.count(before) == 1
    replacements = {
        old_evidence["contentSnapshot"]: HEAD,
        old_evidence["contentVersion"]: VERSION,
        Path(old_evidence["archive"]).name: ARCHIVE.name,
        before: after,
    }
    text = source
    for left, right in replacements.items():
        assert left in text
        text = text.replace(left, right)
    assert text.count("ContentSync(app.db, app.settings.sync, http).sync(") == 1
    assert "ContentParser.parse" not in text
    fixture.write_text(text, encoding="utf-8")
    diff = WORK / "fixture-revised-mnemonic.diff"
    diff.write_text("".join(difflib.unified_diff(
        source.splitlines(keepends=True), text.splitlines(keepends=True),
        fromfile=old.relative_to(R).as_posix(), tofile=fixture.name, n=2)), encoding="utf-8")
    subprocess.run(["git", "archive", "--format=zip", "--prefix=n1-batch-091/",
                    f"--output={ARCHIVE}", HEAD], cwd=R, check=True)
    with zipfile.ZipFile(ARCHIVE) as archive:
        names = archive.namelist()
        assert len(names) == len(set(names)) <= 18000
        assert all(n.startswith("n1-batch-091/") and "\\" not in n and ".." not in n.split("/") for n in names)
        raw = archive.read("n1-batch-091/manifest.json")
        assert raw == (R / "manifest.json").read_bytes()
        retained, verified = len(raw), 0
        for kind, entries in manifest.items():
            if isinstance(entries, dict):
                for name, digest in entries.items():
                    data = archive.read("n1-batch-091/" + name)
                    limit = 150 * 1024 if kind in {"images", "listeningTaskImages"} else (
                        512 * 1024 if kind in {"audio", "listeningTaskAudio"} else 2 * 1024 * 1024)
                    assert len(data) <= limit
                    media = kind in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                    assert hashlib.sha256(data if media else data.replace(b"\r\n", b"\n")).hexdigest() == digest
                    retained += len(data)
                    verified += 1
        inflated = sum(info.file_size for info in archive.infolist())
        assert verified == 8432 and retained <= 56 * 1024 * 1024 and inflated <= 80 * 1024 * 1024
        assert ARCHIVE.stat().st_size <= 42 * 1024 * 1024
        assert not any("/docs/" in n or "/tools/" in n for n in names)
    preparation = {
        "schemaVersion": 1, "execution": 654, "batch": "091", "status": "prepared-not-executed",
        "contentSnapshot": HEAD, "androidSnapshot": APP, "productionBaseline": PROD,
        "contentVersion": VERSION, "expectedCounts": {"kanji": 1114, "words": 5070, "n1": 123},
        "fixture": str(fixture), "fixtureSha256": sha(fixture),
        "archive": str(ARCHIVE), "archiveSha256": sha(ARCHIVE),
        "zipEntries": len(names), "compressedBytes": ARCHIVE.stat().st_size,
        "inflatedBytes": inflated, "retainedBytes": retained, "verifiedRuntimeHashes": verified,
        "manifestEqual": True, "originalBudgetsPassed": True,
        "priorFixture": old.relative_to(R).as_posix(), "priorFixtureSha256": sha(old),
        "exactDiff": str(diff), "exactDiffSha256": sha(diff),
        "revisedMnemonicSelector": plain,
        "selectedCase": "io.github.stopcran.kanji.ui.N1Batch091ArticleTest",
        "selectionRationale": "Smallest fixture change: four exact text/archive identity substitutions; reuse unchanged complete ArticleTest assertions, omit unrelated GlyphTest. No new dictionary or font-probe loop.",
        "nativeExecuted": False, "phoneEvidence": False,
    }
    save(VERIFICATION, preparation)
    wrapper = (C / "run-649-native-compile.ps1").read_text(encoding="utf-8-sig")
    for left, right in {
        "734088c1-c57b-4b51-9ff4-c0fe2a71fe83": L.name,
        "$p.checkpoint -ne 648": "$p.checkpoint -ne 653",
        "batch-091-native-preparation-in-progress": "batch-091-revised-native-confirmation-in-progress",
        "batch-091-native-fixture-verification.json": VERIFICATION.name,
        "n1-batch-091-native-test.apk": "n1-batch-091-native-revision-654-test.apk",
        "n1-batch-091-native-app.apk": "n1-batch-091-native-revision-654-app.apk",
    }.items():
        assert left in wrapper, left
        wrapper = wrapper.replace(left, right)
    assert "File.Open" not in wrapper
    (C / "run-654-native-compile.ps1").write_text(wrapper, encoding="utf-8")
    print("Revised fixture/full archive prepared; all8432runtime hashes and unchanged budgets verified.", flush=True)


def compiled():
    clean()
    ownership()
    preparation = load(VERIFICATION)
    assert (L / "native-compile-exit.txt").read_text(encoding="utf-8-sig").strip() == "0"
    assert "BUILD SUCCESSFUL" in (L / "native-compile.txt").read_text(encoding="utf-8-sig")
    test = C / "artifacts" / "n1-batch-091-native-revision-654-test.apk"
    app = C / "artifacts" / "n1-batch-091-native-revision-654-app.apk"
    assert sha(app) == "0224e8e3f8c744a554da173ec20f133d5d00cb6b6226b001da5ea030856bd407"
    with zipfile.ZipFile(test) as archive:
        assert hashlib.sha256(archive.read("assets/" + ARCHIVE.name)).hexdigest() == sha(ARCHIVE)
        dex = b"".join(archive.read(n) for n in archive.namelist() if n.endswith(".dex"))
        assert b"N1Batch091ArticleTest" in dex
    compiled_receipt = {
        "fixtureVerification": preparation,
        "testApk": {"path": str(test), "sha256": sha(test)},
        "appApk": {"path": str(app), "sha256": sha(app)},
    }
    save(C / "batch-091-revised-compiled-654.json", compiled_receipt)
    wrapper = (C / "run-650-native.ps1").read_text(encoding="utf-8")
    changes = {
        "ec5e6e3f-0cb4-47c8-850d-3b276eba0562": L.name,
        "batch-091-native-attempt-650": "batch-091-native-revision-attempt-654",
        '$compiled = Get-Content "$content\\docs\\n1-sources\\execution-649.json"': '$compiled = Get-Content "$control\\batch-091-revised-compiled-654.json"',
        "execution=650;": "execution=654;",
        "3a31f5eecbe403b81cb0c0bce9a467025feaef89": HEAD,
        "$checkpoint.checkpoint -ne 649": "$checkpoint.checkpoint -ne 653",
        "batch-091-native-execution-in-progress": "batch-091-revised-native-confirmation-in-progress",
        "io.github.stopcran.kanji.ui.N1Batch091GlyphTest,io.github.stopcran.kanji.ui.N1Batch091ArticleTest": preparation["selectedCase"],
        "$result.terminalSuccessCases -eq 2": "$result.terminalSuccessCases -eq 1",
        "'OK \\(2 tests\\)'": "'OK \\(1 test\\)'",
    }
    for left, right in changes.items():
        assert left in wrapper, left
        wrapper = wrapper.replace(left, right)
    assert "File.Open" not in wrapper and "N1Batch091GlyphTest" not in wrapper
    (C / "run-654-native.ps1").write_text(wrapper, encoding="utf-8")
    print("Revised test APK embedded archive verified; one-case native wrapper ready.", flush=True)


def record():
    clean()
    ownership()
    manifest = runtime()
    preparation = load(VERIFICATION)
    compiled_receipt = load(C / "batch-091-revised-compiled-654.json")
    source = C / "artifacts" / "batch-091-native-revision-attempt-654"
    receipt = load(source / "execution.json")
    assert receipt["passed"] and receipt["terminalSuccessCases"] == 1
    assert receipt["ownedHelperStopped"] and receipt["ownedQemuStopped"]
    assert receipt["contentSnapshot"] == HEAD
    assert receipt["archiveSha256"] == preparation["archiveSha256"] == sha(ARCHIVE)
    assert receipt["fixtureSha256"] == preparation["fixtureSha256"] == sha(Path(preparation["fixture"]))
    assert not receipt["parentLockTouched"] and not receipt["guardsChanged"]
    assert not receipt["guestOrAppHeapChanged"]
    raw = (source / "instrumentation.txt").read_text(encoding="utf-8-sig")
    assert raw.count("INSTRUMENTATION_STATUS_CODE: 0") == 1 and "OK (1 test)" in raw
    assert "N1Batch091GlyphTest" not in raw and "N1Batch091ArticleTest" in raw
    route = load(source / "n1-091-article-route.json")
    assert route["passed"] and route["archiveRequests"] == 1
    assert route["contentSnapshot"] == HEAD and route["contentVersion"] == VERSION
    assert (route["importedKanji"], route["importedWords"], route["n1Cards"],
            route["problems"], route["acceptedReadingParserEpoch"]) == (1114, 5070, 123, 0, 1)
    for key in ["reciprocalLinkAndSystemBack", "extraForefrontTransition",
                "meaningQuestionAndFeedback", "onlyKunHaNoOnPersistedGoodAndDone",
                "drawingTraceThenRecall", "drawingGradeRecordedOnNext", "offline"]:
        assert route[key]
    assert route["mappedReciprocalPairs"] == 1 and route["directedLinkTransitions"] == 2
    assert route["completeArticleProjections"] == 2 and route["changedReusedArticles"] == 0
    assert route["quizOnKeys"] == [] and route["quizKunKeys"] == ["\u306f"]
    assert route["fullOnyomi"] == ["\u30b8\u30f3", "\u30cb\u30f3"]
    assert route["fullKunyomi"] == ["\u306f", "\u3084\u3044\u3070", "\u304d.\u308b"]
    assert route["touchInjectedReferenceStrokes"] == 3 and route["directWordGuardCount"] == 5
    for pool in route["productionBuilderN1AndAllExactChoices"].values():
        assert pool["availableCuratedCount"] == 3 and pool["fallbackOptions"] == 0
    pngs = sorted(source.glob("*.png"))
    assert len(pngs) == 47
    assert not FOLDER.exists()
    FOLDER.mkdir()
    artifacts = []

    def retain(path, destination):
        assert not destination.exists()
        shutil.copyfile(path, destination)
        assert sha(path) == sha(destination)
        artifacts.append({"source": str(path), "archive": destination.relative_to(R).as_posix(),
                          "sha256": sha(destination), "bytes": destination.stat().st_size})

    for path in sorted(source.iterdir()):
        assert path.is_file()
        retain(path, FOLDER / path.name)
    for path in sorted(WORK.iterdir()):
        retain(path, FOLDER / path.name)
    for path in [
        Path(__file__), C / "run-654-native-compile.ps1", C / "run-654-native.ps1",
        C / "post-native-revision-654.ps1", VERIFICATION,
        C / "batch-091-revised-compiled-654.json", L / "native-revision-runner-role.json",
        L / "native-compile-command.json", L / "native-compile-start.txt",
        L / "native-compile-end.txt", L / "native-compile-exit.txt",
    ]:
        retain(path, FOLDER / path.name)
    build = FOLDER / "native-compile.txt.gz"
    with build.open("wb") as file:
        with gzip.GzipFile(filename="", mode="wb", fileobj=file, mtime=0) as zipped:
            zipped.write((L / "native-compile.txt").read_bytes())
    assert gzip.decompress(build.read_bytes()) == (L / "native-compile.txt").read_bytes()
    artifacts.append({"source": str(L / "native-compile.txt"), "archive": build.relative_to(R).as_posix(),
                      "sha256": sha(build), "sourceSha256": sha(L / "native-compile.txt"),
                      "losslessGzip": True})
    inspected = FOLDER / "n1-091-kanji-04.png"
    visual = {
        "snapshot": HEAD, "contentVersion": VERSION,
        "reviewer": "Coordinator, actual GPT-6.1 Sol (gpt-6.1-sol); not independent review",
        "scope": "Only newly changed mnemonic paragraph layout and immediately surrounding rendered article.",
        "capturedPngs": 47, "individuallyInspectedPngs": 1, "notSeparatelyInspectedPngs": 46,
        "inspectedOriginalPngs": [{"file": inspected.name, "sha256": sha(inspected)}],
        "disposition": "Viewed original900x2000 capture. Complete revised paragraph, mnemonic/not-etymology heading, separate-stroke/font qualification, crossing-diagram explanation and final nonhistorical disclaimer all visible and readable without clipping. Adjacent reading table retains its explicit sideways-scroll guidance; not a claim that every column is simultaneously visible.",
        "findings": [],
        "limits": [
            "Coordinator observation, not original-reviewer dependent confirmation or native-speaker certification.",
            "Remaining46newPNGs preserved, not separately viewed. Their actual production selector/route assertions passed.",
            "Unchanged GlyphTest not rerun; inherit650's exact font-panel/fallback evidence and limits, not fresh font acceptance.",
            "No phone/latest-app-main/identifiedfallbackface/humanhandwriting/successfulMLKit evidence.",
        ],
    }
    save(FOLDER / "visual-inspection.json", visual)
    artifacts.append({"archive": (FOLDER / "visual-inspection.json").relative_to(R).as_posix(),
                      "sha256": sha(FOLDER / "visual-inspection.json")})
    evidence = {
        "schemaVersion": 1, "execution": 654, "batch": "091", "status": STAGE,
        "startingState": load(C / "progress.json")["execution654StartingState"],
        "preparation": preparation, "compiled": compiled_receipt, "executionReceipt": receipt,
        "nativeRoute": route, "visualInspection": visual, "artifacts": artifacts,
        "runtime": {"runtimeHashesVerified": 8432, "manifestFresh": True,
                    "contentVersion": manifest["contentVersion"],
                    "manifestSha256": sha(R / "manifest.json"), "runtimeUnchanged": True},
        "oldArchiveAndReceiptsPreserved": True,
        "rawOutputWhitespace": "Retain exact adb/emulator logs and generated diff bytes including emitted spaces/blank context. All other staged source/evidence paths checked separately.",
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "revisedVersionNativeConfirmed": True, "independentRenderedConfirmation": "pending",
        "independentReviewersLaunched": 0, "freshGlyphTestClaimed": False,
        "parentLockTouched": False, "actualNewPermissionDenials": [],
        "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": "7100a3873282b54515b9ef130766e77cf151a47b",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": NEXT,
    }
    save(R / "docs" / "n1-sources" / "execution-654.json", evidence)
    print("Revised full native import/route and one actually viewed PNG archived; no publication.", flush=True)


def finalize():
    ownership()
    saved = git("rev-parse", "HEAD")
    clean(saved)
    assert git("rev-parse", "HEAD^") == HEAD
    assert not git("diff", HEAD, saved, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    changed = git("diff", "--name-only", HEAD, saved).splitlines()
    assert all(p.startswith(("docs/n1-reviews/batch-091-native/execution-654/",
                             "docs/n1-sources/execution-654.json")) for p in changed)
    runtime()
    evidence = load(R / "docs" / "n1-sources" / "execution-654.json")
    for item in evidence["artifacts"]:
        path = R.joinpath(*item["archive"].split("/"))
        assert sha(path) == item["sha256"]
        if item.get("losslessGzip"):
            assert hashlib.sha256(gzip.decompress(path.read_bytes())).hexdigest() == item["sourceSha256"]
    prefix = C / "batch-091-native-revision-654-issue-"
    receipt = load(Path(str(prefix) + "receipt.json"))
    posted = load(Path(str(prefix) + "posted.json"))
    body = Path(str(prefix) + "body.txt").read_bytes().decode("utf-8-sig")
    assert receipt["body"] == posted["body"] == body
    assert receipt["user"]["login"] == posted["user"]["login"] == "stop-cran"
    assert receipt["id"] == posted["id"]
    state, before = load(C / "progress.json"), load(BEFORE)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    checkpoint = {
        "schemaVersion": 1, "execution": 654, "checkpoint": 654, "batch": "091",
        "savedCommit": saved, "signature": "G", "status": "continue", "stage": STAGE,
        "evidence": "docs/n1-sources/execution-654.json",
        "contentSnapshot": HEAD, "contentVersion": VERSION,
        "manifestSha256": sha(R / "manifest.json"), "runtimeHashesVerified": 8432,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "revisedVersionNativeConfirmed": True, "terminalSuccessCases": 1, "nativeSkips": 0,
        "archiveRequests": 1, "importedKanji": 1114, "importedWords": 5070, "n1Cards": 123,
        "problems": 0, "acceptedReadingParserEpoch": 1, "freshGlyphTestClaimed": False,
        "capturedPngs": 47, "individuallyInspectedPngs": 1, "independentRenderedConfirmation": "pending",
        "ownedEmulatorPid": 13396, "ownedQemuPid": 15708, "ownedHelpersStopped": True,
        "dedicatedWorktreesClean": True, "parentLockTouched": False,
        "actualNewPermissionDenials": [], "optionalHistoricalSessionHelpersAccessed": False,
        "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": before["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "issueUpdate": receipt["html_url"], "ownerAuthorAndBodyVerified": True,
        "originalRootKeysCompared": len(before), "allOriginalHistoricalRootValuesPreservedExactly": True,
        "nextAction": NEXT,
    }
    state["execution654StartingState"]["status"] = "signed-local-revised-native-checkpoint-complete"
    state["execution654CoordinatorCheckpoint"] = checkpoint
    state["batch091RevisedNativeCheckpoint"] = copy.deepcopy(checkpoint)
    state.update(checkpoint=654, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    for key, value in before.items():
        if key not in allowed:
            assert state[key] == value, key
    persist(state)
    assert load(C / "progress.json") == state
    save(L / "native-revision-final-verification.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2), flush=True)


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "compiled": compiled,
     "record": record, "finalize": finalize}[sys.argv[1]]()
