"""Preserve original reviews, a minimal correction and the resumable checkpoint."""
import ast
import gzip
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "d195583f-f80d-422a-9401-2a01567f444d"
INITIAL = "2a296c3f1cadca725b80274f7e312773f4c18ca8"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
MAIN = "a38f4cf554300ce34ee65aada79e87b7c9d0319e"
REVISED = "08e76c1688ada4898a79e25e13650687dadf65d1"
STAGE = "batch-103-textual-review-closed-runtime-acceptance-pending"
NEXT = (
    "SAME103 fresh qualifiedAndroidbf30cdead HOST acceptance checkpoint: non-skipped RealContentTest/"
    "RareHanTest plus actual production meaning-builder defaultN1/All/custom-pool choices and direct "
    "symmetric NONTRANSITIVE guards. Two blind different-family initial TEXTUAL reviews complete on "
    "signed2a296c3f; original-session confirmations accept the minimal English translation clarification "
    "in 激励, all other teaching/metadata unchanged. Preserve complete original reports, actual model/"
    "session/read/process evidence and dependent confirmations. Packet267532bytes/5542lines/"
    "47member+31comparison=78completefamilies/11rawcharacters/38articlebodies/FOURpublicdictionarytexts. "
    "Both initial full packets returned exactly; GPT additionally made three serial overlapping tail "
    "reads, first two truncated; no missing scope/overlap. Byte access/self-report is not exhaustive "
    "sense-by-sense comprehension, equal depth or independent upstream retrieval. Three selected entries "
    "still TWO actual offered keys れい/はげむ; preserve onレイ/kunはげ.む,はげ.ます fullsourceorder/"
    "selections/ownrowlinks and sharedstemgrouping. Original786three-keyclaim remains corrected, not rewritten. "
    "Plain励ます versus polite励みます; activityに励む/personを励ます and passive roles explicit. "
    "Four directkanjiguards努勉勤支 and27directwordpairs accepted textually, not universal synonyms/"
    "cliques. Only劣 ofthree curatedwrong劣万厚 isN1; actual defaultN1fallback/All/custom options, reverse/"
    "pairwise exclusions and finite semantic optionset acceptance mandatory. Threeallmappedpairs/"
    "sixdirections/zeroactivatedbaselinepairs; reused応援慰める学問 navigation-only, easier levels/metadata/"
    "readings/exclusions unchanged; no inferred supportwordlevels. Actual47Han includes 厂U+5382 absent "
    "from allTHREEbundledcmaps, NOTglyphfailure/nativeaccepted. Require specific厂fallback/readability "
    "in allfourfonts/default plus all scopedHan and sevenstroke drawing. QualifiedAPP approvedguard+"
    "schemaonlybridges NOTunrelatedlatestmain. Then productionContentSyncONCE/nativeN1/All/meaning/"
    "curatedreading/drawing/article/Back/offline/fourfont/rendered acceptance, currentcontent/signedapp/"
    "ownedport-device checks/unchanged2gguest192mheap/oneworker/terminalcase0/cleanup. All original "
    "combinedcurrentmain/allrequiredPython/vocabulary/normalsigning/ownerfastforward/terminalgreenCI/"
    "EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed80MiBinflated56MiBretained/"
    "perfilepathmedia/verifiedownerissue gates remain before publication or104. Any new consequential "
    "teaching change requires exact evidence, minimal correction, audits/manifest/signedfreeze and BOTH "
    "originalsessionconfirmations. Verify whollyclean signedheads/freshmain/liveparentancestry/"
    "decodedlauncher/exactsession. Parent5920 ownsrunner.lock: no childacquire/delete/unlock/readprobe; "
    "approvedcontrol/committedsource/frozeninputs only, not optional historicalsessionrecipes. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership. No unreviewedpush/104/"
    "authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease. Published129/1228 and"
    "1099acceptance-remainder unchanged;1126kanji5077words includes unaccepted励/three supports, "
    "not deliveredN1vocabulary. Six separatelyplacedsource保案派第策結 retain earlierN2levels, "
    "not issue60acceptedadditions; neverduplicate/relevel. CompatibleAndroid#125+#132 required; "
    "oldclientsignore. Original102finite128optionset/40labelCLEANonlywithinsample/unrestrictedlivepool"
    "UNVERIFIED; original780ClaudeNONCOMPLIANT/UNACCEPTED immutable/781dependentsupplementNOT"
    "retroacceptance/782rescaledrenditionsNOToriginalpixels/equalcomprehension/nativespeaker retained. "
    "Original historical readdepth/image/process/permission/OOM/source-only/pending limits retained, "
    "not retroaccepted or freshly certified. Physicalphone/generalrelease/whole-setoutstanding; projectincomplete."
)


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    temporary = path.with_suffix(path.suffix + ".788.tmp")
    assert not temporary.exists()
    temporary.write_text(json.dumps(data, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == data
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def absent(pid):
    return subprocess.run(["pwsh", "-NoProfile", "-Command",
                           f"if (Get-Process -Id {pid} -ErrorAction SilentlyContinue) {{ exit 1 }}"],
                          capture_output=True).returncode == 0


def common():
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    assert not absent(5920)
    assert load(L / "preflight-788.json")["lockTouched"] is False
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (787, "103", "continue")


def archive(path):
    target = path.with_name(path.name + ".gz")
    if target.exists():
        assert not path.exists(), "Never replace an existing evidence archive"
        raw = gzip.decompress(target.read_bytes())
        original = C / path.name
        assert original.is_file() and original.read_bytes() == raw
        return {"rawName": path.name, "rawSha256": hashlib.sha256(raw).hexdigest(),
                "archive": target.name, "archiveSha256": sha(target), "losslessGzip": True}
    target.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
    assert gzip.decompress(target.read_bytes()) == path.read_bytes()
    receipt = {"rawName": path.name, "rawSha256": sha(path), "archive": target.name,
               "archiveSha256": sha(target), "losslessGzip": True}
    path.unlink()
    return receipt


def audit_runtime():
    sys.path.insert(0, str(R / "tools"))
    from build_manifest import build_manifest, sha256 as manifest_sha256
    from audit_n1_batch import audit as batch_audit
    current = load(R / "manifest.json")
    assert current == build_manifest(R)
    old = json.loads(subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "show", f"{INITIAL}:manifest.json"]))
    changed = []
    count = 0
    for section, entries in current.items():
        if not isinstance(entries, dict):
            continue
        assert set(entries) == set(old[section])
        for name, digest in entries.items():
            path = R / name
            actual = sha(path) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else manifest_sha256(path)
            assert actual == digest, name
            count += 1
            if old[section][name] != digest:
                changed.append(name)
    assert changed == ["words/激励.md"] and count == 8463
    assert current["contentVersion"] != old["contentVersion"]
    prior = subprocess.check_output(["git", "--no-pager", "-C", str(R), "show",
                                     f"{INITIAL}:words/激励.md"]).decode("utf-8").replace("\r\n", "\n")
    actual = (R / "words" / "激励.md").read_text(encoding="utf-8")
    assert actual == prior.replace("— Encourage the team.", "— They encourage the team.")
    assert prior.count("— Encourage the team.") == 1
    runtime = ["kanji", "words", "articles", "strokes", "manifest.json", "tools"]
    assert set(git("-c", "core.quotepath=false", "diff", "--name-only", INITIAL,
                   "--", *runtime).splitlines()) == {"words/激励.md", "manifest.json"}
    result = batch_audit(R, "103")
    assert result["dictionaryFamilies"] == 78 and result["curatedOfferedKeys"] == 2
    assert result["readingDispositions"] == 3 and result["requiredReciprocalPairs"] == 3
    return {"contentVersion": current["contentVersion"], "runtimeHashesVerified": count,
            "changedPayloadsSinceInitialReview": changed, "batchAudit": result,
            "allOtherRuntimeBytesPreserved": True,
            "onlyTeachingChange": "Explicit English statement 'They encourage the team.'; Japanese, kana, metadata, full source order and all guards unchanged.",
            "hanInventoryUnchanged": True, "actualHan": 47,
            "requiredNativeFallbackTarget": "厂 U+5382; absent from all three bundled cmaps, not a glyphfailure/readability result."}


