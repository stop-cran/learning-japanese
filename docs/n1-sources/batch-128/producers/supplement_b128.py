import copy
import gzip
import json
import re
import xml.etree.ElementTree as ET
from b128_common import BASE, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write
from extract_b128 import HashReader, INPUTS, canonical

EXTRA = {
    "margin", "margins", "brim", "brink", "fringe", "boundary", "boundaries",
    "vicinity", "neighborhood", "neighbourhood", "bank", "banks", "shore",
    "shores", "side", "sides", "perimeter", "outskirts",
    "sound", "sounds", "voice", "voices", "speech", "speak", "speaking",
    "talk", "talking", "consonant", "consonants", "labium", "labrum",
    "shock", "shocked", "shiver", "shivering", "quake", "quaking",
}

guard = start_guard()
try:
    original = json.loads((PACKET / "baseline-gloss-scan.json").read_text(encoding="utf-8"))
    keywords = set(original["expandedSemanticKeywords"]) | EXTRA
    rows = []
    for row in original["rows"]:
        item = dict(row)
        item["matchedWords"] = sorted(keywords & set(re.findall(r"[a-z]+", " ".join([row["title"], *row["meanings"]]).lower())))
        rows.append(item)
    hits = [r["kanji"] for r in rows if r["matchedWords"]]
    write(PACKET / "baseline-gloss-scan-002.json", {
        **{k: v for k, v in original.items() if k not in ("rows", "matches", "expandedSemanticKeywords", "producerSha256")},
        "expandedSemanticKeywords": sorted(keywords), "rows": rows, "matches": hits,
        "producerSha256": sha(open(__file__, "rb").read()),
        "expansionReason": "Jitsu's historical 脣=ホトリ gloss and surprise branch, Kanjipedia's mouth-trembling account, and Nikkoku's しん as lip/labial-consonant noun. These source-positive branches are not dismissed by rarity or dictionary differences.",
    })
    added = set(hits) - set(original["matches"])
    for char in sorted(added):
        write(PACKET / "comparison-cards" / (char + ".md"), git("show", f"{BASE}:kanji/{char}.md"))
    path = ROOT / "control" / "inputs" / INPUTS["kanjidic2"][0]
    selected, hashes = [], {}
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event != "end" or node.tag != "character":
                continue
            char = node.findtext("literal")
            if char in added:
                selected.append(copy.deepcopy(node))
                hashes[char] = sha(canonical(node).encode())
            node.clear()
            root.clear()
    assert reader.digest.hexdigest() == INPUTS["kanjidic2"][2]
    assert hashes.keys() == added
    root = ET.Element("kanjidic2")
    root.extend(selected)
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    write(PACKET / "kanjidic2-expanded-comparison-records.xml", raw)
    assert {n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw).findall("character")} == hashes
    write(PACKET / "supplement-receipt.json", {
        "base": BASE, "source": INPUTS["kanjidic2"][0], "compressedInputSha256": INPUTS["kanjidic2"][1],
        "decompressedInputSha256": reader.digest.hexdigest(),
        "output": "kanjidic2-expanded-comparison-records.xml", "outputSha256": sha(raw),
        "completeCanonicalRecordHashes": hashes, "transformation": "Complete parsed/reserialized records, not raw source slices.",
        "scanOutputSha256": sha((PACKET / "baseline-gloss-scan-002.json").read_bytes()),
        "producerSha256": sha(open(__file__, "rb").read()),
    })
    print(json.dumps({"scanMatches": [{"kanji": r["kanji"], "title": r["title"], "meanings": r["meanings"], "matched": r["matchedWords"]} for r in rows if r["matchedWords"]], "added": sorted(added)}, ensure_ascii=False, indent=2))
finally:
    write(HERE / "supplement-memory-001.json", guard.finish())
