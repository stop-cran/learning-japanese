import copy
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from common_132 import BASE, CHARS, HERE, REPO, git, normalized, sha, start_guard, write
from survey_132 import INPUTS, records

OUT = HERE / "source-001"
EXTRA = {
    "墓": "grave graves tomb tombs burial buried bury burying interment inter graveyard cemetery mound mounds monument monumentally marker gravestone gravestones stone headstone memorial funerary sepulchre sepulcher mausoleum barrow graveyard",
    "嵐": "storm storms stormy tempest tempestuous wind windy winds gale gales gust blast hurricane squall typhoon violent violence tumult tumultuous uproar hullabaloo commotion turbulence turbulent turmoil disturbance disturb agitation disorder confusion upheaval conflict dispute discord trouble hardship difficulty difficulty adversity rain rainfall rainy thunder snow blizzard cloud mist fog haze vapor vapour air mountain mountains atmosphere",
}
READINGS = {
    "墓": ["ぼ", "はか", "も", "おくつき", "つか", "むはふ", "くさ"],
    "嵐": ["らん", "あらし", "ぞれ", "ときかぜ", "やまかぜ", "をか", "おか"],
}
CONTAINS = ["墓", "嵐", "嵐"]
CURATED = set("古右川")


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def xml_output(path, tag, nodes):
    nodes = list(nodes)
    original = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in nodes}
    assert len(original) == len(nodes)
    root = ET.Element(tag)
    root.extend(copy.deepcopy(nodes))
    ET.indent(root, space="  ")
    raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    write(path, raw)
    actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
    assert original == actual
    return {"sha256": sha(raw), "bytes": len(raw), "canonicalRecordHashes": actual}


def compact(node):
    return [node.tag, dict(node.attrib), (node.text or "").strip(), [compact(n) for n in node]]


