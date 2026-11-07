"""Prepare the first bounded source packet for batch101; no runtime authoring."""
import argparse
import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "a0d936ec-01ae-4b86-bd0f-368644d4eba0"
BASE = "ba1a7f467a2431523e3131d4f259c1d3260c93af"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u529f"
PREFIX = "batch-101-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as manifest_sha256
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".762.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def frozen():
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == snapshot["jmdict"]["xmlSha256"]
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, inputs, ET.fromstring(jm), ET.fromstring(kd)


def start():
    clean(R, BASE)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == BASE
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (761, "100", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1101
    assert not list(S.glob(PREFIX + "*"))
    role = load(L / "preflight-762.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 761
    assert checkpoint["execution761CoordinatorCheckpoint"] == p["execution761CoordinatorCheckpoint"]
    assert not (L / "progress-before-762.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-762.json")
    state = {
        "execution": 762, "batch": "101", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded batch101 initial source-preparation checkpoint for frozen row112 only; no runtime draft, reviewer, Android/native, publication,102 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed before acting. Operative contract, approved issue and final761 inspected directly; historical middle parsed, not freshly semantically re-reviewed. Initial output encoding failure occurred after full loading."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main equals content. Android approved pair-guard/schema-only backport, NOT latest application main. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution762StartingState"] = state
    p.update(batch="101", stage="batch-101-initial-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "101"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 112
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[111] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "101", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+529F in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "jmdict.xml")).write_bytes(raw)
    compact = []
    for entry in ET.fromstring(raw):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    text = ("\n".join(compact) + "\n").encode("utf-8")
    (C / "batch-101-full-family-reading.txt").write_bytes(text)
    (S / (PREFIX + "full-family-reading.txt.gz")).write_bytes(gzip.compress(text, mtime=0))
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == CHAR)))
    ET.indent(selected, space="  ")
    (S / (PREFIX + "kanjidic2.xml")).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "101", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR], "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha((S / (PREFIX + "kanjidic2.xml")).read_bytes()),
        "provenance": "Complete frozen character record/header parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repository NOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m,
                               "sha256": sha(path.read_bytes())})
    save(S / (PREFIX + "source-navigation.json"), {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    progress = {
        "schemaVersion": 1, "batch": "101", "baseCommit": BASE, "membership": [CHAR],
        "sourceRows": [112], "members": [{"kanji": CHAR, "sourceRow": 112}],
        "selectionReason": "Next absent frozen row after published\u5275. Three readings, independent merit/success labels, a Buddhist compound reading and a native lookup reading justify one-character source scope; earlier deferred rows remain pending.",
        "status": "initial-source-packet-only", "drafted": [], "reviewClosed": [], "published": [],
        "sourcePreparationComplete": False, "runtimeChanged": False, "runtimePublished": False,
        "sourceReadingOrder": {k: row["metadata"][k] for k in ("onyomi", "kunyomi")},
        "publishedAdditions": 127, "remainingAdditions": 1101,
        "limits": "Initial member-family packet and navigation only. Complete reading allocation/usefulness, comparison families, quiz/link/font/stroke plan remain required before any runtime draft.",
    }
    save(S / (PREFIX + "membership.json"), progress)
    save(S / (PREFIX + "progress.json"), progress)
    print(json.dumps({"families": len(ids), "compactBytes": len(text),
                      "candidateArticles": [c["article"] for c in candidates]}, ensure_ascii=True))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(child) for child in element))


