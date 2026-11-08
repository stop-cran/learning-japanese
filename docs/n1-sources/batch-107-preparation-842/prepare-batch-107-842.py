"""Preserve the initial, source-only packet for N1 batch 107."""
import argparse
import copy
import gzip
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "rollout-recovered" / "learning-japanese"
A = C.parent / "rollout-recovered" / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "69167545-b703-4e71-81c9-45610a3fe234"
BASE = "476f429108415d00f9d41863af9d2f9470b5bbc0"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u52d8"
PREFIX = "batch-107-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest
from freeze_n1_sources import metadata_record


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args],
        encoding="utf-8",
    ).strip()


def save(path, value):
    temporary = path.with_name(path.name + ".842.tmp")
    if temporary.exists():
        raise FileExistsError(temporary)
    temporary.write_text(
        json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8"
    )
    assert load(temporary) == value
    temporary.replace(path)


def new(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def xml_bytes(root):
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def unicode_radicals(inputs):
    radicals = {}
    for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines():
        fields = line.split(";")
        cp = int(fields[0], 16)
        if 0x2F00 <= cp <= 0x2FD5:
            radicals[cp - 0x2F00 + 1] = chr(int(fields[5].split()[-1], 16))
    assert len(radicals) == 214
    return radicals


def current():
    runner = load(C / "runner.json")
    assert runner["status"] == "running" and runner["sessionId"] == L.name
    assert runner["pid"] == 31724
    p = load(C / "progress.json")
    assert p["checkpoint"] == 841 and p["status"] == "continue"
    assert p["remainingAdditions"] == 1095 and p["lastPublishedCommit"] == BASE
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    assert git("rev-parse", "origin/main") == BASE
    return p


def start():
    p = current()
    assert p["batch"] == "106" and git("rev-parse", "HEAD") == BASE
    assert git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    role = load(L / "preflight-842.json")
    assert role["liveParentPid"] == 31724 and role["lockTouched"] is False
    assert not list(S.glob(PREFIX + "*"))
    request = (L / "request.txt").read_bytes()
    text = request.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    checkpoint = json.loads(text.split(marker, 1)[1])
    assert checkpoint["checkpoint"] == p["checkpoint"]
    assert load(L / "checkpoint-full.json") == p
    projected_publication = copy.deepcopy(checkpoint["batch106PublicationCheckpoint"])
    full_publication = copy.deepcopy(p["batch106PublicationCheckpoint"])
    for left, right in ((projected_publication, full_publication),
                        (projected_publication["terminalCi"], full_publication["terminalCi"])):
        assert datetime.fromisoformat(left["recordedAt"]) == datetime.fromisoformat(right["recordedAt"])
        left.pop("recordedAt")
        right.pop("recordedAt")
    assert projected_publication == full_publication
    assert p["execution792HistoryCorrection"]["ownerReportCorrection"].startswith("https://github.com/")
    before = L / "progress-before-842.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 842, "batch": "107", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": BASE, "androidHead": APP, "freshOriginMain": BASE,
        "scope": "One initial source-only packet for batch107; no runtime draft, independent review, HOST/native check, publication or batch108.",
        "request": {
            "sha256": sha(request), "bytes": len(request), "lines": len(text.splitlines()),
            "completeFileLoadedAndCheckpointParsed": True,
            "limits": "Complete file loaded/decoded and final checkpoint parsed; operative contract and current recovery/publication inspected directly. Historical embedded records parsed, not freshly semantically re-reviewed.",
        },
        "runnerPreflight": role,
        "artifactPathPreflight": "Committed sources and frozen approved workspace inputs only; reusable helper in control. No optional historical-session helpers accessed.",
        "diagnostics": [
            "Historical -EncodedCommand preflight failed before Git/source writes; direct process inspection authenticated recovered exact -File runner.ps1, actual PID31724 and coordinator22036.",
            "Read-only row inspection initially failed on cp1252 output; ASCII-escaped JSON corrected output, not a permission denial or source failure.",
            "Initial start check rejected identical timestamp instants serialized at +01:00 in the PowerShell projection and +00:00 in full progress. Full immutable checkpoint equals live exactly; both timestamp instants and every other publication field verified before saving. Original failure preserved.",
        ],
        "parentLockTouched": False, "actualNewPermissionDenials": [],
    }
    p["execution842StartingState"] = state
    p.update(batch="107", stage="batch-107-initial-source-preparation-in-progress",
             nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Initial source scope saved; complete live history preserved.")


def frozen():
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert len(raw) == record["bytes"] and sha(raw) == record["sha256"], name
        inputs[name] = raw
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    assert sha(jm) == snapshot["jmdict"]["xmlSha256"]
    return snapshot, inputs, jm, ET.fromstring(kd)


def packet():
    p = current()
    assert p["batch"] == "107" and git("rev-parse", "HEAD") == BASE
    snapshot, inputs, jm, kd = frozen()
    row = next(x for x in load(S / "source-index.json") if x["kanji"] == CHAR)
    assert row["sourceRow"] == 118
    assert json.loads(inputs["n1-kanji-source-20261102.json"])[117] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    family_root = ET.Element("JMdict")
    for _, entry in ET.iterparse(io.BytesIO(jm), events=("end",)):
        if entry.tag != "entry":
            continue
        if any(CHAR in k.text for k in entry.findall("k_ele/keb")):
            family_root.append(copy.deepcopy(entry))
        entry.clear()
    ids = [e.findtext("ent_seq") for e in family_root]
    assert ids and len(ids) == len(set(ids))
    raw = xml_bytes(family_root)
    new(S / (PREFIX + "jmdict.xml"), raw)
    save(S / (PREFIX + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "107", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen JMdict family containing U+52D8 in any keb, in source order; complete aliases/readings/restrictions/senses retained.",
        "limits": "Extraction is not inspection, allocation, frequency evidence or independent review.",
    })
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, unicode_radicals(inputs)) == row["metadata"]
    readings = character.findall("reading_meaning/rmgroup/reading")
    for kind, label in (("ja_on", "onyomi"), ("ja_kun", "kunyomi")):
        assert [e.text for e in readings if e.get("r_type") == kind] == row["metadata"][label]
    assert int(character.findtext("misc/stroke_count")) == row["metadata"]["strokes"]
    assert int(next(e.text for e in character.findall("radical/rad_value")
                    if e.get("rad_type") == "classical")) == row["metadata"]["radicalNumber"]
    character_root = ET.Element("kanjidic2")
    character_root.append(copy.deepcopy(kd.find("header")))
    character_root.append(copy.deepcopy(character))
    kd_raw = xml_bytes(character_root)
    new(S / (PREFIX + "kanjidic2.xml"), kd_raw)
    save(S / (PREFIX + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "107", "baseCommit": BASE, "characters": [CHAR],
        "sourceIndexRecord": row, "rawCharacterPacket": PREFIX + "kanjidic2.xml",
        "rawCharacterPacketSha256": sha(kd_raw),
        "provenance": "Full frozen character record and header parsed and reserialized; source order preserved, nanori not selected.",
        "verifiedInputHashes": {name: record["sha256"] for name, record in snapshot["inputs"].items()},
        "dictionaryAttribution": snapshot["dictionaryAttribution"],
    })
    inventory = {}
    candidates = []
    for folder in ("kanji", "words"):
        for path in sorted((R / folder).glob("*.md")):
            name = path.relative_to(R).as_posix()
            m = metadata(R, name)
            inventory[name] = {"metadata": m, "sha256": sha(path.read_bytes())}
            if folder == "words" and (CHAR in m.get("kanji", []) or CHAR in m["word"]):
                matches = []
                for entry in family_root:
                    if (any(k.text == m["word"] for k in entry.findall("k_ele/keb"))
                            and any(e.text == m["reading"] for e in entry.findall("r_ele/reb"))):
                        matches.append(entry.findtext("ent_seq"))
                candidates.append({"article": name, **inventory[name],
                                   "candidateFamilyIds": matches,
                                   "limits": "Exact spelling/reading navigation only; restrictions, selected senses, allocation and actual prose still require inspection."})
    save(S / (PREFIX + "baseline-plan.json"), {
        "schemaVersion": 1, "batch": "107", "baseCommit": BASE, "inventory": inventory,
        "runtimeManifest": load(R / "manifest.json"),
        "manifestRawSha256": sha((R / "manifest.json").read_bytes()),
        "limits": "Complete current metadata/byte baseline, not a new linguistic review of unchanged cards.",
    })
    save(S / (PREFIX + "source-navigation.json"), {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [e for e in load(S / "baseline-word-candidates.json") if e["kanji"] == CHAR],
    })
    snapshots = [{"article": e["article"], "sha256": e["sha256"],
                  "text": (R / e["article"]).read_text(encoding="utf-8")}
                 for e in candidates]
    save(S / (PREFIX + "existing-article-snapshots.json"), snapshots)
    record = {
        "schemaVersion": 1, "batch": "107", "baseCommit": BASE,
        "membership": [CHAR], "sourceRows": [118], "members": [{"kanji": CHAR, "sourceRow": 118}],
        "selectionReason": "Next absent frozen row after accepted 勅; intuition versus counting/checking senses and three existing support candidates merit a single-character full-family audit.",
        "status": "initial-source-packet-only", "sourcePreparationComplete": False,
        "sourceReadingOrder": {key: row["metadata"][key] for key in ("onyomi", "kunyomi")},
        "drafted": [], "reviewClosed": [], "published": [], "runtimeChanged": False,
        "runtimePublished": False, "publishedAdditions": 133, "remainingAdditions": 1095,
        "limits": "All final support, quiz, link, font and stroke decisions remain pending; no accepted coverage.",
    }
    save(S / (PREFIX + "membership.json"), record)
    save(S / (PREFIX + "progress.json"), record)
    print(json.dumps({"families": len(ids), "candidateArticles": candidates}, ensure_ascii=True))


