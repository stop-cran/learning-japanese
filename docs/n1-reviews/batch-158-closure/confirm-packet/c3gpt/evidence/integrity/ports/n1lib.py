# -*- coding: utf-8 -*-
"""Shared helpers for the lean N1 batch tooling (read-only against the repo)."""
import gzip
import hashlib
import json
import os
import re
import subprocess
import xml.etree.ElementTree as ET
from collections import OrderedDict, defaultdict
from pathlib import Path

REPO = Path(os.environ.get("N1_REPO", r"C:\Users\romanko\n1-kanji-workspace\learning-japanese"))
INPUTS = Path(r"C:\Users\romanko\n1-kanji-workspace\jmdict")
LEAN = Path(r"C:\Users\romanko\n1-kanji-workspace\lean")
CACHE = LEAN / "cache"
JMDICT_GZ = INPUTS / "JMdict_e.gz"
# Continuation machine: the full planning KANJIDIC2 gz is not available; the frozen selected records live in the repo.
KANJIDIC_GZ = REPO / "docs" / "n1-sources" / "kanjidic2-selected.xml"

CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0002ffff]")
FM_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def git(*args, check=True):
    p = subprocess.run(["git", "-c", "core.quotepath=false", *args], cwd=REPO, capture_output=True)
    if check and p.returncode:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), p.stderr.decode("utf-8", "replace")))
    return p.stdout.decode("utf-8", "replace")


def read(path):
    return Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse(text):
    """Return (front matter OrderedDict or None, body)."""
    m = FM_RE.match(text)
    if not m:
        return None, text
    fm = OrderedDict()
    for line in m.group(1).split("\n"):
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            fm[k.strip()] = [x.strip() for x in v[1:-1].split(",") if x.strip()]
        else:
            fm[k.strip()] = v
    return fm, text[m.end():]


def sections(body):
    out, cur = OrderedDict(), None
    for line in body.split("\n"):
        m = re.match(r"## (.+?)\s*$", line)
        if m:
            cur = m.group(1)
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return OrderedDict((k, "\n".join(v)) for k, v in out.items())


def rel_links(text):
    res = []
    for t in LINK_RE.findall(text):
        if re.match(r"[A-Za-z][A-Za-z0-9+.-]*:", t) or t.startswith("#"):
            continue
        res.append(t.split("#")[0])
    return res


def distinct_kanji(word):
    seen = []
    for c in word:
        if CJK.match(c) and c not in seen:
            seen.append(c)
    return seen


def load_cards():
    kc, wc = {}, {}
    for p in sorted((REPO / "kanji").glob("*.md")):
        kc[p.stem] = parse(read(p))
    for p in sorted((REPO / "words").glob("*.md")):
        wc[p.stem] = parse(read(p))
    return kc, wc


def source_index():
    return {r["kanji"]: r for r in json.loads(read(REPO / "docs/n1-sources/source-index.json"))}


# ---------------------------------------------------------------- JMdict / KANJIDIC2 caches

PRI_ONE = {"news1", "ichi1", "spec1", "gai1"}
PRI_TWO = {"news2", "ichi2", "spec2", "gai2"}


