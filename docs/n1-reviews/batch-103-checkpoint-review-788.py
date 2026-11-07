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


if __name__ == "__main__":
    {"freeze": freeze, "audit": lambda: print(json.dumps(audit_runtime(), ensure_ascii=True))}[sys.argv[1]]()
