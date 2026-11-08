"""Persist the bounded batch 104 local unreviewed runtime draft."""
import argparse
import gzip
import hashlib
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
L = C / "logs" / "a35853d9-7a7f-4820-9b94-71b73c4dd702"
BASE = "b4b381728793f4c1d0d9b09f8eee47eaf5b8985e"
MAIN = "2491799cffe960a7664a6135614b452e24dce459"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
STAGE = "batch-104-local-unreviewed-runtime-draft-frozen"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from audit_n1_batch import audit as batch_audit, base_file, runtime_delta
from build_manifest import build_manifest, sha256 as manifest_sha256


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".798.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(root), *args],
        encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=root)


def start():
    clean(R, BASE)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (797, "104", "continue")
    assert p["lastPublishedCommit"] == MAIN and p["remainingAdditions"] == 1098
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["execution797CoordinatorCheckpoint"] == p["execution797CoordinatorCheckpoint"]
    role = load(L / "preflight-798.json")
    assert role["liveParentPid"] == 13320 and role["sessionId"] == L.name and not role["lockTouched"]
    assert not (L / "progress-before-798.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-798.json")
    state = {
        "execution": 798, "batch": "104", "startingHead": BASE, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME104 bounded LOCAL UNREVIEWED runtime draft/freeze only: new 劾, generated eight-stroke geometry, necessary 弾劾 support, zero baseline runtime edits and regenerated manifest. No reviewer, Android/native, publication,105 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed before implementation; operative contract, approved issue and final797 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main unchanged. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
        "status": "runtime-draft-in-progress",
    }
    p["execution798StartingState"] = state
    p.update(stage="batch-104-runtime-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting draft scope saved with full historical state preserved.")


def generate():
    from generate_strokes import convert, KANJIVG_REVISION

    assert git("rev-parse", "HEAD") == BASE
    plan = load(S / "batch-104-authoring-plan.json")
    assert metadata(R, "kanji/劾.md") == plan["proposedMetadata"]
    assert metadata(R, "words/弾劾.md") == plan["newSupportMetadata"][0]
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    converter_hash = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter_hash == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    svg = (S / "batch-104-kanjivg.svg").read_bytes()
    evidence = load(S / "batch-104-stroke-evidence.json")
    assert sha(svg) == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == evidence["gitBlob"]
    assert KANJIVG_REVISION == evidence["revision"]
    stroke_path = R / "strokes" / "劾.json"
    assert not stroke_path.exists()
    data = convert("劾", svg.decode("utf-8"))
    assert data["strokeCount"] == len(data["strokes"]) == 8
    stroke_path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                           encoding="utf-8", newline="\n")
    ledger = load(S / "batch-104-progress.json")
    assert ledger["sourcePreparationComplete"] and ledger["drafted"] == []
    ledger["sourcePreparationLimits"] = ledger["limits"]
    ledger.update(
        status="local-unreviewed-runtime-draft", drafted=["劾"], runtimeChanged=True, runtimePublished=False,
        dictionaryPackets=[
            {"selection": "batch-104-lexical-selection.json", "xml": "batch-104-jmdict.xml"},
            {"selection": "batch-104-comparison-selection.json", "xml": "batch-104-comparison-jmdict.xml"}],
        readingDispositions=[
            {**row, "kanji": "劾", "selected": True, "sourceOnly": False,
             "article": row["example"]["article"],
             "reason": row["allocation"] + " " + row["usefulness"]}
            for row in plan["readingDispositions"]],
        supportMappings=[
            {"kanji": row["kanji"], "article": row["article"], "primaryReading": row["reading"],
             "entryIds": [row["entryId"]], "newArticle": True, "status": "local-unreviewed-draft"}
            for row in plan["supportMappings"]],
        requiredReciprocalPairs=plan["allMappedReciprocalPairs"], activatedBaselinePairs=[],
        changedReusedPassages=[],
        curatedProjection=[{"kanji": "劾", "quizOnyomi": ["ガイ"], "quizKunyomi": [],
                            "onKeys": ["がい"], "kunKeys": []}],
        quizAudit={"劾": {
            "title": plan["proposedMetadata"]["title"],
            "distractors": plan["proposedMetadata"]["distractors"],
            "labels": [metadata(R, f"kanji/{c}.md")["title"]
                       for c in plan["proposedMetadata"]["distractors"]],
            "meaningDecisions": plan["quizPlan"]["wrongChoices"],
            "directExclusions": plan["quizPlan"]["directKanjiGuards"],
            "guardSemantics": "Direct, symmetric and nontransitive; declaration on new 劾 only.",
            "poolLimits": plan["quizPlan"]["limits"]}},
        wordQuizAudit={
            "directExclusions": [{"word": row["word"], "exclude": row["quiz_exclusions"]}
                                 for row in plan["newSupportMetadata"]],
            "evidence": plan["wordQuizPlan"]["directGuards"],
            "limits": "Seven direct symmetric nontransitive pairs; not exhaustive live/future pool safety."},
        strokeDraft={"source": evidence, "converted": True, "converterNormalizedSha256": converter_hash,
                     "generatedSha256": sha(stroke_path.read_bytes()), "nativeDrawingAccepted": False},
        limits=[
            "LOCAL UNREVIEWED runtime draft only; no push or acceptance.",
            "Source796/797 observations remain historical; source-stage readiness is not review closure.",
            "Full/selected sole ガイ gives がい; full/selected kunyomi remain empty.",
            "Both serial blind different-family reviews, qualified Android/native/rendered acceptance and every publication gate remain.",
            "Physical-phone/general-release and whole-set acceptance outstanding."],
        nextAction="SAME104 freeze audit and signed local unreviewed snapshot, then two serial blind different-family textual reviews. No unreviewed push.")
    save(S / "batch-104-progress.json", ledger)
    print("Eight strokes generated from pinned SVG; unreviewed draft ledger saved.")


