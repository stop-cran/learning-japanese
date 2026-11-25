# -*- coding: utf-8 -*-
"""Lean N1 batch tool: lint | dossier | evidence | packet.

Read-only against the repository except where a subcommand states an output directory.
"""
import argparse
import json
import re
import sys
import urllib.parse
from collections import OrderedDict, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from n1lib import *  # noqa: E402,F401,F403

SIX_N2 = set("保案派第策結")
KANJI_KEYS = ["kanji", "title", "jlpt", "tags", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi",
              "quizOnyomi", "quizKunyomi", "distractors", "quiz_exclusions"]
KANJI_SECTIONS = ["Meaning and origin", "Readings", "Common words", "Notes"]
WORD_SECTIONS = ["Meaning", "How the kanji combine", "Synonyms and antonyms", "Distinctive meaning"]
WORD_TYPES = {"kango", "wago", "jukujikun", "gairaigo"}
KANA_RE = re.compile(r"^[ぁ-ゟァ-ヿー.\-]+$")
RAW_HTML = re.compile(r"<\s*/?\s*(script|iframe|style|object|embed|img|a|div|span|svg)\b", re.I)
MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")


class Report:
    def __init__(self):
        self.errors, self.warnings = [], []

    def err(self, path, msg):
        self.errors.append("%s: %s" % (path, msg))

    def warn(self, path, msg):
        self.warnings.append("%s: %s" % (path, msg))


def resolve_link(base_dir, target):
    return (base_dir / urllib.parse.unquote(target.split("#", 1)[0])).resolve()


def check_links(R, rel, base_dir, body, kanji_ids, word_ids):
    if RAW_HTML.search(body):
        R.err(rel, "raw HTML")
    for t in MD_LINK.findall(body):
        if t.startswith("https://") or t.startswith("#"):
            continue
        if re.match(r"[a-z][a-z0-9+.-]*:", t, re.I):
            R.err(rel, "unsupported link scheme: " + t)
            continue
        fp = urllib.parse.unquote(t.split("#", 1)[0])
        if not fp.endswith(".md"):
            R.err(rel, "link must target .md: " + t)
            continue
        tp = (base_dir / fp).resolve()
        if tp.parent.name not in ("kanji", "words", "articles") or tp.parent.parent != REPO.resolve():
            R.err(rel, "relative link targets non-imported content: " + t)
        elif not tp.is_file():
            R.err(rel, "broken link: " + t)


def reading_rows(body):
    secs = sections(body)
    text = secs.get("Readings", "")
    rows = []
    for line in text.split("\n"):
        s = line.strip()
        if s.startswith("|") and not re.match(r"^\|\s*:?-{3,}:?\s*\|", s):
            cells = [c.strip() for c in s.strip("|").split("|")]
            rows.append(cells)
    return rows[1:] if rows and rows[0][0].lower() == "reading" else rows


