import copy
import gzip
import hashlib
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from b130_common import BASE, CHARS, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write

INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4", "entry"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8", "character"),
}
KEYWORDS = {
    "塀": "fence fences wall walls enclosure enclose enclosures barrier barriers boundary boundaries screen screens partition partitions hedge hedges",
    "拍": "clap claps clapping applause beat beats beating strike strikes hit hits tap taps knock knocking rhythm rhythmic music musical time pulse pulses pat pats slapping board boards wood wooden block blocks syllable mora cheer cheers caress stroke strokes rub rubbing squeeze squeezing",
    "桜": "cherry cherries tree trees flower flowers blossom blossoms bloom blooms plant plants shrub shrubs horse meat horsemeat decoy fake shill customer audience planted sakura",
    "皇": "emperor empress imperial king queen monarch sovereign ruler royal august great greatness heaven heavenly god gods divine bright white shining beautiful",
    "耗": "decrease decreases decreasing reduce reduces reduction diminish diminishing consume consumption expend expenditure deplete depletion exhaust exhaustion waste loss lose wear worn abrasion news tidings message rat mouse damage destroy destruction harm harmful bad evil thin barren poor dark darkness disorder confusion confused ruin break broken tear tears weak weaken decline wipe empty hollow perish vanish hate hatred startle surprise astonish separate return change",
}
EXACT_READINGS = {
    "へい", "べい", "かき", "はく", "ひょう", "ひゃく", "うつ", "たたく", "はやし",
    "おふす", "ひむささら", "なづ", "にしる", "こう", "もう", "ぼう",
    "へる", "みだれる", "へらす", "つきる", "なくする", "ついやす", "やぶる",
    "そこなう", "わるい", "うすい", "くらい", "たかへす", "とか", "をぢなし",
    "そこなはる", "ついゆ", "のごふ", "ほろぶ", "きぬ", "うつかす", "つく",
    "おどろく", "そこなふ", "へなる", "かへる", "にくむ", "むなし",
}


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        chunk = self.stream.read(size)
        self.digest.update(chunk)
        return chunk


