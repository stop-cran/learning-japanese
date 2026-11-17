import json
import xml.etree.ElementTree as ET
from common_133 import HERE, canonical, normalized, start_guard, write

SOURCE = HERE / "source-002"
OUT = HERE / "readback-002"


def mapping(node):
    out = {}
    for child in node:
        value = mapping(child) if len(child) else child.text or ""
        if child.attrib:
            value = {"value": value, "attributes": child.attrib}
        out.setdefault(child.tag, []).append(value)
    return out


def main():
    guard = start_guard()
    try:
        nodes = {}
        for name in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml"):
            for n in ET.parse(SOURCE / name).getroot():
                identifier = n.findtext("ent_seq")
                if identifier in nodes:
                    assert canonical(nodes[identifier]) == canonical(n)
                nodes[identifier] = n
        paths = sorted((SOURCE / "comparison-cards").glob("*.md"))
        for start in range(0, len(paths), 4):
            parts = []
            for path in paths[start:start + 4]:
                ch = path.stem
                data = json.loads((SOURCE / "comparison-readback" / (ch + ".json")).read_bytes())
                parts += [f"==== {ch} COMPLETE CARD ====", normalized(path)]
                record = data["completeKanjidic"]
                parts += ["COMPLETE ENGLISH CHARACTER MEANINGS: " + json.dumps(
                    [r[2] for group in record[3] if group[0] == "reading_meaning"
                     for rm in group[3] if rm[0] == "rmgroup" for r in rm[3]
                     if r[0] == "meaning" and r[1].get("m_lang", "en") == "en"], ensure_ascii=False)]
            write(OUT / f"cards-{start//4 + 1:02d}.txt", ("\n".join(parts) + "\n").encode())
        families = []
        for n in nodes.values():
            obj = mapping(n)
            for sense in obj.get("sense", []):
                sense["gloss"] = [g["value"] if isinstance(g, dict) and g["attributes"] == {"{http://www.w3.org/XML/1998/namespace}lang": "eng"} else g for g in sense["gloss"]]
            families.append(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
        for start in range(0, len(families), 40):
            write(OUT / f"families-{start//40 + 1:02d}.txt", ("\n".join(families[start:start+40]) + "\n").encode())
        print(json.dumps({"cards": len(paths), "families": len(families), "files": [(p.name, p.stat().st_size) for p in sorted(OUT.glob("*.txt"))]}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()
