"""Freeze and reproduce the initial source-only packet for N1 batch 108."""
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
A = R.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "68ceabfa-9c21-4d59-86f5-8b82acb120cb"
HEAD = "eb7eb038e5bcff21754e158a2393c1b89b978757"
PUBLIC = "e766221c2a9c5ada2314805c307e534ccf4537ec"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
CHAR = "\u52e7"
P = "batch-108-"
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
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def save(path, value):
    temporary = path.with_name(path.name + ".859.tmp")
    if temporary.exists():
        raise FileExistsError(temporary)
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def xml_bytes(root):
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


def current():
    runner = load(C / "runner.json")
    assert runner["status"] == "running" and runner["sessionId"] == L.name
    assert runner["pid"] == 27864
    p = load(C / "progress.json")
    assert p["checkpoint"] == 858 and p["status"] == "continue" and p["batch"] == "108"
    assert p["lastPublishedCommit"] == PUBLIC and p["remainingAdditions"] == 1094
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    assert git("rev-parse", "origin/main") == PUBLIC
    return p


def start():
    p = current()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert load(L / "checkpoint-full.json") == p
    role = load(L / "preflight-859.json")
    assert role["runnerPid"] == 27864 and role["coordinatorPid"] == 23040
    assert role["liveRunnerIsCoordinatorParent"] and role["runnerScriptAuthenticated"]
    assert role["parentLockTouched"] is False
    assert not list(S.glob(P + "*"))
    assert p["execution792HistoryCorrection"]["ownerReportCorrection"].startswith("https://github.com/")
    before = L / "progress-before-859.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    p["execution859StartingState"] = {
        "execution": 859, "batch": "108", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "publishedBase": PUBLIC, "androidHead": APP,
        "scope": "One bounded initial source packet, no runtime draft/review/native/publication.",
        "runnerPreflight": role, "completeRequestReadIncludingFinalCheckpoint": True,
        "fullHistoryBefore": str(before), "fullHistoryBeforeSha256": sha(before.read_bytes()),
        "artifactPolicy": "Committed packets and approved frozen workspace inputs only; reusable helper in control; no optional historical session recipes.",
        "status": "source-preparation-in-progress",
    }
    p.update(stage="batch-108-initial-source-preparation-in-progress",
             nextAction="Freeze row119 complete source families and baseline; all acceptance gates unchanged.")
    save(C / "progress.json", p)
    print("Source scope saved with full live history.")


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
    radicals = {}
    for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines():
        fields = line.split(";")
        cp = int(fields[0], 16)
        if 0x2F00 <= cp <= 0x2FD5:
            radicals[cp - 0x2F00 + 1] = chr(int(fields[5].split()[-1], 16))
    assert len(radicals) == 214
    return snapshot, inputs, jm, ET.fromstring(kd), radicals


def member_families(jm):
    root = ET.Element("JMdict")
    for _, entry in ET.iterparse(io.BytesIO(jm), events=("end",)):
        if entry.tag == "entry":
            if any(CHAR in k.text for k in entry.findall("k_ele/keb")):
                root.append(copy.deepcopy(entry))
            entry.clear()
    return root


