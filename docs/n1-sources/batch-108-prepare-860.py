"""Complete the bounded source preparation for N1 batch 108."""
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
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "rollout-recovered" / "learning-japanese"
A = R.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "d29e3fec-c862-40dc-ad3a-454bdb39426f"
HEAD = "4e33eafe4bbf8b29a06b76a66ddc47a2e7cc1f81"
PUBLIC = "e766221c2a9c5ada2314805c307e534ccf4537ec"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
P = "batch-108-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def git(*args, root=R):
    return subprocess.check_output(
        ["git", "--no-pager", "-C", str(root), *args], encoding="utf-8"
    ).strip()


def save(path, value):
    temp = path.with_name(path.name + ".860.tmp")
    if temp.exists():
        raise FileExistsError(temp)
    temp.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temp) == value
    temp.replace(path)


def current():
    runner = load(C / "runner.json")
    assert runner["status"] == "running" and runner["sessionId"] == L.name
    assert runner["pid"] == 27864
    p = load(C / "progress.json")
    assert p["checkpoint"] == 859 and p["status"] == "continue" and p["batch"] == "108"
    assert p["lastPublishedCommit"] == PUBLIC and p["remainingAdditions"] == 1094
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    return p


def start():
    p = current()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert load(L / "checkpoint-full.json") == p
    assert git("rev-parse", "origin/main") == PUBLIC
    assert p["execution792HistoryCorrection"]["ownerReportCorrection"].startswith("https://github.com/")
    before = L / "progress-before-860.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    p["execution860StartingState"] = {
        "execution": 860, "batch": "108", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": HEAD, "publishedBase": PUBLIC, "androidHead": APP,
        "scope": "Complete source mappings and evidence only; no runtime, reviewers or publication.",
        "runnerPid": 27864, "coordinatorPid": 26376,
        "liveRunnerIsCoordinatorParent": True,
        "runnerScriptSha256": sha((C / "runner.ps1").read_bytes()),
        "parentLockTouched": False, "completeRequestReadIncludingFinalCheckpoint": True,
        "fullHistoryBefore": str(before), "fullHistoryBeforeSha256": sha(before.read_bytes()),
        "status": "source-completion-in-progress",
    }
    p.update(stage="batch-108-source-completion-in-progress",
             nextAction="Complete SAME108 comparison, quiz, links, readings and font source plan; all gates retained.")
    save(C / "progress.json", p)
    print("Full-history starting scope persisted.")


def inspect():
    current()
    needles = ("recommend", "encourag", "advice", "advise", "warn", "suggest", "invit", "solicit", "urge", "persua")
    for folder in ("kanji", "words"):
        for path in sorted((R / folder).glob("*.md")):
            m = metadata(R, path.relative_to(R).as_posix())
            if any(n in m["title"].lower() for n in needles):
                print(json.dumps({"path": path.relative_to(R).as_posix(), **m}, ensure_ascii=True))


def xml_bytes(root):
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


COMPARISONS = [
    "\u63a8\u85a6", "\u63d0\u6848", "\u8b66\u544a", "\u76f8\u8ac7",
    "\u52b1\u307e\u3059", "\u6fc0\u52b1", "\u52b1\u3080", "\u52df\u96c6",
    "\u62db\u304f", "\u62db\u5f85", "\u8a98\u3046", "\u547c\u3073\u639b\u3051\u308b",
    "\u652f\u3048\u308b", "\u610f\u898b", "\u547d\u4ee4", "\u6307\u793a", "\u6ce8\u610f",
]
KANJI = "\u52e7\u544a\u52b1\u52df\u62db\u8b66\u652f\u89b3\u78ba\u6a29"
LEGACY = "\u4eba\u4f11\u4f55\u5165\u51fa\u53e3\u5973\u65e5\u6708\u7537\u8cb7"


