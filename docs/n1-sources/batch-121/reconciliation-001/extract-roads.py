import gzip
import hashlib
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

root = Path(r"C:\Users\stop-\n1-kanji-workspace")
repo = root / "b121-worktree"
here = Path(__file__).resolve().parent
base = "b5302617bf4c7232bab5bcd1e76b8ae6b938bc3a"
assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo).decode().strip() == base
targets = {"道", "達"}
queries = targets | {"道徳", "道理", "上達", "達する"}
for filename, source, digest, tag, needles in [
    ("roads-jmdict-records.xml", "n1-implementation-JMdict_e.gz", "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d", "entry", queries),
    ("roads-kanjidic2-records.xml", "n1-planning-kanjidic2.xml.gz", "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed", "character", targets),
]:
    path = root / "control" / "inputs" / source
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1024 * 1024), b""):
            h.update(b)
    assert h.hexdigest() == digest
    result = ET.Element("JMdict" if tag == "entry" else "kanjidic2")
    with gzip.open(path, "rb") as f:
        parser = ET.iterparse(f, events=("start", "end"))
        _, docroot = next(parser)
        for event, elem in parser:
            if event != "end" or elem.tag != tag:
                continue
            keys = {x.text for x in elem.findall("k_ele/keb")} if tag == "entry" else {elem.findtext("literal")}
            if keys & needles:
                result.append(elem)
            else:
                elem.clear()
            docroot.clear()
    ET.indent(result, space="  ")
    raw = ET.tostring(result, encoding="utf-8", xml_declaration=True) + b"\n"
    with (here / filename).open("xb") as f:
        f.write(raw)
    print(json.dumps({"file": filename, "sha256": hashlib.sha256(raw).hexdigest(),
                      "entries": [e.findtext("ent_seq") or e.findtext("literal") for e in result]}, ensure_ascii=False))
for char in targets:
    data = subprocess.check_output(["git", "show", f"{base}:kanji/{char}.md"], cwd=repo)
    with (here / "comparison-cards" / f"{char}.md").open("xb") as f:
        f.write(data)
    print(json.dumps({"card": char, "sha256": hashlib.sha256(data).hexdigest()}, ensure_ascii=False))
