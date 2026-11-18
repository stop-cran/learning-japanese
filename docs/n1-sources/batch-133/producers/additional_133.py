import copy
import json
import re
from pathlib import Path
from common_133 import BASE, HERE, INPUTS, REPO, canonical, git, normalized, records, sha, start_guard, write, xml_output

OUT = HERE / "additional-001"
CHARS = "丘化銀白筆炭"


def main():
    guard = start_guard()
    try:
        manifest = json.loads(git("show", f"{BASE}:manifest.json"))
        exact = set(CHARS)
        for ch in CHARS:
            path = f"kanji/{ch}.md"
            assert path in manifest["files"]
            raw = git("show", f"{BASE}:{path}")
            write(OUT / "comparison-cards" / f"{ch}.md", raw)
            exact.update(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", raw.decode()))
        entries, membership = [], {}
        counts = {s: 0 for s in sorted(exact)}
        for n in records("jmdict", guard):
            keys = sorted({s.text for s in n.findall("k_ele/keb")} & exact)
            if keys:
                entries.append(copy.deepcopy(n))
                membership[n.findtext("ent_seq")] = keys
                for key in keys:
                    counts[key] += 1
        kd = [copy.deepcopy(n) for n in records("kanjidic2", guard) if n.findtext("literal") in CHARS]
        outputs = {
            "jmdict-additional-families.xml": xml_output(OUT / "jmdict-additional-families.xml", "JMdict", entries),
            "kanjidic2-additional-comparisons.xml": xml_output(OUT / "kanjidic2-additional-comparisons.xml", "kanjidic2", kd),
        }
        write(OUT / "query-membership.json", membership)
        write(OUT / "source-receipt.json", {
            "base": BASE, "inputs": INPUTS, "outputs": outputs, "allExactSpellings": sorted(exact),
            "queryCountsIncludingAbsences": counts,
            "predicate": "Complete exact-spelling families for six additional actual baseline comparisons and every declared linked word. No reading/priority/sense filter.",
            "reason": "Source-positive mound, cosmetic and lead-like-substance senses prompted hill, transformation/makeup, silver, white, writing implement and carbon comparisons beyond original token scan.",
            "transformation": "Complete parsed/reserialized records, not raw slices.",
            "producerSha256": sha(Path(__file__).read_bytes())})
        reread = {n.findtext("ent_seq"): sha(canonical(n).encode()) for n in records("jmdict", guard)
                  if {s.text for s in n.findall("k_ele/keb")} & exact}
        assert reread == outputs["jmdict-additional-families.xml"]["canonicalRecordHashes"]
        kdreread = {n.findtext("literal"): sha(canonical(n).encode()) for n in records("kanjidic2", guard)
                    if n.findtext("literal") in CHARS}
        assert kdreread == outputs["kanjidic2-additional-comparisons.xml"]["canonicalRecordHashes"]
        write(OUT / "verification.json", {"status": "PASS", "families": len(reread), "characters": len(kdreread),
              "receiptSha256": sha((OUT / "source-receipt.json").read_bytes()),
              "method": "Author's separate full-stream canonical record and input-hash recomputation, not independent review."})
        lines = []
        for ch in CHARS:
            lines += [normalized(OUT / "comparison-cards" / f"{ch}.md")]
            node = next(n for n in kd if n.findtext("literal") == ch)
            lines += [json.dumps({"character": ch, "completeEnglishMeanings": [m.text for m in node.findall("reading_meaning/rmgroup/meaning") if m.get("m_lang") in (None, "en")]}, ensure_ascii=False)]
        for node in entries:
            lines += [json.dumps({"id": node.findtext("ent_seq"), "xml": canonical(node)}, ensure_ascii=False)]
        write(OUT / "readback.txt", ("\n".join(lines) + "\n").encode())
        print(json.dumps({"families": len(entries), "characters": len(kd), "exactSpellings": sorted(exact)}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()
