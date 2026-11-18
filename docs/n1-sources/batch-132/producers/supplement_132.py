import copy
import json
from pathlib import Path

from common_132 import BASE, HERE, sha, start_guard, write
from survey_132 import records
from sources_132 import compact, xml_output

OUT = HERE / "source-003"
SPELLINGS = ["埋める", "埋まる", "埋もれる", "埋ける", "募る", "募集", "募金", "応募", "暮れる", "暮らす", "暮らし"]


def main():
    guard = start_guard()
    try:
        selected, membership = [], {}
        counts = {s: 0 for s in SPELLINGS}
        for node in records("jmdict", guard):
            spellings = {n.text for n in node.findall("k_ele/keb")}
            hits = sorted(spellings & set(SPELLINGS))
            if hits:
                selected.append(copy.deepcopy(node))
                membership[node.findtext("ent_seq")] = hits
                for hit in hits:
                    counts[hit] += 1
        output = xml_output(OUT / "jmdict-supplemental-families.xml", "JMdict", selected)
        write(OUT / "supplemental-query-membership.json", membership)
        write(OUT / "supplemental-source-receipt.json", {
            "base": BASE, "sourceReceiptSha256": sha((OUT / "source-receipt.json").read_bytes()),
            "allExactSpellings": SPELLINGS, "countsIncludingAbsences": counts,
            "predicate": "Union of complete families with any exact spelling from the explicit comparison-card lexical examples, no priority or sense filter.",
            "transformation": "Complete parsed/reserialized XML, not raw slices; source/output canonical equality checked.",
            "outputs": {"jmdict-supplemental-families.xml": output},
            "producerSha256": sha(Path(__file__).read_bytes())})
        write(OUT / "supplemental-readback.json", [{"id": n.findtext("ent_seq"), "record": compact(n)} for n in selected])
        print(json.dumps({"families": len(selected), "counts": counts}, ensure_ascii=False))
    finally:
        write(OUT / "supplement-memory.json", guard.finish())


if __name__ == "__main__":
    main()
