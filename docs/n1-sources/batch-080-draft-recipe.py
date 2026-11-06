"""Persist and audit the bounded, unreviewed batch 080 runtime draft."""
import ast
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

CONTROL = Path(r"C:\Users\stop-\n1-kanji-workspace\control")
ROOT = CONTROL.parent / "learning-japanese"
LOG = CONTROL / "logs" / "c7d55cd7-345c-4608-9f06-9d38573272ae"
OUT = ROOT / "docs" / "n1-sources"
SOURCE = "d5063dbecad8f15cbc58a200477b394f99841f0f"
BASE = "b120125ae5cdbfe9f3bcb1b0a7ae8a61e422ec8d"
SCOPE = ["kanji/冴.md", "words/冴える.md"]
sys.path.insert(0, str(ROOT / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", *args], cwd=ROOT, encoding="utf-8").strip()


def start():
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == 537 and progress["batch"] == "080"
    assert progress["lastPublishedCommit"] == BASE
    assert git("rev-parse", "HEAD") == SOURCE and git("rev-parse", "origin/main") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    backup = LOG / "execution-538-start-progress.json"
    assert not backup.exists()
    save(backup, progress)
    raw = (LOG / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 537
    progress["execution538StartingState"] = {
        "execution": 538, "batch": "080", "startingHead": SOURCE, "freshOriginMain": BASE,
        "scope": "SAME080 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,081 or second runner.",
        "status": "runtime-draft-in-progress",
        "authorization": {
            "requestSha256": digest(raw), "bytes": len(raw), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded and final checkpoint parsed; operative contract, final537 and complete approved issue inspected directly. Historical middle parsed, not freshly semantically re-reviewed.",
        },
        "artifactPathPreflight": {
            "guide": str(CONTROL / "authoring-artifact-path-notes.txt"),
            "durableHelper": str(Path(__file__)), "optionalHistoricalHelpersAccessed": False,
            "actualNewPermissionDenials": [],
        },
        "worktrees": "Dedicated content and Android clean with signed G heads d5063dbe/f9b59a2; fresh main b120125a. Canonical repositories not accessed.",
        "startedAt": datetime.now().astimezone().isoformat(),
    }
    progress.update(status="continue", stage="batch-080-runtime-draft-in-progress", blocker=None,
                    nextAction="SAME080 bounded runtime draft, checks and normal signed LOCAL UNREVIEWED freeze; yield before later gates.")
    save(CONTROL / "progress.json", progress)
    print("Starting scope persisted; full live history preserved.")


def strokes():
    from generate_strokes import convert
    record = load(OUT / "batch-080-stroke-evidence.json")
    svg = Path(record["input"]).read_bytes()
    assert digest(svg) == record["sha256"]
    assert digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == record["converterNormalizedSha256"]
    data = convert("冴", svg.decode("utf-8"))
    assert data["strokeCount"] == len(data["strokes"]) == 7
    assert data["sourceRevision"] == record["revision"]
    path = ROOT / "strokes" / "冴.json"
    assert not path.exists()
    path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print("Seven strokes generated with unchanged pinned converter.")


def ledger():
    data = load(OUT / "batch-080-progress.json")
    assert data["status"] == "source-prepared-not-drafted"
    data.update(status="local-unreviewed-draft", drafted=["冴"])
    for row in data["readingDispositions"]:
        row["kanji"] = "冴"
        row["selected"] = row["proposedQuizSelection"]
    mappings = []
    for old in data["proposedSupportMapping"]:
        row = dict(old)
        row["entryIds"] = [row.pop("entryId")]
        row["newArticle"] = row.pop("newArticleNecessary")
        row["status"] = "local-unreviewed-draft"
        mappings.append(row)
    data["supportMappings"] = mappings
    data["requiredReciprocalPairs"] = data["proposedReciprocalPairs"]
    data["allMappedReciprocalPairs"] = data["proposedReciprocalPairs"]
    data["changedReusedPassages"] = []
    data["curatedProjection"] = [dict(data["proposedCuratedProjection"], kanji="冴")]
    quiz = data["proposedKanjiQuizAudit"]
    data["quizAudit"] = {"冴": {
        "title": quiz["title"], "distractors": [r["kanji"] for r in quiz["distractors"]],
        "labels": [r["title"] for r in quiz["distractors"]],
        "meaningDecisions": quiz["distractors"], "legacyFallbackDisposition": quiz["legacyFallback"],
    }}
    word_quiz = data["proposedWordQuizAudit"]
    data["wordQuizAudit"] = {
        "directExclusions": [{"word": "冴える", "exclude": word_quiz["directExclusions"],
                              "reason": word_quiz["reason"]}],
        "confusableInventory": word_quiz["inventory"], "limits": word_quiz["scopeLimits"],
    }
    data["draftAuthorInspection"] = {
        "execution": 538, "sourceCheckpoint": SOURCE,
        "freshCompletePacketRanges": {
            "batch-080-jmdict.xml": [[1, 210], [211, 402]],
            "batch-080-comparison-jmdict.xml": [[1, 220], [221, 441]],
            "batch-080-related-jmdict.xml": [[1, 180], [181, 353]],
            "batch-080-kanjidic2.xml": [[1, 271]],
        },
        "freshExistingArticles": [
            "words/澄む.md", "words/覚める.md", "words/冷える.md", "words/凍る.md",
            "words/光る.md", "words/輝く.md", "words/鋭い.md", "words/透き通る.md",
            "words/明るい.md", "words/すっきり.md", "words/上手.md", "words/上手い.md",
            "words/器用.md", "words/優れる.md", "words/凍える.md", "words/寒い.md",
            "kanji/次.md", "kanji/汗.md", "kanji/河.md",
        ],
        "freshPublicSources": [
            {"url": "https://kotobank.jp/word/%E5%86%B4%E3%81%88%E3%82%8B-508792",
             "range": [0, 9000], "heading": "さ・える【×冴える／×冱える】",
             "scope": "All seven Daijisen senses/examples; later synonym tail truncated and not used as full inspection."},
            {"url": "https://kotobank.jp/word/%E5%86%B4-2786520", "range": [0, 6000],
             "scope": "Complete short 字通 character entry; image-based historical derivation not adopted."},
        ],
        "examples": [
            {"draft": "今日は頭が冴えています。", "source": "今日は頭が冴えている",
             "operation": "Only polite-ending adaptation; mental clear-headedness, not permanent intelligence."},
            {"draft": "目が冴えて眠れません。", "source": "目が冴えて眠れない",
             "operation": "Only polite negative-ending adaptation; wakefulness prevents sleep, not eye brightness."},
        ],
        "limits": "Coordinator reads, not independent review or native-speaker/corpus certification. Prior source records and their lookup/read limits remain.",
    }
    data["runtimeDraftEvidence"] = "batch-080-draft-audit.json"
    data["fontDisposition"] = "Every actual Han in both new articles inventoried in batch-080-draft-font-audit.json; native fallback/phone acceptance pending."
    data["nextAction"] = "Two serial blind different-family textual initial reviews on the same normally signed local080 draft; then evidence-based reconciliation. No081 or unreviewed publication."
    data["limits"] = (
        "LOCAL UNREVIEWED runtime draft only. No independent reviewer, fresh Android/native/font/phone acceptance, "
        "review closure, runtime publication or081. Every original source/reviewer/process/denial/OOM/read-depth "
        "limitation, baseline exception and unchanged archive guard remains. Compatible Android f9b59a2+ "
        "required; physical-phone/general-release/whole-set acceptance outstanding. Overall project incomplete.")
    save(OUT / "batch-080-progress.json", data)
    print("Draft ledger generated; original source proposals retained.")


def audit():
    from audit_n1_batch import audit as batch_audit, lexical_pair
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    result = batch_audit(ROOT, "080")
    data = load(OUT / "batch-080-progress.json")
    assert data["status"] == "local-unreviewed-draft"
    assert data["reviewClosed"] == data["published"] == []
    snapshot = load(ROOT / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (CONTROL / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and digest(raw) == info["sha256"], name
    raw = (CONTROL / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    families, packets = {}, []
    for packet in data["dictionaryPackets"]:
        selected = load(OUT / packet["selection"])
        path = OUT / packet["xml"]
        expected = extract(raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], selected["entryIds"])
        assert expected == path.read_bytes()
        entries = ET.fromstring(expected).findall("entry")
        families.update((e.findtext("ent_seq"), e) for e in entries)
        packets.append({"path": path.name, "families": len(entries), "sha256": digest(expected),
                        "freshExtractionMatches": True})
    assert len(families) == 35
    assert lexical_pair(families["1297050"], "冴える", "さえる")
    assert families["1877830"].findtext("sense/misc") == "rare term"
    assert "jlpt" not in metadata(ROOT, "words/冴える.md")
    pairs = {(c, m["article"]) for m in data["supportMappings"]
             for c in metadata(ROOT, m["article"])["kanji"]
             if (ROOT / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(p) for p in data["allMappedReciprocalPairs"]} == {("冴", "words/冴える.md")}
    declared = {f"words/{p.name}" for p in (ROOT / "words").glob("*.md")
                if "冴" in metadata(ROOT, f"words/{p.name}")["kanji"]}
    assert declared == {"words/冴える.md"}
    baseline = load(OUT / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = ["川", "出", "木"]
            assert metadata(ROOT, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert digest((ROOT / name).read_bytes()) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(CONTROL / "inputs" / "n1-kanji-source-20261102.json")
    assert named[88] == "冴"
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in OUT.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {p.stem for p in (ROOT / "kanji").glob("*.md")}
    assert len(published) == 106 and current - old == published | {"冴"}
    assert len(current) == 1092 and len(current & set(named)) == 111
    assert metadata(ROOT, "kanji/妖.md")["jlpt"] == 1
    assert sum(metadata(ROOT, f"kanji/{p.name}")["jlpt"] == 1 for p in (ROOT / "kanji").glob("*.md")) == 112
    assert len(list((ROOT / "words").glob("*.md"))) == 5048
    manifest = build_manifest(ROOT)
    assert manifest == load(ROOT / "manifest.json")
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = digest((ROOT / name).read_bytes()) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(ROOT / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8366
    source = load(OUT / "batch-080-stroke-evidence.json")
    svg = Path(source["input"]).read_bytes()
    assert digest(svg) == source["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == source["gitBlob"]
    assert digest((ROOT / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == source["converterNormalizedSha256"]
    assert load(ROOT / "strokes" / "冴.json") == convert("冴", svg.decode("utf-8"))
    save(OUT / "batch-080-draft-stroke-audit.json", dict(
        source, converted=True, output="strokes/冴.json",
        outputSha256=digest((ROOT / "strokes" / "冴.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False,
        limits="Exact pinned converter output; not native drawing, recognition, handwriting or recall acceptance."))
    text = "".join((ROOT / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(OUT / "batch-080-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert digest(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    save(OUT / "batch-080-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "080", "completeRuntimeScope": SCOPE,
        "articleHashes": {n: digest((ROOT / n).read_bytes()) for n in SCOPE},
        "actualHanCount": len(han), "actualHan": han, "fonts": fonts,
        "rareHanRangeCharacters": rare,
        "limits": "Complete actual draft inventory and unchanged bundled cmaps; absence is not glyph failure. Every actual Han needs later assigned native/font/viewport acceptance. No phone claim.",
    })
    result.update({
        "schemaVersion": 1, "execution": 538, "stage": "local-unreviewed-draft",
        "sourceCheckpoint": SOURCE, "packets": packets, "frozenInputHashesVerified": 5,
        "allMappedReciprocalPairs": len(pairs), "directedLinksVerified": len(pairs) * 2,
        "originalBaselineMetadataAndStrokesPreserved": counts, "baselineMetadataExceptions": exceptions,
        "baselineKanjiDistractorException": {"kanji/山.md": ["川", "出", "木"]},
        "allRuntimePayloadHashesVerified": checked, "publishedAdditions": 106,
        "draftOnlyAdditions": ["冴"], "remainingAdditions": 1122,
        "currentCounts": {"kanji": 1092, "words": 5048, "n1Labels": 112, "namedSourceMembersPresent": 111},
        "actualHanCount": len(han), "pendingNativeFallbackLabels": fonts[0]["allActualMissing"],
        "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "limits": data["limits"],
    })
    save(OUT / "batch-080-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(OUT / "batch-080-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "draft-tests", "budget"]:
        path = LOG / f"{stem}-538.txt"
        text = path.read_text(encoding="utf-8-sig")
        if stem == "validate":
            assert "0 error(s)" in text
        elif stem == "manifest":
            assert "8366" in text and result["contentVersion"] in text
        elif stem == "audit":
            assert json.loads(text) == result
        elif stem == "draft-tests":
            assert "Ran 34 tests" in text and "OK" in text and "FAILED" not in text and "skipped" not in text
        else:
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] == 8388
        receipts[stem] = {"path": str(path), "sha256": digest(path.read_bytes()), "completeOutput": text}
    recipe = OUT / "batch-080-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(OUT / "execution-538.json", {
        "schemaVersion": 1, "execution": 538, "batch": "080", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": SOURCE, "baseCommit": BASE,
        "startingState": load(CONTROL / "progress.json")["execution538StartingState"],
        "runtimeScope": SCOPE + ["strokes/冴.json", "manifest.json"],
        "sourcePacket": "batch-080-progress.json", "draftAudit": "batch-080-draft-audit.json",
        "strokeAudit": "batch-080-draft-stroke-audit.json", "fontAudit": "batch-080-draft-font-audit.json",
        "durableRecipe": {"controlPath": str(Path(__file__)), "archive": recipe.name,
                          "sha256": digest(recipe.read_bytes())},
        "checks": receipts, "archiveBudget": budget, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "runtimePublished": False,
        "reviewClosed": [], "published": [], "publishedAdditions": 106, "remainingAdditions": 1122,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": "Normally sign LOCAL UNREVIEWED080 freeze, record owner issue receipt and full checkpoint, then yield before two serial blind different-family textual initial reviews.",
        "limits": result["limits"],
    })
    print("Complete draft evidence and durable recipe archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    result = load(OUT / "batch-080-draft-audit.json")
    body = (
        f"Batch080 runtime draft frozen at normally signed LOCAL {head}; UNREVIEWED, not pushed or published. "
        "New 冴 and necessary 冴えるさえる support article, no inferred vocabulary level or reused edits. "
        "All five full readings remain in source order: ゴ/コ and さ.える/こお.る/ひ.える. "
        "Only さ.える has a selected linked practice row; explicit empty on subset. Rare 冴寒ごかん is "
        "recognition-only; unmatched readings remain qualified lookup information, not invented examples. "
        "Draft distinguishes mental alertness/vividness, wakefulness versus waking, contextual lacklustre "
        "negatives and the older coldness branch. Two core contexts adapt attested Daijisen examples only "
        "in polite endings. Three wrong meanings 次/汗/河 and 15 direct conservative word safeguards "
        "remain subject to independent review, not universal synonym claims.\n\n"
        f"Draft checks pass: validator, regenerated manifest {result['contentVersion']}, 34 focused audit "
        "regressions, original unchanged archive guards, all 8,366 runtime hashes, exact membership, "
        "baseline metadata/strokes with previously reviewed exceptions, and one mapped pair/two directions. "
        "Seven strokes exactly regenerated from the pinned SVG/converter. Complete 35 distinct dictionary "
        f"families and four raw records freshly inspected. All {result['actualHanCount']} actual Han checked "
        "against three unchanged bundled cmaps; native legibility/fallback/phone acceptance is still pending. "
        "Cmap absence is not a glyph failure. Public Daijisen synonym tail was truncated and not claimed fully read.\n\n"
        "Checkpoint538 yields before SAME080 two serial blind different-family textual initial reviews. "
        "No reviewers, fresh Android/native testing, review closure, publication or081. Helper is in approved "
        "control and archived with source evidence; optional historical helper paths not accessed, no new "
        "permission denial. Published106/1228, remaining1122 unchanged. Every original acceptance gate, "
        "archive guard and historical source/review/process/denial/OOM/read-depth limitation remains. "
        "Compatible Android f9b59a2+ required; physical-phone/general-release/whole-set acceptance outstanding.\n")
    (LOG / "issue-update-538.txt").write_text(body, encoding="utf-8")
    print(f"Owner issue body prepared for signed LOCAL UNREVIEWED {head}.")


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    response = load(LOG / "issue-response-538.json")
    body = (LOG / "issue-update-538.txt").read_text(encoding="utf-8")
    assert response["user"]["login"] == "stop-cran"
    assert response["body"].replace("\r\n", "\n").rstrip() == body.replace("\r\n", "\n").rstrip()
    original = load(LOG / "execution-538-start-progress.json")
    progress = load(CONTROL / "progress.json")
    assert progress["checkpoint"] == original["checkpoint"] == 537
    result = load(OUT / "batch-080-draft-audit.json")
    next_action = (
        f"SAME080 normally signed LOCAL UNREVIEWED draft {head}; not pushed/reviewed/published. NEXT fresh "
        "coordinator read entire request/final checkpoint/scoped live keys; preserve FULL history and verify "
        "clean signed dedicated heads/fresh main. Execute TWO serial blind different-family textual initial "
        "reviewers on this SAME frozen snapshot, actual help/catalog/model/process/read evidence; wait for "
        "first process exit, serial internal tools, no author agents/nested trees/concurrent heavy work/second "
        "runner. Scope new冴/necessary冴える plus complete applicable comparison bodies and actual15direct "
        "guards, allfivefull reading dispositions/order, explicitemptyon/さ.える ownlinkedrow, source-only "
        "コこお.るひ.える and rare冴寒ゴ, actual wrong次汗河 labels, intransitiveichidan/える boundary, "
        "wakefulnessvswaking/vividness/deftness/contextualnegative/oldcoldness and phone comprehensibility. "
        "35distinct completefamilies/fourrawrecords/freshboundedpublicheadings; truncatedDaijisentail not "
        "fullread. No wordlevel inference or reused changes; onepair/twodirections/noactivatedbaselinepair. "
        f"Pinnedsevenstrokes exactly regenerated;{result['actualHanCount']}actualHan/threecmaps checked; "
        f"nativefallback{result['pendingNativeFallbackLabels']}PENDING, notfailure.34focusedtests/validator/"
        "manifest/all8366hashes/baseline/exactmembership/localbudgets pass, not linguistic/native/phone "
        "acceptance. Required later original-session confirmations/Androidnonskips/native/font/currentmain/"
        "normalsigning/ownerfastforward/greenCI/EVERYimmutableZIPhash/originalguards unchanged. Approved "
        "workspace inputs/committedpackets/durablecontrolhelpers only; optional historical recipes skipped. "
        "Preserve/report/yield actualnewdenial; signinghang stop/yield withoutretry. No unreviewedpush or081. "
        "Published106/1228,remaining1122; physicalphone/generalrelease/whole-set outstanding. Preserve every "
        "original historical/source/reviewer/process/denial/OOM/read-depth limit and baseline exception.")
    progress["execution538StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    progress["execution538CoordinatorCheckpoint"] = {
        "schemaVersion": 1, "execution": 538, "checkpoint": 538, "batch": "080",
        "savedCommit": head, "signature": "G", "sourceCommit": SOURCE,
        "sourcePacket": "docs/n1-sources/batch-080-progress.json",
        "draftAudit": "docs/n1-sources/batch-080-draft-audit.json",
        "evidence": "docs/n1-sources/execution-538.json", "runtimeDrafted": ["冴"],
        "reviewClosed": [], "published": [], "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "focusedTestsPassed": 34, "runtimeHashesVerified": 8366,
        "contentVersion": result["contentVersion"], "actualHanCount": result["actualHanCount"],
        "pendingNativeFallbackLabels": result["pendingNativeFallbackLabels"],
        "publishedAdditions": 106, "remainingAdditions": 1122, "lastPublishedCommit": BASE,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [],
        "issueUpdate": response["html_url"], "ownerAuthorAndBodyVerified": True,
        "allOriginalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(original), "nextAction": next_action, "status": "continue",
    }
    progress.update(checkpoint=538, status="continue", stage="batch-080-local-unreviewed-draft",
                    nextAction=next_action, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[k] == v for k, v in original.items() if k not in allowed)
    save(CONTROL / "progress.json", progress)
    reread = load(CONTROL / "progress.json")
    assert all(reread[k] == v for k, v in original.items() if k not in allowed)
    save(LOG / "execution-538-final-checkpoint.json", reread["execution538CoordinatorCheckpoint"])
    print(f"Checkpoint538 saved; all {len(original)} original root values preserved outside explicit state fields.")


if __name__ == "__main__":
    actions = {"start": start, "strokes": strokes, "ledger": ledger, "audit": audit,
               "record": record, "issue": issue, "checkpoint": checkpoint}
    actions[sys.argv[1]]()
