import copy
import gzip
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from b129_common import BASE, CHARS, HERE, PACKET, ROOT, git, sha, start_guard, write
from extract_b129 import HashReader, INPUTS, canonical

EXTRA = {
    "茉": "jasmine jasmin",
    "絹": "snare snares trap traps ensnare net nets capture catch hang hanging curtain curtains veil veils drape screen twill twilled gauze brocade",
    "羊": "paper papers banknote banknotes money currency bill bills bank notes barber barbers hair hairdresser hairdressing good goodness auspicious luck lucky fortunate happiness happy omen omens roam roaming wander wandering leisure leisurely carefree",
    "虹": "flag flags banner banners oil dish dishes lamp lamps disorder disorders confusion confused disturbance disturbed quarrel quarrels argue argument arguments attack attacks blame accuse aggression rebel rebellion rebelled",
    "霜": "sharp blade blades sword swords severe severity strict strictness harsh harshness stern keen rigid intense violent fierce destroy destroyed destruction perish perished die death loss lose losing lost ruin ruined expire wither withered",
}
DISTRACTORS = {"茉": list("未本古"), "絹": list("紙約級"), "羊": list("牛半午"), "虹": list("紅功石"), "霜": list("箱想電")}
EXTRAS = {"茉": ["まつり", "まち", "み"], "絹": ["かとり", "かく", "わな", "わなをかける"],
          "羊": ["よい", "めでたい", "めでたいしるし", "しょう"],
          "虹": ["のじ", "ぬじ", "おにじ", "はし", "あぶらざら", "みだれる", "あらそう", "せめる"],
          "霜": ["とし", "ほろぶ", "うしなう", "しもをむすぶ"]}

guard = start_guard()
try:
    comparisons = set()
    for ch in CHARS:
        old = json.loads((PACKET / "scans" / (ch + ".json")).read_text(encoding="utf-8"))
        keywords = set(old["expandedKeywords"]) | set(EXTRA[ch].split())
        rows = []
        for row in old["rows"]:
            item = dict(row)
            item["matchedKeywords"] = sorted(keywords & set(re.findall("[a-z]+", " ".join([row["title"], *row["completeMeanings"]]).lower())))
            rows.append(item)
        hits = [r["kanji"] for r in rows if r["matchedKeywords"]]
        comparisons.update(hits)
        comparisons.update(DISTRACTORS[ch])
        write(PACKET / "scans-003" / (ch + ".json"), {**old, "expandedKeywords": sorted(keywords), "rows": rows, "matches": hits,
              "expansion": "Positive Nikkoku/Daijisen standalone secondary senses and Jitsu historical character glosses, plus English morphological alternatives; source claims remain qualified, not discarded as rare."})
    originals, selected, queries = {}, {}, {}
    exact = comparisons | {"羂", "罠", "網", "掛ける", "かとり", "虹", "霓", "茉", "絹"}
    extra_readings = set(r for ch in CHARS for r in EXTRAS[ch])
    for name, (filename, compressed_sha, xml_sha, tag) in INPUTS.items():
        path = ROOT / "control" / "inputs" / filename
        with path.open("rb") as stream:
            digest = __import__("hashlib").sha256()
            for chunk in iter(lambda: stream.read(65536), b""):
                guard.check()
                digest.update(chunk)
        assert digest.hexdigest() == compressed_sha
        chosen, hashes = {}, {}
        with gzip.open(path, "rb") as stream:
            reader = HashReader(stream, guard)
            context = ET.iterparse(reader, events=("start", "end"))
            _, root = next(context)
            for event, node in context:
                if event != "end" or node.tag != tag:
                    continue
                if name == "jmdict":
                    eid = node.findtext("ent_seq")
                    kebs = {k.text for k in node.findall("k_ele/keb")}
                    rebs = {r.text for r in node.findall("r_ele/reb")}
                    predicates = [f"exact-spelling:{k}" for k in sorted(exact & kebs)] + [f"exact-reading:{r}" for r in sorted(extra_readings & rebs)]
                    admit = bool(predicates)
                    if admit:
                        queries[eid] = predicates
                else:
                    eid = node.findtext("literal")
                    admit = eid in comparisons
                if admit:
                    chosen[eid] = copy.deepcopy(node)
                    hashes[eid] = sha(canonical(node).encode())
                node.clear()
                root.clear()
        assert reader.digest.hexdigest() == xml_sha
        selected[name], originals[name] = chosen, hashes
    assert set(selected["kanjidic2"]) == comparisons
    outputs = {}
    for name, filename in [("jmdict", "jmdict-supplemental-comparisons-002.xml"), ("kanjidic2", "kanjidic2-comparison-records-003.xml")]:
        root = ET.Element("JMdict" if name == "jmdict" else "kanjidic2")
        root.extend(selected[name].values())
        ET.indent(root, space="  ")
        raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
        write(PACKET / filename, raw)
        actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
        assert actual == originals[name]
        outputs[filename] = {"sha256": sha(raw), "bytes": len(raw), "completeCanonicalEquality": True, "canonicalRecordHashes": actual}
    for ch in comparisons:
        path = PACKET / "comparison-cards" / (ch + ".md")
        if not path.exists():
            write(path, git("show", f"{BASE}:kanji/{ch}.md"))
    write(PACKET / "supplement-query-membership-002.json", queries)
    write(PACKET / "supplement-receipt-002.json", {"base": BASE, "inputs": {n: {"filename": v[0], "compressedSha256": v[1], "decompressedSha256": v[2]} for n, v in INPUTS.items()},
          "predicate": "Every complete exact-keb family for each actual comparison character and explicit lexical queries, union every complete exact-reb family for supplemental keys. Predicates listed per entry; not a target-containing query or an allocation of compound readings.",
          "outputs": outputs, "distractors": {ch: DISTRACTORS[ch] for ch in CHARS}, "conservativeExternalReadingKeys": {ch: EXTRAS[ch] for ch in CHARS},
          "transformation": "Complete parsed/reserialized XML; not raw source slices.",
          "producerSha256": sha(Path(__file__).read_bytes())})
    for ch in CHARS:
        scan = json.loads((PACKET / "scans-003" / (ch + ".json")).read_text(encoding="utf-8"))
        print(ch, json.dumps([{"kanji": r["kanji"], "title": r["title"], "meanings": r["completeMeanings"], "matched": r["matchedKeywords"]} for r in scan["rows"] if r["matchedKeywords"]], ensure_ascii=False))
    print("comparisons", len(comparisons), "supplementalFamilies", len(selected["jmdict"]))
    lines = []
    for ch in sorted(comparisons):
        card = (PACKET / "comparison-cards" / (ch + ".md")).read_text(encoding="utf-8")
        lines.extend([f"===== {ch} =====", card])
    write(HERE / "comparison-card-readback-003.txt", "\n".join(lines).encode())
finally:
    write(HERE / "supplement-memory-003.json", guard.finish())
