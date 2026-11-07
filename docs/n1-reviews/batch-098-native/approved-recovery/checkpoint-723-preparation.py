import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "e59095db-3fa8-4186-8272-9eab5c7232a2"
HEAD = "6cca181b977144603296506cfe0b9ed744e2d193"
ANDROID = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
S = R / "docs" / "n1-sources" / "execution-723.json"
D = R / "docs" / "n1-reviews" / "batch-098-native" / "approved-recovery"
STAGE = "batch-098-native-preparation-signed-awaiting-native"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(root, *args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).rstrip("\r\n")


def heads(expected=HEAD):
    assert git(R, "rev-parse", "HEAD") == expected
    for root in (R, A):
        assert git(root, "log", "-1", "--format=%G?") == "G"
    assert git(A, "rev-parse", "HEAD") == ANDROID
    assert not git(A, "status", "--porcelain=v1", "--untracked-files=all")
    assert git(R, "config", "--get", "commit.gpgsign") == "true"


def persist(p):
    before = load(L / "progress-before-723.json")
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in changed:
            assert p[key] == value, key
    target = C / "progress.723.tmp"
    assert not target.exists()
    save(target, p)
    assert load(target) == p
    target.replace(C / "progress.json")


def start():
    heads()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"], p["stage"]) == (
        722, "098", "continue", "batch-098-approved-diagnostic-resolved-awaiting-signed-preparation"
    )
    dirty = git(R, "status", "--porcelain=v1").splitlines()
    assert dirty == ["?? docs/n1-reviews/batch-098-native/", "?? docs/n1-sources/execution-722.json"]
    text = (L / "request.txt").read_text(encoding="utf-8-sig")
    frozen = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1
    )[1])
    assert frozen["checkpoint"] == 722
    recovery = load(C / "batch-098-approved-diagnostic-recovery.json")
    assert frozen["parentExecution722ApprovedDiagnosticRecovery"] == recovery
    assert p["parentExecution722ApprovedDiagnosticRecovery"] == recovery
    role = load(L / "preflight-723.json")
    runner = load(C / "runner.json")
    assert runner["sessionId"] == L.name and runner["pid"] == role["liveParentPid"]
    assert runner["status"] == "running" and not role["lockTouched"]
    assert not (L / "progress-before-723.json").exists()
    save(L / "progress-before-723.json", p)
    p["execution723StartingState"] = {
        "execution": 723, "batch": "098", "startingHead": HEAD, "androidHead": ANDROID,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "Complete normally signed LOCAL native-preparation checkpoint after explicitly approved diagnostic recovery; no native/reviewer/publication/099.",
        "request": {
            "sha256": sha(L / "request.txt"), "bytes": (L / "request.txt").stat().st_size,
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and checkpoint JSON decoded; operative contract, complete approved issue and final checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerLockRole": role,
        "artifactPathPreflight": "Approved workspace inputs, existing contributor evidence and durable control helpers only; no optional historical-session helper access.",
        "actualNewPermissionDenials": [],
    }
    p["stage"] = "batch-098-approved-recovery-preparation-verification"
    persist(p)
    print("Starting723 saved with original history preserved.")


def collect():
    heads()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 722 and "execution723StartingState" in p
    recovery = load(C / "batch-098-approved-diagnostic-recovery.json")
    assert recovery["actualDiagnosticExitCode"] == 0
    assert not recovery["accessPolicyChanged"] and not recovery["signingBypassed"]
    items = [recovery["originalDenial"], recovery["originalExecution"]]
    items += recovery["preservedPreparationEvidence"]
    for item in items:
        assert sha(Path(item["path"])) == item["sha256"], item["path"]
    e722 = load(R / "docs" / "n1-sources" / "execution-722.json")
    assert e722["compileExitCode"] == 0 and not e722["nativeOrVisualExecuted"]
    assert not e722["runtimePublished"] and not e722["localEvidenceCommitCreated"]
    assert len(e722["actualNewPermissionDenials"]) == 1
    fixture = e722["fixtureVerification"]
    for item in (e722["testApk"], e722["appApk"]):
        assert sha(Path(item["path"])) == item["sha256"]
    assert sha(Path(fixture["archive"])) == fixture["archiveSha256"]
    assert sha(Path(fixture["fixture"])) == fixture["fixtureSha256"]
    assert sha(R / e722["committedFixture"]) == fixture["fixtureSha256"]
    spec = importlib.util.spec_from_file_location("prior_runtime", C / "checkpoint-721-android.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    runtime = module.runtime()
    manifest = load(R / "manifest.json")
    with zipfile.ZipFile(fixture["archive"]) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) == fixture["zipEntries"]
        manifest_name = next(n for n in names if n.endswith("/manifest.json"))
        prefix = manifest_name[:-len("manifest.json")]
        assert json.loads(z.read(manifest_name)) == manifest
        count = 0
        for entries in manifest.values():
            if isinstance(entries, dict):
                for name in entries:
                    assert z.read(prefix + name) == R.joinpath(*name.split("/")).read_bytes(), name
                    count += 1
        assert count == 8449
        assert len(names) <= 18000
        assert Path(fixture["archive"]).stat().st_size <= 42 * 1024**2
        assert sum(i.file_size for i in z.infolist()) == fixture["inflatedBytes"] <= 80 * 1024**2
        assert fixture["retainedBytes"] <= 56 * 1024**2
    assert not git(R, "diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert not D.exists() and not S.exists()
    D.mkdir()
    records = []
    for source in (
        C / "batch-098-approved-diagnostic-recovery.json",
        Path(recovery["originalDenial"]["path"]),
        L / "preflight-723.json", C / "preflight-723.ps1", Path(__file__),
    ):
        dest = D / source.name
        shutil.copyfile(source, dest)
        records.append({"path": dest.relative_to(R).as_posix(), "sha256": sha(dest)})
    next_action = (
        "SAME098 execute native/visual gates from the preserved compiled all-example-cells fixture and exact full archive; "
        "preparation is now normally signed LOCAL only, NOT native acceptance or publication. "
        "No redundant compilation/HOST/initial textual review absent new concern. "
        "Original722 denial and blocked evidence remain immutable; approved parent recovery is separately archived. "
        "Fresh actual runner ancestry/clean signed heads and device/PID/local+remoteport ownership (including TimeWait), "
        "owned read-only AVD5580/5581 only, explicitadbserial, no child runner.lock acquire/delete/unlock/readprobe. "
        "Full frozen productionContentSync ONCE; exact N1 ONE curated wrong剛/TWO fallback semantic inspection, "
        "ざい-only/no-kun/full raw readings, ten strokes/four navigation directions/all19Han/fourfonts/Paint/directPNG/"
        "allarticles/reciprocallinks/SystemBack/offline/persistence, named terminal0everycase/noskips/no-2/-3. "
        "BOTH original model-family sessions require bounded rendered confirmation SERIALly before acceptance. "
        "Then latestmain nonrewritingmerge/changedteachingreview/allcurrentPython/validator/vocabulary/manifest/"
        "exactreviewedquizguards/originalarchivebudgets/normalsignedownerfastforward/exactpublicSHA/terminalgreenCI/"
        "EVERYimmutableZIPhash/terminalreceipt/ownerissue60 BEFORE099. "
        "Productionf9 unchanged; qualified test-onlyAndroid1c and HOST2ginit retained, never HOSTinit in native. "
        "Preserve all original source/review/process/read-depth/viewport/fallback/MLKit/phone/generalrelease/whole-set limits "
        "and complete progress history. No historicalsessionhelpers, authoragents, secondrunner, gatewaiver or unreviewedpush. "
        "Signing popup: stop/yield without retry/bypass. New actual denials or uncertain ownership: preserve/report/yield. "
        "Published124/1228,remaining1104/latestpublic69af99e5d7bf34b093959d90dddc7d59fe6393b5 unchanged;098NOTdelivered. "
        "Physicalphone/generalrelease/whole-set outstanding."
    )
    e = {
        "schemaVersion": 1, "execution": 723, "batch": "098", "status": STAGE,
        "startingState": p["execution723StartingState"], "contentSnapshot": HEAD, "androidHead": ANDROID,
        "reviewedTeachingSnapshot": fixture["reviewedTeachingSnapshot"],
        "productionBaseline": e722["productionBaseline"], "approvalRecovery": recovery,
        "originalDenialPreservedUnchanged": True, "original722EvidencePreservedUnchanged": True,
        "originalDeniedSuboperation": recovery["originalDeniedSuboperation"],
        "artifacts": records, "runtime": runtime,
        "fullArchiveRuntimeBytesCompared": count, "archiveSha256": fixture["archiveSha256"],
        "fixtureSha256": fixture["fixtureSha256"], "testApk": e722["testApk"], "appApk": e722["appApk"],
        "compileExitCode": 0, "compilationRerun": False, "hostChecksRerun": False,
        "nativeOrVisualExecuted": False, "independentReviewersLaunched": 0,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "accessPolicyChanged": False, "signingBypassed": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "publishedAdditions": 124, "remainingAdditions": 1104, "lastPublishedCommit": p["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "nextAction": next_action,
        "limits": [
            "Prepared/compiled fixture only; no new native, rendered review, physical phone or publication evidence.",
            "Original blocked722 outcome is historical and was not retroactively relabelled accepted.",
            "Fresh721 host cases and720 textual review retained without rerun or broader review credit.",
            "All original acceptance/publication gates remain; exact N1 fallbacks need actual semantic inspection.",
        ],
    }
    save(S, e)
    print("Evidence collected; all8449 runtime archive payloads match unchanged current tree.")


def finish():
    head = git(R, "rev-parse", "HEAD")
    heads(head)
    assert head != HEAD and git(R, "rev-parse", "HEAD^") == HEAD
    assert not git(R, "status", "--porcelain=v1", "--untracked-files=all")
    assert not git(R, "diff", HEAD, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    e = load(S)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 722
    receipt = load(C / "batch-098-native-723-issue-receipt.json")
    body = (C / "batch-098-native-723-issue-body.txt").read_bytes().decode("utf-8-sig")
    assert receipt["user"]["login"] == "stop-cran" and receipt["body"] == body
    assert head in body and "124/1,228" in body
    checkpoint = {
        "schemaVersion": 1, "execution": 723, "checkpoint": 723, "batch": "098",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "evidence": S.relative_to(R).as_posix(), "issueUpdate": receipt["html_url"],
        "ownerAuthorAndBodyVerified": True, "dedicatedWorktreesClean": True,
        "normalSignedLocalPreparation": True, "nativeOrVisualExecuted": False,
        "runtimeChanged": False, "runtimeAccepted": False, "runtimePublished": False,
        "allRuntimeArchivePayloadsCompared": 8449, "actualNewPermissionDenials": [],
        "original722DenialAndEvidencePreserved": True,
        "parentLockTouched": False, "publishedAdditions": 124, "remainingAdditions": 1104,
        "lastPublishedCommit": p["lastPublishedCommit"], "wholeProjectComplete": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "nextBatchStarted": False, "nextAction": e["nextAction"],
        "originalRootKeysCompared": len(load(L / "progress-before-723.json")),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    p["execution723CoordinatorCheckpoint"] = checkpoint
    p["batch098SignedNativePreparationCheckpoint"] = checkpoint.copy()
    p.update(checkpoint=723, status="continue", stage=STAGE, nextAction=e["nextAction"], blocker=None)
    persist(p)
    save(L / "checkpoint-723.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


{"start": start, "collect": collect, "finish": finish}[sys.argv[1]]()
