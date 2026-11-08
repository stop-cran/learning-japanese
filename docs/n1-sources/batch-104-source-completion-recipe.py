"""Complete batch 104 source preparation without changing runtime content."""
import argparse
import copy
import gzip
import hashlib
import json
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
A = C.parent / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "2b83c2d7-d1f1-4f27-9b9d-b5cd7a341d95"
BASE = "9d44e63ffaa72875540f68cc55af284ffe6e4f56"
MAIN = "2491799cffe960a7664a6135614b452e24dce459"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata, offered_keys, quiz_readings
from build_manifest import build_manifest, sha256 as manifest_sha256
from extract_n1_jmdict import extract


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    temporary = path.with_suffix(path.suffix + ".797.tmp")
    assert not temporary.exists(), temporary
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def git(*args, root=R):
    return subprocess.check_output(["git", "--no-pager", "-C", str(root), *args],
                                   encoding="utf-8").strip()


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
    assert git("rev-parse", "origin/main") == MAIN
    assert git("branch", "--show-current") == "content/n1-kanji"
    p = load(C / "progress.json")
    assert (p["checkpoint"], p["batch"], p["status"]) == (796, "104", "continue")
    assert p["lastPublishedCommit"] == MAIN and p["remainingAdditions"] == 1098
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    embedded = json.loads(text.split(
        "Current execution checkpoint (complete historical state remains at checkpointHistory paths):", 1)[1])
    assert embedded["checkpoint"] == p["checkpoint"]
    assert embedded["nextAction"] == p["nextAction"]
    role = load(L / "preflight-797.json")
    assert role["liveParentPid"] == 13320 and role["sessionId"] == L.name
    assert not role["lockTouched"]
    assert not (L / "progress-before-797.json").exists()
    shutil.copyfile(C / "progress.json", L / "progress-before-797.json")
    state = {
        "execution": 797, "batch": "104", "startingHead": BASE, "freshOriginMain": MAIN,
        "androidHead": APP, "startedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "SAME104 bounded source completion only; no runtime draft, reviewer, Android/native, publication,105 or second runner.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Entire request loaded/decoded and embedded checkpoint parsed before implementation. Operative contract, approved issue and final796 directly inspected; historical middle parsed, not freshly semantically re-reviewed."},
        "runnerPreflight": role,
        "artifactPathPreflight": "Approved control helpers, committed source packets and frozen workspace inputs only; no optional historical-session recipes accessed.",
        "worktrees": "Wholly clean dedicated signed content and qualified Android heads; fresh main unchanged. Canonical repositories not accessed.",
        "actualNewPermissionDenials": [],
        "status": "source-completion-in-progress",
    }
    p["execution797StartingState"] = state
    p.update(stage="batch-104-source-completion-in-progress", nextAction=state["scope"], blocker=None)
    save(C / "progress.json", p)
    print("Starting scope persisted with full live history.")


def navigation():
    result = {}
    pattern = re.compile(r"censur|impeach|denounc|accus|blam|reproach|condemn|critic|scold|rebuk|investigat|indict|prosecut", re.I)
    for folder in ("kanji", "words"):
        hits = []
        for path in sorted((R / folder).glob("*.md")):
            relative = path.relative_to(R).as_posix()
            m = metadata(R, relative)
            if pattern.search(m["title"]):
                hits.append({"article": relative, "metadata": m, "sha256": sha(path.read_bytes())})
        result[folder] = hits
    save(S / "batch-104-label-navigation-797.json", {
        "baseCommit": BASE, "pattern": pattern.pattern, "matches": result,
        "limits": "Complete title scan is candidate navigation, not a whole-corpus semantic audit. Applicable complete families and bodies must be read separately."
    })
    for folder, hits in result.items():
        print(folder)
        for hit in hits:
            m = hit["metadata"]
            print(hit["article"], m["title"], "distractors=",
                  m.get("distractors", []), "exclusions=", m.get("quiz_exclusions", []))
    for char in "刻効労努":
        name = f"kanji/{char}.md"
        print(name, json.dumps(metadata(R, name), ensure_ascii=False))


