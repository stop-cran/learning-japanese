"""Mechanical proof for the B134 integration merge.

Usage: python -X utf8 merge_proof.py <repo-root> <merge-commit> <out.json>

Checks that every path in the merge tree, except the derived manifest.json,
is byte-identical to one of the two parents, that the B134 runtime files are
unchanged from the reviewed snapshot and closure commits, and that no
main-side change references or is linked from the B134 cards.
"""
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

REVIEWED = "cc374051"
CLOSURE = "ae155573"
B134_FILES = ["kanji/紫.md", "strokes/紫.json", "words/紫.md"]
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
    base = git(root, "merge-base", ours, theirs).strip()
    m, o, t = tree(root, merge), tree(root, ours), tree(root, theirs)
    unmatched = sorted(
        p for p in set(m) | set(o) | set(t)
        if p not in DERIVED and m.get(p) not in {o.get(p), t.get(p)}
    )
    main_changed = sorted(
        line for line in git(root, "diff", "--name-only", base, theirs).splitlines() if line
    )
    reviewed, closure = tree(root, REVIEWED), tree(root, CLOSURE)
    b134 = {
        p: {
            "merge": m.get(p),
            "reviewed": reviewed.get(p),
            "closure": closure.get(p),
            "identical": m.get(p) is not None and m.get(p) == reviewed.get(p) == closure.get(p),
        }
        for p in B134_FILES
    }
    links = sorted({
        link for p in B134_FILES if p.endswith(".md")
        for link in card_links(git(root, "show", f"{merge}:{p}"), p)
    })
    mentions = sorted(
        p for p in main_changed
        if p not in DERIVED and p in m
        and "紫" in git(root, "show", f"{merge}:{p}")
    )
    manifest_files = json.loads(git(root, "show", f"{merge}:manifest.json"))["files"]
    result = {
        "merge": merge,
        "parents": {"b134Handoff": ours, "originMain": theirs},
        "mergeBase": base,
        "pathsCompared": len(set(m) | set(o) | set(t)),
        "nonDerivedPathsMatchingNeitherParent": unmatched,
        "mainChangedPaths": len(main_changed),
        "mainChangedOverlapWithB134Runtime": sorted(set(main_changed) & set(B134_FILES)),
        "b134RuntimeFiles": b134,
        "b134CardLinks": links,
        "b134CardLinksChangedByMain": sorted(set(links) & set(main_changed)),
        "mainChangedNonDerivedPathsMentioningB134Kanji": mentions,
        "manifestListsB134Files": all(p in manifest_files for p in B134_FILES),
    }
    result["pass"] = (
        not unmatched
        and not result["mainChangedOverlapWithB134Runtime"]
        and all(v["identical"] for v in b134.values())
        and not result["b134CardLinksChangedByMain"]
        and not mentions
        and result["manifestListsB134Files"]
    )
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"pass": result["pass"], "unmatched": len(unmatched)}))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
