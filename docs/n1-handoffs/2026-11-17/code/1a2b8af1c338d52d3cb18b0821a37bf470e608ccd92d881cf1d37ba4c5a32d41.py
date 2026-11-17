"""Owner-signed B134 closure/receipt commits, fast-forward publication, exact ZIP/CI and served-tree checks.

Derived from sign_b133_delivery.py, publish_b133.py and finish_b133_delivery.py. Differences: the
reviewed snapshot (the signed candidate or its owner-signed reconciliation descendant), gate summaries and
evidence folders are explicit arguments; served-runtime counts come from the exact manifest; accounting
comes from the B134 ledger; outputs use new delivery-* names and no step is retried automatically.

Usage:
  sign closure REVIEWED CLOSURE_GATES
  sign receipt REVIEWED PUBLISHED
  push closure REVIEWED COMMIT CLOSURE_GATES COMMITTED_GATES
  push receipt REVIEWED COMMIT
  zip COMMIT OUT | ci COMMIT OUT
  equal PUBLISHED RECEIPT PUBLISHED_ZIP_DIR RECEIPT_ZIP_DIR RECEIPT_CI
  checkpoint PUBLISHED RECEIPT RECEIPT_CI
Gate summaries are frozen summary.json files from run_b134_closure_checks.py; OUT and evidence must be
direct children of scratch-134.
"""
import hashlib
import json
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path

from b134_closure_progress import validate_progress
from common import GUARD, GUARD_SHA, freeze_json, frozen, load_module, require, sha, start_guard
from record_b117_publication_v3 import validate_delivery
from record_b134_publication import validate_gate
from run_b134_closure_checks import BASE, BATCH, CLOSURE, HERE, MEMBERS, ORDER, PROGRESS, REPO, lineage
from verify_b134_packet import RUNNER
from verify_b134_sources import FINGERPRINT, OWNER, TRAILER, Git

REPOSITORY = "stop-cran/learning-japanese"
ORIGIN = f"https://github.com/{REPOSITORY}.git"
PUBLICATION = f"docs/n1-reviews/batch-{BATCH}-publication/"
TITLES = {"closure": "Close independent review of N1 purple card",
          "receipt": "Record verified N1 purple card delivery"}
FULL_SHA = re.compile(r"[0-9a-f]{40}")
WHITESPACE = "core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol"
PUBLISHED_ACCOUNTING = {"publishedPendingRecordsWithCards": 272, "publishedN1Additions": 266,
                        "undelivered": 956, "overallN1TaskComplete": False}


def full(*commits):
    require(all(FULL_SHA.fullmatch(commit) for commit in commits), "Use full commit IDs")


def scratch(path, exists):
    path = Path(path).resolve()
    require(path.parent == HERE and path.exists() == exists,
            "Use a direct scratch-134 path that " + ("exists" if exists else "does not exist yet"))
    return path


def allowed(paths, prefix):
    require(paths and all(name == PROGRESS or name.startswith(prefix) for name in paths),
            "Changes outside the progress ledger and " + prefix)
    return paths


def gate(path, mode, reviewed, commit, manifest, closure_raw):
    path = Path(path).resolve()
    require(path.name == "summary.json" and path.parent.parent == HERE, "Use an actual B134 gate summary")
    raw = frozen(path)
    summary = json.loads(raw)
    files = len(json.loads(closure_raw)["recordedFileSha256"]) + 1
    validate_gate(summary, mode, reviewed, commit, sha(manifest), sha(closure_raw), files)
    for name in ORDER:
        frozen(path.parent / f"{name}.json", summary["logs"][name]["receiptSha256"])
        frozen(path.parent / f"{name}.log", summary["logs"][name]["logSha256"])
    return raw


def published_proof(proof, commit):
    require(proof["publishedCommit"] == commit and proof["batch"] == BATCH
            and proof["status"] == "published-verified-with-disclosed-review-limits",
            "Unverified publication receipt")
    return proof


def published_ledger(ledger, commit):
    require(ledger["batch"] == BATCH and ledger["published"] == MEMBERS and ledger["runtimePublished"] is True
            and ledger["status"] == "published-verified-with-disclosed-review-limits"
            and ledger["publication"]["commit"] == commit
            and all(type(ledger["accounting"][key]) is type(value) and ledger["accounting"][key] == value
                    for key, value in PUBLISHED_ACCOUNTING.items()),
            "Published B134 accounting differs")
    return ledger


