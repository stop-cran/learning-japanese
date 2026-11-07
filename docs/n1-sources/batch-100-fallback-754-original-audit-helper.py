"""Freeze and audit the bounded native-fallback correction, not acceptance."""
import copy
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
S = R / "docs" / "n1-sources"
L = C / "logs" / "c74e7537-1643-4fa7-acc6-1ee654237065"
BASE = "344abbb2195fece3c72e897bda76852c577e1c42"
PREFIX = "batch-100-fallback-754-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_batch import audit as batch_audit
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256
from extract_n1_jmdict import extract


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(p, data):
    assert not p.exists(), p
    p.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(p) == data


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), *args], encoding="utf-8"
    ).strip()


def canonical(e):
    return (e.tag, sorted(e.attrib.items()), (e.text or "").strip(),
            [canonical(v) for v in e])


def frozen():
    snap = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, info in snap["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == snap["jmdict"]["xmlSha256"]
    assert sha(kd) == snap["kanjidic2"]["xmlSha256"]
    return snap, inputs, ET.fromstring(jm), ET.fromstring(kd)


def prepare():
    assert git("rev-parse", "HEAD") == BASE
    snap, inputs, jm, kd = frozen()
    families = {e.findtext("ent_seq"): e for e in jm}
    old_packets = []
    for name in ("batch-015-jmdict.xml", "batch-100-jmdict.xml",
                 "batch-100-comparison-jmdict.xml", "batch-100-correction-jmdict.xml"):
        packet = ET.parse(S / name).getroot()
        assert all(canonical(e) == canonical(families[e.findtext("ent_seq")]) for e in packet)
        old_packets.append({"path": name, "families": len(packet),
                            "sha256": sha((S / name).read_bytes()),
                            "everyCompleteFamilyEqualsFrozenSource": True})
    route_path = R / "docs" / "n1-reviews" / "batch-100-native-753" / "retry" / "n1-100-article-route.json.gz"
    route = json.loads(gzip.decompress(route_path.read_bytes()))
    labels = sorted({(o["kanji"], o["title"])
                     for row in route["productionBuilderN1AndAllExactChoices"]
                     for o in row["options"]})
    assert len(labels) == 23
    queries = {"樹立", "創立", "始める", "創作", "作る", "樹木", "樹脂", "木", "創傷"}
    chosen = [e for e in jm if queries & {v.text for v in e.findall("k_ele/keb")}]
    ids = [e.findtext("ent_seq") for e in chosen]
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snap["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "jmdict.xml")).write_bytes(raw)
    save(S / (PREFIX + "selection.json"), {
        "schemaVersion": 1, "batch": "100", "execution": 754,
        "entryIds": ids, "exactKebQueries": sorted(queries),
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "sourceGzipSha256": snap["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
        "sourceXmlSha256": snap["jmdict"]["xmlSha256"], "packetSha256": sha(raw),
        "selectionRule": "Every full frozen family matching an exact query spelling; all aliases, readings, restrictions and senses retained.",
        "attribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repository NOTICE.",
        "limits": "Extraction/frozen equality is not semantic inspection, frequency or independent review.",
    })
    compact = []
    for e in ET.fromstring(raw):
        for node in e.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(e, encoding="unicode"))
    text = ("\n".join(compact) + "\n").encode()
    (C / (PREFIX + "full-family-reading.txt")).write_bytes(text)
    (S / (PREFIX + "full-family-reading.txt.gz")).write_bytes(gzip.compress(text, mtime=0))
    chars = {e.findtext("literal"): e for e in kd.findall("character")}
    packet = ET.Element("kanjidic2")
    packet.append(copy.deepcopy(kd.find("header")))
    for char, title in labels:
        assert metadata(R, f"kanji/{char}.md")["title"] == title
        packet.append(copy.deepcopy(chars[char]))
    ET.indent(packet, space="  ")
    kd_bytes = ET.tostring(packet, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / (PREFIX + "kanjidic2.xml.gz")).write_bytes(gzip.compress(kd_bytes, mtime=0))
    summaries = []
    for char, title in labels:
        e = chars[char]
        summaries.append({
            "kanji": char, "title": title, "article": f"kanji/{char}.md",
            "articleSha256": sha((R / "kanji" / (char + ".md")).read_bytes()),
            "sourceMeanings": [m.text for m in e.findall("reading_meaning/rmgroup/meaning")
                               if "m_lang" not in m.attrib],
            "sourceOn": [v.text for v in e.findall("reading_meaning/rmgroup/reading")
                         if v.get("r_type") == "ja_on"],
            "sourceKun": [v.text for v in e.findall("reading_meaning/rmgroup/reading")
                          if v.get("r_type") == "ja_kun"],
        })
    save(S / (PREFIX + "sampled-labels.json"), {
        "schemaVersion": 1, "batch": "100", "execution": 754,
        "routePath": str(route_path.relative_to(R)).replace("\\", "/"),
        "routeCompressedSha256": sha(route_path.read_bytes()), "choiceRows": 64,
        "labels": summaries, "limits": "Bounded sampled labels, not every possible random fallback or future pool.",
    })
    save(S / (PREFIX + "source-provenance.json"), {
        "schemaVersion": 1, "batch": "100", "execution": 754,
        "frozenInputsVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "priorPackets": old_packets, "completeFreshApplicableFamilies": ids,
        "rawCharacterRecords": [c for c, _ in labels],
        "rawCharacterPacket": PREFIX + "kanjidic2.xml.gz",
        "rawCharacterPacketSha256": sha((S / (PREFIX + "kanjidic2.xml.gz")).read_bytes()),
        "attribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repository NOTICE.",
        "limits": "Prior185 樹 and137 創 families verified against frozen source, not all freshly semantically rereviewed. Fresh semantic inspection is bounded to the selected complete families, full創/樹 raw records and all23 sampled labels/English meaning sections/source meaning lists. No new public lookup or independent review.",
    })
    print(json.dumps({"families": len(ids), "entryIds": ids, "sampledLabels": 23,
                      "compactFamilyBytes": len(text)}, ensure_ascii=True))


def audit():
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    result = batch_audit(R, "100")
    ledger = load(S / "batch-100-progress.json")
    old_text = subprocess.check_output(
        ["git", "-C", str(R), "show", f"{BASE}:kanji/創.md"]).decode("utf-8")
    text = (R / "kanji" / "創.md").read_text(encoding="utf-8")
    before = "quiz_exclusions: [作, 造, 始, 元, 原, 本, 緒, 産, 設, 初]"
    assert old_text.count(before) == 1
    assert text == old_text.replace(before, before[:-1] + ", 樹]", 1)
    meta = metadata(R, "kanji/創.md")
    assert meta == ledger["proposedMetadata"]
    assert meta["quiz_exclusions"] == list("作造始元原本緒産設初樹")
    assert [r["kanji"] for r in ledger["quizAudit"]["創"]["directExclusions"]] == meta["quiz_exclusions"]
    old_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    changes = []
    verified = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        assert entries.keys() == old_manifest[section].keys()
        for name, expected in entries.items():
            actual = (sha((R / name).read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
            assert actual == expected, name
            if expected != old_manifest[section][name]:
                changes.append(name)
            verified += 1
    assert changes == ["kanji/創.md"] and verified == 8453
    previous_audit = load(S / "batch-100-draft-audit.json")
    baseline = load(S / "baseline-inventory.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in previous_audit["baselineMetadataExceptions"]:
                expected["quiz_exclusions"] = previous_audit["baselineMetadataExceptions"][name]
            if name in previous_audit["baselineKanjiDistractorException"]:
                expected["distractors"] = previous_audit["baselineKanjiDistractorException"][name]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha((R / name).read_bytes()) == info["sha256"]
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    assert git("-c", "core.quotepath=false", "diff", "--name-only", BASE, "--",
               "kanji", "words", "articles", "strokes") == "kanji/創.md"
    for name, level, n in [("words/創作.md", 2, 13), ("words/作る.md", 5, 5)]:
        m = metadata(R, name)
        assert m["jlpt"] == level and len(m["quiz_exclusions"]) == n
        assert m["quiz_exclusions"] == ledger["wordQuizAudit"]["preservedOriginalExclusions"][name]
    assert len(ledger["allMappedReciprocalPairs"]) == 5
    for char, name in ledger["allMappedReciprocalPairs"]:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / f"kanji/{char}.md").read_text(encoding="utf-8")
    from fontTools.ttLib import TTFont
    combined_text = text + "".join(row["after"] for row in ledger["changedReusedPassages"])
    han = sorted({c for c in combined_text if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF or 0xF900 <= ord(c) <= 0xFAFF
                  or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-100-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(C.parent / "kanji-cards-android")
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap]})
    save(S / (PREFIX + "font-audit.json"), {
        "schemaVersion": 1, "batch": "100", "execution": 754,
        "completeArticleScope": ["kanji/創.md"],
        "changedReusedScope": ledger["changedReusedPassages"],
        "actualHanCount": len(han), "actualHan": han,
        "newSince749": sorted(set(han) - set(load(S / "batch-100-correction-font-audit.json")["actualHan"])),
        "fonts": fonts, "freshNativeRenderingAccepted": False,
        "limits": "樹 newly appears in metadata scope. Cmap presence is not readability; absence is not glyph failure. Fresh21-Han/four-family native/rendered acceptance pending.",
    })
    result.update({
        "execution": 754, "changedSince753": changes,
        "exactNewCardOnlyMetadataEdit": True, "runtimeHashesVerified": verified,
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "directKanjiPairs": 11, "newDirectPair": ["創", "樹"],
        "legacy樹Unchanged": True, "wordExclusionsPreserved": [13, 5],
        "allMappedPairs": 5, "directedLinksVerified": 10,
        "actualHanCount": len(han), "nativeAndIndependentConfirmation": "pending",
        "publishedAdditions": 126, "remainingAdditions": 1102,
        "runtimePublished": False, "wholeProjectComplete": False,
    })
    save(S / (PREFIX + "audit.json"), result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "audit": audit}[sys.argv[1]]()
