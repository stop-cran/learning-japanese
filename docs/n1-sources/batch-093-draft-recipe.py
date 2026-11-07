"""Preserve one source-bounded LOCAL UNREVIEWED batch093 checkpoint."""
import argparse
import ast
import copy
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "548ac74f-7df6-4bd2-b170-4a82700c8a16"
S = R / "docs" / "n1-sources"
HEAD = "52e706b56b7fb04c134ea6894666c52f301491ba"
BASE = "fe9e1a37acddae69a3b131bdf2ea01f9ca8cd2f4"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u5211"
SCOPE = ["kanji/刑.md", "words/刑事.md", "kanji/事.md"]
NEXT = (
    "SAME093 two serial blind different-model-family initial textual reviews on the normally "
    "signed LOCAL UNREVIEWED draft: complete 刑 card and reused N3刑事, exact component-link/"
    "four direct police-label safeguards/事 reciprocal-navigation diff, complete180 frozen "
    "dictionary families/eight character records and comparison articles. Preserve fullケイ/"
    "emptykun, [ケイ]/[] and offeredけい, special whole-wordでか and outside-freezeギョウ "
    "distinctions. Cover correctness/scoped coverage/phone comprehensibility; actual available "
    "models/read-only tools and process exit before next reviewer, original complete reports/"
    "sessions/read limits, evidence-based reconciliation. Then all original fresh non-skipped "
    "Android, production ContentSync ONCE/native N1/All choices/reading/drawing/article/Back/"
    "offline/four-font/all-Han/visual and original-session confirmation gates; combined-main/"
    "normal signing/owner fast-forward/terminal green CI/EVERY immutable ZIP runtime hash/"
    "unchanged budgets/verified owner issue. No094 or unreviewed push. Approvedcontrol/"
    "committedsource/frozeninputs only. Parent19008 retainsrunner.lock: no childacquire/delete/"
    "unlock. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. Published119/"
    "1228 and1109 acceptance-remainder unchanged; physicalphone/generalrelease/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    tmp = path.with_suffix(path.suffix + ".668.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == data
    tmp.replace(path)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def identity(drafted=False):
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^" if drafted else "HEAD") == HEAD
    assert git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (667, "093", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    before = L / "progress-before-668.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 667
    state = {
        "execution": 668, "batch": "093", "startingHead": HEAD, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME093 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,094 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint parsed; operative contract, complete approved issue and final667 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": {
            "liveParentPid": 19008, "sessionId": L.name,
            "ancestry": [24708, 30280, 19008],
            "ownershipEvidence": "Fresh Win32_Process ancestry reaches live19008 encoded control/runner.ps1; runner.json matches running parent/session. Parent owns runner.lock throughout child lifetime.",
            "lockTouched": False,
        },
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs and durable control helpers only; optional historical-session helpers not accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals published BASE. Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain; canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p = load(C / "progress.json")
    p["execution668StartingState"] = state
    p.update(stage="batch-093-runtime-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("SAME093 bounded runtime-draft scope persisted; complete live history preserved.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    svg = (S / "batch-093-kanjivg.svg").read_bytes()
    proof = load(S / "batch-093-stroke-evidence.json")
    assert sha(svg) == proof["sha256"] and svg == Path(proof["input"]).read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 6
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-093-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [104]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR])
    frozen["limits"] = "LOCAL UNREVIEWED draft only; not review closure, native acceptance or publication. Earlier deferred rows and separately placed earlier-level source members remain unchanged."
    save(S / "batch-093-membership.json", frozen)
    p = load(S / "batch-093-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR])
    p["dictionaryPackets"] = [
        {"selection": "batch-093-lexical-selection.json", "xml": "batch-093-jmdict.xml"},
        {"selection": "batch-093-comparison-selection.json", "xml": "batch-093-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], reason=row["qualification"] + " " + row["evidence"])
        if row["selected"]:
            row["article"] = "words/刑事.md"
    p["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": False, "allWrittenKanji": row["allWrittenKanji"],
         "wordJlpt": row["preservedWordJlpt"], "selectedSenses": row["selectedSenses"],
         "status": "local-unreviewed-draft"} for row in p["proposedSupportMapping"]
    ]
    # The generic batch audit counts new-character mappings; the full audit also checks 事.
    p["requiredReciprocalPairs"] = [["刑", "words/刑事.md"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = p["proposedReusedChanges"]
    p["curatedProjection"] = [p["proposedCuratedProjection"]]
    p["quizAudit"] = {CHAR: {
        "title": p["proposedQuiz"]["kanjiTitle"],
        "distractors": p["proposedQuiz"]["distractors"], "labels": p["proposedQuiz"]["labels"],
        "meaningDecisions": p["proposedQuiz"]["rationale"],
        "unsafeComparisons": p["proposedQuiz"]["unsafeComparisons"],
        "limits": "Three existing N1-available wrong labels; default-four fallback not required. Production N1/All options and independent semantic review pending.",
    }}
    p["wordQuizAudit"] = {
        "directExclusions": p["proposedQuiz"]["proposedDirectExclusions"],
        "existingInboundGuards": p["proposedQuiz"]["existingInboundGuards"],
        "limits": p["proposedQuiz"]["limits"],
    }
    p["draftAuthorInspection"] = {
        "execution": 668, "sourceCheckpoint": HEAD,
        "completeMemberFamilies": {
            "path": "control/batch-093-full-family-reading.txt",
            "returnedRanges": [[1, 30], [31, 60], [61, 90], [91, 125], [126, 157]],
            "families": 157,
            "limits": "Faithful compact complete XML freshly returned in five disjoint ranges; raw XML semantic equality audited. Full entries include unselected historical/sensitive/organization-name families, not teaching approval.",
        },
        "completeComparisonFamilies": {
            "path": "control/batch-093-comparison-reading-668.txt",
            "returnedRanges": [[1, 11], [12, 23]], "families": 23,
        },
        "completeCharacterReads": {"batch-093-kanjidic2.xml": [1, 78],
                                   "batch-093-comparison-kanjidic2.xml": [[1, 200], [201, 400], [401, 522]]},
        "completeExistingArticlesRead": list(load(S / "batch-093-preparation-audit.json")["inspectedArticleHashes"]),
        "publicLookup": "Complete committed Digital Daijisen刑/刑事 article-only extractions freshly read, including attributed later material. Archived coordinator-supplied source evidence, not independent upstream retrieval. Missing gaiji preclude a historical derivation claim.",
        "pinnedSvg": "Complete committed SVG freshly read; six ordered paths and explicit right刂/original刀 annotation. Shape mnemonic only; phon attribute not adopted as historical evidence.",
        "diagnostics": ["Optional control comparison text filename did not exist; exposed the committed lossless gzip under a new approved control path. No mandatory evidence missing or permission denial."],
        "limits": "Author inspection, not independent review, native-speaker certification, phone evidence or uniform reviewer read-depth evidence.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no independent reviewer, fresh Android/native/font/phone acceptance or publication.",
        "Exactly one full onケイ/emptykun preserved; explicit[ケイ]/[] offersけい. Broader dictionaryギョウ and special whole-word刑事でか are recognized without modifying frozen metadata or inventing a kun allocation.",
        "No new support words. Existing刑事 identity/reading/title/N3level unchanged, only activated component link and four direct police-label guards; existing探偵 inbound guard retained. Existing事 changes one navigation line only.",
        "Two all-mapped pairs/four directions, one activated baseline pair; distinct from one new-kanji support mapping. All mapped existing components included.",
        "Modern-shape mnemonic only, structure-unclassified, no phonetic field. Canonical刀18 retained, visible刂 explained; 形彡/型土 comparisons qualified. Six pinned paths generated, not manually edited.",
        "Three N1-available wrong labels and four new direct word guards; semantic author audit not universal live-pool certification. Production N1/All choices pending.",
        "Final Han/cmap inventory is not native legibility/fallback-face acceptance. Fresh four-font/all-Han, non-skipped RareHan/native and rendered original-session review gates pending.",
        "Published119/1228 and1109 acceptance-remainder unchanged. Six separate source保案派第策結 retain earlierN2levels and are not accepted issue60 additions; separate妖exception retained.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest appmain; physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates remain. No optional historical-session helpers, parent-lock touch,094 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-093-progress.json", p)
    print("Six pinned paths generated; exact source/member and LOCAL UNREVIEWED ledgers prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "093")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    ledger = load(S / "batch-093-progress.json")
    packets = []
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt.gz" if i == 0 else "comparison-full-family-reading.txt.gz"
        compact_raw = gzip.decompress((S / f"batch-093-{suffix}").read_bytes())
        exposed = C / ("batch-093-full-family-reading.txt" if i == 0 else "batch-093-comparison-reading-668.txt")
        assert compact_raw == exposed.read_bytes()
        assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact_raw.decode("utf-8") + "</JMdict>")] == [
            canonical(e) for e in ET.fromstring(raw)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True, "completeCompactSemanticEquality": True})
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-093-kanjidic2.xml", "batch-093-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(records[entry.findtext("literal")])
            count += 1
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"],
                  "words/刈る.md": ["切る", "収穫"],
                  "words/刑事.md": ["警官", "警察", "巡査", "おまわりさん"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = ["川", "出", "木"]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha((R / name).read_bytes()) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and named[103] == CHAR
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    base_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in base_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {CHAR} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    for c in "保案派第策結":
        assert metadata(R, f"kanji/{c}.md")["jlpt"] == 2
    word = metadata(R, "words/刑事.md")
    assert word["jlpt"] == 3 and word["reading"] == "けいじ" and word["kanji"] == ["刑", "事"]
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/刑事.md"}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {
        ("刑", "words/刑事.md"), ("事", "words/刑事.md")}
    for c, name in all_pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    verified = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = (sha((R / name).read_bytes()) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
                assert actual == expected, name
                verified += 1
    assert verified == 8436
    svg = (S / "batch-093-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-093-draft-stroke-audit.json", dict(
        load(S / "batch-093-stroke-evidence.json"), converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / "strokes" / f"{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-093-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    save(S / "batch-093-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "093", "completeArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE},
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "Complete new card and actual complete reused support/事 articles. Deliberately broader than source-preparation proposed inventory. Cmap presence/absence not native legibility/fallback-face acceptance; fresh four-font/all-Han and non-skipped RareHan/native gates pending.",
    })
    explicit = sorted(p.stem for p in (R / "kanji").glob("*.md")
                      if p.stem != CHAR and CHAR in metadata(R, f"kanji/{p.name}").get("distractors", []))
    assert explicit == []
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in ["乃", "凹", "凸"])
    assert "刑事" in metadata(R, "words/探偵.md")["quiz_exclusions"]
    result.update(
        schemaVersion=1, execution=668, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=5, decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=2, directedLinksVerified=4, newDirectWordExclusionPairs=4,
        existingExplicitTargetDistractors=explicit, allRuntimePayloadHashesVerified=verified,
        actualHanCount=len(han), pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=119,
        remainingAdditions=1109, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-093-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-093-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-668.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8436" in text and result["contentVersion"] in text
        elif stem == "audit":
            assert json.loads(text) == result
        elif stem == "tests":
            assert re.search(r"^OK\r?$", text, re.MULTILINE) and "skipped" not in text
            assert not re.search(r"^(FAILED|ERROR:|FAIL:)", text, re.MULTILINE)
            total = int(re.search(r"Ran (\d+) tests", text)[1])
        elif stem == "vocabulary":
            assert "reviewed prompts" in text
        elif stem == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        elif stem == "whitespace":
            assert not text.strip()
        target = S / f"batch-093-draft-{stem}-668.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    recipe = S / "batch-093-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-668.json", {
        "schemaVersion": 1, "execution": 668, "batch": "093", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution668StartingState"],
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "vocabularyCommand": "python -X utf8 -B tools/grammar_vocabulary.py check",
        "vocabularyLimits": "Existing pilot coverage2122/2431 reviewed prompts; consistency passed, not complete unrelated grammar coverage.",
        "audit": "docs/n1-sources/batch-093-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-093-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-093-draft-stroke-audit.json",
        "recipe": recipe.relative_to(R).as_posix(), "recipeSha256": sha(recipe.read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock throughout child lifetime; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helpers in control. No optional historical-session-helper access.",
        "readEvidenceLimits": load(S / "batch-093-progress.json")["draftAuthorInspection"],
        "actualNewPermissionDenials": [], "publishedAdditions": 119, "remainingAdditions": 1109,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft check receipts and durable recipe archived.")


def freeze():
    identity(drafted=True)
    assert not git("status", "--porcelain")
    signed = git("rev-parse", "HEAD")
    expected = set(SCOPE) | {
        f"strokes/{CHAR}.json", "manifest.json",
        "docs/n1-sources/batch-093-membership.json", "docs/n1-sources/batch-093-progress.json",
        "docs/n1-sources/batch-093-draft-audit.json", "docs/n1-sources/batch-093-draft-font-audit.json",
        "docs/n1-sources/batch-093-draft-stroke-audit.json", "docs/n1-sources/batch-093-draft-recipe.py",
        "docs/n1-sources/execution-668.json",
    } | {f"docs/n1-sources/batch-093-draft-{n}-668.txt.gz"
         for n in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]}
    changed = set(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", signed],
        encoding="utf-8").rstrip("\0").split("\0"))
    assert changed == expected, changed ^ expected
    from build_manifest import build_manifest
    assert build_manifest(R) == load(R / "manifest.json")
    evidence = load(S / "execution-668.json")
    result = load(S / "batch-093-draft-audit.json")
    body = (
        f"Batch093 — signed LOCAL UNREVIEWED draft checkpoint668, not publication.\n\n"
        f"Saved `{signed}` (normal signature G), parent source `{HEAD}`; remote main remains "
        f"`{BASE}`. New 刑 card and six generated pinned KanjiVG paths; no new support word. "
        "Existing N3刑事 changes only its activated component link and four direct police-label "
        "quiz safeguards (警官/警察/巡査/おまわりさん); existing探偵 inbound guard retained. "
        "Existing事 gains one reciprocal-navigation line. All original identities, primary readings, "
        "titles, easier levels and guards are preserved.\n\n"
        "Fullケイ/emptykun retained; explicit[ケイ]/[] offers onlyけい. Broader dictionaryギョウ "
        "and slang whole-word刑事でか are recognized without adding frozen metadata or a kun allocation. "
        "Two all-mapped pairs/four directions, one activated baseline pair; three semantically wrong "
        "N1 labels. Complete180 frozen dictionary families/eight character records, baseline metadata/"
        "strokes, exact runtime delta and all8436 current payload hashes audited. "
        f"Final complete new card/support/事 Han inventory{result['actualHanCount']}; "
        f"main-font cmap absences {''.join(result['pendingNativeFallbackLabels'])}. "
        "Inventory deliberately includes the entire otherwise unchanged事 article, broader than "
        "the proposed source-preparation inventory. Fresh native four-font rendering remains "
        "required; cmap presence/absence is not legibility evidence.\n\n"
        f"Validator0; regenerated manifest `{evidence['contentVersion']}`; "
        f"{evidence['pythonTestsPassed']} focused source/audit tests passed. Vocabulary consistency "
        "passed at existing pilot2122/2431 reviewed prompts, not completed unrelated grammar coverage. "
        f"Local archive {evidence['localBudget']['entries']} entries, "
        f"{evidence['localBudget']['localZipBytes']} compressed / "
        f"{evidence['localBudget']['inflatedBytes']} inflated / "
        f"{evidence['localBudget']['retainedBytes']} retained bytes; unchanged budgets pass. "
        "Evidence/recipe/receipts: docs/n1-sources/execution-668.json and batch-093-draft-*.\n\n"
        "No reviewer, Android/native run, content push or094 started. Next: same frozen draft's "
        "two serial blind different-model-family initial reviews, then reconciliation and every "
        "original Android/native/rendered/integration/publication gate. Published119/1228, "
        "acceptance-remainder1109 unchanged. Compatible curated-reading Androidf9b59a2+ required; "
        "qualifiedTESTONLY Android1c1b7bf4 is not latest appmain. Physical-phone/general-release/"
        "whole-set acceptance remains outstanding.\n\n"
        "Approved workspace/committed evidence/frozen sources only, durable helper in control; "
        "optional historical-session paths not accessed. Live parent19008 retains runner.lock "
        "untouched. No new permission denial. An optional control comparison text filename was "
        "absent; the committed lossless comparison packet was exposed at a new approved control "
        "path and semantic-equality checked. This recoverable draft is not review closure or project completion.\n"
    )
    (C / "batch-093-draft-668-issue.txt").write_bytes(body.encode("utf-8"))
    save(C / "batch-093-draft-668-freeze.json", {
        "commit": signed, "sourceCommit": HEAD, "signature": "G", "whollyClean": True,
        "exactChangedPaths": sorted(changed), "issueBodySha256": sha(body.encode("utf-8")),
        "runtimePublished": False, "parentLockTouched": False,
    })
    print(signed)


def seal():
    identity(drafted=True)
    signed = git("rev-parse", "HEAD")
    assert not git("status", "--porcelain")
    assert signed == load(C / "batch-093-draft-668-freeze.json")["commit"]
    receipt = load(C / "batch-093-draft-668-issue-receipt.json")
    posted = load(L / "issue-668-reread.json")
    expected_body = (C / "batch-093-draft-668-issue.txt").read_bytes().decode("utf-8")
    assert posted["body"] == expected_body and posted["user"]["login"] == "stop-cran"
    assert receipt["verified"] and receipt["author"] == "stop-cran"
    assert receipt["bodySha256"] == sha(posted["body"].encode("utf-8"))
    evidence = load(S / "execution-668.json")
    result = load(S / "batch-093-draft-audit.json")
    state = {
        "schemaVersion": 1, "execution": 668, "checkpoint": 668, "batch": "093",
        "status": "continue", "stage": "local-unreviewed-draft", "savedCommit": signed,
        "signature": "G", "sourceCommit": HEAD, "lastPublishedCommit": BASE,
        "evidence": "docs/n1-sources/execution-668.json",
        "sourcePacket": "docs/n1-sources/batch-093-progress.json",
        "audit": "docs/n1-sources/batch-093-draft-audit.json",
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "completeDictionaryFamilies": 180, "completeRawCharacterRecords": 8,
        "metadataReadings": 1, "newSupportArticles": 0, "reusedSupportArticles": 1,
        "changedReusedArticles": 2, "allMappedReciprocalPairs": 2, "directedLinksVerified": 4,
        "activatedBaselinePairs": 1, "newDirectWordExclusionPairs": 4,
        "generatedStrokePaths": 6, "actualHanCount": result["actualHanCount"],
        "pendingNativeFallbackLabels": result["pendingNativeFallbackLabels"],
        "contentVersion": result["contentVersion"],
        "allRuntimePayloadHashesVerified": result["allRuntimePayloadHashesVerified"],
        "pythonTestsPassed": evidence["pythonTestsPassed"], "validatorErrors": 0,
        "localBudget": evidence["localBudget"], "publishedAdditions": 119,
        "remainingAdditions": 1109, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["url"],
        "nextAction": NEXT,
    }
    before = load(L / "progress-before-668.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in mutable:
            assert p[key] == value, key
    state["originalHistoricalRootKeysCompared"] = len(before)
    state["allOriginalHistoricalValuesPreserved"] = True
    p["execution668CoordinatorCheckpoint"] = state
    p["batch093DraftCheckpoint"] = state
    p["batch093DraftIssueReceipt"] = receipt
    p["execution668StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p.update(checkpoint=668, status="continue", stage="batch-093-local-unreviewed-draft",
             nextAction=NEXT, blocker=None)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    for key, value in before.items():
        if key not in mutable:
            assert persisted[key] == value, key
    save(L / "checkpoint-668.json", state)
    print(json.dumps(state, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=["start", "prepare", "audit", "record", "freeze", "seal"])
    args = parser.parse_args()
    globals()[args.phase]()
