"""Freeze the source-complete batch 106 as local unreviewed content."""
import argparse
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
S = R / "docs" / "n1-sources"
L = C / "logs" / "2aeccbc9-c6fe-4ac9-80dc-3c90417aacdc"
HEAD = "aee3db6af366ff51a422448b73db9c54aa8ac326"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
MAIN = "0c582f18b31f65a5e1a908d92e37dde3d34f81ee"
ADDED_LINE = "- [勅令](../words/勅令.md) ちょくれい - imperial edict; a historical/governmental term"
sys.path.insert(0, str(R / "tools"))
sys.stdout.reconfigure(encoding="utf-8")


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".821.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == value
    tmp.replace(path)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), *args],
                                   encoding="utf-8").strip()


def start():
    assert git("rev-parse", "HEAD") == HEAD
    assert not git("status", "--porcelain", "--untracked-files=all")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (820, "106", "continue")
    preflight = load(L / "preflight-821.json")
    assert preflight["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    embedded = json.loads(text.split(marker, 1)[1])
    assert embedded["checkpoint"] == 820
    before = L / "progress-before-821.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 821, "batch": "106", "startingHead": HEAD,
        "scope": "SAME106 bounded runtime draft and normal signed LOCAL UNREVIEWED freeze only; no reviewer, Android/native, publication,107 or second runner.",
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "request": {
            "sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed before implementation. Operative contract, complete approved issue and final820 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."
        },
        "runnerPreflight": preflight,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution821StartingState"] = state
    p.update(stage="batch-106-runtime-draft-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Bounded draft scope persisted; complete progress history retained.")


def geometry():
    from generate_strokes import convert, KANJIVG_REVISION, POINTS_PER_STROKE
    evidence = load(S / "batch-106-stroke-evidence.json")
    source = (S / "batch-106-kanjivg.svg").read_bytes()
    converter = (R / "tools" / "generate_strokes.py").read_text(encoding="utf-8")
    assert sha(source) == evidence["sha256"]
    assert sha(converter.encode()) == evidence["converterNormalizedSha256"]
    assert KANJIVG_REVISION == evidence["revision"] and POINTS_PER_STROKE == 16
    out = R / "strokes" / "勅.json"
    assert not out.exists()
    data = convert("勅", source.decode("utf-8"))
    variants = load(R / "tools" / "order_variants.json")
    if "勅" in variants:
        data["orderVariants"] = variants["勅"]
    assert data["strokeCount"] == 9
    assert [s["id"] for s in data["strokes"]] == list(range(1, 10))
    assert all(len(s["points"]) == 16 for s in data["strokes"])
    out.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
                   encoding="utf-8")
    print("Generated nine ordered strokes at 16 points/path using unchanged pinned converter.")


