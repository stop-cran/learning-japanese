import copy
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b130_common import BASE, HERE, REPO, ROOT, git, normalized, sha, start_guard, write
from survey_b130 import HashReader, INPUTS, canonical

PARENT = "ce1b5c895fac90852143f322a115c2de4e768e20"
OUT = REPO / "docs" / "n1-sources" / "batch-130-reconciliation"
LOCAL = HERE / "reconciliation-001"
COMPARISONS = "擦摩削便突文信疲磨研欠乏枯下落退用鳴響勉勇乗記識筆城書音"
EXACT = set(COMPARISONS) | {
    "便り", "疲れる", "疲らす", "疲れ", "磨く", "磨る", "研ぐ", "研磨", "欠ける", "欠く",
    "乏しい", "貧乏", "枯れる", "枯らす", "下げる", "下がる", "下る", "落ちる", "落とす",
    "退く", "退ける", "用いる", "鳴る", "鳴らす", "鳴く", "響く", "響き", "勉める", "努める",
    "勇む", "勇ましい", "乗る", "乗り", "乗せる", "記す", "識す", "城壁", "音耗", "音信",
    "拍", "拍つ", "拍手", "拍子", "耗", "消耗", "摩耗", "磨耗", "擦る", "擦れる", "摩る",
    "摩する", "削る", "削ぐ", "削減", "突く", "囃す", "はやす", "囃し", "はやし", "塀"
}


def emit(name, tag, nodes, source):
    root = ET.Element(tag)
    root.extend(copy.deepcopy(nodes))
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    hashes = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in nodes}
    actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
    assert hashes == actual
    write(OUT / name, raw)
    return {"source": source, "sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": hashes,
            "completeCanonicalEquality": True}


guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    inputs, outputs, membership = {}, {}, {}
    card_bindings = {}
    for ch in COMPARISONS:
        raw = git("show", f"{PARENT}:kanji/{ch}.md")
        assert raw.replace(b"\r\n", b"\n").decode() == normalized(REPO / "kanji" / (ch + ".md"))
        write(OUT / "comparison-cards" / (ch + ".md"), raw)
        card_bindings[ch] = {"path": f"comparison-cards/{ch}.md", "sha256": sha(raw)}
    original = {}
    initial = REPO / "docs" / "n1-sources" / "batch-130"
    for name in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml", "jmdict-final-families.xml"):
        for node in ET.parse(initial / name).getroot():
            key = node.findtext("ent_seq")
            value = sha(canonical(node).encode())
            if key in original:
                assert original[key] == value
            original[key] = value
    retained = []
    counts = {"exact-spelling:" + q: 0 for q in sorted(EXACT)}
    for source in ("jmdict", "kanjidic2"):
        filename, compressed, decompressed, tag = INPUTS[source]
        path = ROOT / "control" / "inputs" / filename
        assert sha(path.read_bytes()) == compressed
        nodes, scanned = [], 0
        with gzip.open(path, "rb") as stream:
            reader = HashReader(stream, guard)
            context = ET.iterparse(reader, events=("start", "end"))
            _, root = next(context)
            for event, node in context:
                if event != "end" or node.tag != tag:
                    continue
                scanned += 1
                if source == "jmdict":
                    key = node.findtext("ent_seq")
                    predicates = ["exact-spelling:" + s for s in sorted(
                        EXACT & {e.text for e in node.findall("k_ele/keb")})]
                    if predicates:
                        nodes.append(copy.deepcopy(node))
                        membership[key] = predicates
                        for p in predicates:
                            counts[p] += 1
                        if key in original:
                            assert sha(canonical(node).encode()) == original[key], key
                elif node.findtext("literal") in set(COMPARISONS + "塀拍耗"):
                    nodes.append(copy.deepcopy(node))
                node.clear()
                root.clear()
        assert reader.digest.hexdigest() == decompressed
        inputs[source] = {"filename": filename, "compressedSha256": compressed,
                          "decompressedSha256": decompressed, "recordsScanned": scanned}
        name = "jmdict-families.xml" if source == "jmdict" else "kanjidic2-records.xml"
        outputs[name] = emit(name, "JMdict" if source == "jmdict" else "kanjidic2", nodes, source)
        if source == "jmdict":
            retained = nodes
    write(OUT / "query-membership.json", membership)
    write(OUT / "source-receipt.json", {
        "parent": PARENT, "publishedBase": BASE, "inputs": inputs, "outputs": outputs,
        "selectors": {"exactSpellings": sorted(EXACT), "characterLiterals": sorted(set(COMPARISONS + "塀拍耗")),
                      "queryCountsIncludingZero": counts},
        "transformation": "Complete parsed/reserialized records, not raw slices. Exact input hashes, full stream, canonical equality before/after serialization, complete original-family duplicate checks; no spelling/priority/sense filtering.",
        "comparisonCards": card_bindings, "membershipSha256": sha((OUT / "query-membership.json").read_bytes()),
        "attribution": "Copyright J. W. Breen and EDRDG, JMdict and KANJIDIC2 CC BY-SA 4.0, https://www.edrdg.org/",
        "producerSha256": sha(Path(__file__).read_bytes())})
    for i in range(0, len(retained), 10):
        lines = []
        for node in retained[i:i + 10]:
            key = node.findtext("ent_seq")
            lines.append(json.dumps({"id": key, "selectors": membership[key],
                                     "completeRecord": ET.tostring(node, encoding="unicode")}, ensure_ascii=False))
        write(LOCAL / f"complete-families-{i // 10 + 1:02}.jsonl", ("\n".join(lines) + "\n").encode())
    write(LOCAL / "character-inventories.jsonl", ("\n".join(
        json.dumps({"character": n.findtext("literal"), "completeRecord": ET.tostring(n, encoding="unicode")}, ensure_ascii=False)
        for n in ET.parse(OUT / "kanjidic2-records.xml").getroot()) + "\n").encode())
    print(json.dumps({"families": len(retained), "characters": len(outputs["kanjidic2-records.xml"]["canonicalRecordHashes"]),
                      "comparisons": len(card_bindings), "readbacks": (len(retained) + 9) // 10,
                      "zeroQueries": [k for k, v in counts.items() if not v]}, ensure_ascii=False))
finally:
    write(LOCAL / "source-memory-001.json", guard.finish())
