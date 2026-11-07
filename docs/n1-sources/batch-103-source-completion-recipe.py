"""Complete the comparison and authoring plan for batch 103, without runtime edits."""
import argparse
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
L = C / "logs" / "78d3bc2f-7fc7-49d9-8fcb-f9905e90af49"
HEAD = "cbb067776d8f095823e15435cb302e40e43efb9c"
MAIN = "a38f4cf554300ce34ee65aada79e87b7c9d0319e"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract
from build_manifest import build_manifest, sha256 as manifest_sha256

STAGE = "batch-103-source-prepared-not-drafted"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".786.tmp")
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
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (785, "103", "continue")
    role = load(L / "preflight-786.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution785CoordinatorCheckpoint"] == p["execution785CoordinatorCheckpoint"]
    assert not (L / "progress-before-786.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-786.json")
    state = {
        "execution": 786, "batch": "103", "startingHead": HEAD, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME103 bounded source-completion checkpoint only: comparison families, exact labels/direct safeguards, complete authoring/link/font/stroke plan. No runtime draft, reviewer, Android/native, publication,104 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request read/decoded and checkpoint parsed; operative contract, approved issue and final785 directly inspected. Historical middle parsed, not freshly linguistically reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main verified. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution786StartingState"] = state
    p.update(stage="batch-103-source-completion-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting source-completion scope saved, preserving complete live history.")


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


def comparisons():
    _, inputs, jm, kd = frozen()
    words = [
        "応援", "慰める", "努める", "努力", "一生懸命", "苦心", "凝らす",
        "せっせと", "勧める", "ねっしん", "注ぐ", "熱中", "夢中", "集中",
        "凝る", "張り切る", "くるくる", "ばりばり", "もりもり",
        "学問", "力強い", "支える", "助ける", "勉強", "勤勉", "激しい",
    ]
    aliases = {"ねっしん": "熱心", "せっせと": "せっせ", "努める": "勉める"}
    wanted = set(words) | set(aliases.values())
    entries = [e for e in jm.findall("entry") if wanted.intersection(
        [n.text for n in e.findall("k_ele/keb") + e.findall("r_ele/reb")])]
    ids = [e.findtext("ent_seq") for e in entries]
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / "batch-103-comparison-jmdict.xml").write_bytes(raw)
    compact = []
    for entry in ET.fromstring(raw):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    text = ("\n".join(compact) + "\n").encode("utf-8")
    (C / "batch-103-comparison-reading.txt").write_bytes(text)
    (S / "batch-103-comparison-reading.txt.gz").write_bytes(gzip.compress(text, mtime=0))
    chars = "励激努勉勤劣万厚助支丞"
    selected = ET.Element("kanjidic2")
    selected.append(kd.find("header"))
    for e in kd.findall("character"):
        if e.findtext("literal") in chars:
            selected.append(e)
    assert len(selected.findall("character")) == len(chars)
    ET.indent(selected, space="  ")
    (S / "batch-103-comparison-kanjidic2.xml").write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    articles = []
    for name in words:
        path = R / "words" / (name + ".md")
        if path.exists():
            articles.append({"article": path.relative_to(R).as_posix(),
                             "metadata": metadata(R, path.relative_to(R).as_posix()),
                             "sha256": sha(path.read_bytes())})
    for name in "努勉勤劣万厚支助丞":
        path = R / "kanji" / (name + ".md")
        articles.append({"article": path.relative_to(R).as_posix(),
                         "metadata": metadata(R, path.relative_to(R).as_posix()),
                         "sha256": sha(path.read_bytes())})
    save(S / "batch-103-comparison-selection.json", {
        "schemaVersion": 1, "batch": "103", "sourceBase": HEAD, "words": words,
        "additionalExactAliases": aliases, "entryIds": ids, "completeFamilies": len(ids),
        "selectionRule": "All complete frozen families with an exact keb or reb in words/alias list, including other readings/senses of the exact written form.",
        "characters": list(chars), "articleSnapshots": articles,
        "limits": "Candidate evidence only until actual full-family inspection and explicit pair dispositions; no automatic synonym or frequency inference.",
    })
    print(json.dumps({"completeComparisonFamilies": len(ids), "compactBytes": len(text),
                      "compactLines": len(compact), "existingArticles": len(articles)}, ensure_ascii=True))


