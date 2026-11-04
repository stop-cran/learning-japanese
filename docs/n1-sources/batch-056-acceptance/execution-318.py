import copy
import gzip
import hashlib
import json
import math
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
BASE = "340ce10b1f17ebc93ebb70535db25ab912334596"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=R, encoding="utf-8").strip()


if sys.argv[1] == "start":
    p = load(C / "progress.json")
    assert p["checkpoint"] == 317 and p["status"] == "continue" and p["batch"] == "056"
    assert git("rev-parse", "HEAD") == BASE and not git("status", "--porcelain")
    backup = C / "execution-318-starting-progress.json"
    assert not backup.exists()
    backup.write_bytes((C / "progress.json").read_bytes())
    request = C / "logs" / "1970b5c0-463e-4b15-962a-ceecc152e8db" / "request.txt"
    raw = request.read_bytes()
    record = {
        "execution": 318, "batch": "056", "startingHead": BASE,
        "startedAt": datetime.now().astimezone().isoformat(),
        "scope": "Same056 bounded runtime draft and normally signed LOCAL UNREVIEWED snapshot only; no057, reviewer, Android/native, runtime publication or second runner.",
        "status": "authoring-local-unreviewed-draft",
        "requestRead": {
            "sha256": hashlib.sha256(raw).hexdigest(),
            "lines": len(raw.decode("utf-8-sig").splitlines()),
            "boundary": "Entire 940436-character request acquired into memory and complete embedded checkpoint parsed; operative authorization and final150 lines inspected directly. Historical middle records acquired/parsed, not freshly semantically re-reviewed."
        },
        "worktrees": "Clean signedG340ce10b content and clean dedicated Android. Fresh normal fetch/merge already up to date; no substantive main delta. Full live history preserved."
    }
    after = copy.deepcopy(p)
    after.update(stage="batch-056-authoring-local-unreviewed-draft",
                 execution318StartingState=record, activeExecution=copy.deepcopy(record))
    assert all(after[k] == v for k, v in p.items() if k not in {"stage", "activeExecution"})
    save(C / "progress-execution-318-start.tmp", after)
    (C / "progress-execution-318-start.tmp").replace(C / "progress.json")
    print("Execution318 scope saved; complete live history preserved.")
