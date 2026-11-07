import copy
import gzip
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

C = Path(__file__).parent
spec = importlib.util.spec_from_file_location("review091", C / "review-batch-091.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
review = module.review
R, A, S, V, L = review.R, review.A, review.S, review.V, review.L
load, save, sha, git = review.load, review.save, review.sha, review.git
INITIAL = review.SNAPSHOT
STAGE = "textually-review-closed-awaiting-fresh-android"
NEXT = (
    "SAME091 fresh non-skipped sibling Android RealContentTest THREE cases and RareHanTest ONE case "
    "against THIS content tree; preserve exact XML/provenance and normally signed local evidence, then yield. "
    "Qualified TESTONLY Android1c1b7bf42cc91d820a93169f1088dc647ac51c0d retains productionf9b59a2, "
    "not latest app main. Explicit JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-17.0.20.101-hotspot "
    "and ANDROID_HOME=C:\\Users\\stop-\\AppData\\Local\\Android\\Sdk in same shell, one Gradle worker and "
    "quoted '-Pkotlin.compiler.execution.strategy=in-process'. Parent19008 already owns runner.lock; "
    "NO child reacquisition/delete/unlock or parent-only recovery wrapper copy. Keep exact signed-head/"
    "checkpoint/wholly-clean-worktree/verified-parent-ancestry checks; preserve/report/yield actual new denial, "
    "signing hang or uncertain ownership. Textual091 closed after serial blind Claude/GPT initials on77e8735b, "
    "one localized conservative English-label correction and both original-session serial confirmations. "
    "Five raw readings ジン/ニン/は/やいば/き.る retained in order; onlyは selected with own linked row. "
    "Recognized on/やいば not source-only or uniformly rare; き.る source-only without fabricated spelling. "
    "New刃 kanji/word, physical-part noun, neutral translated examples, shape-only mnemonic, three N1 wrong "
    "labels, FIVE direct word guards including先端, explicit physical versus figurative cutting-edge contrast, "
    "one mapped pair/two directions. Later native gate requires all21 scopedHan especially丶 across FOUR "
    "productionfont families, THREE pinned drawingstrokes, onlykunは/noon keys, both newarticles/SystemBack/"
    "offline and先端route, actualN1/All productionchoices, fullarchive productionContentSync ONCE with "
    "terminalcase0/no skips. Cmap absence is not glyphfailure; originalsessions retained for dependent "
    "visuals, no newblindcredit. All original source/baseline/link/reading/twofamily/native/currentmain-normalmerge/"
    "substantiveteachingreview/checks/normal-signing/owner-fastforward/terminalgreenCI/EVERYimmutableZIP"
    "manifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/media/path/ownerissue "
    "gates remain. Published117/1228 and1111acceptanceremainder unchanged; physicalphone/generalrelease/"
    "whole-set outstanding. No092, native/reviewer/publication or secondrunner in next hostcheckpoint."
)


def records(kind="initial"):
    result = {}
    prior = None
    for label, model in review.MODELS.items():
        prefix = f"batch-091-{kind}-{label}"
        record = load(V / (prefix + "-execution.json"))
        coverage = load(V / (prefix + "-coverage.json"))
        assert record["exitCode"] == 0 and record["actualModels"] == [model]
        assert record["usageCurrentModel"] == model
        assert record["multiToolResponseCount"] == 0
        assert not record["unfinishedTools"] and not record["observedToolOverlaps"]
        assert coverage["allAssignedRangesReturned"]
        assert len(record["toolCalls"]) == 1
        call = record["toolCalls"][0]
        assert call["name"] == "view" and call["success"]
        assert call["exactRequestedTextContainedInResult"] and not call["truncationMarker"]
        assert sha(V / (prefix + ".md")) == record["reportSha256"]
        assert sha(V / (prefix + ".jsonl")) == record["rawExecutionSha256"]
        assert review.absent(record["launcherPid"])
        if prior:
            assert prior < record["startedAt"]
        prior = record["completedAt"]
        if kind == "confirmation":
            initial = load(V / f"batch-091-initial-{label}-execution.json")
            assert initial["sessionId"] == record["sessionId"]
            assert initial["completedAt"] < record["startedAt"]
        result[label] = {
            **{key: record[key] for key in [
                "launcherPid", "sessionId", "startedAt", "completedAt", "exitCode",
                "requestedModel", "actualModels", "snapshot", "reportSha256", "rawExecutionSha256",
            ]},
            "report": prefix + ".md", "execution": prefix + "-execution.json",
            "coverage": prefix + "-coverage.json", "allAssignedRangesReturned": True,
            "toolCalls": 1, "observedToolOverlaps": 0, "firstCallExactFullPacketReturned": True,
        }
    return result


def prepare_fix():
    assert git("rev-parse", "HEAD") == INITIAL and git("log", "-1", "--format=%G?") == "G"
    processes = records()
    assert not (V / "batch-091-initial-adjudication.json").exists()
    changed = git("-c", "core.quotepath=false", "diff", "--name-only", INITIAL, "--",
                  "kanji", "words", "articles", "strokes", "manifest.json", "tools").splitlines()
    assert changed == ["words/刃.md"]
    ledger = load(S / "batch-091-progress.json")
    assert ledger["status"] == "local-unreviewed-draft"
    ledger["initialDraftWordQuizAudit"] = copy.deepcopy(ledger["wordQuizAudit"])
    row = ledger["wordQuizAudit"]["directExclusions"][0]
    assert row["exclude"] == ["刀", "日本刀", "端", "縁"]
    row["exclude"].append("先端")
    row["reason"] += " Independent review identified figurative English cutting-edge/leading-edge label ambiguity with先端; add this fifth conservative direct guard without claiming physical synonymy."
    ledger["wordQuizAudit"]["notExcluded"] = (
        "ナイフ and 包丁 name whole knives; primaryは physical cutting-part sense is not automatically "
        "either whole object. 先端 now has a conservative DIRECT guard for figurative English-label "
        "overlap, not physical interchangeability. No transitive tool/edge clique."
    )
    ledger["wordQuizAudit"]["limits"] = "Five conservative direct displayed-label guards, not transitive closure, universal synonymy or live-pool certification."
    ledger.update(
        status="textual-correction-awaiting-confirmation", initialReviewSnapshot=INITIAL,
        reviewClosed=[], published=[], textualReviewClosed=False,
        nextAction="SAME091 both original reviewer sessions serially confirm exact localized先端 guard/figurative contrast correction after signed freeze. No Android/native/publication/092.",
    )
    save(S / "batch-091-progress.json", ledger)

    class ArticleText(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.parts = []

        def handle_starttag(self, tag, attrs):
            if tag == "article":
                self.depth += 1
            if self.depth and tag in {"p", "h2", "h3", "br", "section"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "article":
                self.depth -= 1

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    path = C / "batch-091-ninjou-647.html"
    raw = path.read_bytes()
    parser = ArticleText()
    parser.feed(raw.decode("utf-8"))
    text = "".join(parser.parts)
    assert "デジタル大辞泉" in text and "にん" in text and "刃物で人を傷つけること。" in text
    archive = S / "batch-091-ninjou-647.html.gz"
    archive.write_bytes(gzip.compress(raw, mtime=0))
    supplemental = {
        "url": "https://kotobank.jp/word/%E5%88%83%E5%82%B7-537845",
        "retrievedAt": review.now(), "sourcePath": str(path), "sourceSha256": sha(path),
        "archive": archive.name, "archiveSha256": sha(archive),
        "losslessGzip": gzip.decompress(archive.read_bytes()) == raw,
        "inspectedHeadings": ["Digital Daijisen にん‐じょう【刃傷】", "Seisenban Nihon Kokugo Daijiten にん‐じょう【刃傷】"],
        "briefDefinitionExcerpt": "刃物で人を傷つけること。",
        "supports": "The recognition gloss injury or bloodshed involving a blade is not an unsupported transfer from the character meaning. Both exact lexical entries define injuring a person with a bladed implement.",
        "limits": "Fresh coordinator web_fetch and exact downloaded HTML inspected; not independent reviewer upstream retrieval. No graphic example or new teaching sense added. Alternateじんじょう also retained in archived source, not a new selected prompt.",
    }
    save(S / "batch-091-ninjou-supplement-647.json", supplemental)
    save(V / "batch-091-initial-adjudication.json", {
        "schemaVersion": 1, "execution": 647, "batch": "091", "snapshot": INITIAL,
        "initialProcesses": processes,
        "findings": [{
            "id": "F1", "reportedBy": ["Claude"], "severity": "minor",
            "facet": "scoped coverage / quiz curation", "file": "words/刃.md:4,8,30-34",
            "claim": "English cutting edge can mean forefront; 先端 title tip; leading edge can overlap despite distinct physical Japanese meanings.",
            "evidence": "Actual words/先端.md:4,17,37; complete JMdict1388110 sense2; direct unguarded labels in initial snapshot.",
            "disagreement": "GPT initial explicitly found no additional guard established from physical comparison/shared topic. Preserve that assessment; this is English-label ambiguity rather than a physical synonym assertion.",
            "decision": "Accept a conservative localized DIRECT先端 guard and one explicit physical-versus-figurative clarification. Not a claim that the initial full two-gloss label guarantees an ambiguous live question; production impact not measured. Same displayed-label precaution motivates existing端/縁guards.",
            "status": "partially resolved", "remaining": "Both original-session changed-passage confirmations pending.",
        }],
        "hypotheses": [
            {"claim": "blade slang could overlapナイフ", "reportedBy": ["Claude"], "status": "withdrawn",
             "decision": "Not established as defect; ordinary primary physicalpart noun and wholetool contrast supported. No newナイフguard or clique; wider livepools uncertified."},
            {"claim": "Blade-related injury gloss not directly established by supplied lexical definition", "reportedBy": ["Claude"],
             "status": "resolved", "decision": "Fresh exact Daijisen/Nikkoku刃傷entry supports injury with bladed implement; no teaching edit required.",
             "evidence": "docs/n1-sources/batch-091-ninjou-supplement-647.json"},
        ],
        "optional": [
            {"claim": "Kana topicは pronunciation/parsing note", "reportedBy": ["Claude"], "status": "optional", "decision": "No edit; readings use standard orthographic particles and translations are correct."},
            {"claim": "歯 homophone note", "reportedBy": ["Claude"], "status": "optional", "decision": "No edit; written word/physicaltool context disambiguates; not a homophone course."},
            {"claim": "刄 variant", "reportedBy": ["Claude"], "status": "optional", "decision": "No edit; bounded modern-form lesson does not need full variants."},
            {"claim": "Furtherジンexamples such as凶刃", "reportedBy": ["Claude"], "status": "optional", "decision": "No edit; current verified recognition row is sufficient."},
        ],
        "runtimePublished": False, "runtimeAccepted": False,
        "limits": "Both original full reports preserved before fix. Initial disagreement remains explicit, not vote-based adjudication; confirmations dependent, not new blind review.",
    })
    print("Initial reports/processes preserved; one localized correction awaits signed confirmation.")


def checks():
    commands = {
        "validate": [sys.executable, "-B", str(R / "tools" / "validate.py")],
        "manifest": [sys.executable, "-B", str(R / "tools" / "build_manifest.py")],
        "audit": [sys.executable, "-B", str(R / "tools" / "audit_n1_batch.py"), "--batch", "091"],
        "tests": [
            sys.executable, "-B", "-m", "unittest", "test_audit_n1_batch",
            "test_audit_n1_pilot", "test_extract_n1_jmdict", "test_freeze_n1_sources",
        ],
        "budget": [sys.executable, "-B", str(R / "tools" / "check_content_budget.py")],
    }
    for name, command in commands.items():
        path = V / f"batch-091-textual-review-{name}-647.txt"
        assert not path.exists()
        with path.open("wb") as stream:
            result = subprocess.run(command, cwd=R / "tools" if name == "tests" else R,
                                    stdout=stream, stderr=subprocess.STDOUT)
        assert result.returncode == 0, path
        print(name, "passed")


def prepare_confirmations():
    head = git("rev-parse", "HEAD")
    assert head != INITIAL and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    originals = records()
    assert not (C / "batch-091-confirmation-freeze.json").exists()
    packet = C / "batch-091-confirmation-packet.txt"
    parts = [
        f"DEPENDENT CHANGED-PASSAGE CONFIRMATION. Initial {INITIAL}; revised signed HEAD {head}.",
        "Not new blind review. No other reviewer's report is included. Only new guard and figurative contrast changed; no need to reopen complete dictionary packets or unchanged articles.",
    ]
    sources = []
    for path in [
        R / "kanji" / "刃.md", R / "words" / "刃.md", R / "words" / "先端.md",
        S / "batch-091-ninjou-supplement-647.json",
    ]:
        body = path.read_text(encoding="utf-8-sig")
        parts.append(f"SOURCE {path}; SHA256 {sha(path)}\n" +
                     "".join(f"{i}: {line}\n" for i, line in enumerate(body.splitlines(), 1)))
        sources.append({"path": str(path), "sha256": sha(path)})
    root = ET.parse(S / "batch-091-comparison-jmdict.xml").getroot()
    entry = next(e for e in root.findall("entry") if e.findtext("ent_seq") == "1388110")
    parts.append("COMPLETE previously supplied frozen JMdict1388110 family:\n" + ET.tostring(entry, encoding="unicode"))
    parts.append("EXACT runtime diff initial-to-revised:\n" + git(
        "-c", "core.quotepath=false", "diff", INITIAL, head, "--",
        "kanji", "words", "strokes", "articles", "manifest.json", "tools"))
    packet.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    save(V / "batch-091-confirmation-required-ranges.json", [{
        "path": str(packet), "start": 1, "end": len(packet.read_text(encoding="utf-8").splitlines()),
        "sha256": sha(packet),
    }])
    save(C / "batch-091-confirmation-freeze.json", {
        "initialSnapshot": INITIAL, "revisedSnapshot": head, "signature": "G",
        "originals": originals, "packet": str(packet), "packetSha256": sha(packet), "sources": sources,
    })
    shutil.copyfile(packet, V / packet.name)
    print("Normally signed correction freeze:", head)


def run_confirmation(label):
    freeze = load(C / "batch-091-confirmation-freeze.json")
    review.SNAPSHOT = freeze["revisedSnapshot"]
    review.PACKET = C / "batch-091-confirmation-packet.txt"
    review.PROMPT = C / f"batch-091-confirmation-{label}-prompt.txt"
    own = V / f"batch-091-initial-{label}.md"
    prompt = f"""DEPENDENT textual correction confirmation in your ORIGINAL session {freeze['originals'][label]['sessionId']}, actual model {review.MODELS[label]}.
Initial signed snapshot {INITIAL}; revised signed snapshot {review.SNAPSHOT}. This is NOT a fresh blind initial review.
Read exactly ONE resource: {review.PACKET}. Use exactly ONE full-file view with forceReadLargeFiles=true, no view_range; no shell, edits, delegation, other reports or parallel calls. The packet supplies complete two new articles, relevant comparison, complete previously supplied JMdict1388110, fresh coordinator lexical evidence with limits and EXACT actual diff including regenerated manifest.
Your own original report is retained in your session and appended below. No other reviewer's report or adjudication is supplied. Do not reopen whole dictionaries or unrelated articles.
Changes: new word quiz_exclusions appends direct先端 guard; one sentence distinguishes figurative English cutting edge/forefront from physical刃は using existing linked先端せんたん. Assess this as a conservative English-LABEL guard, not assertion physical Japanese senses are interchangeable or transitive. Do not require exhaustive figurative alternatives or extra support articles.
Confirm exact changed passage and regression scope in BOTH new articles for correctness/scopedcoverage/phoneTEXTcomprehensibility. Preserve original raw/curated reading dispositions, useful bounded practice, examples, shape-only mnemonic, threewrongkanjilabels, previous four directguards and one reciprocalpair/twodirections. Addition of comparisonlink does not create a new mappedprimarysupportpair/backlink quota. Read fresh exact Daijisen/Nikkoku刃傷source record for original gloss hypothesis; supplied coordinator lookup, NOT your independent retrieval.
Reconcile OWN original findings/hypotheses/optional notes explicitly (resolved/partially resolved/unresolved/withdrawn/optional). If no new defect, do not manufacture expansion. Retain independent initial disagreement if you do not consider original fix mandatory; assess revised text on evidence, not votes.
Return COMPLETE report: Snapshot;Scope(actual model/read/provenance);Verdicts(correctness/scopedcoverage/textcomprehensibility EACH of2newarticles, distinguish changedpassage assessment from inherited unchanged conclusions);Findings(severity;facet;file:lines;claim+impact;remedy;evidence;confidence ornone);Optional;Limits. Preserve no independentGit/upstream/nativefont/drawing/UI/phone/productionN1/All/generalrelease/whole-set certification. No edits/questions/nextbatch.

YOUR ORIGINAL REPORT (verbatim):
{own.read_text(encoding='utf-8')}
"""
    review.PROMPT.write_text(prompt, encoding="utf-8")
    shutil.copyfile(review.PROMPT, V / review.PROMPT.name)
    source = (C / "review-batch-089.py").read_text(encoding="utf-8")
    start = source.index("def run(label):")
    end = source.index('\n\nif __name__ == "__main__":', start)
    body = source[start:end].replace("batch-089-", "batch-091-")
    body = body.replace("batch-091-initial-", "batch-091-confirmation-")
    body = body.replace("batch-091-required-review-ranges.json", "batch-091-confirmation-required-ranges.json")
    body = body.replace("session = str(uuid.uuid4())",
                        "session = load(C / 'batch-091-confirmation-freeze.json')['originals'][label]['sessionId']")
    exec(compile(body, str(Path(__file__)), "exec"), review.__dict__)
    review.run(label)


def close():
    sys.path.insert(0, str(R / "tools"))
    from audit_n1_batch import audit
    from audit_n1_pilot import metadata
    from build_manifest import build_manifest, sha256
    from extract_n1_jmdict import extract
    from fontTools.ttLib import TTFont
    from generate_strokes import convert

    freeze = load(C / "batch-091-confirmation-freeze.json")
    head = freeze["revisedSnapshot"]
    assert git("rev-parse", "HEAD") == head and git("log", "-1", "--format=%G?") == "G"
    initial_processes, confirmations = records(), records("confirmation")
    assert initial_processes["gpt"]["completedAt"] < confirmations["claude"]["startedAt"]
    assert git("rev-parse", "HEAD", repo=A) == review.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    assert not git("diff", head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for kind in ["initial", "confirmation"]:
        path = C / f"batch-091-{kind}-packet.txt"
        assert path.read_bytes() == (V / path.name).read_bytes()
    ledger = load(S / "batch-091-progress.json")
    assert ledger["status"] == "textual-correction-awaiting-confirmation"
    assert ledger["reviewClosed"] == ledger["published"] == []
    mechanical = audit(R, "091")
    assert mechanical == load(V / "batch-091-textual-review-audit-647.txt")
    source = load(R / "docs" / "n1-source-snapshot.json")
    for name, info in source["inputs"].items():
        path = C / "inputs" / name
        assert sha(path) == info["sha256"] and path.stat().st_size == info["bytes"]
    dictionary = C / "inputs" / "n1-implementation-JMdict_e.gz"
    compressed = dictionary.read_bytes()
    assert review.hashlib.sha256(gzip.decompress(compressed)).hexdigest() == source["jmdict"]["xmlSha256"]
    for packet in ledger["dictionaryPackets"]:
        selection = load(S / packet["selection"])
        assert extract(compressed, source["inputs"][dictionary.name]["sha256"],
                       selection["entryIds"]) == (S / packet["xml"]).read_bytes()
    kd = gzip.decompress((C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes())
    assert review.hashlib.sha256(kd).hexdigest() == source["kanjidic2"]["xmlSha256"]
    chars = {entry.findtext("literal"): entry for entry in ET.fromstring(kd).findall("character")}
    canonical = lambda entry: ET.canonicalize(ET.tostring(entry, encoding="unicode"), strip_text=True)
    raw_count = 0
    for name in ["batch-091-kanjidic2.xml", "batch-091-comparison-kanjidic2.xml"]:
        for entry in ET.parse(S / name).getroot().findall("character"):
            assert canonical(entry) == canonical(chars[entry.findtext("literal")])
            raw_count += 1
    assert raw_count == 5
    baseline = load(S / "baseline-inventory.json")
    exceptions = {"words/虎.md": ["酔っ払い"], "words/猿.md": ["馬鹿"],
                  "words/丘.md": ["坂", "山"], "words/冗談.md": ["ユーモア"]}
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            expected = copy.deepcopy(info["metadata"])
            if name in exceptions:
                expected["quiz_exclusions"] = exceptions[name]
            if name == "kanji/山.md":
                expected["distractors"] = ["川", "出", "木"]
            assert metadata(R, name) == expected, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha(R / name) == info["sha256"], name
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    pairs = {tuple(row) for row in ledger["allMappedReciprocalPairs"]}
    assert pairs == {("刃", "words/刃.md")}
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / "kanji" / (char + ".md")).read_text(encoding="utf-8")
    word = metadata(R, "words/刃.md")
    assert word["quiz_exclusions"] == ["刀", "日本刀", "端", "縁", "先端"]
    assert "jlpt" not in word and word["reading"] == "は" and word["kanji"] == ["刃"]
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    checked = 0
    for section, entries in manifest.items():
        if isinstance(entries, dict):
            for name, expected in entries.items():
                actual = sha(R / name) if section in {
                    "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name)
                assert actual == expected, name
                checked += 1
    assert checked == 8432 and manifest["contentVersion"] == "cb3c857f3614485d"
    assert load(R / "strokes" / "刃.json") == convert(
        "刃", (S / "batch-091-kanjivg.svg").read_text(encoding="utf-8"))
    supplemental = load(S / "batch-091-ninjou-supplement-647.json")
    archive = S / supplemental["archive"]
    assert sha(archive) == supplemental["archiveSha256"]
    assert review.hashlib.sha256(gzip.decompress(archive.read_bytes())).hexdigest() == supplemental["sourceSha256"]
    scoped = ["kanji/刃.md", "words/刃.md"]
    text = "".join((R / name).read_text(encoding="utf-8") for name in scoped)
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    assert len(han) == 21 and "先" in han
    fonts = []
    for row in load(S / "batch-091-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert sha(path) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": sha(path),
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    assert all(row["allActualMissing"] == ["丶"] for row in fonts)
    save(S / "batch-091-reviewed-font-audit-647.json", {
        "schemaVersion": 1, "batch": "091", "scope": scoped, "actualHan": han,
        "actualHanCount": 21, "addedByReviewedCorrection": ["先"], "fonts": fonts,
        "scopeHash": {name: sha(R / name) for name in scoped},
        "nativeFontAcceptance": "pending",
        "limits": "Updated complete article inventory; original20Han draft audit remains historical. Cmap presence/absence not native legibility/fallback-face evidence; fresh four-font/all21Han required.",
    })
    receipts = {}
    for name in ["validate", "manifest", "audit", "tests", "budget"]:
        path = V / f"batch-091-textual-review-{name}-647.txt"
        text = path.read_text(encoding="utf-8-sig")
        if name == "validate":
            assert text.strip() == "0 error(s)"
        elif name == "tests":
            assert "Ran 43 tests" in text and text.rstrip().endswith("OK")
        receipts[name] = {"path": path.relative_to(R).as_posix(), "sha256": sha(path)}
    manifest_hash_explanation = {
        "reportedBy": "Claude confirmation Limits",
        "claim": "Raw packet SHA256 differs from manifest payload SHA256; hashing basis not independently verified.",
        "status": "resolved", "category": "mechanical-provenance-question-not-teaching-defect",
        "evidence": "tools/build_manifest.py:18-19 normalizes CRLF to LF before hashing textual content. Every8432payloadhash reverified using production helper; manifest regenerated and equality checked.",
        "examples": {name: {"rawSha256": sha(R / name), "normalizedManifestSha256": sha256(R / name),
                            "actualManifestEntry": manifest["files"][name]}
                     for name in scoped},
        "limits": "Coordinator mechanism verification, not reviewer independent integrity or runtime import evidence.",
    }
    initial = load(V / "batch-091-initial-adjudication.json")
    finding = copy.deepcopy(initial["findings"][0])
    finding.update(status="resolved", remaining=None,
                   confirmationEvidence=["batch-091-confirmation-claude.md", "batch-091-confirmation-gpt.md"])
    hypotheses = copy.deepcopy(initial["hypotheses"])
    hypotheses[0].update(
        status="unresolved", category="nonactionable-lexical-hypothesis-not-consequential-teaching-claim",
        decision="Claude retains speculative slang ambiguity but recommends no guard; GPT establishes no defect. Primaryはphysicalpart and wholetool contrast remain supported. No livepool certification or fabricated tool clique.",
    )
    limits = [
        "Textual closure only. Fresh Android/native/fourfont/visual/combinedmain/signing/publication gates pending; runtime not accepted or published.",
        "Bothactualfamilies received identical171760byte3761line initialpacket:78completeJMdictfamilies(56lexical22comparison),5rawcharacters,16completearticles. Each used exactlyonefullpacketview, exactfulltextreturned/notruncation/nooverlap. Byteaccess not comprehension/equalfreshreaddepth.",
        "Original reports/disagreement preserved before fix. Claude minor English-label coverage finding accepted conservatively; GPT initial no-mandatory-guard assessment explicitly retained. Both originalsessions confirmed signedcorrectionserially, dependent not newblindreviews.",
        "Newword appends fifthdirect先端guard and one figurativeEnglishcuttingedge/forefrontcontrast. No physicalsynonymy/transitiveclique/wordlevel or newprimarysupportpair. Rawreadings/selectedは/shapeonlymnemonic/examples unchanged.",
        "Fresh exact刃傷Daijisen/Nikkoku lookup resolves gloss hypothesis; coordinatorprovidedrecord/excerpt and losslessHTMLarchive, not reviewer independentupstream. Historical imageglyph/classification limits preserved.",
        "Claude speculativeナイフslang concern remains nonactionable, not an established consequentialtextualdefect. ProductionN1/All actualchoices and widercustompools still uncertified.",
        "RawfileSHA differs from normalizedmanifestSHA whereCRLF; coordinatorverified productionnormalization and every8432payloadhash. Not newruntimeimport/native evidence.",
        "Updated21scopedHan includes added先; allthree mainbundledcmaps lack丶. Cmapabsence notglyphfailure. Freshfourfont/all21/native/drawing/SystemBack/offline/先端route and terminalcase0 stillrequired; inheritedpilotall40historical.",
        "QualifiedTESTONLYAndroid1c1b7bf4 retains productionf9b59a2, not latestappmain. Compatibleclientf9b59a2+ required; oldclientsignorecuration/wordguards. Physicalphone/generalrelease/whole-set outstanding.",
        "Published117/1228 and1111acceptanceremainder unchanged. Sixseparate earlierN2sourcemembers保案派第策結 not counted as acceptedissue60 additions; separate妖exception retained.",
        "Alloriginalnormalmerge/substantiveteachingreview/validation/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifestentryhash/original18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemedia/path/ownerissue gates remain; noguardincrease.",
        "Parent19008retainsrunner.lock; nochildacquisition/delete/unlock. Approvedcontrolhelpers/committedpackets/frozenworkspaceinputs only; nooptionalhistoricalsessionhelperaccess or actualnewpermissiondenial. Incidental post-exit Get-Process check raced with completion and correctly found no process; serialexit independently verified, no retry/denial.",
    ]
    rec = {
        "schemaVersion": 1, "execution": 647, "batch": "091", "status": STAGE,
        "originalTeachingSnapshot": INITIAL, "reviewedTeachingSnapshot": head,
        "teachingChangedAfterInitialReviews": True,
        "reviewedRuntimeHashes": {name: sha(R / name) for name in scoped + ["strokes/刃.json", "manifest.json"]},
        "initialModels": list(review.MODELS.values()), "processes": initial_processes,
        "confirmations": confirmations, "serialReviewerProcessesVerified": True,
        "eachOriginalReportArchivedBeforeNextLaunch": True, "allInternalToolsSerial": True,
        "allAssignedRangesReturned": True, "initialPacketBytes": 171760, "initialPacketLines": 3761,
        "initialDistinctCompleteFamilies": 78, "rawCharacterRecords": 5,
        "completeArticleBodiesSupplied": 16, "newArticleBodies": 2, "changedReusedBodies": 0,
        "originalSessionSupplements": 2,
        "verdicts": {name: {"correctness": "CLEAN", "scopedCoverage": "CLEAN",
                          "textComprehensibility": "CLEAN", "scope": "complete new article with bounded changed-passage confirmation"}
                     for name in scoped},
        "findings": [finding], "hypothesisDispositions": hypotheses,
        "optionalDispositions": initial["optional"], "manifestHashBasisDisposition": manifest_hash_explanation,
        "modelContributionComparison": {
            "shared": "Bothaccept completekanji/word, raw/curatedreadings/recognition/source-only distinctions, naturalexamples/translations/particles, toolpartcontrast, shapeonlymnemonic, threewrongkanjilabels, originalfourguards and onepair/twodirections. BothconfirmrevisedEnglishcontrast/directguard.",
            "claudeUnique": "Verified useful localized English cutting-edge/leading-edge label-coverage concern; conservative remedy adopted. Optional four expansions not mandatory. Gloss-evidence hypothesis prompted corroborating exact lexical source, not a proved mistranslation.",
            "gptUnique": "No uniqueverifiedmandatoryteachingdefect. Explicit no-mandatory先端guard assessment retained; confirmation accepts conservative improvement without retracting original independent conclusion.",
            "limits": "Matched snapshot/task/source access, allreportsections including optional/hypotheses/limits compared; nofindingquota/generalmodelranking/equalcomprehension claim. Confirmation is dependent not blind unique discovery.",
        },
        "actionableRemainingTeachingFindings": 0, "consequentialUnresolvedTeachingFindings": 0,
        "textualReviewClosed": True, "runtimeAccepted": False, "runtimePublished": False,
        "mechanicalBatchAudit": mechanical, "runtimeHashesReverified": checked,
        "originalBaselineMetadataAndStrokesPreserved": counts,
        "freshFrozenLexicalPacketsVerified": 2, "frozenInputHashesVerified": 5,
        "completeRawCharacterRecordsVerified": raw_count,
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "directWordExclusionPairs": 5,
        "actualHanCount": 21, "nativeFontPending": ["丶"],
        "checks": receipts, "focusedTestsPassedThisCheckpoint": 43,
        "newNativeOrAndroidClaimed": False, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "nextAction": NEXT, "limits": limits,
    }
    assert not (V / "batch-091-reconciliation.json").exists()
    save(V / "batch-091-reconciliation.json", rec)
    ledger["runtimeDraftLimits"] = ledger["limits"]
    ledger.update(
        status=STAGE, textualReviewClosed=True, runtimeAccepted=False, reviewClosed=[], published=[],
        reviewSnapshot=head, initialReviewSnapshot=INITIAL,
        reviewEvidence="docs/n1-reviews/batch-091-reconciliation.json",
        textuallyResolvedFindings=["F1"], nextAction=NEXT, limits=limits,
        reviewedFontAudit="docs/n1-sources/batch-091-reviewed-font-audit-647.json",
    )
    save(S / "batch-091-progress.json", ledger)
    shutil.copyfile(Path(__file__), S / "batch-091-textual-closure-recipe.py")
    save(S / "execution-647.json", {
        "schemaVersion": 1, "execution": 647, "batch": "091",
        "initialTeachingSnapshot": INITIAL, "reviewedTeachingSnapshot": head, "status": STAGE,
        "startingState": load(C / "progress.json")["execution647StartingState"],
        "reconciliation": "docs/n1-reviews/batch-091-reconciliation.json",
        "reconciliationSha256": sha(V / "batch-091-reconciliation.json"),
        "recipeHashes": {"docs/n1-sources/batch-091-textual-closure-recipe.py": sha(S / "batch-091-textual-closure-recipe.py"),
                        **{(V / name).relative_to(R).as_posix(): sha(V / name)
                           for name in ["review-batch-091.py", "batch-091-serial-review-base-recipe.py"]}},
        "checks": receipts, "runtimeHashesReverified": checked, "focusedTestsPassed": 43,
        "runtimeChangedThisExecution": True, "runtimeChangedAfterConfirmations": False,
        "runtimeAccepted": False, "runtimePublished": False, "newAndroidOrNativeClaimed": False,
        "wholeProjectComplete": False, "publishedAdditions": 117, "remainingAdditions": 1111,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "limits": limits,
    })
    print("Both original-session confirmations reconciled; all8432runtime hashes verified.")


def checkpoint():
    head = git("rev-parse", "HEAD")
    freeze = load(C / "batch-091-confirmation-freeze.json")
    assert head != freeze["revisedSnapshot"] and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain")
    assert git("rev-parse", "HEAD", repo=A) == review.ANDROID
    assert git("log", "-1", "--format=%G?", repo=A) == "G"
    assert not git("status", "--porcelain", repo=A)
    runner = load(C / "runner.json")
    assert runner["pid"] == 19008 and runner["sessionId"] == L.name and not review.absent(19008)
    rec = load(V / "batch-091-reconciliation.json")
    for name, expected in rec["reviewedRuntimeHashes"].items():
        assert sha(R / name) == expected
    assert not git("diff", freeze["revisedSnapshot"], head, "--",
                   "kanji", "words", "strokes", "articles", "manifest.json", "tools")
    records()
    records("confirmation")
    progress = load(C / "progress.json")
    original = load(L / "progress-before-647.json")
    assert progress["checkpoint"] == 646 and progress["batch"] == "091"
    progress["execution647StartingState"]["status"] = "signed-local-textual-review-checkpoint-complete"
    cp = {
        "schemaVersion": 1, "execution": 647, "checkpoint": 647, "batch": "091",
        "savedCommit": head, "signature": "G", "initialTeachingSnapshot": INITIAL,
        "reviewedTeachingSnapshot": freeze["revisedSnapshot"],
        "status": "continue", "stage": STAGE,
        "reconciliation": "docs/n1-reviews/batch-091-reconciliation.json",
        "evidence": "docs/n1-sources/execution-647.json",
        "actualInitialModels": rec["initialModels"], "initialReviewerProcesses": 2,
        "originalSessionSupplements": 2, "serialProcessesAndInternalToolsVerified": True,
        "allAssignedPacketRangesReturned": True, "originalReportsPreserved": True,
        "allFourProcessesOneCallExactFullPacketReturned": True,
        "initialDistinctCompleteFamilies": 78, "rawCharacterRecords": 5,
        "textualReviewClosed": True, "actionableRemainingTeachingFindings": 0,
        "consequentialUnresolvedTeachingFindings": 0,
        "resolvedFinding": "F1 conservative direct先端guard and physical/figurative Englishcuttingedge contrast; initial independent disagreement preserved.",
        "runtimeHashesReverified": 8432, "focusedTestsPassedThisCheckpoint": 43,
        "runtimeChangedThisExecution": True, "runtimeChangedAfterConfirmations": False,
        "runtimePublished": False, "runtimeAccepted": False, "newAndroidOrNativeClaimed": False,
        "actualHanCount": 21, "nativeFontPending": ["丶"],
        "allMappedReciprocalPairs": 1, "directedLinksVerified": 2, "directWordExclusionPairs": 5,
        "reviewClosed": [], "published": [], "publishedAdditions": 117, "remainingAdditions": 1111,
        "lastPublishedCommit": progress["lastPublishedCommit"],
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT, "dedicatedWorktreesClean": True,
        "originalHistoricalRootKeysCompared": len(original), "allOriginalHistoricalValuesPreserved": True,
    }
    progress["execution647CoordinatorCheckpoint"] = cp
    progress["batch091TextualReviewCheckpoint"] = dict(cp)
    progress.update(checkpoint=647, status="continue", stage=STAGE, nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(progress[key] == value for key, value in original.items() if key not in allowed)
    temp = C / "progress.647-checkpoint.tmp"
    assert not temp.exists()
    save(temp, progress)
    assert load(temp) == progress
    temp.replace(C / "progress.json")
    print("Checkpoint647 saved:", head, "; historical values preserved:", len(original))


if __name__ == "__main__":
    operation = sys.argv[1]
    if operation == "confirm":
        run_confirmation(sys.argv[2])
    else:
        {"prepare-fix": prepare_fix, "checks": checks, "close": close,
         "checkpoint": checkpoint, "prepare-confirmations": prepare_confirmations}[operation]()