def packet():
    current()
    assert git("rev-parse", "HEAD") == HEAD
    assert not list(S.glob(P + "*"))
    snapshot, inputs, jm, kd, radicals = frozen()
    row = next(e for e in load(S / "source-index.json") if e["sourceRow"] == 119)
    assert row["kanji"] == CHAR and json.loads(inputs["n1-kanji-source-20261102.json"])[118] == CHAR
    assert not (R / row["article"]).exists() and not (R / row["strokeFile"]).exists()
    families = member_families(jm)
    ids = [e.findtext("ent_seq") for e in families]
    assert ids and len(ids) == len(set(ids))
    (S / (P + "jmdict.xml")).write_bytes(xml_bytes(families))
    save(S / (P + "lexical-selection.json"), {
        "schemaVersion": 1, "batch": "108", "entryIds": ids,
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen JMdict family containing U+52E7 in any keb, in source order; all aliases/readings/restrictions/senses retained.",
        "limits": "Extraction is not inspection, per-character allocation, frequency evidence or independent review.",
    })
    character = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    assert metadata_record(character, radicals) == row["metadata"]
    raw_root = ET.Element("kanjidic2")
    raw_root.append(copy.deepcopy(kd.find("header")))
    raw_root.append(copy.deepcopy(character))
    raw_kd = xml_bytes(raw_root)
    (S / (P + "kanjidic2.xml")).write_bytes(raw_kd)
    save(S / (P + "input-metadata.json"), {
        "schemaVersion": 1, "batch": "108", "baseCommit": HEAD, "publishedBaseCommit": PUBLIC,
        "characters": [CHAR], "sourceIndexRecord": row,
        "rawCharacterPacket": P + "kanjidic2.xml", "rawCharacterPacketSha256": sha(raw_kd),
        "provenance": "Complete frozen parsed character record and header reserialized; source reading order preserved, nanori not selected.",
        "verifiedInputHashes": {n: v["sha256"] for n, v in snapshot["inputs"].items()},
        "dictionaryAttribution": snapshot["dictionaryAttribution"],
    })
    inventory, candidates = {}, []
    for folder in ("kanji", "words"):
        for path in sorted((R / folder).glob("*.md")):
            name = path.relative_to(R).as_posix()
            m = metadata(R, name)
            inventory[name] = {"metadata": m, "sha256": sha(path.read_bytes())}
            if folder == "words" and (CHAR in m.get("kanji", []) or CHAR in m["word"]):
                matches = [e.findtext("ent_seq") for e in families
                           if any(k.text == m["word"] for k in e.findall("k_ele/keb"))
                           and any(r.text == m["reading"] for r in e.findall("r_ele/reb"))]
                candidates.append({"article": name, **inventory[name], "candidateFamilyIds": matches,
                                   "limits": "Navigation match only; actual prose, restrictions, selected senses and allocation need inspection."})
    save(S / (P + "baseline-plan.json"), {
        "schemaVersion": 1, "batch": "108", "baseCommit": HEAD, "publishedBaseCommit": PUBLIC,
        "inventory": inventory, "runtimeManifest": load(R / "manifest.json"),
        "manifestRawSha256": sha((R / "manifest.json").read_bytes()),
        "limits": "Complete current metadata/byte baseline, not a fresh review of unchanged cards.",
    })
    save(S / (P + "source-navigation.json"), {
        "sourceIndexRecord": row, "candidates": candidates,
        "baselinePairs": [e for e in load(S / "baseline-word-candidates.json") if e["kanji"] == CHAR],
    })
    save(S / (P + "existing-article-snapshots.json"), [
        {"article": e["article"], "sha256": e["sha256"], "text": (R / e["article"]).read_text(encoding="utf-8")}
        for e in candidates])
    state = {
        "schemaVersion": 1, "batch": "108", "baseCommit": HEAD, "publishedBaseCommit": PUBLIC,
        "membership": [CHAR], "sourceRows": [119], "members": [{"kanji": CHAR, "sourceRow": 119}],
        "selectionReason": "Next absent frozen row after published row118; recommendation/encouragement spellings and secondary on-reading require a single-character bounded family audit.",
        "status": "initial-source-packet-only", "sourcePreparationComplete": False,
        "sourceReadingOrder": {k: row["metadata"][k] for k in ("onyomi", "kunyomi")},
        "drafted": [], "reviewClosed": [], "published": [], "runtimeChanged": False,
        "runtimePublished": False, "publishedAdditions": 134, "remainingAdditions": 1094,
        "limits": "All final support, quiz, link, font and stroke decisions pending; no accepted coverage.",
    }
    for name in ("membership.json", "progress.json"):
        save(S / (P + name), state)
    print(json.dumps({"families": len(ids), "candidates": candidates}, ensure_ascii=True))


