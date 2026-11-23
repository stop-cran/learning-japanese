#!/usr/bin/env python3
"""Run tools/audit_n1_batch.py for batch 159 at the merge with current main.

The stock audit compares the runtime manifest with the manifest at the ledger's
baseCommit. Main changed 13 kanji cards after that base (illness-radical
mnemonics and 隹 relabels), so at the merge the stock audit may stop with
"Changed baseline payload differs from recorded reused passages". This script
first proves that main's runtime changes since the base are exactly the
non-docs files main changed, and that none of them is a batch file (member,
support or recorded reused article), then reruns the unchanged audit with one
substitution:
manifest.json at the base is read from main's head (the merge's second parent).
Every other base read (source index, word candidates, variants, reused
passages) still uses the recorded baseCommit.
"""
import argparse
import contextlib
import io
import json
import subprocess
import sys
from pathlib import Path

BATCH = "159"
MERGE = "3ecba19ca48d16380db5f07e602a6fc8fa0f95a5"
REVIEWED = "33c3b5829887b2e49e0f67ce649fad8b2a722ea7"
MAIN = "f5caf53cea9ac3989c33018408d7d9ffb065b074"


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True).stdout.decode("utf-8")


def payload(manifest):
    return {(section, name): value
            for section, entries in manifest.items() if isinstance(entries, dict)
            for name, value in entries.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    repo = Path(args.repo).resolve()
    head = git(repo, "rev-parse", "HEAD").strip()
    parents = git(repo, "rev-list", "--parents", "-n", "1", MERGE).split()[1:]
    assert parents == [REVIEWED, MAIN], parents
    assert git(repo, "merge-base", "--is-ancestor", MERGE, head) == ""
    sys.path.insert(0, str(repo / "tools"))
    import audit_n1_batch as audit_module

    ledger = json.loads((repo / f"docs/n1-sources/batch-{BATCH}-progress.json")
                        .read_text(encoding="utf-8"))
    base = ledger["baseCommit"]
    stock_error = None
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            audit_module.audit(repo, BATCH)
    except ValueError as error:
        stock_error = str(error)

    base_manifest = json.loads(git(repo, "show", f"{base}:manifest.json"))
    main_manifest = json.loads(git(repo, "show", f"{MAIN}:manifest.json"))
    old, new = payload(base_manifest), payload(main_manifest)
    main_runtime_changes = sorted(f"{s}/{n}" for (s, n) in old.keys() | new.keys()
                                  if old.get((s, n)) != new.get((s, n)))
    meta = lambda m: {k: v for k, v in m.items()
                      if k != "contentVersion" and not isinstance(v, dict)}
    assert meta(base_manifest) == meta(main_manifest)
    main_changed_files = sorted(
        p for p in git(repo, "-c", "core.quotepath=false", "diff", "--name-only", base, MAIN).splitlines()
        if p and not p.startswith("docs/") and p != "manifest.json")
    assert sorted(n.split("/", 1)[1] for n in main_runtime_changes) == main_changed_files, (
        main_runtime_changes, main_changed_files)
    recorded = {r["article"] for r in ledger["changedReusedPassages"]}
    assert not recorded & set(main_changed_files), recorded & set(main_changed_files)
    batch_files = ({f"kanji/{c}.md" for c in ledger["membership"]}
                   | {r["article"] for r in ledger["supportMappings"]} | recorded)
    changed_batch = {n.split("/", 1)[1] for n in main_runtime_changes} & batch_files
    assert not changed_batch, changed_batch

    original = audit_module.base_file

    def base_file(root, commit, name):
        if commit == base and name == "manifest.json":
            return original(root, MAIN, name)
        return original(root, commit, name)

    audit_module.base_file = base_file
    result = audit_module.audit(repo, BATCH)
    report = {
        "head": head, "merge": MERGE, "parents": parents, "baseCommit": base,
        "stockAuditAtMerge": {"pass": stock_error is None, "error": stock_error},
        "mainRuntimeChangesSinceBase": main_runtime_changes,
        "mainChangedNonDocsFiles": main_changed_files,
        "runtimeBaselineSubstitution": f"manifest.json at {base} read from {MAIN}",
        "batchRuntimeFilesChangedByMain": sorted(changed_batch),
        "auditWithMainRuntimeBaseline": result,
    }
    Path(args.out).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8", newline="\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()