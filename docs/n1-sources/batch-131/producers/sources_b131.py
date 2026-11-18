import copy
import hashlib
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from b131_common import BASE, HERE, PACKET, REPO, git, normalized, sha, start_guard, write
from survey_b131 import INPUTS, records, canonical
from survey_b131_002 import xml_output

CHARS = list("衛羊霜")
KEYWORDS = {
    "衛": "defense defence protection guard guards guarding guarded protect protects protecting defend defending defensive safeguard keeper watch ward preserve surround surrounding orbit round circle encircle soldier soldiers military province country territory region boundary patrol encircling",
    "羊": "sheep goat ram ewe lamb paper bill banknote money currency hair barber good auspicious omen lucky wander roam ramble stroll",
    "霜": "frost ice frozen snow white whiten hair grey gray years year time age cold severe harsh sharp intense fierce perish destroy ruin lose loss powder medicine medicinal drug charcoal calcine black ash",
}
EXTRAS = {
    "衛": ["まもる", "まもり", "まほり", "めぐる", "かくむ", "もる", "めぐらす", "かこむ", "い", "もり", "うえい", "ひろ", "よし"],
    "羊": ["ひつじ", "じょう", "しょう"],
    "霜": ["しも", "しょう", "ほろぶ", "うしなう"],
}


