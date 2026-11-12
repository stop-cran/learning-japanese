#!/usr/bin/env python3
"""Reading-quiz option audit for a batch of kanji cards.

Usage: python reading_options.py [--seeds N] [--extra KANJI=reading,reading ...] K [K ...]      (uses N1_REPO / n1lib.REPO)

A port of KanjiReadingQuiz.question and ReadingOptions.mutations of the Android app (core/.../reading/KanjiReadings.kt and
core/.../words/Words.kt). For every reading prompt of the batch (target x kind x quiz reading) it prints

  * the excluded keys: every on and kun reading of the target plus the voicing / long-vowel / small-tsu variants of each;
  * the curated slots: each distractor card offers ONE random usable reading of the asked kind, skipped when excluded;
  * the fallback tiers: when a curated slot is skipped, the app fills it from the other cards (each card offers its reading
    closest to the answer, highest closeness first, ties random); the tiers that can supply the missing options are listed;
  * the unlisted-reading check: readings the dictionaries or the card text attest for the target but the card metadata does
    not list (KANJIDIC2 on / kun / name readings and the --extra readings) are looked up among EVERY reading that any other
    card can offer for the asked kind, so a hit would be a way for a valid reading to appear as a wrong option; KANJIDIC2
    name-only readings (nanori) are not on or kun readings, so they are reported as "info" and are not counted as problems;
  * a seeded simulation of the port: four options, one answer, no excluded wrong option, every wrong option inside the
    curated or fallback candidates.

The pool of other cards is every card in kanji/ (the largest possible pool; the app offers only the cards of the studied stack).
Options are random, so only candidate sets are listed, not a single outcome; the seeded generator is Python's, not Kotlin's.
"""
import random
import sys

from n1lib import build_kanjidic_cache, load_cards

VOICING = {
    "か": "が", "き": "ぎ", "く": "ぐ", "け": "げ", "こ": "ご", "さ": "ざ", "し": "じ", "す": "ず", "せ": "ぜ", "そ": "ぞ",
    "た": "だ", "ち": "じ", "つ": "ず", "て": "で", "と": "ど", "は": "ばぱ", "ひ": "びぴ", "ふ": "ぶぷ", "へ": "べぺ", "ほ": "ぼぽ",
    "が": "か", "ぎ": "き", "ぐ": "く", "げ": "け", "ご": "こ", "ざ": "さ", "じ": "し", "ず": "す", "ぜ": "せ", "ぞ": "そ",
    "だ": "た", "で": "て", "ど": "と", "ば": "は", "び": "ひ", "ぶ": "ふ", "べ": "へ", "ぼ": "ほ",
    "ぱ": "は", "ぴ": "ひ", "ぷ": "ふ", "ぺ": "へ", "ぽ": "ほ",
}
LONG_O = "おこそとのほもよろごぞどぼぽょ"
LONG_U = "ゅくすつぬふむゆるぐずぶぷ"
DOUBLING_NEXT = "かきくけこさしすせそたちつてとぱぴぷぺぽ"
MAX_PER_KIND = 3
KINDS = ("on", "kun")


def fold(s):
    return "".join(chr(ord(c) - 0x60) if "\u30a1" <= c <= "\u30f6" else c for c in s)


def key(raw):
    return "".join(c for c in fold(raw) if c not in ".-・" and not c.isspace())


def stem(raw):
    return key(raw.split(".")[0])


def mutations(reading):
    out = {}
    last = len(reading) - 1
    for i, c in enumerate(reading):
        for r in VOICING.get(c, ""):
            out[reading[:i] + r + reading[i + 1:]] = 1
        if c == "っ":
            out[reading[:i] + reading[i + 1:]] = 1
        elif 0 < i < last and reading[i - 1] != "っ" and c in DOUBLING_NEXT:
            out[reading[:i] + "っ" + reading[i:]] = 1
        if c == "う" and i > 0 and (reading[i - 1] in LONG_O or reading[i - 1] in LONG_U):
            out[reading[:i] + reading[i + 1:]] = 1
        elif c in LONG_O and (i == last or reading[i + 1] != "う"):
            out[reading[:i + 1] + "う" + reading[i + 1:]] = 1
    out.pop(reading, None)
    return [x for x in out if len(x) >= 2]


