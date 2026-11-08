"""Prepare one source-only N1 checkpoint without touching runtime content."""
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
L = C / "logs" / "07145dbf-b4fc-49c3-86c1-f2eee5205283"
BASE = "047c2cef6b6a48b1738f2c5957de01be481c63e1"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u52c1"
PREFIX = "batch-105-"
NEXT = (
    "SAME105 ONE bounded source-completion checkpoint BEFORE runtime draft. Initial source-only "
    "packet for frozen row116 勁 author-inspected all NINE complete member families, ONE complete "
    "raw character, FOUR existing articles, THREE actual Digital Daijisen character/勁草/雄勁 "
    "blocks and pinned NINE-path SVG, not converted. Preserve full [ケイ]/[つよ.い] in source order; "
    "proposed selection [ケイ]/[] keyけい. 勁い is search-only in full1236070; retain documented "
    "kun as qualified recognition, not ordinary spelling, not offered practice, no duplicate "
    "article. Existing 強いつよい/N5 remains unchanged; its link cannot prove 勁 allocation. "
    "ONE proposed necessary NEW雄勁ゆうけい/no inferred wordlevel; actual dictionary art/prose "
    "vigor and な筆跡 example, not generic strong substitution or an absolute art-only rule. "
    "勁草 is inspected alternate candidate, not another required article; retain literal/metaphor "
    "distinction and don't adopt raw resistant-idea gloss unrestrictedly. No written/primaryreading "
    "candidate/activatedbaselinepair; ONE proposed allmappedpair/TWO directions. 雄 has no card: "
    "retain full word metadata/plain component/no out-of-batchaddition/brokenlink; inspect full raw "
    "雄 before teachingユウ. Finish complete comparisonfamilies/actualarticles/exact displayed "
    "labels/ordinarysecondarysenses/THREE wrong existing distractors/direct symmetric NONTRANSITIVE "
    "kanji+word guards/legacyfallbacks/supportteaching/naturalexamples/exactnavigation/fullbaseline/"
    "allmapped+activatedlinks/proposedHan/fourfonts/canonical力radical/modernshapemnemonicNOTetymology/"
    "pinnedconverterplan. 強/剛/力 are semantic neighbors, NOT accepted distractors/decided guards/"
    "authorization to rewrite easier decks. Only after source completion bounded signed LOCAL "
    "UNREVIEWED draft/freeze. Every original TWOserialblind differentfamilies/serialinternaltools/"
    "originalsessionconfirmations/non-skipped qualified Android/nativeContentSyncONCE/rendered/"
    "combinedcurrentmain/normalsigning/ownerfastforward/terminalgreenCI/EVERYimmutableZIPmanifesthash/"
    "unchanged18000entries42MiBcompressed80MiBinflated56MiBretained/perfilemediasafepaths/"
    "verifiedownerissue gate remainsMANDATORY. Verify whollyclean signedheads/freshmain/"
    "liveparentancestry/decodedlauncher/exactsession. Parent13320 ownsrunner.lock: no childacquire/"
    "delete/unlock/readprobe; approvedcontrol/committedsource/frozeninputs only, no optional "
    "historicalsessionrecipes. Preserve/report/yield actualnewdenial/signinghang/uncertainownership. "
    "Published131/1228,1097acceptanceremainder unchanged;1127kanji5078words136N1labels141namedmembers"
    "+separate妖;129necessarysupportsNOTN1vocabulary. Six separatelyplaced保案派第策結retainN2/"
    "noacceptedcredit/noduplicate/relevel. CompatibleAndroid#125+#132required;oldclientsignore;"
    "qualifiedsignedbf30cdead8515739bc0e671d57a54b9a3109dd46guard+schemaonlyNOTlatestmain. "
    "Original806/104 finite192optionsets/live-default/native/rendered acceptance and ALL "
    "historical source/review/process/readdepth/image/rendition/ANR/routing/permission/OOM/"
    "phone/pending limitations unchanged, not retroaccepted; preserve execution806CoordinatorCheckpoint"
    ".nextAction and underlying full histories. Delivered900x2000NOT1080x2400/equalcomprehension/"
    "fallbackface/retention/native-speaker/effectiveness certification; no new image loop/"
    "blindreviewcredit/forcedfindingwithdrawal/modelvote/newguard from unproved hypotheses. "
    "Physicalphone/generalrelease/whole-setoutstanding;projectincomplete. No106/unreviewedpush/"
    "authoragents/concurrentheavywork/secondrunner/signingretry/guardincrease."
)
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest, sha256 as manifest_sha256
from extract_n1_jmdict import extract

