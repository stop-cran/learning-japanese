import json
import re
import xml.etree.ElementTree as ET
from b130_common import CHARS, HERE, PACKET, normalized, start_guard, write

guard = start_guard()
try:
    membership = json.loads((PACKET / "query-membership.json").read_text(encoding="utf-8"))
    nodes = list(ET.parse(PACKET / "jmdict-complete-families.xml").getroot())
    for ch in CHARS:
        rows = []
        for node in nodes:
            eid = node.findtext("ent_seq")
            if f"contains:{ch}" in membership[eid]:
                rows.append({"id": eid, "predicates": membership[eid],
                             "completeRecord": ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)})
        write(HERE / f"target-{ch}-readback.jsonl", ("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n").encode())
    comparisons = []
    for p in sorted((PACKET / "comparison-cards").glob("*.md")):
        guard.check()
        text = normalized(p)
        ch = p.stem
        comparisons.append({"kanji": ch, "completeCard": text,
                            "completeExactSpellingFamilies": [
                                ET.canonicalize(ET.tostring(n, encoding="unicode"), strip_text=True)
                                for n in nodes if f"exact-spelling:{ch}" in membership[n.findtext("ent_seq")]]})
    for n in range(0, len(comparisons), 16):
        write(HERE / f"comparison-readback-{n//16+1:02}.jsonl",
              ("\n".join(json.dumps(r, ensure_ascii=False) for r in comparisons[n:n+16]) + "\n").encode())
    for ch in CHARS:
        scan = json.loads((PACKET / "scans" / (ch + ".json")).read_text(encoding="utf-8"))
        print(ch, len(scan["matches"]), "".join(scan["matches"]))
    print("Targets:", {ch: sum(f"contains:{ch}" in v for v in membership.values()) for ch in CHARS})
    print("Comparison readbacks:", len(comparisons))
finally:
    write(HERE / "readback-memory-001.json", guard.finish())
