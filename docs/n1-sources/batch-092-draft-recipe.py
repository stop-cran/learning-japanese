"""Prepare and preserve the bounded LOCAL UNREVIEWED batch092 draft."""
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
L = C / "logs" / "eb264d1c-41f1-4824-9422-5bee6d3842ad"
S = R / "docs" / "n1-sources"
HEAD = "40c5160cc3b92077a886720084ba3d18454a4859"
BASE = "2186eda1bf306c7cc16c1ceca80d273dd893a0bd"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u5208"
SCOPE = [f"kanji/{CHAR}.md", f"words/{CHAR}\u308b.md"]
NEXT = (
    "SAME092 two serial blind different-model-family initial textual reviews on the normally "
    "signed LOCAL UNREVIEWED draft: complete 刈 card and reused N3 刈る, actual component-link/"
    "direct収穫-guard diff, complete75 dictionary families/six character records and comparison "
    "articles. Preserve ガイ/カイ/か.る source order, []/[か.る] and offeredかる, both recognized "
    "unselected刈除 readings, one all-mapped pair/two directions, labelled shape-only mnemonic/"
    "刀-visible刂 distinction, three wrong N1 labels and existing word guards. Cover correctness/"
    "scoped coverage/phone comprehensibility; verify actual available models/read-only tools and "
    "reviewer process exit before next reviewer. Preserve original reports/models/read limits/"
    "sessions and reconcile evidence-based findings. Then all original fresh non-skipped Android, "
    "full production ContentSync ONCE/native N1/All choices/reading/drawing/article/Back/offline/"
    "four-font/visual and original-session confirmation gates; combined-current-main checks/"
    "normal signing/owner fast-forward/terminal green CI/EVERY immutable ZIP runtime hash/"
    "unchanged budgets/verified owner issue. No093 or unreviewed push. Approved control helpers/"
    "committed packets/frozen workspace inputs only; parent19008 retains runner.lock untouched. "
    "Preserve/report/yield actual new denial, signing hang or uncertain ownership. Published118/"
    "1228 and1110 acceptance-remainder unchanged; physical-phone/general-release/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data):
    tmp = p.with_suffix(p.suffix + ".659.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == data
    tmp.replace(p)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def identity():
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    progress = load(C / "progress.json")
    assert (progress["checkpoint"], progress["batch"], progress["status"]) == (658, "092", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    before = L / "progress-before-659.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 658
    state = {
        "execution": 659, "batch": "092", "startingHead": HEAD, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME092 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,093 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/parsed; operative contract, complete approved issue and final658 inspected directly. Historical middle parsed, not freshly semantically re-reviewed. Initial console encoding failure followed complete loading/parsing; bounded UTF-8 inspection succeeded."},
        "runnerPreflight": {
            "liveParentPid": 19008, "sessionId": L.name,
            "ownershipEvidence": "Fresh Win32_Process19008 command decoded as control/runner.ps1; runner.json matches running parent/session. Parent owns runner.lock throughout child lifetime.",
            "lockTouched": False,
        },
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs and durable control helpers only; optional historical-session helpers not accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals published BASE. Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain; canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p = load(C / "progress.json")
    p["execution659StartingState"] = state
    p.update(stage="batch-092-runtime-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("SAME092 bounded runtime-draft scope persisted; complete live history preserved.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    svg = (S / "batch-092-kanjivg.svg").read_bytes()
    proof = load(S / "batch-092-stroke-evidence.json")
    assert sha(svg) == proof["sha256"] and svg == Path(proof["input"]).read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 4
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-092-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [103]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR])
    frozen["limits"] = "LOCAL UNREVIEWED draft only; not review closure, native acceptance or publication. Earlier deferred rows and separately placed earlier-level source members remain unchanged."
    save(S / "batch-092-membership.json", frozen)
    p = load(S / "batch-092-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR])
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], reason=row["qualification"] + " " + row["evidence"])
        if row["selected"]:
            row["article"] = SCOPE[1]
    p["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": False, "allWrittenKanji": row["allWrittenKanji"],
         "wordJlpt": row["preservedWordJlpt"], "selectedSenses": row["selectedSenses"],
         "status": "local-unreviewed-draft"} for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = p["proposedReusedChanges"]
    p["curatedProjection"] = [p["proposedCuratedProjection"]]
    p["quizAudit"] = {CHAR: {
        "title": p["proposedQuiz"]["kanjiTitle"],
        "distractors": p["proposedQuiz"]["distractors"],
        "labels": p["proposedQuiz"]["labels"],
        "meaningDecisions": p["proposedQuiz"]["rationale"],
        "unsafeComparisons": p["proposedQuiz"]["unsafeComparisons"],
        "limits": "Three existing N1-available wrong labels; default-four fallback not required. Production N1/All options and independent semantic review pending.",
    }}
    p["wordQuizAudit"] = {
        "titles": {CHAR + "る": metadata(R, SCOPE[1])["title"],
                   "収穫": metadata(R, "words/収穫.md")["title"]},
        "directExclusions": p["proposedQuiz"]["proposedDirectExclusions"],
        "existingInboundGuards": p["proposedQuiz"]["existingInboundGuards"],
        "notAutomaticallyExcluded": p["proposedQuiz"]["notAutomaticallyExcluded"],
        "confusableInventory": "Scoped inventory search for 刈/reap/mow/harvest/clip returned no entry; title unchanged. Actual complete lexical families and relevant older articles inspected, not title strings alone.",
        "limits": "One new direct harvest/reap safeguard, preserving original 切る guard and unchanged inbound 剃る/取り入れる pairs. Not transitive closure or unrestricted substitution.",
    }
    p["draftAuthorInspection"] = {
        "execution": 659, "sourceCheckpoint": HEAD,
        "completeMemberFamilies": {
            "path": "control/batch-092-full-family-reading.txt",
            "returnedRanges": [[1, 31], [32, 62]],
            "families": 62,
            "limits": "Faithful whitespace-compacted complete XML freshly returned in two disjoint ranges. Raw packet equality checked semantically; no flags/aliases/restrictions/senses omitted.",
        },
        "completeComparisonFamilies": {
            "path": "batch-092-comparison-jmdict.xml",
            "returnedRanges": [[1, 220], [221, 440], [441, 581]], "families": 13,
        },
        "completeCharacterReads": {"batch-092-kanjidic2.xml": [1, 81],
                                   "batch-092-comparison-kanjidic2.xml": [[1, 200], [201, 386]]},
        "completeExistingArticlesRead": list(load(S / "batch-092-preparation-audit.json")["inspectedArticleHashes"]),
        "publicLookup": "Complete committed karu/gaijo article-only extractions freshly read. Coordinator-supplied archived source evidence, not independent upstream retrieval. Jitsu corroboratesガイ only; no frequency/history claim adopted.",
        "pinnedSvg": "Complete committedSVG freshly read; four ordered paths and explicit right刂/original刀 annotation. Shape mnemonic only; no phonetic/scissors derivation.",
        "diagnostics": [
            "Initial combined compact comparison output exceeded tool return limit; raw packets then read completely in bounded disjoint ranges.",
            "Initial request console output hit cp1252 after entire file loading/parsing; bounded UTF-8 output succeeded. Historical middle parsed, not freshly semantically re-reviewed.",
        ],
        "limits": "Author inspection, not independent content review, native-speaker certification, phone evidence or uniform future reviewer read-depth evidence.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no independent reviewer, fresh Android/native/font/phone acceptance or publication.",
        "All three metadata readings preserved in source order; both on readings recognized through unrestricted刈除 family, not classified as missing/source-only/obsolete. Onlyか.る selected, with linked existingN3 support and actual offered keyかる.",
        "No new support words. Existing刈る identity/reading/title/N3level and original切る exclusion preserved; only component link and direct収穫guard changed. One all-mapped/baseline pair, two link directions.",
        "Modern-shape mnemonic only, structure-unclassified, no phonetic field. Canonical刀18 retained, visible刂 explained. Four pinned paths generated, not manually edited.",
        "Three N1-available wrong labels and one new direct word guard; semantic author audit not universal live-pool certification. Production N1/All checks pending.",
        "Final Han/cmap inventory is not native legibility/fallback-face acceptance. Fresh four-font/all-Han, non-skipped RareHan/native and rendered original-session review gates pending.",
        "Published118/1228 and1110 acceptance-remainder unchanged. Six separate source保案派第策結 retain earlierN2levels and are not accepted issue60 additions; separate妖exception retained.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest appmain; physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates remain. No optional historical-session helpers, parent-lock touch,093 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-092-progress.json", p)
    print("Four pinned paths generated; exact source/member and LOCAL UNREVIEWED ledgers prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "092")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    ledger = load(S / "batch-092-progress.json")
    packets = []
    for packet in ledger["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    compact_raw = (C / "batch-092-full-family-reading.txt").read_bytes()
    assert compact_raw == gzip.decompress((S / "batch-092-full-family-reading.txt.gz").read_bytes())
    compact = compact_raw.decode("utf-8")
    assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact + "</JMdict>")] == [
        canonical(e) for e in ET.parse(S / "batch-092-jmdict.xml").getroot()]
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-092-kanjidic2.xml", "batch-092-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(records[entry.findtext("literal")])
            count += 1
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"],
                  SCOPE[1]: ["切る", "収穫"]}
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
    assert named == load(S / "community-list-20261102.json") and named[102] == CHAR
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    base_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in base_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {CHAR} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    for c in "保案派第策結":
        assert metadata(R, f"kanji/{c}.md")["jlpt"] == 2
    word = metadata(R, SCOPE[1])
    assert word["jlpt"] == 3 and word["reading"] == "かる" and word["kanji"] == [CHAR]
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {SCOPE[1]}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {(CHAR, SCOPE[1])}
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
    assert verified == 8434
    svg = (S / "batch-092-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-092-draft-stroke-audit.json", dict(
        load(S / "batch-092-stroke-evidence.json"), converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / "strokes" / f"{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-092-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    save(S / "batch-092-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "092", "completeArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE},
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "Complete new card and actual complete reused support. Cmap presence/absence not native legibility/fallback-face acceptance; fresh four-font/all-Han and non-skipped RareHan/native gates pending.",
    })
    neighbor = metadata(R, "kanji/切.md")
    assert len(neighbor["distractors"]) == 3 and CHAR not in neighbor["distractors"]
    explicit = sorted(p.stem for p in (R / "kanji").glob("*.md")
                      if p.stem != CHAR and CHAR in metadata(R, f"kanji/{p.name}").get("distractors", []))
    assert explicit == []
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in ["乃", "凹", "凸"])
    for inbound in ["剃る", "取り入れる"]:
        assert CHAR + "る" in metadata(R, f"words/{inbound}.md")["quiz_exclusions"]
    result.update(
        schemaVersion=1, execution=659, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=5, decompressedDictionaryHashesVerified=2, packets=packets,
        compactFullFamilyTextSemanticallyEqualToRawXml=True,
        completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=1, directedLinksVerified=2, newDirectWordExclusionPairs=1,
        legacyDefaultFallbackNeighbor={"切": neighbor["distractors"]},
        existingExplicitTargetDistractors=explicit, allRuntimePayloadHashesVerified=verified,
        actualHanCount=len(han), pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=118,
        remainingAdditions=1110, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-092-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-092-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-659.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8434" in text and result["contentVersion"] in text
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
        target = S / f"batch-092-draft-{stem}-659.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    recipe = S / "batch-092-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-659.json", {
        "schemaVersion": 1, "execution": 659, "batch": "092", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution659StartingState"],
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "vocabularyCommand": "python -X utf8 -B tools/grammar_vocabulary.py check",
        "vocabularyLimits": "Existing pilot coverage2122/2431 reviewed prompts; consistency passed, not complete unrelated grammar coverage.",
        "audit": "docs/n1-sources/batch-092-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-092-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-092-draft-stroke-audit.json",
        "recipe": recipe.relative_to(R).as_posix(), "recipeSha256": sha(recipe.read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock throughout child lifetime; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helpers in control. No optional historical-session-helper access.",
        "readEvidenceLimits": load(S / "batch-092-progress.json")["draftAuthorInspection"],
        "draftAuditDiagnostic": "First audit stopped at a helper text comparison because read_text normalized CRLF in the compact dictionary file while the archived bytes retained CRLF. Changed comparison to exact raw bytes, then semantic XML equality; all75 complete frozen families and six character records passed. No source bytes altered, permission denial or acceptance waiver.",
        "actualNewPermissionDenials": [], "publishedAdditions": 118, "remainingAdditions": 1110,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft check receipts and durable recipe archived.")


def freeze():
    signed = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD and not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == BASE
    expected = {
        SCOPE[0], SCOPE[1], f"strokes/{CHAR}.json", "manifest.json",
        "docs/n1-sources/batch-092-membership.json", "docs/n1-sources/batch-092-progress.json",
        "docs/n1-sources/batch-092-draft-audit.json", "docs/n1-sources/batch-092-draft-font-audit.json",
        "docs/n1-sources/batch-092-draft-stroke-audit.json", "docs/n1-sources/batch-092-draft-recipe.py",
        "docs/n1-sources/execution-659.json",
    } | {f"docs/n1-sources/batch-092-draft-{n}-659.txt.gz"
         for n in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]}
    changed = set(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", signed],
        encoding="utf-8").rstrip("\0").split("\0"))
    assert changed == expected, changed ^ expected
    from build_manifest import build_manifest
    assert build_manifest(R) == load(R / "manifest.json")
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    evidence = load(S / "execution-659.json")
    body = (
        f"Batch092 — signed LOCAL UNREVIEWED draft checkpoint659, not publication.\n\n"
        f"Saved `{signed}` (normal signature G), parent source `{HEAD}`; remote main remains "
        f"`{BASE}`. New 刈 card and four generated pinned KanjiVG paths; no new support word. "
        "Existing N3 刈る changes only its activated component link and direct 収穫 quiz safeguard; "
        "identity, primary reading, title, easier level and original 切る exclusion preserved.\n\n"
        "Full ガイ/カイ/か.る source order retained; explicit []/[か.る] offers only かる. "
        "Both 刈除 readings remain recognized unselected examples, not invented source-only/obsolete uses. "
        "One all-mapped/baseline pair, two link directions; three semantically wrong N1 labels. "
        "Complete75 frozen dictionary families/six character records, baseline metadata/strokes, exact "
        "runtime delta and all8434 current payload hashes audited. Final complete card/support Han "
        "inventory16; visible刂 is absent from three bundled cmaps, so fresh native fallback/rendered "
        "review remains required. Cmaps are not legibility evidence.\n\n"
        f"Validator0; regenerated manifest `{evidence['contentVersion']}`; "
        f"{evidence['pythonTestsPassed']} focused source/audit tests passed. Vocabulary consistency "
        "passed at existing pilot2122/2431 reviewed prompts, not completed unrelated grammar coverage. "
        f"Local archive {evidence['localBudget']['entries']} entries, "
        f"{evidence['localBudget']['localZipBytes']} compressed / "
        f"{evidence['localBudget']['inflatedBytes']} inflated / "
        f"{evidence['localBudget']['retainedBytes']} retained bytes; unchanged budgets pass. "
        "Evidence/recipe/receipts: docs/n1-sources/execution-659.json and batch-092-draft-*.\n\n"
        "No reviewer, Android/native run, content push or093 started. Next: same frozen draft's "
        "two serial blind different-model-family initial reviews, then reconciliation and every "
        "original Android/native/rendered/integration/publication gate. Published118/1228, "
        "acceptance-remainder1110 unchanged. Compatible curated-reading Androidf9b59a2+ required; "
        "qualifiedTESTONLY Android1c1b7bf4 is not latest appmain. Physical-phone/general-release/"
        "whole-set acceptance remains outstanding.\n\n"
        "Approved workspace/committed evidence/frozen sources only, durable helper in control; "
        "optional historical-session paths not accessed. Live parent19008 retains runner.lock "
        "untouched. No new permission denial. Helper CRLF comparison diagnostic preserved; "
        "exact raw-byte and semantic dictionary checks subsequently passed. This is a recoverable "
        "draft checkpoint, not batch review closure or project completion.\n"
    )
    (C / "batch-092-draft-659-issue.txt").write_bytes(body.encode("utf-8"))
    save(C / "batch-092-draft-659-freeze.json", {
        "commit": signed, "sourceCommit": HEAD, "signature": "G", "whollyClean": True,
        "exactChangedPaths": sorted(changed), "issueBodySha256": sha(body.encode("utf-8")),
        "runtimePublished": False, "parentLockTouched": False,
    })
    print(signed)


