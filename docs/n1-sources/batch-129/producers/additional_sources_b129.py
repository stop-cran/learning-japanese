import copy
import gzip
import hashlib
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from b129_common import HERE, PACKET, ROOT, sha, start_guard, write
from extract_b129 import HashReader, INPUTS, PageText, canonical

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
    selected, hashes, membership = {}, {}, {}
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event != "end" or node.tag != tag:
                continue
            eid = node.findtext("ent_seq")
            kebs = {e.text for e in node.findall("k_ele/keb")}
            rebs = {e.text for e in node.findall("r_ele/reb")}
            predicates = [f"exact-spelling:{k}" for k in sorted(kebs & {"木綿"})]
            predicates += [f"exact-reading:{r}" for r in sorted(rebs & {"きぎぬ", "ぎぬ"})]
            if predicates:
                selected[eid] = copy.deepcopy(node)
                hashes[eid] = sha(canonical(node).encode())
                membership[eid] = predicates
            node.clear()
            root.clear()
    assert reader.digest.hexdigest() == decompressed
    root = ET.Element("JMdict")
    root.extend(selected.values())
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    actual = {n.findtext("ent_seq"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
    assert actual == hashes
    write(PACKET / "jmdict-additional-families.xml", raw)
    write(PACKET / "additional-query-membership.json", membership)
    write(PACKET / "additional-source-receipt.json", {
        "input": {"filename": filename, "compressedSha256": compressed, "decompressedSha256": decompressed},
        "predicate": "Complete exact-spelling 木綿 family and every complete exact-reading きぎぬ/ぎぬ family. No sense, priority or rarity filtering.",
        "output": {"filename": "jmdict-additional-families.xml", "sha256": sha(raw), "bytes": len(raw),
                   "completeCanonicalEquality": True, "canonicalRecordHashes": actual},
        "transformation": "Complete parsed/reserialized XML, not raw source slices.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    url = "https://kotobank.jp/word/" + __import__("urllib.parse", fromlist=["quote"]).quote("綿")
    request = urllib.request.Request(url, headers={"User-Agent": "N1-author-source-check/129"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
        final_url = response.geturl()
    guard.check()
    parser = PageText()
    parser.feed(raw.decode("utf8"))
    text = ("\n".join(parser.parts) + "\n").encode()
    capture = HERE / "external-pages" / "綿-kotobank.html"
    write(capture, raw)
    write(capture.with_suffix(".txt"), text)
    write(HERE / "external-pages" / "receipt-002.json", [{
        "character": "綿", "provider": "kotobank", "url": url, "finalUrl": final_url,
        "capturedAt": datetime.now(timezone.utc).isoformat(), "rawSha256": sha(raw),
        "rawBytes": len(raw), "textSha256": sha(text), "localRawCapture": str(capture)}])
    print(json.dumps({"additionalFamilies": list(selected), "cottonCapture": str(capture), "captureBytes": len(raw)}, ensure_ascii=False))
finally:
    write(HERE / "additional-source-memory-001.json", guard.finish())
