"""Prepare the initial source-only packet for N1 batch 103."""
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
L = C / "logs" / "9db45bce-b615-4f35-9337-2087e94c6c4a"
BASE = "a38f4cf554300ce34ee65aada79e87b7c9d0319e"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u52b1"
PREFIX = "batch-103-"
NEXT = (
    "SAME103 source completion BEFORE runtime drafting. Signed initial packet for frozen row114 "
    "\u52b1 preserves/author-inspects47 complete member families/one raw character/FOUR actual "
    "public dictionary pages/pinned7pathSVG. This is NOT a fully prepared authoring plan or "
    "independent review. Finish complete comparison families/actual relevant articles/exact "
    "kanji and word quiz labels/ordinarysecondarysenses/THREE existing defensibly wrong "
    "distractors/direct symmetric NONTRANSITIVE guards/legacyfallbacks. Proposed full readings "
    "in sourceorder [\u30ec\u30a4]/[\u306f\u3052.\u3080,\u306f\u3052.\u307e\u3059], all "
    "three selections/offeredkeys\u308c\u3044/\u306f\u3052\u3080/\u306f\u3052\u307e\u3059. "
    "NecessaryNEW\u6fc0\u52b1\u3052\u304d\u308c\u3044,\u52b1\u3080\u306f\u3052\u3080,"
    "\u52b1\u307e\u3059\u306f\u3052\u307e\u3059; no inferred wordlevels. Modern activity "
    "\u306b\u52b1\u3080 versus person\u3092\u52b1\u307e\u3059; latter is plain godan-su "
    "NOT polite\u52b1\u3080 (\u52b1\u307f\u307e\u3059). Historical transitive/dated "
    "voice-raising/technical/idiom/rare-spelling families remain qualified; no invented "
    "frequency/origin claims. No existing primary word candidates/zero activated baselinepairs. "
    "THREE proposed allmappedpairs/SIXdirections; \u6fc0 has no card, retain word metadata "
    "but no brokenlink/out-of-batchaddition. Preserve existing easier cards/wordidentities/"
    "levels/fullmetadata/order/guards. Finish natural support teaching/exact navigationdiff/"
    "baseline audit/proposedHan/fourfonts/canonicalradical/pinnedconverter plan. Only then "
    "bounded LOCAL UNREVIEWED draft/freeze. All original TWOserialblinddifferentfamilies/"
    "serialinternaltools/originalsessionconfirmation/non-skipped qualifiedAndroid/"
    "ContentSyncONCE/native/rendered/combinedcurrentmain/normalsigning/ownerfastforward/"
    "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry/42MiBcompressed/"
    "80MiBinflated/56MiBretained/perfilepathmedia/verifiedownerissue gates remain. Verify "
    "whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. "
    "Parent5920 ownsrunner.lock: no childacquire/delete/unlock/readprobe; approvedcontrol/"
    "committedsource/frozeninputs only, no optional historicalsessionrecipes. Preserve/report/"
    "yield actualnewdenial/signinghang/uncertainownership. No unreviewedpush,104,authoragents,"
    "concurrentheavywork,secondrunner,signingretry or guardincrease. Published129/1228,1099 "
    "acceptance-remainder unchanged;1125kanji5074words134N1labels139namedmembers+separate"
    "\u5996;125necessarysupportsNOTN1vocabulary. Six separatelyplacedsource"
    "\u4fdd\u6848\u6d3e\u7b2c\u7b56\u7d50 retain earlierN2levels, not issue60accepted "
    "additions; never duplicate/relevel. CompatibleAndroid#132/main2edbf366 plus#125 required; "
    "oldclientsignore. QualifiedsignedAndroidbf30cdead8515739bc0e671d57a54b9a3109dd46 "
    "approvedguard+schemaonlybridges NOTunrelatedlatestmain. Original102finite128optionset/"
    "40labelsemanticacceptanceCLEANonlywithinsample/unrestrictedlivepoolUNVERIFIED; "
    "original780ClaudeNONCOMPLIANT/UNACCEPTED immutable/781dependentsupplementNOTretroacceptance/"
    "782rescaledrenditionsNOToriginalpixels/equalcomprehension/nativespeaker retained. "
    "Original historical readdepth/image/process/permission/OOM/source-only/pending limits "
    "remain, not retroaccepted or freshly certified. Physicalphone/generalrelease/whole-set"
    "outstanding;projectincomplete."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as manifest_sha256
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".785.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (784, "102", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1099
    assert not list(S.glob(PREFIX + "*"))
    role = load(L / "preflight-785.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 784
    assert checkpoint["execution784CoordinatorCheckpoint"] == p["execution784CoordinatorCheckpoint"]
    assert not (L / "progress-before-785.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-785.json")
    state = {
        "execution": 785, "batch": "103", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded batch103 initial source-preparation checkpoint for frozen row114 only; no runtime draft, reviewer, Android/native, publication,104 or second runner.",
        "request": {
            "sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and complete checkpoint recursively traversed before acting. Operative contract, complete approved issue and final784 inspected directly; historical middle parsed, not freshly semantically re-reviewed.",
        },
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main equals content. Android approved pair-guard/schema-only backport, NOT latest application main. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution785StartingState"] = state
    p.update(batch="103", stage="batch-103-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "103"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 114
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[113] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "103", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+52B1 in any keb; preserve all aliases/readings/restrictions/senses.",
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
    (C / "batch-103-full-family-reading.txt").write_bytes(text)
    (S / (PREFIX + "full-family-reading.txt.gz")).write_bytes(gzip.compress(text, mtime=0))
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == CHAR)))
    ET.indent(selected, space="  ")
    (S / (PREFIX + "kanjidic2.xml")).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "103", "baseCommit": BASE, "sourceIndexRecord": row,
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
        "schemaVersion": 1, "batch": "103", "baseCommit": BASE, "membership": [CHAR],
        "sourceRows": [114], "members": [{"kanji": CHAR, "sourceRow": 114}],
        "selectionReason": "Next absent frozen row after published\u52a3. Encouragement versus own diligent effort, transitivity, and three readings justify a one-character source scope; earlier deferred rows remain pending.",
        "status": "initial-source-packet-only", "drafted": [], "reviewClosed": [], "published": [],
        "sourcePreparationComplete": False, "runtimeChanged": False, "runtimePublished": False,
        "sourceReadingOrder": {k: row["metadata"][k] for k in ("onyomi", "kunyomi")},
        "publishedAdditions": 129, "remainingAdditions": 1099,
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

    receipts = []
    for label, url, expected, scope in [
        ("character", "https://kotobank.jp/word/%E5%8A%B1-660815",
         [CHAR, "\u30ec\u30a4", "\u306f\u3052\u3080", "\u306f\u3052\u307e\u3059", "\u6fc0\u52b1"],
         "Digital Daijisen exact character heading, both meanings and compound lists; separate noun and Jitsu historical blocks are not the selected metadata or etymology."),
        ("hagemu", "https://kotobank.jp/word/%E5%8A%B1%E3%82%80-600680",
         ["\u306f\u3052", "\u52b1\u3080", "\u52d5\u30de\u4e94", "\u5b66\u696d", "\u81ea\u52d5\u8a5e", "\u4ed6\u52d5\u8a5e"],
         "Digital Daijisen actual verb heading, godan notation and activity-ni examples; Seisenban's historical transitive examples do not invalidate scoped modern intransitive teaching."),
        ("hagemasu", "https://kotobank.jp/word/%E5%8A%B1%E3%81%BE%E3%81%99-600677",
         ["\u306f\u3052\u307e", "\u52b1\u307e\u3059", "\u52d5\u30b5\u4e94", "\u5143\u6c17", "\u58f0"],
         "Digital Daijisen actual verb heading and encouragement versus forceful-voice senses; conjugational dot in hagemasu headword is not the KANJIDIC okurigana boundary."),
        ("gekirei", "https://kotobank.jp/word/%E6%BF%80%E5%8A%B1-489780",
         ["\u3052\u304d", "\u308c\u3044", "\u6fc0\u52b1", "\u9078\u624b\u56e3"],
         "Digital Daijisen exact noun/suru heading and encouraging the team example; separate historical self-exertion sense is not taught as the unrestricted modern core."),
    ]:
        source = C / f"batch-103-{label}.html"
        raw = source.read_bytes()
        parser = ArticleText()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert all(word in text for word in expected), label
        page = S / (PREFIX + label + ".html.gz")
        page.write_bytes(gzip.compress(raw, mtime=0))
        target = S / (PREFIX + label + "-public-text.txt")
        target.write_text(text, encoding="utf-8")
        receipts.append({
            "url": url, "downloadedAt": datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).isoformat(),
            "rawBytes": len(raw), "rawSha256": sha(raw), "archive": page.name,
            "archiveSha256": sha(page.read_bytes()), "losslessGzip": gzip.decompress(page.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "inspectedBlocks": scope,
            "limits": "Actual raw page archived. Plain text strips links/formatting and does not decode image gaiji. Relevant dictionary blocks inspected, not every linked entry or historical citation. No etymological teaching is adopted.",
        })
    save(S / (PREFIX + "public-source-receipts.json"), receipts)
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    svg_raw = (C / "inputs" / "n1-052b1-70a0b7ae.svg").read_bytes()
    blob = hashlib.sha1(f"blob {len(svg_raw)}\0".encode() + svg_raw).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"]
    assert len(svg_raw) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg_raw).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 7
    assert [p.attrib["id"] for p in paths] == [f"kvg:052b1-s{i}" for i in range(1, 8)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg_raw)
    save(S / (PREFIX + "stroke-evidence.json"), {
        "revision": snapshot["kanjivg"]["revision"], "gitBlob": blob,
        "sha256": sha(svg_raw), "bytes": len(svg_raw), "dictionaryStrokeCount": 7,
        "sourceStrokePaths": 7, "converted": False, "nativeDrawingAccepted": False,
        "converterNormalizedSha256": converter,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/052b1.svg",
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repository NOTICE.",
        "limits": "Pinned SVG identity, path order and count only; no generated runtime geometry or font/native acceptance. SVG grouping is not independently adopted as etymology.",
    })
    progress = load(S / (PREFIX + "progress.json"))
    progress.update(sourceObservations=PREFIX + "source-observations.json",
                    nextAction="SAME103 source completion before runtime draft: finalize three reading/curation/usefulness dispositions, inspect full comparison families and exact quiz labels/direct symmetric nontransitive guards, necessary three support articles, all-mapped+activated links, proposed Han/font and pinned conversion plan. Preserve all readings and easier decks. All original acceptance gates remain.")
    save(S / (PREFIX + "progress.json"), progress)
    print("Four actual dictionary pages and pinned seven-path SVG archived.")


