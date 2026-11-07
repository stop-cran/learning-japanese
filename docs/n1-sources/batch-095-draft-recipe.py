"""Freeze one source-bounded local UNREVIEWED draft; never publish runtime."""
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
L = C / "logs" / "31b58347-206a-4c4a-b32e-2671ae2748a9"
S = R / "docs" / "n1-sources"
HEAD = "9b4fd365e8af44ab9aa976676d1f0d3ec311cbef"
BASE = "d6a261903f269d6223afc067815b02c595da41a3"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u5256"
SCOPE = ["kanji/剖.md", "words/解剖.md", "kanji/解.md"]
NEXT = (
    "SAME095 two serial blind different-model-family initial textual reviews on the "
    "normally signed LOCAL UNREVIEWED draft: complete剖/解剖 and exact navigation-only解 "
    "diff; same frozen full dictionary/character/public evidence. Cover correctness, "
    "scoped coverage and phone comprehensibility; actual available models/read-only "
    "tools, actual process exit before next reviewer, complete original reports/sessions/"
    "read limits, evidence-based reconciliation and bounded original-session confirmations. "
    "Preserve sole fullボウ/empty kun, selectedボウ and new解剖かいぼう without inferred word "
    "jlpt; three direct分析/分解/検査 guards are not unrestricted substitution claims. "
    "Then fresh non-skipped Android, production ContentSync ONCE/native N1/All choices/"
    "reading/drawing/article/Back/offline/four-font/all-Han/rendered review; actual "
    "combined-main/normal signing/owner fast-forward/terminal CI/EVERY immutable ZIP "
    "runtime hash/unchanged budgets/verified owner issue gates. No096 or unreviewed push. "
    "Approved control/committed evidence/frozen inputs only; parent19008 retains runner.lock, "
    "no child acquire/delete/unlock. Preserve/report/yield actual new denial/signing hang/"
    "uncertain ownership. Published121/1228,1107 acceptance remainder unchanged; "
    "physical-phone/general-release/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".690.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (689, "095", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    before = L / "progress-before-690.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["checkpoint"] == 689
    assert checkpoint["execution689CoordinatorCheckpoint"] == p["execution689CoordinatorCheckpoint"]
    role = load(L / "preflight-690.json")
    assert role["liveParentPid"] == 19008 and role["sessionId"] == L.name and not role["lockTouched"]
    p["execution690StartingState"] = {
        "execution": 690, "batch": "095", "startingHead": HEAD, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME095 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,096 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete issue and final689 directly inspected; historical middle parsed, not freshly semantically re-reviewed. Initial scalar output encountered cp1252 after successful parse; UTF-8 bounded output succeeded."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs and durable control helpers only; optional historical-session recipes not accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals published BASE. Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain; canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-095-runtime-draft-in-progress",
             nextAction=p["execution690StartingState"]["scope"], blocker=None)
    save(C / "progress.json", p)
    print("SAME095 draft scope persisted; complete historical values preserved.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    proof = load(S / "batch-095-stroke-evidence.json")
    svg = (S / "batch-095-kanjivg.svg").read_bytes()
    assert sha(svg) == proof["sha256"] and svg == Path(proof["input"]).read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 10
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-095-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [106]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR])
    frozen["limits"] = "LOCAL UNREVIEWED draft only, not review closure, native acceptance or publication."
    save(S / "batch-095-membership.json", frozen)
    p = load(S / "batch-095-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR])
    p["dictionaryPackets"] = [
        {"selection": "batch-095-lexical-selection.json", "xml": "batch-095-jmdict.xml"},
        {"selection": "batch-095-comparison-selection.json", "xml": "batch-095-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], article="words/解剖.md",
                   reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": True, "allWrittenKanji": row["allWrittenKanji"],
         "wordJlpt": None, "selectedSenses": row["selectedSenses"], "status": "local-unreviewed-draft"}
        for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = [[CHAR, "words/解剖.md"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = p["proposedReusedChanges"]
    p["curatedProjection"] = [p["proposedCuratedProjection"]]
    p["quizAudit"] = {CHAR: {
        "title": p["proposedQuiz"]["kanjiTitle"], "distractors": p["proposedQuiz"]["distractors"],
        "labels": p["proposedQuiz"]["labels"], "meaningDecisions": p["proposedQuiz"]["rationale"],
        "unsafeComparisons": p["proposedQuiz"]["unsafeComparisons"],
        "limits": "Default-four fallback unnecessary; independent semantic and production N1/All review pending.",
    }}
    p["wordQuizAudit"] = {
        "directExclusions": [{"word": "解剖", "exclude": ["分析", "分解", "検査"],
                              "reasons": p["proposedQuiz"]["proposedDirectExclusions"]}],
        "limits": "Direct pairs only; broad examination guard does not assert unrestricted Japanese interchangeability. Not full live-pool certification.",
    }
    p["draftAuthorInspection"] = {
        "execution": 690, "sourceCheckpoint": HEAD,
        "completeMemberFamilies": {"path": "control/batch-095-full-family-reading.txt", "returnedRanges": [[1, 16]], "families": 16},
        "completeComparisonFamilies": {"path": "control/batch-095-comparison-reading.txt", "returnedRanges": [[1, 11], [12, 21]], "families": 21},
        "rawCharacterScope": "Complete new member record freshly read; six comparison character records inherited source689 inspection, freshly frozen-byte-bound, not freshly fully semantically read.",
        "completeExistingArticlesRead": ["kanji/解.md", "kanji/部.md", "kanji/倍.md", "kanji/副.md", "words/分析.md", "words/分解.md", "words/検査.md"],
        "publicLookup": "Complete committed character/解剖 article extractions freshly read. Archived coordinator evidence, not fresh upstream retrieval. No gaiji-based historical claim.",
        "pinnedSvg": "Complete committed SVG freshly read; ten paths and right-hand刂/original刀 annotation. SVG phon attribute not historical proof.",
        "navigationDiagnostic": "One guessed optional control compact filename did not exist; actual committed recipe path batch-095-comparison-reading.txt was read in full. No permission denial, outside-workspace access or missing required source evidence.",
        "limits": "Author inspection only, not independent review, native-speaker certification, phone evidence or uniform reviewer comprehension.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft; no reviewer, fresh Android/native/font/phone acceptance or runtime publication.",
        "Full soleボウ and empty kunyomi retained; explicitボウ/[] selection. Supplementalホウ/native historical annotations not appended to pinned metadata.",
        "One necessary解剖 article without inferred vocabulary level; existing解 receives only one navigation line, preserving all metadata/teaching.",
        "Two all-mapped pairs/four directions, including existing解; zero activated baseline pairs. Three direct word guards, no transitive exclusion assumptions.",
        "Labelled modern-shape mnemonic only, structure-unclassified, no phonetic claim. Canonical刀18 retained, visible刂 explained; ten pinned paths generated.",
        "Final Han/cmap audit is not native glyph/fallback acceptance. Fresh non-skipped Android/native/four-font/all-Han/rendered review pending.",
        "Published121/1228 and1107 acceptance remainder unchanged. Six earlier-level source保案派第策結 remain separate;妖exception preserved.",
        "CompatibleAndroidf9b59a2+ required; qualified TESTONLY1c1b7bf4 not latest appmain. Physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates retained; no096 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-095-progress.json", p)
    print("Ten pinned paths and local UNREVIEWED ledgers prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "095")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    ledger = load(S / "batch-095-progress.json")
    packets = []
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt" if i == 0 else "comparison-full-family-reading.txt"
        compact = gzip.decompress((S / f"batch-095-{suffix}.gz").read_bytes())
        exposed = C / ("batch-095-full-family-reading.txt" if i == 0 else "batch-095-comparison-reading.txt")
        assert compact == exposed.read_bytes()
        assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact.decode("utf-8") + "</JMdict>")] == [
            canonical(e) for e in ET.fromstring(raw)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True, "completeCompactSemanticEquality": True})
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-095-kanjidic2.xml", "batch-095-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(records[entry.findtext("literal")])
            count += 1
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"],
                  "words/刈る.md": ["切る", "収穫"],
                  "words/刑事.md": ["警官", "警察", "巡査", "おまわりさん"],
                  "words/削る.md": ["切る", "減らす", "省く", "消す", "除く", "外す", "縮める"],
                  "words/削除.md": ["消す", "除く", "外す", "取る", "削る", "省く"]}
    prior = load(S / "batch-094-publication.json")
    assert prior["status"] == "published-verified-bounded-owner-testing"
    for name in ["words/削る.md", "words/削除.md"]:
        prior_text = git("show", f"{BASE}:{name}")
        assert yaml.safe_load(prior_text.split("---", 2)[1])["quiz_exclusions"] == exceptions[name]
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
    assert named == load(S / "community-list-20261102.json") and named[105] == CHAR
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    old_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in old_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {CHAR} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    for c in "保案派第策結":
        assert metadata(R, f"kanji/{c}.md")["jlpt"] == 2
    assert "jlpt" not in metadata(R, "words/解剖.md")
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/解剖.md"}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {
        ("剖", "words/解剖.md"), ("解", "words/解剖.md")}
    for c, name in all_pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    assert metadata(R, "words/解剖.md")["quiz_exclusions"] == ["分析", "分解", "検査"]
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
    assert verified == 8441
    svg = (S / "batch-095-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-095-draft-stroke-audit.json", dict(
        load(S / "batch-095-stroke-evidence.json"), converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / "strokes" / f"{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-095-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    save(S / "batch-095-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "095", "completeArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE}, "fonts": fonts,
        "rareHanRangeCharacters": [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF
            or 0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF],
        "nativeFontAcceptance": "pending", "limits": "Cmap evidence only, not glyph/fallback-face acceptance; fresh four-font/all-Han/native gates pending.",
    })
    for c in "分解刀部倍副":
        assert len(metadata(R, f"kanji/{c}.md")["distractors"]) == 3
    result.update(
        schemaVersion=1, execution=690, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        latestBaselineExceptionEvidence="docs/n1-sources/batch-094-publication.json; docs/n1-reviews/batch-094-correction-reconciliation-686.json; exact signed BASE metadata",
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=2, directedLinksVerified=4, newDirectWordExclusionPairs=3,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=121,
        remainingAdditions=1107, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-095-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-095-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-690.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8441" in text and result["contentVersion"] in text
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
        target = S / f"batch-095-draft-{stem}-690.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    for source, target in [
        (Path(__file__), S / "batch-095-draft-recipe.py"),
        (C / "preflight-690.ps1", S / "batch-095-draft-preflight-690.ps1.txt"),
        (C / "checks-batch-095-draft-690.ps1", S / "batch-095-draft-checks-690.ps1.txt"),
    ]:
        target.write_bytes(source.read_bytes())
    save(S / "execution-690.json", {
        "schemaVersion": 1, "execution": 690, "batch": "095", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution690StartingState"],
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "vocabularyLimits": "Existing reviewed-prompt consistency only, not unrelated coverage completion.",
        "audit": "docs/n1-sources/batch-095-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-095-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-095-draft-stroke-audit.json",
        "recipe": "docs/n1-sources/batch-095-draft-recipe.py", "recipeSha256": sha(Path(__file__).read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helpers in control.",
        "readEvidenceLimits": load(S / "batch-095-progress.json")["draftAuthorInspection"],
        "actualNewPermissionDenials": [], "publishedAdditions": 121, "remainingAdditions": 1107,
        "auditDiagnostic": {
            "initialFailure": "Draft recipe inherited the previous pre094 exception list; original audit correctly stopped at words/削る.md before tests. Original failure retained in execution log.",
            "resolution": "Explicitly added only the two already published/reviewed094 additive exclusion lists, verified against signed BASE and publication/correction evidence. No runtime change or weakened baseline comparison.",
            "originalLog": str(L / "audit-690-original-baseline-exceptions-failure.txt"),
        },
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
        "docs/n1-sources/batch-095-membership.json", "docs/n1-sources/batch-095-progress.json",
        "docs/n1-sources/batch-095-draft-audit.json", "docs/n1-sources/batch-095-draft-font-audit.json",
        "docs/n1-sources/batch-095-draft-stroke-audit.json", "docs/n1-sources/batch-095-draft-recipe.py",
        "docs/n1-sources/batch-095-draft-preflight-690.ps1.txt",
        "docs/n1-sources/batch-095-draft-checks-690.ps1.txt", "docs/n1-sources/execution-690.json",
    } | {f"docs/n1-sources/batch-095-draft-{n}-690.txt.gz"
         for n in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]}
    changed = set(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", signed],
        encoding="utf-8").rstrip("\0").split("\0"))
    assert changed == expected, changed ^ expected
    from build_manifest import build_manifest
    assert build_manifest(R) == load(R / "manifest.json")
    result = load(S / "batch-095-draft-audit.json")
    evidence = load(S / "execution-690.json")
    before = load(L / "progress-before-690.json")
    p = load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 690, "checkpoint": 690, "batch": "095",
        "status": "continue", "stage": "local-unreviewed-draft", "savedCommit": signed,
        "signature": "G", "sourceCommit": HEAD, "lastPublishedCommit": BASE,
        "membership": [CHAR], "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "runtimePublished": False, "dedicatedWorktreesClean": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 121, "remainingAdditions": 1107,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "validatorErrors": 0,
        "contentVersion": result["contentVersion"], "allRuntimePayloadHashesVerified": 8441,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 0,
        "metadataReadingDispositions": 1, "curatedOfferedKeys": 1, "newSupportArticles": 1,
        "changedReusedArticles": 1, "newDirectWordExclusionPairs": 3,
        "actualHanCount": result["actualHanCount"], "pendingNativeFallbackLabels": result["pendingNativeFallbackLabels"],
        "sourcePacket": "docs/n1-sources/batch-095-progress.json",
        "audit": "docs/n1-sources/batch-095-draft-audit.json", "evidence": "docs/n1-sources/execution-690.json",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [], "nextAction": NEXT,
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
    }
    p["execution690StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution690CoordinatorCheckpoint"] = checkpoint
    p["batch095LocalUnreviewedDraft"] = copy.deepcopy(checkpoint)
    p.update(checkpoint=690, status="continue", stage="batch-095-local-unreviewed-draft",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    save(L / "checkpoint-690.json", checkpoint)
    body = (
        f"Batch095: signed LOCAL UNREVIEWED draft checkpoint690, not publication.\n\n"
        f"Saved `{signed}` (normal signature G), source `{HEAD}`; remote main remains `{BASE}`. "
        "New 剖 card, necessary 解剖かいぼう article without inferred vocabulary level, "
        "and ten generated pinned KanjiVG strokes. Existing N3解 gains only one reciprocal "
        "navigation line; original metadata/readings/levels/exclusions retained. Sole fullボウ "
        "and empty kun preserved; explicitボウ/[] yieldsぼう only. Two all-mapped pairs/four "
        "directions include existing解. Three direct guards against分析/分解/検査 reflect "
        "analysis/broad English examination overlap, not unrestricted Japanese substitution.\n\n"
        f"Evidence: `docs/n1-sources/execution-690.json` and draft audit/font/stroke records. "
        "Frozen37 complete dictionary families/seven character records freshly byte-bound; "
        "baseline metadata/strokes and all8441 runtime payload hashes audited. "
        f"Final complete article Han inventory{result['actualHanCount']}; main-font cmap absences "
        f"{''.join(result['pendingNativeFallbackLabels'])}, not native glyph acceptance.\n\n"
        "All independent textual review/reconciliation, fresh non-skipped Android/native/"
        "four-font/all-Han/rendered and combined-main/CI/every immutable ZIP hash gates remain. "
        "No reviewer, Android/native run, runtime push or096 in this checkpoint. "
        "Published121/1228;1107 acceptance remainder unchanged. Compatible curated-reading APK "
        "required; physical-phone/general-release/whole-set acceptance outstanding. "
        "Approved workspace/control artifacts only; live parent's runner.lock untouched.\n"
    )
    (C / "batch-095-draft-690-issue.txt").write_bytes(body.encode("utf-8"))
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))


