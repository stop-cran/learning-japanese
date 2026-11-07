"""Generate and audit the source-bounded, local unreviewed batch089 draft."""
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
L = C / "logs" / "e564a197-4880-41fd-a440-46abb05b4a82"
S = R / "docs" / "n1-sources"
HEAD = "0a192edaf05a6aaeaaed9482dbe865e367887f1f"
BASE = "703ebf5fba412aefdc516ea18b36658d227631d1"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
SCOPE = ["kanji/凶.md", "words/凶作.md"]
NEXT = (
    "SAME089 two serial blind different-model-family initial textual reviews on the normally signed "
    "LOCAL UNREVIEWED snapshot: complete凶/凶作 and exact additive作 navigation diff, sole full/selected"
    "キョウ and explicitkun[], complete applicable dictionary families, agricultural modifier+head "
    "作crop/yield, noun/not harvest verb, verypoor versus zeroyield/famine/ordinary badwork, original "
    "rice/cold-damage examples and translations, 不作/豊作 comparisons, labelled shape-only mnemonic, "
    "three N1 curated wrong labels, one direct収穫guard and two allmappedpairs/four directions, "
    "correctness/scopedcoverage/phonecomprehensibility. Use actual available models/read-only tools; "
    "freeze edits and verify actual process exit before next reviewer. Preserve full reports, actual "
    "models/readlimits/originalsessions; reconcile and confirm necessary fixes. Then fresh non-skipped "
    "Android, native full production ContentSync ONCE, N1/All production choices/reading/drawing/article/"
    "Back/offline/fourfont and bounded visual acceptance, combined current-main/normal signing/owner "
    "fast-forward/terminal green CI/EVERY immutable ZIP runtime hash/original budgets/verified ownerissue "
    "gates. No090 or unreviewed push. Parent19008 retains lock untouched. Published115/1228 and1113 "
    "acceptance-remainder unchanged; physicalphone/generalrelease/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temp = path.with_suffix(path.suffix + ".628.tmp")
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
    assert p["checkpoint"] == 627 and p["batch"] == "089" and p["status"] == "continue"


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    svg = (S / "batch-089-kanjivg.svg").read_bytes()
    stroke = load(S / "batch-089-stroke-evidence.json")
    assert sha(svg) == stroke["sha256"]
    assert KANJIVG_REVISION == stroke["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == stroke["converterNormalizedSha256"]
    geometry = convert("凶", svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 4
    target = R / "strokes" / "凶.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-089-membership.json")
    assert frozen["membership"] == ["凶"] and frozen["sourceRows"] == [98]
    frozen["members"] = [{"kanji": "凶", "sourceRow": 98}]
    frozen.update(status="local-unreviewed-draft", drafted=["凶"])
    save(S / "batch-089-membership.json", frozen)
    p = load(S / "batch-089-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=["凶"])
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"], reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": "凶", "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": True, "allWrittenKanji": row["allWrittenKanji"],
         "wordJlpt": None, "selectedSenses": row["selectedTeaching"], "status": "local-unreviewed-draft"}
        for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = [["凶", "words/凶作.md"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["pairScopeQualification"] = "Generic batch auditor checks the new-member support mapping. Separate all-mapped audit also requires existing作, yielding two pairs/four directions, not one pair."
    before = "- 作業 さぎょう — work; task; operation\n"
    after = before + "- [凶作](../words/凶作.md) きょうさく — poor harvest; crop failure\n"
    p["changedReusedPassages"] = [{"article": "kanji/作.md", "before": before, "after": after,
                                  "scope": "One additive navigation/example line; existing metadata/body otherwise unchanged."}]
    p["curatedProjection"] = [dict(p["proposedCuratedProjection"], kanji="凶")]
    card = metadata(R, SCOPE[0])
    p["quizAudit"] = {"凶": {
        "title": card["title"], "distractors": card["distractors"],
        "labels": [metadata(R, f"kanji/{c}.md")["title"] for c in card["distractors"]],
        "meaningDecisions": p["proposedQuiz"]["evidence"],
        "legacyFallbackDisposition": p["proposedQuiz"]["legacyFallback"],
        "limits": "Three N1-available wrong cards; actual production N1/All options pending. Not universal custom/random-pool certification.",
    }}
    p["wordQuizAudit"] = {
        "titles": {"凶作": metadata(R, SCOPE[1])["title"]},
        "directExclusions": p["proposedQuiz"]["proposedDirectExclusions"],
        "notExcluded": p["proposedQuiz"]["notExcluded"],
        "confusableInventory": p["proposedQuiz"]["confusableInventory"],
        "limits": "One conservative pairwise displayed-label safeguard, not transitive closure or unrestricted substitution.",
    }
    p["draftAuthorInspection"] = {
        "execution": 628, "sourceCheckpoint": HEAD,
        "completeFreshPacketReads": {
            "batch-089-kanjidic2.xml": "complete1-77EOF",
            "batch-089-jmdict.xml": [[1, 330], [331, 660], [661, 958]],
            "batch-089-comparison-jmdict.xml": [[1, 265], [266, 522]],
            "batch-089-comparison-kanjidic2.xml": [[1, 205], [206, 406]],
            "batch-089-kyou-public-text.txt": "complete throughEOF",
            "batch-089-kyousaku-public-text.txt": "complete throughEOF",
            "batch-089-kanjivg.svg": "complete throughEOF",
        },
        "completeExistingArticlesRead": ["kanji/作.md", "kanji/凡.md", "kanji/凸.md", "kanji/凹.md",
            "kanji/悪.md", "words/作物.md", "words/収穫.md", "words/取り入れる.md",
            "words/不運.md", "words/不幸.md", "words/災難.md"],
        "lexicalDecisions": "All55 exact-member and18 comparison families freshly inspected complete. Only1235440 selected for a necessary new article; complete1297240 sense2 verifies作crop/yield. No extra kun inferred from dictionary glosses. Every other family retains source-preparation disposition.",
        "exampleProvenance": "Original full sentences, not quotations. 米poorharvest and冷害causation supported by archivedNipponica; Daijisen二年続きの凶作 supports consecutiveyear context. Grammar/translations author-inspected; independent naturalness review still pending.",
        "publicLookup": "Fresh read of committed coordinator-extracted actual dictionary text, not independent upstream retrieval. Original HTML/extraction/image-placeholder/historical limits remain.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no independent reviewer, fresh Android/native/font/phone acceptance or publication.",
        "Sole raw/selected onキョウ preserved, source kun[] and explicitquizkun[]. Exact dictionary pair/Daijisen character reading, not a kana-substring allocation or frequency inference.",
        "One necessary new support凶作, metadata凶and作, no wordJLPT inferred. Agricultural noun/verypooryield, not badwork/harvestverb/necessaryzeroyield/famine; full original sentences await independent naturalness review.",
        "Existing runtime bytes/identities/levels/readings/exclusions unchanged except one recorded additive作navigation line. One new kanji/word/generatedstroke; two allmappedpairs/four directions include reused作.",
        "Three N1-available curated wrong cards and one direct収穫guard; semantic author audit not universal livepool certification. Actual N1/All production checks pending.",
        "Exact final Han/cmap inventory is not native legibility or fallback-face acceptance. Fresh fourfont/allHan rendering and non-skipped RareHan/native gates pending; pilot all40 remains historical.",
        "Published115/1228 and1113 acceptance-remainder unchanged. Six separate source保案派第策結 retain earlierN2levels and are not accepted issue60 additions; separate妖exception retained.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest appmain; physicalphone/generalrelease/whole-set outstanding.",
        "All original source/review/process/denial/OOM/readdepth/native/combinedmain/signing/ownerpush/terminalCI/EVERYimmutableZIPhash/budget/ownerissue gates remain. No optional historicalsessionhelpers, parentlock touch,090 or secondrunner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-089-progress.json", p)
    print("Four pinned paths generated; exact source/member and LOCAL UNREVIEWED ledger prepared.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "089")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    ledger = load(S / "batch-089-progress.json")
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
    for name in ["batch-089-kanjidic2.xml", "batch-089-comparison-kanjidic2.xml"]:
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
    assert named == load(S / "community-list-20261102.json") and named[97] == "凶"
    current = {path.stem for path in (R / "kanji").glob("*.md")}
    base_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in base_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {"凶"} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    word = metadata(R, SCOPE[1])
    assert "jlpt" not in word and word["kanji"] == ["凶", "作"]
    assert {f"words/{path.name}" for path in (R / "words").glob("*.md")
            if "凶" in metadata(R, f"words/{path.name}")["kanji"]} == {SCOPE[1]}
    all_pairs = {(c, SCOPE[1]) for c in word["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} == {("凶", SCOPE[1]), ("作", SCOPE[1])}
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
    assert verified == 8426
    svg = (S / "batch-089-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / "凶.json") == convert("凶", svg.decode("utf-8"))
    save(S / "batch-089-draft-stroke-audit.json", dict(
        load(S / "batch-089-stroke-evidence.json"), converted=True, output="strokes/凶.json",
        outputSha256=sha((R / "strokes" / "凶.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-089-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    neighbor = metadata(R, "kanji/悪.md")
    assert len(neighbor["distractors"]) == 3 and "凶" not in neighbor["distractors"]
    explicit = [path.stem for path in (R / "kanji").glob("*.md")
                if path.stem != "凶" and "凶" in metadata(R, f"kanji/{path.name}").get("distractors", [])]
    assert explicit == []
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in ["凡", "凸", "凹"])
    save(S / "batch-089-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "089", "completeNewArticleScope": SCOPE,
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE},
        "navigationOnlyReusedScope": ledger["changedReusedPassages"],
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "Actual complete new articles; added作navigation contains no additionalHan. Cmap presence/absence not native legibility/fallback-face acceptance. Fresh fourfont/allHan and non-skipped RareHan/native gates pending.",
    })
    result.update(
        schemaVersion=1, execution=628, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=5, decompressedDictionaryHashesVerified=2, packets=packets,
        completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=2, directedLinksVerified=4, directWordExclusionPairs=1,
        legacyDefaultFallbackNeighbors={"悪": {"title": neighbor["title"], "distractors": neighbor["distractors"]}},
        existingExplicitTargetDistractors=explicit, allRuntimePayloadHashesVerified=verified,
        actualHanCount=len(han), pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=115,
        remainingAdditions=1113, draftOnlyAdditions=["凶"], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-089-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-089-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-628.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8426" in text and result["contentVersion"] in text
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
        target = S / f"batch-089-draft-{stem}-628.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    recipe = S / "batch-089-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-628.json", {
        "schemaVersion": 1, "execution": 628, "batch": "089", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "runtimeDrafted": ["凶"], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "audit": "docs/n1-sources/batch-089-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-089-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-089-draft-stroke-audit.json",
        "recipe": recipe.relative_to(R).as_posix(), "recipeSha256": sha(recipe.read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock throughout coordinator26512; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helper in control. No optional historicalsessionhelper access.",
        "diagnostics": [
            "Initial complete request read/JSON parse succeeded, then console cp1252 print failed. Set PYTHONUTF8/PYTHONIOENCODING for subsequent commands; inspected final request ranges directly.",
            "Added exact凶/sourceRow98 members projection required by existing auditor; immutable frozen membership/sourceRows/source-index untouched.",
            "Existing generic auditor permits supportMappings only for new members. Kept its one凶pair explicit; independently enumerated/verified both凶andexisting作 allmappedpairs/fourdirections.",
        ],
        "actualNewPermissionDenials": [], "publishedAdditions": 115, "remainingAdditions": 1113,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft check receipts and durable recipe archived.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=["prepare", "audit", "record"])
    globals()[parser.parse_args().phase]()