def check():
    p = current()
    assert p["batch"] == "107"
    snapshot, inputs, jm, kd = frozen()
    selected = ET.parse(S / (PREFIX + "jmdict.xml")).getroot()
    extracted_ids = []
    for _, e in ET.iterparse(io.BytesIO(jm), events=("end",)):
        if e.tag != "entry":
            continue
        if any(CHAR in k.text for k in e.findall("k_ele/keb")):
            extracted_ids.append(e.findtext("ent_seq"))
            ET.indent(e, space="  ", level=1)
            actual = selected[len(extracted_ids) - 1]
            assert ET.tostring(e).strip() == ET.tostring(actual).strip()
        e.clear()
    assert extracted_ids == load(S / (PREFIX + "lexical-selection.json"))["entryIds"]
    assert len(selected) == len(extracted_ids)
    raw_kd = ET.parse(S / (PREFIX + "kanjidic2.xml")).getroot()
    original = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    assert metadata_record(original, unicode_radicals(inputs)) == row["metadata"]
    ET.indent(original, space="  ", level=1)
    assert ET.tostring(original).strip() == ET.tostring(raw_kd.find("character")).strip()
    baseline = load(S / (PREFIX + "baseline-plan.json"))
    assert load(R / "manifest.json") == baseline["runtimeManifest"] == build_manifest(R)
    manifest_raw = (R / "manifest.json").read_bytes()
    committed_manifest = subprocess.check_output(["git", "-C", str(R), "show", BASE + ":manifest.json"])
    assert manifest_raw == committed_manifest
    assert b"\r\n" not in committed_manifest
    assert sha(committed_manifest.replace(b"\n", b"\r\n")) == baseline["manifestRawSha256"]
    save(S / (PREFIX + "manifest-representation.json"), {
        "originalCheckoutSha256": baseline["manifestRawSha256"],
        "generatedAndCommittedManifestSha256": sha(committed_manifest),
        "generatedBytesExactlyEqualPublishedGitBlob": True,
        "originalCheckoutExactlyReproducedByCrLf": True,
        "manifestObjectAndContentVersionUnchanged": True,
        "disposition": "Initial raw-hash audit failed after normal generator changed checkout CRLF to committed LF. Preserve the original baseline/raw-hash failure; verify exact committed bytes and the original checkout representation separately, not a silent baseline rewrite or relaxed hash guard.",
    })
    for name, item in baseline["inventory"].items():
        assert metadata(R, name) == item["metadata"]
        assert sha((R / name).read_bytes()) == item["sha256"]
    for item in load(S / (PREFIX + "existing-article-snapshots.json")):
        assert sha((R / item["article"]).read_bytes()) == item["sha256"]
        assert (R / item["article"]).read_text(encoding="utf-8") == item["text"]
    assert not (R / "kanji" / (CHAR + ".md")).exists()
    assert not (R / "strokes" / (CHAR + ".json")).exists()
    result = {
        "schemaVersion": 1, "execution": 842, "batch": "107", "baseCommit": BASE,
        "allFiveFrozenInputHashesVerified": True, "bothDecompressedDictionaryHashesVerified": True,
        "completeMemberFamiliesReproduced": len(selected), "rawCharacterRecordsReproduced": 1,
        "baselineArticlesUnchanged": len(baseline["inventory"]),
        "candidateArticleSnapshotsVerified": len(load(S / (PREFIX + "existing-article-snapshots.json"))),
        "allRowMetadataAndUnicodeRadicalReproduced": True,
        "manifestFreshAndUnchanged": True, "runtimeChanged": False,
        "sourcePreparationComplete": False,
        "limits": "Mechanical initial source check only; no linguistic review, final mappings, native or publication acceptance.",
    }
    save(S / (PREFIX + "initial-source-audit.json"), result)
    print(json.dumps(result))


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

    current()
    source = C / "batch-107-character-842.html"
    raw = source.read_bytes()
    parser = DictionaryBlocks()
    parser.feed(raw.decode("utf-8"))
    text = parser.blocks[0]
    assert all(term in text for term in ("カン", "かんがえる", "勘定", "考え合わせる", "直感"))
    new(S / (PREFIX + "character-public-text.txt"), text.encode("utf-8"))
    page = S / (PREFIX + "character.html.gz")
    new(page, gzip.compress(raw, mtime=0))
    assert gzip.decompress(page.read_bytes()) == raw
    save(S / (PREFIX + "public-source-receipts.json"), [{
        "url": "https://www.weblio.jp/content/%E5%8B%98",
        "downloadedAt": datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).isoformat(),
        "rawBytes": len(raw), "rawSha256": sha(raw), "archive": page.name,
        "archiveSha256": sha(page.read_bytes()), "losslessGzip": True,
        "extractedText": PREFIX + "character-public-text.txt",
        "extractedTextSha256": sha(text.encode("utf-8")),
        "scope": "First Digital Daijisen dictionary wrapper only; includes character and standalone noun headings. Other aggregator wrappers are not adopted.",
        "limits": "Coordinator retrieval and source inspection; not independent reviewer upstream lookup. Raw later page retained for provenance, not semantic review.",
    }])
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    svg = (C / "batch-107-kanjivg-842.download.svg").read_bytes()
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    root = ET.fromstring(svg)
    paths = root.findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 11
    assert [e.get("id") for e in paths] == [f"kvg:052d8-s{i}" for i in range(1, 12)]
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    new(S / (PREFIX + "kanjivg.svg"), svg)
    save(S / (PREFIX + "stroke-evidence.json"), {
        "revision": snapshot["kanjivg"]["revision"], "gitBlob": blob,
        "sha256": sha(svg), "bytes": len(svg), "dictionaryStrokeCount": 11,
        "sourceStrokePaths": 11, "converted": False, "nativeDrawingAccepted": False,
        "converterNormalizedSha256": converter,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/052d8.svg",
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repository NOTICE.",
        "limits": "Pinned geometry identity/order/count only. The SVG phon label does not itself establish historical formation or a licensed phonetic explanation; use a qualified modern-shape account unless separately verified.",
    })
    print(text.encode("ascii", errors="backslashreplace").decode())
    print("Pinned eleven-path SVG archived; no runtime conversion.")


