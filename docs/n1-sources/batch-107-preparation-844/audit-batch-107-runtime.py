"""Exact-current batch107 audit; source/format mechanics, not teaching acceptance."""
import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "rollout-recovered" / "learning-japanese"
S = R / "docs" / "n1-sources"
BASE = "476f429108415d00f9d41863af9d2f9470b5bbc0"
SOURCE = "dfed2c150d7fe921aacdb1d616ff527df1935f3b"
sys.path.insert(0, str(R / "tools"))
from audit_n1_batch import (
    activated_baseline_pairs, reused_changes, runtime_delta, teachable_lexical_pair,
)
from audit_n1_pilot import metadata, offered_keys, quiz_readings
from build_manifest import build_manifest
from freeze_n1_sources import metadata_record, require
from generate_strokes import convert


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def verify_source_bytes(raw, blob, recorded_hash, binary=False):
    require(sha(raw) == recorded_hash, "Retained source raw hash changed")
    require(raw == blob if binary else raw.replace(b"\r\n", b"\n") == blob.replace(b"\r\n", b"\n"),
            "Retained source differs from signed Git representation")


def git_bytes(commit, name):
    return subprocess.check_output(["git", "--no-pager", "-C", str(R), "show", f"{commit}:{name}"])


def canonical(element):
    return (element.tag, sorted(element.attrib.items()), (element.text or "").strip(),
            [canonical(child) for child in element])


def verify_directions(root, directions, pairs):
    expected = {(f"kanji/{c}.md", word) for c, word in pairs}
    expected |= {(word, f"kanji/{c}.md") for c, word in pairs}
    require(len(directions) == len(expected) and
            {(row["from"], row["to"]) for row in directions} == expected,
            "Directions do not enumerate every mapped pair exactly once")
    for row in directions:
        require(row["relative"] == "../" + row["to"], "Wrong relative target")
        require(f"({row['relative']})" in (root / row["from"]).read_text(encoding="utf-8"),
                f"Missing required direction: {row['from']} -> {row['to']}")


def verify_member(meta, plan, raw):
    fields = ("title", "jlpt", "tags", "strokes", "radical", "radicalNumber",
              "onyomi", "kunyomi", "quizOnyomi", "quizKunyomi")
    require(meta["kanji"] == "勘" and all(meta[key] == plan[key] for key in fields),
            "Member metadata differs from recorded plan")
    require("phonetic" not in meta, "Unverified phonetic added")
    for kind, field in (("ja_on", "onyomi"), ("ja_kun", "kunyomi")):
        require([e.text for e in raw.findall("reading_meaning/rmgroup/reading")
                 if e.get("r_type") == kind] == meta[field], "Frozen full readings changed")
    require(meta["distractors"] == [row["kanji"] for row in plan["curatedDistractors"]],
            "Curated distractors changed")
    require(meta["quiz_exclusions"] == plan["quizExclusions"], "Direct guards changed")
    require(not set(meta["distractors"]) & set(meta["quiz_exclusions"]), "Wrong/excluded overlap")
    keys = {kind: offered_keys(quiz_readings(meta, field))
            for kind, field in (("on", "onyomi"), ("kun", "kunyomi"))}
    require(keys == plan["offeredKeys"] == {"on": ["かん"], "kun": []}, "Offered key mismatch")


def verify_geometry(svg, stroke, evidence, row, converter):
    require(sha(svg) == evidence["sha256"], "Pinned SVG hash mismatch")
    require(len(svg) == evidence["bytes"] == row["kanjivgInventory"]["size"], "SVG size mismatch")
    blob = hashlib.sha1(f"blob {len(svg)}\0".encode() + svg).hexdigest()
    require(blob == evidence["gitBlob"] == row["kanjivgInventory"]["sha"], "SVG Git blob mismatch")
    require(sha(converter.replace(b"\r\n", b"\n")) == evidence["converterNormalizedSha256"],
            "Converter changed")
    expected = convert("勘", svg.decode("utf-8"))
    variants = load(R / "tools" / "order_variants.json")
    if "勘" in variants:
        expected["orderVariants"] = variants["勘"]
    require(stroke == expected, "Geometry differs from exact pinned converter output")
    require(stroke["strokeCount"] == row["metadata"]["strokes"] == 11, "Stroke count mismatch")
    require(stroke["sourceRevision"] == evidence["revision"], "Stroke revision mismatch")
    require(all(len(path["points"]) == 16 for path in stroke["strokes"]), "Resampling count changed")
    require([e.get("id") for e in ET.fromstring(svg).findall(".//{http://www.w3.org/2000/svg}path")]
            == [f"kvg:052d8-s{i}" for i in range(1, 12)], "Source stroke order mismatch")


