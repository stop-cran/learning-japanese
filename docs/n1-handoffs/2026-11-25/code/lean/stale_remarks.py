"""Find stale card-absence remarks: sentences in kanji/*.md and words/*.md that
say a kanji has no card ("has no card here", "does not have a kanji card here",
"has no card yet", ...) about a kanji whose card now exists.

For each absence phrase, the kanji the remark is about is taken as the last
kanji written outside a Markdown link before the phrase in the same sentence,
skipping the article's own kanji. A remark is STALE if that kanji has a card.
Remarks judged by a reviewer not to be about that kanji are passed as
--reviewed "path:line:kanji=reason" and listed as REVIEWED instead.
Remarks with no such kanji before the phrase cannot be checked; they are
listed as unresolved for a human reader and do not count as problems.

usage: python stale_remarks.py REPO [--reviewed PATH:LINE:K=REASON ...]
"""
import argparse
import re
import sys
from pathlib import Path

ABSENCE = re.compile(
    r"(no (kanji )?card|card yet|not yet (a |its own )?(kanji )?card|ha(s|ve) no (kanji )?card"
    r"|not have (a |its own )?(kanji )?card|n't have (a |its own )?(kanji )?card"
    r"|without (a|its own) (kanji )?card|no card of its own|lacks? (a |its own )?(kanji )?card"
    r"|(is|are)n't (yet )?(a )?card|(is|are) not (yet )?(a )?card"
    r"|not (yet )?(in|part of) (the|this) (collection|deck|app)|no kanji cards?)", re.I)
LINK = re.compile(r"\[[^\]]*\]\([^)]*\)")
CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0003134f]")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--reviewed", action="append", default=[])
    a = ap.parse_args()
    repo = Path(a.repo)
    cards = {p.stem for p in (repo / "kanji").glob("*.md") if len(p.stem) == 1}
    reviewed = {}
    for r in a.reviewed:
        key, reason = r.split("=", 1)
        reviewed[key] = reason
    stale, ok_reviewed, absent, unresolved = [], [], [], []
    files = sorted((repo / "kanji").glob("*.md")) + sorted((repo / "words").glob("*.md"))
    for f in files:
        rel = f.relative_to(repo).as_posix()
        own = f.stem if rel.startswith("kanji/") else ""
        for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if not ABSENCE.search(line):
                continue
            for sentence in re.split(r"(?<=[.!?。])\s+", line):
                bare = LINK.sub("", sentence)
                for m in ABSENCE.finditer(bare):
                    before = [c for c in CJK.findall(bare[:m.start()]) if c != own]
                    if not before:
                        unresolved.append((rel, n, sentence.strip()))
                        continue
                    k = before[-1]
                    entry = (rel, n, k, sentence.strip())
                    if k not in cards:
                        absent.append(entry)
                    elif f"{rel}:{n}:{k}" in reviewed:
                        ok_reviewed.append(entry + (reviewed[f"{rel}:{n}:{k}"],))
                    else:
                        stale.append(entry)
    unused = sorted(set(reviewed) - {f"{e[0]}:{e[1]}:{e[2]}" for e in ok_reviewed})
    print(f"Scanned {len(files)} articles ({len(cards)} kanji cards) for sentences saying a kanji has no card.")
    for rel, n, k, s in stale:
        print(f"STALE {rel}:{n} {k} has a card: {s}")
    for rel, n, k, s, why in ok_reviewed:
        print(f"REVIEWED {rel}:{n} {k}: {why} :: {s}")
    for key in unused:
        print(f"UNUSED REVIEW ENTRY {key}")
    print(f"remarks about kanji without a card: {len(absent)}")
    for rel, n, k, s in absent:
        print(f"  {rel}:{n} {k}")
    print(f"remarks with no kanji before the phrase (subject not resolved, not checked): {len(unresolved)}")
    for rel, n, s in unresolved:
        print(f"  {rel}:{n} :: {s}")
    problems = len(stale) + len(unused)
    print(f"stale: {len(stale)}; reviewed: {len(ok_reviewed)}; problems: {problems}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