NEXT = (
    "SAME107 bounded source completion before any runtime draft. Read committed "
    "batch-107-source-observations.json, membership, source-navigation, all92 complete "
    "JMdict families, full raw character record, exact public dictionary wrapper, "
    "pinned11-path SVG and execution-842.json. Row118 勘; frozen fullon[カン]/fullkun[] "
    "preserved; provisional practice[カン]/[]. Additional Daijisen nativeかんがえる "
    "and rare JMdict spelling勘える are supplementary recognition, not metadata "
    "extension, rare-pronunciation or invalid-reading claims. Reuse verified candidates "
    "勘かん N3,勘定かんじょう N3,勘違いかんちがい N2, preserving identities/readings/"
    "levels/originalguards; no new support presently necessary. Finish complete actual "
    "comparison families/cards/ordinary secondary meanings, THREEwrongkanji choices/"
    "direct symmetric nontransitive guards/legacy fallback plan, raw定/違 allocation/"
    "all5proposedmappedpairs10directions/3activatedbaselinepairs/exact reused passages, "
    "source-qualified shape/radical and allHan/fourfonts. No geometry converted or "
    "runtime authored, no independent review/Android/native acceptance/publication/108. "
    "Later signed LOCAL UNREVIEWED freeze only after source-ready, then original TWO "
    "serial blind different-family content reviews with actual models/serial internal "
    "tools/retained reports/evidence reconciliation/originalsession confirmations as "
    "needed; qualified signed clean bf30cde Android/no-skips HOST/native ContentSync "
    "ONCE/meaning/reading/drawing/articles/Back/offline/fonts/rendered; full source/"
    "membership/baseline/link/reading/quiz/stroke/Python/vocabulary/manifest checks; "
    "latest-main nonrewriting merge/changedteaching review/actualcombined validation/"
    "normal signing/owner scoped fastforward/terminal exact CI/EVERY immutable ZIP "
    "runtimehash/18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-"
    "safepath/verifiedownerissue gates remain mandatory before delivery or108. "
    "Normal generator converted local manifest CRLF to exact published Git LF; "
    "original baseline/failure and separate representation proof retained, no hash "
    "waiver. Preserve full live history,792 correction/report,106 acceptance and "
    "nonblocking勅/訓/いまし.める limits, all original reports/denials/OOMs/viewport/"
    "finitepool/phone limits and earlier-level source dispositions. Recovered sibling "
    "worktrees only; approved control/committed sources/frozeninputs, no optional "
    "historical session recipes. Authenticate actual -File launcher/signedheads/"
    "clean-accountedstate/currentcheckpoint/session/liveancestry; parent owns "
    "runner.lock, NOchildacquire/delete/unlock/readprobe. Preserve/report/yield new "
    "denial/signinghang/uncertainownership; no signing retry/bypass, changed guards, "
    "authoragents, concurrent heavy work or secondrunner. Published133/1228,remaining"
    "1095 unchanged; necessary supports are NOT N1 vocabulary. Compatible Android125/"
    "132 required; physical-phone/generalrelease/whole-set outstanding; project incomplete."
)