def issue():
    posted = load(L / "issue-690-posted.json")
    actual = load(L / "issue-690-reread.json")
    raw = (C / "batch-095-draft-690-issue.txt").read_bytes()
    assert posted["id"] == actual["id"] and actual["user"]["login"] == "stop-cran"
    assert actual["body"].encode("utf-8") == raw
    receipt = {"id": actual["id"], "url": actual["html_url"], "author": "stop-cran",
               "bodySha256": sha(raw), "verified": True, "comparison": "Exact UTF-8 bytes."}
    p = load(C / "progress.json")
    before = load(L / "progress-before-690.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (690, "095", "continue")
    assert git("rev-parse", "HEAD") == p["execution690CoordinatorCheckpoint"]["savedCommit"]
    for root in (R, A):
        assert not git("status", "--porcelain", root=root)
        assert git("log", "-1", "--format=%G?", root=root) == "G"
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    for key in ["execution690CoordinatorCheckpoint", "batch095LocalUnreviewedDraft"]:
        p[key]["issueUpdate"] = receipt["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    p["batch095DraftIssueReceipt"] = receipt
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    save(L / "checkpoint-690.json", p["execution690CoordinatorCheckpoint"])
    save(C / "batch-095-draft-690-issue-receipt.json", receipt)
    print("Owner issue bytes, signed clean heads and complete historical values verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=["start", "prepare", "audit", "record", "freeze", "issue"])
    globals()[parser.parse_args().step]()
