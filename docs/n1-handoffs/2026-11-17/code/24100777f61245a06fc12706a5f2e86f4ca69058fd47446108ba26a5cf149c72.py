"""Bounded GitHub publication and exact ZIP checks for the accepted B133 closure."""
import json
import re
import subprocess
import sys
from pathlib import Path

from common import GUARD, GUARD_SHA, freeze_json, frozen, load_module, require, sha, start_guard
from record_b133_publication_v2 import validate_progress
from run_b133_closure_checks import BASE, CLOSURE, HERE, ORDER, PROGRESS, REPO, lineage
from verify_b133_packet import RUNNER
from verify_b133_sources import FINGERPRINT, OWNER, TRAILER, Git
from b133_closure_origins import REVISION


def api(git, *args):
    child = subprocess.Popen(["gh", *args], cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw, error = git.wait(child)
    require(child.returncode == 0, "GitHub command failed: " + error.decode("utf-8", "replace"))
    return raw


def push(mode, commit):
    require(mode in ("closure", "receipt") and re.fullmatch(r"[0-9a-f]{40}", commit), "Wrong publication mode/commit")
    output = HERE / ("push-" + mode + "-001.json")
    require(not output.exists(), "Preserve the previous publication result")
    guard, _ = start_guard("B133 signed fast-forward publication")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == commit
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Wrong or dirty publication")
        require(git("show", "-s", "--format=%G?|%GF|%ae|%ce", commit).decode().strip()
                == f"G|{FINGERPRINT}|{OWNER}|{OWNER}" and TRAILER in git("show", "-s", "--format=%B", commit),
                "Publication signature differs")
        require(json.loads(api(git, "api", "user"))["login"] == "stop-cran", "Wrong GitHub account")
        lineage(git, REVISION)
        closure_raw = frozen(REPO / CLOSURE / "provenance.json")
        if mode == "closure":
            require(git("show", "-s", "--format=%P", commit).decode().strip() == REVISION, "Wrong closure parent")
            validate_progress(json.loads(frozen(REPO / PROGRESS)), REVISION,
                              git("show", REVISION + ":manifest.json"), closure_raw)
            for kind in ("closure", "committed"):
                summary = json.loads(frozen(HERE / ("closure-gates-001" if kind == "closure" else "closure-gates-committed-001") / "summary.json"))
                require(summary["status"] == "PASS" and summary["checks"] == ORDER
                        and summary["head"] == (REVISION if kind == "closure" else commit)
                        and summary["closureProvenanceSha256"] == sha(closure_raw), "Closure gates differ")
            expected_remote = BASE
        else:
            proof = json.loads(frozen(REPO / "docs/n1-reviews/batch-133-publication/provenance.json"))
            expected_remote = proof["publishedCommit"]
            require(git("show", "-s", "--format=%P", commit).decode().strip() == expected_remote,
                    "Receipt parent differs")
            changes = git("diff", "--name-only", expected_remote, commit).decode().splitlines()
            require(changes and all(path == PROGRESS or path.startswith("docs/n1-reviews/batch-133-publication/")
                                    for path in changes), "Receipt changed unrelated paths")
            require(git("show", commit + ":manifest.json") == git("show", expected_remote + ":manifest.json"),
                    "Receipt changed runtime manifest")
        git("fetch", "--quiet", "origin", "main")
        require(git("rev-parse", "origin/main").decode().strip() == expected_remote
                and git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == expected_remote,
                "Remote main advanced; do not overwrite or force-push")
        result = git("push", "origin", "HEAD:refs/heads/main", include_stderr=True).decode("utf-8")
        require(git("ls-remote", "origin", "refs/heads/main").decode().split()[0] == commit, "Remote push unverified")
        remote = json.loads(api(git, "api", "repos/stop-cran/learning-japanese/commits/" + commit))
        require(remote["sha"] == commit and remote["commit"]["verification"]["verified"]
                and remote["author"]["login"] == remote["committer"]["login"] == "stop-cran",
                "Remote owner signature not verified")
        print(json.dumps(freeze_json(output, {"commit": commit, "previousRemote": expected_remote,
                                              "url": remote["html_url"], "pushOutput": result,
                                              "verifiedOwnerSignature": True})))
    finally:
        require(not guard.finish()["breach"], "Publication RAM breach")


def zip_check(commit, output):
    require(re.fullmatch(r"[0-9a-f]{40}", commit) and output.parent == HERE and not output.exists(),
            "Use the exact commit and a new direct B133 scratch directory")
    frozen(GUARD, GUARD_SHA)
    guard, _ = start_guard("B133 exact served ZIP")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == commit
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Wrong/dirty ZIP snapshot")
        verifier = load_module("b133_pinned_zip", GUARD)

        def bounded_git(root, *args):
            require(Path(root) == REPO, "ZIP Git escaped the batch worktree")
            return git(*args)

        verifier.git = bounded_git
        output.mkdir()
        receipt = verifier.verify(REPO, commit, output, guard)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "ZIP RAM breach")
    receipt.update(memory=memory, verifierSha256=GUARD_SHA,
                   wrapperSha256=sha(frozen(Path(__file__))),
                   executionQualification="Original pinned ZIP comparisons with bounded Git child waits.")
    print(json.dumps(freeze_json(output / "receipt.json", receipt)))


def ci(commit, output):
    require(re.fullmatch(r"[0-9a-f]{40}", commit) and output.parent == HERE and not output.exists(),
            "Use exact CI commit and a new B133 snapshot")
    guard, _ = start_guard("B133 CI observation")
    try:
        git = Git(REPO, RUNNER, guard)
        runs = json.loads(api(git, "run", "list", "--repo", "stop-cran/learning-japanese", "--commit", commit,
                              "--workflow", "validate.yml", "--limit", "5", "--json",
                              "databaseId,headSha,status,conclusion,url,workflowName"))
        require(runs and all(row["headSha"] == commit for row in runs), "No matching CI run yet")
        row = runs[0]
        full = json.loads(api(git, "run", "view", str(row["databaseId"]), "--repo", "stop-cran/learning-japanese",
                              "--json", "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt"))
        print(json.dumps(freeze_json(output, full)))
        print(json.dumps(full))
    finally:
        require(not guard.finish()["breach"], "CI observation RAM breach")


if __name__ == "__main__":
    action, *args = sys.argv[1:]
    if action == "push":
        push(*args)
    elif action == "zip":
        zip_check(args[0], Path(args[1]).resolve())
    elif action == "ci":
        ci(args[0], Path(args[1]).resolve())
    else:
        raise SystemExit("push closure|receipt COMMIT | zip COMMIT OUTPUT | ci COMMIT OUTPUT")
