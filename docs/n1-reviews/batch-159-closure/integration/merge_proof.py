"""Mechanical proof for the B159 integration merge.

Usage: python -X utf8 merge_proof.py <repo-root> <merge-commit> <out.json> [<first-parent>]

Adapted from the B157 closure's merge_proof.py. Checks that every path in the
merge tree, except the derived manifest.json, is byte-identical to one of the
two parents; that the B159 runtime files (every non-docs path the batch changed
from its base, at the reviewed snapshot 33c3b582) equal the first parent; and
that no main-side change touches or is linked from the batch's files, and no
line that main adds or removes mentions the batch's kanji or word articles.
Files that main changed and that mention them on lines main left alone are
listed for information. Binary files that main changed (images) are listed but
not scanned for mentions. The first parent defaults to 33c3b582.

One addition to the B157 version: main changed kanji cards, so the proof also
lists every batch file that mentions a kanji whose card main changed, and
compares each such card's front matter (title, readings, quiz fields, distractors
and exclusions) between the merge base and main. A changed quiz field on a
card the batch mentions fails the proof; other front-matter changes (such as
tags) are listed.

A main-side line that mentions a batch kanji passes only if it is listed in
REVIEWED with the reason it does not affect the batch, and only if the set of
flagged files and characters equals REVIEWED exactly.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

PUBLISHED_BASE = "2787e43b5706a569d83627849aa40ed3582a7d18"
BATCH_TIP = "33c3b5829887b2e49e0f67ce649fad8b2a722ea7"
KANJI = "厘又叔叙吉后吏吟呈呉"
QUIZ_FIELDS = ("kanji", "title", "onyomi", "kunyomi", "quizOnyomi", "quizKunyomi",
               "distractors", "quiz_exclusions")
DERIVED = {"manifest.json"}
REVIEWED = {
    "kanji/護.md": {
        "hits": ["又"],
        "reason": ("d513049c rewrote the 護 mnemonic line that already named 又 (\"the shape 又 below it\" became "
                   "\"隻 is the bird shape 隹 above the hand shape 又\"). The line does not link 又.md and makes no "
                   "claim about 又's title, readings or quiz fields; calling 又 a hand shape matches 右.md and 寂.md, "
                   "and 又.md makes no claim about the shape's origin."),
    },
}


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


def front_matter(text):
    head = text.replace("\r\n", "\n").split("---\n", 2)[1]
    fields = {}
    for line in head.splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields


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
        raise SystemExit("first parent must be the reviewed snapshot")
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
    main_kanji = {}
    for p in main_changed:
        if p.startswith("kanji/") and p.endswith(".md") and p in m and p in tree(root, base):
            before = front_matter(git(root, "show", f"{base}:{p}"))
            after = front_matter(git(root, "show", f"{theirs}:{p}"))
            main_kanji[PurePosixPath(p).stem] = {
                "path": p,
                "frontMatterKeysChanged": sorted(k for k in set(before) | set(after)
                                                 if before.get(k) != after.get(k)),
            }
    reverse = {}
    for c, info in main_kanji.items():
        info["batchFilesMentioning"] = sorted(
            p for p in batch_files if p.endswith(".md") and c in git(root, "show", f"{merge}:{p}"))
        info["quizFieldsChanged"] = [k for k in info["frontMatterKeysChanged"] if k in QUIZ_FIELDS]
        reverse[c] = info
    manifest_files = set()
    for group in json.loads(git(root, "show", f"{merge}:manifest.json")).values():
        if isinstance(group, dict):
            manifest_files |= set(group)
    result = {
        "merge": merge,
        "parents": {"b159ReviewedSnapshot": ours, "originMain": theirs},
        "mergeBase": base,
        "publishedBase": PUBLISHED_BASE,
        "pathsCompared": len(set(m) | set(o) | set(t)),
        "nonDerivedPathsMatchingNeitherParent": unmatched,
        "mainChangedPathsKept": [p for p in main_changed if p in m],
        "mainDeletedPaths": {
            "count": len(deleted),
            "sha256OfSortedNewlineJoinedList": hashlib.sha256("\n".join(deleted).encode("utf-8")).hexdigest(),
        },
        "b159RuntimePaths": len(batch_files),
        "mainChangedOverlapWithB159Runtime": sorted(set(main_changed) & set(batch_files)),
        "b159RuntimeFilesIdenticalToReviewed": all(v["identical"] for v in runtime.values()),
        "b159RuntimeFiles": runtime,
        "b159LinkTargets": len(links),
        "b159LinkTargetsChangedByMain": sorted(set(links) & set(main_changed)),
        "mainChangedLinesMentioningB159KanjiOrWords": mentions,
        "reviewedMainLineMentions": REVIEWED,
        "mainDeletedPathsMentioningB159KanjiOrWords": deleted_mentions,
        "mainChangedBinaryPathsNotScanned": [p for p in binary if p in m],
        "mainDeletedBinaryPaths": sum(1 for p in binary if p not in m),
        "mainChangedPathsMentioningB159KanjiOrWordsOnUnchangedLinesOnly": context_mentions,
        "mainChangedKanjiCards": reverse,
        "manifestListsB159Files": all(p in manifest_files for p in batch_files
                                      if not p.startswith("tools/")),
    }
    result["pass"] = (
        not unmatched
        and not result["mainChangedOverlapWithB159Runtime"]
        and result["b159RuntimeFilesIdenticalToReviewed"]
        and not result["b159LinkTargetsChangedByMain"]
        and {p: sorted(h) for p, h in mentions.items()} == {p: sorted(v["hits"]) for p, v in REVIEWED.items()}
        and result["manifestListsB159Files"]
        and not any(v["batchFilesMentioning"] and v["quizFieldsChanged"] for v in reverse.values())
    )
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"pass": result["pass"], "unmatched": len(unmatched),
                      "runtime": len(batch_files), "links": len(links)}))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
