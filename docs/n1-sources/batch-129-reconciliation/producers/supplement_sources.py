import copy
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from recon_common import *
from extract_b129 import HashReader, INPUTS, canonical

guard = start_guard()
try:
    filename, compressed, decompressed, tag = INPUTS["jmdict"]
    path = ROOT / "control" / "inputs" / filename
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            guard.check()
            digest.update(chunk)
    assert digest.hexdigest() == compressed
    queries = {"exact-spelling:括り": [], "exact-reading:くくり": []}
    nodes, hashes, memberships = {}, {}, {}
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event != "end" or node.tag != tag:
                continue
            eid = node.findtext("ent_seq")
            predicates = []
            if "括り" in {n.text for n in node.findall("k_ele/keb")}:
                predicates.append("exact-spelling:括り")
            if "くくり" in {n.text for n in node.findall("r_ele/reb")}:
                predicates.append("exact-reading:くくり")
            if predicates:
                nodes[eid] = copy.deepcopy(node)
                hashes[eid] = sha(canonical(node).encode())
                memberships[eid] = predicates
                for predicate in predicates:
                    queries[predicate].append(eid)
            node.clear()
            root.clear()
    assert reader.digest.hexdigest() == decompressed
    root = ET.Element("JMdict")
    root.extend(nodes.values())
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    assert {n.findtext("ent_seq"): sha(canonical(n).encode()) for n in ET.fromstring(raw)} == hashes
    write(PACKET / "jmdict-supplement-complete-records.xml", raw)
    write(PACKET / "supplement-query-membership.json", {
        "queries": queries, "recordPredicates": memberships,
        "zeroMatches": [q for q, ids in queries.items() if not ids],
        "trigger": "Complete Nikkoku 括 article positively records くくり as a bird/animal snare; follow the exact noun rather than infer a trap from generic tying.",
    })
    write(PACKET / "supplement-source-receipt.json", {
        "input": {"path": str(path), "compressedSha256": compressed, "decompressedSha256": decompressed},
        "output": {"path": "jmdict-supplement-complete-records.xml", "sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": hashes},
        "completeCanonicalEquality": True, "transformation": "Complete parsed/reserialized XML, not raw slices.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    print(raw.decode())
finally:
    write(HERE / "supplement-source-memory-001.json", guard.finish())