def audit():
    from audit_n1_pilot import metadata, offered_keys
    from build_manifest import build_manifest, sha256 as text_sha
    from extract_n1_jmdict import extract
    from generate_strokes import convert
    from fontTools.ttLib import TTFont

    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    plan = load(S / "batch-106-source-completion-plan.json")
    assert plan["sourcePreparationComplete"] and plan["membership"] == ["勅"]
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    for name, rec in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert sha(raw) == rec["sha256"] and len(raw) == rec["bytes"], name
    kd_raw = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert sha(kd_raw) == snapshot["kanjidic2"]["xmlSha256"]
    kd = ET.fromstring(kd_raw)
    character = next(e for e in kd.findall("character") if e.findtext("literal") == "勅")
    assert [r.text for r in character.findall(".//reading[@r_type='ja_on']")] == ["チョク"]
    assert [r.text for r in character.findall(".//reading[@r_type='ja_kun']")] == ["いまし.める", "みことのり"]
    source_members = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert len(source_members) == len(set(source_members)) == 1232 and "勅" in source_members
    source_index = load(S / "batch-106-input-metadata.json")["sourceIndexRecord"]
    assert source_index["sourceRow"] == 117 and source_index["kanji"] == "勅"
    packets = [
        ("lexical-selection", "jmdict", 44),
        ("comparison-selection", "comparisons", 17),
        ("completion-selection", "completion-comparisons", 18),
    ]
    families = set()
    jm_raw = (C / "inputs" / "n1-implementation-JMdict_e.gz").read_bytes()
    assert sha(gzip.decompress(jm_raw)) == snapshot["jmdict"]["xmlSha256"]
    for selection, packet, count in packets:
        ids = load(S / f"batch-106-{selection}.json")["entryIds"]
        assert len(ids) == count and not families.intersection(ids)
        assert extract(jm_raw, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
                       ids) == (S / f"batch-106-{packet}.xml").read_bytes()
        families.update(ids)
    assert len(families) == 79
    for receipt_file in ["batch-106-public-source-receipts.json",
                         "batch-106-completion-public-receipts.json"]:
        for rec in load(S / receipt_file):
            archived = (S / rec["archive"]).read_bytes()
            assert sha(archived) == rec["archiveSha256"]
            assert sha(gzip.decompress(archived)) == rec["rawSha256"]
            assert sha((S / rec["extractedText"]).read_bytes()) == rec["extractedTextSha256"]

    baseline = load(S / "batch-106-baseline-plan.json")
    before_manifest = baseline["runtimeManifest"]
    assert before_manifest == json.loads(subprocess.check_output(
        ["git", "show", f"{HEAD}:manifest.json"], cwd=R, encoding="utf-8"))
    current = load(R / "manifest.json")
    assert current == build_manifest(R)
    maps = ["files", "images", "scenes", "curriculum", "listening", "audio",
            "listeningTasks", "listeningTaskAudio", "listeningTaskImages"]
    additions, changed, verified = {}, [], 0
    binary = {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
    for kind in maps:
        before, after = before_manifest.get(kind, {}), current.get(kind, {})
        assert set(before) <= set(after), kind
        additions[kind] = sorted(set(after) - set(before))
        for path, digest in after.items():
            actual = sha((R / path).read_bytes()) if kind in binary else text_sha(R / path)
            assert actual == digest, path
            verified += 1
            if path in before and before[path] != digest:
                changed.append(path)
    assert additions["files"] == ["kanji/勅.md", "strokes/勅.json", "words/勅令.md"]
    assert all(not paths for kind, paths in additions.items() if kind != "files")
    assert changed == ["kanji/令.md"]
    for name, rec in baseline["inventory"].items():
        assert metadata(R, name) == rec["metadata"], name
        raw = (R / name).read_bytes()
        if name == "kanji/令.md":
            line = ADDED_LINE.encode("utf-8")
            assert raw.count(line) == 1
            raw = raw.replace(line + b"\r\n", b"").replace(line + b"\n", b"")
        assert sha(raw) == rec["sha256"], name
    assert len(baseline["inventory"]) == 1128 + 5079
    k = metadata(R, "kanji/勅.md")
    w = metadata(R, "words/勅令.md")
    for field in ["title", "jlpt", "tags", "strokes", "radical", "radicalNumber",
                  "onyomi", "kunyomi", "quizOnyomi", "quizKunyomi"]:
        assert k[field] == plan["kanjiPlan"][field], field
    assert "phonetic" not in k
    assert k["distractors"] == ["束", "効", "勤"] and k["quiz_exclusions"] == ["令", "命"]
    assert w["reading"] == "ちょくれい" and w["kanji"] == ["勅", "令"] and "jlpt" not in w
    assert w["title"] == "imperial edict" and w["type"] == "kango"
    assert w["quiz_exclusions"] == ["命令", "命じる", "命ずる", "法", "法律", "規則"]
    for char in k["distractors"] + k["quiz_exclusions"]:
        assert (R / "kanji" / f"{char}.md").is_file()
    assert len({metadata(R, f"kanji/{c}.md")["title"] for c in k["distractors"]}) == 3
    for word in w["quiz_exclusions"]:
        assert (R / "words" / f"{word}.md").is_file()
    for row in plan["linkPlan"]["requiredDirections"]:
        assert row["relative"] in (R / row["from"]).read_text(encoding="utf-8"), row
    assert [p.stem for p in (R / "words").glob("*.md")
            if "勅" in metadata(p.parent, p.name).get("kanji", [])] == ["勅令"]
    assert not any("勅" in rec["metadata"].get("kanji", [])
                   for name, rec in baseline["inventory"].items() if name.startswith("words/"))
    assert offered_keys(k["quizOnyomi"]) == ["ちょく"] and offered_keys(k["quizKunyomi"]) == []
    assert not (R / "words" / "勅.md").exists()
    svg = (S / "batch-106-kanjivg.svg").read_bytes()
    stroke_source = load(S / "batch-106-stroke-evidence.json")
    assert sha(svg) == stroke_source["sha256"]
    assert hashlib.sha1(b"blob " + str(len(svg)).encode() + b"\0" + svg).hexdigest() == stroke_source["gitBlob"]
    assert text_sha(R / "tools" / "generate_strokes.py") == stroke_source["converterNormalizedSha256"]
    expected_strokes = convert("勅", svg.decode("utf-8"))
    variants = load(R / "tools" / "order_variants.json")
    if "勅" in variants:
        expected_strokes["orderVariants"] = variants["勅"]
    assert load(R / "strokes" / "勅.json") == expected_strokes

    texts = [(R / p).read_text(encoding="utf-8") for p in ["kanji/勅.md", "words/勅令.md"]]
    texts.append(ADDED_LINE)
    han = sorted({c for text in texts for c in text
                  if 0x3400 <= ord(c) <= 0x9fff or 0xf900 <= ord(c) <= 0xfaff})
    ranges, start = [], None
    radical_checked = False
    for line in (C / "inputs" / "n1-UnicodeData-17.0.0.txt").read_text(encoding="utf-8").splitlines():
        fields = line.split(";")
        code = int(fields[0], 16)
        if fields[1].endswith(", First>"):
            start = code
        elif fields[1].endswith(", Last>"):
            ranges.append((start, code))
            start = None
        else:
            ranges.append((code, code))
        if code == 0x2F00 + 19 - 1:
            assert fields[5] == "<compat> 529B"
            radical_checked = True
    assert radical_checked and all(any(a <= ord(c) <= b for a, b in ranges) for c in han)
    app = C.parent / "kanji-cards-android"
    fonts = []
    for path in sorted((app / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path.relative_to(app)), "sha256": sha(path.read_bytes()),
                      "missing": [c for c in han if ord(c) not in cmap]})
    assert len(fonts) == 3
    result = {
        "schemaVersion": 1, "execution": 821, "batch": "106", "sourceBase": HEAD,
        "publishedBaseline": MAIN, "sourceRow": 117, "membership": ["勅"],
        "frozenInputHashesVerified": 5, "distinctCompleteDictionaryFamiliesReproduced": 79,
        "sourcePublicArchiveHashesVerified": True, "exactSourceMembershipAndRawMetadataVerified": True,
        "baselineMetadataRecordsPreserved": len(baseline["inventory"]),
        "baselineWordBytesPreserved": 5079, "baselineKanjiBytesUnchanged": 1127,
        "onlyBaselineBodyEdit": {"article": "kanji/令.md", "addedLine": ADDED_LINE,
                                 "allOtherBytesPreserved": True,
                                 "classification": "new sourced example teaching; not navigation-only"},
        "runtimeManifestHashesVerified": verified,
        "baselineRuntimeHashesPreserved": verified - 4,
        "runtimeAdditions": additions, "baselineRuntimeEdits": changed,
        "contentVersion": current["contentVersion"],
        "allMappedPairs": plan["linkPlan"]["allMappedPairs"], "requiredLinkDirectionsVerified": 4,
        "activatedBaselinePairs": [], "fullOnyomi": k["onyomi"], "fullKunyomi": k["kunyomi"],
        "quizOnyomi": k["quizOnyomi"], "quizKunyomi": k["quizKunyomi"],
        "offeredOnKeysMirrorNotAppExecution": ["ちょく"], "offeredKunKeysMirrorNotAppExecution": [],
        "directKanjiGuards": k["quiz_exclusions"], "directWordGuards": w["quiz_exclusions"],
        "guardsSymmetricNotTransitive": True, "curatedWrongChoices": k["distractors"],
        "strokePaths": 9, "pointsPerPath": 16, "exactPinnedConverterOutput": True,
        "actualRuntimeHan": han, "hanCount": len(han), "bundledFonts": fonts,
        "allActualHanInFrozenUnicode": True, "canonicalRadicalFromFrozenUnicode": True,
        "absentFromAllBundledCmaps": [c for c in han if all(c in f["missing"] for f in fonts)],
        "missingCmapIsRenderingFailure": False,
        "runtimeHashes": {p: current["files"][p] for p in
                          ["kanji/勅.md", "kanji/令.md", "words/勅令.md", "strokes/勅.json"]},
        "sourcePlan": "batch-106-source-completion-plan.json",
        "freshAuthorReads": "Source-completion plan, exact member raw record and selected complete1430550/1597670/1604470 families, actual public勅/勅令/notation extracted blocks and current令/命 plus examplecard bodies. Complete79-family/28-article preparation inspection is inherited819/820, not claimed as a fresh full reread.",
        "limits": "Mechanical and author draft audits, not independent linguistic review, production finite quiz-option execution, Android/native/font/phone acceptance. Two serial blind families and every original downstream acceptance gate remain mandatory."
    }
    save(S / "batch-106-draft-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def evidence():
    draft = load(S / "batch-106-draft-audit.json")
    before = load(L / "progress-before-821.json")
    receipts = {}
    for label in ["validate", "manifest", "tests", "vocabulary", "budget", "audit", "whitespace"]:
        raw = (L / f"821-{label}.txt").read_bytes()
        archive = S / f"batch-106-draft-{label}-821.txt.gz"
        archive.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw
        receipts[label] = {"archive": archive.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                           "archiveSha256": sha(archive.read_bytes())}
    helpers = [Path(__file__), C / "preflight-821.ps1", C / "checks-batch-106-draft-821.ps1",
               C / "post-batch-106-draft-821.ps1"]
    for source in helpers:
        shutil.copyfile(source, S / f"batch-106-{source.name}")
    next_action = (
        "SAME106 TWO SERIAL blind different-model-family independent initial TEXTUAL reviews on the SAME "
        "signed LOCAL UNREVIEWED draft; cover complete kanji/勅.md, words/勅令.md and exact new Commonwords "
        "line in kanji/令.md (new sourced teaching, NOT navigation-only), correctness/scopedcoverage/"
        "phonecomprehensibility with serial internal tools and common bounded complete-source access. "
        "Persist complete original reports, actual model identity/process exit/read limits before reconciliation. "
        "No other report/author adjudication in initial prompts, no editing frozen snapshot, confirm first "
        "process exit before second. No Android/native/publication/107/secondrunner in this review checkpoint. "
        "Source820 and draft821 retain row117 勅/fullon[チョク]fullkun[いまし.める,みことのり] EXACTSOURCEORDER/"
        "selected[チョク][]/mirrorちょくNOTproductionexecution; characterdictionaryonlyいまし.める"
        "modernwrittenuseUNVERIFIED/noinventedspelling; documentednounみことのりNOTsearchonly/"
        "outsideJoyoREADINGlistNOTfrequencyorinvalidity/unselectedboundedchoice. ONEnecessary勅令"
        "noinferredwordlevel/sovereigngeneral+MeijilegalformNOTJapanese-onlyMeiji-onlyalloldedictvoid. "
        "THREEwrong束効勤/TWOdirectkanjiguards令命/SIXdirectwordguards命令命じる命ずる法法律規則/"
        "symmetricNONTRANSITIVEnotJapaneseequivalence; later finitequalified HOST+native wordBOTHdirections/"
        "kanji/defaultN1/All/custom/reducedpoolsexactlabelssecondarysenses/fallbackreviewMANDATORY. "
        "TWOmappedpairsFOURdirectionsZEROactivatedbaselinepairs/ONEexact令lineONLYbaselinebodychange/"
        "ALL6207baselinemetadatarecordsand5079wordbytes+1127kanjibytespreserved. PinnedNINEpaths16points"
        "convertedUNCHANGEDconverterNOTnativedrawing; actualHan/fonts in batch-106-draft-audit.json/"
        "cmapNOTreadability/fallbackface; laterALLfourfont/defaultsystem/wholeword/radical/lookalike/rendered"
        "acceptanceMANDATORY. Aftertextualreconciliation alloriginalqualifiednon-skippedAndroidbf30HOST/"
        "nativeContentSyncONCE/meaning/curatedreading/drawing/articles/Back/offline/combinedcurrentmain/"
        "fullPython/vocabulary/baseline-membership-links/manifest/perfilemedia-safepaths/normalsigning/"
        "ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entries42MiBcompressed"
        "80MiBinflated56MiBretained/verifiedownerissue remainMANDATORY. Verifywhollyclean signedheads/"
        "freshmain/liveparentancestry/decodedlauncher/exactsession. Parent13320ownsrunner.lock:"
        "NOchildacquire/delete/unlock/readprobe; approvedcontrol/committedsource/frozeninputs only,"
        "nooptionalhistoricalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
        "Published132/1228,1096remainder unchanged; draft1129kanji5080words138N1labels, ONEnewnecessarysupport"
        "NOTN1vocabulary. Sixseparatelyplaced保案派第策結retainN2/noacceptedcredit/noduplicate/relevel. "
        "CompatibleAndroid125+132required;oldclientsignore;qualifiedsignedbf30cdead8515739bc0e671d57a54b9a3109dd46"
        "guard+schemaonlyNOTlatestmain. Original820/819/818+ALLhistoricalsource/review/process/readdepth/"
        "permission/OOM/ANR/routing/rendering/phone/pendinglimits retained EXACT in execution821Inherited820Gates "
        "and before821snapshot; NOTnew821runs/retroaccepted. Originalpixels/equalcomprehension/fallbackface/"
        "everyrequestretention/native-speaker/phone/effectivenessremainUNVERIFIED; noforcedfindingwithdrawal/"
        "modelvote/newguardfromunprovedhypothesis. Physicalphone/generalrelease/whole-setoutstanding;"
        "projectincomplete. No107/unreviewedpush/authoragents/concurrentheavywork/secondrunner/signingretry/"
        "guardincrease."
    )
    test_text = (L / "821-tests.txt").read_text(encoding="utf-8-sig")
    tests = int(re.search(r"Ran (\d+) tests?", test_text).group(1))
    assert "\nOK" in test_text and tests > 0
    validator = (L / "821-validate.txt").read_text(encoding="utf-8-sig")
    assert "0 error(s)" in validator or "0 errors" in validator
    record = {
        "schemaVersion": 1, "execution": 821, "checkpoint": 821, "batch": "106",
        "stage": "batch-106-local-unreviewed-runtime-draft",
        "baseCommit": HEAD, "publishedBase": MAIN, "androidSignedHead": APP,
        "membership": ["勅"], "sourceRows": [117], "draftAudit": "batch-106-draft-audit.json",
        "validation": receipts, "pythonTestsPassed": tests, "validatorErrors": 0,
        "runnerPreflight": load(L / "preflight-821.json"),
        "runtimeDrafted": ["勅"], "necessarySupportDrafted": ["勅令"],
        "changedReusedPassages": [{"article": "kanji/令.md", "addedLine": ADDED_LINE,
                                   "classification": "new sourced example teaching"}],
        "reviewClosed": [], "published": [], "runtimeChanged": True, "runtimePublished": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "actualBuilderChecked": False, "nativeDrawingAccepted": False, "renderedAcceptance": False,
        "publishedAdditions": 132, "remainingAdditions": 1096, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "nextAction": next_action, "limits": draft["limits"],
        "durableHelperHashes": {f"batch-106-{source.name}": sha(source.read_bytes()) for source in helpers},
        "inheritedGates": {"checkpoint": 820, "nextAction": before["nextAction"],
                           "invariant": "Preserve exact inherited gates and limitations; draft821 does not rerun or retroaccept them."},
    }
    save(S / "execution-821.json", record)
    p = load(S / "batch-106-progress.json")
    p.update(status="local-unreviewed-runtime-draft", drafted=["勅"], runtimeChanged=True,
             draftExecution=821, draftAudit="batch-106-draft-audit.json",
             draftContentVersion=draft["contentVersion"], nextAction=next_action,
             limits="LOCAL UNREVIEWED runtime draft after source820. Original819/820 records remain historical and unchanged. Draft audit is not independent linguistic review or Android/native/rendered/phone acceptance; every original downstream gate remains mandatory.")
    save(S / "batch-106-progress.json", p)
    print("Draft audit, command receipts, durable recipes and unreviewed state preserved.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != HEAD and git("rev-parse", "HEAD^") == HEAD
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    app = C.parent / "kanji-cards-android"
    assert subprocess.check_output(["git", "-C", str(app), "rev-parse", "HEAD"], encoding="utf-8").strip() == APP
    assert not subprocess.check_output(["git", "-C", str(app), "status", "--porcelain",
                                        "--untracked-files=all"], encoding="utf-8").strip()
    assert git("rev-parse", "origin/main") == MAIN
    runner = load(C / "runner.json")
    assert runner["pid"] == 13320 and runner["status"] == "running" and runner["sessionId"] == L.name
    before = load(L / "progress-before-821.json")
    p = load(C / "progress.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    for key, value in before.items():
        if key not in allowed:
            assert p[key] == value, key
    record = load(S / "execution-821.json")
    issue = load(C / "batch-106-draft-821-issue-receipt.json")
    assert issue["verified"] and issue["author"] == "stop-cran" and issue["localCommit"] == head
    checkpoint = dict(record)
    checkpoint.update(savedCommit=head, signature="G", status="continue", dedicatedWorktreesClean=True,
                      originalHistoricalRootValuesPreserved=True, originalRootKeysCompared=len(before),
                      issueUpdate=issue["url"], ownerIssueAuthorAndBodyVerified=True)
    p["execution821CoordinatorCheckpoint"] = checkpoint
    p["execution821Inherited820Gates"] = record["inheritedGates"]
    p["batch106DraftIssueReceipt"] = issue
    p["execution821StartingState"]["status"] = "signed-local-unreviewed-draft-checkpoint-complete"
    p.update(checkpoint=821, status="continue", stage=record["stage"],
             nextAction=record["nextAction"], blocker=None)
    save(C / "progress.json", p)
    reloaded = load(C / "progress.json")
    for key, value in before.items():
        if key not in allowed:
            assert reloaded[key] == value, key
    assert reloaded["checkpoint"] == 821 and reloaded["lastPublishedCommit"] == MAIN
    save(L / "checkpoint-821-verification.json", {
        "savedCommit": head, "signature": "G", "originalRootKeysCompared": len(before),
        "allOriginalHistoricalValuesPreserved": True, "dedicatedWorktreesClean": True,
        "runtimePublished": False, "wholeProjectComplete": False, "parentLockTouched": False})
    print(f"Checkpoint821 saved and verified: {head}; LOCAL UNREVIEWED, not published.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=["start", "geometry", "audit", "evidence", "finish"])
    args = parser.parse_args()
    globals()[args.operation]()
