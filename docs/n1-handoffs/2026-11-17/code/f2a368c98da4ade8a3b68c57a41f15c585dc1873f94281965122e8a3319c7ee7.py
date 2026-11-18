"""Run the unchanged ten host gates on B127's contributor-only closure tree."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, load_module, require, sha, start_guard
from finalize_b127 import check_history, check_proof

HERE = WS / "scratch-127"
ORDER = ["lint", "quiz-safety", "linkplan", "reading-exposure", "validate", "manifest",
         "unittest", "budget", "vocabulary", "manifest-rebuild"]


def main(mode, commit, output):
    require(mode in ("closure", "committed") and output.parent == HERE and not output.exists(),
            "Use closure|committed SHA and a new direct scratch-127 output")
    config = load_batch(127)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-127-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    candidate = provenance["reviewedSnapshot"]
    proof = json.loads(frozen(closure / "verification" / "reconciliation-001.json"))
    check_history(provenance, candidate, config)
    check_proof(proof, candidate, config)
    guard, _ = start_guard("B127 closure host gates")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == commit, "HEAD differs")
        before = git(config, "status", "--porcelain=v1", "--untracked-files=all")
        if mode == "closure":
            require(commit == candidate and before, "Expected unsigned contributor-only closure")
            paths = [line[3:] for line in before.decode().splitlines()]
            require(all(path.startswith("docs/n1-reviews/batch-127-closure/")
                        or path == "docs/n1-sources/batch-127-progress.json" for path in paths),
                    "Unaccounted worktree edits")
        else:
            require(not before and git(config, "show", "-s", "--format=%P", commit).decode().strip() == candidate,
                    "Signed closure is not a clean direct child")
            paths = git(config, "diff", "--name-only", candidate, commit).decode().splitlines()
            require(paths and all(path.startswith("docs/") for path in paths), "Runtime changed")
        manifest = git(config, "show", f"{candidate}:manifest.json")
        require((repo / "manifest.json").read_bytes() == manifest
                and sha(manifest) == proof["manifestSha256"], "Reviewed manifest differs")
        validation = json.loads(frozen(closure / "validation-provenance.json"))
        require(validation["candidate"] == candidate
                and validation["reviewClosureSha256"] == sha(provenance_raw), "Validation scope differs")
        for inventory in (provenance, validation):
            for path, digest in inventory["recordedFileSha256"].items():
                frozen(closure / path, digest)
                guard.check()
        source_bindings = {}
        for name in ("b127_common.py", "run_b127_gates.py", "check_reading_b127.py"):
            expected = frozen(HERE / "review" / "candidate-inputs" / name)
            actual = (HERE / name).read_bytes()
            require(expected == actual == git(
                config, "show", f"{config['candidate']}:docs/n1-sources/batch-127/producers/{name}"),
                "Original gate implementation changed")
            source_bindings[name] = sha(actual)
        sys.path.insert(0, str(HERE))
        runner = load_module("b127_closure_host_gates", HERE / "run_b127_gates.py")
        require(list(runner.CHECKS) == ORDER, "Original gate order differs")
        for name in ORDER:
            original = json.loads(frozen(Path(config["gates"]) / f"{name}.json"))
            require(original["command"][2:] == list(map(str, runner.CHECKS[name]))
                    and original["cwd"] == str(repo), "Original gate command differs")
        output.mkdir()
        expected = None
        for name in ORDER:
            expected = runner.run_gate(name, output, expected)
            guard.check()
        require(expected == sha(manifest)
                and git(config, "status", "--porcelain=v1", "--untracked-files=all") == before
                and git(config, "rev-parse", "HEAD").decode().strip() == commit,
                "Gates changed the actual tree")
        result = {
            "batch": 127, "status": "PASS", "mode": mode, "head": commit, "base": config["base"],
            "reviewedSnapshot": candidate, "checks": ORDER, "manifestSha256": expected,
            "manifestReproducible": True, "closureProvenanceSha256": sha(provenance_raw),
            "wrapperSha256": sha(frozen(Path(__file__))), "sources": source_bindings,
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
    main(sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve())
