import copy
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from common_133 import BASE, HERE, INPUTS, canonical, records, sha, start_guard, write, xml_output

OUT = HERE / "source-002"
VARIANTS = "珡琹鈆瀧"
EXACT = ["琴", "和琴", "琴線", "鉛", "鉛筆", "鉛粉", "白粉", "贋金", "金属", "滝", "滝水", "早瀬", "浸す", "潤す", "墓", "墳墓"]
COMPONENTS = "玉王今金八口水氵竜龍"


def main():
    guard = start_guard()
    try:
        counts = {**{f"contains:{c}": 0 for c in VARIANTS}, **{f"exact-spelling:{s}": 0 for s in EXACT}}
        selected, membership = [], {}
        for n in records("jmdict", guard):
            spellings = {s.text for s in n.findall("k_ele/keb")}
            keys = [f"contains:{c}" for c in VARIANTS if any(c in s for s in spellings)]
            keys += [f"exact-spelling:{s}" for s in EXACT if s in spellings]
            if keys:
                selected.append(copy.deepcopy(n))
                membership[n.findtext("ent_seq")] = keys
                for k in keys:
                    counts[k] += 1
        kd = [copy.deepcopy(n) for n in records("kanjidic2", guard) if n.findtext("literal") in VARIANTS + COMPONENTS]
        outputs = {
            "jmdict-supplemental-families.xml": xml_output(OUT / "jmdict-supplemental-families.xml", "JMdict", selected),
            "kanjidic2-variants-components.xml": xml_output(OUT / "kanjidic2-variants-components.xml", "kanjidic2", kd),
        }
        write(OUT / "supplemental-query-membership.json", membership)
        write(OUT / "supplemental-source-receipt.json", {"base": BASE, "inputs": INPUTS, "outputs": outputs,
              "containsKeys": list(VARIANTS), "allExactSpellings": EXACT, "allExactReadings": [],
              "queryCountsIncludingAbsences": counts,
              "predicate": "Union of complete families with any spelling containing KANJIDIC2-resolved variant 珡琹鈆瀧 or exact supplemental lexical spelling. No priority/reading/sense filter. Complete character records for those variants and named components/radicals.",
              "transformation": "Complete parsed/reserialized XML, not raw slices. Canonical full-record source/output equality.",
              "producerSha256": sha(Path(__file__).read_bytes())})
        reread = {}
        for n in records("jmdict", guard):
            spellings = {s.text for s in n.findall("k_ele/keb")}
            if any(c in s for c in VARIANTS for s in spellings) or spellings.intersection(EXACT):
                reread[n.findtext("ent_seq")] = sha(canonical(n).encode())
        assert reread == outputs["jmdict-supplemental-families.xml"]["canonicalRecordHashes"]
        expected = outputs["kanjidic2-variants-components.xml"]["canonicalRecordHashes"]
        found = {n.findtext("literal"): sha(canonical(n).encode()) for n in records("kanjidic2", guard) if n.findtext("literal") in expected}
        assert expected == found
        write(OUT / "supplemental-verification.json", {"status": "PASS", "completeJmdict": len(reread), "completeKanjidic": len(found),
              "sourceReceiptSha256": sha((OUT / "supplemental-source-receipt.json").read_bytes()),
              "verification": "Author's separate full-stream original hash and canonical-record recomputation, not independent linguistic review."})
        print(json.dumps({"families": len(reread), "characters": len(found), "counts": counts}, ensure_ascii=False))
    finally:
        write(OUT / "supplement-memory.json", guard.finish())


if __name__ == "__main__":
    main()
