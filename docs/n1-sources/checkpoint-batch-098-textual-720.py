import copy
import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("batch098", C / "review-batch-098.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.review
R, A, S, V, L = r.R, r.A, r.S, r.V, r.L
load, sha, git = r.load, r.sha, r.git
SNAPSHOT = r.SNAPSHOT
STAGE = "batch-098-textual-review-closed-awaiting-android-native"
NEXT = (
    "SAME098 fresh non-skipped THREE RealContentTest and ONE RareHanTest against THIS sibling next; "
    "textual closure ONLY on signed233d3ad, NOT native or full batch acceptance. "
    "Actual ClaudeOpus5.5 original sessiond41cdccb-18bc-4302-803f-803d7bd4a007 and GPT6.1Sol "
    "original session33216339-ddd8-411a-8aca-b73da1a3bae7 completed serial blind initial reviews "
    "on SAME291277byte/7905line packet:352distinct complete dictionary families/354occurrences, "
    "eight raw records,16complete articles including new剤 and exact reused洗剤/洗 navigation changes. "
    "Both returned exact full packet in first serial view, then each unnecessarily reread one tail "
    "(Claude7880-EOF, GPT7800-EOF); no tool overlap/truncation/missinglines. Original complete "
    "reports/models/sessions/process/read limits archived. No actionable textual defect or "
    "consequential unresolved teaching claim; teaching unchanged, no dependent textual fix confirmation "
    "needed. Optional source-only gloss/shape orientation not adopted. Coordinator independently "
    "confirmed 刈る/刀 link targets, unchanged N2metadata, ten supplied paths and baseline activation; "
    "supplemental full frozen製/推 records support comparative allocation, not fresh reviewer retrieval. "
    "Fullザイ/スイ/セイ andかる/けず.る retained; only quizOnyomi[ザイ], quizKunyomi[] selected. "
    "One existing洗剤せんざい N2 support, originalせっけん exclusion unchanged; no new word/title/guard. "
    "Use explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot and "
    "ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, oneGradleworker and quoted "
    "'-Pkotlin.compiler.execution.strategy=in-process'; inspect terminal test cases and actual sibling path. "
    "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain. Then fresh fullarchive "
    "productionContentSync ONCE/native N1-All actual choices/ざい only and NO kun/tenstroke drawing/"
    "complete剤 article/reused洗剤-洗 links/SystemBack/offline/all19Han/fourfonts with fresh safe "
    "port/device ownership checks; 刂/氵cmap absences NOT glyph failure. Preserve exact fixture/hash "
    "and terminal percase0, no doubleparse, heap/archiveguard increase or shared-device interference. "
    "Original two model sessions need serial bounded rendered confirmations; current textual review "
    "certifies neither native/phone nor widercustom/random/fallback pools. All combined-current-main/"
    "nonrewritingmerge/changedteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutableZIPmanifestentryhash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/"
    "media/path/verifiedownerissue gates remain. Parent19008 retains runner.lock throughout child lifetime; "
    "NO child acquire/delete/unlock/readprobe. Approved control/committed evidence/frozen inputs only, "
    "no optional historical-session helper access. Preserve/report/yield actual new denial/signing hang/"
    "uncertain ownership. Published124/1228 and1104 acceptance remainder unchanged; physicalphone/"
    "generalrelease/whole-set outstanding. No099, unreviewedpush or secondrunner."
)


def save(path, value):
    temp = path.with_suffix(path.suffix + ".720.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def processes():
    records, previous = {}, None
    for label, model in r.MODELS.items():
        prefix = f"batch-098-initial-{label}"
        record = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert record["snapshot"] == SNAPSHOT
        assert record["exitCode"] == 0 and record["actualModels"] == [model]
        assert record["usageCurrentModel"] == model
        assert record["availableTools"] == ["view"] and "--available-tools=view" in record["command"]
        assert record["multiToolResponseCount"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert coverage["allAssignedRangesReturned"]
        assert len(record["toolCalls"]) == 2
        first, second = record["toolCalls"]
        assert first["arguments"] == {"path": str(r.PACKET), "forceReadLargeFiles": True}
        assert second["arguments"] == {
            "path": str(r.PACKET), "view_range": [7880 if label == "claude" else 7800, -1]}
        for call in record["toolCalls"]:
            assert call["name"] == "view" and call["success"]
            assert call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
        assert sha(V / (prefix + ".md")) == record["reportSha256"]
        assert sha(V / (prefix + ".jsonl")) == record["rawExecutionSha256"]
        assert r.absent(record["launcherPid"])
        if previous:
            assert previous < record["startedAt"]
        previous = record["completedAt"]
        records[label] = {
            **{k: record[k] for k in [
                "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
                "requestedModel", "actualModels", "snapshot", "reportSha256", "rawExecutionSha256"]},
            "report": prefix + ".md", "execution": prefix + "-execution.json",
            "coverage": prefix + "-coverage.json", "allAssignedRangesReturned": True,
            "toolCalls": 2, "observedToolOverlaps": 0, "exactFullPacketReturnedInFirstCall": True,
            "unnecessarySerialTailReread": second["arguments"]["view_range"],
            "limits": "Actual complete returned bytes/ranges verified, not comprehension certification.",
        }
    return records


def prepare():
    r.frozen()
    records = processes()
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert r.PACKET.read_bytes() == (V / r.PACKET.name).read_bytes()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (719, "098")
    ledger = load(S / "batch-098-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    receipts = {}
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "098"],
        "tests": [sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
                  "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources"],
        "vocabulary": [sys.executable, "-B", str(R / "tools" / "grammar_vocabulary.py"), "check"],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
        "whitespace": ["git", "--no-pager", "diff", "--check"],
    }
    for name, command in commands.items():
        path = V / f"batch-098-textual-review-{name}-720.txt.gz"
        assert not path.exists()
        run = subprocess.run(command, cwd=R / "tools" if name == "tests" else R,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        path.write_bytes(gzip.compress(run.stdout, mtime=0))
        assert run.returncode == 0, (name, run.stdout.decode("utf-8", errors="replace")[-2000:])
        if name == "tests":
            assert b"Ran 43 tests" in run.stdout and run.stdout.rstrip().endswith(b"OK")
        receipts[name] = {
            "path": path.relative_to(R).as_posix(), "sha256": sha(path),
            "uncompressedSha256": hashlib.sha256(run.stdout).hexdigest(),
        }
        print(name, "passed", flush=True)
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from build_manifest import build_manifest, sha256

    mechanical = audit(R, "098")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "0cbdc2723b0433f2"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8449
    for source in load(V / "batch-098-review-dictionary-provenance.json")["sources"]:
        assert sha(Path(source["path"])) == source["sha256"]
    pairs = ledger["allMappedReciprocalPairs"]
    assert len(pairs) == 2
    for char, word in pairs:
        assert "(../" + word + ")" in (R / "kanji" / (char + ".md")).read_text(encoding="utf-8")
        assert "(../kanji/" + char + ".md)" in (R / word).read_text(encoding="utf-8")
    targets = ["words/刈る.md", "kanji/刀.md"]
    assert all((R / name).is_file() for name in targets)
    frozen = C / "inputs" / "n1-planning-kanjidic2.xml.gz"
    assert sha(frozen) == "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed"
    xml = gzip.decompress(frozen.read_bytes())
    assert hashlib.sha256(xml).hexdigest() == "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8"
    root = ET.fromstring(xml)
    supplemental = ET.Element("kanjidic2")
    supplemental.append(copy.deepcopy(root.find("header")))
    for char, reading in [("製", "セイ"), ("推", "スイ")]:
        record = next(e for e in root.findall("character") if e.findtext("literal") == char)
        assert reading in [e.text for e in record.findall(".//reading[@r_type='ja_on']")]
        supplemental.append(copy.deepcopy(record))
        print("Supplemental frozen record:", ET.tostring(record, encoding="unicode"), flush=True)
    supplement_path = V / "batch-098-coordinator-supplement-kanjidic2.xml"
    ET.indent(supplemental)
    ET.ElementTree(supplemental).write(supplement_path, encoding="utf-8", xml_declaration=True)
    reviewed = {name: sha(R / name) for name in [
        "kanji/剤.md", "words/洗剤.md", "kanji/洗.md", "strokes/剤.json", "manifest.json"]}
    limits = [
        "TEXTUAL closure only, NOT full batch review closure, runtime acceptance or publication; reviewClosed/published arrays remain empty.",
        "Both original reports/executions preserved. Each process returned its exact entire assigned packet in first call, then unnecessarily reread an overlapping tail serially. No truncation/missinglines/overlap/unfinishedtool. Actual exit before next reviewer verified; returned bytes do not certify comprehension.",
        "Both initial reviewers received the same352-family packet and exact two reused diffs, independently of other findings or author adjudication. Claude reports full read but not independent numerical recount; counts mechanically verified. Public text is coordinator-supplied committed extraction, not independent upstream retrieval.",
        "Runtime and all8449 payload hashes unchanged; prior complete source/baseline/stroke/font audit is execution719, not relabelled as fresh full linguistic inspection.",
        "Default-four three kanjichoices accepted textually. Actual N1/All and widercustom/random/legacy fallback pools remain runtime gates; exposure is not certified safe. Old APKs ignore curation.",
        "Coordinator confirms linked刈る/刀 targets and frozen製/推 source readings; this supplemental evidence was not in initial reviewer packet or independently retrieved by reviewers. N2label is preserved baseline metadata, not newly inferred or re-sourced.",
        "Fresh Android/RareHan/native/fourfonts/drawing/reading/N1-All/Back/offline/ContentSyncONCE and dependent original-session rendered review remain pending.",
        "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Compatibleclientf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
        "Published124/1228 and1104 acceptance remainder unchanged; six separate earlierN2source members保案派第策結 and separate妖exception retained. No099 or project completion.",
        "All original combined-main/signing/ownerpush/terminalCI/EVERYimmutableZIPhash/originalbudgets/ownerissue gates remain. Parent lock untouched, no optional historical helper access or new permission denial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 720, "batch": "098", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False, "reviewedRuntimeHashes": reviewed,
        "initialModels": list(r.MODELS.values()), "processes": records,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 291277, "initialPacketLines": 7905,
        "distinctCompleteFamilies": 352, "familyOccurrences": 354, "rawCharacterRecords": 8,
        "completeArticleBodies": 16, "newArticleBodies": 1, "changedReusedPassages": 2,
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
            for name in ["kanji/剤.md:1-57", "words/洗剤.md:28", "kanji/洗.md:38"]},
        "findings": [],
        "optionalDispositions": [
            {"reportedBy": "Claude", "claim": "Clarify where斉 sits in済 versus剤.",
             "status": "optional", "decision": "No edit. Existing note already distinguishes left-hand氵 from right-hand刂; no false orientation claim or consequential gap established."},
            {"reportedBy": "Claude", "claim": "Gloss KANJIDIC2 source-only lookup reading.",
             "status": "optional", "decision": "No edit. Four rows and following paragraph already explain reference-only information, no taught example, not interchangeable with洗剤 and no invalidity/obsolescence inference."}],
        "hypothesisDispositions": [
            {"reportedBy": "Claude; equivalent GPT runtime limit", "claim": "薬/剤 overlap may enter wider legacy fallback.",
             "status": "unresolved", "severity": "runtime gate, not a current default-four teaching defect",
             "decision": "Authored three semantically wrong choices cover default four. Actual N1/All and wider/custom/random/legacy fallback remain runtime gates, not certified. No publication before original acceptance."},
            {"reportedBy": "Both", "claim": "Older APKs ignore curation.",
             "status": "resolved", "decision": "Known compatibility requirement retained. Updatedf9b59a2+ client required; not waived by this textual checkpoint."}],
        "reviewLimitDispositions": [
            {"reportedBy": "Claude", "claim": "刈る/刀 target existence not in supplied packet.",
             "status": "resolved", "decision": "Coordinator confirms both actual files exist; validator and link audit pass. Initial reviewer evidence limitation preserved, not rebranded as reviewer verification.",
             "targetHashes": {name: sha(R / name) for name in targets}},
            {"reportedBy": "Both", "claim": "N2 vocabulary assignment not freshly sourced.",
             "status": "resolved", "decision": "Preservation rather than reclassification is scope. Existing N2metadata retained byte-for-byte; previous full draft/baseline audit and fresh batch audit establish preservation, not a new source claim."},
            {"reportedBy": "Claude", "claim": "製/推 raw source records absent from packet.",
             "status": "resolved", "decision": "Coordinator extracted and inspected complete製/推 from exact hash-verified frozen KANJIDIC2:セイ/スイ respectively. Complete compound families and剤ザイ heading support comparison; no substring-only allocation. Supplement not an independent reviewer read.",
             "supplement": supplement_path.relative_to(R).as_posix(), "sha256": sha(supplement_path),
             "frozenCompressedSha256": sha(frozen),
             "frozenXmlSha256": hashlib.sha256(xml).hexdigest()},
            {"reportedBy": "Claude", "claim": "Ten pinned paths and activated-baseline record not in packet.",
             "status": "resolved", "decision": "Both completeSVG and generatedJSON actually supplied in initial packet; original Claude report also acknowledges10. GPT explicitly inspected10. Coordinator preserves original inconsistent limitation and verifies original draftstrokeaudit exact-regeneration/pathcount and draftaudit baselineactivation1; no native drawing claim."}],
        "modelContributionComparison": {
            "shared": "Both assessed boundmeaning/cleaning-agent scope, full洗剤 examples/translations and soapcategory, rawreadings/order and four source-only qualifications, exactザイallocation/curation, compounds/noncompositional粘剤, metadata/mnemonic/strokes, allfourlinks/twoboundedreusedchanges, preservedN2metadata/せっけん guard, threewronglabels and runtime/upstream/native limits. Equivalent differently labelled observations are shared.",
            "claudeUniqueVerifiedUseful": [], "gptUniqueVerifiedUseful": [],
            "claudeUniqueNonblocking": "Optional shapeorientation and source-onlygloss; explicit targetexistence and製/推 rawrecord limits; inconsistent missingpaths limit retained and checked.",
            "unsupportedMandatorySuggestions": "No mandatory textual fix, new source-only lexical example, historical classification, wordarticle or exclusion established.",
            "limits": "Matched sample/source access, not a general model benchmark, equal-depth comprehension certification or native-speaker review."},
        "actionableRemainingTextualFindingGroups": 0, "consequentialUnresolvedTeachingClaims": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "dependentTextualConfirmation": "Not needed: no teaching edit or established textual defect. Original sessions retained for required later rendered confirmation.",
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "previousCompleteSourceBaselineFontStrokeAudit": "docs/n1-sources/batch-098-draft-audit.json",
        "previousCompleteSourceBaselineFontStrokeAuditSha256": sha(S / "batch-098-draft-audit.json"),
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairsAppliedInDraft": 0,
        "actualHanCount": 19, "nativeFontPending": ["刂", "氵"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    save(V / "batch-098-reconciliation.json", rec)
    ledger["initialDraftLimits"] = copy.deepcopy(ledger["limits"])
    ledger.update(status=STAGE, initialReviewSnapshot=SNAPSHOT, reviewedTeachingSnapshot=SNAPSHOT,
                  textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False, nextAction=NEXT)
    ledger["limits"][0] = limits[0]
    ledger["independentReviewersLaunched"] = 2
    ledger["quizAudit"]["剤"]["limits"] = "Default-four textually accepted; actual production N1/All and wider-pool review pending."
    ledger["textualReview"] = {
        "snapshot": SNAPSHOT, "models": rec["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-098-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-098-reconciliation.json"),
        "teachingChanged": False, "textualReviewClosed": True,
        "actionableRemainingTextualFindings": 0, "runtimeAccepted": False}
    ledger["pendingGates"] = [
        "Fresh non-skipped THREE RealContentTest/ONE RareHanTest against actual sibling.",
        "Full productionContentSyncONCE/native N1-All choices/ざい and NOkun/tenstroke drawing/articles/reusedlinks/Back/offline/all19Han/fourfonts; dependent original-session rendered confirmations.",
        "Combined-current-main integration, changed teaching re-review if needed, all checks/normal signing/owner fastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/originalbudgets/verifiedownerissue."]
    for row in ledger["supportMappings"]:
        row["status"] = "textual-review-closed-awaiting-android-native"
    save(S / "batch-098-progress.json", ledger)
    membership = load(S / "batch-098-membership.json")
    membership["initialDraftLimits"] = copy.deepcopy(membership["limits"])
    membership.update(status=STAGE, initialReviewSnapshot=SNAPSHOT,
                      textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False)
    membership["limits"] = limits[0]
    save(S / "batch-098-membership.json", membership)
    recipe = S / Path(__file__).name
    shutil.copyfile(Path(__file__), recipe)
    shutil.copyfile(C / "preflight-720.ps1", S / "batch-098-textual-preflight-720.ps1.txt")
    save(S / "execution-720.json", {
        "schemaVersion": 1, "execution": 720, "batch": "098", "status": STAGE,
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "startingState": p["execution720StartingState"],
        "reconciliation": "docs/n1-reviews/batch-098-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-098-reconciliation.json"),
        "recipeHashes": {path.relative_to(R).as_posix(): sha(path) for path in [
            recipe, V / "review-batch-098.py", V / "batch-098-serial-review-base-recipe.py",
            S / "batch-098-textual-preflight-720.ps1.txt"]},
        "checks": receipts, "runtimeBytesChanged": False,
        "publishedAdditions": 124, "remainingAdditions": 1104,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT})
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    print("SAME098 two-family TEXTUAL closure saved; Android/native/publication remain.", flush=True)


def staged_whitespace():
    captures = [
        "docs/n1-reviews/batch-098-cli-config-help-execution-720.txt",
        "docs/n1-reviews/batch-098-initial-packet.txt",
    ]
    command = ["git", "--no-pager", "diff", "--cached", "--check"]
    original = subprocess.run(command, cwd=R, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert original.returncode == 2
    names = {line.split(":", 1)[0] for line in original.stdout.decode("utf-8").splitlines()
             if line.startswith("docs/")}
    assert names == set(captures), names
    original_log = V / "batch-098-lossless-capture-whitespace-720.txt.gz"
    original_log.write_bytes(gzip.compress(original.stdout, mtime=0))
    exclusions = [":(exclude)" + name.replace("/", "\\") for name in captures]
    scoped = subprocess.run(command + ["--", ".", *exclusions], cwd=R,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert scoped.returncode == 0, scoped.stdout.decode("utf-8", errors="replace")
    scoped_log = V / "batch-098-staged-authored-whitespace-720.txt.gz"
    scoped_log.write_bytes(gzip.compress(scoped.stdout, mtime=0))
    rec = load(V / "batch-098-reconciliation.json")
    rec["checks"]["staged-authored-whitespace"] = {
        "path": scoped_log.relative_to(R).as_posix(), "sha256": sha(scoped_log),
        "uncompressedSha256": hashlib.sha256(scoped.stdout).hexdigest(),
    }
    rec["whitespaceDiagnostic"] = {
        "initialStagedCheckExitCode": original.returncode,
        "initialLog": original_log.relative_to(R).as_posix(), "initialLogSha256": sha(original_log),
        "exactLosslessCaptureExceptions": {name: sha(R / name) for name in captures},
        "disposition": "Preserve exact original reviewer packet and actual CLI help bytes, including numbered blank-line spaces and CLI trailing blank line. Initial cached whole-tree whitespace check correctly reported only these two lossless captures; authored files pass exact-path scoped check. No capture, report, hash or runtime content edited, no signing attempted in failed wrapper, no acceptance gate waived.",
        "scopedCommand": command + ["--", ".", *exclusions],
    }
    save(V / "batch-098-reconciliation.json", rec)
    ledger = load(S / "batch-098-progress.json")
    ledger["textualReview"]["reconciliationSha256"] = sha(V / "batch-098-reconciliation.json")
    save(S / "batch-098-progress.json", ledger)
    recipe = S / Path(__file__).name
    shutil.copyfile(Path(__file__), recipe)
    evidence = load(S / "execution-720.json")
    evidence["reconciliationSha256"] = sha(V / "batch-098-reconciliation.json")
    evidence["checks"] = rec["checks"]
    evidence["whitespaceDiagnostic"] = rec["whitespaceDiagnostic"]
    evidence["recipeHashes"][recipe.relative_to(R).as_posix()] = sha(recipe)
    save(S / "execution-720.json", evidence)
    print("Authored staged whitespace passed; exact two lossless captures preserved and exceptions recorded.")


def verify_signed():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == SNAPSHOT
    for repo, expected in [(R, head), (A, r.ANDROID)]:
        assert git("rev-parse", "HEAD", repo=repo) == expected
        assert git("log", "-1", "--format=%G?", repo=repo) == "G"
        assert not git("status", "--porcelain", repo=repo)
    assert not git("diff", SNAPSHOT, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (19008, L.name, "running")
    assert not r.absent(19008)
    processes()
    rec = load(V / "batch-098-reconciliation.json")
    evidence = load(S / "execution-720.json")
    assert sha(V / "batch-098-reconciliation.json") == evidence["reconciliationSha256"]
    for name, expected in {**rec["reviewedRuntimeHashes"], **evidence["recipeHashes"]}.items():
        assert sha(R / name) == expected
    for info in evidence["checks"].values():
        assert sha(R / info["path"]) == info["sha256"]
    return head, rec


def seal():
    head, rec = verify_signed()
    original = load(L / "progress-before-720.json")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (719, "098")
    cp = {
        "schemaVersion": 1, "execution": 720, "checkpoint": 720, "batch": "098",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "evidence": "docs/n1-sources/execution-720.json",
        "sourcePacket": "docs/n1-sources/batch-098-progress.json",
        "reconciliation": "docs/n1-reviews/batch-098-reconciliation.json",
        "textualReviewClosed": True, "runtimeDrafted": ["剤"], "reviewClosed": [], "published": [],
        "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionCoverageSupplements": 0, "serialReviewerExitAndScopeReverified": True,
        "bothProcessesExactFullPacketReturnedFirstCall": True,
        "eachProcessUnnecessarilyRereadOneSerialTail": True,
        "actionableRemainingTextualFindings": 0, "teachingChanged": False,
        "completeDictionaryFamilies": 352, "familyOccurrences": 354,
        "completeRawCharacterRecords": 8, "coordinatorOnlySupplementalRawRecords": 2,
        "metadataReadings": 5, "sourceOnlyReadings": 4, "curatedOfferedKeys": 1,
        "newSupportArticles": 0, "changedReusedArticles": 2,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairsAppliedInDraft": 0, "generatedStrokePaths": 10,
        "actualHanCount": 19, "pendingNativeFallbackLabels": ["刂", "氵"],
        "contentVersion": "0cbdc2723b0433f2", "allRuntimePayloadHashesVerified": 8449,
        "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 124, "remainingAdditions": 1104,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT}
    p.update(checkpoint=720, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution720CoordinatorCheckpoint"] = cp
    p["batch098TextualReviewCheckpoint"] = copy.deepcopy(cp)
    p["execution720StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-098-textual-720-seal.json", cp)
    save(L / "checkpoint-720.json", cp)
    print("Verified signed clean checkpoint720:", head)


def issue_body():
    head, rec = verify_signed()
    body = (
        f"Batch098 (剤) — two-family TEXTUAL review closed at normally signed LOCAL checkpoint720 "
        f"`{head}` (signature G). Not Android/native acceptance, publication or project completion.\n\n"
        f"Same frozen draft `{SNAPSHOT}` reviewed serially by actual Claude Opus5.5 "
        "(`claude-opus-5.5`, sessiond41cdccb-18bc-4302-803f-803d7bd4a007), then GPT6.1Sol "
        "(`gpt-6.1-sol`, session33216339-ddd8-411a-8aca-b73da1a3bae7). Identical packet291277bytes/"
        "7905lines covered352 distinct complete dictionary families/354occurrences, eight raw records "
        "and16complete article bodies, including complete new剤 and exact reused洗剤/洗 navigation "
        "changes. Each isolated view-only process returned its exact whole packet first call, then "
        "unnecessarily reread one overlapping tail serially (Claude7880-EOF; GPT7800-EOF); no tool "
        "overlap/truncation/missinglines/unfinishedtool. Actual reviewer exit before next launch "
        "verified. Original full reports/models/sessions/executions/coverage retained in "
        "docs/n1-reviews/batch-098-*. Returned bytes do not certify comprehension or independent "
        "upstream retrieval; Claude did not independently recount336families.\n\n"
        "New article and both bounded reused passages: correctness, scoped coverage and phone-TEXT "
        "comprehensibility CLEAN in scope; no actionable textual defect or consequential unresolved "
        "teaching claim. Teaching unchanged, so no dependent textual fix confirmation needed; original "
        "sessions retained for later rendered confirmation. Optional shape orientation/source-only "
        "gloss not adopted. Wider/custom/random/legacy fallback overlap remains a runtime gate, "
        "NOT certified safe. Coordinator confirms 刈る/刀 targets, preservedN2metadata, ten supplied "
        "paths and baselineactivation1; full supplemental frozen製/推 records support comparative "
        "セイ/スイ allocation, not a fresh independent reviewer lookup. Original inconsistent "
        "missing-path limitation is preserved rather than rewritten.\n\n"
        "Fullザイ/スイ/セイ andかる/けず.る retained in source order; onlyquizOnyomi[ザイ], "
        "quizKunyomi[] selected. Four separately qualified source-only rows; no invented spelling, "
        "invalidity/obsolescence claim, phonetic history or substring-reading allocation. Actual "
        "洗剤せんざい N2 support and originalせっけん exclusion unchanged; no new word/title/guard. "
        "TWO allmappedpairs/FOUR directions/ONE activatedbaselinepair. Ten generated strokes/"
        "all19Han unchanged;刂/氵cmap absence is NOT glyph failure.\n\n"
        "Fresh validator0, regenerated unchanged manifest0cbdc2723b0433f2,43focusedtests, exact "
        "batch audit, vocabularyconsistency, whitespace and original archivebudget checks passed; "
        "all8449 runtimepayloadhashes verified. Prior complete source/baseline/stroke/font audit "
        "retained as execution719, not relabelled as fresh linguistic inspection. Runtime bytes "
        "unchanged; only evidence/ledger local commit, no push.\n\n"
        "Next SAME098 fresh non-skipped THREE RealContentTest/ONE RareHanTest, production "
        "ContentSync ONCE/fullarchive/N1-All actual choices/ざい and NOkun/tenstroke drawing/"
        "articles/reusedlinks/SystemBack/offline/all19Han/fourfonts, then original-session rendered "
        "confirmations. Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest "
        "appmain. All combined-current-main/signing/ownerfastforward/terminalgreenCI/"
        "EVERYimmutableZIP runtime manifesthash/originalbudgets/verifiedownerissue gates remain.\n\n"
        "Published124/1228;1104 acceptance remainder unchanged. Physical-phone/general-release/"
        "whole-set outstanding. Compatible updated client required. No099, unreviewedpush, "
        "parent-lock manipulation, optional historical-session helper access, actual new permission "
        "denial or secondrunner. Full historicalprogress preserved; statuscontinue."
    )
    (C / "batch-098-textual-720-issue-body.txt").write_bytes(body.encode("utf-8"))


def receipt():
    verify_signed()
    posted = load(L / "issue-720-reread.json")
    body = (C / "batch-098-textual-720-issue-body.txt").read_bytes().decode("utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    p = load(C / "progress.json")
    original = load(L / "progress-before-720.json")
    assert (p["checkpoint"], p["status"], p["stage"]) == (720, "continue", STAGE)
    record = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "verified": True, "comparison": "Exact UTF-8 bytes."}
    p["batch098TextualReviewIssueReceipt"] = record
    for key in ["execution720CoordinatorCheckpoint", "batch098TextualReviewCheckpoint"]:
        p[key]["issueUpdate"] = record["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-098-textual-720-issue-receipt.json", record)
    save(L / "checkpoint-720.json", p["execution720CoordinatorCheckpoint"])
    assert load(C / "progress.json") == p
    print("Verified persisted checkpoint720, historical preservation and owner issue:", record["url"])


if __name__ == "__main__":
    {"prepare": prepare, "staged-whitespace": staged_whitespace, "seal": seal,
     "issue-body": issue_body, "receipt": receipt}[sys.argv[1]]()