def compact(node):
    return [node.tag, dict(node.attrib), (node.text or "").strip(), [compact(n) for n in node]]


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == BASE
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        survey = json.loads((HERE / "survey-002" / "membership.json").read_text(encoding="utf8"))
        index = {r["kanji"]: r for r in survey["rows"]}
        supports = {c: survey["supports"][c] for c in CHARS}
        write(PACKET / "source-rows.json", [index[c] for c in CHARS])
        write(PACKET / "selection.json", {"batch": 131, "base": BASE, "members": CHARS, "allDeclaredSupportArticles": supports,
              "requiredReciprocalPairs": [[c, w] for c in CHARS for w in supports[c]], "deliveredAtBase": 264, "undeliveredAtBase": 964,
              "reason": "Surveyed all five suggestions. Three members/four existing word supports form this independent author packet. Complete positive historical/native secondary evidence for 羊 and 霜 is retained and resolved conservatively, not ignored.",
              "notSelected": {"皇": "Separate packet needed for native/prefix forms, ruler/divinity/brightness/greatness and hurried senses. Positive survey records retained locally; no resolution asserted.",
                              "桜": "Separate packet needed for 17 native secondary senses, title/name uses and supplemental ゆすらうめ. Positive survey retained locally; no resolution asserted."},
              "deferred": {"伯": "row 33; 伯母さん does not establish ハク", "憶": "row 395; unresolved remember/think evidence", "撲": "row 461; 相撲 does not establish ボク"},
              "survey": {"directory": str(HERE / "survey-002"), "membershipSha256": sha((HERE / "survey-002" / "membership.json").read_bytes()),
                         "xmlReceiptSha256": sha((HERE / "survey-002" / "dictionary-receipt.json").read_bytes())},
              "failedAttempts": [{"directory": str(HERE / "survey-001"), "failure": "ElementTree utf8 declaration not accepted on reparse; retained, corrected to utf-8 in 002."},
                                 {"directory": str(HERE / "survey-002"), "failure": "All ten unescaped-Unicode URLs failed before HTTP request. Exact errors retained; percent-encoded fresh captures in external-003."}]})
        write(PACKET / "reading-keys.json", {"testedKeys": EXTRAS, "limits": "Includes positive supplemental/historical forms, modernized kana precautions and name keys; these are not all ordinary character readings."})
        kd = {n.findtext("literal"): copy.deepcopy(n) for n in records("kanjidic2", guard)}
        manifest = json.loads(git("show", f"{BASE}:manifest.json"))
        paths = sorted(p for p in manifest["files"] if p.startswith("kanji/"))
        assert len(paths) == 1254
        comparisons, scans = set("古右石"), {}
        for ch in CHARS:
            row = index[ch]
            for kind in ("on", "kun"):
                assert [n.text for n in kd[ch].findall(f"reading_meaning/rmgroup/reading[@r_type='ja_{kind}']")] == row["metadata"][kind + "yomi"]
            literal = set(re.findall("[a-z]+", " ".join(row["metadata"]["meanings"]).lower()))
            keys = literal | set(KEYWORDS[ch].split())
            rows = []
            for rel in paths:
                guard.check()
                c = rel.split("/")[-1][:-3]
                raw = (REPO / rel).read_bytes()
                assert sha(raw.replace(b"\r\n", b"\n")) == manifest["files"][rel]
                title = re.search(r"^title: (.+)$", normalized(REPO / rel), re.M).group(1)
                means = [n.text for n in kd[c].findall("reading_meaning/rmgroup/meaning") if n.get("m_lang") in (None, "en")]
                hits = sorted(keys & set(re.findall("[a-z]+", " ".join([title, *means]).lower())))
                rows.append({"kanji": c, "path": rel, "title": title, "completeMeanings": means, "matchedKeywords": hits,
                             "baselineWorkingBytesSha256": sha(raw), "baselineNormalizedSha256": manifest["files"][rel]})
                if hits:
                    comparisons.add(c)
            scan = {"base": BASE, "kanji": ch, "literalKeywords": sorted(literal), "expandedKeywords": sorted(keys),
                    "tokenRegex": "[a-z]+", "rows": rows, "matches": [r["kanji"] for r in rows if r["matchedKeywords"]],
                    "limits": "Complete baseline KANJIDIC2 English meanings and actual displayed labels; explicit semantic expansion is finite, not exhaustive synonym discovery."}
            scans[ch] = scan
            write(PACKET / "scans" / (ch + ".json"), scan)
        for c in sorted(comparisons):
            write(PACKET / "comparison-cards" / (c + ".md"), git("show", f"{BASE}:kanji/{c}.md"))
        for ch, words in supports.items():
            for word in words:
                write(PACKET / "baseline-words" / (word + ".md"), git("show", f"{BASE}:words/{word}.md"))
        exact = comparisons | set(CHARS) | {w for ws in supports.values() for w in ws}
        readings = set(r for rs in EXTRAS.values() for r in rs) | {"えい", "え", "よう", "そう"}
        members, selected = {}, []
        for node in records("jmdict", guard):
            keb = {n.text for n in node.findall("k_ele/keb")}
            reb = {n.text for n in node.findall("r_ele/reb")}
            predicates = [f"contains:{c}" for c in [*CHARS, "衞"] if any(c in s for s in keb)]
            predicates += [f"exact-spelling:{s}" for s in sorted(keb & exact)]
            predicates += [f"exact-reading:{r}" for r in sorted(reb & readings)]
            if predicates:
                selected.append(copy.deepcopy(node))
                members[node.findtext("ent_seq")] = predicates
        write(PACKET / "query-membership.json", members)
        outputs = {
            "jmdict-complete-families.xml": xml_output(PACKET / "jmdict-complete-families.xml", "JMdict", selected),
            "kanjidic2-target-records.xml": xml_output(PACKET / "kanjidic2-target-records.xml", "kanjidic2", [kd[c] for c in CHARS]),
            "kanjidic2-comparison-records.xml": xml_output(PACKET / "kanjidic2-comparison-records.xml", "kanjidic2", [kd[c] for c in sorted(comparisons)]),
        }
        captures = json.loads((HERE / "external-003" / "bindings.json").read_text(encoding="utf8"))
        captures["captures"] = [c for c in captures["captures"] if c["character"] in CHARS]
        assert len(captures["captures"]) == 6 and all("error" not in c for c in captures["captures"])
        for item in captures["captures"]:
            from pathlib import Path
            path = Path(item["localRawCapture"])
            assert sha(path.read_bytes()) == item["rawSha256"] and sha(path.with_suffix(".txt").read_bytes()) == item["textSha256"]
        captures["limits"] = "Full external captures stay local. Extracted image glyphs may be missing; source headings are distinguished, not guessed. Only bounded attributable excerpts and authored analysis committed."
        write(PACKET / "external-capture-bindings.json", captures)
        svgs = {}
        for ch in CHARS:
            row = index[ch]
            url = "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/" + row["kanjivgInventory"]["path"]
            with urllib.request.urlopen(url, timeout=30) as response:
                raw = response.read()
            blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            assert blob == row["kanjivgInventory"]["sha"] and len(raw) == row["kanjivgInventory"]["size"]
            filename = f"kanjivg/{ord(ch):05x}.svg"
            write(PACKET / filename, raw)
            svgs[ch] = {"url": url, "path": filename, "sha256": sha(raw), "gitBlob": blob}
        write(PACKET / "source-receipt.json", {"batch": 131, "base": BASE, "inputs": INPUTS, "outputs": outputs,
              "predicate": "Union of complete families with any spelling containing 衛羊霜 or variant 衞; exact spellings of every comparison/support; exact metadata/supplemental/name reading keys. Explicit successful per-entry predicates in query-membership; all requested including absent keys remain in producer.",
              "allExactSpellings": sorted(exact), "allExactReadings": sorted(readings), "containsKeys": list("衛羊霜衞"),
              "transformation": "Complete parsed/reserialized XML, not raw slices; canonical equality with original full decompressed input stream. No priority/rarity/sense filter.",
              "kanjivg": svgs, "indexSha256": survey["indexSha256"],
              "dictionaryAttribution": "Copyright James William Breen and EDRDG, CC BY-SA 4.0.",
              "kanjivgAttribution": "Copyright Ulrich Apel and contributors, CC BY-SA 3.0.",
              "producerSha256": sha(__import__("pathlib").Path(__file__).read_bytes())})
        for c in CHARS:
            nodes = [n for n in selected if f"contains:{c}" in members[n.findtext("ent_seq")] or f"exact-spelling:{c}" in members[n.findtext("ent_seq")]]
            lines = [json.dumps({"id": n.findtext("ent_seq"), "k": [compact(k) for k in n.findall("k_ele")],
                     "r": [compact(r) for r in n.findall("r_ele")], "sense": [compact(s) for s in n.findall("sense")]}, ensure_ascii=False) for n in nodes]
            write(HERE / f"complete-target-{c}.jsonl", ("\n".join(lines) + "\n").encode())
        readback = []
        for c in sorted(comparisons):
            raw = (PACKET / "comparison-cards" / (c + ".md")).read_bytes()
            readback.append(json.dumps({"kanji": c, "completeCard": raw.decode(), "completeKanjidic": compact(kd[c]),
                "completeJmdict": [compact(n) for n in selected if f"exact-spelling:{c}" in members[n.findtext("ent_seq")]]}, ensure_ascii=False))
        for i in range(0, len(readback), 10):
            write(HERE / f"comparison-readback-{i // 10 + 1:02}.jsonl", ("\n".join(readback[i:i + 10]) + "\n").encode())
        print(json.dumps({"members": CHARS, "supports": supports, "families": len(selected), "comparisons": len(comparisons),
              "matches": {c: [{"kanji": r["kanji"], "title": r["title"], "completeMeanings": r["completeMeanings"]} for r in scans[c]["rows"] if r["matchedKeywords"]] for c in CHARS}}, ensure_ascii=False))
    finally:
        write(HERE / "source-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
