"""Prepare the bounded changed-tree correction checkpoint, not acceptance."""
import argparse
import ast
import copy
import gzip
import hashlib
import io
import json
import math
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
V = R / "docs" / "n1-reviews"
L = C / "logs" / "d9449cde-a292-4325-a8ad-908806a2ac62"
HEAD = "b799e904d379466b8b7a034d10d906b06644fefd"
TEACHING = "5a52b28e9f6f506171c5041bd52b0d9f8c261323"
MAIN = "716c610153234e8d2240dcf528de3ef83b654b27"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
NEXT = (
    "SAME100 TWO SERIAL original-session changed-passage confirmations on the normally signed "
    "LOCAL corrected snapshot. Initial textual reviews are COMPLETE on5a52b28e: preserve "
    "Claude4975f494-5c25-4a2d-8060-775ded9c734c/claude-opus-5.5 and "
    "GPTc9e3c7f4-b439-4f44-9255-4256c0987d25/gpt-6.1-sol original reports and actual "
    "read/process limits; do not rerun blind initial reviews. Supply each original reviewer "
    "their original findings, exact5a52b28e-to-current teaching diff, complete revised創, "
    "unchanged three reused changes/context and same bounded correction source supplement: "
    "12complete frozen families including1398640創立そうりつ establishment/founding and "
    "1398490創傷そうしょう formal/literary wound/injury; full設/初 source records and "
    "actual unchanged cards, original source blocks and correction decisions. F1/C1-establish/"
    "H1-initial are author-corrected but NOT independently confirmed: two unlinked examples "
    "plus direct創/設 establishment and conservative創/初 beginning/genesis guards now "
    "declared on new創 only; ten direct symmetric NONTRANSITIVE guards total. Review初 "
    "independently from exactfirst time;initial label, rawbeginning and創start/genesis; "
    "NOT merely substring初めて or shared topic. No universal substitution, transitive clique, "
    "new word identity/level or legacy設/初 edit. H1-wound remains withdrawn: no "
    "kanji/傷.md; words/傷.md is another namespace. Original optional polish stays optional. "
    "All six full readings/order and selectedソウ/つく.る remain; source-onlyショウ/"
    "けず.しける allocation UNVERIFIED, explicitly qualified/unselected. Reused創作N2/"
    "作るN5 metadata and13/5 guards preserved; five all-mapped pairs/ten directions/"
    "one activated baseline pair/three exact reused changes. ActualHan/font scope recomputed; "
    "cmap absence is NOT glyphfailure; native four-font/all-Han/rendered acceptance pending. "
    "Confirm serial reviewer PROCESS EXIT and internal tools, exact models/complete reports/"
    "read limits, reconcile evidence and check regressions; no actionable/consequential "
    "unresolved teaching claim before closure. Then fresh non-skipped qualifiedAndroid"
    "bf30cdead RealContent/RareHan, productionContentSyncONCE/native N1-All/meaning/"
    "curatedreading/drawing/article/Back/offline/four-font/all-Han/rendered acceptance, "
    "combinedcurrentmain checks, normal signing/ownerfastforward/terminalgreenCI/"
    "EVERYimmutableZIPmanifesthash/unchanged18000entry42MiBcompressed80MiBinflated"
    "56MiBretained/perfilepathmedia/verifiedownerissue gates remain mandatory. "
    "No unreviewedpush/101/authoragent/concurrentheavywork/secondrunner/signingretry/"
    "guardincrease. Verify whollyclean signedheads/freshmain/liveparentancestry/"
    "decodedlauncher/exactsession. Parent5920 ownsrunner.lock: no childacquire/delete/"
    "unlock/readprobe. Approvedcontrol/committedsource/frozeninputs only, not optional "
    "historicalsessionrecipes; preserve/report/yield actualnewdenial/signinghang/"
    "uncertainownership. Published126/1228,1102acceptanceremainder unchanged; six earlier"
    "N2placements保案派第策結 remain separate, never duplicate/relevel. "
    "Physicalphone/generalrelease/whole-set outstanding; projectincomplete."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    tmp = path.with_suffix(path.suffix + ".749.tmp")
    assert not tmp.exists(), tmp
    tmp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(tmp) == value
    tmp.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


def identity():
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (748, "100", "continue")


def start():
    identity()
    assert not git("status", "--porcelain")
    assert git("branch", "--show-current") == "content/n1-kanji"
    role = load(L / "preflight-749.json")
    assert role["sessionId"] == L.name and role["liveParentPid"] == 5920
    assert role["lockTouched"] is False
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    checkpoint = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    p = load(C / "progress.json")
    assert checkpoint["execution748CoordinatorCheckpoint"] == p["execution748CoordinatorCheckpoint"]
    before = L / "progress-before-749.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 749, "batch": "100", "startingHead": HEAD, "androidHead": APP,
        "freshOriginMain": MAIN, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME100 bounded correction/source supplement and signed LOCAL changed-tree freeze before original-session confirmations; no reviewer, Android/native, publication,101 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "characters": len(text),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete checkpoint parsed. Operative contract, complete approved issue and final748 directly inspected; historical middle parsed, not freshly semantically re-reviewed. Initial output encoding failure occurred after full loading/parsing."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved committed packets/frozen workspace inputs and durable control helpers only; optional historical-session recipes not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution749StartingState"] = state
    p.update(stage="batch-100-correction-source-supplement-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print(json.dumps(state["request"], ensure_ascii=True))


def supplement():
    identity()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
        inputs[name] = raw
    jm = inputs["n1-implementation-JMdict_e.gz"]
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    queries = {"設ける", "初めて", "初め", "初", "最初", "初恋", "建設", "設備", "創立", "創傷"}
    ids, reasons = [], {}
    for _, entry in ET.iterparse(io.BytesIO(gzip.decompress(jm)), events=["end"]):
        if entry.tag != "entry":
            continue
        matched = sorted(queries & {e.text for e in entry.findall("k_ele/keb")})
        if matched:
            eid = entry.findtext("ent_seq")
            ids.append(eid)
            reasons[eid] = matched
        entry.clear()
    assert {"1398640", "1398490", "1386070"} <= set(ids)
    raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    path = S / "batch-100-correction-jmdict.xml"
    assert not path.exists()
    path.write_bytes(raw)
    save(S / "batch-100-correction-selection.json", {
        "schemaVersion": 1, "batch": "100", "execution": 749, "entryIds": ids,
        "matchedSpellings": reasons, "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen family matching any exact keb in the bounded query set; no alias/reading/restriction/sense filtering.",
        "exactKebQueries": sorted(queries),
        "sourceGzipSha256": snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"],
        "sourceXmlSha256": snapshot["jmdict"]["xmlSha256"],
        "packetSha256": sha(raw),
        "attribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repositoryNOTICE.",
        "limits": "Extraction proves bytes, not lexical inspection, frequency or reviewer acceptance.",
    })
    source = ET.fromstring(kd)
    packet = ET.Element("kanjidic2")
    packet.append(copy.deepcopy(source.find("header")))
    for char in "設初":
        packet.append(copy.deepcopy(next(e for e in source.findall("character")
                                         if e.findtext("literal") == char)))
    ET.indent(packet, space="  ")
    kdpath = S / "batch-100-correction-kanjidic2.xml"
    assert not kdpath.exists()
    kdpath.write_bytes(ET.tostring(packet, encoding="utf-8", xml_declaration=True) + b"\n")
    compact = []
    for entry in ET.fromstring(raw):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    text = ("\n".join(compact) + "\n").encode("utf-8")
    (C / "batch-100-correction-full-family-reading.txt").write_bytes(text)
    (S / "batch-100-correction-full-family-reading.txt.gz").write_bytes(gzip.compress(text, mtime=0))
    print(json.dumps({"ids": ids, "matches": reasons, "families": len(ids),
                      "compactBytes": len(text), "frozenInputsVerified": len(inputs)}, ensure_ascii=True))


def record():
    identity()
    assert metadata(R, "kanji/創.md")["quiz_exclusions"] == list("作造始元原本緒産設初")
    assert not (R / "kanji" / "傷.md").exists()
    decisions = {
        "schemaVersion": 1, "batch": "100", "execution": 749,
        "initialTeachingSnapshot": TEACHING, "correctionBase": HEAD,
        "status": "author-corrected-awaiting-original-session-confirmations",
        "fullSupplementFamiliesInspected": load(S / "batch-100-correction-selection.json")["entryIds"],
        "completeSupplementRawRecordsInspected": ["設", "初"],
        "completeSupplementArticlesInspected": ["kanji/設.md", "kanji/初.md"],
        "sourceInspection": "Complete compact12-family text and both complete raw character records read directly. Full unchanged設/初 articles and original Daijisen創 block inspected. Frozen source bytes/hash verification is separate from semantic inspection.",
        "findings": [
            {"id": "F1", "status": "partially resolved",
             "authorChange": "Two minimal unlinked Common words examples: 創立そうりつ establishment/founding and創傷そうしょう wound/injury, explicitly formal or literary. Exact complete1398640/1398490; no new article, inferred level, frequency claim or idiom expansion.",
             "evidence": "JMdict1398640 full sense and1398490 full sense/misc; original actual Daijisen創 sense1創傷/sense2創立.",
             "limits": "Claude's localized coverage finding accepted; GPT initial coverage CLEAN remains historical disagreement. Await both original-session regression confirmations."},
            {"id": "C1-establish", "status": "partially resolved", "kanji": "設",
             "label": "establish; provide",
             "reason": "設's displayed establish branch can answer創's explicitly taught establishment/founding/start-up meaning. Raw設 English establishment/provision/prepare, full1386000 sense2 set up/establish and1257420 establishment support the overlap. Provide is not asserted equivalent to every創 sense.",
             "authorChange": "Direct創/設 exclusion on new創 only; legacy設 unchanged.",
             "limits": "Author source-confirmed correction; no independent changed-passage or live-pool acceptance yet."},
            {"id": "H1-initial", "status": "partially resolved", "kanji": "初",
             "label": "first time; initial",
             "reason": "Conservative direct guard for the initial/beginning branch: raw初 has beginning and創 has start/genesis; full1342540 beginning/start/outset and1293990 beginning/outset support that branch. Initial occurrence is not always creation, and first time is not a general translation of創. The pair is not inferred solely from Daijisen's初めて substring, novelty, a common topic or another guard.",
             "authorChange": "Direct創/初 exclusion on new創 only; unchanged初 N3 metadata, source readings and article remain historical context.",
             "limits": "Previously tentative hypothesis now has bounded author evidence and conservative safeguard. Both original reviewers must independently assess actual labels/senses; do not call this an independently verified defect or universal synonymy."},
            {"id": "H1-wound", "status": "withdrawn",
             "reason": "No kanji/傷.md exists. words/傷.md is another quiz namespace; no missing-card guard or new傷 card introduced."},
        ],
        "extraDirectGuards": [
            {"kanji": "設", "label": "establish; provide",
             "reason": "Displayed establishment branch overlaps創's explicitly taught founding/start-up sense; full1386000 sense2/raw設 and1398640 support the direct pair."},
            {"kanji": "初", "label": "first time; initial",
             "reason": "Conservative initial/beginning versus創 start/genesis overlap from exact full1342540/1293990 and raw初/創, not merely shared novelty; not unrestricted substitution."},
        ],
        "guardSemantics": "Ten direct pairs on new創 only, symmetric and nontransitive; preserve all eight original pairs and three wrong choices. No edges among existing neighbors, metadata releveling or unrelated legacy rewrite.",
        "cardEvidence": [
            {"path": f"kanji/{c}.md", "sha256": sha((R / f"kanji/{c}.md").read_bytes()),
             "unchangedSinceInitialSnapshot": (R / f"kanji/{c}.md").read_bytes() == subprocess.check_output(
                 ["git", "--no-pager", "-C", str(R), "show", f"{TEACHING}:kanji/{c}.md"])}
            for c in "設初"
        ],
        "sourceOnlyLexicalAllocation": "UNVERIFIED; unchanged explicit lookup-only unselectedショウ/けず.しける rows; no invented gloss/example/invalidity/obsolescence.",
        "originalOptionalItems": "O1-O4 remain optional; no scope expansion.",
        "initialReviewsComplete": True, "textualAcceptanceComplete": False, "reviewClosed": [],
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "nextAction": NEXT,
    }
    assert all(r["unchangedSinceInitialSnapshot"] for r in decisions["cardEvidence"])
    save(S / "batch-100-correction-decisions.json", decisions)
    ledger = load(S / "batch-100-progress.json")
    ledger["status"] = decisions["status"]
    ledger["proposedMetadata"] = metadata(R, "kanji/創.md")
    ledger["quizAudit"]["創"]["directExclusions"].extend(copy.deepcopy(decisions["extraDirectGuards"]))
    ledger["quizAudit"]["創"]["guardSemantics"] = decisions["guardSemantics"]
    ledger["dictionaryPackets"].append({
        "selection": "batch-100-correction-selection.json",
        "xml": "batch-100-correction-jmdict.xml"})
    ledger["limits"][0] = "Author-corrected local changed-tree draft; both original-session confirmations pending. No new reviewer, Android/native/font/phone acceptance or publication."
    ledger["limits"][5] = "Five all-mapped pairs/ten directions/one activated baseline pair, three exact reused changes. Ten direct symmetric nontransitive kanji guards; two author-added pairs await original reviewers."
    ledger["correctionCheckpoint"] = {
        "execution": 749, "initialTeachingSnapshot": TEACHING,
        "decisions": "batch-100-correction-decisions.json",
        "originalAuthoringPlanUnchanged": True, "changedTreeConfirmations": "pending",
        "supplementFamilies": 12, "supplementRawCharacterRecords": 2,
    }
    ledger["nextAction"] = NEXT
    save(S / "batch-100-progress.json", ledger)
    reconciliation = load(V / "batch-100-reconciliation.json")
    reconciliation["status"] = decisions["status"]
    reconciliation["teachingChangedAfterInitialReviews"] = True
    for row in reconciliation["findings"]:
        update = next(d for d in decisions["findings"] if d["id"] == row["id"])
        if update["status"] != "withdrawn":
            row["statusBefore749"] = row["status"]
            row["status"] = update["status"]
            row["correction749"] = copy.deepcopy(update)
    reconciliation["correctionCheckpoint"] = copy.deepcopy(ledger["correctionCheckpoint"])
    reconciliation["verdicts"]["kanji/創.md"]["scopedCoverage"] = "UNVERIFIED; author correction awaits original-session confirmations"
    reconciliation["verdicts"]["kanji/創.md"]["quizPoolAcceptance"] = "UNVERIFIED; author-added設/初 pairs await changed-tree semantic and native checks"
    reconciliation["runtimeChangedThisExecution"] = True
    reconciliation["nextAction"] = NEXT
    save(V / "batch-100-reconciliation.json", reconciliation)
    diff = subprocess.check_output(
        ["git", "--no-pager", "-C", str(R), "diff", "--no-ext-diff", TEACHING, "--",
         "kanji/創.md", "words/創作.md", "words/作る.md", "kanji/作.md"])
    (L / "batch-100-correction-teaching-diff.patch").write_bytes(diff)
    (S / "batch-100-correction-teaching-diff.patch.gz").write_bytes(gzip.compress(diff, mtime=0))
    assert git("-c", "core.quotepath=false", "diff", "--name-only", TEACHING, "--",
               "kanji", "words", "strokes", "articles") == "kanji/創.md"
    print("Author corrections/source decisions and exact teaching diff recorded; not review closure.")


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(c) for c in element))


