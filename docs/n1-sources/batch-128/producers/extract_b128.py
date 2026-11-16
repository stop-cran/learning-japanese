import copy
import gzip
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from b128_common import BASE, GUARD_SHA, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write

CHAR = "唇"
DISTRACTORS = ["古", "右", "石"]
KEYWORDS = {
    "lip", "lips", "labial", "mouth", "mouths", "rim", "rims", "edge", "edges",
    "border", "borders", "petal", "petals", "flower", "flowers", "blossom",
    "blossoms", "startle", "startled", "surprise", "surprised", "astonish",
    "astonished", "fright", "frighten", "frightened", "fear", "dread",
    "tremble", "trembling", "tremor", "shake", "shaking", "quiver", "shudder",
}
QUERIES = {"口", "口縁", "縁", "縁取る", "端", "花", "花弁", "花びら", "驚く", "驚かす", "驚かせる", "震える", "震う", "振るう", "振るえる", "恐れる", "恐ろしい"}
INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4", "entry"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8", "character"),
}


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        chunk = self.stream.read(size)
        self.digest.update(chunk)
        return chunk


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []

    def handle_data(self, data):
        if data.strip():
            self.parts.append(data.strip())


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        assert git("remote", "get-url", "origin").decode().strip() == "https://github.com/stop-cran/learning-japanese.git"
        assert not PACKET.exists()
        index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
        community_raw = git("show", f"{BASE}:docs/n1-sources/community-list-20261102.json")
        assert sha(index_raw) == "0d517145b92c19ea4a17ba5aa9ca12c18f408001fdc01f0f7bb1a99659bbe1dd"
        assert sha(community_raw) == "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73"
        row = next(r for r in json.loads(index_raw) if r["kanji"] == CHAR)
        assert row["sourceRow"] == 159 and row["statusAtFreeze"] == "pending"
        assert json.loads(community_raw)[158] == CHAR
        assert not (REPO / row["article"]).exists() and not (REPO / row["strokeFile"]).exists()
        write(PACKET / "source-row.json", row)
        support = []
        for path in sorted((REPO / "words").glob("*.md")):
            guard.check()
            text = path.read_text(encoding="utf-8")
            match = re.search(r"^kanji: \[([^\]]*)\]$", text, re.M)
            if match and CHAR in [p.strip() for p in match.group(1).split(",")]:
                support.append(path.stem)
                write(PACKET / ("baseline-" + path.name), git("show", f"{BASE}:words/{path.name}"))
        assert support == ["唇"], support
        write(PACKET / "selection.json", {
            "batch": "128", "baseCommit": BASE,
            "membership": [{"kanji": CHAR, "sourceRow": 159}],
            "supportArticles": [{"word": "唇", "reading": "くちびる", "path": "words/唇.md", "levelPreserved": 2}],
            "declaringArticlesAtBase": support, "requiredReciprocalPairs": [[CHAR, "唇"]],
            "distractors": DISTRACTORS, "quizOnyomi": [], "quizKunyomi": ["くちびる"],
            "rejectedOrDeferred": [
                {"kanji": "伯", "sourceRow": 33, "reason": "伯母さん does not establish ハク."},
                {"kanji": "憶", "sourceRow": 395, "reason": "Deferred; remember/think comparisons need their own packet."},
                {"kanji": "撲", "sourceRow": 461, "reason": "相撲 does not establish ボク."},
            ],
            "scopeReason": "One missing member with one existing support; stop early for complete secondary-sense/reading comparisons.",
            "necessaryProseException": "Remove only the now-false no-card sentence from words/唇.md when wrapping its substantive introduction; retain all other prose and metadata.",
        })
        inputs, records, originals = {}, {}, {}
        memberships = {q: [] for q in sorted(QUERIES)}
        for name, (filename, compressed_sha, xml_sha, tag) in INPUTS.items():
            path = ROOT / "control" / "inputs" / filename
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for chunk in iter(lambda: stream.read(65536), b""):
                    guard.check()
                    digest.update(chunk)
            assert digest.hexdigest() == compressed_sha
            selected, canonical_records = [], {}
            with gzip.open(path, "rb") as stream:
                reader = HashReader(stream, guard)
                context = ET.iterparse(reader, events=("start", "end"))
                _, root = next(context)
                for event, node in context:
                    if event != "end" or node.tag != tag:
                        continue
                    guard.check()
                    if name == "jmdict":
                        eid = node.findtext("ent_seq")
                        kebs = {k.text for k in node.findall("k_ele/keb")}
                        matched = QUERIES & kebs
                        for query in matched:
                            memberships[query].append(eid)
                        admit = bool(matched) or any("唇" in k or "脣" in k for k in kebs)
                    else:
                        eid, admit = node.findtext("literal"), True
                    if admit:
                        selected.append(copy.deepcopy(node))
                        canonical_records[eid] = sha(canonical(node).encode())
                    node.clear()
                    root.clear()
            assert reader.digest.hexdigest() == xml_sha
            records[name], originals[name] = selected, canonical_records
            inputs[name] = {"filename": filename, "compressedSha256": compressed_sha, "decompressedXmlSha256": xml_sha}
        kd = {r.findtext("literal"): r for r in records["kanjidic2"]}
        target, meta = kd[CHAR], row["metadata"]
        group = target.find("reading_meaning/rmgroup")
        assert [r.text for r in group.findall("reading[@r_type='ja_on']")] == meta["onyomi"]
        assert [r.text for r in group.findall("reading[@r_type='ja_kun']")] == meta["kunyomi"]
        assert [r.text for r in group.findall("meaning") if r.get("m_lang") in (None, "en")] == meta["meanings"]
        assert int(target.findtext("misc/stroke_count")) == meta["strokes"]
        assert int(target.findtext("radical/rad_value[@rad_type='classical']")) == meta["radicalNumber"]
        literal_tokens = set(re.findall(r"[a-z]+", " ".join(meta["meanings"]).lower()))
        assert literal_tokens <= KEYWORDS
        scan_rows, hits = [], []
        for path in sorted((REPO / "kanji").glob("*.md")):
            guard.check()
            raw = git("show", f"{BASE}:kanji/{path.name}")
            text = raw.decode("utf-8").replace("\r\n", "\n")
            title = re.search(r"^title: (.+)$", text, re.M).group(1)
            meanings = [m.text for m in kd[path.stem].findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
            matched = sorted(KEYWORDS & set(re.findall(r"[a-z]+", " ".join([title, *meanings]).lower())))
            scan_rows.append({"kanji": path.stem, "path": "kanji/" + path.name, "baselineGitBytesSha256": sha(raw), "title": title, "meanings": meanings, "matchedWords": matched})
            if matched:
                hits.append(path.stem)
        write(PACKET / "baseline-gloss-scan.json", {
            "baseCommit": BASE, "newKanji": CHAR, "newSourceMeanings": meta["meanings"], "newTitle": "lips",
            "literalGlossTokens": sorted(literal_tokens), "expandedSemanticKeywords": sorted(KEYWORDS),
            "caseFoldAndTokenPattern": "[a-z]+", "scannedBaselineCards": len(scan_rows),
            "matches": hits, "rows": scan_rows, "producerSha256": sha(open(__file__, "rb").read()),
            "limits": "Actual whole-baseline title and complete KANJIDIC2 English-meaning scan; includes potential secondary edge/petal/surprise/trembling senses and English polysemy, not exhaustive synonym discovery.",
        })
        comparisons = sorted(set(DISTRACTORS + hits))
        for ch in comparisons:
            write(PACKET / "comparison-cards" / (ch + ".md"), git("show", f"{BASE}:kanji/{ch}.md"))
        source_checks = {}
        for name, label, chosen in [
            ("jmdict-selected-records.xml", "jmdict", records["jmdict"]),
            ("kanjidic2-selected-records.xml", "kanjidic2", [target]),
            ("kanjidic2-comparison-records.xml", "kanjidic2", [kd[ch] for ch in comparisons]),
        ]:
            root = ET.Element("JMdict" if label == "jmdict" else "kanjidic2")
            root.extend(copy.deepcopy(chosen))
            ET.indent(root, space="  ")
            raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
            write(PACKET / name, raw)
            tag = INPUTS[label][3]
            actual = {(n.findtext("ent_seq") or n.findtext("literal")): sha(canonical(n).encode()) for n in ET.fromstring(raw).findall(tag)}
            expected = {(n.findtext("ent_seq") or n.findtext("literal")): originals[label][n.findtext("ent_seq") or n.findtext("literal")] for n in chosen}
            assert actual == expected
            source_checks[name] = {"records": len(chosen), "completeCanonicalRecordEqualityToInput": True, "canonicalRecordHashes": actual}
            inputs[label].setdefault("outputs", {})[name] = {"sha256": sha(raw), "bytes": len(raw), "records": list(actual)}
        write(PACKET / "complete-source-verification.json", source_checks)
        write(PACKET / "comparison-query-membership.json", memberships)
        svg_rel = row["kanjivgInventory"]["path"]
        url = f"https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/{svg_rel}"
        with urllib.request.urlopen(url, timeout=30) as response:
            svg = response.read()
        guard.check()
        blob = hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest()
        assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
        write(PACKET / "05507.svg", svg)
        write(PACKET / "source-receipt.json", {
            "batch": "128", "baseCommit": BASE, "createdAt": datetime.now(timezone.utc).isoformat(),
            "membership": {"sourceIndexSha256": sha(index_raw), "communitySha256": sha(community_raw), "row": 159, "kanji": CHAR},
            "dictionaryInputs": inputs,
            "completeJmdictFamilySelection": "Every complete entry with 唇 or 脣 in any k_ele/keb, plus complete exact-keb comparison families from comparison-query-membership.json.",
            "transformation": "Complete parsed/reserialized XML records, not raw compressed-file slices. All spelling, reading and sense restrictions retained. No priority/rarity filtering.",
            "kanjivg": {"revision": "70a0b7ae0c18ceb5cb358274b029cce0234a43bc", "url": url, "path": svg_rel, "gitBlob": blob, "sha256": sha(svg), "bytes": len(svg)},
            "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA 4.0.",
            "kanjivgAttribution": "Copyright Ulrich Apel and contributors, CC BY-SA 3.0.",
            "producerSha256": sha(open(__file__, "rb").read()), "guardSha256": GUARD_SHA,
            "files": {p.relative_to(PACKET).as_posix(): {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size} for p in sorted(PACKET.rglob("*")) if p.is_file()},
        })
        print(json.dumps({"selectedJmdictFamilies": len(records["jmdict"]), "scanCards": len(scan_rows), "scanMatches": hits, "comparisons": comparisons, "metadata": meta, "nanori": [n.text for n in target.findall("reading_meaning/nanori")]}, ensure_ascii=False))
    finally:
        write(HERE / "extraction-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
