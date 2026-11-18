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


for source in ("kanjidic2", "jmdict"):
    root = ET.parse(PACKET / f"{source}-complete-records.xml").getroot()
    lines = [json.dumps(present(n), ensure_ascii=False, separators=(",", ":")) for n in root]
    write(HERE / f"{source}-complete-presentation.jsonl", ("\n".join(lines) + "\n").encode())
    print(source, len(lines), "records", sum(map(len, lines)), "characters")
