"""Prepare and audit the bounded batch100 LOCAL UNREVIEWED snapshot."""
import argparse
import copy
import gzip
import hashlib
import io
import json
import math
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
S = R / "docs" / "n1-sources"
L = C / "logs" / "cad52b97-90c7-458e-b57e-f78e2f3cdccd"
HEAD = "8a8daf9c63527fb34379346641f4c577dca7623e"
MAIN = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "創"
REUSED = ["words/創作.md", "words/作る.md", "kanji/作.md"]
NEXT = (
    "SAME100 TWO serial blind different-model-family initial textual reviews on the "
    "normally signed LOCAL UNREVIEWED draft: complete創 and exact reused創作/作る/作 "
    "changes, correctness/scoped coverage/phone comprehensibility. Both reviewers get "
    "same frozen137 member+16comparison families/13raw character records, actual public "
    "source blocks and final labels. Preserve six exact source readings/order; selected "
    "ソウ/つく.る yieldそう/つくる. Reused創作そうさく N2 and same-family作るつくる "
    "N5 retain all metadata and13/5 original guards; no new word identity/level. "
    "Qualified rare創める establishment sense only; standalone創きず rare SPELLING, "
    "not pronunciation. Exactショウ/けず.しける remain explicitly source-only, "
    "lexical allocation UNVERIFIED, no invented gloss/example/invalidity/obsolescence/"
    "source repair, both excluded from quiz. No rigid作る/造る/創る compartments or "
    "cooking/crop substitutions. FIVE all-mapped pairs/TENdirections/ONEactivatedpair; "
    "THREE exact reused changes. Title originate; create; actual wrong labels剣/倹/験 "
    "and eight DIRECT symmetric NONTRANSITIVE guards作造始元原本緒産 need independent "
    "semantic review, no edits to unrelated existing cards. Canonical刀18 visibly刂; "
    "structure-unclassified/no phonetic/history claim; twelve pinned converted paths. "
    "Cmap absence is NOT glyphfailure; actualHan and four-font/native/rendered acceptance "
    "pending. Preserve actual models, same snapshot, complete reports/read limits; "
    "serial reviewer processes AND internal tools, actual exit before next reviewer, "
    "evidence reconciliation and original-session confirmations. Then fresh non-skipped "
    "qualifiedAndroidbf30cdead RealContent/RareHan, productionContentSyncONCE/native "
    "N1-All/meaning/curatedreading/drawing/article/Back/offline/four-font/all-Han/rendered "
    "review, combinedcurrentmain checks, normal signing/ownerfastforward/terminalgreenCI/"
    "EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed80MiBinflated"
    "56MiBretained/perfilepathmedia/verifiedownerissue gates remain mandatory. "
    "No unreviewedpush/101/authoragent/concurrentheavywork/secondrunner/signingretry/"
    "guardincrease. Verify whollyclean signedheads/freshmain/liveparentancestry/"
    "decodedlauncher/exactsession. Parent5920 ownsrunner.lock: no childacquire/delete/"
    "unlock/readprobe. Approvedcontrol/committedsource/frozeninputs only, not optional "
    "historicalsessionrecipes; preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Published126/1228,1102acceptanceremainder unchanged; six earlier "
    "N2placements保案派第策結 remain separate, never duplicate/relevel. "
    "Physicalphone/generalrelease/whole-setoutstanding; projectincomplete."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".747.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == value
    tmp.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def identity():
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (746, "100", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    assert git("branch", "--show-current") == "content/n1-kanji"
    role = load(L / "preflight-747.json")
    assert role["sessionId"] == L.name and role["liveParentPid"] == 5920
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution746CoordinatorCheckpoint"] == p["execution746CoordinatorCheckpoint"]
    assert not (L / "progress-before-747.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-747.json")
    state = {
        "execution": 747, "batch": "100", "startingHead": HEAD, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME100 bounded LOCAL UNREVIEWED runtime draft/freeze only; no reviewer, Android/native, publication,101 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete approved issue and final746 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution747StartingState"] = state
    p.update(stage="batch-100-local-unreviewed-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history; wholly clean signed worktrees verified.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    plan = load(S / "batch-100-authoring-plan.json")
    svg = (S / "batch-100-kanjivg.svg").read_bytes()
    proof = load(S / "batch-100-stroke-evidence.json")
    assert sha(svg) == proof["sha256"]
    assert svg == (C / "inputs" / "n1-05275-70a0b7ae.svg").read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 12
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-100-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [111]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR])
    frozen["limits"] = "LOCAL UNREVIEWED draft only, not review closure, native acceptance or publication."
    save(S / "batch-100-membership.json", frozen)
    p = load(S / "batch-100-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR], runtimeChanged=True)
    p["dictionaryPackets"] = [
        {"selection": "batch-100-lexical-selection.json", "xml": "batch-100-jmdict.xml"},
        {"selection": "batch-100-comparison-selection.json", "xml": "batch-100-comparison-jmdict.xml"},
    ]
    p["readingDispositions"] = []
    for row in plan["readingDispositions"]:
        r = copy.deepcopy(row)
        r.update(kanji=CHAR, selected=r["status"] == "selected",
                 sourceOnly=r["status"] == "source-only-unselected")
        r["reason"] = " ".join(r[k] for k in ["allocation", "qualification", "decision", "limits"] if k in r)
        p["readingDispositions"].append(r)
    p["supportMappings"] = [
        {"kanji": CHAR, "article": name, "primaryReading": metadata(R, name)["reading"],
         "entryIds": [entry], "newArticle": False, "status": "local-unreviewed-draft"}
        for name, entry in [("words/創作.md", "1398420"), ("words/作る.md", "1597890")]
    ]
    p["requiredReciprocalPairs"] = [[CHAR, r["article"]] for r in p["supportMappings"]]
    p["allMappedReciprocalPairs"] = plan["allMappedReciprocalPairs"]
    edits = [
        ("words/創作.md", "創 contributes originating or creating,",
         "[創](../kanji/創.md) contributes originating or creating,"),
        ("words/作る.md", "and 創る, emphasizing creation.",
         "and [創](../kanji/創.md)る, emphasizing creation."),
        ("kanji/作.md", "- [凶作](../words/凶作.md) きょうさく — poor harvest; crop failure",
         "- [凶作](../words/凶作.md) きょうさく — poor harvest; crop failure\n"
         "- [創作](../words/創作.md) そうさく — creative production; original work"),
    ]
    p["changedReusedPassages"] = [{"article": name, "before": before, "after": after}
                                  for name, before, after in edits]
    p["curatedProjection"] = [{
        "kanji": CHAR, "quizOnyomi": ["ソウ"], "quizKunyomi": ["つく.る"],
        "onKeys": ["そう"], "kunKeys": ["つくる"],
    }]
    p["quizAudit"] = {CHAR: {
        "title": plan["proposedMetadata"]["title"],
        "distractors": plan["proposedMetadata"]["distractors"],
        "labels": [r["label"] for r in plan["quizPlan"]["distractors"]],
        "meaningDecisions": plan["quizPlan"]["distractors"],
        "directExclusions": plan["quizPlan"]["directGuards"],
        "guardSemantics": plan["quizPlan"]["guardSemantics"],
        "limits": "Author semantic audit, not independent review or empirical live-quiz safety.",
    }}
    p["wordQuizAudit"] = {
        "directExclusions": [], "newOrRewordedTitles": 0,
        "preservedOriginalExclusions": {name: metadata(R, name)["quiz_exclusions"]
                                       for name in plan["reusedSupportArticles"]},
        "limits": "No new word identity, level, title or guard. Original thirteen/five direct exclusions unchanged.",
    }
    p["draftAuthorInspection"] = {
        "execution": 747, "sourceCheckpoint": HEAD,
        "freshCompleteApplicableMemberFamilies": ["1307550", "1345890", "1398420", "1580260", "1597890"],
        "freshCompleteComparisonFamilies": 16,
        "inheritedSourceInspection": "Original745 read137 complete member families;746 inspected full comparison families/raw character fields and16 existing articles. Original receipts and read-depth limits unchanged; no fresh137-family linguistic reread claimed.",
        "freshChangedArticles": REUSED, "freshCompleteDistractorArticles": ["kanji/剣.md", "kanji/倹.md", "kanji/験.md"],
        "publicLookup": "Committed full-family and actual authority-headed archived public evidence, not fresh upstream retrieval. No frequency/historical claim inferred from source presence.",
        "limits": "Author inspection only, not independent review, native-speaker certification, phone evidence or uniform source comprehension.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only; no reviewer, fresh Android/native/font/phone acceptance or runtime publication.",
        "Six full readings and source order unchanged; two selected keys, two qualified rare-spelling recognition rows, two explicitly limited source-only rows.",
        "Exactショウ/けず.しける lexical allocation remains UNVERIFIED, no invented example/gloss/invalidity/obsolescence/source repair.",
        "Reuse創作N2 and same-family作るN5, preserving all metadata,13/5 original exclusions and original examples; no new word identity or level.",
        "創める establishment sense only; rare standalone創きず spelling not pronunciation. No rigid作る/造る/創る semantic compartments.",
        "Five all-mapped pairs/ten directions/one activated baseline pair, three exact reused changes. Eight direct symmetric nontransitive kanji guards.",
        "Canonical刀18 visibly刂; twelve pinned generated paths, labelled modern-shape mnemonic only, structure-unclassified/no phonetic or history claim.",
        "ActualHan/cmaps are not native glyph acceptance. Fresh qualifiedAndroid/non-skipped RareHan/native four-font/all-Han/rendered checks pending.",
        "Compatible kanji-exclusion-aware client required. QualifiedAndroidbf30cdead approved pair-guard/schema-only backport, NOT latest application main.",
        "Published126/1228,1102 acceptance remainder unchanged. Six earlier N2 placements separate; physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates retained; no101 or second runner.",
    ]
    p["nextAction"] = NEXT
    save(S / "batch-100-progress.json", p)
    print("Twelve pinned paths generated and local UNREVIEWED ledgers prepared; no new word identity.")


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(child) for child in element))


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "100")
    plan = load(S / "batch-100-authoring-plan.json")
    ledger = load(S / "batch-100-progress.json")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
        inputs[name] = raw
    jm = inputs["n1-implementation-JMdict_e.gz"]
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    packets = []
    for i, packet in enumerate(ledger["dictionaryPackets"]):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        suffix = "full-family-reading.txt.gz" if i == 0 else "comparison-full-family-reading.txt.gz"
        lines = gzip.decompress((S / f"batch-100-{suffix}").read_bytes()).decode("utf-8").splitlines()
        assert [canonical(ET.fromstring(line)) for line in lines] == [
            canonical(e) for e in ET.fromstring(raw)]
        packets.append({"xml": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    expected_records = ET.parse(S / "batch-100-comparison-kanjidic2.xml").getroot().findall("character")
    records = {e.findtext("literal"): canonical(e) for e in expected_records}
    actual = {}
    for _, element in ET.iterparse(io.BytesIO(kd), events=["end"]):
        if element.tag == "character":
            char = element.findtext("literal")
            if char in records:
                actual[char] = canonical(element)
            element.clear()
    assert actual == records and len(actual) == 13
    assert canonical(ET.parse(S / "batch-100-kanjidic2.xml").getroot().find("character")) == actual[CHAR]
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and named[110] == CHAR
    source = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert source == load(S / "batch-100-input-metadata.json")["sourceIndexRecord"]
    assert metadata(R, f"kanji/{CHAR}.md") == plan["proposedMetadata"]
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
    current_chars = {p.stem for p in (R / "kanji").glob("*.md")}
    previous = json.loads(git("show", f"{MAIN}:manifest.json"))
    previous_chars = {Path(p).stem for p in previous["files"] if p.startswith("kanji/")}
    assert current_chars - previous_chars == {CHAR} and not previous_chars - current_chars
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in "保案派第策結")
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/創作.md"}
    pairs = {(r["kanji"], r["article"]) for r in plan["supportMappings"]}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 5
    for name in plan["reusedSupportArticles"]:
        assert {(c, name) for c in metadata(R, name)["kanji"]} <= pairs
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / f"kanji/{c}.md").read_text(encoding="utf-8")
    for name, level, n in [("words/創作.md", 2, 13), ("words/作る.md", 5, 5)]:
        m = metadata(R, name)
        assert m["jlpt"] == level and len(m["quiz_exclusions"]) == n
        assert m["quiz_exclusions"] == ledger["wordQuizAudit"]["preservedOriginalExclusions"][name]
    for row in plan["quizPlan"]["distractors"] + plan["quizPlan"]["directGuards"]:
        name = f"kanji/{row['kanji']}.md"
        m = metadata(R, name)
        assert m["title"] == row["label"]
        if name not in REUSED:
            assert sha((R / name).read_bytes()) == load(
                S / "batch-100-preparation-audit.json")["inspectedArticleHashes"][name]
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    verified = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        assert section in {"files", "scenes", "listening", "curriculum", "listeningTasks",
                           "images", "audio", "listeningTaskAudio", "listeningTaskImages"}
        for name, expected in entries.items():
            value = (sha((R / name).read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
            assert value == expected, name
            verified += 1
    assert verified == 8453
    svg = (S / "batch-100-kanjivg.svg").read_bytes()
    proof = load(S / "batch-100-stroke-evidence.json")
    assert sha(svg) == proof["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == proof["gitBlob"]
    assert svg == (C / "inputs" / "n1-05275-70a0b7ae.svg").read_bytes()
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert [p.attrib["id"] for p in paths] == [f"kvg:05275-s{i}" for i in range(1, 13)]
    geometry = load(R / f"strokes/{CHAR}.json")
    assert geometry == convert(CHAR, svg.decode("utf-8")) and geometry["viewBox"] == [0, 0, 109, 109]
    for i, stroke in enumerate(geometry["strokes"], 1):
        assert stroke["id"] == i and len(stroke["points"]) == 16
        assert all(len(p) == 2 and all(math.isfinite(v) for v in p) for p in stroke["points"])
    save(S / "batch-100-draft-stroke-audit.json", dict(
        proof, converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / f"strokes/{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, finite16pointPolylines=12, nativeDrawingAccepted=False))
    text = (R / f"kanji/{CHAR}.md").read_text(encoding="utf-8")
    text += "".join(row["after"] for row in ledger["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-100-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    save(S / "batch-100-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "100", "completeArticleScope": [f"kanji/{CHAR}.md"],
        "changedReusedScope": ledger["changedReusedPassages"], "actualHanCount": len(han),
        "actualHan": han, "fonts": fonts, "rareHanRangeCharacters": rare,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in [f"kanji/{CHAR}.md"] + REUSED},
        "nativeFontAcceptance": "pending",
        "limits": "Cmap absence is not glyph failure. Fresh four-font/all-Han/native gates pending; unchanged reused text is inherited, not fresh font acceptance scope.",
    })
    unchanged = 0
    for name, expected in load(S / "batch-100-preparation-audit.json")["inspectedArticleHashes"].items():
        if name not in REUSED:
            assert sha((R / name).read_bytes()) == expected, name
            unchanged += 1
    before, now = load(L / "progress-before-747.json"), load(C / "progress.json")
    assert all(now[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    result.update(
        schemaVersion=1, execution=747, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=len(inputs), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=len(actual),
        originalBaselineMetadataAndStrokesPreserved=counts, baselineMetadataExceptions=exceptions,
        baselineKanjiDistractorException={"kanji/山.md": ["川", "出", "木"]},
        allMappedReciprocalPairs=5, directedLinksVerified=10, newDirections=5,
        newDirectKanjiExclusionPairs=8, newDirectWordExclusionPairs=0,
        preservedWordExclusions=ledger["wordQuizAudit"]["preservedOriginalExclusions"],
        originalSourcePreparationArticlesByteUnchanged=unchanged, reusedMetadataPreserved=REUSED,
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        currentCounts={"kanji": len(current_chars), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current_chars),
                       "namedSourceMembersPresent": len(current_chars & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=126,
        remainingAdditions=1102, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-100-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "prepare", "audit"])
    globals()[parser.parse_args().step]()