def next_action():
    previous = load(L / "progress-before-798.json")["nextAction"]
    marker = "Every original TWOserialblind "
    assert marker in previous
    return (
        "SAME104 independent textual review of the identical signed LOCAL UNREVIEWED draft: "
        "TWO actual different model families from current catalog, blind independent initial reports "
        "covering correctness/scopedcoverage/phonecomprehensibility on new劾 and necessary弾劾. "
        "ONE headless read-only reviewer at a time; serial internal tools/no nested agents; wait actual exit "
        "and persist complete original report before next. Use committed FOURmember/23comparison families, "
        "full rawcharacter/allocation/public packets, exact labels/THREEwrongchoices/FIVEdirectkanji/"
        "SEVENdirectword safeguards and zero baseline edits; no author rationale/other report in initial prompt. "
        "Sole full/selectedガイ givesがい; kunyomi empty. 弾hasnoKANJIcard: plain component/fullmetadata, "
        "existingwords/弾たま unchanged/notcompoundreuse. Impeachment and broaderdenunciation are distinct; "
        "accusation is not proven guilt/completedremoval. Exact actual-Han/four-font draft audit is in "
        "batch-104-draft-font-audit.json; 刂U+5202 absentallTHREEbundledcmaps, NOTglyphfailure. "
        "Later inspect actual刂fallback/readability in allfour selected/defaultmodes. "
        "No publication,105 or secondrunner in textual-review checkpoint. Draft totals1127kanji/5078words "
        "include ONEunreviewedaddition/ONEnecessarysupport, NOT delivery or N1vocabulary. "
        "One allmappedpair/twodirections/zeroactivatedpairs. "
        + marker + previous.split(marker, 1)[1]
    )


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())), (element.text or "").strip(),
            tuple(canonical(child) for child in element))


