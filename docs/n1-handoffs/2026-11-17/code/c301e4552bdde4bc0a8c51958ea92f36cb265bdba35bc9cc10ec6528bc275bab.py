"""Verify the contributor receipt's entire served tree, then post one owner checkpoint."""
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard
from publish_b132 import api
from record_b117_publication_v3 import validate_delivery
from run_b132_closure_checks import HERE, PROGRESS, REPO
from verify_b132_packet import RUNNER
from verify_b132_sources import FINGERPRINT, OWNER, TRAILER, Git

PUBLISHED = "902d6021214aaf28f8bdf41b9920b0d76a79b83c"
REPOSITORY = "stop-cran/learning-japanese"
EQUALITY = HERE / "receipt-tree-check-001" / "receipt.json"
CI = HERE / "receipt-ci-run.json"


def stream_sha(stream, guard):
    digest = hashlib.sha256()
    while chunk := stream.read(64 * 1024):
        guard.check()
        digest.update(chunk)
    return digest.hexdigest()


def entries(folder, commit, manifest, ci, guard):
    receipt = json.loads(frozen(folder / "receipt.json"))
    validate_delivery(commit, manifest, ci, receipt)
    require(receipt["verifiedRuntimeHashes"] == 8739 and receipt["contentVersion"] == "adbf488f76c55cc2",
            "Archive does not establish exact B132 delivery")
    path = folder / f"zipball-{commit[:12]}.zip"
    with path.open("rb") as stream:
        require(stream_sha(stream, guard) == receipt["sha256"], "Verified ZIP bytes changed")
    result = {}
    with zipfile.ZipFile(path) as archive:
        roots = {item.filename.split("/")[0] for item in archive.infolist()}
        require(len(roots) == 1, "Archive has multiple roots")
        prefix = roots.pop() + "/"
        require(prefix.endswith(commit[:7] + "/"), "Wrong archive root")
        for item in archive.infolist():
            guard.check()
            name = item.filename[len(prefix):]
            if not name:
                continue
            require(name not in result, "Duplicate served path")
            with archive.open(item) as stream:
                result[name] = (item.is_dir(), stream_sha(stream, guard))
    require(len(result) + 1 == receipt["zipEntries"], "Archive entry count differs")
    return result, receipt


def receipt_tree(git, commit):
    require(re.fullmatch(r"[0-9a-f]{40}", commit), "Full receipt commit required")
    require(git("rev-parse", "HEAD").decode().strip() == commit
            and not git("status", "--porcelain=v1", "--untracked-files=all")
            and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", commit).decode().strip()
            == f"{PUBLISHED}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
            and TRAILER in git("show", "-s", "--format=%B", commit), "Receipt identity or lineage differs")
    paths = git("diff", "--name-only", PUBLISHED, commit).decode().splitlines()
    require(paths and all(path == PROGRESS or path.startswith("docs/n1-reviews/batch-132-publication/")
                         for path in paths), "Receipt changed unrelated paths")
    manifest = git("show", PUBLISHED + ":manifest.json")
    require(git("show", commit + ":manifest.json") == manifest, "Receipt changed runtime manifest")
    return manifest


def equal(commit):
    require(not EQUALITY.exists(), "Preserve existing equality receipt")
    guard, _ = start_guard("B132 full served-tree equality")
    try:
        git = Git(REPO, RUNNER, guard)
        manifest = receipt_tree(git, commit)
        published_ci = json.loads(frozen(REPO / "docs/n1-reviews/batch-132-publication/ci-run.json"))
        receipt_ci = json.loads(frozen(CI))
        before, published = entries(HERE / "publication-zip-001", PUBLISHED, manifest, published_ci, guard)
        after, receipt = entries(HERE / "receipt-zip-001", commit, manifest, receipt_ci, guard)
        result = {
            "publishedCommit": PUBLISHED, "receiptCommit": commit,
            "publishedZipSha256": published["sha256"], "receiptZipSha256": receipt["sha256"],
            "entries": [len(before), len(after)], "namesEqual": before.keys() == after.keys(),
            "contentEqual": before == after, "onlyInPublished": sorted(before.keys() - after.keys()),
            "onlyInReceipt": sorted(after.keys() - before.keys()),
            "differing": sorted(name for name in before.keys() & after.keys() if before[name] != after[name]),
            "method": "Prefix-stripped names,directory flags and streamed SHA-256 of every served entry; "
                      "both archive hashes independently checked.",
            "verifierSha256": sha(frozen(Path(__file__))),
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"] and result["namesEqual"] and result["contentEqual"],
            "Publication and receipt served trees are not verified equal")
    result["memory"] = memory
    print(json.dumps(freeze_json(EQUALITY, result)))