class Card:
    def __init__(self, kanji, fm):
        self.kanji = kanji
        self.title = fm.get("title", "")
        self.on = fm.get("onyomi", [])
        self.kun = fm.get("kunyomi", [])
        self.ask_lists = {"on": fm.get("quizOnyomi", self.on), "kun": fm.get("quizKunyomi", self.kun)}
        self.distractors = fm.get("distractors", [])
        self._usable = {k: [(r, key(r)) for r in self.ask_lists[k] if key(r)] for k in KINDS}

    def usable(self, kind):
        return self._usable[kind]

    def quiz_readings(self, kind):
        seen, first = set(), []
        for raw, _ in self.usable(kind):
            s = stem(raw)
            if s not in seen:
                seen.add(s)
                first.append(raw)
        seen, second = set(), []
        for raw in first:
            k = key(raw)
            if k not in seen:
                seen.add(k)
                second.append(raw)
        return second[:MAX_PER_KIND]


def excluded_keys(target):
    out = set()
    for r in target.on + target.kun:
        k = key(r)
        out.add(k)
        out.update(mutations(k))
    return out


def closeness(k, correct):
    return (2 if abs(len(k) - len(correct)) <= 1 else 0) + (1 if k[-1] == correct[-1] else 0) + (1 if k[0] == correct[0] else 0)


def best_reading(card, kind, correct):
    best, best_c = None, -1
    for _, k in card.usable(kind):
        c = closeness(k, correct)
        if c > best_c:
            best, best_c = k, c
    return best, best_c


def question(target, kind, cards, by_kanji, rng, correct, excluded, count=4):
    used = {correct}
    chosen = []

    def add(k):
        if len(chosen) < count - 1 and k and k not in excluded and k not in used:
            used.add(k)
            chosen.append(k)

    others = [c for c in cards if c.kanji != target.kanji and c.usable(kind)]
    for d in target.distractors:
        c = by_kanji.get(d)
        if c is not None and c.kanji != target.kanji and c.usable(kind):
            add(rng.choice(c.usable(kind))[1])
    shuffled = others[:]
    rng.shuffle(shuffled)
    best = [best_reading(c, kind, correct) for c in shuffled]
    best.sort(key=lambda b: -b[1])
    for k, _ in best:
        add(k)
    shuffled = others[:]
    rng.shuffle(shuffled)
    for c in shuffled:
        if len(chosen) >= count - 1:
            break
        for _, k in c.usable(kind):
            add(k)
    return chosen


def analyse(target, kind, correct, cards, by_kanji, excluded):
    curated = []
    for d in target.distractors:
        c = by_kanji.get(d)
        curated.append((d, [(k, k in excluded or k == correct) for _, k in c.usable(kind)] if c else []))
    curated_ok = {k for _, ks in curated for k, bad in ks if not bad}
    tiers = {}
    for c in cards:
        if c.kanji == target.kanji or not c.usable(kind):
            continue
        k, t = best_reading(c, kind, correct)
        if k in excluded or k == correct:
            continue
        tiers.setdefault(t, {}).setdefault(k, []).append(c.kanji)
    # Three distinct keys from the highest tiers are always enough: curated picks that repeat a tier key are skipped as used.
    need = 3
    pool, count = [], 0
    for t in sorted(tiers, reverse=True):
        pool.append((t, tiers[t]))
        count += len(tiers[t])
        if count >= need:
            break
    return curated, curated_ok, tiers, pool


