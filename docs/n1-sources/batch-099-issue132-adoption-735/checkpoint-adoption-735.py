import gzip
import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
SESSION = "fc7ebb05-a8bf-4501-9314-c7759000faa7"
L = C / "logs" / SESSION
F = R / "docs" / "n1-sources" / "batch-099-issue132-adoption-735"
HEAD = "309189fcda2723ddcf652a9ae5cba7c807d24872"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
MAIN = "2d3a3fa022d48aca6ea8a2ac629bd7ee66b85f9f"
STAGE = "batch-099-approved-kanji-guard-archived-awaiting-content-integration"
NEXT = (
    "SAME099 prerequisite archival complete; read docs/n1-sources/execution-735.json "
    "and docs/n1-sources/batch-099-issue132-adoption-735. Integrate current content "
    "origin/main normally/nonrewriting (last verified2d3a3fa0), inspect approved "
    "validator/docs delta, and author ONLY source-evidenced quiz_exclusions:[冗] "
    "on new剰. Preserve all titles, membership, levels, full/curated reading order, "
    "eleven strokes, source provenance, two reciprocal pairs/four directions, "
    "the one activated baseline pair, reused過剰N2 metadata and seven word guards. "
    "Regenerate manifest, run actual combined Python checks and focused audits, "
    "then normally sign a LOCAL UNREVIEWED changed-tree checkpoint; no unreviewed "
    "push or100. Qualified Android is signedbf30cdead8515739bc0e671d57a54b9a3109dd46 "
    "on n1/issue-132-meaning-exclusions, not latest applicationmain: only approved "
    "direct/symmetric/nontransitive guard and schema-only17->18->19->20 bridges. "
    "Original733/734 evidence and Claude9tool-overlap deviation remain unchanged, "
    "not retroaccepted. New metadata/current archive requires NEW named fixture "
    "carrying quizExclusions through every parse/entity/normal/padding/QuizCard "
    "mapping, fresh justified signed-head HOST/native acceptance with production "
    "ContentSync ONCE and every named terminalcase0/no skips, both target "
    "orientations and arbitrary supported filtered pools. Reconstruction matches "
    "16 original outputs but original733 pool membership/order was not captured. "
    "Obtain only necessary serial ORIGINAL-session dependent semantic/rendered "
    "confirmations (Claude2ac79fdb then GPT240faa46), actual process exits and "
    "per-tool serialization; no newblind credit or repeated-read loop. Separate "
    "app main-pushCI42394221803 remains governed by its archived actual status; "
    "verify terminal success before claiming it green or closing issue132 adoption. "
    "Older APKs ignore guards; compatible-client owner testing only. All signed "
    "latest-main integration/changedteachingreview/combinedchecks/ownerfastforward/"
    "exactremote/terminalgreenCI/EVERYimmutableZIPmanifesthash/18000entries/"
    "42MiBcompressed/80MiBinflated/56MiBretained/perfile-media-safepath/"
    "verifiedownerissue gates remain. No runtime accepted/published, no100, "
    "125delivered/1103remaining unchanged. Physicalphone/generalrelease/whole-set "
    "outstanding. Verify actual live runner ancestry/session/checkpoint/exact "
    "signed heads/whollyclean; parent owns runner.lock throughout child lifetime: "
    "NOchild acquire/delete/unlock/readprobe. Approved control/committed sources/"
    "frozeninputs only. Preserve/report/yield actual new denial/signinghang/"
    "uncertainownership. No secondrunner."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "-C", str(root), "--no-pager", *args], encoding="utf-8"
    ).strip()


def gh(*args):
    return json.loads(subprocess.check_output(["gh", *args], encoding="utf-8"))


def heads(clean=True):
    for root, expected in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        if clean:
            assert not git("status", "--porcelain", root=root)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD^{tree}", root=A) == "8d1d8345da7a862d133f08713d489670d8af67c4"


