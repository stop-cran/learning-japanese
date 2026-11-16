"""Run the unchanged signed B132 host gates on the actual B132 review closure.

Derived from run_b131_closure_checks.py. Differences: the reviewed snapshot is an explicit argument
(the signed candidate itself, or its linear owner-signed reconciliation descendant), B132's own signed
helpers are used, and every Git child is waited on in <=0.1-second slices.

Usage: run_b132_closure_checks.py closure|committed REVIEWED COMMIT OUT
  closure    HEAD is REVIEWED with only the uncommitted closure archive and progress ledger present.
  committed  HEAD is the clean signed closure commit whose sole parent is REVIEWED.
OUT must be a new direct child of scratch-132.
"""
import json
import re
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard
from verify_b132_packet import RUNNER
from verify_b132_sources import FINGERPRINT, OWNER, TRAILER, Git

BATCH = 132
REPO = WS / "b132-worktree"
HERE = WS / "scratch-132"
BASE = "2375ab9add0cc5d569c8ea35d229b82813fd8557"
CANDIDATE = "2e618b38ae5b420f7a1fe6783268093348367c51"
MEMBERS = ["\u5893"]
CLOSURE = f"docs/n1-reviews/batch-{BATCH}-closure/"
PROGRESS = f"docs/n1-sources/batch-{BATCH}-progress.json"
HELPERS = ("common_132.py", "run_132_gates.py", "check_reading_132.py")
ORDER = ["lint", "quiz-safety", "linkplan", "reading-exposure", "validate", "manifest",
         "unittest", "budget", "vocabulary", "manifest-rebuild"]
FULL_SHA = re.compile(r"[0-9a-f]{40}")


def validate_lineage(rows, messages, candidate, reviewed):
    """rows: oldest-first `%H|%P|%G?|%GF|%ae|%ce` for candidate..reviewed; messages: full bodies."""
    require(FULL_SHA.fullmatch(candidate) and FULL_SHA.fullmatch(reviewed), "Use full commit IDs")
    parent = candidate
    for row, body in zip(rows, messages, strict=True):
        commit, parents, status, fingerprint, author, committer = row.split("|")
        require(parents == parent, f"Reviewed lineage is not linear from the candidate at {commit}")
        require(status == "G" and fingerprint == FINGERPRINT and author == committer == OWNER,
                f"Reconciliation commit is not owner-signed: {commit}")
        require(TRAILER in body, f"Reconciliation commit lacks the Copilot trailer: {commit}")
        parent = commit
    require(parent == reviewed, "Reviewed snapshot is not the end of the candidate lineage")
    return len(rows)


def lineage(git, reviewed):
    rows = [line for line in git("log", "--reverse", "--format=%H|%P|%G?|%GF|%ae|%ce",
                                 f"{CANDIDATE}..{reviewed}").decode().splitlines() if line]
    bodies = [git("show", "-s", "--format=%B", row.split("|")[0]) for row in rows]
    git("merge-base", "--is-ancestor", CANDIDATE, reviewed)
    return validate_lineage(rows, bodies, CANDIDATE, reviewed)