def seal():
    current()
    tests = (L / "source-tests-842.txt").read_text(encoding="utf-8-sig")
    count = int(re.search(r"Ran (\d+) tests", tests)[1])
    assert count == 97 and tests.rstrip().endswith("OK")
    assert "Verified 92 complete" in (L / "extract-842.txt").read_text(encoding="utf-8-sig")
    assert "0 error(s)" in (L / "validate-842.txt").read_text(encoding="utf-8-sig")
    manifest_diff = (L / "manifest-diff-842.txt").read_text(encoding="utf-8-sig").strip()
    assert manifest_diff == "warning: in the working copy of 'manifest.json', LF will be replaced by CRLF the next time Git touches it"
    assert not git("diff", "--cached", "--", "manifest.json")
    assert not git("diff", "--", "manifest.json")
    assert load(S / (PREFIX + "initial-source-audit.json"))["allRowMetadataAndUnicodeRadicalReproduced"]
    assert "allRowMetadataAndUnicodeRadicalReproduced" in (L / "audit-842-final.txt").read_text(encoding="utf-8-sig")
    extra = "words/\u8003\u3048\u308b.md"
    save(S / (PREFIX + "additional-article-snapshots.json"), [{
        "article": extra, "sha256": sha((R / extra).read_bytes()),
        "text": (R / extra).read_text(encoding="utf-8"),
        "scope": "Existing usual-spelling identity, relevant to supplementary rare 勘える evidence; no declared new component pair or requested edit.",
    }])
    evidence = S / (PREFIX + "preparation-842")
    evidence.mkdir()
    artifacts = []
    recipes = [
        Path(__file__), C / "preflight-842.ps1", C / "checks-batch-107-source-842.ps1",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
    ]
    receipts = [
        L / (name + "-842.txt") for name in
        ("source-tests", "extract", "validate", "manifest", "manifest-diff",
         "budget", "vocabulary", "audit", "whitespace")
    ] + [L / "audit-842-final.txt", L / "preflight-842.json", L / "preflight-842-checks.json"]
    for path in recipes + receipts:
        destination = evidence / path.name
        raw = path.read_bytes()
        new(destination, raw)
        artifacts.append({"path": destination.relative_to(R).as_posix(), "sha256": sha(raw)})
    files = {path.relative_to(R).as_posix(): sha(path.read_bytes())
             for path in sorted(S.glob(PREFIX + "*")) if path.is_file()}
    manifest = load(R / "manifest.json")
    record = {
        "schemaVersion": 1, "execution": 842, "batch": "107", "membership": [CHAR],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": BASE,
        "stage": "initial-source-prepared-awaiting-normal-local-signature",
        "sourceFiles": files, "archivedArtifacts": artifacts,
        "authorInspection": load(S / (PREFIX + "source-observations.json"))["authorInspection"],
        "validation": {
            "focusedSourceTestsPassed": count, "existingExtractorExactFamilies": 92,
            "validatorErrors": 0, "manifestFreshAndGitUnchanged": True,
            "sourceAudit": load(S / (PREFIX + "initial-source-audit.json")),
            "manifestRepresentation": load(S / (PREFIX + "manifest-representation.json")),
            "budget": (L / "budget-842.txt").read_text(encoding="utf-8-sig").strip(),
            "vocabulary": (L / "vocabulary-842.txt").read_text(encoding="utf-8-sig").strip(),
        },
        "runtime": {"contentVersion": manifest["contentVersion"], "schemaVersion": manifest["schemaVersion"],
                    "kanji": 1129, "words": 5080,
                    "manifestGitSha256": sha((R / "manifest.json").read_bytes())},
        "sourcePreparationComplete": False, "runtimeChangedInGit": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "projectPublishedAdditions": 133, "remainingAdditions": 1095,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False,
        "parentLockTouched": False,
        "diagnostics": load(C / "progress.json")["execution842StartingState"]["diagnostics"] + [
            "One redundant beyond-EOF member range returned nothing; all1733 actual member lines had already been returned.",
            "Raw-manifest baseline audit failed after normal generation normalized checkout CRLF. Exact public Git LF bytes and original CRLF hash were reproduced separately; failure retained, no baseline rewrite.",
            "Source-only preflight detected manifest stat-cache modification despite an empty normalized Git diff. Normal staging of regenerated manifest proved an empty staged diff and cleared the cache; no runtime commit delta.",
            "First seal check expected an empty manifest-diff log, but Git emitted only its LF-to-CRLF warning. Exact warning and empty staged/unstaged diffs verified; original log retained.",
            "Read-only evidence measurement initially omitted explicit UTF-8 on manifest; corrected decoder measured1733 member lines and75 raw-character lines. No source bytes changed.",
        ],
        "nextAction": NEXT,
    }
    save(S / "execution-842.json", record)
    print("Initial source evidence sealed; no runtime or review acceptance.")


