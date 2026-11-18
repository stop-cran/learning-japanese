import json
import xml.etree.ElementTree as ET
from b131_common import HERE, PACKET, normalized, write


def flatten(node):
    head = node.tag + "".join(f"@{k}={v}" for k, v in node.attrib.items())
    if not len(node):
        return head + "=" + (node.text or "").strip()
    return head + "{" + "; ".join(flatten(n) for n in node) + "}"


nodes = list(ET.parse(PACKET / "jmdict-complete-families.xml").getroot())
membership = json.loads((PACKET / "query-membership.json").read_text(encoding="utf8"))
kd = {n.findtext("literal"): n for n in ET.parse(PACKET / "kanjidic2-comparison-records.xml").getroot()}
for ch in "衛羊霜":
    selected = [n for n in nodes if f"contains:{ch}" in membership[n.findtext("ent_seq")] or f"exact-spelling:{ch}" in membership[n.findtext("ent_seq")]]
    lines = [flatten(n) for n in selected]
    for i in range(0, len(lines), 40):
        write(HERE / f"target-compact-{ch}-{i // 40 + 1:02}.txt", ("\n".join(lines[i:i + 40]) + "\n").encode())
rows = []
for p in sorted((PACKET / "comparison-cards").glob("*.md")):
    ch = p.stem
    means = [n.text for n in kd[ch].findall("reading_meaning/rmgroup/meaning") if n.get("m_lang") in (None, "en")]
    exact = [flatten(n) for n in nodes if f"exact-spelling:{ch}" in membership[n.findtext("ent_seq")]]
    rows.append("CARD " + ch + "\n" + normalized(p) + "\nCOMPLETE KD ENGLISH: " + "; ".join(means) + "\nCOMPLETE EXACT-SPELLING FAMILIES:\n" + "\n".join(exact))
for i in range(0, len(rows), 8):
    write(HERE / f"cards-compact-{i // 8 + 1:02}.txt", ("\n\n".join(rows[i:i + 8]) + "\n").encode())
print({c: len([n for n in nodes if f"contains:{c}" in membership[n.findtext("ent_seq")]]) for c in "衛羊霜"})