def identity(git, commit, parent):
    require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", commit).decode().strip()
            == f"{parent}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
            and TRAILER in git("show", "-s", "--format=%B", commit), "Owner-signed identity or parent differs")


def api(git, *args):
    child = subprocess.Popen(["gh", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw, error = git.wait(child)
    require(child.returncode == 0, "GitHub command failed: " + error.decode("utf-8", "replace"))
    return raw


def sign(mode, reviewed, other):
    require(mode in TITLES, "Use closure or receipt")
    full(reviewed)
    output = HERE / f"delivery-sign-{mode}-001"
    require(not output.exists(), "A signing attempt already exists; do not retry")
    guard, _ = start_guard(f"B134 {mode} signature")
    child = git = None
    result = {"mode": mode, "reviewed": reviewed, "attempted": False, "timedOut": False}
    try:
        git = Git(REPO, RUNNER, guard)
        parent = reviewed if mode == "closure" else other
        full(parent)
        result["parent"] = parent
        require(git("rev-parse", "HEAD").decode().strip() == parent, "Signing parent differs")
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("config", "user.email").decode().strip() == OWNER
                and git("config", "user.signingkey").decode().strip() == FINGERPRINT, "Signing identity differs")
        require(git("config", "user.name").decode().strip()
                == git("show", "-s", "--format=%an", reviewed).decode().strip(), "Owner name changed")
        require(not git("diff", "--cached", "--name-only"), "Existing staged work must be preserved")
        lineage(git, reviewed)
        prefix = CLOSURE if mode == "closure" else PUBLICATION
        paths = allowed([line[3:] for line in
                         git("status", "--porcelain=v1", "--untracked-files=all").decode().splitlines()], prefix)
        manifest = git("show", reviewed + ":manifest.json")
        closure_raw = frozen(REPO / CLOSURE / "provenance.json")
        bound = {"manifestSha256": sha(manifest), "closureSha256": sha(closure_raw)}
        if mode == "closure":
            validate_progress(json.loads(frozen(REPO / PROGRESS)), reviewed, manifest, closure_raw)
            bound["closureGatesSha256"] = sha(gate(other, "closure", reviewed, reviewed, manifest, closure_raw))
        else:
            identity(git, parent, reviewed)
            allowed(git("diff", "--name-only", reviewed, parent).decode().splitlines(), CLOSURE)
            proof_raw = frozen(REPO / PUBLICATION / "provenance.json")
            require(published_proof(json.loads(proof_raw), parent)["reviewedSnapshot"] == reviewed,
                    "Publication receipt names another reviewed snapshot")
            published_ledger(json.loads(frozen(REPO / PROGRESS)), parent)
            bound["publicationSha256"] = sha(proof_raw)
        require((REPO / "manifest.json").read_bytes() == manifest, "Runtime manifest changed")
        git("add", "--sparse", "--", PROGRESS, prefix)
        staged = git("diff", "--cached", "--name-only").decode().splitlines()
        require(staged and set(staged) == set(paths), "Staging differs from exact inspected paths")
        for path in staged:
            require(git("show", ":" + path) == (REPO / path).read_bytes(), "Staging changed bytes: " + path)
        git("-c", WHITESPACE, "diff", "--cached", "--check")
        output.mkdir()
        freeze_json(output / "staged.json", {"parent": parent, "paths": staged, **bound})
        command = ["git", "--no-pager", "commit", "-S", "-m", TITLES[mode], "-m", TRAILER.decode()]
        with (output / "commit.log").open("xb") as stream:
            child = subprocess.Popen(command, cwd=REPO, stdout=stream, stderr=subprocess.STDOUT)
            result["attempted"] = True
            deadline = time.monotonic() + 75
            while child.poll() is None:
                try:
                    child.wait(timeout=0.1)
                except subprocess.TimeoutExpired:
                    guard.check()
                    if time.monotonic() >= deadline:
                        result["timedOut"] = True
                        break
        git.cleanup.stop_child(child)
        result["exitCode"] = child.returncode
        require(not result["timedOut"], "Signing stalled; preserve staged work and ask the user to sign again.")
        require(child.returncode == 0, "Signing failed; no automatic retry.")
        commit = git("rev-parse", "HEAD").decode().strip()
        identity(git, commit, parent)
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Signed tree is not clean")
        result.update(commit=commit, clean=True, verifiedOwnerSignature=True)
        print(json.dumps(result))
    finally:
        if child is not None and git is not None:
            git.cleanup.stop_child(child)
        result["memory"] = guard.finish()
        if output.exists():
            log = output / "commit.log"
            if log.exists():
                log.chmod(0o444)
                result["logSha256"] = sha(frozen(log))
            freeze_json(output / "receipt.json", result)


def push(mode, reviewed, commit, closure_gates=None, committed_gates=None):
    require(mode in TITLES, "Use closure or receipt")
    full(reviewed, commit)
    output = HERE / f"delivery-push-{mode}-001.json"
    require(not output.exists(), "Preserve the previous publication result")
    guard, _ = start_guard("B134 signed fast-forward publication")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == commit
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Wrong or dirty publication")
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(json.loads(api(git, "api", "user"))["login"] == "stop-cran", "Wrong GitHub account")
        lineage(git, reviewed)
        manifest = git("show", reviewed + ":manifest.json")
        require(git("show", commit + ":manifest.json") == manifest, "Runtime differs from the reviewed snapshot")
        if mode == "closure":
            identity(git, commit, reviewed)
            allowed(git("diff", "--name-only", reviewed, commit).decode().splitlines(), CLOSURE)
            closure_raw = frozen(REPO / CLOSURE / "provenance.json")
            validate_progress(json.loads(frozen(REPO / PROGRESS)), reviewed, manifest, closure_raw)
            gates = {"closure": sha(gate(closure_gates, "closure", reviewed, reviewed, manifest, closure_raw)),
                     "committed": sha(gate(committed_gates, "committed", reviewed, commit, manifest, closure_raw))}
            expected = BASE
        else:
            proof = published_proof(json.loads(frozen(REPO / PUBLICATION / "provenance.json")),
                                    git("show", "-s", "--format=%P", commit).decode().strip())
            expected = proof["publishedCommit"]
            require(proof["reviewedSnapshot"] == reviewed, "Publication receipt names another reviewed snapshot")
            identity(git, expected, reviewed)
            identity(git, commit, expected)
            allowed(git("diff", "--name-only", expected, commit).decode().splitlines(), PUBLICATION)
            published_ledger(json.loads(frozen(REPO / PROGRESS)), expected)
            gates = {}
        git("fetch", "--quiet", "origin", "main")
        require(git("rev-parse", "origin/main").decode().strip() == expected
                and git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == expected,
                "Remote main advanced; do not overwrite or force-push")
        git("merge-base", "--is-ancestor", expected, commit)
        pushed = git("push", "origin", "HEAD:refs/heads/main", include_stderr=True).decode("utf-8")
        require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit, "Remote push unverified")
        remote = json.loads(api(git, "api", f"repos/{REPOSITORY}/commits/{commit}"))
        require(remote["sha"] == commit and remote["commit"]["verification"]["verified"]
                and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
                "Remote owner signature not verified")
        print(json.dumps(freeze_json(output, {
            "mode": mode, "commit": commit, "reviewed": reviewed, "previousRemote": expected,
            "url": remote["html_url"], "pushOutput": pushed, "gateSummarySha256": gates,
            "manifestSha256": sha(manifest), "verifiedOwnerSignature": True})))
    finally:
        require(not guard.finish()["breach"], "Publication RAM breach")


