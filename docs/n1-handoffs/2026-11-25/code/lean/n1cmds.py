# -*- coding: utf-8 -*-
"""dossier | evidence | webcheck | packet subcommands for the lean N1 tool."""
import copy
import datetime
import gzip
import hashlib
import html
import json
import re
import shutil
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict, defaultdict
from pathlib import Path

from n1lib import *  # noqa: F401,F403

MD_LINK = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)\)")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


def now_utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ------------------------------------------------------------------ evidence

def jmdict_xml(ids):
    ids = set(ids)
    keep = {}
    with gzip.open(JMDICT_GZ) as f:
        for _, el in ET.iterparse(f, events=("end",)):
            if el.tag != "entry":
                continue
            if el.findtext("ent_seq") in ids:
                keep[el.findtext("ent_seq")] = copy.deepcopy(el)
            el.clear()
    missing = ids - keep.keys()
    if missing:
        raise SystemExit("JMdict entries not found: %s" % sorted(missing))
    root = ET.Element("JMdict")
    for eid in sorted(keep, key=int):
        root.append(keep[eid])
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def kanjidic_xml(chars):
    want = list(OrderedDict.fromkeys(chars))
    keep, header = {}, None
    with open(KANJIDIC_GZ, "rb") as f:
        for _, el in ET.iterparse(f, events=("end",)):
            if el.tag == "header":
                header = copy.deepcopy(el)
            elif el.tag == "character":
                lit = el.findtext("literal")
                if lit in want:
                    keep[lit] = copy.deepcopy(el)
                el.clear()
    root = ET.Element("kanjidic2")
    if header is not None:
        root.append(header)
    for c in want:
        if c in keep:
            root.append(keep[c])
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n", [c for c in want if c not in keep]


def jmdict_digest(kanji):
    jm = build_jmdict_cache()
    lines = ["kanji\tentry\twritten forms containing it\treadings\tpriority tags\tfirst-sense pos\tfirst-sense glosses"]
    for k in kanji:
        rows = []
        for eid in jm["char_index"].get(k, []):
            e = jm["entries"][eid]
            forms = [x for x in e["k"] if k in x[0]]
            pri = sorted({t for x in forms for t in x[1]} | {t for r in e["r"] for t in r[1]})
            score = max([pri_score(x[1]) for x in forms] + [0]) + max([pri_score(r[1]) for r in e["r"]] + [0])
            s0 = e["s"][0] if e["s"] else {"pos": [], "gloss": []}
            rows.append((-score, int(eid), "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
                k, eid, " ".join(x[0] for x in forms), " ".join(r[0] for r in e["r"]), " ".join(pri),
                "; ".join(s0["pos"])[:80], "; ".join(s0["gloss"][:4])[:140])))
        rows.sort()
        lines += [r[2] for r in rows]
    return "\n".join(lines) + "\n"


def webcheck_text(k):
    url = "https://www.weblio.jp/content/" + urllib.parse.quote(k)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "ja,en;q=0.8"})
    raw = urllib.request.urlopen(req, timeout=40).read()
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    t = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
    i = t.find("デジタル大辞泉")
    block = ""
    # The character entry's head may mark the kanji (▽/×), list old forms (〔辨〕) and, for kokuji, have only ［訓］.
    head = r"[ぁ-ゖー‐・]{1,8}【\s*(?:[▽×]\s*)?%s[^】]{0,24}】 読み方：[^ ]+ (?:［ (?:常用|人名用)漢字 ］ )?" % re.escape(k)
    m = re.search(head + r"［音］", t) or re.search(head + r"［訓］", t)
    if m:
        block = t[m.start():m.start() + 1500]
        end = block.find("索引トップ")
        block = block[:end if end > 0 else len(block)].strip()
    elif i >= 0:
        j = t.find("索引トップ", i + 10)
        j = t.find("凡例", j) + 2 if j >= 0 else i
        end = t.find("索引トップ", j)
        block = t[j:end if end > 0 else j + 1500].strip()[:1800]
    return url, raw, block