class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.ignore = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.ignore += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.ignore = max(0, self.ignore - 1)

    def handle_data(self, data):
        if not self.ignore and data.strip():
            self.parts.append(data.strip())


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def output_xml(filename, tag, nodes, source):
    nodes = list(nodes)
    root = ET.Element(tag)
    root.extend(copy.deepcopy(nodes))
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    write(PACKET / filename, raw)
    original = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in nodes}
    actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
    assert original == actual
    return {"source": source, "sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": actual,
            "completeCanonicalEquality": True}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
        assert git("config", "user.email").decode().strip() == "stop-cran@list.ru"
        assert git("config", "user.signingkey").decode().strip() == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
        index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
        community_raw = git("show", f"{BASE}:docs/n1-sources/community-list-20261102.json")
        assert sha(index_raw) == "0d517145b92c19ea4a17ba5aa9ca12c18f408001fdc01f0f7bb1a99659bbe1dd"
        assert sha(community_raw) == "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73"
        index = {r["kanji"]: r for r in json.loads(index_raw)}
        for ch in CHARS:
            row = index[ch]
            assert row["statusAtFreeze"] == "pending" and json.loads(community_raw)[row["sourceRow"] - 1] == ch
            assert not (REPO / row["article"]).exists() and not (REPO / row["strokeFile"]).exists()
        write(PACKET / "source-rows.json", [index[ch] for ch in CHARS])
        supports = {ch: [] for ch in CHARS}
        for path in sorted((REPO / "words").glob("*.md")):
            text = normalized(path)
            match = re.search(r"^kanji: \[([^\]]*)\]$", text, re.M)
            if not match:
                continue
            for ch in CHARS:
                if ch in [p.strip() for p in match.group(1).split(",")]:
                    supports[ch].append(path.stem)
                    dest = PACKET / "baseline-words" / path.name
                    if not dest.exists():
                        write(dest, git("show", f"{BASE}:words/{path.name}"))
        write(PACKET / "selection.json", {"batch": 130, "base": BASE, "members": CHARS,
              "allDeclaredSupportArticles": supports,
              "requiredReciprocalPairs": [[ch, w] for ch in CHARS for w in supports[ch]],
              "selectionReason": "Three genuinely missing members with one existing support each. Split the five-member survey before teaching: 皇 and 桜 have extensive source-positive supplemental/native secondary ranges. The preserved planning-five-001 is not final gate evidence.",
              "deliveredAtBase": 261, "undeliveredAtBase": 967,
              "deferred": {"伯": "row 33: 伯母さん does not establish ハク",
                           "憶": "row 395: unresolved remember/think evidence",
                           "撲": "row 461: 相撲 does not establish ボク"},
              "notSelected": {"桜": "Full Nikkoku native secondary inventory and Jitsu ゆすらうめ require a separate bounded packet; preserve positive survey evidence.",
                              "皇": "Full monolingual supplemental senses/native forms require a separate bounded packet; preserve positive survey evidence.",
                              "衛": "Guard/defend secondary comparison scope not selected for this bounded packet.",
                              "羊": "B129 survey remains historical; not independently resolved here.",
                              "霜": "B129 survey remains historical; not independently resolved here."}})
        old_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
        baseline_paths = [p for p in old_manifest["files"] if p.startswith("kanji/")]
        assert len(baseline_paths) == 1251
        kd, inputs = {}, {}
        filename, compressed_sha, xml_sha, tag = INPUTS["kanjidic2"]
        path = ROOT / "control" / "inputs" / filename
        assert sha(path.read_bytes()) == compressed_sha
        with gzip.open(path, "rb") as stream:
            reader = HashReader(stream, guard)
            context = ET.iterparse(reader, events=("start", "end"))
            _, root = next(context)
            for event, node in context:
                if event == "end" and node.tag == tag:
                    kd[node.findtext("literal")] = copy.deepcopy(node)
                    node.clear()
                    root.clear()
        assert reader.digest.hexdigest() == xml_sha
        inputs["kanjidic2"] = {"filename": filename, "compressedSha256": compressed_sha, "decompressedSha256": xml_sha}
        comparisons, scans = set("古右石"), {}
        for ch in CHARS:
            row = index[ch]
            meanings = [m.text for m in kd[ch].findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
            assert meanings == row["metadata"]["meanings"]
            for kind in ("on", "kun"):
                assert [r.text for r in kd[ch].findall(f"reading_meaning/rmgroup/reading[@r_type='ja_{kind}']")] == row["metadata"][kind + "yomi"]
            literal = set(re.findall("[a-z]+", " ".join(meanings).lower()))
            keywords = set(KEYWORDS[ch].split()) | literal
            scan_rows = []
            for rel in sorted(baseline_paths):
                guard.check()
                char = rel.split("/")[-1][:-3]
                raw = (REPO / rel).read_bytes()
                assert sha(raw.replace(b"\r\n", b"\n")) == old_manifest["files"][rel]
                title = re.search(r"^title: (.+)$", raw.decode().replace("\r\n", "\n"), re.M).group(1)
                full = [m.text for m in kd[char].findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
                hits = sorted(keywords & set(re.findall("[a-z]+", " ".join([title, *full]).lower())))
                scan_rows.append({"kanji": char, "path": rel, "baselineWorkingBytesSha256": sha(raw),
                                  "baselineNormalizedSha256": old_manifest["files"][rel], "title": title,
                                  "completeMeanings": full, "matchedKeywords": hits})
                if hits:
                    comparisons.add(char)
            scans[ch] = {"base": BASE, "kanji": ch, "literalKeywords": sorted(literal), "expandedKeywords": sorted(keywords),
                         "tokenRegex": "[a-z]+", "rows": scan_rows,
                         "matches": [r["kanji"] for r in scan_rows if r["matchedKeywords"]],
                         "limits": "Complete baseline displayed-title/KANJIDIC2 English-meaning scan; expanded semantic keywords are explicit, not exhaustive synonym discovery. Positive supplemental senses may require an appended scan."}
            write(PACKET / "scans" / (ch + ".json"), scans[ch])
        for ch in sorted(comparisons):
            write(PACKET / "comparison-cards" / (ch + ".md"), git("show", f"{BASE}:kanji/{ch}.md"))
        exact = comparisons | set(CHARS) | {w for ws in supports.values() for w in ws}
        filename, compressed_sha, xml_sha, tag = INPUTS["jmdict"]
        path = ROOT / "control" / "inputs" / filename
        assert sha(path.read_bytes()) == compressed_sha
        selected, membership = {}, {}
        with gzip.open(path, "rb") as stream:
            reader = HashReader(stream, guard)
            context = ET.iterparse(reader, events=("start", "end"))
            _, root = next(context)
            for event, node in context:
                if event != "end" or node.tag != tag:
                    continue
                kebs = {k.text for k in node.findall("k_ele/keb")}
                rebs = {r.text for r in node.findall("r_ele/reb")}
                predicates = [f"contains:{ch}" for ch in [*CHARS, "屏"] if any(ch in k for k in kebs)]
                predicates += [f"exact-spelling:{k}" for k in sorted(exact & kebs)]
                predicates += [f"exact-reading:{r}" for r in sorted(EXACT_READINGS & rebs)]
                if predicates:
                    eid = node.findtext("ent_seq")
                    selected[eid], membership[eid] = copy.deepcopy(node), predicates
                node.clear()
                root.clear()
        assert reader.digest.hexdigest() == xml_sha
        inputs["jmdict"] = {"filename": filename, "compressedSha256": compressed_sha, "decompressedSha256": xml_sha}
        outputs = {
            "jmdict-complete-families.xml": output_xml("jmdict-complete-families.xml", "JMdict", selected.values(), "jmdict"),
            "kanjidic2-target-records.xml": output_xml("kanjidic2-target-records.xml", "kanjidic2", [kd[c] for c in CHARS], "kanjidic2"),
            "kanjidic2-comparison-records.xml": output_xml("kanjidic2-comparison-records.xml", "kanjidic2", [kd[c] for c in sorted(comparisons)], "kanjidic2"),
        }
        write(PACKET / "query-membership.json", membership)
        svgs = {}
        for ch in CHARS:
            row = index[ch]
            url = "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/" + row["kanjivgInventory"]["path"]
            with urllib.request.urlopen(url, timeout=30) as response:
                raw = response.read()
            guard.check()
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            assert blob == row["kanjivgInventory"]["sha"] and len(raw) == row["kanjivgInventory"]["size"]
            filename = f"{ord(ch):05x}.svg"
            write(PACKET / "kanjivg" / filename, raw)
            svgs[ch] = {"url": url, "file": "kanjivg/" + filename, "gitBlob": blob, "sha256": sha(raw)}
        write(PACKET / "source-receipt.json", {
            "batch": 130, "base": BASE, "createdAt": datetime.now(timezone.utc).isoformat(),
            "indexSha256": sha(index_raw), "communitySha256": sha(community_raw), "dictionaryInputs": inputs,
            "predicate": "Union of complete families with any spelling containing 塀/拍/耗 or alternative spelling 屏, exact spellings of every baseline comparison and support, and exact supplemental/metadata reading keys enumerated in query-membership.json. Query keys absent from the source remain explicit in the producer. No priority/rarity/sense filtering.",
            "transformation": "Complete parsed/reserialized XML, not raw source slices; canonical field equality with original decompressed stream.",
            "outputs": outputs, "kanjivg": svgs, "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA 4.0.",
            "kanjivgAttribution": "Copyright Ulrich Apel and contributors, CC BY-SA 3.0.", "producerSha256": sha(__import__("pathlib").Path(__file__).read_bytes())})
        pages = []
        original_pages = json.loads((HERE / "external-pages" / "receipt-001.json").read_text(encoding="utf-8"))
        for ch in CHARS:
            for label, url in [("weblio", f"https://www.weblio.jp/content/{ch}"),
                               ("kotobank", f"https://kotobank.jp/word/{ch}")]:
                existing = next(p for p in original_pages if p["character"] == ch and p["provider"] == label)
                assert sha(__import__("pathlib").Path(existing["localRawCapture"]).read_bytes()) == existing["rawSha256"]
                assert sha(__import__("pathlib").Path(existing["localRawCapture"]).with_suffix(".txt").read_bytes()) == existing["textSha256"]
                pages.append(existing)
        write(PACKET / "external-capture-bindings.json", {"captures": pages, "completeCapturesCommitted": False,
              "copyrightBoundary": "Complete external captures remain local; commit only bindings, short attributable excerpts and authored analysis.",
              "limitations": "Mixed multi-dictionary text extraction; image glyphs and formatting may be absent. Provider sections must be distinguished. No inferred glyph identity."})
        for ch in CHARS:
            lines = []
            for eid, node in selected.items():
                if f"contains:{ch}" in membership[eid] or f"exact-spelling:{ch}" in membership[eid]:
                    lines.append(ET.tostring(node, encoding="unicode"))
            write(HERE / f"{ch}-complete-family-readback-002.txt", "\n".join(lines).encode())
        print(json.dumps({"supports": supports, "completeFamilies": len(selected), "comparisonCards": len(comparisons),
                          "scans": {c: [{"kanji": r["kanji"], "title": r["title"], "meanings": r["completeMeanings"]} for r in s["rows"] if r["matchedKeywords"]] for c, s in scans.items()},
                          "pages": [{k: v for k, v in p.items() if k in ("character", "provider", "rawBytes", "error")} for p in pages]}, ensure_ascii=False, indent=2))
    finally:
        write(HERE / "survey-memory-002.json", guard.finish())


if __name__ == "__main__":
    main()
