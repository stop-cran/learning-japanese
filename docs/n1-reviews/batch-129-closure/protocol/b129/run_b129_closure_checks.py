"""Run the signed reconciliation's unchanged ten gates on B129 closure."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, load_module, require, sha, start_guard
from finalize_b129 import CANDIDATE, check_history, check_proof

HERE = WS / "scratch-129"
SOURCE = HERE / "reconciliation-001"
ORDER = ["lint", "quiz-safety", "linkplan", "reading-exposure", "validate", "manifest",
         "unittest", "budget", "vocabulary", "manifest-rebuild"]


def main(mode, commit, output):
    require(mode in ("closure", "committed") and output.parent == HERE and not output.exists(),
            "Use closure|committed SHA and a new direct scratch-129 output")
    config = load_batch(129)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-129-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    proof = json.loads(frozen(closure / "verification" / "reconciliation-001.json"))
    check_history(provenance, CANDIDATE, config)
    check_proof(proof, CANDIDATE, config)
    guard, _ = start_guard("B129 closure host gates")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == commit, "HEAD differs")
        before = git(config, "status", "--porcelain=v1", "--untracked-files=all")
        if mode == "closure":
            require(commit == CANDIDATE and before, "Expected unsigned contributor closure")
            paths = [line[3:] for line in before.decode().splitlines()]
            require(all(path.startswith("docs/n1-reviews/batch-129-closure/")
                        or path == "docs/n1-sources/batch-129-progress.json" for path in paths),
                    "Unaccounted worktree changes")
        else:
            require(not before and git(config, "show", "-s", "--format=%P", commit).decode().strip() == CANDIDATE,
                    "Signed closure is not a clean direct child")
            paths = git(config, "diff", "--name-only", CANDIDATE, commit).decode().splitlines()
            require(paths and all(path.startswith("docs/") for path in paths), "Runtime changed")
        manifest = git(config, "show", f"{CANDIDATE}:manifest.json")
        require((repo / "manifest.json").read_bytes() == manifest
                and sha(manifest) == proof["manifestSha256"], "Reviewed manifest differs")
        validation = json.loads(frozen(closure / "validation-provenance.json"))
        require(validation["candidate"] == CANDIDATE
                and validation["reviewClosureSha256"] == sha(provenance_raw), "Validation differs")
        for inventory in (provenance, validation):
            for path, digest in inventory["recordedFileSha256"].items():
                frozen(closure / path, digest)
                guard.check()
        bindings = {}
        for name in ("b129_common.py", "recon_common.py", "run_gates.py", "check_reading.py"):
            path = HERE / name if name == "b129_common.py" else SOURCE / name
            expected = git(config, "show", f"{CANDIDATE}:docs/n1-sources/batch-129-reconciliation/producers/{name}")
            require(path.read_bytes() == expected, "Signed gate helper differs: " + name)
            bindings[name] = sha(expected)
        sys.path.insert(0, str(SOURCE))
        runner = load_module("b129_closure_gates", SOURCE / "run_gates.py")
        require(list(runner.CHECKS) == ORDER, "Signed gate order differs")
        for name in ORDER:
            receipt = json.loads(frozen(SOURCE / "committed-gates-001" / f"{name}.json"))
            require(receipt["command"][2:] == list(map(str, runner.CHECKS[name]))
                    and receipt["cwd"] == str(repo), "Signed gate command differs")
        output.mkdir()
        expected = None
        for name in ORDER:
            expected = runner.run_gate(name, output, expected)
            guard.check()
        require(expected == sha(manifest)
                and git(config, "status", "--porcelain=v1", "--untracked-files=all") == before
                and git(config, "rev-parse", "HEAD").decode().strip() == commit, "Gates changed tree")
        result = {
            "batch": 129, "status": "PASS", "mode": mode, "head": commit, "base": config["base"],
            "reviewedSnapshot": CANDIDATE, "checks": ORDER, "manifestSha256": expected,
            "manifestReproducible": True, "closureProvenanceSha256": sha(provenance_raw),
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
    main(sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve())