def prepared():
    from fontTools.ttLib import TTFont

    plan = load(S / "batch-103-authoring-plan.json")
    snapshot, inputs, _, _ = frozen()
    text = plan["proposedHanText"]
    han = sorted(set(c for c in text if 0x3400 <= ord(c) <= 0x9FFF or
                     0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    fonts = []
    for path in sorted((A / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            missing = [c for c in han if ord(c) not in cmap]
        fonts.append({"path": str(path), "sha256": sha(path.read_bytes()),
                      "keyGlyphPresence": {c: c not in missing for c in han},
                      "allProposedMissing": missing})
    assert len(fonts) == 3
    radical = next(line for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines()
                   if line.startswith("2F12;"))
    assert radical.split(";")[5] == "<compat> 529B"
    rare = [c for c in text if (0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x4DBF or
                               0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF)]
    assert not rare
    save(S / "batch-103-font-preparation.json", {
        "schemaVersion": 1, "batch": "103", "proposedTextInventory": text,
        "inventoryScope": plan["fontInventoryScope"], "auditedHan": han,
        "auditedHanCount": len(han), "fonts": fonts, "rareHanRangeCharacters": rare,
        "unicodeRadicalRecord": radical,
        "mechanism": "Unchanged RareHan.kt and RareHanTest.kt inspected. Three actual bundled cmaps checked; ordinary力U+529B versus compatibility radicalU+2F12 distinguished. Fourth/default system typeface requires later actual native rendering, not a fabricated host cmap.",
        "missingGlyphDisposition": plan["fontPreparationDisposition"],
        "limits": "Proposed text only; cmap presence/absence is not native rendered acceptance. Final actual-Han audit, non-skipped RareHan test and fresh native four-font/all-Han rendering remain mandatory.",
    })
    selection = load(S / "batch-103-comparison-selection.json")
    save(S / "batch-103-baseline-plan.json", {
        "schemaVersion": 1, "batch": "103", "baseCommit": HEAD, "publishedBase": MAIN,
        "androidHead": APP, "manifestSha256": sha((R / "manifest.json").read_bytes()),
        "contentVersion": load(R / "manifest.json")["contentVersion"],
        "allExistingRuntimeBytesMustRemain": "No baseline runtime change except the exact three navigation-only replacements in the authoring plan. Preserve all baseline metadata, stable identities, levels, full readings/order and exclusions.",
        "comparisonArticleSnapshots": selection["articleSnapshots"],
        "reusedPassageChanges": plan["reusedPassageChanges"],
        "allMappedReciprocalPairs": plan["allMappedReciprocalPairs"],
        "requiredDirections": 6, "activatedBaselinePairs": [],
        "newRuntimeFiles": ["kanji/励.md", "strokes/励.json", *plan["newSupportArticles"]],
        "missingComponent": plan["missingComponentDisposition"],
        "limits": "Source-stage preservation plan. Actual runtime diff/metadata/link/font/manifest checks are required again at drafting and acceptance, not certified in advance.",
    })
    progress = load(S / "batch-103-progress.json")
    progress.update(status="source-prepared-not-drafted", sourcePreparationComplete=True,
                    authoringPlan="batch-103-authoring-plan.json",
                    comparisonFamilies=selection["completeFamilies"],
                    nextAction=plan["nextAction"])
    save(S / "batch-103-progress.json", progress)
    print(json.dumps({"sourcePreparationComplete": True, "proposedHan": len(han),
                      "missingByFont": [f["allProposedMissing"] for f in fonts],
                      "geometryConverted": False, "runtimeChanged": False}, ensure_ascii=True))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(c) for c in element))


def audit():
    snapshot, inputs, jm, kd = frozen()
    plan = load(S / "batch-103-authoring-plan.json")
    selection = load(S / "batch-103-comparison-selection.json")
    member_ids = load(S / "batch-103-lexical-selection.json")["entryIds"]
    expected_members = [e.findtext("ent_seq") for e in jm.findall("entry")
                        if any("励" in k.text for k in e.findall("k_ele/keb"))]
    assert member_ids == expected_members and len(member_ids) == 47
    wanted = set(selection["words"]) | set(selection["additionalExactAliases"].values())
    expected_comparisons = [e.findtext("ent_seq") for e in jm.findall("entry")
                            if wanted.intersection([n.text for n in
                                e.findall("k_ele/keb") + e.findall("r_ele/reb")])]
    assert expected_comparisons == selection["entryIds"]
    assert len(expected_comparisons) == selection["completeFamilies"] == 31
    for name, ids in [("batch-103-jmdict.xml", member_ids),
                      ("batch-103-comparison-jmdict.xml", expected_comparisons)]:
        raw = (S / name).read_bytes()
        assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                              snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        compact = gzip.decompress((S / name.replace("jmdict.xml", "reading.txt.gz")).read_bytes()) if name.startswith("batch-103-comparison-") else gzip.decompress((S / "batch-103-full-family-reading.txt.gz").read_bytes())
        lines = compact.decode("utf-8").splitlines()
        entries = ET.fromstring(raw).findall("entry")
        assert len(lines) == len(entries) and all(canonical(ET.fromstring(a)) == canonical(b)
                                                  for a, b in zip(lines, entries))
    raw_chars = {e.findtext("literal"): e for e in kd.findall("character")}
    packet_chars = ET.parse(S / "batch-103-comparison-kanjidic2.xml").getroot().findall("character")
    assert len(packet_chars) == 11
    assert all(canonical(e) == canonical(raw_chars[e.findtext("literal")]) for e in packet_chars)
    row = load(S / "batch-103-source-navigation.json")["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["kanji"] == "励")
    assert row["sourceRow"] == 114 and json.loads(inputs["n1-kanji-source-20261102.json"])[113] == "励"
    proposed = plan["proposedMetadata"]
    for key in ["kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"]:
        assert proposed[key] == row["metadata"][key], key
    assert proposed["quizOnyomi"] == proposed["onyomi"]
    assert proposed["quizKunyomi"] == proposed["kunyomi"]
    assert [(r["kind"], r["reading"]) for r in plan["readingDispositions"]] == [
        ("on", "レイ"), ("kun", "はげ.む"), ("kun", "はげ.ます")]
    assert plan["readingKeys"] == {"on": ["れい"], "kun": ["はげむ", "はげます"]}
    assert len(proposed["distractors"]) == len(set(proposed["distractors"])) == 3
    assert not set(proposed["distractors"]) & set(proposed["quiz_exclusions"])
    assert proposed["title"] not in [metadata(R, p.relative_to(R).as_posix())["title"]
                                    for p in (R / "kanji").glob("*.md")]
    for char in proposed["distractors"] + proposed["quiz_exclusions"]:
        assert (R / "kanji" / (char + ".md")).is_file()
    for char in proposed["distractors"]:
        m = metadata(R, f"kanji/{char}.md")
        assert not set(proposed["distractors"]) & set(m.get("quiz_exclusions", []))
    for record in selection["articleSnapshots"]:
        path = R / record["article"]
        assert sha(path.read_bytes()) == record["sha256"]
        assert metadata(R, record["article"]) == record["metadata"]
    assert len(selection["articleSnapshots"]) == 34
    for change in plan["reusedPassageChanges"]:
        assert (R / change["article"]).read_text(encoding="utf-8").count(change["old"]) == 1
        assert change["new"].replace("[励ます](励ます.md)", "励ます").replace("[励む](励む.md)", "励む") == change["old"]
    assert len(plan["reusedPassageChanges"]) == 3
    assert not (R / "kanji" / "激.md").exists()
    words = plan["newSupportMetadata"]
    assert [w["word"] for w in words] == ["激励", "励む", "励ます"]
    assert words[0]["kanji"] == ["激", "励"]
    pairs = set()
    evidence_pairs = set()
    for record in plan["quizPlan"]["wordGuardEvidence"]:
        for word in record["newWords"]:
            for other in record["neighbors"]:
                evidence_pairs.add(tuple(sorted([word, other])))
        assert set(record["entryIds"]) <= set(member_ids + expected_comparisons)
    for word in words:
        assert "jlpt" not in word
        assert not (R / "words" / (word["word"] + ".md")).exists()
        assert len(word["quiz_exclusions"]) == len(set(word["quiz_exclusions"]))
        for other in word["quiz_exclusions"]:
            assert other != word["word"]
            assert other in [w["word"] for w in words] or (R / "words" / (other + ".md")).is_file()
            pair = tuple(sorted([word["word"], other]))
            assert pair not in pairs
            pairs.add(pair)
    assert pairs == evidence_pairs and len(pairs) == 27
    mappings = plan["allMappedReciprocalPairs"]
    assert mappings == [["励", f"words/{w['word']}.md"] for w in words]
    assert plan["requiredDirections"] == len(mappings) * 2 == 6
    assert not plan["activatedBaselinePairs"]
    assert load(S / "batch-103-source-navigation.json")["candidates"] == []
    assert not [p.name for p in (R / "words").glob("*.md") if
                metadata(R, p.relative_to(R).as_posix())["reading"] in {"げきれい", "はげむ", "はげます"}]
    for page in load(S / "batch-103-public-source-receipts.json"):
        raw = (S / page["archive"]).read_bytes()
        assert sha(raw) == page["archiveSha256"]
        assert sha(gzip.decompress(raw)) == page["rawSha256"]
        assert sha((S / page["extractedText"]).read_bytes()) == page["extractedTextSha256"]
    svg = (S / "batch-103-kanjivg.svg").read_bytes()
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 7
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    fonts = load(S / "batch-103-font-preparation.json")
    assert len(fonts["fonts"]) == 3 and not fonts["rareHanRangeCharacters"]
    assert fonts["proposedTextInventory"] == plan["proposedHanText"]
    assert all(sha(Path(f["path"]).read_bytes()) == f["sha256"] for f in fonts["fonts"])
    assert all(f["allProposedMissing"] == ["厂"] for f in fonts["fonts"])
    assert not (R / "kanji" / "励.md").exists() and not (R / "strokes" / "励.json").exists()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("diff", HEAD, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for section in ("files", "images", "scenes", "audio", "listening", "curriculum", "listeningTasks",
                    "listeningTaskAudio", "listeningTaskImages"):
        for name, digest in manifest.get(section, {}).items():
            path = R / name
            actual = sha(path.read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else manifest_sha256(path)
            assert actual == digest, name
            count += 1
    assert count == 8458
    before = load(L / "progress-before-786.json")
    now = load(C / "progress.json")
    mutable = {"stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    result = {
        "schemaVersion": 1, "execution": 786, "batch": "103", "sourceBase": HEAD,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": 47, "completeComparisonFamilies": 31,
        "exactFreshExtractionsMatch": True, "compactFullFamilySemanticEquality": True,
        "completeRawCharacterRecords": 11, "rawCharacterSemanticEquality": True,
        "sourceRow": 114, "kanji": "励", "metadataReadingEntries": 3,
        "selectedReadingEntries": 3, "newNecessarySupportWords": 3,
        "existingArticleSnapshotsVerified": 34, "navigationOnlyReusedChanges": 3,
        "directKanjiGuards": 4, "directWordGuards": len(pairs), "curatedWrongChoices": 3,
        "allMappedPairs": 3, "requiredDirections": 6, "activatedBaselinePairs": 0,
        "proposedHan": fonts["auditedHanCount"], "bundledFonts": 3,
        "missingFromAllBundledCmaps": ["厂"], "missingCmapIsRenderingFailure": False,
        "defaultSystemFont": "Later native rendering required", "rareHanCharacters": 0,
        "geometryConverted": False, "pinnedSvgPaths": 7,
        "runtimeBytesUnchanged": True, "runtimeManifestHashesVerified": count,
        "contentVersion": manifest["contentVersion"], "originalHistoricalRootValuesPreserved": True,
        "sourcePreparationComplete": True,
        "limits": "Source-stage author inspection/mechanical audit, not independent linguistic review or fresh Android/native/font/phone acceptance. Direct safeguards do not certify every unsampled quiz pool.",
    }
    save(S / "batch-103-source-completion-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    result = load(S / "batch-103-source-completion-audit.json")
    assert result["sourcePreparationComplete"] and result["runtimeManifestHashesVerified"] == 8458
    checks = {}
    for name in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                 "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{name}-786.txt").read_bytes()
        path = S / f"batch-103-{name}-786.txt.gz"
        path.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(path.read_bytes()) == raw
        checks[name] = {"archive": path.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                        "archiveSha256": sha(path.read_bytes())}
    tests = (L / "source-tests-786.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-786.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    helpers = {}
    for source, target in [("source-786.py", "batch-103-source-completion-recipe.py"),
                           ("preflight-786.ps1", "batch-103-preflight-786.ps1.txt"),
                           ("checks-source-786.ps1", "batch-103-checks-source-786.ps1.txt")]:
        shutil.copyfile(C / source, S / target)
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-786.json")
    shutil.copyfile(L / "preflight-786.json", S / "batch-103-runner-role-786.json")
    save(S / "execution-786.json", {
        "schemaVersion": 1, "execution": 786, "checkpoint": 786, "batch": "103",
        "stage": STAGE, "baseCommit": HEAD, "androidSignedHead": APP,
        "membership": ["励"], "sourceRows": [114], "sourceCompletionAudit": result,
        "authoringPlan": "batch-103-authoring-plan.json", "validation": checks,
        "durableHelperHashes": helpers, "runnerPreflight": role,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 129, "remainingAdditions": 1099, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [],
        "nextAction": load(S / "batch-103-authoring-plan.json")["nextAction"],
        "limits": "Normally signed LOCAL source-only checkpoint; no push, runtime draft, independent review, app/native or publication acceptance. All historical limitations and original gates remain unchanged. Vocabulary check retains its incomplete pilot coverage.",
    })
    print("Source-completion audit, validation receipts and durable helpers archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    result = load(S / "batch-103-source-completion-audit.json")
    body = (
        "Batch 103 / checkpoint 786: **LOCAL source-completion checkpoint**, not published teaching.\n\n"
        f"Normally signed saved commit `{head}`; public main remains `{MAIN}`.\n\n"
        "Completed the authoring plan for frozen row 114 **励**: 47 complete member families "
        "and 31 complete comparison families author-inspected, 11 full raw character records "
        "retained, 34 actual existing articles/labels checked, and all three source-order readings "
        "レイ / はげ.む / はげ.ます selected with necessary 激励・励む・励ます support. "
        "The plan explicitly distinguishes activity に励む from person を励ます and plain "
        "励ます from polite 励みます; no vocabulary levels or historical formation are inferred.\n\n"
        "Three wrong kanji choices (劣・万・厚), four direct kanji safeguards and 27 direct word "
        "safeguards have evidence-based authoring dispositions, including non-initial hard-work "
        "senses of くるくる・ばりばり・もりもり・勉強. These remain subject to independent "
        "review and actual qualified-builder/native sampling, not universal semantic certification. "
        "Guards are symmetric and nontransitive, not synonym cliques. Three all-mapped pairs/six "
        "directions, zero activated baseline pairs; exactly three navigation-only reused changes "
        "(応援・慰める・学問) planned. 激 remains in word metadata without an absent-card link.\n\n"
        f"Proposed {result['proposedHan']} Han characters checked against all three bundled font cmaps: "
        "**厂 U+5382 is absent from all three**, while 励 and the other proposed Han are present. "
        "There are no rare-Han-range characters. Cmap absence is not a glyph failure: retain the "
        "useful modern-shape comparison and explicitly inspect actual 厂 fallback/readability in all "
        "four selected/default typography modes before acceptance. The fourth/default system typeface, "
        "actual final-draft Han, non-skipped Android and fresh native/rendered checks remain required. "
        "No rendered acceptance or fallback-face identity is claimed. Pinned seven-path SVG/converter identity verified, "
        "geometry not yet generated.\n\n"
        "43 focused source tests, structural validation, unchanged regenerated manifest, vocabulary "
        "consistency (existing incomplete pilot coverage), budgets and packet/link/metadata audit passed. "
        "All 8,458 runtime hashes and contentVersion `f376333b242ebb23` unchanged. Complete live history "
        "preserved. Parent launcher ancestry/decoded command/exact session verified; its lock was not "
        "touched. Only approved workspace/control inputs used; no historical-session helper access or "
        "new permission denial.\n\n"
        "**129/1,228 additions published; 1,099 acceptance remainder unchanged.** No runtime draft, "
        "reviewer, Android/native run, push or next batch in this execution. Next is SAME103 bounded "
        "LOCAL UNREVIEWED draft/freeze, followed by every original two-family serial review, native, "
        "combined-main and publication gate. Compatible stop-cran/kanji-cards-android#125 and "
        "stop-cran/kanji-cards-android#132 mechanisms remain required. Physical-phone, general-release "
        "and whole-set acceptance remain outstanding; historical process/image/read-depth limits "
        "are not retroaccepted.\n"
    )
    (C / "issue-786.txt").write_text(body, encoding="utf-8", newline="\n")
    save(C / "issue-request-786.json", {"body": body})
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    changes = git("diff", "--name-only", HEAD, head).splitlines()
    assert changes and all(n.startswith("docs/n1-sources/batch-103-") or
                           n == "docs/n1-sources/execution-786.json" for n in changes)
    assert not git("diff", HEAD, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    before = load(L / "progress-before-786.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    posted = load(L / "issue-786-verified.json")
    body = (C / "issue-786.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body and head in body
    audit_result = load(S / "batch-103-source-completion-audit.json")
    next_action = load(S / "batch-103-authoring-plan.json")["nextAction"] + " " + before["nextAction"].split("All original TWOserialblinddifferentfamilies/", 1)[1]
    receipt = {
        "schemaVersion": 1, "execution": 786, "checkpoint": 786, "batch": "103",
        "savedCommit": head, "signature": "G", "sourceBase": HEAD, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-786.json", "membership": ["励"], "sourceRows": [114],
        "completeMemberFamilies": 47, "completeComparisonFamilies": 31,
        "metadataReadingEntries": 3, "newNecessarySupportWords": 3,
        "sourcePreparationComplete": True, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 129, "remainingAdditions": 1099,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue", "stage": STAGE,
        "runtimeManifestHashesVerified": 8458, "contentVersion": "f376333b242ebb23",
        "sourceTestsPassed": 43, "sourceCompletionAudit": audit_result,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": next_action, "blocker": None,
    }
    p["execution786StartingState"]["status"] = "signed-local-source-completion-checkpoint-complete"
    p["execution786CoordinatorCheckpoint"] = receipt
    p["batch103SourceCompletionIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": sha(body.encode("utf-8")), "verified": True,
    }
    p.update(checkpoint=786, status="continue", stage=STAGE, nextAction=next_action, blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p and all(reread[k] == v for k, v in before.items() if k not in mutable)
    save(L / "checkpoint-786-final-verification.json", receipt)
    print(json.dumps({"checkpoint": 786, "status": "continue", "savedCommit": head,
                      "signature": "G", "sourcePreparationComplete": True,
                      "historicalRootKeysPreserved": len(before),
                      "issueUpdate": posted["html_url"], "runtimeChanged": False}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["start", "comparisons", "prepared", "audit", "record", "issue", "finish"])
    args = parser.parse_args()
    globals()[args.mode]()
