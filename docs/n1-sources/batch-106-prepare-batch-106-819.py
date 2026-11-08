"""Freeze and audit the bounded, source-only first packet for N1 batch 106."""
import argparse
import copy
import gzip
import hashlib
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "2472a3c1-ac5f-4972-aa59-315365085f22"
BASE = "0c582f18b31f65a5e1a908d92e37dde3d34f81ee"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u52c5"
P = "batch-106-"
NEXT = (
    "SAME106 ONE bounded source-completion checkpoint BEFORE runtime draft. Initial source packet "
    "for frozen row117 勅 retains44 complete member families plus17 complete comparison families, "
    "FOUR full raw character records and FIVE actual existing articles, actual Daijisen "
    "character/nounちょく/nounみことのり and both勅令 senses, plus pinnedNINE-pathSVG/notconverted. "
    "Fullon[チョク]/fullkun[いまし.める,みことのり] EXACTSOURCEORDER; provisionalpractice[チョク]/[] "
    "keyちょく is NOT final curation. いまし.める documentedKANJIDIC2/no member lexical example; "
    "fullいましめる families戒める/誡める/警める versus縛める doNOTcontain勅. Exactmodern "
    "writtenuse/register UNVERIFIED: retain qualifiedsourceonly, no invented勅める/readingdrop/"
    "wrong-spellingallocation. みことのり IS documented1604470詔/勅/御言宣, NOTsearchonly; "
    "inspect actual▽notationguide before claiming its meaning, decide bounded usefulness. "
    "ONE proposed necessary NEW勅令ちょくれい/no inferredwordlevel, not final commitment. "
    "Daijisensense1sovereigns/sense2Meiji legal form: no universalJapanese-only/Meiji-only/"
    "ordinarycommand/everyoldedictvoid claim. No existing written or frozenactivatedmemberpair. "
    "If勅令selected TWOallmappedpairsFOURdirections include令; adding令commonword would be "
    "NEWexampleteaching, not navigation-only. Finish finalcompletecomparisonfamilies/actualarticles/"
    "exactlabels/ordinarysecondarysenses/THREEwrongexistingdistractors/directsymmetricNONTRANSITIVE"
    "kanji+wordguards/legacyfallbacks/supportnaturalexamples/readingallocation/fullbaseline/"
    "allmapped+activatedlinks/exactreusedpassages/proposedHan/fourfonts/canonical力radical/"
    "modern束+力shapemnemonicNOTetymology/pinnedconverterplan. 令commanddecree/命lifecommand/"
    "命令ordercommand are potential overlaps, NOTacceptedwrongchoices/decidedguards/authority "
    "to rewrite easierdecks. Only after source completion later bounded signedLOCALUNREVIEWED "
    "draft/freeze. Every original TWOserialblind differentfamilies/serialinternaltools/"
    "originalsessionconfirmations/non-skippedqualifiedAndroid/nativeContentSyncONCE/meaning/"
    "curatedreading/drawing/articles/Back/offline/fonts/rendered/combinedcurrentmain/fullPython/"
    "vocabulary/baseline-membership-links/manifest/perfilemedia-safepaths/normalsigning/"
    "ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/unchanged18000entries/"
    "42MiBcompressed80MiBinflated56MiBretained/verifiedownerissue remainsMANDATORY. "
    "Verifywhollyclean signedheads/freshmain/liveparentancestry/decodedlauncher/exactsession. "
    "Parent13320ownsrunner.lock:NOchildacquire/delete/unlock/readprobe;approvedcontrol/"
    "committedsource/frozeninputs only,no optional historicalsessionrecipes. Preserve/report/yield "
    "actualnewdenial/signinghang/uncertainownership. Published132/1228,1096acceptanceremainder/"
    "1128kanji5079words137N1labels142namedmembers+separate妖/130necessarysupportsNOTN1vocabulary "
    "unchanged. Sixseparatelyplaced保案派第策結retainN2/noacceptedcredit/noduplicate/relevel. "
    "CompatibleAndroid125+132required;oldclientsignore;qualifiedsignedbf30cdead8515739bc0e671d57a54b9a3109dd46"
    "guard+schemaonlyNOTlatestmain. Original818publicationand105boundedruntimeacceptance/"
    "ALLhistoricalsource/review/process/readdepth/permission/OOM/ANR/routing/rendering/phone/"
    "pendinglimits preservedNOTnew819runs/retroaccepted. Exact prior nextAction retained in "
    "execution819Inherited818Gates and before819 immutable snapshot. Originalpixels/"
    "equalcomprehension/fallbackface/everyrequestretention/native-speaker/phone/effectiveness "
    "remainUNVERIFIED;noforcedfindingwithdrawal/modelvote/newguard from unprovedhypothesis. "
    "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No107/unreviewedpush/"
    "authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as text_sha256
from extract_n1_jmdict import extract

sys.stdout.reconfigure(encoding="utf-8")


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".819.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n",
                         encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def frozen():
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == snapshot["jmdict"]["xmlSha256"]
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    return snapshot, inputs, ET.fromstring(jm), ET.fromstring(kd)


def start():
    for root, head in [(R, BASE), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == head
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    assert git("rev-parse", "origin/main") == BASE
    assert git("branch", "--show-current") == "content/n1-kanji"
    role = load(L / "preflight-819.json")
    runner = load(C / "runner.json")
    assert role["sessionId"] == runner["sessionId"] == L.name
    assert runner["pid"] == role["liveParentPid"] == 13320
    assert runner["status"] == "running" and role["lockTouched"] is False
    before = load(C / "progress.json")
    assert (before["checkpoint"], before["status"], before["batch"]) == (818, "continue", "105")
    assert before["remainingAdditions"] == 1096
    assert before["lastPublishedCommit"] == BASE
    request = (L / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    checkpoint = json.loads(text.split(marker, 1)[1])
    assert checkpoint["checkpoint"] == 818
    assert not list(S.glob(P + "*"))
    assert not (L / "progress-before-819.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-819.json")
    state = {
        "execution": 819, "batch": "106", "startingHead": BASE,
        "freshOriginMain": BASE, "androidHead": APP,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded batch106 initial source-preparation checkpoint only; no runtime draft, reviewer, Android/native, publication,107 or second runner.",
        "request": {"sha256": sha(request), "bytes": len(request),
                    "lines": len(text.splitlines()), "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed. Operative contract, complete approved issue and final818 inspected directly; historical middle parsed, not freshly semantically re-reviewed. Initial terminal output encoding error preserved; no permission denial or missing source."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only. No optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; freshly fetched main equals content. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    before["execution819StartingState"] = state
    before.update(batch="106", stage="batch-106-initial-source-preparation-in-progress",
                  nextAction=state["scope"], blocker=None)
    save(C / "progress.json", before)
    print("Starting source-only scope persisted; complete live history retained.")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "106"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 117
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[116] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    selection = {
        "schemaVersion": 1, "batch": "106", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen JMdict family containing U+52C5 in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    }
    save(S / (P + "lexical-selection.json"), selection)
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (P + "jmdict.xml")).write_bytes(raw)
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == CHAR)))
    ET.indent(selected, space="  ")
    kd_raw = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / (P + "kanjidic2.xml")).write_bytes(kd_raw)
    save(S / (P + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "106", "baseCommit": BASE,
        "sourceIndexRecord": row, "characters": [CHAR],
        "rawCharacterPacket": P + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha(kd_raw),
        "provenance": "Complete frozen character record/header parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repository NOTICE.",
    })
    candidates = []
    inventory = {}
    for folder in ("kanji", "words"):
        for path in sorted((R / folder).glob("*.md")):
            name = path.relative_to(R).as_posix()
            m = metadata(R, name)
            inventory[name] = {"metadata": m, "sha256": sha(path.read_bytes())}
            if folder == "words" and (CHAR in m.get("kanji", []) or CHAR in m["word"]):
                candidates.append({"article": name, **inventory[name]})
    save(S / (P + "baseline-plan.json"), {
        "schemaVersion": 1, "batch": "106", "baseCommit": BASE,
        "inventory": inventory, "runtimeManifest": load(R / "manifest.json"),
        "manifestRawSha256": sha((R / "manifest.json").read_bytes()),
        "limits": "Complete current metadata/byte baseline, not a fresh linguistic review of unchanged articles.",
    })
    save(S / (P + "source-navigation.json"), {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json")
                          if r["kanji"] == CHAR],
    })
    progress = {
        "schemaVersion": 1, "batch": "106", "baseCommit": BASE,
        "membership": [CHAR], "sourceRows": [117],
        "members": [{"kanji": CHAR, "sourceRow": 117}],
        "selectionReason": "Next absent frozen row after accepted 勁. Imperial-order vocabulary and two nonroutine kun readings require a bounded single-character full-family audit; deferred earlier rows remain pending.",
        "status": "initial-source-packet-only", "drafted": [], "reviewClosed": [],
        "published": [], "sourcePreparationComplete": False,
        "runtimeChanged": False, "runtimePublished": False,
        "sourceReadingOrder": {k: row["metadata"][k] for k in ("onyomi", "kunyomi")},
        "publishedAdditions": 132, "remainingAdditions": 1096,
        "limits": "Member-family extraction/navigation only. Reading allocation/usefulness, comparison families, quiz/link/font/stroke plan and actual inspection remain required; no acceptance credit.",
    }
    save(S / (P + "membership.json"), progress)
    save(S / (P + "progress.json"), progress)
    print(json.dumps({"families": len(ids), "candidateArticles": candidates},
                     ensure_ascii=False, indent=2))


