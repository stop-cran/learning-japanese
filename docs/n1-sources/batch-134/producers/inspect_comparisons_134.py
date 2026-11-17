import json
import sys
from pathlib import Path

root = Path(__file__).parent / "source-002" / "comparison-readback"


def compact_text(node):
    tag, attrs, text, children = node
    fields = [tag]
    if attrs:
        fields.append(str(attrs))
    if text:
        fields.append(text)
    if children:
        fields.append("[" + " ".join(compact_text(child) for child in children) + "]")
    return "(" + " ".join(fields) + ")"


def descend(node, tag):
    return ([node] if node[0] == tag else []) + [
        match for child in node[3] for match in descend(child, tag)
    ]


for char in sys.argv[1]:
    data = json.loads((root / (char + ".json")).read_bytes())
    print("\n========", char, "========\n")
    print(data["completeCard"])
    kd = data["completeKanjidic"]
    print("CHARACTER MEANINGS:", ", ".join(
        compact_text(node) for node in descend(kd, "meaning")
        if node[1].get("m_lang") in (None, "en")
    ))
    for entry in data["completeApplicableJmdict"]:
        print("WORD FAMILY:", " ".join(
            compact_text(node) for node in entry[3]
            if node[0] in ("ent_seq", "k_ele", "r_ele", "sense")
        ))