def audit():
    from audit_n1_batch import audit as batch_audit
    from build_manifest import build_manifest, sha256
    from fontTools.ttLib import TTFont
    from generate_strokes import convert
    identity()
    result = batch_audit(R, "100")
    assert result["dictionaryFamilies"] == 163
    ledger = load(S / "batch-100-progress.json")
    decisions = load(S / "batch-100-correction-decisions.json")
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == info["bytes"] and sha(raw) == info["sha256"], name
        inputs[name] = raw
    jm = inputs["n1-implementation-JMdict_e.gz"]
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    assert sha(gzip.decompress(jm)) == snapshot["jmdict"]["xmlSha256"]
    packets = []
    for packet, compact in zip(ledger["dictionaryPackets"], [
            "batch-100-full-family-reading.txt.gz",
            "batch-100-comparison-full-family-reading.txt.gz",
            "batch-100-correction-full-family-reading.txt.gz"]):
        ids = load(S / packet["selection"])["entryIds"]
        raw = extract(jm, snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        assert raw == (S / packet["xml"]).read_bytes()
        assert [canonical(ET.fromstring(line)) for line in gzip.decompress(
            (S / compact).read_bytes()).decode("utf-8").splitlines()] == [
                canonical(e) for e in ET.fromstring(raw)]
        packets.append({"xml": packet["xml"], "families": len(ids), "sha256": sha(raw),
                        "freshFrozenExtractionMatches": True})
    frozen_kd = {e.findtext("literal"): canonical(e) for e in ET.fromstring(kd).findall("character")}
    records = {}
    for name in ["batch-100-kanjidic2.xml", "batch-100-comparison-kanjidic2.xml",
                 "batch-100-correction-kanjidic2.xml"]:
        for e in ET.parse(S / name).getroot().findall("character"):
            char = e.findtext("literal")
            assert canonical(e) == frozen_kd[char]
            records[char] = canonical(e)
    assert len(records) == 15
    meta = metadata(R, "kanji/創.md")
    original_plan = load(S / "batch-100-authoring-plan.json")
    expected = copy.deepcopy(original_plan["proposedMetadata"])
    expected["quiz_exclusions"] += ["設", "初"]
    assert meta == ledger["proposedMetadata"] == expected
    guards = ledger["quizAudit"]["創"]["directExclusions"]
    assert [r["kanji"] for r in guards] == meta["quiz_exclusions"] == list("作造始元原本緒産設初")
    for row in guards + ledger["quizAudit"]["創"]["meaningDecisions"]:
        assert metadata(R, f"kanji/{row['kanji']}.md")["title"] == row["label"]
    assert not set(meta["distractors"]) & set(meta["quiz_exclusions"])
    assert not (R / "kanji" / "傷.md").exists()
    previous_audit = load(S / "batch-100-draft-audit.json")
    baseline = load(S / "baseline-inventory.json")
    counts = {"kanji": 0, "words": 0, "strokes": 0}
    for name, info in baseline["files"].items():
        kind = name.split("/")[0]
        if kind in {"kanji", "words"}:
            baseline_meta = copy.deepcopy(info["metadata"])
            if name in previous_audit["baselineMetadataExceptions"]:
                baseline_meta["quiz_exclusions"] = previous_audit["baselineMetadataExceptions"][name]
            if name in previous_audit["baselineKanjiDistractorException"]:
                baseline_meta["distractors"] = previous_audit["baselineKanjiDistractorException"][name]
            assert metadata(R, name) == baseline_meta, name
            counts[kind] += 1
        elif kind == "strokes":
            assert sha((R / name).read_bytes()) == info["sha256"]
            counts[kind] += 1
    assert counts == {"kanji": 985, "words": 4942, "strokes": 985}
    assert git("-c", "core.quotepath=false", "diff", "--name-only", TEACHING, "--",
               "kanji", "words", "articles", "strokes") == "kanji/創.md"
    for name in ["words/創作.md", "words/作る.md", "kanji/作.md", "kanji/設.md",
                 "kanji/初.md", "strokes/創.json"]:
        assert (R / name).read_bytes() == subprocess.check_output(
            ["git", "--no-pager", "-C", str(R), "show", f"{TEACHING}:{name}"]), name
    assert all(sha((R / row["path"]).read_bytes()) == row["sha256"]
               for row in decisions["cardEvidence"])
    named = load(C / "inputs" / "n1-kanji-source-20261102.json")
    assert named == load(S / "community-list-20261102.json") and named[110] == "創"
    current_chars = {p.stem for p in (R / "kanji").glob("*.md")}
    previous = json.loads(git("show", f"{MAIN}:manifest.json"))
    previous_chars = {Path(p).stem for p in previous["files"] if p.startswith("kanji/")}
    assert current_chars - previous_chars == {"創"} and not previous_chars - current_chars
    assert metadata(R, "kanji/妖.md")["jlpt"] == 1
    assert all(metadata(R, f"kanji/{c}.md")["jlpt"] == 2 for c in "保案派第策結")
    pairs = {tuple(p) for p in ledger["allMappedReciprocalPairs"]}
    assert pairs == {(r["kanji"], r["article"]) for r in original_plan["supportMappings"]}
    assert len(pairs) == 5
    for char, name in pairs:
        assert f"(../kanji/{char}.md)" in (R / name).read_text(encoding="utf-8")
        assert f"(../{name})" in (R / f"kanji/{char}.md").read_text(encoding="utf-8")
    for name, level, n in [("words/創作.md", 2, 13), ("words/作る.md", 5, 5)]:
        m = metadata(R, name)
        assert m["jlpt"] == level and len(m["quiz_exclusions"]) == n
        assert m["quiz_exclusions"] == ledger["wordQuizAudit"]["preservedOriginalExclusions"][name]
    manifest = build_manifest(R)
    assert manifest == load(R / "manifest.json")
    verified = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, expected_hash in entries.items():
            actual_hash = (sha((R / name).read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else sha256(R / name))
            assert actual_hash == expected_hash, name
            verified += 1
    assert verified == 8453
    svg = (S / "batch-100-kanjivg.svg").read_bytes()
    stroke_proof = load(S / "batch-100-stroke-evidence.json")
    assert sha(svg) == stroke_proof["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke_proof["gitBlob"]
    assert svg == (C / "inputs" / "n1-05275-70a0b7ae.svg").read_bytes()
    geometry = load(R / "strokes" / "創.json")
    assert geometry == convert("創", svg.decode("utf-8"))
    assert geometry["strokeCount"] == len(geometry["strokes"]) == 12
    assert all(s["id"] == i and len(s["points"]) == 16 and
               all(len(p) == 2 and all(math.isfinite(v) for v in p) for p in s["points"])
               for i, s in enumerate(geometry["strokes"], 1))
    text = (R / "kanji" / "創.md").read_text(encoding="utf-8")
    assert "創立 そうりつ — establishment; founding" in text
    assert "創傷 そうしょう — wound; injury (formal or literary)" in text
    text += "".join(r["after"] for r in ledger["changedReusedPassages"])
    han = sorted({c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or 0x3400 <= ord(c) <= 0x9FFF
                  or 0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF})
    fonts = []
    for row in load(S / "batch-100-font-preparation.json")["fonts"]:
        path = Path(row["path"])
        assert path.is_relative_to(A) and sha(path.read_bytes()) == row["sha256"]
        with TTFont(path) as font:
            cmap = font.getBestCmap()
        fonts.append({"path": str(path), "sha256": row["sha256"],
                      "allActualMissing": [c for c in han if ord(c) not in cmap],
                      "actualPresence": {c: ord(c) in cmap for c in han}})
    scope_hashes = {n: sha((R / n).read_bytes()) for n in [
        "kanji/創.md", "words/創作.md", "words/作る.md", "kanji/作.md"]}
    font_audit = {
        "schemaVersion": 1, "batch": "100", "execution": 749,
        "completeArticleScope": ["kanji/創.md"],
        "changedReusedScope": ledger["changedReusedPassages"],
        "actualHanCount": len(han), "actualHan": han, "fonts": fonts,
        "newSinceDraft747": sorted(set(han) - set(load(S / "batch-100-draft-font-audit.json")["actualHan"])),
        "rareHanRangeCharacters": [c for c in han if 0x2E80 <= ord(c) <= 0x2FDF or
                                   0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF
                                   or 0x20000 <= ord(c) <= 0x2FFFF],
        "scopeHash": scope_hashes, "nativeFontAcceptance": "pending",
        "limits": "Cmap absence is not glyph failure. Fresh four-font/all-Han/native/rendered gates pending; no fresh phone evidence.",
    }
    save(S / "batch-100-correction-font-audit.json", font_audit)
    result.update(
        schemaVersion=1, execution=749, stage="author-corrected-awaiting-original-session-confirmations",
        correctionBase=HEAD, originalTeachingSnapshot=TEACHING,
        frozenInputHashesVerified=len(inputs), decompressedDictionaryHashesVerified=2,
        packets=packets, completeRawCharacterRecordsVerified=len(records),
        originalBaselineMetadataAndStrokesPreserved=counts,
        baselineMetadataExceptions=previous_audit["baselineMetadataExceptions"],
        baselineKanjiDistractorException=previous_audit["baselineKanjiDistractorException"],
        allMappedReciprocalPairs=5, directedLinksVerified=10, activatedBaselinePairs=1,
        newDirectKanjiExclusionPairs=10, addedCorrectionDirectPairs=[["創", "設"], ["創", "初"]],
        newDirectWordExclusionPairs=0,
        preservedWordExclusions=ledger["wordQuizAudit"]["preservedOriginalExclusions"],
        onlyTeachingFileChangedSinceInitial="kanji/創.md",
        allRuntimePayloadHashesVerified=verified, actualHanCount=len(han),
        pendingNativeFallbackLabels=fonts[0]["allActualMissing"],
        sourceOnlyLexicalAllocation=decisions["sourceOnlyLexicalAllocation"],
        generatedStrokeGeometryUnchangedAndExactlyRegenerated=True,
        publishedAdditions=126, remainingAdditions=1102, runtimePublished=False,
        independentReviewersLaunchedThisExecution=0, freshAndroidOrNativeClaimed=False,
        physicalPhoneAcceptance="outstanding", generalReleaseAcceptance="outstanding",
        wholeProjectComplete=False, optionalHistoricalHelpersAccessed=False,
        parentLockTouched=False, actualNewPermissionDenials=[])
    save(S / "batch-100-correction-audit.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def seal():
    identity()
    audit_result = load(S / "batch-100-correction-audit.json")
    assert audit_result["manifestFresh"] and audit_result["dictionaryFamilies"] == 163
    assert audit_result["allRuntimePayloadHashesVerified"] == 8453
    assert audit_result["newDirectKanjiExclusionPairs"] == 10
    raw_diff = S / "batch-100-correction-teaching-diff.patch"
    if raw_diff.exists():
        original = raw_diff.read_bytes()
        archived_diff = S / "batch-100-correction-teaching-diff.patch.gz"
        assert not archived_diff.exists()
        archived_diff.write_bytes(gzip.compress(original, mtime=0))
        assert gzip.decompress(archived_diff.read_bytes()) == original
        assert not (L / raw_diff.name).exists()
        shutil.move(raw_diff, L / raw_diff.name)
    save(S / "batch-100-correction-diagnostic-749.json", {
        "firstStagedWhitespaceCheck": "git diff --cached --check flagged five context-only single-space lines in the exact captured teaching diff.patch; no card/source whitespace defect.",
        "remedy": "Retain the original raw capture under the current execution log and archive its exact bytes as deterministic diff.patch.gz. No diff trimming, original-evidence rewrite, whitespace-rule relaxation, content edit, signature retry or acceptance waiver.",
        "originalDiffSha256": sha((L / "batch-100-correction-teaching-diff.patch").read_bytes()),
        "archivedDiffSha256": sha((S / "batch-100-correction-teaching-diff.patch.gz").read_bytes()),
        "lossless": gzip.decompress((S / "batch-100-correction-teaching-diff.patch.gz").read_bytes())
                    == (L / "batch-100-correction-teaching-diff.patch").read_bytes(),
        "actualNewPermissionDenials": [],
    })
    checks, budget = {}, None
    for label in ["tests", "validate", "manifest", "budget", "vocabulary", "audit", "whitespace"]:
        path = L / f"{label}-749.txt"
        text = path.read_text(encoding="utf-8-sig")
        if label == "tests":
            assert "Ran 52 tests" in text and "\nOK" in text
        elif label == "validate":
            assert "0 error(s)" in text
        elif label == "manifest":
            assert "8453 files" in text and audit_result["contentVersion"] in text
        elif label == "budget":
            budget = ast.literal_eval(text.strip())
            assert budget["entries"] <= 18000 and budget["retainedBytes"] <= 56 * 1024**2
            assert budget["inflatedBytes"] <= 80 * 1024**2 and budget["localZipBytes"] <= 42 * 1024**2
        elif label == "vocabulary":
            assert "2122/2431 reviewed prompts; stage=pilot" in text
        elif label == "audit":
            assert json.loads(text) == audit_result
        else:
            assert not text.strip()
        dest = S / f"batch-100-correction-{label}-749.txt.gz"
        dest.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        assert gzip.decompress(dest.read_bytes()) == path.read_bytes()
        checks[label] = {"archive": dest.name, "rawSha256": sha(path.read_bytes()),
                         "archiveSha256": sha(dest.read_bytes())}
    for src, dest in [
        (C / "correct-batch-100-749.py", S / "batch-100-correction-recipe.py"),
        (C / "preflight-749.ps1", S / "batch-100-correction-preflight-749.ps1.txt"),
        (C / "checks-batch-100-749.ps1", S / "batch-100-correction-checks-749.ps1.txt"),
        (C / "post-batch-100-correction-749.ps1", S / "batch-100-correction-issue-recipe-749.ps1.txt"),
        (L / "preflight-749.json", S / "batch-100-correction-runner-role-749.json"),
    ]:
        shutil.copyfile(src, dest)
    save(S / "batch-100-correction-source-provenance.json", {
        "schemaVersion": 1, "batch": "100", "execution": 749,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "freshlyVerifiedFrozenInputs": 5, "freshlyVerifiedDecompressedDictionaries": 2,
        "packets": audit_result["packets"],
        "supplementCharacterPacket": "batch-100-correction-kanjidic2.xml",
        "supplementCharacterPacketSha256": sha((S / "batch-100-correction-kanjidic2.xml").read_bytes()),
        "completeSupplementCharacterRecords": ["設", "初"],
        "allRawCharacterRecordsVerified": 15,
        "freshSupplementFullFamilyRead": load(S / "batch-100-correction-selection.json")["entryIds"],
        "supplementFreshReadLimit": "Complete12-family compact extract and both complete raw records read; prior137+16 initial source inspection/reviewer evidence inherited, not freshly rereviewed.2創 example families repeat preserved originals; union163distinct families.",
        "publicEvidence": "Unchanged committed batch-100-character-public-text.txt actual Digital Daijisen創 heading/senses directly inspected; no new upstream lookup or frequency claim.",
        "attribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repositoryNOTICE.",
    })
    save(S / "execution-749.json", {
        "schemaVersion": 1, "execution": 749, "batch": "100",
        "stage": "author-corrected-awaiting-original-session-confirmations",
        "correctionBase": HEAD, "originalTeachingSnapshot": TEACHING,
        "androidSignedHead": APP, "freshOriginMain": MAIN,
        "startingState": load(C / "progress.json")["execution749StartingState"],
        "correctionDecisions": "docs/n1-sources/batch-100-correction-decisions.json",
        "reconciliation": "docs/n1-reviews/batch-100-reconciliation.json",
        "sourceProvenance": "docs/n1-sources/batch-100-correction-source-provenance.json",
        "exactTeachingDiff": "docs/n1-sources/batch-100-correction-teaching-diff.patch.gz",
        "checks": checks, "pythonTestsPassed": 52, "validatorErrors": 0, "localBudget": budget,
        "runtimeHashesVerified": 8453, "contentVersion": audit_result["contentVersion"],
        "runtimeChangedThisExecution": True, "onlyChangedTeachingFile": "kanji/創.md",
        "initialReviewsComplete": True, "textualAcceptanceComplete": False,
        "authorCorrectedAwaitingConfirmation": ["F1", "C1-establish", "H1-initial"],
        "withdrawnHypotheses": ["H1-wound"],
        "independentReviewersLaunchedThisExecution": 0, "reviewClosed": [], "published": [],
        "runtimePublished": False, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "nextAction": NEXT,
    })
    before, now = load(L / "progress-before-749.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    print("Correction source/audit/test/recipe evidence sealed; original live historical values preserved.")


def signed_identity():
    head = git("rev-parse", "HEAD")
    assert git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "HEAD^") == HEAD and not git("status", "--porcelain")
    assert git("rev-parse", "origin/main") == MAIN
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", root=A)
    runner = load(C / "runner.json")
    assert (runner["status"], runner["pid"], runner["sessionId"]) == ("running", 5920, L.name)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (748, "100", "continue")
    changes = git("-c", "core.quotepath=false", "diff", "--name-only", HEAD, "HEAD").splitlines()
    allowed = {"kanji/創.md", "manifest.json", "docs/n1-sources/batch-100-progress.json",
               "docs/n1-reviews/batch-100-reconciliation.json", "docs/n1-sources/execution-749.json"}
    assert changes and all(n in allowed or n.startswith("docs/n1-sources/batch-100-correction-")
                           for n in changes)
    from build_manifest import build_manifest
    assert build_manifest(R) == load(R / "manifest.json")
    return head


def issue():
    head = signed_identity()
    audit_result = load(S / "batch-100-correction-audit.json")
    font = load(S / "batch-100-correction-font-audit.json")
    target = C / "batch-100-correction-749-issue.txt"
    assert not target.exists()
    target.write_text(
        "Batch100: **bounded source-backed corrections frozen locally; original-reviewer confirmations pending**.\n\n"
        f"Normally signed LOCAL UNREVIEWED changed-tree checkpoint `{head}` corrects teaching "
        f"snapshot `{TEACHING}`. Two minimal unlinked examples now show founding "
        "(創立そうりつ) and formal/literary wound/injury (創傷そうしょう), using full frozen "
        "JMdict1398640/1398490 and the actual Daijisen創 block; no new word article, inferred "
        "level or frequency claim. Direct創/設 establishment and conservative創/初 beginning/"
        "genesis guards bring the list to ten direct symmetric nontransitive pairs. "
        "Exact設/初 displayed labels, unchanged articles, complete12-family supplement and "
        "both full raw character records retained. 初 is an author-supported conservative "
        "safeguard, not yet an independently confirmed defect or a universal synonym claim. "
        "F1/C1-establish/H1-initial remain partially resolved pending both original-session "
        "changed-passage confirmations; withdrawn傷-kanji hypothesis remains withdrawn "
        "(no such kanji card; the word article is a different namespace). Original reports, "
        "coverage disagreement and optional polish are preserved.\n\n"
        "Six full readings/order and two selected keys unchanged; source-onlyショウ/"
        "けず.しける allocation remains explicitly UNVERIFIED/unselected. Reused創作N2/"
        "作るN5 metadata and13/5 exclusions unchanged. Five all-mapped pairs/ten link "
        "directions/one activated baseline pair/three reused changes preserved; "
        "baseline985kanji/4942words/985strokes preserved with recorded historical exceptions. "
        f"52focused tests passed, validator0errors, regenerated contentVersion"
        f"`{audit_result['contentVersion']}`, all8453runtime hashes verified, source/reading/"
        "quiz/link/baseline/audit/budgets passed. Vocabulary consistency retains its "
        f"2122/2431pilot scope. Final actualHan scope={font['actualHanCount']}; cmaps recomputed "
        "(刂 absent in bundled subsets is not a glyph failure). Native four-font/all-Han/"
        "rendered acceptance remains pending.\n\n"
        "Evidence: docs/n1-sources/execution-749.json, batch-100-correction-decisions.json, "
        "complete source packets/provenance, exact teaching diff, audit/font/check archives; "
        "docs/n1-reviews/batch-100-reconciliation.json. No reviewer launched this execution, "
        "Android/native/rendered rerun, publication, batch101 or second runner. Live parent/"
        "decoded launcher/exact session verified; runner.lock untouched; durable control/"
        "committed evidence only; no new permission denial. Next SAME100 two serial "
        "original-session changed-passage confirmations with exact diff and supplemental "
        "full evidence, then all original Android/native/combined-main/signing/owner-push/"
        "terminal-CI/exact-immutable-ZIP/runtime-hash/budget gates. Published coverage "
        "**126/1228;1102 acceptance remainder** unchanged. Physical-phone/general-release/"
        "whole-set acceptance outstanding; project incomplete.\n",
        encoding="utf-8")
    (L / "signed-head-749.txt").write_text(head + "\n", encoding="ascii")
    print("Signed clean correction checkpoint verified; owner issue body prepared.")


def finish():
    head = signed_identity()
    issue_data = load(L / "issue-749-verified.json")
    assert issue_data["user"]["login"] == "stop-cran"
    assert issue_data["body"] == (C / "batch-100-correction-749-issue.txt").read_bytes().decode("utf-8")
    assert head in issue_data["body"]
    before, p = load(L / "progress-before-749.json"), load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    audit_result = load(S / "batch-100-correction-audit.json")
    state = {
        "schemaVersion": 1, "execution": 749, "checkpoint": 749, "batch": "100",
        "savedCommit": head, "signature": "G", "correctionBase": HEAD,
        "originalTeachingSnapshot": TEACHING, "freshOriginMain": MAIN,
        "androidSignedHead": APP, "evidence": "docs/n1-sources/execution-749.json",
        "reconciliation": "docs/n1-reviews/batch-100-reconciliation.json",
        "contentVersion": audit_result["contentVersion"], "initialReviewsComplete": True,
        "textualAcceptanceComplete": False, "authorCorrectedAwaitingConfirmation": [
            "F1", "C1-establish", "H1-initial"],
        "withdrawnHypotheses": ["H1-wound"], "runtimeDrafted": ["創"], "reviewClosed": [],
        "published": [], "runtimeChangedThisExecution": True, "runtimePublished": False,
        "independentReviewersLaunchedThisExecution": 0, "freshAndroidOrNativeClaimed": False,
        "supplementFamilies": 12, "distinctDictionaryFamilies": 163,
        "completeRawCharacterRecords": 15, "fullMetadataReadings": 6,
        "selectedReadingKeys": ["そう", "つくる"], "directKanjiGuardPairs": 10,
        "allMappedReciprocalPairs": 5, "directedLinksVerified": 10,
        "activatedBaselinePairs": 1, "changedReusedArticles": 3, "newWords": 0,
        "pythonTestsPassed": 52, "validatorErrors": 0, "runtimeHashesVerified": 8453,
        "actualHanCount": audit_result["actualHanCount"],
        "mainFontCmapAbsences": audit_result["pendingNativeFallbackLabels"],
        "sourceOnlyLexicalAllocation": "UNVERIFIED; explicit source-only lookup rows, both unselected",
        "publishedAdditions": 126, "remainingAdditions": 1102, "lastPublishedCommit": MAIN,
        "dedicatedWorktreesClean": True, "originalHistoricalRootValuesPreservedExactly": True,
        "originalRootKeysCompared": len(before), "ownerIssueAuthorAndExactBodyVerified": True,
        "issueUpdate": issue_data["html_url"], "parentLockTouched": False,
        "optionalHistoricalSessionHelpersAccessed": False, "actualNewPermissionDenials": [],
        "status": "continue", "stage": "batch-100-corrected-local-freeze-awaiting-original-session-confirmations",
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": NEXT, "blocker": None,
    }
    p["execution749CoordinatorCheckpoint"] = state
    p["execution749StartingState"]["status"] = "signed-local-correction-checkpoint-complete"
    p.update(checkpoint=749, status="continue", stage=state["stage"], batch="100",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == value for k, value in before.items() if k not in mutable)
    save(C / "progress.json", p)
    persisted = load(C / "progress.json")
    assert persisted == p
    assert all(persisted[k] == value for k, value in before.items() if k not in mutable)
    save(L / "checkpoint-749-final-verification.json", state)
    print(json.dumps({k: state[k] for k in [
        "checkpoint", "savedCommit", "status", "stage", "issueUpdate",
        "originalHistoricalRootValuesPreservedExactly"]}, indent=2))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "supplement", "record", "audit", "seal", "issue", "finish"])
    globals()[parser.parse_args().step]()
