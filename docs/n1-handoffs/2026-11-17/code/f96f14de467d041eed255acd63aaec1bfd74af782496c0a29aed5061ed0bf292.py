"""SUPERSEDED DRAFT, retained only. Not a selected runnable handoff.

Coordinator supplied actual revision002 scope/gate producers instead. The selected
b134_revision_proofs_v1.py consumes those proofs; do not run this duplicate runner.

The original signed ten run_gate functions/commands are reused unchanged, but their
old main() (which requires parent e17) is NOT invoked. This wrapper admits only a
direct signed child of reviewed355, purple-card/manifest edits and additive same-
batch source evidence. Existing source/claim/review/ledger objects stay byte-identical.
Usage: author|committed CANDIDATE_OR_DASH NEW_DIRECT_REVIEW_OUTPUT
"""
import json
import sys
from pathlib import Path

import b134_integrated_v1 as base
from common import GUARD_SHA, freeze_json, frozen, json_bytes, load_module, require, sha, start_guard
from run_b134_integration_gates_v1 import tree_digest, working_tree
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

ROOT = base.REVIEW
CARD = "kanji/\u7d2b.md"


def verify_revision(git, candidate=None, staged=None, read=None):
    before = base.tree(git, base.REVIEWED)
    if candidate is not None:
        base.identity(git, candidate, [base.REVIEWED])
        after = base.tree(git, candidate)
        read = lambda path: base.blob(git, candidate, path)
    else:
        require(staged is not None and read is not None, "Pending revision files missing")
        after = staged
    require(before.keys() <= after.keys()
            and {path for path in before if before[path] != after[path]} == {CARD, "manifest.json"},
            "Revision changed/removed existing objects beyond purple and manifest")
    added = after.keys() - before.keys()
    require(all(path.startswith("docs/n1-sources/batch-134/") and after[path][:2] == ("100644", "blob")
                for path in added)
            and all(after[path][:2] == ("100644", "blob") for path in (CARD, "manifest.json")),
            "Revision adds unrelated/nonregular evidence")
    old_raw, new_raw = base.blob(git, base.REVIEWED, "manifest.json"), read("manifest.json")
    old, new = (base.runtime_entries(json.loads(raw)) for raw in (old_raw, new_raw))
    require(old.keys() == new.keys() and len(new) == 8747
            and {p for p in old if old[p] != new[p]} == {CARD}
            and all(old[p][1] == new[p][1] for p in old), "Revision runtime membership/classification changed")
    expected = json.loads(old_raw)
    rows = [values for values in expected.values() if isinstance(values, dict) and CARD in values]
    require(len(rows) == 1, "Purple manifest membership differs")
    rows[0][CARD] = sha(read(CARD).replace(b"\r\n", b"\n"))
    payload = {key: value for key, value in expected.items() if key not in ("schemaVersion", "contentVersion")}
    expected["contentVersion"] = sha(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode())[:16]
    require(new_raw == (json.dumps(expected, ensure_ascii=False, indent=1, sort_keys=True) + "\n").encode(),
            "Revision manifest is not the exact deterministic update")
    return {"status": "PASS_ACTUAL_SIGNED_REVISION_PRESERVATION_ONLY" if candidate else "PASS_PENDING_REVISION_SCOPE_ONLY",
            "candidate": candidate, "priorSnapshot": base.REVIEWED, "changedPaths": [CARD, "manifest.json"],
            "addedEvidence": sorted(added), "manifestSha256": sha(new_raw),
            "contentVersion": expected["contentVersion"], "runtimeEntries": 8747,
            "reviewAccepted": False, "publicationAccepted": False}


