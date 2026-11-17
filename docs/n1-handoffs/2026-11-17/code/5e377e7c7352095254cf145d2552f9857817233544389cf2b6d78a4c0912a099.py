"""Run the original ten serial host gates on B126's actual contributor-only tree."""
import json
import sys
from pathlib import Path

from close_b126 import (BASE, CANDIDATE, GIT_HELPER_SHA, REPO, REVIEW, bounded_git,
                       read, verify_archive)
from common import WS, freeze_json, frozen, load_module, require, sha, start_guard

HERE = WS / "scratch-126"
RUNNER_SHA = "16668c4867b038b9b9518610e09c0f14f245ae73619fe92a4d4264db81a72c4f"
ORDER = ["lint", "quiz-safety", "linkplan", "reading-exposure", "validate", "manifest",
         "unittest", "budget", "vocabulary", "manifest-rebuild"]


def main(mode, commit, output):
    require(mode in ("closure", "committed") and output.parent == HERE and not output.exists(),
            "Use closure|committed SHA and a new direct scratch-126 output")
    guard, _ = start_guard("B126 closure gate preflight")
    try:
        git = bounded_git(guard)
        require(git("rev-parse", "HEAD").decode().strip() == commit, "HEAD differs")
        before = git("status", "--porcelain=v1", "--untracked-files=all")
        if mode == "closure":
            require(commit == CANDIDATE and before, "Expected unsigned contributor-only closure")
            paths = [line[3:] for line in before.decode().splitlines()]
            require(all(path.startswith("docs/n1-reviews/batch-126-closure/")
                        or path == "docs/n1-sources/batch-126-progress.json" for path in paths),
                    "Unaccounted worktree edits")
        else:
            require(not before and git("show", "-s", "--format=%P", commit).decode().strip() == CANDIDATE,
                    "Signed closure is not a clean direct child")
            paths = git("diff", "--name-only", CANDIDATE, commit).decode().splitlines()
            require(paths and all(path.startswith("docs/") for path in paths), "Runtime changed")
        manifest = git("show", f"{CANDIDATE}:manifest.json")
        require((REPO / "manifest.json").read_bytes() == manifest, "Reviewed manifest differs")
        archive = verify_archive()
        frozen(REVIEW / "candidate-inputs" / "run_b126_gates.py", RUNNER_SHA)
        require(sha((HERE / "run_b126_gates.py").read_bytes()) == RUNNER_SHA
                and sha((HERE / "b126_common.py").read_bytes()) == GIT_HELPER_SHA,
                "Original gate runner or helper changed")
        for name in ("b126_common.py", "run_b126_gates.py", "check_reading_b126.py"):
            require((HERE / name).read_bytes() ==
                    git("show", f"{CANDIDATE}:docs/n1-sources/batch-126/producers/{name}"),
                    "Gate implementation differs from the signed author source")
        sys.path.insert(0, str(HERE))
        runner = load_module("b126_closure_host_gates", HERE / "run_b126_gates.py")
        require(list(runner.CHECKS) == ORDER, "Actual gate order differs")
        for name in ORDER:
            original = read(REVIEW / "candidate-inputs" / "committed" / f"{name}.json")
            require(original["command"][2:] == list(map(str, runner.CHECKS[name]))
                    and original["cwd"] == str(REPO), "Actual gate command differs")
        output.mkdir()
        expected = None
        for name in ORDER:
            expected = runner.run_gate(name, output, expected)
            guard.check()
        require(expected == sha(manifest)
                and git("status", "--porcelain=v1", "--untracked-files=all") == before
                and git("rev-parse", "HEAD").decode().strip() == commit, "Gates changed the actual tree")
        result = {
            "batch": 126, "status": "PASS", "mode": mode, "head": commit, "base": BASE,
            "reviewedSnapshot": CANDIDATE, "checks": ORDER, "manifestSha256": expected,
            "manifestReproducible": True, "closureProvenanceSha256": archive["provenanceSha256"],
            "wrapperSha256": sha(frozen(Path(__file__))), "runnerSha256": RUNNER_SHA,
            "logs": {name: {"receiptSha256": sha((output / f"{name}.json").read_bytes()),
                            "logSha256": sha((output / f"{name}.log").read_bytes())} for name in ORDER},
            "limits": "Actual-tree host gates, not native/device, arbitrary-pool or publication acceptance."}
        freeze_json(output / "summary.json", result)
        for path in output.iterdir():
            path.chmod(0o444)
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Closure gates RAM breach")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve())
