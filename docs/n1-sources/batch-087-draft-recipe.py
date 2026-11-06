"""Persist and audit the bounded, unreviewed batch 087 runtime draft."""
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
L = C / "logs" / "80600bd0-fa68-4e41-ad45-4e0812f25074"
S = R / "docs" / "n1-sources"
HEAD = "e03a16b6d9c97e6e430f59b1d950a928cb43613e"
BASE = "6eaa018dcbcabe57d9e22ddf6b07c6b8ee2dfea6"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SCOPE = ["kanji/凪.md", "words/凪.md", "words/凪ぐ.md"]
NEXT = (
    "SAME087 two serial blind different-model-family initial textual reviews on the normally signed "
    "LOCAL UNREVIEWED snapshot: complete 凪/凪/凪ぐ, both raw kun readings, no on reading, "
    "noun/verb/weather-versus-feelings/modern gu-conjugation, complete applicable source families, "
    "seven direct word guards, all two mapped pairs/four directions and phone comprehensibility. "
    "Use actual available models and read-only tools, freeze edits, verify actual process exit before "
    "next reviewer, retain complete reports/model/read limits; reconcile and confirm necessary fixes. "
    "Then fresh non-skipped Android/native full ContentSync ONCE, N1/All actual fallback/reading/"
    "drawing/article/Back/offline/fourfont and bounded visual acceptance, combined current-main/"
    "normal signing/owner fast-forward/terminal green CI/EVERY immutable ZIP runtime hash/original "
    "budgets/ownerissue gates. No088 or unreviewed push. Parent19008 retains lock untouched. "
    "Published113/1228 and1115 acceptance-remainder unchanged; physicalphone/generalrelease/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data):
    raw = json.dumps(data, ensure_ascii=True, indent=2) + "\n"
    temp = p.with_suffix(p.suffix + ".610.tmp")
    assert not temp.exists(), temp
    temp.write_text(raw, encoding="utf-8")
    assert load(temp) == data
    temp.replace(p)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def start():
    for root, expected in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    assert git("rev-parse", "origin/main") == BASE
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (609, "087", "continue")
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    assert not (L / "progress-before-610.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-610.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    assert json.loads(text.split(marker, 1)[1])["checkpoint"] == 609
    state = {
        "execution": 610, "batch": "087", "startingHead": HEAD,
        "freshOriginMain": BASE, "androidHead": APP,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME087 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,088 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and checkpoint parsed; operative contract, approved issue and final609 directly inspected. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 and coordinator26824 parent relationship verified with Win32_Process; matching runner.json session. Parent retains runner.lock; no child acquisition/delete/unlock.",
        "artifactPathPreflight": "Committed batch087 packets and approved control helpers/inputs only. No optional historical-session helper accessed.",
        "worktrees": "Dedicated content and qualified TESTONLY Android wholly clean with signatures G; fresh origin/main equals published base. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution610StartingState"] = state
    p.update(stage="batch-087-runtime-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting runtime-draft scope persisted; all prior history retained.")


def geometry():
    from generate_strokes import convert, KANJIVG_REVISION
    source = (S / "batch-087-kanjivg.svg").read_bytes()
    receipt = load(S / "batch-087-stroke-evidence.json")
    assert sha(source) == receipt["sha256"]
    assert KANJIVG_REVISION == receipt["revision"]
    converter = (R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")
    assert sha(converter) == receipt["converterNormalizedSha256"]
    result = convert("凪", source.decode("utf-8"))
    assert result["strokeCount"] == 6 and len(result["strokes"]) == 6
    path = R / "strokes" / "凪.json"
    assert not path.exists()
    path.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    print("Six paths generated by pinned production converter; no manual geometry.")


def prepare():
    p = load(S / "batch-087-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=["凪"])
    p["dictionaryPackets"] = [
        {"selection": "batch-087-lexical-selection.json", "xml": "batch-087-jmdict.xml"},
        {"selection": "batch-087-comparison-selection.json", "xml": "batch-087-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"],
                   reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": "凪", "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": True,
         "allWrittenKanji": row["allWrittenKanji"], "wordJlpt": None,
         "selectedSenses": row["selectedTeaching"], "status": "local-unreviewed-draft"}
        for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["allMappedReciprocalPairs"] = p["requiredReciprocalPairs"]
    p["changedReusedPassages"] = []
    p["curatedProjection"] = [dict(p["proposedCuratedProjection"], kanji="凪")]
    card = metadata(R, SCOPE[0])
    p["quizAudit"] = {"凪": {
        "title": card["title"], "distractors": card["distractors"],
        "labels": [metadata(R, f"kanji/{c}.md")["title"] for c in card["distractors"]],
        "meaningDecisions": p["proposedQuiz"]["evidence"],
        "legacyFallbackDisposition": p["proposedQuiz"]["legacyFallback"],
        "limits": "Actual production N1-only has two available curated wrong cards and needs fallback. N1/All production choices remain required Android/native gates; no universal livepool certification.",
    }}
    p["wordQuizAudit"] = {
        "titles": {metadata(R, name)["word"]: metadata(R, name)["title"] for name in SCOPE[1:]},
        "directExclusions": p["proposedQuiz"]["proposedDirectExclusions"],
        "notExcluded": p["proposedQuiz"]["notExcluded"],
        "confusableInventory": "Introductory contract plus targeted calm/state/change/cessation inventory and title search; no direct 凪/凪ぐ row. No exhaustive corpus semantic review claimed.",
        "limits": "Seven direct pairs are conservative displayed-label safeguards, not transitive cliques or unrestricted Japanese substitution; actual production pools remain pending.",
    }
    p["draftAuthorInspection"] = {
        "execution": 610, "sourceCheckpoint": HEAD,
        "completeFreshPacketReads": {
            "batch-087-kanjidic2.xml": "complete through EOF53",
            "batch-087-jmdict.xml": "complete through EOF169",
            "batch-087-comparison-jmdict.xml": [[1, 200], [201, 400], [401, 570]],
            "batch-087-nagi-public-text.txt": "complete through EOF",
            "batch-087-nagu-public-text.txt": "complete through EOF",
        },
        "existingArticleScope": ["kanji/風.md", "kanji/凡.md", "kanji/凹.md",
                                 "words/穏やか.md", "words/静か.md", "words/静まる.md",
                                 "words/止む.md", "words/落ち着く.md"],
        "sourceDecisions": "Ten complete exact-member families and fifteen complete comparison families inspected. Select noun1459650 and modern intransitive verb1459660; source-bound 朝凪/夕凪 recognition only. Separate feelings 和ぐ2859999 and classical inflections are not transferred. No frequency or personal-name reading inference.",
        "publicLookup": "Coordinator-provided committed exact dictionary text read afresh, not independent upstream retrieval. Original HTML hashes/provenance and image-placeholder limits remain in source packet.",
        "missingPriorArt": "Two guessed 凋/凋む card paths returned notfound; no permission denial or dependency. Existing 凍 and 止む format examples read instead.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no independent reviewer, fresh Android/native/font/phone acceptance or publication.",
        "Complete raw readings/order preserved: on[], kunなぎ/な.ぐ, both selected with separate linked articles. No word JLPT inferred from kanji membership/grade9.",
        "All existing runtime bytes/identities/levels/readings/exclusions unchanged; only one kanji, two necessary support articles and one generated stroke file added.",
        "Three curated wrong cards exist in All but only凡/凹 in N1. N1 needs a real production fallback check; displayed choices not certified here.",
        "Seven direct word guards are label safeguards, not transitive or unrestricted equivalence. Source sense/spelling boundaries and modern/Classical distinction retained.",
        "Exact cmap inventory is not native legibility or fallback-face acceptance. Fresh fourfont/allHan rendering and non-skipped RareHan/native checks pending; pilot all40 remains historical.",
        "Published113/1228 and1115 acceptance-remainder unchanged. Six separate source保案派第策結 retain earlierN2levels and are not accepted issue60 additions; do not duplicate/relevel.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest appmain; physicalphone/generalrelease/whole-set outstanding.",
        "All original source/review/process/denial/native/combinedmain/signing/ownerpush/terminalCI/EVERYimmutableZIPhash/budget/ownerissue gates remain. No optional historicalsessionhelpers, parentlock touch,088 or secondrunner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-087-progress.json", p)
    print("Exact LOCAL UNREVIEWED draft ledger prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    result = batch_audit(R, "087")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    packets = []
    for packet in load(S / "batch-087-progress.json")["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-087-kanjidic2.xml", "batch-087-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(records[entry.findtext("literal")])
            count += 1
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
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
    assert named == load(S / "community-list-20261102.json") and named[95] == "凪"
    current = {path.stem for path in (R / "kanji").glob("*.md")}
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    assert len(published) == 113
    assert current - old == published | set("保案派第策結坊的誰身阪") | {"凪"}
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    assert {f"words/{path.name}" for path in (R / "words").glob("*.md")
            if "凪" in metadata(R, f"words/{path.name}")["kanji"]} == set(SCOPE[1:])
    for name in SCOPE[1:]:
        assert "jlpt" not in metadata(R, name)
        assert metadata(R, name)["kanji"] == ["凪"]
    current_manifest = build_manifest(R)
    assert current_manifest == load(R / "manifest.json")
    verified = 0
    for section, entries in current_manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = (sha((R / name).read_bytes()) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
                assert actual == expected, name
                verified += 1
    assert verified == 8420
    svg = (S / "batch-087-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / "凪.json") == convert("凪", svg.decode("utf-8"))
    save(S / "batch-087-draft-stroke-audit.json", dict(
        load(S / "batch-087-stroke-evidence.json"), converted=True, output="strokes/凪.json",
        outputSha256=sha((R / "strokes" / "凪.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-087-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    neighbors = {}
    for c in ["安", "平", "静"]:
        m = metadata(R, f"kanji/{c}.md")
        assert len(m["distractors"]) == 3 and "凪" not in m["distractors"]
        neighbors[c] = {"title": m["title"], "distractors": m["distractors"]}
    explicit = [path.stem for path in (R / "kanji").glob("*.md")
                if path.stem != "凪" and "凪" in metadata(R, f"kanji/{path.name}").get("distractors", [])]
    assert explicit == []
    save(S / "batch-087-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "087", "completeNewArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE},
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "All three complete new articles; cmap presence/absence not glyph/native/fallback-face acceptance. Fresh fourfont/allHan and non-skipped RareHan/native gates pending.",
    })
    result.update(
        schemaVersion=1, execution=610, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=5, decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=2, directedLinksVerified=4, directWordExclusionPairs=7,
        legacyDefaultFallbackNeighbors=neighbors, existingExplicitTargetDistractors=explicit,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=113,
        remainingAdditions=1115, draftOnlyAdditions=["凪"], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=load(S / "batch-087-progress.json")["limits"])
    save(S / "batch-087-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    result = load(S / "batch-087-draft-audit.json")
    receipts = {}
    total = 0
    stems = ["validate", "manifest", "draft-audit"] + [
        f"draft-tests-610-part{i}" for i in range(1, 6)
    ] + ["vocabulary-consistency", "budget"]
    for stem in stems:
        filename = stem + ".txt" if stem.startswith("draft-tests-610-part") else f"{stem}-610.txt"
        raw = (L / filename).read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8420" in text and result["contentVersion"] in text
        elif stem == "draft-audit":
            assert json.loads(text) == result
        elif stem.startswith("draft-tests-610-part"):
            assert text.rstrip().endswith("OK") and "skipped" not in text
            total += int(re.search(r"Ran (\d+) tests", text)[1])
        elif stem == "vocabulary-consistency":
            assert "reviewed prompts" in text
        elif stem == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        target = S / f"batch-087-{filename}.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                          "uncompressedSha256": sha(raw)}
    recipe = S / "batch-087-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-610.json", {
        "schemaVersion": 1, "execution": 610, "batch": "087", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "runtimeDrafted": ["凪"], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "focusedTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "audit": "docs/n1-sources/batch-087-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-087-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-087-draft-stroke-audit.json",
        "recipe": recipe.relative_to(R).as_posix(), "recipeSha256": sha(recipe.read_bytes()),
        "focusedTestModules": ["test_audit_n1_batch", "test_audit_n1_pilot",
                              "test_extract_n1_jmdict", "test_freeze_n1_sources",
                              "test_validate", "test_content_language"],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock throughout coordinator26824; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helper in control. No optional historicalsessionhelper access.",
        "diagnostics": "Initial validate_grammar_vocabulary.py invocation was a library-only no-op, not vocabulary-check evidence; actual grammar_vocabulary.py check subsequently required and archived.",
        "actualNewPermissionDenials": [], "publishedAdditions": 113, "remainingAdditions": 1115,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft check receipts and durable recipe archived.")


def finish():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name
    evidence = load(S / "execution-610.json")
    for receipt in evidence["checks"].values():
        raw = (R / receipt["path"]).read_bytes()
        assert sha(raw) == receipt["sha256"] and sha(gzip.decompress(raw)) == receipt["uncompressedSha256"]
    assert sha((R / evidence["recipe"]).read_bytes()) == evidence["recipeSha256"]
    before = load(L / "progress-before-610.json")
    p = load(C / "progress.json")
    changing = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in changing:
            assert p[key] == value, key
    result = load(S / "batch-087-draft-audit.json")
    checkpoint = dict(
        schemaVersion=1, execution=610, checkpoint=610, batch="087", status="continue",
        stage="local-unreviewed-draft", savedCommit=head, signature="G",
        sourceCommit=HEAD, evidence="docs/n1-sources/execution-610.json",
        membership=["凪"], sourceRow=96, runtimeDrafted=["凪"], reviewClosed=[], published=[],
        runtimePublished=False, contentVersion=result["contentVersion"],
        focusedTestsPassed=evidence["focusedTestsPassed"], validatorErrors=0,
        metadataReadings=2, curatedOnKeys=[], curatedKunKeys=["なぎ", "なぐ"],
        allMappedReciprocalPairs=2, directedLinksVerified=4, newNecessarySupportArticles=2,
        reusedSupportArticles=0, changedReusedFiles=0, directWordExclusionPairs=7, pinnedStrokePaths=6,
        allRuntimePayloadHashesVerified=8420, actualHanCount=result["actualHanCount"],
        nativeFontAcceptance="pending", dedicatedWorktreesClean=True,
        originalHistoricalRootKeysCompared=len(before), allOriginalHistoricalValuesPreserved=True,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        parentLockTouched=False, optionalHistoricalSessionHelpersAccessed=False,
        actualNewPermissionDenials=[], publishedAdditions=113, remainingAdditions=1115,
        lastPublishedCommit=p["lastPublishedCommit"], physicalPhoneAcceptance="outstanding",
        generalReleaseAcceptance="outstanding", wholeProjectComplete=False, nextBatchStarted=False,
        nextAction=NEXT)
    p.update(checkpoint=610, status="continue", stage="batch-087-local-unreviewed-draft",
             nextAction=NEXT, blocker=None)
    p["execution610StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution610CoordinatorCheckpoint"] = checkpoint
    save(C / "progress.json", p)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["start", "geometry", "prepare", "audit", "record", "finish"])
    args = parser.parse_args()
    globals()[args.phase]()