def main():
    guard = start_guard()
    OUT.mkdir()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
        index = {r["kanji"]: r for r in json.loads(index_raw)}
        manifest_raw = git("show", f"{BASE}:manifest.json")
        manifest = json.loads(manifest_raw)
        paths = sorted(p for p in manifest["files"] if p.startswith("kanji/"))
        assert len(paths) == 1257
        kd = {n.findtext("literal"): copy.deepcopy(n) for n in records("kanjidic2", guard)}
        comparisons = set(CURATED)
        scan_results = {}
        for ch in CHARS:
            row = index[ch]
            assert row["statusAtFreeze"] == "pending" and row["article"] not in manifest["files"]
            for kind in ("on", "kun"):
                assert [n.text for n in kd[ch].findall(f"reading_meaning/rmgroup/reading[@r_type='ja_{kind}']")] == row["metadata"][kind + "yomi"]
            literal = set(re.findall("[a-z]+", " ".join(row["metadata"]["meanings"]).lower()))
            keys = literal | set(EXTRA[ch].split())
            rows = []
            for rel in paths:
                guard.check()
                c = Path(rel).stem
                raw = (REPO / rel).read_bytes()
                assert sha(raw.replace(b"\r\n", b"\n")) == manifest["files"][rel]
                match = re.search(r"^title: (.+)$", normalized(REPO / rel), re.M)
                assert match and c in kd
                title = match.group(1)
                meanings = [n.text for n in kd[c].findall("reading_meaning/rmgroup/meaning") if n.get("m_lang") in (None, "en")]
                hits = sorted(keys & set(re.findall("[a-z]+", " ".join([title, *meanings]).lower())))
                rows.append({"kanji": c, "path": rel, "title": title, "completeMeanings": meanings, "matchedKeywords": hits,
                             "baselineWorkingBytesSha256": sha(raw), "baselineNormalizedSha256": manifest["files"][rel]})
                if hits:
                    comparisons.add(c)
            scan = {"base": BASE, "kanji": ch, "literalKeywords": sorted(literal), "expandedKeywords": sorted(keys),
                    "tokenRegex": "[a-z]+", "rows": rows, "matches": [r["kanji"] for r in rows if r["matchedKeywords"]],
                    "limits": "Finite manually expanded keywords against full English KANJIDIC2 meanings and displayed titles, not exhaustive synonym discovery."}
            scan_results[ch] = scan
            write(OUT / "scans" / (ch + ".json"), scan)
        for c in sorted(comparisons):
            write(OUT / "comparison-cards" / (c + ".md"), git("show", f"{BASE}:kanji/{c}.md"))
        for ch in CHARS:
            write(OUT / "baseline-words" / (ch + ".md"), git("show", f"{BASE}:words/{ch}.md"))
        exact = comparisons | set(CHARS)
        readings = set(r for rs in READINGS.values() for r in rs)
        selected, membership = [], {}
        counts = {f"{kind}:{key}": 0 for kind, values in (("contains", CONTAINS), ("exact-spelling", sorted(exact)), ("exact-reading", sorted(readings))) for key in values}
        for node in records("jmdict", guard):
            keb = {n.text for n in node.findall("k_ele/keb")}
            reb = {n.text for n in node.findall("r_ele/reb")}
            predicates = [f"contains:{c}" for c in CONTAINS if any(c in s for s in keb)]
            predicates += [f"exact-spelling:{s}" for s in sorted(keb & exact)]
            predicates += [f"exact-reading:{r}" for r in sorted(reb & readings)]
            if predicates:
                selected.append(copy.deepcopy(node))
                membership[node.findtext("ent_seq")] = predicates
                for predicate in predicates:
                    counts[predicate] += 1
        write(OUT / "query-membership.json", membership)
        outputs = {
            "jmdict-complete-families.xml": xml_output(OUT / "jmdict-complete-families.xml", "JMdict", selected),
            "kanjidic2-targets.xml": xml_output(OUT / "kanjidic2-targets.xml", "kanjidic2", [kd[c] for c in CHARS]),
            "kanjidic2-comparisons.xml": xml_output(OUT / "kanjidic2-comparisons.xml", "kanjidic2", [kd[c] for c in sorted(comparisons)]),
        }
        captures = json.loads((HERE / "survey-001" / "external-bindings.json").read_bytes())
        captures["captures"] = [c for c in captures["captures"] if c["character"] in CHARS]
        assert len(captures["captures"]) == 2 * len(CHARS) and all("error" not in c for c in captures["captures"])
        for item in captures["captures"]:
            raw = Path(item["localRawCapture"])
            assert sha(raw.read_bytes()) == item["rawSha256"] and sha(raw.with_suffix(".txt").read_bytes()) == item["textSha256"]
        write(OUT / "external-capture-bindings.json", captures)
        svgs = {}
        for ch in CHARS:
            row = index[ch]
            url = "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/" + row["kanjivgInventory"]["path"]
            with urllib.request.urlopen(url, timeout=30) as response:
                raw = response.read()
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            assert blob == row["kanjivgInventory"]["sha"] and len(raw) == row["kanjivgInventory"]["size"]
            filename = f"kanjivg/{ord(ch):05x}.svg"
            write(OUT / filename, raw)
            svgs[ch] = {"url": url, "path": filename, "sha256": sha(raw), "gitBlob": blob}
        write(OUT / "source-rows.json", [index[c] for c in CHARS])
        write(OUT / "reading-keys.json", {"testedKeys": READINGS, "limits": "Includes supplemental, name and historical forms to be over-tested; these are not all ordinary character readings."})
        write(OUT / "source-receipt.json", {"base": BASE, "inputs": INPUTS, "outputs": outputs, "containsKeys": CONTAINS,
              "allExactSpellings": sorted(exact), "allExactReadings": sorted(readings), "queryCountsIncludingAbsences": counts,
              "predicate": "Union of complete families with any spelling containing target or explicit variant, exact comparison/support spelling, or exact metadata/supplemental/name reading; no priority or sense filter.",
              "transformation": "Complete parsed/reserialized XML, not raw slices; source and output canonical record equality checked.",
              "kanjivg": svgs, "indexSha256": sha(index_raw), "manifestSha256": sha(manifest_raw),
              "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA 4.0.",
              "kanjivgAttribution": "Copyright Ulrich Apel and contributors, CC BY-SA 3.0.",
              "producerSha256": sha(Path(__file__).read_bytes())})
        for ch in CHARS:
            nodes = [n for n in selected if f"contains:{ch}" in membership[n.findtext("ent_seq")]]
            lines = [json.dumps({"id": n.findtext("ent_seq"), "record": compact(n)}, ensure_ascii=False) for n in nodes]
            write(OUT / f"complete-target-{ch}.jsonl", ("\n".join(lines) + "\n").encode())
        for c in sorted(comparisons):
            card = normalized(OUT / "comparison-cards" / (c + ".md"))
            exact_records = [compact(n) for n in selected if f"exact-spelling:{c}" in membership[n.findtext("ent_seq")]]
            data = {"kanji": c, "completeCard": card, "completeKanjidic": compact(kd[c]), "completeJmdict": exact_records}
            write(OUT / "comparison-readback" / (c + ".json"), data)
        print(json.dumps({"members": CHARS, "families": len(selected), "comparisons": len(comparisons),
                          "matches": {c: [(r["kanji"], r["title"], r["matchedKeywords"]) for r in scan_results[c]["rows"] if r["matchedKeywords"]] for c in CHARS},
                          "absentQueries": [k for k, v in counts.items() if not v]}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()