def lint_kanji(R, ch, idx, kc, wc, titles, jm=None, strict=True):
    rel = "kanji/%s.md" % ch
    fm, body = kc[ch]
    soft = R.err if strict else R.warn
    if fm is None:
        R.err(rel, "missing front matter")
        return
    keys = list(fm.keys())
    required = KANJI_KEYS[:9]
    for k in required:
        if k not in fm:
            R.err(rel, "missing key " + k)
    unknown = [k for k in keys if k not in KANJI_KEYS]
    if unknown:
        R.err(rel, "unknown keys %s" % unknown)
    order = [k for k in KANJI_KEYS if k in keys]
    if order != [k for k in keys if k in KANJI_KEYS]:
        R.warn(rel, "front matter key order differs from the usual order")
    if fm.get("kanji") != ch or len(ch) != 1:
        R.err(rel, "'kanji' must equal the file name")
    src = idx.get(ch)
    if src is None:
        R.warn(rel, "not in the N1 source index; source comparison skipped")
    meta = src["metadata"] if src else None
    jl = fm.get("jlpt")
    expected_jl = "2" if ch in SIX_N2 else "1"
    if src and src["statusAtFreeze"] == "pending" and jl != expected_jl:
        R.err(rel, "jlpt %s, expected %s" % (jl, expected_jl))
    tags = fm.get("tags", [])
    if src and src["statusAtFreeze"] == "pending":
        want = ["jlpt-n" + expected_jl, "grade-%s" % meta["grade"], "structure-unclassified"]
        if tags[:3] != want:
            R.err(rel, "tags %s, expected prefix %s" % (tags, want))
    if meta:
        for key in ("strokes", "radicalNumber"):
            if str(fm.get(key)) != str(meta[key]):
                R.err(rel, "%s %s != source %s" % (key, fm.get(key), meta[key]))
        if fm.get("radical") != meta["radical"]:
            R.err(rel, "radical %s != source %s" % (fm.get("radical"), meta["radical"]))
        for key in ("onyomi", "kunyomi"):
            if fm.get(key) != meta[key]:
                R.err(rel, "%s %s != source %s" % (key, fm.get(key), meta[key]))
    for key in ("onyomi", "kunyomi", "quizOnyomi", "quizKunyomi"):
        for r in fm.get(key, []):
            if not KANA_RE.match(r):
                R.err(rel, "%s entry not kana: %s" % (key, r))
    for key, full in (("quizOnyomi", "onyomi"), ("quizKunyomi", "kunyomi")):
        sel = fm.get(key)
        if sel is None:
            R.warn(rel, "no " + key)
            continue
        if len(sel) != len(set(sel)) or any(r not in fm.get(full, []) for r in sel):
            R.err(rel, "%s must be distinct members of %s" % (key, full))
    title = (fm.get("title") or "").strip().lower()
    if not title:
        R.err(rel, "empty title")
    elif title in titles and titles[title] != ch:
        R.err(rel, "duplicate title %r (also %s)" % (fm["title"], titles[title]))
    sp = REPO / "strokes" / ("%s.json" % ch)
    if not sp.is_file():
        R.err(rel, "missing strokes file")
    else:
        try:
            sd = json.loads(read(sp))
            n = len(sd.get("strokes", sd.get("paths", [])))
            if n and str(n) != str(fm.get("strokes")):
                R.err(rel, "strokes JSON has %d strokes, card says %s" % (n, fm.get("strokes")))
        except Exception as e:  # noqa: BLE001
            R.err(rel, "strokes JSON unreadable: %s" % e)
    dis = fm.get("distractors", [])
    if len(dis) != len(set(dis)):
        R.err(rel, "repeated distractors")
    good = [d for d in dis if len(d) == 1 and d != ch and d in kc]
    if len(good) != len(dis):
        R.err(rel, "distractors must be existing nonself kanji cards: %s" % dis)
    if len(set(good)) < 2:
        R.err(rel, "need >= 2 distinct distractors")
    elif len(set(good)) != 3:
        R.warn(rel, "%d distractors (usual practice is 3)" % len(set(good)))
    ex = fm.get("quiz_exclusions", [])
    if len(ex) != len(set(ex)):
        R.err(rel, "repeated quiz_exclusions")
    for e in ex:
        if e == ch:
            R.err(rel, "quiz_exclusions includes the card itself")
        elif e not in kc:
            R.err(rel, "exclusion %s has no card" % e)
        if e in dis:
            R.err(rel, "%s is both distractor and exclusion" % e)
    # body
    secs = sections(body)
    got = [s for s in secs.keys() if s in KANJI_SECTIONS]
    if got != KANJI_SECTIONS:
        R.err(rel, "sections %s, expected %s" % (list(secs.keys()), KANJI_SECTIONS))
    h1 = [l for l in body.split("\n") if l.startswith("# ")]
    if len(h1) != 1 or h1[0] != "# %s \u2014 %s" % (ch, fm.get("title")):
        R.err(rel, "H1 must be '# %s \u2014 %s', got %s" % (ch, fm.get("title"), h1))
    pre = body.split("\n## ")[0].replace("**", "")
    if not (re.search(r"\bStrokes:", pre) and re.search(r"\bKey\s*\(radical\):", pre) and re.search(r"\bJLPT:", pre)):
        R.err(rel, "facts line (Strokes, Key (radical), JLPT) missing")
    else:
        m = re.search(r"Strokes:\s*(\d+)", pre)
        if m and str(fm.get("strokes")) != m.group(1):
            R.err(rel, "facts line strokes %s != front matter %s" % (m.group(1), fm.get("strokes")))
        if fm.get("radical") and fm["radical"] not in pre:
            R.err(rel, "facts line does not mention the radical %s" % fm["radical"])
        m = re.search(r"JLPT:\s*N(\d)", pre)
        if m and m.group(1) != str(fm.get("jlpt")):
            R.err(rel, "facts line JLPT N%s != jlpt %s" % (m.group(1), fm.get("jlpt")))
    rows = reading_rows(body)
    cells0 = [r[0].strip(" *`") for r in rows]
    norm0 = [c.strip("-") for c in cells0]
    for r in fm.get("onyomi", []) + fm.get("kunyomi", []):
        if r not in cells0 and r.strip("-") not in norm0:
            R.err(rel, "metadata reading %s has no Readings row" % r)
    for key in ("quizOnyomi", "quizKunyomi"):
        for r in fm.get(key, []):
            ok = False
            for row in rows:
                if row[0].strip(" *`") == r:
                    for t in MD_LINK.findall("|".join(row[2:])):
                        tp = resolve_link(REPO / "kanji", t)
                        if tp.parent.name == "words" and tp.is_file():
                            ok = True
                            wfm = wc.get(tp.stem, (None,))[0]
                            if wfm and ch not in wfm.get("kanji", []):
                                R.warn(rel, "%s example %s does not declare %s in kanji:" % (r, tp.stem, ch))
            if not ok:
                R.err(rel, "%s '%s' needs a Readings row linking a word example" % (key, r))
    if not MD_LINK.search(secs.get("Common words", "")):
        R.err(rel, "Common words has no link")
    meta_m = re.search(r"^(Metadata|Sources?):.*", body, re.M | re.S)
    if not meta_m:
        soft(rel, "no Metadata: line")
    elif jm is not None:
        ids = entry_ids(meta_m.group(0))
        if not ids:
            soft(rel, "Metadata: block cites no JMdict entry ids")
        for eid in ids:
            if eid not in jm["entries"]:
                soft(rel, "cited JMdict entry %s does not exist" % eid)
    check_links(R, rel, REPO / "kanji", body, kc, wc)


