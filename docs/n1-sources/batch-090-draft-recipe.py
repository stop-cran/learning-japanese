"""Generate and audit the source-bounded local unreviewed batch090 draft."""
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
L = C / "logs" / "012962a4-ff55-440c-8452-ca79e83363dc"
S = R / "docs" / "n1-sources"
HEAD = "26c32af8be61e11421b9523b0a32b76f43b2d3ef"
BASE = "ebfd48dc911f32be0eeb9426db2f2d35a9084044"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SCOPE = ["kanji/刀.md", "words/日本刀.md"]
NEXT = (
    "SAME090 two serial blind different-model-family initial textual reviews on the normally signed "
    "LOCAL UNREVIEWED snapshot: complete 刀/日本刀 and exact four reused navigation/component diffs, "
    "all raw トウ/かたな/そり in order, selected トウ and かたな with own linked rows, source-only "
    "そり without allocating it from jukujikun 剃刀, complete applicable dictionary families, "
    "日本/Japan as lexical modifier plus 刀/sword, both にほんとう/にっぽんとう without frequency "
    "ranking or general sound-change rule, neutral museum/photo sentences and translations, "
    "sword/category/tool distinctions, labelled shape-only mnemonic and 力 comparison, three N1 "
    "wrong labels, one direct 日本刀/刀 guard, five all-mapped pairs/ten directions, correctness/"
    "scoped coverage/phone comprehensibility. Use actual available models/read-only tools; freeze "
    "edits and verify actual process exit before next reviewer. Preserve full reports, actual "
    "models/read limits/original sessions; reconcile and confirm necessary fixes. Then fresh "
    "non-skipped Android, native full production ContentSync ONCE, N1/All production choices/"
    "reading/drawing/article/Back/offline/four-font and bounded visual acceptance, combined "
    "current-main/normal signing/owner fast-forward/terminal green CI/EVERY immutable ZIP runtime "
    "hash/original budgets/verified owner-issue gates. No091 or unreviewed push. Parent19008 retains "
    "lock untouched. Published116/1228 and1112 acceptance-remainder unchanged; physical-phone/"
    "general-release/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(path.suffix + ".637.tmp")
    assert not temp.exists(), temp
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == data
    temp.replace(path)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def identity():
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (636, "090", "continue")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    svg = (S / "batch-090-kanjivg.svg").read_bytes()
    stroke = load(S / "batch-090-stroke-evidence.json")
    assert sha(svg) == stroke["sha256"]
    assert svg == Path(stroke["input"]).read_bytes()
    assert KANJIVG_REVISION == stroke["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == stroke["converterNormalizedSha256"]
    geometry = convert("刀", svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 2
    target = R / "strokes" / "刀.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-090-membership.json")
    assert frozen["membership"] == ["刀"] and frozen["sourceRows"] == [101]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen["limits"] = "LOCAL UNREVIEWED runtime draft only; not review closure, native acceptance or publication. Preserve separate earlier-level source members 保案派第策結 without duplicating or releveling them."
    frozen["members"] = [{"kanji": "刀", "sourceRow": 101}]
    frozen.update(status="local-unreviewed-draft", drafted=["刀"])
    save(S / "batch-090-membership.json", frozen)
    p = load(S / "batch-090-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=["刀"])
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": "刀", "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": row["article"] == "words/日本刀.md",
         "allWrittenKanji": row["allWrittenKanji"], "wordJlpt": row["preservedWordJlpt"],
         "selectedSenses": row["selectedTeaching"], "status": "local-unreviewed-draft"}
        for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = [["刀", row["article"]] for row in p["supportMappings"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["pairScopeQualification"] = "Generic batch auditor verifies the three new-member pairs. Separate all-mapped audit also requires existing日/本, yielding five pairs/ten directions, not three pairs."
    passages = [
        ("words/刀.md",
         "刀 is one character, with the native reading かたな for this standalone word.",
         "[刀](../kanji/刀.md) is one character, with the native reading かたな for this standalone word.",
         "Link the existing component introduction only; all original metadata/teaching preserved."),
        ("words/剃刀.md", "剃 concerns shaving and 刀 a blade,",
         "剃 concerns shaving and [刀](../kanji/刀.md) a blade,",
         "Link the existing component introduction only; preserve whole-word warning, N2 level and鋭い exclusion."),
        ("kanji/日.md", "- 毎日 まいにち — every day\n",
         "- 毎日 まいにち — every day\n- [日本刀](../words/日本刀.md) にほんとう — Japanese sword; 日本 names Japan in this compound\n",
         "One additive navigation-only line; no new rawニチ allocation or old teaching rewrite."),
        ("kanji/本.md", "- 本物 ほんもの — the real thing\n",
         "- 本物 ほんもの — the real thing\n- [日本刀](../words/日本刀.md) にほんとう — Japanese sword; 日本 names Japan in this compound\n",
         "One additive navigation-only line; 日本 is the country name as a lexical unit."),
    ]
    p["changedReusedPassages"] = [
        {"article": name, "before": before, "after": after, "scope": scope}
        for name, before, after, scope in passages
    ]
    p["curatedProjection"] = [dict(p["proposedCuratedProjection"], kanji="刀")]
    card = metadata(R, SCOPE[0])
    p["quizAudit"] = {"刀": {
        "title": card["title"], "distractors": card["distractors"],
        "labels": [metadata(R, f"kanji/{c}.md")["title"] for c in card["distractors"]],
        "meaningDecisions": p["proposedQuiz"]["evidence"],
        "legacyFallbackDisposition": p["proposedQuiz"]["legacyFallback"],
        "limits": "Three N1-available wrong cards; actual production N1/All options pending. Not universal custom/random-pool certification.",
    }}
    p["wordQuizAudit"] = {
        "titles": {"日本刀": metadata(R, SCOPE[1])["title"]},
        "directExclusions": p["proposedQuiz"]["proposedDirectExclusions"],
        "notExcluded": p["proposedQuiz"]["notExcluded"],
        "confusableInventory": p["proposedQuiz"]["confusableInventory"],
        "limits": "One direct displayed-label safeguard, not transitive closure or unrestricted historical subtype equivalence.",
    }
    p["draftAuthorInspection"] = {
        "execution": 637, "sourceCheckpoint": HEAD,
        "freshCompleteCharacterReads": {"batch-090-kanjidic2.xml": "1-82EOF",
            "batch-090-comparison-kanjidic2.xml": [[1, 200], [201, 400], [401, 576]]},
        "freshCompleteLexicalReads": {
            "batch-090-jmdict.xml": {"1418800": [388, 410], "1435180": [469, 510],
                "1446420": [603, 646], "1464780": [967, 989], "1622000": [1235, 1263]},
            "batch-090-comparison-jmdict.xml": [[1, 220], [221, 426]],
        },
        "sourcePreparationFullFamilyCoverage": "Execution636 inspected all194 complete exact-member families; inherited source-preparation evidence, not claimed as194 fresh draft-execution reads. This execution freshly inspected five complete applicable lexical families plus all13 comparison families. Other exact-member families remain complete and unselected.",
        "publicLookup": "Fresh read of complete committed katana article-only extraction1-123 and nihontou precise lexical headings1-19. Coordinator-provided actual dictionary extraction, not independent upstream retrieval. Longer nihontou history/metallurgy remains archived, not adopted or freshly verified.",
        "completeExistingArticlesRead": ["words/刀.md", "words/剃刀.md", "words/日本.md",
            "words/包丁.md", "words/ナイフ.md", "kanji/日.md", "kanji/本.md",
            "kanji/乃.md", "kanji/凹.md", "kanji/凸.md", "kanji/力.md", "kanji/切.md"],
        "exampleProvenance": "Original neutral museum/photo full sentences, not quotations or weapon-use instructions. Noun/particles/translation author-inspected; independent naturalness review still pending.",
        "lexicalDecisions": "日本刀 primaryにほんとう and alternateにっぽんとう retained without frequency inference. Daijisen lexical split and explicit日本刀 example allocate finalトウ. Noじ/ほん microallocation claim, no compulsory curvature/history rule. Source-onlyそり retained without assigning it fromかみそり.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no independent reviewer, fresh Android/native/font/phone acceptance or publication.",
        "All rawトウ/かたな/そり retained in source order; onlyトウ/かたな selected with own linked table rows. Source-onlyそり not inferred nonexistent/archaic or allocated from jukujikun剃刀.",
        "Necessary new日本刀 has every written kanji and no inferred vocabulary level. Existing刀N3/剃刀N2 metadata/readings/exclusions unchanged; reused日/本 receive navigation-only lines. 日本/Japan acts as lexical modifier, not sun-book etymology.",
        "One new kanji/word/generatedstroke; five all-mapped reciprocal pairs/ten directions include both baseline reuse words and existing日/本. 剃 has no current card and is retained in word metadata without a broken link.",
        "Three N1-available curated wrong cards and one direct日本刀/刀 guard; semantic author audit not universal live-pool certification. Actual N1/All production checks pending.",
        "Exact final Han/cmap inventory is not native legibility or fallback-face acceptance. Fresh four-font/all-Han rendering and non-skipped RareHan/native gates pending; pilot all40 remains historical.",
        "Published116/1228 and1112 acceptance-remainder unchanged. Six separate source保案派第策結 retain earlierN2levels and are not accepted issue60 additions; separate妖exception retained.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest appmain; physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates remain. No optional historical-session helpers, parent-lock touch,091 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-090-progress.json", p)
    print("Two pinned paths generated; exact source/member and LOCAL UNREVIEWED ledger prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "090")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    ledger = load(S / "batch-090-progress.json")
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
    for name in ["batch-090-kanjidic2.xml", "batch-090-comparison-kanjidic2.xml"]:
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
    assert named == load(S / "community-list-20261102.json") and named[100] == "刀"
    current = {path.stem for path in (R / "kanji").glob("*.md")}
    base_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in base_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {"刀"} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    word = metadata(R, SCOPE[1])
    assert "jlpt" not in word and word["kanji"] == ["日", "本", "刀"]
    activated = {f"words/{path.name}" for path in (R / "words").glob("*.md")
                 if "刀" in metadata(R, f"words/{path.name}")["kanji"]}
    assert activated == {"words/刀.md", "words/剃刀.md", "words/日本刀.md"}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"]
                 if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert len(all_pairs) == 5
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
    assert verified == 8429
    svg = (S / "batch-090-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / "刀.json") == convert("刀", svg.decode("utf-8"))
    save(S / "batch-090-draft-stroke-audit.json", dict(
        load(S / "batch-090-stroke-evidence.json"), converted=True, output="strokes/刀.json",
        outputSha256=sha((R / "strokes" / "刀.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    changed = ledger["changedReusedPassages"]
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    text += "".join(row["after"] for row in changed)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-090-font-preparation.json")["fonts"]:
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
    for c in ["力", "切"]:
        row = metadata(R, f"kanji/{c}.md")
        assert len(row["distractors"]) == 3 and "刀" not in row["distractors"]
        neighbors[c] = {"title": row["title"], "distractors": row["distractors"]}
    explicit = [path.stem for path in (R / "kanji").glob("*.md")
                if path.stem != "刀" and "刀" in metadata(R, f"kanji/{path.name}").get("distractors", [])]
    assert explicit == []
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in ["乃", "凹", "凸"])
    save(S / "batch-090-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "090", "completeNewArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE},
        "exactReusedChangedPassagesIncluded": changed,
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "Complete new articles plus exact reused after-passages. Cmap presence/absence not native legibility/fallback-face acceptance. Fresh four-font/all-Han and non-skipped RareHan/native gates pending.",
    })
    result.update(
        schemaVersion=1, execution=637, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=5, decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=5, directedLinksVerified=10, directWordExclusionPairs=1,
        legacyDefaultFallbackNeighbors=neighbors, existingExplicitTargetDistractors=explicit,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=116,
        remainingAdditions=1112, draftOnlyAdditions=["刀"], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-090-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-090-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-637.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8429" in text and result["contentVersion"] in text
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
        target = S / f"batch-090-draft-{stem}-637.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    recipe = S / "batch-090-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-637.json", {
        "schemaVersion": 1, "execution": 637, "batch": "090", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution637StartingState"],
        "runtimeDrafted": ["刀"], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "audit": "docs/n1-sources/batch-090-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-090-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-090-draft-stroke-audit.json",
        "recipe": recipe.relative_to(R).as_posix(), "recipeSha256": sha(recipe.read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock throughout coordinator16548; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helper in control. No optional historical-session-helper access.",
        "readEvidenceLimits": "All194 complete lexical families inspected in source preparation636, not re-claimed fresh here. Fresh draft reads: five applicable complete lexical families, all13 comparison families, eight complete character records, twelve existing articles, actual lexical dictionary headings and pinnedSVG.",
        "diagnostics": ["Initial receipt recording stopped on a regex that omitted the carriage return in PowerShell-redirected test output. The original exit0 log has terminal Ran372/OK followed by fixture stdout. Corrected receipt parsing to accept CRLF; no test rerun, failure concealment or content change."],
        "actualNewPermissionDenials": [], "publishedAdditions": 116, "remainingAdditions": 1112,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft check receipts and durable recipe archived.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "audit", "record"])
    globals()[parser.parse_args().phase]()
