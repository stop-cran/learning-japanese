# -*- coding: utf-8 -*-
"""Word-quiz option audit for new word articles (Python port of WordQuizBuilder.select and ReadingOptions.build).

usage: python word_quiz_audit.py REPO_ROOT WORD [WORD ...]

Pool: every word article in REPO_ROOT\\words (the app's "All" word stack); the reading-quiz pool keeps only words
whose written form has a reading to learn. For each listed word it prints:
  meaning quizzes (JpToEn and EnToJp share one option set): curated distractors, then the scored candidates
  (score = 2 per shared tag + 1 same type + 1 shared kanji); every candidate whose score reaches the last needed
  slot can be drawn (the "reachable tier"); ties are broken at random;
  reading quiz: the generated look-alike readings (two are drawn) and the top closeness tier for the third slot;
  any option that is also a JMdict reading of the target's written form is flagged ATTESTED.
Then the reverse direction: existing words whose meaning or reading quiz can draw one of the listed words.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\romanko\n1-kanji-workspace\lean")
import n1lib  # noqa: E402

ROOT = Path(sys.argv[1])
NEW = sys.argv[2:]
FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)


def front(path):
    m = FM.match(path.read_text(encoding="utf-8"))
    out = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        out[k.strip()] = [x.strip() for x in v[1:-1].split(",") if x.strip()] if v.startswith("[") and v.endswith("]") else v
    return out


W = {}
for p in sorted((ROOT / "words").glob("*.md")):
    f = front(p)
    W[f["word"]] = dict(word=f["word"], reading=f.get("reading", ""), title=f.get("title", ""), type=f.get("type") or None,
                        kanji=f.get("kanji", []) or [], tags=f.get("tags", []) or [], excl=f.get("quiz_exclusions", []) or [],
                        cur=f.get("quiz_distractors", []) or [])
for w in NEW:
    assert w in W, w

D = n1lib.build_jmdict_cache()
E, CI = D["entries"], D["char_index"]


def attested(word):
    """Every JMdict reading of the entries that list `word` as a written form (re_restr respected)."""
    out = set()
    cjk = [c for c in word if n1lib.CJK.match(c)]
    if not cjk:
        return out
    for eid in CI.get(cjk[0], []):
        e = E[eid]
        if any(k[0] == word for k in e["k"]):
            for r in e["r"]:
                if not r[3] and (not r[2] or word in r[2]):
                    out.add(r[0])
    return out


def excluded(a, b):
    return b["word"] in a["excl"] or a["word"] in b["excl"]


def score(t, c):
    return 2 * sum(1 for x in c["tags"] if x in t["tags"]) + (1 if c["type"] is not None and c["type"] == t["type"] else 0) + \
        (1 if any(k in t["kanji"] for k in c["kanji"]) else 0)


def meaning(t, count=4):
    """Curated options (at most count-2) and the scored candidates in descending score order."""
    cur = [W[x] for x in t["cur"] if x in W and x != t["word"] and not excluded(t, W[x])]
    over = len(cur) > count - 2  # more curated cards than slots: a random subset is shown
    cur = cur[: count - 2]
    missing = [x for x in t["cur"] if x not in W]
    need = count - 1 - len(cur)
    used_t, used_w = {t["title"]} | {c["title"] for c in cur}, {t["word"]} | {c["word"] for c in cur}
    cands = []
    for c in W.values():
        if c["word"] in used_w or c["title"] in used_t or excluded(t, c) or any(excluded(x, c) for x in cur):
            continue
        cands.append((score(t, c), c))
    cands.sort(key=lambda x: -x[0])
    thr = cands[need - 1][0] if 0 < need <= len(cands) else None
    return cur, over, missing, need, thr, cands


LONG_O = "おこそとのほもよろごぞどぼぽょ"
LONG_U = "ゅくすつぬふむゆるぐずぶぷ"
DOUBLING_NEXT = "かきくけこさしすせそたちつてとぱぴぷぺぽ"
VOICING = {**dict(zip("かきくけこさしすせそ", "がぎぐげござじずぜぞ")), 'た': "だ", 'ち': "じ", 'つ': "ず", 'て': "で", 'と': "ど",
           'は': "ばぱ", 'ひ': "びぴ", 'ふ': "ぶぷ", 'へ': "べぺ", 'ほ': "ぼぽ",
           **dict(zip("がぎぐげござじずぜぞだでどばびぶべぼ", "かきくけこさしすせそたてとはひふへほ")),
           **dict(zip("ぱぴぷぺぽ", "はひふへほ"))}


def mutations(r):
    out = []

    def add(x):
        if x not in out:
            out.append(x)
    for i, c in enumerate(r):
        for v in VOICING.get(c, ""):
            add(r[:i] + v + r[i + 1:])
        if c == "っ":
            add(r[:i] + r[i + 1:])
        elif 0 < i < len(r) - 1 and r[i - 1] != "っ" and c in DOUBLING_NEXT:
            add(r[:i] + "っ" + r[i:])
        if c == "う" and i > 0 and (r[i - 1] in LONG_O or r[i - 1] in LONG_U):
            add(r[:i] + r[i + 1:])
        elif c in LONG_O and (i == len(r) - 1 or r[i + 1] != "う"):
            add(r[:i + 1] + "う" + r[i + 1:])
    return [x for x in out if x != r and len(x) >= 2]


def has_reading(w):
    return bool(w["reading"]) and w["word"] != w["reading"] and any(n1lib.CJK.match(c) for c in w["word"])


def closeness(t, c):
    d = abs(len(c["reading"]) - len(t["reading"]))
    return (3 if any(k in t["kanji"] for k in c["kanji"]) else 0) + (2 if d <= 1 else 0) + \
        (1 if c["reading"][-1] == t["reading"][-1] else 0) + (1 if c["reading"][0] == t["reading"][0] else 0)


RPOOL = [w for w in W.values() if has_reading(w)]


def reading(t):
    gen = mutations(t["reading"])
    n_gen = min(2, len(gen))
    need = 3 - n_gen
    cands = sorted(((closeness(t, c), c) for c in RPOOL if c["word"] != t["word"] and c["reading"] != t["reading"]),
                   key=lambda x: -x[0])
    thr = cands[need - 1][0] if 0 < need <= len(cands) else None
    return gen, n_gen, need, thr, cands


def show(c):
    return "%s (%s) \"%s\"" % (c["word"], c["reading"], c["title"])


print("# Word-quiz option audit")
print("command: python word_quiz_audit.py <repo at the candidate> " + " ".join(NEW))
print("pool: %d word articles (the app's All word stack); reading-quiz pool: %d words with a reading to learn" % (len(W), len(RPOOL)))
print("JMdict: pinned %s (lean cache)" % n1lib.JMDICT_GZ.name)
print("Python port of WordQuizBuilder.select (meaning quizzes) and ReadingOptions.build (reading quiz) in evidence\\app-code\\Words.kt.")
print("A word in a tier that ties at the last needed slot is drawn at random; every listed tier member can appear.")
problems = 0
for w in NEW:
    t = W[w]
    print("\n## %s" % show(t))
    print("type=%s tags=[%s] kanji=[%s]" % (t["type"], ", ".join(t["tags"]), ", ".join(t["kanji"])))
    print("quiz_exclusions (%d): %s" % (len(t["excl"]), "; ".join("%s \"%s\"" % (x, W[x]["title"]) if x in W else x + " (NO ARTICLE)" for x in t["excl"]) or "none"))
    rev = sorted(c["word"] for c in W.values() if t["word"] in c["excl"])
    print("excluded from the other side: %s" % (", ".join(rev) or "none"))
    cur, over, missing, need, thr, cands = meaning(t)
    print("### meaning quizzes (JpToEn and EnToJp share one option set)")
    print("curated options: %s%s%s" % ("; ".join(show(c) for c in cur) or "none", " (random subset)" if over else " (always shown)" if cur else "",
                                      ("; curated ids without an article: " + ", ".join(missing)) if missing else ""))
    if need > 0 and thr is None:
        print("scored slots needed: %d; TOO FEW CANDIDATES" % need)
        problems += 1
    elif need > 0:
        sure = [c for s, c in cands if s > thr]
        tie = [c for s, c in cands if s == thr]
        print("scored slots needed: %d; last-slot score %d; %d candidates above it, %d tie at it" % (need, thr, len(sure), len(tie)))
        for s, c in cands:
            if s < thr:
                break
            print("  %d  %s  shared tags=[%s]" % (s, show(c), ", ".join(x for x in c["tags"] if x in t["tags"])))
    att = attested(t["word"])
    print("### reading quiz")
    print("JMdict readings of the written form %s: %s" % (t["word"], ", ".join(sorted(att)) or "none"))
    if not has_reading(t):
        print("no reading quiz (no reading to learn)")
        continue
    gen, n_gen, rneed, rthr, rc = reading(t)
    flags = [g for g in gen if g in att]
    print("generated look-alikes (%d of these %d are drawn at random; any left over fill a short corpus tier): %s%s"
          % (n_gen, len(gen), ", ".join(gen) or "none", ("  ATTESTED: " + ", ".join(flags)) if flags else ""))
    problems += len(flags)
    if rneed > 0 and rthr is not None:
        tier = [c for s, c in rc if s >= rthr]
        hits = [c for c in tier if c["reading"] in att]
        print("corpus slots: %d; reachable closeness tier >= %d (%d words): %s" % (
            rneed, rthr, len(tier), ", ".join("%s %s" % (c["word"], c["reading"]) for c in tier[:80]) + (" ..." if len(tier) > 80 else "")))
        if hits:
            print("  ATTESTED corpus readings: " + "; ".join(show(c) for c in hits))
            problems += len(hits)

print("\n## reverse: existing words whose quizzes can draw a listed word")
newset = set(NEW)
rev_meaning, rev_reading = [], []
for t in W.values():
    if t["word"] in newset:
        continue
    cur, over, _, need, thr, cands = meaning(t)
    for c in cur:
        if c["word"] in newset:
            rev_meaning.append((t, c, "curated", ""))
    if thr is not None and need > 0:
        tie = sum(1 for s, _ in cands if s == thr)
        for s, c in cands:
            if s < thr:
                break
            if c["word"] in newset:
                rev_meaning.append((t, c, str(s), "above the last slot" if s > thr else "tie of %d" % tie))
    if has_reading(t):
        gen, n_gen, rneed, rthr, rc = reading(t)
        if rneed > 0 and rthr is not None:
            att = None
            for s, c in rc:
                if s < rthr:
                    break
                if c["word"] in newset:
                    att = attested(t["word"]) if att is None else att
                    rev_reading.append((t, c, s, c["reading"] in att))
print("### meaning quizzes: %d (target, drawable listed word) pairs" % len(rev_meaning))
for t, c, s, how in sorted(rev_meaning, key=lambda x: (NEW.index(x[1]["word"]), x[0]["word"])):
    print("  %s  shown for  %s  [score %s%s]" % (show(c), show(t), s, (", " + how) if how else ""))
print("### reading quiz: %d (target, drawable listed word) pairs" % len(rev_reading))
for t, c, s, hit in sorted(rev_reading, key=lambda x: (NEW.index(x[1]["word"]), x[0]["word"])):
    print("  %s %s  shown for  %s %s  [closeness %d]%s" % (c["word"], c["reading"], t["word"], t["reading"], s, "  ATTESTED" if hit else ""))
    problems += 1 if hit else 0
print("\nATTESTED or too-few-candidate problems: %d" % problems)
