import copy
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from b130_common import BASE, CHARS, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write
from survey_b130 import EXACT_READINGS, HashReader, INPUTS, canonical, output_xml

KEYS = {
    "塀": ["かき"],
    "拍": ["ひゃく", "うつ", "たたく", "はやし", "おふす", "ひむささら", "なづ", "なず", "なでる", "にしる", "かしわで", "びんざさら"],
    "耗": ["ぼう", "へる", "みだれる", "たより", "へらす", "つきる", "なくする", "ついやす", "やぶる", "そこなう", "わるい", "うすい", "くらい",
           "たかへす", "とか", "をぢなし", "おぢなし", "そこなはる", "そこなわる", "ついゆ", "ついえる", "のごふ", "ぬぐう", "ほろぶ",
           "きぬ", "うつかす", "つく", "おどろく", "そこなふ", "へなる", "かへる", "かえる", "にくむ", "むなし", "むなしい"],
}

guard = start_guard()
try:
    write(PACKET / "reading-keys.json", {
        "testedKeys": KEYS,
        "sourceMapping": {
            "塀": "字通 [字訓] かき; not in the frozen empty kun list.",
            "拍": "Weblio/Wiktionary ヒャク; 字通 [字訓]/[訓義] うつ・たたく・はやし and historical quotations. かしわで/びんざさら are whole-word-only extras.",
            "耗": "字通 ボウ, [字訓]/[訓義] and complete old-dictionary strings; verified Kanjipedia へる・たより.",
        },
        "modernizedPrecautionsNotNewSourceClaims": ["なず", "なでる", "おぢなし", "そこなわる", "ついえる", "ぬぐう", "かえる", "むなしい"],
        "compoundOnlyPrecautions": ["ひむささら", "かしわで", "びんざさら"],
        "limit": "Positive source glosses/lookup forms are deliberately over-tested; this is not a classification of every key as an ordinary modern character reading."})
    receipts = [json.loads((PACKET / n).read_text(encoding="utf-8")) for n in ("source-receipt.json", "supplemental-source-receipt.json")]
    original, expected_hashes = {}, {}
    for receipt in receipts:
        for name, info in receipt["outputs"].items():
            path = PACKET / name
            assert sha(path.read_bytes()) == info["sha256"]
            hashes = {}
            for node in ET.parse(path).getroot():
                key = node.findtext("ent_seq") or node.findtext("literal")
                hashes[key] = sha(canonical(node).encode())
                if key in expected_hashes:
                    assert expected_hashes[key] == hashes[key], (name, key)
                expected_hashes[key] = hashes[key]
                if node.tag == "entry":
                    original[key] = node
            assert hashes == info["canonicalRecordHashes"], name
    old_comparisons = set(receipts[0]["outputs"]["kanjidic2-comparison-records.xml"]["canonicalRecordHashes"])
    supports = json.loads((PACKET / "selection.json").read_text(encoding="utf-8"))["allDeclaredSupportArticles"]
    old_exact = old_comparisons | set(CHARS) | {w for ws in supports.values() for w in ws}
    supplemental_exact = set(receipts[1]["predicates"]["exactSpellings"])
    supplemental_readings = set(receipts[1]["predicates"]["exactReadings"])
    extra_readings = set().union(*map(set, KEYS.values()))
    exact = old_exact | supplemental_exact
    all_readings = EXACT_READINGS | supplemental_readings | extra_readings
    query_counts = {k + ":" + v: 0 for k, values in (("contains", [*CHARS, "屏"]), ("exact-spelling", sorted(exact)), ("exact-reading", sorted(all_readings))) for v in values}
    matched, additional, membership = set(), [], {}
    filename, compressed_sha, xml_sha, tag = INPUTS["jmdict"]
    path = ROOT / "control" / "inputs" / filename
    assert sha(path.read_bytes()) == compressed_sha
    count = 0
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event != "end" or node.tag != tag:
                continue
            count += 1
            kebs = {n.text for n in node.findall("k_ele/keb")}
            rebs = {n.text for n in node.findall("r_ele/reb")}
            predicates = [f"contains:{c}" for c in [*CHARS, "屏"] if any(c in k for k in kebs)]
            predicates += [f"exact-spelling:{k}" for k in sorted(exact & kebs)]
            predicates += [f"exact-reading:{r}" for r in sorted(all_readings & rebs)]
            if predicates:
                eid = node.findtext("ent_seq")
                for p in predicates:
                    query_counts[p] += 1
                if eid in original:
                    assert sha(canonical(node).encode()) == expected_hashes[eid], eid
                else:
                    additional.append(copy.deepcopy(node))
                matched.add(eid)
                membership[eid] = predicates
            node.clear()
            root.clear()
    assert reader.digest.hexdigest() == xml_sha
    assert original.keys() <= matched
    output = output_xml("jmdict-final-families.xml", "JMdict", additional, "jmdict")
    kd_expected = {k: v for k, v in expected_hashes.items() if not k.isdecimal()}
    filename, compressed_sha, xml_sha, tag = INPUTS["kanjidic2"]
    path = ROOT / "control" / "inputs" / filename
    assert sha(path.read_bytes()) == compressed_sha
    kd_seen = set()
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event == "end" and node.tag == tag:
                ch = node.findtext("literal")
                if ch in kd_expected:
                    assert sha(canonical(node).encode()) == kd_expected[ch], ch
                    kd_seen.add(ch)
                node.clear()
                root.clear()
    assert reader.digest.hexdigest() == xml_sha and kd_seen == kd_expected.keys()
    assert {p.stem for p in (PACKET / "comparison-cards").glob("*.md")} <= kd_seen
    write(PACKET / "final-query-membership.json", membership)
    write(PACKET / "final-source-audit.json", {
        "base": BASE, "completeJmdictUnion": len(matched), "originalFamiliesRechecked": len(original),
        "additionalFamilies": len(additional), "wholeJmdictEntriesScanned": count,
        "completeKanjidicRecordsRechecked": len(kd_seen),
        "queryCountsIncludingAbsences": query_counts, "finalAdditionalOutput": output,
        "dictionaryInputs": receipts[0]["dictionaryInputs"],
        "verification": "Independent full decompression, exact input hashes, full union-predicate recomputation, complete canonical equality for every retained original family/character record, and complete additional records. No priority/rarity/sense filtering. Complete parsed/reserialized XML, not raw slices.",
        "producerSha256": sha(Path(__file__).read_bytes())})
    print(json.dumps({"completeJmdictUnion": len(matched), "additionalFamilies": len(additional), "completeKanjidic": len(kd_seen), "absentQueries": [k for k, n in query_counts.items() if not n]}, ensure_ascii=False))
finally:
    write(HERE / "final-source-memory-001.json", guard.finish())
