"""Prepare and checkpoint the bounded initial source packet for N1 batch 104."""
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
L = C / "logs" / "ca0c73bd-9afa-40ee-b78c-8569d573ad15"
BASE = "2491799cffe960a7664a6135614b452e24dce459"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u52be"
PREFIX = "batch-104-"
NEXT = (
    "SAME104 bounded source completion BEFORE any runtime draft. Initial signed source-only "
    "packet for frozen row115 劾 retains/author-inspects all FOUR complete member families, "
    "ONE full raw character, THREE actual public pages (Kotobank character; Kotobank word "
    "encyclopedia navigation NOT lexical authority; Weblio actual Digital Daijisen word "
    "block) and pinned EIGHT-path SVG, not converted. Full metadata [ガイ]/[] in source "
    "order; proposed selected [ガイ]/[], keyがい and necessary NEW弾劾だんがい/no inferred "
    "wordlevel. Impeachment and broader exposing wrongdoing/demanding accountability are "
    "separate senses: not every criticism is impeachment, and the word does not establish "
    "guilt or completed removal. Historical 劾奏/institution-name families retained, not "
    "extra articles. No matching written/primaryreading article; ZERO activated baseline "
    "pairs; ONE proposed allmapped pair/TWO directions. 弾 has no card: keep it in word "
    "metadata/no brokenlink/out-of-batchaddition; inspect raw弾 before allocatingダン. "
    "Finish complete comparison families/actual relevant articles/exact kanji+word labels/"
    "ordinarysecondarysenses/THREE defensibly wrong existing distractors/direct symmetric "
    "NONTRANSITIVE guards/legacyfallbacks/support teaching/natural examples/exact navigation "
    "diff/fullbaseline/allmapped+activated links/proposedHan/fourfonts/canonicalradical/"
    "pinnedconverter plan. 責/批判/批評/責める are inspected candidates, NOT accepted "
    "wrong choices/decided exclusions/permission to rewrite easier decks. Only after "
    "source completion bounded LOCAL UNREVIEWED draft/freeze. Every original TWOserialblind "
    "differentfamilies/serialinternaltools/originalsessionconfirmation/non-skipped qualified "
    "Android/nativeContentSyncONCE/rendered/combinedcurrentmain/normalsigning/ownerfastforward/"
    "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entries42MiBcompressed80MiB"
    "inflated56MiBretained/perfilemediasafepaths/verifiedownerissue gate remains. Verify "
    "whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. "
    "Parent13320 ownsrunner.lock: no childacquire/delete/unlock/readprobe; approvedcontrol/"
    "committedsource/frozeninputs only, no optional historicalsessionrecipes. Preserve/report/"
    "yield actualnewdenial/signinghang/uncertainownership. Published130/1228,1098acceptance "
    "remainder unchanged;1126kanji5077words135N1labels140namedmembers+separate妖;128necessary "
    "supports NOT N1vocabulary. Six separatelyplaced保案派第策結 retainN2/noacceptedcredit/"
    "noduplicate/relevel. CompatibleAndroid#125+#132 required; oldclientsignore; qualified "
    "signedbf30cdead8515739bc0e671d57a54b9a3109dd46 guard+schemaonly NOT latestmain. "
    "Original batch103 finite128optionset/native/rendered acceptance remains bounded as "
    "795; delivered900x2000renditions NOT original1080x2400/equalcomprehension/fallbackface/"
    "retention certification; GPT independent completevisualcoverageUNVERIFIED; no new "
    "73image-loop/newblindcredit or unapproved stronger pixel guarantees. All original "
    "source/review/process/readdepth/image/permission/OOM/pending/source-only limitations "
    "remain preserved, not retroaccepted. Physicalphone/generalrelease/whole-set outstanding; "
    "projectincomplete. No105/unreviewedpush/authoragents/concurrentheavywork/secondrunner/"
    "signingretry/guardincrease."
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
    temporary = path.with_suffix(path.suffix + ".796.tmp")
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
    assert not git("status", "--porcelain", "--untracked-files=all", root=root)


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
    assert (p["checkpoint"], p["batch"], p["status"]) == (795, "103", "continue")
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1098
    assert not list(S.glob(PREFIX + "*"))
    role = load(L / "preflight-796.json")
    assert role["liveParentPid"] == 13320 and role["sessionId"] == L.name
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 795
    assert checkpoint["lastPublishedCommit"] == p["lastPublishedCommit"]
    assert not (L / "progress-before-796.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-796.json")
    state = {
        "execution": 796, "batch": "104", "startingHead": BASE, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded batch104 initial source-preparation checkpoint, frozen row115 only. No runtime draft, reviewer, Android/native, publication,105 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and embedded checkpoint parsed before implementation. Operative contract, approved issue and final795 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main equals content. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution796StartingState"] = state
    p.update(batch="104", stage="batch-104-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "104"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 115
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[114] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "104", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing U+52BE in any keb; preserve all aliases/readings/restrictions/senses.",
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
    (C / "batch-104-full-family-reading.txt").write_bytes(text)
    (S / (PREFIX + "full-family-reading.txt.gz")).write_bytes(gzip.compress(text, mtime=0))
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == CHAR)))
    ET.indent(selected, space="  ")
    (S / (PREFIX + "kanjidic2.xml")).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "104", "baseCommit": BASE, "sourceIndexRecord": row,
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
        "schemaVersion": 1, "batch": "104", "baseCommit": BASE, "membership": [CHAR],
        "sourceRows": [115], "members": [{"kanji": CHAR, "sourceRow": 115}],
        "selectionReason": "Next absent frozen row after published 励. Legal accusation/impeachment versus generic criticism and criminal inquiry need a bounded one-character evidence scope; earlier deferred rows remain pending.",
        "status": "initial-source-packet-only", "drafted": [], "reviewClosed": [], "published": [],
        "sourcePreparationComplete": False, "runtimeChanged": False, "runtimePublished": False,
        "sourceReadingOrder": {k: row["metadata"][k] for k in ("onyomi", "kunyomi")},
        "publishedAdditions": 130, "remainingAdditions": 1098,
        "limits": "Initial member-family packet and navigation only. Complete reading allocation/usefulness, comparison families, quiz/link/font/stroke plan remain required before any runtime draft.",
    }
    save(S / (PREFIX + "membership.json"), progress)
    save(S / (PREFIX + "progress.json"), progress)
    print(json.dumps({"families": len(ids), "compactBytes": len(text),
                      "candidateArticles": [c["article"] for c in candidates]}, ensure_ascii=True))


