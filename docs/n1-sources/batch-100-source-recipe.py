"""Freeze the first source packet for N1 batch 100; never author runtime content."""
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
L = C / "logs" / "b54e1c11-ed77-4905-8fc1-6f5f338723d1"
BASE = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u5275"
PREFIX = "batch-100-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".745.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (744, "099", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1102
    assert not list(S.glob(PREFIX + "*"))
    role = load(L / "preflight-745.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 744
    assert checkpoint["execution744CoordinatorCheckpoint"] == p["execution744CoordinatorCheckpoint"]
    before = L / "progress-before-745.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 745, "batch": "100", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded batch100 initial source-packet checkpoint for frozen row111 only; no runtime draft, reviewer, Android/native, publication,101 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed. Operative contract, approved issue and final744 directly inspected; historical middle parsed, not freshly semantically re-reviewed. Initial output encoding failure occurred after full loading."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main equals content. Android approved pair-guard/schema-only backport, NOT latest application main. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution745StartingState"] = state
    p.update(batch="100", stage="batch-100-initial-source-packet-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def character_packet(kd, chars, name):
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / (PREFIX + name)).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "100"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 111
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[110] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    selection = {
        "schemaVersion": 1, "batch": "100", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+5275 in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    }
    save(S / (PREFIX + "lexical-selection.json"), selection)
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
    (C / "batch-100-full-family-reading.txt").write_bytes(text)
    (S / (PREFIX + "full-family-reading.txt.gz")).write_bytes(gzip.compress(text, mtime=0))
    character_packet(kd, CHAR, "kanjidic2.xml")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "100", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR], "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha((S / (PREFIX + "kanjidic2.xml")).read_bytes()),
        "provenance": "Complete frozen character record/header parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repositoryNOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m})
    save(S / (PREFIX + "source-navigation.json"), {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    save(S / (PREFIX + "membership.json"), {
        "schemaVersion": 1, "batch": "100", "baseCommit": BASE, "membership": [CHAR],
        "sourceRows": [111], "members": [{"kanji": CHAR, "sourceRow": 111}],
        "selectionReason": "Next absent frozen row after published剰. Six readings, multiple lexical identities and wound/create spelling distinctions justify one-character source scope; earlier deferred rows remain pending.",
        "status": "initial-source-packet-only", "drafted": [], "reviewClosed": [], "published": [],
        "limits": "Source extraction and navigation only. Reading dispositions, useful support, comparison families, quiz/link/font/stroke plan still require evidence-based completion before any runtime draft. No acceptance or publication.",
    })
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

    receipts = []
    for label, url in [
        ("character", "https://kotobank.jp/word/%E5%89%B5-551711"),
        ("sosaku", "https://kotobank.jp/word/%E5%89%B5%E4%BD%9C-89359"),
    ]:
        raw = (C / f"batch-100-{label}.html").read_bytes()
        parser = ArticleText()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert CHAR in text and len(text) > 500
        if label == "sosaku":
            assert "そう‐さく" in text and "つくりごと" in text
        path = S / f"batch-100-{label}.html.gz"
        path.write_bytes(gzip.compress(raw, mtime=0))
        target = S / f"batch-100-{label}-public-text.txt"
        target.write_text(text, encoding="utf-8")
        receipts.append({
            "url": url, "downloadedAt": datetime.now(timezone.utc).isoformat(),
            "rawBytes": len(raw), "rawSha256": sha(raw), "archive": path.name,
            "archiveSha256": sha(path.read_bytes()),
            "losslessGzip": gzip.decompress(path.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "limits": "Actual page bytes archived; article text strips links/formatting and does not decode image gaiji. Author inspected relevant dictionary blocks, not every unrelated book/name entry.",
        })
    save(S / (PREFIX + "public-source-receipts.json"), receipts)
    snapshot, inputs, jm, kd = frozen()
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    svg_path = C / "inputs" / "n1-05275-70a0b7ae.svg"
    raw = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(raw) == row["kanjivgInventory"]["size"]
    svg = ET.fromstring(raw)
    paths = svg.findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 12
    assert [p.attrib["id"] for p in paths] == [f"kvg:05275-s{i}" for i in range(1, 13)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    (S / (PREFIX + "kanjivg.svg")).write_bytes(raw)
    save(S / (PREFIX + "stroke-evidence.json"), {
        "revision": snapshot["kanjivg"]["revision"], "gitBlob": blob,
        "sha256": sha(raw), "bytes": len(raw), "dictionaryStrokeCount": 12,
        "sourceStrokePaths": 12, "converted": False, "nativeDrawingAccepted": False,
        "converterNormalizedSha256": converter,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/05275.svg",
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repository NOTICE.",
        "limits": "Pinned SVG identity and count only; no generated runtime geometry or font/native acceptance. Source phon tags not independently adopted as etymology.",
    })
    progress = load(S / (PREFIX + "membership.json"))
    progress.update(
        sourceObservations=PREFIX + "source-observations.json",
        sourcePreparationComplete=False, runtimeChanged=False, runtimePublished=False,
        sourceReadingOrder={k: row["metadata"][k] for k in ("onyomi", "kunyomi")},
        publishedAdditions=126, remainingAdditions=1102,
        nextAction="SAME100 source completion before runtime draft: finish six evidence-based reading/curation/support dispositions, complete comparison families, actual quiz labels/direct guards, all-mapped links, proposed Han/font and pinned conversion plan. Preserve full source metadata including unresolved ショウ and けず.しける; no invented examples or silent repairs. All original review/native/combined-main/signing/publication gates remain.",
    )
    save(S / (PREFIX + "progress.json"), progress)
    print("Actual public evidence and pinned SVG archived; source completion remains explicit.")


def audit():
    snapshot, inputs, jm, kd = frozen()
    selection = load(S / (PREFIX + "lexical-selection.json"))
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    assert ids == selection["entryIds"] and len(ids) == len(set(ids))
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
    manifest = load(R / "manifest.json")
    before = load(L / "progress-before-745.json")
    now = load(C / "progress.json")
    mutable = {"batch", "stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    observations = load(S / (PREFIX + "source-observations.json"))
    expected_readings = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                         for reading in row["metadata"][field]]
    assert [(r["kind"], r["reading"]) for r in observations["readingObservations"]] == expected_readings
    assert all(set(r["entryIds"]) <= set(ids) for r in observations["readingObservations"])
    assert observations["authorInspection"]["completeMemberFamilies"] == len(ids) == 137
    assert observations["runtimeDrafted"] == observations["reviewClosed"] == observations["published"] == []
    assert not load(S / (PREFIX + "progress.json"))["sourcePreparationComplete"]
    for record in load(S / (PREFIX + "public-source-receipts.json")):
        archive_raw = (S / record["archive"]).read_bytes()
        assert sha(archive_raw) == record["archiveSha256"]
        assert sha(gzip.decompress(archive_raw)) == record["rawSha256"]
        assert sha((S / record["extractedText"]).read_bytes()) == record["extractedTextSha256"]
    result = {
        "schemaVersion": 1, "execution": 745, "batch": "100", "baseCommit": BASE,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": len(ids), "exactFreshExtractionMatches": True,
        "compactFullFamilySemanticEquality": True, "completeRawCharacterRecords": 1,
        "rawCharacterSemanticEquality": True,
        "sourceRow": 111, "kanji": CHAR, "metadataReadingEntries": 6,
        "candidateArticles": len(load(S / (PREFIX + "source-navigation.json"))["candidates"]),
        "runtimeBytesUnchanged": True, "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True,
        "limits": "Mechanical packet identity and full-family retention only, not independent review or acceptance. No runtime authored, no fresh app/native/phone evidence.",
    }
    save(S / (PREFIX + "initial-packet-audit.json"), result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "packet", "archive", "audit"])
    args = parser.parse_args()
    globals()[args.step]()
