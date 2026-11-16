import copy
import gzip
import json
import re
import xml.etree.ElementTree as ET
from b126_common import BASE, HERE, PACKET, ROOT, REPO, git, sha, start_guard, write

guard = start_guard()
try:
    original = json.loads((PACKET / "baseline-gloss-scan.json").read_text(encoding="utf-8"))
    jm = ET.parse(PACKET / "jmdict-selected-records.xml")
    single = [e for e in jm.findall("entry") if any(k.text == "傘" for k in e.findall("k_ele/keb"))]
    glosses = [g.text for e in single for g in e.findall("sense/gloss")]
    stopwords = {"a", "an", "the", "of", "or", "and", "like", "something"}
    tokens = set(re.findall("[a-z]+", " ".join(glosses).lower())) - stopwords
    tokens |= set(original["expandedSemanticKeywords"]) | {"caps", "hats", "shapes", "covering", "covers", "sunshade"}
    rows = []
    for row in original["rows"]:
        guard.check()
        item = dict(row)
        item["matchedWords"] = sorted(tokens & set(re.findall("[a-z]+", " ".join([row["title"], *row["meanings"]]).lower())))
        rows.append(item)
    hits = [r["kanji"] for r in rows if r["matchedWords"]]
    write(PACKET / "baseline-gloss-scan-002.json", {
        "baseCommit": BASE, "extends": {"file": "baseline-gloss-scan.json", "sha256": sha((PACKET / "baseline-gloss-scan.json").read_bytes())},
        "newKanji": "傘", "singleCharacterJmdictEntries": [e.findtext("ent_seq") for e in single],
        "allSingleCharacterJmdictGlosses": glosses, "sourceMeanings": ["umbrella"],
        "meaningfulTokenPolicy": "Every content token from all single-headword JMdict senses plus KANJIDIC2 English meanings and title, with explicit semantic expansion; no stemming or transitive guards.",
        "omittedFunctionTokens": sorted(stopwords), "scanTokens": sorted(tokens),
        "scannedBaselineCards": len(rows), "matches": hits, "rows": rows,
        "producerSha256": sha(open(__file__, "rb").read()),
        "limits": "Retains actual scan output for all baseline cards. Token overlap is a comparison trigger, not synonymy. Whole-compound senses such as affiliation in 傘下 are not promoted to character glosses.",
    })
    selected = []
    with gzip.open(ROOT / "control" / "inputs" / "n1-planning-kanjidic2.xml.gz", "rb") as stream:
        context = ET.iterparse(stream, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event != "end" or node.tag != "character":
                continue
            guard.check()
            ch = node.findtext("literal")
            if ch in hits:
                selected.append(copy.deepcopy(node))
            node.clear()
            root.clear()
    root = ET.Element("kanjidic2")
    for record in selected:
        root.append(record)
    ET.indent(root, space="  ")
    write(PACKET / "kanjidic2-expanded-comparison-records.xml", ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n")
    for ch in hits:
        path = PACKET / "comparison-cards" / (ch + ".md")
        if not path.exists():
            write(path, git("show", f"{BASE}:kanji/{ch}.md"))
    print(json.dumps({"glosses": glosses, "scanTokens": sorted(tokens), "matches": [r for r in rows if r["matchedWords"]]}, ensure_ascii=False, indent=2))
finally:
    write(HERE / "expanded-scan-memory-001.json", guard.finish())
