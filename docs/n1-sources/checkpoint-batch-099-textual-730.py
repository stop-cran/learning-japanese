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
spec = importlib.util.spec_from_file_location("batch099", C / "review-batch-099.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
r = m.review
R, A, S, V, L = r.R, r.A, r.S, r.V, r.L
load, sha, git = r.load, r.sha, r.git
SNAPSHOT = r.SNAPSHOT
STAGE = "batch-099-textual-review-closed-awaiting-android-native"
NEXT = (
    "SAME099 fresh non-skipped THREE RealContentTest and ONE RareHanTest against THIS sibling next; "
    "textual closure ONLY on signed70dfe334, NOT native or full batch acceptance. "
    "Actual ClaudeOpus5.5 original session2ac79fdb-83fc-485d-8f64-6c5d7b473973 and GPT6.1Sol "
    "original session240faa46-7797-4c93-998e-af5db5677c98 completed serial blind initial reviews "
    "on SAME174358byte/3598line packet:66distinct complete dictionary families/68occurrences, "
    "nine raw records,15complete articles including new剰 and exact reused過剰/過 navigation changes. "
    "Both returned exact full packet in first serial view; Claude exactly ONEcall; GPT unnecessarily "
    "reread3400-3598 serially. No tool overlap/truncation/missinglines. Original complete "
    "reports/models/sessions/process/read limits archived. No actionable textual defect or "
    "consequential unresolved teaching claim; teaching unchanged, no dependent textual fix confirmation "
    "needed. Optional namedcharacterdictionary/newcitation/historicalclassification not adopted. "
    "Coordinator confirms ELEVEN suppliedSVG/generated paths, source membership and preserved N2metadata; "
    "original Claude inconsistent tenfiles/missingpaths limitation and overbroad unselectedreadings "
    "paraphrase preserved and corrected in reconciliation, not rewritten. Fullジョウ and "
    "あまつさえ/あま.り/あま.る retained; only quizOnyomi[ジョウ], quizKunyomi[] selected. "
    "Three separate kun rows distinguish rare-spelling dated usually-kana剰え, search-only剰り "
    "with nounあまり notあんまり, character-dictionaryあま.る with ordinary余る, no invented剰る. "
    "One existing過剰かじょう N2 support, originalSEVENexclusions unchanged; no new word/title/guard. "
    "TWO allmappedpairs/FOUR directions/ONE activatedbaselinepair. Use explicit "
    "JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot and "
    "ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, oneGradleworker and quoted "
    "'-Pkotlin.compiler.execution.strategy=in-process'; inspect terminal test cases and actual sibling path. "
    "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest appmain. Then fresh fullarchive "
    "productionContentSync ONCE/native N1-All actual choices/じょう only and NO kun/elevenstroke drawing/"
    "complete剰 article/reused過剰-過 links/SystemBack/offline/all12Han/fourfonts with fresh safe "
    "port/device ownership checks; 刂/older剩cmap absences NOT glyph failure. Preserve exact fixture/hash "
    "and terminal percase0, no doubleparse, heap/archiveguard increase or shared-device interference. "
    "Original two model sessions need serial bounded rendered confirmations; current textual review "
    "certifies neither native/phone nor widercustom/random/fallback pools. All combined-current-main/"
    "nonrewritingmerge/changedteachingreview/checks/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutableZIPmanifestentryhash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/"
    "media/path/verifiedownerissue gates remain. Parent15692 retains runner.lock throughout child lifetime; "
    "NO child acquire/delete/unlock/readprobe. Approved control/committed evidence/frozen inputs only, "
    "no optional historical-session helper access. Preserve/report/yield actual new denial/signing hang/"
    "uncertain ownership. Published125/1228 and1103 acceptance remainder unchanged; six separate earlier "
    "placements not counted as accepted batches. Physicalphone/generalrelease/whole-set outstanding. "
    "No100, unreviewedpush or secondrunner."
)


def save(path, value):
    temp = path.with_suffix(path.suffix + ".730.tmp")
    assert not temp.exists()
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def processes():
    records, previous = {}, None
    for label, model in r.MODELS.items():
        prefix = f"batch-099-initial-{label}"
        record = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert record["snapshot"] == SNAPSHOT
        assert record["exitCode"] == 0 and record["actualModels"] == [model]
        assert record["usageCurrentModel"] == model
        assert record["availableTools"] == ["view"] and "--available-tools=view" in record["command"]
        assert record["multiToolResponseCount"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert coverage["allAssignedRangesReturned"]
        assert len(record["toolCalls"]) == (1 if label == "claude" else 2)
        first = record["toolCalls"][0]
        assert first["arguments"] == {"path": str(r.PACKET), "forceReadLargeFiles": True}
        if label == "gpt":
            assert record["toolCalls"][1]["arguments"] == {
                "path": str(r.PACKET), "view_range": [3400, 3598]}
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
            "toolCalls": len(record["toolCalls"]), "observedToolOverlaps": 0,
            "exactFullPacketReturnedInFirstCall": True,
            "unnecessarySerialTailReread": None if label == "claude" else [3400, 3598],
            "limits": "Actual complete returned bytes/ranges verified, not comprehension certification.",
        }
    return records


def prepare():
    r.frozen()
    records = processes()
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert r.PACKET.read_bytes() == (V / r.PACKET.name).read_bytes()
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (729, "099")
    ledger = load(S / "batch-099-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    assert ledger["reviewClosed"] == ledger["published"] == []
    receipts = {}
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "099"],
        "tests": [sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
                  "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources"],
        "vocabulary": [sys.executable, "-B", str(R / "tools" / "grammar_vocabulary.py"), "check"],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
        "whitespace": ["git", "--no-pager", "diff", "--check"],
    }
    for name, command in commands.items():
        path = V / f"batch-099-textual-review-{name}-730.txt.gz"
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

    mechanical = audit(R, "099")
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    assert manifest["contentVersion"] == "5408632b5aa1382c"
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8451
    provenance = load(V / "batch-099-review-dictionary-provenance.json")
    for source in provenance["sources"]:
        assert sha(Path(source["path"])) == source["sha256"]
    pairs = ledger["allMappedReciprocalPairs"]
    assert len(pairs) == 2
    for char, word in pairs:
        assert "(../" + word + ")" in (R / "kanji" / (char + ".md")).read_text(encoding="utf-8")
        assert "(../kanji/" + char + ".md)" in (R / word).read_text(encoding="utf-8")
    svg = ET.parse(S / "batch-099-kanjivg.svg").getroot()
    paths = svg.findall(".//{http://www.w3.org/2000/svg}path")
    stroke = load(R / "strokes" / "剰.json")
    assert len(paths) == len(stroke["strokes"]) == stroke["strokeCount"] == 11
    assert [s["id"] for s in stroke["strokes"]] == list(range(1, 12))
    stroke_audit = load(S / "batch-099-draft-stroke-audit.json")
    assert stroke_audit["geometryExactlyRegenerated"]
    assert sha(S / "batch-099-kanjivg.svg") == stroke_audit["sha256"]
    assert sha(R / stroke_audit["output"]) == stroke_audit["outputSha256"]
    named = C / "inputs" / "n1-kanji-source-20261102.json"
    assert sha(named) == "889faaefbec573e806f298766d2eee1300674c7b229bd973a35169cd2652cd73"
    assert "剰" in load(named)
    targets = ["words/余る.md", "kanji/刀.md", "kanji/乗.md", "kanji/剣.md", "kanji/則.md"]
    assert all((R / name).is_file() for name in targets)
    reviewed = {name: sha(R / name) for name in [
        "kanji/剰.md", "words/過剰.md", "kanji/過.md", "strokes/剰.json", "manifest.json"]}
    limits = [
        "TEXTUAL closure only, NOT full batch review closure, runtime acceptance or publication; reviewClosed/published arrays remain empty.",
        "Both original reports/executions preserved. Each process returned its exact entire assigned packet in first call; Claude used exactly one call, GPT unnecessarily reread3400-3598 serially. No truncation/missinglines/overlap/unfinishedtool. Actual exit before next reviewer verified; returned bytes do not certify comprehension.",
        "Both initial reviewers received the same66-family packet and exact two reused diffs, independently of other findings or author adjudication. Source counts mechanically verified; public text is coordinator-supplied committed extraction, not independent upstream retrieval.",
        "Runtime and all8451 payload hashes unchanged; prior complete source/baseline/stroke/font audit is execution729, not relabelled as fresh full linguistic inspection.",
        "Default-four three kanjichoices accepted textually. Actual N1/All and widercustom/random/legacy fallback pools remain runtime gates, not certified. Old APKs ignore curation.",
        "Claude's original tenfiles/missing-eleven-paths limitation is inconsistent with supplied complete SVG/JSON. Coordinator freshly counts11 SVGpaths/11 numberedgeneratedrecords and rebinds exact prior regeneration audit; GPT explicitly inspected11. Original report preserved, not rebranded as uniform independent verification.",
        "Claude overbroad paraphrase of line35 ('unselected readings are not rare or invalid') is not the actual claim. Actual text limits this to ordinaryあまり/あまる and separately marks剰えrare/dated; both reports retain the correct distinction elsewhere. No teaching defect established.",
        "N1 named-source membership freshly confirmed from exact frozen bytes; N2 vocabulary metadata preserved, not a new inference or fresh source verification. No physicalphone or native evidence from textual review.",
        "Fresh Android/RareHan/native/fourfonts/drawing/reading/N1-All/Back/offline/ContentSyncONCE and dependent original-session rendered review remain pending.",
        "Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latestappmain. Compatibleclientf9b59a2+ required; physicalphone/generalrelease/whole-set outstanding.",
        "Published125/1228 and1103 acceptance remainder unchanged; six separate earlierN2source members保案派第策結 and separate妖exception retained. No100 or project completion.",
        "All original combined-main/signing/ownerpush/terminalCI/EVERYimmutableZIPhash/originalbudgets/ownerissue gates remain. Parent lock untouched, no optional historical helper access or new permission denial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 730, "batch": "099", "status": STAGE,
        "originalTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "teachingChangedAfterInitialReviews": False, "reviewedRuntimeHashes": reviewed,
        "initialModels": list(r.MODELS.values()), "processes": records,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": r.PACKET.stat().st_size,
        "initialPacketLines": len(r.PACKET.read_text(encoding="utf-8").splitlines()),
        "distinctCompleteFamilies": 66, "familyOccurrences": 68, "rawCharacterRecords": 9,
        "completeArticleBodies": 15, "newArticleBodies": 1, "changedReusedPassages": 2,
        "verdicts": {
            name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
            for name in ["kanji/剰.md:1-51", "words/過剰.md:25", "kanji/過.md:41"]},
        "findings": [],
        "optionalDispositions": [
            {"reportedBy": "Claude", "claim": "Name the character dictionary in line33.",
             "status": "optional", "decision": "No edit. Explicit dictionary links and actual heading already given in source line; source-only qualification is clear."},
            {"reportedBy": "Claude", "claim": "Add JMdict1196170 to reused過 source line.",
             "status": "optional", "decision": "No edit. Existing navigation-only change with linked actual過剰article already carrying exact dictionary entry. No broken or false source claim established."},
            {"reportedBy": "Claude; equivalent GPT shape assessment", "claim": "Phonetic classification could be added.",
             "status": "optional", "decision": "No edit. Explicit mnemonic and structure-unclassified make no false denial. Undecoded historical gaiji and SVGtags not treated as sufficient to expand historical teaching."}],
        "hypothesisDispositions": [
            {"reportedBy": "Claude; equivalent GPT runtime limit", "claim": "余 surplus meaning or shared乗ジョウ might appear in wider fallback/reading pools.",
             "status": "unresolved", "severity": "runtime gate, not a current default-four teaching defect",
             "decision": "Three authored semantically wrong choices cover default four; full metadata remains wrong-option protected by compatible client. Actual N1/All and wider/custom/random/legacy fallback remain runtime gates, not certified or waived."},
            {"reportedBy": "Both", "claim": "Older APKs ignore curation.",
             "status": "resolved", "decision": "Known compatibility requirement retained. Updatedf9b59a2+ client required; not waived by this textual checkpoint."}],
        "reviewLimitDispositions": [
            {"reportedBy": "Claude", "claim": "Could not map eleven paths; saw ten source/generated files.",
             "status": "resolved", "decision": "No teaching edit. Complete SVGandJSON were actually supplied. Coordinator counts11 numberedpaths/11 generatedstrokes and verifies exact prior regeneration evidence/hashes. GPT explicitly inspected11. Preserve original inconsistent Claude limit; no uniform-depth/native drawing claim.",
             "svgPaths": len(paths), "generatedStrokes": len(stroke["strokes"]),
             "priorStrokeAudit": "docs/n1-sources/batch-099-draft-stroke-audit.json",
             "priorStrokeAuditSha256": sha(S / "batch-099-draft-stroke-audit.json")},
            {"reportedBy": "Claude", "claim": "No level-source evidence in packet.",
             "status": "resolved", "decision": "Coordinator confirms剰membership in exact hash-verified frozen N1namedset. N2label is preserved baseline metadata, not newly inferred or re-sourced. Initial reviewer evidence limitation remains honest.",
             "frozenNamedSourceSha256": sha(named)},
            {"reportedBy": "Claude", "claim": "Line35 says unselected readings are not rare.",
             "status": "withdrawn", "decision": "Overbroad reviewer paraphrase, not actual teaching. Actual sentence says ordinaryあまり/あまる are not made rare/invalid by exclusion; line31 explicitly qualifies剰えas rare/dated. Both reports otherwise recognize this distinction.",
             "actualText": (R / "kanji" / "剰.md").read_text(encoding="utf-8").splitlines()[34]},
            {"reportedBy": "Both", "claim": "No manifest, archive, actual UI/native/font/phone verification in textual packet.",
             "status": "unresolved", "decision": "Not textual evidence. Coordinator reverified all8451currentpayloadhashes; all fresh native/Android/publication/immutableZIP and phone distinctions remain explicit pending gates, not reviewer certification."}],
        "modelContributionComparison": {
            "shared": "Both assessed surplus/remainder boundmeaning, actual過剰 identity/examples/translations and seven exclusions, allfour readings and source-only/spelling/register restrictions, allocation/curation, shape/mnemonic/strokes, allfourlinks/twoboundedreusedchanges, preservedN2metadata, threewronglabels and runtime/upstream/native limits. Equivalent differently labelled observations count as shared.",
            "claudeUniqueVerifiedUseful": [], "gptUniqueVerifiedUseful": [],
            "claudeUniqueNonblocking": "Named-dictionary/additionalcitation/historicalclassification options; inconsistent missingpath count and overbroad line35 paraphrase preserved and adjudicated.",
            "gptUniqueNonblocking": "Explicit independent report assertion of11paths; coordinator and original supplied files support it, not evidence of fresh upstream retrieval.",
            "unsupportedMandatorySuggestions": "No mandatory textual fix, extra source-only lexical example, historical classification, new support article or exclusion established.",
            "limits": "Matched sample/source access, not general model benchmark, equal-depth comprehension certification or native-speaker review."},
        "actionableRemainingTextualFindingGroups": 0, "consequentialUnresolvedTeachingClaims": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "dependentTextualConfirmation": "Not needed: no teaching edit or established textual defect. Original sessions retained for required later rendered confirmation.",
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "previousCompleteSourceBaselineFontStrokeAudit": "docs/n1-sources/batch-099-draft-audit.json",
        "previousCompleteSourceBaselineFontStrokeAuditSha256": sha(S / "batch-099-draft-audit.json"),
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 1,
        "linkTargetsVerified": {name: sha(R / name) for name in targets},
        "newDirectWordExclusionPairsAppliedInDraft": 0,
        "actualHanCount": 12, "nativeFontPending": ["刂", "剩"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "freshAndroidOrNativeClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    save(V / "batch-099-reconciliation.json", rec)
    ledger["initialDraftLimits"] = copy.deepcopy(ledger["limits"])
    ledger.update(status=STAGE, initialReviewSnapshot=SNAPSHOT, reviewedTeachingSnapshot=SNAPSHOT,
                  textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False, nextAction=NEXT)
    ledger["limits"][0] = limits[0]
    ledger["independentReviewersLaunched"] = 2
    ledger["quizAudit"]["剰"]["limits"] = "Default-four textually accepted; actual production N1/All and wider-pool review pending."
    ledger["textualReview"] = {
        "snapshot": SNAPSHOT, "models": rec["initialModels"],
        "reconciliation": "docs/n1-reviews/batch-099-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-099-reconciliation.json"),
        "teachingChanged": False, "textualReviewClosed": True,
        "actionableRemainingTextualFindings": 0, "runtimeAccepted": False}
    ledger["pendingGates"] = [
        "Fresh non-skipped THREE RealContentTest/ONE RareHanTest against actual sibling.",
        "Full productionContentSyncONCE/native N1-All choices/じょう and NOkun/elevenstroke drawing/articles/reusedlinks/Back/offline/all12Han/fourfonts; dependent original-session rendered confirmations.",
        "Combined-current-main integration, changed teaching re-review if needed, all checks/normal signing/owner fastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/originalbudgets/verifiedownerissue."]
    for row in ledger["supportMappings"]:
        row["status"] = "textual-review-closed-awaiting-android-native"
    save(S / "batch-099-progress.json", ledger)
    membership = load(S / "batch-099-membership.json")
    membership["initialDraftLimits"] = copy.deepcopy(membership["limits"])
    membership.update(status=STAGE, initialReviewSnapshot=SNAPSHOT,
                      textualReviewClosed=True, runtimeAccepted=False, runtimePublished=False)
    membership["limits"] = limits[0]
    save(S / "batch-099-membership.json", membership)
    recipe = S / Path(__file__).name
    shutil.copyfile(Path(__file__), recipe)
    shutil.copyfile(C / "preflight-730.ps1", S / "batch-099-textual-preflight-730.ps1.txt")
    save(S / "execution-730.json", {
        "schemaVersion": 1, "execution": 730, "batch": "099", "status": STAGE,
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "startingState": p["execution730StartingState"],
        "reconciliation": "docs/n1-reviews/batch-099-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-099-reconciliation.json"),
        "recipeHashes": {path.relative_to(R).as_posix(): sha(path) for path in [
            recipe, V / "review-batch-099.py", V / "batch-099-serial-review-base-recipe.py",
            S / "batch-099-textual-preflight-730.ps1.txt"]},
        "checks": receipts, "runtimeBytesChanged": False,
        "publishedAdditions": 125, "remainingAdditions": 1103,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT})
    assert not git("diff", SNAPSHOT, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    print("SAME099 two-family TEXTUAL closure saved; Android/native/publication remain.", flush=True)


def staged_whitespace():
    captures = [
        "docs/n1-reviews/batch-099-cli-config-help-execution-730.txt",
        "docs/n1-reviews/batch-099-initial-packet.txt",
    ]
    command = ["git", "--no-pager", "diff", "--cached", "--check"]
    original = subprocess.run(command, cwd=R, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    names = {line.split(":", 1)[0] for line in original.stdout.decode("utf-8").splitlines()
             if line.startswith("docs/")}
    assert original.returncode in (0, 2)
    assert names.issubset(captures), names
    original_log = V / "batch-099-lossless-capture-whitespace-730.txt.gz"
    original_log.write_bytes(gzip.compress(original.stdout, mtime=0))
    exclusions = [":(exclude)" + name.replace("/", "\\") for name in sorted(names)]
    scoped = subprocess.run(command + ["--", ".", *exclusions], cwd=R,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert scoped.returncode == 0, scoped.stdout.decode("utf-8", errors="replace")
    scoped_log = V / "batch-099-staged-authored-whitespace-730.txt.gz"
    scoped_log.write_bytes(gzip.compress(scoped.stdout, mtime=0))
    rec = load(V / "batch-099-reconciliation.json")
    rec["checks"]["staged-authored-whitespace"] = {
        "path": scoped_log.relative_to(R).as_posix(), "sha256": sha(scoped_log),
        "uncompressedSha256": hashlib.sha256(scoped.stdout).hexdigest(),
    }
    rec["whitespaceDiagnostic"] = {
        "initialStagedCheckExitCode": original.returncode,
        "initialLog": original_log.relative_to(R).as_posix(), "initialLogSha256": sha(original_log),
        "exactLosslessCaptureExceptions": {name: sha(R / name) for name in sorted(names)},
        "disposition": "Preserve exact original reviewer packet and actual CLI help bytes. Authored files pass exact-path scoped check; no report/hash/runtime content edited.",
        "scopedCommand": command + ["--", ".", *exclusions],
    }
    save(V / "batch-099-reconciliation.json", rec)
    ledger = load(S / "batch-099-progress.json")
    ledger["textualReview"]["reconciliationSha256"] = sha(V / "batch-099-reconciliation.json")
    save(S / "batch-099-progress.json", ledger)
    recipe = S / Path(__file__).name
    shutil.copyfile(Path(__file__), recipe)
    evidence = load(S / "execution-730.json")
    evidence["reconciliationSha256"] = sha(V / "batch-099-reconciliation.json")
    evidence["checks"] = rec["checks"]
    evidence["whitespaceDiagnostic"] = rec["whitespaceDiagnostic"]
    evidence["recipeHashes"][recipe.relative_to(R).as_posix()] = sha(recipe)
    save(S / "execution-730.json", evidence)
    print("Staged authored whitespace passed; lossless capture exceptions:", sorted(names))


def verify_signed():
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == SNAPSHOT
    for repo, expected in [(R, head), (A, r.ANDROID)]:
        assert git("rev-parse", "HEAD", repo=repo) == expected
        assert git("log", "-1", "--format=%G?", repo=repo) == "G"
        assert not git("status", "--porcelain", repo=repo)
    assert not git("diff", SNAPSHOT, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runner = load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (15692, L.name, "running")
    assert not r.absent(15692)
    processes()
    rec = load(V / "batch-099-reconciliation.json")
    evidence = load(S / "execution-730.json")
    assert sha(V / "batch-099-reconciliation.json") == evidence["reconciliationSha256"]
    for name, expected in {**rec["reviewedRuntimeHashes"], **evidence["recipeHashes"]}.items():
        assert sha(R / name) == expected
    for info in evidence["checks"].values():
        assert sha(R / info["path"]) == info["sha256"]
    return head, rec


def seal():
    head, rec = verify_signed()
    original = load(L / "progress-before-730.json")
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"]) == (729, "099")
    cp = {
        "schemaVersion": 1, "execution": 730, "checkpoint": 730, "batch": "099",
        "status": "continue", "stage": STAGE, "savedCommit": head, "signature": "G",
        "initialTeachingSnapshot": SNAPSHOT, "reviewedTeachingSnapshot": SNAPSHOT,
        "lastPublishedCommit": p["lastPublishedCommit"],
        "evidence": "docs/n1-sources/execution-730.json",
        "sourcePacket": "docs/n1-sources/batch-099-progress.json",
        "reconciliation": "docs/n1-reviews/batch-099-reconciliation.json",
        "textualReviewClosed": True, "runtimeDrafted": ["剰"], "reviewClosed": [], "published": [],
        "runtimeAccepted": False, "runtimePublished": False,
        "initialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionCoverageSupplements": 0, "serialReviewerExitAndScopeReverified": True,
        "bothProcessesExactFullPacketReturnedFirstCall": True,
        "claudeOneCall": True, "gptUnnecessarySerialTailReread": [3400, 3598],
        "actionableRemainingTextualFindings": 0, "teachingChanged": False,
        "completeDictionaryFamilies": 66, "familyOccurrences": 68,
        "completeRawCharacterRecords": 9, "completeArticleBodies": 15,
        "metadataReadings": 4, "sourceOnlyReadings": 2, "unselectedRecognitionReadings": 1,
        "curatedOfferedKeys": 1, "newSupportArticles": 0, "changedReusedArticles": 2,
        "allMappedReciprocalPairs": 2, "directedLinksVerified": 4, "activatedBaselinePairs": 1,
        "newDirectWordExclusionPairsAppliedInDraft": 0, "generatedStrokePaths": 11,
        "actualHanCount": 12, "pendingNativeFallbackLabels": ["刂", "剩"],
        "contentVersion": "5408632b5aa1382c", "allRuntimePayloadHashesVerified": 8451,
        "pythonTestsPassed": 43, "validatorErrors": 0,
        "dedicatedWorktreesClean": True, "runtimeBytesUnchanged": True,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 125, "remainingAdditions": 1103,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalHelpersAccessed": False,
        "actualNewPermissionDenials": [], "originalHistoricalRootKeysCompared": len(original),
        "allOriginalHistoricalValuesPreserved": True, "nextAction": NEXT}
    p.update(checkpoint=730, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    p["execution730CoordinatorCheckpoint"] = cp
    p["batch099TextualReviewCheckpoint"] = copy.deepcopy(cp)
    p["execution730StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(C / "batch-099-textual-730-seal.json", cp)
    save(L / "checkpoint-730.json", cp)
    print("Verified signed clean checkpoint730:", head)


def issue_body():
    head, rec = verify_signed()
    body = (
        f"Batch099 (剰) — two-family TEXTUAL review closed at normally signed LOCAL checkpoint730 "
        f"`{head}` (signature G). Not Android/native acceptance, publication or project completion.\n\n"
        f"Same frozen draft `{SNAPSHOT}` reviewed serially by actual Claude Opus5.5 "
        "(`claude-opus-5.5`, session2ac79fdb-83fc-485d-8f64-6c5d7b473973), then GPT6.1Sol "
        "(`gpt-6.1-sol`, session240faa46-7797-4c93-998e-af5db5677c98). Identical packet174358bytes/"
        "3598lines covered66 distinct complete dictionary families/68occurrences, nine raw records "
        "and15complete article bodies, including complete new剰 and exact reused過剰/過 navigation "
        "changes. Each isolated view-only process returned its exact whole packet first call: "
        "Claude exactlyONEcall; GPT unnecessarily reread3400-3598 serially. No tool overlap/"
        "truncation/missinglines/unfinishedtool. Actual reviewer exit before next launch verified. "
        "Original full reports/models/sessions/executions/coverage retained in docs/n1-reviews/"
        "batch-099-*. Returned bytes do not certify comprehension or independent upstream retrieval.\n\n"
        "New article and both bounded reused passages: correctness, scoped coverage and phone-TEXT "
        "comprehensibility CLEAN in scope; no actionable textual defect or consequential unresolved "
        "teaching claim. Teaching unchanged; no dependent textual fix confirmation needed. Original "
        "sessions retained for later rendered confirmation. Optional named-dictionary/citation/"
        "historical-classification expansions not adopted. Coordinator confirms11SVGpaths/"
        "11generatedrecords; original Claude inconsistent tenfiles/missingpaths limit and overbroad "
        "line35 paraphrase preserved and adjudicated, not rewritten. N1membership freshly verified "
        "against exact frozenbytes; N2metadata preserved, not newly inferred or re-sourced. "
        "Wider/custom/random/legacy fallback overlap remains a runtime gate, NOT certified safe.\n\n"
        "Fullジョウ andあまつさえ/あま.り/あま.る retained in source order; onlyquizOnyomi[ジョウ], "
        "quizKunyomi[] selected. Three separate kun rows distinguish rare-spelling dated usually-kana "
        "剰え, search-only剰り (nounあまり,notあんまり) and character-dictionaryあま.る with ordinary "
        "余る spelling, no invented剰る. Actual過剰かじょう N2 support and originalSEVENexclusions "
        "unchanged; no new word/title/guard. TWO allmappedpairs/FOUR directions/ONE activatedbaselinepair. "
        "Eleven generatedstrokes/all12Han unchanged;刂/older剩cmap absence is NOT glyph failure.\n\n"
        "Fresh validator0, regenerated unchanged manifest5408632b5aa1382c,43focusedtests, exact "
        "batch audit, vocabularyconsistency, whitespace and original archivebudget checks passed; "
        "all8451runtimepayloadhashes verified. Prior complete source/baseline/stroke/font audit "
        "retained as execution729, not relabelled as fresh linguistic inspection. Runtime bytes "
        "unchanged; both dedicated worktrees clean and normally signed. No push or nextbatch.\n\n"
        "Next SAME099: fresh non-skipped THREE RealContentTest/ONE RareHanTest, then fullarchive "
        "productionContentSyncONCE/native N1-All/meaning/じょうonly-NOkun/elevenstroke drawing/"
        "articles/Back/offline/all12Han/fourfonts and both original-session serial rendered "
        "confirmations. Qualified TESTONLY Android1c1b7bf4 retains productionf9b59a2, NOT latest "
        "appmain. All combined-current-main/signing/ownerfastforward/terminalgreenCI/"
        "EVERYimmutableZIPmanifesthash/original18000entry42MiBcompressed80MiBinflated56MiBretained/"
        "per-file/path/media/verifiedownerissue gates remain. Parent15692 lock untouched; approved "
        "control/committed/frozen inputs only, no optional historical-session helpers or new denial. "
        "Published125/1228,1103 acceptance remainder unchanged; six separate earlier placements "
        "not counted as accepted batches. Physical-phone/general-release/whole-set acceptance "
        "explicitly outstanding; compatible curated-reading APKf9b59a2+ required."
    )
    (C / "batch-099-textual-730-issue-body.txt").write_text(body, encoding="utf-8")


def attach_issue():
    head, _ = verify_signed()
    posted = load(L / "issue-730-reread.json")
    body = (C / "batch-099-textual-730-issue-body.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body
    receipt = {"id": posted["id"], "url": posted["html_url"], "author": "stop-cran",
               "bodySha256": hashlib.sha256(body.encode("utf-8")).hexdigest(), "verified": True}
    save(C / "batch-099-textual-730-issue-receipt.json", receipt)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (730, "099", "continue")
    assert p["execution730CoordinatorCheckpoint"]["savedCommit"] == head
    for key in ["execution730CoordinatorCheckpoint", "batch099TextualReviewCheckpoint"]:
        p[key]["issueUpdate"] = receipt["url"]
        p[key]["ownerIssueAuthorAndBodyVerified"] = True
    p["batch099TextualReviewIssueReceipt"] = receipt
    original = load(L / "progress-before-730.json")
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in original.items() if k not in allowed)
    save(C / "progress.json", p)
    save(L / "checkpoint-730.json", p["execution730CoordinatorCheckpoint"])
    print(receipt["url"])
    print("Full historical progress preserved; SAME099 next gate Android; project incomplete.")


if __name__ == "__main__":
    {"prepare": prepare, "whitespace": staged_whitespace, "seal": seal,
     "issue-body": issue_body, "attach-issue": attach_issue}[sys.argv[1]]()
