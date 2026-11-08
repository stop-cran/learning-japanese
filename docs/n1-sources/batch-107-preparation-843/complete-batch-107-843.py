"""Source-only batch 107 completion; never acquires the launcher lock."""
import argparse
import copy
import gzip
import hashlib
import io
import json
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "rollout-recovered" / "learning-japanese"
A = C.parent / "rollout-recovered" / "kanji-cards-android"
S = R / "docs" / "n1-sources"
L = C / "logs" / "705603bf-c82b-4428-89cc-12d3b66a42db"
BASE = "476f429108415d00f9d41863af9d2f9470b5bbc0"
START = "25e3bac1ae63ac017e9810b5ea2a2d43e2d573c4"
APP = "bf30cdead8515739bc0e671d57a54b9a3109dd46"
PREFIX = "batch-107-"
sys.path.insert(0, str(R / "tools"))
from audit_n1_pilot import metadata
from build_manifest import build_manifest
from audit_n1_batch import teachable_lexical_pair
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
    temporary = path.with_name(path.name + ".843.tmp")
    if temporary.exists():
        raise FileExistsError(temporary)
    temporary.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    assert load(temporary) == value
    temporary.replace(path)


def new(path, raw):
    with path.open("xb") as stream:
        stream.write(raw)


def current():
    runner = load(C / "runner.json")
    assert runner["status"] == "running" and runner["pid"] == 31724 and runner["sessionId"] == L.name
    p = load(C / "progress.json")
    assert p["checkpoint"] == 842 and p["status"] == "continue" and p["batch"] == "107"
    assert p["remainingAdditions"] == 1095 and p["lastPublishedCommit"] == BASE
    assert p["execution792HistoryCorrection"]["ownerReportCorrection"].startswith("https://github.com/")
    assert git("rev-parse", "HEAD", root=A) == APP
    assert git("log", "-1", "--format=%G?", root=A) == "G"
    assert not git("status", "--porcelain", "--untracked-files=all", root=A)
    return p


def start():
    p = current()
    assert git("rev-parse", "HEAD") == START and git("log", "-1", "--format=%G?") == "G"
    assert not git("status", "--porcelain", "--untracked-files=all")
    assert load(L / "checkpoint-full.json") == p
    raw = (L / "request.txt").read_bytes()
    text = raw.decode("utf-8-sig")
    marker = "Current execution checkpoint (complete historical state remains at checkpointHistory paths):"
    projection = json.loads(text.split(marker, 1)[1])
    assert projection["checkpoint"] == 842 and projection["execution842CoordinatorCheckpoint"]["savedCommit"] == START
    before = L / "progress-before-843.json"
    assert not before.exists()
    shutil.copyfile(C / "progress.json", before)
    state = {
        "execution": 843, "batch": "107", "startedAt": datetime.now(timezone.utc).isoformat(),
        "startingHead": START, "baseCommit": BASE, "androidHead": APP,
        "scope": "Bounded source completion only; no runtime draft/review/Android/native/publication/batch108.",
        "request": {"sha256": sha(raw), "bytes": len(raw), "lines": len(text.splitlines()),
                    "completeFileLoadedAndCheckpointParsed": True,
                    "limits": "Full request decoded; operative contract and complete final projected checkpoint inspected. Historical records not freshly linguistically reviewed."},
        "runnerPreflight": load(L / "preflight-843.json"),
        "fullHistoryBefore": str(before), "fullHistoryBeforeSha256": sha(before.read_bytes()),
        "artifactPathPreflight": "Committed evidence and approved frozen inputs; reusable helpers in control. No optional historical session recipes.",
        "parentLockTouched": False, "actualNewPermissionDenials": [],
    }
    p["execution843StartingState"] = state
    p.update(stage="batch-107-source-completion-in-progress", nextAction=state["scope"])
    save(C / "progress.json", p)
    print("Source-completion starting scope persisted with full live history.")


def xml_bytes(root):
    ET.indent(root, space="  ")
    return ET.tostring(root, encoding="utf-8", xml_declaration=True) + b"\n"


COMPARISON_CHARACTERS = "勤助期感思考判査比算胸識知覚察"
COMPARISON_WORDS = [
    "勤める", "勤勉", "助", "助ける", "期", "期間", "時期",
    "感", "感じる", "感覚", "直感", "思う", "考える", "判断", "判",
    "検査", "調査", "比較", "比べる", "計算", "算", "胸", "認識",
    "知る", "覚える", "察する", "予想", "会計", "支払う", "誤解", "間違い",
    "誤り", "ミス", "失敗", "定規", "違い", "違う",
]


