import hashlib
import importlib.util
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
FOLDER = ROOT / "docs" / "n1-sources"
START = "0f959cfaebac16f6103a292a2f9c9a507fdd2689"
BASE = "42f144c76f013bedc392b201c5be7eed35083b88"
sys.path.insert(0, str(ROOT / "tools"))
from audit_n1_batch import base_file, lexical_pair, reused_changes, runtime_delta
from audit_n1_pilot import metadata, offered_keys
from build_manifest import build_manifest, sha256
from check_content_budget import archive_names, check
from extract_n1_jmdict import extract
from fontTools.ttLib import TTFont
from generate_strokes import convert

spec = importlib.util.spec_from_file_location("source379", CONTROL / "execution-379.py")
source = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source)
EXCLUSIONS = ["給料", "給与", "月給", "収入", "支給", "支払", "払う", "支払う", "代金"]
NEXT = (
    "SAME062 obtain two serial blind different-model-family initial reviews on signed draft snapshot "
    "containing execution-380.json: kanji/俸.md, words/俸給.md, exact one-line kanji/給.md diff, "
    "all42 complete families and source/reading/quiz/link/font/geometry dispositions. Verify current "
    "CLI catalog and actual models/process exit; one active reviewer, serial internal tools and no "
    "frozen-snapshot edits. Reconcile evidence then applicable fresh Android3+1/native/visual/currentmain/"
    "signing/ownerfastforward/greenCI/every immutable public ZIP hash gates. No unreviewed push,063 or second runner."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args):
    return subprocess.check_output(
        ["git", "--no-pager", *args], cwd=ROOT, text=True, encoding="utf-8"
    ).strip()


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 379 and progress["batch"] == "062"
    assert git("rev-parse", "HEAD") == START
    assert git("rev-parse", "origin/main") == BASE
    assert not git("status", "--porcelain")
    request = CONTROL / "logs" / "d3b5a1bb-9600-4a09-b2cf-a2ed0bd54466" / "request.txt"
    text = request.read_text(encoding="utf-8-sig")
    json.loads(text.split("Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    progress["execution380StartingState"] = {
        "execution": 380, "batch": "062", "startingHead": START,
        "recordedAt": datetime.now().astimezone().isoformat(),
        "scope": "SAME062 bounded substantive draft and normally signed local unreviewed checkpoint only. No reviewer, Android/native, publication,063 or second runner.",
        "status": "authoring-bounded-draft",
        "authorization": {
            "requestSha256": hashlib.sha256(request.read_bytes()).hexdigest(),
            "characters": len(text), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request acquired into memory and complete embedded checkpoint parsed; operative contract, complete final379 checkpoint and approved issue inspected directly. Historical middle acquired and parsed, not freshly semantically re-reviewed.",
        },
        "worktrees": "Dedicated content and Android clean; normal fresh fetch origin/main42f144c7 remains parent of local source checkpoint0f959cfa. No canonical checkout accessed.",
    }
    progress["stage"] = "batch-062-authoring-bounded-draft"
    save(CONTROL / "progress.json", progress)
    print("Starting scope persisted; complete live history preserved.")


def prepare():
    snapshot = source.inputs()
    ids = ["1310130", "1310300", "1501620", "1594480"]
    selection = FOLDER / "batch-062-quiz-comparison-selection.json"
    packet = FOLDER / "batch-062-quiz-comparison-jmdict.xml"
    assert not selection.exists() and not packet.exists()
    dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    raw = extract(dictionary, hashlib.sha256(dictionary).hexdigest(), ids)
    packet.write_bytes(raw)
    save(selection, {
        "schemaVersion": 1, "batch": "062", "entryIds": ids,
        "selectionSpellings": ["支給", "支払う", "払う", "支払"],
        "provenance": "Complete additional frozen JMdict families for actual displayed pay/payment/provision neighbors; original source packets preserved unchanged.",
        "limits": "Conservative direct quiz-label safeguards, not unrestricted Japanese synonymy or a change to the original source freeze.",
    })
    svg = (CONTROL / "inputs" / "n1-04ff8-70a0b7ae.svg").read_bytes()
    row = load(FOLDER / "batch-062-input-metadata.json")["sourceIndexRecord"]
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert len(svg) == row["kanjivgInventory"]["size"] == 4533
    assert blob == row["kanjivgInventory"]["sha"]
    converter_hash = hashlib.sha256((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    assert converter_hash == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    data = convert("俸", svg.decode("utf-8"))
    assert data["strokeCount"] == row["metadata"]["strokes"] == 10
    target = ROOT / "strokes" / "俸.json"
    assert not target.exists()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    save(FOLDER / "batch-062-stroke-evidence.json", {
        "schemaVersion": 1, "batch": "062", "character": "俸",
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/04ff8.svg",
        "sourceRevision": data["sourceRevision"], "sourceBytes": len(svg), "gitBlob": blob,
        "sourceSha256": hashlib.sha256(svg).hexdigest(),
        "sourceLocalPath": "control/inputs/n1-04ff8-70a0b7ae.svg",
        "converter": "tools/generate_strokes.py:convert; unchanged pinned converter",
        "converterNormalizedSha256": converter_hash,
        "target": "strokes/俸.json", "targetSha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "strokeCount": 10, "pointsPerStroke": 16, "dictionaryAndSvgCountAgreement": True,
        "license": "KanjiVG CC BY-SA 3.0; generated file retains attribution.",
        "limits": "Pinned SVG conversion only, not native drawing recognition, readable glyphs or phone evidence. No historical/phonetic analysis inferred from SVG annotations.",
    })
    print("Generated pinned ten-stroke geometry and four complete quiz-comparison families:", len(raw.splitlines()), "lines.")


def audit():
    snapshot = source.inputs()
    ledger = load(FOLDER / "batch-062-progress.json")
    frozen = load(FOLDER / "batch-062-membership.json")
    row = load(FOLDER / "batch-062-input-metadata.json")["sourceIndexRecord"]
    assert ledger["baseCommit"] == frozen["baseCommit"] == BASE
    assert ledger["membership"] == frozen["membership"] == ledger["drafted"] == ["俸"]
    assert ledger["reviewClosed"] == ledger["published"] == []
    assert ledger["status"] == "local-unreviewed-draft"
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert len(named) == len(set(named)) == 1232 and named[55] == "俸"
    assert row == next(r for r in load(FOLDER / "source-index.json") if r["kanji"] == "俸")
    inventory = load(CONTROL / "inputs" / "n1-kanjivg-tree-70a0b7ae.json")
    assert next(r for r in inventory["tree"] if r["path"] == row["kanjivgInventory"]["path"]) == row["kanjivgInventory"]
    assert (FOLDER / "batch-062-kanjidic2.xml").read_bytes() == source.raw_metadata()
    families, packets = {}, []
    dictionary = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    for packet in ledger["dictionaryPackets"]:
        ids = load(FOLDER / packet["selection"])["entryIds"]
        raw = (FOLDER / packet["xml"]).read_bytes()
        assert raw == extract(dictionary, hashlib.sha256(dictionary).hexdigest(), ids)
        entries = ET.fromstring(raw).findall("entry")
        assert [e.findtext("ent_seq") for e in entries] == ids
        assert not families.keys() & set(ids)
        families.update(zip(ids, entries))
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": hashlib.sha256(raw).hexdigest()})
    for kind, ids in source.groups(dictionary).items():
        assert load(FOLDER / f"batch-062-{kind}-selection.json")["entryIds"] == ids
        dispositions = [i for d in ledger[f"{kind}Dispositions"] for i in d["entries"]]
        assert len(dispositions) == len(set(dispositions)) and set(dispositions) == set(ids)
    assert len(families) == 42
    manifest = load(ROOT / "manifest.json")
    assert manifest == build_manifest(ROOT)
    additions = {"kanji/俸.md", "words/俸給.md", "strokes/俸.json"}
    runtime_delta(json.loads(base_file(ROOT, BASE, "manifest.json")), manifest, additions, {"kanji/給.md"})
    reused_changes(base_file(ROOT, BASE, "kanji/給.md"), (ROOT / "kanji" / "給.md").read_text(encoding="utf-8"), ledger["changedReusedPassages"])
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    exceptions = {"words/虎.md": {"quiz_exclusions": ["酔っ払い"]},
                  "words/猿.md": {"quiz_exclusions": ["馬鹿"]},
                  "words/丘.md": {"quiz_exclusions": ["坂", "山"]},
                  "kanji/山.md": {"distractors": ["川", "出", "木"]}}
    for name, item in load(FOLDER / "baseline-inventory.json")["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(item["metadata"])
            expected.update(exceptions.get(name, {}))
            assert metadata(ROOT, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == item["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    immutable = ["docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
                 "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json"]
    for name in immutable:
        assert (ROOT / name).read_text(encoding="utf-8") == base_file(ROOT, BASE, name)
    for path in FOLDER.glob("batch-062-*"):
        if path.name in {"batch-062-membership.json", "batch-062-source-evidence.json", "batch-062-input-metadata.json",
                         "batch-062-jmdict.xml", "batch-062-comparison-jmdict.xml", "batch-062-kanjidic2.xml",
                         "batch-062-lexical-selection.json", "batch-062-comparison-selection.json", "batch-062-preparation-audit.json"}:
            assert path.read_bytes() == subprocess.check_output(
                ["git", "--no-pager", "show", f"{START}:{path.relative_to(ROOT).as_posix()}"], cwd=ROOT
            ), path
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = hashlib.sha256((ROOT / name).read_bytes()).hexdigest() if section in {"images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(ROOT / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8314
    m = metadata(ROOT, "kanji/俸.md")
    for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        assert m[field] == row["metadata"][field]
    assert m["jlpt"] == 1 and m["tags"] == ["jlpt-n1", "grade-8", "structure-unclassified"] and "phonetic" not in m
    assert m["quizOnyomi"] == ["ホウ"] and m["quizKunyomi"] == []
    assert offered_keys(m["quizOnyomi"]) == ledger["curatedProjection"][0]["onKeys"] == ["ほう"]
    assert len(ledger["readingDispositions"]) == 1 and ledger["readingDispositions"][0]["selected"]
    table = (ROOT / "kanji" / "俸.md").read_text(encoding="utf-8").split("## Readings\n", 1)[1].split("## Common words", 1)[0]
    assert len([line for line in table.splitlines() if line.startswith("| ホウ |") and "(../words/俸給.md)" in line]) == 1
    w = metadata(ROOT, "words/俸給.md")
    assert w["word"] == "俸給" and w["reading"] == "ほうきゅう" and w["kanji"] == ["俸", "給"] and "jlpt" not in w
    assert w["quiz_exclusions"] == EXCLUSIONS
    assert lexical_pair(families["1515280"], w["word"], w["reading"])
    pairs = {(r["kanji"], r["article"]) for r in ledger["supportMappings"]}
    assert pairs == set(map(tuple, ledger["requiredReciprocalPairs"])) == {("俸", "words/俸給.md"), ("給", "words/俸給.md")}
    assert pairs == {(c, "words/俸給.md") for c in w["kanji"] if (ROOT / "kanji" / f"{c}.md").exists()}
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (ROOT / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (ROOT / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    declared = [{"article": p.relative_to(ROOT).as_posix(), "word": v["word"], "primaryReading": v["reading"]}
                for p in sorted((ROOT / "words").glob("*.md"))
                if "俸" in (v := metadata(ROOT, p.relative_to(ROOT).as_posix())).get("kanji", [])]
    assert declared == ledger["currentDeclaredWordPairs"] == [{"article": "words/俸給.md", "word": "俸給", "primaryReading": "ほうきゅう"}]
    assert not [r for r in load(FOLDER / "baseline-word-candidates.json") if r["kanji"] == "俸"]
    assert m["distractors"] == ["棒", "借", "付"] == ledger["quizAudit"]["俸"]["distractors"]
    assert [metadata(ROOT, f"kanji/{c}.md")["title"] for c in m["distractors"]] == ledger["quizAudit"]["俸"]["labels"]
    assert sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["title"] == m["title"] for p in (ROOT / "kanji").glob("*.md")) == 1
    assert ledger["wordQuizAudit"]["directExclusions"] == [{"word": "俸給", "exclude": EXCLUSIONS}]
    for word in EXCLUSIONS:
        assert (ROOT / "words" / f"{word}.md").exists()
    svg = (CONTROL / "inputs" / "n1-04ff8-70a0b7ae.svg").read_bytes()
    geometry = load(FOLDER / "batch-062-stroke-evidence.json")
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"] == geometry["gitBlob"]
    assert hashlib.sha256(svg).hexdigest() == geometry["sourceSha256"]
    data = load(ROOT / "strokes" / "俸.json")
    assert data == convert("俸", svg.decode("utf-8"))
    assert data["strokeCount"] == len(data["strokes"]) == 10
    assert hashlib.sha256((ROOT / "strokes" / "俸.json").read_bytes()).hexdigest() == geometry["targetSha256"]
    for stroke in data["strokes"]:
        assert len(stroke["points"]) == 16
        assert all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p) for p in stroke["points"])
    articles = ["kanji/俸.md", "words/俸給.md", "kanji/給.md"]
    han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "\n".join((ROOT / n).read_text(encoding="utf-8") for n in articles))))
    assert {"俸", "奉", "亻", "給"} <= set(han)
    android = CONTROL.parent / "kanji-cards-android"
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=android, text=True).strip() == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android).strip()
    fonts = []
    for record in load(FOLDER / "font-coverage.json")["fonts"]:
        path = android / record["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        with TTFont(path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        fonts.append({"path": record["path"], "sha256": record["sha256"], "missing": missing})
    legacy = [{key: v[key] for key in ("kanji", "title", "distractors")}
              for p in sorted((ROOT / "kanji").glob("*.md"))
              if len((v := metadata(ROOT, p.relative_to(ROOT).as_posix())).get("distractors", [])) < 3]
    assert [v["kanji"] for v in legacy] == ["人", "休", "何", "入", "出", "口", "女", "日", "月", "男", "買"]
    actual_counts = {
        "kanji": len(list((ROOT / "kanji").glob("*.md"))),
        "words": len(list((ROOT / "words").glob("*.md"))),
        "n1Labelled": sum(metadata(ROOT, p.relative_to(ROOT).as_posix())["jlpt"] == 1 for p in (ROOT / "kanji").glob("*.md")),
        "namedSourceMembersPresent": sum((ROOT / "kanji" / f"{c}.md").exists() for c in named)}
    assert actual_counts == {"kanji": 1074, "words": 5032, "n1Labelled": 94, "namedSourceMembersPresent": 93}
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    originals = {Path(n).stem for n in load(FOLDER / "baseline-inventory.json")["files"] if n.startswith("kanji/")}
    local_additions = {p.stem for p in (ROOT / "kanji").glob("*.md")} - originals
    assert len(local_additions) == 89 and local_additions <= set(named)
    result = {
        "schemaVersion": 1, "execution": 380, "batch": "062", "status": "local-unreviewed-draft",
        "baseCommit": BASE, "sourceCheckpoint": START, "sourceRow": 56,
        "exactFrozenNamedMembershipAndKanjiVGRecordVerified": True,
        "frozenInputHashesVerified": 5, "decompressedDictionaryHashesVerified": 2,
        "freshExactDictionaryFamilies": 42, "packets": packets,
        "baselineMetadataAndStrokesChecked": counts, "explicitInheritedMetadataExceptions": exceptions,
        "newBaselineMetadataExceptions": [], "immutableEvidenceUnchanged": immutable,
        "runtimeAdditions": sorted(additions), "changedReusedRuntimePayloads": ["kanji/給.md"],
        "manifestFresh": True, "contentVersion": manifest["contentVersion"], "runtimePayloadHashesVerified": checked,
        "baseRuntimeHashesUnchanged": 8310, "actualDraftCounts": actual_counts,
        "requiredReciprocalPairs": 2, "directedLinks": 4, "activatedBaselinePairs": 0,
        "fullReadingDispositions": 1, "offeredKeys": ["ほう"], "sourceOnlyOfferedKeys": [],
        "newWords": 1, "newWordJlptInferred": False, "newDirectWordExclusions": len(EXCLUSIONS),
        "legacyFallbackCandidatesWithFewerThanThree": legacy,
        "legacyFallbackDisposition": "All eleven displayed labels inspected: general person/gender, rest/what, enter/exit, mouth/sun/moon and buy are not salary/stipend. Work/employee and money transaction associations alone are not synonymy. No default four-choice collision established; larger/random/live pools unverified.",
        "geometry": geometry,
        "actualAuthoredHanFonts": {"articles": articles, "characters": han, "count": len(han), "fonts": fonts,
                                  "missingUnion": sorted({c for f in fonts for c in f["missing"]}),
                                  "limits": "Cmap audit of all new/changed article Han including 亻, not native rendering/fallback/drawing or phone acceptance."},
        "budget": check(ROOT, archive_names(ROOT)),
        "publishedAdditions": 88, "remainingAdditions": 1140,
        "limits": "Local unreviewed draft only. No independent reviewer, fresh Android/native check or publication. One local draft does not reduce published remaining additions.",
    }
    save(FOLDER / "batch-062-draft-audit.json", result)
    print(json.dumps({key: result[key] for key in ("actualDraftCounts", "contentVersion", "runtimePayloadHashesVerified", "actualAuthoredHanFonts", "budget")}, ensure_ascii=False, indent=2))


def record():
    assert git("rev-parse", "HEAD") == START
    progress = load(CONTROL / "progress.json")
    audit_record = load(FOLDER / "batch-062-draft-audit.json")
    test_raw = (CONTROL / "logs" / "execution-380-python-tests.txt").read_bytes()
    test_text = test_raw.decode("utf-8-sig")
    assert "Ran 368 tests" in test_text and test_text.rstrip().endswith("OK")
    test_copy = FOLDER / "execution-380-python-tests.txt"
    assert not test_copy.exists()
    test_copy.write_bytes(test_raw)
    record = {
        "schemaVersion": 1, **progress["execution380StartingState"],
        "checkpoint": 380, "recordedAt": datetime.now().astimezone().isoformat(),
        "status": "validated-unreviewed-draft-awaiting-normally-signed-snapshot",
        "membership": ["俸"], "sourceRow": 56, "publishedBase": BASE, "sourceCheckpoint": START,
        "runtimeScope": {
            "newKanji": ["kanji/俸.md"], "newNecessaryWords": ["words/俸給.md"],
            "generatedGeometry": ["strokes/俸.json"], "changedReusedPassages": load(FOLDER / "batch-062-progress.json")["changedReusedPassages"],
            "existingMetadataChanges": [], "fullOn": ["ホウ"], "fullKun": [],
            "proposedOnKeys": ["ほう"], "proposedKunKeys": [], "requiredReciprocalPairs": 2,
            "directedLinks": 4, "newDirectWordExclusions": 9,
        },
        "sourcePacketHashes": {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(FOLDER.glob("batch-062-*")) if p.is_file()},
        "coordinatorInspection": load(FOLDER / "batch-062-progress.json")["draftInspection"],
        "checks": {
            "validatorErrors": 0, "manifestFresh": True,
            "contentVersion": audit_record["contentVersion"], "runtimeHashesVerified": 8314,
            "baselinePreserved": audit_record["baselineMetadataAndStrokesChecked"],
            "newBaselineMetadataExceptions": [], "exactFrozenDictionaryFamilies": 42,
            "frozenInputHashes": 5, "decompressedDictionaryHashes": 2,
            "pythonTests": 368, "pythonFailures": 0, "pythonErrors": 0,
            "pythonLog": test_copy.relative_to(ROOT).as_posix(),
            "pythonLogSha256": hashlib.sha256(test_raw).hexdigest(),
            "testOutputQualification": "Generated-media and429 messages come from existing synthetic fixtures; no media generation authorized or new runtime media produced.",
            "grammarVocabularyConsistency": "Actual python -X utf8 -B tools\\grammar_vocabulary.py check passed; existing2122/2431 coverage retained, not repaired or counted as new work.",
            "localBudget": audit_record["budget"],
            "authoredHan": 30, "bundledMissingUnion": ["亻"],
            "fontQualification": "29/30 Han in all3 unchanged bundled cmaps; actual亻 fallback explicitly inherited from061, not fresh062 rendering.",
            "dedicatedAndroidHead": "f9b59a2bc5a203c6b4de26be50021a4c720dc22c", "dedicatedAndroidClean": True,
        },
        "operationalObservations": [
            "Initial request-tail console print hit cp1252 UnicodeEncodeError after full file load and full embedded JSON parse. Reissued UTF8 inspection; no source/content lost.",
            "First draft-audit run failed at an unchanged generated source-selection file due to comparing newline-normalized read_text against raw Git bytes. Replaced that comparison with exact raw bytes; frozen source packet unchanged and fresh audit passed.",
            "An initial validate_grammar_vocabulary.py invocation only loaded a library and is not counted as vocabulary consistency. The actual grammar_vocabulary.py check was subsequently executed.",
        ],
        "draftAudit": "batch-062-draft-audit.json",
        "draftAuditSha256": hashlib.sha256((FOLDER / "batch-062-draft-audit.json").read_bytes()).hexdigest(),
        "helper": str(Path(__file__).resolve()), "helperSha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "independentReview": "Not started. This is the common local snapshot for future serial blind two-family reviews; no unreviewed push.",
        "freshAndroidNativePhone": "Not performed. Accepted061 evidence remains historical, not substitute062 test results. Physical-phone/general-release acceptance outstanding.",
        "publishedAdditions": 88, "remainingAdditions": 1140,
        "publishedNecessarySupportArticles": 89, "localDraftAdditions": 89, "localSupportArticles": 90,
        "pushed": False, "nextAction": NEXT,
        "limits": audit_record["limits"],
    }
    save(FOLDER / "execution-380.json", record)
    print("Recorded complete bounded draft evidence; ready for normal signed local commit.")


def finish():
    progress = load(CONTROL / "progress.json")
    original = load(CONTROL / "logs" / "d3b5a1bb-9600-4a09-b2cf-a2ed0bd54466" / "checkpoint-full.json")
    assert progress["checkpoint"] == original["checkpoint"] == 379
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    for key, value in original.items():
        if key not in mutable:
            assert progress[key] == value, key
    assert not git("status", "--porcelain")
    saved = git("rev-parse", "HEAD")
    assert saved != START and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == progress["lastPublishedCommit"] == BASE
    expected = {
        "docs/n1-authoring-notes.md", "docs/n1-sources/batch-062-progress.json",
        "docs/n1-sources/batch-062-draft-audit.json",
        "docs/n1-sources/batch-062-quiz-comparison-jmdict.xml",
        "docs/n1-sources/batch-062-quiz-comparison-selection.json",
        "docs/n1-sources/batch-062-stroke-evidence.json",
        "docs/n1-sources/execution-380.json", "docs/n1-sources/execution-380-python-tests.txt",
        "kanji/俸.md", "kanji/給.md", "words/俸給.md", "strokes/俸.json", "manifest.json",
    }
    changed = set(subprocess.check_output(
        ["git", "-c", "core.quotepath=false", "diff", "--name-only", START, saved],
        cwd=ROOT, text=True, encoding="utf-8"
    ).splitlines())
    assert changed == expected, changed
    record = load(FOLDER / "execution-380.json")
    record.update({
        "status": "signed-local-unreviewed-draft-checkpoint-complete",
        "savedCommit": saved, "signature": "G", "dedicatedContentClean": True,
        "localOnly": True, "lastPublishedCommit": BASE,
        "allOriginalHistoricalKeysPreservedExactly": True,
        "originalTopLevelKeys": len(original), "recordedAt": datetime.now().astimezone().isoformat(),
    })
    save(CONTROL / "execution-380-verification.json", record)
    progress.update({
        "checkpoint": 380, "status": "continue", "stage": "batch-062-draft-awaiting-independent-review",
        "batch": "062", "blocker": None, "nextAction": NEXT,
        "batch062DraftCheckpoint": record, "execution380CoordinatorCheckpoint": record,
    })
    progress["execution380StartingState"]["status"] = record["status"]
    save(CONTROL / "progress.json", progress)
    reread = load(CONTROL / "progress.json")
    for key, value in original.items():
        if key not in mutable:
            assert reread[key] == value, key
    assert reread["checkpoint"] == 380 and reread["status"] == "continue"
    print(json.dumps({"checkpoint": 380, "savedCommit": saved, "signature": "G",
                      "status": "continue", "stage": reread["stage"], "originalTopLevelKeysPreserved": len(original) - len(mutable)}, indent=2))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "audit": audit, "record": record, "finish": finish}[sys.argv[1]]()
