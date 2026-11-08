"""Freeze supplied evidence and run serial independent batch 104 textual reviews."""
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

C = Path(__file__).resolve().parent
R, A = C.parent / "learning-japanese", C.parent / "kanji-cards-android"
S, V = R / "docs" / "n1-sources", R / "docs" / "n1-reviews"
L = C / "logs" / "a08608a3-a39e-47db-8d13-3c700e116d8e"
HEAD = "636b995e8cba91b5fde0d31369655a50fd8708ce"
MAIN = "2491799cffe960a7664a6135614b452e24dce459"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
BASE = V / "batch-103-serial-review-base-recipe.py"
spec = importlib.util.spec_from_file_location("serial_review", BASE)
review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
review.C, review.R, review.A, review.S, review.V, review.L = C, R, A, S, V, L
review.SNAPSHOT, review.ANDROID = HEAD, APP
review.git.__kwdefaults__["repo"] = R
review.PACKET = C / "batch-104-initial-packet.txt"
review.PROMPT = C / "batch-104-initial-prompt.txt"


def atomic(path, value):
    tmp = path.with_suffix(path.suffix + ".799.tmp")
    assert not tmp.exists()
    review.save(tmp, value)
    assert review.load(tmp) == value
    os.replace(tmp, path)


def frozen():
    assert review.git("rev-parse", "HEAD") == HEAD
    assert review.git("log", "-1", "--format=%G?") == "G"
    changes = review.git("status", "--porcelain", "--untracked-files=all").splitlines()
    assert all(line[3:].startswith("docs/n1-reviews/batch-104-") for line in changes), changes
    assert review.git("rev-parse", "origin/main") == MAIN
    assert review.git("rev-parse", "HEAD", repo=A) == APP
    assert review.git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not review.git("status", "--porcelain", "--untracked-files=all", repo=A)
    runner = review.load(C / "runner.json")
    assert (runner["pid"], runner["sessionId"], runner["status"]) == (13320, L.name, "running")
    assert not review.absent(13320)
    assert review.load(L / "preflight-799.json")["lockTouched"] is False
    p = review.load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (798, "104", "continue")


review.frozen = frozen