def freeze():
    common()
    assert git("rev-parse", "HEAD") == INITIAL
    processes = {}
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        prefix = f"batch-103-initial-{label}"
        execution = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert execution["snapshot"] == coverage["snapshot"] == INITIAL
        assert execution["exitCode"] == 0 and execution["actualModels"] == [model]
        assert execution["usageCurrentModel"] == model and coverage["allAssignedRangesReturned"]
        assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
        assert execution["availableTools"] == ["view"] and execution["multiToolResponseCount"] == 0
        assert execution["toolCalls"][0]["exactRequestedTextContainedInResult"]
        assert not execution["toolCalls"][0]["truncationMarker"]
        assert all(t["name"] == "view" and t["arguments"]["path"] == str(C / "batch-103-initial-packet.txt")
                   for t in execution["toolCalls"])
        assert absent(execution["launcherPid"])
        assert sha(V / (prefix + ".md")) == execution["reportSha256"]
        raw_path = V / (prefix + ".jsonl")
        if not raw_path.exists():
            raw_path = C / (prefix + ".jsonl")
        assert sha(raw_path) == execution["rawExecutionSha256"]
        archived = archive(V / (prefix + ".jsonl"))
        processes[label] = {k: execution[k] for k in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
            "snapshot", "reportSha256", "rawExecutionSha256"]}
        processes[label].update(
            report=prefix + ".md", execution=prefix + "-execution.json",
            coverage=prefix + "-coverage.json", allAssignedRangesReturned=True,
            toolCalls=len(execution["toolCalls"]), observedToolOverlaps=0,
            exactFullPacketReturnedInFirstCall=True, losslessExecutionArchive=archived)
    assert processes["claude"]["completedAt"] < processes["gpt"]["startedAt"]
    required = load(V / "batch-103-required-review-ranges.json")[0]
    assert required["end"] == 5542 and sha(C / "batch-103-initial-packet.txt") == required["sha256"]
    runtime = audit_runtime()
    save(V / "batch-103-runtime-correction-audit-788.json", runtime)
    patch = subprocess.check_output(["git", "--no-pager", "-c", "core.quotepath=false",
                                     "diff", INITIAL, "--", "words/激励.md"], cwd=R)
    patch_path = V / "batch-103-translation-correction-788.patch.gz"
    patch_path.write_bytes(gzip.compress(patch, mtime=0))
    save(V / "batch-103-initial-reconciliation-788.json", {
        "schemaVersion": 1, "batch": "103", "execution": 788,
        "status": "minimal-translation-clarification-awaiting-original-session-confirmations",
        "originalTeachingSnapshot": INITIAL, "initialModels": ["claude-opus-5.5", "gpt-6.1-sol"],
        "processes": processes, "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 267532, "initialPacketLines": 5542,
        "completeFamiliesSupplied": 78, "rawCharacterRecordsSupplied": 11,
        "completeArticleBodies": 38, "newArticleBodies": 4, "changedReusedPassages": 3,
        "finding": {
            "id": "F1", "reviewer": "claude", "status": "partially resolved",
            "originalClassification": "Minor correctness; medium-high confidence",
            "coordinatorClassification": "Minor text-comprehensibility/translation ambiguity, not a categorical Japanese error",
            "location": "words/激励.md:17",
            "claim": "Bare English 'Encourage the team.' reads as an imperative while the Japanese dictionary example is presented as an ordinary plain-form model.",
            "preciseDisagreement": "GPT accepted the example as pedagogically natural; a dictionary-phrase translation can use an English bare infinitive. This is not a universal rule that Japanese plain forms cannot be directives. Explicit English declarative removes the local avoidable ambiguity without changing the source sentence.",
            "change": "They encourage the team.",
            "evidence": ["batch-103-gekirei-public-text.txt:4-5", "batch-103-jmdict.xml:4-25"],
            "remainingGate": "Both original-session changed-passage confirmation on one signed revised snapshot",
        },
        "hypotheses": [
            {"id": "H1", "reviewer": "claude", "status": "withdrawn",
             "claim": "自分が勉強に励む is slightly marked; が gives exhaustive focus.",
             "disposition": "No demonstrated defect. The explicit role contrast supplies focus; が need not universally mean exhaustive identification. GPT accepts this contrast. Do not rewrite natural contextual example or invent a general particle rule."},
            {"id": "H2", "reviewer": "claude", "status": "optional",
             "claim": "give a pep talk is not a JMdict gloss for 激励 itself.",
             "disposition": "No exact-dictionary-gloss identity claimed. Daijisenはげまして奮い立たせる supports the context-dependent encouragement paraphrase; encourage leads, and later text denies obligatory shouting/harshness. No evidence that this common encouragement use is false. Do not require every English paraphrase to be literally enumerated by JMdict."},
        ],
        "optional": [
            {"id": "O1", "reviewer": "claude", "status": "optional",
             "claim": "Use displayレイ rather than keyれい in card prose.",
             "disposition": "No edit. It describes actual question key and adjacent row already givesレイ; native label/key acceptance remains required."},
            {"id": "O2", "reviewer": "claude", "status": "optional",
             "claim": "Remove words/actions non-division in激励.",
             "disposition": "No edit; explicitly prevents treating practical応援 versus encouragement as rigid compartments."},
            {"id": "O3", "reviewer": "claude", "status": "optional",
             "claim": "Repeat励まない versus励まさない contrast.",
             "disposition": "No edit. Both exact negative forms and distinct verbs already taught; not a missing prerequisite."},
        ],
        "coordinatorEvidence": "Fresh four new articles, exact three reused diff, four complete archived public dictionary extracted blocks and full JMdict1253760/1557390/1557350/1907660 inspected. Other78-family/34comparison author source inspection inherited from786/787, not freshly claimed in full.",
        "runtime": runtime,
        "processDiagnostic": {
            "operation": "One optional live progress probe successfully found reviewerPID29872, then .NET File.ReadAllLines on the open redirected rawJSONL failed with IOException: file is being used by another process.",
            "disposition": "No live-log retry, alternate sharing mode, permission change, ACL change or policy bypass. Waited for normal reviewer termination; ordinary post-exit helper then archived complete original output. This was an open-writer sharing conflict, not an UnauthorizedAccess/permission-policy denial or missing mandatory source. Error preserved here; parent lock never touched.",
            "actualNewPermissionDenials": [],
        },
        "limits": [
            "Both first view responses contained exact full267532byte packet; access is not comprehension or equal semantic depth.",
            "GPT made three extra serial overlapping tail reads; first two truncated, last complete. Original report and raw ranges preserve this, no missing original scope.",
            "Claude explicitly did not assess input-metadata JSON or governing instruction text as review targets; teaching/source scope was inspected.",
            "No independent upstream/Git/signature verification, image-gaiji reconstruction, native/font/drawing/UI/phone acceptance or unrestricted live-pool guarantee.",
        ],
        "fullBatchAcceptanceComplete": False, "reviewClosed": [], "runtimePublished": False,
        "freshAndroidOrNativeClaimed": False, "wholeProjectComplete": False,
    })
    checks = {}
    for label in ["tests", "validate", "manifest", "audit", "budget", "vocabulary", "whitespace"]:
        path = L / f"{label}-788.txt"
        text = path.read_text(encoding="utf-8-sig")
        if label == "tests":
            assert "Ran 43 tests" in text and text.rstrip().endswith("OK")
        elif label == "validate":
            assert text.strip() == "0 error(s)"
        elif label == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        elif label == "vocabulary":
            assert "2122/2431 reviewed prompts; stage=pilot" in text
        dest = V / f"batch-103-textual-review-{label}-788.txt.gz"
        dest.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        checks[label] = {"archive": dest.name, "rawSha256": sha(path), "archiveSha256": sha(dest)}
    archives = [archive(V / name) for name in [
        "batch-103-initial-packet.txt", "batch-103-cli-config-help-execution-788.txt"]]
    save(V / "batch-103-evidence-packaging-788.json", {
        "snapshot": INITIAL, "archives": archives,
        "reason": "Lossless archives preserve original source/catalog whitespace and exact reviewer inputs."})
    for name in ["preflight-788.ps1", "checks-batch-103-review-788.ps1",
                 "checkpoint-review-788.py"]:
        shutil.copyfile(C / name, V / ("batch-103-" + name + (".txt" if name.endswith(".ps1") else "")))
    shutil.copyfile(L / "preflight-788.json", V / "batch-103-runner-role-788.json")
    ledger_path = S / "batch-103-progress.json"
    ledger = load(ledger_path)
    ledger.update(
        status="textual-correction-awaiting-original-session-confirmations",
        textualReview={"execution": 788, "initialSnapshot": INITIAL,
                       "initialModels": ["claude-opus-5.5", "gpt-6.1-sol"],
                       "initialReviewsComplete": True, "textualAcceptanceComplete": False,
                       "fullBatchAcceptanceComplete": False, "reviewClosed": [],
                       "initialReconciliation": "docs/n1-reviews/batch-103-initial-reconciliation-788.json"},
        nextAction="SAME103 both original-session serial confirmations of exact minimal translation correction on one signed changed tree; no native/publication/104.")
    save(ledger_path, ledger)
    save(L / "freeze-evidence-788.json", {
        "initialSnapshot": INITIAL, "runtime": runtime, "checks": checks, "budget": budget})
    message = (
        "Clarify batch 103 example translation and preserve blind initial reviews\n\n"
        "Local changed-tree freeze; original-session confirmations and all runtime/publication gates pending.\n\n"
        "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n")
    (C / "commit-freeze-788.txt").write_text(message, encoding="utf-8")
    print("Both original reviews preserved; minimal changed-tree correction audited and ready for normal signed local freeze.")


