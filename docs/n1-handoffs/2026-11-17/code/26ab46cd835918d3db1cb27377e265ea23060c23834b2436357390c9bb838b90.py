import json
import xml.etree.ElementTree as ET

from common_134 import HERE, sha, start_guard, write

SOURCE = HERE / "reconciliation-sources-001"
OUT = HERE / "reconciliation-readback-001"
guard = start_guard()
try:
    index = json.loads((SOURCE / "comparison-index.json").read_bytes())
    membership = json.loads((SOURCE / "query-membership.json").read_bytes())
    families = {n.findtext("ent_seq"): n for n in ET.parse(SOURCE / "jmdict-complete-families.xml").getroot()}
    characters = {n.findtext("literal"): n for n in ET.parse(SOURCE / "kanjidic2-complete-characters.xml").getroot()}
    for ch, item in index.items():
        keys = {"exact-spelling:" + s for s in [ch, *item["linkedWords"]]}
        selected = [n for identifier, n in families.items() if keys & set(membership[identifier])]
        lines = [f"=== {ch}: COMPLETE ARTICLE ===", (SOURCE / "comparison-cards" / f"{ch}.md").read_bytes().decode("utf-8"),
                 "=== COMPLETE KANJIDIC2 CHARACTER ===", ET.tostring(characters[ch], encoding="unicode"),
                 "=== COMPLETE APPLICABLE EXACT-SPELLING FAMILIES ==="]
        lines.extend(ET.tostring(n, encoding="unicode") for n in selected)
        write(OUT / (ch + ".txt"), ("\n".join(lines) + "\n").encode())
    write(OUT / "index.json", {"readbacks": {c: sha((OUT / (c + ".txt")).read_bytes()) for c in index},
                                 "limits": "Readback is an inspection convenience; complete selected XML and predicate membership are retained separately."})
finally:
    write(OUT / "memory.json", guard.finish())
