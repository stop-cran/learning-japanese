import json
import xml.etree.ElementTree as ET
from pathlib import Path
from common_134 import BASE, HERE, canonical, records, sha, start_guard, write

OUT = HERE / "source-001"


def main():
    guard = start_guard()
    try:
        receipt = json.loads((OUT / "source-receipt.json").read_bytes())
        assert receipt["base"] == BASE
        expected = {}
        for name, info in receipt["outputs"].items():
            path = OUT / name
            assert sha(path.read_bytes()) == info["sha256"]
            hashes = {}
            for node in ET.parse(path).getroot():
                identifier = node.findtext("ent_seq") or node.findtext("literal")
                assert identifier not in hashes
                hashes[identifier] = sha(canonical(node).encode())
            assert hashes == info["canonicalRecordHashes"]
            expected[name] = hashes
        counts = {key: 0 for key in receipt["queryCountsIncludingAbsences"]}
        found, membership = {}, {}
        exact, readings = set(receipt["allExactSpellings"]), set(receipt["allExactReadings"])
        for node in records("jmdict", guard):
            spellings = {n.text for n in node.findall("k_ele/keb")}
            keys = {n.text for n in node.findall("r_ele/reb")}
            predicates = [f"contains:{c}" for c in receipt["containsKeys"] if any(c in s for s in spellings)]
            predicates += [f"exact-spelling:{s}" for s in sorted(spellings & exact)]
            predicates += [f"exact-reading:{r}" for r in sorted(keys & readings)]
            if predicates:
                identifier = node.findtext("ent_seq")
                found[identifier] = sha(canonical(node).encode())
                membership[identifier] = predicates
                for predicate in predicates:
                    counts[predicate] += 1
        assert found == expected["jmdict-complete-families.xml"]
        assert membership == json.loads((OUT / "query-membership.json").read_bytes())
        assert counts == receipt["queryCountsIncludingAbsences"]
        kd_expected = expected["kanjidic2-targets.xml"] | expected["kanjidic2-comparisons.xml"]
        kd_found = {}
        for node in records("kanjidic2", guard):
            literal = node.findtext("literal")
            if literal in kd_expected:
                kd_found[literal] = sha(canonical(node).encode())
        assert kd_found == kd_expected
        write(OUT / "source-verification.json", {"base": BASE,
              "sourceReceiptSha256": sha((OUT / "source-receipt.json").read_bytes()),
              "queryMembershipSha256": sha((OUT / "query-membership.json").read_bytes()),
              "completeJmdictFamilies": len(found), "completeKanjidicRecords": len(kd_found),
              "countsIncludingAbsences": counts,
              "verification": "Separate full-stream compressed/decompressed hash, query-membership/absence and canonical complete-record recomputation by the author; not independent linguistic review.",
              "producerSha256": sha(Path(__file__).read_bytes())})
        print(json.dumps({"families": len(found), "characters": len(kd_found), "status": "PASS"}))
    finally:
        write(OUT / "verification-memory.json", guard.finish())


if __name__ == "__main__":
    main()