def archive():
    from html.parser import HTMLParser

    class EvidenceText(HTMLParser):
        def __init__(self, mode):
            super().__init__()
            self.mode = mode
            self.depth = 0
            self.finished = False
            self.parts = []

        def handle_starttag(self, tag, attrs):
            attributes = dict(attrs)
            if self.mode == "kotobank":
                if tag == "article":
                    self.depth += 1
                    self.parts.append("\n[DICTIONARY BLOCK]\n")
            elif tag == "div":
                if self.depth:
                    self.depth += 1
                elif not self.finished and "kijiWrp" in attributes.get("class", "").split():
                    self.depth = 1
            if self.depth and tag in {"p", "h2", "h3", "br", "section", "li"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if self.mode == "kotobank":
                if tag == "article" and self.depth:
                    self.depth -= 1
                    self.parts.append("\n[END BLOCK]\n")
            elif tag == "div" and self.depth:
                self.depth -= 1
                if not self.depth:
                    self.finished = True

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    receipts = []
    for label, url, mode, expected, scope in [
        ("character", "https://kotobank.jp/word/%E5%8A%BE-456688", "kotobank",
         ["がい【劾】", "ガイ", "罪を調べ追及する", "弾劾"],
         "Exact Digital Daijisen character heading/reading/meaning/example inspected. Separate Jitsu readings and image-gaiji historical analysis are not adopted."),
        ("dangai", "https://kotobank.jp/word/%E5%BC%BE%E5%8A%BE-94889", "kotobank",
         ["弾劾", "impeachment"],
         "Redirect inspected as encyclopedia navigation only; not a Digital Daijisen word entry. Country-specific legal/historical claims not adopted."),
        ("dangai-dictionary", "https://www.weblio.jp/content/%E5%BC%BE%E5%8A%BE", "weblio",
         ["だん‐がい【弾劾】", "だんがい", "責任をとる", "政府", "失政", "公務員"],
         "First kijiWrp is the actual Digital Daijisen noun/suru word entry; both lexical senses and wrongdoing example inspected. Later Wikipedia/history blocks are not used."),
    ]:
        source = C / f"batch-104-{label}.html"
        raw = source.read_bytes()
        parser = EvidenceText(mode)
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert all(word in text for word in expected), (label, text[:400])
        target = S / (PREFIX + label + "-public-text.txt")
        target.write_text(text, encoding="utf-8")
        page = S / (PREFIX + label + ".html.gz")
        page.write_bytes(gzip.compress(raw, mtime=0))
        receipts.append({
            "url": url, "downloadedAt": datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).isoformat(),
            "rawBytes": len(raw), "rawSha256": sha(raw), "archive": page.name,
            "archiveSha256": sha(page.read_bytes()), "losslessGzip": gzip.decompress(page.read_bytes()) == raw,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "inspectedBlocks": scope,
            "limits": "Actual raw page archived. Text extraction strips links/formatting and does not decode image gaiji. Receipt establishes bytes, not independent review or adoption of every page claim.",
        })
    save(S / (PREFIX + "public-source-receipts.json"), receipts)
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    svg = (C / "inputs" / "n1-052be-70a0b7ae.svg").read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 8
    assert [p.attrib["id"] for p in paths] == [f"kvg:052be-s{i}" for i in range(1, 9)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    save(S / (PREFIX + "stroke-evidence.json"), {
        "revision": snapshot["kanjivg"]["revision"], "gitBlob": blob,
        "sha256": sha(svg), "bytes": len(svg), "dictionaryStrokeCount": 8,
        "sourceStrokePaths": 8, "converted": False, "nativeDrawingAccepted": False,
        "converterNormalizedSha256": converter,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/052be.svg",
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repository NOTICE.",
        "limits": "Pinned SVG identity, path order and count only; no runtime geometry, font/native acceptance or historical formation claim.",
    })
    p = load(S / (PREFIX + "progress.json"))
    p.update(sourceObservations=PREFIX + "source-observations.json",
             nextAction="SAME104 source completion before any runtime draft: complete comparison families, exact labels/direct nontransitive safeguards, three wrong choices, support/all-mapped links, baseline/font and pinned conversion plan. Preserve all original gates.")
    save(S / (PREFIX + "progress.json"), p)
    print("Three actual source pages and pinned eight-path SVG archived.")


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(child) for child in element))


