"""Persist one source-bounded local, unreviewed N1 draft checkpoint."""
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
L = C / "logs" / "80bb7faf-5416-4e2f-8a73-1eeb54b65f72"
S = R / "docs" / "n1-sources"
HEAD = "efb840c5f1224361b8dc29223f8517e74c032ceb"
BASE = "48765e20846e1d6769c6ddc35146f6ce58deab57"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u524a"
SCOPE = ["kanji/削.md", "words/削る.md", "words/削除.md", "kanji/除.md"]
NEXT = (
    "SAME094 two serial blind different-model-family initial textual reviews on the normally "
    "signed LOCAL UNREVIEWED draft: complete削 card, complete reused N2削る/削除 and exact "
    "navigation-only diff including N3除; complete frozen dictionary packets and character records "
    "with source evidence. Preserve fullサク andけず.る/はつ.る/そ.ぐ order, select onlyサク/けず.る; "
    "do not link recognitionはつる to primaryけずる or globalize the sense-local usually-kana flag "
    "forそぐ. Cover correctness/scoped coverage/phone comprehensibility; actual available models "
    "and read-only tools, process exit before next reviewer, complete original reports/sessions/"
    "read limits, evidence-based reconciliation. Then original fresh non-skipped Android, "
    "production ContentSync ONCE/native N1/All choices/reading/drawing/article/Back/offline/"
    "four-font/all-Han/rendered review and original-session confirmation gates; combined-main/"
    "normal signing/owner fast-forward/terminal green CI/EVERY immutable ZIP runtime hash/"
    "unchanged budgets/verified owner issue. No095 or unreviewed push. Approved control/"
    "committed source/frozen inputs only. Parent19008 retains runner.lock; no child acquire/"
    "delete/unlock. Preserve/report/yield actual new denial/signing hang/uncertain ownership. "
    "Published120/1228 and1108 acceptance-remainder unchanged; physicalphone/generalrelease/"
    "whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    tmp = path.with_suffix(path.suffix + ".677.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (676, "094", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    before = L / "progress-before-677.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 676
    assert checkpoint["execution676CoordinatorCheckpoint"] == load(C / "progress.json")["execution676CoordinatorCheckpoint"]
    role = load(L / "preflight-677.json")
    assert role["liveParentPid"] == 19008 and role["sessionId"] == L.name and not role["lockTouched"]
    state = {
        "execution": 677, "batch": "094", "startingHead": HEAD, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME094 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,095 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, complete approved issue and final676 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial scalar display failed under cp1252 after successful full read/parse; bounded UTF-8 output succeeded."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs and durable control helpers only; optional historical-session helpers not accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals published BASE. Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain; canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p = load(C / "progress.json")
    p["execution677StartingState"] = state
    p.update(stage="batch-094-runtime-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("SAME094 draft scope persisted; complete live history preserved.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    svg = (S / "batch-094-kanjivg.svg").read_bytes()
    proof = load(S / "batch-094-stroke-evidence.json")
    assert sha(svg) == proof["sha256"] and svg == Path(proof["input"]).read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 9
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-094-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [105]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR])
    frozen["limits"] = "LOCAL UNREVIEWED draft only; not review closure, native acceptance or publication. Earlier deferred rows and separately placed earlier-level source members remain unchanged."
    save(S / "batch-094-membership.json", frozen)
    p = load(S / "batch-094-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR])
    p["dictionaryPackets"] = [
        {"selection": "batch-094-lexical-selection.json", "xml": "batch-094-jmdict.xml"},
        {"selection": "batch-094-comparison-selection.json", "xml": "batch-094-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": False, "allWrittenKanji": row["allWrittenKanji"],
         "wordJlpt": row["preservedWordJlpt"], "selectedSenses": row["selectedSenses"],
         "status": "local-unreviewed-draft"} for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = [["削", "words/削る.md"], ["削", "words/削除.md"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = p["proposedReusedChanges"]
    p["curatedProjection"] = [p["proposedCuratedProjection"]]
    p["quizAudit"] = {CHAR: {
        "title": p["proposedQuiz"]["kanjiTitle"],
        "distractors": p["proposedQuiz"]["distractors"], "labels": p["proposedQuiz"]["labels"],
        "meaningDecisions": p["proposedQuiz"]["rationale"],
        "unsafeComparisons": p["proposedQuiz"]["unsafeComparisons"],
        "limits": "Three existing wrong labels; default-four fallback not required. Production N1/All options and independent semantic review pending.",
    }}
    p["wordQuizAudit"] = {
        "directExclusions": [],
        "existingInboundGuards": p["proposedQuiz"]["existingInboundGuards"],
        "existingOwnGuards": p["proposedQuiz"]["existingOwnGuards"],
        "limits": p["proposedQuiz"]["legacyFallbackDisposition"],
    }
    p["draftAuthorInspection"] = {
        "execution": 677, "sourceCheckpoint": HEAD,
        "completeMemberFamilies": {"path": "control/batch-094-full-family-reading.txt",
                                   "returnedRanges": [[1, 25], [26, 50], [51, 75], [76, 99]], "families": 99},
        "completeComparisonFamilies": {"path": "control/batch-094-comparison-reading.txt",
                                       "returnedRanges": [[1, 13], [14, 26]], "families": 26},
        "rawCharacterScope": "Complete new member record freshly read; nine comparison records inherited source676 inspection and freshly frozen-byte-bound, not a fresh full semantic read.",
        "completeExistingArticlesRead": SCOPE[1:] + ["kanji/前.md", "kanji/判.md", "kanji/刑.md"],
        "publicLookup": "Complete committed Digital Daijisen削/削る/削除 article extractions freshly read, including attributed later material. Archived coordinator-supplied evidence, not fresh upstream retrieval. Missing gaiji preclude a historical derivation claim.",
        "pinnedSvg": "Complete committed SVG freshly read; nine ordered paths and explicit right刂/original刀 annotation. Shape mnemonic only; phon attribute not adopted as historical evidence.",
        "limits": "Author inspection, not independent review, native-speaker certification, phone evidence or uniform reviewer read-depth evidence. Prior source676 complete comparison-article inspection remains attributed to source preparation.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no independent reviewer, fresh Android/native/font/phone acceptance or publication.",
        "Fullサク andけず.る/はつ.る/そ.ぐ retained in source order; explicit[サク]/[けず.る] offersさく/けずる. Recognitionはつる is separate from primaryけずる;そぐ's usually-kana flag is sense-local, not global.",
        "No new support words. Existing削る/削除 retain N2, identity, primary reading, title, forms, senses and exclusions. Existing除 retains N3 and all metadata. Three exact navigation-only reused changes.",
        "Three all-mapped pairs/six directions, two activated baseline pairs; distinct from two new-kanji support mappings. All mapped existing components included.",
        "Modern-shape mnemonic only, structure-unclassified, no phonetic field. Canonical刀18 retained, visible刂 explained; nine pinned paths generated, not manually edited.",
        "Three semantically distinct wrong labels; no new direct word exclusions. Existing own/inbound guards retained. Semantic author audit not universal live-pool certification. Production N1/All choices pending.",
        "Final Han/cmap inventory is not native legibility/fallback-face acceptance. Fresh four-font/all-Han, non-skipped RareHan/native and rendered original-session review gates pending.",
        "Published120/1228 and1108 acceptance-remainder unchanged. Six separate source保案派第策結 retain earlierN2levels and are not accepted issue60 additions; separate妖exception retained.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest appmain; physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates remain. No optional historical-session helpers, parent-lock touch,095 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-094-progress.json", p)
    print("Nine pinned paths and LOCAL UNREVIEWED ledgers prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "094")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    ledger = load(S / "batch-094-progress.json")
    packets = []
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt" if i == 0 else "comparison-full-family-reading.txt"
        compact_raw = gzip.decompress((S / f"batch-094-{suffix}.gz").read_bytes())
        exposed = C / ("batch-094-full-family-reading.txt" if i == 0 else "batch-094-comparison-reading.txt")
        assert compact_raw == exposed.read_bytes()
        assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact_raw.decode("utf-8") + "</JMdict>")] == [
            canonical(e) for e in ET.fromstring(raw)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True, "completeCompactSemanticEquality": True})
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-094-kanjidic2.xml", "batch-094-comparison-kanjidic2.xml"]:
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
    assert named == load(S / "community-list-20261102.json") and named[104] == CHAR
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    base_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in base_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {CHAR} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    for c in "保案派第策結":
        assert metadata(R, f"kanji/{c}.md")["jlpt"] == 2
    for row in ledger["supportMappings"]:
        assert metadata(R, row["article"])["jlpt"] == 2
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/削る.md", "words/削除.md"}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {
        ("削", "words/削る.md"), ("削", "words/削除.md"), ("除", "words/削除.md")}
    for c, name in all_pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    for row in ledger["wordQuizAudit"]["existingOwnGuards"]:
        assert metadata(R, f"words/{row['word']}.md")["quiz_exclusions"] == row["exclude"]
    for row in ledger["wordQuizAudit"]["existingInboundGuards"]:
        assert row["excludeContains"] in metadata(R, f"words/{row['word']}.md")["quiz_exclusions"]
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
    assert verified == 8438
    svg = (S / "batch-094-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-094-draft-stroke-audit.json", dict(
        load(S / "batch-094-stroke-evidence.json"), converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / "strokes" / f"{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-094-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    save(S / "batch-094-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "094", "completeArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE},
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "Complete new card, both complete reused support articles and complete navigation-only除 article. Cmap presence/absence not native legibility/fallback-face acceptance; fresh four-font/all-Han and non-skipped RareHan/native gates pending.",
    })
    explicit = sorted(p.stem for p in (R / "kanji").glob("*.md")
                      if p.stem != CHAR and CHAR in metadata(R, f"kanji/{p.name}").get("distractors", []))
    for c in "消切減省除":
        assert len(metadata(R, f"kanji/{c}.md")["distractors"]) == 3
    result.update(
        schemaVersion=1, execution=677, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=3, directedLinksVerified=6, newDirectWordExclusionPairs=0,
        existingExplicitTargetDistractors=explicit, allRuntimePayloadHashesVerified=verified,
        actualHanCount=len(han), pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=120,
        remainingAdditions=1108, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-094-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-094-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-677.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8438" in text and result["contentVersion"] in text
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
        target = S / f"batch-094-draft-{stem}-677.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    for source, target in [
        (Path(__file__), S / "batch-094-draft-recipe.py"),
        (C / "preflight-677.ps1", S / "batch-094-draft-preflight-677.ps1.txt"),
        (C / "checks-batch-094-draft-677.ps1", S / "batch-094-draft-checks-677.ps1.txt"),
    ]:
        target.write_bytes(source.read_bytes())
    save(S / "execution-677.json", {
        "schemaVersion": 1, "execution": 677, "batch": "094", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution677StartingState"],
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "vocabularyCommand": "python -X utf8 -B tools/grammar_vocabulary.py check",
        "vocabularyLimits": "Existing pilot coverage2122/2431 reviewed prompts; consistency passed, not complete unrelated grammar coverage.",
        "audit": "docs/n1-sources/batch-094-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-094-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-094-draft-stroke-audit.json",
        "recipe": "docs/n1-sources/batch-094-draft-recipe.py",
        "recipeSha256": sha(Path(__file__).read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock throughout child lifetime; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helpers in control. No optional historical-session-helper access.",
        "readEvidenceLimits": load(S / "batch-094-progress.json")["draftAuthorInspection"],
        "actualNewPermissionDenials": [], "publishedAdditions": 120, "remainingAdditions": 1108,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft check receipts and durable recipes archived.")


def freeze():
    identity(drafted=True)
    assert not git("status", "--porcelain")
    signed = git("rev-parse", "HEAD")
    expected = set(SCOPE) | {
        f"strokes/{CHAR}.json", "manifest.json",
        "docs/n1-sources/batch-094-membership.json", "docs/n1-sources/batch-094-progress.json",
        "docs/n1-sources/batch-094-draft-audit.json", "docs/n1-sources/batch-094-draft-font-audit.json",
        "docs/n1-sources/batch-094-draft-stroke-audit.json", "docs/n1-sources/batch-094-draft-recipe.py",
        "docs/n1-sources/batch-094-draft-preflight-677.ps1.txt",
        "docs/n1-sources/batch-094-draft-checks-677.ps1.txt", "docs/n1-sources/execution-677.json",
    } | {f"docs/n1-sources/batch-094-draft-{n}-677.txt.gz"
         for n in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]}
    changed = set(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", signed],
        encoding="utf-8").rstrip("\0").split("\0"))
    assert changed == expected, changed ^ expected
    from build_manifest import build_manifest
    assert build_manifest(R) == load(R / "manifest.json")
    evidence = load(S / "execution-677.json")
    result = load(S / "batch-094-draft-audit.json")
    before = load(L / "progress-before-677.json")
    p = load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 677, "checkpoint": 677, "batch": "094",
        "status": "continue", "stage": "local-unreviewed-draft",
        "savedCommit": signed, "signature": "G", "sourceCommit": HEAD,
        "lastPublishedCommit": BASE, "membership": [CHAR], "runtimeDrafted": [CHAR],
        "reviewClosed": [], "published": [], "runtimePublished": False,
        "dedicatedWorktreesClean": True, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 120,
        "remainingAdditions": 1108, "pythonTestsPassed": evidence["pythonTestsPassed"],
        "validatorErrors": 0, "contentVersion": result["contentVersion"],
        "allRuntimePayloadHashesVerified": result["allRuntimePayloadHashesVerified"],
        "allMappedReciprocalPairs": 3, "directedLinksVerified": 6,
        "activatedBaselinePairs": 2, "metadataReadingDispositions": 4,
        "curatedOfferedKeys": 2, "newSupportArticles": 0, "changedReusedArticles": 3,
        "newDirectWordExclusionPairs": 0, "actualHanCount": result["actualHanCount"],
        "pendingNativeFallbackLabels": result["pendingNativeFallbackLabels"],
        "sourcePacket": "docs/n1-sources/batch-094-progress.json",
        "audit": "docs/n1-sources/batch-094-draft-audit.json", "evidence": "docs/n1-sources/execution-677.json",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
    }
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    p["execution677StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution677CoordinatorCheckpoint"] = checkpoint
    p["batch094LocalUnreviewedDraft"] = copy.deepcopy(checkpoint)
    p.update(checkpoint=677, status="continue", stage="batch-094-local-unreviewed-draft",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    checkpoint["originalHistoricalRootKeysCompared"] = len(before)
    checkpoint["allOriginalHistoricalValuesPreserved"] = True
    p["batch094LocalUnreviewedDraft"] = copy.deepcopy(checkpoint)
    save(C / "progress.json", p)
    save(L / "checkpoint-677.json", checkpoint)
    body = (
        f"Batch094: signed LOCAL UNREVIEWED draft checkpoint677, not publication.\n\n"
        f"Saved `{signed}` (normal signature G), source `{HEAD}`; remote main remains `{BASE}`. "
        "New 削 card and nine generated pinned KanjiVG strokes; no new support words. "
        "Existing N2削る/削除 gain only activated component links; N3除 gains one reciprocal "
        "navigation line. Original identities, readings, titles, easier levels and exclusions preserved.\n\n"
        "Fullサク andけず.る/はつ.る/そ.ぐ retained in source order; select onlyサク/けず.る "
        "(さく/けずる). The separateはつる reading is not linked to the primaryけずる article; "
        "そぐ is not called obsolete or globally usually-kana. Three all-mapped pairs/six links "
        "and two activated baseline pairs checked. No new quiz guards; all existing direct "
        "guards preserved. Frozen121 distinct dictionary families/ten character records freshly "
        "byte-bound; original baseline metadata/strokes and all8438 runtime payload hashes audited. "
        f"Final complete article Han inventory{result['actualHanCount']}; main-font cmap absences "
        f"{''.join(result['pendingNativeFallbackLabels'])}, not native glyph acceptance.\n\n"
        f"Evidence: `docs/n1-sources/execution-677.json` and draft audit/font/stroke records. "
        "All independent textual review, reconciliation, fresh non-skipped Android/native/"
        "four-font/all-Han/rendered acceptance and combined-main/CI/exact immutable ZIP gates remain. "
        "No reviewer, Android/native run, runtime push or095 in this checkpoint. "
        "Published120/1228;1108 acceptance-remainder unchanged. Compatible curated-reading APK "
        "required; physical-phone/general-release/whole-set acceptance remains outstanding. "
        "Approved workspace inputs/control helpers only; live parent ownsrunner.lock, untouched."
    )
    (C / "batch-094-draft-677-issue.txt").write_text(body + "\n", encoding="utf-8")
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))


def issue():
    posted = load(L / "issue-677-posted.json")
    actual = load(L / "issue-677-reread.json")
    body = (C / "batch-094-draft-677-issue.txt").read_text(encoding="utf-8").strip()
    assert posted["id"] == actual["id"] and actual["user"]["login"] == "stop-cran"
    assert actual["body"].strip() == body
    receipt = {"id": actual["id"], "url": actual["html_url"], "author": "stop-cran",
               "bodySha256": sha(actual["body"].encode("utf-8")), "verified": True}
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (677, "094", "continue")
    before = load(L / "progress-before-677.json")
    for key in ["execution677CoordinatorCheckpoint", "batch094LocalUnreviewedDraft"]:
        p[key]["issueUpdate"] = receipt["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    p["batch094DraftIssueReceipt"] = receipt
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    assert not git("status", "--porcelain") and not git("status", "--porcelain", root=A)
    assert git("rev-parse", "HEAD") == p["execution677CoordinatorCheckpoint"]["savedCommit"]
    assert git("log", "-1", "--format=%G?") == "G"
    save(C / "progress.json", p)
    save(L / "checkpoint-677.json", p["execution677CoordinatorCheckpoint"])
    save(C / "batch-094-draft-677-issue-receipt.json", receipt)
    print("Owner issue author/body verified; full-history checkpoint677 persisted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["start", "prepare", "audit", "record", "freeze", "issue"])
    globals()[parser.parse_args().operation]()