def discovery():
    _, _, jm, kd = frozen()
    existing = {p.stem for p in (R / "kanji").glob("*.md")}
    terms = re.compile(r"censur|impeach|denounc|accus|blam|reproach|condemn|critic|scold|rebuk|investigat|indict|prosecut", re.I)
    print("CHARACTER-SENSE CANDIDATES")
    for node in kd.findall("character"):
        char = node.findtext("literal")
        meanings = [m.text for m in node.findall("reading_meaning/rmgroup/meaning")
                    if "m_lang" not in m.attrib]
        if char in existing and any(terms.search(m) for m in meanings):
            name = f"kanji/{char}.md"
            print(name, metadata(R, name)["title"], meanings)
    existing_words = {p.stem for p in (R / "words").glob("*.md")}
    print("EXISTING WORDS WITH RELEVANT FROZEN SENSES")
    for entry in jm:
        spellings = [n.text for n in entry.findall("k_ele/keb")]
        readings = [n.text for n in entry.findall("r_ele/reb")]
        matches = existing_words.intersection(spellings + readings)
        glosses = [n.text for n in entry.findall("sense/gloss")]
        if matches and any(terms.search(m) for m in glosses):
            print(entry.findtext("ent_seq"), sorted(matches), glosses)


def packet():
    snapshot, inputs, jm, kd = frozen()
    terms = ["批判", "批評", "評論", "責める", "攻撃", "叩く", "切る", "叱る",
             "絞る", "恨む", "意見", "努力", "効果", "刻む", "詰問", "調査",
             "研究", "弾", "不正", "裁判官"]
    selected = []
    selection_map = {}
    for word in terms:
        rows = [e for e in jm if word in [n.text for n in e.findall("k_ele/keb")]]
        assert rows, word
        selection_map[word] = [e.findtext("ent_seq") for e in rows]
        selected.extend(selection_map[word])
    ids = list(dict.fromkeys(selected))
    save(S / "batch-104-comparison-selection.json", {
        "schemaVersion": 1, "batch": "104", "entryIds": ids, "terms": selection_map,
        "selectionRule": "Every complete frozen family with an exact written match to the selected comparison/support/context terms; preserve aliases, alternate readings, all senses and restrictions.",
        "sourceSnapshot": "docs/n1-source-snapshot.json",
        "limits": "Bounded author evidence, not independent review or unrestricted synonym substitutions."
    })
    raw = extract(inputs["n1-implementation-JMdict_e.gz"],
                  snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
    (S / "batch-104-comparison-jmdict.xml").write_bytes(raw)
    compact = []
    for entry in ET.fromstring(raw):
        for node in entry.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact.append(ET.tostring(entry, encoding="unicode"))
    text = ("\n".join(compact) + "\n").encode("utf-8")
    (C / "batch-104-comparison-full-family-reading.txt").write_bytes(text)
    (S / "batch-104-comparison-full-family-reading.txt.gz").write_bytes(gzip.compress(text, mtime=0))
    chars = list("弾刻効努責詰査調究罪処偵力亥")
    root = ET.Element("kanjidic2")
    root.append(copy.deepcopy(kd.find("header")))
    for char in chars:
        root.append(copy.deepcopy(next(e for e in kd.findall("character")
                                      if e.findtext("literal") == char)))
    ET.indent(root, space="  ")
    raw_kd = ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"
    (S / "batch-104-comparison-kanjidic2.xml").write_bytes(raw_kd)
    compact_kd = []
    for element in root.findall("character"):
        for node in element.iter():
            if node.text and not node.text.strip():
                node.text = None
            node.tail = None
        compact_kd.append(ET.tostring(element, encoding="unicode"))
    kd_text = ("\n".join(compact_kd) + "\n").encode("utf-8")
    (C / "batch-104-comparison-character-reading.txt").write_bytes(kd_text)
    (S / "batch-104-comparison-character-reading.txt.gz").write_bytes(gzip.compress(kd_text, mtime=0))
    names = [f"kanji/{c}.md" for c in chars if (R / "kanji" / f"{c}.md").exists()]
    names += [f"words/{word}.md" for word in terms if (R / "words" / f"{word}.md").exists()]
    snapshots = []
    for name in names:
        raw_body = (R / name).read_bytes()
        snapshots.append({"article": name, "metadata": metadata(R, name),
                          "sha256": sha(raw_body), "bytes": len(raw_body),
                          "body": raw_body.decode("utf-8")})
    save(S / "batch-104-existing-article-snapshots.json", {
        "baseCommit": BASE, "articles": snapshots,
        "limits": "Exact full baseline bodies supplied for bounded comparisons; retention/hash is not a fresh read or review certification."
    })
    print(json.dumps({"families": len(ids), "familyLines": len(compact), "compactBytes": len(text),
                      "characterRecords": len(chars), "compactCharacterBytes": len(kd_text),
                      "existingArticles": names}, ensure_ascii=False))


def public():
    from html.parser import HTMLParser

    class Blocks(HTMLParser):
        def __init__(self):
            super().__init__()
            self.depth = 0
            self.parts = []

        def handle_starttag(self, tag, attrs):
            if tag == "div":
                if self.depth:
                    self.depth += 1
                elif "kijiWrp" in dict(attrs).get("class", "").split():
                    self.depth = 1
                    self.parts.append("\n[ENTRY BLOCK]\n")
            if self.depth and tag in {"p", "h2", "h3", "br", "li"}:
                self.parts.append("\n")

        def handle_endtag(self, tag):
            if tag == "div" and self.depth:
                self.depth -= 1
                if not self.depth:
                    self.parts.append("\n[END BLOCK]\n")

        def handle_data(self, data):
            if self.depth:
                self.parts.append(data)

    source = C / "batch-104-dan-character.html"
    raw = source.read_bytes()
    parser = Blocks()
    parser.feed(raw.decode("utf-8"))
    text = "\n".join(line.strip() for line in "".join(parser.parts).splitlines()
                     if line.strip()) + "\n"
    assert "弾劾" in text and "ダン" in text
    target = S / "batch-104-dan-character-public-text.txt"
    target.write_text(text, encoding="utf-8")
    archive = S / "batch-104-dan-character.html.gz"
    archive.write_bytes(gzip.compress(raw, mtime=0))
    save(S / "batch-104-public-source-completion-receipt.json", {
        "url": "https://www.weblio.jp/content/%E5%BC%BE",
        "downloadedAt": datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).isoformat(),
        "rawBytes": len(raw), "rawSha256": sha(raw), "archive": archive.name,
        "archiveSha256": sha(archive.read_bytes()), "losslessGzip": gzip.decompress(archive.read_bytes()) == raw,
        "extractedText": target.name, "extractedTextSha256": sha(target.read_bytes()),
        "scope": "Actual Digital Daijisen character heading and numbered blame/criticism sense for 弾劾; other homographs, word families and site blocks are not allocation evidence.",
        "limits": "Text extraction strips links/formatting. Exact heading/sense requires author inspection; hash is not independent review."
    })
    print("\n".join(text.splitlines()[:9]))