sys.stdout.reconfigure(encoding="utf-8")


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".807.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n",
                         encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8").strip()


def clean(root, head):
    assert git("rev-parse", "HEAD", root=root) == head
    assert git("log", "-1", "--format=%G?", root=root) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=root)


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
    clean(R, BASE)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == BASE
    assert git("branch", "--show-current") == "content/n1-kanji"
    runner = load(C / "runner.json")
    assert runner["pid"] == 13320 and runner["status"] == "running"
    assert runner["sessionId"] == L.name
    role_script = r"""
$ErrorActionPreference='Stop'
$id=$PID; $chain=@()
for($i=0;$i -lt 6 -and $id;$i++){
 $x=Get-CimInstance Win32_Process -Filter "ProcessId=$id"
 if(-not $x){break}
 $chain+=@{pid=[int]$x.ProcessId;parent=[int]$x.ParentProcessId;name=$x.Name}
 $id=$x.ParentProcessId
}
$r=Get-CimInstance Win32_Process -Filter 'ProcessId=13320'
if(-not $r){throw 'Expected parent launcher absent'}
$encoded=($r.CommandLine -split '-EncodedCommand ')[1]
$decoded=[Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($encoded))
@{chain=$chain;decodedLauncher=$decoded}|ConvertTo-Json -Depth 5 -Compress
"""
    role = json.loads(subprocess.check_output(
        ["pwsh", "-NoProfile", "-NonInteractive", "-Command", role_script],
        encoding="utf-8"))
    assert 13320 in [p["pid"] for p in role["chain"]]
    assert str(C / "runner.ps1") in role["decodedLauncher"]
    role.update(liveParentPid=13320, sessionId=L.name, lockTouched=False,
                role="Child inherits live parent protection; no lock acquisition/read/delete/unlock.")
    save(L / "preflight-807.json", role)
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (806, "104", "continue")
    assert p["remainingAdditions"] == 1097 and p["lastPublishedCommit"] == BASE
    assert not list(S.glob(PREFIX + "*"))
    request = (L / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    cp = json.loads(text.split(marker, 1)[1])
    assert cp["checkpoint"] == 806 and cp["lastPublishedCommit"] == BASE
    assert not (L / "progress-before-807.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-807.json")
    state = {
        "execution": 807, "batch": "105", "startingHead": BASE,
        "freshOriginMain": BASE, "androidHead": APP,
        "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "ONE bounded batch105 source-preparation checkpoint only. No runtime draft, reviewer, Android/native, publication,106 or second runner.",
        "request": {"sha256": sha(request), "bytes": len(request),
                    "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and complete embedded checkpoint parsed. Operative contract, approved issue and final806 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only. No optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; freshly fetched main equals content. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
    }
    p["execution807StartingState"] = state
    p.update(batch="105", stage="batch-105-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting source-only scope persisted; complete live history retained.")


def packet():
    snapshot, inputs, jm, kd = frozen()
    assert load(C / "progress.json")["batch"] == "105"
    row = next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert row["sourceRow"] == 116
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[115] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "105", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen JMdict family containing U+52C1 in any keb; preserve all aliases/readings/restrictions/senses.",
        "limits": "Extraction alone is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / (PREFIX + "jmdict.xml")).write_bytes(raw)
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(kd.find("header")))
    selected.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == CHAR)))
    ET.indent(selected, space="  ")
    kd_raw = ET.tostring(selected, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / (PREFIX + "kanjidic2.xml")).write_bytes(kd_raw)
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "105", "baseCommit": BASE,
        "sourceIndexRecord": row, "characters": [CHAR],
        "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha(kd_raw),
        "provenance": "Complete frozen character record/header parsed and reserialized.",
        "dictionaryAttribution": "Copyright James William Breen and EDRDG; CC BY-SA4.0; repository NOTICE.",
    })
    candidates = []
    for path in sorted((R / "words").glob("*.md")):
        name = path.relative_to(R).as_posix()
        m = metadata(R, name)
        if CHAR in m.get("kanji", []) or CHAR in m["word"]:
            candidates.append({"article": name, "metadata": m,
                               "sha256": sha(path.read_bytes())})
    save(S / (PREFIX + "source-navigation.json"), {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [r for r in load(S / "baseline-word-candidates.json")
                          if r["kanji"] == CHAR],
    })
    progress = {
        "schemaVersion": 1, "batch": "105", "baseCommit": BASE,
        "membership": [CHAR], "sourceRows": [116],
        "members": [{"kanji": CHAR, "sourceRow": 116}],
        "selectionReason": "Next absent frozen row after accepted 劾. Name-use classification, alternate spellings of strong and potential strength/rigidity overlap warrant a bounded single-character source scope; deferred earlier rows remain pending.",
        "status": "initial-source-packet-only", "drafted": [], "reviewClosed": [],
        "published": [], "sourcePreparationComplete": False,
        "runtimeChanged": False, "runtimePublished": False,
        "sourceReadingOrder": {k: row["metadata"][k] for k in ("onyomi", "kunyomi")},
        "publishedAdditions": 131, "remainingAdditions": 1097,
        "limits": "Member-family extraction/navigation only. Reading allocation/usefulness, comparison families, quiz/link/font/stroke plan and actual inspection remain required; no acceptance credit.",
    }
    save(S / (PREFIX + "membership.json"), progress)
    save(S / (PREFIX + "progress.json"), progress)
    print(json.dumps({"families": len(ids), "candidateArticles": candidates},
                     ensure_ascii=True, indent=2))


