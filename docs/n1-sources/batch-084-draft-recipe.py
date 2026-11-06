"""Durable bounded batch084 draft checks; never acquires the parent runner lock."""
import argparse
import ast
import copy
import gzip
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "acc99737-6954-43c2-a1e8-1ae4ccd3f91e"
HEAD = "73f982ef379b54a5cc9d2b7668f8417e27c7837d"
APP = "1c1b7bf42cc91d820a93169f1088dc647ac51c0d"
CHAR = "\u51dc"
sys.path.insert(0, str(R / "tools"))


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".583.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def start():
    for root, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    p = load(C / "progress.json")
    assert p["checkpoint"] == 582 and p["batch"] == "084" and p["status"] == "continue"
    before = L / "progress-before-583.json"
    assert not before.exists()
    save(before, p)
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 582
    state = {
        "execution": 583, "batch": "084", "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": git("rev-parse", "origin/main"),
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME084 bounded runtime draft and normally signed LOCAL UNREVIEWED freeze only; no reviewers, Android/native, publication,085 or second runner.",
        "request": {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                    "characters": len(text), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded and complete checkpoint decoded; operative contract, approved issue and final582 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerLockRole": "Live parent19008 verified; child inherits launcher protection and does not acquire/delete/unlock runner.lock.",
        "artifactPathPreflight": "Committed source packets and approved control/frozen inputs only; no optional historical-session recipe accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution583StartingState"] = state
    p.update(stage="batch-084-runtime-drafting", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting bounded draft scope persisted; all prior history retained.")


def comparisons():
    from extract_n1_jmdict import extract
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    path = C / "inputs" / "n1-implementation-JMdict_e.gz"
    raw = path.read_bytes()
    expected = snapshot["inputs"][path.name]
    assert hashlib.sha256(raw).hexdigest() == expected["sha256"]
    root = ET.fromstring(gzip.decompress(raw))
    words = ["厳しい", "寒い", "准", "冗", "凹", "冷たい", "冷える", "凍える",
             "澄む", "透き通る", "冴える", "さわやか", "爽やか", "鷹揚", "はっきり",
             "朗らか", "きつい", "ひどい", "激しい", "険しい", "冷静", "明らか",
             "明確", "すっきり"]
    ids = [e.findtext("ent_seq") for e in root.findall("entry")
           if any(k.text in words for k in e.findall("k_ele/keb") + e.findall("r_ele/reb"))]
    selection = {"schemaVersion": 1, "batch": "084", "entryIds": ids,
                 "exactSpellings": words,
                 "sourceSnapshot": "docs/n1-source-snapshot.json",
                 "limits": "Exact full comparison families; extraction alone is not semantic inspection."}
    save(S / "batch-084-comparison-selection.json", selection)
    (S / "batch-084-comparison-jmdict.xml").write_bytes(extract(raw, expected["sha256"], ids))
    kd_path = C / "inputs" / "n1-planning-kanjidic2.xml.gz"
    kd_raw = kd_path.read_bytes()
    assert hashlib.sha256(kd_raw).hexdigest() == snapshot["inputs"][kd_path.name]["sha256"]
    kd = ET.fromstring(gzip.decompress(kd_raw))
    packet = ET.Element("kanjidic2")
    packet.append(copy.deepcopy(kd.find("header")))
    for entry in kd.findall("character"):
        if entry.findtext("literal") in ["准", "冗", "凹"]:
            packet.append(copy.deepcopy(entry))
    ET.indent(packet, space="  ")
    (S / "batch-084-comparison-kanjidic2.xml").write_bytes(
        ET.tostring(packet, encoding="utf-8", xml_declaration=True) + b"\n")
    print("Extracted comparison families:", len(ids))


def geometry():
    from generate_strokes import convert, KANJIVG_REVISION
    evidence = load(S / "batch-084-stroke-evidence.json")
    raw = (S / "batch-084-kanjivg.svg").read_bytes()
    assert len(raw) == evidence["bytes"]
    assert hashlib.sha256(raw).hexdigest() == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == evidence["gitBlob"]
    assert hashlib.sha256((R / "tools" / "generate_strokes.py").read_bytes().replace(
        b"\r\n", b"\n")).hexdigest() == evidence["converterNormalizedSha256"]
    data = convert(CHAR, raw.decode("utf-8"))
    assert data["strokeCount"] == 15 and data["sourceRevision"] == KANJIVG_REVISION
    target = R / "strokes" / (CHAR + ".json")
    assert not target.exists()
    target.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print("Generated pinned15-stroke geometry with unchanged repository converter.")


def ledger():
    from audit_n1_pilot import metadata
    p = load(S / "batch-084-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR])
    p["dictionaryPackets"] = [
        {"selection": "batch-084-lexical-selection.json", "xml": "batch-084-jmdict.xml"},
        {"selection": "batch-084-comparison-selection.json", "xml": "batch-084-comparison-jmdict.xml"},
    ]
    for row in p["readingDispositions"]:
        row.update(kanji=CHAR, selected=row["proposedQuizSelection"],
                   sourceOnly=row["kind"] == "kun",
                   entryIds=["1564320"] if row["kind"] == "on" else [],
                   reason=row.get("qualification", "") + " " + row["evidence"])
        if row["selected"]:
            row["article"] = "words/凜.md"
    p["supportMappings"] = [{
        "kanji": CHAR, "article": "words/凜.md", "primaryReading": "りん",
        "entryIds": ["1564320"], "newArticle": True, "allWrittenKanji": [CHAR],
        "selectedSenses": "Dignified bearing and bracing cold; clear/firm ringing voice",
        "status": "local-unreviewed-draft", "wordJlpt": None,
    }]
    p["curatedProjection"] = [dict(p["proposedCuratedProjection"], kanji=CHAR)]
    p["requiredReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["allMappedReciprocalPairs"] = p["proposedReciprocalPairs"]
    p["changedReusedPassages"] = []
    card = metadata(R, "kanji/凜.md")
    p["quizAudit"] = {CHAR: {
        "title": card["title"], "distractors": card["distractors"],
        "labels": [metadata(R, f"kanji/{c}.md")["title"] for c in card["distractors"]],
        "meaningDecisions": [
            {"kanji": "准", "reason": "quasi/associate rank and approval; not severe cold or dignity",
             "evidence": "Complete frozen character record and unchanged complete准 article"},
            {"kanji": "冗", "reason": "redundancy/uselessness, including joke compound; not dignity/cold",
             "evidence": "Complete frozen character record, JMdict1355480 and unchanged complete冗 article"},
            {"kanji": "凹", "reason": "concave/hollow/sunken; not dignity/cold",
             "evidence": "Complete frozen character record, JMdict1179150/2756450 and unchanged complete凹 article"},
        ],
        "legacyFallbackDisposition": "New凜 has three wrong labels for default four-choice quiz. Targeted cold/severity legacy-title navigation identified冷/寒, both already have three curated choices; no new凜 fallback slot in default questions. Larger pools remain a documented limitation.",
    }}
    excluded = metadata(R, "words/凜.md")["quiz_exclusions"]
    p["wordQuizAudit"] = {
        "title": metadata(R, "words/凜.md")["title"],
        "directExclusions": [{"word": CHAR, "exclude": excluded,
                              "reason": "Direct conservative quiz-label safeguards for documented cold/severity, dignity/composure and clear-sound senses. Not unrestricted substitution rules or a transitive cluster."}],
        "decisions": [
            {"words": ["寒い", "厳しい", "冷たい", "冷える", "凍える", "きつい", "ひどい", "激しい", "険しい"],
             "reason": "Broad cold/severe/intense/stern labels can obscure凜's severe-cold or tightly composed-bearing branches. Some describe a process, bodily chill or harsh treatment rather than the exact凜 construction; conservative pair guards do not assert free interchangeability.",
             "entryIds": ["1210360", "1262530", "1556730", "1556630", "1446180", "1003450", "1602060", "1600720", "1260530"]},
            {"words": ["澄む", "透き通る", "冴える", "さわやか", "はっきり", "朗らか", "明らか", "明確", "すっきり"],
             "reason": "The凜 family has ordinary clear/ringing sound even though its primary title focuses on dignity/cold. Guard clear/distinct/refined labels, especially the explicit sound senses of澄む/透き通る/冴える/さわやか.明らか/明確 concern evident/definite clarity and朗らか includes cheerfulness/sky; their broad English clear labels warrant conservative protection, not a new unrestricted voice-substitution claim.",
             "entryIds": ["1373680", "1450510", "1297050", "1399520", "1010150", "1560710", "1532310", "1532410", "1006120"]},
            {"words": ["鷹揚", "冷静"],
             "reason": "Composed manner is close to the tightly composed bearing in Seisen凜;鷹揚's existing article expressly discusses dignified manner. Guard partial label overlap, while retaining differences between outward dignity, magnanimity and mental composure.",
             "entryIds": ["1608970", "1557050"]},
        ],
        "confusableInventory": "Read candidate contract and exact search; CW039 cold-weather/contact distinction retained. No凜/凛 row exists; actual full families and articles, not inventory presence, justify guards.",
        "limits": "Targeted current-label scan and complete applicable families/selected articles; not whole-corpus quiz certification. Twenty direct pairs on new article only, no existing exclusions removed or transitive expansion.",
    }
    p["draftAuthorInspection"] = {
        "execution": 583, "sourceCheckpoint": HEAD,
        "freshCompletePacketRanges": {"batch-084-jmdict.xml": [[1, 217]],
                                      "batch-084-comparison-jmdict.xml": [[1, 210], [211, 420], [421, 630], [631, 832]]},
        "lexicalFamilies": 7, "comparisonFamilies": 24, "totalFamilyOccurrences": 31,
        "rawCharacterRanges": {"batch-084-kanjidic2.xml": [[1, 116]],
                                "batch-084-comparison-kanjidic2.xml": [[1, 180], [181, 207]]},
        "completeExistingArticlesRead": ["kanji/准.md", "kanji/冗.md", "kanji/凹.md", "kanji/冴.md",
                                         "kanji/冷.md", "kanji/寒.md"]
            + [f"words/{word}.md" for word in excluded],
        "existingBodyReadLimits": "Actual twenty excluded word bodies returned in full; no rewrite or full historical review implied.",
        "publicSource": {"url": "https://kotobank.jp/word/凜-659857",
                         "maxLength": 14000, "scope": "Complete returned Daijisen lexical and character headings plus Seisen/Jitsu. Only scoped lexical/variant and short example evidence adopted; image-dependent historical phonetic claims omitted."},
        "examples": {"凜とした声がひびく": "Exact short Daijisen example with original English translation and kana",
                     "凜とした朝の寒気": "Exact short Daijisen noun phrase with original English translation and kana"},
        "limits": "Coordinator source inspection, not independent review or measured native/phone comprehensibility. Full凛-only families not claimed inspected: no new凛-only compounds are taught.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED runtime draft only; original source-preparation proposals and limits preserved.",
        "Both raw readings preserved; onlyリン selected,きびし.いsource-only/kun[] with no manufactured spelling.",
        "No reviewer, fresh Android/native, glyph legibility, physical phone, review closure or runtime publication.",
        "Latest-main106a36dd separate supplementary content not integrated or counted in N1 remainder; actual latest-main reconciliation remains mandatory before publication.",
        "All two-family/source/reading/link/choice/baseline/font/stroke/Android/native/signing/combinedmain/ownerpush/CI/everyimmutableZIPhash/originalbudget/issue gates unchanged. Published110/1228;1118remaining; whole project incomplete.",
    ]
    p["nextAction"] = "SAME084: two serial blind different-family initial textual reviews on normally signed LOCAL UNREVIEWED frozen snapshot; reconcile before later Android/native/publication gates. No085 or push."
    save(S / "batch-084-progress.json", p)
    print("Draft ledger written; original source-only qualifications and history retained.")


def audit():
    from audit_n1_batch import audit as batch_audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    result = batch_audit(R, "084")
    p = load(S / "batch-084-progress.json")
    assert p["status"] == "local-unreviewed-draft" and p["reviewClosed"] == p["published"] == []
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and hashlib.sha256(raw).hexdigest() == info["sha256"], name
    raw_jm = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    raw_kd = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert hashlib.sha256(gzip.decompress(raw_jm)).hexdigest() == snapshot["jmdict"]["xmlSha256"]
    assert hashlib.sha256(gzip.decompress(raw_kd)).hexdigest() == snapshot["kanjidic2"]["xmlSha256"]
    packet_receipts = []
    for packet in p["dictionaryPackets"]:
        selection = load(S / packet["selection"])
        expected = extract(raw_jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
                           selection["entryIds"])
        assert expected == (S / packet["xml"]).read_bytes()
        packet_receipts.append({"path": packet["xml"], "families": len(selection["entryIds"]),
                                "lines": len(expected.splitlines()),
                                "sha256": hashlib.sha256(expected).hexdigest(),
                                "freshFrozenExtractionMatches": True})
    assert sum(x["families"] for x in packet_receipts) == 31
    records = {e.findtext("literal"): e for e in ET.fromstring(gzip.decompress(raw_kd)).findall("character")}
    canonical = lambda e: ET.canonicalize(ET.tostring(e, encoding="unicode"), strip_text=True)
    character_count = 0
    for name in ["batch-084-kanjidic2.xml", "batch-084-comparison-kanjidic2.xml"]:
        for record in ET.parse(S / name).getroot().findall("character"):
            assert canonical(record) == canonical(records[record.findtext("literal")])
            character_count += 1
    assert character_count == 5
    base = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in base["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = dict(info["metadata"])
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
    assert named == load(S / "community-list-20261102.json") and named[92] == CHAR
    published = set("幹氏扱乃凹凸矛鷹彗漱栞莉")
    for path in S.glob("batch-*-progress.json"):
        published.update(load(path).get("published", []))
    old = {Path(n).stem for n in base["files"] if n.startswith("kanji/")}
    current = {path.stem for path in (R / "kanji").glob("*.md")}
    assert len(published) == 110 and current - old == published | {CHAR}
    assert len(current) == 1096 and len(current & set(named)) == 115
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    assert sum(metadata(R, f"kanji/{path.name}")["jlpt"] == 1
               for path in (R / "kanji").glob("*.md")) == 116
    assert len(list((R / "words").glob("*.md"))) == 5053
    word = metadata(R, "words/凜.md")
    assert word["kanji"] == [CHAR] and word["reading"] == "りん" and "jlpt" not in word
    pairs = {(c, row["article"]) for row in p["supportMappings"]
             for c in metadata(R, row["article"])["kanji"] if (R / "kanji" / f"{c}.md").exists()}
    assert pairs == {tuple(row) for row in p["allMappedReciprocalPairs"]} == {(CHAR, "words/凜.md")}
    assert {f"words/{path.name}" for path in (R / "words").glob("*.md")
            if CHAR in metadata(R, f"words/{path.name}")["kanji"]} == {"words/凜.md"}
    assert not (R / "kanji" / "凛.md").exists() and not (R / "words" / "凛.md").exists()
    assert len(word["quiz_exclusions"]) == len(set(word["quiz_exclusions"])) == 20
    assert set(word["quiz_exclusions"]) == {w for row in p["wordQuizAudit"]["decisions"] for w in row["words"]}
    for row in p["wordQuizAudit"]["decisions"]:
        assert len(row["entryIds"]) == len(row["words"])
    for c in ["冷", "寒"]:
        assert len(metadata(R, f"kanji/{c}.md")["distractors"]) == 3
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = (hashlib.sha256((R / name).read_bytes()).hexdigest() if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
                assert actual == expected, name
                checked += 1
    assert checked == 8379
    svg = (S / "batch-084-kanjivg.svg").read_bytes()
    assert load(R / "strokes" / "凜.json") == convert(CHAR, svg.decode("utf-8"))
    save(S / "batch-084-draft-stroke-audit.json", dict(
        load(S / "batch-084-stroke-evidence.json"), converted=True,
        output="strokes/凜.json", outputSha256=hashlib.sha256((R / "strokes" / "凜.json").read_bytes()).hexdigest(),
        geometryExactlyRegenerated=True, nativeDrawingAccepted=False,
        limits="Pinned unchanged converter and exact SVG output; no native drawing or handwriting acceptance."))
    scope = ["kanji/凜.md", "words/凜.md"]
    text = "".join((R / name).read_text(encoding="utf-8") for name in scope)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-084-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    assert not rare, rare
    save(S / "batch-084-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "084", "completeNewArticleScope": scope,
        "changedReusedScope": [], "actualHanCount": len(han), "actualHan": han,
        "articleHashes": {name: hashlib.sha256((R / name).read_bytes()).hexdigest() for name in scope},
        "fonts": fonts, "rareHanRangeCharacters": rare,
        "nativeFontAcceptance": "pending",
        "limits": "Actual complete draft Han and unchanged cmaps; absence is not a glyph failure. Fresh non-skipped RareHan and native/system-font variant/component comparisons remain pending.",
    })
    result.update(schemaVersion=1, execution=583, stage="local-unreviewed-draft",
                  sourceCheckpoint=HEAD, packets=packet_receipts, frozenInputHashesVerified=5,
                  decompressedDictionaryHashesVerified=2, completeRawCharacterRecordsVerified=character_count,
                  originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
                  baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
                  allMappedReciprocalPairs=len(pairs), directedLinksVerified=len(pairs) * 2,
                  directWordExclusionPairs=20, allRuntimePayloadHashesVerified=checked,
                  currentCounts={"kanji": 1096, "words": 5053, "n1Labels": 116, "namedSourceMembersPresent": 115},
                  actualHanCount=len(han), pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
                  publishedAdditions=110, remainingAdditions=1118, draftOnlyAdditions=[CHAR],
                  runtimePublished=False, independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
                  physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
                  wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False,
                  actualNewPermissionDenials=[], limits=p["limits"])
    save(S / "batch-084-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    result = load(S / "batch-084-draft-audit.json")
    receipts = {}
    for stem in ["validate", "manifest", "draft-audit", "draft-n1-tests",
                 "draft-format-tests", "vocabulary-consistency", "budget"]:
        raw = (L / f"{stem}-583.txt").read_bytes()
        text = raw.decode("utf-8-sig")
        if stem == "validate":
            assert text.strip() == "0 error(s)"
        elif stem == "manifest":
            assert "8379" in text and result["contentVersion"] in text
        elif stem == "draft-audit":
            assert json.loads(text) == result
        elif stem == "draft-n1-tests":
            assert "Ran 43 tests" in text and text.rstrip().endswith("OK")
        elif stem == "draft-format-tests":
            assert "Ran 82 tests" in text and text.rstrip().endswith("OK")
        elif stem == "vocabulary-consistency":
            assert "2122/2431 reviewed prompts" in text
        elif stem == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000
            assert budget["retainedBytes"] <= 56 * 1024 ** 2
            assert budget["inflatedBytes"] <= 80 * 1024 ** 2
            assert budget["localZipBytes"] <= 42 * 1024 ** 2
        target = S / f"batch-084-{stem}-583.txt.gz"
        packed = gzip.compress(raw, mtime=0)
        target.write_bytes(packed)
        receipts[stem] = {"path": target.relative_to(R).as_posix(),
                          "sha256": hashlib.sha256(packed).hexdigest(),
                          "uncompressedSha256": hashlib.sha256(raw).hexdigest()}
    evidence = {
        "schemaVersion": 1, "execution": 583, "batch": "084",
        "stage": "local-unreviewed-draft", "sourceCheckpoint": HEAD,
        "baseCommit": result["baseCommit"], "runtimePublished": False,
        "runtimeDrafted": [CHAR], "reviewClosed": [], "published": [],
        "contentVersion": result["contentVersion"], "checks": receipts,
        "focusedTestsPassed": 125, "validatorErrors": 0, "localBudget": budget,
        "audit": "docs/n1-sources/batch-084-draft-audit.json",
        "fontAudit": "docs/n1-sources/batch-084-draft-font-audit.json",
        "strokeAudit": "docs/n1-sources/batch-084-draft-stroke-audit.json",
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "recipe": "docs/n1-sources/batch-084-draft-recipe.py",
        "artifactPathPreflight": "Committed source packets and approved workspace inputs only. No optional historical-session helper accessed or requested.",
        "runnerLockRole": "Parent19008 retains sole runner.lock ownership; no child acquisition/delete/unlock.",
        "actualNewPermissionDenials": [],
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "limits": result["limits"],
        "nextAction": load(S / "batch-084-progress.json")["nextAction"],
    }
    (S / "batch-084-draft-recipe.py").write_bytes(Path(__file__).read_bytes())
    evidence["recipeSha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    save(S / "execution-583.json", evidence)
    print("Complete local check receipts and reusable workspace recipe archived.")


def finish():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    evidence = load(S / "execution-583.json")
    for receipt in evidence["checks"].values():
        raw = (R / receipt["path"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == receipt["sha256"]
        assert hashlib.sha256(gzip.decompress(raw)).hexdigest() == receipt["uncompressedSha256"]
    assert hashlib.sha256((S / "batch-084-draft-recipe.py").read_bytes()).hexdigest() == evidence["recipeSha256"]
    before = load(L / "progress-before-583.json")
    p = load(C / "progress.json")
    allowed = {"stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    next_action = evidence["nextAction"] + (
        " Preserve actual native凜/凛/冫/稟 legibility pending, existing original all40 evidence and all acceptance limits. "
        "Later non-skipped Android/native, fresh latest-main normal integration/review/checks, owner fast-forward, "
        "terminalCI/everyimmutableZIPhash/originalbudgets/verifiedissue gates remain. Parent retains runner.lock; "
        "no child acquisition. Published110/1228;1118remaining; physicalphone/generalrelease/whole-set outstanding.")
    checkpoint = {
        "schemaVersion": 1, "execution": 583, "checkpoint": 583, "batch": "084",
        "status": "continue", "stage": "local-unreviewed-draft",
        "savedCommit": head, "signature": "G", "sourceCommit": HEAD,
        "evidence": "docs/n1-sources/execution-583.json",
        "membership": [CHAR], "sourceRow": 93, "runtimeDrafted": [CHAR],
        "reviewClosed": [], "published": [], "runtimePublished": False,
        "focusedTestsPassed": 125, "validatorErrors": 0,
        "allRuntimePayloadHashesVerified": 8379, "readingDispositions": 2,
        "curatedOfferedKeys": 1, "sourceOnlyOfferedKeys": 0,
        "completeDictionaryFamilies": 31, "rawCharacterRecords": 5,
        "allMappedReciprocalPairs": 1, "directWordExclusionPairs": 20,
        "pinnedConvertedStrokes": 15, "actualHan": 28,
        "nativeFontAcceptance": "pending",
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 110, "remainingAdditions": 1118,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "dedicatedWorktreesClean": True, "wholeProjectComplete": False, "nextBatchStarted": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "originalHistoricalRootKeysCompared": len(before), "allOriginalHistoricalValuesPreserved": True,
        "nextAction": next_action,
    }
    p["execution583CoordinatorCheckpoint"] = checkpoint
    p.update(checkpoint=583, status="continue", stage="batch-084-signed-local-unreviewed-draft",
             nextAction=next_action, blocker=None)
    allowed |= {"checkpoint", "status"}
    assert all(p[k] == v for k, v in before.items() if k not in allowed)
    save(C / "progress.json", p)
    body = (
        f"Batch 084 local **unreviewed** draft preserved at normally signed `{head}` (source `{HEAD}`).\n\n"
        "Added only 凜, its necessary 凜（りん） support article and generated pinned 15-stroke geometry. "
        "Both source readings remain; only リン is selected and きびし.い is explicitly source-only. "
        "31 complete dictionary families, 5 raw character records, 20 direct word guards and the reciprocal pair "
        "are recorded. 125 focused tests, validator, manifest, vocabulary consistency and local budget checks passed; "
        "8,379 runtime hashes verified. No baseline metadata/stroke changes outside historical documented exceptions.\n\n"
        "**Not published or review-closed.** No reviewer, fresh Android/native or phone acceptance claimed. "
        "凜/凛/冫/稟 native fallback comparison remains pending; cmap absence is not a glyph failure. "
        "Next: two serial blind different-family textual reviews on this frozen snapshot, then reconciliation and "
        "all original Android/native/latest-main/normal-signing/owner-push/CI/immutable-ZIP/budget gates. "
        "Fresh main's separate supplementary changes are not integrated or counted here. "
        "110/1,228 additions published; 1,118 remain. Physical-phone/general-release/whole-set acceptance outstanding. "
        "Checkpoint 583 saved with full history, status `continue`; no next batch or second runner.\n"
    )
    (C / "batch-084-draft-583-issue.txt").write_text(body, encoding="utf-8")
    print("Signed clean draft checkpoint persisted:", head)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=["start", "comparisons", "geometry", "ledger", "audit",
                                             "record", "finish"])
    args = parser.parse_args()
    {"start": start, "comparisons": comparisons, "geometry": geometry, "ledger": ledger, "audit": audit,
     "record": record, "finish": finish}[args.operation]()