def reproduce_sources(plan):
    snapshot = load(R / "docs" / "n1-source-snapshot.json")
    frozen = {}
    for name, record in snapshot["inputs"].items():
        raw = (C / "inputs" / name).read_bytes()
        require(sha(raw) == record["sha256"] and len(raw) == record["bytes"], f"Frozen input: {name}")
        frozen[name] = raw
    jm = gzip.decompress(frozen["n1-implementation-JMdict_e.gz"])
    kd = gzip.decompress(frozen["n1-planning-kanjidic2.xml.gz"])
    require(sha(jm) == snapshot["jmdict"]["xmlSha256"], "JMdict XML hash mismatch")
    require(sha(kd) == snapshot["kanjidic2"]["xmlSha256"], "KANJIDIC XML hash mismatch")
    packets, selected = [], {}
    for selection, packet in (("lexical-selection", "jmdict"), ("comparison-selection", "comparison-jmdict")):
        record = load(S / f"batch-107-{selection}.json")
        entries = ET.parse(S / f"batch-107-{packet}.xml").getroot().findall("entry")
        ids = [e.findtext("ent_seq") for e in entries]
        require(ids == record["entryIds"] and len(ids) == len(set(ids)), "Packet IDs/order mismatch")
        packets.append(ids)
        for e in entries:
            identity = e.findtext("ent_seq")
            require(identity not in selected or canonical(selected[identity]) == canonical(e),
                    "Conflicting duplicate family")
            selected[identity] = e
    comparison = load(S / "batch-107-comparison-selection.json")
    matches = {word: [] for word in comparison["comparisonForms"]}
    reproduced = [[], []]
    for _, entry in ET.iterparse(io.BytesIO(jm), events=("end",)):
        if entry.tag != "entry":
            continue
        identity = entry.findtext("ent_seq")
        forms = {e.text for e in entry.findall("k_ele/keb")} | {e.text for e in entry.findall("r_ele/reb")}
        if any("勘" in (e.text or "") for e in entry.findall("k_ele/keb")):
            reproduced[0].append(identity)
        applicable = forms & matches.keys()
        if applicable:
            reproduced[1].append(identity)
            for word in applicable:
                matches[word].append(identity)
        if identity in selected:
            require(canonical(entry) == canonical(selected[identity]), f"Full family mismatch: {identity}")
        entry.clear()
    require(reproduced == packets and matches == comparison["matches"], "Exact extraction mismatch")
    require(list(map(len, packets)) == [92, 43] and len(selected) == 134, "Family coverage mismatch")
    characters = {}
    for packet in plan["sourceEvidence"]["rawCharacterPackets"]:
        for entry in ET.parse(S / packet).getroot().findall("character"):
            c = entry.findtext("literal")
            require(c not in characters, "Duplicate character")
            characters[c] = entry
    reproduced_chars = set()
    for entry in ET.fromstring(kd).findall("character"):
        c = entry.findtext("literal")
        if c in characters:
            require(canonical(entry) == canonical(characters[c]), f"Raw character mismatch: {c}")
            reproduced_chars.add(c)
    require(len(characters) == 18 and reproduced_chars == characters.keys(), "Character packet incomplete")
    radicals = {}
    for line in frozen["n1-UnicodeData-17.0.0.txt"].decode("utf-8").splitlines():
        fields = line.split(";")
        cp = int(fields[0], 16)
        if 0x2F00 <= cp <= 0x2FD5:
            radicals[cp - 0x2F00 + 1] = chr(int(fields[5].split()[-1], 16))
    row = load(S / "batch-107-input-metadata.json")["sourceIndexRecord"]
    source = json.loads(frozen["n1-kanji-source-20261102.json"])
    index = load(S / "source-index.json")
    require([item["kanji"] for item in index] == source, "Full source index order/membership mismatch")
    require(row == index[117] and row["sourceRow"] == 118 and source[117] == "勘", "Source row changed")
    require(metadata_record(characters["勘"], radicals) == row["metadata"], "Raw row metadata mismatch")
    for suffix in ("membership", "progress"):
        member = load(S / f"batch-107-{suffix}.json")
        require(member["membership"] == ["勘"] and member["sourceRows"] == [118] and
                member["sourceReadingOrder"] == {"onyomi": ["カン"], "kunyomi": []}, "Membership changed")
    for receipt in load(S / "batch-107-public-source-receipts.json"):
        archive = (S / receipt["archive"]).read_bytes()
        raw = gzip.decompress(archive)
        require(sha(archive) == receipt["archiveSha256"] and sha(raw) == receipt["rawSha256"] and
                len(raw) == receipt["rawBytes"], "Public source archive mismatch")
        require(sha((S / receipt["extractedText"]).read_bytes()) == receipt["extractedTextSha256"],
                "Public source extraction changed")
    return selected, characters, row


