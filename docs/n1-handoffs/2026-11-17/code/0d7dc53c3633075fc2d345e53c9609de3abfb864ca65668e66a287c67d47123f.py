"""Run B134's unchanged host checks on working or signed reconciliation revisions.

Usage: run_b134_reconciliation_checks.py working|committed HEAD NEW_OUTPUT
NEW_OUTPUT must be a new direct child of scratch-134. This verifies mechanical
scope and signed lineage, not source claims or independent-review closure.
"""
import json
import re
import sys
from pathlib import Path, PurePosixPath

from common import freeze_json, frozen, load_module, require, sha, start_guard
import run_b134_closure_checks as closure
from verify_b134_sources import FINGERPRINT, Git, OWNER, TRAILER

RUNTIME = {"kanji/\u7d2b.md", "manifest.json"}
EVIDENCE = re.compile(r"docs/n1-sources/batch-134-reconciliation-[0-9]{3}/.+")
CLOSURE_HELPER_SHA = "cf02eab562db75a45a71c8ff0279a4e953dfe8724c31f56945d174eb3708e080"


def parse_changes(raw):
    fields = raw.decode("utf-8").split("\0")
    require(fields[-1] == "", "Git change list lacks its NUL terminator")
    fields.pop()
    require(len(fields) % 2 == 0, "Invalid Git change list")
    return list(zip(fields[::2], fields[1::2], strict=True))


def validate_scope(changes):
    require(changes, "No reconciliation changes")
    names = [name for _, name in changes]
    require(len(names) == len(set(names)), "Duplicate reconciliation path")
    for status, name in changes:
        path = PurePosixPath(name)
        require(not path.is_absolute() and ".." not in path.parts and "\\" not in name
                and str(path) == name, "Unsafe reconciliation path: " + name)
        if name in RUNTIME:
            require(status == "M", "Runtime content must remain an existing regular file: " + name)
        else:
            require(status == "A" and EVIDENCE.fullmatch(name),
                    "Only new reconciliation evidence and the card/manifest may change: " + name)
    return sorted(names)


def changed_files(git):
    changes = parse_changes(git("diff", "--no-renames", "--name-status", "-z", closure.CANDIDATE, "--"))
    untracked = git("ls-files", "--others", "--exclude-standard", "-z").decode("utf-8")
    changes.extend(("A", name) for name in untracked.split("\0") if name)
    return validate_scope(changes)


def snapshot(names):
    result = {}
    for name in names:
        path = closure.REPO / Path(name)
        require(path.is_file() and not path.is_symlink(), "Nonregular reconciliation file: " + name)
        result[name] = sha(path.read_bytes())
    return result


def main(mode, head, output):
    require(mode in ("working", "committed") and closure.FULL_SHA.fullmatch(head)
            and output.parent == closure.HERE and not output.exists(),
            "Use working|committed FULL_HEAD and a new direct scratch-134 output")
    frozen(Path(closure.__file__), CLOSURE_HELPER_SHA)
    guard, _ = start_guard("B134 reconciliation host gates")
    try:
        git = Git(closure.REPO, closure.RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == head, "HEAD differs")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", closure.CANDIDATE).decode().strip()
                == f"{closure.BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Initial candidate identity differs")
        require(TRAILER in git("show", "-s", "--format=%B", closure.CANDIDATE),
                "Initial candidate lacks trailer")
        count = closure.lineage(git, head)
        before_status = git("status", "--porcelain=v1", "--untracked-files=all")
        require(bool(before_status) if mode == "working" else not before_status,
                "Working mode requires edits; committed mode requires a clean tree")
        require(mode != "committed" or count > 0, "Committed reconciliation cannot be the initial candidate")
        names = changed_files(git)
        before = snapshot(names)
        manifest = (closure.REPO / "manifest.json").read_bytes()
        bindings = {}
        for name in closure.HELPERS:
            raw = git("show", f"{closure.CANDIDATE}:docs/n1-sources/batch-134/producers/{name}")
            require((closure.HERE / name).read_bytes() == raw, "Signed gate helper differs: " + name)
            bindings[name] = sha(raw)
        sys.path.insert(0, str(closure.HERE))
        runner = load_module("b134_reconciliation_gates", closure.HERE / "run_134_gates.py")
        require(list(runner.CHECKS) == closure.ORDER, "Signed gate order differs")
        output.mkdir()
        expected = None
        for name in closure.ORDER:
            expected = runner.run_gate(name, output, expected)
            guard.check()
        require(expected == sha(manifest), "Manifest was stale before reconciliation gates")
        require(git("rev-parse", "HEAD").decode().strip() == head
                and git("status", "--porcelain=v1", "--untracked-files=all") == before_status
                and changed_files(git) == names and snapshot(names) == before,
                "Gates changed the reconciliation tree")
        result = {
            "batch": 134, "status": "PASS", "mode": mode, "head": head, "base": closure.BASE,
            "initialSnapshot": closure.CANDIDATE, "reconciliationCommits": count,
            "checks": closure.ORDER, "manifestSha256": expected, "manifestReproducible": True,
            "changedFiles": before, "wrapperSha256": sha(frozen(Path(__file__))),
            "closureHelperSha256": CLOSURE_HELPER_SHA, "sources": bindings,
            "logs": {name: {"receiptSha256": sha((output / f"{name}.json").read_bytes()),
                           "logSha256": sha((output / f"{name}.log").read_bytes())}
                     for name in closure.ORDER},
            "limits": "Mechanical actual-tree checks only; not source/linguistic, review closure, "
                      "native/device, arbitrary-pool or publication acceptance.",
        }
        freeze_json(output / "summary.json", result)
        for path in output.iterdir():
            path.chmod(0o444)
        print(json.dumps(result))
    finally:
        require(not guard.finish()["breach"], "Reconciliation gates RAM breach")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: run_b134_reconciliation_checks.py working|committed FULL_HEAD NEW_OUTPUT")
    main(sys.argv[1], sys.argv[2], Path(sys.argv[3]).resolve())