elif sys.argv[1] == "audit":
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from check_content_budget import archive_names, check
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    f = R / "docs" / "n1-sources"
    ledger = load(f / "batch-056-progress.json")
    mechanical = audit(R, "056")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, row in snapshot["inputs"].items():
        assert hashlib.sha256((C / "inputs" / name).read_bytes()).hexdigest() == row["sha256"]
    for name, section in [
        ("n1-planning-kanjidic2.xml.gz", "kanjidic2"),
        ("n1-implementation-JMdict_e.gz", "jmdict"),
    ]:
        assert hashlib.sha256(gzip.decompress((C / "inputs" / name).read_bytes())).hexdigest() == snapshot[section]["xmlSha256"]
    raw_dictionary = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    families = set()
    packets = []
    for packet in ledger["dictionaryPackets"]:
        selection = load(f / packet["selection"])
        raw = (f / packet["xml"]).read_bytes()
        assert raw == extract(raw_dictionary, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], selection["entryIds"])
        families.update(selection["entryIds"])
        packets.append({"path": packet["xml"], "families": len(selection["entryIds"]),
                        "sha256": hashlib.sha256(raw).hexdigest()})
    assert len(families) == 64
    immutable = [
        "docs/n1-source-snapshot.json", "docs/n1-sources/source-index.json",
        "docs/n1-sources/baseline-inventory.json", "docs/n1-sources/baseline-word-candidates.json",
        *[f"docs/n1-sources/batch-056-{s}" for s in (
            "input-metadata.json", "dictionary-evidence.json", "qualification-audit.json",
            "preparation-audit.json", "jmdict.xml", "comparison-jmdict.xml",
            "lexical-selection.json", "comparison-selection.json")],
    ]
    for name in immutable:
        assert (R / name).read_bytes() == subprocess.check_output(["git", "show", f"{BASE}:{name}"], cwd=R)
    original = load(f / "baseline-inventory.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"]}
    for name, row in original["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(row["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert hashlib.sha256((R / name).read_bytes()).hexdigest() == row["sha256"]
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    manifest = load(R / "manifest.json")
    assert manifest == build_manifest(R)
    before = json.loads(git("show", f"{BASE}:manifest.json"))
    payloads = {name: digest for entries in manifest.values() if isinstance(entries, dict)
                for name, digest in entries.items()}
    previous = {name: digest for entries in before.values() if isinstance(entries, dict)
                for name, digest in entries.items()}
    additions = {"kanji/乏.md", "words/乏しい.md", "words/貧乏.md", "strokes/乏.json"}
    assert set(payloads) - set(previous) == additions and previous.items() <= payloads.items()
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, digest in entries.items():
                actual = hashlib.sha256((R / name).read_bytes()).hexdigest() if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert digest == actual, name
    assert len(previous) == 8293 and len(payloads) == 8297
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    row = next(x for x in load(f / "source-index.json") if x["kanji"] == "乏")
    assert len(named) == len(set(named)) == 1232 and named[row["sourceRow"] - 1] == "乏"
    assert row["sourceRow"] == 10
    raw_svg = (C / "artifacts" / "batch-056-04e4f.svg").read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw_svg)).encode() + b"\0" + raw_svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"]
    raw_strokes = (R / "strokes" / "乏.json").read_bytes()
    normalized = raw_strokes.replace(b"\r\n", b"\n")
    candidate = (C / "artifacts" / "batch-056-stroke-candidate.json").read_bytes()
    assert normalized == candidate
    strokes = json.loads(raw_strokes)
    assert strokes == convert("乏", raw_svg.decode("utf-8"))
    assert strokes["strokeCount"] == 4 and [x["count"] for x in row["metadata"]["strokeCountAnnotations"]] == [4, 3]
    for stroke in strokes["strokes"]:
        assert len(stroke["points"]) == 16
        assert all(len(point) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in point) for point in stroke["points"])
    converter_hash = hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes()).hexdigest()
    assert converter_hash == snapshot["kanjivg"]["converter"]["sha256"]
    authored = sorted(additions - {"strokes/乏.json"})
    han = sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", "\n".join(
        (R / name).read_text(encoding="utf-8") for name in authored))))
    fonts = []
    android = C.parent / "kanji-cards-android"
    assert subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=android, text=True).strip() == "f9b59a2bc5a203c6b4de26be50021a4c720dc22c"
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android).strip()
    for font_record in load(f / "font-coverage.json")["fonts"]:
        path = android / font_record["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == font_record["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            missing = [ch for ch in han if ord(ch) not in cmap]
        fonts.append({"path": font_record["path"], "sha256": font_record["sha256"], "missing": missing})
    assert all(row["missing"] == ["丿", "饉"] for row in fonts)
    legacy = []
    for path in sorted((R / "kanji").glob("*.md")):
        meta = metadata(R, path.relative_to(R).as_posix())
        if len(meta.get("distractors", [])) < 3:
            legacy.append({key: meta[key] for key in ("kanji", "title", "distractors")})
    assert len(legacy) == 12
    pairs = {frozenset((r["word"], target)) for r in ledger["wordQuizAudit"]["directExclusions"] for target in r["exclude"]}
    assert len(pairs) == 9
    for mapping in ledger["supportMappings"]:
        meta = metadata(R, mapping["article"])
        assert "jlpt" not in meta and "jlpt-n1" not in meta["tags"]
        assert meta["kanji"] == sorted(set(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", meta["word"])),
                                       key=lambda c: meta["word"].index(c))
    assert "(../kanji/貧.md)" in (R / "words" / "貧乏.md").read_text(encoding="utf-8")
    result = {
        "schemaVersion": 1, "execution": 318, "batch": "056", "status": "local-unreviewed-runtime-draft",
        "mechanicalBatchAudit": mechanical, "frozenInputHashesVerified": len(snapshot["inputs"]),
        "decompressedDictionaryHashesVerified": 2, "freshExactFrozenFamilyExtraction": len(families),
        "dictionaryPackets": packets, "freshLinguisticReviewOfAllFamiliesClaimed": False,
        "inspectionScope": ledger["draftInspection"], "namedSourceRow": 10,
        "originalBaselineMetadataAndStrokesPreserved": counts, "baselineMetadataExceptions": exceptions,
        "runtimePayloadHashesVerified": len(payloads), "baseRuntimePayloadHashesPreserved": len(previous),
        "runtimeAdditions": sorted(additions), "changedReusedRuntimePayloads": [], "immutableEvidenceUnchanged": immutable,
        "actualDraftCounts": {"kanji": len(list((R / "kanji").glob("*.md"))),
                              "words": len(list((R / "words").glob("*.md"))),
                              "n1Labels": sum(metadata(R, p.relative_to(R).as_posix())["jlpt"] == 1 for p in (R / "kanji").glob("*.md")),
                              "unpublishedBatchAdditions": 1},
        "actualAuthoredHanFonts": {"characters": han, "count": len(han), "fonts": fonts, "missing": ["丿", "饉"],
                                  "requiredNativeFallback": ["丿", "饉"], "limits": "Cmap coverage only. 饉 enters via the justified 飢饉 quiz-exclusion ID, not a new card or invented spelling; include its full existing word in bounded native comparison evidence. No native readability/fallback-face identification or phone acceptance."},
        "legacyFallbackCandidatesWithFewerThanThree": legacy,
        "legacyFallbackDisposition": "All12 actual labels inspected; person/rest/what/enter/exit/mouth/woman/mountain/sun-day/moon-month/man/buy do not denote scarcity, lack or poverty. Existing scarcity-neighbor 貧/欠/少/小/限 each has three curated choices; no default four-choice fallback fill newly required. Three authored wrong labels checked against actual complete cards and ordinary secondary senses. Not every larger/random/live pool certified.",
        "selectedReciprocalPairs": 2, "directedSelectedLinks": 4, "activatedBaselinePairs": 0,
        "existingComponentLinks": 1, "directWordExclusions": len(pairs), "noTransitiveClique": True,
        "geometry": {"sha256": hashlib.sha256(normalized).hexdigest(),
                     "rawRuntimeSha256": hashlib.sha256(raw_strokes).hexdigest(),
                     "rawSvgSha256": hashlib.sha256(raw_svg).hexdigest(), "gitBlob": blob,
                     "strokes": 4, "pointsPerStroke": 16, "unchangedConverter": True,
                     "equalToQualifiedCandidateAfterLfNormalization": True,
                     "serialization": "Unchanged generator Windows CRLF versus prior LF candidate; normalized bytes and parsed geometry identical. No hand-edited geometry."},
        "budget": check(R, archive_names(R)), "publishedAdditions": 82, "remainingAdditions": 1146,
        "limits": ledger["limits"],
    }
    assert result["actualDraftCounts"] == {"kanji": 1068, "words": 5027, "n1Labels": 88, "unpublishedBatchAdditions": 1}
    save(f / "batch-056-draft-audit.json", result)
    print(json.dumps({key: result[key] for key in ("mechanicalBatchAudit", "actualDraftCounts", "actualAuthoredHanFonts", "budget")}, ensure_ascii=False, indent=2))
elif sys.argv[1] == "finish":
    p = load(C / "progress.json")
    assert p["checkpoint"] == 317 and p["status"] == "continue" and p["batch"] == "056"
    head = git("rev-parse", "HEAD")
    assert head == "4dba935415312d39b1c2defdc05b938d37fe21f0"
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    receipt = load(C / "execution-318-issue-receipt.json")
    assert receipt["snapshot"] == head and receipt["author"] == "stop-cran"
    assert receipt["authorAndExactBodyReadbackVerified"] and not receipt["runtimePushed"]
    remote = git("ls-remote", "origin", "refs/heads/main").split()[0]
    assert remote == p["lastPublishedCommit"] == "9b5e9fd9f596801eb78078ab14e4c4b35973479d"
    android = C.parent / "kanji-cards-android"
    assert not subprocess.check_output(["git", "status", "--porcelain"], cwd=android).strip()
    audit = load(R / "docs" / "n1-sources" / "batch-056-draft-audit.json")
    record = {
        **p["execution318StartingState"],
        "status": "signed-local-unreviewed-runtime-draft-checkpoint",
        "savedCommit": head, "signature": "G", "checkpoint": 318,
        "recordedAt": datetime.now().astimezone().isoformat(),
        "runtimeVersion": audit["mechanicalBatchAudit"]["contentVersion"],
        "issueUpdate": receipt["url"], "issueReceipt": "control/execution-318-issue-receipt.json",
        "result": "SAME056 signed local UNREVIEWED 乏 plus necessary 乏しい/貧乏 support; four runtime additions, all8293 existing payload hashes preserved. Full ordered readings retained, two practice keys, two reciprocal pairs plus 貧 component link, nine direct quiz guards, pinned four-stroke geometry.368Python/validator/vocabulary/freshmanifest/all64 exactfamilyextractions/originalbaseline/28authoredHan/originalbudgets passed. Bundled missing 丿/饉 require fresh bounded native fallback evidence. No reviewer/Android/native/push/057/secondrunner.",
        "validation": {
            "pythonTests": 368, "pythonFailures": 0, "pythonErrors": 0, "pythonSkips": 0,
            "validatorErrors": 0, "vocabularyConsistency": "pass",
            "frozenInputHashes": 5, "decompressedDictionaryHashes": 2,
            "exactCompleteFamilyExtractions": 64, "runtimeHashesVerified": 8297,
            "existingRuntimeHashesUnchanged": 8293,
            "actualDraftCounts": audit["actualDraftCounts"], "budget": audit["budget"],
        },
        "limits": "Coordinator draft/source audits, not independent linguistic/native-speaker approval or native/phone/publication acceptance. Full55-family preparation inherited316/317, not a fictional fresh64-family linguistic read. Fresh14 complete families/three archived Japanese sections/actual comparison and distractor articles/12shortfallback labels inspected318. ともしい frequency/register UNVERIFIED, excluded from teaching claims. Cmap absence not native failure. Historical generation cp1252, rawCRLF mismatch, stem-key ledger correction and expanded饉font obligation retained in execution-318.json. Public82/1228,1146remaining. Physical-phone/general-release and whole-set outstanding.",
        "evidence": "docs/n1-sources/execution-318.json",
        "audit": "docs/n1-sources/batch-056-draft-audit.json",
        "scopeUnchanged": "Same056 only; no057 or runtime publication.",
        "dedicatedWorktreesClean": True, "remoteMainObserved": remote,
        "script": {"path": "control/execution-318.py",
                   "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
    }
    next_action = (
        "Resume SAME056乏 at signed LOCAL UNREVIEWED teaching4dba935415312d39b1c2defdc05b938d37fe21f0, "
        "checkpoint318. Read complete authorized request/finalcheckpoint/approvedissue, scoped currentlivekeys; "
        "preserve FULL live history. Review docs/n1-sources/execution-318.json, batch-056-progress.json, "
        "batch-056-draft-audit.json and preserved source qualification. Two SERIAL blind DIFFERENT actual model-family "
        "complete-content initial reviews on SAME signed snapshot; include complete乏/乏しい/貧乏/all3facets, "
        "all64frozenfamilies/actualrelevantcomparisonpassages/exactJapanese-sourcepackets/readings/quiz/link/font/geometry "
        "evidence. Actual currentCLIcatalog/modelidentity/read-onlyavailabletools, oneactivereviewer, serialinternaltools, "
        "realprocessexit and completeoriginalreport/archive before next launch; do not edit frozen snapshot during review. "
        "Treat findings as hypotheses/evidence, preserve original actual read/process limits; original-session bounded "
        "confirmations when justified. Runtimefullorderボウ/とぼ.しい/とも.しい preserved; selectedボウ/とぼ.しい "
        "keysぼう/とぼしい, recognizedalternateともしい ownplainrow not falseprimarylink; frequency/registerUNVERIFIED "
        "and not claimed. Two necessary new support words/noinferredJLPTlevels, tworeciprocalpairs/fourdirections plus "
        "貧componentlink, nineDIRECTwordguards nottransitive, wrongkanjichoices久/反/乃 and12legacyfallback labels "
        "audited. ExactpinnedSVGfbbe870444f6d9a79116535bf0f61c9461607c88/4paths/16points each; standardgenerator "
        "CRLF equals qualifiedLFcandidate afternormalization, sourcealternate3countretained. All28authoredHan checked; "
        "丿 AND 饉 absentall3bundledfonts: canonical丿metadata and justifiedexisting飢饉guard RETAINED, obtain necessary "
        "freshRareHan/native fallback readability including fullcomparisonword; no new饉card/丶prose or glyphfailure "
        "inferred fromcmap. All8293oldruntimehashes preserved;8297current verified, baseline985kanji4942words985strokes "
        "and exact虎[酔っ払い]/猿[馬鹿] guards preserved. Fresh318368Python/validator/vocabulary/manifestcb85043f73a606f3/"
        "64exactfamilies/5frozen2decompressed/baseline/link/readings/geometry/fonts/originalbudgets passed; "
        "fresh14family/3archivedJapanesesection/actualarticles read, preparation55inheritednotfresh64linguisticread. "
        "Then allapplicable FRESH non-skippedAndroid/native(fullarchiveContentSyncONCE/routes/drawing)/originalvisual/"
        "latestmainnormalnonrewritingmerge/combinedtree/sourcebaseline-reading-link-font-stroke/Python/vocabulary/"
        "validator/freshmanifest/originalbudgets/normalsigning/ownerfastforward/remoteSHA/terminalgreenCI/"
        "everyimmutablepublicZIPruntimehash/terminalreceipts/ownerissue60 BEFOREdelivery or057. "
        "No accepted055 review/Android/native rerun absentnewconcern. Published82/1228,1146remaining; currentLOCALdraft "
        "1068kanji5027words88N1labels includes ONE UNPUBLISHED addition. Androidf9b59a2+ required; "
        "physicalphone/generalrelease/whole-setoutstanding. Noauthoragents/concurrentheavywork/secondrunner/"
        "signingretry/permissionworkaround. Overallprojectincomplete."
    )
    after = copy.deepcopy(p)
    after.update(checkpoint=318, status="continue", stage="batch-056-signed-local-unreviewed-draft",
                 blocker=None, nextAction=next_action,
                 batch056DraftCheckpoint=record, execution318CoordinatorCheckpoint=record,
                 activeExecution=copy.deepcopy(record))
    changed = {"checkpoint", "status", "stage", "blocker", "nextAction", "activeExecution"}
    assert all(after[k] == v for k, v in p.items() if k not in changed)
    assert after["remainingAdditions"] == 1146 and after["lastPublishedCommit"] == remote
    temp = C / "progress-execution-318-finish.tmp"
    assert not temp.exists()
    save(temp, after)
    temp.replace(C / "progress.json")
    actual = load(C / "progress.json")
    assert actual == after and len(actual) >= len(p)
    save(C / "execution-318-checkpoint-receipt.json", {
        "checkpoint": 318, "status": "continue", "stage": actual["stage"],
        "savedCommit": head, "signature": "G", "issueUpdate": receipt["url"],
        "fullHistoryPreserved": True, "originalKeyCount": len(p), "currentKeyCount": len(actual),
        "publishedAdditions": 82, "remainingAdditions": 1146,
        "runtimePushed": False, "nextAction": next_action,
    })
    print(json.dumps({"checkpoint": actual["checkpoint"], "status": actual["status"],
                      "stage": actual["stage"], "head": head, "signature": "G",
                      "issue": receipt["url"], "historyPreserved": True}, indent=2))
else:
    raise ValueError("Expected start, audit or finish")