def seal():
    signed = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD and not git("status", "--porcelain")
    assert signed == load(C / "batch-092-draft-659-freeze.json")["commit"]
    assert git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    receipt = load(C / "batch-092-draft-659-issue-receipt.json")
    posted = load(L / "issue-659-reread.json")
    expected_body = (C / "batch-092-draft-659-issue.txt").read_bytes().decode("utf-8")
    assert posted["body"] == expected_body and posted["user"]["login"] == "stop-cran"
    assert receipt["verified"] and receipt["author"] == "stop-cran"
    assert receipt["bodySha256"] == sha(posted["body"].encode("utf-8"))
    evidence = load(S / "execution-659.json")
    audit_result = load(S / "batch-092-draft-audit.json")
    state = {
        "schemaVersion": 1, "execution": 659, "checkpoint": 659, "batch": "092",
        "status": "continue", "stage": "local-unreviewed-draft", "savedCommit": signed,
        "signature": "G", "sourceCommit": HEAD, "lastPublishedCommit": BASE,
        "evidence": "docs/n1-sources/execution-659.json",
        "sourcePacket": "docs/n1-sources/batch-092-progress.json",
        "audit": "docs/n1-sources/batch-092-draft-audit.json",
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "completeDictionaryFamilies": 75, "completeRawCharacterRecords": 6,
        "metadataReadings": 3, "newSupportArticles": 0, "reusedSupportArticles": 1,
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2,
        "activatedBaselinePairs": 1, "newDirectWordExclusionPairs": 1,
        "generatedStrokePaths": 4, "actualHanCount": audit_result["actualHanCount"],
        "pendingNativeFallbackLabels": audit_result["pendingNativeFallbackLabels"],
        "contentVersion": audit_result["contentVersion"],
        "allRuntimePayloadHashesVerified": audit_result["allRuntimePayloadHashesVerified"],
        "pythonTestsPassed": evidence["pythonTestsPassed"], "validatorErrors": 0,
        "localBudget": evidence["localBudget"], "publishedAdditions": 118,
        "remainingAdditions": 1110, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "ownerIssueAuthorAndBodyVerified": True, "issueUpdate": receipt["url"],
        "nextAction": NEXT,
    }
    before = load(L / "progress-before-659.json")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (658, "092", "continue")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    for k, v in before.items():
        if k not in mutable:
            assert p[k] == v, k
    state["originalHistoricalRootKeysCompared"] = len(before)
    state["allOriginalHistoricalValuesPreserved"] = True
    p["execution659CoordinatorCheckpoint"] = state
    p["batch092DraftCheckpoint"] = state
    p["batch092DraftIssueReceipt"] = receipt
    p.update(checkpoint=659, status="continue", stage="batch-092-local-unreviewed-draft",
             nextAction=NEXT, blocker=None)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    for k, v in before.items():
        if k not in mutable:
            assert persisted[k] == v, k
    save(L / "checkpoint-659.json", state)
    print(json.dumps(state, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["start", "prepare", "audit", "record", "freeze", "seal"])
    globals()[parser.parse_args().phase]()
