"""Preserve an actual reviewer denial without retrying its denied read."""
import argparse
import gzip
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "rollout-recovered" / "learning-japanese"
L = C / "logs" / "c60bb35d-39a2-4212-b8ce-adede31eff34"
D = C / "artifacts" / "batch-108-textual-862"
V = R / "docs" / "n1-reviews" / "batch-108-textual-862"
S = R / "docs" / "n1-sources"
HEAD = "9955ac122d1b4f1084f702d3d6d5afeb82d35e3a"
PUBLIC = "e766221c2a9c5ada2314805c307e534ccf4537ec"
DENIED = str(C.parent / "auditor-compatibility-isolated" / ".git" / "worktrees" / "learning-japanese" / "HEAD")


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(R), *args],
        encoding="utf-8",
    ).strip()


def write(path, value):
    with path.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(value, ensure_ascii=True, indent=2) + "\n")


def state():
    p = load(C / "progress.json")
    runner = load(C / "runner.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (861, "108", "continue")
    assert runner["status"] == "running" and runner["sessionId"] == L.name and runner["pid"] == 27864
    result = subprocess.run(
        ["pwsh", "-NoProfile", "-Command",
         "$c=Get-CimInstance Win32_Process -Filter 'ProcessId=29432';"
         "if ($c.ParentProcessId -ne 27864 -or -not (Get-Process -Id 27864 -ErrorAction SilentlyContinue)) {exit 1}"],
        capture_output=True,
    )
    assert result.returncode == 0
    assert p["lastPublishedCommit"] == PUBLIC and p["remainingAdditions"] == 1094
    return p


def archive():
    state()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    e = load(D / "claude-execution.json")
    assert e["actualModels"] == ["claude-opus-5.5"] and e["processExited"]
    assert len(e["calls"]) == 2 and len(e["actualDenials"]) == 1
    assert e["actualDenials"][0]["arguments"]["path"] == DENIED
    assert not e["mechanicalExecutionAccepted"] and len(e["missingCompleteResources"]) == 21
    assert not (D / "gpt-active.json").exists()
    assert not V.exists()
    V.mkdir()
    for path in sorted(D.iterdir()):
        assert path.is_file()
        shutil.copyfile(path, V / path.name)
    for name in ("review-batch-108-862.py", "checkpoint-batch-108-textual-862.py",
                 "post-batch-108-textual-862.ps1", "batch-108-textual-862-issue-template.txt"):
        shutil.copyfile(C / name, V / name)
    log_dir = C / "review-logs" / "batch-108-textual-862-claude"
    log_receipts = []
    for path in sorted(log_dir.glob("*.log")):
        target = V / (path.name + ".gz")
        target.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        assert gzip.decompress(target.read_bytes()) == path.read_bytes()
        log_receipts.append({"originalPath": str(path), "originalSha256": sha(path),
                             "archive": target.name, "archiveSha256": sha(target)})
    blocker = {
        "kind": "actual-reviewer-tool-permission-denial", "execution": 862, "batch": "108",
        "reviewSnapshot": HEAD, "actualModel": "claude-opus-5.5",
        "reviewerSession": e["sessionId"], "reviewerPid": e["pid"], "reviewerProcessExited": True,
        "tool": "view", "path": DENIED,
        "actualDenial": e["actualDenials"][0], "retried": False,
        "alternateToolOrPathUsedToEvade": False, "permissionsPoliciesAclsChanged": False,
        "fullReport": "docs/n1-reviews/batch-108-textual-862/claude.md",
        "rawExecution": "docs/n1-reviews/batch-108-textual-862/claude.jsonl",
        "rawExecutionSha256": sha(D / "claude.jsonl"), "originalReportSha256": sha(D / "claude.md"),
        "actualReturnedScope": "Only the worktree .git pointer returned; HEAD denied. Ref and all nineteen source packet parts unattempted.",
        "allFourArticlesAllThreeFacets": "UNVERIFIED; no independent content review occurred.",
        "secondReviewerStarted": False, "reviewAccepted": False, "parentLockTouched": False,
        "safeNextAction": "Obtain actual narrow interactive one-request permission for the original reviewer HEAD/ref authentication, under the existing owner grant. Preserve this denial and original session. Do not retry noninteractively, broaden directory/session grants, use a receipt-only substitution or reroute reads. Then finish both blind serial different-family initial textual reviews on the unchanged exact snapshot before reconciliation and later gates.",
    }
    write(S / "execution-862-permission-blocker.json", blocker)
    files = [{"path": p.relative_to(R).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size}
             for p in sorted(V.iterdir())]
    record = {
        "schemaVersion": 1, "execution": 862, "batch": "108",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "status": "blocked-on-actual-reviewer-metadata-permission-denial",
        "reviewSnapshot": HEAD, "publishedBase": PUBLIC,
        "membership": ["\u52e7"], "blindCommonPacketBytes": 263867, "blindCommonPacketParts": 19,
        "preparedCompleteArticleBodies": 44, "preparedCompleteDictionaryFamilies": 64,
        "preparedDistinctRawCharacterRecords": 14,
        "preparedScopeIsNotActualReviewerReadScope": True,
        "actualModel": "claude-opus-5.5", "reviewerSession": e["sessionId"],
        "reviewerProcessExited": True, "reviewerToolCalls": 2, "successfulToolCalls": 1,
        "actualDenials": 1, "observedToolOverlaps": 0, "sourcePacketPartsRead": 0,
        "secondReviewerStarted": False, "independentContentReviewAccepted": False,
        "verdicts": {name: {"correctness": "UNVERIFIED", "scopedCoverage": "UNVERIFIED",
                            "comprehensibility": "UNVERIFIED"}
                     for name in load(D / "provenance.json")["affectedArticles"]},
        "blocker": blocker, "retainedOriginalEvidence": files, "processLogs": log_receipts,
        "runtimeChanged": False, "runtimePublished": False, "pushed": False,
        "publishedAdditions": 134, "remainingAdditions": 1094,
        "hostNativeRenderedOrPublicationAttempted": False, "parentLockTouched": False,
        "fullHistoryBefore": str(L / "progress-before-862.json"),
        "limits": "Source-backed draft remains unreviewed and unpublished. Packet preparation is not independent reviewer evidence. No phone, handwriting-model, general-release or whole-set acceptance.",
    }
    write(S / "execution-862.json", record)
    print("Original denied execution/report and complete blind packet archived; no runtime edit or second reviewer.")


def package():
    state()
    assert git("rev-parse", "HEAD") == HEAD
    names = ["batch-108-cli-catalog-862.txt", "common-packet.txt", "claude.jsonl", "claude-usage.json"]
    names.extend(f"common-part-{i:02}.txt" for i in range(1, 20))
    mappings = []
    for name in names:
        original, archived = D / name, V / name
        assert original.read_bytes() == archived.read_bytes()
        target = V / (name + ".gz")
        assert not target.exists()
        target.write_bytes(gzip.compress(original.read_bytes(), mtime=0))
        assert gzip.decompress(target.read_bytes()) == original.read_bytes()
        mappings.append({"originalArtifact": name, "originalSha256": sha(original),
                         "archive": target.name, "archiveSha256": sha(target)})
        archived.unlink()
    blocker_path = S / "execution-862-permission-blocker.json"
    blocker = load(blocker_path)
    blocker["rawExecution"] += ".gz"
    blocker_path.write_text(json.dumps(blocker, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    record_path = S / "execution-862.json"
    record = load(record_path)
    record["blocker"] = blocker
    record["bytePreservingPackaging"] = {
        "reason": "Initial git diff --cached --check rejected numbered blank source lines and a catalog trailing blank. Signing was never reached. Exact original artifacts are gzip-packed, not whitespace-rewritten; all decompressed hashes verified.",
        "artifacts": mappings,
        "originalArtifactsUnmodifiedInControl": True,
    }
    shutil.copyfile(C / "checkpoint-batch-108-textual-862.py", V / "checkpoint-batch-108-textual-862.py")
    record["retainedOriginalEvidence"] = [
        {"path": p.relative_to(R).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size}
        for p in sorted(V.iterdir())
    ]
    record_path.write_text(json.dumps(record, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print("Exact original source packet/catalog/JSONL/usage gzip-packaged and decompression hashes verified.")


def finish():
    old = state()
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert not git("diff", "--name-only", HEAD, head, "--", "kanji", "words", "articles",
                   "strokes", "manifest.json", "grammar", "listening", "listening-tasks",
                   "audio", "task-audio", "task-images")
    issue = load(D / "issue-receipt.json")
    assert issue["verified"] and issue["author"] == "stop-cran" and issue["localCommit"] == head
    blocker = load(S / "execution-862-permission-blocker.json")
    action = (
        "SAME108 BLOCKED after actual original Claude view denial on recovered Git HEAD metadata; "
        "do not launch GPT or retry/reroute denied reads. Original session "
        "c3aef375-64f3-485e-810a-cb08336243aa exited. Only worktree .git pointer returned; "
        "HEAD denied; branch ref/all19 common source parts unattempted. ALL4articles/"
        "ALL3facets UNVERIFIED, no content-review credit. Read execution-862.json and original "
        "report/execution in docs\\n1-reviews\\batch-108-textual-862. Obtain actual narrow "
        "interactive one-request approvals for original-session exact HEAD/ref reads under "
        "existing owner metadata grant; no directory/session/global grants, alternate path/tool, "
        "receipt-only substitution or noninteractive retry. Resume SAME signed9955ac draft, "
        "both blind serial different-family textual reviews, actual models/complete returned "
        "scope/process exit/serial internal tools, then evidence-based reconciliation. "
        "All source/current-runtime audit/HOST/production options/native full ContentSync ONCE/"
        "fourfonts/rendered/original-session confirmations/latestmain nonrewriting integration/"
        "changedteaching rereview/combined checks/normal signing/owner fastforward/exact terminal "
        "greenCI/EVERY immutableZIP runtimehash and original budgets/perfile-media-safepath/"
        "verifiedownerissue gates remain before any publication or109. Preserve FULLlivehistory/"
        "792correction/all prior denials/OOMs/accepted publications and unresolved 定/違,"
        "支払う/支払,勘/識,勅/訓. Recovered siblings only; committedsources/approvedinputs/"
        "controlhelpers, no optional historicalsessionrecipes. Parent owns runner.lock; "
        "NOchild reacquire/delete/unlock/readprobe; authenticate live ancestry/currentcheckpoint/"
        "signedheads/cleanstate. Preserve/report/yield actual denial/signinghang/uncertainownership. "
        "Published134/1228,remaining1094 unchanged; six earlier-level dispositions not issue60 "
        "acceptancecredit. Compatible clients125/132 required; physicalphone/handwritingmodel/"
        "generalrelease/whole-setacceptance outstanding; project incomplete."
    )
    new = json.loads(json.dumps(old))
    new["execution862PermissionBlocker"] = {
        **blocker, "signedEvidenceCommit": head, "signature": "G", "ownerReport": issue["url"],
    }
    new["execution862CoordinatorCheckpoint"] = {
        "execution": 862, "batch": "108", "status": "blocked", "signedLocalCommit": head,
        "signature": "G", "record": "docs/n1-sources/execution-862.json",
        "recordSha256": sha(S / "execution-862.json"), "runtimeUnchangedFromUnreviewedSnapshot": HEAD,
        "reviewAccepted": False, "secondReviewerStarted": False, "pushed": False,
        "runtimePublished": False, "publishedAdditions": 134, "remainingAdditions": 1094,
        "issueUpdate": issue["url"], "ownerAuthorAndBodyAndUrlVerified": True,
        "parentLockTouched": False, "nextAction": action,
    }
    new.update(checkpoint=862, status="blocked", stage="batch-108-reviewer-metadata-permission-blocked",
               nextAction=action, blocker={**blocker, "signedEvidenceCommit": head, "ownerReport": issue["url"]})
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(new[key] == old[key] for key in old if key not in mutable)
    before = L / "progress-before-finish-862.json"
    shutil.copyfile(C / "progress.json", before)
    write(L / "checkpoint-after-862.json", new)
    temp = C / "progress.json.862-finish.tmp"
    write(temp, new)
    assert load(temp) == new and load(C / "progress.json") == old
    temp.replace(C / "progress.json")
    assert load(C / "progress.json") == new
    print(json.dumps({"checkpoint": 862, "status": "blocked", "head": head,
                      "historicalRootKeysPreserved": len(old), "issue": issue["url"]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("archive", "package", "finish"))
    args = parser.parse_args()
    {"archive": archive, "package": package, "finish": finish}[args.operation]()
