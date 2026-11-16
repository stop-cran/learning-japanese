import json
import xml.etree.ElementTree as ET
from b130_common import HERE, PACKET, write

records = {}
for name in ("kanjidic2-comparison-records.xml", "kanjidic2-supplemental-comparisons.xml"):
    for node in ET.parse(PACKET / name).getroot():
        records[node.findtext("literal")] = node
lines = []
for ch, node in sorted(records.items()):
    means = [m.text for m in node.findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]
    readings = [m.text for m in node.findall("reading_meaning/rmgroup/reading") if m.get("r_type", "").startswith("ja_")]
    lines.append(f'{ch} | {"; ".join(means)} | {", ".join(readings)}')
write(HERE / "complete-comparison-character-inventories.txt", ("\n".join(lines) + "\n").encode())
