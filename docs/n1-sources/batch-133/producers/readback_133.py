import json
import re
import xml.etree.ElementTree as ET
from common_133 import HERE, canonical, normalized, sha, start_guard, write

SOURCE = HERE / "source-002"
OUT = HERE / "readback-001"


def semantic(n):
    return ET.tostring(n, encoding="unicode").replace("\n", "").replace("  ", "")


def main():
    guard = start_guard()
    try:
        nodes = {}
        for name in ("jmdict-complete-families.xml", "jmdict-supplemental-families.xml"):
            for n in ET.parse(SOURCE / name).getroot():
                key = n.findtext("ent_seq")
                if key in nodes:
                    assert canonical(n) == canonical(nodes[key])
                nodes[key] = n
        paths = sorted((SOURCE / "comparison-cards").glob("*.md"))
        for start in range(0, len(paths), 6):
            parts = []
            for path in paths[start:start + 6]:
                ch, text = path.stem, normalized(path)
                data = json.loads((SOURCE / "comparison-readback" / (ch + ".json")).read_bytes())
                parts += [f"==== {ch} COMPLETE CARD ====", text, "COMPLETE KANJIDIC RECORD", json.dumps(data["completeKanjidic"], ensure_ascii=False)]
                words = {ch} | set(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", text))
                parts += ["COMPLETE EXACT CHARACTER/LINKED-WORD FAMILIES"]
                parts += [semantic(n) for n in nodes.values() if words.intersection(x.text for x in n.findall("k_ele/keb"))]
            write(OUT / f"comparisons-{start//6 + 1:02d}.txt", ("\n".join(parts) + "\n").encode())
        write(OUT / "supplemental.txt", ("\n".join(semantic(n) for n in ET.parse(SOURCE / "jmdict-supplemental-families.xml").getroot()) + "\n").encode())
        print(json.dumps({"comparisons": len(paths), "uniqueCompleteFamilies": len(nodes), "files": [(p.name, p.stat().st_size) for p in sorted(OUT.glob("*.txt"))]}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()
