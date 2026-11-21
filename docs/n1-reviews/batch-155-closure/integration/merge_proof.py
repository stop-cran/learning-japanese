"""Mechanical proof for the B155 integration merge.

Usage: python -X utf8 merge_proof.py <repo-root> <merge-commit> <out.json>

Checks that every path in the merge tree, except the derived manifest.json,
is byte-identical to one of the two parents; that the B155 runtime files
(every non-docs path the batch changed from its published base) equal the
reviewed fix snapshot; and that no main-side change touches, is linked
from, or mentions the batch's kanji or word articles.
"""
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

PUBLISHED_BASE = "6cbc14fe25c05447674a90c6c3173060d5b4c621"
REVIEWED = "25609582e7d44eed71b10b3fe8ab7e9a5a3931e9"
KANJI = "卑汰沙沢胡鼓"
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
    merge = git(root, "rev-parse", merge).strip()
    parents = git(root, "rev-list", "--parents", "-n", "1", merge).split()[1:]
    if len(parents) != 2:
        raise SystemExit("merge commit must have exactly two parents")
    ours, theirs = parents
    if ours != REVIEWED:
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
        line for line in git(root, "diff", "--name-only", PUBLISHED_BASE, REVIEWED).splitlines()
        if line and not line.startswith("docs/") and line not in DERIVED
    )
    words = [PurePosixPath(p).stem for p in batch_files if p.startswith("words/")]
    reviewed = tree(root, REVIEWED)
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
    mentions = {}
    for p in main_changed:
        if p in DERIVED or p not in m:
            continue
        text = git(root, "show", f"{merge}:{p}")
        hits = sorted({c for c in text if c in KANJI}) + [w for w in words if w in text]
        if hits:
            mentions[p] = hits
    manifest_files = set()
    for group in json.loads(git(root, "show", f"{merge}:manifest.json")).values():
        if isinstance(group, dict):
            manifest_files |= set(group)
    result = {
        "merge": merge,
        "parents": {"b155ReviewedFix": ours, "originMain": theirs},
        "mergeBase": base,
        "publishedBase": PUBLISHED_BASE,
        "pathsCompared": len(set(m) | set(o) | set(t)),
        "nonDerivedPathsMatchingNeitherParent": unmatched,
        "mainChangedPaths": main_changed,
        "b155RuntimePaths": len(batch_files),
        "mainChangedOverlapWithB155Runtime": sorted(set(main_changed) & set(batch_files)),
        "b155RuntimeFilesIdenticalToReviewed": all(v["identical"] for v in runtime.values()),
        "b155RuntimeFiles": runtime,
        "b155LinkTargets": len(links),
        "b155LinkTargetsChangedByMain": sorted(set(links) & set(main_changed)),
        "mainChangedNonDerivedPathsMentioningB155KanjiOrWords": mentions,
        "manifestListsB155Files": all(p in manifest_files for p in batch_files),
    }
    result["pass"] = (
        not unmatched
        and not result["mainChangedOverlapWithB155Runtime"]
        and result["b155RuntimeFilesIdenticalToReviewed"]
        and not result["b155LinkTargetsChangedByMain"]
        and not mentions
        and result["manifestListsB155Files"]
    )
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"pass": result["pass"], "unmatched": len(unmatched),
                      "runtime": len(batch_files), "links": len(links)}))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
