import json
import re
import xml.etree.ElementTree as ET
from b129_common import HERE, PACKET, sha, start_guard, write

guard = start_guard()
try:
    lines = []
    for path in sorted((PACKET / "comparison-cards").glob("*.md")):
        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        lines += ["===== " + path.stem + " =====", re.search("^title: (.*)$", text, re.M).group(0)]
        for heading in ("Meaning and origin", "Notes"):
            match = re.search(r"^## " + heading + r"\n(.*?)(?=^## |\Z)", text, re.M | re.S)
            if match:
                lines += ["## " + heading, match.group(1).strip()]
    write(HERE / "comparison-semantic-readback.txt", ("\n".join(lines) + "\n").encode())
    lines, records = [], {}
    for filename in ("jmdict-complete-families.xml", "jmdict-supplemental-comparisons-002.xml"):
        for el in ET.parse(PACKET / filename).findall("entry"):
            eid = el.findtext("ent_seq")
            if eid in records:
                assert ET.canonicalize(ET.tostring(records[eid], encoding="unicode"), strip_text=True) == ET.canonicalize(ET.tostring(el, encoding="unicode"), strip_text=True)
            records[eid] = el
    for eid, el in records.items():
        data = {"id": eid, "k": [{c.tag: c.text for c in k if c.tag != "ke_pri"} for k in el.findall("k_ele")],
                "r": [{"reading": r.findtext("reb"), "restrictions": [v.text for v in r.findall("re_restr")], "flags": [v.text for v in r.findall("re_inf")], "noKanji": r.find("re_nokanji") is not None} for r in el.findall("r_ele")],
                "s": [{tag: [v.text for v in s.findall(tag)] for tag in ("gloss", "misc", "field", "stagk", "stagr", "s_inf", "xref")} for s in el.findall("sense")]}
        lines.append(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    write(HERE / "complete-source-readback-002.txt", ("\n".join(lines) + "\n").encode())
    write(PACKET / "readback-bindings.json", {"comparisonSemanticReadback": {"path": str(HERE / "comparison-semantic-readback.txt"), "sha256": sha((HERE / "comparison-semantic-readback.txt").read_bytes())},
          "completeSourceReadback": {"path": str(HERE / "complete-source-readback-002.txt"), "sha256": sha((HERE / "complete-source-readback-002.txt").read_bytes()), "families": len(records)},
          "limits": "Readbacks assist inspection; original complete XML retains all fields and repeated flags. Duplicate source families were equality-checked before deduplication."})
    print(len(records))
finally:
    write(HERE / "readback-memory-001.json", guard.finish())
