import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-sources"
START = "5935b5db1e3d852523ec0d1d07d1ec7441acfa94"
BASE = "54fd8ff471eec7c98a83860ae94b92a673cf05bd"
LOG = CONTROL / "logs" / "c215a68d-7377-4f98-80ec-4018ffa0e506"
NEXT = (
    "SAME063 obtain two serial blind different-model-family initial reviews on the normally signed draft "
    "containing execution-390.json: complete kanji/倣.md, words/模倣.md and exact one-line words/倣う.md "
    "diff plus applicable unchanged context; all35 complete families and source/reading/quiz/link/font/geometry "
    "evidence. Verify actual CLI catalog/model identity and process exit, at most one reviewer and serial tools; "
    "do not edit frozen teaching. Reconcile evidence then fresh Android3+1/native/visual/currentmain/signing/"
    "ownerfastforward/greenCI/every immutable public ZIP hash gates. Native must inspect reused 傚 as well as "
    "倣/模 and 人/亻; prior radical evidence is inherited. No unreviewed push,064 or second runner."
)
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_batch import audit as batch_audit, base_file
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256
from check_content_budget import archive_names, check
from extract_n1_jmdict import extract
from fontTools.ttLib import TTFont
from generate_strokes import convert

spec = importlib.util.spec_from_file_location("source389", CONTROL / "execution-389.py")
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)
load, save, digest, git = source.load, source.save, source.digest, source.git


def prepare():
    snapshot = source.inputs()
    svg = (CONTROL / "inputs" / "n1-05023-70a0b7ae.svg").read_bytes()
    row = load(FOLDER / "batch-063-input-metadata.json")["sourceIndexRecord"]
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert len(svg) == row["kanjivgInventory"]["size"] == 4324
    assert blob == row["kanjivgInventory"]["sha"]
    converter_hash = digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter_hash == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    data = convert("倣", svg.decode("utf-8"))
    assert data["strokeCount"] == row["metadata"]["strokes"] == 10
    target = ROOT / "strokes" / "倣.json"
    assert not target.exists()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    save(FOLDER / "batch-063-stroke-evidence.json", {
        "schemaVersion": 1, "batch": "063", "character": "倣",
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/05023.svg",
        "sourceRevision": data["sourceRevision"], "sourceBytes": len(svg), "gitBlob": blob,
        "sourceSha256": digest(svg), "sourceLocalPath": "control/inputs/n1-05023-70a0b7ae.svg",
        "converter": "tools/generate_strokes.py:convert; unchanged pinned converter",
        "converterNormalizedSha256": converter_hash, "target": "strokes/倣.json",
        "targetSha256": digest(target.read_bytes()), "strokeCount": 10, "pointsPerStroke": 16,
        "dictionaryAndSvgCountAgreement": True, "license": "KanjiVG CC BY-SA3.0; generated attribution retained.",
        "limits": "Pinned conversion, not native drawing recognition, historical derivation or phone evidence.",
    })
    ids = ["1378240", "1589970"]
    selection = FOLDER / "batch-063-written-copy-selection.json"
    packet = FOLDER / "batch-063-written-copy-jmdict.xml"
    assert not selection.exists() and not packet.exists()
    dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    packet.write_bytes(extract(dictionary, digest(dictionary), ids))
    save(selection, {
        "schemaVersion": 1, "batch": "063", "entryIds": ids,
        "selectionSpellings": ["清書", "書き取り"],
        "provenance": "Complete additional frozen families for actual fair-copy/written-copying quiz labels; original33 families preserved.",
        "limits": "Conservative uncontextualized English copying-label comparison, not unrestricted Japanese synonymy.",
    })
    print("Pinned ten-stroke geometry generated; two complete written-copy families extracted.")