def audit():
    snapshot, inputs, jm, kd = frozen()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    assert ids == load(S / (PREFIX + "lexical-selection.json"))["entryIds"]
    assert len(ids) == len(set(ids)) == 4
    raw = (S / (PREFIX + "jmdict.xml")).read_bytes()
    assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                          snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    lines = gzip.decompress((S / (PREFIX + "full-family-reading.txt.gz")).read_bytes()).decode("utf-8").splitlines()
    entries = ET.fromstring(raw).findall("entry")
    assert len(lines) == len(entries) == len(ids)
    assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(lines, entries))
    source_record = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert canonical(source_record) == canonical(ET.parse(S / (PREFIX + "kanjidic2.xml")).getroot().find("character"))
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    assert not (R / "words" / "\u5f3e\u52be.md").exists()
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD") == BASE and git("rev-parse", "origin/main") == BASE
    clean(A, APP)
    before = load(L / "progress-before-796.json")
    now = load(C / "progress.json")
    mutable = {"batch", "stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    observations = load(S / (PREFIX + "source-observations.json"))
    assert observations["authorInspection"]["completeMemberFamilies"] == len(ids)
    assert [(r["kind"], r["reading"]) for r in observations["readingObservations"]] == [("on", "\u30ac\u30a4")]
    assert all(set(r["entryIds"]) <= set(ids) for r in observations["readingObservations"])
    navigation = load(S / (PREFIX + "source-navigation.json"))
    assert navigation["candidates"] == [] and navigation["baselinePairs"] == []
    reading_candidates = [path.name for path in (R / "words").glob("*.md")
                          if metadata(R, path.relative_to(R).as_posix())["reading"] == "\u3060\u3093\u304c\u3044"]
    assert reading_candidates == [], reading_candidates
    for name in observations["authorInspection"]["existingArticlesReadCompletely"]:
        assert (R / name).is_file()
    for record in load(S / (PREFIX + "public-source-receipts.json")):
        archived = (S / record["archive"]).read_bytes()
        assert sha(archived) == record["archiveSha256"]
        assert sha(gzip.decompress(archived)) == record["rawSha256"]
        assert sha((S / record["extractedText"]).read_bytes()) == record["extractedTextSha256"]
    svg = (S / (PREFIX + "kanjivg.svg")).read_bytes()
    evidence = load(S / (PREFIX + "stroke-evidence.json"))
    assert sha(svg) == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 8
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
        "schemaVersion": 1, "execution": 796, "batch": "104", "baseCommit": BASE,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": len(ids), "exactFreshExtractionMatches": True,
        "compactFullFamilySemanticEquality": True, "completeRawCharacterRecords": 1,
        "rawCharacterSemanticEquality": True, "sourceRow": 115, "kanji": CHAR,
        "metadataReadingEntries": 1, "runtimeBytesUnchanged": True,
        "runtimeManifestHashesVerified": runtime_count, "candidateArticles": 0,
        "primaryReadingCandidates": 0, "activatedBaselinePairs": 0, "pinnedSvgPaths": 8,
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
        raw = (L / f"{label}-796.txt").read_bytes()
        target = S / f"batch-104-{label}-796.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    tests = (L / "source-tests-796.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-796.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    audit_result = load(S / "batch-104-initial-packet-audit.json")
    assert audit_result["runtimeManifestHashesVerified"] == 8463
    assert audit_result["completeMemberFamilies"] == 4
    helpers = {}
    for name, target in [
        ("source-796.py", "batch-104-source-recipe.py"),
        ("preflight-796.ps1", "batch-104-preflight-796.ps1.txt"),
        ("checks-source-796.ps1", "batch-104-checks-source-796.ps1.txt"),
        ("issue-796.ps1", "batch-104-issue-796.ps1.txt"),
    ]:
        shutil.copyfile(C / name, S / target)
        assert (C / name).read_bytes() == (S / target).read_bytes()
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-796.json")
    assert role["liveParentPid"] == 13320 and role["sessionId"] == L.name and not role["lockTouched"]
    shutil.copyfile(L / "preflight-796.json", S / "batch-104-runner-role-796.json")
    save(S / "execution-796.json", {
        "schemaVersion": 1, "execution": 796, "checkpoint": 796, "batch": "104",
        "stage": "batch-104-initial-source-packet-prepared-not-authoring-ready",
        "baseCommit": BASE, "androidSignedHead": APP, "membership": [CHAR], "sourceRows": [115],
        "sourcePacketAudit": audit_result, "sourceObservations": "batch-104-source-observations.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 130, "remainingAdditions": 1098,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "limits": "Normally signed LOCAL source-only checkpoint; no push, independent content review, app/native acceptance or runtime publication. Original checkpoints and all acceptance gates remain historical/intact. Vocabulary checker retains its reported pilot coverage, not whole-corpus completion.",
    })
    print("Source evidence, validations, runner role and durable helpers archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    clean(R, head)
    body = (
        "Batch 104 / checkpoint 796: **LOCAL source-only checkpoint**, not newly published teaching.\n\n"
        f"Normally signed saved commit: `{head}`; published main remains `{BASE}`.\n\n"
        "Frozen row 115 劾: retained and author-inspected all four complete applicable JMdict "
        "families, its full character record, exact Digital Daijisen character/word entries "
        "and the pinned eight-path SVG (not converted). Five frozen input hashes and both "
        "decompressed dictionary hashes passed. Full metadata [ガイ]/[] is preserved; proposed "
        "practice uses ガイ with necessary 弾劾だんがい support, not an inferred word level. "
        "No existing written/primary-reading article or activated baseline pair was found. "
        "One proposed all-mapped pair/two directions; absent 弾 remains in proposed word "
        "metadata without a broken link or out-of-batch addition.\n\n"
        "The evidence preserves formal impeachment separately from broader denunciation/"
        "demanding accountability. The word does not itself establish guilt or completed "
        "removal. Kotobank's word redirect was an encyclopedia, not the desired word dictionary; "
        "Weblio's actual Daijisen block supplies the two-sense lexical evidence. Historical "
        "劾奏 and institution-name families remain evidence, not extra support articles. "
        "Comparison families, actual labels/three wrong options/direct symmetric nontransitive "
        "safeguards, support teaching, complete link/baseline/Han/font and conversion plans "
        "remain required **before runtime drafting**. No reviewer, Android/native run, "
        "runtime publication or phone evidence is claimed.\n\n"
        "43 focused source tests, structural validation, unchanged regenerated manifest, "
        "vocabulary consistency (existing pilot coverage 2122/2431), publishing budgets and "
        "exact source-packet audits passed. All 8,463 runtime manifest hashes and "
        "contentVersion `38c32a8df5fd6063` remain unchanged. Live parent ancestry/decoded "
        "launcher/exact session/clean signed heads were verified without touching runner.lock. "
        "Reusable helpers are under approved control and archived with the source packet; "
        "no historical session recipe was accessed and no new permission denial occurred.\n\n"
        "**130/1,228 additions published; 1,098 acceptance remainder unchanged.** Compatible "
        "stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 mechanisms "
        "remain required. Six separately placed source members retain N2 and are not newly "
        "counted accepted additions. All historical source/reviewer/process/image/denial/OOM "
        "limits remain intact, including batch103's bounded rendition/finite-sample acceptance, "
        "not expanded or retroaccepted. Physical-phone, general-release and whole-set "
        "acceptance remain outstanding. Next: same104 source completion only; no105, "
        "unreviewed push or second runner.\n"
    )
    (C / "issue-796.txt").write_text(body, encoding="utf-8", newline="\n")
    save(C / "issue-request-796.json", {"body": body})
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    clean(R, head)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == BASE
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert changed and all(name.startswith("docs/n1-sources/batch-104-") or
                           name == "docs/n1-sources/execution-796.json" for name in changed)
    assert not git("diff", BASE, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for name, digest in load(S / "execution-796.json")["durableHelperHashes"].items():
        assert sha((S / name).read_bytes()) == digest, name
    posted = load(L / "issue-796-verified.json")
    body = (C / "issue-796.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    assert head in body and "LOCAL source-only" in body
    before = load(L / "progress-before-796.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    result = {
        "schemaVersion": 1, "execution": 796, "checkpoint": 796, "batch": "104",
        "status": "continue", "stage": "batch-104-initial-source-packet-prepared-not-authoring-ready",
        "savedCommit": head, "signature": "G", "baseCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-104-progress.json",
        "evidence": "docs/n1-sources/execution-796.json",
        "membership": [CHAR], "sourceRows": [115], "completeDictionaryFamilies": 4,
        "completeRawCharacterRecords": 1, "completeExistingArticlesRead": 4,
        "actualSourcePagesArchived": 3, "pinnedSvgPaths": 8, "geometryConverted": False,
        "sourcePreparationComplete": False, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "runtimeHashesUnchanged": 8463,
        "manifestBytesUnchanged": True, "contentVersion": "38c32a8df5fd6063",
        "focusedTestsPassed": 43, "validatorErrors": 0, "dedicatedWorktreesClean": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 130, "remainingAdditions": 1098, "lastPublishedCommit": BASE,
        "issueUpdate": posted["html_url"], "issueAuthorVerified": "stop-cran",
        "actualNewPermissionDenials": [], "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "nextAction": NEXT,
    }
    p["execution796StartingState"]["status"] = "signed-local-initial-source-checkpoint-complete"
    p["execution796CoordinatorCheckpoint"] = result
    p["batch104InitialSourceCheckpoint"] = result
    p.update(checkpoint=796, status="continue", stage=result["stage"], batch="104",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-796-final-verification.json", {
        "checkpoint": result, "originalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "changedOriginalRootFields": sorted(k for k in before if before[k] != reread[k]),
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "ownerIssueAuthorAndBodyVerified": True,
    })
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "packet", "archive", "audit", "record", "issue", "finish"])
    globals()[parser.parse_args().step]()
