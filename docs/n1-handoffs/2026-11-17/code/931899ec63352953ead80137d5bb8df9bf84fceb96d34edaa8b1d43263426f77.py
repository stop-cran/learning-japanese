#!/usr/bin/env python3
"""Cross-check of the real KanjiReadingQuiz (Kotlin, ScratchReadingExposureTest) against the exact reachability analysis.

Usage: python reading_exposure_crosscheck.py [--extra KANJI=reading,reading ...] KOTLIN_OUTPUT [KOTLIN_OUTPUT ...]      (uses N1_REPO / n1lib.REPO)

Each KOTLIN_OUTPUT is a file the scratch test wrote (POOLS / TARGET / EXCLUDED / PROMPT / SMALL lines). Pools are matched by name, so a run
that sampled only the "Starter practice session" pool can be checked together with a run of the N1 / All stack pools. For every sampled
prompt it checks that the pool sizes and excluded keys match the Python port, that the real code never returned a missing or ambiguous
question, that every wrong option it drew lies inside the exact reachable set of reading_exposure.reach (a PROBLEM otherwise), which
reachable options it never drew (a NOTE: low probability or a port difference), and which attested but unlisted readings
(reading_exposure.inventory) it drew at all: a HIT, counted as a problem, in the N1 / All stack pools; a PAD-HIT, reported, in the
Starter practice session pool (a short Starter "Practice more" session padded with the target); reported as the risk class for the
small pools; KANJIDIC2 name-only readings are reported as info. Exit code 1 on any problem or HIT.
"""
import sys

import reading_exposure as rx
import reading_options as ro
from n1lib import build_jmdict_cache, build_kanjidic_cache, load_cards


def parse_wrong(text):
    out = {}
    for part in text.split():
        k, _, n = part.rpartition(":")
        out[k] = int(n)
    return out


def main(argv):
    extra, paths = {}, []
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--extra":
            k, _, v = args.pop(0).partition("=")
            extra[k] = [x for x in v.split(",") if x]
        else:
            paths.append(a)
    kc, _ = load_cards()
    cards = [rx.PCard(k, fm) for k, (fm, _) in kc.items() if fm]
    by_kanji = {c.kanji: c for c in cards}
    pools = dict(rx.pools_of(cards))
    starter = [c for c in cards if "starter" in c.tags]
    sizes = {name: len(pool) for name, pool in pools.items()}
    sizes[rx.STARTER_LABEL] = len(starter)
    kd = build_kanjidic_cache()["chars"]
    jm = build_jmdict_cache()
    problems = hits = pad_hits = prompts = starter_prompts = small = notes = 0
    for path in paths:
        print("== %s" % path)
        for ln in (x.rstrip("\r\n") for x in open(path, encoding="utf-8")):
            f = ln.split("|")
            if f[0] == "POOLS":
                kotlin = {p.split("=")[0]: int(p.split("=")[1]) for p in f[1:]}
                total = kotlin.pop("cards")
                python = {name: sizes.get(name) for name in kotlin}
                ok = kotlin == python and total == len(cards)
                print("pools: Kotlin %s of %d cards; Python %s of %d cards -> %s" % (kotlin, total, python, len(cards), "match" if ok else "MISMATCH"))
                problems += 0 if ok else 1
            elif f[0] == "EXCLUDED":
                t = by_kanji[f[1]]
                if sorted(ro.excluded_keys(t)) != sorted(f[2].split()):
                    problems += 1
                    print("PROBLEM: excluded keys of %s differ: Kotlin %s; Python %s" % (f[1], f[2], " ".join(sorted(ro.excluded_keys(t)))))
            elif f[0] in ("PROMPT", "SMALL"):
                small_case = f[0] == "SMALL"
                label, ch, kind, reading = f[1], f[2], f[3].lower(), f[4]
                meta = dict(x.split("=", 1) for x in f[5:9])
                wrong = parse_wrong(f[9].split("=", 1)[1])
                t = by_kanji[ch]
                excluded = ro.excluded_keys(t)
                if small_case:
                    pool = [t, by_kanji[label.split("+")[1]]]
                elif label == rx.STARTER_LABEL:
                    pool = rx.starter_pool(starter, t)
                else:
                    pool = pools[label]
                exact = rx.reach(t, kind, reading, pool, excluded)["reachable"]
                att = rx.inventory(t, kd, jm, extra)
                name_only = {k for k, srcs in att.items() if srcs == ["KANJIDIC2 name reading"]}
                if small_case:
                    small += 1
                elif label == rx.STARTER_LABEL:
                    starter_prompts += 1
                else:
                    prompts += 1
                outside = sorted(set(wrong) - exact)
                undrawn = sorted(exact - set(wrong))
                drawn_att = sorted(k for k in wrong if k in att and k not in name_only)
                drawn_name = sorted(k for k in wrong if k in name_only)
                note = []
                if meta["null"] != "0" and not small_case:
                    note.append("null questions: %s" % meta["null"])
                if meta["badCorrect"] != "0":
                    note.append("ambiguous or wrong correct option in %s questions" % meta["badCorrect"])
                if outside:
                    note.append("wrong options outside the exact reachable set: %s" % " ".join(outside))
                if note:
                    problems += 1
                tag = ""
                if drawn_att and not small_case:
                    if label == rx.STARTER_LABEL:
                        pad_hits += 1
                        tag = "PAD-HIT"
                    else:
                        hits += 1
                        tag = "HIT"
                if undrawn:
                    notes += 1
                print("%s %s %s %s %s: %s seeds, sizes %s, %d of %d reachable wrong options drawn%s%s%s%s%s" % (
                    f[0].lower(), label, ch, kind, reading, meta["seeds"].replace("seeds=", ""), meta["sizes"].replace("sizes=", ""),
                    len(wrong), len(exact),
                    ("; %s attested drawn: " % (tag or "risk class") + ", ".join("%s x%d (%s)" % (k, wrong[k], "/".join(att[k])) for k in drawn_att)) if drawn_att else "",
                    ("; name-only drawn (info): " + ", ".join("%s x%d" % (k, wrong[k]) for k in drawn_name)) if drawn_name else "",
                    ("; NOTE reachable but never drawn: " + " ".join(undrawn)) if undrawn else "",
                    ("; PROBLEM: " + "; ".join(note)) if note else "",
                    ""))
    print("\n%d whole-stack-pool prompts, %d Starter-session prompts and %d small-pool prompts checked; %d problem(s); %d whole-stack prompt(s) drew an attested unlisted reading (HIT); %d Starter-session prompt(s) drew one (PAD-HIT); %d prompt(s) with reachable options never drawn (NOTE)" % (
        prompts, starter_prompts, small, problems, hits, pad_hits, notes))
    return 1 if (problems or hits) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
