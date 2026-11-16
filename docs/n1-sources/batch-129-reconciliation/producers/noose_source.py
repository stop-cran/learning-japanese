import copy
import gzip
import hashlib
import xml.etree.ElementTree as ET
from pathlib import Path
from recon_common import *
from extract_b129 import HashReader, INPUTS, canonical

guard = start_guard()
try:
    filename, compressed, decompressed, tag = INPUTS["jmdict"]
    path = ROOT / "control" / "inputs" / filename
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    assert digest == compressed
    nodes, hashes = {}, {}
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event != "end" or node.tag != tag:
                continue
            if "羂索" in {n.text for n in node.findall("k_ele/keb")}:
                eid = node.findtext("ent_seq")
                nodes[eid] = copy.deepcopy(node)
                hashes[eid] = sha(canonical(node).encode())
            node.clear()
            root.clear()
    assert reader.digest.hexdigest() == decompressed
    root = ET.Element("JMdict")
    root.extend(nodes.values())
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    assert {n.findtext("ent_seq"): sha(canonical(n).encode()) for n in ET.fromstring(raw)} == hashes
    write(PACKET / "jmdict-noose-complete-records.xml", raw)
    write(PACKET / "noose-source-receipt.json", {
        "trigger": "Nikkoku 索 noun sense 2 independently names the Buddhist 羂索; follow this explicit positive rather than dismiss it as generic rope.",
        "queries": {"exact-spelling:羂索": list(nodes)},
        "zeroMatches": [] if nodes else ["exact-spelling:羂索"],
        "input": {"path": str(path), "compressedSha256": compressed, "decompressedSha256": decompressed},
        "output": {"path": "jmdict-noose-complete-records.xml", "sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": hashes},
        "completeCanonicalEquality": True, "transformation": "Complete parsed/reserialized XML; no substring, priority, age, frequency, language or sense filter.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    print(raw.decode())
finally:
    write(HERE / "noose-source-memory-001.json", guard.finish())