def audit():
    snapshot = source.inputs()
    ledger = load(FOLDER / "batch-063-progress.json")
    result = batch_audit(ROOT, "063")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    assert git("rev-parse", "origin/main") == ledger["baseCommit"] == BASE
    row = load(FOLDER / "batch-063-input-metadata.json")["sourceIndexRecord"]
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[58] == "倣"
    assert row == next(r for r in load(FOLDER / "source-index.json") if r["kanji"] == "倣")
    inventory = load(CONTROL / "inputs" / "n1-kanjivg-tree-70a0b7ae.json")
    assert next(r for r in inventory["tree"] if r["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    assert (FOLDER / "batch-063-kanjidic2.xml").read_bytes() == source.raw_metadata()
    dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    groups = source.groups(dictionary)
    packets, families = [], set()
    for packet in ledger["dictionaryPackets"]:
        ids = load(FOLDER / packet["selection"])["entryIds"]
        raw = (FOLDER / packet["xml"]).read_bytes()
        assert raw == extract(dictionary, digest(dictionary), ids)
        assert [e.findtext("ent_seq") for e in ET.fromstring(raw).findall("entry")] == ids
        assert not families & set(ids)
        families.update(ids)
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": digest(raw)})
    for kind, ids in groups.items():
        assert load(FOLDER / f"batch-063-{kind}-selection.json")["entryIds"] == ids
        decisions = [i for d in ledger[f"{kind.replace('-', '')}Dispositions"] for i in d["entries"]]
        assert len(decisions) == len(set(decisions)) and set(decisions) == set(ids)
    assert len(families) == 35
    immutable = [
        "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
        "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json",
    ]
    for name in immutable:
        assert (ROOT / name).read_text(encoding="utf-8") == base_file(ROOT, BASE, name)
    for name in ["membership", "input-metadata", "source-evidence", "preparation-audit",
                 "lexical-selection", "comparison-selection", "quiz-comparison-selection"]:
        path = FOLDER / f"batch-063-{name}.json"
        assert path.read_bytes() == subprocess.check_output(
            ["git", "--no-pager", "show", f"{START}:{path.relative_to(ROOT).as_posix()}"], cwd=ROOT), name
    exceptions = {
        "words/虎.md": {"quiz_exclusions": ["酔っ払い"]},
        "words/猿.md": {"quiz_exclusions": ["馬鹿"]},
        "words/丘.md": {"quiz_exclusions": ["坂", "山"]},
        "kanji/山.md": {"distractors": ["川", "出", "木"]},
    }
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, old in load(FOLDER / "baseline-inventory.json")["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(old["metadata"])
            expected.update(exceptions.get(name, {}))
            assert metadata(ROOT, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert digest((ROOT / name).read_bytes()) == old["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    manifest = load(ROOT / "manifest.json")
    assert manifest == build_manifest(ROOT)
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = digest((ROOT / name).read_bytes()) if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(ROOT / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8317
    card, word = metadata(ROOT, "kanji/倣.md"), metadata(ROOT, "words/模倣.md")
    assert "phonetic" not in card and card["tags"] == ["jlpt-n1", "grade-8", "structure-unclassified"]
    assert "jlpt" not in word and word["kanji"] == ["模", "倣"]
    assert not (ROOT / "kanji" / "模.md").exists()
    declared = [{"article": p.relative_to(ROOT).as_posix(), "word": v["word"], "primaryReading": v["reading"]}
                for p in sorted((ROOT / "words").glob("*.md"))
                if "倣" in (v := metadata(ROOT, p.relative_to(ROOT).as_posix())).get("kanji", [])]
    assert declared == ledger["currentDeclaredWordPairs"]
    assert {(r["kanji"], r["article"]) for r in ledger["supportMappings"]} == {("倣", r["article"]) for r in declared}
    assert sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["title"] == card["title"] for p in (ROOT / "kanji").glob("*.md")) == 1
    geometry = load(FOLDER / "batch-063-stroke-evidence.json")
    svg = (CONTROL / "inputs" / "n1-05023-70a0b7ae.svg").read_bytes()
    assert digest(svg) == geometry["sourceSha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"] == row["kanjivgInventory"]["sha"]
    data = load(ROOT / "strokes" / "倣.json")
    assert data == convert("倣", svg.decode("utf-8"))
    assert digest((ROOT / "strokes" / "倣.json").read_bytes()) == geometry["targetSha256"]
    for i, stroke in enumerate(data["strokes"], 1):
        assert stroke["id"] == i and len(stroke["points"]) == 16
        assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
    articles = ["kanji/倣.md", "words/模倣.md", "words/倣う.md"]
    han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "\n".join((ROOT / name).read_text(encoding="utf-8") for name in articles))))
    android = CONTROL.parent / "kanji-cards-android"
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=android, text=True).strip() == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android).strip()
    fonts = []
    for record in load(FOLDER / "font-coverage.json")["fonts"]:
        path = android / record["path"]
        assert digest(path.read_bytes()) == record["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        fonts.append({"path": record["path"], "sha256": record["sha256"], "missing": missing})
    legacy = [{key: value[key] for key in ("kanji", "title", "distractors")}
              for p in sorted((ROOT / "kanji").glob("*.md"))
              if len((value := metadata(ROOT, p.relative_to(ROOT).as_posix())).get("distractors", [])) < 3]
    actual_counts = {
        "kanji": len(list((ROOT / "kanji").glob("*.md"))),
        "words": len(list((ROOT / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["jlpt"] == 1 for p in (ROOT / "kanji").glob("*.md")),
        "namedSourceMembersPresent": sum((ROOT / "kanji" / f"{c}.md").exists() for c in named),
    }
    assert actual_counts == {"kanji": 1075, "words": 5033, "n1Labelled": 95, "namedSourceMembersPresent": 94}
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    result.update({
        "schemaVersion": 1, "execution": 390, "status": "local-unreviewed-draft",
        "sourceCheckpoint": START, "sourceRow": 59,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "freshExactDictionaryFamilies": len(families), "packets": packets,
        "baselineMetadataAndStrokesChecked": counts, "explicitInheritedMetadataExceptions": exceptions,
        "newBaselineMetadataExceptions": [], "immutableEvidenceUnchanged": immutable,
        "runtimeAdditions": ["kanji/倣.md", "strokes/倣.json", "words/模倣.md"],
        "changedReusedRuntimePayloads": ["words/倣う.md"],
        "runtimePayloadHashesVerified": checked, "baseRuntimeHashesUnchanged": checked - 4,
        "actualDraftCounts": actual_counts, "directedLinks": 4,
        "newWordJlptInferred": False, "newDirectWordExclusions": len(word["quiz_exclusions"]),
        "legacyFallbackCandidatesWithFewerThanThree": legacy,
        "legacyFallbackDisposition": "All eleven displayed labels inspected; none names imitation/emulation. Existing 写/似/則 meaning neighbors already have three choices. Larger/random/live pools unverified.",
        "geometry": geometry,
        "actualAuthoredHanFonts": {"articles": articles, "characters": han, "count": len(han), "fonts": fonts,
                                  "missingUnion": sorted({c for f in fonts for c in f["missing"]}),
                                  "limits": "Complete article-Han cmap audit, not native rendering/fallback/drawing or phone evidence."},
        "budget": check(ROOT, archive_names(ROOT)),
        "publishedAdditions": 89, "remainingAdditions": 1139,
        "limits": "Local unreviewed draft only; no reviewer, fresh Android/native check or publication. Draft does not reduce published remaining additions.",
    })
    save(FOLDER / "batch-063-draft-audit.json", result)
    print(json.dumps({key: result[key] for key in ("actualDraftCounts", "contentVersion", "runtimePayloadHashesVerified", "actualAuthoredHanFonts", "budget", "legacyFallbackCandidatesWithFewerThanThree")}, ensure_ascii=False, indent=2))


def record():
    assert git("rev-parse", "HEAD") == START
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 389 and progress["batch"] == "063"
    original = load(LOG / "checkpoint-full.json")
    assert original["checkpoint"] == 389 and original["lastPublishedCommit"] == BASE
    request = (LOG / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == 389 and embedded["batch"] == "063"
    test_raw = (CONTROL / "logs" / "execution-390-python-tests.txt").read_bytes()
    test_text = test_raw.decode("utf-8-sig")
    assert "Ran 368 tests" in test_text and test_text.rstrip().endswith("OK")
    target = FOLDER / "execution-390-python-tests.txt"
    assert not target.exists()
    target.write_bytes(test_raw)
    audit_record = load(FOLDER / "batch-063-draft-audit.json")
    ledger = load(FOLDER / "batch-063-progress.json")
    result = {
        "schemaVersion": 1, **progress["execution390StartingState"],
        "checkpoint": 390, "recordedAt": source.now(),
        "status": "validated-unreviewed-draft-awaiting-normally-signed-snapshot",
        "authorization": {
            "requestSha256": digest(request), "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Complete request acquired and checkpoint parsed; operative contract, complete final389 checkpoint and approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
        },
        "membership": ["倣"], "sourceRow": 59, "publishedBase": BASE, "sourceCheckpoint": START,
        "runtimeScope": {
            "newKanji": ["kanji/倣.md"], "newNecessaryWords": ["words/模倣.md"],
            "generatedGeometry": ["strokes/倣.json"], "changedReusedPassages": ledger["changedReusedPassages"],
            "existingMetadataChanges": [], "fullOn": ["ホウ"], "fullKun": ["なら.う"],
            "proposedOnKeys": ["ほう"], "proposedKunKeys": ["ならう"],
            "requiredReciprocalPairs": 2, "directedLinks": 4, "activatedBaselinePairs": 1,
            "newDirectWordExclusions": 8,
        },
        "sourcePacketHashes": {p.relative_to(ROOT).as_posix(): digest(p.read_bytes())
                               for p in sorted(FOLDER.glob("batch-063-*")) if p.is_file()},
        "coordinatorInspection": ledger["draftInspection"],
        "checks": {
            "validatorErrors": 0, "manifestFresh": True,
            "contentVersion": audit_record["contentVersion"], "runtimeHashesVerified": 8317,
            "baselinePreserved": audit_record["baselineMetadataAndStrokesChecked"],
            "newBaselineMetadataExceptions": [], "exactFrozenDictionaryFamilies": 35,
            "frozenInputHashes": 5, "decompressedDictionaryHashes": 2,
            "pythonTests": 368, "pythonFailures": 0, "pythonErrors": 0,
            "pythonLog": target.relative_to(ROOT).as_posix(), "pythonLogSha256": digest(test_raw),
            "testOutputQualification": "Existing synthetic generated-media/retry fixture output is not new authorized media generation.",
            "grammarVocabularyConsistency": "Actual tools/grammar_vocabulary.py check passed; existing2122/2431 pilot coverage retained, not repaired or counted as new work.",
            "localBudget": audit_record["budget"],
            "authoredHan": 34, "bundledMissingUnion": ["亻", "傚"],
            "fontQualification": ledger["fontDisposition"],
            "dedicatedAndroidHead": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c",
            "dedicatedAndroidClean": True,
        },
        "draftAudit": "batch-063-draft-audit.json",
        "draftAuditSha256": digest((FOLDER / "batch-063-draft-audit.json").read_bytes()),
        "helper": str(Path(__file__).resolve()), "helperSha256": digest(Path(__file__).read_bytes()),
        "operationalObservations": [
            "A broad control-root helper listing exceeded returned-output limits; not counted as complete inspection. Subsequent helper selection used exact filenames.",
            "An absent 侍 card lookup yielded no evidence and was not used. No permission failure or signing workaround.",
        ],
        "independentReview": "Not started. This is a common local snapshot for future serial blind two-family reviews, not review-closed teaching.",
        "freshAndroidNativePhone": "Not performed. Prior062 evidence is historical and not substitute063 acceptance; physical-phone/general-release and whole-set outstanding.",
        "publishedAdditions": 89, "remainingAdditions": 1139, "localDraftAdditions": 90,
        "pushed": False, "nextAction": NEXT, "limits": audit_record["limits"],
    }
    save(FOLDER / "execution-390.json", result)
    print("Durable bounded draft evidence recorded; ready for normally signed local snapshot.")


def finish():
    original = load(LOG / "checkpoint-full.json")
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == original["checkpoint"] == 389
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker", "activeExecution"}
    for key, value in original.items():
        if key not in mutable:
            assert progress[key] == value, key
    assert not git("status", "--porcelain")
    saved = git("rev-parse", "HEAD")
    assert saved != START and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == progress["lastPublishedCommit"] == BASE
    assert git("show", "-s", "--format=%P", saved) == START
    expected = {
        "docs/n1-authoring-notes.md", "docs/n1-sources/batch-063-progress.json",
        "docs/n1-sources/batch-063-draft-audit.json", "docs/n1-sources/batch-063-stroke-evidence.json",
        "docs/n1-sources/batch-063-written-copy-selection.json", "docs/n1-sources/batch-063-written-copy-jmdict.xml",
        "docs/n1-sources/execution-390.json", "docs/n1-sources/execution-390-python-tests.txt",
        "kanji/倣.md", "words/模倣.md", "words/倣う.md", "strokes/倣.json", "manifest.json",
    }
    changed = set(subprocess.check_output(
        ["git", "-c", "core.quotepath=false", "diff", "--name-only", START, saved],
        cwd=ROOT, text=True, encoding="utf-8").splitlines())
    assert changed == expected, changed
    record = load(FOLDER / "execution-390.json")
    assert digest(Path(__file__).read_bytes()) == record["helperSha256"]
    for name, value in record["sourcePacketHashes"].items():
        assert digest((ROOT / name).read_bytes()) == value, name
    record.update({
        "status": "signed-local-unreviewed-draft-checkpoint-complete",
        "savedCommit": saved, "signature": "G", "dedicatedContentClean": True, "localOnly": True,
        "lastPublishedCommit": BASE, "allOriginalHistoricalKeysPreservedExactly": True,
        "originalTopLevelKeys": len(original), "recordedAt": source.now(),
    })
    save(CONTROL / "execution-390-verification.json", record)
    progress.update({
        "checkpoint": 390, "status": "continue", "stage": "batch-063-draft-awaiting-independent-review",
        "batch": "063", "blocker": None, "nextAction": NEXT,
        "batch063DraftCheckpoint": record, "execution390CoordinatorCheckpoint": record,
    })
    progress["execution390StartingState"]["status"] = record["status"]
    progress["activeExecution"] = progress["execution390StartingState"]
    save(CONTROL / "progress.json", progress)
    reread = load(CONTROL / "progress.json")
    for key, value in original.items():
        if key not in mutable:
            assert reread[key] == value, key
    assert reread["checkpoint"] == 390 and reread["status"] == "continue"
    print(json.dumps({"checkpoint": 390, "savedCommit": saved, "signature": "G",
                      "status": "continue", "stage": reread["stage"], "originalTopLevelKeysPreserved": len(original) - len(mutable)}, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "audit": audit, "record": record, "finish": finish}[sys.argv[1]]()
