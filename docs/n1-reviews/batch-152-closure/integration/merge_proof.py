"""Mechanical proof for the B152 integration merge.

Usage: python -X utf8 merge_proof.py <repo-root> <merge-commit> <out.json>

Checks that every path in the merge tree, except the derived manifest.json,
is byte-identical to one of the two parents; that the B152 runtime files
(every non-docs path the batch changed from its published base) equal the
reviewed snapshot; and that no main-side change touches, is linked
from, or mentions the batch's kanji or word articles. Main-side blobs that
are not UTF-8 text (images, audio) are counted but not scanned.

"strictPass" applies the whole-file rules: no link target of a batch file
changed by main, and no main-changed file mentioning a batch kanji or word
anywhere. "pass" keeps every other strict rule but classifies those two:
a main-changed link target passes when every batch line linking it is
older than the batch and its front matter (title, readings, quiz fields)
is unchanged; a mention passes when it is not on a line main added.
"""
import json
import re
import subprocess
import sys
from pathlib import PurePosixPath

PUBLISHED_BASE = "d59c45576d5438036e317dfbbc3c353ea4fc74a6"
REVIEWED = "b81299f38d9d5184b94f7c05e6355ca7de085466"
KANJI = "趣跳踏躍較載輝輩迫逸遂遣避郡郷"
DERIVED = {"manifest.json"}


def git(root, *args):
    return subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=root, check=True, capture_output=True, text=True, encoding="utf-8",
    ).stdout


def show_text(root, spec):
    """Return the blob as text, or None when it is not UTF-8 (images, audio)."""
    raw = subprocess.run(
        ["git", "-c", "core.quotepath=false", "show", spec],
        cwd=root, check=True, capture_output=True,
    ).stdout
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return None


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


def added_lines(root, a, b, path):
    out = git(root, "diff", "-U0", a, b, "--", path)
    return [l[1:] for l in out.splitlines() if l.startswith("+") and not l.startswith("+++")]


def removed_lines(root, a, b, path):
    out = git(root, "diff", "-U0", a, b, "--", path)
    return [l[1:] for l in out.splitlines() if l.startswith("-") and not l.startswith("---")]


def front_matter(text):
    text = (text or "").replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else None


def main():
    root, merge, out = sys.argv[1:4]
    merge = git(root, "rev-parse", merge).strip()
    parents = git(root, "rev-list", "--parents", "-n", "1", merge).split()[1:]
    if len(parents) != 2:
        raise SystemExit("merge commit must have exactly two parents")
    ours, theirs = parents
    if ours != REVIEWED:
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
    binary = []
    for p in main_changed:
        if p in DERIVED or p not in m:
            continue
        text = show_text(root, f"{merge}:{p}")
        if text is None:
            binary.append(p)
            continue
        hits = sorted({c for c in text if c in KANJI}) + [w for w in words if w in text]
        if hits:
            mentions[p] = hits
    target_detail = {}
    for target in sorted(set(links) & set(main_changed)):
        linking = []
        for p in batch_files:
            if not p.endswith(".md"):
                continue
            text = git(root, "show", f"{merge}:{p}")
            if target not in card_links(text, p):
                continue
            batch_added = set(added_lines(root, PUBLISHED_BASE, REVIEWED, p))
            for n, line in enumerate(text.splitlines(), 1):
                line = line.rstrip("\r")
                if target in card_links(line, p):
                    linking.append({"file": p, "line": n, "addedByBatch": line in batch_added})
        target_detail[target] = {
            "linkingLines": linking,
            "frontMatterChangedByMain": front_matter(show_text(root, f"{base}:{target}"))
            != front_matter(show_text(root, f"{theirs}:{target}")),
            "mainRemovedLines": removed_lines(root, base, theirs, target),
            "mainAddedLines": added_lines(root, base, theirs, target),
        }
    added_mentions = {}
    for p in mentions:
        hits = set()
        for line in added_lines(root, base, theirs, p):
            hits |= {c for c in line if c in KANJI} | {w for w in words if w in line}
        if hits:
            added_mentions[p] = sorted(hits)
    manifest_files = set()
    for group in json.loads(git(root, "show", f"{merge}:manifest.json")).values():
        if isinstance(group, dict):
            manifest_files |= set(group)
    result = {
        "merge": merge,
        "parents": {"b152Reviewed": ours, "originMain": theirs},
        "mergeBase": base,
        "publishedBase": PUBLISHED_BASE,
        "pathsCompared": len(set(m) | set(o) | set(t)),
        "nonDerivedPathsMatchingNeitherParent": unmatched,
        "mainChangedPaths": main_changed,
        "b152RuntimePaths": len(batch_files),
        "mainChangedOverlapWithB152Runtime": sorted(set(main_changed) & set(batch_files)),
        "b152RuntimeFilesIdenticalToReviewed": all(v["identical"] for v in runtime.values()),
        "b152RuntimeFiles": runtime,
        "b152LinkTargets": len(links),
        "b152LinkTargetsChangedByMain": sorted(set(links) & set(main_changed)),
        "mainChangedBinaryPathsNotScanned": len(binary),
        "b152LinkTargetsChangedByMainDetail": target_detail,
        "mainChangedNonDerivedPathsMentioningB152KanjiOrWords": mentions,
        "mainAddedLinesMentioningB152KanjiOrWords": added_mentions,
        "manifestListsB152Files": all(p in manifest_files for p in batch_files),
    }
    hard = (
        not unmatched
        and not result["mainChangedOverlapWithB152Runtime"]
        and result["b152RuntimeFilesIdenticalToReviewed"]
        and result["manifestListsB152Files"]
    )
    result["strictPass"] = hard and not result["b152LinkTargetsChangedByMain"] and not mentions
    result["pass"] = (
        hard
        and all(
            not d["frontMatterChangedByMain"]
            and d["linkingLines"]
            and not any(l["addedByBatch"] for l in d["linkingLines"])
            for d in target_detail.values()
        )
        and not added_mentions
    )
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(json.dumps({"pass": result["pass"], "strictPass": result["strictPass"], "unmatched": len(unmatched),
                      "runtime": len(batch_files), "links": len(links)}))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
