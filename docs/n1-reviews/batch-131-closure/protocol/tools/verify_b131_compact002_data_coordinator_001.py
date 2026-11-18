"""Independently verify compact002 source transformations and retained packet bytes."""
import copy
import difflib
import hashlib
import json
import os
import re
import stat
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
OLD = WS / "review-packets" / "batch-131-1359b467-compact-001"
NEW = WS / "review-packets" / "batch-131-1359b467-compact-002"
OLD_SHA = "454c924ce460d050d31eedca225b9553d42790a0060df474088e38c7ca049b39"
ADDED = {
    "evidence/kanjidic2-review-projection.xml",
    "evidence/jmdict-review-core.xml",
    "evidence/title-index-delta.txt",
    "evidence/jmdict-extension-index.json",
}
CHANGED = {"REVIEW.md", "packet.json"}
REMOVED_READINGS = {"pinyin", "korean_r", "korean_h", "vietnam"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def frozen(path, expected=None):
    raw = path.read_bytes()
    require(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_READONLY,
            f"Writable input: {path.name}")
    if expected is not None:
        require(hashlib.sha256(raw).hexdigest() == expected, f"Hash mismatch: {path.name}")
    return raw


def canonical(node):
    return ET.canonicalize(ET.tostring(node, encoding="unicode"), strip_text=True)


def projected_character(original):
    node = copy.deepcopy(original)
    for parent in node.iter():
        for child in list(parent):
            remove = (
                child.tag in {"codepoint", "dic_number", "query_code"}
                or child.tag == "meaning" and "m_lang" in child.attrib
                or child.tag == "reading" and child.get("r_type") in REMOVED_READINGS
            )
            if remove:
                parent.remove(child)
    return node


def expected_projection(raw):
    root = ET.fromstring(raw)
    require(root.tag == "kanjidic2" and not root.attrib, "Unexpected KANJIDIC root")
    require(all(node.tag == "character" for node in root), "Non-character source child")
    lines = [canonical(projected_character(node)) for node in root]
    return ("<kanjidic2>\n" + "\n".join(lines) + "\n</kanjidic2>\n").encode("utf-8")


def jmdict_partition(raw, targets, declared, readings):
    lines = raw.decode("utf-8").splitlines()
    require(lines[0] == "<JMdict>" and lines[-1] == "</JMdict>", "Unexpected JMdict wrapper")
    core, remainder, ids, chosen = [], [], set(), []
    for line in lines[1:-1]:
        node = ET.fromstring(line)
        require(node.tag == "entry", "Expected one complete entry per line")
        identity = node.findtext("ent_seq")
        require(identity is not None and identity not in ids, "Missing or duplicate entry ID")
        ids.add(identity)
        spellings = [n.text for n in node.findall("k_ele/keb")]
        pronunciations = [n.text for n in node.findall("r_ele/reb")]
        matches = (
            any(character in spelling for spelling in spellings for character in targets)
            or bool(declared.intersection(spellings))
            or bool(readings.intersection(pronunciations))
        )
        (core if matches else remainder).append(line)
        if matches:
            chosen.append(identity)
    projected = ("<JMdict>\n" + "\n".join(core) + "\n</JMdict>\n").encode("utf-8")
    return projected, chosen, len(remainder), len(ids)


def title_delta(before, after):
    def index(raw):
        rows = [line.split(" ", 1) for line in raw.decode("utf-8").splitlines()]
        require(all(len(row) == 2 and len(row[0]) == 1 for row in rows), "Bad title-index row")
        require(len({row[0] for row in rows}) == len(rows), "Duplicate title-index character")
        return dict(rows)
    baseline, candidate = index(before), index(after)
    return {
        "added": {c: candidate[c] for c in candidate if c not in baseline},
        "removed": {c: baseline[c] for c in baseline if c not in candidate},
        "changed": {c: [baseline[c], candidate[c]]
                    for c in baseline.keys() & candidate.keys() if baseline[c] != candidate[c]},
    }


def main(manifest_sha, output):
    require(re.fullmatch(r"[a-f0-9]{64}", manifest_sha), "Expected actual handoff manifest hash")
    output = Path(output)
    require(output.parent == WS / "scratch-131" / "review" and not output.exists(),
            "Output must be a new direct child of scratch-131/review")
    old = json.loads(frozen(OLD / "SHA256SUMS.json", OLD_SHA))
    new = json.loads(frozen(NEW / "SHA256SUMS.json", manifest_sha))
    record_files = {name for name in new
                    if re.fullmatch(r"evidence/jmdict-extension-records/[0-9]+\.xml", name)}
    require(set(new) == set(old) | ADDED | record_files, "Unexpected packet addition or removal")
    actual = {p.relative_to(NEW).as_posix() for p in NEW.rglob("*") if p.is_file()}
    require(actual == set(new) | {"SHA256SUMS.json"}, "Unlisted packet file or missing file")
    for name, digest in new.items():
        parts = name.split("/")
        require(all(p not in ("", ".", "..") and ":" not in p and "\\" not in p for p in parts),
                "Unsafe packet-relative path")
        frozen(NEW.joinpath(*parts), digest)
        if name in old and name not in CHANGED:
            require(digest == old[name], f"Unaccounted change: {name}")
    metadata = json.loads(frozen(NEW / "packet.json"))
    prior_metadata = json.loads(frozen(OLD / "packet.json", old["packet.json"]))
    for key in prior_metadata:
        require(metadata[key] == prior_metadata[key], f"Candidate binding changed: {key}")
    kd = frozen(NEW / "evidence" / "kanjidic2-records.xml")
    projection = frozen(NEW / "evidence" / "kanjidic2-review-projection.xml")
    require(projection == expected_projection(kd), "Projection differs from exact allowed deletion")
    require(len(ET.fromstring(projection)) == 182, "KANJIDIC record count differs")
    reference = json.loads(frozen(NEW / "eligibility-reference.json"))
    declared = set(reference["newCards"]) | {"\u885e"}
    for card in reference["cards"]:
        declared.update(card["quiz_exclusions"])
        declared.update(card["distractors"])
    readings = set()
    for character in reference["newCards"]:
        text = frozen(NEW / "snapshot" / "kanji" / f"{character}.md").decode("utf-8")
        for kind in ("onyomi", "kunyomi"):
            matches = re.findall(rf"^{kind}: \[([^\]]*)\]\r?$", text, re.M)
            require(len(matches) == 1, f"Missing or ambiguous {kind}")
            for reading in filter(None, (v.strip() for v in matches[0].split(","))):
                readings.add("".join(chr(ord(c) - 0x60) if "\u30a1" <= c <= "\u30f6" else c
                                     for c in reading))
    target_forms = set(reference["newCards"]) | {"\u885e"}
    jd = frozen(NEW / "evidence" / "jmdict-families.xml")
    expected, ids, remaining, total = jmdict_partition(jd, target_forms, declared, readings)
    require(frozen(NEW / "evidence" / "jmdict-review-core.xml") == expected,
            "JMdict core is not the exact complete-record partition")
    require(total == 874 and len(ids) == 615 and remaining == 259, "Source partition count differs")
    core_ids, remainder_ids, characters = set(ids), [], {}
    for line in jd.decode("utf-8").splitlines()[1:-1]:
        node = ET.fromstring(line)
        identity = node.findtext("ent_seq")
        kind = "matchingCoreIds" if identity in core_ids else "matchingRemainderIds"
        for spelling in dict.fromkeys(n.text for n in node.findall("k_ele/keb")):
            if len(spelling) == 1:
                characters.setdefault(spelling, {"matchingCoreIds": [], "matchingRemainderIds": []})
                characters[spelling][kind].append(identity)
        if identity not in core_ids:
            remainder_ids.append(identity)
            record_name = f"evidence/jmdict-extension-records/{identity}.xml"
            require(frozen(NEW.joinpath(*record_name.split("/"))) == (line + "\n").encode("utf-8"),
                    f"Supplemental record altered: {identity}")
    extension_index = json.loads(frozen(NEW / "evidence" / "jmdict-extension-index.json"))
    require(extension_index["characters"] == characters, "Supplemental exact-keb index differs")
    require(extension_index["recordOrder"] == remainder_ids, "Supplemental record order differs")
    require(record_files == {f"evidence/jmdict-extension-records/{i}.xml" for i in remainder_ids},
            "Missing or extraneous supplemental record file")
    baseline = frozen(NEW / "evidence" / "baseline-title-index.txt")
    candidate = frozen(NEW / "evidence" / "title-index.txt")
    delta = title_delta(baseline, candidate)
    require(set(delta["added"]) == set(reference["newCards"]) and not delta["removed"]
            and not delta["changed"], "Baseline-to-candidate title delta differs")
    delta_text = "".join(difflib.unified_diff(
        baseline.decode("utf-8").splitlines(keepends=True),
        candidate.decode("utf-8").splitlines(keepends=True),
        fromfile="evidence/baseline-title-index.txt", tofile="evidence/title-index.txt", n=0,
    ))
    require(frozen(NEW / "evidence" / "title-index-delta.txt") == delta_text.encode("utf-8"),
            "Displayed title delta differs")
    result = {
        "status": "PASS_DATA_ONLY", "packetManifestSha256": manifest_sha,
        "predecessorManifestSha256": OLD_SHA, "packetFiles": len(new),
        "retainedFilesUnchanged": len(old) - len(CHANGED),
        "projectionBytes": len(projection), "kanjidicRecords": 182,
        "jmdictCoreRecords": len(ids), "jmdictRemainderRecords": remaining,
        "completeSupplementalRecordFiles": len(record_files),
        "exactKebIndexCharacters": len(characters),
        "jmdictCoreBytes": len(expected), "titleDelta": delta,
        "deltaPresentationSha256": new["evidence/title-index-delta.txt"],
        "limits": "Source data and retained-byte verification only. Human inspection of REVIEW.md and packet metadata "
                  "disclosures remains required. Chain, forecast, dynamic comparison "
                  "extensions, lifecycle, prompt neutrality and reviewer acceptance are not certified here.",
    }
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    output.chmod(stat.S_IREAD)
    print(json.dumps(result, ensure_ascii=False))
    print("Record SHA256: " + hashlib.sha256(output.read_bytes()).hexdigest())


class TransformationTests(unittest.TestCase):
    def test_projection_preserves_english_japanese_radical_and_nanori(self):
        raw = b'<kanjidic2><character><literal>X</literal><radical><rad_value>1</rad_value></radical><codepoint><cp_value>10</cp_value></codepoint><reading_meaning><rmgroup><reading r_type="ja_on">ON</reading><reading r_type="pinyin">PIN</reading><meaning>ordinary</meaning><meaning m_lang="fr">autre</meaning></rmgroup><nanori>NAME</nanori></reading_meaning></character></kanjidic2>'
        node = ET.fromstring(expected_projection(raw))[0]
        self.assertEqual(node.findtext("radical/rad_value"), "1")
        self.assertEqual(node.findtext("reading_meaning/nanori"), "NAME")
        self.assertEqual(node.findtext("reading_meaning/rmgroup/meaning"), "ordinary")
        self.assertEqual(node.findtext("reading_meaning/rmgroup/reading"), "ON")
        self.assertEqual(len(node.findall(".//meaning")), 1)
        self.assertEqual(len(node.findall(".//reading")), 1)
        self.assertIsNone(node.find("codepoint"))

    def test_partition_keeps_all_senses_and_rejects_duplicate_ids(self):
        raw = b'<JMdict>\n<entry><ent_seq>1</ent_seq><k_ele><keb>AB</keb></k_ele><sense><gloss>first</gloss></sense><sense><gloss>second</gloss></sense></entry>\n<entry><ent_seq>2</ent_seq><r_ele><reb>R</reb></r_ele></entry>\n</JMdict>\n'
        core, ids, remainder, total = jmdict_partition(raw, {"A"}, set(), set())
        self.assertIn(b"<gloss>second</gloss>", core)
        self.assertEqual((ids, remainder, total), (["1"], 1, 2))
        with self.assertRaises(ValueError):
            jmdict_partition(raw.replace(b"<ent_seq>2", b"<ent_seq>1"), {"A"}, set(), set())

    def test_delta_detects_changed_removed_and_duplicate_titles(self):
        result = title_delta(b"A before\nB stays\nC removed\n", b"A after\nB stays\nD added\n")
        self.assertEqual(result["changed"], {"A": ["before", "after"]})
        self.assertEqual(result["removed"], {"C": "removed"})
        self.assertEqual(result["added"], {"D": "added"})
        with self.assertRaises(ValueError):
            title_delta(b"A first\nA second\n", b"A first\n")


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test"]:
        unittest.main(argv=[sys.argv[0]])
    elif len(sys.argv) == 3:
        main(*sys.argv[1:])
    else:
        raise SystemExit("usage: verifier MANIFEST_SHA NEW_OUTPUT.json | --self-test")
