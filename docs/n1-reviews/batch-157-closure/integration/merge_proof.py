"""Mechanical proof for the B157 integration merge.

Usage: python -X utf8 merge_proof.py <repo-root> <merge-commit> <out.json> [<first-parent>]

Adapted from the B157 closure's merge_proof.py. Checks that every path in the
merge tree, except the derived manifest.json, is byte-identical to one of the
two parents; that the B157 runtime files (every non-docs path the batch changed
from its published base before the merge, at f1a69909) equal the first parent;
and that no main-side change touches or is linked from the batch's files, and no
line that main adds or removes mentions the batch's kanji or word articles.
Files that main changed and that mention them on lines main left alone are
listed for information. Binary files that main changed (images) are listed but
not scanned for mentions. The first parent defaults to f1a69909.

Two changes from the B156 version: mentions on lines of files that main deleted
outright (the pruned raw review transcripts) are listed separately and do not
fail the proof, since no merged file keeps those lines; and the manifest check
covers only runtime content paths, not the batch's change to tools/. Paths
that main deleted are reported as a count and a SHA-256 of their sorted,
newline-joined list rather than listed, to keep the record small.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

PUBLISHED_BASE = "e2c25363285fd8fa100d1c4178e7289592562a31"
BATCH_TIP = "f1a699094f4a7dd3aa4490ef83247f95c3af6bea"
KANJI = "佐佳併侍侮侯俊俗俵倫"
DERIVED = {"manifest.json"}


def git(root, *args):
    return subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=root, check=True, capture_output=True, text=True, encoding="utf-8",
    ).stdout


def tree(root, rev):
    out = git(root, "ls-tree", "-r", "-z", rev)
    entries = {}
    for item in out.split("\0"):
        if item:
            meta, path = item.split("\t", 1)
            entries[path] = meta.split()[2]
    return entries


def card_links(text, path):
    base = PurePosixPath(path).parent
    links = set()
    for target in re.findall(r"\]\(([^)#\s]+\.md)\)", text):
        parts = []
        for part in (base / target).parts:
            if part == "..":
                parts.pop()
            else:
                parts.append(part)
        links.add("/".join(parts))
    return sorted(links)


def main():
    root, merge, out = sys.argv[1:4]
    reviewed_rev = git(root, "rev-parse", sys.argv[4] if len(sys.argv) > 4 else BATCH_TIP).strip()
    merge = git(root, "rev-parse", merge).strip()
    parents = git(root, "rev-list", "--parents", "-n", "1", merge).split()[1:]
    if len(parents) != 2:
        raise SystemExit("merge commit must have exactly two parents")
    ours, theirs = parents
    if ours != reviewed_rev:
        raise SystemExit("first parent must be the reviewed fix snapshot")
    base = git(root, "merge-base", ours, theirs).strip()
    m, o, t = tree(root, merge), tree(root, ours), tree(root, theirs)
    unmatched = sorted(
        p for p in set(m) | set(o) | set(t)
        if p not in DERIVED and m.get(p) not in {o.get(p), t.get(p)}
    )
    main_changed = sorted(
        line for line in git(root, "diff", "--name-only", base, theirs).splitlines() if line
    )
    batch_files = sorted(
        line for line in git(root, "diff", "--name-only", PUBLISHED_BASE, BATCH_TIP).splitlines()
        if line and not line.startswith("docs/") and line not in DERIVED
    )
    words = [PurePosixPath(p).stem for p in batch_files if p.startswith("words/")]
    reviewed = tree(root, reviewed_rev)
    runtime = {
        p: {
            "merge": m.get(p),
            "reviewed": reviewed.get(p),
            "identical": m.get(p) is not None and m.get(p) == reviewed.get(p),
        }
        for p in batch_files
    }
    links = sorted({
        link for p in batch_files if p.endswith(".md")
        for link in card_links(git(root, "show", f"{merge}:{p}"), p)
    })
    def hits_in(text):
        return sorted({c for c in text if c in KANJI}) + [w for w in words if w in text]

    mentions = {}
    deleted_mentions = {}
    context_mentions = {}
    binary = sorted(
        line.split("\t", 2)[2] for line in git(root, "diff", "--numstat", base, theirs).splitlines()
        if line.startswith("-\t-\t")
    )
    for p in main_changed:
        if p in DERIVED or p in binary:
            continue
        diff = git(root, "diff", "-U0", base, theirs, "--", p)
        changed_lines = "\n".join(
            line[1:] for line in diff.splitlines()
            if line[:1] in "+-" and not line.startswith(("+++", "---"))
        )
        hits = hits_in(changed_lines)
        if hits and p not in m:
            deleted_mentions[p] = hits
        elif hits:
            mentions[p] = hits
        if p in m:
            whole = hits_in(git(root, "show", f"{merge}:{p}"))
            if whole and not hits:
                context_mentions[p] = whole
    deleted = [p for p in main_changed if p not in m]
    manifest_files = set()
    for group in json.loads(git(root, "show", f"{merge}:manifest.json")).values():
        if isinstance(group, dict):
            manifest_files |= set(group)
    result = {
        "merge": merge,
        "parents": {"b157ReviewedFix": ours, "originMain": theirs},
        "mergeBase": base,
        "publishedBase": PUBLISHED_BASE,
        "pathsCompared": len(set(m) | set(o) | set(t)),
        "nonDerivedPathsMatchingNeitherParent": unmatched,
        "mainChangedPathsKept": [p for p in main_changed if p in m],
        "mainDeletedPaths": {
            "count": len(deleted),
            "sha256OfSortedNewlineJoinedList": hashlib.sha256("\n".join(deleted).encode("utf-8")).hexdigest(),
        },
        "b157RuntimePaths": len(batch_files),
        "mainChangedOverlapWithB157Runtime": sorted(set(main_changed) & set(batch_files)),
        "b157RuntimeFilesIdenticalToReviewed": all(v["identical"] for v in runtime.values()),
        "b157RuntimeFiles": runtime,
        "b157LinkTargets": len(links),
        "b157LinkTargetsChangedByMain": sorted(set(links) & set(main_changed)),
        "mainChangedLinesMentioningB157KanjiOrWords": mentions,
        "mainDeletedPathsMentioningB157KanjiOrWords": deleted_mentions,
        "mainChangedBinaryPathsNotScanned": [p for p in binary if p in m],
        "mainDeletedBinaryPaths": sum(1 for p in binary if p not in m),
        "mainChangedPathsMentioningB157KanjiOrWordsOnUnchangedLinesOnly": context_mentions,
        "manifestListsB157Files": all(p in manifest_files for p in batch_files
                                      if not p.startswith("tools/")),
    }
    result["pass"] = (
        not unmatched
        and not result["mainChangedOverlapWithB157Runtime"]
        and result["b157RuntimeFilesIdenticalToReviewed"]
        and not result["b157LinkTargetsChangedByMain"]
        and not mentions
        and result["manifestListsB157Files"]
    )
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"pass": result["pass"], "unmatched": len(unmatched),
                      "runtime": len(batch_files), "links": len(links)}))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