def start():
    heads()
    before = L / "progress-before-735.json"
    assert not before.exists()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 734 and p["batch"] == "099" and p["status"] == "continue"
    shutil.copyfile(C / "progress.json", before)
    request = L / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    parsed = json.loads(text.split(marker, 1)[1])
    assert parsed["checkpoint"] == 734
    p["execution735StartingState"] = {
        "execution": 735,
        "batch": "099",
        "startedAt": datetime.now().astimezone().isoformat(),
        "startingHead": HEAD,
        "androidHead": APP,
        "freshOriginMain": MAIN,
        "scope": "FIRST required prerequisite archival and normally signed local evidence checkpoint only; no runtime edit/main integration/reviewer/native/publication/100.",
        "request": {
            "sha256": sha(request),
            "bytes": request.stat().st_size,
            "characters": len(text),
            "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed. Operative contract, complete issue and final persisted checkpoint inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerPreflight": load(L / "preflight-735.json"),
        "artifactPathPreflight": "Approved control artifacts and committed source evidence only; no optional historical session-state helper access.",
        "actualNewPermissionDenials": [],
    }
    p.update(status="continue", stage="batch-099-archiving-approved-kanji-guard", blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted without changing the checkpoint or historical records.")


def runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256

    manifest = load(R / "manifest.json")
    original = json.loads(subprocess.check_output(
        ["git", "-C", str(R), "show", HEAD + ":manifest.json"], encoding="utf-8"
    ))
    assert build_manifest(R) == manifest == original
    count = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for path, digest in entries.items():
            actual = sha(R / path) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"
            } else sha256(R / path)
            assert actual == digest, path
            count += 1
    assert count == 8451 and manifest["contentVersion"] == "5408632b5aa1382c"
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    return {
        "verifiedRuntimeHashes": count,
        "contentVersion": manifest["contentVersion"],
        "manifestSha256": sha(R / "manifest.json"),
        "manifestFreshAndUnchanged": True,
    }


def capture():
    heads()
    p = load(C / "progress.json")
    assert p["checkpoint"] == 734 and "execution735StartingState" in p
    adoption = load(C / "batch-099-kanji-guard-adoption.json")
    for item in adoption["artifactInventory"]:
        assert sha(Path(item["path"])) == item["sha256"], item["path"]
    for field in ["originalExecution", "originalRenderedReconciliation"]:
        item = adoption[field]
        assert sha(R / item["path"]) == item["sha256"]
    assert not F.exists()
    F.mkdir()
    for name in [
        "batch-099-kanji-guard-adoption.json",
        "kanji-pair-guard-work-item.txt",
        "kanji-pair-guard-plan-review.txt",
        "kanji-pair-guard-code-review.txt",
        "batch-099-parent-android-recovery.json",
        "run-734-parent-host.ps1",
        "preflight-735.ps1",
        Path(__file__).name,
    ]:
        shutil.copyfile(C / name, F / name)
    shutil.copyfile(L / "preflight-735.json", F / "preflight-735.json")
    shutil.copytree(C / "issue132-frozen-qualification", F / "frozen-qualification")
    shutil.copytree(
        C / "artifacts" / "batch-099-issue132-signed-host", F / "parent-signed-host"
    )
    for name in ["RealContentTest", "RareHanTest"]:
        shutil.copyfile(
            C / "artifacts" / f"batch-099-parent-{name}.xml",
            F / "parent-signed-host" / f"TEST-{name}.xml",
        )
    for name in ["issue132-frozen17-to20.db", "issue132-main20-reopened.db"]:
        source = C / name
        packed = F / (name + ".gz")
        packed.write_bytes(gzip.compress(source.read_bytes(), mtime=0))
        assert gzip.decompress(packed.read_bytes()) == source.read_bytes()
        with sqlite3.connect(source.as_uri() + "?mode=ro&immutable=1", uri=True) as db:
            assert db.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
            assert db.execute("SELECT identity_hash FROM room_master_table WHERE id=42").fetchone()[0] == adoption["schema20Identity"]
    host = adoption["freshSignedHeadHost"]
    start_time = datetime.fromisoformat((F / "parent-signed-host" / "start.txt").read_text().strip())
    end_time = datetime.fromisoformat((F / "parent-signed-host" / "end.txt").read_text().strip())
    assert (F / "parent-signed-host" / "exit.txt").read_text().strip() == "0"
    assert "-Pkotlin.compiler.execution.strategy=in-process" in load(F / "parent-signed-host" / "arguments.json")
    for entry in host["tests"]:
        source = Path(entry["artifactPath"])
        assert sha(source) == entry["sha256"]
        suite = ET.parse(source).getroot()
        assert int(suite.attrib["tests"]) == entry["tests"]
        assert all(int(suite.attrib[key]) == 0 for key in ["failures", "errors", "skipped"])
        timestamp = datetime.fromisoformat(suite.attrib["timestamp"]).replace(tzinfo=start_time.tzinfo)
        assert start_time <= timestamp <= end_time
        assert sorted(c.attrib["name"] for c in suite.findall("testcase")) == sorted(entry["caseNames"])
    qualification = load(F / "frozen-qualification" / "qualification.json")
    for group, record in qualification["tests"].items():
        suites = [ET.parse(path).getroot() for path in (F / "frozen-qualification" / group).glob("*.xml")]
        assert sum(int(s.attrib["tests"]) for s in suites) == record["tests"]
        assert all(int(s.attrib[key]) == 0 for s in suites for key in ["failures", "errors", "skipped"])
    schema = A / "app" / "schemas" / "io.github.stopcran.kanji.data.AppDatabase" / "20.json"
    assert sha(schema) == adoption["schema20Sha256"]
    public = {}
    for label, repo, number in [
        ("app-pr", "stop-cran/kanji-cards-android", 133),
        ("content-pr", "stop-cran/learning-japanese", 63),
    ]:
        receipt = gh("pr", "view", str(number), "--repo", repo, "--json",
                     "number,state,mergedAt,mergeCommit,headRefOid,url")
        expected = adoption["appMain"] if label == "app-pr" else MAIN
        assert receipt["state"] == "MERGED" and receipt["mergeCommit"]["oid"] == expected
        save(F / (label + ".json"), receipt)
        public[label] = receipt
    for label, repo, run, expected, required in [
        ("app-pr-ci", "stop-cran/kanji-cards-android", 42392821090, adoption["appMain"], True),
        ("app-main-ci", "stop-cran/kanji-cards-android", 42394221803, adoption["appMain"], False),
        ("content-pr-ci", "stop-cran/learning-japanese", 42392566316, MAIN, True),
        ("content-main-ci", "stop-cran/learning-japanese", 42393132653, MAIN, True),
    ]:
        receipt = gh("run", "view", str(run), "--repo", repo, "--json",
                     "databaseId,headSha,status,conclusion,url,jobs")
        assert receipt["headSha"] == expected
        if required:
            assert receipt["status"] == "completed" and receipt["conclusion"] == "success"
        save(F / (label + ".json"), receipt)
        public[label] = {k: v for k, v in receipt.items() if k != "jobs"}
    issue = gh("issue", "view", "132", "--repo", "stop-cran/kanji-cards-android",
               "--json", "number,title,body,state,url,author,comments")
    assert issue["author"]["login"] == "stop-cran"
    assert "Ok, approve, please proceed" in issue["body"]
    for name in ["kanji-pair-guard-plan-review.txt", "kanji-pair-guard-code-review.txt"]:
        expected = (C / name).read_text(encoding="utf-8-sig").strip()
        assert any(c["author"]["login"] == "stop-cran" and c["body"].replace("\r\n", "\n").strip() == expected
                   for c in issue["comments"])
    save(F / "issue132.json", issue)
    frozen_remote = subprocess.check_output([
        "git", "-C", str(A), "ls-remote", "--heads", "origin",
        "refs/heads/n1/issue-132-meaning-exclusions"
    ], encoding="utf-8").strip()
    assert frozen_remote.split()[0] == APP
    (F / "qualified-branch-remote.txt").write_text(frozen_remote + "\n", encoding="utf-8")
    evidence = {
        "schemaVersion": 1,
        "execution": 735,
        "batch": "099",
        "status": STAGE,
        "startingState": p["execution735StartingState"],
        "snapshot": HEAD,
        "androidHead": APP,
        "freshOriginMain": MAIN,
        "artifacts": F.relative_to(R).as_posix(),
        "publicPrerequisiteReceipts": public,
        "qualification": {
            "inheritedTargetedCoreTests": 53,
            "inheritedTargetedAppTests": 92,
            "inheritedCrossApplicationReopenTests": 1,
            "parentFreshSignedHeadHostTests": 4,
            "allArchivedXmlCountsAndNoSkipsVerified": True,
            "parentHostExplicitStartAndXmlFreshnessVerified": True,
            "archivedParentArtifactHashesVerified": True,
            "schema20Identity": adoption["schema20Identity"],
            "schema20Sha256": adoption["schema20Sha256"],
            "bothClosedDatabaseHashesAndIntegrityVerified": True,
            "qualifiedBranchRemoteExact": True,
            "testsNewlyExecutedHere": 0,
            "limits": "Archival verification of supplied actual receipts, not newly executed JVM/native tests or new independent code/linguistic review. Original qualification's notRun/newCommits fields describe its earlier staged snapshot; signed publication and later parent HOST are separately recorded, not silently rewritten.",
        },
        "runtime": runtime(),
        "parentWrapper": {
            "path": (F / "run-734-parent-host.ps1").relative_to(R).as_posix(),
            "role": "IMMUTABLE HISTORICAL PARENT-ONLY recipe archived for provenance; not invoked or copied into a child wrapper. Its exclusiveLockAvailable receipt belongs to the parent recovery context, not this child's ownership test.",
            "executedHere": False,
        },
        "preservedFindings": {
            "N099-FALLBACK-JOU": "Approved mechanism exists, but content declaration and changed-tree semantic/native/rendered acceptance remain open. No retroacceptance.",
            "N099-RENDERED-PROTOCOL-734": "Original Claude9tool-overlap deviation remains open. Reports and audit unchanged; necessary compliant dependent confirmation still required.",
            "reconstructedPools": "All16 original outputs reproduced in prerequisite evidence, but original733 membership/order was not captured; reconstruction is not original-membership proof.",
        },
        "codeReviewModel": "Unavailable in supplied plan/code-review receipts; no model-family or original099-review credit claimed.",
        "normalMainIntegrationPerformed": False,
        "runtimeChanged": False,
        "runtimeAccepted": False,
        "runtimePublished": False,
        "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False,
        "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "reviewClosed": [],
        "published": [],
        "publishedAdditions": 125,
        "remainingAdditions": 1103,
        "lastPublishedCommit": "d5a376ee2b014aae3c47c58eea47b327e44be6d2",
        "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False,
        "nextBatchStarted": False,
        "nextAction": NEXT,
    }
    save(R / "docs" / "n1-sources" / "execution-735.json", evidence)
    inventory = [
        {"path": path.relative_to(R).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(F.rglob("*")) if path.is_file()
    ]
    save(F / "inventory.json", inventory)
    batch_path = R / "docs" / "n1-sources" / "batch-099-progress.json"
    batch = load(batch_path)
    assert "approvedKanjiGuardAdoption735" not in batch
    batch["approvedKanjiGuardAdoption735"] = {
        "evidence": "docs/n1-sources/execution-735.json",
        "artifacts": F.relative_to(R).as_posix(),
        "qualifiedAndroidHead": APP,
        "contentDeclarationAdded": False,
        "runtimeAccepted": False,
        "runtimePublished": False,
        "original734Retroaccepted": False,
        "nextAction": NEXT,
    }
    save(batch_path, batch)
    print("Verified and archived prerequisite receipts; runtime and original734 evidence unchanged.")


def seal():
    saved = git("rev-parse", "HEAD")
    assert saved != HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("rev-parse", "HEAD^") == HEAD
    evidence = load(R / "docs" / "n1-sources" / "execution-735.json")
    assert runtime() == evidence["runtime"]
    assert (L / "validate-735.txt").read_text(encoding="utf-8-sig").strip().endswith("0 error(s)")
    baseline = load(L / "progress-before-735.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 734
    adoption = load(C / "batch-099-kanji-guard-adoption.json")
    for field in ["originalExecution", "originalRenderedReconciliation"]:
        assert sha(R / adoption[field]["path"]) == adoption[field]["sha256"]
    issue = load(L / "issue-735-reread.json")
    expected_body = (C / "batch-099-adoption-735-issue-body.txt").read_bytes().decode("utf-8-sig")
    assert issue["user"]["login"] == "stop-cran" and issue["body"] == expected_body
    checkpoint = {
        "schemaVersion": 1,
        "execution": 735,
        "checkpoint": 735,
        "batch": "099",
        "savedCommit": saved,
        "signature": "G",
        "status": "continue",
        "stage": STAGE,
        "evidence": "docs/n1-sources/execution-735.json",
        "artifacts": F.relative_to(R).as_posix(),
        "issueUpdate": issue["html_url"],
        "ownerAuthorAndBodyVerified": True,
        "dedicatedWorktreesClean": True,
        "runtime": evidence["runtime"],
        "qualifiedAndroidHead": APP,
        "appMainPushCi": evidence["publicPrerequisiteReceipts"]["app-main-ci"],
        "normalMainIntegrationPerformed": False,
        "contentDeclarationAdded": False,
        "runtimeChanged": False,
        "runtimeAccepted": False,
        "runtimePublished": False,
        "original734Retroaccepted": False,
        "independentRenderedReviewClosed": False,
        "reviewClosed": [],
        "published": [],
        "publishedAdditions": 125,
        "remainingAdditions": 1103,
        "lastPublishedCommit": baseline["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False,
        "nextBatchStarted": False,
        "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [],
        "nextAction": NEXT,
        "originalRootKeysCompared": len(baseline),
        "allOriginalHistoricalRootValuesPreservedExactly": True,
    }
    changed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in baseline.items() if k not in changed)
    p.update(checkpoint=735, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution735CoordinatorCheckpoint"] = checkpoint
    p["batch099KanjiGuardArchivalCheckpoint"] = checkpoint
    assert all(p[k] == v for k, v in baseline.items() if k not in changed)
    save(C / "progress.json", p)
    after = load(C / "progress.json")
    assert all(after[k] == v for k, v in baseline.items() if k not in changed)
    save(L / "checkpoint-735.json", checkpoint)
    print("Checkpoint735 sealed; all historical root values preserved; same099 continues.")


def checks():
    assert (L / "validate-735.txt").read_text(encoding="utf-8-sig").strip() == "0 error(s)"
    assert "version 5408632b5aa1382c" in (L / "manifest-735.txt").read_text(encoding="utf-8-sig")
    for name in ["validate-735.txt", "manifest-735.txt"]:
        shutil.copyfile(L / name, F / name)
    packed_sources = []
    for relative in [
        Path("frozen-qualification") / "frozen-backport.patch",
        Path("parent-signed-host") / "gradle.txt",
    ]:
        source = F / relative
        packed = source.with_suffix(source.suffix + ".gz")
        if source.exists():
            raw = source.read_bytes()
            packed.write_bytes(gzip.compress(raw, mtime=0))
            assert gzip.decompress(packed.read_bytes()) == raw
            source.unlink()
        else:
            raw = gzip.decompress(packed.read_bytes())
        original = (C / "issue132-frozen-qualification" / relative.name
                    if relative.parent.name == "frozen-qualification"
                    else C / "artifacts" / "batch-099-issue132-signed-host" / relative.name)
        assert raw == original.read_bytes()
        packed_sources.append({
            "path": packed.relative_to(R).as_posix(),
            "originalSha256": hashlib.sha256(raw).hexdigest(),
            "roundTripExact": True,
        })
    shutil.copyfile(Path(__file__), F / Path(__file__).name)
    evidence_path = R / "docs" / "n1-sources" / "execution-735.json"
    evidence = load(evidence_path)
    evidence["contentChecks"] = {
        "validatorErrors": 0,
        "manifestFreshAndUnchanged": True,
        "runtimeHashesVerified": 8451,
        "archiveExportIgnore": True,
        "scope": "Documentation/evidence-only checkpoint; no code or teaching changes and no new JVM/native/model-review acceptance claimed.",
    }
    evidence["packedSourceArtifacts"] = packed_sources
    evidence["archivalDiagnostic"] = (
        "Initial staged whitespace check reported blank-context patch lines and one "
        "Gradle-emitted trailing space. Preserve exact originals as deterministic gzip "
        "with round-trip byte verification instead of editing historical evidence. "
        "Control originals remain unchanged."
    )
    assert evidence["runtime"] == runtime()
    save(evidence_path, evidence)
    inventory = [
        {"path": path.relative_to(R).as_posix(), "bytes": path.stat().st_size, "sha256": sha(path)}
        for path in sorted(F.rglob("*")) if path.is_file() and path.name != "inventory.json"
    ]
    save(F / "inventory.json", inventory)
    adoption = load(F / "batch-099-kanji-guard-adoption.json")
    for field in ["originalExecution", "originalRenderedReconciliation"]:
        assert sha(R / adoption[field]["path"]) == adoption[field]["sha256"]
    assert not git("status", "--porcelain", root=A)
    print(f"Precommit checks recorded; {len(inventory)} archived artifacts verified; runtime unchanged.")


if __name__ == "__main__":
    {"start": start, "capture": capture, "checks": checks, "seal": seal}[sys.argv[1]]()