def cmd_webcheck(a):
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    receipts = []
    for k in a.kanji:
        try:
            url, raw, block = webcheck_text(k)
        except Exception as e:  # noqa: BLE001
            print("%s: fetch failed: %s" % (k, e))
            continue
        (out / ("weblio-%s.txt" % k)).write_text(
            "Source: %s\nRetrieved: %s\nRaw HTML sha256: %s (%d bytes)\n"
            "Extract: Digital Daijisen character entry on the Weblio page, else its first Daijisen block "
            "(coordinator retrieval)\n\n%s\n"
            % (url, now_utc(), hashlib.sha256(raw).hexdigest(), len(raw), block or "(no Digital Daijisen block found)"),
            encoding="utf-8")
        receipts.append({"kanji": k, "url": url, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)})
        print("%s: %d bytes, daijisen block %d chars" % (k, len(raw), len(block)))
    return 0


def collect(base, sha):
    mb = git("merge-base", base, sha).strip()
    changed = OrderedDict()
    for line in git("diff", "--name-status", mb, sha, "--", "kanji", "words", "strokes").strip().split("\n"):
        if line.strip():
            st, p = line.split("\t", 1)
            changed[p.strip()] = st[0]
    texts = {p: git("show", "%s:%s" % (sha, p)) for p, s in changed.items() if s != "D" and p.endswith(".md")}
    new_kanji = [Path(p).stem for p, s in changed.items() if p.startswith("kanji/") and s == "A"]
    new_words = [Path(p).stem for p, s in changed.items() if p.startswith("words/") and s == "A"]
    cited = []
    compare = []
    for p, t in texts.items():
        for i in entry_ids(t):
            if i not in cited:
                cited.append(i)
        fm, body = parse(t.replace("\r\n", "\n"))
        for tgt in MD_LINK.findall(body):
            tp = tgt.split("#")[0]
            m = re.search(r"kanji/([^/]+)\.md$", tp.replace("\\", "/"))
            if m and len(m.group(1)) == 1 and m.group(1) not in compare:
                compare.append(m.group(1))
        if fm and p.startswith("kanji/"):
            for c in fm.get("distractors", []) + fm.get("quiz_exclusions", []):
                if c not in compare:
                    compare.append(c)
        if fm and p.startswith("words/"):
            for c in fm.get("kanji", []):
                if c not in compare:
                    compare.append(c)
    return {"base": mb, "sha": sha, "changed": changed, "texts": texts, "new_kanji": new_kanji,
            "new_words": new_words, "cited": cited, "compare": compare}