def record():
    common()
    assert git("rev-parse", "HEAD") == REVISED and git("rev-parse", "HEAD^") == INITIAL
    before = load(V / "batch-103-initial-reconciliation-788.json")
    confirmations = {}
    for label, model in [("claude", "claude-opus-5.5"), ("gpt", "gpt-6.1-sol")]:
        prefix = f"batch-103-confirmation-{label}"
        execution = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert execution["snapshot"] == coverage["snapshot"] == REVISED
        assert execution["sessionId"] == before["processes"][label]["sessionId"]
        assert execution["exitCode"] == 0 and execution["actualModels"] == [model]
        assert execution["usageCurrentModel"] == model and coverage["allAssignedRangesReturned"]
        assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
        assert execution["availableTools"] == ["view"] and execution["multiToolResponseCount"] == 0
        assert len(execution["toolCalls"]) == 1
        call = execution["toolCalls"][0]
        assert call["success"] and call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
        assert absent(execution["launcherPid"])
        assert sha(V / (prefix + ".md")) == execution["reportSha256"]
        assert sha(V / (prefix + ".jsonl")) == execution["rawExecutionSha256"]
        confirmations[label] = {k: execution[k] for k in [
            "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode", "actualModels",
            "snapshot", "reportSha256", "rawExecutionSha256"]}
        confirmations[label].update(
            report=prefix + ".md", execution=prefix + "-execution.json",
            coverage=prefix + "-coverage.json", allAssignedRangesReturned=True,
            toolCalls=1, observedToolOverlaps=0,
            losslessExecutionArchive=archive(V / (prefix + ".jsonl")))
    assert before["processes"]["gpt"]["completedAt"] < confirmations["claude"]["startedAt"]
    assert confirmations["claude"]["completedAt"] < confirmations["gpt"]["startedAt"]
    runtime = audit_runtime()
    assert runtime == load(V / "batch-103-runtime-correction-audit-788.json")
    required = load(V / "batch-103-confirmation-required-review-ranges.json")[0]
    assert required["end"] == 502 and sha(C / "batch-103-confirmation-packet.txt") == required["sha256"]
    hypotheses = before["hypotheses"]
    hypotheses[1].update(
        status="withdrawn",
        finalDisposition="Original Claude confirmation withdraws the hypothesis: context-dependent pep-talk paraphrase is supported, not an asserted literal JMdict gloss. GPT retains original CLEAN.")
    finding = before["finding"]
    finding.update(
        status="resolved", revisedTeachingSnapshot=REVISED,
        finalDisposition="Original Claude confirms minor English ambiguity resolved, high confidence. Original GPT accepts clarity improvement but explicitly does not retroactively classify original English as a proved error. This calibrated disagreement is preserved; both find no remaining in-scope textual defect.",
        bothOriginalSessionsConfirmed=True)
    verdicts = {
        unit: {"correctness": "CLEAN", "scopedCoverage": "CLEAN", "textComprehensibility": "CLEAN"}
        for unit in ["kanji/励.md:1-53", "words/激励.md:1-32", "words/励む.md:1-43",
                     "words/励ます.md:1-38", "words/応援.md:40",
                     "words/慰める.md:33", "words/学問.md:21"]
    }
    reconciliation = {
        "schemaVersion": 1, "execution": 788, "batch": "103",
        "status": STAGE, "originalTeachingSnapshot": INITIAL, "revisedTeachingSnapshot": REVISED,
        "initialModels": before["initialModels"], "processes": before["processes"],
        "confirmations": confirmations,
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allAssignedRangesReturned": True,
        "initialPacketBytes": 267532, "initialPacketLines": 5542,
        "confirmationPacketBytes": 30573, "confirmationPacketLines": 502,
        "completeFamiliesSupplied": 78, "rawCharacterRecordsSupplied": 11,
        "completeArticleBodies": 38, "newArticleBodies": 4, "changedReusedPassages": 3,
        "verdicts": verdicts, "findings": [finding], "hypotheses": hypotheses,
        "optional": before["optional"], "consequentialUnresolvedChangedTeachingClaims": [],
        "coordinatorEvidence": before["coordinatorEvidence"],
        "runtime": runtime,
        "boundedEvidenceLimits": before["limits"] + [
            "Confirmations reread four complete current new articles, four complete relevant families and four extracted public dictionary texts. Broader78-family/34comparison/guard/navigation scope carried forward from originals, not freshly repeated.",
            "Reused navigation-only passages not supplied again in confirmations; initial CLEAN verdicts carried forward explicitly. Coordinator runtime diff proves they are unchanged.",
            "Native 厂 fallback/readability in allfourfonts/default remains mandatory; neither reviewer independently reproduced47Han/cmap inventory.",
            "No exhaustive whole-corpus/future-pool semantic guarantee, native-speaker approval, physical-phone/general-release acceptance or learning-effectiveness claim.",
        ],
        "matchedSampleContributions": {
            "shared": "All seven scoped units CLEAN after confirmation, three raw readingentries/twoactualkeys/allocation, conjugations/eventroles,27directword/fourkanjiguards/sixlinkdirections and preserved navigation-only legacy content accepted textually.",
            "claudeUnique": "Identified avoidable imperative-looking English translation; minimal declarative clarification implemented and confirmed. Also raised contextualが and pep-talk hypotheses, both withdrawn in original-session evidence reconciliation; three optional repetitions/display hints declined.",
            "gptUnique": "No unique proved defect; retained original declarative/dictionary-phrase acceptance and explicit non-retroactive classification. Detailed sense-local homograph/spelling restrictions support current guards, not invented new defect credit.",
            "limits": "Common snapshot/scope/source access; compared equivalent findings/hypotheses/optional/limits. Actual byte return is not equal read depth or a general model benchmark.",
        },
        "processDiagnostic": before["processDiagnostic"],
        "initialReviewsComplete": True, "textualAcceptanceComplete": True,
        "fullBatchAcceptanceComplete": False, "reviewClosed": [], "runtimeChangedThisExecution": True,
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT,
    }
    save(V / "batch-103-reconciliation.json", reconciliation)
    ledger_path = S / "batch-103-progress.json"
    ledger = load(ledger_path)
    ledger.update(status=STAGE, nextAction=NEXT)
    ledger["textualReview"].update(
        revisedSnapshot=REVISED, textualAcceptanceComplete=True,
        reconciliation="docs/n1-reviews/batch-103-reconciliation.json",
        bothOriginalSessionsConfirmed=True, fullBatchAcceptanceComplete=False,
        scopeLimits=reconciliation["boundedEvidenceLimits"])
    ledger["limits"][0] = "Textual reviews and both original-session confirmations closed; full batch acceptance/publication still pending."
    ledger["limits"][3] = "Fresh non-skipped qualified Android, ContentSyncONCE/native/rendered/font/finite-option acceptance and all publication gates remain."
    save(ledger_path, ledger)
    freeze_evidence = load(L / "freeze-evidence-788.json")
    save(S / "execution-788.json", {
        "schemaVersion": 1, "execution": 788, "checkpoint": 788, "batch": "103",
        "stage": STAGE, "originalTeachingSnapshot": INITIAL, "revisedTeachingSnapshot": REVISED,
        "androidSignedHead": APP, "freshOriginMain": MAIN,
        "startingState": load(C / "progress.json")["execution788StartingState"],
        "initialReviewers": before["processes"], "confirmations": confirmations,
        "reconciliation": "docs/n1-reviews/batch-103-reconciliation.json",
        "checks": freeze_evidence["checks"], "pythonTestsPassed": 43, "validatorErrors": 0,
        "localBudget": freeze_evidence["budget"], "runtimeHashesVerified": 8463,
        "contentVersion": runtime["contentVersion"], "runtimeChangedThisExecution": True,
        "onlyRuntimeChange": runtime["onlyTeachingChange"], "runtimePublished": False, "reviewClosed": [],
        "initialReviewsComplete": True, "bothOriginalSessionsConfirmed": True,
        "textualAcceptanceComplete": True, "fullBatchAcceptanceComplete": False,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 129,
        "remainingAdditions": 1099, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "processDiagnostic": before["processDiagnostic"],
        "localAuditDiagnostic": "First correction audit compared Git blobCRLF to universal-newline text and failed an assertion after preserving initial JSONL archives. Corrected comparison to normalize CRLF, verified existing archives byte-for-byte against original control outputs, resumed without overwriting original reports or archives. No source/runtime semantic relaxation or signing retry.",
        "nextAction": NEXT,
    })
    for name in ["checkpoint-review-788.py", "confirm-batch-103-788.py"]:
        target = ("batch-103-checkpoint-review-788.py" if name.startswith("checkpoint")
                  else "batch-103-confirmation-recipe.py")
        shutil.copyfile(C / name, V / target)
    shutil.copyfile(C / "post-batch-103-review-788.ps1",
                    V / "batch-103-post-batch-103-review-788.ps1.txt")
    archive(V / "batch-103-confirmation-packet.txt")
    (C / "commit-review-788.txt").write_text(
        "Record batch 103 textual reconciliation and original-session confirmations\n\n"
        "Textual acceptance only; qualified Android/native/rendered and publication remain pending.\n\n"
        "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>\n",
        encoding="utf-8")
    print("Both original sessions confirmed; final textual reconciliation and pending runtime gates persisted.")