def audit():
    plan = load(S / "batch-107-source-completion-plan.json")
    require(plan["baseCommit"] == BASE and plan["membership"] == ["勘"] and plan["sourcePreparationComplete"],
            "Unqualified source plan")
    # Authenticate retained evidence against the signed source commit, not a session recipe.
    record_raw = (S / "execution-843.json").read_bytes()
    verify_source_bytes(record_raw, git_bytes(SOURCE, "docs/n1-sources/execution-843.json"),
                        "c57a20dc97b6d4fba24e74500aa03e6e472a5a9d5a81ac51d93f6a913fab20db")
    source_record = json.loads(record_raw)
    source_representations = []
    for name, expected in source_record["sourceFiles"].items():
        raw = (R / name).read_bytes()
        blob = git_bytes(SOURCE, name)
        verify_source_bytes(raw, blob, expected, binary=name.endswith(".gz"))
        source_representations.append({
            "path": name, "recordedLocalRawSha256": expected, "localRawSha256": sha(raw),
            "signedGitRawSha256": sha(blob), "byteEqual": raw == blob,
            "localCRLF": raw.count(b"\r\n"), "gitCRLF": blob.count(b"\r\n"),
            "exactLfRepresentationEqual": True,
        })
    families, characters, row = reproduce_sources(plan)
    baseline = load(S / "batch-107-baseline-plan.json")
    before = json.loads(git_bytes(BASE, "manifest.json"))
    require(before == baseline["runtimeManifest"], "Wrong published baseline")
    current = load(R / "manifest.json")
    require(current == build_manifest(R), "Manifest stale")
    changes = {edit["article"] for edit in plan["linkPlan"]["exactReusedChanges"]}
    additions = {"kanji/勘.md", "strokes/勘.json"}
    runtime_delta(before, current, additions, changes)
    require(current["schemaVersion"] == 1 and current["baseLanguage"] == "en" and
            current["targetLanguage"] == "ja", "Language/schema changed")
    for name, old in baseline["inventory"].items():
        require(metadata(R, name) == old["metadata"], f"Baseline metadata changed: {name}")
        if name not in changes:
            require(sha((R / name).read_bytes()) == old["sha256"], f"Baseline article bytes changed: {name}")
    require({p.relative_to(R).as_posix() for folder in ("kanji", "words") for p in (R / folder).glob("*.md")}
            == set(baseline["inventory"]) | {"kanji/勘.md"}, "Unexpected article membership")
    for edit in plan["linkPlan"]["exactReusedChanges"]:
        reused_changes(git_bytes(BASE, edit["article"]).decode("utf-8"),
                       (R / edit["article"]).read_text(encoding="utf-8"), [edit])
    verify_member(metadata(R, "kanji/勘.md"), plan["kanjiPlan"], characters["勘"])
    require(len({metadata(R, name)["title"] for name in current["files"] if name.startswith("kanji/")})
            == len([name for name in current["files"] if name.startswith("kanji/")]), "Duplicate kanji title")
    require(plan["supportPlan"]["newNecessary"] == [], "Unexpected support creation")
    for word in plan["supportPlan"]["reused"]:
        meta = metadata(R, word["article"])
        require(all(meta[key] == word[key] for key in ("word", "reading", "title", "jlpt", "type")) and
                meta.get("quiz_exclusions", []) == word["originalExclusions"], "Reused word identity/guards changed")
        require(all(teachable_lexical_pair(families[word["entryId"]], word["word"], word["reading"], sense)
                    for sense in word["selectedSenses"]), "Selected sense restrictions mismatch")
    pairs = {(c, word["article"]) for word in plan["supportPlan"]["reused"]
             for c in metadata(R, word["article"])["kanji"]}
    require(pairs == {tuple(pair) for pair in plan["linkPlan"]["allMappedPairs"]} and len(pairs) == 5,
            "All mapped pairs differ from written components")
    candidates = load(S / "baseline-word-candidates.json")
    require(activated_baseline_pairs(before, ["勘"], candidates) ==
            {tuple(pair) for pair in plan["linkPlan"]["activatedBaselinePairs"]} ==
            {("勘", word["article"]) for word in plan["supportPlan"]["reused"]}, "Activated baseline pair missing")
    verify_directions(R, plan["linkPlan"]["requiredDirections"], pairs)
    text = (R / "kanji" / "勘.md").read_text(encoding="utf-8")
    reading_table = text.split("## Readings\n", 1)[1].split("## Common words\n", 1)[0]
    rows = [line for line in reading_table.splitlines() if line.startswith("| カン | on |")]
    require(len(rows) == 1 and "(../words/勘.md)" in rows[0], "Own curated row linked example missing")
    require(teachable_lexical_pair(families["1210590"], "勘", "かん", 1), "On example unsupported")
    require(teachable_lexical_pair(families["1281020"], "勘える", "かんがえる", 1), "Rare spelling unsupported")
    require(any(k.findtext("keb") == "勘える" and k.findtext("ke_inf") == "rarely used kanji form"
                for k in families["1281020"].findall("k_ele")), "Spelling qualifier lost")
    for distractor in plan["kanjiPlan"]["curatedDistractors"]:
        require(metadata(R, f"kanji/{distractor['kanji']}.md")["title"] == distractor["actualTitle"],
                "Wrong choice label changed")
    for guard in plan["kanjiPlan"]["directGuardRationale"]:
        require(metadata(R, f"kanji/{guard['kanji']}.md")["title"] == guard["actualTitle"], "Guard label changed")
    for first, second in plan["supportPlan"]["wordQuizAudit"]["preservedDirectPairs"]:
        require(second in metadata(R, f"words/{first}.md").get("quiz_exclusions", []) or
                first in metadata(R, f"words/{second}.md").get("quiz_exclusions", []), "Original word pair lost")
    verify_geometry((S / "batch-107-kanjivg.svg").read_bytes(), load(R / "strokes" / "勘.json"),
                    load(S / "batch-107-stroke-evidence.json"), row,
                    (R / "tools" / "generate_strokes.py").read_bytes())
    # Existing geometry/other payload preservation is independently covered by runtime_delta and fresh hashing.
    learner_paths = ["kanji/勘.md", *sorted(changes)]
    learner_text = "\n".join((R / name).read_text(encoding="utf-8") for name in learner_paths)
    han = sorted(set(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", learner_text)))
    inspection_han = sorted(set(han) | set(re.findall(
        r"[\u3400-\u9fff\uf900-\ufaff]", plan["fontPlan"]["proposedTextInventory"])))
    from fontTools.ttLib import TTFont
    fonts = []
    for old in load(S / "batch-107-font-preparation.json")["fonts"]:
        font_path = Path(old["path"])
        require(sha(font_path.read_bytes()) == old["sha256"], "Bundled font changed")
        with TTFont(font_path) as font:
            cmap = font.getBestCmap()
            missing = [c for c in inspection_han if ord(c) not in cmap or cmap[ord(c)] == ".notdef"]
        fonts.append({"path": str(font_path), "sha256": old["sha256"], "missing": missing})
    all_hashes = {name: digest for section in current.values() if isinstance(section, dict)
                  for name, digest in section.items()}
    return {
        "schemaVersion": 1, "batch": "107", "execution": 844, "baseCommit": BASE,
        "sourceSnapshot": SOURCE, "sourceRows": [118], "membership": ["勘"],
        "sourceRepresentations": source_representations,
        "originalAuditFailure": "Initial844 exact raw-to-Git comparison stopped at additional-article-snapshots.json. "
                                "Its recorded/local raw hash matched;8CRLF local versus0CRLF Git differed only by "
                                "repository line-ending conversion. Original runtime-audit-844.txt retained; "
                                "raw recorded source hashes remain strictly checked, text Git identity separately "
                                "uses exact LF representation, and binary.gz identity remains byte-exact.",
        "frozenInputHashesVerified": True, "decompressedDictionaryHashesVerified": True,
        "completeFamiliesReproduced": 134, "completeRawCharacterRecordsReproduced": 18,
        "fullSourceIndexOrderVerified": True, "exactRawMemberMetadataVerified": True,
        "runtimeAdditions": sorted(additions), "baselineRuntimeEdits": sorted(changes),
        "baselineArticles": len(baseline["inventory"]), "baselineMetadataPreserved": True,
        "unchangedBaselineArticleBytesVerified": len(baseline["inventory"]) - len(changes),
        "allOtherBaselineRuntimeHashesPreserved": True, "exactReusedEditsVerified": 5,
        "allMappedPairs": sorted([list(pair) for pair in pairs]), "requiredDirections": 10,
        "activatedBaselinePairs": 3, "newWords": 0, "reusedWords": 3,
        "fullOnyomi": ["カン"], "fullKunyomi": [], "quizOnyomi": ["カン"], "quizKunyomi": [],
        "offeredKeysMechanicalMirrorOnly": {"on": ["かん"], "kun": []},
        "curatedWrongChoices": ["勤", "助", "期"], "directKanjiGuards": plan["kanjiPlan"]["quizExclusions"],
        "preservedDirectWordPairs": plan["supportPlan"]["wordQuizAudit"]["preservedDirectPairs"],
        "supplementarySpelling": {"word": "勘える", "reading": "かんがえる", "entry": "1281020",
                                 "rareSpellingNotRarePronunciation": True, "offered": False},
        "strokePaths": 11, "pointsPerPath": 16, "exactPinnedConverterOutput": True,
        "manifestFresh": True, "contentVersion": current["contentVersion"],
        "runtimeHashCount": len(all_hashes),
        "changedRuntimeHashes": {name: current["files"][name] for name in sorted(additions | changes)},
        "learnerArticlePaths": learner_paths, "finalLearnerHan": han, "finalLearnerHanCount": len(han),
        "allInspectionHan": inspection_han, "allInspectionHanCount": len(inspection_han),
        "fonts": fonts, "actualFourModeRendering": "pending",
        "productionQuizChecks": "pending; not established by this Python mirror",
        "independentContentReview": "pending", "nativeAcceptance": "pending", "published": False,
        "auditorDisposition": "Dedicated equivalent exact-current audit reuses repository invariants without "
                              "fabricating the generic source-plan shape; generic CLI not claimed run.",
        "limits": "Mechanical full-source/current-runtime/baseline/pairs/readings/guards/geometry/manifest checks only. "
                  "Not lexical naturalness, actual production options, native/rendered/phone, independent review "
                  "or publication. All original acceptance gates remain mandatory.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    with args.output.open("x", encoding="utf-8") as stream:
        stream.write(json.dumps(result, ensure_ascii=True, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=True))
