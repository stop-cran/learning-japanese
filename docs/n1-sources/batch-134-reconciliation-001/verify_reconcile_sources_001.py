import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common_134 import HERE, canonical, records, sha, start_guard, write

OUT = HERE / "reconciliation-sources-001"

guard = start_guard()
try:
    receipt = json.loads((OUT / "receipt.json").read_bytes())
    expected = {}
    for name, info in receipt["outputs"].items():
        raw = (OUT / name).read_bytes()
        assert sha(raw) == info["sha256"]
        rows = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
        assert rows == info["canonicalRecordHashes"]
        expected[name] = rows
    counts = {key: 0 for key in receipt["countsIncludingZero"]}
    membership, found = {}, {}
    for node in records("jmdict", guard):
        spellings = {n.text for n in node.findall("k_ele/keb")}
        readings = {n.text for n in node.findall("r_ele/reb")}
        predicates = [f"exact-spelling:{s}" for s in sorted(spellings & set(receipt["exactSpellings"]))]
        predicates += [f"exact-reading:{r}" for r in sorted(readings & set(receipt["exactReadings"]))]
        if predicates:
            identifier = node.findtext("ent_seq")
            found[identifier] = sha(canonical(node).encode())
            membership[identifier] = predicates
            for predicate in predicates:
                counts[predicate] += 1
    assert found == expected["jmdict-complete-families.xml"]
    assert membership == json.loads((OUT / "query-membership.json").read_bytes())
    assert counts == receipt["countsIncludingZero"]
    kd = {}
    for node in records("kanjidic2", guard):
        ch = node.findtext("literal")
        if ch in expected["kanjidic2-complete-characters.xml"]:
            kd[ch] = sha(canonical(node).encode())
    assert kd == expected["kanjidic2-complete-characters.xml"]
    write(OUT / "verification.json", {
        "status": "PASS", "candidate": receipt["candidate"], "families": len(found),
        "characters": len(kd), "sourceReceiptSha256": sha((OUT / "receipt.json").read_bytes()),
        "queryMembershipSha256": sha((OUT / "query-membership.json").read_bytes()),
        "countsIncludingZero": counts,
        "method": "Separate full-stream compressed/decompressed input hash, selector membership/zero-count and complete canonical-record recomputation.",
        "producerSha256": sha(Path(__file__).read_bytes())})
finally:
    write(OUT / "verification-memory.json", guard.finish())
