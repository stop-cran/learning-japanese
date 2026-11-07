"""Freeze one local, unreviewed batch 103 runtime draft; never publish it."""
import argparse
import gzip
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "f8aa9dd7-e51a-4f7b-a40f-1f2f0f7154a3"
HEAD = "cd8ce525546909151199eebb924a9bdf0b225198"
MAIN = "a38f4cf554300ce34ee65aada79e87b7c9d0319e"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
STAGE = "batch-103-local-unreviewed-runtime-draft-frozen"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as manifest_sha256
from audit_n1_batch import audit as batch_audit, base_file, runtime_delta, reused_changes


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".787.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "-C", str(root), *args],
        encoding="utf-8").strip()


def start():
    for root, head in [(R, HEAD), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", root=root)
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (786, "103", "continue")
    role = load(L / "preflight-787.json")
    assert role["liveParentPid"] == 5920 and role["sessionId"] == L.name and not role["lockTouched"]
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution786CoordinatorCheckpoint"] == p["execution786CoordinatorCheckpoint"]
    assert not (L / "progress-before-787.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-787.json")
    state = {
        "execution": 787, "batch": "103", "startingHead": HEAD, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME103 bounded LOCAL UNREVIEWED runtime draft/freeze only: one kanji, generated strokes, three necessary support articles, exactly three navigation-only reused changes and regenerated manifest. No reviewer, Android/native, publication,104 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request read/decoded and checkpoint parsed before acting; operative contract, approved issue and final786 directly inspected. Historical middle parsed, not freshly semantically or linguistically reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main verified. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution787StartingState"] = state
    p.update(stage="batch-103-runtime-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting local draft scope saved with full historical state preserved.")


def generate():
    from generate_strokes import convert, KANJIVG_REVISION

    assert git("rev-parse", "HEAD") == HEAD
    plan = load(S / "batch-103-authoring-plan.json")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    converter_hash = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter_hash == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    svg = (S / "batch-103-kanjivg.svg").read_bytes()
    evidence = load(S / "batch-103-stroke-evidence.json")
    assert sha(svg) == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == evidence["gitBlob"]
    assert KANJIVG_REVISION == evidence["revision"]
    stroke_path = R / "strokes" / "励.json"
    assert not stroke_path.exists()
    data = convert("励", svg.decode("utf-8"))
    assert data["strokeCount"] == len(data["strokes"]) == 7
    stroke_path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                           encoding="utf-8", newline="\n")
    ledger = load(S / "batch-103-progress.json")
    assert ledger["sourcePreparationComplete"] and ledger["drafted"] == []
    ledger["sourcePreparationLimits"] = ledger["limits"]
    ledger.update(
        status="local-unreviewed-runtime-draft",
        drafted=["励"], runtimeChanged=True, runtimePublished=False,
        dictionaryPackets=[
            {"selection": "batch-103-lexical-selection.json", "xml": "batch-103-jmdict.xml"},
            {"selection": "batch-103-comparison-selection.json", "xml": "batch-103-comparison-jmdict.xml"}],
        readingDispositions=[
            {**row, "kanji": "励", "selected": True, "sourceOnly": False,
             "article": row["example"]["article"],
             "reason": row["allocation"] + " " + row["usefulness"]}
            for row in plan["readingDispositions"]],
        supportMappings=[
            {"kanji": row["kanji"], "article": row["article"], "primaryReading": row["reading"],
             "entryIds": [row["entryId"]], "newArticle": True, "status": "local-unreviewed-draft"}
            for row in plan["supportMappings"]],
        requiredReciprocalPairs=plan["allMappedReciprocalPairs"],
        activatedBaselinePairs=[],
        changedReusedPassages=[
            {"article": row["article"], "before": row["old"], "after": row["new"]}
            for row in plan["reusedPassageChanges"]],
        curatedProjection=[{
            "kanji": "励", "quizOnyomi": ["レイ"], "quizKunyomi": ["はげ.む", "はげ.ます"],
            "onKeys": ["れい"], "kunKeys": ["はげむ"]}],
        readingProjectionCorrection787=plan["readingProjectionCorrection787"],
        quizAudit={"励": {
            "title": plan["proposedMetadata"]["title"],
            "distractors": plan["proposedMetadata"]["distractors"],
            "labels": [metadata(R, f"kanji/{c}.md")["title"]
                       for c in plan["proposedMetadata"]["distractors"]],
            "meaningDecisions": plan["quizPlan"]["distractors"],
            "directExclusions": plan["quizPlan"]["directGuards"],
            "guardSemantics": plan["quizPlan"]["guardSemantics"],
            "poolLimits": plan["quizPlan"]["fallbackScope"],
            "limits": "Unreviewed author decisions; actual qualified builder, semantic and native checks remain."}},
        wordQuizAudit={
            "directExclusions": [{"word": row["word"], "exclude": row["quiz_exclusions"]}
                                 for row in plan["newSupportMetadata"]],
            "evidence": plan["quizPlan"]["wordGuardEvidence"],
            "guardSemantics": plan["quizPlan"]["wordGuardSemantics"],
            "limits": "27 direct pairs; not transitive, not exhaustive live/future pool safety."},
        strokeDraft={"source": evidence, "converted": True, "converterNormalizedSha256": converter_hash,
                     "generatedSha256": sha(stroke_path.read_bytes()), "nativeDrawingAccepted": False},
        limits=[
            "LOCAL UNREVIEWED runtime draft only; no push or acceptance.",
            "Original785/786 source-only receipts remain historical, including corrected786 offered-key claim.",
            "Three selected entries yield TWO offered keys: れい/はげむ; sharedはげ stem collapses はげ.ます.",
            "Both blind different-family serial reviews, actual qualified Android/native/rendered acceptance and all publication gates remain.",
            "Physical-phone/general-release and whole-set acceptance outstanding."],
        nextAction="SAME103 freeze audit and signed local unreviewed snapshot, then two serial blind different-model-family textual reviews on the identical frozen tree. Do not push this unreviewed draft.")
    save(S / "batch-103-progress.json", ledger)
    print("Seven strokes generated from pinned SVG; unreviewed runtime ledger and corrected TWO-key projection saved.")


def audit():
    import xml.etree.ElementTree as ET
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    from extract_n1_jmdict import extract

    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    result = batch_audit(R, "103")
    assert result["curatedOfferedKeys"] == 2 and result["readingDispositions"] == 3
    plan = load(S / "batch-103-authoring-plan.json")
    meta = metadata(R, "kanji/励.md")
    assert meta == plan["proposedMetadata"]
    source = next(r for r in load(S / "source-index.json") if r["kanji"] == "励")
    assert source["sourceRow"] == 114
    assert source == load(S / "batch-103-source-navigation.json")["sourceIndexRecord"]
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
        inputs[name] = raw
    assert sha(gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])) == snapshot["jmdict"]["xmlSha256"]
    assert sha(gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])) == snapshot["kanjidic2"]["xmlSha256"]
    for packet, selection in [("batch-103-jmdict.xml", "batch-103-lexical-selection.json"),
                               ("batch-103-comparison-jmdict.xml", "batch-103-comparison-selection.json")]:
        ids = load(S / selection)["entryIds"]
        assert (S / packet).read_bytes() == extract(
            inputs["n1-implementation-JMdict_e.gz"],
            snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    for page in load(S / "batch-103-public-source-receipts.json"):
        raw = (S / page["archive"]).read_bytes()
        assert sha(raw) == page["archiveSha256"]
        assert sha(gzip.decompress(raw)) == page["rawSha256"]
        assert sha((S / page["extractedText"]).read_bytes()) == page["extractedTextSha256"]
    current = load(R / "manifest.json")
    assert build_manifest(R) == current
    old_manifest = json.loads(base_file(R, HEAD, "manifest.json"))
    additions = {"kanji/励.md", "strokes/励.json", *plan["newSupportArticles"]}
    changed = {r["article"] for r in plan["reusedPassageChanges"]}
    runtime_delta(old_manifest, current, additions, changed)
    for row in plan["reusedPassageChanges"]:
        reused_changes(base_file(R, HEAD, row["article"]),
                       (R / row["article"]).read_text(encoding="utf-8"),
                       [{"before": row["old"], "after": row["new"]}])
    comparison = load(S / "batch-103-comparison-selection.json")
    for record in comparison["articleSnapshots"]:
        path = R / record["article"]
        assert metadata(R, record["article"]) == record["metadata"]
        if record["article"] not in changed:
            assert sha(path.read_bytes()) == record["sha256"]
    for row in plan["newSupportMetadata"]:
        m = metadata(R, f"words/{row['word']}.md")
        assert m == row and "jlpt" not in m
        assert not any(tag.startswith("jlpt-") for tag in m["tags"])
    assert not (R / "kanji" / "激.md").exists()
    assert "(../kanji/激.md)" not in (R / "words" / "激励.md").read_text(encoding="utf-8")
    pairs = {tuple(sorted([row["word"], other]))
             for row in plan["newSupportMetadata"] for other in row["quiz_exclusions"]}
    assert len(pairs) == 27
    expected_pairs = {tuple(sorted([word, other]))
                      for row in plan["quizPlan"]["wordGuardEvidence"]
                      for word in row["newWords"] for other in row["neighbors"]}
    assert pairs == expected_pairs
    assert meta["quiz_exclusions"] == ["努", "勉", "勤", "支"]
    for c in meta["distractors"]:
        assert not set(meta["distractors"]) & set(metadata(R, f"kanji/{c}.md").get("quiz_exclusions", []))
    svg = (S / "batch-103-kanjivg.svg").read_bytes()
    evidence = load(S / "batch-103-stroke-evidence.json")
    assert sha(svg) == evidence["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == evidence["gitBlob"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == evidence["converterNormalizedSha256"]
    strokes = load(R / "strokes" / "励.json")
    assert strokes == convert("励", svg.decode("utf-8"))
    assert strokes["strokeCount"] == len(strokes["strokes"]) == 7
    assert [r["id"] for r in strokes["strokes"]] == list(range(1, 8))
    assert all(len(r["points"]) == 16 and
               all(len(p) == 2 and all(math.isfinite(v) for v in p) for p in r["points"])
               for r in strokes["strokes"])
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 7
    text = "\n".join((R / n).read_text(encoding="utf-8") for n in sorted(additions) if n.endswith(".md"))
    text += "\n" + "\n".join(r["new"] for r in plan["reusedPassageChanges"])
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
    assert len(fonts) == 3 and all(f["missing"] == ["厂"] for f in fonts) and not rare
    save(S / "batch-103-draft-font-audit.json", {
        "schemaVersion": 1, "batch": "103", "execution": 787,
        "scope": "All four new Markdown files including metadata and exactly three changed navigation passages; generated geometry stroke-type glyphs covered structurally, not treated as Han prose.",
        "han": han, "hanCount": len(han), "rareHan": rare, "bundledFonts": fonts,
        "defaultSystemFont": "Later native four-font rendering required",
        "requiredNativeFallbackTarget": "厂 U+5382, absent from all three bundled cmaps",
        "limits": "Cmap absence is not rendered failure; no fresh native/rendered or physical-phone evidence."})
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
    assert count == 8463
    before = load(L / "progress-before-787.json")
    now = load(C / "progress.json")
    assert all(now[k] == v for k, v in before.items() if k not in {"stage", "nextAction", "blocker"})
    changed_paths = git("diff", "--name-only", HEAD).splitlines()
    assert set(changed_paths) == {
        "manifest.json", "docs/n1-sources/batch-103-authoring-plan.json",
        "docs/n1-sources/batch-103-progress.json", *changed}
    for folder in ["kanji", "words", "strokes"]:
        files = set(git("ls-tree", "-r", "--name-only", HEAD, "--", folder).splitlines())
        actual_files = {p.relative_to(R).as_posix() for p in (R / folder).glob("*") if p.is_file()}
        assert actual_files - files == {n for n in additions if n.startswith(folder + "/")}
        assert not files - actual_files
    result.update(
        execution=787, sourceRow=114, draftSignedBase=HEAD, androidSignedHead=APP,
        sourceInputsVerified=len(inputs), decompressedDictionaryHashesVerified=2,
        completeMemberFamilies=47, completeComparisonFamilies=31, archivedPublicPagesVerified=4,
        readingSelectionEntries=3, actualOfferedKeys={"on": ["れい"], "kun": ["はげむ"]},
        correctedEarlierProjection=True, baselineComparisonMetadataPreserved=34,
        directKanjiGuards=4, directWordGuards=27, requiredLinkDirections=6,
        geometryRegenerationEqual=True, generatedStrokes=7, pointsPerStroke=16,
        actualDraftHan=len(han), missingFromAllBundledCmaps=["厂"], rareHanCharacters=0,
        runtimeManifestHashesVerified=count,
        kanjiCount=len(list((R / "kanji").glob("*.md"))),
        wordCount=len(list((R / "words").glob("*.md"))),
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        independentReviewersLaunched=0, freshAndroidOrNativeClaimed=False,
        publishedAdditions=129, remainingAdditions=1099,
        limits="Mechanical LOCAL UNREVIEWED draft audit, not independent linguistic review, exhaustive quiz-pool safety, native/rendered/font/phone acceptance or publication.")
    save(S / "batch-103-draft-audit-787.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def next_action():
    return (
        "SAME103 independent textual review of the identical signed LOCAL UNREVIEWED snapshot: "
        "one headless read-only reviewer at a time, two actual different model families from current catalog, "
        "serial internal tools/no nested agents; wait for real exit and persist complete original report before next. "
        "Use the frozen runtime scope and committed47member/31comparison/fourpublic-page source packets, "
        "all three new necessary supports and three exact navigation-only reused changes. Explicitly review "
        "the corrected TWO offered keys れい/はげむ: はげ.む and はげ.ます share the はげ stem; "
        "both full entries/order/selections/linked rows preserved, not three independent practice questions. "
        "Four directkanji/27directword safeguards are symmetric NONTRANSITIVE; three allmappedpairs/sixdirections, "
        "zeroactivatedbaselinepairs. Actual47Han includes 厂 U+5382 absent from all THREEbundledcmaps; "
        "NOT glyphfailure/renderedacceptance. Require actual 厂 fallback/readability in allfourfonts/default. "
        "All original original-session confirmations, non-skipped qualified Android, ContentSyncONCE/native/"
        "rendered/semantic option-set acceptance, combined-current-main/normal signing/ownerfastforward/"
        "terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entry/42MiBcompressed/80MiBinflated/"
        "56MiBretained/perfilepathmedia/verifiedownerissue gates remain required before publication or104. "
        "Verify clean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. Parent5920 ownsrunner.lock: "
        "no childacquire/delete/unlock/readprobe; approvedcontrol/committedsource/frozeninputs only, no optional "
        "historicalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
        "No unreviewedpush,104,authoragents,concurrentheavywork,secondrunner,signingretry or guardincrease. "
        "Published129/1228 and1099acceptance-remainder unchanged; draft1126kanji5077words includes ONEunreviewedaddition/"
        "THREEunreviewednecessarysupports, not delivered N1 vocabulary. Six separatelyplacedsource保案派第策結 "
        "retain earlierN2levels and are not issue60accepted additions; never duplicate/relevel. "
        "CompatibleAndroid#132/main2edbf366 plus#125 required; oldclientsignore. QualifiedsignedAndroid"
        "bf30cdead8515739bc0e671d57a54b9a3109dd46 approvedguard+schemaonlybridges NOTunrelatedlatestmain. "
        "Original102finite128optionset/40labelsemanticacceptanceCLEANonlywithinsample/unrestrictedlivepoolUNVERIFIED; "
        "original780ClaudeNONCOMPLIANT/UNACCEPTED immutable/781dependentsupplementNOTretroacceptance/"
        "782rescaledrenditionsNOToriginalpixels/equalcomprehension/nativespeaker retained. Original historical "
        "readdepth/image/process/permission/OOM/source-only/pending limits remain, not retroaccepted or freshly certified. "
        "Original786 three-key claim explicitly corrected, not rewritten in its historical receipts. "
        "Physicalphone/generalrelease/whole-setoutstanding; projectincomplete."
    )


def record():
    result = load(S / "batch-103-draft-audit-787.json")
    assert result["runtimeManifestHashesVerified"] == 8463 and result["curatedOfferedKeys"] == 2
    checks = {}
    for name in ["source-tests", "validate", "manifest", "batch-audit", "audit", "budget",
                 "vocabulary", "whitespace"]:
        raw = (L / f"{name}-787.txt").read_bytes()
        path = S / f"batch-103-{name}-787.txt.gz"
        path.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(path.read_bytes()) == raw
        checks[name] = {"archive": path.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                        "archiveSha256": sha(path.read_bytes())}
    tests = (L / "source-tests-787.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-787.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    plan = load(S / "batch-103-authoring-plan.json")
    scope = ["kanji/励.md", "strokes/励.json", *plan["newSupportArticles"],
             *[r["article"] for r in plan["reusedPassageChanges"]], "manifest.json"]
    hashes = {name: {"rawSha256": sha((R / name).read_bytes()),
                     "manifestSha256": manifest_sha256(R / name)} for name in scope}
    diff = subprocess.check_output(
        ["git", "--no-pager", "-c", "core.quotepath=false", "diff", HEAD, "--",
         *[r["article"] for r in plan["reusedPassageChanges"]]], cwd=R)
    diff_path = S / "batch-103-navigation-diff-787.patch.gz"
    diff_path.write_bytes(gzip.compress(diff, mtime=0))
    assert gzip.decompress(diff_path.read_bytes()) == diff
    save(S / "batch-103-draft-freeze-787.json", {
        "schemaVersion": 1, "batch": "103", "execution": 787,
        "signedParent": HEAD, "publishedBase": MAIN, "androidSignedHead": APP,
        "status": "local-unreviewed-runtime-draft",
        "runtimeFiles": hashes, "contentVersion": result["contentVersion"],
        "navigationDiff": {"archive": diff_path.name, "rawBytes": len(diff),
                           "rawSha256": sha(diff), "archiveSha256": sha(diff_path.read_bytes())},
        "readingProjectionCorrection": plan["readingProjectionCorrection787"],
        "sourcePackets": ["batch-103-jmdict.xml", "batch-103-comparison-jmdict.xml",
                          "batch-103-kanjidic2.xml", "batch-103-comparison-kanjidic2.xml",
                          "batch-103-public-source-receipts.json"],
        "textualReviewScope": {
            "newArticles": ["kanji/励.md", *plan["newSupportArticles"]],
            "changedReusedPassages": plan["reusedPassageChanges"],
            "facets": ["correctness", "scoped coverage", "phone comprehensibility"],
            "quizScope": "Actual labels, three curated wrong choices, four direct kanji and27 direct word guards, ordinary secondary senses and legacy-fallback disposition. Actual builder/live-pool/native checks remain separate later gates.",
            "readingScope": "Three selected entries, two actual offered keys; explicit shared-stem grouping, plain励ます versus polite励みます, activityに versus personを.",
            "fontScope": "Actual47Han; 厂 fallback/readability in allfourfonts remains later native/rendered gate.",
            "process": "TWO different actual model families, independent blind initials on identical frozen teaching; ONE active reviewer and serial internal tools; no author rationale or other report in initial prompts."},
        "limits": "Byte freeze, not reviewer comprehension, linguistic correctness, app/native/font/phone acceptance or publication."})
    ledger = load(S / "batch-103-progress.json")
    ledger.update(draftAudit="batch-103-draft-audit-787.json",
                  draftFreeze="batch-103-draft-freeze-787.json",
                  draftFontAudit="batch-103-draft-font-audit.json", nextAction=next_action())
    save(S / "batch-103-progress.json", ledger)
    helpers = {}
    for source_name, target in [("draft-787.py", "batch-103-draft-recipe-787.py"),
                                ("preflight-787.ps1", "batch-103-preflight-787.ps1.txt"),
                                ("checks-draft-787.ps1", "batch-103-checks-draft-787.ps1.txt")]:
        shutil.copyfile(C / source_name, S / target)
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-787.json")
    shutil.copyfile(L / "preflight-787.json", S / "batch-103-runner-role-787.json")
    save(S / "execution-787.json", {
        "schemaVersion": 1, "execution": 787, "checkpoint": 787, "batch": "103",
        "stage": STAGE, "baseCommit": HEAD, "publishedBase": MAIN, "androidSignedHead": APP,
        "membership": ["励"], "sourceRows": [114], "draftAudit": result, "validation": checks,
        "draftFreeze": "batch-103-draft-freeze-787.json", "durableHelperHashes": helpers,
        "runnerPreflight": role, "runtimeDrafted": ["励"], "newNecessarySupportWords": 3,
        "reviewClosed": [], "published": [], "runtimeChanged": True, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 129, "remainingAdditions": 1099, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [],
        "authorInspection": {
            "memberFamilies": "47 complete compact families freshly read, lines1-47 returned without truncation.",
            "comparisonFamilies": "31 complete compact families freshly read, lines1-15/16-31 returned without truncation.",
            "publicDictionaries": "All FOUR committed extracted actual dictionary headings/sense blocks freshly read; no new upstream fetch claimed. Existing gaiji/extraction limits preserved.",
            "freshExistingArticles": ["kanji/劣.md", "kanji/万.md", "kanji/厚.md", "words/応援.md",
                                      "words/慰める.md", "words/学問.md", "words/努める.md", "words/努力.md"],
            "otherComparisons": "Source786's34-article inspection inherited, not repeated in full. All34 metadata snapshots reverified; source families freshly read. Not equal fresh-read coverage or independent review.",
            "productionReadingCode": "Qualified bf30cdead core KanjiReadings.kt stem and quizReadings inspected directly; Python mirror confirms TWO keys.",
            "diagnostics": "Two guessed optional in-workspace evidence filenames were absent; used actual committed source paths after glob discovery. Initial staged diff check flagged literal blank context lines in the archived navigation.patch, not runtime whitespace. Replaced that generated artifact with lossless hashed gzip; final staged check required. No permission denial, historical-session access or silent substitution."},
        "nextAction": next_action(),
        "limits": "Normally signed LOCAL UNREVIEWED checkpoint only. No push, reviewer, Android/native/rendered acceptance or next batch. Forty-three focused source tests, not the later full acceptance suite. Existing vocabulary pilot coverage remains incomplete. All original gates/historical limits remain."})
    print("Draft freeze, corrected offered-key evidence, validation receipts and durable recipes archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    result = load(S / "batch-103-draft-audit-787.json")
    body = (
        "Batch 103 / checkpoint 787: **LOCAL UNREVIEWED runtime draft frozen; not published**.\n\n"
        f"Normally signed saved commit `{head}`; public main remains `{MAIN}`.\n\n"
        "Drafted frozen row114 **励**, seven strokes generated by the unchanged pinned KanjiVG converter, "
        "and three necessary support articles **激励・励む・励ます**. Exactly three navigation-only "
        "reused changes (応援・慰める・学問); existing metadata/levels/identities/guards preserved. "
        "Supporting-word levels are omitted rather than inferred from the N1 kanji. Three all-mapped "
        "pairs/six directions; zero activated baseline pairs; four direct kanji and27 direct word "
        "safeguards remain symmetric, nontransitive and unreviewed, not universal pool certification.\n\n"
        "**Correction to checkpoint786:** the app groups readings by the kana stem before the dot. "
        "はげ.む and はげ.ます share はげ, so the three selected full readings produce **TWO actual "
        "practice keys: れい / はげむ**, not three. Complete metadata/order and both linked kun rows/"
        "selections remain; the card explains that はげます does not create a separate question. "
        "No algorithm or SRS change. The original786 audit/issue claim is preserved as historical "
        "evidence, explicitly corrected here and in the draft ledger. Plain 励ます versus polite "
        "励みます, and activity に励む versus person を励ます, are taught explicitly.\n\n"
        f"Actual **{result['actualDraftHan']} draft Han** audited against all three bundled font cmaps: "
        "**厂 U+5382** remains absent from all three. This is NOT a glyph-failure or rendered-acceptance "
        "claim; actual 厂 fallback/readability in all four selected/default modes remains mandatory. "
        "No rare-Han-range character introduced; seven generated16-point strokes regenerate identically.\n\n"
        "43 focused source tests, validator, regenerated manifest, existing batch audit, exact source/"
        "metadata/navigation/link/font/guard audit, vocabulary consistency and unchanged packaging budgets "
        "passed. Vocabulary coverage remains the existing incomplete pilot (2122/2431 reviewed prompts). "
        f"Every **{result['runtimeManifestHashesVerified']} runtime hash** verified; contentVersion "
        f"`{result['contentVersion']}`. Local draft totals1126kanji/5077words include this unaccepted "
        "draft and must not be counted as delivery.\n\n"
        "**129/1228 additions published; 1099 acceptance remainder unchanged.** No reviewers, app/native/"
        "rendered checks, push or next batch in this execution. Next is SAME103 two serial blind "
        "different-family textual reviews on this exact frozen teaching, then every original confirmation/"
        "qualified Android/native/rendered/current-main/signing/owner-fast-forward/terminal-CI/exact-immutable-ZIP "
        "acceptance gate. Approved signed Android `bf30cdead8515739bc0e671d57a54b9a3109dd46` remains "
        "the qualified curated-reading/pair-guard+schema-only backport, not unrelated latest main. Compatible "
        "stop-cran/kanji-cards-android#125 and stop-cran/kanji-cards-android#132 mechanisms required; "
        "old clients ignore them. Parent launcher ancestry/session verified without touching its lock; "
        "approved workspace/control artifacts only, no new denial. Physical-phone/general-release/"
        "whole-set acceptance remains outstanding; original historical process/image/read-depth limits "
        "are not retroaccepted.\n"
    )
    (C / "issue-787.txt").write_text(body, encoding="utf-8", newline="\n")
    save(C / "issue-request-787.json", {"body": body})
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G" and not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP and not git("status", "--porcelain", root=A)
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    frozen = load(S / "batch-103-draft-freeze-787.json")
    for name, hashes in frozen["runtimeFiles"].items():
        assert sha((R / name).read_bytes()) == hashes["rawSha256"]
        assert manifest_sha256(R / name) == hashes["manifestSha256"]
    assert build_manifest(R) == load(R / "manifest.json")
    changes = set(git("diff", "--name-only", HEAD, head).splitlines())
    runtime = set(frozen["runtimeFiles"])
    assert runtime <= changes
    assert all(n in runtime or n.startswith("docs/n1-sources/batch-103-") or
               n == "docs/n1-sources/execution-787.json" for n in changes)
    before = load(L / "progress-before-787.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    posted = load(L / "issue-787-verified.json")
    body = (C / "issue-787.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body and head in body
    result = load(S / "batch-103-draft-audit-787.json")
    receipt = {
        "schemaVersion": 1, "execution": 787, "checkpoint": 787, "batch": "103",
        "savedCommit": head, "signature": "G", "sourceBase": HEAD, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-787.json", "membership": ["励"], "sourceRows": [114],
        "completeMemberFamilies": 47, "completeComparisonFamilies": 31,
        "metadataReadingEntries": 3, "newNecessarySupportWords": 3,
        "sourcePreparationComplete": True, "runtimeDrafted": ["励"], "reviewClosed": [], "published": [],
        "runtimeChanged": True, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 129, "remainingAdditions": 1099,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue", "stage": STAGE,
        "runtimeManifestHashesVerified": result["runtimeManifestHashesVerified"],
        "contentVersion": result["contentVersion"], "sourceTestsPassed": 43,
        "draftAudit": result, "draftFreeze": "docs/n1-sources/batch-103-draft-freeze-787.json",
        "readingProjectionCorrection": frozen["readingProjectionCorrection"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": next_action(), "blocker": None}
    p["execution787StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p["execution787CoordinatorCheckpoint"] = receipt
    p["batch103DraftIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": sha(body.encode("utf-8")), "verified": True}
    p.update(checkpoint=787, status="continue", stage=STAGE, nextAction=next_action(), blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p and all(reread[k] == v for k, v in before.items() if k not in mutable)
    save(L / "checkpoint-787-final-verification.json", receipt)
    print(json.dumps({"checkpoint": 787, "status": "continue", "savedCommit": head,
                      "signature": "G", "drafted": ["励"], "reviewed": [], "published": [],
                      "historicalRootKeysPreserved": len(before),
                      "issueUpdate": posted["html_url"], "runtimePublished": False}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["start", "generate", "audit", "record", "issue", "finish"])
    args = parser.parse_args()
    globals()[args.mode]()