def lint_word(R, w, kc, wc, jm=None, strict=True):
    rel = "words/%s.md" % w
    fm, body = wc[w]
    soft = R.err if strict else R.warn
    if fm is None:
        R.err(rel, "missing front matter")
        return
    for k in ("word", "reading", "title", "type", "kanji", "tags"):
        if k not in fm:
            R.err(rel, "missing key " + k)
    if fm.get("word") != w:
        R.err(rel, "'word' must equal the file name")
    if not KANA_RE.match(fm.get("reading", "")):
        R.err(rel, "reading is not kana")
    if fm.get("type") not in WORD_TYPES:
        R.err(rel, "unknown type %s" % fm.get("type"))
    declared = fm.get("kanji", [])
    for c in declared:
        if len(c) != 1 or c not in w:
            R.err(rel, "kanji entry %r not in the word" % c)
    written = set(c for c in w if CJK.match(c) or c == "\u3007")
    if written - set(declared):
        R.err(rel, "kanji: is missing %s" % sorted(written - set(declared)))
    secs = sections(body)
    got = [s for s in secs.keys() if s in WORD_SECTIONS]
    if declared:
        if got != WORD_SECTIONS:
            R.err(rel, "sections %s, expected %s" % (list(secs.keys()), WORD_SECTIONS))
    else:
        want = [s for s in WORD_SECTIONS if s != "How the kanji combine"]
        if got not in (WORD_SECTIONS, want):
            R.err(rel, "sections %s" % list(secs.keys()))
    ex = fm.get("quiz_exclusions", [])
    if len(ex) != len(set(ex)):
        R.err(rel, "repeated quiz_exclusions")
    for e in ex:
        if e == w:
            R.err(rel, "quiz_exclusions includes the word itself")
        elif e not in wc:
            R.err(rel, "exclusion %s has no word article" % e)
    linked = set()
    for t in MD_LINK.findall(body):
        tp = resolve_link(REPO / "words", t)
        if tp.parent.name == "kanji":
            linked.add(tp.stem)
    for c in dict.fromkeys(declared):
        if c in kc and c not in linked:
            R.err(rel, "kanji %s has a card but the article does not link it" % c)
    h1 = [l for l in body.split("\n") if l.startswith("# ")]
    if len(h1) != 1 or not h1[0].startswith("# %s (%s) - " % (w, fm.get("reading"))) and not h1[0].startswith("# %s" % w):
        R.warn(rel, "H1 shape %s" % h1)
    dict_lines = [l for l in body.split("\n") if l.startswith("Dictionary:")]
    if not dict_lines:
        soft(rel, "no Dictionary: line")
    elif jm is not None:
        ids = entry_ids(dict_lines[0])
        if not ids:
            soft(rel, "Dictionary: line cites no JMdict entry id")
        okany = False
        for eid in ids:
            e = jm["entries"].get(eid)
            if e is None:
                soft(rel, "JMdict entry %s does not exist" % eid)
                continue
            kebs = [k[0] for k in e["k"]]
            rebs = [r[0] for r in e["r"]]
            if w in kebs or w in rebs:
                okany = True
        if ids and not okany:
            soft(rel, "no cited JMdict entry has the spelling %s" % w)
    check_links(R, rel, REPO / "words", body, kc, wc)