def packet():
    current()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    raw_inputs = {}
    for name, info in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert sha(raw) == info["sha256"] and len(raw) == info["bytes"], name
        raw_inputs[name] = raw
    jm = gzip.decompress(raw_inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(raw_inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == snapshot["jmdict"]["xmlSha256"]
    assert sha(kd) == snapshot["kanjidic2"]["xmlSha256"]
    selected = ET.Element("JMdict")
    for _, entry in ET.iterparse(io.BytesIO(jm), events=("end",)):
        if entry.tag == "entry":
            if any(k.text in COMPARISONS for k in entry.findall("k_ele/keb")):
                selected.append(copy.deepcopy(entry))
            entry.clear()
    path = S / (P + "comparison-jmdict.xml")
    assert not path.exists()
    path.write_bytes(xml_bytes(selected))
    chars = ET.fromstring(kd)
    root = ET.Element("kanjidic2")
    root.append(copy.deepcopy(chars.find("header")))
    for entry in chars.findall("character"):
        if entry.findtext("literal") in KANJI:
            root.append(copy.deepcopy(entry))
    (S / (P + "comparison-kanjidic2.xml")).write_bytes(xml_bytes(root))
    overlap = []
    for entry in chars.findall("character"):
        char = entry.findtext("literal")
        meanings = [e.text for e in entry.findall("reading_meaning/rmgroup/meaning") if not e.attrib]
        if (R / "kanji" / (char + ".md")).exists() and any(
            needle in m.lower() for m in meanings
            for needle in ("recommend", "encourag", "advise", "persuad", "offer")
        ):
            overlap.append({"kanji": char, "meanings": meanings,
                            "metadata": metadata(R, f"kanji/{char}.md")})
    save(S / (P + "comparison-selection.json"), {
        "schemaVersion": 1, "batch": "108", "snapshot": "docs/n1-source-snapshot.json",
        "selectionRule": "Every complete frozen JMdict family with any keb exactly matching a listed comparison spelling, in source order; no alias, reading, restriction or sense filtering.",
        "comparisonSpellings": COMPARISONS,
        "entryIds": [e.findtext("ent_seq") for e in selected],
        "matchedSpellings": {w: [e.findtext("ent_seq") for e in selected
                               if any(k.text == w for k in e.findall("k_ele/keb"))] for w in COMPARISONS},
        "kanjidicCharacters": [e.findtext("literal") for e in root.findall("character")],
        "existingKanjiEnglishOverlapNavigation": overlap,
        "limits": "Substring navigation is not a synonym certification or a whole-corpus semantic audit. Final choices require actual complete family and card inspection.",
        "allFiveFrozenInputsVerified": True, "bothXmlHashesVerified": True,
    })
    print(json.dumps({"comparisonFamilies": len(selected), "overlapNavigation": overlap}, ensure_ascii=True))


def supplement():
    current()
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    raw = (C / "inputs" / "n1-planning-kanjidic2.xml.gz").read_bytes()
    assert sha(raw) == snapshot["inputs"]["n1-planning-kanjidic2.xml.gz"]["sha256"]
    root = ET.fromstring(gzip.decompress(raw))
    selected = ET.Element("kanjidic2")
    selected.append(copy.deepcopy(root.find("header")))
    for entry in root.findall("character"):
        if entry.findtext("literal") in "\u4f9b\u796d\u52c9\u8a2a":
            selected.append(copy.deepcopy(entry))
    path = S / (P + "overlap-kanjidic2.xml")
    assert not path.exists()
    path.write_bytes(xml_bytes(selected))
    articles = [f"kanji/{k}.md" for k in LEGACY]
    articles += [f"kanji/{k}.md" for k in KANJI if k != "\u52e7"]
    articles += [f"kanji/{k}.md" for k in "\u4f9b\u796d\u52c9\u8a2a"]
    articles += [f"words/{w}.md" for w in COMPARISONS if (R / "words" / (w + ".md")).exists()]
    articles += ["words/\u52e7\u3081\u308b.md", "words/\u9032\u3081\u308b.md"]
    saved = []
    for name in sorted(set(articles)):
        path = R / name
        saved.append({"article": name, "sha256": sha(path.read_bytes()),
                      "metadata": metadata(R, name), "text": path.read_text(encoding="utf-8")})
    save(S / (P + "comparison-article-snapshots.json"), saved)
    text = "".join(f"\n===== {name} =====\n" + (R / name).read_text(encoding="utf-8")
                   for name in [f"kanji/{k}.md" for k in LEGACY])
    (S / (P + "legacy-fallback-cards.txt")).write_text(text, encoding="utf-8")
    print(json.dumps({"savedCurrentArticleSnapshots": len(saved),
                      "legacyPacketLines": len(text.splitlines())}))


def archive():
    class Blocks(HTMLParser):
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
    page = C / "batch-108-kankoku-860.html"
    raw = page.read_bytes()
    parser = Blocks()
    parser.feed(raw.decode("utf-8"))
    text = parser.blocks[0]
    assert all(t in text for t in ("\u52e7\u544a", "\u304b\u3093\u3053\u304f",
                                   "\u8f9e\u8077", "\u884c\u52d5"))
    archive_path = S / (P + "support-public.html.gz")
    text_path = S / (P + "support-public-text.txt")
    assert not archive_path.exists() and not text_path.exists()
    archive_path.write_bytes(gzip.compress(raw, mtime=0))
    text_path.write_text(text, encoding="utf-8")
    save(S / (P + "support-public-source-receipt.json"), {
        "url": "https://www.weblio.jp/content/%E5%8B%A7%E5%91%8A",
        "downloadedAt": datetime.fromtimestamp(page.stat().st_mtime, timezone.utc).isoformat(),
        "rawBytes": len(raw), "rawSha256": sha(raw), "archive": archive_path.name,
        "archiveSha256": sha(archive_path.read_bytes()), "losslessGzip": True,
        "extractedText": text_path.name, "extractedTextSha256": sha(text_path.read_bytes()),
        "scope": "First actual Digital Daijisen wrapper only: exact heading, reading, action-recommendation definition and resignation example.",
        "limits": "Coordinator retrieval, not independent upstream reviewer lookup. Later Wikipedia/Wiktionary/generated example wrappers not adopted as Daijisen; no blanket current legal-force claim.",
    })
    print(text)


def fonts():
    from fontTools.ttLib import TTFont

    current()
    plan = load(S / (P + "source-completion-plan.json"))
    text = plan["fontPlan"]["proposedTextInventory"]
    for name in ("words/\u52e7\u3081\u308b.md", "kanji/\u544a.md"):
        text += (R / name).read_text(encoding="utf-8")
    for item in plan["linkPlan"]["exactReusedChanges"]:
        text += item["after"]
    for item in plan["supportPlan"]["newNecessary"][0]["exampleCandidates"]:
        text += item["japanese"]
    han = sorted({c for c in text if unicodedata.name(c, "").startswith(
        ("CJK UNIFIED IDEOGRAPH-", "CJK COMPATIBILITY IDEOGRAPH-"))}, key=ord)
    records = []
    for name in ("kanji_mincho.ttf", "kanji_textbook.ttf", "kanji_brush.ttf"):
        path = A / "app" / "src" / "main" / "res" / "font" / name
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            missing = [c for c in han if ord(c) not in cmap]
        records.append({"font": name, "sha256": sha(path.read_bytes()),
                        "hanCount": len(han), "missing": missing})
    save(S / (P + "font-preparation.json"), {
        "schemaVersion": 1, "batch": "108", "androidHead": APP,
        "inventory": han, "hanCount": len(han), "bundledFonts": records,
        "fourthMode": "Default/system font, not a fourth bundled file.",
        "actualNativeInspection": False,
        "limits": "Proposed text and complete reused bodies only. Recompute final runtime Han after drafting. Cmaps do not prove glyph readability, fallback-face identity, physical-phone or successful handwriting acceptance.",
    })
    print(json.dumps({"hanCount": len(han), "fonts": records}, ensure_ascii=True))


def check():
    from build_manifest import build_manifest
    from freeze_n1_sources import metadata_record

    current()
    assert git("rev-parse", "HEAD") == HEAD and git("log", "-1", "--format=%G?") == "G"
    plan = load(S / (P + "source-completion-plan.json"))
    source = load(R / "docs" / "n1-source-snapshot.json")
    inputs = {}
    for name, info in source["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        assert sha(raw) == info["sha256"] and len(raw) == info["bytes"], name
        inputs[name] = raw
    jm = gzip.decompress(inputs["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(inputs["n1-planning-kanjidic2.xml.gz"])
    assert sha(jm) == source["jmdict"]["xmlSha256"]
    assert sha(kd) == source["kanjidic2"]["xmlSha256"]
    full_chars = ET.fromstring(kd)
    radicals = {}
    for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines():
        fields = line.split(";")
        cp = int(fields[0], 16)
        if 0x2F00 <= cp <= 0x2FD5:
            radicals[cp - 0x2F00 + 1] = chr(int(fields[5].split()[-1], 16))
    member, comparison = ET.Element("JMdict"), ET.Element("JMdict")
    for _, entry in ET.iterparse(io.BytesIO(jm), events=("end",)):
        if entry.tag == "entry":
            spellings = [e.text for e in entry.findall("k_ele/keb")]
            if any("\u52e7" in s for s in spellings):
                member.append(copy.deepcopy(entry))
            if any(s in COMPARISONS for s in spellings):
                comparison.append(copy.deepcopy(entry))
            entry.clear()
    for name, root, selection in (
        ("jmdict.xml", member, "lexical-selection.json"),
        ("comparison-jmdict.xml", comparison, "comparison-selection.json"),
    ):
        assert xml_bytes(root) == (S / (P + name)).read_bytes(), name
        assert [e.findtext("ent_seq") for e in root] == load(S / (P + selection))["entryIds"]
    assert len(member) == 46 and len(comparison) == 18
    assert len({e.findtext("ent_seq") for e in [*member, *comparison]}) == 64
    for filename, chars in (("kanjidic2.xml", "\u52e7"),
                            ("comparison-kanjidic2.xml", KANJI),
                            ("overlap-kanjidic2.xml", "\u4f9b\u796d\u52c9\u8a2a")):
        expected = ET.Element("kanjidic2")
        expected.append(copy.deepcopy(full_chars.find("header")))
        for e in full_chars.findall("character"):
            if e.findtext("literal") in chars:
                expected.append(copy.deepcopy(e))
        assert xml_bytes(expected) == (S / (P + filename)).read_bytes(), filename
    row = next(e for e in load(S / "source-index.json") if e["sourceRow"] == 119)
    assert row["kanji"] == json.loads(inputs["n1-kanji-source-20261102.json"])[118] == "\u52e7"
    char = next(e for e in full_chars if e.findtext("literal") == "\u52e7")
    assert metadata_record(char, radicals) == row["metadata"]
    kp = plan["kanjiPlan"]
    for key in ("strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
        assert kp[key] == row["metadata"][key], key
    rows = kp["readingRows"]
    assert [(r["kind"], r["raw"]) for r in rows] == [
        ("on", "\u30ab\u30f3"), ("on", "\u30b1\u30f3"), ("kun", "\u3059\u3059.\u3081\u308b")]
    assert kp["quizOnyomi"] == [r["raw"] for r in rows if r["kind"] == "on" and r["selected"]]
    assert kp["quizKunyomi"] == [r["raw"] for r in rows if r["kind"] == "kun" and r["selected"]]
    families = {e.findtext("ent_seq"): e for e in [*member, *comparison]}
    for r in rows:
        if not r["selected"]:
            assert r["example"] is None and r["disposition"] and r["qualification"]
            continue
        assert r["allocationEvidence"] and r["usefulness"]
        entry = families[r["entryIds"][0]]
        assert any(k.text == r["example"] for k in entry.findall("k_ele/keb"))
        assert any(re.text == r["reading"] for re in entry.findall("r_ele/reb"))
    verb = families["1595680"]
    assert [[x.text for x in sense.findall("stagk")] for sense in verb.findall("sense")] == [
        ["\u52e7\u3081\u308b", "\u5968\u3081\u308b"], [],
        ["\u52e7\u3081\u308b", "\u5968\u3081\u308b"]]
    baseline = load(S / (P + "baseline-plan.json"))
    for name, item in baseline["inventory"].items():
        assert metadata(R, name) == item["metadata"] and sha((R / name).read_bytes()) == item["sha256"], name
    now = {p.relative_to(R).as_posix() for folder in ("kanji", "words")
           for p in (R / folder).glob("*.md")}
    assert now == set(baseline["inventory"])
    assert build_manifest(R) == load(R / "manifest.json") == baseline["runtimeManifest"]
    assert sha((R / "manifest.json").read_bytes()) == baseline["manifestRawSha256"]
    assert not git("diff", HEAD, "--", "manifest.json", "kanji", "words", "strokes")
    assert not git("diff", "--cached", HEAD, "--", "manifest.json", "kanji", "words", "strokes")
    assert not (R / "kanji" / "\u52e7.md").exists()
    assert not (R / "words" / "\u52e7\u544a.md").exists()
    assert not (R / "strokes" / "\u52e7.json").exists()
    for item in load(S / (P + "comparison-article-snapshots.json")):
        path = R / item["article"]
        assert sha(path.read_bytes()) == item["sha256"] and path.read_text(encoding="utf-8") == item["text"]
        assert metadata(R, item["article"]) == item["metadata"]
    mapping = plan["linkPlan"]
    pairs = [(m["kanji"], m["article"]) for m in load(S / "baseline-word-candidates.json")
             if m["kanji"] == "\u52e7"]
    assert pairs == [tuple(p) for p in mapping["activatedBaselinePairs"]]
    all_pairs = set()
    for item in plan["supportPlan"]["reused"] + plan["supportPlan"]["newNecessary"]:
        meta = metadata(R, item["article"]) if (R / item["article"]).exists() else item
        assert meta["word"] == item["word"] and meta["reading"] == item["reading"]
        for kanji in meta["kanji"]:
            if kanji == "\u52e7" or (R / "kanji" / (kanji + ".md")).exists():
                all_pairs.add((kanji, item["article"]))
    assert all_pairs == {tuple(p) for p in mapping["allMappedPairs"]}
    directions = {(f"kanji/{k}.md", w) for k, w in all_pairs} | {
        (w, f"kanji/{k}.md") for k, w in all_pairs}
    assert directions == {(d["from"], d["to"]) for d in mapping["requiredDirections"]}
    for d in mapping["requiredDirections"]:
        path = R / d["from"]
        present = path.exists() and f"]({d['relative']})" in path.read_text(encoding="utf-8")
        assert present == d["currentlyPresent"]
    for edit in mapping["exactReusedChanges"]:
        text = (R / edit["article"]).read_text(encoding="utf-8")
        assert text.count(edit["before"]) == 1 and edit["after"] not in text, edit["article"]
    distractors = kp["curatedDistractors"]
    assert len({d["kanji"] for d in distractors}) == 3
    assert not ({d["kanji"] for d in distractors} & set(kp["quizExclusions"]))
    for d in distractors + kp["directGuardRationale"] + kp["otherComparedLabels"]:
        assert metadata(R, f"kanji/{d['kanji']}.md")["title"] == d["actualTitle"]
    assert kp["title"] not in {v["metadata"]["title"] for n, v in baseline["inventory"].items()
                              if n.startswith("kanji/")}
    for a, b in [d["pair"] for d in plan["supportPlan"]["wordQuizAudit"]["newDirectPairs"]]:
        for w in (a, b):
            assert w == "\u52e7\u544a" or (R / "words" / (w + ".md")).exists(), w
    legacy = {m["metadata"]["kanji"] for n, m in baseline["inventory"].items()
              if n.startswith("kanji/") and len(m["metadata"].get("distractors", [])) < 3}
    assert legacy == set(LEGACY) == set(plan["legacyFallbackPlan"]["legacyFewerThanThree"])
    incoming = [m["metadata"]["kanji"] for n, m in baseline["inventory"].items()
                if n.startswith("kanji/") and "\u52e7" in m["metadata"].get("distractors", [])]
    assert incoming == plan["legacyFallbackPlan"]["incomingTargetCuratedReferences"] == []
    for receipt in load(S / (P + "public-source-receipts.json")) + [
        load(S / (P + "support-public-source-receipt.json"))
    ]:
        raw = gzip.decompress((S / receipt["archive"]).read_bytes())
        assert sha(raw) == receipt["rawSha256"] and len(raw) == receipt["rawBytes"]
        assert sha((S / receipt["archive"]).read_bytes()) == receipt["archiveSha256"]
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    svg = (S / (P + "kanjivg.svg")).read_bytes()
    stroke = load(S / (P + "stroke-evidence.json"))
    assert sha(svg) == stroke["sha256"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == 13 and [e.get("id") for e in paths] == [f"kvg:052e7-s{i}" for i in range(1, 14)]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == (
        source["kanjivg"]["converter"]["normalizedSha256"]) == plan["strokePlan"]["converterNormalizedSha256"]
    fonts = load(S / (P + "font-preparation.json"))
    for f in fonts["bundledFonts"]:
        path = A / "app" / "src" / "main" / "res" / "font" / f["font"]
        assert sha(path.read_bytes()) == f["sha256"]
    assert not fonts["actualNativeInspection"]
    result = {
        "schemaVersion": 1, "execution": 860, "batch": "108", "head": HEAD,
        "allFiveFrozenInputHashesVerified": True, "bothDecompressedDictionaryHashesVerified": True,
        "exactMemberFamiliesReproduced": 46, "exactComparisonFamiliesReproduced": 18,
        "distinctCompleteFamilies": 64, "distinctCompleteCharacterRecordsReproduced": 14,
        "baselineArticlesUnchanged": len(now), "exactSourceRowMetadataAndUnicodeRadicalVerified": True,
        "plannedFullReadingDispositions": 3, "plannedSelectedReadingKeys": 2,
        "plannedSourceOnlyKeysOffered": 0, "sourceSenseRestrictionsChecked": True,
        "allMappedPairs": len(all_pairs), "requiredDirections": len(directions),
        "activatedBaselinePairs": len(pairs), "exactReusedChangesVerified": 3,
        "sourceOnlyCandidateAndQuizAndLegacyChecksPassed": True,
        "pinned13PathGeometryAndConverterVerified": True,
        "manifestFreshAndUnchanged": True, "runtimeChanged": False,
        "sourcePreparationComplete": True, "runtimeDraftAuditExecuted": False,
        "independentReviewersLaunched": 0, "androidOrNativeExecuted": False,
        "limits": "Mechanical source-plan checks, not independent teaching/production quiz/rendered/native review or runtime acceptance. Runtime exact-current audit remains required.",
    }
    save(S / (P + "source-completion-audit.json"), result)
    print(json.dumps(result, ensure_ascii=True))


NEXT = (
    "SAME108 next bounded LOCAL UNREVIEWED runtime draft only, using committed "
    "batch-108-source-completion-plan.json and source-completion-audit.json. Row119 勧; "
    "64completefamilies/14distinctrawcharacters, fivefrozeninputs and bothXMLhashes "
    "reproduced. Preserve fullon[カン,ケン]/fullkun[すす.める], selectカン/すす.める; "
    "ケン source-only because usable example not established, NOT invalid/obsolete/rare. "
    "Add only 勧.md, pinned13stroke conversion and necessary 勧告かんこく, no invented "
    "vocabularylevel; reuse 勧めるすすめる N3 identity/senses/restrictions. Exact reused "
    "edits: 勧める componentlink plus additive direct推薦/提案 wordguards, and sourced告 "
    "Commonwords backlink. ALL3mappedpairs6directions/1activatedbaselinepair; "
    "threecurated観確権 and direct勧guards励供勉支, new勧告sixdirectwordguards. "
    "57proposedHan/allthreebundledcmaps checked; 隹 absent each, explicit default/system "
    "plus threefont nativefallback target, not glyphfailure/waiver. Recompute final "
    "runtimeHan. No runtime authored, no reviewers/HOST/native/publication/109 at860. "
    "Generic source-plan auditor currently rejects reusedsupport; do NOT fabricate "
    "ledger/duplicate/drop reusedarticle or claim generic pass. Before draft acceptance "
    "implement/run checked equivalent exact-current source/membership/baseline/readings/"
    "quiz/ALLlinks/strokes/manifest invariant audit; preserve actual failure/yield if "
    "any required invariant unavailable. Source completion is NOT content review. "
    "Then normal signed clean local UNREVIEWED freeze; both serial blind different-family "
    "content reviews on same snapshot, actual models/complete reports/serial internal "
    "tools/original-session confirmations as needed; qualified signed clean bf30 "
    "Android non-skippedHOST, actual production option samples/shortpools, native full "
    "ContentSync ONCE/meaning/curated reading/drawing/articles/Back/offline/fourfonts/"
    "rendered; requiredPython/vocabulary/validator/freshmanifest/all publishingbudgets "
    "remain. Latest-main nonrewriting integration/changedteaching review/combined "
    "validation/normal signing/owner fastforward/exact terminal greenCI/EVERY immutable "
    "ZIP runtimehash and18000entries42MiBcompressed80MiBinflated56MiBretained/"
    "perfile-media-safepath/verifiedownerissue gates remain before delivery. Preserve "
    "FULLlivehistory/792correction/all prior denials/OOMs/accepted publications and "
    "unresolved定/違,支払う/支払,勘/識,勅/訓. Recovered siblings only; committed "
    "sources/approvedinputs/controlhelpers, no optional historicalsessionrecipes. "
    "Authenticate live launcher ancestry/session/currentcheckpoint/exactsignedheads/"
    "clean-accountedstate. Parent owns runner.lock; NOchild reacquire/delete/unlock/"
    "readprobe. Preserve/report/yield actual newdenial/signinghang/uncertainownership; "
    "no retry/bypass/permissions expansion/guardchanges/concurrentheavywork/"
    "authoragents/secondrunner. Published134/1228,remaining1094 unchanged; six "
    "earlier-level dispositions are not issue60 acceptancecredit. Compatible clients125/"
    "132 required; physical-phone/handwriting-model/general-release/whole-set "
    "acceptance outstanding; project incomplete."
)


def seal():
    current()
    text = (L / "source-tests-860.txt").read_text(encoding="utf-8-sig")
    count = int(re.search(r"Ran (\d+) tests", text)[1])
    assert count == 97 and text.rstrip().endswith("OK")
    assert "Verified 46 complete" in (L / "extract-member-860.txt").read_text(encoding="utf-8-sig")
    assert "Verified 18 complete" in (L / "extract-comparison-860.txt").read_text(encoding="utf-8-sig")
    assert "0 error(s)" in (L / "validate-860.txt").read_text(encoding="utf-8-sig")
    assert not git("diff", HEAD, "--", "manifest.json", "kanji", "words", "strokes")
    audit = load(S / (P + "source-completion-audit.json"))
    assert audit["sourcePreparationComplete"] and not audit["runtimeChanged"]
    for suffix in ("membership.json", "progress.json"):
        path = S / (P + suffix)
        state = load(path)
        state.update(status="source-complete-for-later-local-unreviewed-draft",
                     sourcePreparationComplete=True,
                     sourceCompletionPlan=P + "source-completion-plan.json",
                     sourceCompletionAudit=P + "source-completion-audit.json")
        save(path, state)
    for suffix, source_path in (
        ("prepare-860.py", Path(__file__)),
        ("checks-860.ps1", C / "checks-batch-108-source-860.ps1"),
    ):
        destination = S / (P + suffix)
        assert not destination.exists()
        shutil.copyfile(source_path, destination)
    for name in ("preflight", "source-tests", "extract-member", "extract-comparison",
                 "validate", "manifest", "manifest-diff", "budget", "vocabulary", "audit", "whitespace"):
        extension = "json" if name == "preflight" else "txt"
        path = L / f"{name}-860.{extension}"
        destination = S / (P + f"checks-860-{name}.{extension}.gz")
        assert path.exists() and not destination.exists()
        destination.write_bytes(gzip.compress(path.read_bytes(), mtime=0))
        assert gzip.decompress(destination.read_bytes()) == path.read_bytes()
    evidence = [{"path": p.relative_to(R).as_posix(), "sha256": sha(p.read_bytes()),
                 "bytes": p.stat().st_size} for p in sorted(S.glob(P + "*"))]
    record = {
        "schemaVersion": 1, "execution": 860, "batch": "108",
        "recordedAt": datetime.now(timezone.utc).isoformat(),
        "startingCommit": HEAD, "publishedBaseCommit": PUBLIC,
        "status": "local-source-completion-only", "membership": ["\u52e7"], "sourceRows": [119],
        "sourcePreparationComplete": True, "memberFamilies": 46, "comparisonFamilies": 18,
        "distinctCompleteFamilies": 64, "distinctCompleteRawCharacterRecords": 14,
        "readingDispositions": 3, "selectedReadingKeys": 2, "sourceOnlyKeysOffered": 0,
        "allMappedPairs": 3, "requiredDirections": 6, "activatedBaselinePairs": 1,
        "proposedHan": 57, "bundledFontsChecked": 3, "cmapAbsentNativeTarget": ["\u96b9"],
        "sourceTests": count, "validatorManifestBudgetVocabularyPassed": True,
        "vocabularyCoverageLimit": "Existing pilot coverage2122/2431, not complete coverage or a claim that unrelated baseline gaps were fixed.",
        "exactCurrentSourceAudit": P + "source-completion-audit.json",
        "runtimeDraftAuditDisposition": "Not executed: no runtime exists. Checked equivalent exact-current audit is required for the later legitimate reused-support draft; generic CLI's empty-reused restriction is not bypassed or retroclaimed passed.",
        "runtimeChanged": False, "runtimePublished": False, "pushed": False,
        "independentReviewersLaunched": 0, "androidOrNativeExecuted": False,
        "androidHead": APP, "publishedAdditions": 134, "remainingAdditions": 1094,
        "parentLockTouched": False, "fullHistoryBefore": str(L / "progress-before-860.json"),
        "evidence": evidence, "nextAction": NEXT,
        "limits": "Coordinator source inspection/mechanical source checks only, not accepted teaching, independent review, runtime/native/phone/handwriting-model/general-release/whole-set acceptance.",
    }
    assert not (S / "execution-860.json").exists()
    save(S / "execution-860.json", record)
    print("Source-only completion evidence sealed for normal local signing; no runtime content authored.")


def finish():
    p = current()
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == HEAD and git("log", "-1", "--format=%G?") == "G"
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("status", "--porcelain", "--untracked-files=all")
    changed = git("diff", "--name-only", HEAD, head).splitlines()
    assert changed and all(name.startswith("docs/n1-sources/batch-108-") or
                           name == "docs/n1-sources/execution-860.json" for name in changed)
    assert not git("diff", HEAD, head, "--", "manifest.json", "kanji", "words", "strokes")
    record = load(S / "execution-860.json")
    for item in record["evidence"]:
        assert sha((R / item["path"]).read_bytes()) == item["sha256"], item["path"]
    assert sha((S / (P + "prepare-860.py")).read_bytes()) == sha(Path(__file__).read_bytes())
    assert record["sourcePreparationComplete"] and record["distinctCompleteFamilies"] == 64
    issue = load(L / "issue-receipt-860.json")
    assert issue["verified"] and issue["author"] == "stop-cran" and issue["localCommit"] == head
    before = copy.deepcopy(p)
    p["execution860StartingState"]["status"] = "signed-source-completion-checkpoint-complete"
    checkpoint = {
        "execution": 860, "batch": "108", "status": "continue",
        "signedLocalCommit": head, "signature": "G", "record": "docs/n1-sources/execution-860.json",
        "recordSha256": sha((S / "execution-860.json").read_bytes()),
        "membership": ["\u52e7"], "sourcePreparationComplete": True,
        "distinctCompleteFamilies": 64, "distinctCompleteRawCharacterRecords": 14,
        "runtimeChanged": False, "runtimePublished": False, "pushed": False,
        "publishedAdditions": 134, "remainingAdditions": 1094,
        "issueUpdate": issue["url"], "ownerAuthorAndBodyAndUrlVerified": True,
        "parentLockTouched": False, "nextAction": NEXT,
    }
    p["execution860CoordinatorCheckpoint"] = checkpoint
    p.update(checkpoint=860, status="continue",
             stage="batch-108-sources-complete-awaiting-local-unreviewed-runtime-draft",
             nextAction=NEXT, blocker=None)
    allowed = {"checkpoint", "status", "stage", "nextAction", "blocker", "execution860StartingState"}
    for key in before:
        if key not in allowed:
            assert p[key] == before[key], key
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p and len(p) == len(before) + 1
    print(json.dumps(checkpoint, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("start", "inspect", "packet", "supplement", "archive", "fonts", "check", "seal", "finish"))
    globals()[parser.parse_args().mode]()