def archive():
    class DictionaryBlocks(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.parts = []
            self.blocks = []

        def handle_starttag(self, tag, attrs):
            if tag == "div":
                if self.depth:
                    self.depth += 1
                elif "kijiWrp" in dict(attrs).get("class", "").split():
                    self.depth = 1
            if self.depth and tag in {"p", "h2", "h3", "br", "li"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "div" and self.depth:
                self.depth -= 1
                if not self.depth:
                    self.blocks.append("\n".join(
                        line.strip() for line in "".join(self.parts).splitlines()
                        if line.strip()) + "\n")
                    self.parts = []

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    receipts = []
    for label, encoded, count, expected in [
        ("character", "%E5%8B%85", 1, ["チョク", "みことのり", "天子", "詔／▽勅"]),
        ("chokurei", "%E5%8B%85%E4%BB%A4", 1, ["ちょくれい", "国王", "明治憲法下"]),
    ]:
        source = C / f"batch-106-{label}-819.html"
        raw = source.read_bytes()
        parser = DictionaryBlocks()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(parser.blocks[:count])
        assert len(parser.blocks) >= count and all(word in text for word in expected), (label, text)
        target = S / (P + label + "-public-text.txt")
        target.write_text(text, encoding="utf-8")
        page = S / (P + label + ".html.gz")
        page.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(page.read_bytes()) == raw
        receipts.append({
            "url": "https://www.weblio.jp/content/" + encoded,
            "downloadedAt": datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).isoformat(),
            "rawBytes": len(raw), "rawSha256": sha(raw), "archive": page.name,
            "archiveSha256": sha(page.read_bytes()), "losslessGzip": True,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "inspectedBlocks": f"First {count} Digital Daijisen dictionary wrapper, including every headword/reading/sense inside it; other aggregator wrappers not adopted.",
            "limits": "Coordinator retrieval and author inspection, not independent upstream reviewer lookup. Markup stripped in extraction; original raw page retained. Entire later page not semantically inspected.",
        })
        print(label + ":\n" + text)
    save(S / (P + "public-source-receipts.json"), receipts)
    snapshot, inputs, jm, kd = frozen()
    row = load(S / (P + "input-metadata.json"))["sourceIndexRecord"]
    svg = (C / "inputs" / "n1-052c5-70a0b7ae.svg").read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"]
    assert len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 9
    assert [p.attrib["id"] for p in paths] == [f"kvg:052c5-s{i}" for i in range(1, 10)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    (S / (P + "kanjivg.svg")).write_bytes(svg)
    save(S / (P + "stroke-evidence.json"), {
        "revision": snapshot["kanjivg"]["revision"], "gitBlob": blob,
        "sha256": sha(svg), "bytes": len(svg), "dictionaryStrokeCount": 9,
        "sourceStrokePaths": 9, "converted": False, "nativeDrawingAccepted": False,
        "converterNormalizedSha256": converter,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/052c5.svg",
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repository NOTICE.",
        "limits": "Pinned SVG identity/order/count, not converted geometry, native drawing, font acceptance or historical formation.",
    })
    member_ids = set(load(S / (P + "lexical-selection.json"))["entryIds"])
    terms = {"令", "命", "束", "命令", "命じる", "命ずる", "天皇"}
    comparison_ids = [e.findtext("ent_seq") for e in jm.findall("entry")
                      if e.findtext("ent_seq") not in member_ids
                      and (any(k.text in terms for k in e.findall("k_ele/keb"))
                           or any(r.text == "いましめる" for r in e.findall("r_ele/reb")))]
    save(S / (P + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "106", "entryIds": comparison_ids,
        "selectionRule": "Complete frozen families with exact keb among 令/命/束/命令/命じる/命ずる/天皇 or rebいましめる, excluding already selected complete member families.",
        "limits": "Bounded navigation supplement, not the complete final comparison/quiz evidence or a claim that unlisted homographs do not exist.",
    })
    (S / (P + "comparisons.xml")).write_bytes(extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], comparison_ids))
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    for char in "令命束":
        selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                          if e.findtext("literal") == char)))
    ET.indent(selected, space="  ")
    (S / (P + "comparison-kanjidic2.xml")).write_bytes(
        ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n")
    print("Supplemental complete families:", len(comparison_ids))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(c) for c in element))


