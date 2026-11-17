#!/usr/bin/env python3
"""Reading-quiz exposure audit: which wrong options can the app really draw, in the pools it really builds.

Usage: python reading_exposure.py [--extra KANJI=reading,reading ...] [--scan-all] [--seeds N] K [K ...]      (uses N1_REPO / n1lib.REPO)

Extends reading_options.py (same port of KanjiReadingQuiz.question / ReadingOptions.mutations) with three things:

  * a wider inventory of attested-but-unlisted readings: KANJIDIC2 on / kun / name readings, the --extra readings (card text)
    AND every reading of every JMdict entry whose headword is the single kanji (for 嫌 that is 1587610: いや, や, イヤ; readings restricted to
    other kanji forms and search-only forms are skipped), minus the target's own readings and their voicing / long-vowel / small-tsu
    variants (those are already excluded by the app);
  * the pools the app builds: KanjiReadingViewModel.start passes content.inStack(stack), i.e. the WHOLE shipped content of the
    stack (not the learner's studied cards). The N1 stack is every card tagged jlpt-n1 .. jlpt-n5 (Stacks.includes), All is every
    card; JLPT stacks of other levels cannot contain an N1 card. One smaller pool exists: a "Practice more" session of the
    Starter stack that is too short is padded (KanjiReadingViewModel.pad, Padding.kt padCandidates) with started cards of OTHER
    stacks, N1 cards included, and each borrowed card is added to the Starter cards; its curated cards are then usually absent.
    That pool is analysed as "Starter practice session" = every starter card plus the borrowed target;
  * an exact reachability analysis instead of a candidate superset: every outcome of the curated step (each curated distractor
    card offers one random usable reading) is enumerated; the fallback tiers are consulted only for the slots the curated step
    leaves open, so a prompt whose three curated cards always fill all three wrong slots can never draw anything else.

For every prompt it prints the curated outcomes, the possible deficits, the number of drawable wrong options, and for every
attested-but-unlisted key that another card offers: whether the key can be drawn in the N1 stack pool and in the All pool
(a HIT, counted as a problem, when it can), in the Starter practice session pool (a PAD-HIT: reported, not counted as a problem), and for
a key that cannot be drawn anywhere: the "risk class" example (a pool that lacks the curated cards: unit-test sized or hypothetical
content subsets, never a shipped stack) and the Starter practice session that also borrows ONE card that offers the key. The reachable
sets are supersets where the real code is deterministic: the last fallback step adds the remaining readings of each other card in list
order, which the analysis treats as "any of them". With --seeds the ported question() is also
sampled in every pool and every sampled wrong option is checked against the exact reachable set. With --scan-all the same exact
analysis runs for every card and prompt of the content (N1, All and Starter pools), using the JMdict single-kanji inventory only.

KANJIDIC2 name-only readings (nanori) are not on or kun readings: reported as info, never as problems.
"""
import itertools
import random
import sys

import reading_options as ro
from n1lib import build_jmdict_cache, build_kanjidic_cache, load_cards

JLPT = {"jlpt-n%d" % n for n in range(1, 6)}


class PCard(ro.Card):
    def __init__(self, kanji, fm):
        super().__init__(kanji, fm)
        self.tags = fm.get("tags", [])


def pools_of(cards):
    """The pools the app builds for a card tagged jlpt-n1: the N1 stack (Stacks.includes: any jlpt-n1..n5 tag) and All."""
    return [("N1 stack", [c for c in cards if JLPT & set(c.tags)]), ("All stack", cards)]


STARTER_LABEL = "Starter practice session"


def starter_pool(starter, target):
    """Pool of a Starter-stack "Practice more" session that borrows `target`: the starter cards plus the borrowed card
    (a starter card is already in the pool; the pool of a borrowed card carries none of its other-stack curated cards)."""
    return starter if target in starter else starter + [target]


def jmdict_readings(kanji, jm):
    """Readings of JMdict entries that have the single kanji as a headword, except readings restricted to other kanji forms,
    search-only kanji forms and search-only kana forms (none of those attests a reading of the kanji)."""
    out = []
    for eid in jm["char_index"].get(kanji, []):
        e = jm["entries"][eid]
        forms = [k for k in e["k"] if k[0] == kanji and "search-only kanji form" not in k[2]]
        if not forms:
            continue
        for r in e["r"]:
            if r[2] and kanji not in r[2]:
                continue
            if "search-only kana form" in r[4]:
                continue
            out.append((r[0], eid))
    return out


