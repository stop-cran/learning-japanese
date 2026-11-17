#!/usr/bin/env python3
"""Quiz-safety and consistency checks for a freshly authored batch of kanji cards.

Usage: python quiz_safety.py K [K ...]      (uses N1_REPO / n1lib.REPO)

Simulates the Android "guess the meaning" option builder (curated distractors, symmetric quiz_exclusions) and the reading
quiz (wrong readings from distractors, filtered against the target's readings), and checks titles, tags/grades, quiz readings
linked to existing word articles, and that every distractor/exclusion is explained in the card's Notes.
"""
import re
import sys

from n1lib import REPO, build_kanjidic_cache, hira, load_cards, parse, read, reading_variants, rel_links, sections

STOP = {"to", "of", "a", "the", "up", "out", "off", "in", "on", "an", "and", "or", "for", "with", "one", "ones", "put"}


def key(raw):
    return hira(raw).replace(".", "").replace("-", "")


def toks(title):
    return {t for t in re.split(r"[;,\s()/]+", title.lower()) if t and t not in STOP}


def main(batch):
    kc, wc = load_cards()
    kd = build_kanjidic_cache()["chars"]
    errs, warns = [], []

    def err(m):
        errs.append(m)

    def warn(m):
        warns.append(m)

    missing = [c for c in batch if c not in kc]
    if missing:
        print("missing cards:", missing)
        return 2

    def fm_of(c):
        return kc[c][0]

    def excluded(a, b):
        return b in fm_of(a).get("quiz_exclusions", []) or a in fm_of(b).get("quiz_exclusions", [])

    titles = {}
    for c, (fm, _) in kc.items():
        titles.setdefault((fm or {}).get("title", "").strip().lower(), []).append(c)
    for t, cs in titles.items():
        if len(cs) > 1 and any(c in batch for c in cs):
            err("duplicate title %r: %s" % (t, cs))

    for ch in batch:
        fm, body = kc[ch]
        dis, exs = fm.get("distractors", []), fm.get("quiz_exclusions", [])
        label = "%s (%s)" % (ch, fm["title"])
        if len(dis) != 3 or len(set(dis)) != 3:
            err("%s: expected 3 distinct distractors, got %s" % (label, dis))
        for d in dis:
            if d not in kc:
                err("%s: distractor %s has no card" % (label, d))
            if d == ch:
                err("%s: distractor is itself" % label)
        for e in exs:
            if e not in kc:
                err("%s: exclusion %s has no card" % (label, e))
            if e == ch:
                err("%s: exclusion is itself" % label)
        if set(dis) & set(exs):
            err("%s: distractors overlap exclusions %s" % (label, sorted(set(dis) & set(exs))))
        group = [ch] + [d for d in dis if d in kc]
        for i, a in enumerate(group):
            for b in group[i + 1:]:
                if excluded(a, b):
                    err("%s: excluded pair %s-%s inside the option set %s" % (label, a, b, group))
        # exclusion pairs are one-sided by convention
        for e in exs:
            if e in kc and ch in fm_of(e).get("quiz_exclusions", []):
                warn("%s: exclusion %s is mirrored on both cards (convention: one side only)" % (label, e))
        # tags / grade
        tags = fm.get("tags", [])
        g = kd.get(ch, {}).get("grade")
        expect = "grade-%s" % g if g else None
        gtags = [t for t in tags if t.startswith("grade-")]
        if expect and gtags != [expect]:
            err("%s: grade tag %s but KANJIDIC grade is %s" % (label, gtags, g))
        if "jlpt-n1" not in tags or fm.get("jlpt") != "1":
            err("%s: not tagged jlpt-n1 / jlpt 1" % label)
        # quiz readings linked to existing words that declare the kanji
        sec = sections(body)
        rows = []
        for line in sec.get("Readings", "").split("\n"):
            s = line.strip()
            if s.startswith("|") and not re.match(r"^\|\s*:?-{3,}:?\s*\|", s):
                rows.append([c.strip() for c in s.strip("|").split("|")])
        rows = rows[1:] if rows and rows[0][0].lower() == "reading" else rows
        for qk in ("quizOnyomi", "quizKunyomi"):
            base = fm.get("onyomi" if qk == "quizOnyomi" else "kunyomi", [])
            for r in fm.get(qk, []):
                if r not in base:
                    err("%s: %s %s not in the card's readings" % (label, qk, r))
                row = [x for x in rows if x[0].strip(" *`") == r]
                ok = False
                for x in row:
                    for t in rel_links("|".join(x[2:])):
                        tp = (REPO / "kanji" / t).resolve()
                        if tp.parent.name == "words" and tp.is_file() and ch in (wc.get(tp.stem, ({},))[0] or {}).get("kanji", []):
                            ok = True
                if not ok:
                    err("%s: selected reading %s has no linked word article declaring %s" % (label, r, ch))
        # every distractor/exclusion explained in the Notes
        notes = sec.get("Notes", "")
        for d in dis:
            if d not in notes:
                err("%s: distractor %s is not mentioned in Notes" % (label, d))
        for e in exs:
            if e not in notes:
                warn("%s: exclusion %s is not mentioned in Notes" % (label, e))
        # at least one linked word article that declares the kanji
        linked = [t for t in rel_links(body) if t.startswith("../words/")]
        if not linked:
            err("%s: no linked word article" % label)

        # informational view of the two quizzes
        dtitles = [kc[d][0]["title"] for d in dis if d in kc]
        shared = []
        pool = [toks(fm["title"])] + [toks(t) for t in dtitles]
        for i in range(len(pool)):
            for j in range(i + 1, len(pool)):
                if pool[i] & pool[j]:
                    shared.append((i, j, sorted(pool[i] & pool[j])))
        print("%s  options: %s" % (label, " | ".join(dtitles)))
        if shared:
            warn("%s: shared title words among options %s" % (label, shared))
        excl_all = set()
        for r in fm.get("onyomi", []) + fm.get("kunyomi", []):
            k = key(r)
            excl_all.add(k)
            for v in reading_variants(k):
                excl_all.add(v)
        for kind, qk in (("on", "quizOnyomi"), ("kun", "quizKunyomi")):
            for r in fm.get(qk, []):
                usable = 0
                for d in dis:
                    if d not in kc:
                        continue
                    dfm = kc[d][0]
                    ask = dfm.get(qk, dfm.get("onyomi" if kind == "on" else "kunyomi", []))
                    if any(key(x) and key(x) not in excl_all for x in ask):
                        usable += 1
                print("    reading %-6s (%s): wrong options from distractors %d/3 (rest filled from other cards)" % (r, kind, usable))

    # existing cards whose curated options do not fill all three slots can draw fallback options by shared tags
    newset = set(batch)
    prone = []
    for c, (fm, _) in kc.items():
        if c in newset or not fm:
            continue
        chosen, used = [], {fm.get("title")}
        for d in fm.get("distractors", []):
            if d not in kc or d == c or len(chosen) >= 3:
                continue
            if excluded(c, d) or any(excluded(x, d) for x in chosen):
                continue
            t = kc[d][0].get("title")
            if t in used:
                continue
            used.add(t)
            chosen.append(d)
        if len(chosen) < 3:
            prone.append((c, fm.get("title"), len(chosen)))
    print("existing cards that fall back to tag-similar options: %d" % len(prone))
    for c, t, n in prone[:40]:
        print("    %s (%s) curated slots used %d/3" % (c, t, n))

    print("\n%d error(s), %d warning(s)" % (len(errs), len(warns)))
    for m in errs:
        print("ERROR", m)
    for m in warns:
        print("WARN ", m)
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(list(sys.argv[1:])))