def prepared():
    from fontTools.ttLib import TTFont

    plan = load(S / "batch-104-authoring-plan.json")
    _, inputs, _, _ = frozen()
    text = plan["proposedHanText"]
    han = sorted(set(c for c in text if 0x3400 <= ord(c) <= 0x9FFF or
                     0xF900 <= ord(c) <= 0xFAFF or 0x20000 <= ord(c) <= 0x2FFFF))
    fonts = []
    for path in sorted((A / "app" / "src" / "main" / "res" / "font").glob("kanji_*.ttf")):
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            missing = [c for c in han if ord(c) not in cmap]
        fonts.append({"path": str(path), "sha256": sha(path.read_bytes()),
                      "keyGlyphPresence": {c: c not in missing for c in han},
                      "allProposedMissing": missing})
    assert len(fonts) == 3
    radical = next(line for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines()
                   if line.startswith("2F12;"))
    assert radical.split(";")[5] == "<compat> 529B"
    rare = sorted(set(c for c in text if 0x2E80 <= ord(c) <= 0x2FDF or
                      0x3400 <= ord(c) <= 0x4DBF or 0xF900 <= ord(c) <= 0xFAFF or
                      0x20000 <= ord(c) <= 0x2FFFF))
    save(S / "batch-104-font-preparation.json", {
        "schemaVersion": 1, "batch": "104", "proposedTextInventory": text,
        "inventoryScope": plan["fontInventoryScope"], "auditedHan": han,
        "auditedHanCount": len(han), "fonts": fonts, "rareHanRangeCharacters": rare,
        "unicodeRadicalRecord": radical,
        "mechanism": "Unchanged RareHan.kt and RareHanTest.kt inspected. Three actual bundled cmaps checked; ordinary力U+529B versus compatibility radicalU+2F12 distinguished. Fourth/default system typeface requires later actual native rendering, not a fabricated host cmap.",
        "missingGlyphDisposition": plan["fontPreparationDisposition"],
        "limits": "Proposed text only; cmap presence/absence is not native rendered acceptance. Final actual-Han audit, non-skipped RareHan test and fresh native four-font/all-Han rendering remain mandatory."
    })
    snapshots = load(S / "batch-104-existing-article-snapshots.json")["articles"]
    save(S / "batch-104-baseline-plan.json", {
        "schemaVersion": 1, "batch": "104", "baseCommit": BASE, "publishedBase": MAIN,
        "androidHead": APP, "manifestSha256": sha((R / "manifest.json").read_bytes()),
        "contentVersion": load(R / "manifest.json")["contentVersion"],
        "allExistingRuntimeBytesMustRemain": "No baseline runtime edits. Preserve every baseline file hash, metadata, identity, primary reading, easier level, full reading/order and original exclusion. The exact immutable base manifest is the complete hash inventory, not merely these comparison snapshots.",
        "comparisonArticleSnapshots": [
            {k: v for k, v in record.items() if k != "body"} for record in snapshots
        ],
        "reusedPassageChanges": [],
        "allMappedReciprocalPairs": plan["allMappedReciprocalPairs"],
        "requiredDirections": 2, "activatedBaselinePairs": [],
        "newRuntimeFiles": ["kanji/劾.md", "strokes/劾.json", "words/弾劾.md"],
        "missingComponent": plan["missingComponentDisposition"],
        "limits": "Source-stage preservation plan. Actual runtime diff/metadata/link/font/manifest checks are required again at drafting and acceptance, not certified in advance."
    })
    progress = load(S / "batch-104-progress.json")
    progress.update(status="source-prepared-not-drafted", sourcePreparationComplete=True,
                    authoringPlan="batch-104-authoring-plan.json",
                    comparisonFamilies=23, nextAction=plan["nextAction"],
                    limits="Source preparation complete; no runtime authoring, independent review or app/native/publication acceptance. Original initial source observations remain historical.")
    save(S / "batch-104-progress.json", progress)
    print(json.dumps({"sourcePreparationComplete": True, "proposedHan": len(han),
                      "missingByFont": [f["allProposedMissing"] for f in fonts],
                      "geometryConverted": False, "runtimeChanged": False}, ensure_ascii=True))


