"""Batch102 bounded comparison-source checkpoint, without runtime edits."""
import argparse
import copy
import gzip
import hashlib
import json
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
L = C / "logs" / "e0bfa045-79ef-477b-8a4c-94a9364ded48"
BASE = "e82cbc214adb2e034d1c99482fa289d8cd39a3c9"
MAIN = "1621cf6cbd2283d377936c77f9c81851baffdf20"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as manifest_sha256
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".773.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", root=root)


def frozen():
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == snapshot["jmdict"]["xmlSha256"]
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, inputs, ET.fromstring(jm), ET.fromstring(kd)


def start():
    clean(R, BASE)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (772, "102", "continue")
    assert p["lastPublishedCommit"] == MAIN and p["remainingAdditions"] == 1100
    role = load(L / "preflight-773.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["checkpoint"] == 772
    assert checkpoint["execution772CoordinatorCheckpoint"] == p["execution772CoordinatorCheckpoint"]
    assert not (L / "progress-before-773.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-773.json")
    state = {
        "execution": 773, "batch": "102", "startingHead": BASE, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME102 bounded comparison-source completion; no runtime draft, reviewer, Android/native, publication,103 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed before acting. Operative contract, complete approved issue and final772 inspected directly; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main unchanged. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution773StartingState"] = state
    p.update(stage="batch-102-comparison-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def comparisons():
    snapshot, inputs, jm, kd = frozen()
    spellings = [
        "\u52aa\u3081\u308b", "\u529f", "\u7701\u304f", "\u7701\u307f\u308b",
        "\u5f31\u3044", "\u60aa\u3044", "\u4e0b", "\u4f4e\u3044", "\u8ca7\u3057\u3044",
        "\u8ca0\u3051\u308b", "\u6557\u308c\u308b", "\u6b20\u3051\u308b", "\u5c11\u306a\u3044",
        "\u529b", "\u8cea", "\u512a\u3057\u3044", "\u512a\u308c\u308b",
        "\u6bd4\u8f03", "\u5dee", "\u76f8\u9055", "\u9055\u3044", "\u5229\u5bb3",
        "\u640d\u5f97", "\u9577\u6240", "\u77ed\u6240", "\u9577\u77ed",
        "\u7279\u9577", "\u4e0a\u7b49", "\u529f\u7e3e",
    ]
    member_ids = set(load(S / "batch-102-lexical-selection.json")["entryIds"])
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(k.text in spellings for k in e.findall("k_ele/keb"))
           and e.findtext("ent_seq") not in member_ids]
    selection = {
        "schemaVersion": 1, "batch": "102", "entryIds": ids, "exactSpellings": spellings,
        "memberPacketAlsoApplicable": ["1539620", "1558400"],
        "selectionRule": "Every complete frozen family with an exact selected keb, excluding member-packet families. Preserve all aliases, readings, restrictions and senses.",
        "scope": "Actual distractor and possible fallback-overlap labels; source extraction is not independent review or an assertion that all matches are teaching examples.",
    }
    save(S / "batch-102-comparison-selection.json", selection)
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / "batch-102-comparison-jmdict.xml").write_bytes(raw)
    compact = []
    for entry in ET.fromstring(raw):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    text = ("\n".join(compact) + "\n").encode("utf-8")
    (C / "batch-102-comparison-full-family-reading.txt").write_bytes(text)
    (S / "batch-102-comparison-full-family-reading.txt.gz").write_bytes(gzip.compress(text, mtime=0))
    chars = "\u52a3\u52aa\u529f\u7701\u5f31\u60aa\u4e0b\u4f4e\u8ca7\u8ca0\u6557\u6b20\u5c11\u529b\u8cea\u512a"
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / "batch-102-comparison-kanjidic2.xml").write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    print(json.dumps({"families": len(ids), "entryIds": ids, "characters": list(chars)}))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(child) for child in element))