def audit():
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    result = batch_audit(R, "104")
    assert result["curatedOfferedKeys"] == result["readingDispositions"] == 1
    plan = load(S / "batch-104-authoring-plan.json")
    assert metadata(R, "kanji/劾.md") == plan["proposedMetadata"]
    source = next(r for r in load(S / "source-index.json") if r["kanji"] == "劾")
    assert source["sourceRow"] == 115
    assert source == load(S / "batch-104-input-metadata.json")["sourceIndexRecord"]
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
        inputs[name] = raw
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[114] == "劾"
    assert sha(gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])) == snapshot["jmdict"]["xmlSha256"]
    kd_bytes = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(kd_bytes) == snapshot["kanjidic2"]["xmlSha256"]
    for packet, selection, compact in [
        ("batch-104-jmdict.xml", "batch-104-lexical-selection.json", "batch-104-full-family-reading.txt.gz"),
        ("batch-104-comparison-jmdict.xml", "batch-104-comparison-selection.json",
         "batch-104-comparison-full-family-reading.txt.gz")
    ]:
        ids = load(S / selection)["entryIds"]
        raw = (S / packet).read_bytes()
        assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                              snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        compact_lines = gzip.decompress((S / compact).read_bytes()).decode("utf-8").splitlines()
        entries = ET.fromstring(raw).findall("entry")
        assert len(compact_lines) == len(entries) == len(ids)
        assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(compact_lines, entries))
    raw_characters = {e.findtext("literal"): e for e in ET.fromstring(kd_bytes).findall("character")}
    chars = []
    for packet in ("batch-104-kanjidic2.xml", "batch-104-comparison-kanjidic2.xml"):
        chars.extend(ET.parse(S / packet).getroot().findall("character"))
    assert len(chars) == 15
    assert all(canonical(e) == canonical(raw_characters[e.findtext("literal")]) for e in chars)
    pages = load(S / "batch-104-public-source-receipts.json") + [
        load(S / "batch-104-public-source-completion-receipt.json")]
    for page in pages:
        raw = (S / page["archive"]).read_bytes()
        assert sha(raw) == page["archiveSha256"]
        assert sha(gzip.decompress(raw)) == page["rawSha256"]
        assert sha((S / page["extractedText"]).read_bytes()) == page["extractedTextSha256"]
    snapshots = load(S / "batch-104-existing-article-snapshots.json")["articles"]
    assert len(snapshots) == 31
    for record in snapshots:
        raw = (R / record["article"]).read_bytes()
        assert sha(raw) == record["sha256"] and len(raw) == record["bytes"]
        assert raw.decode("utf-8") == record["body"]
        assert metadata(R, record["article"]) == record["metadata"]
    word = metadata(R, "words/弾劾.md")
    assert word == plan["newSupportMetadata"][0] and "jlpt" not in word
    assert not any(t.startswith("jlpt-") for t in word["tags"])
    assert not (R / "kanji" / "弾.md").exists()
    word_body = (R / "words" / "弾劾.md").read_text(encoding="utf-8")
    assert "../kanji/弾.md" not in word_body and "弾.md" not in word_body
    assert word["quiz_exclusions"] == [r["other"] for r in plan["wordQuizPlan"]["directGuards"]]
    assert len(word["quiz_exclusions"]) == 7
    meta = metadata(R, "kanji/劾.md")
    assert meta["quiz_exclusions"] == [r["other"] for r in plan["quizPlan"]["directKanjiGuards"]]
    assert len(meta["quiz_exclusions"]) == 5
    for guard in plan["quizPlan"]["directKanjiGuards"] + plan["quizPlan"]["wrongChoices"]:
        char = guard.get("other", guard.get("kanji"))
        m = metadata(R, f"kanji/{char}.md")
        assert m["title"] == guard["label"] and len(m["distractors"]) >= 3
        assert not set(meta["distractors"]) & set(m.get("quiz_exclusions", []))
    for guard in plan["wordQuizPlan"]["directGuards"]:
        assert metadata(R, f"words/{guard['other']}.md")["title"] == guard["label"]
    current = load(R / "manifest.json")
    assert build_manifest(R) == current
    old_manifest = json.loads(base_file(R, BASE, "manifest.json"))
    additions = {"kanji/劾.md", "words/弾劾.md", "strokes/劾.json"}
    runtime_delta(old_manifest, current, additions, set())
    assert not plan["reusedPassageChanges"] and not plan["activatedBaselinePairs"]
    assert plan["allMappedReciprocalPairs"] == [["劾", "words/弾劾.md"]]
    svg = (S / "batch-104-kanjivg.svg").read_bytes()
    evidence = load(S / "batch-104-stroke-evidence.json")
    assert sha(svg) == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == evidence["gitBlob"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == evidence["converterNormalizedSha256"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert [p.attrib["id"] for p in paths] == [f"kvg:052be-s{i}" for i in range(1, 9)]
    strokes = load(R / "strokes" / "劾.json")
    assert strokes == convert("劾", svg.decode("utf-8"))
    assert strokes["strokeCount"] == len(strokes["strokes"]) == 8
    assert [r["id"] for r in strokes["strokes"]] == list(range(1, 9))
    assert all(len(r["points"]) == 16 and
               all(len(p) == 2 and all(math.isfinite(v) and 0 <= v <= 109 for v in p)
                   for p in r["points"]) for r in strokes["strokes"])
    text = "\n".join((R / name).read_text(encoding="utf-8") for name in sorted(additions) if name.endswith(".md"))
    han = sorted(set(c for c in text if 0x3400 <= ord(c) <= 0x9FFF or
                     0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    rare = sorted(set(c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or
                      0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF or
                      0x20000 <= ord(c) <= 0x2FFFF))
    fonts = []
    for font_path in sorted((A / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        with TTFont(font_path) as font:
            missing = [c for c in han if ord(c) not in font.getBestCmap()]
        fonts.append({"path": str(font_path), "sha256": sha(font_path.read_bytes()), "missing": missing})
    assert len(fonts) == 3 and all(f["missing"] == ["刂"] for f in fonts) and not rare
    assert "刂" in han and "力" in han and "\u2f12" not in text
    save(S / "batch-104-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "104", "execution": 798,
        "scope": "Both complete new Markdown files, including all metadata/direct guard IDs, examples, grammar forms, component/comparison text and links. No changed baseline passages.",
        "han": han, "hanCount": len(han), "rareHan": rare, "bundledFonts": fonts,
        "proposedSourceHanCount": 37,
        "proposedButNotIntroduced": sorted(set(load(S / "batch-104-font-preparation.json")["auditedHan"]) - set(han)),
        "defaultSystemFont": "Later native four-font rendering required",
        "requiredNativeFallbackTarget": "刂 U+5202, absent from all three bundled cmaps",
        "limits": "Cmap absence is not rendered failure; native four-mode readable/distinguishable fallback, drawing and physical-phone checks are not claimed."})
    count = 0
    for section, entries in current.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            path = R / name
            actual = sha(path.read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else manifest_sha256(path)
            assert actual == digest, name
            count += 1
    assert count == 8466
    changes = set(git("diff", "--name-only", BASE).splitlines())
    assert changes == {"manifest.json", "docs/n1-sources/batch-104-progress.json"}
    for folder in ("kanji", "words", "strokes"):
        files = set(git("ls-tree", "-r", "--name-only", BASE, "--", folder).splitlines())
        actual_files = {p.relative_to(R).as_posix() for p in (R / folder).glob("*") if p.is_file()}
        assert actual_files - files == {n for n in additions if n.startswith(folder + "/")}
        assert not files - actual_files
    before = load(L / "progress-before-798.json")
    now = load(C / "progress.json")
    assert all(now[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    result.update(
        execution=798, sourceRow=115, draftSignedBase=BASE, androidSignedHead=APP,
        frozenInputHashesVerified=len(inputs), decompressedDictionaryHashesVerified=2,
        completeMemberFamilies=4, completeComparisonFamilies=23, fullRawCharacterRecords=15,
        archivedPublicPagesVerified=4, exactFreshPacketExtractionsMatch=True,
        metadataReadingEntries=1, actualOfferedKeys={"on": ["がい"], "kun": []},
        baselineComparisonMetadataAndBytesPreserved=31, changedBaselineRuntimeFiles=0,
        directKanjiGuards=5, directWordGuards=7, requiredLinkDirections=2,
        geometryRegenerationEqual=True, generatedStrokes=8, pointsPerStroke=16,
        actualDraftHan=len(han), missingFromAllBundledCmaps=["刂"], rareHanCharacters=0,
        runtimeManifestHashesVerified=count, baselineRuntimeHashesPreserved=8463,
        kanjiCount=len(list((R / "kanji").glob("*.md"))),
        wordCount=len(list((R / "words").glob("*.md"))),
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        publishedAdditions=130, remainingAdditions=1098,
        limits="Mechanical LOCAL UNREVIEWED draft audit, not independent linguistic review, exhaustive quiz-pool safety, native/rendered/font/phone acceptance or publication.")
    assert result["kanjiCount"] == 1127 and result["wordCount"] == 5078
    save(S / "batch-104-draft-audit-798.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    result = load(S / "batch-104-draft-audit-798.json")
    assert result["runtimeManifestHashesVerified"] == 8466 and result["curatedOfferedKeys"] == 1
    checks = {}
    for name in ("source-tests", "validate", "manifest", "batch-audit", "audit", "budget",
                 "vocabulary", "whitespace"):
        raw = (L / f"{name}-798.txt").read_bytes()
        path = S / f"batch-104-{name}-798.txt.gz"
        assert not path.exists(), path
        path.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(path.read_bytes()) == raw
        checks[name] = {"archive": path.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                        "archiveSha256": sha(path.read_bytes())}
    tests = (L / "source-tests-798.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-798.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    scope = ["kanji/劾.md", "words/弾劾.md", "strokes/劾.json", "manifest.json"]
    hashes = {name: {"rawSha256": sha((R / name).read_bytes()),
                     "manifestSha256": manifest_sha256(R / name)} for name in scope}
    save(S / "batch-104-draft-freeze-798.json", {
        "schemaVersion": 1, "batch": "104", "execution": 798,
        "signedParent": BASE, "publishedBase": MAIN, "androidSignedHead": APP,
        "status": "local-unreviewed-runtime-draft",
        "runtimeFiles": hashes, "contentVersion": result["contentVersion"],
        "baselineRuntimeChanges": [], "activatedBaselinePairs": [],
        "sourcePackets": ["batch-104-jmdict.xml", "batch-104-comparison-jmdict.xml",
                          "batch-104-kanjidic2.xml", "batch-104-comparison-kanjidic2.xml",
                          "batch-104-public-source-receipts.json",
                          "batch-104-public-source-completion-receipt.json"],
        "textualReviewScope": {
            "newArticles": ["kanji/劾.md", "words/弾劾.md"], "changedReusedPassages": [],
            "facets": ["correctness", "scoped coverage", "phone comprehensibility"],
            "quizScope": "Actual labels, three curated wrong choices, five direct kanji/seven direct word guards, ordinary secondary senses, excessive/missing-pair risks and legacy fallbacks. Actual qualified builder/live-pool/native checks remain later gates.",
            "readingScope": "Sole full/selected ガイ yields がい, no kunyomi; exact allocation in 弾劾 and distinct 弾 component sense.",
            "meaningScope": "Impeachment versus wider denunciation, transitive suru/object roles, noun construction, no guilt/fairness/completed-removal inference and no inferred vocabulary level.",
            "fontScope": "Actual28Han, 刂 absent from all three bundled cmaps; later native four-mode rendering required.",
            "process": "TWO actual different model families, independent blind initials on identical frozen teaching; ONE active reviewer and serial internal tools; no author rationale/other report in initial prompts."},
        "limits": "Byte freeze, not reviewer comprehension, linguistic correctness, app/native/font/phone acceptance or publication."})
    ledger = load(S / "batch-104-progress.json")
    ledger.update(draftAudit="batch-104-draft-audit-798.json",
                  draftFreeze="batch-104-draft-freeze-798.json",
                  draftFontAudit="batch-104-draft-font-audit.json", nextAction=next_action())
    save(S / "batch-104-progress.json", ledger)
    helpers = {}
    for source_name, target in [
        ("draft-798.py", "batch-104-draft-recipe-798.py"),
        ("preflight-798.ps1", "batch-104-preflight-798.ps1.txt"),
        ("checks-draft-798.ps1", "batch-104-checks-draft-798.ps1.txt"),
        ("issue-798.ps1", "batch-104-issue-798.ps1.txt")
    ]:
        assert not (S / target).exists(), target
        shutil.copyfile(C / source_name, S / target)
        helpers[target] = sha((S / target).read_bytes())
    shutil.copyfile(L / "preflight-798.json", S / "batch-104-runner-role-798.json")
    save(S / "execution-798.json", {
        "schemaVersion": 1, "execution": 798, "checkpoint": 798, "batch": "104",
        "stage": STAGE, "baseCommit": BASE, "publishedBase": MAIN, "androidSignedHead": APP,
        "membership": ["劾"], "sourceRows": [115], "draftAudit": result, "validation": checks,
        "draftFreeze": "batch-104-draft-freeze-798.json", "durableHelperHashes": helpers,
        "runnerPreflight": load(L / "preflight-798.json"),
        "runtimeDrafted": ["劾"], "newNecessarySupportWords": 1,
        "reviewClosed": [], "published": [], "runtimeChanged": True, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 130, "remainingAdditions": 1098, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [],
        "authorInspection": {
            "memberFamilies": "All FOUR complete entries freshly returned in full expanded71-line XML packet.",
            "comparisonFamilies": "All23 complete compact families freshly returned without truncation in ranges1-12 and13-23; aliases, restrictions and secondary senses retained.",
            "rawCharacters": "Full original69-line劾 and all14 full compact comparison records freshly returned in ranges1-7/8-14; no source fields inferred from the plan.",
            "publicDictionaries": "Fresh read of committed actual劾 character block, both弾劾 word senses/example and first nine lines of actual弾 character heading/senses1-5. No fresh upstream retrieval claimed; gaiji/encyclopedia-navigation/extraction limits inherited.",
            "freshExistingArticles": ["kanji/刻.md", "kanji/効.md", "kanji/努.md", "kanji/責.md",
                                      "words/批判.md", "words/責める.md", "words/不正.md",
                                      "kanji/励.md", "words/激励.md"],
            "otherComparisons": "Source797 full31-article inspection inherited, not equally freshly reread; all31 raw byte/body/metadata snapshots independently reverified mechanically.",
            "sourceReadingAllocation": "Frozen raw劾/弾 and actual Digital Daijisen character headings and explicit弾劾 examples, not kana substring inference.",
            "diagnostics": "Initial request decoding succeeded but cp1252 console printing failed; entire file decoded again with UTF-8 before acting. An optional guessed current-workspace words/奨励.md example was absent; used existing words/激励.md. An oversized extracted弾 page returned a size-limit message; inspected exact relevant first35 lines. No permission denial, historical-session access or substituted mandatory evidence."},
        "nextAction": next_action(),
        "limits": "Normally signed LOCAL UNREVIEWED checkpoint only. No push/reviewer/Android/native/rendered acceptance or next batch. Forty-three focused source tests are not the later full acceptance suite. Existing vocabulary pilot coverage remains incomplete; all original gates and historical limitations remain."})
    print("Draft freeze, validation receipts and durable recipes archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    clean(R, head)
    result = load(S / "batch-104-draft-audit-798.json")
    body = (
        "Batch 104 / checkpoint 798: **LOCAL UNREVIEWED runtime draft frozen; not published**.\n\n"
        f"Normally signed saved commit `{head}`; public main remains `{MAIN}`.\n\n"
        "Drafted frozen row115 **劾**, eight strokes generated by the unchanged pinned KanjiVG converter, "
        "and one necessary support article **弾劾 (だんがい)**. **Zero baseline runtime edits**; all "
        "existing identities/readings/levels/bodies/exclusions preserved. Supporting-word level omitted "
        "rather than inferred from the N1 kanji. One all-mapped pair/two directions; no activated baseline "
        "pairs. Full/selected on-reading **ガイ** gives **がい**; full/selected kunyomi remain empty.\n\n"
        "The draft distinguishes legal impeachment from wider denunciation of wrongdoing, teaches "
        "transitive する and the noun construction, and does not infer guilt, fair accusation or completed "
        "removal. 弾 has no kanji card: both written characters remain in word metadata, its component "
        "stays plain, and existing words/弾 (たま, bullet) remains unchanged. Five direct kanji and seven "
        "direct word safeguards are symmetric/nontransitive and still unreviewed; they are not universal "
        "quiz-pool certification.\n\n"
        f"**{result['actualDraftHan']} actual draft Han** audited against all three bundled font cmaps "
        "(37 proposed source-stage Han was a broader candidate inventory). **刂 U+5202** remains "
        "absent from all three; this is NOT a glyph-failure or rendered-acceptance claim. The useful 刻 "
        "shape contrast remains; actual 刂 fallback/readability in all four selected/default modes is "
        "still mandatory. No rare-Han-range characters introduced. All eight16-point strokes regenerate "
        "identically from the pinned SVG.\n\n"
        "43 focused source tests, validator, regenerated manifest, existing batch audit, exact frozen-source/"
        "baseline/reading/link/guard/font audits, vocabulary consistency and unchanged packaging budgets "
        "passed. Vocabulary coverage remains the existing incomplete pilot (2122/2431 reviewed prompts). "
        f"Every **{result['runtimeManifestHashesVerified']} runtime hash** verified; contentVersion "
        f"`{result['contentVersion']}`. Local draft totals1127kanji/5078words include this unaccepted "
        "kanji/support article and are NOT delivered N1 vocabulary.\n\n"
        "**130/1228 additions published; 1098 acceptance remainder unchanged.** No reviewers, app/native/"
        "rendered checks, push or next batch in this execution. Next is SAME104 two serial blind "
        "different-family textual reviews on the identical frozen teaching, then every original "
        "original-session confirmation/qualified Android/native/rendered/current-main/signing/"
        "owner-fast-forward/terminal-CI/exact-immutable-ZIP acceptance gate. Qualified signed Android "
        "`bf30cdead8515739bc0e671d57a54b9a3109dd46` remains the approved curated-reading/pair-guard+"
        "schema-only backport, NOT unrelated latest main. Compatible stop-cran/kanji-cards-android#125 "
        "and stop-cran/kanji-cards-android#132 mechanisms required; old clients ignore them. Parent "
        "launcher ancestry/session verified without touching its lock; approved control/committed-source/"
        "frozen-input artifacts only; no new denial. All original historical process/image/read-depth/"
        "permission/OOM/source-only limits remain, not retroaccepted. Physical-phone/general-release/"
        "whole-set acceptance remains outstanding; project incomplete.\n"
    )
    assert not (C / "issue-798.txt").exists()
    (C / "issue-798.txt").write_text(body, encoding="utf-8", newline="\n")
    save(C / "issue-request-798.json", {"body": body})
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    clean(R, head)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    frozen = load(S / "batch-104-draft-freeze-798.json")
    for name, hashes in frozen["runtimeFiles"].items():
        assert sha((R / name).read_bytes()) == hashes["rawSha256"]
        assert manifest_sha256(R / name) == hashes["manifestSha256"]
    assert build_manifest(R) == load(R / "manifest.json")
    changes = set(git("diff", "--name-only", BASE, head).splitlines())
    runtime = set(frozen["runtimeFiles"])
    assert runtime <= changes
    assert all(n in runtime or n.startswith("docs/n1-sources/batch-104-") or
               n == "docs/n1-sources/execution-798.json" for n in changes)
    for name, digest in load(S / "execution-798.json")["durableHelperHashes"].items():
        assert sha((S / name).read_bytes()) == digest, name
    before = load(L / "progress-before-798.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    posted = load(L / "issue-798-verified.json")
    body = (C / "issue-798.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body and head in body
    result = load(S / "batch-104-draft-audit-798.json")
    receipt = {
        "schemaVersion": 1, "execution": 798, "checkpoint": 798, "batch": "104",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-798.json", "membership": ["劾"], "sourceRows": [115],
        "completeMemberFamilies": 4, "completeComparisonFamilies": 23,
        "metadataReadingEntries": 1, "newNecessarySupportWords": 1,
        "sourcePreparationComplete": True, "runtimeDrafted": ["劾"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 130, "remainingAdditions": 1098,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue", "stage": STAGE,
        "runtimeManifestHashesVerified": result["runtimeManifestHashesVerified"],
        "contentVersion": result["contentVersion"], "sourceTestsPassed": 43,
        "draftAudit": result, "draftFreeze": "docs/n1-sources/batch-104-draft-freeze-798.json",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": next_action(), "blocker": None}
    p["execution798StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution798CoordinatorCheckpoint"] = receipt
    p["batch104DraftIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": sha(body.encode("utf-8")), "verified": True}
    p.update(checkpoint=798, status="continue", stage=STAGE, nextAction=next_action(), blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p and all(reread[k] == v for k, v in before.items() if k not in mutable)
    save(L / "checkpoint-798-final-verification.json", receipt)
    print(json.dumps({"checkpoint": 798, "status": "continue", "savedCommit": head,
                      "signature": "G", "drafted": ["劾"], "reviewed": [], "published": [],
                      "historicalRootKeysPreserved": len(before), "issueUpdate": posted["html_url"],
                      "runtimePublished": False}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["start", "generate", "audit", "record", "issue", "finish"])
    args = parser.parse_args()
    globals()[args.operation]()