def changed_paths(base):
    out = git("diff", "--name-status", base, "--", "kanji", "words", "strokes", "docs", "manifest.json")
    paths = {}
    for line in out.strip().split("\n"):
        if line.strip():
            st, p = line.split("\t", 1)
            paths[p.strip()] = st[0]
    for line in git("status", "--porcelain", "--untracked-files=all", "--", "kanji", "words", "strokes").split("\n"):
        if line.strip():
            st, p = line[:2], line[3:].strip().strip('"')
            paths.setdefault(p, "A" if "?" in st else "M")
    return paths


def cmd_lint(a):
    idx = source_index()
    kc, wc = load_cards()
    jm = build_jmdict_cache() if not a.no_jmdict else None
    titles = {}
    for k, (fm, b) in kc.items():
        if fm:
            titles[(fm.get("title") or "").strip().lower()] = k
    R = Report()
    strict_k, strict_w = set(), set()
    if a.all_n1:
        lo, hi = (a.rows or "1-99999").split("-")
        lo, hi = int(lo), int(hi)
        targets_k = [k for k, (fm, b) in kc.items() if (fm and "jlpt-n1" in fm.get("tags", [])) or k in SIX_N2]
        strict_k = {k for k in targets_k if k in idx and lo <= idx[k]["sourceRow"] <= hi and a.rows}
        targets_w = []
        if a.words:
            targets_w = sorted(wc)
    else:
        paths = changed_paths(a.base)
        targets_k = [Path(p).stem for p, st in paths.items() if p.startswith("kanji/") and p.endswith(".md") and st != "D"]
        targets_w = [Path(p).stem for p, st in paths.items() if p.startswith("words/") and p.endswith(".md") and st != "D"]
        strict_k = {Path(p).stem for p, st in paths.items() if p.startswith("kanji/") and st == "A"}
        strict_w = {Path(p).stem for p, st in paths.items() if p.startswith("words/") and st == "A"}
    for k in a.kanji or []:
        if k not in targets_k:
            targets_k.append(k)
        strict_k.add(k)
    for k in targets_k:
        if k in kc:
            lint_kanji(R, k, idx, kc, wc, titles, jm, strict=k in strict_k)
    # words declaring any linted kanji must link them
    kset = set(targets_k)
    for w, (fm, b) in wc.items():
        if fm and kset & set(fm.get("kanji", [])):
            if w not in targets_w:
                targets_w.append(w)
    for w in targets_w:
        if w in wc:
            lint_word(R, w, kc, wc, jm, strict=w in strict_w)
    print("kanji checked: %d, words checked: %d" % (len(targets_k), len(targets_w)))
    for m in R.warnings:
        print("WARN  " + m)
    for m in R.errors:
        print("ERROR " + m)
    print("%d error(s), %d warning(s)" % (len(R.errors), len(R.warnings)))
    return 1 if R.errors else 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("lint")
    p.add_argument("--base", default="origin/main")
    p.add_argument("--all-n1", action="store_true")
    p.add_argument("--rows", help="A-B source-row range treated as strict in --all-n1 mode")
    p.add_argument("--words", action="store_true")
    p.add_argument("--no-jmdict", action="store_true")
    p.add_argument("kanji", nargs="*")
    p.set_defaults(fn=cmd_lint)
    try:
        import n1cmds  # dossier / evidence / webcheck / packet
    except ModuleNotFoundError as e:
        if e.name != "n1cmds":
            raise
    else:
        n1cmds.register(sub)
    a = ap.parse_args()
    sys.exit(a.fn(a))


if __name__ == "__main__":
    main()

