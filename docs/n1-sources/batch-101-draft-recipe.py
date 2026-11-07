"""Prepare and audit batch101's bounded LOCAL UNREVIEWED draft."""
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
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "ff1e9841-2508-4a32-b027-5ce26ca5834d"
HEAD = "b1da01c20d896866431670213d584c5ca056b096"
MAIN = "ba1a7f467a2431523e3131d4f259c1d3260c93af"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "功"
REUSED = ["words/功績.md", "words/成功.md", "kanji/成.md"]
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".764.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


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
    assert (p["checkpoint"], p["batch"], p["status"]) == (763, "101", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    assert git("branch", "--show-current") == "content/n1-kanji"
    role = load(L / "preflight-764.json")
    assert role["sessionId"] == L.name and role["liveParentPid"] == 5920 and not role["lockTouched"]
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution763CoordinatorCheckpoint"] == p["execution763CoordinatorCheckpoint"]
    assert not (L / "progress-before-764.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-764.json")
    state = {
        "execution": 764, "batch": "101", "startingHead": HEAD, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME101 bounded LOCAL UNREVIEWED runtime draft/freeze only; no reviewer, Android/native, publication,102 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed before implementation. Operative contract, full approved issue and final763 inspected directly; historical middle parsed, not freshly semantically re-reviewed. Initial output encoding failure occurred after full loading."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution764StartingState"] = state
    p.update(stage="batch-101-local-unreviewed-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with all live history; clean signed worktrees verified.")


def prepare():
    from generate_strokes import convert, KANJIVG_REVISION
    identity()
    plan = load(S / "batch-101-authoring-plan.json")
    proof = load(S / "batch-101-stroke-evidence.json")
    svg = (S / "batch-101-kanjivg.svg").read_bytes()
    assert len(svg) == proof["bytes"] and sha(svg) == proof["sha256"]
    assert svg == (C / "inputs" / "n1-0529f-70a0b7ae.svg").read_bytes()
    assert KANJIVG_REVISION == proof["revision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == proof["converterNormalizedSha256"]
    geometry = convert(CHAR, svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 5
    target = R / "strokes" / f"{CHAR}.json"
    assert not target.exists()
    target.write_text(json.dumps(geometry, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    frozen = load(S / "batch-101-membership.json")
    assert frozen["membership"] == [CHAR] and frozen["sourceRows"] == [112]
    frozen["sourcePreparationLimits"] = frozen["limits"]
    frozen.update(status="local-unreviewed-draft", drafted=[CHAR],
                  sourcePreparationComplete=True, runtimeChanged=True)
    frozen["limits"] = "LOCAL UNREVIEWED draft, not independent review closure, native acceptance or publication."
    save(S / "batch-101-membership.json", frozen)
    p = load(S / "batch-101-progress.json")
    assert p["status"] == "source-prepared-not-drafted"
    p["sourcePreparationLimits"] = p["limits"]
    p.update(status="local-unreviewed-draft", drafted=[CHAR], runtimeChanged=True)
    p["dictionaryPackets"] = [
        {"selection": "batch-101-lexical-selection.json", "xml": "batch-101-jmdict.xml"},
        {"selection": "batch-101-comparison-selection.json", "xml": "batch-101-comparison-jmdict.xml"},
    ]
    p["readingDispositions"] = []
    for row in plan["readingDispositions"]:
        r = copy.deepcopy(row)
        r.update(kanji=CHAR, selected=r["status"] == "selected", sourceOnly=False)
        if r["selected"]:
            r["article"] = r["examples"][0]["article"]
        r["reason"] = " ".join(r[k] for k in ["allocation", "usefulness", "qualification"] if k in r)
        p["readingDispositions"].append(r)
    p["supportMappings"] = [
        {"kanji": CHAR, "article": row["article"], "primaryReading": row["reading"],
         "entryIds": [row["entryId"]], "newArticle": False, "status": "local-unreviewed-draft"}
        for row in plan["supportMappings"] if row["kanji"] == CHAR
    ]
    p["requiredReciprocalPairs"] = [[CHAR, r["article"]] for r in p["supportMappings"]]
    p["allMappedReciprocalPairs"] = plan["allMappedReciprocalPairs"]
    p["changedReusedPassages"] = [
        {"article": r["article"], "before": r["old"], "after": r["new"]}
        for r in plan["reusedPassageChanges"]
    ]
    p["curatedProjection"] = [{
        "kanji": CHAR, "quizOnyomi": ["コウ"], "quizKunyomi": [],
        "onKeys": ["こう"], "kunKeys": [],
    }]
    p["quizAudit"] = {CHAR: {
        "title": plan["proposedMetadata"]["title"],
        "distractors": plan["proposedMetadata"]["distractors"],
        "labels": [r["label"] for r in plan["quizPlan"]["distractors"]],
        "meaningDecisions": plan["quizPlan"]["distractors"],
        "directExclusions": plan["quizPlan"]["directGuards"],
        "guardSemantics": plan["quizPlan"]["guardSemantics"],
        "poolLimits": plan["quizPlan"]["poolLimits"],
        "limits": "Author semantic audit, not independent review or actual production-builder/native fallback acceptance.",
    }}
    p["wordQuizAudit"] = {
        "directExclusions": [], "newOrRewordedTitles": 0,
        "preservedOriginalExclusions": {name: metadata(R, name).get("quiz_exclusions", [])
                                       for name in plan["reusedSupportArticles"]},
        "limits": "No new word identity, level, title or guard. All seven original 功績 exclusions and 成功 metadata unchanged.",
    }
    p["draftAuthorInspection"] = {
        "execution": 764, "sourceCheckpoint": HEAD,
        "freshCompleteApplicableMemberFamilies": ["1275070", "1275080", "1375690", "1872670", "2411570", "2411590", "2870785"],
        "freshCompleteComparisonFamilies": 23,
        "freshCompleteTargetCharacterRecord": True,
        "freshChangedArticles": REUSED,
        "freshCompleteDistractorArticles": ["kanji/加.md", "kanji/幼.md", "kanji/刀.md"],
        "inheritedSourceInspection": "Original762 inspected99 complete member families;763 read7 applicable plus23 comparison families,19 articles and relevant fields of18 raw character records. No fresh99-family reread claimed.",
        "publicLookup": "Fresh read of all committed authority-headed extracted blocks. Original upstream retrieval, raw HTML and extraction limits preserved; no new upstream fetch or measured frequency claim.",
        "limits": "Author inspection only, not independent review, uniform source comprehension, native-speaker certification, rendered or phone acceptance.",
    }
    p["limits"] = [
        "LOCAL UNREVIEWED draft only, no reviewer, app/native/rendered acceptance or runtime publication.",
        "All three source readings/order preserved; only コウ selected. ク valid religious-compound recognition, いさお a dated lexical noun, not merely nanori.",
        "Reused功績N2/成功N3 preserve all metadata, original seven功績 exclusions and all prose except exact navigation. No new support identity or inferred word level.",
        "Four all-mapped pairs/eight directions/five new directions/two activated baseline pairs; exact three navigation-only reused changes.",
        "Thirteen direct symmetric NONTRANSITIVE kanji guards, not neighbor-neighbor edges. Actual production-builder/default N1-only fallback acceptance pending; two curated choices are outside N1.",
        "Canonical力19 on the right, 工 left; five pinned generated paths, labelled modern-shape mnemonic only, structure-unclassified/no phonetic/history claim.",
        "ActualHan/cmaps are not rendered glyph acceptance. Fresh qualifiedAndroid/non-skipped RareHan/native four-font/all-Han/rendered review gates pending.",
        "Compatible reading-curation/kanji-exclusion-aware client required. QualifiedAndroidbf30cdead approved pair-guard/schema-only backport, NOT latest application main.",
        "Published127/1228,1101 acceptance remainder unchanged. Six earlierN2placements separate; physical-phone/general-release/whole-set outstanding.",
        "All original source/review/process/denial/OOM/read-depth/native/combined-main/signing/owner-push/terminal-CI/EVERY-immutable-ZIP-hash/budget/owner-issue gates retained; no102 or second runner.",
    ]
    p["nextAction"] = "SAME101 two serial blind different-model-family initial textual reviews on the signed LOCAL UNREVIEWED draft; all later acceptance/publication gates remain."
    save(S / "batch-101-progress.json", p)
    print("Five pinned paths generated and LOCAL UNREVIEWED ledgers prepared; no new word.")


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
    result = batch_audit(R, "101")
    plan = load(S / "batch-101-authoring-plan.json")
    ledger = load(S / "batch-101-progress.json")
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
        lines = gzip.decompress((S / f"batch-101-{suffix}").read_bytes()).decode("utf-8").splitlines()
        assert [canonical(ET.fromstring(line)) for line in lines] == [
            canonical(e) for e in ET.fromstring(raw)]
        packets.append({"xml": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    records = {e.findtext("literal"): canonical(e) for e in ET.parse(
        S / "batch-101-comparison-kanjidic2.xml").getroot().findall("character")}
    actual = {}
    for _, element in ET.iterparse(io.BytesIO(kd), events=["end"]):
        if element.tag == "character":
            char = element.findtext("literal")
            if char in records:
                actual[char] = canonical(element)
            element.clear()
    assert actual == records and len(actual) == 18
    assert canonical(ET.parse(S / "batch-101-kanjidic2.xml").getroot().find("character")) == actual[CHAR]
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and named[111] == CHAR
    assert metadata(R, f"kanji/{CHAR}.md") == plan["proposedMetadata"]
    before_manifest = json.loads(git("show", f"{HEAD}:manifest.json"))
    current_chars = {p.stem for p in (R / "kanji").glob("*.md")}
    previous_chars = {Path(p).stem for p in before_manifest["files"] if p.startswith("kanji/")}
    assert current_chars - previous_chars == {CHAR} and not previous_chars - current_chars
    baseline = load(S / "baseline-inventory.json")
    baseline_counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            original = info["metadata"]
            previous = metadata_from_base(name)
            current = metadata(R, name)
            assert current == previous, name
            for key, value in original.items():
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
    assert activated == {"words/功績.md", "words/成功.md"}
    pairs = {(r["kanji"], r["article"]) for r in plan["supportMappings"]}
    assert pairs == {tuple(p) for p in ledger["allMappedReciprocalPairs"]} and len(pairs) == 4
    for name in plan["reusedSupportArticles"]:
        assert {(c, name) for c in metadata(R, name)["kanji"]} <= pairs
        assert metadata(R, name) == metadata_from_base(name)
    for c, name in pairs:
        assert f"(../kanji/{c}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / f"kanji/{c}.md").read_text(encoding="utf-8")
    assert metadata(R, "words/功績.md")["jlpt"] == 2
    assert len(metadata(R, "words/功績.md")["quiz_exclusions"]) == 7
    assert metadata(R, "words/成功.md")["jlpt"] == 3
    for row in plan["quizPlan"]["distractors"] + plan["quizPlan"]["directGuards"]:
        assert metadata(R, f"kanji/{row['kanji']}.md")["title"] == row["label"]
    guards = plan["proposedMetadata"]["quiz_exclusions"]
    assert len(guards) == len(set(guards)) == 13
    assert not set(guards) & set(plan["proposedMetadata"]["distractors"])
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    verified = unchanged = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, expected in entries.items():
            value = (sha((R / name).read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
            assert value == expected, name
            verified += 1
            if name in before_manifest.get(section, {}) and name not in REUSED:
                assert expected == before_manifest[section][name], name
                unchanged += 1
    assert verified == 8455 and unchanged == 8450
    svg = (S / "batch-101-kanjivg.svg").read_bytes()
    proof = load(S / "batch-101-stroke-evidence.json")
    assert sha(svg) == proof["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == proof["gitBlob"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert [p.attrib["id"] for p in paths] == [f"kvg:0529f-s{i}" for i in range(1, 6)]
    geometry = load(R / f"strokes/{CHAR}.json")
    assert geometry == convert(CHAR, svg.decode("utf-8")) and geometry["viewBox"] == [0, 0, 109, 109]
    for i, stroke in enumerate(geometry["strokes"], 1):
        assert stroke["id"] == i and len(stroke["points"]) == 16
        assert all(len(p) == 2 and all(math.isfinite(v) for v in p) for p in stroke["points"])
    save(S / "batch-101-draft-stroke-audit.json", dict(
        proof, converted=True, output=f"strokes/{CHAR}.json",
        outputSha256=sha((R / f"strokes/{CHAR}.json").read_bytes()),
        geometryExactlyRegenerated=True, finite16pointPolylines=5, nativeDrawingAccepted=False))
    text = (R / f"kanji/{CHAR}.md").read_text(encoding="utf-8")
    text += "".join(row["after"] for row in ledger["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-101-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    save(S / "batch-101-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "101", "completeArticleScope": [f"kanji/{CHAR}.md"],
        "changedReusedScope": ledger["changedReusedPassages"], "actualHanCount": len(han),
        "actualHan": han, "fonts": fonts, "rareHanRangeCharacters": rare,
        "scopeHash": {n: sha((R / n).read_bytes()) for n in [f"kanji/{CHAR}.md"] + REUSED},
        "nativeFontAcceptance": "pending",
        "limits": "Cmap presence is not rendering acceptance. Fresh four-font/all-Han/native gates pending; unchanged reused text is inherited.",
    })
    old, now = load(L / "progress-before-764.json"), load(C / "progress.json")
    assert all(now[k] == v for k, v in old.items() if k not in {"stage", "nextAction", "blocker"})
    result.update(
        schemaVersion=1, execution=764, stage="local-unreviewed-draft", sourceCheckpoint=HEAD,
        frozenInputHashesVerified=len(inputs), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=len(actual),
        originalBaselinePreserved=baseline_counts, baselineMetadataExactlyPreservedAgainstSignedSourceBase=True,
        allMappedReciprocalPairs=4, directedLinksVerified=8, newDirections=5,
        newDirectKanjiExclusionPairs=13, newDirectWordExclusionPairs=0,
        preservedWordExclusions=ledger["wordQuizAudit"]["preservedOriginalExclusions"],
        allRuntimePayloadHashesVerified=verified, priorRuntimeHashesUnchangedOutsideThreeNavigationChanges=unchanged,
        actualHanCount=len(han), actualCmapAbsences=fonts[0]["allActualMissing"],
        rareHanRangeCharacters=rare,
        currentCounts={"kanji": len(current_chars), "words": len(list((R / "words").glob("*.md"))),
                       "n1Labels": sum(metadata(R, f"kanji/{c}.md")["jlpt"] == 1 for c in current_chars),
                       "namedSourceMembersPresent": len(current_chars & set(named))},
        separateEarlierLevelSourceMembers=sorted("保案派第策結"), publishedAdditions=127,
        remainingAdditions=1101, draftOnlyAdditions=[CHAR], runtimePublished=False,
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False, parentLockTouched=False,
        actualNewPermissionDenials=[], limits=ledger["limits"])
    save(S / "batch-101-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def metadata_from_base(name):
    import yaml
    return yaml.safe_load(BASE_TEXT[name].split("---", 2)[1])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "prepare", "audit"])
    step = parser.parse_args().step
    if step == "audit":
        import tarfile
        archive = subprocess.check_output(["git", "-C", str(R), "archive", HEAD, "kanji", "words"])
        with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
            BASE_TEXT = {m.name: tar.extractfile(m).read().decode("utf-8")
                         for m in tar if m.isfile()}
    globals()[step]()