def describe(eid, jm):
    """Short description of a JMdict entry for triage: id, usage flags of its first sense and its first glosses."""
    s = jm["entries"][eid]["s"][0]
    return "%s: %s%s" % (eid, ("[%s] " % ", ".join(s["misc"])) if s["misc"] else "", ", ".join(s["gloss"][:3]))


def inventory(target, kd, jm, extra):
    """Attested-but-unlisted readings of the target: key -> list of source labels."""
    excluded = ro.excluded_keys(target)
    att = {}
    d = kd.get(target.kanji, {})

    def add(raw, src):
        k = ro.key(raw)
        if k and k not in excluded:
            att.setdefault(k, [])
            if src not in att[k]:
                att[k].append(src)

    for v in d.get("on", []):
        add(v, "KANJIDIC2 on")
    for v in d.get("kun", []):
        add(v, "KANJIDIC2 kun")
    for v in d.get("nanori", []):
        add(v, "KANJIDIC2 name reading")
    for v in extra.get(target.kanji, []):
        add(v, "card text")
    for raw, eid in jmdict_readings(target.kanji, jm):
        add(raw, "JMdict %s" % eid)
    return att


def reach(target, kind, correct, pool, excluded, count=4):
    """Exact set of wrong options question() can draw for one prompt from `pool` (every outcome of the curated step enumerated)."""
    slots = count - 1
    by_kanji = {c.kanji: c for c in pool}
    others = [c for c in pool if c.kanji != target.kanji and c.usable(kind)]
    cur_cards, cur = [], []
    for d in target.distractors:
        c = by_kanji.get(d)
        if c is not None and c.kanji != target.kanji and c.usable(kind):
            cur_cards.append(d)
            cur.append(sorted({k for _, k in c.usable(kind)}))
    tiers = {}
    for c in others:
        k, t = ro.best_reading(c, kind, correct)
        if k not in excluded and k != correct:
            tiers.setdefault(t, {}).setdefault(k, set()).add(c.kanji)
    order = sorted(tiers, reverse=True)
    out = {"curated_cards": cur_cards, "outcomes": 0, "deficits": {}, "curated": set(), "fallback": {}}
    reached, deep = set(), False
    for combo in itertools.product(*cur):
        used, chosen = {correct}, []
        for k in combo:
            if len(chosen) < slots and k not in excluded and k not in used:
                used.add(k)
                chosen.append(k)
        out["outcomes"] += 1
        m = slots - len(chosen)
        out["deficits"][m] = out["deficits"].get(m, 0) + 1
        out["curated"].update(chosen)
        remaining = m
        for t in order:
            if remaining <= 0:
                break
            reached.add(t)
            remaining -= len(tiers[t]) - len(set(chosen) & tiers[t].keys())
        if remaining > 0:
            deep = True
    for t in reached:
        for k, cs in tiers[t].items():
            out["fallback"].setdefault(k, set()).update(cs)
    if deep:
        for c in others:
            for _, k in c.usable(kind):
                if k not in excluded and k != correct:
                    out["fallback"].setdefault(k, set()).add(c.kanji)
    out["reachable"] = out["curated"] | set(out["fallback"])
    return out


def deficit_text(res):
    keys = sorted(res["deficits"])
    if keys == [0]:
        return "the curated options fill all three wrong slots in every outcome, the fallback is never consulted"
    return "deficit %s: the fallback fills the open slots" % "/".join(str(k) for k in keys)