def finish():
    p = current()
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    assert git("log", "-1", "--format=%G?") == "G"
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("status", "--porcelain", "--untracked-files=all")
    changed = git("diff", "--name-only", BASE, head).splitlines()
    assert changed and all(name.startswith("docs/n1-sources/batch-107-")
                           or name == "docs/n1-sources/execution-842.json" for name in changed)
    record = load(S / "execution-842.json")
    for name, digest in record["sourceFiles"].items():
        assert sha((R / name).read_bytes()) == digest
    for item in record["archivedArtifacts"]:
        assert sha((R / item["path"]).read_bytes()) == item["sha256"]
    issue = load(L / "issue-receipt-842.json")
    assert issue["author"] == "stop-cran" and issue["verified"] is True
    assert issue["localCommit"] == head
    before = load(L / "progress-before-842.json")
    preserved = set(before) - {"batch", "stage", "nextAction", "blocker"}
    assert all(p[key] == before[key] for key in preserved)
    p["execution842CoordinatorCheckpoint"] = {
        "execution": 842, "checkpoint": 842, "batch": "107", "status": "continue",
        "stage": "batch-107-initial-source-signed-awaiting-completion",
        "savedCommit": head, "signature": "G", "record": "docs/n1-sources/execution-842.json",
        "recordSha256": sha((S / "execution-842.json").read_bytes()),
        "initialSourceAudit": record["validation"]["sourceAudit"],
        "issueUpdate": issue["url"], "ownerAuthorAndBodyVerified": True,
        "sourcePreparationComplete": False, "runtimeChangedInGit": False,
        "reviewersLaunched": 0, "freshAndroidOrNative": False,
        "runtimePublished": False, "publishedAdditions": 133, "remainingAdditions": 1095,
        "dedicatedWorktreesClean": True, "allOriginalHistoricalRootValuesPreserved": True,
        "parentLockTouched": False, "nextAction": NEXT,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
    }
    p["execution842StartingState"]["status"] = "signed-local-initial-source-checkpoint-complete"
    p["execution842Inherited841Gates"] = {
        "priorNextAction": before["nextAction"], "priorStage": before["stage"],
        "immutableBefore": str(L / "progress-before-842.json"),
        "immutableBeforeSha256": sha((L / "progress-before-842.json").read_bytes()),
        "latestPublication": copy.deepcopy(before["batch106PublicationCheckpoint"]),
        "allOriginalAcceptanceGatesRemainMandatory": True,
    }
    p.update(checkpoint=842, status="continue", stage="batch-107-initial-source-signed-awaiting-completion",
             nextAction=NEXT, blocker=None)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    new(L / "checkpoint-after-842.json", (C / "progress.json").read_bytes())
    print("Checkpoint842 saved with full history, verified local signature/owner issue; publication counters unchanged.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("start", "packet", "check", "archive", "seal", "finish"))
    args = parser.parse_args()
    {"start": start, "packet": packet, "check": check, "archive": archive,
     "seal": seal, "finish": finish}[args.mode]()
