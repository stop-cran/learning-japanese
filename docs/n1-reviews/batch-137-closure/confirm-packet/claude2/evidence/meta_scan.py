"""Find words named on a card whose JMdict entry id is missing from the card's Metadata line.

usage: python -X utf8 meta_scan.py REPO KANJI...

Scope: each maximal run of Japanese script (kanji, kana, 々, ー) in the card text, excluding the
front matter, the Metadata line and link targets, that has at least two characters, contains a
kanji and exactly equals a JMdict kanji spelling. Also reports every substring of such a run (at
least two characters, with a kanji) that equals a JMdict kanji spelling, marked "part of RUN".
Words written only in kana and single-kanji words are not checked.

Needs the author's helper module n1lib (its JMdict index of the pinned JMdict_e.gz), found in
the directory named by the N1_LEAN environment variable or next to this script. n1lib is not
included in the review packets.
"""
import os
import re
import sys

sys.path.insert(0, os.environ.get("N1_LEAN", os.path.dirname(os.path.abspath(__file__))))
import n1lib

D = n1lib.build_jmdict_cache()
E = D["entries"]
CI = D["char_index"]
JP = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff々ー]+")
KANJI = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff々]")


def entries_for(w):
    pool = set()
    for c in w:
        if KANJI.match(c) and c != "々":
            pool = set(CI.get(c, [])) if not pool else pool & set(CI.get(c, []))
    return sorted(eid for eid in pool if any(k[0] == w for k in E[eid]["k"]))


def scan(repo, kanji):
    text = open(os.path.join(repo, "kanji", kanji + ".md"), encoding="utf-8").read().split("\n")
    end = text.index("---", 1)
    meta = [i for i, l in enumerate(text) if l.startswith("Metadata:")]
    listed = set(re.findall(r"\b\d{7}\b", text[meta[0]])) if meta else set()
    out = []
    seen = set()
    for i, line in enumerate(text):
        if i <= end or i in meta:
            continue
        body = re.sub(r"\]\([^)]*\)", "]", line)
        for m in JP.finditer(body):
            run = m.group(0)
            for a in range(len(run)):
                for b in range(a + 2, len(run) + 1):
                    w = run[a:b]
                    if not KANJI.search(w) or (w, run) in seen:
                        continue
                    ids = entries_for(w)
                    if not ids:
                        continue
                    seen.add((w, run))
                    if not listed & set(ids):
                        part = "" if w == run else f" part of {run}"
                        out.append(f"{kanji}.md:{i + 1}: {w} {'/'.join(ids)} not listed{part}")
    return out


if __name__ == "__main__":
    repo = sys.argv[1]
    rows = []
    for k in sys.argv[2:]:
        rows += scan(repo, k)
    whole = [r for r in rows if " part of " not in r]
    print("\n".join(whole) if whole else "whole runs: none missing")
    print(f"-- whole-run gaps: {len(whole)}; part-of-run matches not listed: {len(rows) - len(whole)}")
    for r in rows:
        if " part of " in r:
            print("   " + r)