def archive():
    class FirstDictionaryBlock(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.finished = False
            self.parts = []

        def handle_starttag(self, tag, attrs):
            if tag == "div":
                if self.depth:
                    self.depth += 1
                elif not self.finished and "kijiWrp" in dict(attrs).get("class", "").split():
                    self.depth = 1
            if self.depth and tag in {"p", "h2", "h3", "br", "li"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "div" and self.depth:
                self.depth -= 1
                if not self.depth:
                    self.finished = True

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    receipts = []
    for label, encoded, expected in [
        ("character", "%E5%8B%81", ["ケイ", "つよい", "人名用漢字", "雄勁"]),
        ("keisou", "%E5%8B%81%E8%8D%89", ["けいそう", "風雪", "思想", "節操"]),
        ("yuukei", "%E9%9B%84%E5%8B%81", ["ゆうけい", "形動", "書画", "詩文", "筆跡"]),
    ]:
        source = C / f"batch-105-{label}.html"
        raw = source.read_bytes()
        parser = FirstDictionaryBlock()
        parser.feed(raw.decode("utf-8"))
        text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                         if line.strip()) + "\n"
        assert parser.finished and all(word in text for word in expected), (label, text)
        target = S / (PREFIX + label + "-public-text.txt")
        target.write_text(text, encoding="utf-8")
        page = S / (PREFIX + label + ".html.gz")
        page.write_bytes(gzip.compress(raw, mtime=0))
        receipts.append({
            "url": "https://www.weblio.jp/content/" + encoded,
            "downloadedAt": datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).isoformat(),
            "rawBytes": len(raw), "rawSha256": sha(raw), "archive": page.name,
            "archiveSha256": sha(page.read_bytes()), "losslessGzip": True,
            "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
            "inspectedBlocks": "Actual Digital Daijisen first dictionary block, exact heading/reading and complete short entry. Other dictionary/automatic-example/neighbor blocks not adopted.",
            "limits": "Coordinator retrieval and author inspection, not independent reviewer upstream lookup. Text extraction removes markup; raw page retained for checking context.",
        })
        assert gzip.decompress(page.read_bytes()) == raw
        print(label + ":\n" + text)
    save(S / (PREFIX + "public-source-receipts.json"), receipts)
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    svg = (C / "inputs" / "n1-052c1-70a0b7ae.svg").read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"]
    assert len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 9
    assert [p.attrib["id"] for p in paths] == [f"kvg:052c1-s{i}" for i in range(1, 10)]
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    (S / (PREFIX + "kanjivg.svg")).write_bytes(svg)
    save(S / (PREFIX + "stroke-evidence.json"), {
        "revision": snapshot["kanjivg"]["revision"], "gitBlob": blob,
        "sha256": sha(svg), "bytes": len(svg), "dictionaryStrokeCount": 9,
        "sourceStrokePaths": 9, "converted": False, "nativeDrawingAccepted": False,
        "converterNormalizedSha256": converter,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/052c1.svg",
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repository NOTICE.",
        "limits": "Pinned SVG identity/order/count, not converted geometry, native drawing, font acceptance or historical formation.",
    })
    p = load(S / (PREFIX + "progress.json"))
    p.update(sourceObservations=PREFIX + "source-observations.json",
             nextAction="SAME105 source completion before runtime drafting; see source observations and all original issue60 gates.")
    save(S / (PREFIX + "progress.json"), p)


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(c) for c in element))