def build_evidence(info, out, web=True):
    out.mkdir(parents=True, exist_ok=True)
    jm = build_jmdict_cache()
    fam = sorted({eid for k in info["new_kanji"] for eid in jm["char_index"].get(k, [])} | set(info["cited"]), key=int)
    (out / "jmdict-families.xml").write_bytes(jmdict_xml(fam))
    (out / "jmdict-digest.tsv").write_text(jmdict_digest(info["new_kanji"]), encoding="utf-8")
    chars = info["new_kanji"] + [c for c in info["compare"] if c not in info["new_kanji"]]
    kd, missing = kanjidic_xml(chars)
    (out / "kanjidic2-records.xml").write_bytes(kd)
    idx = source_index()
    (out / "source-metadata.json").write_text(
        json.dumps({k: idx[k]["metadata"] | {"sourceRow": idx[k]["sourceRow"]} for k in info["new_kanji"] if k in idx},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    snap = json.loads(read(REPO / "docs/n1-source-snapshot.json"))
    cont = json.loads(read(REPO / "docs/n1-sources/continuation-inputs.json"))
    jm_sha = sha256_file(JMDICT_GZ)
    if jm_sha != cont["inputs"]["n1-continuation-JMdict_e.gz"]["sha256"]:
        raise SystemExit("JMdict file does not match the continuation pin")
    prov = {"builtAt": now_utc(), "jmdictFile": JMDICT_GZ.name, "jmdictSha256": jm_sha,
            "jmdictPin": "docs/n1-sources/continuation-inputs.json#n1-continuation-JMdict_e.gz",
            "kanjidic2File": "docs/n1-sources/kanjidic2-selected.xml", "kanjidic2Sha256": sha256_file(KANJIDIC_GZ),
            "frozenInputs": snap.get("inputs", {}), "continuationInputs": cont["inputs"], "familyCount": len(fam),
            "familiesCited": info["cited"], "kanjidicMissing": missing,
            "note": "jmdict-families.xml holds every JMdict family that writes any new kanji of this batch, plus every "
                    "family cited by the changed cards, from the continuation JMdict (created 2026-11-17). "
                    "kanjidic2-records.xml holds the frozen 2026-11-02 KANJIDIC2 records preserved in the repository "
                    "for N1 source members only; other comparison kanji are listed in kanjidicMissing and their cards "
                    "are under repo/kanji. Pinned dictionary data may differ from today's online dictionaries."}
    (out / "provenance.json").write_text(json.dumps(prov, ensure_ascii=False, indent=2), encoding="utf-8")
    if web:
        cmd_webcheck(argparse_ns(out=str(out / "public-source"), kanji=info["new_kanji"]))
    return fam


class argparse_ns:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def cmd_evidence(a):
    info = collect(a.base, a.sha)
    fam = build_evidence(info, Path(a.out), web=not a.no_web)
    print("batch kanji:", " ".join(info["new_kanji"]), "| new words:", " ".join(info["new_words"]))
    print("families:", len(fam), "cited:", len(info["cited"]), "comparison kanji:", len(info["compare"]))
    return 0


# ------------------------------------------------------------------ dossier

def kanji_readings_of_entry(kd, e, k):
    """Distinct (segment, label) that kanji k takes in the best-priority form of entry e."""
    for keb, reb, sc, inf in sorted(entry_pairs(e), key=lambda x: -x[2]):
        if k not in keb:
            continue
        found = []
        for seg in align(kd, keb, reb):
            for ch, s, label in seg:
                if ch == k and label not in ("kana", "skip"):
                    if (s, label) not in found:
                        found.append((s, label))
        if found:
            return keb, reb, sc, found
    return None


def cmd_dossier(a):
    idx = source_index()
    kc, wc = load_cards()
    jm = build_jmdict_cache()
    kd = build_kanjidic_cache()["chars"]
    out = []
    for k in a.kanji:
        r = idx.get(k)
        if not r:
            out.append("## %s: not in the N1 source index\n" % k)
            continue
        m = r["metadata"]
        out.append("## %s (source row %d) - grade %s, radical %s (%s), %s strokes" % (
            k, r["sourceRow"], m["grade"], m["radical"], m["radicalNumber"], m["strokes"]))
        out.append("source on: %s | kun: %s | meanings: %s" % (m["onyomi"], m["kunyomi"], m["meanings"]))
        d = kd.get(k, {})
        out.append("KANJIDIC2 freq=%s nanori=%s" % (d.get("freq"), d.get("nanori")))
        out.append("card exists: %s" % (k in kc))
        decl = [(w, fm) for w, (fm, b) in wc.items() if fm and k in fm.get("kanji", [])]
        out.append("existing words declaring %s (%d):" % (k, len(decl)))
        for w, fm in decl[:40]:
            linked = bool(re.search(r"\.\./kanji/%s\.md" % re.escape(k), wc[w][1]))
            out.append("  - %s (%s) %s | %s | jlpt=%s | links kanji=%s" % (
                w, fm.get("reading"), fm.get("type"), fm.get("title"), fm.get("jlpt", "-"), linked))
        spelled = [w for w in wc if k in w and w not in {x[0] for x in decl}]
        if spelled:
            out.append("  words spelled with %s but NOT declaring it: %s" % (k, spelled[:20]))
        ids = jm["char_index"].get(k, [])
        scored = []
        for eid in ids:
            e = jm["entries"][eid]
            best = max([p[2] for p in entry_pairs(e) if k in p[0]] + [0])
            scored.append((-best, int(eid), eid))
        scored.sort()
        out.append("JMdict entries writing %s: %d (showing top %d by priority)" % (k, len(ids), a.top))
        groups = defaultdict(list)
        for sc, _, eid in scored:
            e = jm["entries"][eid]
            got = kanji_readings_of_entry(kd, e, k)
            s0 = e["s"][0] if e["s"] else {"gloss": [], "pos": []}
            if got:
                keb, reb, p, found = got
                lab = ",".join("%s[%s]" % (s, l) for s, l in found[:3])
            else:
                keb = next((x[0] for x in e["k"] if k in x[0]), "?")
                reb = e["r"][0][0] if e["r"] else "?"
                p, lab = -sc, "UNALIGNED"
            groups[lab.split("[")[0] if "[" in lab else lab].append(keb)
            if len([1 for _ in groups]) and sum(len(v) for v in groups.values()) <= a.top:
                out.append("  %s %s (%s) pri=%d K=%s | %s | %s" % (
                    eid, keb, reb, p, lab, "; ".join(s0["pos"])[:40], "; ".join(s0["gloss"][:3])[:90]))
        out.append("reading groups (all %d entries): %s" % (len(ids), {g: (len(v), v[:6]) for g, v in groups.items()}))
        same_rad = [c for c, (fm, b) in kc.items() if fm and fm.get("radicalNumber") == str(m["radicalNumber"])
                    and c != k][:18]
        out.append("existing cards sharing radical %s: %s" % (m["radical"], " ".join(same_rad)))
        same_on = {}
        for on in m["onyomi"]:
            same_on[on] = [c for c, (fm, b) in kc.items() if fm and on in fm.get("onyomi", []) and c != k][:12]
        out.append("existing cards sharing an on reading: %s" % same_on)
        out.append("header skeleton:")
        out.append("---\nkanji: %s\ntitle: \njlpt: 1\ntags: [jlpt-n1, grade-%s, structure-unclassified]\nstrokes: %s\n"
                   "radical: %s\nradicalNumber: %s\nonyomi: [%s]\nkunyomi: [%s]\nquizOnyomi: []\nquizKunyomi: []\n"
                   "distractors: []\nquiz_exclusions: []\n---" % (
                       k, m["grade"], m["strokes"], m["radical"], m["radicalNumber"],
                       ", ".join(m["onyomi"]), ", ".join(m["kunyomi"])))
        out.append("")
    text = "\n".join(out)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print("wrote", a.out, len(text), "chars")
    else:
        print(text)
    return 0


# ------------------------------------------------------------------ packet

INSTR = """# Independent review packet: N1 kanji batch {batch}, candidate {sha8}

You are one of several independent reviewers from different model families. You will not see the other reviewers'
reports or the author's rationale, and you must not look for them. Work alone, serially and read-only.

## Mandate

- **Read-only.** Do not edit, stage, commit, push or run any command that changes files, except that you write your own
  report to the one path you are given in your assignment. Do not start other agents, sessions or background jobs.
  Make one tool call at a time; read large files in ranges rather than all at once.
- **Blind.** This packet is your complete local evidence set. Do not open any other path on this machine (in particular
  no repository checkouts, no `docs\\n1-reviews`, no `docs\\n1-sources\\batch-*`, no `docs\\n1-authoring-notes.md`, no other
  packets or reports). Public web sources are allowed and encouraged for verification.
- **Scope.** The files in `snapshot\\` are the unit under review. `repo\\` is a read-only export of the rest of the
  content at the same commit, for checking links, titles, readings, exclusions and consistency; it is context, not
  further scope. `diffs\\` shows how modified existing files changed.

## What the batch is

Teaching cards for JLPT N1 kanji (community list). Kanji added: {kanji}. New word articles: {new_words}.
Modified existing files: {modified}. Audience: an English speaker at roughly JLPT N5-N4 reading on a phone. The format
contract is `repo\\docs\\content-format.md`; the review contract is `rubric\\copilot-instructions.md`.

## Facets (cover all four; your assignment names the one to examine deepest)

1. **Correctness.** Front matter against the pinned metadata (`evidence\\source-metadata.json`, `evidence\\kanjidic2-records.xml`);
   every reading claim; word readings, types, senses, register and restrictions against complete JMdict families
   (`evidence\\jmdict-families.xml`, `evidence\\jmdict-digest.tsv`) and independent public sources; example sentences
   (grammar, naturalness, translation, kana); mnemonics labelled as mnemonics; no unsupported etymology; every
   comparison claim in Notes and Synonyms is true.
2. **Scoped coverage.** For each kanji, are the readings and the common usage it needs for N1 study present or explicitly
   qualified (every metadata reading has a row; source-only or rare readings are marked as such; important words from the
   dictionary families are not wrongly omitted or misdescribed)? Do not demand every related word.
3. **Consistency and quiz safety.** Links resolve to the intended cards; each declared kanji of each word has a card link where
   a card exists; titles are unique and unambiguous as quiz answers; `distractors` are plausible wrong answers that cannot also
   be correct; `quiz_exclusions` cover real synonym or confusable pairs (see `repo\\docs\\confusable-words.md`); `quizOnyomi`
   and `quizKunyomi` are selected from the metadata and each has a linked word example; tags, levels, section order, headings.
4. **Comprehensibility.** Clear to a beginner on a phone: central idea first, jargon explained, kana where needed,
   contrastive natural examples, mnemonic concrete and honest, no wall of text, no padding.

Treat `mechanical-checks.md` as the output of automatic checks, not as a verdict on any facet.

## Evidence

- `evidence\\provenance.json`: pinned dictionary inputs and hashes. Pinned data may differ from today's online dictionaries;
  say so when it matters.
- `evidence\\public-source\\`: retrieved public dictionary text (coordinator retrieval, not your independent lookup).
{extra_lines}- Verify consequential claims yourself against reputable sources (for example JMdict/Jisho, KANJIDIC2/kanjiapi.dev,
  Weblio/Kotobank dictionaries, NHK or established teaching sources). A search snippet is not verification: inspect the
  actual entry, reading, sense and register. Say what you could not verify.

## Report contract (use exactly this shape)

```text
Snapshot: <commit {sha8}; reviewer model as you identify it>
Scope: <files reviewed and the facet you examined deepest>
Verdicts: <for each facet - correctness, scoped coverage, consistency and quiz safety, comprehensibility: CLEAN | NEEDS FIX | UNVERIFIED, one line each, per file where they differ>
Findings: <numbered; severity (blocker/major/minor); facet; file:lines; claim and impact; remedy; evidence; confidence>
Optional: <nonblocking expansion or polish, or none>
Limits: <unverified claims and review limitations, or none>
```

CLEAN means no actionable defect established within the reviewed scope, not exhaustive correctness. Do not label a
consequential unresolved claim CLEAN. No finding quota. Separate defects from optional polish and editorial preference.
Severity reflects demonstrated impact on learning; confidence reflects the strength of evidence.
"""


def read_log(path):
    raw = Path(path).read_bytes()
    if raw.startswith(b"\xff\xfe") or raw.startswith(b"\xfe\xff"):
        text = raw.decode("utf-16", "replace")
    else:
        text = raw.decode("utf-8-sig", "replace")
    keep = [l for l in text.replace("\r\n", "\n").split("\n")
            if not re.match(r"^(At .*char:\d+|\s*\+ .*|\s*FullyQualifiedErrorId.*)$", l)]
    return "\n".join(l for l in keep if l.strip())


def mechanical_text(parts):
    out = ["# Mechanical checks (automatic output, not a review verdict)", ""]
    for title, body in parts:
        out += ["## " + title, "", "```text", body.strip()[-4000:], "```", ""]
    return "\n".join(out)


def cmd_packet(a):
    sha = git("rev-parse", a.sha).strip()
    head = git("rev-parse", "HEAD").strip()
    if sha != head:
        raise SystemExit("candidate %s is not HEAD %s; check it out first" % (sha, head))
    dirty = [l for l in git("status", "--porcelain", "--untracked-files=no").split("\n") if l.strip()]
    if dirty:
        raise SystemExit("tracked changes present: %s" % dirty[:5])
    untracked = [l for l in git("status", "--porcelain", "--untracked-files=all", "--", "kanji", "words", "strokes",
                                "docs", "manifest.json").split("\n") if l.strip()]
    if untracked:
        raise SystemExit("untracked teaching/doc files present: %s" % untracked[:5])
    out = Path(a.out)
    if out.exists():
        raise SystemExit("packet dir exists: %s" % out)
    info = collect(a.base, sha)
    out.mkdir(parents=True)
    # snapshot + diffs
    for p, st in info["changed"].items():
        if st == "D":
            continue
        dst = out / "snapshot" / p
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((REPO / p).read_bytes())
        if st == "M":
            dd = out / "diffs"
            dd.mkdir(exist_ok=True)
            (dd / (p.replace("/", "__") + ".diff")).write_text(
                git("diff", "--no-color", info["base"], sha, "--", p), encoding="utf-8")
    modified = [p for p, st in info["changed"].items() if st == "M" and p.endswith(".md")]
    # evidence
    build_evidence(info, out / "evidence", web=not a.no_web)
    # repo context
    for d in ("kanji", "words"):
        shutil.copytree(REPO / d, out / "repo" / d)
    for f in ("docs/content-format.md", "docs/confusable-words.md", "docs/jlpt-levels.md", "README.md"):
        dst = out / "repo" / f
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes((REPO / f).read_bytes())
    kc, wc = load_cards()
    (out / "titles").mkdir()
    (out / "titles" / "kanji-titles.tsv").write_text(
        "kanji\ttitle\tjlpt\n" + "".join("%s\t%s\t%s\n" % (k, fm.get("title"), fm.get("jlpt"))
                                         for k, (fm, b) in sorted(kc.items()) if fm), encoding="utf-8")
    (out / "titles" / "word-titles.tsv").write_text(
        "word\treading\ttitle\ttype\tjlpt\n" + "".join(
            "%s\t%s\t%s\t%s\t%s\n" % (w, fm.get("reading"), fm.get("title"), fm.get("type"), fm.get("jlpt", ""))
            for w, (fm, b) in sorted(wc.items()) if fm), encoding="utf-8")
    # rubric
    (out / "rubric" / "agents").mkdir(parents=True)
    shutil.copy2(REPO / ".github/copilot-instructions.md", out / "rubric" / "copilot-instructions.md")
    for f in sorted((REPO / ".github" / "agents").glob("*.agent.md")):
        shutil.copy2(f, out / "rubric" / "agents" / f.name)
    # mechanical checks
    parts = []
    for spec in a.check or []:
        name, _, path = spec.partition("=")
        body = read_log(path) if Path(path).is_file() else "(missing %s)" % path
        if "unit" in name.lower():
            body = "\n".join(body.split("\n")[-3:])
        parts.append((name, body))
    (out / "mechanical-checks.md").write_text(mechanical_text(parts), encoding="utf-8")
    extra_lines = ""
    for spec in a.extra or []:
        src, _, rest = spec.partition("=")
        dest, _, desc = rest.partition(":")
        dst = out / dest
        if dst.exists():
            raise SystemExit("extra destination exists: %s" % dest)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        extra_lines += "- `%s`: %s\n" % (dest.replace("/", "\\"), desc)
    (out / "INSTRUCTIONS.md").write_text(INSTR.format(
        batch=a.batch, sha8=sha[:8], kanji=" ".join(info["new_kanji"]) or "none",
        new_words=" ".join(info["new_words"]) or "none", modified=" ".join(modified) or "none",
        extra_lines=extra_lines), encoding="utf-8")
    # manifest
    files = {}
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "packet-manifest.json":
            files[p.relative_to(out).as_posix()] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    (out / "packet-manifest.json").write_text(json.dumps({
        "batch": a.batch, "candidate": sha, "base": info["base"], "builtAt": now_utc(),
        "newKanji": info["new_kanji"], "newWords": info["new_words"], "changed": info["changed"],
        "fileCount": len(files), "files": files}, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(v["bytes"] for v in files.values())
    print("packet %s: %d files, %.1f MB; kanji %s; new words %s" % (
        out, len(files), total / 1e6, info["new_kanji"], info["new_words"]))
    return 0


def cmd_survey(a):
    idx = source_index()
    kc, wc = load_cards()
    jm = build_jmdict_cache()
    lo, hi = (int(x) for x in a.rows.split("-"))
    decl = defaultdict(list)
    for w, (fm, b) in wc.items():
        if fm:
            for c in fm.get("kanji", []):
                decl[c].append(w)
    rows = sorted((r for r in idx.values() if lo <= r["sourceRow"] <= hi and r["kanji"] not in kc),
                  key=lambda r: r["sourceRow"])
    for r in rows:
        k, m = r["kanji"], r["metadata"]
        common = {}
        for eid in jm["char_index"].get(k, []):
            for keb, reb, sc, inf in entry_pairs(jm["entries"][eid]):
                if k in keb and sc >= a.min_score and (keb not in common or common[keb][0] < sc):
                    common[keb] = (sc, reb, eid)
        ranked = sorted(common.items(), key=lambda kv: -kv[1][0])
        have = [w for w, _ in ranked if w in wc]
        miss = ["%s(%s,%d)" % (w, v[1], v[0]) for w, v in ranked if w not in wc][:6]
        print("%4d %s g%s %2ss | decl=%d %s | common=%d have=%d %s | MISSING %s" % (
            r["sourceRow"], k, m["grade"], m["strokes"], len(decl[k]), " ".join(decl[k][:5]), len(ranked),
            len(have), " ".join(have[:5]), " ".join(miss)))
    return 0


def register(sub):
    p = sub.add_parser("survey")
    p.add_argument("--rows", required=True, help="A-B source rows")
    p.add_argument("--min-score", type=int, default=3)
    p.set_defaults(fn=cmd_survey)
    p = sub.add_parser("dossier")
    p.add_argument("kanji", nargs="+")
    p.add_argument("--top", type=int, default=16)
    p.add_argument("--out")
    p.set_defaults(fn=cmd_dossier)
    p = sub.add_parser("evidence")
    p.add_argument("--base", default="origin/main")
    p.add_argument("--sha", default="HEAD")
    p.add_argument("--out", required=True)
    p.add_argument("--no-web", action="store_true")
    p.set_defaults(fn=cmd_evidence)
    p = sub.add_parser("webcheck")
    p.add_argument("kanji", nargs="+")
    p.add_argument("--out", required=True)
    p.set_defaults(fn=cmd_webcheck)
    p = sub.add_parser("packet")
    p.add_argument("--batch", required=True)
    p.add_argument("--base", default="origin/main")
    p.add_argument("--sha", default="HEAD")
    p.add_argument("--out", required=True)
    p.add_argument("--no-web", action="store_true")
    p.add_argument("--check", action="append", help="NAME=path of a check output file to embed")
    p.add_argument("--extra", action="append", help="SRC=DEST:DESCRIPTION extra evidence file listed in INSTRUCTIONS")
    p.set_defaults(fn=cmd_packet)
