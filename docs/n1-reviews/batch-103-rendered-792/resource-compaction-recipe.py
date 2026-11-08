"""Compact generated review resources without dropping any supplied dictionary record."""
import gzip
import importlib.util
import json
import re
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prep792", C / "prepare-batch-103-rendered-792.py")
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)
p.verify_heads()
provenance = p.load(p.D / "source-provenance.json")
original = p.load(p.D / "bounded-resources.json")
first = Path(original[0]["path"]).read_text(encoding="utf-8")
sections = [first.split("\n\nSOURCE ", 1)[0]]
normalizations = []
for row in provenance["sources"]:
    path = Path(row["path"])
    assert p.sha(path) == row["sha256"]
    raw = gzip.decompress(path.read_bytes()) if row["derivation"] else path.read_bytes()
    body = raw.decode("utf-8-sig")
    label = "SOURCE"
    if path.suffix == ".xml":
        root = ET.fromstring(raw)
        compact_children = [p.element_bytes(child).decode("utf-8") for child in root]
        body = f"<{root.tag}>\n" + "\n".join(compact_children) + f"\n</{root.tag}>"
        back = ET.fromstring(body)
        assert [p.element_bytes(e) for e in root] == [p.element_bytes(e) for e in back]
        label = "COMPLETE XML; INSIGNIFICANT WHITESPACE NORMALIZED; RECORD LINES NOT ORIGINAL SOURCE LINES"
    elif path.suffix == ".json" or path.name.endswith(".json.gz"):
        value = json.loads(body)
        body = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        assert json.loads(body) == value
        label = "COMPLETE JSON; WHITESPACE NORMALIZED; NO FIELDS OMITTED HERE"
    else:
        body = "\n".join(f"{i}: {line}" for i, line in enumerate(body.splitlines(), 1))
    sections.append(f"{label} {path}; SHA256 {p.sha(path)}\n{body}")
    normalizations.append({"path": str(path), "sha256": p.sha(path),
                           "suppliedUtf8Bytes": len(body.encode("utf-8")), "representation": label})

chunks, current = [], ""
for section in sections:
    if current and len((current + "\n\n" + section).encode("utf-8")) > 100000:
        chunks.append(current)
        current = ""
    for line in (section + "\n\n").splitlines(keepends=True):
        if current and len((current + line).encode("utf-8")) > 100000:
            chunks.append(current)
            current = ""
        current += line
if current:
    chunks.append(current)
resources = []
for i, body in enumerate(chunks, 1):
    archive = p.D / f"review-resource-{i:02}.txt.gz"
    destination = C / "batch-103-rendered-792" / f"review-resource-{i:02}.txt"
    raw = body.encode("utf-8")
    assert len(raw) <= 100000 and not archive.exists() and not destination.exists()
    archive.write_bytes(gzip.compress(raw, mtime=0))
    destination.write_bytes(raw)
    resources.append({"path": str(destination), "archive": str(archive),
                      "archiveSha256": p.sha(archive), "sha256": p.digest(raw),
                      "bytes": len(raw), "lines": len(body.splitlines())})
p.save(p.D / "review-resources.json", resources)
p.save(p.D / "review-resource-normalization.json", {
    "scope": "Complete previous source dossier with XML/JSON whitespace compacted, no records/fields/senses/restrictions removed.",
    "xmlProof": "Normalized element equality verified for every record, in source order.",
    "jsonProof": "Decoded JSON equality verified for every supplied JSON object/array.",
    "sources": normalizations,
    "previousResourceBytes": sum(r["bytes"] for r in original),
    "reviewResourceBytes": sum(r["bytes"] for r in resources),
    "reviewersLaunched": 0,
})
def listing(rows):
    return "\n".join(f"{r['path']} ({r['bytes']} bytes; lines1-{r['lines']}; SHA256 {r['sha256']})" for r in rows)
for family in p.MODELS:
    original_task = p.D / f"{family}-task.txt.gz"
    prompt = gzip.decompress(original_task.read_bytes()).decode("utf-8")
    assert listing(original) in prompt
    prompt = prompt.replace(listing(original), listing(resources))
    prompt = prompt.replace("Read ALL common resources in order", "XML/JSON whitespace is losslessly normalized; record lines are not original source-file lines. Read ALL common resources in order")
    archive = p.D / f"{family}-review-task.txt.gz"
    assert not archive.exists()
    archive.write_bytes(gzip.compress(prompt.encode("utf-8"), mtime=0))
shutil.copyfile(Path(__file__), p.D / "resource-compaction-recipe.py")
print(json.dumps({"resources": len(resources), "bytes": sum(r["bytes"] for r in resources),
                  "maximumBytes": max(r["bytes"] for r in resources), "allRecordsPreserved": True,
                  "reviewersLaunched": 0}, indent=2))