def zip_check(commit, output):
    full(commit)
    output = scratch(output, False)
    frozen(GUARD, GUARD_SHA)
    guard, _ = start_guard("B134 exact served ZIP")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == commit
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Wrong/dirty ZIP snapshot")
        verifier = load_module("b134_pinned_zip", GUARD)

        def bounded_git(root, *args):
            require(Path(root) == REPO, "ZIP Git escaped the batch worktree")
            return git(*args)

        verifier.git = bounded_git
        output.mkdir()
        receipt = verifier.verify(REPO, commit, output, guard)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "ZIP RAM breach")
    receipt.update(memory=memory, verifierSha256=GUARD_SHA, wrapperSha256=sha(frozen(Path(__file__))),
                   executionQualification="Original pinned ZIP comparisons with bounded Git child waits.")
    print(json.dumps(freeze_json(output / "receipt.json", receipt)))


def ci(commit, output):
    full(commit)
    output = scratch(output, False)
    guard, _ = start_guard("B134 CI observation")
    try:
        git = Git(REPO, RUNNER, guard)
        runs = json.loads(api(git, "run", "list", "--repo", REPOSITORY, "--commit", commit,
                              "--workflow", "validate.yml", "--limit", "5", "--json",
                              "databaseId,headSha,status,conclusion,url,workflowName"))
        require(runs and all(row["headSha"] == commit for row in runs), "No matching CI run yet")
        observed = json.loads(api(git, "run", "view", str(runs[0]["databaseId"]), "--repo", REPOSITORY, "--json",
                                  "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt"))
        require(observed["headSha"] == commit, "CI run head differs")
        print(json.dumps(freeze_json(output, observed)))
    finally:
        require(not guard.finish()["breach"], "CI observation RAM breach")