def main(mode, reviewed, commit, output):
    require(mode in ("closure", "committed") and output.parent == HERE and not output.exists(),
            "Use closure|committed REVIEWED COMMIT and a new direct scratch-132 output")
    closure = REPO / Path(CLOSURE)
    guard, _ = start_guard("B132 closure host gates")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == commit, "HEAD differs")
        reconciliation_commits = lineage(git, reviewed)
        before = git("status", "--porcelain=v1", "--untracked-files=all")
        if mode == "closure":
            require(commit == reviewed and before, "Expected the uncommitted closure on the reviewed snapshot")
            paths = [line[3:] for line in before.decode().splitlines()]
        else:
            require(not before and git("show", "-s", "--format=%P", commit).decode().strip() == reviewed,
                    "Signed closure is not a clean direct child of the reviewed snapshot")
            row = git("show", "-s", "--format=%G?|%GF|%ae|%ce", commit).decode().strip()
            require(row == f"G|{FINGERPRINT}|{OWNER}|{OWNER}", "Closure commit is not owner-signed")
            require(TRAILER in git("show", "-s", "--format=%B", commit), "Closure commit lacks trailer")
            paths = git("diff", "--name-only", reviewed, commit).decode().splitlines()
        require(paths and all(name.startswith(CLOSURE) or name == PROGRESS for name in paths),
                "Changes outside the closure archive and progress ledger")
        provenance_raw = frozen(closure / "provenance.json")
        provenance = json.loads(provenance_raw)
        require(provenance["batch"] == BATCH and provenance["reviewedSnapshot"] == reviewed
                and provenance["base"] == BASE and provenance["initialSnapshot"] == CANDIDATE
                and provenance["publication"] == "PENDING", "Closure provenance differs")
        for count, (name, digest) in enumerate(provenance["recordedFileSha256"].items()):
            frozen(closure / Path(name), digest)
            if count % 50 == 0:
                guard.check()
        on_disk = sorted(p.relative_to(closure).as_posix() for p in closure.rglob("*") if p.is_file())
        require(on_disk == sorted([*provenance["recordedFileSha256"], "provenance.json"]),
                "Closure tree differs from provenance inventory")
        progress = json.loads(frozen(REPO / Path(PROGRESS)))
        require(progress["status"] == "textual-review-closed-publication-pending"
                and progress["batch"] == BATCH and progress["members"] == MEMBERS
                and progress["reviewedSnapshot"] == reviewed and progress["initialSnapshot"] == CANDIDATE
                and progress["review"]["closureProvenanceSha256"] == sha(provenance_raw)
                and progress["review"]["finalRuns"] == provenance["finalRuns"],
                "Progress ledger does not bind the closure")
        manifest = git("show", f"{reviewed}:manifest.json")
        require((REPO / "manifest.json").read_bytes() == manifest
                and sha(manifest) == progress["manifestSha256"], "Reviewed manifest differs")
        bindings = {}
        for name in HELPERS:
            expected = git("show", f"{reviewed}:docs/n1-sources/batch-{BATCH}/producers/{name}")
            require((HERE / name).read_bytes() == expected, "Signed gate helper differs: " + name)
            bindings[name] = sha(expected)
        sys.path.insert(0, str(HERE))
        runner = load_module("b132_closure_gates", HERE / "run_132_gates.py")
        require(list(runner.CHECKS) == ORDER, "Signed gate order differs")
        output.mkdir()
        expected = None
        for name in ORDER:
            expected = runner.run_gate(name, output, expected)
            guard.check()
        require(expected == sha(manifest)
                and git("status", "--porcelain=v1", "--untracked-files=all") == before
                and git("rev-parse", "HEAD").decode().strip() == commit, "Gates changed tree")
        result = {
            "batch": BATCH, "status": "PASS", "mode": mode, "head": commit, "base": BASE,
            "initialSnapshot": CANDIDATE, "reviewedSnapshot": reviewed,
            "reconciliationCommits": reconciliation_commits, "checks": ORDER, "manifestSha256": expected,
            "manifestReproducible": True, "closureProvenanceSha256": sha(provenance_raw),
            "closureFiles": len(provenance["recordedFileSha256"]) + 1,
            "wrapperSha256": sha(frozen(Path(__file__))), "sources": bindings,
            "logs": {name: {"receiptSha256": sha((output / f"{name}.json").read_bytes()),
                           "logSha256": sha((output / f"{name}.log").read_bytes())} for name in ORDER},
            "limits": "Actual-tree host gates, not native/device, arbitrary-pool or publication acceptance.",
        }
        freeze_json(output / "summary.json", result)
        for path in output.iterdir():
            path.chmod(0o444)
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Closure gates RAM breach")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("usage: run_b132_closure_checks.py closure|committed REVIEWED COMMIT OUT")
    main(sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4]).resolve())
