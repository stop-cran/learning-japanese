import copy
import gzip
import hashlib
import json
import xml.etree.ElementTree as ET
from b128_common import HERE, PACKET, ROOT, sha, start_guard, write
from extract_b128 import HashReader, INPUTS, canonical

QUERIES = {"側", "辺", "辺り", "際", "境", "界", "岸", "畔", "音", "声", "動く", "恐怖", "怖い", "咲く"}
guard = start_guard()
try:
    path = ROOT / "control" / "inputs" / INPUTS["jmdict"][0]
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            guard.check()
            digest.update(chunk)
    assert digest.hexdigest() == INPUTS["jmdict"][1]
    selected, hashes, memberships = [], {}, {q: [] for q in sorted(QUERIES)}
    memberships["reading=ほとり"] = []
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event != "end" or node.tag != "entry":
                continue
            eid = node.findtext("ent_seq")
            matched = QUERIES & {k.text for k in node.findall("k_ele/keb")}
            if "ほとり" in {r.text for r in node.findall("r_ele/reb")}:
                matched.add("reading=ほとり")
            if matched:
                selected.append(copy.deepcopy(node))
                hashes[eid] = sha(canonical(node).encode())
                for query in matched:
                    memberships[query].append(eid)
            node.clear()
            root.clear()
    assert reader.digest.hexdigest() == INPUTS["jmdict"][2]
    root = ET.Element("JMdict")
    root.extend(selected)
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    write(PACKET / "jmdict-comparison-records.xml", raw)
    assert {n.findtext("ent_seq"): sha(canonical(n).encode()) for n in ET.fromstring(raw).findall("entry")} == hashes
    write(PACKET / "comparison-source-receipt.json", {
        "compressedInputSha256": digest.hexdigest(), "decompressedInputSha256": reader.digest.hexdigest(),
        "inputFilename": INPUTS["jmdict"][0], "output": "jmdict-comparison-records.xml",
        "outputSha256": sha(raw), "canonicalCompleteRecordHashes": hashes,
        "exactKebOrRebQueries": memberships, "producerSha256": sha(open(__file__, "rb").read()),
        "transformation": "Complete parsed/reserialized records, not raw slices; no spelling/reading/sense/priority filtering.",
    })
    lines = []
    for node in selected:
        guard.check()
        lines.append(ET.tostring(node, encoding="unicode"))
    write(HERE / "comparison-record-readback.txt", "\n".join(lines).encode())
    print(json.dumps({"records": len(selected), "memberships": memberships, "readback": str(HERE / "comparison-record-readback.txt")}, ensure_ascii=False))
finally:
    write(HERE / "comparison-source-memory-001.json", guard.finish())