def check():
    current()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    snapshot, inputs, jm, kd, radicals = frozen()
    assert xml_bytes(member_families(jm)) == (S / (P + "jmdict.xml")).read_bytes()
    selected = ET.parse(S / (P + "jmdict.xml")).getroot()
    assert [e.findtext("ent_seq") for e in selected] == load(S / (P + "lexical-selection.json"))["entryIds"]
    original = next(e for e in kd.findall("character") if e.findtext("literal") == CHAR)
    actual = ET.parse(S / (P + "kanjidic2.xml")).getroot().find("character")
    ET.indent(original, space="  ", level=1)
    assert ET.tostring(original).strip() == ET.tostring(actual).strip()
    assert metadata_record(original, radicals) == load(S / (P + "input-metadata.json"))["sourceIndexRecord"]["metadata"]
    baseline = load(S / (P + "baseline-plan.json"))
    assert baseline["runtimeManifest"] == build_manifest(R) == load(R / "manifest.json")
    assert sha((R / "manifest.json").read_bytes()) == baseline["manifestRawSha256"]
    committed = json.loads(subprocess.check_output(["git", "-C", str(R), "show", HEAD + ":manifest.json"]))
    assert committed == baseline["runtimeManifest"]
    for name, item in baseline["inventory"].items():
        assert metadata(R, name) == item["metadata"] and sha((R / name).read_bytes()) == item["sha256"]
    assert not (R / "kanji" / (CHAR + ".md")).exists()
    assert not (R / "strokes" / (CHAR + ".json")).exists()
    assert not git("diff", HEAD, "--", "manifest.json", "kanji", "words", "strokes")
    for receipt in load(S / (P + "public-source-receipts.json")):
        raw = gzip.decompress((S / receipt["archive"]).read_bytes())
        assert sha(raw) == receipt["rawSha256"] and len(raw) == receipt["rawBytes"]
        assert sha((S / receipt["archive"]).read_bytes()) == receipt["archiveSha256"]
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    svg = (S / (P + "kanjivg.svg")).read_bytes()
    geometry = load(S / (P + "stroke-evidence.json"))
    assert sha(svg) == geometry["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == geometry["gitBlob"]
    assert len(ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")) == 13
    result = {
        "schemaVersion": 1, "execution": 859, "batch": "108", "baseCommit": HEAD,
        "allFiveFrozenInputHashesVerified": True, "bothDecompressedDictionaryHashesVerified": True,
        "completeMemberFamiliesReproduced": len(selected), "rawCharacterRecordsReproduced": 1,
        "baselineArticlesUnchanged": len(baseline["inventory"]),
        "allRowMetadataAndUnicodeRadicalReproduced": True, "manifestFreshAndUnchanged": True,
        "runtimeChanged": False, "sourcePreparationComplete": False,
        "limits": "Mechanical initial source check only; no final mappings, independent review, native or publication acceptance.",
    }
    save(S / (P + "initial-source-audit.json"), result)
    print(json.dumps(result))


def archive():
    class DictionaryBlocks(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth, self.parts, self.blocks = 0, [], []

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
    page = C / "batch-108-character-859.html"
    raw = page.read_bytes()
    parser = DictionaryBlocks()
    parser.feed(raw.decode("utf-8"))
    text = parser.blocks[0]
    assert all(term in text for term in ("\u52e7", "\u30ab\u30f3", "\u3059\u3059\u3081\u308b", "\u52e7\u8a98", "\u52f8"))
    target = S / (P + "character-public-text.txt")
    assert not target.exists()
    target.write_text(text, encoding="utf-8")
    archive_path = S / (P + "character.html.gz")
    archive_path.write_bytes(gzip.compress(raw, mtime=0))
    assert gzip.decompress(archive_path.read_bytes()) == raw
    save(S / (P + "public-source-receipts.json"), [{
        "url": "https://www.weblio.jp/content/%E5%8B%A7",
        "downloadedAt": datetime.fromtimestamp(page.stat().st_mtime, timezone.utc).isoformat(),
        "rawBytes": len(raw), "rawSha256": sha(raw), "archive": archive_path.name,
        "archiveSha256": sha(archive_path.read_bytes()), "losslessGzip": True,
        "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
        "scope": "First Digital Daijisen character wrapper only, not subsequent Wiktionary or KANJIDIC2 aggregator wrappers.",
        "limits": "Coordinator retrieval, not independent reviewer upstream lookup. Daijisen supplies カン/すすめる, not an unrestricted claim that other readings are invalid; frozen ケン stays intact.",
    }])
    svg = (C / "batch-108-kanjivg-859.download.svg").read_bytes()
    row = load(S / (P + "input-metadata.json"))["sourceIndexRecord"]
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    assert blob == row["kanjivgInventory"]["sha"] and len(svg) == row["kanjivgInventory"]["size"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == row["metadata"]["strokes"] == 13
    assert [e.get("id") for e in paths] == [f"kvg:052e7-s{i}" for i in range(1, 14)]
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    converter = sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n"))
    assert converter == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    (S / (P + "kanjivg.svg")).write_bytes(svg)
    save(S / (P + "stroke-evidence.json"), {
        "revision": snapshot["kanjivg"]["revision"], "gitBlob": blob,
        "sha256": sha(svg), "bytes": len(svg), "dictionaryStrokeCount": 13,
        "sourceStrokePaths": 13, "converted": False, "nativeDrawingAccepted": False,
        "converterNormalizedSha256": converter,
        "sourceUrl": "https://raw.githubusercontent.com/KanjiVG/kanjivg/70a0b7ae0c18ceb5cb358274b029cce0234a43bc/kanji/052e7.svg",
        "attribution": "Ulrich Apel and contributors, KanjiVG, CC BY-SA3.0; repository NOTICE.",
        "limits": "Pinned geometry/order/count only. SVG phon/component annotations are not independent historical evidence; runtime conversion/native checks pending.",
    })
    print(text.encode("ascii", errors="backslashreplace").decode())
    print("Pinned thirteen-path SVG preserved; no runtime conversion.")


NEXT = (
    "SAME108 bounded source completion, then a later local unreviewed runtime freeze only when source-ready. "
    "Read committed batch-108-source-observations.json, membership/navigation, all46 complete member families, "
    "full raw character, first Daijisen wrapper and pinned13-path SVG. Row119 勧; preserve fullon[カン,ケン]/"
    "fullkun[すす.める] in source order. Provisional quizzes[カン]/[すす.める]; ケン is retained source-only "
    "because no verified usable per-character example was established, NOT declared invalid/rare merely "
    "from missing examples. Reuse actual 勧めるすすめる N3 identity/level; inspect sense-specific spelling "
    "restrictions of complete1595680. One new necessary カン support candidate (勧告 or 勧誘), not a new "
    "N1 vocabulary section; decide from complete families and actual existing component coverage. Finish "
    "comparison/distractor full families/cards/ordinary secondary senses, three wrong kanji titles/direct "
    "symmetric nontransitive safeguards/legacy fallbacks, actual activated baseline pair plus all mapped "
    "existing component pairs and exact reused passages, all full/selected reading dispositions, qualified "
    "shape/radical/font plan. No runtime authored, no review/HOST/native/publication/109 this checkpoint. "
    "Both serial blind different-family content reviews and retained actual models/reports/serial internal "
    "tools/original-session confirmations as needed remain mandatory. Qualified signed clean bf30cde "
    "Android, non-skipped HOST, native full ContentSync ONCE/meaning/curated reading/drawing/articles/Back/"
    "offline/fourfonts/rendered checks; exact-current source/membership/baseline/readings/quiz/links/strokes/"
    "Python/vocabulary/manifest/budgets; latest-main nonrewriting integration/changedteaching review/combined "
    "validation/normal signing/owner fastforward/exact terminal greenCI/EVERY immutableZIP runtimehash and "
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/verifiedownerissue gates "
    "remain before delivery. Preserve full live history,792 correction,all prior denials/OOMs/accepted "
    "publications/unresolved reading and quiz limits including 定/違,支払う/支払,勘/識 and 勅/訓. Recovered "
    "siblings only; committed sources/approved inputs/control helpers, no optional historicalsession recipes. "
    "Authenticate live launcher ancestry/session/currentcheckpoint/exactsignedheads/clean-accountedstate; "
    "parent owns runner.lock, NOchild reacquire/delete/unlock/readprobe. Preserve/report/yield on actual "
    "newdenial/signinghang/uncertainownership; no signingretry/bypass/permissions expansion/guard changes/"
    "concurrent heavywork/authoragents/secondrunner. Published134/1228,remaining1094 unchanged; six earlier-"
    "level source dispositions are not issue60 acceptance credit. Compatible client125/132 required; "
    "physical-phone/handwriting-model/general-release/whole-set acceptance outstanding; project incomplete."
)


def seal():
    current()
    test_text = (L / "source-tests-859.txt").read_text(encoding="utf-8-sig")
    test_count = int(re.search(r"Ran (\d+) tests", test_text)[1])
    assert test_count >= 97 and test_text.rstrip().endswith("OK")
    assert "Verified 46 complete" in (L / "extract-859.txt").read_text(encoding="utf-8-sig")
    assert "0 error(s)" in (L / "validate-859.txt").read_text(encoding="utf-8-sig")
    assert not git("diff", "--", "manifest.json")
    assert not git("diff", "--cached", "--", "manifest.json")
    assert load(S / (P + "initial-source-audit.json"))["completeMemberFamiliesReproduced"] == 46
    assert not load(S / (P + "source-observations.json"))["sourcePreparationComplete"]
    for path in (S / "execution-859.json", S / (P + "prepare-859.py")):
        assert not path.exists()
    shutil.copyfile(Path(__file__), S / (P + "prepare-859.py"))
    shutil.copyfile(C / "checks-batch-108-source-859.ps1", S / (P + "checks-859.ps1"))
    evidence = []
    for path in sorted(S.glob(P + "*")):
        evidence.append({"path": path.relative_to(R).as_posix(), "sha256": sha(path.read_bytes()),
                         "bytes": path.stat().st_size})
    for name in ("preflight", "source-tests", "extract", "validate", "manifest", "manifest-diff", "budget", "vocabulary", "audit", "whitespace"):
        ext = "json" if name == "preflight" else "txt"
        path = L / f"{name}-859.{ext}"
        assert path.exists()
        destination = S / (P + f"checks-859-{name}.{ext}.gz")
        destination.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        evidence.append({"path": destination.relative_to(R).as_posix(), "sha256": sha(destination.read_bytes()),
                         "bytes": destination.stat().st_size})
    record = {
        "schemaVersion": 1, "execution": 859, "batch": "108",
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": HEAD,
        "publishedBaseCommit": PUBLIC, "membership": [CHAR], "sourceRows": [119],
        "status": "local-initial-source-packet-only", "runtimeChanged": False,
        "sourcePreparationComplete": False, "independentReviewersLaunched": 0,
        "memberFamilies": 46, "characterRecords": 1, "pinnedStrokePaths": 13,
        "baselineArticlesUnchanged": 6210, "sourceTests": test_count,
        "validatorAndManifestAndBudgetAndVocabularyPassed": True,
        "vocabularyCoverageLimit": "Existing pilot coverage2122/2431, not complete coverage or a claim that unrelated baseline gaps were fixed.",
        "runtimeBatchAuditDisposition": "No runtime draft exists; current-schema runtime audit is deferred to the actual draft, not waived or claimed passed.",
        "androidHead": APP, "androidOrNativeExecuted": False, "publishedAdditions": 134,
        "remainingAdditions": 1094, "parentLockTouched": False,
        "fullHistoryBefore": str(L / "progress-before-859.json"), "evidence": evidence,
        "nextAction": NEXT,
        "limits": "Coordinator source inspection and mechanical checks only; no runtime draft, independent review, native or publication acceptance. No physical-phone, handwriting-model, general-release or whole-set acceptance.",
    }
    save(S / "execution-859.json", record)
    print("Evidence sealed for normal signed LOCAL source-only checkpoint.")


def finish():
    p = current()
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("status", "--porcelain", "--untracked-files=all")
    changed = git("diff", "--name-only", HEAD, head).splitlines()
    assert changed and all(name.startswith("docs/n1-sources/batch-108-") or name == "docs/n1-sources/execution-859.json"
                           for name in changed)
    assert not git("diff", HEAD, head, "--", "manifest.json", "kanji", "words", "strokes")
    issue = load(L / "issue-receipt-859.json")
    assert issue["verified"] and issue["author"] == "stop-cran" and issue["localCommit"] == head
    snapshot = load(S / "execution-859.json")
    assert snapshot["memberFamilies"] == 46 and snapshot["sourcePreparationComplete"] is False
    assert sha((S / (P + "prepare-859.py")).read_bytes()) == sha(Path(__file__).read_bytes())
    before = copy.deepcopy(p)
    p["execution859StartingState"]["status"] = "signed-initial-source-checkpoint-complete"
    checkpoint = {
        "execution": 859, "batch": "108", "status": "continue", "signedLocalCommit": head,
        "signature": "G", "record": "docs/n1-sources/execution-859.json",
        "recordSha256": sha((S / "execution-859.json").read_bytes()),
        "membership": [CHAR], "completeMemberFamilies": 46, "sourcePreparationComplete": False,
        "runtimeChanged": False, "runtimePublished": False, "pushed": False,
        "publishedAdditions": 134, "remainingAdditions": 1094, "issueUpdate": issue["url"],
        "ownerAuthorAndBodyAndUrlVerified": True, "parentLockTouched": False,
        "nextAction": NEXT,
    }
    p["execution859CoordinatorCheckpoint"] = checkpoint
    p.update(checkpoint=859, status="continue", stage="batch-108-initial-sources-frozen-awaiting-source-completion",
             nextAction=NEXT, blocker=None)
    for key in before:
        if key not in {"checkpoint", "status", "stage", "nextAction", "blocker", "execution859StartingState"}:
            assert p[key] == before[key], key
    save(C / "progress.json", p)
    verified = load(C / "progress.json")
    assert verified == p and len(verified) == len(before) + 1
    print(json.dumps(checkpoint, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("start", "packet", "check", "archive", "seal", "finish"))
    globals()[parser.parse_args().mode]()