def verify_gates(git, candidate, refs, manifest_sha):
    require(set(refs) == {"author", "committed"}, "Both actual revision gate runs required")
    expected_tree = tree_digest(base.tree(git, candidate))
    helpers = {name: sha(base.blob(git, base.REVIEWED, f"docs/n1-sources/batch-134/producers/{name}"))
               for name in base.HELPERS}
    for mode, item in refs.items():
        summary = json.loads(base.read_ref(item))
        require(summary["status"] == "PASS_REVISION_GATES_ONLY" and summary["mode"] == mode
                and summary["head"] == (base.REVIEWED if mode == "author" else candidate)
                and summary["candidate"] == (None if mode == "author" else candidate)
                and summary["priorSnapshot"] == base.REVIEWED
                and summary["treeInventorySha256"] == expected_tree
                and summary["helperHashes"] == helpers
                and summary["checks"] == base.ORDER and summary["serial"] is True
                and summary["manifestSha256"] == manifest_sha
                and summary["producerSha256"] == sha(Path(__file__).read_bytes())
                and summary["commands"] == base.expected_commands()
                and not summary["memory"]["breach"], "Revision gate summary identity differs")
        folder, previous = Path(item["path"]).parent, None
        for name in base.ORDER:
            row = summary["logs"][name]
            receipt = json.loads(frozen(folder / (name + ".json"), row["receiptSha256"]))
            log = frozen(folder / (name + ".log"), row["logSha256"])
            require(receipt["gate"] == name and receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                    and receipt["cleanupError"] is None and receipt["activeError"] is None
                    and not receipt["memory"]["breach"] and receipt["guardSha256"] == GUARD_SHA
                    and receipt["command"] == summary["commands"][name] and receipt["cwd"] == str(base.REPO)
                    and receipt["base"] == base.BASE and receipt["logSha256"] == sha(log)
                    and receipt["runnerSha256"] == helpers["run_134_gates.py"]
                    and receipt["commonHelperSha256"] == helpers["common_134.py"]
                    and receipt["boundedLauncherSha256"] == helpers["bounded_launch_134.py"]
                    and receipt["waitTimeoutSeconds"] == .1 and receipt["cleanupTimeoutSecondsPerStage"] == 10
                    and receipt["startedAt"] <= receipt["completedAt"]
                    and (previous is None or previous <= receipt["startedAt"]), "Revision gate execution differs")
            previous = receipt["completedAt"]
            if name in ("manifest", "manifest-rebuild"):
                require(receipt["manifestSha256"] == manifest_sha, "Revision manifest gate differs")
            if name == "manifest-rebuild":
                require(receipt["manifestReproducible"] is True, "Revision manifest not reproduced")


def run(mode, candidate, out):
    require(mode in ("author", "committed") and (candidate == "-") == (mode == "author"), "Wrong gate mode/candidate")
    candidate = None if mode == "author" else candidate
    out = Path(out).resolve()
    require(out.parent == ROOT and not out.exists(), "Use a NEW direct review output")
    out.mkdir()
    guard, _ = start_guard("B134 actual revision host gates")
    try:
        git = Git(base.REPO, RUNNER, guard)
        head = candidate or base.REVIEWED
        require(git("rev-parse", "HEAD").decode().strip() == head
                and git("remote", "get-url", "origin").decode().strip()
                == "https://github.com/stop-cran/learning-japanese.git", "Revision HEAD/origin differs")
        if candidate:
            require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Dirty signed revision")
        before = working_tree(git, base.REPO, guard)
        proof = verify_revision(git, candidate, before, lambda path: (base.REPO / path).read_bytes())
        require(before == (base.tree(git, candidate) if candidate else before), "Revision worktree differs")
        status = git("status", "--porcelain=v1", "--untracked-files=all")
        helpers = {}
        for name in base.HELPERS:
            digest = sha(base.blob(git, base.REVIEWED, f"docs/n1-sources/batch-134/producers/{name}"))
            frozen(base.SCRATCH / name, digest)
            helpers[name] = digest
        sys.path.insert(0, str(base.SCRATCH))
        runner = load_module("b134_signed_revision_gates", base.SCRATCH / "run_134_gates.py")
        commands = {name: [sys.executable, "-B", str(base.SCRATCH / "bounded_launch_134.py"),
                           *map(str, runner.CHECKS[name])] for name in base.ORDER}
        require(list(runner.CHECKS) == base.ORDER and runner.REPO == base.REPO
                and commands == base.expected_commands(), "Revision changed signed gate commands/order")
        expected = None
        for name in base.ORDER:
            expected = runner.run_gate(name, out, expected)
            guard.check()
        require(before == working_tree(git, base.REPO, guard)
                and status == git("status", "--porcelain=v1", "--untracked-files=all")
                and expected == proof["manifestSha256"], "Revision gates changed files/index/status")
        result = {"status": "PASS_REVISION_GATES_ONLY", "mode": mode, "head": head, "candidate": candidate,
                  "priorSnapshot": base.REVIEWED, "treeInventorySha256": tree_digest(before),
                  "helperHashes": helpers, "checks": base.ORDER, "serial": True, "commands": commands,
                  "manifestSha256": expected, "producerSha256": sha(Path(__file__).read_bytes()),
                  "scopeProof": proof,
                  "logs": {name: {"receiptSha256": sha((out / (name + ".json")).read_bytes()),
                                  "logSha256": sha((out / (name + ".log")).read_bytes())} for name in base.ORDER}}
    finally:
        memory = guard.finish()
        for path in out.iterdir():
            path.chmod(0o444)
        freeze_json(out / "memory.json", memory)
    require(not memory["breach"], "Revision host gates RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(out / "summary.json", result)))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("author", "committed"))
    parser.add_argument("candidate")
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    run(args.mode, args.candidate, args.out)
