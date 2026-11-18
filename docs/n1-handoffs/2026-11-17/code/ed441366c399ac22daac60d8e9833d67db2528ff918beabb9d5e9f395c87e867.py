"""Make one owner-signed closure or receipt commit, never retrying stalled signing."""
import json
import subprocess
import sys
import time
from pathlib import Path

from common import freeze_json, frozen, require, sha, start_guard
from record_b132_publication import validate_progress
from run_b132_closure_checks import CLOSURE, HERE, ORDER, PROGRESS, REPO, lineage
from verify_b132_packet import RUNNER
from verify_b132_sources import FINGERPRINT, OWNER, TRAILER, Git
from verify_b132_teaching_revision import REVISION


def main(mode, parent):
    require(mode in ("closure", "receipt"), "Use closure or receipt")
    output = HERE / ("sign-" + mode + "-001")
    require(not output.exists(), "A signing attempt already exists; do not retry")
    guard, _ = start_guard("B132 " + mode + " signature")
    child = None
    result = {"mode": mode, "parent": parent, "attempted": False, "timedOut": False}
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == parent, "Signing parent differs")
        require(git("remote", "get-url", "origin").decode().strip()
                == "https://github.com/stop-cran/learning-japanese.git", "Wrong origin")
        require(git("config", "user.email").decode().strip() == OWNER
                and git("config", "user.signingkey").decode().strip() == FINGERPRINT,
                "Signing identity differs")
        require(git("config", "user.name").decode().strip()
                == git("show", "-s", "--format=%an", parent).decode().strip(), "Owner name changed")
        require(not git("diff", "--cached", "--name-only"), "Existing staged work must be preserved")
        publication = "docs/n1-reviews/batch-132-publication/"
        prefix = CLOSURE if mode == "closure" else publication
        paths = [line[3:] for line in git("status", "--porcelain=v1", "--untracked-files=all").decode().splitlines()]
        require(paths and all(name == PROGRESS or name.startswith(prefix) for name in paths),
                "Unexpected paths before staging")
        closure_raw = frozen(REPO / CLOSURE / "provenance.json")
        manifest = git("show", REVISION + ":manifest.json")
        if mode == "closure":
            require(parent == REVISION, "Wrong closure parent")
            validate_progress(json.loads(frozen(REPO / PROGRESS)), REVISION, manifest, closure_raw)
            summary = json.loads(frozen(HERE / "closure-gates-closure-001" / "summary.json"))
            require(summary["status"] == "PASS" and summary["head"] == REVISION
                    and summary["checks"] == ORDER and summary["manifestSha256"] == sha(manifest)
                    and summary["closureProvenanceSha256"] == sha(closure_raw), "Closure gates differ")
            title = "Close independent review of N1 grave card"
        else:
            lineage(git, REVISION)
            proof = json.loads(frozen(REPO / publication / "provenance.json"))
            require(proof["publishedCommit"] == parent
                    and proof["status"] == "published-verified-with-disclosed-review-limits",
                    "Unverified publication receipt")
            title = "Record verified N1 grave card delivery"
        require((REPO / "manifest.json").read_bytes() == manifest, "Runtime manifest changed")
        git("add", "--sparse", "--", PROGRESS, prefix)
        staged = git("diff", "--cached", "--name-only").decode().splitlines()
        require(staged and set(staged) == set(paths), "Staging differs from exact inspected paths")
        git("diff", "--cached", "--check")
        output.mkdir()
        freeze_json(output / "staged.json", {"parent": parent, "paths": staged,
                                           "manifestSha256": sha(manifest), "closureSha256": sha(closure_raw)})
        command = ["git", "--no-pager", "commit", "-S", "-m", title, "-m", TRAILER.decode()]
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
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", commit).decode().strip()
                == f"{parent}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", commit)
                and not git("status", "--porcelain=v1", "--untracked-files=all"), "Signed commit differs")
        result.update(commit=commit, clean=True, verifiedOwnerSignature=True)
        print(json.dumps(result))
    finally:
        if child is not None:
            git.cleanup.stop_child(child)
        result["memory"] = guard.finish()
        if output.exists():
            log = output / "commit.log"
            if log.exists():
                log.chmod(0o444)
                result["logSha256"] = sha(frozen(log))
            freeze_json(output / "receipt.json", result)


if __name__ == "__main__":
    main(*sys.argv[1:])
