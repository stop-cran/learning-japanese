import json
import re
import sys
import xml.etree.ElementTree as ET
from b130_common import CHARS, HERE, PACKET, ROOT, normalized, sha, start_guard, write

sys.path.insert(0, str(ROOT / "lean"))
import n1lib

guard = start_guard()
try:
    entries, digests = {}, {}
    for filename in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml"):
        for node in ET.parse(PACKET / filename).getroot():
            eid = node.findtext("ent_seq")
            digest = sha(ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True).encode())
            if eid in digests:
                assert digest == digests[eid]
            entries[eid], digests[eid] = node, digest
    semantic = []
    for path in sorted((PACKET / "comparison-cards").glob("*.md")):
        fm, body = n1lib.parse(normalized(path))
        sections = n1lib.sections(body)
        meaning = sections.get("Meaning and origin", "")
        meaning = re.split(r"\*\*Modern.shape mnemonic", meaning, maxsplit=1, flags=re.I)[0].strip()
        notes = re.split(r"\n(?:Metadata|Sources?|Readings and metadata|Usage evidence):", sections.get("Notes", ""), maxsplit=1)[0].strip()
        families = []
        for eid, node in entries.items():
            if path.stem not in [n.text for n in node.findall("k_ele/keb")]:
                continue
            families.append({"id": eid,
                             "k": [{tag: [v.text for v in el.findall(tag)] for tag in ("keb", "ke_inf", "ke_pri")} for el in node.findall("k_ele")],
                             "r": [{tag: [v.text for v in el.findall(tag)] for tag in ("reb", "re_restr", "re_inf", "re_nokanji", "re_pri")} for el in node.findall("r_ele")],
                             "s": [{tag: [v.text for v in el.findall(tag)] for tag in ("gloss", "pos", "misc", "field", "stagk", "stagr", "s_inf", "xref", "ant", "lsource")} for el in node.findall("sense")]})
        semantic.append({"kanji": path.stem, "title": fm["title"], "actualMeaning": meaning,
                         "actualNotes": notes, "completeExactSpellingFamilySemantics": families})
    for n in range(0, len(semantic), 12):
        write(HERE / f"semantic-readback-{n//12+1:02}.jsonl",
              ("\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in semantic[n:n+12]) + "\n").encode())
    write(HERE / "semantic-readback-index.json", {
        "cards": len(semantic), "completeCanonicalFamilyUnion": len(entries),
        "limits": "Convenience semantic projections are not complete XML or whole-card byte reads. Exact complete source records and raw baseline cards remain authoritative.",
        "members": {c: json.loads((PACKET / "scans-002" / (c + ".json")).read_text(encoding="utf-8"))["matches"] for c in CHARS}})
    print("Cards:", len(semantic), "Complete canonical family union:", len(entries))
finally:
    write(HERE / "semantic-readback-memory-001.json", guard.finish())
