"""Preserve one source-bounded local UNREVIEWED draft; never publish runtime."""
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

import yaml

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "e60e842d-0567-4a4a-962f-63922f36da0c"
S = R / "docs" / "n1-sources"
HEAD = "c296c481428473fcd401cf22cd3c3f6383c7f9c7"
BASE = "4c2416e4c5925e6910b32215412bb1b795f60524"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "剛"
SCOPE = ["kanji/剛.md", "words/剛健.md"]
NEXT = (
    "SAME096 TWO serial blind different-model-family initial textual reviews on the "
    "normally signed LOCAL UNREVIEWED snapshot: complete剛/剛健, sole fullゴウ/empty kun "
    "and explicitゴウ/[], twelve direct word guards, ONE all-mapped pair/TWO directions, "
    "no changed reused passages. Same frozen complete102 dictionary families/12 raw "
    "character records/public source evidence for both reviewers; correctness, scoped "
    "coverage and phone comprehensibility. Actual available models/read-only tools and "
    "actual process exit before next reviewer, complete original reports/sessions/read "
    "limits, evidence reconciliation and bounded original-session confirmations. Then "
    "fresh non-skipped Android, production ContentSync ONCE/native N1-All/meaning/reading/"
    "drawing/article/Back/offline/four-font/all-Han/rendered review, actual combined-main "
    "acceptance, normal signing/owner fast-forward/terminal CI/EVERY immutable public ZIP "
    "runtime hash/unchanged budgets/verified owner issue. Do not start097 or push unreviewed "
    "content. Approved control/committed evidence/frozen inputs only; parent19008 retains "
    "runner.lock, no child acquire/delete/unlock/readprobe. Preserve/report/yield actual "
    "new denial/signing hang/uncertain ownership. Published122/1228,1106 acceptance "
    "remainder unchanged; physical-phone/general-release/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".701.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (700, "096", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    before = L / "progress-before-701.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["checkpoint"] == 700
    assert checkpoint["execution700CoordinatorCheckpoint"] == p["execution700CoordinatorCheckpoint"]
    role = load(L / "preflight-701.json")
    assert role["liveParentPid"] == 19008 and role["sessionId"] == L.name and not role["lockTouched"]
    p["execution701StartingState"] = {
        "execution": 701, "batch": "096", "startingHead": HEAD, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME096 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,097 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete approved issue and final700 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs and durable control helpers only; optional historical-session recipes not accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals published BASE. Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain; canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-096-runtime-draft-in-progress",
             nextAction=p["execution701StartingState"]["scope"], blocker=None)
    save(C / "progress.json", p)
    print("SAME096 runtime-draft scope persisted; complete historical values preserved.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    proof = load(S / "batch-096-stroke-evidence.json")
    svg = (S / "batch-096-kanjivg.svg").read_bytes()
    assert sha(svg) == proof["sha256"] and svg == Path(proof["input"]).read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 10
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-096-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [107]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR])
    frozen["limits"] = "LOCAL UNREVIEWED draft only, not review closure, native acceptance or publication."
    save(S / "batch-096-membership.json", frozen)
    p = load(S / "batch-096-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR])
    p["dictionaryPackets"] = [
        {"selection": f"batch-096-{stem}selection.json", "xml": f"batch-096-{xml}.xml"}
        for stem, xml in [("lexical-", "jmdict"), ("comparison-", "comparison-jmdict"),
                          ("final-label-", "final-label-jmdict")]
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], article="words/剛健.md",
                   reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": True, "allWrittenKanji": row["allWrittenKanji"],
         "wordJlpt": None, "selectedSenses": row["selectedSenses"], "status": "local-unreviewed-draft"}
        for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = []
    p["curatedProjection"] = [p["proposedCuratedProjection"]]
    p["quizAudit"] = {CHAR: {
        "title": p["proposedQuiz"]["kanjiTitle"], "distractors": p["proposedQuiz"]["distractors"],
        "labels": p["proposedQuiz"]["labels"], "meaningDecisions": p["proposedQuiz"]["rationale"],
        "unsafeComparisons": p["proposedQuiz"]["unsafeComparisons"],
        "limits": "Default-four fallback unnecessary; independent semantic and production N1/All review pending.",
    }}
    exclusions = [r["words"][1] for r in p["proposedQuiz"]["proposedDirectExclusions"]] + ["活力"]
    p["wordQuizAudit"] = {
        "directExclusions": [{"word": "剛健", "exclude": exclusions,
                              "reasons": p["proposedQuiz"]["proposedDirectExclusions"] + [{
                                  "words": ["剛健", "活力"], "entryIds": ["1284120", "1208480"],
                                  "evidence": "Actual vitality; energy label and personal vitality use overlap robust vigor. Conservative direct guard, not unrestricted Japanese substitution."}]}],
        "finalLabelAudit": {
            "proposedGuards": 11, "actualGuards": 12,
            "addedGuard": "剛健/活力, supported by complete newly extracted1208480 and actual existing article.",
            "additionalComparison": "Complete1010340/actualばりばり article inspected: ripping/crunching or vigorous work is not robust constitution or character; no added guard.",
            "otherLabelNavigation": "Existing title scan for robust/vigor/sturdy/vitality/strong/strength/energetic/healthy returned23 titles before this draft. Activity/strengthening, strong yen, deep color/concentration, strong points and losing vigor do not themselves mean robust or vigorous; no automatic topic clique.",
            "confusableInventory": "CW035 and vitality/onomatopoeia navigation checked, not assumed exhaustive.",
        },
        "limits": "Direct pairs only, not transitive cliques or full live-pool certification.",
    }
    p["draftAuthorInspection"] = {
        "execution": 701, "sourceCheckpoint": HEAD,
        "completeMemberFamilies": {"path": "control/batch-096-full-family-reading.txt", "returnedRanges": [[1, 42], [43, 90]], "families": 78},
        "completeComparisonFamilies": {"path": "control/batch-096-comparison-reading.txt", "returnedRanges": [[1, 30]], "families": 25},
        "finalLabelFamilies": {"path": "docs/n1-sources/batch-096-final-label-jmdict.xml", "families": 2, "completeFreshRead": True},
        "rawCharacterScope": "Complete剛 and健 freshly read. Ten remaining complete comparison records inherited source700 inspection and freshly frozen-byte-bound, not freshly fully semantically read.",
        "existingArticleScope": "All25 source-preparation articles freshly read; additional活力/ばりばり articles freshly read, unchanged.",
        "publicLookup": "Complete committed剛/剛健 article extractions freshly read. Archived coordinator evidence, not fresh upstream retrieval. No gaiji-based historical claim.",
        "pinnedSvg": "Complete committed SVG freshly read; ten paths, 岡/冂/山 modern shapes and right-hand刂/original刀 annotation. SVG phon attribute not historical proof.",
        "limits": "Author inspection only, not independent review, native-speaker certification, phone evidence or uniform reviewer comprehension.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no reviewer, fresh Android/native/font/phone acceptance or runtime publication.",
        "Full soleゴウ and empty kun retained; explicitゴウ/[] selection. Supplementalコウ/native glosses/name readings not appended to pinned metadata.",
        "One necessary剛健ごうけん article, no inferred vocabulary level; metadata includes健 despite its missing card. No changed reused passages.",
        "ONE all-mapped pair/TWO directions/ZERO activated baseline pairs. Twelve direct guards after exact final-label audit, not transitive exclusions or unrestricted substitutions.",
        "Labelled modern-shape mnemonic only, structure-unclassified, no phonetic/history claim. Canonical刀18 retained, visible刂 explained; ten pinned paths generated.",
        "Final Han/cmap audit is not native glyph/fallback acceptance. Fresh non-skipped Android/native/four-font/all-Han/rendered review pending.",
        "Published122/1228 and1106 acceptance remainder unchanged. Six earlier-level source保案派第策結 remain separate;妖exception preserved.",
        "CompatibleAndroidf9b59a2+ required; qualified TESTONLY1c1b7bf4 not latest appmain. Physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates retained; no097 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-096-progress.json", p)
    print("Ten pinned paths and local UNREVIEWED ledgers prepared; final-label guard12 recorded.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "096")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    ledger = load(S / "batch-096-progress.json")
    packets = []
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        if i < 2:
            suffix = "full-family-reading.txt" if i == 0 else "comparison-full-family-reading.txt"
            compact = gzip.decompress((S / f"batch-096-{suffix}.gz").read_bytes())
            exposed = C / ("batch-096-full-family-reading.txt" if i == 0 else "batch-096-comparison-reading.txt")
            assert compact == exposed.read_bytes()
            assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact.decode("utf-8") + "</JMdict>")] == [
                canonical(e) for e in ET.fromstring(raw)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-096-kanjidic2.xml", "batch-096-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(records[entry.findtext("literal")])
            count += 1
    assert count == 12
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
    assert named == load(S / "community-list-20261102.json") and named[106] == CHAR
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    old_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in old_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {CHAR} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    for c in "保案派第策結":
        assert metadata(R, f"kanji/{c}.md")["jlpt"] == 2
    word = metadata(R, "words/剛健.md")
    assert "jlpt" not in word and word["kanji"] == ["剛", "健"]
    assert not (R / "kanji" / "健.md").exists()
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/剛健.md"}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {("剛", "words/剛健.md")}
    for c, name in all_pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    assert len(word["quiz_exclusions"]) == 12
    final_labels = {w: metadata(R, f"words/{w}.md")["title"] for w in word["quiz_exclusions"]}
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
    assert verified == 8444
    svg = (S / "batch-096-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-096-draft-stroke-audit.json", dict(
        load(S / "batch-096-stroke-evidence.json"), converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / "strokes" / f"{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-096-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    save(S / "batch-096-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "096", "completeArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE}, "fonts": fonts,
        "rareHanRangeCharacters": [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF
            or 0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF],
        "nativeFontAcceptance": "pending", "limits": "Cmap evidence only, not glyph/fallback acceptance; fresh four-font/all-Han/native gates pending.",
    })
    for c in "削剖則強力硬固柔":
        assert len(metadata(R, f"kanji/{c}.md")["distractors"]) == 3
    for name, expected in load(S / "batch-096-preparation-audit.json")["inspectedArticleHashes"].items():
        assert sha((R / name).read_bytes()) == expected, name
    result.update(
        schemaVersion=1, execution=701, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=1, directedLinksVerified=2, newDirectWordExclusionPairs=12,
        actualFinalExcludedLabels=final_labels, originalSourcePreparationArticlesByteUnchanged=25,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=122,
        remainingAdditions=1106, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-096-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-096-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-701.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8444" in text and result["contentVersion"] in text
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
        target = S / f"batch-096-draft-{stem}-701.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    for source, target in [
        (Path(__file__), S / "batch-096-draft-recipe.py"),
        (C / "preflight-701.ps1", S / "batch-096-draft-preflight-701.ps1.txt"),
        (C / "checks-batch-096-draft-701.ps1", S / "batch-096-draft-checks-701.ps1.txt"),
    ]:
        target.write_bytes(source.read_bytes())
    save(S / "execution-701.json", {
        "schemaVersion": 1, "execution": 701, "batch": "096", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution701StartingState"],
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "vocabularyLimits": "Existing reviewed-prompt consistency only, not unrelated coverage completion.",
        "audit": "docs/n1-sources/batch-096-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-096-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-096-draft-stroke-audit.json",
        "recipe": "docs/n1-sources/batch-096-draft-recipe.py", "recipeSha256": sha(Path(__file__).read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock; child never acquires/deletes/unlocks/read-probes.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helpers in control.",
        "readEvidenceLimits": load(S / "batch-096-progress.json")["draftAuthorInspection"],
        "actualNewPermissionDenials": [], "publishedAdditions": 122, "remainingAdditions": 1106,
        "finalLabelAuditChange": "Added direct活力 guard to original eleven proposals after actual final-label/article/full-family inspection. Preserved original proposal/evidence; additional1010340 inspected without guard.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft receipts and durable recipes archived.")


def freeze():
    identity(drafted=True)
    assert not git("status", "--porcelain")
    signed = git("rev-parse", "HEAD")
    expected = set(SCOPE) | {f"strokes/{CHAR}.json", "manifest.json",
        "docs/n1-sources/batch-096-membership.json", "docs/n1-sources/batch-096-progress.json",
        "docs/n1-sources/batch-096-draft-audit.json", "docs/n1-sources/batch-096-draft-font-audit.json",
        "docs/n1-sources/batch-096-draft-stroke-audit.json", "docs/n1-sources/batch-096-draft-recipe.py",
        "docs/n1-sources/batch-096-draft-preflight-701.ps1.txt",
        "docs/n1-sources/batch-096-draft-checks-701.ps1.txt", "docs/n1-sources/execution-701.json",
        "docs/n1-sources/batch-096-final-label-selection.json", "docs/n1-sources/batch-096-final-label-jmdict.xml",
    } | {f"docs/n1-sources/batch-096-draft-{n}-701.txt.gz"
         for n in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]}
    changed = set(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", signed],
        encoding="utf-8").rstrip("\0").split("\0"))
    assert changed == expected, changed ^ expected
    from build_manifest import build_manifest
    assert build_manifest(R) == load(R / "manifest.json")
    result = load(S / "batch-096-draft-audit.json")
    evidence = load(S / "execution-701.json")
    before = load(L / "progress-before-701.json")
    p = load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 701, "checkpoint": 701, "batch": "096",
        "status": "continue", "stage": "local-unreviewed-draft", "savedCommit": signed,
        "signature": "G", "sourceCommit": HEAD, "lastPublishedCommit": BASE,
        "membership": [CHAR], "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "runtimePublished": False, "dedicatedWorktreesClean": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 122, "remainingAdditions": 1106,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "validatorErrors": 0,
        "contentVersion": result["contentVersion"], "allRuntimePayloadHashesVerified": 8444,
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "activatedBaselinePairs": 0,
        "metadataReadingDispositions": 1, "curatedOfferedKeys": 1, "newSupportArticles": 1,
        "changedReusedArticles": 0, "newDirectWordExclusionPairs": 12, "dictionaryFamilies": 102,
        "actualHanCount": result["actualHanCount"], "pendingNativeFallbackLabels": result["pendingNativeFallbackLabels"],
        "sourcePacket": "docs/n1-sources/batch-096-progress.json",
        "audit": "docs/n1-sources/batch-096-draft-audit.json", "evidence": "docs/n1-sources/execution-701.json",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [], "nextAction": NEXT,
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
    }
    p["execution701StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution701CoordinatorCheckpoint"] = checkpoint
    p["batch096LocalUnreviewedDraft"] = copy.deepcopy(checkpoint)
    p.update(checkpoint=701, status="continue", stage="batch-096-local-unreviewed-draft",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    save(L / "checkpoint-701.json", checkpoint)
    body = (
        f"Batch096: signed LOCAL UNREVIEWED draft checkpoint701, not publication.\n\n"
        f"Saved `{signed}` (normal signature G), source `{HEAD}`; remote main remains `{BASE}`. "
        "New 剛 card, necessary 剛健ごうけん article without inferred vocabulary level, "
        "and ten generated pinned KanjiVG strokes. No reused teaching/metadata changed; "
        "健 remains in the word metadata without a broken link to its absent card. "
        "Full soleゴウ/empty kun retained; explicitゴウ/[] yieldsごう only. "
        "ONE all-mapped pair/TWO directions/ZERO activated baseline pairs. Twelve direct "
        "word guards: final-label audit adds活力 to the eleven source proposals using "
        "its actual article and complete frozen family; not unrestricted substitution.\n\n"
        "Evidence: `docs/n1-sources/execution-701.json` and draft audit/font/stroke records. "
        "Frozen102 complete dictionary families/12 character records freshly byte-bound; "
        f"baseline metadata/strokes and all8444 runtime hashes audited. Complete new-article "
        f"Han inventory{result['actualHanCount']}; main-font cmap absences "
        f"{''.join(result['pendingNativeFallbackLabels'])}, not native glyph acceptance.\n\n"
        "Next: TWO serial blind different-family textual reviews on this snapshot, "
        "evidence reconciliation/original-session confirmations, fresh non-skipped Android/"
        "native/four-font/all-Han/rendered and combined-main/CI/every immutable ZIP hash "
        "gates. No reviewer, Android/native run, runtime push or097 in this checkpoint. "
        "Published122/1228;1106 acceptance remainder unchanged. Compatible curated-reading "
        "APK required; physical-phone/general-release/whole-set outstanding. Approved "
        "workspace/control artifacts only; live parent's runner.lock untouched.\n"
    )
    (C / "batch-096-draft-701-issue.txt").write_bytes(body.encode("utf-8"))
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))