def signed_final():
    common()
    head = git("rev-parse", "HEAD")
    assert head != REVISED and git("rev-parse", "HEAD^") == REVISED
    assert not git("status", "--porcelain")
    changes = git("-c", "core.quotepath=false", "diff", "--name-only", REVISED, head).splitlines()
    assert all(n.startswith("docs/n1-reviews/batch-103-")
               or n in {"docs/n1-sources/batch-103-progress.json", "docs/n1-sources/execution-788.json"}
               for n in changes), changes
    assert not git("diff", REVISED, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    runtime = audit_runtime()
    assert runtime == load(V / "batch-103-runtime-correction-audit-788.json")
    return head, runtime


def package_confirmation_tasks():
    common()
    assert git("rev-parse", "HEAD") == REVISED
    receipts = [archive(V / f"batch-103-confirmation-{label}-task.txt")
                for label in ["claude", "gpt"]]
    save(V / "batch-103-confirmation-evidence-packaging-788.json", {
        "snapshot": REVISED, "archives": receipts,
        "diagnostic": "Final staged whitespace check found an extra blank EOF line in each exact original confirmation prompt. Archived original prompt bytes losslessly rather than modifying reviewer inputs or weakening the check. No runtime change or signing attempt occurred."})
    shutil.copyfile(Path(__file__), V / "batch-103-checkpoint-review-788.py")
    print("Exact original confirmation prompts archived without changing their bytes.")


def issue():
    head, runtime = signed_final()
    path = C / "batch-103-review-788-issue.txt"
    assert not path.exists()
    path.write_text(
        "Batch103 / checkpoint788: **two independent textual reviews and both original-session "
        "confirmations completed; runtime/native/publication acceptance pending**.\n\n"
        f"Normally signed local evidence `{head}` preserves initial snapshot `{INITIAL}` and revised "
        f"teaching `{REVISED}`. Claude Opus5.5 (`claude-opus-5.5`) and GPT-6.1 Sol (`gpt-6.1-sol`) "
        "ran serially, view-only, against the same267532-byte/5542-line blind packet:47member+31comparison="
        "78complete JMdict families,11raw character records,38complete article bodies,4archived public "
        "dictionary texts. Each first read returned the exact full packet. GPT made3additional serial "
        "overlapping tail reads (first2truncated); all original scope already returned, no missing scope. "
        "Actual models, zero internal tool overlap, and real process exit before each subsequent "
        "review verified; complete original reports, raw/model/session/range evidence preserved.\n\n"
        "**One minimal clarification:** 激励's team example now translates as **'They encourage the team.'** "
        "instead of imperative-looking 'Encourage the team.' Japanese/kana unchanged. Claude identified "
        "minor ambiguity and confirms resolution; GPT accepted the original as a dictionary-style "
        "translation and accepts the clarity improvement without retrospectively calling it a proved "
        "error. That calibrated disagreement is retained, not decided by votes. Both original sessions "
        "confirm the same signed revised tree and find no consequential textual defect/regression. "
        "Claude withdraws its contextualが/pep-talk hypotheses; optional repetitions/display hints are "
        "not required changes. All4newarticles and3exact navigation-only reused passages CLEAN in "
        "the three bounded textual facets. Confirmations reread4currentarticles/4relevantfamilies/"
        "4dictionarytexts; unchanged broader scope carried forward, not claimed freshly reread. "
        "Byte access/self-report is not equal semantic depth or independent upstream retrieval.\n\n"
        "The three retained/selected full readings still yield **TWO keys れい/はげむ**, not an "
        "independentはげます question. Original786three-keyclaim remains explicitly corrected, not rewritten. "
        "Plain励ます versus polite励みます, activityに versus personを, conjugations/passive roles, "
        "4directkanji/27directwordguards,3mappedpairs/6directions and navigation-only legacy metadata/"
        "levels/identities preserved. No supportwordlevel inferred. Actual47Han still includes "
        "**厂 U+5382**, absent from all3bundledcmaps: NOT a glyphfailure or native-readability "
        "result. Its specific fallback/readability in all4fonts/default remains mandatory.\n\n"
        f"43focused tests, validator0errors, regenerated manifest/batch-baseline-link-reading audits, "
        f"vocabulary consistency and unchanged local budgets passed; all**8463runtime hashes** verified, "
        f"contentVersion`{runtime['contentVersion']}`. Existing vocabulary coverage remains2122/2431pilot. "
        "Runtime diff since initial review is ONLY this English clarification plus generated manifest. "
        "Local initial auditCRLF comparison diagnostic corrected without semantic relaxation. One optional "
        "live-log probe hit an open-writer sharing conflict; no live retry/access-policy change, waited "
        "for reviewer exit, then normal closed-output archiving succeeded. Not an ACL/policy denial; "
        "original error/disposition retained. Parent5920/exact session/ancestry verified; runner.lock "
        "untouched; durable control/committed evidence only.\n\n"
        "**129/1228 published;1099 acceptance remainder unchanged.** No push, fresh Android/native/"
        "rendered acceptance or batch104. Next SAME103 non-skipped qualifiedAndroid host checks and "
        "actual production N1/All/custom meaning-builder/fallback/direct-symmetric-nontransitive guards "
        "(only劣 of劣万厚 isN1), then current-content ContentSyncONCE/native/four-font/厂fallback/"
        "rendered finite-option semantic acceptance and every original combined-main/signing/"
        "owner-fast-forward/terminal-CI/exact-immutable-ZIP/hash/budget publication gate. Approved "
        "Android`bf30cdead8515739bc0e671d57a54b9a3109dd46` remains qualifiedguard+schemaonly, not "
        "unrelated latestmain. Compatible stop-cran/kanji-cards-android#125 and "
        "stop-cran/kanji-cards-android#132 mechanisms required; old clients ignore them. "
        "Physical-phone/general-release/whole-set acceptance remains outstanding; project incomplete. "
        "Evidence: docs/n1-reviews/batch-103-reconciliation.json and docs/n1-sources/execution-788.json.\n",
        encoding="utf-8", newline="\n")
    (L / "signed-head-788.txt").write_text(head + "\n", encoding="ascii")
    print("Signed clean local textual acceptance verified; exact owner issue body prepared.")


def finish():
    head, runtime = signed_final()
    posted = load(L / "issue-788-verified.json")
    body = (C / "batch-103-review-788-issue.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body and head in body
    before, p = load(L / "progress-before-788.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    receipt = {
        "schemaVersion": 1, "execution": 788, "checkpoint": 788, "batch": "103",
        "savedCommit": head, "signature": "G", "originalTeachingSnapshot": INITIAL,
        "revisedTeachingSnapshot": REVISED, "freshOriginMain": MAIN, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-788.json",
        "reconciliation": "docs/n1-reviews/batch-103-reconciliation.json",
        "contentVersion": runtime["contentVersion"], "initialReviewsComplete": True,
        "bothOriginalSessionsConfirmed": True, "textualAcceptanceComplete": True,
        "fullBatchAcceptanceComplete": False, "runtimeDrafted": ["励"], "reviewClosed": [], "published": [],
        "runtimeChangedThisExecution": True, "runtimePublished": False,
        "independentReviewersLaunched": 2, "dependentOriginalSessionConfirmations": 2,
        "models": ["claude-opus-5.5", "gpt-6.1-sol"],
        "originalSessions": {
            "claude": "eb1a8995-1568-4cd5-b7bb-0a1056233592",
            "gpt": "93b54be3-157e-4b13-a32c-e48e9f51c8d8"},
        "serialReviewerProcessesVerified": True, "allInternalToolsSerial": True,
        "allAssignedRangesReturned": True, "freshAndroidOrNativeClaimed": False,
        "pythonTestsPassed": 43, "validatorErrors": 0, "runtimeHashesVerified": 8463,
        "unresolvedChangedTeachingFindings": [],
        "readDepthLimits": "Both exact full initial packets returned. GPT3extra overlapping serialtailreads(first2truncated) retained. Confirmations reread4newarticles/4families/4dictionarytexts; broader original scope carriedforward. Byteaccess is not comprehension/equaldepth/upstreamverification.",
        "publishedAdditions": 129, "remainingAdditions": 1099, "lastPublishedCommit": MAIN,
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before), "ownerIssueAuthorAndExactBodyVerified": True,
        "issueUpdate": posted["html_url"], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "sharingConflict": "One optional live rawJSONL read failed while reviewer output writer open; no live retry or policy change, waited normal exit and archived closed output. Preserved in reconciliation/execution receipt.",
        "status": "continue", "stage": STAGE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "nextAction": NEXT, "blocker": None,
    }
    p["execution788CoordinatorCheckpoint"] = receipt
    p["execution788StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    p["batch103TextualReviewIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": hashlib.sha256(body.encode("utf-8")).hexdigest(), "verified": True}
    p.update(checkpoint=788, status="continue", stage=STAGE, batch="103", nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    assert persisted == p
    assert all(persisted[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-788-final-verification.json", receipt)
    print(json.dumps({k: receipt[k] for k in ["checkpoint", "savedCommit", "status", "stage", "issueUpdate",
                                            "originalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    {"freeze": freeze, "audit": lambda: print(json.dumps(audit_runtime(), ensure_ascii=True)),
     "record": record, "package": package_confirmation_tasks,
     "issue": issue, "finish": finish}[sys.argv[1]]()
