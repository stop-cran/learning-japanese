"""Bounded source-backed local UNREVIEWED draft; no runtime publication."""
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
L = C / "logs" / "47d1af28-dc02-481e-9d98-69756bbbc418"
S = R / "docs" / "n1-sources"
HEAD = "0ccfbcc2ee066534a28414d428d6fc3a6240ef67"
BASE = "69af99e5d7bf34b093959d90dddc7d59fe6393b5"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "剤"
SCOPE = ["kanji/剤.md"]
REUSED = ["words/洗剤.md", "kanji/洗.md"]
NEXT = (
    "SAME098 TWO serial blind different-model-family initial textual reviews on the "
    "normally signed LOCAL UNREVIEWED snapshot: complete剤 and exact reused洗剤/洗 "
    "navigation changes. Fullザイ/スイ/セイ andかる/けず.る retained in source order; "
    "only quizOnyomi[ザイ], quizKunyomi[] selected; FOUR individually qualified "
    "source-only rows. 洗剤せんざい N2 identity/all metadata/originalせっけん exclusion "
    "preserved; no new support word/word level/word title/guard. TWO all-mapped pairs/"
    "FOUR directions/ONE activated baseline pair. Same frozen352 complete dictionary "
    "families/eight raw character records/actual public sources for both reviewers; "
    "correctness, scoped coverage and phone comprehensibility. No invented剤る spelling, "
    "obsolescence claim, phonetic history or substring-reading allocation. Actual models/"
    "read-only tools, wait for actual process exit before next reviewer, preserve complete "
    "reports/sessions/read limits, reconcile evidence and use original-session confirmations. "
    "Then fresh non-skipped Android, production ContentSync ONCE/native N1-All/meaning/"
    "curated reading/drawing/article/Back/offline/four-font/all-Han/rendered review, "
    "combined-current-main validation, normal signing/owner fast-forward/terminal green CI/"
    "EVERY immutable public ZIP runtime hash/unchanged18000entry42MiBcompressed80MiBinflated"
    "56MiBretained/per-file/path/media guards/verified ownerissue remain mandatory. "
    "No unreviewed push/099/authoragent/concurrentheavywork/secondrunner. Parent19008 "
    "owns runner.lock; no child acquire/delete/unlock/readprobe. Approved control/"
    "committed evidence/frozen inputs only; preserve/report/yield actual new denial/"
    "signing hang/uncertain ownership. Preserve every historical source/review/process/"
    "denial/OOM/read-depth/native/phone limitation. Published124/1228,1104 acceptance "
    "remainder unchanged; physical-phone/general-release/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".719.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == data
    temporary.replace(path)


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
    assert (p["checkpoint"], p["batch"], p["status"]) == (718, "098", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    before = L / "progress-before-719.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["checkpoint"] == 718
    assert checkpoint["execution718CoordinatorCheckpoint"] == p["execution718CoordinatorCheckpoint"]
    role = load(L / "preflight-719.json")
    assert role["liveParentPid"] == 19008 and not role["lockTouched"]
    p["execution719StartingState"] = {
        "execution": 719, "batch": "098", "startingHead": HEAD, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME098 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,099 or second runner.",
        "status": "runtime-draft-in-progress",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed before implementation. Operative contract, complete approved issue and final718 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs and durable control helpers only; optional historical-session recipes not accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals published BASE. Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain; canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-098-runtime-draft-in-progress",
             nextAction=p["execution719StartingState"]["scope"], blocker=None)
    save(C / "progress.json", p)
    print("SAME098 draft scope persisted; complete historical values preserved.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    proof = load(S / "batch-098-stroke-evidence.json")
    svg = (S / "batch-098-kanjivg.svg").read_bytes()
    assert sha(svg) == proof["sha256"] and svg == Path(proof["input"]).read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 10
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-098-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [109]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR])
    frozen["limits"] = "LOCAL UNREVIEWED draft only, not review closure, native acceptance or publication."
    save(S / "batch-098-membership.json", frozen)
    p = load(S / "batch-098-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR], runtimeChanged=True)
    p["dictionaryPackets"] = [
        {"selection": "batch-098-lexical-selection.json", "xml": "batch-098-jmdict.xml"},
        {"selection": "batch-098-comparison-selection.json", "xml": "batch-098-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"],
                   reason=row["qualification"] + " " + row["evidence"])
        if row["selected"]:
            row["article"] = "words/洗剤.md"
    p["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": row["newArticle"],
         "allWrittenKanji": row["allWrittenKanji"], "wordJlpt": row["wordJlpt"],
         "selectedSenses": row["selectedSenses"], "status": "local-unreviewed-draft"}
        for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = [[CHAR, r["article"]] for r in p["supportMappings"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = [
        {"article": "words/洗剤.md",
         "before": "[洗](../kanji/洗.md) contributes washing, and 剤 an agent or preparation.",
         "after": "[洗](../kanji/洗.md) contributes washing, and [剤](../kanji/剤.md) an agent or preparation."},
        {"article": "kanji/洗.md",
         "before": "- 洗濯 せんたく — laundry; washing\n\n## Notes",
         "after": "- 洗濯 せんたく — laundry; washing\n- [洗剤](../words/洗剤.md) せんざい — detergent; cleaning agent\n\n## Notes"},
    ]
    p["curatedProjection"] = [p["proposedCuratedProjection"]]
    p["quizAudit"] = {CHAR: {
        "title": p["proposedQuiz"]["kanjiTitle"], "distractors": p["proposedQuiz"]["distractors"],
        "labels": p["proposedQuiz"]["labels"], "meaningDecisions": p["proposedQuiz"]["rationale"],
        "unsafeComparisons": p["proposedQuiz"]["unsafeComparisons"],
        "limits": "Default-four fallback unnecessary; independent semantic and production N1/All review pending.",
    }}
    p["wordQuizAudit"] = {
        "directExclusions": [],
        "finalLabelAudit": {
            "newOrRewordedTitles": 0, "newDirectExclusions": 0,
            "reusedTitle": metadata(R, "words/洗剤.md")["title"],
            "preservedOriginalExclusions": ["せっけん"],
            "disposition": p["proposedQuiz"]["wordQuizDisposition"],
            "limits": "No new/reworded word title; existing guard retained, not an all-pool quiz certification.",
        },
    }
    p["draftAuthorInspection"] = {
        "execution": 719, "sourceCheckpoint": HEAD,
        "freshCompleteLexicalFamilies": ["1296370", "1357120", "1390950", "1429160", "1538220",
                                        "2170160", "2276330", "2569220", "2837804"],
        "freshCompleteComparisonFamilies": ["1209540", "1298090", "1298100"],
        "inheritedSourceInspection": "Committed718 full336 member/18 comparison families (352 distinct), eight raw character records and15 complete older articles retained. Unselected lexical families are freshly byte-bound to frozen dictionary, not all freshly semantically reread in719.",
        "rawCharacterScope": "Complete剤 and洗 raw records freshly read; remaining comparison raw records inherited718 and freshly byte-bound. No historical/phonetic claim derived from SVG.",
        "freshExistingArticles": ["words/洗剤.md", "kanji/洗.md", "kanji/済.md", "kanji/剛.md",
                                  "kanji/則.md", "kanji/薬.md", "kanji/剣.md"],
        "publicLookup": "Committed actual Digital Daijisen剤 and洗剤 entry blocks freshly read with authority headings and provenance; archived coordinator source evidence, not fresh upstream retrieval. Character mirror/Wiktionary blocks not treated as independent reputable allocation evidence.",
        "pinnedSvg": "Complete committed SVG freshly read; ten paths. Source shape attributes not promoted to historical/phonetic teaching.",
        "limits": "Author inspection only, not independent review, native-speaker certification, phone evidence or uniform reviewer comprehension.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no reviewer, fresh Android/native/font/phone acceptance or runtime publication.",
        "Fullザイ/スイ/セイ andかる/けず.る retained in source order. Onlyザイ offered; four individually qualified source-only rows, not claims of invalidity/obsolescence.",
        "No new support article or inferred word level; reused洗剤せんざい N2 metadata/readings/originalせっけん guard unchanged.",
        "TWO all-mapped pairs/FOUR directions/ONE activated baseline pair. Two exact reused navigation changes, no broader rewrite or metadata change.",
        "No new word title/direct guard. Three final kanji labels semantically wrong for medicinal preparation/chemical agent;薬 retained as overlapping comparison, not wrong choice.",
        "Labelled modern-shape mnemonic only, structure-unclassified, no phonetic/history claim. Canonical刀18 retained, visible刂 explained; ten pinned paths generated.",
        "Final Han/cmap audit is not native glyph/fallback acceptance. Fresh non-skipped Android/native/four-font/all-Han/rendered review pending.",
        "Published124/1228 and1104 acceptance remainder unchanged. Six earlier-level source保案派第策結 remain separate;妖exception preserved.",
        "CompatibleAndroidf9b59a2+ required; qualified TESTONLY1c1b7bf4 not latest appmain. Physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates retained; no099 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-098-progress.json", p)
    print("Ten pinned paths and local UNREVIEWED ledgers prepared; no new support word.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "098")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    ledger = load(S / "batch-098-progress.json")
    packets = []
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt" if i == 0 else "comparison-full-family-reading.txt"
        compact = gzip.decompress((S / f"batch-098-{suffix}.gz").read_bytes())
        assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact.decode("utf-8") + "</JMdict>")] == [
            canonical(e) for e in ET.fromstring(raw)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-098-kanjidic2.xml", "batch-098-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(records[entry.findtext("literal")])
            count += 1
    assert count == 8
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"],
                  "words/刈る.md": ["切る", "収穫"],
                  "words/刑事.md": ["警官", "警察", "巡査", "おまわりさん"],
                  "words/削る.md": ["切る", "減らす", "省く", "消す", "除く", "外す", "縮める"],
                  "words/削除.md": ["消す", "除く", "外す", "取る", "削る", "省く"]}
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
    assert named == load(S / "community-list-20261102.json") and named[108] == CHAR
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    old_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in old_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {CHAR} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    for c in "保案派第策結":
        assert metadata(R, f"kanji/{c}.md")["jlpt"] == 2
    word = metadata(R, "words/洗剤.md")
    assert word["jlpt"] == 2 and word["reading"] == "せんざい" and word["quiz_exclusions"] == ["せっけん"]
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/洗剤.md"}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(all_pairs) == 2
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
    assert verified == 8449
    svg = (S / "batch-098-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-098-draft-stroke-audit.json", dict(
        load(S / "batch-098-stroke-evidence.json"), converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / "strokes" / f"{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    text += "".join(row["after"] for row in ledger["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-098-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    save(S / "batch-098-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "098", "completeArticleScope": SCOPE,
        "changedReusedScope": ledger["changedReusedPassages"],
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE + REUSED}, "fonts": fonts,
        "rareHanRangeCharacters": [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF
            or 0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF],
        "nativeFontAcceptance": "pending", "limits": "Cmap evidence only, not glyph/fallback acceptance; fresh four-font/all-Han/native gates pending. Unchanged reused article text outside exact diff is inherited, not fresh font acceptance scope.",
    })
    for c in "済剛則薬洗削":
        assert len(metadata(R, f"kanji/{c}.md")["distractors"]) == 3
    unchanged = 0
    for name, expected in load(S / "batch-098-preparation-audit.json")["inspectedArticleHashes"].items():
        if name not in REUSED:
            assert sha((R / name).read_bytes()) == expected, name
            unchanged += 1
    assert unchanged == 13
    result.update(
        schemaVersion=1, execution=719, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=2, directedLinksVerified=4, newDirectWordExclusionPairs=0,
        preservedWordExclusions=word["quiz_exclusions"],
        originalSourcePreparationArticlesByteUnchanged=unchanged, reusedMetadataPreserved=REUSED,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=124,
        remainingAdditions=1104, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-098-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-098-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-719.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8449" in text and result["contentVersion"] in text
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
        else:
            assert not text.strip()
        target = S / f"batch-098-draft-{stem}-719.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    for source, target in [
        (Path(__file__), S / "batch-098-draft-recipe.py"),
        (C / "preflight-719.ps1", S / "batch-098-draft-preflight-719.ps1.txt"),
        (C / "checks-batch-098-draft-719.ps1", S / "batch-098-draft-checks-719.ps1.txt"),
    ]:
        target.write_bytes(source.read_bytes())
    save(S / "execution-719.json", {
        "schemaVersion": 1, "execution": 719, "batch": "098", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution719StartingState"],
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "vocabularyLimits": "Existing reviewed-prompt consistency only, not unrelated coverage completion.",
        "audit": "docs/n1-sources/batch-098-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-098-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-098-draft-stroke-audit.json",
        "recipe": "docs/n1-sources/batch-098-draft-recipe.py", "recipeSha256": sha(Path(__file__).read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock; child never acquires/deletes/unlocks/read-probes.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helpers in control.",
        "readEvidenceLimits": load(S / "batch-098-progress.json")["draftAuthorInspection"],
        "actualNewPermissionDenials": [], "publishedAdditions": 124, "remainingAdditions": 1104,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft receipts and durable recipes archived.")


def freeze():
    from build_manifest import build_manifest
    identity(drafted=True)
    assert not git("status", "--porcelain")
    signed = git("rev-parse", "HEAD")
    expected = set(SCOPE + REUSED) | {f"strokes/{CHAR}.json", "manifest.json",
        "docs/n1-sources/batch-098-membership.json", "docs/n1-sources/batch-098-progress.json",
        "docs/n1-sources/batch-098-draft-audit.json", "docs/n1-sources/batch-098-draft-font-audit.json",
        "docs/n1-sources/batch-098-draft-stroke-audit.json", "docs/n1-sources/batch-098-draft-recipe.py",
        "docs/n1-sources/batch-098-draft-preflight-719.ps1.txt",
        "docs/n1-sources/batch-098-draft-checks-719.ps1.txt", "docs/n1-sources/execution-719.json",
    } | {f"docs/n1-sources/batch-098-draft-{n}-719.txt.gz"
         for n in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]}
    changed = set(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", signed],
        encoding="utf-8").rstrip("\0").split("\0"))
    assert changed == expected, changed ^ expected
    assert build_manifest(R) == load(R / "manifest.json")
    result = load(S / "batch-098-draft-audit.json")
    evidence = load(S / "execution-719.json")
    before = load(L / "progress-before-719.json")
    p = load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 719, "checkpoint": 719, "batch": "098",
        "status": "continue", "stage": "local-unreviewed-draft", "savedCommit": signed,
        "signature": "G", "sourceCommit": HEAD, "lastPublishedCommit": BASE,
        "membership": [CHAR], "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "runtimePublished": False, "dedicatedWorktreesClean": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 124, "remainingAdditions": 1104,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "validatorErrors": 0,
        "contentVersion": result["contentVersion"], "allRuntimePayloadHashesVerified": 8449,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 1,
        "metadataReadingDispositions": 5, "sourceOnlyReadings": 4, "curatedOfferedKeys": 1,
        "newSupportArticles": 0, "changedReusedArticles": 2, "newDirectWordExclusionPairs": 0,
        "dictionaryFamilies": 352, "actualHanCount": result["actualHanCount"],
        "pendingNativeFallbackLabels": result["pendingNativeFallbackLabels"],
        "sourcePacket": "docs/n1-sources/batch-098-progress.json",
        "audit": "docs/n1-sources/batch-098-draft-audit.json", "evidence": "docs/n1-sources/execution-719.json",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [], "nextAction": NEXT,
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
    }
    p["execution719StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution719CoordinatorCheckpoint"] = checkpoint
    p["batch098LocalUnreviewedDraft"] = copy.deepcopy(checkpoint)
    p.update(checkpoint=719, status="continue", stage="batch-098-local-unreviewed-draft",
             nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", p)
    assert all(load(C / "progress.json")[k] == v for k, v in before.items() if k not in allowed)
    save(L / "checkpoint-719.json", checkpoint)
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["start", "prepare", "audit", "record", "freeze"])
    args = parser.parse_args()
    globals()[args.stage]()
