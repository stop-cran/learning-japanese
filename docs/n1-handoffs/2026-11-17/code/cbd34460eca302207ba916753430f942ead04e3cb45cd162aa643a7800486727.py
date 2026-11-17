"""Run the unchanged signed B130 host gates on the actual contributor-only closure."""
import json
import sys
from pathlib import Path

from b130_closure_ledger_v2 import check_history
from b130_fresh_archive import ledger_acceptance
from b130_revision_gates import commands
from common import WS, freeze_json, frozen, git, load_batch, load_module, require, sha, start_guard
from confirm_b130_fresh_context import preflight
from finalize_b130 import CANDIDATE, check_proofs

HERE = WS / "scratch-130"
ORDER = ["lint", "quiz-safety", "linkplan", "reading-exposure", "validate", "manifest",
         "unittest", "budget", "vocabulary", "manifest-rebuild"]


def main(mode, commit, output):
    require(mode in ("closure", "committed") and output.parent == HERE and not output.exists(),
            "Use closure|committed SHA and a new direct scratch-130 output")
    config = load_batch(130)
    repo = Path(config["repo"])
    closure = repo / "docs" / "n1-reviews" / "batch-130-closure"
    provenance_raw = frozen(closure / "provenance.json")
    provenance = json.loads(provenance_raw)
    proof = json.loads(frozen(closure / "verification" / "reconciliation-001.json"))
    runtime = json.loads(frozen(closure / "verification" / "runtime-proof.json"))
    sources = json.loads(frozen(closure / "verification" / "source-proof.json"))
    check_proofs(proof, runtime, sources)
    finals = []
    for family in ("claude", "gpt"):
        run = f"N1-B130-{family.upper()}-CONFIRM-002"
        accepted = json.loads(frozen(HERE / "review" / "confirm" / f"{run}-acceptance.json"))
        record, _ = preflight(HERE / "review" / "confirm" / f"{run}-preflight.json")
        finals.append(ledger_acceptance(accepted, record))
    check_history(provenance, CANDIDATE, config, finals)
    guard, _ = start_guard("B130 closure host gates")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == commit, "HEAD differs")
        before = git(config, "status", "--porcelain=v1", "--untracked-files=all")
        if mode == "closure":
            require(commit == CANDIDATE and before, "Expected unsigned contributor closure")
            paths = [line[3:] for line in before.decode().splitlines()]
            require(all(name.startswith("docs/n1-reviews/batch-130-closure/")
                        or name == "docs/n1-sources/batch-130-progress.json" for name in paths),
                    "Unaccounted worktree changes")
        else:
            require(not before and git(config, "show", "-s", "--format=%P", commit).decode().strip()
                    == CANDIDATE, "Signed closure is not a clean direct child")
            paths = git(config, "diff", "--name-only", CANDIDATE, commit).decode().splitlines()
            require(paths and all(name.startswith("docs/") for name in paths), "Runtime changed")
        manifest = git(config, "show", f"{CANDIDATE}:manifest.json")
        require((repo / "manifest.json").read_bytes() == manifest
                and sha(manifest) == runtime["manifestSha256"], "Reviewed manifest differs")
        validation = json.loads(frozen(closure / "validation-provenance.json"))
        require(validation["candidate"] == CANDIDATE
                and validation["reviewClosureSha256"] == sha(provenance_raw), "Validation differs")
        for inventory in (provenance, validation):
            for name, digest in inventory["recordedFileSha256"].items():
                frozen(closure / name, digest)
                guard.check()
        bindings = {}
        for name in ("b130_common.py", "run_b130_gates.py", "check_reading_b130.py"):
            expected = git(config, "show", f"{CANDIDATE}:docs/n1-sources/batch-130/producers/{name}")
            require((HERE / name).read_bytes() == expected, "Signed gate helper differs: " + name)
            bindings[name] = sha(expected)
        sys.path.insert(0, str(HERE))
        runner = load_module("b130_closure_gates", HERE / "run_b130_gates.py")
        require(list(runner.CHECKS) == ORDER
                and {key: list(map(str, value)) for key, value in runner.CHECKS.items()}
                == {key: list(map(str, value)) for key, value in commands().items()},
                "Signed gate commands or order differ")
        output.mkdir()
        expected = None
        for name in ORDER:
            expected = runner.run_gate(name, output, expected)
            guard.check()
        require(expected == sha(manifest)
                and git(config, "status", "--porcelain=v1", "--untracked-files=all") == before
                and git(config, "rev-parse", "HEAD").decode().strip() == commit, "Gates changed tree")
        result = {
            "batch": 130, "status": "PASS", "mode": mode, "head": commit, "base": config["base"],
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