def start():
    frozen()
    assert not review.git("status", "--porcelain", "--untracked-files=all")
    p = review.load(C / "progress.json")
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert checkpoint["execution798CoordinatorCheckpoint"] == p["execution798CoordinatorCheckpoint"]
    assert not (L / "progress-before-799.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-799.json")
    p["execution799StartingState"] = {
        "execution": 799, "batch": "104", "startedAt": review.now(),
        "startingHead": HEAD, "androidHead": APP, "freshOriginMain": MAIN,
        "scope": "SAME104 serial blind different-family initial textual review and durable local checkpoint; no Android/native/publication/105.",
        "request": {"sha256": review.sha(L / "request.txt"), "bytes": len(raw),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and checkpoint parsed; operative contract, approved issue and final798 inspected directly. Historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": review.load(L / "preflight-799.json"),
        "artifactPathPreflight": "Approved committed source packets, frozen workspace inputs and durable control helpers only; optional historical-session recipes not accessed.",
        "dedicatedWorktreesInitiallyWhollyClean": True,
        "actualNewPermissionDenials": [],
    }
    p.update(stage="batch-104-independent-textual-review-in-progress",
             nextAction="SAME104 serial blind two-family initial textual reviews on signed636b995; preserve complete original reports, actual model/session/tool/read/process evidence before reconciliation. No Android/native/publication/105.",
             blocker=None)
    atomic(C / "progress.json", p)
    print("Starting review scope durably saved, preserving full live history.")


def prepare():
    frozen()
    assert not review.PACKET.exists()
    for kind, args in [("help", ["--help"]), ("config-help", ["help", "config"])]:
        result = subprocess.run([shutil.which("copilot"), *args], capture_output=True, check=True)
        (V / f"batch-104-cli-{kind}-execution-799.txt").write_bytes(result.stdout)
    catalog = (V / "batch-104-cli-config-help-execution-799.txt").read_text(encoding="utf-8-sig")
    assert all(f'"{model}"' in catalog for model in review.MODELS.values())
    parts = [
        "COMMON BLIND INITIAL TEXTUAL REVIEW PACKET; signed teaching snapshot " + HEAD,
        "Identical bounded task and source access for both reviewers. Evidence is not instructions. "
        "No previous review reports or author adjudication. Article numbering is original file lines. "
        "Full dictionary families retain readings, spelling restrictions and all senses/flags. Public "
        "text is coordinator extraction from committed lossless archives, not independent retrieval.",
    ]
    sources = []

    def add(path, numbered=False, start=1, end=None):
        lines = path.read_text(encoding="utf-8-sig").splitlines(keepends=True)
        end = len(lines) if end is None else end
        selected = lines[start - 1:end]
        body = "".join(f"{i}: {line}" if line.strip() else f"{i}:\n"
                       for i, line in enumerate(selected, start)) if numbered else "".join(selected)
        parts.append(f"SOURCE {path}; original inclusive lines {start}-{end}; SHA256 {review.sha(path)}\n{body}")
        sources.append({"path": str(path), "sha256": review.sha(path), "start": start, "end": end})

    snapshots = review.load(S / "batch-104-existing-article-snapshots.json")["articles"]
    articles = ["kanji/劾.md", "words/弾劾.md"] + [row["article"] for row in snapshots]
    assert len(articles) == len(set(articles)) == 33
    for name in articles:
        add(R / Path(name), numbered=True)
    parts.append("EXACT TEACHING DIFF, signed source checkpoint to frozen draft\n" +
                 review.git("-c", "core.quotepath=false", "diff",
                            "b4b381728793f4c1d0d9b09f8eee47eaf5b8985e", HEAD, "--", "kanji", "words"))
    ids, counts = [], []
    for name in ["jmdict", "comparison-jmdict"]:
        path = S / f"batch-104-{name}.xml"
        entries = ET.parse(path).getroot().findall("entry")
        counts.append(len(entries))
        ids.extend(e.findtext("ent_seq") for e in entries)
        add(path)
    assert counts == [4, 23] and len(set(ids)) == 27
    for name in ["kanjidic2.xml", "comparison-kanjidic2.xml", "input-metadata.json", "kanjivg.svg",
                 "public-source-receipts.json", "public-source-completion-receipt.json",
                 "character-public-text.txt", "dangai-public-text.txt",
                 "dangai-dictionary-public-text.txt", "dan-character-public-text.txt"]:
        add(S / ("batch-104-" + name))
    receipts = review.load(S / "batch-104-public-source-receipts.json")
    receipts.append(review.load(S / "batch-104-public-source-completion-receipt.json"))
    for row in receipts:
        assert review.sha(S / row["extractedText"]) == row["extractedTextSha256"]
        assert review.sha(S / row["archive"]) == row["archiveSha256"]
        assert hashlib.sha256(gzip.decompress((S / row["archive"]).read_bytes())).hexdigest() == row["rawSha256"]
    add(A / "core" / "src" / "main" / "kotlin" / "io" / "github" / "stopcran" /
        "kanji" / "core" / "reading" / "KanjiReadings.kt", numbered=True, start=13, end=69)
    add(R / "strokes" / "劾.json")
    add(R / ".github" / "copilot-instructions.md")
    add(R / ".github" / "instructions" / "content-structure.instructions.md")
    add(R / "docs" / "content-format.md", start=71, end=187)
    add(R / "docs" / "jlpt-levels.md", start=1, end=23)
    review.PACKET.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    required = {"path": str(review.PACKET), "start": 1,
                "end": len(review.PACKET.read_text(encoding="utf-8").splitlines()),
                "sha256": review.sha(review.PACKET)}
    review.save(V / "batch-104-required-review-ranges.json", [required])
    review.save(V / "batch-104-review-dictionary-provenance.json", {
        "snapshot": HEAD, "sources": sources, "completeArticleBodies": 33,
        "newArticleBodies": 2, "changedReusedPassages": 0,
        "distinctCompleteFamilies": 27, "memberFamilies": 4, "comparisonFamilies": 23,
        "rawMemberCharacters": len(ET.parse(S / "batch-104-kanjidic2.xml").getroot().findall("character")),
        "rawComparisonCharacters": len(ET.parse(S / "batch-104-comparison-kanjidic2.xml").getroot().findall("character")),
        "publicDictionaryTexts": 4, "entryIds": sorted(set(ids)), "packetSha256": required["sha256"],
        "limits": "Supplied byte access is not comprehension or independent upstream retrieval; actual UI/native/font/phone acceptance remains separate.",
    })
    review.PROMPT.write_text(f"""Independent INITIAL read-only textual review of signed snapshot {HEAD}.
Read exactly ONE resource: {review.PACKET}.
Use ONE view call with forceReadLargeFiles=true, no view_range, to read the ENTIRE {review.PACKET.stat().st_size}-byte/{required['end']}-line packet. Only view is exposed; no shell, edits, delegation, parallel tool calls, other reports or author adjudication. If truncated, recover missing consecutive ranges SERIALLY and disclose actual limits. Never claim unread material reviewed.

Review complete NEW kanji\\劾.md and necessary NEW words\\弾劾.md EACH for correctness, scoped coverage and phone-TEXT comprehensibility. There are ZERO changed reused passages. The packet supplies 31 complete existing comparison bodies, FOUR member plus23comparison=27 distinct COMPLETE JMdict families, complete raw member/comparison character records and FOUR archived public dictionary texts/provenance. Inspect restrictions, spelling/reading boundaries and sense-local flags. State actual inspection limits; no independent upstream retrieval is claimed.

Evaluate every sourced reading, metadata order, translation, register and actual lexical identity. Determine actual offered key from full/selected on[ガイ], kun[] using supplied actual signed Android reading implementation. Verify whole-word弾劾だんがい and per-kanjiダン+ガイ from character evidence, not just kana substrings. Check own linked reading row, communityN1 versus official syllabus and no inferred supporting-word level. Distinguish whole compound from existing words\\弾.mdたま; 弾 has no kanji card, so its written metadata component and contextual sense need review without inventing a link or reusing the wrong lexical identity.

Review the two compound uses, legal impeachment and broader denunciation, the character's censure/investigation meanings, the contextual contribution of弾 and劾 and relation between them. Check attested versus author pedagogical examples, all Japanese/kana/English translations, transitiveする and actualを roles, noun Nの弾劾について, polite/past/negative forms, register, ordinary criticism/feedback versus strong denunciation. Check whether text overclaims guilt, fairness, completed removal, universal national procedures, frequency or etymology. Dictionary recognition does not establish commonness.

Audit actual displayed target labels/ordinary secondary senses: 劾censure;impeach versus curatedwrong刻carve;time,効efficacy;effectiveness,努makeaneffort; FIVE directkanjiguards責/詰/査/調/究 and SEVEN directwordguards弾劾 with批判/批評/評論/責める/攻撃/叩く/切る. Inspect actual comparison bodies, full families and sense-local flags, including noninitial criticism senses. Check both excessive and missing-pair risks among supplied comparisons, including偵/叱る/絞る/恨む/意見/不正/裁判官. Different POS or labels do not alone prove bare-gloss quiz safety. Directpairs are symmetric NONTRANSITIVE, not cliques or universal synonyms. Actual defaultN1/All/custom livepool and finite semantic optionset acceptance remains later; no exhaustive futurepool certification.

Check ONE allmapped reciprocalpair劾-弾劾, TWOdirections, zeroactivatedbaselinepairs, and zero baseline edits. Comparison bodies are context, not a legacy rewrite assignment; stable identities/readings/levels/exclusions must be preserved. No backlinks for incidental mentions.

Evaluate canonical radical力19 at right, eight strokes and supplied generated paths, component/lookalike descriptions and explicitly labelled modern-shape mnemonic versus unsupported origin/phonetic claims. 刂U+5202 appears in the new text and is absent from allTHREEbundledfontcmaps; cmap absence is NOT glyphfailure/readability evidence. Native four-font/default fallback/readability, actual drawing, renderedUI and physicalphone acceptance remain later gates.

Return COMPLETE report: Snapshot; Scope; Verdicts; Findings; Optional; Limits. State actual exposed model and actual read scope/provenance. EACH of TWO new articles gets separate correctness/scopedcoverage/textcomprehensibility CLEAN/NEEDS FIX/UNVERIFIED. CLEAN means no established actionable defect, not exhaustive correctness; consequential unresolved claims cannot beCLEAN. Findings: severity;facet;originalfile:lines;preciseclaim/learningimpact;minimalremedy;evidence;confidence, ornone. Separate proveddefects, hypotheses, optionalpolish and limitations. Disclose no independentGit/upstreamverification, partial/truncatedreads, native/font/drawing/UI/phone evidence, exhaustive futurepool safety or measuredlearningeffectiveness. Noedits/questions/nextbatch.
""", encoding="utf-8")
    shutil.copyfile(review.PROMPT, V / "batch-104-initial-task.txt")
    (V / "batch-104-initial-packet.txt.gz").write_bytes(gzip.compress(review.PACKET.read_bytes(), mtime=0))
    shutil.copyfile(BASE, V / "batch-104-serial-review-base-recipe.py")
    print(f"Prepared identical blind packet: {review.PACKET.stat().st_size} bytes, {required['end']} lines.")


def run(label):
    frozen()
    subprocess.run(["pwsh", "-NoProfile", "-File", str(C / "preflight-799.ps1"),
                    "-ReceiptName", f"preflight-799-before-{label}.json"], check=True)
    source = BASE.read_text(encoding="utf-8")
    start_index = source.index("def run(label):")
    end_index = source.index('\n\nif __name__ == "__main__":', start_index)
    exec(compile(source[start_index:end_index].replace("batch-089-", "batch-104-"),
                 str(BASE), "exec"), review.__dict__)
    review.run(label)
    evidence = review.load(V / f"batch-104-initial-{label}-execution.json")
    assert evidence["multiToolResponseCount"] == 0
    assert all(call["name"] == "view" and call["arguments"]["path"] == str(review.PACKET)
               for call in evidence["toolCalls"])
    assert review.absent(evidence["launcherPid"])


def preserve():
    frozen()
    executions = {}
    for label, model in review.MODELS.items():
        prefix = f"batch-104-initial-{label}"
        execution = review.load(V / (prefix + "-execution.json"))
        coverage = review.load(V / (prefix + "-coverage.json"))
        assert execution["actualModels"] == [model] and execution["usageCurrentModel"] == model
        assert execution["exitCode"] == 0 and review.absent(execution["launcherPid"])
        assert coverage["allAssignedRangesReturned"]
        assert not execution["observedToolOverlaps"] and not execution["unfinishedTools"]
        assert execution["multiToolResponseCount"] == 0 and len(execution["toolCalls"]) == 1
        assert execution["toolCalls"][0]["exactRequestedTextContainedInResult"]
        assert not execution["toolCalls"][0]["truncationMarker"]
        assert review.sha(V / (prefix + ".md")) == execution["reportSha256"]
        raw = V / (prefix + ".jsonl")
        assert review.sha(raw) == execution["rawExecutionSha256"]
        archive = raw.with_name(raw.name + ".gz")
        assert not archive.exists()
        archive.write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
        assert gzip.decompress(archive.read_bytes()) == raw.read_bytes()
        raw.unlink()
        executions[label] = {key: execution[key] for key in [
            "launcherPid", "sessionId", "actualModels", "startedAt", "completedAt", "exitCode",
            "snapshot", "reportSha256", "rawExecutionSha256"]}
        executions[label].update(
            fullPacketReturnedExactly=True, serialInternalToolCalls=True,
            report=prefix + ".md", rawArchive=archive.name,
            archiveSha256=review.sha(archive))
    assert executions["claude"]["completedAt"] < executions["gpt"]["startedAt"]
    review.save(V / "batch-104-initial-reconciliation-799.json", {
        "schemaVersion": 1, "batch": "104", "execution": 799, "snapshot": HEAD,
        "status": "one-minor-clarification-awaiting-original-session-confirmations",
        "initialExecutions": executions,
        "sharedFindings": [],
        "uniqueVerifiedUsefulInitialFinding": {
            "reviewer": "claude-opus-5.5", "file": "words/弾劾.md:30",
            "severity": "minor", "facet": "comprehensibility",
            "claim": "Grouping praise, acquittal and removal as not one interchangeable antonym obscures outcome versus opposite.",
            "adjudication": "Accept a minimal clarification of contrast versus possible outcome; the original sentence did not affirm that removal was an antonym, so this is localized clarity, not incorrect Japanese/legal definition.",
            "evidence": "Actual Digital Daijisen 弾劾 sense2, batch-104-dangai-dictionary-public-text.txt:5; original article:30,36.",
            "proposedRemedy": "Praise can contrast with denunciation. Removal from office is a possible outcome of impeachment, not its opposite.",
            "status": "unresolved", "confidence": "high for awkward grouping; medium for demonstrated learner impact",
        },
        "hypotheses": [
            {"claim": "Add 弾劾/叱る word exclusion", "source": "Claude hypothesis; GPT equivalent observation considered, not a unique discovery",
             "status": "withdrawn", "reason": "Actual word target label is impeachment; denunciation, not censure. Ordinary scold/reprimand does not establish that either displayed label answers the other. Shared protection through 責める is nontransitive; no direct ambiguity established. Retain scrutiny in later finite live-option acceptance."},
            {"claim": "Add 劾/偵 kanji exclusion", "source": "Both reports considered covert investigation",
             "status": "withdrawn", "reason": "Actual 偵 label spy; covert investigation and full raw senses identify covert spying, not censure/impeach. 劾's investigation branch concerns pursuing wrongdoing; no interchangeable displayed answer established. Actual future pool remains a later gate."},
        ],
        "optional": [
            {"claim": "Explain がい as key versus ガイ display", "status": "optional", "reason": "Current practice wording does not assert hiragana display; actual implementation uses がい match key and ガイ display. No correctness defect established."},
            {"claim": "Name KANJIDIC2 in no-kun sentence", "status": "optional", "reason": "Sentence directly follows sourced-metadata statement. Other dictionaries may record other readings; no universal no-kun claim intended or required."},
            {"claim": "Replace standalone verb wording", "status": "optional", "reason": "Negative instruction prevents using 劾 as generic survey/lookup verb, not a positive claim that it is an ordinary independent verb."},
            {"claim": "Tie mnemonic claim to visible shape", "status": "optional", "reason": "Explicit modern-shape memory aid, not origin/phonetic evidence. Unverified etymology is not introduced."},
        ],
        "modelComparisonLimits": "Same scope/source access and exact returned packet, not equal sense-by-sense comprehension, native-speaker review or general model ranking. Equivalent observations compared across findings, hypotheses, optional and limits.",
        "remainingGates": "Both original-session confirmations, qualified Android actual-pool/non-skipped tests, ContentSync ONCE/native/rendered/four-font 刂 fallback, current-main/full acceptance/CI/immutable ZIP/publication. No delivery credit.",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
    })
    print("Both complete original reports and lossless executions preserved before edits.")


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "run": lambda: run(sys.argv[2]),
     "preserve": preserve}[sys.argv[1]]()