def stream_sha(stream, guard):
    digest = hashlib.sha256()
    while chunk := stream.read(64 * 1024):
        guard.check()
        digest.update(chunk)
    return digest.hexdigest()


def entries(folder, commit, manifest, observed_ci, guard):
    receipt = json.loads(frozen(folder / "receipt.json"))
    validate_delivery(commit, manifest, observed_ci, receipt)
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


def compare(before, after):
    shared = before.keys() & after.keys()
    return {"entries": [len(before), len(after)], "namesEqual": before.keys() == after.keys(),
            "contentEqual": before == after, "onlyInPublished": sorted(before.keys() - after.keys()),
            "onlyInReceipt": sorted(after.keys() - before.keys()),
            "differing": sorted(name for name in shared if before[name] != after[name])}


def receipt_tree(git, published, commit):
    full(published, commit)
    require(git("rev-parse", "HEAD").decode().strip() == commit
            and not git("status", "--porcelain=v1", "--untracked-files=all"), "Receipt is not the clean HEAD")
    identity(git, commit, published)
    allowed(git("diff", "--name-only", published, commit).decode().splitlines(), PUBLICATION)
    manifest = git("show", published + ":manifest.json")
    require(git("show", commit + ":manifest.json") == manifest, "Receipt changed runtime manifest")
    proof = published_proof(json.loads(git("show", f"{commit}:{PUBLICATION}provenance.json")), published)
    lineage(git, proof["reviewedSnapshot"])
    identity(git, published, proof["reviewedSnapshot"])
    allowed(git("diff", "--name-only", proof["reviewedSnapshot"], published).decode().splitlines(), CLOSURE)
    published_ledger(json.loads(git("show", f"{commit}:{PROGRESS}")), published)
    return manifest


def equality_path():
    return HERE / "delivery-tree-equality-001" / "receipt.json"


def equal(published, commit, published_zip, receipt_zip, receipt_ci):
    output = equality_path()
    require(not output.parent.exists(), "Preserve existing equality receipt")
    published_zip, receipt_zip = scratch(published_zip, True), scratch(receipt_zip, True)
    receipt_ci = scratch(receipt_ci, True)
    guard, _ = start_guard("B134 full served-tree equality")
    try:
        git = Git(REPO, RUNNER, guard)
        manifest = receipt_tree(git, published, commit)
        committed_ci = json.loads(git("show", f"{commit}:{PUBLICATION}ci-run.json"))
        require(frozen(published_zip / "receipt.json") == git("show", f"{commit}:{PUBLICATION}zip-receipt.json"),
                "Published ZIP evidence differs from the committed receipt")
        before, first = entries(published_zip, published, manifest, committed_ci, guard)
        after, second = entries(receipt_zip, commit, manifest, json.loads(frozen(receipt_ci)), guard)
        result = {"publishedCommit": published, "receiptCommit": commit,
                  "publishedZipSha256": first["sha256"], "receiptZipSha256": second["sha256"],
                  "receiptCiSha256": sha(frozen(receipt_ci)), **compare(before, after),
                  "method": "Prefix-stripped names, directory flags and streamed SHA-256 of every served entry; "
                            "both archive hashes independently checked.",
                  "verifierSha256": sha(frozen(Path(__file__)))}
    finally:
        memory = guard.finish()
    require(not memory["breach"] and result["namesEqual"] and result["contentEqual"],
            "Publication and receipt served trees are not verified equal")
    result["memory"] = memory
    output.parent.mkdir()
    print(json.dumps(freeze_json(output, result)))


def checkpoint_body(body, receipt_url, ci_url, served):
    return body + (f"\n\nThe owner-signed [publication receipt]({receipt_url}) also passed "
                   f"[its CI]({ci_url}); all **{served:,} served entries** are byte-identical after "
                   "stripping the archive-root prefix. The runtime manifest is unchanged.")


