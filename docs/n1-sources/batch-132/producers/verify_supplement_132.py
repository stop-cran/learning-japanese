import json
import xml.etree.ElementTree as ET
from pathlib import Path

from common_132 import BASE, HERE, sha, start_guard, write
from survey_132 import records
from sources_132 import canonical

OUT = HERE / "source-003"


def main():
    guard = start_guard()
    try:
        receipt = json.loads((OUT / "supplemental-source-receipt.json").read_bytes())
        assert receipt["base"] == BASE
        info = receipt["outputs"]["jmdict-supplemental-families.xml"]
        path = OUT / "jmdict-supplemental-families.xml"
        assert sha(path.read_bytes()) == info["sha256"]
        expected = {n.findtext("ent_seq"): sha(canonical(n).encode()) for n in ET.parse(path).getroot()}
        assert expected == info["canonicalRecordHashes"]
        spellings = set(receipt["allExactSpellings"])
        counts = dict.fromkeys(spellings, 0)
        found, membership = {}, {}
        for node in records("jmdict", guard):
            hits = sorted({n.text for n in node.findall("k_ele/keb")} & spellings)
            if hits:
                identifier = node.findtext("ent_seq")
                found[identifier] = sha(canonical(node).encode())
                membership[identifier] = hits
                for hit in hits:
                    counts[hit] += 1
        assert found == expected
        assert membership == json.loads((OUT / "supplemental-query-membership.json").read_bytes())
        assert counts == receipt["countsIncludingAbsences"]
        write(OUT / "supplemental-verification.json", {
            "base": BASE, "sourceReceiptSha256": sha((OUT / "supplemental-source-receipt.json").read_bytes()),
            "membershipSha256": sha((OUT / "supplemental-query-membership.json").read_bytes()),
            "families": len(found), "countsIncludingAbsences": counts,
            "verification": "Independent full compressed/decompressed input hash check and complete-stream exact-spelling predicate and canonical record equality. Parsed/reserialized XML, not raw slices.",
            "producerSha256": sha(Path(__file__).read_bytes())})
        print(json.dumps({"families": len(found), "status": "PASS"}))
    finally:
        write(OUT / "supplement-verification-memory.json", guard.finish())


if __name__ == "__main__":
    main()
