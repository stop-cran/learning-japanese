import copy
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from common_134 import BASE, HERE, INPUTS, REPO, ROOT, canonical, git, normalized, records, sha, start_guard, write, xml_output

CHARS = "紫"
OUT = HERE / "source-002"
SUPPORTS = {"紫": ["紫"]}
CURATED = {"紫": list("古右川")}
EXTRA = {
    "紫": "purple violet color colour colors colours gromwell plant plants herb herbs root roots dye dyed dyeing cloth paper fabric woman women female girl soy sauce condiment sardine sardines fish blind blindness rank court palace sacred beautiful beauty wrap wrapping tale story stories novel fiction literary literature book books writing relationship connection city cities capital tokyo edo",
}
READINGS = {
    "紫": ["し", "むらさき", "ゆかり", "さい", "つつむ"],
}
CONTAINS = ["紫", "茈"]
ADDITIONAL_EXACT = {"茈", "醤油", "鰯", "紫色", "紫草", "紫根", "染料",
                    "紫陽花", "紫外線", "江戸", "紫式部", "源氏物語"}


def compact(node):
    return [node.tag, dict(node.attrib), (node.text or "").strip(), [compact(n) for n in node]]


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        index_raw = git("show", f"{BASE}:docs/n1-sources/source-index.json")
        index = {r["kanji"]: r for r in json.loads(index_raw)}
        manifest_raw = git("show", f"{BASE}:manifest.json")
        manifest = json.loads(manifest_raw)
        paths = sorted(p for p in manifest["files"] if p.startswith("kanji/"))
        kd = {n.findtext("literal"): copy.deepcopy(n) for n in records("kanjidic2", guard)}
        comparisons = set(c for cs in CURATED.values() for c in cs)
        scans = {}
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
                title = re.search(r"^title: (.+)$", normalized(REPO / rel), re.M).group(1)
                meanings = [n.text for n in kd[c].findall("reading_meaning/rmgroup/meaning") if n.get("m_lang") in (None, "en")]
                hits = sorted(keys & set(re.findall("[a-z]+", " ".join([title, *meanings]).lower())))
                rows.append({"kanji": c, "path": rel, "title": title, "completeMeanings": meanings, "matchedKeywords": hits,
                             "baselineWorkingBytesSha256": sha(raw), "baselineNormalizedSha256": manifest["files"][rel]})
                if hits:
                    comparisons.add(c)
            scan = {"base": BASE, "kanji": ch, "literalKeywords": sorted(literal), "expandedKeywords": sorted(keys),
                    "tokenRegex": "[a-z]+", "rows": rows, "matches": [r["kanji"] for r in rows if r["matchedKeywords"]],
                    "limits": "Finite manually expanded keywords against complete English KANJIDIC2 meanings and displayed titles, not exhaustive synonym discovery."}
            scans[ch] = scan
            write(OUT / "scans" / (ch + ".json"), scan)
        exact = set(CHARS) | comparisons | ADDITIONAL_EXACT | {w for ws in SUPPORTS.values() for w in ws}
        for c in sorted(comparisons):
            raw = git("show", f"{BASE}:kanji/{c}.md")
            write(OUT / "comparison-cards" / (c + ".md"), raw)
            text = raw.replace(b"\r\n", b"\n").decode()
            exact.update(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", text))
        for ws in SUPPORTS.values():
            for w in ws:
                write(OUT / "baseline-words" / (w + ".md"), git("show", f"{BASE}:words/{w}.md"))
        readings = set(r for rs in READINGS.values() for r in rs)
        selected, membership = [], {}
        counts = {f"{kind}:{key}": 0 for kind, values in (("contains", CONTAINS), ("exact-spelling", sorted(exact)), ("exact-reading", sorted(readings))) for key in values}
        for n in records("jmdict", guard):
            keb = {x.text for x in n.findall("k_ele/keb")}
            reb = {x.text for x in n.findall("r_ele/reb")}
            predicates = [f"contains:{c}" for c in CONTAINS if any(c in s for s in keb)]
            predicates += [f"exact-spelling:{s}" for s in sorted(keb & exact)]
            predicates += [f"exact-reading:{r}" for r in sorted(reb & readings)]
            if predicates:
                selected.append(copy.deepcopy(n))
                membership[n.findtext("ent_seq")] = predicates
                for predicate in predicates:
                    counts[predicate] += 1
        write(OUT / "query-membership.json", membership)
        outputs = {
            "jmdict-complete-families.xml": xml_output(OUT / "jmdict-complete-families.xml", "JMdict", selected),
            "kanjidic2-targets.xml": xml_output(OUT / "kanjidic2-targets.xml", "kanjidic2", [kd[c] for c in CHARS]),
            "kanjidic2-comparisons.xml": xml_output(OUT / "kanjidic2-comparisons.xml", "kanjidic2", [kd[c] for c in sorted(comparisons)]),
        }
        captures = json.loads((HERE / "survey-001" / "reused-capture-bindings.json").read_bytes())
        captures["captures"] = [c for c in captures["captures"] if c["character"] in CHARS]
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
        write(OUT / "reading-keys.json", {"testedKeys": READINGS, "limits": "Supplemental, name, historical and variant forms deliberately over-tested; not all ordinary independent modern readings."})
        write(OUT / "source-receipt.json", {"base": BASE, "inputs": INPUTS, "outputs": outputs, "containsKeys": CONTAINS,
              "allExactSpellings": sorted(exact), "allExactReadings": sorted(readings), "queryCountsIncludingAbsences": counts,
              "predicate": "Union of complete families with any spelling containing 紫 or explicit search-only 茈 variant, exact comparison/support, source-driven or linked comparison-word spelling, or exact metadata/supplemental/historical reading; no priority or sense filter.",
              "transformation": "Complete parsed/reserialized XML, not raw slices; source and output canonical record equality checked.",
              "kanjivg": svgs, "indexSha256": sha(index_raw), "manifestSha256": sha(manifest_raw),
              "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA 4.0.",
              "kanjivgAttribution": "Copyright Ulrich Apel and contributors, CC BY-SA 3.0.",
              "producerSha256": sha(Path(__file__).read_bytes())})
        for ch in CHARS:
            nodes = [n for n in selected if any(
                f"contains:{form}" in membership[n.findtext("ent_seq")]
                for form in (ch, "茈")
            )]
            write(OUT / f"complete-target-{ch}.jsonl", ("\n".join(json.dumps({"id": n.findtext("ent_seq"), "record": compact(n)}, ensure_ascii=False) for n in nodes) + "\n").encode())
        for c in sorted(comparisons):
            card = normalized(OUT / "comparison-cards" / (c + ".md"))
            words = {c} | set(re.findall(r"\]\(\.\./words/([^/)]+)\.md\)", card))
            matching = [compact(n) for n in selected if any(f"exact-spelling:{w}" in membership[n.findtext("ent_seq")] for w in words)]
            write(OUT / "comparison-readback" / (c + ".json"), {"kanji": c, "completeCard": card, "completeKanjidic": compact(kd[c]), "completeApplicableJmdict": matching})
        print(json.dumps({"members": CHARS, "families": len(selected), "comparisons": len(comparisons),
                          "matches": {c: [(r["kanji"], r["title"], r["matchedKeywords"]) for r in scans[c]["rows"] if r["matchedKeywords"]] for c in CHARS},
                          "absentQueries": [k for k, v in counts.items() if not v]}, ensure_ascii=False))
    finally:
        write(OUT / "memory.json", guard.finish())


if __name__ == "__main__":
    main()