def main(argv):
    seeds, extra, scan_all, batch = 0, {}, False, []
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--seeds":
            seeds = int(args.pop(0))
        elif a == "--extra":
            k, _, v = args.pop(0).partition("=")
            extra[k] = [x for x in v.split(",") if x]
        elif a == "--scan-all":
            scan_all = True
        else:
            batch.append(a)
    kc, _ = load_cards()
    cards = [PCard(k, fm) for k, (fm, _) in kc.items() if fm]
    by_kanji = {c.kanji: c for c in cards}
    pools = pools_of(cards)
    pool_maps = {name: {c.kanji: c for c in pool} for name, pool in pools}
    starter = [c for c in cards if "starter" in c.tags]
    kd = build_kanjidic_cache()["chars"]
    jm = build_jmdict_cache()
    offered = {}
    for name, pool in pools:
        offered[name] = {kind: {} for kind in ro.KINDS}
        for c in pool:
            for kind in ro.KINDS:
                for _, k in c.usable(kind):
                    offered[name][kind].setdefault(k, set()).add(c.kanji)
    print("Reading-exposure audit: pools as built by the app (content.inStack): %s." % "; ".join(
        "%s = %d cards" % (name, len(pool)) for name, pool in pools))
    print("N1 stack = every card tagged jlpt-n1 .. jlpt-n5 (Stacks.includes); All = every card in kanji/. The pool is the whole shipped content of the stack.")
    print("%s = the %d cards tagged starter plus the borrowed target (the Starter stack borrows started cards of other stacks to pad a short \"Practice more\" session; the All and JLPT stacks borrow nothing)." % (STARTER_LABEL, len(starter)))
    problems = latent = padded = 0
    for ch in batch:
        t = by_kanji.get(ch)
        if t is None:
            print("missing card", ch)
            return 2
        excluded = ro.excluded_keys(t)
        att = inventory(t, kd, jm, extra)
        name_only = {k for k, srcs in att.items() if srcs == ["KANJIDIC2 name reading"]}
        spool = starter_pool(starter, t)
        card_pools = pools + [(STARTER_LABEL, spool)]
        card_maps = dict(pool_maps, **{STARTER_LABEL: {c.kanji: c for c in spool}})
        print("\n== %s (%s)   curated option cards: %s   tags: %s" % (ch, t.title, " ".join(t.distractors), " ".join(t.tags)))
        for d in t.distractors:
            dc = by_kanji.get(d)
            present = [name for name, _ in card_pools if d in card_maps[name]]
            print("   curated %s: tags %s; in pools: %s; on %s | kun %s" % (
                d, " ".join(dc.tags) if dc else "-", ", ".join(present) or "none",
                " ".join(r for r, _ in dc.usable("on")) or "-" if dc else "-", " ".join(r for r, _ in dc.usable("kun")) or "-" if dc else "-"))
        print("   JMdict single-kanji entries: %s" % ("; ".join(
            "%s -> %s" % (describe(eid, jm), "・".join(r for r, e2 in jmdict_readings(ch, jm) if e2 == eid)) for eid in sorted({e for _, e in jmdict_readings(ch, jm)})) or "none"))
        print("   unlisted readings attested for %s: %s" % (ch, "  ".join("%s (%s)" % (k, ", ".join(s)) for k, s in att.items()) or "none"))
        for kind in ro.KINDS:
            prompts = t.quiz_readings(kind)
            if not prompts:
                print("   %s: no reading prompts" % kind)
            for raw in prompts:
                correct = ro.key(raw)
                print("   %s prompt %s (key %s)" % (kind, raw, correct))
                results = {name: reach(t, kind, correct, pool, excluded) for name, pool in card_pools}
                first = results[card_pools[0][0]]
                same = all(results[n]["reachable"] == first["reachable"] and results[n]["deficits"] == first["deficits"] for n, _ in card_pools)
                for name, _ in card_pools:
                    if same and name != card_pools[0][0]:
                        print("       %s: identical to %s" % (name, card_pools[0][0]))
                        continue
                    r = results[name]
                    print("       %s: curated %s -> %d outcomes; %s; %d drawable wrong options (%d curated, %d fallback)" % (
                        name, " ".join(r["curated_cards"]) or "none", r["outcomes"], deficit_text(r), len(r["reachable"]),
                        len(r["curated"]), len(set(r["fallback"]) - r["curated"])))
                for k, srcs in att.items():
                    if k == correct or k not in offered["All stack"][kind]:
                        continue
                    holders = sorted(offered["All stack"][kind][k])
                    shown = " ".join(holders[:8]) + (" (+%d more)" % (len(holders) - 8) if len(holders) > 8 else "")
                    drawn = [name for name, _ in card_pools if k in results[name]["reachable"]]
                    if drawn and k in name_only:
                        print("       info: %s (%s) is a KANJIDIC2 name-only reading offered by %s; can be drawn in: %s" % (k, ", ".join(srcs), shown, ", ".join(drawn)))
                        continue
                    if [n for n in drawn if n != STARTER_LABEL]:
                        problems += 1
                        print("       HIT: attested reading %s (%s) can be drawn as a wrong option in: %s; offered by %s" % (k, ", ".join(srcs), ", ".join(drawn), shown))
                        continue
                    if drawn:
                        padded += 1
                        print("       PAD-HIT: attested reading %s (%s) can be drawn as a wrong option only in a %s (the target borrowed to pad a short Starter \"Practice more\" session); offered by %s" % (
                            k, ", ".join(srcs), STARTER_LABEL, shown))
                        continue
                    latent += 1
                    print("       attested reading %s (%s) is offered by %s; it cannot be drawn in the N1 stack, All stack or Starter practice session pool" % (k, ", ".join(srcs), shown))
                    ex = []
                    for h in holders:
                        small = reach(t, kind, correct, [t, by_kanji[h]], excluded)
                        if k in small["reachable"]:
                            ex.append("[%s %s] -> %s" % (t.kanji, h, " ".join(sorted(small["reachable"]))))
                        if len(ex) == 2:
                            break
                    print("       risk class (a smaller pool without the curated cards, e.g. unit-test sized or hypothetical content; not a pool the app builds from the shipped stacks): %s" % ("; ".join(ex) or "none found"))
                    co = []
                    for h in holders:
                        hc = by_kanji[h]
                        if hc not in starter and k in reach(t, kind, correct, starter_pool(starter, t) + [hc], excluded)["reachable"]:
                            co.append(h)
                    print("       %s that also borrows one holder card (the pool grows by that card): %s" % (STARTER_LABEL, (
                        "drawable with %d of %d holders: %s" % (len(co), len(holders), " ".join(co[:8]) + (" ..." if len(co) > 8 else ""))) if co
                        else "not drawable with any single holder (%d holders tried)" % len(holders)))
                if seeds:
                    for name, pool in card_pools:
                        r = results[name]
                        seen = set()
                        for seed in range(seeds):
                            for k in ro.question(t, kind, pool, card_maps[name], random.Random(seed), correct, excluded):
                                seen.add(k)
                                if k not in r["reachable"]:
                                    problems += 1
                                    print("       PROBLEM: sampled wrong option %s is outside the exact reachable set (%s, seed %d)" % (k, name, seed))
                        print("       sampling %s: %d seeds, %d of %d drawable wrong options seen" % (name, seeds, len(seen), len(r["reachable"])))
    print("\n%d production hit(s) (N1 / All stack pools); %d padded-session hit(s) (Starter practice session only); %d latent collision(s) (attested reading offered by another card, not drawable in any of these pools)" % (problems, padded, latent))
    if scan_all:
        hits, collisions, prompts_n, total_other = [], 0, 0, 0
        for c in cards:
            excluded = ro.excluded_keys(c)
            att = {}
            for raw, eid in jmdict_readings(c.kanji, jm):
                k = ro.key(raw)
                if k and k not in excluded:
                    att.setdefault(k, set()).add(eid)
            if not att:
                continue
            total_other += 1
            for kind in ro.KINDS:
                for raw in c.quiz_readings(kind):
                    correct = ro.key(raw)
                    prompts_n += 1
                    scan_pools = pools + [("Starter stack" if c in starter else STARTER_LABEL, starter_pool(starter, c))]
                    for name, pool in scan_pools:
                        r = reach(c, kind, correct, pool, excluded)
                        for k in att:
                            if k != correct and k in r["reachable"]:
                                hits.append((c.kanji, kind, raw, name, k, sorted(att[k])))
                    for k in att:
                        if k != correct and k in offered["All stack"][kind]:
                            collisions += 1
        prod = [h for h in hits if h[3] != STARTER_LABEL]
        pad = [h for h in hits if h[3] == STARTER_LABEL]
        print("\nScan of every card: %d cards have JMdict single-kanji readings beyond their own; %d prompts checked in the N1, All and Starter pools; %d attested-reading/other-card collisions by kind; %d hit(s) in whole-stack pools (N1, All, Starter stack); %d hit(s) only in a Starter practice session that borrows the card." % (
            total_other, prompts_n, collisions, len(prod), len(pad)))
        for h in prod + pad:
            print("   %s %s %s prompt %s in %s: %s (JMdict %s)" % ("HIT" if h in prod else "PAD-HIT", h[0], h[1], h[2], h[3], h[4], "; ".join(describe(e, jm) for e in h[5])))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
