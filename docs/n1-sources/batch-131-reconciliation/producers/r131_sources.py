import copy
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from r131_common import *
from survey_b131 import INPUTS, canonical, records
from survey_b131_002 import xml_output

WORDS = "冴える 冴え 涼しい 涼む 涼やか 久しい 久しぶり 害 枯れる 枯らす 殺す 卒する 卒える 卒る 当番 侍 軍 戦 送る 抵抗 援助 救援 援護 循環 護衛 衛護 宿衛 軍衛".split()
guard = start_guard()
try:
    assert git("rev-parse", "HEAD").decode().strip() == PARENT
    assert not git("status", "--porcelain=v1", "--untracked-files=all")
    entry_ids = set()
    for ch in COMPARISONS:
        raw = git("show", f"{PARENT}:kanji/{ch}.md")
        write(PACKET / "comparison-cards" / (ch + ".md"), raw)
        entry_ids.update(re.findall(r"\b\d{7}\b", raw.decode()))
    exact = set(COMPARISONS) | set(WORDS)
    membership, families = {}, []
    counts = {f"{kind}:{key}": 0 for kind, keys in
              (("exact-spelling", sorted(exact)), ("entry-id", sorted(entry_ids))) for key in keys}
    for node in records("jmdict", guard):
        eid = node.findtext("ent_seq")
        spellings = {n.text for n in node.findall("k_ele/keb")}
        predicates = [f"exact-spelling:{s}" for s in sorted(exact & spellings)]
        if eid in entry_ids:
            predicates.append("entry-id:" + eid)
        if predicates:
            membership[eid] = predicates
            for predicate in predicates:
                counts[predicate] += 1
            families.append(copy.deepcopy(node))
    kd = [copy.deepcopy(n) for n in records("kanjidic2", guard)
          if n.findtext("literal") in set(COMPARISONS) | set("衛霜")]
    assert len(kd) == 19
    outputs = {
        "jmdict-families.xml": xml_output(PACKET / "jmdict-families.xml", "JMdict", families),
        "kanjidic2-records.xml": xml_output(PACKET / "kanjidic2-records.xml", "kanjidic2", kd)}
    write(PACKET / "query-membership.json", membership)
    external = json.loads((FROZEN / "evidence" / "external-snapshots" / "manifest.json").read_text(encoding="utf8"))
    selected = [s for s in external["snapshots"] if s["index"] in (1, 5, 6)]
    for item in selected:
        for field in ("response", "extract"):
            assert sha((FROZEN / item[field]["path"]).read_bytes()) == item[field]["sha256"]
    reuse = {}
    for name in ("source-receipt.json", "supplemental-source-receipt.json", "manual-source-receipt.json",
                 "final-source-audit-002.json", "reading-keys.json", "evidence-inventory-002.json"):
        reuse[name] = sha((ORIGINAL / name).read_bytes())
    write(PACKET / "source-receipt.json", {
        "parent": PARENT, "publishedBase": BASE, "inputs": INPUTS, "outputs": outputs,
        "predicates": {"exactSpellings": sorted(exact), "entryIdsFromCompleteComparisonCards": sorted(entry_ids)},
        "queryCountsIncludingAbsences": counts, "membershipFile": "query-membership.json",
        "completeFamilies": len(families), "completeCharacterRecords": len(kd),
        "originalSourceReuseBindings": reuse,
        "verification": "Exhausted original pinned input streams with exact compressed/decompressed hashes. Complete selected records and canonical equality before/after reserialization, not raw slices. No rarity/priority/sense filtering; zero matches retained.",
        "attribution": "JMdict/KANJIDIC2: James William Breen and EDRDG, CC BY-SA 4.0; see original source receipt.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    write(PACKET / "external-source-bindings.json", {
        "frozenRoot": str(FROZEN), "manifestSha256": sha((FROZEN / "evidence" / "external-snapshots" / "manifest.json").read_bytes()),
        "snapshots": selected, "extractionMethod": external["extractionMethod"],
        "scope": "Complete existing frozen source captures/neutral extracts, not new fetches. Full responses/extracts stay local. Source URLs, timestamps and exact raw/extracted hashes retained; image omissions remain."})
    rows = []
    for node in families:
        rows.append(json.dumps({"completeEntry": ET.tostring(node, encoding="unicode"),
                                "predicates": membership[node.findtext("ent_seq")]}, ensure_ascii=False))
    for node in kd:
        rows.append(json.dumps({"completeCharacter": ET.tostring(node, encoding="unicode")}, ensure_ascii=False))
    chunks, chunk = [], ""
    for row in rows:
        if len(chunk) + len(row) > 14000 and chunk:
            chunks.append(chunk)
            chunk = ""
        chunk += row + "\n"
    if chunk:
        chunks.append(chunk)
    for i, chunk in enumerate(chunks, 1):
        write(HERE / f"source-readback-{i:02}.jsonl", chunk.encode())
    print(json.dumps({"families": len(families), "characters": len(kd), "readbackChunks": len(chunks),
                      "absences": [k for k, v in counts.items() if not v]}, ensure_ascii=False))
finally:
    write(HERE / "sources-memory-001.json", guard.finish())
