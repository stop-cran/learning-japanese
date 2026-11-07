"""Batch102 bounded local draft, verification and history-preserving checkpoint."""
import argparse
import copy
import gzip
import hashlib
import io
import json
import math
import shutil
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "9bcae3c2-8513-424c-b948-7868e1fd3719"
BASE = "a47f728aba421ed41618e6892b0aa26db2ec7c81"
MAIN = "1621cf6cbd2283d377936c77f9c81851baffdf20"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u52a3"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata

NEXT = (
    "SAME102 TWO serial blind different-model-family initial textual reviews on the normally "
    "signed LOCAL UNREVIEWED draft: complete new劣 and necessary優劣, exact navigation-only "
    "words/劣る.md and kanji/優.md changes; correctness/scoped coverage/phone comprehensibility "
    "on ONE fixed snapshot. Same frozen69member+43comparison families/16rawcharacterrecords/"
    "THREE actual publicdictionary pages and actual labels. Full[レツ]/[おと.る] source order "
    "and both selections; own-row linked優劣ゆうれつ and existing劣るおとるN3; onlyれつ/おとる. "
    "優劣 is two-sided relative superiority/inferiority NOT inferiority alone; no wordlevel inferred. "
    "All reused metadata/levels/readings/exclusions unchanged. THREEallmappedpairs/SIXdirections/"
    "ONEactivatedbaselinepair include 優-to-優劣. Three wrong labels努功省, SEVEN DIRECT symmetric "
    "NONTRANSITIVE kanji guards and FOUR direct word guards need independent semantic review; "
    "N1-only requires tag/random fallback since only功 is N1. SIX pinned generated paths, "
    "canonical力19 below少, labelledmodernshapemnemonic/structure-unclassified/no adopted "
    "etymology. ActualHan/cmaps NOT fourfont/native rendered acceptance. Original77269family "
    "inspection/773sourcecompletion retained; this774 freshly reads applicable families and "
    "actual changed/comparison articles, not fresh69-family certification. Discover actual CLI "
    "model IDs; serial reviewer processes AND internal tools, actual exit before next reviewer, "
    "preserve complete original reports/models/snapshot/interruptions/readlimits. Reconcile "
    "by precise evidence and reuse original sessions for bounded changed-passage confirmation. "
    "Then qualified non-skipped Androidbf30cdead RealContent/RareHan, productionContentSyncONCE/"
    "native N1/All/meaning/curatedreading/drawing/article/Back/offline/fourfont/allHan/rendered "
    "review, combinedcurrentmain/allrequiredPython/vocabulary/normal signing/ownerfastforward/"
    "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed80MiB"
    "inflated56MiBretained/perfilepathmedia/verifiedownerissue gates remain mandatory. "
    "No unreviewedpush/103/authoragents/concurrentheavywork/secondrunner/signingretry/"
    "guardincrease. Verify whollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/"
    "exactsession. Parent5920 ownsrunner.lock: no childacquire/delete/unlock/readprobe. "
    "Approvedcontrol/committedsource/frozeninputs only, not optional historicalsessionrecipes; "
    "preserve/report/yield actualnewdenial/signinghang/uncertainownership. QualifiedAndroid "
    "approvedpairguard+schemaonly, NOT unrelated latestmain. Published128/1228,1100acceptance "
    "remainder unchanged; six earlierN2placements保案派第策結 separate, never duplicate/relevel. "
    "CompatibleAndroid#125+#132 required; oldclientsignorecuration/guards. Physicalphone/"
    "generalrelease/whole-setoutstanding;projectincomplete. Historical limitations preserved."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".774.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def identity():
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (773, "102", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    assert git("branch", "--show-current") == "content/n1-kanji"
    role = load(L / "preflight-774.json")
    assert role["sessionId"] == L.name and role["liveParentPid"] == 5920 and not role["lockTouched"]
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution773CoordinatorCheckpoint"] == p["execution773CoordinatorCheckpoint"]
    assert not (L / "progress-before-774.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-774.json")
    state = {
        "execution": 774, "batch": "102", "startingHead": BASE, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME102 bounded LOCAL UNREVIEWED runtime draft/freeze only; no reviewer, Android/native, publication,103 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed before implementation. Operative contract, full approved issue and final773 inspected directly; historical middle parsed, not freshly semantically re-reviewed. Initial output encoding failure occurred after complete loading."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution774StartingState"] = state
    p.update(stage="batch-102-local-unreviewed-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with complete live history; clean signed worktrees verified.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    plan = load(S / "batch-102-authoring-plan.json")
    assert plan["sourcePreparationComplete"]
    proof = load(S / "batch-102-stroke-evidence.json")
    svg = (S / "batch-102-kanjivg.svg").read_bytes()
    assert len(svg) == proof["bytes"] and sha(svg) == proof["sha256"]
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 6
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    for suffix in ["membership", "progress"]:
        path = S / f"batch-102-{suffix}.json"
        row = load(path)
        assert row["drafted"] == [] and row["reviewClosed"] == [] and row["published"] == []
        row["sourcePreparationLimits"] = row["limits"]
        row.update(status="local-unreviewed-draft", drafted=[CHAR],
                   sourcePreparationComplete=True, runtimeChanged=True)
        row["limits"] = "LOCAL UNREVIEWED draft only, not independent review closure, app/native/rendered acceptance or publication."
        save(path, row)
    ledger = load(S / "batch-102-progress.json")
    ledger["dictionaryPackets"] = [
        {"selection": "batch-102-lexical-selection.json", "xml": "batch-102-jmdict.xml"},
        {"selection": "batch-102-comparison-selection.json", "xml": "batch-102-comparison-jmdict.xml"},
    ]
    ledger["readingDispositions"] = []
    for row in plan["readingDispositions"]:
        item = copy.deepcopy(row)
        item.update(kanji=CHAR, selected=True, sourceOnly=False,
                    article=row["example"]["article"],
                    reason=row["allocation"] + " " + row["usefulness"])
        ledger["readingDispositions"].append(item)
    ledger["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["reading"],
         "entryIds": [row["entryId"]], "newArticle": row["newArticle"],
         "status": "local-unreviewed-draft"}
        for row in plan["supportMappings"] if row["kanji"] == CHAR
    ]
    ledger["requiredReciprocalPairs"] = [[CHAR, r["article"]] for r in ledger["supportMappings"]]
    ledger["allMappedReciprocalPairs"] = plan["allMappedReciprocalPairs"]
    ledger["changedReusedPassages"] = [
        {"article": row["article"], "before": row["old"], "after": row["new"]}
        for row in plan["reusedPassageChanges"]
    ]
    ledger["curatedProjection"] = [{
        "kanji": CHAR, "quizOnyomi": ["レツ"], "quizKunyomi": ["おと.る"],
        "onKeys": ["れつ"], "kunKeys": ["おとる"],
    }]
    ledger["quizAudit"] = {CHAR: {
        "title": plan["proposedMetadata"]["title"],
        "distractors": plan["proposedMetadata"]["distractors"],
        "labels": [r["label"] for r in plan["quizPlan"]["distractors"]],
        "meaningDecisions": plan["quizPlan"]["distractors"],
        "directExclusions": plan["quizPlan"]["directGuards"],
        "guardSemantics": plan["quizPlan"]["guardSemantics"],
        "poolLimits": plan["quizPlan"]["fallbackScope"],
        "limits": "Author semantic audit, not independent review or actual production-builder/native fallback acceptance.",
    }}
    ledger["wordQuizAudit"] = {
        "directExclusions": [{"word": "優劣", "exclude": plan["newSupportMetadata"]["quiz_exclusions"]}],
        "meaningDecisions": plan["quizPlan"]["newWordGuards"],
        "newOrRewordedTitles": 1, "confusableInventory": "Consulted docs/confusable-words.md and exact term search; no matching row.",
        "preservedOriginalExclusions": {"words/劣る.md": metadata(R, "words/劣る.md").get("quiz_exclusions", [])},
        "limits": "Four new direct symmetric NONTRANSITIVE pairs only; no neighbor clique or exhaustive corpus semantic certification.",
    }
    ledger["draftAuthorInspection"] = {
        "execution": 774, "sourceCheckpoint": BASE,
        "freshCompleteApplicableMemberFamilies": ["1539620", "1558400", "2108410"],
        "freshCompleteComparisonFamilies": [
            "1151260", "1184140", "1240820", "1275070", "1320640", "1324520",
            "1348910", "1351040", "1406770", "1430070", "1434180", "1483560",
            "1490740", "1497980", "1549500", "2080200", "2411570", "2411590", "2836356"],
        "freshCompleteTargetCharacterRecord": True,
        "freshCompleteExistingArticles": [
            "words/劣る.md", "kanji/優.md", "kanji/努.md", "kanji/功.md", "kanji/省.md",
            "kanji/弱.md", "kanji/悪.md", "kanji/下.md", "kanji/低.md", "kanji/貧.md",
            "kanji/負.md", "kanji/少.md", "words/比較.md", "words/質.md",
            "words/長短.md", "words/利害.md", "words/損得.md"],
        "inheritedSourceInspection": "Original772 inspected69 complete member families;773 freshly inspected3 applicable plus43 comparison families,30 existing articles and relevant fields of16 raw character records. No fresh69-family or all43-comparison reread claimed here.",
        "publicLookup": "Fresh read of all committed authority-headed extracted blocks. Original upstream retrieval, raw HTML and extraction limits preserved; no new upstream fetch or measured frequency claim.",
        "limits": "Author inspection only, not independent review, uniform source comprehension, native-speaker certification, rendered or phone acceptance.",
    }
    ledger["limits"] = [
        "LOCAL UNREVIEWED draft only; no reviewer, app/native/rendered acceptance or runtime publication.",
        "Both source readings/order retained and selected, with own-row links; onlyれつ/おとる offered.",
        "優劣 is two-sided relative superiority/inferiority; no inferred word level. Existing劣る and優 retain N3 and all metadata; exact two navigation-only changes.",
        "Three all-mapped pairs/six directions/one activated baseline pair, including existing優-to-new優劣.",
        "Seven direct symmetric NONTRANSITIVE kanji guards and four word guards, not neighbor-neighbor edges. Actual production-builder/default N1-only fallback acceptance pending; two curated choices outside N1.",
        "Canonical力19 below少; six pinned converted paths; modern-shape mnemonic only, structure-unclassified/no phonetic/history claim.",
        "ActualHan/cmaps are not rendered glyph acceptance. Fresh qualifiedAndroid/non-skipped RareHan/native four-font/all-Han/rendered review gates pending.",
        "Compatible reading-curation/kanji-exclusion-aware client required. QualifiedAndroidbf30cdead approved pair-guard/schema-only backport, NOT latest application main.",
        "Published128/1228,1100 acceptance remainder unchanged. Six earlierN2placements separate; physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates retained; no103 or second runner.",
    ]
    ledger["nextAction"] = NEXT
    save(S / "batch-102-progress.json", ledger)
    print("Six pinned paths generated and LOCAL UNREVIEWED ledgers prepared.")


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(child) for child in element))


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    import yaml

    identity()
    result = batch_audit(R, "102")
    plan = load(S / "batch-102-authoring-plan.json")
    ledger = load(S / "batch-102-progress.json")
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
        lines = gzip.decompress((S / f"batch-102-{suffix}").read_bytes()).decode("utf-8").splitlines()
        assert [canonical(ET.fromstring(line)) for line in lines] == [canonical(e) for e in ET.fromstring(raw)]
        packets.append({"xml": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    records = {e.findtext("literal"): canonical(e) for e in ET.parse(
        S / "batch-102-comparison-kanjidic2.xml").getroot().findall("character")}
    actual = {}
    for _, element in ET.iterparse(io.BytesIO(kd), events=["end"]):
        if element.tag == "character":
            char = element.findtext("literal")
            if char in records:
                actual[char] = canonical(element)
            element.clear()
    assert actual == records and len(actual) == 16
    assert canonical(ET.parse(S / "batch-102-kanjidic2.xml").getroot().find("character")) == actual[CHAR]
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and named[112] == CHAR
    assert metadata(R, f"kanji/{CHAR}.md") == plan["proposedMetadata"]
    assert metadata(R, "words/優劣.md") == plan["newSupportMetadata"]
    before_manifest = json.loads(git("show", f"{BASE}:manifest.json"))
    current_chars = {p.stem for p in (R / "kanji").glob("*.md")}
    previous_chars = {Path(p).stem for p in before_manifest["files"] if p.startswith("kanji/")}
    assert current_chars - previous_chars == {CHAR} and not previous_chars - current_chars
    archive = subprocess.check_output(["git", "-C", str(R), "archive", BASE, "kanji", "words"])
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        old_text = {m.name: tar.extractfile(m).read().decode("utf-8")
                    for m in tar if m.isfile()}
    for name, text in old_text.items():
        assert metadata(R, name) == yaml.safe_load(text.split("---", 2)[1]), name
    baseline = load(S / "baseline-inventory.json")
    baseline_counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            current = metadata(R, name)
            for key, value in info["metadata"].items():
                if key == "quiz_exclusions":
                    assert set(value) <= set(current.get(key, [])), name
                elif name == "kanji/山.md" and key == "distractors":
                    assert current[key] == ["川", "出", "木"]
                else:
                    assert current[key] == value, (name, key)
            baseline_counts[kind] += 1
        elif kind == "strokes":
            assert sha((R / name).read_bytes()) == info["sha256"], name
            baseline_counts[kind] += 1
    assert baseline_counts == {"kanji": 985, "words": 4942, "strokes": 985}
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in "保案派第策結")
    activated = {f"words/{p.name}" for p in (R / "words").glob("*.md")
                 if CHAR in metadata(R, f"words/{p.name}")["kanji"]}
    assert activated == {"words/劣る.md", "words/優劣.md"}
    pairs = {(r["kanji"], r["article"]) for r in plan["supportMappings"]}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 3
    for name in plan["newSupportArticles"] + plan["reusedSupportArticles"]:
        assert {(c, name) for c in metadata(R, name)["kanji"]} <= pairs
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / f"kanji/{c}.md").read_text(encoding="utf-8")
    assert metadata(R, "words/劣る.md")["jlpt"] == metadata(R, "kanji/優.md")["jlpt"] == 3
    for row in plan["quizPlan"]["distractors"] + plan["quizPlan"]["directGuards"]:
        assert metadata(R, f"kanji/{row['kanji']}.md")["title"] == row["label"]
    for row in plan["quizPlan"]["newWordGuards"]:
        assert metadata(R, f"words/{row['word']}.md")["title"] == row["label"]
    guards = plan["proposedMetadata"]["quiz_exclusions"]
    assert len(guards) == len(set(guards)) == 7
    distractors = plan["proposedMetadata"]["distractors"]
    assert not set(guards) & set(distractors)
    for c in distractors:
        assert not (set(metadata(R, f"kanji/{c}.md").get("quiz_exclusions", []))
                    & (set(distractors) | {CHAR}))
    assert "jlpt" not in metadata(R, "words/優劣.md")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    reused = {r["article"] for r in plan["reusedPassageChanges"]}
    verified = unchanged = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, expected in entries.items():
            value = (sha((R / name).read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
            assert value == expected, name
            verified += 1
            if name in before_manifest.get(section, {}) and name not in reused:
                assert expected == before_manifest[section][name], name
                unchanged += 1
    assert verified == 8458 and unchanged == 8453
    svg = (S / "batch-102-kanjivg.svg").read_bytes()
    proof = load(S / "batch-102-stroke-evidence.json")
    assert sha(svg) == proof["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == proof["gitBlob"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert [p.attrib["id"] for p in paths] == [f"kvg:052a3-s{i}" for i in range(1, 7)]
    geometry = load(R / f"strokes/{CHAR}.json")
    assert geometry == convert(CHAR, svg.decode("utf-8")) and geometry["viewBox"] == [0, 0, 109, 109]
    for i, stroke in enumerate(geometry["strokes"], 1):
        assert stroke["id"] == i and len(stroke["points"]) == 16
        assert all(len(p) == 2 and all(math.isfinite(v) for v in p) for p in stroke["points"])
    save(S / "batch-102-draft-stroke-audit.json", dict(
        proof, converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / f"strokes/{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, finite16pointPolylines=6, nativeDrawingAccepted=False))
    for receipt in load(S / "batch-102-public-source-receipts.json"):
        compressed = (S / receipt["archive"]).read_bytes()
        raw = gzip.decompress(compressed)
        assert sha(compressed) == receipt["archiveSha256"]
        assert sha(raw) == receipt["rawSha256"] and len(raw) == receipt["rawBytes"]
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    scope = [f"kanji/{CHAR}.md", "words/優劣.md"]
    text = "".join((R / name).read_text(encoding="utf-8") for name in scope)
    text += "".join(row["after"] for row in ledger["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-102-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    save(S / "batch-102-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "102", "completeArticleScope": scope,
        "changedReusedScope": ledger["changedReusedPassages"], "actualHanCount": len(han),
        "actualHan": han, "fonts": fonts, "rareHanRangeCharacters": rare,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in scope + sorted(reused)},
        "nativeFontAcceptance": "pending",
        "limits": "Cmap presence is not rendering acceptance. Fresh four-font/all-Han/native gates pending; unchanged reused text is inherited.",
    })
    old, now = load(L / "progress-before-774.json"), load(C / "progress.json")
    assert all(now[k] == v for k, v in old.items() if k not in {"stage", "nextAction", "blocker"})
    result.update(
        schemaVersion=1, execution=774, stage="local-unreviewed-draft", sourceCheckpoint=BASE,
        frozenInputHashesVerified=len(inputs), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=len(actual),
        originalBaselinePreserved=baseline_counts, allExistingMetadataRecordsExactlyPreserved=len(old_text),
        allMappedReciprocalPairs=3, directedLinksVerified=6, newDirections=6,
        newDirectKanjiExclusionPairs=7, newDirectWordExclusionPairs=4,
        allRuntimePayloadHashesVerified=verified, priorRuntimeHashesUnchangedOutsideTwoNavigationChanges=unchanged,
        actualHanCount=len(han), actualCmapAbsences=fonts[0]["allActualMissing"],
        rareHanRangeCharacters=rare,
        currentCounts={"kanji": len(current_chars), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current_chars),
                       "namedSourceMembersPresent": len(current_chars & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=128,
        remainingAdditions=1100, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-102-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "prepare", "audit"])
    globals()[parser.parse_args().step]()
