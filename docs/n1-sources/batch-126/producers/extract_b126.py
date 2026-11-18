import copy
import gzip
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from b126_common import BASE, GUARD_SHA, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write

CHAR = "傘"
DISTRACTORS = ["金", "全", "合"]
KEYWORDS = {"umbrella", "umbrellas", "parasol", "parasols", "canopy", "awning", "shelter", "shade", "cover", "protection"}
INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4", "entry"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8", "character"),
}


class Reader:
    def __init__(self, stream, guard):
        import hashlib
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        chunk = self.stream.read(size)
        self.digest.update(chunk)
        return chunk


guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == BASE
    assert not git("status", "--porcelain")
    assert not PACKET.exists()
    index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
    community_raw = git("show", f"{BASE}:docs/n1-sources/community-list-20261102.json")
    assert sha(index_raw) == "0d517145b92c19ea4a17ba5aa9ca12c18f408001fdc01f0f7bb1a99659bbe1dd"
    assert sha(community_raw) == "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73"
    row = next(r for r in json.loads(index_raw) if r["kanji"] == CHAR)
    assert row["sourceRow"] == 70 and row["statusAtFreeze"] == "pending"
    assert json.loads(community_raw)[69] == CHAR
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
    assert support == [CHAR]
    selection = {
        "batch": "126", "baseCommit": BASE, "membership": [{"kanji": CHAR, "sourceRow": 70}],
        "supportArticles": [{"word": CHAR, "reading": "かさ", "path": "words/傘.md", "levelPreserved": 5}],
        "declaringArticlesAtBase": support, "requiredReciprocalPairs": [[CHAR, CHAR]],
        "distractors": DISTRACTORS, "quizOnyomi": [], "quizKunyomi": ["かさ"],
        "rejectedOrDeferred": [
            {"kanji": "伯", "reason": "The only existing support 伯母さん is a whole-word おばさん reading; it does not support ハク practice. Requires a separate lexical/reading packet."},
            {"kanji": "憶", "sourceRow": 395, "reason": "B120 preliminary candidate remains deferred; remember/think comparison complexity is not adjudicated here."},
            {"kanji": "撲", "reason": "Existing 相撲 supports a whole-word すもう reading, not the metadata ボク; broad strike/speak senses require a separate packet."},
        ],
        "scopeReason": "One card, one existing word, one reciprocal pair; fuller-reading candidates surveyed but not admitted.",
    }
    write(PACKET / "selection.json", selection)
    inputs = {}
    records = {}
    for name, (filename, compressed_sha, xml_sha, tag) in INPUTS.items():
        path = ROOT / "control" / "inputs" / filename
        import hashlib
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(65536), b""):
                guard.check()
                digest.update(chunk)
        assert digest.hexdigest() == compressed_sha
        selected = []
        with gzip.open(path, "rb") as stream:
            reader = Reader(stream, guard)
            context = ET.iterparse(reader, events=("start", "end"))
            _, root = next(context)
            for event, node in context:
                if event != "end" or node.tag != tag:
                    continue
                guard.check()
                if name == "jmdict":
                    if any(CHAR in (k.findtext("keb") or "") for k in node.findall("k_ele")):
                        selected.append(copy.deepcopy(node))
                else:
                    selected.append(copy.deepcopy(node))
                node.clear()
                root.clear()
        assert reader.digest.hexdigest() == xml_sha
        records[name] = selected
        inputs[name] = {"filename": filename, "compressedSha256": compressed_sha, "decompressedXmlSha256": xml_sha}

    kd = {r.findtext("literal"): r for r in records["kanjidic2"]}
    target = kd[CHAR]
    group = target.find("reading_meaning/rmgroup")
    meta = row["metadata"]
    assert [r.text for r in group.findall("reading[@r_type='ja_on']")] == meta["onyomi"]
    assert [r.text for r in group.findall("reading[@r_type='ja_kun']")] == meta["kunyomi"]
    assert [r.text for r in group.findall("meaning") if r.get("m_lang") in (None, "en")] == meta["meanings"]
    assert int(target.findtext("misc/stroke_count")) == meta["strokes"]
    assert int(target.findtext("radical/rad_value[@rad_type='classical']")) == meta["radicalNumber"]
    scan_rows, hits = [], []
    for path in sorted((REPO / "kanji").glob("*.md")):
        guard.check()
        raw = path.read_bytes()
        text = raw.decode("utf-8").replace("\r\n", "\n")
        title = re.search(r"^title: (.+)$", text, re.M).group(1)
        record = kd[path.stem]
        meanings = [m.text for m in record.findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
        matched = sorted(KEYWORDS & set(re.findall(r"[a-z]+", " ".join([title, *meanings]).lower())))
        item = {"kanji": path.stem, "path": "kanji/" + path.name, "baselineRawSha256": sha(raw), "title": title, "meanings": meanings, "matchedWords": matched}
        scan_rows.append(item)
        if matched:
            hits.append(path.stem)
    scan = {
        "baseCommit": BASE, "newKanji": CHAR, "newSourceMeanings": meta["meanings"],
        "newTitle": "umbrella; parasol", "literalGlossTokens": ["umbrella"],
        "expandedSemanticKeywords": sorted(KEYWORDS), "caseFoldAndTokenPattern": "[a-z]+",
        "scannedBaselineCards": len(scan_rows), "matches": hits, "rows": scan_rows,
        "producerSha256": sha(open(__file__, "rb").read()),
        "limits": "Actual complete baseline title/KANJIDIC2 English-gloss scan, not exhaustive semantic synonym discovery. Related keywords intentionally overinclude English polysemy; dispositions are separate.",
    }
    write(PACKET / "baseline-gloss-scan.json", scan)
    comparisons = sorted(set(DISTRACTORS + hits))
    for ch in comparisons:
        write(PACKET / "comparison-cards" / (ch + ".md"), git("show", f"{BASE}:kanji/{ch}.md"))
    for name, chosen in [("jmdict-selected-records.xml", records["jmdict"]), ("kanjidic2-selected-records.xml", [target]), ("kanjidic2-comparison-records.xml", [kd[ch] for ch in comparisons])]:
        root = ET.Element("JMdict" if name.startswith("jmdict") else "kanjidic2")
        for r in chosen:
            root.append(r)
        ET.indent(root, space="  ")
        raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
        write(PACKET / name, raw)
        inputs["jmdict" if name.startswith("jmdict") else "kanjidic2"].setdefault("outputs", {})[name] = {
            "sha256": sha(raw), "bytes": len(raw), "records": [r.findtext("ent_seq") or r.findtext("literal") for r in chosen],
        }
    svg_rel = row["kanjivgInventory"]["path"]
    url = f"https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/{svg_rel}"
    with urllib.request.urlopen(url, timeout=30) as response:
        svg = response.read()
    guard.check()
    blob = hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    write(PACKET / "05098.svg", svg)
    write(PACKET / "source-receipt.json", {
        "batch": "126", "baseCommit": BASE, "createdAt": datetime.now(timezone.utc).isoformat(),
        "membership": {"sourceIndexSha256": sha(index_raw), "communitySha256": sha(community_raw), "row": 70, "kanji": CHAR},
        "dictionaryInputs": inputs, "completeJmdictFamilySelection": "Every full entry having 傘 in any k_ele/keb; all spelling, reading and sense restrictions retained.",
        "transformation": "Complete parsed/reserialized XML records, not raw compressed-file slices. No priority-based omission or rarity inference.",
        "kanjivg": {"revision": "70a0b7ae0c18ceb5cb358274b029cce0234a43bc", "url": url, "path": svg_rel, "gitBlob": blob, "sha256": sha(svg), "bytes": len(svg)},
        "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA 4.0.",
        "kanjivgAttribution": "Copyright Ulrich Apel and contributors, CC BY-SA 3.0.",
        "producerSha256": sha(open(__file__, "rb").read()), "guardSha256": GUARD_SHA,
        "files": {p.relative_to(PACKET).as_posix(): {"sha256": sha(p.read_bytes()), "bytes": p.stat().st_size} for p in sorted(PACKET.rglob("*")) if p.is_file()},
    })
    print(json.dumps({"selectedJmdictFamilies": len(records["jmdict"]), "scanCards": len(scan_rows), "scanMatches": hits, "comparisons": comparisons, "metadata": meta, "nanori": [n.text for n in target.findall("reading_meaning/nanori")]}, ensure_ascii=False))
finally:
    write(HERE / "extraction-memory-001.json", guard.finish())
