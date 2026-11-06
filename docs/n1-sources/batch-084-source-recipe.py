"""Bounded batch 084 source preparation; runtime and publication remain gated."""
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
L = C / "logs" / "c59ed2a1-da38-48ce-b462-e1509f31a3f6"
BASE = "73b19c3eafb75721add6c8e333a1c3bef9e960d7"
MAIN = "106a36dd9617a0d0826a512da82ee1ed9bf9e34d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u51dc"
BEFORE = L / "progress-before-582.json"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest
from extract_n1_jmdict import extract
from freeze_n1_sources import metadata_record


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".582.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


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
    assert git("rev-parse", "origin/main") == MAIN
    subprocess.run(["git", "merge-base", "--is-ancestor", BASE, MAIN], cwd=R, check=True)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 581 and p["batch"] == "083" and p["status"] == "continue"
    assert p["lastPublishedCommit"] == BASE and p["remainingAdditions"] == 1118
    assert not BEFORE.exists() and not list(S.glob("batch-084-*"))
    shutil.copyfile(C / "progress.json", BEFORE)
    request = (L / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 581
    state = {
        "execution": 582, "batch": "084", "startingHead": BASE, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE risk/evidence-bounded084 source-preparation checkpoint only; no runtime, reviewer, Android/native, publication,085 or second runner.",
        "request": {"sha256": sha(request), "bytes": len(request), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint decoded; operative contract, complete approved issue and final581 inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Verified live launcher19008 in coordinator14548 ancestry; parent retains lock; no child acquisition/deletion/unlock.",
        "artifactPathPreflight": {"durableHelper": str(Path(__file__)),
                                  "priorArt": "Approved control/source-batch-083.py and committed extraction/freeze tools.",
                                  "optionalHistoricalSessionHelpersAccessed": False},
        "actualNewPermissionDenials": [],
        "worktrees": "Dedicated signed G clean content/Android. Fresh main advanced normally to106a36dd with separate supplementary N3/N2 coverage; local source base remains published73b19c3e. No overlap with084 source member; actual latest-main integration/reconciliation required before publication. Qualified Android test-only head atop unchanged production f9b59a2; canonical repositories not accessed.",
    }
    p["execution582StartingState"] = state
    p.update(batch="084", stage="batch-084-source-preparation-in-progress", blocker=None,
             nextAction=state["scope"])
    save(C / "progress.json", p)
    print("Full-history starting scope persisted.")


def packet():
    assert load(C / "progress.json")["batch"] == "084"
    snapshot, inputs, jm, kd = frozen()
    named = json.loads(inputs["n1-kanji-source-20261102.json"])
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 93 and named[92] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    selection = {
        "schemaVersion": 1, "batch": "084", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family containing exact source member U+51DC in any keb; all aliases/readings/restrictions/senses retained.",
        "limits": "Extraction is not inspection, reading allocation, frequency evidence or independent review.",
    }
    save(S / "batch-084-lexical-selection.json", selection)
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / "batch-084-jmdict.xml").write_bytes(raw)
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    characters = {e.findtext("literal"): e for e in kd.findall("character")}
    for c in [CHAR, "\u51db"]:
        selected.append(copy.deepcopy(characters[c]))
    ET.indent(selected, space="  ")
    raw_kd = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / "batch-084-kanjidic2.xml").write_bytes(raw_kd)
    save(S / "batch-084-input-metadata.json", {
        "schemaVersion": 1, "batch": "084", "baseCommit": BASE, "sourceIndexRecord": row,
        "characters": [CHAR, "\u51db"], "rawCharacterPacket": "batch-084-kanjidic2.xml",
        "rawCharacterPacketSha256": sha(raw_kd),
        "provenance": "Complete frozen records/header; U+51DB is a comparison spelling only, not an authorized extra source member.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA 4.0; repository NOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if any(c in m.get("kanji", []) or c in m["word"] for c in [CHAR, "\u51db"]):
            candidates.append({"article": name, "metadata": m})
    save(C / "batch-084-source-navigation.json", {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == CHAR],
    })
    print(json.dumps({"families": len(ids), "lines": len(raw.splitlines()),
                      "candidates": candidates}, ensure_ascii=True, indent=2))


def audit():
    from audit_n1_batch import lexical_pair
    from audit_n1_pilot import offered_keys
    from fontTools.ttLib import TTFont

    snapshot, inputs, jm, kd = frozen()
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    named = json.loads(inputs["n1-kanji-source-20261102.json"])
    assert named == load(S / "community-list-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[92] == CHAR
    full_kd = {e.findtext("literal"): e for e in kd.findall("character")}
    assert metadata_record(full_kd[CHAR], {15: "\u51ab"}) == row["metadata"]
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    assert ids == load(S / "batch-084-lexical-selection.json")["entryIds"]
    raw = (S / "batch-084-jmdict.xml").read_bytes()
    assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                          snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    decision = load(S / "batch-084-source-evidence.json")
    described = [i for d in decision["lexicalDecisions"] for i in d["entryIds"]]
    assert len(described) == len(set(described)) and set(described) == set(ids)
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    packet_kd = ET.parse(S / "batch-084-kanjidic2.xml").getroot()
    assert canonical(packet_kd.find("header")) == canonical(kd.find("header"))
    assert all(canonical(e) == canonical(full_kd[e.findtext("literal")])
               for e in packet_kd.findall("character"))
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json") and manifest["contentVersion"] == "6dfe6a1e287ce5df"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    checked = sum(len(v) for v in manifest.values() if isinstance(v, dict))
    assert checked == 8376
    baseline = load(S / "baseline-inventory.json")
    original = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    accepted = set("\u5e79\u6c0f\u6271\u4e43\u51f9\u51f8\u77db\u9df9\u5f57\u6f31\u681e\u8389")
    for path in S.glob("batch-*-progress.json"):
        accepted.update(load(path).get("published", []))
    assert current - original == accepted and len(accepted) == 110 and accepted <= set(named)
    assert len(set(named) - current) == 1118 and metadata(R, "kanji/\u5996.md")["jlpt"] == 1
    membership = load(S / "batch-084-membership.json")
    progress = load(S / "batch-084-progress.json")
    assert membership["membership"] == progress["membership"] == [CHAR]
    assert progress["drafted"] == progress["reviewClosed"] == progress["published"] == []
    assert progress["sourceReadingOrder"] == {k: row["metadata"][k] for k in ["onyomi", "kunyomi"]}
    assert [(x["kind"], x["reading"]) for x in progress["readingDispositions"]] == [
        ("on", "\u30ea\u30f3"), ("kun", "\u304d\u3073\u3057.\u3044")]
    families = {e.findtext("ent_seq"): e for e in ET.fromstring(raw).findall("entry")}
    assert lexical_pair(families["1564320"], CHAR, "\u308a\u3093")
    assert not any(e.findtext("r_ele/reb") == "\u304d\u3073\u3057\u3044" for e in families.values())
    assert all(next(k for k in families["1606360"].findall("k_ele")
                    if k.findtext("keb") == spelling).findtext("ke_inf") == "search-only kanji form"
               for spelling in ["\u51dc\u51bd", "\u51dc\u70c8"])
    projection = progress["proposedCuratedProjection"]
    assert projection["onKeys"] == offered_keys(projection["quizOnyomi"]) == ["\u308a\u3093"]
    assert projection["kunKeys"] == offered_keys(projection["quizKunyomi"]) == []
    assert not (R / "words" / f"{CHAR}.md").exists()
    navigation = load(C / "batch-084-source-navigation.json")
    assert navigation["candidates"] == navigation["baselinePairs"] == []
    mapping = progress["proposedSupportMapping"]
    pairs = {(c, m["article"]) for m in mapping for c in m["allWrittenKanji"]
             if c == CHAR or (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in progress["proposedReciprocalPairs"]} == {(CHAR, "words/\u51dc.md")}
    assert {(p["from"], p["to"]) for p in progress["proposedDirectedLinkPlan"]} == {
        ("kanji/\u51dc.md", "words/\u51dc.md"), ("words/\u51dc.md", "kanji/\u51dc.md")}
    tree = json.loads(inputs["n1-kanjivg-tree-70a0b7ae.json"])
    assert not tree["truncated"] and tree["sha"] == snapshot["kanjivg"]["revision"]
    assert next(t for t in tree["tree"] if t["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    svg_path = C / "inputs" / "n1-051dc-70a0b7ae.svg"
    svg = svg_path.read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 15
    assert [p.attrib["id"] for p in paths] == [f"kvg:051dc-s{i}" for i in range(1, 16)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    stroke = {
        "schemaVersion": 1, "batch": "084", "revision": tree["sha"],
        "input": str(svg_path), "gitBlob": blob, "bytes": len(svg), "sha256": sha(svg),
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/051dc.svg",
        "dictionaryStrokeCount": 15, "sourceStrokePaths": 15, "converted": False,
        "nativeDrawingAccepted": False, "converterNormalizedSha256": converter,
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA 3.0; repository NOTICE.",
        "limits": "Exact pinned SVG verified and read; no converted runtime geometry or native drawing claimed.",
    }
    save(S / "batch-084-stroke-evidence.json", stroke)
    han = sorted({c for c in progress["proposedHanText"] if 0x2E80 <= ord(c) <= 0x2FDF
                  or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-083-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert sha(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {c: ord(c) in cmap for c in han},
                      "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    assert not rare
    save(S / "batch-084-font-preparation.json", {
        "schemaVersion": 1, "batch": "084", "proposedTextInventory": progress["proposedHanText"],
        "auditedHan": han, "auditedHanCount": len(han), "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "mechanism": "Actual unchanged RareHan.kt/RareHanTest.kt read; three actual bundled font cmaps inspected.",
        "limits": "Proposed inventory only. Final runtime inventory, non-skipped RareHan test and native variant/radical rendering pending; cmap absence is not glyph failure or fallback-face identification.",
    })
    public = []
    for item in decision["publicSources"]:
        path = C.parent / item["localBytes"]
        body = path.read_bytes()
        assert body and b"kotobank" in body and CHAR.encode("utf-8") in body
        archive = S / (path.stem + ".html.gz")
        archive.write_bytes(gzip.compress(body, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == body
        public.append({"url": item["url"], "sourcePath": str(path),
                       "archive": archive.name, "sourceSha256": sha(body),
                       "archiveSha256": sha(archive.read_bytes()), "losslessGzip": True,
                       "limits": "Byte receipt; actual author heading/sense inspection and limits in source-evidence.json, not whole-HTML semantic certification."})
    result = {
        "schemaVersion": 1, "execution": 582, "batch": "084", "baseCommit": BASE,
        "stage": progress["status"], "membership": [CHAR], "sourceRow": 93,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "exactFrozenNamedMembershipAndRowVerified": True,
        "completeLexicalFamilies": len(ids), "allExtractedEntryIdsAccountedFor": True,
        "freshExactDictionaryExtractionVerified": True, "lexicalPacketSha256": sha(raw),
        "rawCharacterRecordsVerified": 2,
        "proposedMetadataReadingDispositionsVerified": 2,
        "proposedOnKeys": projection["onKeys"], "proposedKunKeys": projection["kunKeys"],
        "proposedNewSupportArticles": 1, "allMappedReciprocalPairs": len(pairs),
        "requiredDirectedLinks": 2, "activatedBaselinePairs": 0,
        "pinnedSvg": stroke, "proposedHanCount": len(han),
        "fontPreparation": "batch-084-font-preparation.json",
        "publicSourceByteReceipts": public,
        "inspectedArticleHashes": {n: sha((R / n).read_bytes())
                                  for n in decision["authorInspection"]["completeExistingArticlesRead"]},
        "runtimeManifestEqualToPublishedBase": True, "runtimeHashesUnchanged": checked,
        "contentVersion": manifest["contentVersion"], "publishedAdditions": 110,
        "remainingAdditions": 1118, "baselinePreservation": "Runtime unchanged from signed published base; no baseline metadata, readings, exclusions or geometry modified.",
        "authorInspection": decision["authorInspection"],
        "runtimeChanges": 0, "reviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "limits": progress["limits"],
    }
    save(S / "batch-084-preparation-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    checks = {}
    for name in ["source-tests", "validate", "budget", "audit"]:
        path = L / f"{name}-582.txt"
        text = path.read_text(encoding="utf-8-sig")
        if name == "source-tests":
            assert "Ran 43 tests" in text and "OK" in text and "FAILED" not in text
        elif name == "validate":
            assert "0 error(s)" in text
        elif name == "audit":
            assert '"runtimeHashesUnchanged": 8376' in text
        else:
            assert "ERROR" not in text
        raw = path.read_bytes()
        archive = S / f"batch-084-{name}-582.txt.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        checks[name] = {"path": str(path), "sha256": sha(raw),
                        "archive": archive.name, "archiveSha256": sha(archive.read_bytes()),
                        "losslessGzip": True,
                        "provenance": "Manually transcribed exact terminal tool10 unittest summary, not raw redirected stdout."
                        if name == "source-tests" else "Direct redirected subprocess output."}
    svg = (C / "inputs" / "n1-051dc-70a0b7ae.svg").read_bytes()
    (S / "batch-084-kanjivg.svg").write_bytes(svg)
    recipe = S / "batch-084-source-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-582.json", {
        "schemaVersion": 1, "execution": 582, "batch": "084", "baseCommit": BASE,
        "startingState": load(C / "progress.json")["execution582StartingState"],
        "sourceAudit": "batch-084-preparation-audit.json",
        "sourcePacket": "batch-084-progress.json", "sourceEvidence": "batch-084-source-evidence.json",
        "recipe": {"durableControlPath": str(Path(__file__)), "archive": recipe.name,
                   "sha256": sha(recipe.read_bytes())},
        "checks": checks, "runtimeChanged": False, "runtimePublished": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False,
        "nextAction": load(S / "batch-084-progress.json")["nextAction"],
        "limits": load(S / "batch-084-progress.json")["limits"],
    })
    print("Source evidence and reusable recipe archived; local signing next, no push.")


def seal():
    head = git("rev-parse", "HEAD")
    clean(R, head)
    clean(A, APP)
    assert head != BASE and git("rev-parse", "origin/main") == MAIN
    assert not git("diff", BASE, "HEAD", "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    before = load(BEFORE)
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert p["checkpoint"] == 581 and p["batch"] == "084"
    assert all(p.get(k) == v for k, v in before.items() if k not in allowed)
    state = {
        "schemaVersion": 1, "execution": 582, "checkpoint": 582, "batch": "084",
        "status": "continue", "stage": "source-prepared-not-drafted", "savedCommit": head,
        "signature": "G", "lastPublishedCommit": BASE,
        "sourcePacket": "docs/n1-sources/batch-084-progress.json",
        "sourceAudit": "docs/n1-sources/batch-084-preparation-audit.json",
        "evidence": "docs/n1-sources/execution-582.json",
        "membership": [CHAR], "sourceRow": 93, "dedicatedWorktreesClean": True,
        "runtimeChanged": False, "runtimePublished": False, "runtimeDrafted": [],
        "reviewClosed": [], "published": [], "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 110,
        "remainingAdditions": 1118, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "runtimeHashesUnchanged": 8376,
        "originalHistoricalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True,
        "nextAction": load(S / "batch-084-progress.json")["nextAction"],
    }
    p["execution582CoordinatorCheckpoint"] = state
    p["batch084SourcePreparation"] = state
    p.update(checkpoint=582, status="continue", stage="batch-084-source-prepared-not-drafted",
             blocker=None, nextAction=state["nextAction"])
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert all(reread.get(k) == v for k, v in before.items() if k not in allowed)
    save(L / "execution-582-final-checkpoint.json", state)
    print(json.dumps(state, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["start", "packet", "audit", "record", "seal"])
    args = parser.parse_args()
    globals()[args.operation]()
