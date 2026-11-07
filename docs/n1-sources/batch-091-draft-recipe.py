"""Generate and audit the bounded LOCAL UNREVIEWED batch091 draft."""
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
L = C / "logs" / "ed6e040c-40b9-47d8-8f36-415cf700b86b"
S = R / "docs" / "n1-sources"
HEAD = "1125f88281e5441e55cbbcf6e5ae9406abc2b6c2"
BASE = "7100a3873282b54515b9ef130766e77cf151a47b"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SCOPE = ["kanji/刃.md", "words/刃.md"]
NEXT = (
    "SAME091 two serial blind different-model-family initial textual reviews on the normally "
    "signed LOCAL UNREVIEWED snapshot: complete 刃 kanji/word, five preserved raw readings "
    "ジン/ニン/は/やいば/き.る in order, conservative []/[は] practice, recognized versus "
    "source-only distinction, complete applicable dictionary families and actual comparison "
    "articles, neutral translated examples, shape-only mnemonic, 刀/tool/edge distinctions, "
    "three N1 wrong labels, four direct word guards and one all-mapped pair/two directions. "
    "Cover correctness/scoped coverage/phone comprehensibility; actual available models and "
    "read-only tools, freeze edits and verify process exit before each next reviewer. Preserve "
    "full reports, actual models/read limits/original sessions, reconcile and confirm necessary "
    "fixes. Then fresh non-skipped Android, full production ContentSync ONCE/native N1/All "
    "choices/reading/drawing/article/Back/offline/four-font/visual acceptance, combined-current-main "
    "checks/normal signing/owner fast-forward/terminal green CI/EVERY immutable ZIP runtime hash/"
    "original budgets/verified owner-issue gates. No092 or unreviewed push. Approved control tools/"
    "committed packets/frozen workspace inputs only. Parent19008 retains runner.lock untouched; "
    "preserve/report/yield on actual new denial, signing hang or uncertain ownership. Published117/"
    "1228 and1111 acceptance-remainder unchanged; physical-phone/general-release/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(p):
    return json.loads(p.read_text(encoding="utf-8-sig"))


def save(p, data):
    tmp = p.with_suffix(p.suffix + ".646.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (645, "091", "continue")
    assert p["execution646StartingState"]["startingHead"] == HEAD


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    svg = (S / "batch-091-kanjivg.svg").read_bytes()
    proof = load(S / "batch-091-stroke-evidence.json")
    assert sha(svg) == proof["sha256"] and svg == Path(proof["input"]).read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert("刃", svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 3
    target = R / "strokes" / "刃.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-091-membership.json")
    assert frozen["membership"] == ["刃"] and frozen["sourceRows"] == [102]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=["刃"])
    frozen["limits"] = "LOCAL UNREVIEWED runtime draft only; not review closure, native acceptance or publication. Preserve separate earlier-level source members and all earlier deferred rows."
    save(S / "batch-091-membership.json", frozen)
    p = load(S / "batch-091-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=["刃"])
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": "刃", "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": True, "allWrittenKanji": row["allWrittenKanji"],
         "wordJlpt": None, "selectedSenses": row["selectedTeaching"],
         "status": "local-unreviewed-draft"} for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = []
    p["curatedProjection"] = [dict(p["proposedCuratedProjection"], kanji="刃")]
    card = metadata(R, SCOPE[0])
    p["quizAudit"] = {"刃": {
        "title": card["title"], "distractors": card["distractors"],
        "labels": [metadata(R, f"kanji/{c}.md")["title"] for c in card["distractors"]],
        "meaningDecisions": p["proposedQuiz"]["evidence"],
        "legacyFallbackDisposition": p["proposedQuiz"]["legacyFallback"],
        "limits": "Three N1-available wrong cards; actual production N1/All options pending. Not universal custom/random-pool certification.",
    }}
    p["wordQuizAudit"] = {
        "titles": {"刃": metadata(R, SCOPE[1])["title"]},
        "directExclusions": p["proposedQuiz"]["proposedDirectExclusions"],
        "notExcluded": p["proposedQuiz"]["notExcluded"],
        "confusableInventory": p["proposedQuiz"]["confusableInventory"],
        "limits": "Four conservative direct displayed-label guards, not transitive closure or unrestricted substitution.",
    }
    p["draftAuthorInspection"] = {
        "execution": 646, "sourceCheckpoint": HEAD,
        "freshCompleteCharacterReads": {"batch-091-kanjidic2.xml": [1, 81],
            "batch-091-comparison-kanjidic2.xml": [[1, 160], [161, 294]]},
        "freshCompleteLexicalReads": {
            "batch-091-jmdict.xml": [[1, 220], [204, 360], [360, 540], [541, 780], [781, 1008]],
            "batch-091-comparison-jmdict.xml": [[1, 220], [221, 440], [441, 650], [651, 821]],
        },
        "limits": "All56 lexical and22 comparison families freshly returned through complete ranges, with disclosed overlap at lexical boundaries. Five raw character records, all14 source-listed existing articles and full pinnedSVG freshly read. Not independent review or evidence of equal future reviewer read depth.",
        "publicLookup": "Fresh read of complete committed actual article-only extraction1-67EOF. Coordinator-provided dictionary extraction, not independent upstream retrieval. Historical image-glyph and classification limits preserved; no etymology adopted.",
        "completeExistingArticlesRead": list(load(S / "batch-091-preparation-audit.json")["inspectedArticleHashes"]),
        "exampleProvenance": "Original neutral kitchen-tool observation and photograph sentences, not quotations or handling/injury instructions. Noun/particles/translation author-inspected; independent naturalness review pending.",
        "lexicalDecisions": "Primaryは physical cutting-part sense from1369820. Separateやいば family not merged; recognizedジン/ニン not called source-only or automatically rare. き.る retained without inventing刃る. Four directguards preserve displayed-label safety without a tool/edge transitive clique.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no independent reviewer, fresh Android/native/font/phone acceptance or publication.",
        "All five raw readings retained in source order. Onlyは selected with its own linked row. ジン/ニン/やいば recognized without universal rarity claims; き.る source-only without fabricated spelling or copied切る senses.",
        "One necessary new physical-blade word article with no inferred vocabulary level. No changed reused articles or activated baseline pairs; one all-mapped pair/two directions.",
        "Three N1-available curated wrong cards and four direct word guards. Semantic author audit not universal live-pool certification; actual production N1/All checks pending.",
        "Exact final Han/cmap inventory is not native legibility or fallback-face acceptance. Fresh four-font/all-Han rendering and non-skipped RareHan/native gates pending; pilot all40 remains historical.",
        "Published117/1228 and1111 acceptance-remainder unchanged. Six separate source保案派第策結 retain earlierN2levels and are not accepted issue60 additions; separate妖exception retained.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest appmain; physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates remain. No optional historical-session helpers, parent-lock touch,092 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-091-progress.json", p)
    print("Three pinned paths generated; exact source/member and LOCAL UNREVIEWED ledgers prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "091")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    ledger = load(S / "batch-091-progress.json")
    packets = []
    for packet in ledger["dictionaryPackets"]:
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-091-kanjidic2.xml", "batch-091-comparison-kanjidic2.xml"]:
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
    assert named == load(S / "community-list-20261102.json") and named[101] == "刃"
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    base_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in base_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {"刃"} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    word = metadata(R, SCOPE[1])
    assert "jlpt" not in word and word["kanji"] == ["刃"]
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if "刃" in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/刃.md"}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {("刃", "words/刃.md")}
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
    assert verified == 8432
    svg = (S / "batch-091-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / "刃.json") == convert("刃", svg.decode("utf-8"))
    save(S / "batch-091-draft-stroke-audit.json", dict(
        load(S / "batch-091-stroke-evidence.json"), converted=True, output="strokes/刃.json",
        outputSha256=sha((R / "strokes" / "刃.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-091-font-preparation.json")["fonts"]:
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
    for c in ["刀", "辺", "際"]:
        row = metadata(R, f"kanji/{c}.md")
        assert len(row["distractors"]) == 3 and "刃" not in row["distractors"]
        neighbors[c] = {"title": row["title"], "distractors": row["distractors"]}
    explicit = [p.stem for p in (R / "kanji").glob("*.md")
                if p.stem != "刃" and "刃" in metadata(R, f"kanji/{p.name}").get("distractors", [])]
    assert explicit == []
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in ["乃", "凹", "凸"])
    save(S / "batch-091-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "091", "completeNewArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE},
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "Complete new articles. Cmap presence/absence not native legibility/fallback-face acceptance. Fresh four-font/all-Han and non-skipped RareHan/native gates pending.",
    })
    result.update(
        schemaVersion=1, execution=646, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
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
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=117,
        remainingAdditions=1111, draftOnlyAdditions=["刃"], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-091-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-091-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-646.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8432" in text and result["contentVersion"] in text
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
        target = S / f"batch-091-draft-{stem}-646.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    recipe = S / "batch-091-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-646.json", {
        "schemaVersion": 1, "execution": 646, "batch": "091", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution646StartingState"],
        "runtimeDrafted": ["刃"], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "audit": "docs/n1-sources/batch-091-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-091-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-091-draft-stroke-audit.json",
        "recipe": recipe.relative_to(R).as_posix(), "recipeSha256": sha(recipe.read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock throughout coordinator20332; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helpers in control. No optional historical-session-helper access.",
        "readEvidenceLimits": load(S / "batch-091-progress.json")["draftAuthorInspection"],
        "diagnostics": [
            "Initial complete checkpoint decoding succeeded but console output hit cp1252 Unicode encoding and size limits. Final645 inspected directly by bounded range. No required source read failed and no permission denial occurred.",
            "Initial vocabulary invocation targeted validate_grammar_vocabulary.py, an import-only module with no CLI, and produced no check evidence. Preserved that empty output as vocabulary-module-noop-646.txt; actual grammar_vocabulary.py check subsequently ran and its reviewed-prompt receipt is the recorded consistency check. Unrelated pilot coverage remains incomplete.",
        ],
        "actualNewPermissionDenials": [], "publishedAdditions": 117, "remainingAdditions": 1111,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft check receipts and durable recipe archived.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "audit", "record"])
    globals()[parser.parse_args().phase]()
