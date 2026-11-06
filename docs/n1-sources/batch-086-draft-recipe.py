"""Bounded local draft evidence; the launcher retains runner.lock untouched."""
import argparse
import ast
import copy
import difflib
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
S = R / "docs" / "n1-sources"
L = C / "logs" / "0a586287-ab81-4809-a71e-592bd41c136e"
HEAD = "553348453ccd627801782e95e9c83ab9c5e73a7b"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u51e1"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".601.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def check_context(clean=False):
    assert git("rev-parse", "HEAD") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    if clean:
        assert not git("status", "--porcelain")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (600, "086", "continue")
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name


def prepare():
    from extract_n1_jmdict import extract
    from generate_strokes import convert
    from audit_n1_pilot import metadata
    check_context()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    raw = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    expected = snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"]
    assert hashlib.sha256(raw).hexdigest() == expected
    root = ET.fromstring(gzip.decompress(raw))
    words = ["メモ", "筆記", "はじめに", "初めに", "始めに", "概論", "鍵", "栞",
             "常", "般"]
    ids = [e.findtext("ent_seq") for e in root.findall("entry")
           if any(x.text in words for x in e.findall("k_ele/keb") + e.findall("r_ele/reb"))]
    selection = {"schemaVersion": 1, "batch": "086", "entryIds": ids,
                 "exactSpellings": words, "sourceSnapshot": "docs/n1-source-snapshot.json",
                 "limits": "Full label-neighbor families; extraction alone is not semantic inspection."}
    save(S / "batch-086-draft-comparison-selection.json", selection)
    (S / "batch-086-draft-comparison-jmdict.xml").write_bytes(extract(raw, expected, ids))
    svg = (S / "batch-086-kanjivg.svg").read_bytes()
    stroke = load(S / "batch-086-stroke-evidence.json")
    assert len(svg) == stroke["bytes"] and hashlib.sha256(svg).hexdigest() == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(
        b"\r\n", b"\n")).hexdigest() == stroke["converterNormalizedSha256"]
    data = convert(CHAR, svg.decode("utf-8"))
    assert data["strokeCount"] == 3 and data["sourceRevision"] == stroke["revision"]
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    p = load(S / "batch-086-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR])
    p["dictionaryPackets"] = [
        {"selection": f"batch-086-{name}selection.json", "xml": f"batch-086-{xml}jmdict.xml"}
        for name, xml in [("lexical-", ""), ("comparison-", "comparison-"),
                          ("draft-comparison-", "draft-comparison-")]
    ]
    for row in p["readingDispositions"]:
        row.update(selected=row["proposedQuizSelection"],
                   reason=row["qualification"] + " " + row["evidence"])
    p["supportMappings"] = [{
        "kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
        "entryIds": [row["entryId"]], "newArticle": row["word"] == "凡例",
        "allWrittenKanji": row["allWrittenKanji"], "wordJlpt": row["preservedWordJlpt"],
        "selectedSenses": row["selectedTeaching"], "status": "local-unreviewed-draft",
    } for row in p["proposedSupportMapping"] if row["word"] in ["平凡", "凡例"]]
    p["recognitionAliasMappings"] = [{
        "kanji": CHAR, "article": row["article"], "primaryReading": row["primaryReading"],
        "entryIds": [row["entryId"]], "spelling": row["recognitionSpellings"][0],
        "qualification": row["selectedTeaching"],
    } for row in p["proposedSupportMapping"] if "recognitionSpellings" in row]
    p["requiredReciprocalPairs"] = [[CHAR, row["article"]] for row in p["supportMappings"]]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["mappingAuditScope"] = (
        "Existing batch tool verifies primary written identities in supportMappings. "
        "Recognition aliases are checked separately against exact full spelling/reading families, "
        "without changing primary IDs/kanji metadata. All seven pairs/fourteen directions audited.")
    p["curatedProjection"] = [dict(p["proposedCuratedProjection"], kanji=CHAR)]
    changed = ["words/平凡.md", "words/およそ.md", "words/全て.md",
               "kanji/平.md", "kanji/例.md", "kanji/全.md"]
    p["changedReusedPassages"] = []
    for name in changed:
        old = subprocess.check_output(["git", "show", f"{p['baseCommit']}:{name}"]).decode("utf-8")
        before = old.replace("\r\n", "\n").splitlines(keepends=True)
        after = (R / name).read_text(encoding="utf-8").splitlines(keepends=True)
        for group in difflib.SequenceMatcher(a=before, b=after).get_grouped_opcodes(n=1):
            p["changedReusedPassages"].append({
                "article": name, "before": "".join(before[group[0][1]:group[-1][2]]),
                "after": "".join(after[group[0][3]:group[-1][4]]),
                "reason": "Exact recognition-alias clarification" if name == "words/全て.md"
                          else "Navigation only; original metadata and other teaching preserved.",
            })
    card = metadata(R, f"kanji/{CHAR}.md")
    p["quizAudit"] = {CHAR: {
        "title": card["title"], "distractors": card["distractors"],
        "labels": [metadata(R, f"kanji/{c}.md")["title"] for c in card["distractors"]],
        "meaningDecisions": p["proposedQuiz"]["evidence"],
        "legacyFallbackDisposition": "Related常/般/全/毎/各/皆/総/平 and all displayed-title neighbors have three curated slots. No new default four-choice fallback slot or explicit凡 distractor. Actual production N1/All choices remain Android/native gates; no exhaustive pool claim.",
    }}
    guards = metadata(R, "words/凡例.md")["quiz_exclusions"]
    p["wordQuizAudit"] = {
        "titles": {"凡例": metadata(R, "words/凡例.md")["title"]},
        "directExclusions": [{"word": "凡例", "exclude": guards,
                              "reason": "Direct label guards, not transitive cliques or unrestricted Japanese substitution."}],
        "decisions": [
            {"words": ["注", "説明", "解説"], "reason": "Explanatory note/explanation and説明's actual legend sense overlap."},
            {"words": ["メモ", "筆記"], "reason": "Broad note labels and recorded notes can be accepted for explanatory notes; conservative direct guards."},
            {"words": ["はじめに", "概論"], "reason": "Introductory remarks/usage introduction overlap in broad English; no claim every preface or subject survey is a凡例."},
            {"words": ["鍵"], "reason": "Bare English key also means a map legend. Label safeguard only, not a claim that Japanese鍵 normally names map legends."},
        ],
        "unselectedNeighbors": [
            {"words": ["栞"], "reason": "Guidebook/bookmark is a publication/page marker, not itself the conventions or symbol legend. Related books tags alone do not require exclusion."},
            {"words": ["例", "判例"], "reason": "Example/precedent or judicial case is not explanatory conventions. Same sound or written component alone does not establish overlap."},
        ],
        "confusableInventory": "Introductory contract and exact relevant spelling search plus displayed-title navigation; no direct凡/凡例 row. Not an exhaustive semantic rereview.",
        "limits": "Targeted full-family/actual-label audit; native pools and independent review remain pending.",
    }
    p["draftAuthorInspection"] = {
        "execution": 601, "sourceCheckpoint": HEAD,
        "freshCompletePacketReads": {"batch-086-jmdict.xml": [[1,245],[246,490],[491,735],[736,980]],
                                    "batch-086-comparison-jmdict.xml": [[1,180],[181,360]],
                                    "batch-086-kanjidic2.xml": "complete through EOF76",
                                    "batch-086-comparison-kanjidic2.xml": [[1,245],[246,490]]},
        "publicLookup": "Fresh Daijisen凡 character entry and凡例 exact heading inspected; character response truncated in later Jitsu compounds, not origin evidence. Committed original page archives/limitations retained.",
        "existingArticleScope": changed + [f"kanji/{c}.md" for c in ["丸","九","凹","常","般"]]
                               + [f"words/{w}.md" for w in ["注","説明","解説","メモ","筆記","はじめに","概論","鍵","栞"]],
        "supplementRead": "Complete returned ranges1-220/221-440 through EOF246 inspected: all10 families, kana-onlyメモ,はじめに section-heading sense,筆記 notes/exam senses,鍵かぎ versusけん, rareとわ and栞guidebook. No般 standalone family found; existing complete般 article inspected, no absence-of-compound claim. Not independent review.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only. No reviewer, fresh Android/native/font/phone acceptance or publication here.",
        "All five full raw readings/order retained. Onlyボン/ハン offered; explicit kun[] suppresses all native questions including unmatchedおうよ.そ. Raw reading's modern use remains unverified, not corrected or invented.",
        "Exact rare spelling凡て and usually-kana凡そ are recognition aliases through stable全て/およそ, not new IDs or vocabulary levels. All reused metadata/readings/levels/exclusions retained.",
        "Eight direct new-word guards are label safeguards, not transitive or unrestricted equivalence. Three curated wrong kanji choices avoid default padding; actual N1/All/live/custom pools not certified.",
        "Final cmap audit is not actual glyph/native/fallback-face evidence. Original all40 inspections inherited; new native/font acceptance pending.",
        "Published112/1228 and1116 acceptance-remainder unchanged. Six separately placed source保案派第策結 retain earlierN2levels and are not issue60accepted additions; do not duplicate/relevel.",
        "CompatibleAndroidf9b59a2+ required. QualifiedTESTONLY1c1b7bf4 is not latest app main. Physicalphone/generalrelease/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combinedmain/signing/ownerpush/terminalCI/EVERYimmutableZIPhash/budget/ownerissue gates remain. No optional historicalsessionhelpers, parentlock touch,087 or secondrunner.",
    ]
    p["nextAction"] = "SAME086 two serial blind different-family initial textual reviews on the normally signed LOCAL UNREVIEWED snapshot: complete new凡/凡例, all six exact reused-file diffs, full source families/recognition aliases/eight direct guards. Preserve original reports, reconcile evidence and confirm fixes in original sessions. Then all fresh non-skipped Android/native/fourfont/visual/combinedmain/normal signing/ownerpush/terminalCI/every immutableZIP hash/originalbudget/ownerissue gates. No087 or unreviewed push."
    save(S / "batch-086-progress.json", p)
    print("Pinned three-stroke geometry, exact draft ledger and full comparison packet prepared;",
          len(ids), "supplement families.")


def audit():
    from audit_n1_batch import audit as batch_audit, lexical_pair
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    check_context()
    result = batch_audit(R, "086")
    p = load(S / "batch-086-progress.json")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and hashlib.sha256(raw).hexdigest() == info["sha256"]
    jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert hashlib.sha256(gzip.decompress(jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(gzip.decompress(kd)).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    packets, families = [], {}
    for row in p["dictionaryPackets"]:
        ids = load(S / row["selection"])["entryIds"]
        expected = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert expected == (S / row["xml"]).read_bytes()
        packets.append({"path": row["xml"], "families": len(ids), "lines": len(expected.splitlines()),
                        "sha256": hashlib.sha256(expected).hexdigest(), "freshFrozenExtractionMatches": True})
        families.update({e.findtext("ent_seq"): e for e in ET.fromstring(expected).findall("entry")})
    for row in p["recognitionAliasMappings"]:
        assert any(lexical_pair(families[i], row["spelling"], row["primaryReading"]) for i in row["entryIds"])
        text = (R / row["article"]).read_text(encoding="utf-8")
        plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        assert row["spelling"] in plain and row["primaryReading"] in plain
        assert f"(../kanji/{CHAR}.md)" in text
        if row["spelling"] == "凡て":
            spelling = next(k for k in families["1595730"].findall("k_ele")
                            if k.findtext("keb") == "凡て")
            assert spelling.findtext("ke_inf") == "rarely used kanji form"
            assert "rare kanji spelling" in plain
    raw_family_root = ET.fromstring(gzip.decompress(jm))
    assert not any(e.text == "おうよそ" for e in raw_family_root.iter("reb"))
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(kd)).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    count = 0
    for name in ["batch-086-kanjidic2.xml", "batch-086-comparison-kanjidic2.xml"]:
        for e in ET.parse(S / name).getroot().findall("character"):
            assert canonical(e) == canonical(records[e.findtext("literal")])
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
            assert hashlib.sha256((R / name).read_bytes()).hexdigest() == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and named[94] == CHAR
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(n).stem for n in baseline["files"] if n.startswith("kanji/")}
    current = {path.stem for path in (R / "kanji").glob("*.md")}
    separate = set("保案派第策結")
    other = set("坊的誰身阪")
    assert len(published) == 112 and current - old == published | separate | other | {CHAR}
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    pairs = {tuple(row) for row in p["allMappedReciprocalPairs"]}
    assert len(pairs) == 7
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / f"{char}.md").read_text(encoding="utf-8")
    mapped_primary = {row["article"] for row in p["supportMappings"]}
    assert {f"words/{path.name}" for path in (R / "words").glob("*.md")
            if CHAR in metadata(R, f"words/{path.name}")["kanji"]} == mapped_primary
    assert "jlpt" not in metadata(R, "words/凡例.md")
    neighbors = {}
    for c in ["常", "般", "全", "毎", "各", "皆", "総", "平"]:
        m = metadata(R, f"kanji/{c}.md")
        assert len(m["distractors"]) == 3 and CHAR not in m["distractors"]
        neighbors[c] = {"title": m["title"], "distractors": m["distractors"]}
    explicit = [path.stem for path in (R / "kanji").glob("*.md")
                if path.stem != CHAR and CHAR in metadata(R, "kanji/" + path.name).get("distractors", [])]
    assert explicit == []
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    verified = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = (hashlib.sha256((R / name).read_bytes()).hexdigest() if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
                assert actual == expected, name
                verified += 1
    assert verified == 8416
    svg = (S / "batch-086-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / f"{CHAR}.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-086-draft-stroke-audit.json", dict(
        load(S / "batch-086-stroke-evidence.json"), converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=hashlib.sha256((R / "strokes" / f"{CHAR}.json").read_bytes()).hexdigest(),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False))
    scope = ["kanji/凡.md", "words/凡例.md"]
    text = "".join((R / name).read_text(encoding="utf-8") for name in scope)
    text += "".join(row["after"] for row in p["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-086-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    assert not rare
    save(S / "batch-086-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "086", "completeNewArticleScope": scope,
        "changedReusedScope": p["changedReusedPassages"], "actualHanCount": len(han), "actualHan": han,
        "scopeHash": {n: hashlib.sha256((R / n).read_bytes()).hexdigest() for n in scope},
        "fonts": fonts, "rareHanRangeCharacters": rare, "nativeFontAcceptance": "pending",
        "limits": "All new text plus exact changed reused ranges/context. Cmap presence/absence not glyph/native/fallback-face acceptance; fresh non-skipped RareHan/native/fourfont/visual gates pending.",
    })
    result.update(
        schemaVersion=1, execution=601, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=5, decompressedDictionaryHashesVerified=2, packets=packets,
        distinctDictionaryFamilies=len(families), completeRawCharacterRecordsVerified=count,
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        recognitionAliasesVerified=len(p["recognitionAliasMappings"]),
        allMappedReciprocalPairs=7, directedLinksVerified=14, directWordExclusionPairs=8,
        legacyDefaultFallbackNeighbors=neighbors, existingExplicitTargetDistractors=explicit,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current),
                       "namedSourceMembersPresent": len(current & set(named))},
        separateEarlierLevelSourceMembers=sorted(separate), publishedAdditions=112,
        remainingAdditions=1116, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=p["limits"])
    save(S / "batch-086-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    result = load(S / "batch-086-draft-audit.json")
    p = load(S / "batch-086-progress.json")
    p["draftAuthorInspection"]["supplementRead"] = (
        "Complete returned ranges1-220/221-440 through EOF246 inspected, all10 full families. "
        "Exact decisions and source/read limits in batch-086-draft-source-evidence.json. "
        "Not independent review or unrestricted equivalence.")
    p["draftAuthorInspection"]["draftSourceEvidence"] = "batch-086-draft-source-evidence.json"
    save(S / "batch-086-progress.json", p)
    receipts = {}
    total = 0
    for stem in ["validate", "manifest", "draft-audit", "draft-tests", "vocabulary-consistency", "budget"]:
        raw = (L / f"{stem}-601.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8416" in text and result["contentVersion"] in text
        elif stem == "draft-audit":
            assert json.loads(text) == result
        elif stem == "draft-tests":
            assert text.rstrip().endswith("OK") and "skipped" not in text
            total += int(re.search(r"Ran (\d+) tests", text)[1])
        elif stem == "vocabulary-consistency":
            assert "reviewed prompts" in text
        elif stem == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        target = S / f"batch-086-{stem}-601.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(),
                          "sha256": hashlib.sha256(packed).hexdigest(),
                          "uncompressedSha256": hashlib.sha256(raw).hexdigest()}
    recipe = S / "batch-086-draft-recipe.py"
    recipe.write_bytes(Path(__file__).read_bytes())
    save(S / "execution-601.json", {
        "schemaVersion": 1, "execution": 601, "batch": "086", "stage": "local-unreviewed-draft",
        "sourceCheckpoint": HEAD, "baseCommit": p["baseCommit"], "runtimePublished": False,
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "focusedTestsPassed": total, "validatorErrors": 0, "localBudget": budget,
        "audit": "docs/n1-sources/batch-086-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-086-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-086-draft-stroke-audit.json",
        "recipe": recipe.relative_to(R).as_posix(),
        "recipeSha256": hashlib.sha256(recipe.read_bytes()).hexdigest(),
        "sourceEvidence": "docs/n1-sources/batch-086-draft-source-evidence.json",
        "sourceEvidenceSha256": hashlib.sha256(
            (S / "batch-086-draft-source-evidence.json").read_bytes()).hexdigest(),
        "focusedTestModules": ["test_audit_n1_batch", "test_audit_n1_pilot",
                              "test_extract_n1_jmdict", "test_freeze_n1_sources",
                              "test_validate", "test_content_language"],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "runnerLockRole": "Parent19008 owns runner.lock throughout coordinator23024; child never acquires/deletes/unlocks.",
        "artifactPathPreflight": "Approved workspace/frozen inputs and committed source evidence only; reusable helper under control; no optional historicalsessionhelper access.",
        "actualNewPermissionDenials": [], "publishedAdditions": 112, "remainingAdditions": 1116,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": p["limits"], "nextAction": p["nextAction"],
    })
    print("Local draft checks, complete evidence and durable recipe archived.")


def finish():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    evidence = load(S / "execution-601.json")
    for receipt in evidence["checks"].values():
        raw = (R / receipt["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt["sha256"]
        assert hashlib.sha256(gzip.decompress(raw)).hexdigest() == receipt["uncompressedSha256"]
    assert hashlib.sha256((R / evidence["recipe"]).read_bytes()).hexdigest() == evidence["recipeSha256"]
    assert hashlib.sha256((R / evidence["sourceEvidence"]).read_bytes()).hexdigest() == evidence["sourceEvidenceSha256"]
    before = load(L / "progress-before-601.json")
    p = load(C / "progress.json")
    changing = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in changing:
            assert p[key] == value, key
    next_action = load(S / "batch-086-progress.json")["nextAction"]
    result = load(S / "batch-086-draft-audit.json")
    checkpoint = dict(
        schemaVersion=1, execution=601, checkpoint=601, batch="086", status="continue",
        stage="local-unreviewed-draft", savedCommit=head, signature="G",
        sourceCommit=HEAD, evidence="docs/n1-sources/execution-601.json",
        membership=[CHAR], sourceRow=95, runtimeDrafted=[CHAR], reviewClosed=[], published=[],
        runtimePublished=False, contentVersion=result["contentVersion"],
        focusedTestsPassed=evidence["focusedTestsPassed"], validatorErrors=0,
        metadataReadings=5, sourceOnlyExactReadings=["おうよ.そ"],
        curatedOnKeys=["ぼん", "はん"], curatedKunKeys=[], allMappedReciprocalPairs=7,
        directedLinksVerified=14, newNecessarySupportArticles=1, reusedSupportArticles=3,
        changedReusedFiles=6, directWordExclusionPairs=8, pinnedStrokePaths=3,
        allRuntimePayloadHashesVerified=8416, actualHanCount=result["actualHanCount"],
        nativeFontAcceptance="pending", dedicatedWorktreesClean=True,
        originalHistoricalRootKeysCompared=len(before), allOriginalHistoricalValuesPreserved=True,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        parentLockTouched=False, optionalHistoricalSessionHelpersAccessed=False,
        actualNewPermissionDenials=[], publishedAdditions=112, remainingAdditions=1116,
        lastPublishedCommit=p["lastPublishedCommit"], physicalPhoneAcceptance="outstanding",
        generalReleaseAcceptance="outstanding", wholeProjectComplete=False, nextBatchStarted=False,
        nextAction=next_action)
    p.update(checkpoint=601, status="continue", stage="batch-086-local-unreviewed-draft",
             nextAction=next_action, blocker=None)
    p["execution601StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution601CoordinatorCheckpoint"] = checkpoint
    save(C / "progress.json", p)
    print(json.dumps(checkpoint, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["prepare", "audit", "record", "finish"])
    globals()[parser.parse_args().action]()
