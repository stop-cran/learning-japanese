import copy
import gzip
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from b130_common import BASE, CHARS, HERE, PACKET, REPO, ROOT, git, normalized, sha, start_guard, write
from survey_b130 import HashReader, INPUTS, PageText, canonical, output_xml

EXTRA_TERMS = {
    "塀": "prison jail",
    "拍": "inject injection send transmit insert write mark sprinkle throw cast till pay payment visit bind make prepare perform move impress touch cheer praise encourage",
    "耗": "information report reports notification notify communication communicate letter correspondence inform ruin destroy empty dark disappear perish hate surprise",
}
EXACT = {"囚", "土", "払", "招", "抱", "耕", "毛", "本", "未", "末", "消", "信", "便", "伝", "告", "音", "知", "音耗", "耗る", "囃す", "撫づ", "拊"}
READINGS = {"たより", "へる", "かき", "ひら", "かしわで", "びんざさら", "なでる", "なず", "こする", "しぼる"}

guard = start_guard()
try:
    url = "https://www.kanjipedia.jp/kanji/0006729100"
    with urllib.request.urlopen(url, timeout=30) as response:
        raw, final_url = response.read(), response.url
    guard.check()
    dest = HERE / "external-pages" / "耗-kanjipedia.html"
    write(dest, raw)
    parser = PageText()
    parser.feed(raw.decode("utf-8"))
    text = "\n".join(parser.parts).encode()
    assert "へる・たより" in text.decode() and "①へる。へらす。すりへらす。" in text.decode()
    write(dest.with_suffix(".txt"), text)
    write(PACKET / "supplemental-external-bindings.json", {
        "captures": [{"character": "耗", "provider": "Kanjipedia / Kadokawa Shinjigen", "url": url,
                      "finalUrl": final_url, "capturedAt": datetime.now(timezone.utc).isoformat(),
                      "rawSha256": sha(raw), "rawBytes": len(raw), "textSha256": sha(text), "localRawCapture": str(dest)}],
        "navigationWarning": "Web-search prose supplied inconsistent Kanjipedia paths for all three targets. Only its actual citation 0006729100 was followed and identity/body verified. Other suggested paths were not used as evidence.",
        "excerpt": "②たより。知らせ。「音耗」",
        "disposition": "Positive supplemental character reading/sense, retained independently of the frozen metadata and explicitly tested in host reading model.",
        "completeCapturesCommitted": False})
    filename, compressed_sha, xml_sha, tag = INPUTS["kanjidic2"]
    path = ROOT / "control" / "inputs" / filename
    assert sha(path.read_bytes()) == compressed_sha
    kd = {}
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event == "end" and node.tag == tag:
                kd[node.findtext("literal")] = copy.deepcopy(node)
                node.clear()
                root.clear()
    assert reader.digest.hexdigest() == xml_sha
    comparisons = set(EXACT & {p.stem for p in (REPO / "kanji").glob("*.md")})
    for ch in CHARS:
        old = json.loads((PACKET / "scans" / (ch + ".json")).read_text(encoding="utf-8"))
        terms = set(old["expandedKeywords"]) | set(EXTRA_TERMS[ch].split())
        rows = []
        for item in old["rows"]:
            row = dict(item)
            row["matchedKeywords"] = sorted(terms & set(re.findall("[a-z]+", " ".join([row["title"], *row["completeMeanings"]]).lower())))
            if row["matchedKeywords"]:
                comparisons.add(row["kanji"])
            rows.append(row)
        write(PACKET / "scans-002" / (ch + ".json"), {
            **old, "expandedKeywords": sorted(terms), "rows": rows,
            "matches": [r["kanji"] for r in rows if r["matchedKeywords"]],
            "expansionBasis": "Full monolingual senses plus cautious review of multi-spelling 拍つ family. A phrase/compound sense is not automatically a bare-character sense."})
    for ch in comparisons:
        dest = PACKET / "comparison-cards" / (ch + ".md")
        if not dest.exists():
            write(dest, git("show", f"{BASE}:kanji/{ch}.md"))
    filename, compressed_sha, xml_sha, tag = INPUTS["jmdict"]
    path = ROOT / "control" / "inputs" / filename
    assert sha(path.read_bytes()) == compressed_sha
    selected, membership = {}, {}
    with gzip.open(path, "rb") as stream:
        reader = HashReader(stream, guard)
        context = ET.iterparse(reader, events=("start", "end"))
        _, root = next(context)
        for event, node in context:
            if event != "end" or node.tag != tag:
                continue
            kebs = {k.text for k in node.findall("k_ele/keb")}
            rebs = {r.text for r in node.findall("r_ele/reb")}
            predicates = [f"exact-spelling:{k}" for k in sorted((comparisons | EXACT) & kebs)]
            predicates += [f"exact-reading:{r}" for r in sorted(READINGS & rebs)]
            if predicates:
                eid = node.findtext("ent_seq")
                selected[eid], membership[eid] = copy.deepcopy(node), predicates
            node.clear()
            root.clear()
    assert reader.digest.hexdigest() == xml_sha
    outputs = {
        "jmdict-supplemental-families.xml": output_xml("jmdict-supplemental-families.xml", "JMdict", selected.values(), "jmdict"),
        "kanjidic2-supplemental-comparisons.xml": output_xml("kanjidic2-supplemental-comparisons.xml", "kanjidic2", [kd[c] for c in sorted(comparisons)], "kanjidic2"),
    }
    original = {}
    for n in ET.parse(PACKET / "jmdict-complete-families.xml").getroot():
        original[n.findtext("ent_seq")] = sha(canonical(n).encode())
    overlap = set(original) & selected.keys()
    assert all(original[eid] == sha(canonical(selected[eid]).encode()) for eid in overlap)
    write(PACKET / "supplemental-query-membership.json", membership)
    write(PACKET / "supplemental-source-receipt.json", {
        "base": BASE, "outputs": outputs, "originalInputs": json.loads((PACKET / "source-receipt.json").read_text(encoding="utf-8"))["dictionaryInputs"],
        "predicates": {"exactSpellings": sorted(comparisons | EXACT), "exactReadings": sorted(READINGS)},
        "matchedFamilies": len(selected), "equalDuplicateFamilies": len(overlap),
        "transformation": "Complete parsed/reserialized XML, not raw slices; equality against complete decompressed source records and duplicate equality checked.",
        "producerSha256": sha(__import__("pathlib").Path(__file__).read_bytes())})
    print(json.dumps({"completeSupplementFamilies": len(selected), "equalDuplicates": len(overlap),
                      "comparisonCards": len(list((PACKET / "comparison-cards").glob("*.md"))),
                      "scans": {c: json.loads((PACKET / "scans-002" / (c + ".json")).read_text(encoding="utf-8"))["matches"] for c in CHARS}}, ensure_ascii=False))
finally:
    write(HERE / "supplement-memory-001.json", guard.finish())
