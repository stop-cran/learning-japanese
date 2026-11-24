"""Mechanical check for the retained-N2 reverse-link correction (not linguistic acceptance).

Usage (cwd = n2rl worktree): python n2rl_check.py BASE_SHA [--jmdict PATH] [--out FILE]
Compares the working tree with BASE: only the five retained kanji cards change at runtime,
their front matter is byte-identical after newline normalization, every word body is unchanged,
each of the nine reverse links appears in the primary-reading row and Common words with the
word's title, and each newly cited JMdict id pairs the word spelling with its reading.
"""
import argparse, gzip, hashlib, json, re, subprocess, sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tools"))
from build_manifest import build_manifest  # noqa: E402

PAIRS = [("保", "保健", "ホ", "1513410"), ("保", "保証", "ホ", "1603500"),
         ("案", "案外", "アン", "1154820"), ("案", "答案", "アン", "1449550"),
         ("派", "立派", "ハ", "1551790"),
         ("結", "結局", "ケツ", "1254730"), ("結", "結構", "ケツ", "1254760"), ("結", "結論", "ケツ", "1255020"),
         ("第", "落第", "ダイ", "1548810")]
CARDS = sorted({p[0] for p in PAIRS}, key="保案派結第".index)
LEVELS = {"保健": 2, "保証": 3, "案外": 2, "答案": 3, "立派": 5, "結局": 3, "結構": 5, "結論": 3, "落第": 2}


def need(ok, msg):
    if not ok:
        raise SystemExit("FAIL: " + msg)


def show(base, name):
    return subprocess.check_output(["git", "--no-pager", "show", f"{base}:{name}"]).decode("utf-8").replace("\r\n", "\n")


def split(text):
    need(text.startswith("---\n"), "front matter")
    head, body = text[4:].split("\n---\n", 1)
    return head, body


def section(body, title):
    return body.split(f"## {title}\n", 1)[1].split("\n## ", 1)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("base")
    ap.add_argument("--jmdict", default=r"C:\Users\romanko\n1-kanji-workspace\jmdict\JMdict_e.gz")
    ap.add_argument("--out")
    a = ap.parse_args()
    root = Path.cwd()
    report = {"base": subprocess.check_output(["git", "rev-parse", a.base]).decode().strip()}
    before = json.loads(show(a.base, "manifest.json"))
    current = build_manifest(root, publish_reading=True)
    need(json.loads((root / "manifest.json").read_text(encoding="utf-8")) == current, "manifest stale")
    meta = lambda m: {k: v for k, v in m.items() if k != "contentVersion" and not isinstance(v, dict)}
    need(meta(before) == meta(current), "runtime metadata changed")
    flat = lambda m: {(s, n): v for s, e in m.items() if isinstance(e, dict) for n, v in e.items()}
    old, new = flat(before), flat(current)
    need(old.keys() == new.keys(), "runtime additions/removals")
    changed = sorted(n for n in old if old[n] != new[n])
    need(changed == sorted(("files", f"kanji/{c}.md") for c in CARDS), f"runtime changes {changed}")
    report["runtimeChanged"] = [n for _, n in changed]
    report["contentVersion"] = {"before": before["contentVersion"], "after": current["contentVersion"]}
    for c in CARDS:
        bh, _ = split(show(a.base, f"kanji/{c}.md"))
        ch, _ = split((root / f"kanji/{c}.md").read_text(encoding="utf-8"))
        need(bh == ch, f"front matter changed: {c}")
    need(sorted(set(subprocess.check_output(["git", "-c", "core.quotepath=off", "diff", "--name-only", a.base, "--", "words", "strokes", "kanji"]).decode("utf-8").split()))
         == sorted(f"kanji/{c}.md" for c in CARDS), "diff outside the five kanji cards")
    with gzip.open(a.jmdict) as f:
        raw = f.read()
    report["jmdictSha256"] = hashlib.sha256(Path(a.jmdict).read_bytes()).hexdigest()
    ids = {p[3] for p in PAIRS}
    entries = {}
    for ev, el in ET.iterparse(__import__("io").BytesIO(raw), events=("end",)):
        if el.tag == "entry":
            i = el.findtext("ent_seq")
            if i in ids:
                entries[i] = el
            else:
                el.clear()
    rows = []
    for c, w, reading_head, eid in PAIRS:
        kt = (root / f"kanji/{c}.md").read_text(encoding="utf-8")
        wt = (root / f"words/{w}.md").read_text(encoding="utf-8")
        wh, wb = split(wt)
        wm = __import__("yaml").safe_load(wh)
        need(wm["jlpt"] == LEVELS[w], f"word level changed {w}")
        need(f"(../kanji/{c}.md)" in wb, f"word lacks kanji link {w}")
        _, kb = split(kt)
        link = f"[{w}](../words/{w}.md) {wm['reading']} - "
        row = [l for l in section(kb, "Readings").splitlines() if l.startswith(f"| {reading_head} |")]
        need(len(row) == 1 and link in row[0], f"reading-row link {c}/{w}")
        common = [l for l in section(kb, "Common words").splitlines() if l.startswith(f"- {link}")]
        need(len(common) == 1 and common[0] == f"- {link}{wm['title']}", f"Common words title {c}/{w}: {common}")
        need(eid in kb.split("Metadata:", 1)[1], f"metadata id {eid}")
        e = entries.get(eid)
        need(e is not None and w in {k.text for k in e.findall("k_ele/keb")}
             and any(r.findtext("reb") == wm["reading"] and r.find("re_nokanji") is None
                     and (not r.findall("re_restr") or w in {x.text for x in r.findall("re_restr")})
                     for r in e.findall("r_ele")), f"JMdict pair {eid} {w}")
        rows.append({"kanji": c, "word": w, "reading": wm["reading"], "readingRow": reading_head,
                     "jmdict": eid, "wordJlpt": wm["jlpt"]})
    report["pairs"] = rows
    report["limits"] = ("Mechanical structure/link/identity check against BASE; not linguistic review, "
                        "quiz-distractor adjudication, publication or device acceptance.")
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8", newline="\n")
    print(text)


main()
