import json
import xml.etree.ElementTree as ET
from recon_common import *


def present(node):
    if not list(node):
        return node.text if not node.attrib else {"text": node.text, "attributes": node.attrib}
    out = {}
    if node.attrib:
        out["@attributes"] = node.attrib
    for child in node:
        out.setdefault(child.tag, []).append(present(child))
    return out


queries = json.loads((PACKET / "jmdict-query-membership.json").read_text(encoding="utf8"))["queries"]
ids = {eid for query, values in queries.items() if query.startswith("exact-spelling:") for eid in values}
ids.update("1483420 1483440 1483390 1419430 1226160 1401210 1198760 1403060 1403040 1403020 1153340 1436260 1383160 1400620".split())
records = {n.findtext("ent_seq"): n for n in ET.parse(PACKET / "jmdict-complete-records.xml").getroot()}
assert ids <= set(records)
lines = [json.dumps(present(records[eid]), ensure_ascii=False, separators=(",", ":")) for eid in sorted(ids)]
write(HERE / "claim-complete-families.jsonl", ("\n".join(lines) + "\n").encode())
write(PACKET / "claim-source-readset.json", {
    "completeFamilyIdsPresented": sorted(ids),
    "selection": "Every complete exact-spelling result in primary query set, plus explicit compound/verb IDs needed for strongest pair senses. Supplemental complete くくり family is read separately.",
    "otherRetainedQueryResults": "Other exact-reading homonyms and cited example families remain complete and hash-bound but are not claimed independently linguistically audited.",
})
kd = []
for n in ET.parse(PACKET / "kanjidic2-complete-records.xml").getroot():
    groups = []
    for group in n.findall("reading_meaning/rmgroup"):
        groups.append({
            "readings": [(r.text, r.attrib) for r in group.findall("reading")],
            "englishMeanings": [m.text for m in group.findall("meaning") if m.get("m_lang") in (None, "en")],
        })
    kd.append({"literal": n.findtext("literal"), "groups": groups,
               "nanori": [x.text for x in n.findall("reading_meaning/nanori")]})
write(HERE / "kanjidic2-semantic-readback.jsonl", ("\n".join(json.dumps(x, ensure_ascii=False) for x in kd) + "\n").encode())
print(len(ids), "complete claim families;", len(kd), "complete English-meaning and reading inventories")