def checkpoint(commit):
    output = HERE / "issue60-checkpoint-receipt-001.json"
    require(not output.exists(), "Checkpoint already recorded")
    guard, _ = start_guard("B132 owner issue checkpoint")
    try:
        git = Git(REPO, RUNNER, guard)
        receipt_tree(git, commit)
        require(json.loads(api(git, "api", "user"))["login"] == "stop-cran", "Wrong checkpoint author")
        require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit,
                "Receipt is not current remote main")
        remote = json.loads(api(git, "api", f"repos/{REPOSITORY}/commits/{commit}"))
        require(remote["sha"] == commit and remote["commit"]["verification"]["verified"]
                and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
                "Remote receipt identity differs")
        ci = json.loads(frozen(CI))
        live_ci = json.loads(api(git, "run", "view", str(ci["databaseId"]), "--repo", REPOSITORY, "--json",
                                 "databaseId,headSha,status,conclusion,url,workflowName"))
        require(live_ci["headSha"] == commit and live_ci["status"] == "completed"
                and live_ci["conclusion"] == "success" and live_ci["workflowName"] == "Validate content",
                "Exact receipt CI is not successful")
        equal_raw = frozen(EQUALITY)
        equality = json.loads(equal_raw)
        require(equality["publishedCommit"] == PUBLISHED and equality["receiptCommit"] == commit
                and equality["namesEqual"] and equality["contentEqual"]
                and not equality["memory"]["breach"] and not equality["differing"]
                and equality["entries"][0] == equality["entries"][1] > 8739, "Equality proof differs")
        ledger = json.loads(git("show", commit + ":" + PROGRESS))
        require(ledger["runtimePublished"] and ledger["published"] == ["\u5893"]
                and ledger["accounting"]["publishedPendingRecordsWithCards"] == 268
                and ledger["accounting"]["publishedN1Additions"] == 262
                and ledger["accounting"]["undelivered"] == 960
                and not ledger["accounting"]["overallN1TaskComplete"], "Published accounting differs")
        body = json.loads(frozen(HERE / "issue60-publication-comment.json"))["body"]
        body += (f"\n\nThe owner-signed [publication receipt]({remote['html_url']}) also passed "
                 f"[its CI]({live_ci['url']}); all **{equality['entries'][0]:,} served entries** "
                 "are byte-identical after stripping the archive-root prefix. The runtime manifest is unchanged.")
        matches, page = [], 1
        while True:
            comments = json.loads(api(git, "api", f"repos/{REPOSITORY}/issues/60/comments?per_page=100&page={page}"))
            matches.extend(item for item in comments if re.search(r"\bB132\b", item["body"]))
            if len(comments) < 100:
                break
            page += 1
        request = HERE / "issue60-checkpoint-001.json"
        if request.exists():
            require(json.loads(frozen(request)) == {"body": body}, "Existing checkpoint request differs")
        else:
            freeze_json(request, {"body": body})
        if matches:
            require(len(matches) == 1 and matches[0]["body"] == body
                    and matches[0]["user"]["login"] == "stop-cran", "Existing B132 checkpoint differs")
            posted = matches[0]
        else:
            posted = json.loads(api(git, "api", "--method", "POST",
                                    f"repos/{REPOSITORY}/issues/60/comments", "--input", str(request)))
        readback = json.loads(api(git, "api", f"repos/{REPOSITORY}/issues/comments/{posted['id']}"))
        require(readback["body"] == body and readback["user"]["login"] == "stop-cran",
                "Checkpoint readback/attribution differs")
        freeze_json(output, {"comment": readback, "publishedCommit": PUBLISHED, "receiptCommit": commit,
                             "ciRun": live_ci["databaseId"], "runtimeEntries": 8739,
                             "equalServedEntries": equality["entries"][0], "equalitySha256": sha(equal_raw),
                             "delivered": 268, "remaining": 960, "overallN1TaskComplete": False})
        print(json.dumps({"commentUrl": readback["html_url"], "author": "stop-cran",
                          "delivered": 268, "remaining": 960}))
    finally:
        require(not guard.finish()["breach"], "Checkpoint RAM breach")


if __name__ == "__main__":
    action, commit = sys.argv[1:]
    if action == "equal":
        equal(commit)
    elif action == "checkpoint":
        checkpoint(commit)
    else:
        raise SystemExit("equal|checkpoint RECEIPT_COMMIT")
