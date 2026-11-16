import copy
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from b129_common import BASE, CHARS, HERE, PACKET, REPO, ROOT, git, sha, start_guard, write
from extract_b129 import HashReader, INPUTS, canonical

guard = start_guard()
try:
    comparisons = set("木綿末衣")
    scans = {}
    for ch in CHARS:
        old = json.loads((PACKET / "scans-003" / (ch + ".json")).read_text(encoding="utf8"))
        keywords = set(old["expandedKeywords"])
        if ch == "茉":
            keywords.update("tree trees woody bush bushes".split())
        rows = []
        for row in old["rows"]:
            tokens = set(re.findall("[a-z]+", " ".join([row["title"], *row["completeMeanings"]]).lower()))
            rows.append({**row, "matchedKeywords": sorted(keywords & tokens)})
        scans[ch] = {**old, "expandedKeywords": sorted(keywords), "rows": rows,
                     "matches": [r["kanji"] for r in rows if r["matchedKeywords"]],
                     "finalExpansion": "Include broader woody-plant categories for jasmine; do not call distinct tree species synonyms. Extra source-positive pairs may be admitted independently of token hits."}
        comparisons.update(scans[ch]["matches"])
        card = (REPO / "kanji" / (ch + ".md")).read_text(encoding="utf8")
        for field in ("distractors", "quiz_exclusions"):
            comparisons.update(re.search(r"^" + field + r": \[([^]]*)\]$", card, re.M).group(1).split(", "))
    assert "" not in comparisons
    for ch in comparisons:
        assert git("ls-tree", BASE, "--", f"kanji/{ch}.md"), ch
    selected, memberships, originals = {}, {}, {}
    for name, (filename, compressed_sha, decompressed_sha, tag) in INPUTS.items():
        path = ROOT / "control" / "inputs" / filename
        digest = hashlib.sha256()
        with path.open("rb") as stream:
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
                eid = node.findtext("ent_seq") if name == "jmdict" else node.findtext("literal")
                if name == "jmdict":
                    matches = comparisons & {k.text for k in node.findall("k_ele/keb")}
                    admit = bool(matches)
                    if admit:
                        memberships[eid] = [f"exact-spelling:{s}" for s in sorted(matches)]
                else:
                    admit = eid in comparisons
                if admit:
                    chosen[eid] = copy.deepcopy(node)
                    hashes[eid] = sha(canonical(node).encode())
                node.clear()
                root.clear()
        assert reader.digest.hexdigest() == decompressed_sha
        selected[name], originals[name] = chosen, hashes
    assert set(selected["kanjidic2"]) == comparisons
    outputs = {}
    for name, filename in [("jmdict", "jmdict-final-comparisons.xml"), ("kanjidic2", "kanjidic2-final-comparisons.xml")]:
        root = ET.Element("JMdict" if name == "jmdict" else "kanjidic2")
        root.extend(selected[name].values())
        ET.indent(root, space="  ")
        raw = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
        actual = {n.findtext("ent_seq") or n.findtext("literal"): sha(canonical(n).encode()) for n in ET.fromstring(raw)}
        assert actual == originals[name]
        write(PACKET / filename, raw)
        outputs[filename] = {"sha256": sha(raw), "bytes": len(raw), "completeCanonicalEquality": True, "canonicalRecordHashes": actual}
    new_cards = []
    for ch in sorted(comparisons):
        path = PACKET / "comparison-cards" / (ch + ".md")
        raw = git("show", f"{BASE}:kanji/{ch}.md")
        if path.exists():
            assert path.read_bytes() == raw
        else:
            write(path, raw)
            new_cards.append(ch)
    for ch in CHARS:
        write(PACKET / "scans-004" / (ch + ".json"), scans[ch])
    write(PACKET / "final-query-membership.json", memberships)
    write(PACKET / "final-source-receipt.json", {
        "base": BASE, "comparisons": sorted(comparisons),
        "inputs": {n: {"filename": v[0], "compressedSha256": v[1], "decompressedSha256": v[2]} for n, v in INPUTS.items()},
        "predicate": "Every complete exact-keb family for every finite final comparison character, including each scan hit, direct guard, curated choice and additional documented comparison. Full character records for the same finite set.",
        "outputs": outputs, "newComparisonCards": new_cards,
        "transformation": "Complete parsed/reserialized records; not raw source slices.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    })
    write(HERE / "new-comparison-readback-004.txt", "\n".join(
        f"===== {ch} =====\n" + (PACKET / "comparison-cards" / (ch + ".md")).read_text(encoding="utf8")
        for ch in new_cards).encode())
    union = {}
    for filename in ("jmdict-complete-families.xml", "jmdict-supplemental-comparisons-002.xml", "jmdict-final-comparisons.xml"):
        for node in ET.parse(PACKET / filename).getroot():
            eid = node.findtext("ent_seq")
            digest = sha(canonical(node).encode())
            if eid in union:
                assert union[eid] == digest, eid
            union[eid] = digest
    write(PACKET / "complete-family-union.json", {"families": len(union), "canonicalRecordHashes": union,
        "deduplication": "Canonical complete-record equality checked before collapsing duplicate entry IDs; no lossy summary is the authority."})
    print(json.dumps({"comparisons": len(comparisons), "families": len(union), "newCards": new_cards,
                      "scanMatches": {c: scans[c]["matches"] for c in CHARS}}, ensure_ascii=False))
finally:
    write(HERE / "final-source-memory-002.json", guard.finish())