def canonical(element):
    return (element.tag, tuple(sorted(element.attrib.items())),
            (element.text or "").strip(), tuple(canonical(c) for c in element))


def audit():
    snapshot, inputs, jm, kd = frozen()
    plan = load(S / "batch-104-authoring-plan.json")
    selection = load(S / "batch-104-comparison-selection.json")
    member_ids = load(S / "batch-104-lexical-selection.json")["entryIds"]
    assert member_ids == [e.findtext("ent_seq") for e in jm
                          if any("劾" in k.text for k in e.findall("k_ele/keb"))]
    assert len(member_ids) == 4
    comparisons = []
    for word, recorded_ids in selection["terms"].items():
        ids = [e.findtext("ent_seq") for e in jm
               if word in [n.text for n in e.findall("k_ele/keb")]]
        assert ids == recorded_ids, word
        comparisons.extend(ids)
    assert list(dict.fromkeys(comparisons)) == selection["entryIds"]
    assert len(selection["entryIds"]) == 23
    for xml, compact, ids in [
        ("batch-104-jmdict.xml", "batch-104-full-family-reading.txt.gz", member_ids),
        ("batch-104-comparison-jmdict.xml", "batch-104-comparison-full-family-reading.txt.gz", selection["entryIds"])
    ]:
        raw = (S / xml).read_bytes()
        assert raw == extract(inputs["n1-implementation-JMdict_e.gz"],
                              snapshot["inputs"]["n1-implementation-JMdict_e.gz"]["sha256"], ids)
        lines = gzip.decompress((S / compact).read_bytes()).decode("utf-8").splitlines()
        entries = ET.fromstring(raw).findall("entry")
        assert len(lines) == len(entries)
        assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(lines, entries))
    raw_chars = {e.findtext("literal"): e for e in kd.findall("character")}
    chars = ET.parse(S / "batch-104-comparison-kanjidic2.xml").getroot().findall("character")
    assert len(chars) == 14
    assert all(canonical(e) == canonical(raw_chars[e.findtext("literal")]) for e in chars)
    compact_chars = gzip.decompress((S / "batch-104-comparison-character-reading.txt.gz").read_bytes()).decode("utf-8").splitlines()
    assert len(compact_chars) == len(chars)
    assert all(canonical(ET.fromstring(a)) == canonical(b) for a, b in zip(compact_chars, chars))
    original = ET.parse(S / "batch-104-kanjidic2.xml").getroot().find("character")
    assert canonical(original) == canonical(raw_chars["劾"])
    row = load(S / "batch-104-input-metadata.json")["sourceIndexRecord"]
    assert row == next(r for r in load(S / "source-index.json") if r["kanji"] == "劾")
    assert row["sourceRow"] == 115 and json.loads(inputs["n1-kanji-source-20261102.json"])[114] == "劾"
    proposed = plan["proposedMetadata"]
    for key in ["kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"]:
        assert proposed[key] == row["metadata"][key], key
    assert [(r["kind"], r["reading"]) for r in plan["readingDispositions"]] == [("on", "ガイ")]
    assert plan["readingKeys"] == {
        "on": offered_keys(quiz_readings(proposed, "onyomi")),
        "kun": offered_keys(quiz_readings(proposed, "kunyomi"))
    } == {"on": ["がい"], "kun": []}
    assert len(proposed["distractors"]) == len(set(proposed["distractors"])) == 3
    assert len(proposed["quiz_exclusions"]) == len(set(proposed["quiz_exclusions"])) == 5
    assert not set(proposed["distractors"]) & set(proposed["quiz_exclusions"])
    assert proposed["title"] not in [metadata(R, p.relative_to(R).as_posix())["title"]
                                    for p in (R / "kanji").glob("*.md")]
    for char in proposed["distractors"] + proposed["quiz_exclusions"]:
        m = metadata(R, f"kanji/{char}.md")
        assert len(m["distractors"]) >= 3
        assert not set(proposed["distractors"]) & set(m.get("quiz_exclusions", []))
    snapshots = load(S / "batch-104-existing-article-snapshots.json")["articles"]
    assert len(snapshots) == 31
    for record in snapshots:
        raw = (R / record["article"]).read_bytes()
        assert sha(raw) == record["sha256"] and len(raw) == record["bytes"]
        assert raw.decode("utf-8") == record["body"]
        assert metadata(R, record["article"]) == record["metadata"]
    assert plan["reusedPassageChanges"] == []
    word = plan["newSupportMetadata"][0]
    assert word["word"] == "弾劾" and word["reading"] == "だんがい"
    assert word["kanji"] == ["弾", "劾"] and "jlpt" not in word
    assert not (R / "kanji" / "弾.md").exists()
    assert len(word["quiz_exclusions"]) == len(set(word["quiz_exclusions"])) == 7
    assert word["quiz_exclusions"] == [r["other"] for r in plan["wordQuizPlan"]["directGuards"]]
    for guard in plan["wordQuizPlan"]["directGuards"]:
        assert (R / "words" / (guard["other"] + ".md")).is_file()
        assert guard["label"] == metadata(R, f"words/{guard['other']}.md")["title"]
        assert set(guard["entryIds"]) <= set(selection["entryIds"])
    assert proposed["quiz_exclusions"] == [r["other"] for r in plan["quizPlan"]["directKanjiGuards"]]
    assert plan["allMappedReciprocalPairs"] == [["劾", "words/弾劾.md"]]
    assert plan["requiredDirections"] == 2 and not plan["activatedBaselinePairs"]
    assert load(S / "batch-104-source-navigation.json")["candidates"] == []
    assert not [p.name for p in (R / "words").glob("*.md") if
                metadata(R, p.relative_to(R).as_posix())["reading"] == "だんがい"]
    assert not [r for r in load(S / "baseline-word-candidates.json") if r["kanji"] == "劾"]
    pages = load(S / "batch-104-public-source-receipts.json") + [
        load(S / "batch-104-public-source-completion-receipt.json")]
    for page in pages:
        raw = (S / page["archive"]).read_bytes()
        assert sha(raw) == page["archiveSha256"]
        assert sha(gzip.decompress(raw)) == page["rawSha256"]
        assert sha((S / page["extractedText"]).read_bytes()) == page["extractedTextSha256"]
    dan = (S / "batch-104-dan-character-public-text.txt").read_text(encoding="utf-8")
    assert "３ 罪をあばく。責めたてる。" in dan and "弾劾" in "\n".join(dan.splitlines()[:9])
    assert "デジタル大辞泉" in gzip.decompress((S / pages[-1]["archive"]).read_bytes()).decode("utf-8")
    svg = (S / "batch-104-kanjivg.svg").read_bytes()
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == row["kanjivgInventory"]["sha"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert len(paths) == 8 and [p.attrib["id"] for p in paths] == [f"kvg:052be-s{i}" for i in range(1, 9)]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == snapshot["kanjivg"]["converter"]["normalizedSha256"]
    fonts = load(S / "batch-104-font-preparation.json")
    assert len(fonts["fonts"]) == 3 and not fonts["rareHanRangeCharacters"]
    assert fonts["proposedTextInventory"] == plan["proposedHanText"]
    assert all(sha(Path(f["path"]).read_bytes()) == f["sha256"] for f in fonts["fonts"])
    assert not (R / "kanji" / "劾.md").exists() and not (R / "strokes" / "劾.json").exists()
    assert not (R / "words" / "弾劾.md").exists()
    assert git("rev-parse", "HEAD") == BASE and git("log", "-1", "--format=%G?") == "G"
    assert git("rev-parse", "origin/main") == MAIN
    clean(A, APP)
    assert not git("diff", BASE, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    original_manifest = subprocess.check_output(["git", "show", f"{BASE}:manifest.json"], cwd=R)
    assert original_manifest == (R / "manifest.json").read_bytes()
    manifest = load(R / "manifest.json")
    assert build_manifest(R) == manifest
    count = 0
    for section, entries in manifest.items():
        if not isinstance(entries, dict):
            continue
        for name, digest in entries.items():
            path = R / name
            actual = sha(path.read_bytes()) if section in {
                "images", "audio", "listeningTaskAudio", "listeningTaskImages"} else manifest_sha256(path)
            assert actual == digest, name
            count += 1
    assert count == 8463
    before = load(L / "progress-before-797.json")
    now = load(C / "progress.json")
    mutable = {"stage", "nextAction", "blocker"}
    assert all(now[k] == v for k, v in before.items() if k not in mutable)
    result = {
        "schemaVersion": 1, "execution": 797, "batch": "104", "sourceBase": BASE,
        "frozenInputHashesVerified": len(inputs), "decompressedDictionaryHashesVerified": 2,
        "completeMemberFamilies": 4, "completeComparisonFamilies": 23,
        "exactFreshExtractionsMatch": True, "compactFullFamilySemanticEquality": True,
        "completeRawCharacterRecords": 15, "rawCharacterSemanticEquality": True,
        "sourceRow": 115, "kanji": "劾", "metadataReadingEntries": 1,
        "selectedReadingEntries": 1, "newNecessarySupportWords": 1,
        "existingArticleSnapshotsVerified": 31, "navigationOnlyReusedChanges": 0,
        "directKanjiGuards": 5, "directWordGuards": 7, "curatedWrongChoices": 3,
        "allMappedPairs": 1, "requiredDirections": 2, "activatedBaselinePairs": 0,
        "actualPublicPagesRetained": 4, "newPublicCharacterEntriesInspected": 1,
        "proposedHan": fonts["auditedHanCount"], "bundledFonts": 3,
        "missingFromAllBundledCmaps": [c for c in fonts["auditedHan"]
                                      if all(not f["keyGlyphPresence"][c] for f in fonts["fonts"])],
        "missingCmapIsRenderingFailure": False, "defaultSystemFont": "Later native rendering required",
        "rareHanCharacters": 0, "geometryConverted": False, "pinnedSvgPaths": 8,
        "runtimeBytesUnchanged": True, "runtimeManifestHashesVerified": count,
        "manifestBytesUnchanged": True, "contentVersion": manifest["contentVersion"],
        "originalHistoricalRootValuesPreserved": True, "sourcePreparationComplete": True,
        "limits": "Source-stage author inspection/mechanical audit, not independent linguistic review or fresh Android/native/font/phone acceptance. Direct safeguards do not certify every unsampled quiz pool."
    }
    save(S / "batch-104-source-completion-audit.json", result)
    print(json.dumps(result, ensure_ascii=True, indent=2))


def record():
    result = load(S / "batch-104-source-completion-audit.json")
    assert result["sourcePreparationComplete"] and result["runtimeManifestHashesVerified"] == 8463
    checks = {}
    for name in ["source-tests", "validate", "manifest", "manifest-diff", "budget",
                 "vocabulary", "audit", "whitespace"]:
        raw = (L / f"{name}-797.txt").read_bytes()
        path = S / f"batch-104-{name}-797.txt.gz"
        path.write_bytes(gzip.compress(raw, mtime=0))
        assert gzip.decompress(path.read_bytes()) == raw
        checks[name] = {"archive": path.name, "rawBytes": len(raw), "rawSha256": sha(raw),
                        "archiveSha256": sha(path.read_bytes())}
    tests = (L / "source-tests-797.txt").read_text(encoding="utf-8")
    assert "Ran 43 tests" in tests and tests.rstrip().endswith("OK")
    assert (L / "validate-797.txt").read_text(encoding="utf-8").rstrip().endswith("0 error(s)")
    helpers = {}
    for source, target in [
        ("source-797.py", "batch-104-source-completion-recipe.py"),
        ("preflight-797.ps1", "batch-104-preflight-797.ps1.txt"),
        ("checks-source-797.ps1", "batch-104-checks-source-797.ps1.txt"),
        ("issue-797.ps1", "batch-104-issue-797.ps1.txt")
    ]:
        shutil.copyfile(C / source, S / target)
        helpers[target] = sha((S / target).read_bytes())
    role = load(L / "preflight-797.json")
    shutil.copyfile(L / "preflight-797.json", S / "batch-104-runner-role-797.json")
    save(S / "execution-797.json", {
        "schemaVersion": 1, "execution": 797, "checkpoint": 797, "batch": "104",
        "stage": "batch-104-source-prepared-not-drafted", "baseCommit": BASE,
        "androidSignedHead": APP, "membership": ["劾"], "sourceRows": [115],
        "sourceCompletionAudit": result, "authoringPlan": "batch-104-authoring-plan.json",
        "validation": checks, "durableHelperHashes": helpers, "runnerPreflight": role,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "sourcePreparationComplete": True,
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "publishedAdditions": 130, "remainingAdditions": 1098, "lastPublishedCommit": MAIN,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "actualNewPermissionDenials": [],
        "nextAction": load(S / "batch-104-authoring-plan.json")["nextAction"],
        "limits": "Normally signed LOCAL source-only checkpoint; no push, runtime draft, independent review, app/native or publication acceptance. All historical limitations and original gates remain unchanged. Vocabulary check retains its incomplete pilot coverage."
    })
    print("Source-completion audit, validation receipts and durable helpers archived.")


def issue():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    clean(R, head)
    clean(A, APP)
    result = load(S / "batch-104-source-completion-audit.json")
    body = (
        "Batch 104 / checkpoint 797: **LOCAL source-completion checkpoint**, not published teaching.\n\n"
        f"Normally signed saved commit `{head}`; public main remains `{MAIN}`.\n\n"
        "Completed the authoring plan for frozen row115 **劾**: four complete member families "
        "and 23 complete comparison families author-inspected, 15 complete raw character records "
        "retained, 31 actual existing articles/labels checked. Full/selected readings remain "
        "**[ガイ]/[]**, key がい. One necessary NEW **弾劾 だんがい** article is planned, "
        "with no inferred vocabulary level. The actual Digital Daijisen 弾 character heading "
        "independently supplies ダン and its explicit 弾劾 sense; this is not allocation from "
        "a kana substring. Existing 弾 たま bullet stays unchanged and is not compound support.\n\n"
        "The plan separates formal impeachment from broader denunciation/exposing wrongdoing "
        "and demanding accountability; it does not imply proven guilt or completed removal. "
        "The attested government-misrule example is not mislabeled as formal impeachment. "
        "No historical/phonetic formation claim is adopted. Three wrong kanji choices "
        "(刻・効・努), five direct kanji safeguards and seven direct word safeguards have "
        "bounded evidence-based authoring dispositions, including secondary censure senses. "
        "These remain subject to both independent reviews and actual compatible-builder/native "
        "checks; exclusions are symmetric and nontransitive, not synonym cliques.\n\n"
        "One all-mapped reciprocal pair/two directions, zero activated baseline pairs and "
        "**zero baseline runtime edits** planned. 弾 stays in word metadata without an absent "
        "kanji-card link. The existing incidental 亥/力/comparison cards do not require new "
        "backlinks. Exact baseline hash inventory and complete comparison bodies are retained.\n\n"
        f"Proposed {result['proposedHan']} Han checked against all three bundled font cmaps; "
        f"all-three absences: {json.dumps(result['missingFromAllBundledCmaps'], ensure_ascii=False)}. "
        "No proposed rare-Han-range characters. Cmap presence is not rendered acceptance: "
        "final actual-Han audit, fourth/default system typography, non-skipped Android and "
        "fresh native/rendered acceptance remain pending. Pinned eight-path SVG and unchanged "
        "converter identity verified; geometry is not yet generated.\n\n"
        "43 focused source tests, structural validation, unchanged regenerated manifest, "
        "vocabulary consistency (existing incomplete pilot coverage), budgets and source/"
        "metadata/link-preservation audit passed. All **8,463 runtime hashes** and "
        "contentVersion `38c32a8df5fd6063` unchanged. Complete live history preserved. "
        "Live parent launcher ancestry/decoded command/exact session verified; its lock was "
        "not touched. Approved workspace/control inputs only; no historical-session helper "
        "access or new permission denial. New public entry's initial multi-block output "
        "was truncated; only the exact relevant character block and publisher context were "
        "used, not claimed as a complete reading of all later site material.\n\n"
        "**130/1,228 additions published; 1,098 acceptance remainder unchanged.** No runtime "
        "draft, reviewer, Android/native run, push or next batch in this execution. Next is "
        "SAME104 bounded LOCAL UNREVIEWED draft/freeze, followed by every original serial "
        "two-family, qualified Android/native, combined-main, signing and publication gate. "
        "Compatible stop-cran/kanji-cards-android#125 and "
        "stop-cran/kanji-cards-android#132 mechanisms remain required. Physical-phone, "
        "general-release and whole-set acceptance remain outstanding. Prior batch103 "
        "image/read-depth/process limits and all historical limitations remain preserved, "
        "not retroaccepted.\n"
    )
    (C / "issue-797.txt").write_text(body, encoding="utf-8", newline="\n")
    save(C / "issue-request-797.json", {"body": body})
    print("Exact owner issue body generated.")


def finish():
    head = git("rev-parse", "HEAD")
    assert head != BASE and git("rev-parse", "HEAD^") == BASE
    clean(R, head)
    clean(A, APP)
    assert git("rev-parse", "origin/main") == MAIN
    changes = git("diff", "--name-only", BASE, head).splitlines()
    assert changes and all(n.startswith("docs/n1-sources/batch-104-") or
                           n == "docs/n1-sources/execution-797.json" for n in changes)
    assert not git("diff", BASE, head, "--", "kanji", "words", "articles", "strokes", "manifest.json", "tools")
    for name, digest in load(S / "execution-797.json")["durableHelperHashes"].items():
        assert sha((S / name).read_bytes()) == digest, name
    before = load(L / "progress-before-797.json")
    p = load(C / "progress.json")
    mutable = {"checkpoint", "status", "stage", "nextAction", "blocker"}
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    posted = load(L / "issue-797-verified.json")
    body = (C / "issue-797.txt").read_text(encoding="utf-8")
    assert posted["user"]["login"] == "stop-cran" and posted["body"] == body and head in body
    result = load(S / "batch-104-source-completion-audit.json")
    plan = load(S / "batch-104-authoring-plan.json")
    marker = "Every original TWOserialblind "
    assert marker in before["nextAction"]
    next_action = plan["nextAction"] + " " + marker + before["nextAction"].split(marker, 1)[1]
    receipt = {
        "schemaVersion": 1, "execution": 797, "checkpoint": 797, "batch": "104",
        "savedCommit": head, "signature": "G", "sourceBase": BASE, "androidSignedHead": APP,
        "evidence": "docs/n1-sources/execution-797.json", "membership": ["劾"], "sourceRows": [115],
        "completeMemberFamilies": 4, "completeComparisonFamilies": 23,
        "metadataReadingEntries": 1, "newNecessarySupportWords": 1,
        "sourcePreparationComplete": True, "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "runtimeChanged": False, "runtimePublished": False, "independentReviewersLaunched": 0,
        "freshAndroidOrNativeClaimed": False, "publishedAdditions": 130, "remainingAdditions": 1098,
        "lastPublishedCommit": MAIN, "dedicatedWorktreesClean": True,
        "originalHistoricalRootValuesPreservedExactly": True, "originalRootKeysCompared": len(before),
        "ownerIssueAuthorAndExactBodyVerified": True, "issueUpdate": posted["html_url"],
        "parentLockTouched": False, "optionalHistoricalSessionHelpersAccessed": False,
        "actualNewPermissionDenials": [], "status": "continue",
        "stage": "batch-104-source-prepared-not-drafted",
        "runtimeManifestHashesVerified": 8463, "contentVersion": "38c32a8df5fd6063",
        "sourceTestsPassed": 43, "sourceCompletionAudit": result,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeProjectComplete": False, "nextAction": next_action, "blocker": None
    }
    p["execution797StartingState"]["status"] = "signed-local-source-completion-checkpoint-complete"
    p["execution797CoordinatorCheckpoint"] = receipt
    p["batch104SourceCompletionIssueReceipt"] = {
        "id": posted["id"], "url": posted["html_url"], "author": posted["user"]["login"],
        "bodySha256": sha(body.encode("utf-8")), "verified": True
    }
    p.update(checkpoint=797, status="continue", stage=receipt["stage"], nextAction=next_action, blocker=None)
    assert all(p[k] == v for k, v in before.items() if k not in mutable)
    save(C / "progress.json", p)
    reread = load(C / "progress.json")
    assert reread == p and all(reread[k] == v for k, v in before.items() if k not in mutable)
    save(L / "checkpoint-797-final-verification.json", receipt)
    print(json.dumps({"checkpoint": 797, "status": "continue", "savedCommit": head,
                      "signature": "G", "sourcePreparationComplete": True,
                      "historicalRootKeysPreserved": len(before),
                      "issueUpdate": posted["html_url"], "runtimeChanged": False}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("step", choices=["start", "navigation", "discovery", "packet", "public",
                                       "prepared", "audit", "record", "issue", "finish"])
    globals()[parser.parse_args().step]()
