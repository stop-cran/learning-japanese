import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from b131_common import HERE, PACKET, sha, start_guard, write
from candidate_b131 import BASE, CHARS
from survey_b131 import INPUTS, canonical, records
from survey_b131_002 import xml_output

guard = start_guard()
try:
    first = json.loads((PACKET / "source-receipt.json").read_text(encoding="utf8"))
    second = json.loads((PACKET / "supplemental-source-receipt.json").read_text(encoding="utf8"))
    manual = json.loads((PACKET / "manual-source-receipt.json").read_text(encoding="utf8"))
    original, expected = {}, {}
    for receipt in (first, second, manual):
        for name, info in receipt["outputs"].items():
            path = PACKET / name
            assert sha(path.read_bytes()) == info["sha256"]
            hashes = {}
            for node in ET.parse(path).getroot():
                key = node.findtext("ent_seq") or node.findtext("literal")
                hashes[key] = sha(canonical(node).encode())
                if key in expected:
                    assert expected[key] == hashes[key]
                expected[key] = hashes[key]
                if node.tag == "entry":
                    original[key] = node
            assert hashes == info["canonicalRecordHashes"], name
    initial_exact, initial_readings = set(first["allExactSpellings"]), set(first["allExactReadings"])
    supplemental_exact = set(second["allExactSpellings"])
    extras = json.loads((PACKET / "reading-keys.json").read_text(encoding="utf8"))["testedKeys"]
    manual_exact = set(manual["allExactSpellings"])
    exact = initial_exact | supplemental_exact | manual_exact
    all_readings = initial_readings | set().union(*map(set, extras.values()))
    contains = first["containsKeys"]
    counts = {k + ":" + v: 0 for k, values in
              (("contains", contains), ("exact-spelling", sorted(exact)), ("exact-reading", sorted(all_readings))) for v in values}
    memberships, initial_memberships, supplemental_memberships, additional = {}, {}, {}, []
    count = 0
    for node in records("jmdict", guard):
        count += 1
        keb = {n.text for n in node.findall("k_ele/keb")}
        reb = {n.text for n in node.findall("r_ele/reb")}
        containing = [f"contains:{c}" for c in contains if any(c in spelling for spelling in keb)]
        initial_predicates = containing + [f"exact-spelling:{s}" for s in sorted(keb & initial_exact)]
        initial_predicates += [f"exact-reading:{r}" for r in sorted(reb & initial_readings)]
        supplemental_predicates = [f"exact-spelling:{s}" for s in sorted(keb & supplemental_exact)]
        predicates = containing + [f"exact-spelling:{s}" for s in sorted(keb & exact)]
        predicates += [f"exact-reading:{r}" for r in sorted(reb & all_readings)]
        eid = node.findtext("ent_seq")
        if initial_predicates:
            initial_memberships[eid] = initial_predicates
        if supplemental_predicates:
            supplemental_memberships[eid] = supplemental_predicates
        if predicates:
            memberships[eid] = predicates
            for p in predicates:
                counts[p] += 1
            if eid in original:
                assert sha(canonical(node).encode()) == expected[eid], eid
            else:
                additional.append(copy.deepcopy(node))
    assert initial_memberships == json.loads((PACKET / "query-membership.json").read_text(encoding="utf8"))
    assert supplemental_memberships == json.loads((PACKET / "supplemental-query-membership.json").read_text(encoding="utf8"))
    assert original.keys() <= memberships.keys()
    output = xml_output(PACKET / "jmdict-final-families-002.xml", "JMdict", additional)
    kd_expected = {k: v for k, v in expected.items() if not k.isdecimal()}
    seen = set()
    for node in records("kanjidic2", guard):
        ch = node.findtext("literal")
        if ch in kd_expected:
            assert sha(canonical(node).encode()) == kd_expected[ch], ch
            seen.add(ch)
    assert seen == kd_expected.keys()
    assert {p.stem for p in (PACKET / "comparison-cards").glob("*.md")} <= seen
    write(PACKET / "final-query-membership-002.json", memberships)
    write(PACKET / "final-source-audit-002.json", {
        "base": BASE, "originalSourceBase": first["base"], "completeJmdictUnion": len(memberships),
        "originalFamiliesRechecked": len(original), "additionalFamilies": len(additional),
        "wholeJmdictEntriesScanned": count, "completeKanjidicRecordsRechecked": len(seen),
        "queryCountsIncludingAbsences": counts, "finalAdditionalOutput": output, "dictionaryInputs": INPUTS,
        "comparisonCopies": len(list((PACKET / "comparison-cards").glob("*.md"))),
        "verification": "Independent complete decompression and exact compressed/decompressed input hashes; full mixed-predicate recomputation including absent keys; initial and supplemental per-entry predicate memberships rechecked; complete original-record canonical equality; duplicate family equality before deduplication. No priority/rarity/sense filtering. Complete parsed/reserialized XML, not raw slices.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    print(json.dumps({"completeJmdictUnion": len(memberships), "additionalFamilies": len(additional),
                      "completeKanjidic": len(seen), "absentQueries": [k for k, n in counts.items() if not n]}, ensure_ascii=False))
finally:
    write(HERE / "final-source-memory-002.json", guard.finish())
