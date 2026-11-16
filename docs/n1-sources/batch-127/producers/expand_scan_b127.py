import copy
import gzip
import json
import re
import xml.etree.ElementTree as ET
from b127_common import BASE, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write
from extract_b127 import HashReader, KEYWORDS

KEYWORDS = KEYWORDS | {
    "keep", "preserve", "contain", "put", "gather", "collect", "depository",
    "magazine", "elevator", "silo", "repository", "prison", "jail", "gaol",
    "detention", "imprison", "imprisonment", "captive", "perish", "perishing",
    "ruin", "ruined", "destroy", "collapse", "fragile", "fragility", "brittle",
}

guard = start_guard()
try:
    kd = {}
    receipt = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))
    with gzip.open(ROOT / "control" / "inputs" / receipt["dictionaryInputs"]["kanjidic2"]["filename"], "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event == "end" and node.tag == "character":
                kd[node.findtext("literal")] = copy.deepcopy(node)
                node.clear()
                root.clear()
    assert reader.digest.hexdigest() == receipt["dictionaryInputs"]["kanjidic2"]["decompressedXmlSha256"]
    original = json.loads((PACKET / "baseline-gloss-scan.json").read_text(encoding="utf-8"))
    rows, hits = [], []
    for item in original["rows"]:
        guard.check()
        item = dict(item)
        item["matchedWords"] = sorted(KEYWORDS & set(re.findall(r"[a-z]+", " ".join([item["title"], *item["meanings"]]).lower())))
        rows.append(item)
        if item["matchedWords"]:
            hits.append(item["kanji"])
    write(PACKET / "baseline-gloss-scan-002.json", {
        **{k: v for k, v in original.items() if k not in ("rows", "matches", "expandedSemanticKeywords", "producerSha256")},
        "extends": "baseline-gloss-scan.json", "expandedSemanticKeywords": sorted(KEYWORDS),
        "reason": "Inspected Kanjipedia sudden/hurried sense and Jitsu direct store/prison senses and quoted old-dictionary readings warrant an overinclusive second scan. JMdict standalone くら also supplies magazine/depository/elevator. Compound-only glosses are not automatically character senses.",
        "rows": rows, "matches": hits, "producerSha256": sha(open(__file__, "rb").read()),
    })
    comparisons = sorted(set(hits) | {"金", "全", "合"})
    xml = ET.Element("kanjidic2")
    for ch in comparisons:
        guard.check()
        path = PACKET / "comparison-cards" / (ch + ".md")
        if not path.exists():
            write(path, git("show", f"{BASE}:kanji/{ch}.md"))
        xml.append(kd[ch])
    ET.indent(xml, space="  ")
    raw = ET.tostring(xml, encoding="utf-8", xml_declaration=True) + b"\n"
    write(PACKET / "kanjidic2-expanded-comparison-records.xml", raw)
    write(PACKET / "expanded-scan-receipt.json", {
        "baseCommit": BASE, "sourceReceipt": "source-receipt.json",
        "decompressedXmlSha256": reader.digest.hexdigest(), "records": comparisons,
        "outputSha256": sha(raw), "outputBytes": len(raw), "completeParsedReserializedRecords": True,
    })
    for row in rows:
        if row["matchedWords"]:
            print(json.dumps(row, ensure_ascii=False))
finally:
    write(HERE / "expanded-scan-memory-001.json", guard.finish())