def audit():
    snapshot, inputs, jm, kd = frozen()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    assert ids == load(S / (PREFIX + "lexical-selection.json"))["entryIds"]
    assert len(ids) == len(set(ids)) == 47
    raw = (S / (PREFIX + "jmdict.xml")).read_bytes()
    assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                          snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    lines = gzip.decompress((S / (PREFIX + "full-family-reading.txt.gz")).read_bytes()).decode("utf-8").splitlines()
    entries = ET.fromstring(raw).findall("entry")
    assert len(lines) == len(entries) == len(ids)
    assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(lines, entries))
    source_record = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    packet_record = ET.parse(S / (PREFIX + "kanjidic2.xml")).getroot().find("character")
    assert canonical(source_record) == canonical(packet_record)
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    for word in ("\u52b1\u3080", "\u52b1\u307e\u3059", "\u6fc0\u52b1"):
        assert not (R / "words" / (word + ".md")).exists()
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD") == BASE and git("rev-parse", "origin/main") == BASE
    clean(A, APP)
    before = load(L / "progress-before-785.json")
    now = load(C / "progress.json")
    mutable = {"batch", "stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    observations = load(S / (PREFIX + "source-observations.json"))
    assert observations["authorInspection"]["completeMemberFamilies"] == len(ids)
    expected = [(kind, reading) for kind, field in [("on", "onyomi"), ("kun", "kunyomi")]
                for reading in row["metadata"][field]]
    assert [(r["kind"], r["reading"]) for r in observations["readingObservations"]] == expected
    assert all(set(r["entryIds"]) <= set(ids) for r in observations["readingObservations"])
    navigation = load(S / (PREFIX + "source-navigation.json"))
    assert navigation["candidates"] == [] and navigation["baselinePairs"] == []
    proposed_readings = {"\u3052\u304d\u308c\u3044", "\u306f\u3052\u3080", "\u306f\u3052\u307e\u3059"}
    reading_candidates = [
        path.name for path in (R / "words").glob("*.md")
        if metadata(R, path.relative_to(R).as_posix())["reading"] in proposed_readings
    ]
    assert reading_candidates == [], reading_candidates
    for name in observations["authorInspection"]["existingArticlesReadCompletely"]:
        assert (R / name).is_file()
    for record in load(S / (PREFIX + "public-source-receipts.json")):
        archive_raw = (S / record["archive"]).read_bytes()
        assert sha(archive_raw) == record["archiveSha256"]
        assert sha(gzip.decompress(archive_raw)) == record["rawSha256"]
        assert sha((S / record["extractedText"]).read_bytes()) == record["extractedTextSha256"]
    svg = (S / (PREFIX + "kanjivg.svg")).read_bytes()
    evidence = load(S / (PREFIX + "stroke-evidence.json"))
    assert sha(svg) == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 7
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
        "schemaVersion": 1, "execution": 785, "batch": "103", "baseCommit": BASE,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": len(ids), "exactFreshExtractionMatches": True,
        "compactFullFamilySemanticEquality": True, "completeRawCharacterRecords": 1,
        "rawCharacterSemanticEquality": True, "sourceRow": 114, "kanji": CHAR,
        "metadataReadingEntries": 3, "runtimeBytesUnchanged": True,
        "runtimeManifestHashesVerified": runtime_count,
        "candidateArticles": 0, "primaryReadingCandidates": 0,
        "activatedBaselinePairs": 0, "pinnedSvgPaths": 7,
        "geometryConverted": False, "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True,
        "limits": "Mechanical packet identity and family retention, not independent review or acceptance; no fresh app/native/phone evidence.",
    }
    save(S / (PREFIX + "initial-packet-audit.json"), result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    checks = {}
    for label in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                  "vocabulary", "audit", "whitespace"]:
        source = L / f"{label}-785.txt"
        raw = source.read_bytes()
        target = S / f"batch-103-{label}-785.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    tests = (L / "source-tests-785.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-785.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    audit_result = load(S / "batch-103-initial-packet-audit.json")
    assert audit_result["runtimeManifestHashesVerified"] == 8458
    assert audit_result["completeMemberFamilies"] == 47
    helpers = {}
    for name, target in [
        ("source-785.py", "batch-103-source-recipe.py"),
        ("preflight-785.ps1", "batch-103-preflight-785.ps1.txt"),
        ("checks-source-785.ps1", "batch-103-checks-source-785.ps1.txt"),
    ]:
        shutil.copyfile(C / name, S / target)
        assert (C / name).read_bytes() == (S / target).read_bytes()
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-785.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    shutil.copyfile(L / "preflight-785.json", S / "batch-103-runner-role-785.json")
    save(S / "execution-785.json", {
        "schemaVersion": 1, "execution": 785, "checkpoint": 785, "batch": "103",
        "stage": "batch-103-initial-source-packet-prepared-not-authoring-ready",
        "baseCommit": BASE, "androidSignedHead": APP, "membership": [CHAR], "sourceRows": [114],
        "sourcePacketAudit": audit_result, "sourceObservations": "batch-103-source-observations.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 129, "remainingAdditions": 1099,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Normally signed LOCAL source-only checkpoint; no push, independent content review, app/native acceptance or runtime publication. Original checkpoints and all acceptance gates remain historical/intact. Vocabulary checker retains its reported pilot coverage, not whole-corpus completion.",
    })
    print("Source evidence, validations, runner role and durable helpers archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    body = (
        "Batch 103 / checkpoint 785: **LOCAL source-only checkpoint**, not newly published teaching.\n\n"
        f"Normally signed saved commit: `{head}`; published main remains `{BASE}`.\n\n"
        "Frozen row 114 励: retained and author-inspected all 47 complete applicable JMdict "
        "families, the full character record, actual 励/励む/励ます/激励 dictionary headings "
        "and the pinned seven-path SVG (not converted). Verified all five frozen inputs and "
        "both decompressed dictionary hashes. Full レイ / はげ.む, はげ.ます metadata order "
        "is preserved. All three are proposed for practice with necessary 激励げきれい, "
        "励むはげむ and 励ますはげます support articles; no vocabulary level is inferred. "
        "There is no matching primary word article or frozen activated word pair to reuse.\n\n"
        "Key teaching boundaries recorded: activity に励む versus encouraging someone を励ます; "
        "励ます is a plain godan-su verb, not the polite form of 励む (励みます). Historical "
        "transitive, dated voice-raising, technical, idiom and rare-spelling evidence remains "
        "qualified. Three proposed all-mapped pairs/six directions; 激 has no card and is "
        "retained in proposed word metadata without a broken link or out-of-batch addition. "
        "Complete comparison families, exact meaning labels, three wrong choices, direct "
        "symmetric nontransitive safeguards, support teaching, navigation and Han/font plan "
        "remain source-completion work **before any runtime draft**. No reviewer, Android/"
        "native run, phone evidence or runtime publication is claimed.\n\n"
        "43 focused source tests, structural validation, unchanged regenerated manifest, "
        "vocabulary consistency (its existing pilot coverage remains incomplete), archive "
        "budgets and exact packet audit passed. All 8,458 runtime manifest hashes and "
        "contentVersion `f376333b242ebb23` remain unchanged. No guard was raised. Live "
        "parent launcher/decoded command/exact session/ancestry were verified without "
        "touching its lock. Helpers are in approved control and archived with this packet; "
        "no historical session recipe was accessed and no new permission denial occurred.\n\n"
        "**129/1,228 additions published; 1,099 acceptance remainder unchanged.** Compatible "
        "stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 mechanisms "
        "remain required; six separately placed source members retain earlier N2 levels and "
        "are not newly counted accepted additions. Physical-phone, general-release and "
        "whole-set acceptance remain outstanding. Prior batch 102 finite semantic-sample "
        "and reviewer-process/image limits remain as recorded, not expanded or "
        "retroaccepted. Next: same103 source completion only, preserving every original "
        "gate; no next batch or second runner.\n"
    )
    (C / "issue-785.txt").write_text(body, encoding="utf-8", newline="\n")
    save(C / "issue-request-785.json", {"body": body})
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    clean(A, APP)
    assert git("rev-parse", "origin/main") == BASE
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert changed and all(p.startswith("docs/n1-sources/batch-103-") or
                           p == "docs/n1-sources/execution-785.json" for p in changed)
    assert not git("diff", BASE, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    posted = load(L / "issue-785-verified.json")
    expected_body = (C / "issue-785.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == expected_body
    assert "LOCAL source-only" in expected_body and head in expected_body
    before = load(L / "progress-before-785.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    receipt = {
        "schemaVersion": 1, "execution": 785, "checkpoint": 785, "batch": "103",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-785.json", "membership": [CHAR], "sourceRows": [114],
        "completeMemberFamilies": 47, "metadataReadingEntries": 3, "publicDictionaryPages": 4,
        "sourcePreparationComplete": False, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 129, "remainingAdditions": 1099,
        "lastPublishedCommit": BASE, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-103-initial-source-packet-prepared-not-authoring-ready",
        "runtimeManifestHashesVerified": 8458, "contentVersion": "f376333b242ebb23",
        "sourceTestsPassed": 43, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None,
    }
    p["execution785StartingState"]["status"] = "signed-local-initial-source-checkpoint-complete"
    p["execution785CoordinatorCheckpoint"] = receipt
    p["batch103SourceIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": sha(expected_body.encode("utf-8")), "verified": True,
    }
    p.update(checkpoint=785, status="continue", batch="103", stage=receipt["stage"],
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-785-final-verification.json", receipt)
    print(json.dumps(receipt, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "packet", "archive", "audit", "record", "issue", "finish"])
    globals()[parser.parse_args().step]()