def issue():
    posted = load(L / "issue-701-posted.json")
    actual = load(L / "issue-701-reread.json")
    raw = (C / "batch-096-draft-701-issue.txt").read_bytes()
    assert posted["id"] == actual["id"] and actual["user"]["login"] == "stop-cran"
    assert actual["body"].encode("utf-8") == raw
    receipt = {"id": actual["id"], "url": actual["html_url"], "author": "stop-cran",
               "bodySha256": sha(raw), "verified": True, "comparison": "Exact UTF-8 bytes."}
    p = load(C / "progress.json")
    before = load(L / "progress-before-701.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (701, "096", "continue")
    assert git("rev-parse", "HEAD") == p["execution701CoordinatorCheckpoint"]["savedCommit"]
    for root in (R, A):
        assert not git("status", "--porcelain", root=root)
        assert git("log", "-1", "--format=%G?", root=root) == "G"
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    for key in ["execution701CoordinatorCheckpoint", "batch096LocalUnreviewedDraft"]:
        p[key]["issueUpdate"] = receipt["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    p["batch096DraftIssueReceipt"] = receipt
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    save(L / "checkpoint-701.json", p["execution701CoordinatorCheckpoint"])
    save(C / "batch-096-draft-701-issue-receipt.json", receipt)
    print("Owner issue bytes, signed clean heads and complete historical values verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=["start", "prepare", "audit", "record", "freeze", "issue"])
    globals()[parser.parse_args().step]()
