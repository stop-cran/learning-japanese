"""Generate and mechanically audit the bounded, unreviewed batch088 draft."""
import argparse
import ast
import copy
import gzip
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
L = C / "logs" / "de4d2673-4d8f-4f05-b033-f34205e1c291"
S = R / "docs" / "n1-sources"
HEAD = "5d7c2ede8650ed8b0c740e1493bdc4629a53d56b"
BASE = "8a36f8cd81c0e35c330079881cac1a1f3a771e26"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SCOPE = ["kanji/凱.md", "words/凱旋.md"]
NEXT = (
    "SAME088 two serial blind different-model-family initial textual reviews on the normally signed "
    "LOCAL UNREVIEWED snapshot: complete 凱/凱旋, four raw readings/order, selectedガイ and explicitkun[], "
    "source-onlyカイ/かちどき/やわらぐ versus actual lexical spellings, intransitive triumphant-return "
    "sports/performance examples, compound-specific旋return, complete applicable source families, "
    "four direct word guards, one allmapped pair/two directions and phone comprehensibility. "
    "Use actual available models/read-only tools; freeze edits and verify actual process exit before "
    "the next reviewer. Preserve full reports, actual model/read limits and original sessions; reconcile "
    "and confirm necessary fixes. Then fresh non-skipped Android/native full ContentSync ONCE, "
    "N1/All production choices/curated reading/drawing/article/Back/offline/fourfont and bounded "
    "visual acceptance, combined current-main/normal signing/owner fast-forward/terminal green CI/"
    "EVERY immutable ZIP runtime hash/original budgets/verified ownerissue gates. "
    "No089 or unreviewed push. Parent19008 retains lock untouched. Published114/1228 and1114 "
    "acceptance-remainder unchanged; physicalphone/generalrelease/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data):
    temp = p.with_suffix(p.suffix + ".619.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    temp.replace(p)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def identity():
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    svg = (S / "batch-088-kanjivg.svg").read_bytes()
    receipt = load(S / "batch-088-stroke-evidence.json")
    membership = load(S / "batch-088-membership.json")
    assert membership["membership"] == ["凱"] and membership["sourceRows"] == [97]
    membership["members"] = [{"kanji": "凱", "sourceRow": 97}]
    save(S / "batch-088-membership.json", membership)
    assert sha(svg) == receipt["sha256"]
    assert KANJIVG_REVISION == receipt["revision"]
    converter = (R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")
    assert sha(converter) == receipt["converterNormalizedSha256"]
    result = convert("凱", svg.decode("utf-8"))
    assert result["strokeCount"] == len(result["strokes"]) == 12
    target = R / "strokes" / "凱.json"
    assert not target.exists()
    target.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    p = load(S / "batch-088-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=["凱"])
    p["dictionaryPackets"] = [
        {"selection": "batch-088-lexical-selection.json", "xml": "batch-088-jmdict.xml"},
        {"selection": "batch-088-comparison-selection.json", "xml": "batch-088-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": "凱", "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": True, "allWrittenKanji": row["allWrittenKanji"],
         "wordJlpt": None, "selectedSenses": row["selectedTeaching"], "status": "local-unreviewed-draft"}
        for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["allMappedReciprocalPairs"] = p["requiredReciprocalPairs"]
    p["changedReusedPassages"] = []
    p["curatedProjection"] = [dict(p["proposedCuratedProjection"], kanji="凱")]
    card = metadata(R, SCOPE[0])
    p["quizAudit"] = {"凱": {
        "title": card["title"], "distractors": card["distractors"],
        "labels": [metadata(R, f"kanji/{c}.md")["title"] for c in card["distractors"]],
        "meaningDecisions": p["proposedQuiz"]["evidence"],
        "legacyFallbackDisposition": p["proposedQuiz"]["legacyFallback"],
        "limits": "All three curated wrong cards available in N1/All; actual production choices remain required. No universal livepool certification.",
    }}
    p["wordQuizAudit"] = {
        "titles": {"凱旋": metadata(R, SCOPE[1])["title"]},
        "directExclusions": p["proposedQuiz"]["proposedDirectExclusions"],
        "notExcluded": p["proposedQuiz"]["notExcluded"],
        "confusableInventory": "Intro1-90 plus scoped return/victory/triumph search; CW009/CW011 compared with actual returning articles and complete families. Not exhaustive semantic certification.",
        "limits": "Four conservative direct displayed-label safeguards, not transitive cliques or unrestricted Japanese substitutions.",
    }
    p["draftAuthorInspection"] = {
        "execution": 619, "sourceCheckpoint": HEAD,
        "completeFreshPacketReads": {
            "batch-088-kanjidic2.xml": "complete through EOF56",
            "batch-088-jmdict.xml": "complete through EOF108",
            "batch-088-comparison-jmdict.xml": [[1, 180], [181, 360], [361, 506]],
            "batch-088-comparison-kanjidic2.xml": [[1, 180], [181, 365]],
            "batch-088-gai-public-text.txt": "complete through EOF",
            "batch-088-gaisen-public-text.txt": "complete through EOF",
        },
        "completeExistingArticlesRead": ["kanji/凪.md", "kanji/凡.md", "kanji/凸.md", "kanji/凹.md",
            "kanji/勝.md", "kanji/歌.md", "words/帰る.md", "words/帰宅.md", "words/帰り.md",
            "words/戻る.md", "words/優勝.md", "words/勝ち.md", "words/凪ぐ.md"],
        "sourceDecisions": "Seven exact-member plus eighteen comparison complete families; select only1203200 as necessary support. Source-only character glosses not ordinary lexical spellings. Scope preserves raw metadata/grade9 and separates triumphant return from winning.",
        "publicLookup": "Fresh read of committed coordinator-extracted actual dictionary text, not independent upstream retrieval. Original HTML/provenance/image-placeholder/historical limits remain.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no independent reviewer, fresh Android/native/font/phone acceptance or publication.",
        "Four complete raw readings/order preserved: onガイ/カイ, undottedkunかちどき/やわらぐ. Onlyガイselected, explicitkun[]. Character glosses not manufactured modern words; no frequency/name-only inference.",
        "One necessary new support凱旋, metadata凱and旋despite absent旋card. No word JLPT inferred. Source intransitive return/nominal object and sports/performance extension retained.",
        "All existing runtime bytes/identities/levels/readings/exclusions unchanged; only one kanji, one necessary word and one generated stroke file added.",
        "Three N1-available curated wrong cards and four direct word guards; semantic author audit not universal livepool certification. Actual N1/All production checks pending.",
        "Exact final Han/cmap inventory is not native legibility or fallback-face acceptance. Fresh fourfont/allHan rendering and non-skipped RareHan/native checks pending; pilot all40 remains historical.",
        "Published114/1228 and1114 acceptance-remainder unchanged. Six separate source保案派第策結 retain earlierN2levels and are not accepted issue60 additions; separate妖exception retained.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest appmain; physicalphone/generalrelease/whole-set outstanding.",
        "All original source/review/process/denial/OOM/readdepth/native/combinedmain/signing/ownerpush/terminalCI/EVERYimmutableZIPhash/budget/ownerissue gates remain. No optional historicalsessionhelpers, parentlock touch,089 or secondrunner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-088-progress.json", p)
    print("Twelve pinned paths generated and LOCAL UNREVIEWED draft ledger prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "088")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    packets = []
    for packet in load(S / "batch-088-progress.json")["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-088-kanjidic2.xml", "batch-088-comparison-kanjidic2.xml"]:
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
    assert named == load(S / "community-list-20261102.json") and named[96] == "凱"
    current = {path.stem for path in (R / "kanji").glob("*.md")}
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    assert len(published) == 114
    assert current - old == published | set("保案派第策結坊的誰身阪") | {"凱"}
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    assert {f"words/{path.name}" for path in (R / "words").glob("*.md")
            if "凱" in metadata(R, f"words/{path.name}")["kanji"]} == {SCOPE[1]}
    word = metadata(R, SCOPE[1])
    assert "jlpt" not in word and word["kanji"] == ["凱", "旋"]
    assert not (R / "kanji" / "旋.md").exists()
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
    assert verified == 8423
    svg = (S / "batch-088-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / "凱.json") == convert("凱", svg.decode("utf-8"))
    save(S / "batch-088-draft-stroke-audit.json", dict(
        load(S / "batch-088-stroke-evidence.json"), converted=True, output="strokes/凱.json",
        outputSha256=sha((R / "strokes" / "凱.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-088-font-preparation.json")["fonts"]:
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
    for c in ["勝", "歌"]:
        m = metadata(R, f"kanji/{c}.md")
        assert len(m["distractors"]) == 3 and "凱" not in m["distractors"]
        neighbors[c] = {"title": m["title"], "distractors": m["distractors"]}
    explicit = [path.stem for path in (R / "kanji").glob("*.md")
                if path.stem != "凱" and "凱" in metadata(R, f"kanji/{path.name}").get("distractors", [])]
    assert explicit == []
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in ["凡", "凸", "凹"])
    save(S / "batch-088-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "088", "completeNewArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE},
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "Actual complete new articles, not proposed inventory. Cmap presence/absence not glyph/native/fallback-face acceptance. Fresh fourfont/allHan and non-skipped RareHan/native gates pending.",
    })
    result.update(
        schemaVersion=1, execution=619, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=5, decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=1, directedLinksVerified=2, directWordExclusionPairs=4,
        legacyDefaultFallbackNeighbors=neighbors, existingExplicitTargetDistractors=explicit,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=114,
        remainingAdditions=1114, draftOnlyAdditions=["凱"], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=load(S / "batch-088-progress.json")["limits"])
    save(S / "batch-088-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-088-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-619.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8423" in text and result["contentVersion"] in text
        elif stem == "audit":
            assert json.loads(text) == result
        elif stem == "tests":
            assert text.rstrip().endswith("OK") and "skipped" not in text
            total = int(re.search(r"Ran (\d+) tests", text)[1])
        elif stem == "vocabulary":
            assert "reviewed prompts" in text
        elif stem == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        elif stem == "whitespace":
            assert not text.strip()
        target = S / f"batch-088-draft-{stem}-619.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    recipe = S / "batch-088-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-619.json", {
        "schemaVersion": 1, "execution": 619, "batch": "088", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "runtimeDrafted": ["凱"], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "audit": "docs/n1-sources/batch-088-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-088-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-088-draft-stroke-audit.json",
        "recipe": recipe.relative_to(R).as_posix(), "recipeSha256": sha(recipe.read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock throughout coordinator17044; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helper in control. No optional historicalsessionhelper access.",
        "diagnostics": [
            "First validator output used Windows cp1252 and failed while printing a broken豆link. Original diagnostic preserved in execution log. Explicit PYTHONUTF8=1 used thereafter; missing豆card now plain text with kana.",
            "Frozen membership lacked the existing auditor's members projection. Added exact凱/sourceRow97 object without changing frozen membership, order, base or source-row identity."
        ],
        "actualNewPermissionDenials": [], "publishedAdditions": 114, "remainingAdditions": 1114,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft check receipts and durable recipe archived.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "audit", "record"])
    globals()[parser.parse_args().phase]()