def audit():
    snapshot, inputs, jm, kd = frozen()
    ids = [e.findtext("ent_seq") for e in jm.findall("entry")
           if any(CHAR in k.text for k in e.findall("k_ele/keb"))]
    assert ids == load(S / (PREFIX + "lexical-selection.json"))["entryIds"]
    assert len(ids) == len(set(ids)) == 9
    assert (S / (PREFIX + "jmdict.xml")).read_bytes() == extract(
        inputs["n1-implementation-JMdict_e.gz"],
        snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    original = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert canonical(original) == canonical(ET.parse(
        S / (PREFIX + "kanjidic2.xml")).getroot().find("character"))
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["kanji"] == CHAR)
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    assert git("rev-parse", "HEAD") == BASE and git("rev-parse", "origin/main") == BASE
    clean(A, APP)
    before, now = load(L / "progress-before-807.json"), load(C / "progress.json")
    mutable = {"batch", "stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    observations = load(S / (PREFIX + "source-observations.json"))
    assert observations["authorInspection"]["completeMemberFamilies"] == len(ids)
    assert [(r["kind"], r["reading"]) for r in observations["readingObservations"]] == [
        ("on", "\u30b1\u30a4"), ("kun", "\u3064\u3088.\u3044")]
    assert all(set(r["entryIds"]) <= set(ids) for r in observations["readingObservations"])
    navigation = load(S / (PREFIX + "source-navigation.json"))
    assert navigation["candidates"] == [] and navigation["baselinePairs"] == []
    primary_candidates = []
    for path in (R / "words").glob("*.md"):
        m = metadata(R, path.relative_to(R).as_posix())
        if m["reading"] in {"\u3086\u3046\u3051\u3044", "\u3051\u3044\u305d\u3046"}:
            primary_candidates.append({"article": path.relative_to(R).as_posix(),
                                       "reading": m["reading"], "word": m["word"]})
    for record in load(S / (PREFIX + "public-source-receipts.json")):
        raw = (S / record["archive"]).read_bytes()
        assert sha(raw) == record["archiveSha256"]
        assert sha(gzip.decompress(raw)) == record["rawSha256"]
        assert sha((S / record["extractedText"]).read_bytes()) == record["extractedTextSha256"]
    svg = (S / (PREFIX + "kanjivg.svg")).read_bytes()
    assert sha(svg) == load(S / (PREFIX + "stroke-evidence.json"))["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 9
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    runtime_count = 0
    for section in ("files", "images", "scenes", "audio", "listening", "curriculum",
                    "listeningTasks", "listeningTaskAudio", "listeningTaskImages"):
        for name, digest in manifest.get(section, {}).items():
            actual = (sha((R / name).read_bytes()) if section in
                      {"images", "audio", "listeningTaskAudio", "listeningTaskImages"}
                      else manifest_sha256(R / name))
            assert actual == digest, name
            runtime_count += 1
    snapshots = {}
    for name in observations["authorInspection"]["existingArticlesReadCompletely"]:
        raw = (R / name).read_bytes()
        snapshots[name] = {"sha256": sha(raw), "bytes": len(raw),
                           "metadata": metadata(R, name)}
    save(S / (PREFIX + "existing-article-snapshots.json"), snapshots)
    result = {
        "schemaVersion": 1, "execution": 807, "batch": "105", "baseCommit": BASE,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": len(ids), "exactFreshExtractionMatches": True,
        "completeRawCharacterRecords": 1, "rawCharacterSemanticEquality": True,
        "sourceRow": 116, "kanji": CHAR, "metadataReadingEntries": 2,
        "runtimeBytesUnchanged": True, "runtimeManifestHashesVerified": runtime_count,
        "candidateArticles": 0, "primaryReadingCandidates": primary_candidates,
        "activatedBaselinePairs": 0, "proposedAllMappedPairs": 1,
        "proposedLinkDirections": 2, "pinnedSvgPaths": 9, "geometryConverted": False,
        "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True,
        "limits": "Mechanical packet identity and family retention, not independent review or acceptance. No fresh app/native/phone evidence. Any same-kana candidates are navigation, not verified support.",
    }
    save(S / (PREFIX + "initial-packet-audit.json"), result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    assert git("rev-parse", "HEAD") == BASE
    clean(A, APP)
    checks = {}
    for label in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                  "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{label}-807.txt").read_bytes()
        target = S / f"batch-105-{label}-807.txt.gz"
        target.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        checks[label] = {"archive": target.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                         "archiveSha256": sha(target.read_bytes())}
    tests = (L / "source-tests-807.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-807.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    audit_result = load(S / (PREFIX + "initial-packet-audit.json"))
    assert audit_result["runtimeManifestHashesVerified"] == 8466
    assert audit_result["primaryReadingCandidates"] == []
    helpers = {}
    for name in ["prepare-batch-105-807.py", "checks-batch-105-source-807.ps1",
                 "post-batch-105-source-807.ps1"]:
        target = S / (PREFIX + name)
        shutil.copyfile(C / name, target)
        assert (C / name).read_bytes() == target.read_bytes()
        helpers[target.name] = sha(target.read_bytes())
    role = load(L / "preflight-807.json")
    shutil.copyfile(L / "preflight-807.json", S / (PREFIX + "runner-role-807.json"))
    p = load(S / (PREFIX + "progress.json"))
    p.update(status="initial-source-prepared-not-authoring-ready",
             initialSourcePacketAudit=PREFIX + "initial-packet-audit.json",
             sourcePreparationComplete=False, nextAction=NEXT)
    save(S / (PREFIX + "progress.json"), p)
    save(S / "execution-807.json", {
        "schemaVersion": 1, "execution": 807, "checkpoint": 807, "batch": "105",
        "stage": "batch-105-initial-source-prepared-not-authoring-ready",
        "baseCommit": BASE, "androidSignedHead": APP, "membership": [CHAR], "sourceRows": [116],
        "sourcePacketAudit": audit_result,
        "sourceObservations": PREFIX + "source-observations.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": False,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 131, "remainingAdditions": 1097,
        "lastPublishedCommit": BASE, "physicalPhoneAcceptance": "outstanding",
        "generalReleaseAcceptance": "outstanding", "wholeProjectComplete": False,
        "actualNewPermissionDenials": [],
        "diagnostics": ["First archive execution stopped on Windows cp1252 console encoding after writing the first generated extraction. Corrected helper stdout to UTF-8, regenerated and re-audited exact source archives. Not a permission denial; no runtime content changed."],
        "nextAction": NEXT,
        "limits": "Normally signed LOCAL source-only checkpoint; no push, independent content review, app/native acceptance or runtime publication. Original checkpoints and all acceptance gates remain intact. Vocabulary checker retains its reported pilot coverage, not whole-corpus completion.",
    })
    print("Source evidence and exact check logs archived for a local signed checkpoint.")


def checkpoint():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    clean(R, head)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == BASE
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    receipt = load(L / "issue-receipt-807.json")
    assert receipt["author"] == "stop-cran" and receipt["verified"]
    before = load(L / "progress-before-807.json")
    p = load(C / "progress.json")
    assert p["checkpoint"] == 806 and p["batch"] == "105"
    changed = {"checkpoint", "status", "stage", "batch", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in changed)
    result = {
        "execution": 807, "checkpoint": 807, "batch": "105",
        "savedCommit": head, "signature": "G", "status": "continue",
        "stage": "batch-105-initial-source-prepared-not-authoring-ready",
        "baseCommit": BASE, "lastPublishedCommit": BASE,
        "membership": [CHAR], "sourceRows": [116], "completeDictionaryFamilies": 9,
        "completeRawCharacterRecords": 1, "existingArticlesReadCompletely": 4,
        "actualPublicDictionaryBlocks": 3, "metadataReadingEntries": 2,
        "proposedQuizOnyomi": ["\u30b1\u30a4"], "proposedQuizKunyomi": [],
        "proposedNecessarySupport": "words/雄勁.md",
        "pinnedSvgPaths": 9, "geometryConverted": False,
        "focusedTestsPassed": 43, "validatorErrors": 0, "runtimeHashesVerified": 8466,
        "runtimeBytesUnchanged": True, "manifestBytesUnchanged": True,
        "contentVersion": "a5bc9b199c7df334", "sourcePreparationComplete": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "dedicatedWorktreesClean": True,
        "publishedAdditions": 131, "remainingAdditions": 1097,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextBatchStarted": False,
        "actualNewPermissionDenials": [], "parentLockTouched": False,
        "optionalHistoricalHelpersAccessed": False,
        "originalHistoricalRootValuesPreserved": True,
        "originalRootKeysCompared": len(before),
        "sourceEvidence": "docs/n1-sources/execution-807.json",
        "issueUpdate": receipt["url"], "ownerIssueAuthorAndBodyVerified": True,
        "nextAction": NEXT,
    }
    p["execution807CoordinatorCheckpoint"] = result
    p["batch105SourceIssueReceipt"] = receipt
    p.update(checkpoint=807, status="continue", stage=result["stage"], batch="105",
             nextAction=NEXT, blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in changed)
    save(C / "progress.json", p)
    saved = load(C / "progress.json")
    assert all(saved[k] == v for k, v in before.items() if k not in changed)
    save(L / "checkpoint-807.json", result)
    print(json.dumps({"checkpoint": 807, "savedCommit": head,
                      "preservedHistoricalRootKeys": len(before),
                      "issueUpdate": receipt["url"], "status": "continue"}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["start", "packet", "archive", "audit", "record", "checkpoint"])
    args = parser.parse_args()
    globals()[args.stage]()
