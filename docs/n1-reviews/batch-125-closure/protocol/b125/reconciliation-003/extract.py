import copy
import gzip
import hashlib
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(r"C:\Users\stop-\n1-kanji-workspace")
repo = root / "b125-worktree"
assert os.environ["N1_REPO"] == str(repo)
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip() == "dbca5192a4308dc6e8d954af37775e0fcd1986ea"
out = Path(sys.argv[1])
chars = "低短小劣汚容美貧"
words = {"低い", "短い", "小さい", "劣る", "汚い", "美しい", "貧しい"}
sources = [
    ("kanjidic2", root / "control" / "inputs" / "n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "character", set(chars)),
    ("jmdict", root / "control" / "inputs" / "n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "entry", words),
]
selections = {}
for name, path, expected, tag, targets in sources:
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(block)
    assert hasher.hexdigest() == expected
    records, matches = [], {t: [] for t in sorted(targets)}
    with gzip.open(path, "rb") as stream:
        context = ET.iterparse(stream, events=("start", "end"))
        _, document = next(context)
        for event, node in context:
            if event != "end" or node.tag != tag:
                continue
            keys = {node.findtext("literal")} if tag == "character" else {k.findtext("keb") for k in node.findall("k_ele")}
            for hit in keys & targets:
                matches[hit].append(node.findtext("literal") if tag == "character" else node.findtext("ent_seq"))
            if keys & targets:
                records.append(copy.deepcopy(node))
            node.clear()
            document.clear()
    assert all(matches.values()), matches
    doc = ET.Element("kanjidic2" if name == "kanjidic2" else "JMdict")
    doc.extend(records)
    ET.indent(doc, space="  ")
    raw = ET.tostring(doc, encoding="utf-8", xml_declaration=True) + b"\n"
    (out / f"{name}-records.xml").write_bytes(raw)
    selections[name] = {"compressedSha256": expected, "outputSha256": hashlib.sha256(raw).hexdigest(), "recordCount": len(records), "exactSelectors": matches}
receipt = {"parent": "dbca5192a4308dc6e8d954af37775e0fcd1986ea", "selections": selections, "license": "JMdict and KANJIDIC2: James William Breen and EDRDG, CC BY-SA 4.0.", "limits": "Complete parsed and reserialized selected records; exact-form matches do not establish usage frequency."}
raw = (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode()
(out / "source-receipt.json").write_bytes(raw)
print(json.dumps(receipt, ensure_ascii=False))
