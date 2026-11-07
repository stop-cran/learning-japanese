"""Source-bound local UNREVIEWED draft checkpoint; never publish runtime."""
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
L = C / "logs" / "e3c4d315-e520-40d1-80d1-6b10ec7a29c5"
S = R / "docs" / "n1-sources"
HEAD = "fb8a532bb0230e0576b854ba71899252cb28542b"
BASE = "1b00a924a007f32da36894ea92b05f675436e60d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "剣"
SCOPE = ["kanji/剣.md", "words/剣.md"]
REUSED = ["words/真剣.md", "kanji/真.md"]
NEXT = (
    "SAME097 TWO serial blind different-model-family initial textual reviews on the "
    "normally signed LOCAL UNREVIEWED snapshot: complete剣/剣つるぎ and exact reused "
    "真剣/真 changes; fullケン/[つるぎ] and both selected, four direct word guards, "
    "THREE all-mapped pairs/SIX directions/ONE activated baseline pair. Same frozen "
    "137 complete dictionary families/11 raw character records/public source evidence "
    "for both reviewers; correctness, scoped coverage and phone comprehensibility. "
    "Use actual available models/read-only tools and wait for actual process exit before "
    "next reviewer; preserve complete original reports/sessions/read limits, reconcile "
    "evidence and obtain bounded original-session confirmations. Then fresh non-skipped "
    "Android, production ContentSync ONCE/native N1-All/meaning/reading/drawing/article/"
    "Back/offline/four-font/all-Han/rendered review, actual combined-main acceptance, "
    "normal signing/owner fast-forward/terminal CI/EVERY immutable public ZIP runtime "
    "hash/unchanged budgets/verified owner issue. Do not start098 or push unreviewed content. "
    "Approved control/committed evidence/frozen inputs only; parent19008 retains runner.lock, "
    "no child acquire/delete/unlock/readprobe. Preserve/report/yield actual new denial/"
    "signing hang/uncertain ownership. Published123/1228,1105 acceptance remainder unchanged; "
    "physical-phone/general-release/whole-set outstanding."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".710.tmp")
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
    assert (p["checkpoint"], p["batch"], p["status"]) == (709, "097", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    before = L / "progress-before-710.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["checkpoint"] == 709
    assert checkpoint["execution709CoordinatorCheckpoint"] == p["execution709CoordinatorCheckpoint"]
    role = load(L / "preflight-710.json")
    assert role["liveParentPid"] == 19008 and role["sessionId"] == L.name and not role["lockTouched"]
    p["execution710StartingState"] = {
        "execution": 710, "batch": "097", "startingHead": HEAD, "freshOriginMain": BASE,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME097 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,098 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete approved issue and final709 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs and durable control helpers only; optional historical-session recipes not accessed.",
        "worktrees": "Wholly clean dedicated content and qualified TESTONLY Android; normal signatures G. Fresh main equals published BASE. Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain; canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-097-runtime-draft-in-progress",
             nextAction=p["execution710StartingState"]["scope"], blocker=None)
    save(C / "progress.json", p)
    print("SAME097 runtime-draft scope persisted; complete historical values preserved.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    proof = load(S / "batch-097-stroke-evidence.json")
    svg = (S / "batch-097-kanjivg.svg").read_bytes()
    assert sha(svg) == proof["sha256"] and svg == Path(proof["input"]).read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 10
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-097-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [108]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR])
    frozen["limits"] = "LOCAL UNREVIEWED draft only, not review closure, native acceptance or publication."
    save(S / "batch-097-membership.json", frozen)
    p = load(S / "batch-097-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR], runtimeChanged=True)
    p["dictionaryPackets"] = [
        {"selection": "batch-097-lexical-selection.json", "xml": "batch-097-jmdict.xml"},
        {"selection": "batch-097-comparison-selection.json", "xml": "batch-097-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"],
                   article="words/真剣.md" if row["kind"] == "on" else "words/剣.md",
                   reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
         "entryIds": [row["entryId"]], "newArticle": row["newArticle"],
         "allWrittenKanji": row["allWrittenKanji"], "wordJlpt": row["wordJlpt"],
         "selectedSenses": row["selectedSenses"], "status": "local-unreviewed-draft"}
        for row in p["proposedSupportMapping"]
    ]
    p["requiredReciprocalPairs"] = [[CHAR, r["article"]] for r in p["supportMappings"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = [
        {"article": "words/真剣.md",
         "before": '[真](../kanji/真.md) contributes "true; real," and 剣 means "sword."',
         "after": '[真](../kanji/真.md) contributes "true; real," and [剣](../kanji/剣.md) means "sword."'},
        {"article": "kanji/真.md",
         "before": "## Common words\n\n- [写真](../words/写真.md) しゃしん — photograph\n",
         "after": "## Common words\n\n- [写真](../words/写真.md) しゃしん — photograph\n- [真剣](../words/真剣.md) しんけん — serious; earnest; also a real sword\n"},
    ]
    p["curatedProjection"] = [p["proposedCuratedProjection"]]
    p["quizAudit"] = {CHAR: {
        "title": p["proposedQuiz"]["kanjiTitle"], "distractors": p["proposedQuiz"]["distractors"],
        "labels": p["proposedQuiz"]["labels"], "meaningDecisions": p["proposedQuiz"]["rationale"],
        "unsafeComparisons": p["proposedQuiz"]["unsafeComparisons"],
        "limits": "Default-four fallback unnecessary; independent semantic and production N1/All review pending.",
    }}
    exclusions = [r["words"][1] for r in p["proposedQuiz"]["proposedDirectExclusions"]]
    p["wordQuizAudit"] = {
        "directExclusions": [{"word": CHAR, "exclude": exclusions,
                              "reasons": p["proposedQuiz"]["proposedDirectExclusions"]}],
        "finalLabelAudit": {
            "proposedGuards": 4, "actualGuards": 4,
            "navigation": "Existing title scan for sword/blade/sabre/saber/dagger/knife/clock hand found刀,日本刀,刃,ナイフ,包丁,針,斬る. Complete actual articles freshly read; full relevant frozen comparison families freshly read. 刀,日本刀,刃 and literal secondary真剣 warrant direct guards. Knife/kitchen-knife labels are not sword;針's clock-hand sense is not established for standaloneつるぎ. 斬る's slash/cut-down verb is not the sword noun; no extra guard.",
            "confusableInventory": "Candidate guidance and sword/blade/剣/刃/刀 search inspected (no matching row); inventory absence is not semantic evidence.",
            "limits": "Four direct pairs only, not a transitive clique, unrestricted substitution or all-pool live certification.",
        },
    }
    p["draftAuthorInspection"] = {
        "execution": 710, "sourceCheckpoint": HEAD,
        "freshCompleteSelectedFamilies": ["1256750", "1256770", "1256910", "1363650"],
        "freshCompleteComparisonFamilies": 17,
        "inheritedSourceInspection": "Source709 complete122 member families/11 raw character records/20 articles retained in committed evidence. Unselected lexical families are freshly byte-bound to frozen dictionary, not all freshly semantically reread in710.",
        "rawCharacterScope": "Complete剣 record freshly read; comparison raw records inherited709 and freshly byte-bound. No historical/phonetic claim derived from SVG.",
        "freshExistingArticles": ["words/真剣.md", "kanji/真.md", "words/刀.md", "words/日本刀.md",
            "words/刃.md", "words/ナイフ.md", "words/針.md", "words/包丁.md", "words/斬る.md",
            "kanji/剛.md", "kanji/剖.md", "kanji/則.md"],
        "publicLookup": "Committed actual Digital Daijisen剣/真剣 entry text freshly read; archived coordinator source evidence, not fresh upstream retrieval. Character extract1-100 read; later unrelated product/place/navigation content inherited709.",
        "pinnedSvg": "Complete committed SVG freshly read; ten paths. Rare component/phon attributes not printed as etymology or necessary learner glyphs.",
        "exampleProvenance": "Original ordinary museum/photograph noun examples, not dictionary quotations or evidence of rare collocation/frequency.",
        "limits": "Author inspection only, not independent review, native-speaker certification, phone evidence or uniform reviewer comprehension.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no reviewer, fresh Android/native/font/phone acceptance or runtime publication.",
        "Fullケン/[つるぎ] retained in original order and both explicitly selected. Valid standaloneけん mentioned without importing its restricted senses intoつるぎ.",
        "One necessary剣つるぎ support with no inferred word level; reused真剣しんけん N3 metadata/readings/originalまじめ guard unchanged.",
        "THREE all-mapped pairs/SIX directions/ONE activated baseline pair. Two exact reused navigation changes, no broader rewrite or metadata change.",
        "Four direct word guards after actual final-label/article/family inspection, not transitive cliques or unrestricted substitutions.",
        "Labelled modern-shape mnemonic only, structure-unclassified, no phonetic/history claim. Canonical刀18 retained, visible刂 explained; ten pinned paths generated.",
        "Final Han/cmap audit is not native glyph/fallback acceptance. Fresh non-skipped Android/native/four-font/all-Han/rendered review pending.",
        "Published123/1228 and1105 acceptance remainder unchanged. Six earlier-level source保案派第策結 remain separate;妖exception preserved.",
        "CompatibleAndroidf9b59a2+ required; qualified TESTONLY1c1b7bf4 not latest appmain. Physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates retained; no098 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-097-progress.json", p)
    print("Ten pinned paths and local UNREVIEWED ledgers prepared; four direct guards retained.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "097")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(kd)) == snapshot["kanjidic2"]["xmlSha256"]
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    ledger = load(S / "batch-097-progress.json")
    packets = []
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt" if i == 0 else "comparison-full-family-reading.txt"
        compact = gzip.decompress((S / f"batch-097-{suffix}.gz").read_bytes())
        assert [canonical(e) for e in ET.fromstring("<JMdict>" + compact.decode("utf-8") + "</JMdict>")] == [
            canonical(e) for e in ET.fromstring(raw)]
        packets.append({"path": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    count = 0
    for name in ["batch-097-kanjidic2.xml", "batch-097-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(records[entry.findtext("literal")])
            count += 1
    assert count == 11
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
    assert named == load(S / "community-list-20261102.json") and named[107] == CHAR
    current = {p.stem for p in (R / "kanji").glob("*.md")}
    old_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    old = {Path(n).stem for n in old_manifest["files"] if n.startswith("kanji/")}
    assert current - old == {CHAR} and not old - current
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    for c in "保案派第策結":
        assert metadata(R, f"kanji/{c}.md")["jlpt"] == 2
    word = metadata(R, "words/剣.md")
    assert "jlpt" not in word and word["kanji"] == [CHAR] and word["reading"] == "つるぎ"
    assert metadata(R, "words/真剣.md")["jlpt"] == 3
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/剣.md", "words/真剣.md"}
    all_pairs = {(c, row["article"]) for row in ledger["supportMappings"]
                 for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").is_file()}
    assert all_pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert len(all_pairs) == 3
    for c, name in all_pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{c}.md").read_text(encoding="utf-8")
    assert len(word["quiz_exclusions"]) == 4
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
    assert verified == 8447
    svg = (S / "batch-097-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-097-draft-stroke-audit.json", dict(
        load(S / "batch-097-stroke-evidence.json"), converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / "strokes" / f"{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    text = "".join((R / n).read_text(encoding="utf-8") for n in SCOPE)
    text += "".join(row["after"] for row in ledger["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-097-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    save(S / "batch-097-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "097", "completeArticleScope": SCOPE,
        "changedReusedScope": ledger["changedReusedPassages"],
        "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in SCOPE + REUSED}, "fonts": fonts,
        "rareHanRangeCharacters": [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF
            or 0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF],
        "nativeFontAcceptance": "pending", "limits": "Cmap evidence only, not glyph/fallback acceptance; fresh four-font/all-Han/native gates pending. Unchanged reused article text outside exact diff is inherited, not a fresh font acceptance scope.",
    })
    for c in "剛剖則刀刃針真険験":
        assert len(metadata(R, f"kanji/{c}.md")["distractors"]) == 3
    unchanged = 0
    for name, expected in load(S / "batch-097-preparation-audit.json")["inspectedArticleHashes"].items():
        if name not in REUSED:
            assert sha((R / name).read_bytes()) == expected, name
            unchanged += 1
    assert unchanged == 18
    for name in REUSED:
        before_text = git("show", f"{BASE}:{name}") + "\n"
        before_meta = metadata(R, name)
        import yaml
        assert before_meta == yaml.safe_load(before_text.split("---", 2)[1])
    result.update(
        schemaVersion=1, execution=710, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=len(snapshot["inputs"]), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=3, directedLinksVerified=6, newDirectWordExclusionPairs=4,
        actualFinalExcludedLabels=final_labels, originalSourcePreparationArticlesByteUnchanged=18,
        reusedMetadataPreserved=REUSED,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=123,
        remainingAdditions=1105, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-097-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    result = load(S / "batch-097-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]:
        raw = (L / f"{stem}-710.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8447" in text and result["contentVersion"] in text
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
        target = S / f"batch-097-draft-{stem}-710.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(), "sha256": sha(packed),
                         "uncompressedSha256": sha(raw)}
    for source, target in [
        (Path(__file__), S / "batch-097-draft-recipe.py"),
        (C / "preflight-710.ps1", S / "batch-097-draft-preflight-710.ps1.txt"),
        (C / "checks-batch-097-draft-710.ps1", S / "batch-097-draft-checks-710.ps1.txt"),
    ]:
        target.write_bytes(source.read_bytes())
    save(S / "execution-710.json", {
        "schemaVersion": 1, "execution": 710, "batch": "097", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": BASE, "runtimePublished": False,
        "startingState": load(C / "progress.json")["execution710StartingState"],
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "pythonTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "focusedTestCommand": "python -X utf8 -B -m unittest test_freeze_n1_sources test_extract_n1_jmdict test_audit_n1_pilot test_audit_n1_batch; PYTHONPATH=tools",
        "vocabularyLimits": "Existing reviewed-prompt consistency only, not unrelated coverage completion.",
        "audit": "docs/n1-sources/batch-097-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-097-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-097-draft-stroke-audit.json",
        "recipe": "docs/n1-sources/batch-097-draft-recipe.py", "recipeSha256": sha(Path(__file__).read_bytes()),
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Live parent19008 owns runner.lock; child never acquires/deletes/unlocks/read-probes.",
        "artifactPathPreflight": "Approved workspace/frozen inputs/committed evidence only; reusable helpers in control.",
        "readEvidenceLimits": load(S / "batch-097-progress.json")["draftAuthorInspection"],
        "actualNewPermissionDenials": [], "publishedAdditions": 123, "remainingAdditions": 1105,
        "finalLabelAuditChange": "Four proposed direct guards retained after final-label audit; additional斬る verb article inspected without new guard or teaching change.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"], "nextAction": NEXT,
    })
    print("Draft receipts and durable recipes archived.")


def freeze():
    identity(drafted=True)
    assert not git("status", "--porcelain")
    signed = git("rev-parse", "HEAD")
    expected = set(SCOPE + REUSED) | {f"strokes/{CHAR}.json", "manifest.json",
        "docs/n1-sources/batch-097-membership.json", "docs/n1-sources/batch-097-progress.json",
        "docs/n1-sources/batch-097-draft-audit.json", "docs/n1-sources/batch-097-draft-font-audit.json",
        "docs/n1-sources/batch-097-draft-stroke-audit.json", "docs/n1-sources/batch-097-draft-recipe.py",
        "docs/n1-sources/batch-097-draft-preflight-710.ps1.txt",
        "docs/n1-sources/batch-097-draft-checks-710.ps1.txt", "docs/n1-sources/execution-710.json",
    } | {f"docs/n1-sources/batch-097-draft-{n}-710.txt.gz"
         for n in ["validate", "manifest", "audit", "tests", "vocabulary", "budget", "whitespace"]}
    changed = set(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", signed],
        encoding="utf-8").rstrip("\0").split("\0"))
    assert changed == expected, changed ^ expected
    from build_manifest import build_manifest
    assert build_manifest(R) == load(R / "manifest.json")
    result = load(S / "batch-097-draft-audit.json")
    evidence = load(S / "execution-710.json")
    before = load(L / "progress-before-710.json")
    p = load(C / "progress.json")
    checkpoint = {
        "schemaVersion": 1, "execution": 710, "checkpoint": 710, "batch": "097",
        "status": "continue", "stage": "local-unreviewed-draft", "savedCommit": signed,
        "signature": "G", "sourceCommit": HEAD, "lastPublishedCommit": BASE,
        "membership": [CHAR], "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "runtimePublished": False, "dedicatedWorktreesClean": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 123, "remainingAdditions": 1105,
        "pythonTestsPassed": evidence["pythonTestsPassed"], "validatorErrors": 0,
        "contentVersion": result["contentVersion"], "allRuntimePayloadHashesVerified": 8447,
        "allMappedReciprocalPairs": 3, "directedLinksVerified": 6, "activatedBaselinePairs": 1,
        "metadataReadingDispositions": 2, "curatedOfferedKeys": 2, "newSupportArticles": 1,
        "changedReusedArticles": 2, "newDirectWordExclusionPairs": 4, "dictionaryFamilies": 137,
        "actualHanCount": result["actualHanCount"], "pendingNativeFallbackLabels": result["pendingNativeFallbackLabels"],
        "sourcePacket": "docs/n1-sources/batch-097-progress.json",
        "audit": "docs/n1-sources/batch-097-draft-audit.json", "evidence": "docs/n1-sources/execution-710.json",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False, "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "actualNewPermissionDenials": [], "nextAction": NEXT,
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
    }
    p["execution710StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution710CoordinatorCheckpoint"] = checkpoint
    p["batch097LocalUnreviewedDraft"] = copy.deepcopy(checkpoint)
    p.update(checkpoint=710, status="continue", stage="batch-097-local-unreviewed-draft",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    save(L / "checkpoint-710.json", checkpoint)
    body = (
        f"Batch097: signed LOCAL UNREVIEWED draft checkpoint710, not publication.\n\n"
        f"Saved `{signed}` (normal signature G), source `{HEAD}`; remote main remains `{BASE}`. "
        "New 剣 card, necessary 剣つるぎ support article without inferred vocabulary level, "
        "and ten generated pinned KanjiVG strokes. Fullケン/[つるぎ] preserved and both "
        "selected. Existing真剣しんけん retains N3 metadata/readings/originalまじめ guard; "
        "only its component link and one真 common-word backlink change. THREE all-mapped "
        "pairs/SIX directions/ONE activated baseline pair. Four direct word guards "
        "(刀,日本刀,刃,真剣) after final-label audit, not a transitive clique or an "
        "absolute single-edge/double-edge taxonomy.\n\n"
        "Evidence: `docs/n1-sources/execution-710.json` and draft audit/font/stroke records. "
        "Frozen137 complete dictionary families/11 raw character records freshly byte-bound; "
        f"baseline metadata/strokes and all8447 runtime hashes audited. Complete new-article/"
        f"exact changed-reused Han inventory{result['actualHanCount']}; main-font cmap absences "
        f"{''.join(result['pendingNativeFallbackLabels'])}, not native glyph acceptance.\n\n"
        "Next: TWO serial blind different-family textual reviews on this snapshot, "
        "evidence reconciliation/original-session confirmations, fresh non-skipped Android/"
        "native/four-font/all-Han/rendered and combined-main/CI/every immutable ZIP hash "
        "gates. No reviewer, Android/native run, runtime push or098 in this checkpoint. "
        "Published123/1228;1105 acceptance remainder unchanged. Compatible curated-reading "
        "APK required; physical-phone/general-release/whole-set outstanding. Approved "
        "workspace/control artifacts only; live parent's runner.lock untouched.\n"
    )
    (C / "batch-097-draft-710-issue.txt").write_bytes(body.encode("utf-8"))
    print(json.dumps(checkpoint, ensure_ascii=False, indent=2))


def issue():
    posted = load(L / "issue-710-posted.json")
    actual = load(L / "issue-710-reread.json")
    raw = (C / "batch-097-draft-710-issue.txt").read_bytes()
    assert posted["id"] == actual["id"] and actual["user"]["login"] == "stop-cran"
    assert actual["body"].encode("utf-8") == raw
    receipt = {"id": actual["id"], "url": actual["html_url"], "author": "stop-cran",
               "bodySha256": sha(raw), "verified": True, "comparison": "Exact UTF-8 bytes."}
    p = load(C / "progress.json")
    before = load(L / "progress-before-710.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (710, "097", "continue")
    assert git("rev-parse", "HEAD") == p["execution710CoordinatorCheckpoint"]["savedCommit"]
    assert git("rev-parse", "origin/main") == BASE
    for root in (R, A):
        assert not git("status", "--porcelain", root=root)
        assert git("log", "-1", "--format=%G?", root=root) == "G"
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    for key in ["execution710CoordinatorCheckpoint", "batch097LocalUnreviewedDraft"]:
        p[key]["issueUpdate"] = receipt["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    p["batch097DraftIssueReceipt"] = receipt
    assert all(p[k] == v for k, v in before.items()
               if k not in {"checkpoint", "status", "stage", "nextAction", "blocker"})
    save(C / "progress.json", p)
    save(L / "checkpoint-710.json", p["execution710CoordinatorCheckpoint"])
    save(C / "batch-097-draft-710-issue-receipt.json", receipt)
    print("Owner issue bytes, signed clean heads and complete historical values verified.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("step", choices=["start", "prepare", "audit", "record", "freeze", "issue"])
    globals()[parser.parse_args().step]()