def archive():
    from html.parser import HTMLParser

    class ArticleText(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.parts = []

        def handle_starttag(self, tag, attrs):
            if tag == "article":
                self.depth += 1
                self.parts.append("\n[DICTIONARY BLOCK]\n")
            if self.depth and tag in {"p", "h2", "h3", "br", "section", "li"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "article" and self.depth:
                self.depth -= 1
                self.parts.append("\n[END BLOCK]\n")

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    raw = (C / "batch-101-character.html").read_bytes()
    parser = ArticleText()
    parser.feed(raw.decode("utf-8"))
    text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                     if line.strip()) + "\n"
    assert "\u529f" in text and "\u3044\u3055\u304a" in text
    assert "\u529f\u5fb3" in text and "\u6210\u529f" in text and len(text) > 500
    page = S / (PREFIX + "character.html.gz")
    page.write_bytes(gzip.compress(raw, mtime=0))
    target = S / (PREFIX + "character-public-text.txt")
    target.write_text(text, encoding="utf-8")
    save(S / (PREFIX + "public-source-receipts.json"), [{
        "url": "https://kotobank.jp/word/%E5%8A%9F-482260",
        "downloadedAt": datetime.now(timezone.utc).isoformat(),
        "rawBytes": len(raw), "rawSha256": sha(raw), "archive": page.name,
        "archiveSha256": sha(page.read_bytes()), "losslessGzip": gzip.decompress(page.read_bytes()) == raw,
        "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
        "inspectedBlocks": "Digital Daijisen noun/character headings; Seisenban Nihon Kokugo Daijiten native reading; Jitsu reading heading.",
        "limits": "Actual raw page archived. Plain text strips links/formatting and does not decode image gaiji. Relevant dictionary blocks inspected, not every linked entry or historical citation. No etymological teaching is adopted.",
    }])
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    svg_raw = (C / "inputs" / "n1-0529f-70a0b7ae.svg").read_bytes()
    blob = hashlib.sha1(f"blob {len(svg_raw)}\0".encode() + svg_raw).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"]
    assert len(svg_raw) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg_raw).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 5
    assert [p.attrib["id"] for p in paths] == [f"kvg:0529f-s{i}" for i in range(1, 6)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg_raw)
    save(S / (PREFIX + "stroke-evidence.json"), {
        "revision": snapshot["kanjivg"]["revision"], "gitBlob": blob,
        "sha256": sha(svg_raw), "bytes": len(svg_raw), "dictionaryStrokeCount": 5,
        "sourceStrokePaths": 5, "converted": False, "nativeDrawingAccepted": False,
        "converterNormalizedSha256": converter,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/0529f.svg",
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repository NOTICE.",
        "limits": "Pinned SVG identity, path order and count only; no generated runtime geometry or font/native acceptance. SVG phonetic tag is not independently adopted as etymology.",
    })
    progress = load(S / (PREFIX + "progress.json"))
    progress.update(sourceObservations=PREFIX + "source-observations.json",
                    nextAction="SAME101 source completion before runtime draft: finalize three reading/curation/usefulness dispositions, inspect full comparison families and exact quiz labels/direct symmetric nontransitive guards, all-mapped+activated links including existing\u6210/\u6210\u529f, proposed Han/font and pinned conversion plan. Preserve all readings and easier word levels. No new support article solely to demonstrate dated/specialist readings. All original acceptance gates remain.")
    save(S / (PREFIX + "progress.json"), progress)
    print("Actual character dictionary and pinned five-path SVG archived.")


def audit():
    snapshot, inputs, jm, kd = frozen()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    assert ids == load(S / (PREFIX + "lexical-selection.json"))["entryIds"]
    assert len(ids) == len(set(ids))
    raw = (S / (PREFIX + "jmdict.xml")).read_bytes()
    assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                          snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    compact = gzip.decompress((S / (PREFIX + "full-family-reading.txt.gz")).read_bytes())
    lines = compact.decode("utf-8").splitlines()
    entries = ET.fromstring(raw).findall("entry")
    assert len(lines) == len(entries) == len(ids)
    assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(lines, entries))
    source_record = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    packet_record = ET.parse(S / (PREFIX + "kanjidic2.xml")).getroot().find("character")
    assert canonical(source_record) == canonical(packet_record)
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD") == BASE and git("rev-parse", "origin/main") == BASE
    clean(A, APP)
    before = load(L / "progress-before-762.json")
    now = load(C / "progress.json")
    mutable = {"batch", "stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    observations = load(S / (PREFIX + "source-observations.json"))
    assert observations["authorInspection"]["completeMemberFamilies"] == len(ids)
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(r["kind"], r["reading"]) for r in observations["readingObservations"]] == expected
    assert all(set(r["entryIds"]) <= set(ids) for r in observations["readingObservations"])
    for item in load(S / (PREFIX + "source-navigation.json"))["candidates"]:
        assert sha((R / item["article"]).read_bytes()) == item["sha256"]
        assert metadata(R, item["article"]) == item["metadata"]
    for record in load(S / (PREFIX + "public-source-receipts.json")):
        archive_raw = (S / record["archive"]).read_bytes()
        assert sha(archive_raw) == record["archiveSha256"]
        assert sha(gzip.decompress(archive_raw)) == record["rawSha256"]
        assert sha((S / record["extractedText"]).read_bytes()) == record["extractedTextSha256"]
    svg = (S / (PREFIX + "kanjivg.svg")).read_bytes()
    evidence = load(S / (PREFIX + "stroke-evidence.json"))
    assert sha(svg) == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 5
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    runtime_count = 0
    for section in ("files", "images", "scenes", "audio", "listening", "curriculum", "listeningTasks",
                    "listeningTaskAudio", "listeningTaskImages"):
        for name, digest in manifest.get(section, {}).items():
            actual = (sha((R / name).read_bytes()) if section in
                      {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                      else manifest_sha256(R / name))
            assert actual == digest, name
            runtime_count += 1
    result = {
        "schemaVersion": 1, "execution": 762, "batch": "101", "baseCommit": BASE,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": len(ids), "exactFreshExtractionMatches": True,
        "compactFullFamilySemanticEquality": True, "completeRawCharacterRecords": 1,
        "rawCharacterSemanticEquality": True, "sourceRow": 112, "kanji": CHAR,
        "metadataReadingEntries": 3, "runtimeBytesUnchanged": True,
        "runtimeManifestHashesVerified": runtime_count,
        "candidateArticles": 2, "pinnedSvgPaths": 5, "geometryConverted": False,
        "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True,
        "limits": "Mechanical packet identity and family retention, not independent review or acceptance; no fresh app/native/phone evidence.",
    }
    save(S / (PREFIX + "initial-packet-audit.json"), result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "packet", "archive", "audit"])
    globals()[parser.parse_args().step]()