def main(argv):
    seeds, extra = 100, {}
    args = list(argv)
    batch = []
    while args:
        a = args.pop(0)
        if a == "--seeds":
            seeds = int(args.pop(0))
        elif a == "--extra":
            k, _, v = args.pop(0).partition("=")
            extra[k] = [x for x in v.split(",") if x]
        else:
            batch.append(a)
    kc, _ = load_cards()
    kd = build_kanjidic_cache()["chars"]
    cards = [Card(k, fm) for k, (fm, _) in kc.items() if fm]
    by_kanji = {c.kanji: c for c in cards}
    offered = {kind: {} for kind in KINDS}
    for c in cards:
        for kind in KINDS:
            for _, k in c.usable(kind):
                offered[kind].setdefault(k, set()).add(c.kanji)
    print("Reading-option audit: %d cards in the pool (every card in kanji/); %d seeds per prompt." % (len(cards), seeds))
    problems = 0
    for ch in batch:
        t = by_kanji.get(ch)
        if t is None:
            print("missing card", ch)
            return 2
        excluded = excluded_keys(t)
        d = kd.get(ch, {})
        attested = {}
        for kind_name, vals in (("KANJIDIC2 on", d.get("on", [])), ("KANJIDIC2 kun", d.get("kun", [])),
                                ("card text", extra.get(ch, [])), ("KANJIDIC2 name reading", d.get("nanori", []))):
            for v in vals:
                k = key(v)
                if k and k not in excluded:
                    attested.setdefault(k, kind_name)
        name_only = {k for k, w in attested.items() if w == "KANJIDIC2 name reading"}
        print("\n== %s (%s)   curated option cards: %s" % (ch, t.title, " ".join(t.distractors)))
        print("   metadata readings: on %s | kun %s" % (" ".join(t.on) or "-", " ".join(t.kun) or "-"))
        print("   unlisted readings attested for %s: %s" % (ch, "  ".join("%s (%s)" % (k, w) for k, w in attested.items()) or "none"))
        for kind in KINDS:
            prompts = t.quiz_readings(kind)
            if not prompts:
                print("   %s: no reading prompts" % kind)
            for raw in prompts:
                correct = key(raw)
                curated, curated_ok, tiers, pool = analyse(t, kind, correct, cards, by_kanji, excluded)
                print("   %s prompt %s (key %s)" % (kind, raw, correct))
                print("       excluded keys: %d" % len(excluded))
                for dc, ks in curated:
                    if not ks:
                        print("       curated %s: no usable %s reading, slot filled from the fallback" % (dc, kind))
                    else:
                        print("       curated %s: %s" % (dc, " ".join("%s%s" % (k, "(skipped: excluded)" if bad else "") for k, bad in ks)))
                print("       fallback tiers (distinct best readings of the other cards; closeness 4 = length within 1 and same first and last kana): %s" % (
                    ", ".join("%d: %d keys" % (tt, len(tiers[tt])) for tt in sorted(tiers, reverse=True))))
                for tt, ks in pool:
                    names = sorted(ks)
                    shown = " ".join(names[:40]) + (" ... (+%d more)" % (len(names) - 40) if len(names) > 40 else "")
                    print("       tier %d candidates (%d): %s" % (tt, len(names), shown))
                allowed = set(curated_ok)
                for _, ks in pool:
                    allowed.update(ks)
                hits = {k: sorted(offered[kind].get(k, ())) for k in attested if k != correct and k in offered[kind]}
                if not hits:
                    print("       unlisted-reading check: none of the %d unlisted readings is offered by any of the %d other %s-reading cards" % (
                        len(attested), len(offered[kind]), kind))
                for k, cs in hits.items():
                    if k in allowed and k in name_only:
                        print("       info (can be drawn): %s is a KANJIDIC2 name-only reading, not an on or kun reading; offered by card(s) %s" % (
                            k, " ".join(cs)))
                    elif k in allowed:
                        problems += 1
                        print("       HIT (can be drawn): unlisted reading %s (%s) is offered by card(s) %s" % (k, attested[k], " ".join(cs)))
                    else:
                        print("       note (cannot be drawn from the full pool; lower closeness tier): unlisted reading %s (%s) is offered only by card(s) %s" % (
                            k, attested[k], " ".join(cs)))
                short, seen, name_seeds = 0, set(), 0
                for seed in range(seeds):
                    wrong = question(t, kind, cards, by_kanji, random.Random(seed), correct, excluded)
                    if len(wrong) < 3:
                        short += 1
                    if any(k in name_only for k in wrong):
                        name_seeds += 1
                    for k in wrong:
                        seen.add(k)
                        if k in name_only and k not in excluded and k != correct:
                            continue
                        if k in excluded or k == correct or k in attested or k not in allowed:
                            problems += 1
                            print("       PROBLEM: wrong option %s (seed %d)" % (k, seed))
                    if len(set(wrong)) != len(wrong):
                        problems += 1
                        print("       PROBLEM: duplicate wrong options (seed %d)" % seed)
                if short:
                    problems += 1
                print("       simulation: %d wrong options seen over %d seeds; %d seeds with fewer than three wrong options" % (len(seen), seeds, short))
                if name_seeds:
                    print("       info: a name-only reading was among the wrong options in %d of %d seeds" % (name_seeds, seeds))
    print("\n%d problem(s)" % problems)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
