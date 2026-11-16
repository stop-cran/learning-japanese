import json
import re
import xml.etree.ElementTree as ET
from b131_common import HERE, PACKET, normalized, write


def compact(node):
    if not len(node):
        return (node.text or "").strip() + (str(node.attrib) if node.attrib else "")
    result = {}
    for child in node:
        result.setdefault(child.tag, []).append(compact(child))
    return result


nodes, kd = {}, {}
for file in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml"):
    for n in ET.parse(PACKET / file).getroot():
        nodes[n.findtext("ent_seq")] = n
for file in ("kanjidic2-comparison-records.xml", "kanjidic2-supplemental-comparisons.xml"):
    for n in ET.parse(PACKET / file).getroot():
        kd[n.findtext("literal")] = n
rows = []
for p in sorted((PACKET / "comparison-cards").glob("*.md")):
    ch = p.stem
    text = normalized(p)
    title = re.search(r"^title: (.+)$", text, re.M).group(1)
    meaning = text.split("## Meaning and origin", 1)[1].split("## Readings", 1)[0].strip()
    notes = text.split("## Notes", 1)[1].strip()
    means = [n.text for n in kd[ch].findall("reading_meaning/rmgroup/meaning") if n.get("m_lang") in (None, "en")]
    exact = [compact(n) for n in nodes.values() if ch in [k.text for k in n.findall("k_ele/keb")]]
    rows.append(json.dumps({"kanji": ch, "title": title, "completeKdEnglish": means, "actualMeaningAndOrigin": meaning, "actualNotesAndSources": notes,
               "completeExactSpellingFamilies": exact}, ensure_ascii=False))
for i in range(0, len(rows), 12):
    write(HERE / f"semantic-{i // 12 + 1:02}.jsonl", ("\n".join(rows[i:i + 12]) + "\n").encode())
print(len(rows))