def pri_score(tags):
    s = 0
    for t in tags:
        if t in PRI_ONE:
            s += 3
        elif t in PRI_TWO:
            s += 1
        m = re.fullmatch(r"nf(\d\d)", t)
        if m:
            s += max(0, 3 - (int(m.group(1)) - 1) // 12)
    return s


def build_jmdict_cache(force=False):
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / "jmdict-compact.json.gz"
    stamp = sha256_file(JMDICT_GZ)
    if out.exists() and not force:
        with gzip.open(out, "rt", encoding="utf-8") as f:
            data = json.load(f)
        if data.get("source_sha256") == stamp:
            return data
    entries = {}
    with gzip.open(JMDICT_GZ) as f:
        for _, el in ET.iterparse(f, events=("end",)):
            if el.tag != "entry":
                continue
            eid = el.findtext("ent_seq")
            ks = []
            for k in el.findall("k_ele"):
                ks.append([k.findtext("keb"), [t.text for t in k.findall("ke_pri")],
                           [t.text for t in k.findall("ke_inf")]])
            rs = []
            for r in el.findall("r_ele"):
                rs.append([r.findtext("reb"), [t.text for t in r.findall("re_pri")],
                           [t.text for t in r.findall("re_restr")], r.find("re_nokanji") is not None,
                           [t.text for t in r.findall("re_inf")]])
            ss, last_pos = [], []
            for s in el.findall("sense"):
                pos = [t.text for t in s.findall("pos")] or last_pos
                last_pos = pos
                ss.append({"pos": pos, "misc": [t.text for t in s.findall("misc")],
                           "gloss": [g.text for g in s.findall("gloss")],
                           "stagk": [t.text for t in s.findall("stagk")],
                           "stagr": [t.text for t in s.findall("stagr")],
                           "field": [t.text for t in s.findall("field")]})
            entries[eid] = {"k": ks, "r": rs, "s": ss}
            el.clear()
    char_index = defaultdict(list)
    for eid, e in entries.items():
        chars = set()
        for k in e["k"]:
            chars.update(c for c in k[0] if CJK.match(c))
        for c in chars:
            char_index[c].append(eid)
    data = {"source_sha256": stamp, "entries": entries, "char_index": char_index}
    with gzip.open(out, "wt", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return data


def build_kanjidic_cache(force=False):
    """Frozen KANJIDIC2 records of the N1 source members plus front-matter readings of every other kanji card."""
    CACHE.mkdir(parents=True, exist_ok=True)
    out = CACHE / "kanjidic-compact.json"
    kcards = sorted((REPO / "kanji").glob("*.md"))
    stamp = sha256_file(KANJIDIC_GZ) + ":%d" % len(kcards)
    if out.exists() and not force:
        data = json.loads(read(out))
        if data.get("source_sha256") == stamp:
            return data
    chars = {}
    for _, el in ET.iterparse(str(KANJIDIC_GZ), events=("end",)):
        if el.tag != "character":
            continue
        lit = el.findtext("literal")
        misc = el.find("misc")
        rm = el.find("reading_meaning")
        on, kun, meanings, nanori = [], [], [], []
        if rm is not None:
            for g in rm.findall("rmgroup"):
                on += [r.text for r in g.findall("reading") if r.get("r_type") == "ja_on"]
                kun += [r.text for r in g.findall("reading") if r.get("r_type") == "ja_kun"]
                meanings += [m.text for m in g.findall("meaning") if m.get("m_lang") in (None, "en")]
            nanori = [n.text for n in rm.findall("nanori")]
        chars[lit] = {"on": on, "kun": kun, "meanings": meanings, "nanori": nanori,
                      "grade": misc.findtext("grade") if misc is not None else None,
                      "strokes": misc.findtext("stroke_count") if misc is not None else None,
                      "freq": misc.findtext("freq") if misc is not None else None}
        el.clear()
    for p in kcards:
        if p.stem in chars:
            continue
        fm, _ = parse(read(p))
        if not fm:
            continue
        grade = next((t[6:] for t in fm.get("tags", []) if t.startswith("grade-")), None)
        chars[p.stem] = {"on": fm.get("onyomi", []), "kun": fm.get("kunyomi", []), "meanings": [fm.get("title", "")],
                         "nanori": [], "grade": grade, "strokes": fm.get("strokes"), "freq": None,
                         "fromCard": True}
    data = {"source_sha256": stamp, "chars": chars}
    out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return data


# ---------------------------------------------------------------- reading alignment

KATA = {chr(c): chr(c - 0x60) for c in range(0x30A1, 0x30F7)}
VOICE = dict(zip("かきくけこさしすせそたちつてとはひふへほ", "がぎぐげござじずぜぞだぢづでどばびぶべぼ"))
HANDAKU = dict(zip("はひふへほ", "ぱぴぷぺぽ"))


def hira(s):
    return "".join(KATA.get(c, c) for c in s)


def is_kana(c):
    return "\u3041" <= c <= "\u3096" or "\u30a1" <= c <= "\u30fc"


def reading_variants(r):
    out = {r}
    if r and r[0] in VOICE:
        out.add(VOICE[r[0]] + r[1:])
    if r and r[0] in HANDAKU:
        out.add(HANDAKU[r[0]] + r[1:])
    for v in list(out):
        if len(v) >= 2 and v[-1] in "つくきち":
            out.add(v[:-1] + "っ")
    return out


def candidate_readings(kd_chars, ch):
    d = kd_chars.get(ch)
    res = OrderedDict()
    if not d:
        return res
    for on in d["on"]:
        for v in sorted(reading_variants(hira(on))):
            res.setdefault(v, "on:" + on)
    for kun in d["kun"]:
        k = kun.strip("-")
        stem, _, ok = k.partition(".")
        base = hira(stem)
        for v in sorted(reading_variants(base)):
            res.setdefault(v, "kun:" + kun)
        if ok:
            for v in sorted(reading_variants(base + hira(ok))):
                res.setdefault(v, "kun:" + kun)
    return res


def align(kd_chars, keb, reb, cap=12):
    """All segmentations of reb over the characters of keb: list of [(char, segment, label)]."""
    reb = hira(reb)
    memo = {}

    def go(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        if i == len(keb):
            res = [[]] if j == len(reb) else []
            memo[(i, j)] = res
            return res
        ch, res = keb[i], []
        if ch == "々" and i > 0:
            lookup = keb[i - 1]
        else:
            lookup = ch
        if CJK.match(lookup) or ch == "々":
            for seg, label in candidate_readings(kd_chars, lookup).items():
                if reb.startswith(seg, j):
                    for rest in go(i + 1, j + len(seg)):
                        res.append([(ch, seg, label)] + rest)
                        if len(res) >= cap:
                            break
                if len(res) >= cap:
                    break
        elif is_kana(ch) or ch in "ー":
            c2 = hira(ch)
            if reb.startswith(c2, j):
                for rest in go(i + 1, j + len(c2)):
                    res.append([(ch, c2, "kana")] + rest)
        else:
            for rest in go(i + 1, j):
                res.append([(ch, "", "skip")] + rest)
        memo[(i, j)] = res[:cap]
        return memo[(i, j)]

    return go(0, 0)


def entry_pairs(e):
    """(keb, reb, priority score, kebinfo) combos of one compact entry."""
    out = []
    for k in e["k"]:
        for r in e["r"]:
            if r[3]:
                continue
            if r[2] and k[0] not in r[2]:
                continue
            out.append((k[0], r[0], pri_score(k[1]) + pri_score(r[1]), k[2]))
    return out


ENTRY_LIST = re.compile(r"\bentr(?:y|ies)\s+(\d{6,7}(?:\s*(?:,|and|,\s*and)\s*\d{6,7})*)", re.I)


def entry_ids(text):
    out = []
    for m in ENTRY_LIST.finditer(text):
        for i in re.findall(r"\d{6,7}", m.group(1)):
            if i not in out:
                out.append(i)
    return out