def prepare():
    from fontTools.ttLib import TTFont
    import yaml

    _, inputs, _, _ = frozen()
    plan = load(S / "batch-102-authoring-plan.json")
    baselines = []
    for name in plan["authorInspection"]["completeExistingArticlesRead"]:
        baselines.append({"article": name, "rawSha256": sha((R / name).read_bytes()),
                          "metadata": metadata(R, name),
                          "scope": "Full existing article freshly read; preserved except exact planned navigation replacement, if assigned."})
    simulations = []
    for change in plan["reusedPassageChanges"]:
        original = (R / change["article"]).read_text(encoding="utf-8")
        assert original.count(change["old"]) == 1, change["article"]
        assert change["new"] not in original, change["article"]
        proposed = original.replace(change["old"], change["new"], 1)
        assert proposed.replace(change["new"], change["old"], 1) == original
        assert yaml.safe_load(proposed.split("---", 2)[1]) == metadata(R, change["article"])
        simulations.append({**change, "oldTextSha256": sha(original.encode()),
                            "proposedTextSha256": sha(proposed.encode()),
                            "metadataPreservedExactly": True, "runtimeEdited": False})
    save(S / "batch-102-baseline-plan.json", {
        "schemaVersion": 1, "batch": "102", "baseCommit": BASE,
        "completeExistingArticles": baselines, "exactNavigationSimulations": simulations,
        "newWordOnly": "words/\u512a\u52a3.md", "existingWordExclusionsUnchanged": True,
        "limits": "In-memory source-plan simulation only, not a runtime diff or independent review.",
    })
    han = sorted({c for c in plan["proposedHanText"] if
                  0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for old in load(S / "batch-101-font-preparation.json")["fonts"]:
        path = Path(old["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == old["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": old["sha256"],
                      "keyGlyphPresence": {c: ord(c) in cmap for c in han},
                      "allProposedMissing": [c for c in han if ord(c) not in cmap]})
    rare = [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF
            or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF]
    radical = next(line for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines()
                   if line.startswith("2F12;"))
    assert radical.split(";")[5] == "<compat> 529B"
    save(S / "batch-102-font-preparation.json", {
        "schemaVersion": 1, "batch": "102", "proposedTextInventory": plan["proposedHanText"],
        "inventoryScope": plan["fontInventoryScope"], "auditedHan": han,
        "auditedHanCount": len(han), "fonts": fonts, "rareHanRangeCharacters": rare,
        "unicodeRadicalRecord": radical,
        "mechanism": "Unchanged RareHan.kt and RareHanTest.kt inspected. Actual three bundled font cmaps checked against proposed text. Canonical力 is ordinary U+529B, not compatibility-radical U+2F12. The fourth default/system typeface requires later actual native rendering, not a fabricated host cmap.",
        "limits": "Proposed text only; cmap absence is not a glyph failure and cmap presence is not native rendered acceptance. Final actual-Han audit, non-skipped RareHan test and fresh native four-font/all-Han rendering remain mandatory.",
    })
    progress = load(S / "batch-102-progress.json")
    progress.update(status="source-prepared-not-drafted", sourcePreparationComplete=True,
                    authoringPlan="batch-102-authoring-plan.json",
                    preparationAudit="batch-102-preparation-audit.json",
                    fullSourceObservationsRemainHistorical=True, nextAction=plan["nextAction"])
    save(S / "batch-102-progress.json", progress)
    print(json.dumps({"articlesPreserved": len(baselines),
                      "navigationSimulations": len(simulations), "proposedHan": len(han),
                      "fontAbsences": [f["allProposedMissing"] for f in fonts]}))


def audit():
    import re

    snapshot, inputs, jm, kd = frozen()
    plan = load(S / "batch-102-authoring-plan.json")
    assert plan["sourcePreparationComplete"]
    assert load(S / "batch-102-progress.json")["sourcePreparationComplete"]
    row = load(S / "batch-102-input-metadata.json")["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["sourceRow"] == 113)
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[112] == row["kanji"] == "\u52a3"
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    assert not (R / "words" / "\u512a\u52a3.md").exists()
    assert plan["sourceReadingOrder"] == {k: row["metadata"][k] for k in ("onyomi", "kunyomi")}
    proposed = plan["proposedMetadata"]
    for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        assert proposed[field] == row["metadata"][field], field
    assert proposed["quizOnyomi"] == proposed["onyomi"] == ["\u30ec\u30c4"]
    assert proposed["quizKunyomi"] == proposed["kunyomi"] == ["\u304a\u3068.\u308b"]
    assert [(r["kind"], r["reading"]) for r in plan["readingDispositions"]] == [
        ("on", "\u30ec\u30c4"), ("kun", "\u304a\u3068.\u308b")]
    members = load(S / "batch-102-lexical-selection.json")["entryIds"]
    fresh_members = [e.findtext("ent_seq") for e in jm.findall("entry")
                     if any("\u52a3" in k.text for k in e.findall("k_ele/keb"))]
    assert members == fresh_members and len(members) == 69
    comparison = load(S / "batch-102-comparison-selection.json")
    expected_ids = [e.findtext("ent_seq") for e in jm.findall("entry")
                    if any(k.text in comparison["exactSpellings"] for k in e.findall("k_ele/keb"))
                    and e.findtext("ent_seq") not in members]
    assert comparison["entryIds"] == expected_ids and len(expected_ids) == 43
    for prefix, ids in [("batch-102-", members), ("batch-102-comparison-", expected_ids)]:
        raw = (S / (prefix + "jmdict.xml")).read_bytes()
        assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                              snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        entries = ET.fromstring(raw).findall("entry")
        lines = gzip.decompress((S / (prefix + "full-family-reading.txt.gz")).read_bytes()).decode().splitlines()
        assert len(entries) == len(lines) == len(ids)
        assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(lines, entries))
    records = ET.parse(S / "batch-102-comparison-kanjidic2.xml").getroot().findall("character")
    assert len(records) == 16
    for record in records:
        original = next(e for e in kd.findall("character")
                        if e.findtext("literal") == record.findtext("literal"))
        assert canonical(record) == canonical(original)
    all_ids = set(members + expected_ids)
    for disposition in plan["readingDispositions"]:
        assert set(disposition["entryIds"]) <= all_ids
        assert disposition["example"]["reading"] == (
            plan["newSupportMetadata"]["reading"] if disposition["example"]["newNecessarySupport"]
            else metadata(R, disposition["example"]["article"])["reading"])
    quiz = plan["quizPlan"]
    for item in [*quiz["distractors"], *quiz["directGuards"]]:
        assert metadata(R, "kanji/" + item["kanji"] + ".md")["title"] == item["label"]
        assert set(item["entryIds"]) <= all_ids
    for item in quiz["newWordGuards"]:
        assert metadata(R, "words/" + item["word"] + ".md")["title"] == item["label"]
        assert set(item["entryIds"]) <= all_ids
    assert proposed["distractors"] == [x["kanji"] for x in quiz["distractors"]]
    assert proposed["quiz_exclusions"] == [x["kanji"] for x in quiz["directGuards"]]
    assert len(set(proposed["distractors"])) == 3 and len(set(proposed["quiz_exclusions"])) == 7
    assert not set(proposed["distractors"]) & set(proposed["quiz_exclusions"])
    word = plan["newSupportMetadata"]
    assert word["quiz_exclusions"] == [x["word"] for x in quiz["newWordGuards"]]
    assert len(set(word["quiz_exclusions"])) == 4 and word["word"] not in word["quiz_exclusions"]
    assert word["kanji"] == ["\u512a", "\u52a3"] and "jlpt" not in word
    assert not any(t.startswith("jlpt-") for t in word["tags"])
    for char in proposed["distractors"]:
        existing = metadata(R, "kanji/" + char + ".md")
        assert not set(existing.get("quiz_exclusions", [])) & set(proposed["distractors"])
    for path in (R / "kanji").glob("*.md"):
        assert metadata(R, path.relative_to(R).as_posix())["title"] != proposed["title"]
    baseline = load(S / "batch-102-baseline-plan.json")
    assert len(baseline["completeExistingArticles"]) == 30
    for item in baseline["completeExistingArticles"]:
        assert sha((R / item["article"]).read_bytes()) == item["rawSha256"]
        assert metadata(R, item["article"]) == item["metadata"]
    for record in load(S / "batch-102-public-source-receipts.json"):
        raw = (S / record["archive"]).read_bytes()
        assert sha(raw) == record["archiveSha256"]
        assert sha(gzip.decompress(raw)) == record["rawSha256"]
        assert sha((S / record["extractedText"]).read_bytes()) == record["extractedTextSha256"]
    svg = (S / "batch-102-kanjivg.svg").read_bytes()
    evidence = load(S / "batch-102-stroke-evidence.json")
    assert sha(svg) == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 6
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == evidence["converterNormalizedSha256"]
    pairs = {(m["kanji"], m["article"]) for m in plan["supportMappings"]}
    assert pairs == {tuple(p) for p in plan["allMappedReciprocalPairs"]} and len(pairs) == 3
    assert plan["requiredDirections"] == plan["newDirectionsRequired"] == 6
    assert plan["activatedBaselinePairs"] == [["\u52a3", "words/\u52a3\u308b.md"]]
    for simulation in baseline["exactNavigationSimulations"]:
        text = (R / simulation["article"]).read_text(encoding="utf-8")
        assert sha(text.encode()) == simulation["oldTextSha256"]
        assert sha(text.replace(simulation["old"], simulation["new"], 1).encode()) == simulation["proposedTextSha256"]
    new_word = json.dumps(plan["newSupportTeaching"], ensure_ascii=False)
    for char in word["kanji"]:
        assert f"../kanji/{char}.md" in new_word
    for reading in plan["readingDispositions"]:
        assert f"../{reading['example']['article']}" in reading["proposedRowText"]
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD") == BASE and git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    status = subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "status", "--porcelain", "--untracked-files=all"],
        encoding="utf-8")
    for line in status.splitlines():
        assert re.match(r"^(?: M|\?\?) docs/n1-sources/batch-102-", line), line
    before = load(L / "progress-before-773.json")
    now = load(C / "progress.json")
    assert all(now[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for section in ("files", "images", "scenes", "audio", "listening", "curriculum", "listeningTasks",
                    "listeningTaskAudio", "listeningTaskImages"):
        for name, digest in manifest.get(section, {}).items():
            actual = (sha((R / name).read_bytes()) if section in
                      {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                      else manifest_sha256(R / name))
            assert actual == digest, name
            count += 1
    assert count == 8455 and manifest["contentVersion"] == "6e9b74967e21fc3c"
    fonts = load(S / "batch-102-font-preparation.json")
    assert len(fonts["fonts"]) == 3 and not fonts["rareHanRangeCharacters"]
    for font in fonts["fonts"]:
        assert sha(Path(font["path"]).read_bytes()) == font["sha256"]
        assert not font["allProposedMissing"]
    result = {
        "schemaVersion": 1, "execution": 773, "batch": "102", "sourceBase": BASE,
        "sourcePreparationComplete": True, "frozenInputHashesVerified": len(inputs),
        "decompressedDictionaryHashesVerified": 2, "completeMemberFamilies": 69,
        "completeComparisonFamilies": 43, "exactFreshExtractionsMatch": True,
        "compactFullFamilySemanticEquality": True, "completeRawCharacterRecords": 16,
        "rawCharacterSemanticEquality": True, "sourceRow": 113, "kanji": "\u52a3",
        "metadataReadingEntries": 2, "selectedOnEntries": 1, "selectedKunEntries": 1,
        "existingArticleBaselines": 30, "navigationOnlySimulations": 2,
        "allMappedPairs": 3, "requiredDirections": 6, "activatedBaselinePairs": 1,
        "curatedWrongKanjiChoices": 3, "directKanjiGuards": 7, "directWordGuards": 4,
        "newNecessarySupportArticles": 1, "newWordLevelInferred": False,
        "proposedHanCount": fonts["auditedHanCount"], "bundledFontsChecked": 3,
        "systemDefaultFontNativeAcceptance": "outstanding",
        "runtimeBytesUnchanged": True, "runtimeManifestHashesVerified": count,
        "pinnedSvgPaths": 6, "geometryConverted": False, "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True,
        "limits": "Mechanical source-plan audit, not independent linguistic review or rendered/native/phone acceptance. Original source-only and historical limits remain.",
    }
    save(S / "batch-102-preparation-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    checks = {}
    for label in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                  "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{label}-773.txt").read_bytes()
        target = S / f"batch-102-{label}-773.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    tests = (L / "source-tests-773.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-773.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    audit_result = load(S / "batch-102-preparation-audit.json")
    assert audit_result["runtimeManifestHashesVerified"] == 8455
    assert audit_result["completeMemberFamilies"] == 69 and audit_result["completeComparisonFamilies"] == 43
    assert json.loads((L / "audit-773.txt").read_text(encoding="utf-8")) == audit_result
    helpers = {}
    for name, target in [
        ("source-773.py", "batch-102-source-completion-recipe.py"),
        ("preflight-773.ps1", "batch-102-preflight-773.ps1.txt"),
        ("checks-source-773.ps1", "batch-102-checks-source-773.ps1.txt"),
    ]:
        shutil.copyfile(C / name, S / target)
        assert (C / name).read_bytes() == (S / target).read_bytes()
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-773.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    shutil.copyfile(L / "preflight-773.json", S / "batch-102-runner-role-773.json")
    save(S / "execution-773.json", {
        "schemaVersion": 1, "execution": 773, "checkpoint": 773, "batch": "102",
        "stage": "source-prepared-not-drafted", "baseCommit": BASE, "publishedBase": MAIN,
        "androidSignedHead": APP, "membership": ["\u52a3"], "sourceRows": [113],
        "preparationAudit": audit_result, "authoringPlan": "batch-102-authoring-plan.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "validationTiming": "Focused source tests/validator/manifest/vocabulary/budgets passed. Final guard-label refinement changed only contributor plan data; prepare and exact audit rerun afterward. No runtime bytes changed.",
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 128, "remainingAdditions": 1100, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [],
        "nextAction": load(S / "batch-102-authoring-plan.json")["nextAction"],
        "limits": "Normally signed LOCAL source-only checkpoint; no push, independent content review, app/native acceptance or runtime publication. Original checkpoints and all acceptance gates remain historical/intact. Initial102membership/observations are historical initial-packet states; current102progress/authoringPlan explicitly supersede only preparation status.",
    })
    print("Source-completion evidence, validation receipts, runner role and durable helpers archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    body = (
        "Batch 102 / checkpoint 773: **source preparation complete, not runtime-drafted or published**.\n\n"
        f"Normally signed LOCAL saved commit: `{head}`; public main remains `{MAIN}`.\n\n"
        "For frozen row113 劣, the source plan preserves all69 full member families and adds43 "
        "complete comparison families/16 raw character records. This execution freshly inspected "
        "the three applicable member families and all43 comparisons; the original69-family "
        "inspection and source qualifications remain historical, not claimed as a fresh full reread. "
        "Both source-order readings レツ / おと.る are selected with own-row links planned: existing "
        "N3 劣るおとる and one necessary NEW 優劣ゆうれつ article, with no inferred word level. "
        "優劣 covers both superiority and inferiority, not inferiority alone.\n\n"
        "The plan fixes exact displayed labels, three wrong kanji choices (努/功/省), seven direct "
        "kanji guards and four direct word guards. These are symmetric NONTRANSITIVE pairs, not "
        "cliques or universal semantic guarantees. Evidence-based non-guard dispositions are also "
        "retained. Thirty actual existing articles/metadata are pinned; only two navigation-only "
        "reused changes are planned. Three all-mapped pairs/six directions include 優↔優劣 and "
        "the activated baseline 劣↔劣る pair. Both complete metadata lists and easier identities "
        "remain unchanged. The six-path pinned SVG is still unconverted.\n\n"
        "43 focused source tests, structural validation, unchanged regenerated manifest, vocabulary "
        "consistency, archive budgets and the final exact preparation audit passed. All8,455 "
        "runtime manifest hashes/contentVersion `6e9b74967e21fc3c` remain unchanged. All36 proposed "
        "Han characters are in each of the three actual bundled font cmaps; this is NOT rendered "
        "acceptance of the fourth/default system font or any native/phone result. No guard was raised. "
        "Live launcher ancestry, decoded command and exact session were verified without touching "
        "the parent's lock. Helpers are in approved control and archived with the packet; no "
        "optional historical-session recipe access or new permission denial occurred.\n\n"
        "**128/1,228 additions published; 1,100 acceptance remainder unchanged.** No new content "
        "was pushed. Next is SAME102 bounded LOCAL UNREVIEWED runtime draft/freeze only. "
        "Two serial blind different-family reviews, original-session reconciliation, qualified "
        "non-skipped Android, ContentSync ONCE/native/four-font rendering and all combined-main, "
        "signing, owner fast-forward, terminal-green CI/every immutable ZIP hash/budget gates remain. "
        "Compatible stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 "
        "mechanisms remain required; physical-phone/general-release/whole-set acceptance remains "
        "outstanding. No next batch or second runner.\n"
    )
    (C / "issue-773.txt").write_text(body, encoding="utf-8", newline="\n")
    save(C / "issue-request-773.json", {"body": body})
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert changed and all(p.startswith("docs/n1-sources/batch-102-") or
                           p == "docs/n1-sources/execution-773.json" for p in changed)
    assert not git("diff", BASE, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    posted = load(L / "issue-773-verified.json")
    expected_body = (C / "issue-773.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == expected_body
    assert head in expected_body and "not runtime-drafted or published" in expected_body
    before = load(L / "progress-before-773.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    plan = load(S / "batch-102-authoring-plan.json")
    audit_result = load(S / "batch-102-preparation-audit.json")
    receipt = {
        "schemaVersion": 1, "execution": 773, "checkpoint": 773, "batch": "102",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-773.json",
        "authoringPlan": "docs/n1-sources/batch-102-authoring-plan.json",
        "membership": ["\u52a3"], "sourceRows": [113], "completeMemberFamilies": 69,
        "completeComparisonFamilies": 43, "completeRawCharacterRecords": 16,
        "sourcePreparationComplete": True, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "metadataReadingEntries": 2, "newNecessarySupportArticles": 1,
        "allMappedPairs": 3, "requiredDirections": 6, "activatedBaselinePairs": 1,
        "curatedWrongKanjiChoices": 3, "directKanjiGuards": 7, "directWordGuards": 4,
        "existingArticleBaselines": 30, "navigationOnlyChangesPlanned": 2,
        "proposedHan": audit_result["proposedHanCount"], "bundledFontsChecked": 3,
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 128, "remainingAdditions": 1100,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue", "stage": "source-prepared-not-drafted",
        "runtimeManifestHashesVerified": 8455, "contentVersion": "6e9b74967e21fc3c",
        "sourceTestsPassed": 43, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "limits": "No fresh69-family reread, independent content review, fourth/system font rendered acceptance or app/native/phone result is claimed. Original checkpoints and all original acceptance gates remain intact.",
        "nextAction": plan["nextAction"], "blocker": None,
    }
    p["execution773StartingState"]["status"] = "signed-local-source-completion-checkpoint-complete"
    p["execution773CoordinatorCheckpoint"] = receipt
    p["batch102SourceCompletionIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": sha(expected_body.encode("utf-8")), "verified": True,
    }
    p.update(checkpoint=773, status="continue", stage=receipt["stage"],
             nextAction=plan["nextAction"], blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p
    assert all(reread[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-773-final-verification.json", receipt)
    print(json.dumps(receipt, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "comparisons", "prepare", "audit",
                                       "record", "issue", "finish"])
    globals()[parser.parse_args().step]()
