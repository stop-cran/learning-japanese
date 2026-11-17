"""Unchanged B134 ten gates on pending/signed integration merges and closures.

Unlike run_b134_closure_checks, the manifest is the deterministic combined manifest,
not the old reviewed manifest. Signed producers/commands/order and RAM rules are reused.
No commit, staging, merge, or network operation is performed.

Usage: MODE C M_OR_DASH HEAD PLAN_OR_DASH NEW_OUT
MODE: merge | committed-merge | closure | committed-closure.
merge uses M=-, HEAD=C and requires MERGE_HEAD=INCOMING; closure uses HEAD=M.
Closure modes require a frozen coordinator integration plan. OUT is a new review child.
"""
import hashlib
import json
import sys
from pathlib import Path

import b134_integrated_v1 as contract
from common import freeze_json, frozen, json_bytes, load_module, require, sha, start_guard
from run_b134_closure_checks import BASE, HELPERS, ORDER
from verify_b134_packet import RUNNER
from verify_b134_sources import Git


def object_id(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def working_tree(git, repo, guard):
    """Whole actual file/mode snapshot, including new archive files; never writes index."""
    tracked = git("ls-files", "--stage", "-z")
    result = {}
    for row in tracked.split(b"\0"):
        if not row:
            continue
        meta, name = row.split(b"\t", 1)
        mode, _, stage = meta.decode().split()
        name = contract.relative(name.decode("utf-8"))
        require(stage == "0" and name not in result and mode in ("100644", "100755"),
                "Unresolved/nonregular/duplicate index entry")
        path = repo / name
        require(path.is_file() and not path.is_symlink(), "Missing or symbolic worktree path")
        result[name] = (mode, "blob", object_id(path.read_bytes()))
        guard.check()
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode("utf-8").split("\0")
    for name in filter(None, untracked):
        contract.relative(name)
        path = repo / name
        require(path.is_file() and not path.is_symlink(), "Nonregular untracked input")
        result[name] = ("100644", "blob", object_id(path.read_bytes()))
        guard.check()
    return result


def tree_digest(entries):
    return sha(json_bytes(dict(sorted(entries.items()))))


def validate_tree(mode, git, repo, closure, merged, head, plan, guard):
    contract.full(closure, head)
    require(git("rev-parse", "HEAD").decode().strip() == head, "HEAD differs")
    working = working_tree(git, repo, guard)
    if mode == "merge":
        require(merged is None and head == closure
                and git("rev-parse", "--verify", "MERGE_HEAD").decode().strip() == contract.INCOMING,
                "Expected actual pending two-parent merge")
        require(not git("diff", "--name-only") and not git("ls-files", "--others", "--exclude-standard"),
                "Merge must be fully resolved/staged with no unrelated files")
        context = contract.merge(git, closure, staged=working, manifest=(repo / "manifest.json").read_bytes())
    elif mode == "committed-merge":
        require(head == merged and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Expected clean signed merge")
        context = contract.merge(git, closure, merged)
        require(working == contract.tree(git, head), "Actual files differ from committed merge")
    else:
        require(plan is not None and plan["signedClosure"] == closure and plan["merge"] == merged,
                "Closure plan differs")
        signed = mode == "committed-closure"
        require(mode in ("closure", "committed-closure") and (signed or head == merged),
                "Closure mode/HEAD differs")
        if signed:
            require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Dirty signed closure")
            require(working == contract.tree(git, head), "Actual files differ from signed closure")
        context = contract.verify_closure(git, plan, head, signed, working,
                                           lambda name: (repo / name).read_bytes())
        contract.plan_gates(git, plan)
    return context, tree_digest(working)


def main(mode, closure, merged, head, plan_path, output):
    require(mode in ("merge", "committed-merge", "closure", "committed-closure"), "Invalid gate mode")
    output = Path(output).resolve()
    require(output.parent == contract.REVIEW and not output.exists(), "Use a new direct review output")
    merged = None if merged == "-" else merged
    plan = None if plan_path == "-" else contract.load_plan(Path(plan_path))[0]
    guard, _ = start_guard("B134 integrated-tree host gates")
    try:
        git = Git(contract.REPO, RUNNER, guard)
        require(git("remote", "get-url", "origin").decode().strip()
                == "https://github.com/stop-cran/learning-japanese.git", "Wrong origin")
        context, before_tree = validate_tree(mode, git, contract.REPO, closure, merged, head, plan, guard)
        before_status = git("status", "--porcelain=v1", "--untracked-files=all")
        helpers = {}
        for name in HELPERS:
            signed = contract.blob(git, contract.REVIEWED, f"docs/n1-sources/batch-134/producers/{name}")
            frozen(contract.SCRATCH / name, sha(signed))
            helpers[name] = sha(signed)
        sys.path.insert(0, str(contract.SCRATCH))
        runner = load_module("b134_integrated_signed_gates", contract.SCRATCH / "run_134_gates.py")
        require(list(runner.CHECKS) == ORDER and runner.REPO == contract.REPO,
                "Signed gate order/worktree differs")
        commands = {name: [sys.executable, "-B", str(contract.SCRATCH / "bounded_launch_134.py"),
                           *map(str, runner.CHECKS[name])] for name in ORDER}
        require(commands == contract.expected_commands(), "Signed gate command contract differs")
        output.mkdir()
        expected = None
        for name in ORDER:
            expected = runner.run_gate(name, output, expected)
            guard.check()
        after_context, after_tree = validate_tree(mode, git, contract.REPO, closure, merged, head, plan, guard)
        require(before_tree == after_tree and context == after_context
                and git("status", "--porcelain=v1", "--untracked-files=all") == before_status
                and expected == sha((contract.REPO / "manifest.json").read_bytes()),
                "Host gates changed the exact integrated tree/manifest/status")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Integrated host gates RAM breach")
    result = {"status": "PASS", "batch": 134, "mode": mode, "head": head,
              "signedClosure": closure, "merge": merged, "incoming": contract.INCOMING,
              "reviewedSnapshot": contract.REVIEWED, "base": BASE, "checks": ORDER, "serial": True,
              "commands": commands, "helperHashes": helpers, "treeInventorySha256": before_tree,
              "manifestSha256": expected, "manifestReproducible": True, "context": context,
              "memory": memory, "producerSha256": sha(frozen(Path(__file__))),
              "logs": {name: {"receiptSha256": sha((output / f"{name}.json").read_bytes()),
                              "logSha256": sha((output / f"{name}.log").read_bytes())} for name in ORDER},
              "limits": "Actual-tree host/static gates, not semantic integration acceptance or publication."}
    for path in output.iterdir():
        path.chmod(0o444)
    freeze_json(output / "summary.json", result)
    print(json.dumps(result))


if __name__ == "__main__":
    require(len(sys.argv) == 7, __doc__)
    main(*sys.argv[1:])