def checkpoint(published, commit, receipt_ci):
    output = HERE / "delivery-issue60-checkpoint-001.json"
    require(not output.exists(), "Checkpoint already recorded")
    receipt_ci = scratch(receipt_ci, True)
    guard, _ = start_guard("B134 owner issue checkpoint")
    try:
        git = Git(REPO, RUNNER, guard)
        manifest = receipt_tree(git, published, commit)
        runtime = sum(len(value) for value in json.loads(manifest).values() if isinstance(value, dict))
        require(json.loads(api(git, "api", "user"))["login"] == "stop-cran", "Wrong checkpoint author")
        require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit,
                "Receipt is not current remote main")
        remote = json.loads(api(git, "api", f"repos/{REPOSITORY}/commits/{commit}"))
        require(remote["sha"] == commit and remote["commit"]["verification"]["verified"]
                and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
                "Remote receipt identity differs")
        recorded_ci_raw = frozen(receipt_ci)
        recorded_ci = json.loads(recorded_ci_raw)
        live_ci = json.loads(api(git, "run", "view", str(recorded_ci["databaseId"]), "--repo", REPOSITORY,
                                 "--json", "databaseId,headSha,status,conclusion,url,workflowName"))
        require(live_ci["headSha"] == commit and live_ci["status"] == "completed"
                and live_ci["conclusion"] == "success" and live_ci["workflowName"] == "Validate content",
                "Exact receipt CI is not successful")
        equal_raw = frozen(equality_path())
        equality = json.loads(equal_raw)
        require(equality["publishedCommit"] == published and equality["receiptCommit"] == commit
                and equality["namesEqual"] and equality["contentEqual"] and not equality["differing"]
                and not equality["memory"]["breach"] and equality["receiptCiSha256"] == sha(recorded_ci_raw)
                and equality["entries"][0] == equality["entries"][1] > runtime, "Equality proof differs")
        body = checkpoint_body(json.loads(frozen(HERE / "issue60-publication-comment.json"))["body"],
                               remote["html_url"], live_ci["url"], equality["entries"][0])
        matches, page = [], 1
        while True:
            comments = json.loads(api(git, "api", f"repos/{REPOSITORY}/issues/60/comments?per_page=100&page={page}"))
            matches.extend(item for item in comments if re.search(rf"\bB{BATCH}\b", item["body"]))
            if len(comments) < 100:
                break
            page += 1
        request = HERE / "delivery-issue60-checkpoint-request-001.json"
        if request.exists():
            require(json.loads(frozen(request)) == {"body": body}, "Existing checkpoint request differs")
        else:
            freeze_json(request, {"body": body})
        if matches:
            require(len(matches) == 1 and matches[0]["body"] == body
                    and matches[0]["user"]["login"] == "stop-cran", "Existing B134 checkpoint differs")
            posted = matches[0]
        else:
            posted = json.loads(api(git, "api", "--method", "POST",
                                    f"repos/{REPOSITORY}/issues/60/comments", "--input", str(request)))
        readback = json.loads(api(git, "api", f"repos/{REPOSITORY}/issues/comments/{posted['id']}"))
        require(readback["body"] == body and readback["user"]["login"] == "stop-cran",
                "Checkpoint readback/attribution differs")
        freeze_json(output, {"comment": readback, "publishedCommit": published, "receiptCommit": commit,
                             "ciRun": live_ci["databaseId"], "runtimeEntries": runtime,
                             "equalServedEntries": equality["entries"][0], "equalitySha256": sha(equal_raw),
                             "delivered": 272, "remaining": 956, "overallN1TaskComplete": False})
        print(json.dumps({"commentUrl": readback["html_url"], "author": "stop-cran",
                          "delivered": 272, "remaining": 956}))
    finally:
        require(not guard.finish()["breach"], "Checkpoint RAM breach")


def dispatch(argv):
    action, *args = argv or [""]
    commands = {("sign", 3): sign, ("push", 3): push, ("push", 5): push, ("zip", 2): zip_check,
                ("ci", 2): ci, ("equal", 5): equal, ("checkpoint", 3): checkpoint}
    command = commands.get((action, len(args)))
    if command is None or (action == "push" and (args[0] == "closure") != (len(args) == 5)):
        raise SystemExit(__doc__)
    return command, args


if __name__ == "__main__":
    command, arguments = dispatch(sys.argv[1:])
    command(*arguments)