def extract():
    current()
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
    root = ET.Element("JMdict")
    matches = {word: [] for word in COMPARISON_WORDS}
    for _, entry in ET.iterparse(io.BytesIO(jm), events=("end",)):
        if entry.tag != "entry":
            continue
        forms = {e.text for e in entry.findall("k_ele/keb")} | {e.text for e in entry.findall("r_ele/reb")}
        applicable = forms.intersection(matches)
        if applicable:
            root.append(copy.deepcopy(entry))
            for word in applicable:
                matches[word].append(entry.findtext("ent_seq"))
        entry.clear()
    assert all(matches.values()), [word for word, ids in matches.items() if not ids]
    new(S / (PREFIX + "comparison-jmdict.xml"), xml_bytes(root))
    kd_root = ET.fromstring(kd)
    retained = ET.Element("kanjidic2")
    retained.append(copy.deepcopy(kd_root.find("header")))
    chars = "定違" + COMPARISON_CHARACTERS
    for character in kd_root.findall("character"):
        if character.findtext("literal") in chars:
            retained.append(copy.deepcopy(character))
    assert len(retained) == len(set(chars)) + 1
    new(S / (PREFIX + "comparison-kanjidic2.xml"), xml_bytes(retained))
    articles = []
    for folder, names in (("kanji", chars), ("words", COMPARISON_WORDS)):
        for name in names:
            path = R / folder / (name + ".md")
            if path.exists():
                articles.append({"article": path.relative_to(R).as_posix(), "sha256": sha(path.read_bytes()),
                                 "metadata": metadata(R, path.relative_to(R).as_posix()),
                                 "text": path.read_text(encoding="utf-8")})
    save(S / (PREFIX + "comparison-article-snapshots.json"), articles)
    record = {
        "schemaVersion": 1, "batch": "107", "baseCommit": BASE,
        "selectionRule": "Complete pinned JMdict families with an exact keb or reb in comparisonForms, source order; all aliases/restrictions/senses retained.",
        "comparisonForms": COMPARISON_WORDS, "matches": matches,
        "entryIds": [e.findtext("ent_seq") for e in root],
        "dictionaryPacket": PREFIX + "comparison-jmdict.xml",
        "dictionaryPacketSha256": sha((S / (PREFIX + "comparison-jmdict.xml")).read_bytes()),
        "componentCharacters": list(chars),
        "rawCharacterPacket": PREFIX + "comparison-kanjidic2.xml",
        "rawCharacterPacketSha256": sha((S / (PREFIX + "comparison-kanjidic2.xml")).read_bytes()),
        "snapshot": "docs/n1-source-snapshot.json",
        "extractionDiagnostics": ["Initial exact-form scan required a standalone 勤 lexical family; the pinned JMdict contains none. It failed before packet writes. 勤 remains in the complete raw-character comparison, with actual 勤める/勤勉 lexical families; no invented standalone noun or silent empty match."],
        "verifiedInputHashes": {name: record["sha256"] for name, record in snapshot["inputs"].items()},
        "limits": "Extraction only; no claim of source inspection, quiz safety, independent review or acceptance.",
    }
    save(S / (PREFIX + "comparison-selection.json"), record)
    print(json.dumps({"comparisonFamilies": len(root), "rawCharacters": len(retained) - 1,
                      "articleSnapshots": len(articles)}, ensure_ascii=True))


def canonical(element):
    return (element.tag, sorted(element.attrib.items()), (element.text or "").strip(),
            [canonical(child) for child in element])


