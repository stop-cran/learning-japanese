"""Run the unchanged signed B131 host gates on the actual B131 review closure.

Usage: run_b131_closure_checks.py closure|committed COMMIT OUT
  closure    HEAD is the signed reviewed snapshot with only the uncommitted closure archive and
             progress ledger present.
  committed  HEAD is the clean signed closure commit whose sole parent is the reviewed snapshot.
"""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_module, require, sha, start_guard

REPO = WS / "b131-worktree"
CONFIG = {"repo": str(REPO)}
HERE = WS / "scratch-131"
REVIEWED = "88a9dfab6a783b082659b742a24242342bb2e461"
BASE = "cb0f5581bdda84f7e673225c19126c85e242e57b"
CLOSURE = "docs/n1-reviews/batch-131-closure/"
PROGRESS = "docs/n1-sources/batch-131-progress.json"
HELPERS = ("b131_common.py", "run_b131_gates.py", "check_reading_b131.py", "candidate_b131.py")
ORDER = ["lint", "quiz-safety", "linkplan", "reading-exposure", "validate", "manifest",
         "unittest", "budget", "vocabulary", "manifest-rebuild"]


def main(mode, commit, output):
    require(mode in ("closure", "committed") and output.parent == HERE and not output.exists(),
            "Use closure|committed SHA and a new direct scratch-131 output")
    closure = REPO / Path(CLOSURE)
    guard, _ = start_guard("B131 closure host gates")
    try:
        require(git(CONFIG, "rev-parse", "HEAD").decode().strip() == commit, "HEAD differs")
        before = git(CONFIG, "status", "--porcelain=v1", "--untracked-files=all")
        if mode == "closure":
            require(commit == REVIEWED and before, "Expected the uncommitted closure on signed 88a9dfab")
            paths = [line[3:] for line in before.decode().splitlines()]
            require(all(name.startswith(CLOSURE) or name == PROGRESS for name in paths),
                    "Unaccounted worktree changes")
        else:
            require(not before and git(CONFIG, "show", "-s", "--format=%P", commit).decode().strip()
                    == REVIEWED, "Signed closure is not a clean direct child of 88a9dfab")
            require(git(CONFIG, "log", "-1", "--format=%G?", commit).decode().strip() == "G",
                    "Closure commit signature is not good")
            paths = git(CONFIG, "diff", "--name-only", REVIEWED, commit).decode().splitlines()
            require(paths and all(name.startswith(CLOSURE) or name == PROGRESS for name in paths),
                    "Closure commit changes paths outside the closure and progress ledger")
        provenance_raw = frozen(closure / "provenance.json")
        provenance = json.loads(provenance_raw)
        require(provenance["batch"] == 131 and provenance["reviewedSnapshot"] == REVIEWED
                and provenance["base"] == BASE and provenance["publication"] == "PENDING",
                "Closure provenance differs")
        for count, (name, digest) in enumerate(provenance["recordedFileSha256"].items()):
            frozen(closure / Path(name), digest)
            if count % 50 == 0:
                guard.check()
        on_disk = sorted(p.relative_to(closure).as_posix() for p in closure.rglob("*") if p.is_file())
        require(on_disk == sorted([*provenance["recordedFileSha256"], "provenance.json"]),
                "Closure tree differs from provenance inventory")
        progress = json.loads(frozen(REPO / Path(PROGRESS)))
        require(progress["status"] == "textual-review-closed-publication-pending"
                and progress["reviewedSnapshot"] == REVIEWED
                and progress["review"]["closureProvenanceSha256"] == sha(provenance_raw)
                and progress["review"]["finalRuns"] == provenance["finalRuns"],
                "Progress ledger does not bind the closure")
        manifest = git(CONFIG, "show", f"{REVIEWED}:manifest.json")
        require((REPO / "manifest.json").read_bytes() == manifest
                and sha(manifest) == progress["runtimeCandidate"]["manifestSha256"], "Reviewed manifest differs")
        bindings = {}
        for name in HELPERS:
            expected = git(CONFIG, "show", f"{REVIEWED}:docs/n1-sources/batch-131/producers/{name}")
            require((HERE / name).read_bytes() == expected, "Signed gate helper differs: " + name)
            bindings[name] = sha(expected)
        sys.path.insert(0, str(HERE))
        runner = load_module("b131_closure_gates", HERE / "run_b131_gates.py")
        require(list(runner.CHECKS) == ORDER, "Signed gate order differs")
        output.mkdir()
        expected = None
        for name in ORDER:
            expected = runner.run_gate(name, output, expected)
            guard.check()
        require(expected == sha(manifest)
                and git(CONFIG, "status", "--porcelain=v1", "--untracked-files=all") == before
                and git(CONFIG, "rev-parse", "HEAD").decode().strip() == commit, "Gates changed tree")
        result = {
            "batch": 131, "status": "PASS", "mode": mode, "head": commit, "base": BASE,
            "reviewedSnapshot": REVIEWED, "checks": ORDER, "manifestSha256": expected,
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
    if len(sys.argv) != 4:
        raise SystemExit("usage: run_b131_closure_checks.py closure|committed COMMIT OUT")
    main(sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve())