def audit():
    snapshot, inputs, jm, kd = frozen()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    assert ids == load(S / (P + "lexical-selection.json"))["entryIds"]
    assert len(ids) == len(set(ids)) == 44
    expected_hash = snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"]
    for label, selection in [("jmdict", "lexical-selection"), ("comparisons", "comparison-selection")]:
        entry_ids = load(S / (P + selection + ".json"))["entryIds"]
        assert (S / (P + label + ".xml")).read_bytes() == extract(
            inputs["n1-implementation-JMdict_e.gz"], expected_hash, entry_ids)
    comparisons = load(S / (P + "comparison-selection.json"))["entryIds"]
    assert len(comparisons) == len(set(comparisons)) == 17
    assert not set(ids) & set(comparisons)
    for label, chars in [("kanjidic2", CHAR), ("comparison-kanjidic2", "令命束")]:
        raw_root = ET.parse(S / (P + label + ".xml")).getroot()
        assert canonical(raw_root.find("header")) == canonical(kd.find("header"))
        assert [e.findtext("literal") for e in raw_root.findall("character")] == list(chars)
        for char in chars:
            original = next(e for e in kd.findall("character") if e.findtext("literal") == char)
            actual = next(e for e in raw_root.findall("character") if e.findtext("literal") == char)
            assert canonical(actual) == canonical(original)
    row = load(S / (P + "input-metadata.json"))["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 117
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    for path in ("kanji", "words", "articles", "strokes", "manifest.json", "tools"):
        assert not git("diff", BASE, "--", path)
    assert git("rev-parse", "HEAD") == BASE and git("rev-parse", "origin/main") == BASE
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    before, now = load(L / "progress-before-819.json"), load(C / "progress.json")
    mutable = {"batch", "stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    baseline = load(S / (P + "baseline-plan.json"))
    for name, record in baseline["inventory"].items():
        assert sha((R / name).read_bytes()) == record["sha256"]
        assert metadata(R, name) == record["metadata"]
    assert sha((R / "manifest.json").read_bytes()) == baseline["manifestRawSha256"]
    observations = load(S / (P + "source-observations.json"))
    assert observations["authorInspection"]["completeMemberFamilies"] == len(ids)
    assert observations["authorInspection"]["completeComparisonFamilies"] == len(comparisons)
    assert [(r["kind"], r["reading"]) for r in observations["readingObservations"]] == [
        ("on", "チョク"), ("kun", "いまし.める"), ("kun", "みことのり")]
    assert row["metadata"]["onyomi"] == ["チョク"]
    assert row["metadata"]["kunyomi"] == ["いまし.める", "みことのり"]
    navigation = load(S / (P + "source-navigation.json"))
    assert navigation["candidates"] == [] and navigation["baselinePairs"] == []
    primary_candidates = []
    for name, record in baseline["inventory"].items():
        m = record["metadata"]
        if name.startswith("words/") and m["reading"] in {"ちょくれい", "ちょく", "みことのり", "いましめる"}:
            primary_candidates.append({"article": name, "reading": m["reading"], "word": m["word"]})
    for record in load(S / (P + "public-source-receipts.json")):
        raw = (S / record["archive"]).read_bytes()
        assert sha(raw) == record["archiveSha256"]
        assert sha(gzip.decompress(raw)) == record["rawSha256"]
        assert sha((S / record["extractedText"]).read_bytes()) == record["extractedTextSha256"]
    character_text = (S / (P + "character-public-text.txt")).read_text(encoding="utf-8")
    assert character_text.count("読み方：") == 3
    assert "ウィキペディア" not in character_text and "歴史民俗用語辞典" not in character_text
    svg = (S / (P + "kanjivg.svg")).read_bytes()
    assert sha(svg) == load(S / (P + "stroke-evidence.json"))["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 9
    manifest = load(R / "manifest.json")
    assert manifest == baseline["runtimeManifest"] == build_manifest(R)
    runtime_count = 0
    for section in ("files", "images", "scenes", "audio", "listening", "curriculum",
                    "listeningTasks", "listeningTaskAudio", "listeningTaskImages"):
        for name, digest in manifest.get(section, {}).items():
            actual = (sha((R / name).read_bytes()) if section in
                      {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                      else text_sha256(R / name))
            assert actual == digest, name
            runtime_count += 1
    assert runtime_count == 8469
    snapshots = {}
    for name in observations["authorInspection"]["existingArticlesReadCompletely"]:
        raw = (R / name).read_bytes()
        snapshots[name] = {"sha256": sha(raw), "bytes": len(raw), "metadata": metadata(R, name)}
    save(S / (P + "existing-article-snapshots.json"), snapshots)
    result = {
        "schemaVersion": 1, "execution": 819, "batch": "106", "baseCommit": BASE,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": len(ids), "completeComparisonFamilies": len(comparisons),
        "exactFreshExtractionsMatch": True, "completeRawCharacterRecords": 4,
        "rawCharacterSemanticEquality": True, "sourceRow": 117, "kanji": CHAR,
        "metadataReadingEntries": 3, "runtimeBytesUnchanged": True,
        "runtimeManifestHashesVerified": runtime_count, "candidateArticles": 0,
        "primaryReadingCandidates": primary_candidates, "activatedBaselinePairs": 0,
        "proposedAllMappedPairsIfChokureiSelected": 2, "proposedLinkDirections": 4,
        "pinnedSvgPaths": 9, "geometryConverted": False, "fontAcceptance": "pending",
        "baselineKanjiMetadataAndBytesPreserved": sum(n.startswith("kanji/") for n in baseline["inventory"]),
        "baselineWordMetadataAndBytesPreserved": sum(n.startswith("words/") for n in baseline["inventory"]),
        "contentVersion": manifest["contentVersion"], "originalHistoricalRootValuesPreserved": True,
        "originalRootKeysCompared": len(before),
        "memberPacketLines": len((S / (P + "jmdict.xml")).read_text(encoding="utf-8").splitlines()),
        "comparisonPacketLines": len((S / (P + "comparisons.xml")).read_text(encoding="utf-8").splitlines()),
        "limits": "Mechanical packet identity/full-family retention/baseline hashes, not independent linguistic review or acceptance. Final source completion, reading dispositions, quiz/link/font/native/publication gates remain. No fresh app/native/phone evidence.",
    }
    save(S / (P + "initial-packet-audit.json"), result)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def record():
    assert git("rev-parse", "HEAD") == BASE
    checks = {}
    for label in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                  "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{label}-819.txt").read_bytes()
        target = S / f"batch-106-{label}-819.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw),
                         "rawSha256": sha(raw), "archiveSha256": sha(target.read_bytes())}
    tests = (L / "source-tests-819.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-819.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    audit_result = load(S / (P + "initial-packet-audit.json"))
    helpers = {}
    for name in ["prepare-batch-106-819.py", "checks-batch-106-source-819.ps1",
                 "preflight-819.ps1", "post-batch-106-source-819.ps1"]:
        target = S / (P + name)
        shutil.copyfile(C / name, target)
        assert (C / name).read_bytes() == target.read_bytes()
        helpers[target.name] = sha(target.read_bytes())
    role = load(L / "preflight-819.json")
    shutil.copyfile(L / "preflight-819.json", S / (P + "runner-role-819.json"))
    p = load(S / (P + "progress.json"))
    p.update(status="initial-source-prepared-not-authoring-ready",
             initialSourcePacketAudit=P + "initial-packet-audit.json",
             sourceObservations=P + "source-observations.json",
             sourcePreparationComplete=False, nextAction=NEXT)
    save(S / (P + "progress.json"), p)
    save(S / "execution-819.json", {
        "schemaVersion": 1, "execution": 819, "checkpoint": 819, "batch": "106",
        "stage": "batch-106-initial-source-prepared-not-authoring-ready",
        "baseCommit": BASE, "androidSignedHead": APP, "membership": [CHAR], "sourceRows": [117],
        "sourcePacketAudit": audit_result, "sourceObservations": P + "source-observations.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 132, "remainingAdditions": 1096,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "actualNewPermissionDenials": [], "nextAction": NEXT,
        "diagnostics": load(S / (P + "source-observations.json"))["diagnostics"],
        "limits": "Normally signed LOCAL source-only checkpoint; no push, independent content review, app/native acceptance or runtime publication. Original checkpoints and all acceptance gates remain intact. Vocabulary checker retains its reported pilot coverage, not whole-corpus completion.",
    })
    print("Source evidence and exact check logs archived for a local signed checkpoint.")


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    for root, expected in [(R, head), (A, APP)]:
        assert git("rev-parse", "HEAD", root=root) == expected
        assert git("log", "-1", "--format=%G?", root=root) == "G"
        assert not git("status", "--porcelain", "--untracked-files=all", root=root)
    assert git("rev-parse", "origin/main") == BASE
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    receipt = load(L / "issue-receipt-819.json")
    assert receipt["author"] == "stop-cran" and receipt["verified"]
    before = load(L / "progress-before-819.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 818 and p["batch"] == "106"
    changed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in changed)
    audit_result = load(S / (P + "initial-packet-audit.json"))
    result = {
        "execution": 819, "checkpoint": 819, "batch": "106", "savedCommit": head,
        "signature": "G", "status": "continue",
        "stage": "batch-106-initial-source-prepared-not-authoring-ready",
        "baseCommit": BASE, "lastPublishedCommit": BASE,
        "membership": [CHAR], "sourceRows": [117], "completeDictionaryFamilies": 61,
        "memberFamilies": 44, "comparisonFamilies": 17, "completeRawCharacterRecords": 4,
        "existingArticlesReadCompletely": 5, "actualPublicDictionaryHeadwords": 4,
        "metadataReadingEntries": 3, "provisionalQuizOnyomi": ["チョク"],
        "provisionalQuizKunyomi": [], "proposedNecessarySupport": "words/勅令.md",
        "supportAndCurationFinal": False, "pinnedSvgPaths": 9, "geometryConverted": False,
        "focusedTestsPassed": 43, "validatorErrors": 0,
        "runtimeHashesVerified": 8469, "runtimeBytesUnchanged": True,
        "manifestBytesUnchanged": True, "contentVersion": audit_result["contentVersion"],
        "sourcePreparationComplete": False, "runtimeDrafted": [], "reviewClosed": [],
        "published": [], "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "publishedAdditions": 132, "remainingAdditions": 1096,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False, "originalHistoricalRootValuesPreserved": True,
        "originalRootKeysCompared": len(before), "sourceEvidence": "docs/n1-sources/execution-819.json",
        "issueUpdate": receipt["url"], "ownerIssueAuthorAndBodyVerified": True, "nextAction": NEXT,
    }
    p["execution819CoordinatorCheckpoint"] = result
    p["execution819Inherited818Gates"] = {
        "checkpoint": 818, "nextAction": before["nextAction"],
        "invariant": "Preserve exact inherited gates/limitations; source-only819 does not retroaccept or waive them.",
    }
    p["batch106SourceIssueReceipt"] = receipt
    p.update(checkpoint=819, status="continue", stage=result["stage"], batch="106",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in changed)
    save(C / "progress.json", p)
    saved = load(C / "progress.json")
    assert all(saved[k] == v for k, v in before.items() if k not in changed)
    save(L / "checkpoint-819.json", result)
    print(json.dumps({"checkpoint": 819, "savedCommit": head,
                      "preservedHistoricalRootKeys": len(before),
                      "issueUpdate": receipt["url"], "status": "continue"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("start", "packet", "archive", "audit", "record", "checkpoint"))
    args = parser.parse_args()
    globals()[args.stage]()