def check():
    current()
    plan = load(S / (PREFIX + "source-completion-plan.json"))
    assert plan["baseCommit"] == BASE and plan["membership"] == ["勘"] and plan["sourceRows"] == [118]
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
    selected = {}
    packet_counts = []
    selections = []
    for selection_name, packet_name in (
        ("lexical-selection.json", "jmdict.xml"),
        ("comparison-selection.json", "comparison-jmdict.xml"),
    ):
        selection = load(S / (PREFIX + selection_name))
        entries = ET.parse(S / (PREFIX + packet_name)).getroot().findall("entry")
        ids = [entry.findtext("ent_seq") for entry in entries]
        assert ids == selection["entryIds"] and len(set(ids)) == len(ids)
        packet_counts.append(len(ids))
        selections.append(ids)
        for entry in entries:
            entry_id = entry.findtext("ent_seq")
            if entry_id in selected:
                assert canonical(selected[entry_id]) == canonical(entry)
            selected[entry_id] = entry
    comparison = load(S / (PREFIX + "comparison-selection.json"))
    assert COMPARISON_WORDS == comparison["comparisonForms"]
    reproduced = [[], []]
    matches = {word: [] for word in COMPARISON_WORDS}
    for _, entry in ET.iterparse(io.BytesIO(jm), events=("end",)):
        if entry.tag != "entry":
            continue
        entry_id = entry.findtext("ent_seq")
        forms = {e.text for e in entry.findall("k_ele/keb")} | {e.text for e in entry.findall("r_ele/reb")}
        if any("勘" in (e.text or "") for e in entry.findall("k_ele/keb")):
            reproduced[0].append(entry_id)
        applicable = forms.intersection(matches)
        if applicable:
            reproduced[1].append(entry_id)
            for word in applicable:
                matches[word].append(entry_id)
        if entry_id in selected:
            assert canonical(entry) == canonical(selected[entry_id]), entry_id
        entry.clear()
    assert reproduced == selections and matches == comparison["matches"]
    assert packet_counts == plan["sourceEvidence"]["completeFamilyCounts"] == [92, 43]
    assert len(selected) == plan["sourceEvidence"]["distinctCompleteFamilies"] == 134
    raw_characters = {}
    for name in plan["sourceEvidence"]["rawCharacterPackets"]:
        packet = ET.parse(S / name).getroot()
        for entry in packet.findall("character"):
            character = entry.findtext("literal")
            assert character not in raw_characters
            raw_characters[character] = entry
    kd_root = ET.fromstring(kd)
    for entry in kd_root.findall("character"):
        character = entry.findtext("literal")
        if character in raw_characters:
            assert canonical(entry) == canonical(raw_characters[character]), character
    assert len(raw_characters) == plan["sourceEvidence"]["completeRawCharacterRecords"] == 18
    radicals = {}
    for line in inputs["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines():
        fields = line.split(";")
        codepoint = int(fields[0], 16)
        if 0x2F00 <= codepoint <= 0x2FD5:
            radicals[codepoint - 0x2F00 + 1] = chr(int(fields[5].split()[-1], 16))
    assert len(radicals) == 214
    row = load(S / (PREFIX + "input-metadata.json"))["sourceIndexRecord"]
    index = load(S / "source-index.json")
    source = json.loads(inputs["n1-kanji-source-20261102.json"])
    assert source[117] == "勘" and row["sourceRow"] == 118
    assert next(item for item in index if item["kanji"] == "勘") == row
    assert metadata_record(raw_characters["勘"], radicals) == row["metadata"]
    for suffix in ("membership.json", "progress.json"):
        member = load(S / (PREFIX + suffix))
        assert member["membership"] == ["勘"] and member["sourceRows"] == [118]
        assert member["sourceReadingOrder"] == {"onyomi": ["カン"], "kunyomi": []}
    baseline = load(S / (PREFIX + "baseline-plan.json"))
    manifest = load(R / "manifest.json")
    assert manifest == baseline["runtimeManifest"] == build_manifest(R)
    committed_manifest = subprocess.check_output(["git", "-C", str(R), "show", BASE + ":manifest.json"])
    assert (R / "manifest.json").read_bytes() == committed_manifest
    assert sha(committed_manifest.replace(b"\n", b"\r\n")) == baseline["manifestRawSha256"]
    for name, item in baseline["inventory"].items():
        assert metadata(R, name) == item["metadata"] and sha((R / name).read_bytes()) == item["sha256"], name
    snapshot_count = 0
    for suffix in ("existing-article-snapshots.json", "comparison-article-snapshots.json"):
        for item in load(S / (PREFIX + suffix)):
            assert sha((R / item["article"]).read_bytes()) == item["sha256"]
            assert (R / item["article"]).read_text(encoding="utf-8") == item["text"]
            snapshot_count += 1
    assert {p.relative_to(R).as_posix() for folder in ("kanji", "words") for p in (R / folder).glob("*.md")} == set(baseline["inventory"])
    assert not (R / "kanji" / "勘.md").exists() and not (R / "strokes" / "勘.json").exists()
    for word in plan["supportPlan"]["reused"]:
        meta = metadata(R, word["article"])
        assert all(meta[key] == word[key] for key in ("word", "reading", "title", "jlpt", "type"))
        assert meta.get("quiz_exclusions", []) == word["originalExclusions"]
        assert all(teachable_lexical_pair(selected[word["entryId"]], word["word"], word["reading"], sense)
                   for sense in word["selectedSenses"])
    assert plan["supportPlan"]["newNecessary"] == []
    pairs = {(c, word["article"]) for word in plan["supportPlan"]["reused"]
             for c in metadata(R, word["article"])["kanji"]}
    assert pairs == {tuple(pair) for pair in plan["linkPlan"]["allMappedPairs"]} and len(pairs) == 5
    navigation = load(S / (PREFIX + "source-navigation.json"))
    activated = {(pair["kanji"], pair["article"]) for pair in navigation["baselinePairs"]}
    assert activated == {tuple(pair) for pair in plan["linkPlan"]["activatedBaselinePairs"]} and len(activated) == 3
    expected_directions = {(f"kanji/{c}.md", word) for c, word in pairs}
    expected_directions |= {(word, f"kanji/{c}.md") for c, word in pairs}
    directions = plan["linkPlan"]["requiredDirections"]
    assert {(row["from"], row["to"]) for row in directions} == expected_directions and len(directions) == 10
    present = 0
    for row in directions:
        assert row["relative"] == "../" + row["to"]
        path = R / row["from"]
        found = path.exists() and f"({row['relative']})" in path.read_text(encoding="utf-8")
        assert found == row["currentlyPresent"]
        present += bool(found)
    assert present == 2
    previews = []
    for edit in plan["linkPlan"]["exactReusedChanges"]:
        path = R / edit["article"]
        text = path.read_text(encoding="utf-8")
        assert text.count(edit["before"]) == 1 and edit["after"] != edit["before"], edit["article"]
        preview = text.replace(edit["before"], edit["after"], 1)
        assert text.split("---", 2)[1] == preview.split("---", 2)[1]
        previews.append({"article": edit["article"], "baselineByteSha256": sha(path.read_bytes()),
                         "plannedText": preview, "plannedLfSha256": sha(preview.encode("utf-8")),
                         "classification": edit["classification"]})
    save(S / (PREFIX + "reused-passage-previews.json"), previews)
    for origin, target in expected_directions:
        if origin == "kanji/勘.md":
            continue
        preview = next(row["plannedText"] for row in previews if row["article"] == origin)
        assert f"(../{target})" in preview, (origin, target)
    kanji_plan = plan["kanjiPlan"]
    assert not any(item["metadata"]["title"] == kanji_plan["title"]
                   for name, item in baseline["inventory"].items() if name.startswith("kanji/"))
    character = raw_characters["勘"]
    for kind, field in (("ja_on", "onyomi"), ("ja_kun", "kunyomi")):
        assert [e.text for e in character.findall("reading_meaning/rmgroup/reading") if e.get("r_type") == kind] == kanji_plan[field]
    assert kanji_plan["onyomi"] == kanji_plan["quizOnyomi"] == ["カン"]
    assert kanji_plan["kunyomi"] == kanji_plan["quizKunyomi"] == []
    assert kanji_plan["offeredKeys"] == kanji_plan["legacyOfferedKeys"] == {"on": ["かん"], "kun": []}
    assert teachable_lexical_pair(selected["1210590"], "勘", "かん", 1)
    assert teachable_lexical_pair(selected["1281020"], "勘える", "かんがえる", 1)
    assert selected["1281020"].findall("k_ele")[1].findtext("ke_inf") == "rarely used kanji form"
    assert "ジョウ" in [e.text for e in raw_characters["定"].findall("reading_meaning/rmgroup/reading")]
    assert "ちが.い" in [e.text for e in raw_characters["違"].findall("reading_meaning/rmgroup/reading")]
    labels = []
    for distractor in kanji_plan["curatedDistractors"]:
        assert metadata(R, f"kanji/{distractor['kanji']}.md")["title"] == distractor["actualTitle"]
        labels.append(distractor["actualTitle"])
    ids = [row["kanji"] for row in kanji_plan["curatedDistractors"]]
    assert len(ids) == len(set(ids)) == len(set(labels)) == 3 and "勘" not in ids
    excluded = kanji_plan["quizExclusions"]
    assert len(excluded) == len(set(excluded)) == 8 and not set(excluded).intersection(ids)
    assert [row["kanji"] for row in kanji_plan["directGuardRationale"]] == excluded
    for row in kanji_plan["directGuardRationale"]:
        assert metadata(R, f"kanji/{row['kanji']}.md")["title"] == row["actualTitle"]
    for origin, target in plan["supportPlan"]["wordQuizAudit"]["preservedDirectPairs"]:
        first = metadata(R, f"words/{origin}.md").get("quiz_exclusions", [])
        second = metadata(R, f"words/{target}.md").get("quiz_exclusions", [])
        assert target in first or origin in second
    legacy = [name[len("kanji/"):-3] for name, item in baseline["inventory"].items()
              if name.startswith("kanji/") and len(item["metadata"].get("distractors", [])) < 3]
    assert legacy == plan["legacyFallbackPlan"]["legacyFewerThanThree"]
    incoming = [name for name, item in baseline["inventory"].items()
                if name.startswith("kanji/") and "勘" in item["metadata"].get("distractors", [])]
    assert incoming == plan["legacyFallbackPlan"]["incomingTargetCuratedReferences"] == []
    legacy_snapshots = [{"article": f"kanji/{c}.md", "sha256": sha((R / "kanji" / (c + ".md")).read_bytes()),
                         "text": (R / "kanji" / (c + ".md")).read_text(encoding="utf-8")}
                        for c in legacy]
    save(S / (PREFIX + "legacy-fallback-snapshots.json"), legacy_snapshots)
    stroke = load(S / (PREFIX + "stroke-evidence.json"))
    svg = (S / (PREFIX + "kanjivg.svg")).read_bytes()
    inventory = navigation["sourceIndexRecord"]["kanjivgInventory"]
    assert sha(svg) == stroke["sha256"] and len(svg) == stroke["bytes"] == inventory["size"]
    assert hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest() == stroke["gitBlob"] == inventory["sha"]
    paths = ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")
    assert [e.get("id") for e in paths] == [f"kvg:052d8-s{i}" for i in range(1, 12)]
    assert len(paths) == int(character.findtext("misc/stroke_count")) == stroke["sourceStrokePaths"] == 11
    assert stroke["revision"] == snapshot["kanjivg"]["revision"] == plan["strokePlan"]["sourceRevision"]
    assert sha((R / "tools" / "generate_strokes.py").read_bytes().replace(b"\r\n", b"\n")) == stroke["converterNormalizedSha256"] == plan["strokePlan"]["converterNormalizedSha256"]
    assert stroke["converted"] is False
    for receipt in load(S / (PREFIX + "public-source-receipts.json")):
        raw = gzip.decompress((S / receipt["archive"]).read_bytes())
        assert sha(raw) == receipt["rawSha256"] and len(raw) == receipt["rawBytes"]
        assert sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"]
    from fontTools.ttLib import TTFont
    import re
    proposed = plan["fontPlan"]["proposedTextInventory"] + "\n" + "\n".join(row["plannedText"] for row in previews)
    han = sorted(set(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", proposed)))
    fonts = []
    for name, expected_hash in (
        ("kanji_brush", "8da5c86e251f6efa0f81fc32bd6e67a5d81d21da26cd6c2b3fa4bb92a7692954"),
        ("kanji_mincho", "168007ae94a45262cdcbe6ca940b70d3aba27a3399362a68f723e1445ac9596d"),
        ("kanji_textbook", "c37ea201be60dc5707693a14f93c1999f815cc6c54c0e63930606d0c598a50ab"),
    ):
        path = A / "app" / "src" / "main" / "res" / "font" / (name + ".ttf")
        assert sha(path.read_bytes()) == expected_hash
        with TTFont(path) as font:
            cmap = font.getBestCmap()
            presence = {c: ord(c) in cmap and cmap[ord(c)] != ".notdef" for c in han}
        fonts.append({"path": str(path), "sha256": sha(path.read_bytes()), "keyGlyphPresence": presence,
                      "allProposedMissing": [c for c, found in presence.items() if not found]})
        assert all(presence[c] for c in set(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", plan["fontPlan"]["proposedTextInventory"])))
    font_record = {
        "schemaVersion": 1, "batch": "107", "execution": 843,
        "proposedTextInventory": proposed, "auditedHan": han, "auditedHanCount": len(han),
        "fonts": fonts, "defaultSystemFont": "Fourth later native rendering mode; not a fourth bundled file.",
        "nativeAndFourModeRenderedAcceptance": False,
        "missingCmapDisposition": "All proposed member/support/shape/choice/guard inventory characters are present. The complete reused bodies additionally contain four unmapped radicals/components 宀/辵/辶/韋 in each bundled cmap. These are baseline fallbacks, not proved glyph failures; inspect each under all four actual native modes later. No app/font file is changed.",
        "limits": "Three cmaps of proposed inventory plus all five complete planned reused article bodies, not final runtime rendering. Cmap presence is not readability or fallback-face identity; actual runtimeHan/four-mode native visual gates remain pending.",
    }
    save(S / (PREFIX + "font-preparation.json"), font_record)
    record = {
        "schemaVersion": 1, "execution": 843, "batch": "107", "baseCommit": BASE,
        "allFiveFrozenInputHashesVerified": True, "bothDecompressedDictionaryHashesVerified": True,
        "memberFamilies": 92, "comparisonFamilies": 43, "completeDictionaryFamilies": 134,
        "completeRawCharacterRecordsReproduced": 18, "baselineArticlesUnchanged": len(baseline["inventory"]),
        "allRowMetadataAndUnicodeRadicalReproduced": True,
        "candidateSnapshotRecordsByteAndTextVerified": snapshot_count,
        "allThreeReusedLexicalIdentitiesAndSelectedSenseRestrictionsVerified": True,
        "fullReadingDispositions": 1, "curatedOfferedKeys": 1, "frozenKunyomi": [],
        "supplementaryRareSpellingNotOffered": True,
        "allMappedPairs": 5, "requiredDirections": 10, "currentlyPresentDirections": 2,
        "plannedMissingDirectionsVerified": 8, "activatedBaselinePairs": 3, "exactReusedEdits": 5,
        "curatedWrongIds": ids, "curatedWrongLabels": labels, "plannedDirectKanjiGuards": excluded,
        "preservedDirectWordPairs": 7, "legacyTwoChoiceTargets": len(legacy),
        "sourceStrokePaths": 11, "geometryConverted": False,
        "proposedHan": len(han), "bundledFontsChecked": 3, "fourModeNativeRendering": "pending",
        "manifestFreshAndRawEqualPublishedGitBlob": True, "runtimeChanged": False,
        "sourcePreparationComplete": True,
        "runtimeAuditSchemaLimit": plan["runtimeAuditDisposition"],
        "limits": "Exact-current source checks only; not linguistic review, runtime draft audit, actual production quiz execution, native/phone acceptance or publication. All source-plan choices remain subject to independent review.",
    }
    save(S / (PREFIX + "source-completion-audit.json"), record)
    print(json.dumps(record, ensure_ascii=True))


NEXT = (
    "SAME107 source-ready LOCAL UNREVIEWED runtime draft next, not108 or publication. "
    "Read signed execution-843.json, batch-107-source-completion-plan.json, exact complete "
    "member/comparison packets and actual affected cards. Row118 勘; add onlykanji/勘.md "
    "and unchangedpinnedconverter strokes/勘.json, preserve fullon[カン]/fullkun[] and "
    "quiz[カン]/[], titleintuition;hunch, radical力19/11strokes/grade8/"
    "structure-unclassified/modern-shape-only/no unverifiedphonetic. Rare spelling "
    "勘えるかんがえる is supplementary recognition linked to usual考える, NOT rare "
    "pronunciation/invalid native/no-dictionary-native or frozenmetadataextension. "
    "Reuse 勘かんN3,勘定かんじょうN3,勘違いかんちがいN2 with exact identities/"
    "earlierlevels/readings/originalguards; no new word. Implement exact5reusededits "
    "(3componentlinks plus sourcedCommonwords on定/違), all5mappedpairs10directions/"
    "3activatedbaselinepairs; review the two new bullets as teaching, not navigation. "
    "Curatedwrong勤/助/期; sourceplanned directguards感/思/考/判/査/比/算/察, not "
    "transitive or semantic compartments. Do not assert an all-pool guarantee; "
    "11legacyfallbacks, actuallyfilteredN1/All/custom/reduced productionoptions/"
    "directions plus unchanged7wordpairs and any actuallydefensibleotherlabel need "
    "qualified actual builder checks. Existinggeneric sourceplan-auditor schema "
    "expects oneNEWword/atmostone reusedkanji, unlike thiscorrect three-reuse/"
    "two-componentexample batch. Establish legitimate equivalent exact-current "
    "runtime baseline/membership/allpairs/readings/guards/pinnedgeometry/manifest "
    "audits before runtime acceptance; never fabricate incompatible ledger, duplicate "
    "support, weakeninvariants or label843sourcechecks a future runtimeaudit. Preserve "
    "actualfailure/report/yield if required invariant unavailable. Recompute FINAL "
    "learnerHan; preparation62Han/threebundledfontcmaps found fourbaselinefallbacks "
    "宀/辵/辶/韋; these are nativeinspectiontargets, NOT glyphfailure/acceptance/"
    "fourthbundledfont. Fouractualmodes defaultsystem/brush/mincho/textbook plus "
    "member/support/radical/lookalikes/ALLHan rendered/native still pending. "
    "After validator/manifest and exact-currentchecks, normal signed whollyclean "
    "LOCAL UNREVIEWED freeze, then TWO SERIAL blind isolated HEADLESS CLI "
    "DIFFERENTactualmodel-family reviews on same frozencomplete content (allnew/"
    "reusedteaching and affectedfullcards), serialinternaltools/noshell/edit/delegation/"
    "noauthoragents/no broadreviewerapprovals; actualmodels/process-exit/readranges/"
    "completeoriginalreports/evidenceadjudication/originalsession confirmations "
    "retained. Qualified signed clean bf30cde Android/no-skipsHOST and native "
    "ContentSyncONCE/meaning/curatedreading/drawing/articles/Back/offline/fonts/"
    "rendered, fullsource/runtime/Python/vocabulary/manifest/budget checks, latestmain "
    "nonrewritingintegration/changedteachingreview/actualcombinedvalidation/normal "
    "signature/ownerfastforward/exact terminalgreenCI/EVERYimmutableZIPruntimehash/"
    "18000entries42MiBcompressed80MiBinflated56MiBretained/perfile-media-safepath/"
    "verifiedownerissue remain mandatory before counting107 or starting108. "
    "Published133/1228,remaining1095 unchanged. Preserve full live history,792 "
    "correction/report,106publication/acceptance and original manifestCRLFbaseline/"
    "failure plus publishedGitLFrepresentation proof, allreports/denials/OOMs/"
    "viewport/finitepool/phone limits and nonblocking勅/訓/いまし.める dispositions. "
    "Recovered sibling worktrees/approvedcontrol/committedsources/frozeninputs only; "
    "optional historical session recipes not dependencies. Authenticate actual "
    "-File launcher/session/liveancestry/checkpoint/signedheads/cleanaccountedstate/"
    "freshmain. Parentownsrunner.lock; NOchildacquire/delete/unlock/readprobe. "
    "Preserve/report/yield actualnewdenial/signinghang/uncertainownership; no "
    "signingretry/bypass/newquizalgorithm/concurrentheavywork/secondrunner. "
    "CompatibleAndroid125/132 required. Physicalphone/generalrelease/whole-set "
    "outstanding; necessarysupports NOT N1vocabulary; wholeprojectincomplete."
)


def seal():
    current()
    import re
    tests = (L / "source-tests-843.txt").read_text(encoding="utf-8-sig")
    count = int(re.search(r"Ran (\d+) tests", tests)[1])
    assert count == 97 and tests.rstrip().endswith("OK")
    assert "Verified 92 complete" in (L / "extract-843.txt").read_text(encoding="utf-8-sig")
    assert "0 error(s)" in (L / "validate-843.txt").read_text(encoding="utf-8-sig")
    assert not git("diff", "--", "manifest.json") and not git("diff", "--cached", "--", "manifest.json")
    assert not (L / "whitespace-843.txt").read_text(encoding="utf-8-sig").strip()
    audit = load(S / (PREFIX + "source-completion-audit.json"))
    assert audit["sourcePreparationComplete"] and not audit["runtimeChanged"]
    assert audit["allRowMetadataAndUnicodeRadicalReproduced"]
    assert audit["allMappedPairs"] == 5 and audit["requiredDirections"] == 10
    plan = load(S / (PREFIX + "source-completion-plan.json"))
    for suffix in ("membership.json", "progress.json"):
        record = load(S / (PREFIX + suffix))
        record.update(
            status="source-ready-for-local-unreviewed-draft", sourcePreparationComplete=True,
            sourceCompletionPlan=PREFIX + "source-completion-plan.json",
            sourceCompletionAudit=PREFIX + "source-completion-audit.json",
            limits="Source-bound support/quiz/link/font/stroke preparation complete; no runtime drafted, content reviewed or published. All independent review, exact-current runtime audit, native/four-font and publication gates remain mandatory.",
        )
        save(S / (PREFIX + suffix), record)
    evidence = S / (PREFIX + "preparation-843")
    evidence.mkdir()
    paths = [
        Path(__file__), C / "preflight-843.ps1", C / "checks-batch-107-source-843.ps1",
        C / "post-batch-107-source-843.ps1", C / "batch-107-source-843-issue-template.txt",
        C / "authoring-artifact-path-notes.txt", C / "runner-lock-role-notes.txt",
        C / "progress-reader-lock-notes.txt",
        L / "source-completion-check-843.log",
        L / "preflight-843.json", L / "preflight-843-before-source-check.json", L / "preflight-843-checks.json",
    ] + [L / (name + "-843.txt") for name in
         ("source-tests", "extract", "validate", "manifest", "manifest-diff", "budget", "vocabulary", "audit", "whitespace")]
    artifacts = []
    for path in paths:
        destination = evidence / path.name
        raw = path.read_bytes()
        new(destination, raw)
        artifacts.append({"path": destination.relative_to(R).as_posix(), "sha256": sha(raw)})
    files = {path.relative_to(R).as_posix(): sha(path.read_bytes())
             for path in sorted(S.glob(PREFIX + "*")) if path.is_file()}
    manifest = load(R / "manifest.json")
    record = {
        "schemaVersion": 1, "execution": 843, "batch": "107", "membership": ["勘"],
        "recordedAt": datetime.now(timezone.utc).isoformat(), "baseCommit": BASE,
        "initialSourceCommit": START, "stage": "source-complete-awaiting-normal-local-signature",
        "sourceFiles": files, "archivedArtifacts": artifacts,
        "initialRecordUnmodifiedSha256": sha((S / "execution-842.json").read_bytes()),
        "authorInspection": plan["authorInspection"],
        "validation": {
            "focusedSourceTestsPassed": count, "existingExtractorExactFamilies": 92,
            "validatorErrors": 0, "manifestFreshAndGitUnchanged": True, "sourceAudit": audit,
            "manifestRepresentation": load(S / (PREFIX + "manifest-representation.json")),
            "budget": (L / "budget-843.txt").read_text(encoding="utf-8-sig").strip(),
            "vocabulary": (L / "vocabulary-843.txt").read_text(encoding="utf-8-sig").strip(),
        },
        "runtime": {"contentVersion": manifest["contentVersion"], "schemaVersion": manifest["schemaVersion"],
                    "kanji": 1129, "words": 5080, "manifestGitSha256": sha((R / "manifest.json").read_bytes())},
        "sourcePreparationComplete": True, "runtimeChangedInGit": False,
        "runtimeDrafted": [], "reviewClosed": [], "published": [],
        "independentReviewersLaunched": 0, "freshAndroidOrNativeClaimed": False,
        "projectPublishedAdditions": 133, "remainingAdditions": 1095,
        "physicalPhoneAcceptance": "outstanding", "generalReleaseAcceptance": "outstanding",
        "wholeSetAcceptance": "outstanding", "wholeProjectComplete": False, "parentLockTouched": False,
        "actualNewPermissionDenials": [],
        "diagnostics": plan["diagnostics"] + [
            "One extra request range beyond actual587lines returned nothing; all587includingcompletefinalJSON were subsequently obtained before substantive action.",
            "Mistaken progress-reader-collision-notes.txt name returned missing path; exact progress-reader-lock-notes.txt located and read. No permission denial, helper reroute, live observer/runner edit or lock operation.",
            "Manifest generation retains exact publishedGitLF bytes and object; the original842CRLFbaseline/hashfailure and representation proof remain immutable.",
        ],
        "runtimeAuditSchemaDisposition": plan["runtimeAuditDisposition"],
        "fontFallbackDisposition": load(S / (PREFIX + "font-preparation.json"))["missingCmapDisposition"],
        "nextAction": NEXT,
    }
    save(S / "execution-843.json", record)
    print("Source-only completion evidence sealed; runtime, review and publication unchanged.")


def finish():
    p = current()
    head = git("rev-parse", "HEAD")
    assert git("rev-parse", "HEAD^") == START and head != START
    assert git("log", "-1", "--format=%G?") == "G"
    assert "Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>" in git("log", "-1", "--format=%B")
    assert not git("status", "--porcelain", "--untracked-files=all")
    changed = git("-c", "core.quotepath=false", "diff", "--name-only", START, head).splitlines()
    assert changed and all(name.startswith("docs/n1-sources/batch-107-")
                           or name == "docs/n1-sources/execution-843.json" for name in changed)
    record = load(S / "execution-843.json")
    for name, digest in record["sourceFiles"].items():
        assert sha((R / name).read_bytes()) == digest
    for item in record["archivedArtifacts"]:
        assert sha((R / item["path"]).read_bytes()) == item["sha256"]
    assert record["sourcePreparationComplete"] and not record["runtimeChangedInGit"]
    assert sha((S / "execution-842.json").read_bytes()) == record["initialRecordUnmodifiedSha256"]
    issue = load(L / "issue-receipt-843.json")
    assert issue["author"] == "stop-cran" and issue["verified"] is True and issue["localCommit"] == head
    before = load(L / "progress-before-843.json")
    preserved = set(before) - {"stage", "nextAction", "blocker"}
    assert all(p[key] == before[key] for key in preserved)
    p["execution843CoordinatorCheckpoint"] = {
        "execution": 843, "checkpoint": 843, "batch": "107", "status": "continue",
        "stage": "batch-107-source-complete-signed-awaiting-local-draft",
        "savedCommit": head, "signature": "G", "record": "docs/n1-sources/execution-843.json",
        "recordSha256": sha((S / "execution-843.json").read_bytes()), "sourceCompletionAudit": record["validation"]["sourceAudit"],
        "issueUpdate": issue["url"], "ownerAuthorAndBodyVerified": True,
        "sourcePreparationComplete": True, "runtimeChangedInGit": False,
        "reviewersLaunched": 0, "freshAndroidOrNative": False, "runtimePublished": False,
        "publishedAdditions": 133, "remainingAdditions": 1095, "dedicatedWorktreesClean": True,
        "allOriginalHistoricalRootValuesPreserved": True, "parentLockTouched": False, "nextAction": NEXT,
        "recordedAt": datetime.now(timezone.utc).isoformat(),
    }
    p["execution843StartingState"]["status"] = "signed-local-source-completion-checkpoint-complete"
    p["execution843Inherited842Gates"] = {
        "priorNextAction": before["nextAction"], "priorStage": before["stage"],
        "immutableBefore": str(L / "progress-before-843.json"),
        "immutableBeforeSha256": sha((L / "progress-before-843.json").read_bytes()),
        "latestPublication": copy.deepcopy(before["batch106PublicationCheckpoint"]),
        "allOriginalAcceptanceGatesRemainMandatory": True,
    }
    p.update(checkpoint=843, status="continue", stage="batch-107-source-complete-signed-awaiting-local-draft",
             nextAction=NEXT, blocker=None)
    save(C / "progress.json", p)
    assert load(C / "progress.json") == p
    new(L / "checkpoint-after-843.json", (C / "progress.json").read_bytes())
    assert all(p[key] == before[key] for key in preserved - {"checkpoint"})
    print(json.dumps({"checkpoint": 843, "status": "continue", "signedLocalCommit": head,
                      "issue": issue["url"], "published": 133, "remaining": 1095,
                      "fullHistoryPreserved": True, "runtimeChanged": False}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["start", "extract", "check", "seal", "finish"])
    args = parser.parse_args()
    globals()[args.mode]()
