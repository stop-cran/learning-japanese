#!/usr/bin/env python3
"""Audit one later N1 batch against its exact base; not linguistic acceptance."""
import argparse
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

from audit_n1_pilot import metadata, offered_keys, quiz_readings
from build_manifest import build_manifest
from freeze_n1_sources import KVG_REVISION, require

ROOT = Path(__file__).resolve().parent.parent


def runtime_delta(before, after, additions, changed):
    def payload(manifest):
        return {(section, name): value
                for section, entries in manifest.items() if isinstance(entries, dict)
                for name, value in entries.items()}

    old, new = payload(before), payload(after)
    require(not old.keys() - new.keys(), "Baseline runtime payload removed")
    require(new.keys() - old.keys() == {("files", name) for name in additions},
            "Runtime additions differ from this batch")
    actual_changes = {name for name in old if old[name] != new[name]}
    require(actual_changes == {("files", name) for name in changed},
            "Changed baseline payload differs from recorded reused passages")


def lexical_pair(entry, spelling, reading):
    spellings = {v.text for v in entry.findall("k_ele/keb")}
    if spelling not in spellings:
        return False
    for row in entry.findall("r_ele"):
        restrictions = {v.text for v in row.findall("re_restr")}
        if (row.findtext("reb") == reading and row.find("re_nokanji") is None
                and (not restrictions or spelling in restrictions)):
            return True
    return False


def base_file(root, commit, name):
    return subprocess.check_output(
        ["git", "--no-pager", "show", f"{commit}:{name}"], cwd=root).decode("utf-8")


def reused_changes(old, new, rows, exclusions=None):
    old = old.replace("\r\n", "\n")
    new = new.replace("\r\n", "\n")
    expected = old
    for row in rows:
        require(expected.count(row["before"]) == 1,
                "Reused passage must match exactly once")
        expected = expected.replace(row["before"], row["after"], 1)
    require(expected == new, "Reused passage exceeds recorded exact edits")
    before = yaml.safe_load(old.split("---", 2)[1])
    after = yaml.safe_load(new.split("---", 2)[1])
    if exclusions is not None:
        previous = before.get("quiz_exclusions", [])
        require(len(exclusions) == len(set(exclusions))
                and set(previous) < set(exclusions),
                "Reused exclusions must be distinct additive safeguards")
        before["quiz_exclusions"] = exclusions
    require(before == after, "Reused metadata changed outside recorded exclusions")


def audit(root, batch):
    require(len(batch) == 3 and batch.isascii() and batch.isdigit(),
            "Batch must be a three-digit number")
    folder = root / "docs" / "n1-sources"
    ledger = json.loads((folder / f"batch-{batch}-progress.json").read_text(encoding="utf-8"))
    frozen = json.loads((folder / f"batch-{batch}-membership.json").read_text(encoding="utf-8"))
    members, commit = ledger["membership"], ledger["baseCommit"]
    require(ledger["batch"] == frozen["batch"] == batch
            and commit == frozen["baseCommit"]
            and len(commit) == 40 and all(c in "0123456789abcdef" for c in commit),
            "Invalid batch/base identity")
    require(0 < len(members) <= 15 and len(set(members)) == len(members)
            and members == frozen["membership"]
            and members == [row["kanji"] for row in frozen["members"]]
            and ledger["drafted"] == members, "Incomplete or changed frozen membership")
    source_name = "docs/n1-sources/source-index.json"
    require((root / source_name).read_text(encoding="utf-8")
            == base_file(root, commit, source_name), "Immutable source index changed")
    source = {r["kanji"]: r for r in json.loads((root / source_name).read_text(encoding="utf-8"))}
    for row in frozen["members"]:
        require(source[row["kanji"]]["sourceRow"] == row["sourceRow"],
                "Frozen source-row identity changed")
    current = build_manifest(root)
    require(json.loads((root / "manifest.json").read_text(encoding="utf-8")) == current,
            "Manifest is stale")
    before = json.loads(base_file(root, commit, "manifest.json"))
    mappings = ledger["supportMappings"]
    pairs = {(r["kanji"], r["article"]) for r in mappings}
    recorded_pairs = [tuple(p) for p in ledger["requiredReciprocalPairs"]]
    require(len(mappings) == len(pairs) == len(recorded_pairs)
            and pairs == set(recorded_pairs), "Reciprocal mappings differ")
    new_words = {r["article"] for r in mappings if r["newArticle"]}
    additions = {f"{kind}/{c}.{suffix}" for c in members
                 for kind, suffix in (("kanji", "md"), ("strokes", "json"))} | new_words
    changes = {r["article"] for r in ledger["changedReusedPassages"]}
    runtime_delta(before, current, additions, changes)
    for name in changes:
        rows = [r for r in ledger["changedReusedPassages"] if r["article"] == name]
        exclusion_rows = [r for r in ledger["wordQuizAudit"]["directExclusions"]
                          if f"words/{r['word']}.md" == name]
        require(len(exclusion_rows) <= 1, "Duplicate reused exclusion decision")
        reused_changes(base_file(root, commit, name),
                       (root / name).read_text(encoding="utf-8"), rows,
                       exclusion_rows[0]["exclude"] if exclusion_rows else None)
    families = {}
    for packet in ledger["dictionaryPackets"]:
        selection = json.loads((folder / packet["selection"]).read_text(encoding="utf-8"))
        entries = ET.parse(folder / packet["xml"]).getroot().findall("entry")
        ids = [e.findtext("ent_seq") for e in entries]
        require(ids == selection["entryIds"] and len(ids) == len(set(ids)),
                "Dictionary packet membership/order differs")
        families.update(zip(ids, entries))
    for row in mappings:
        c, name = row["kanji"], row["article"]
        require(c in members and name.startswith("words/") and name.endswith(".md"),
                "Invalid support mapping")
        meta = metadata(root, name)
        require(meta["reading"] == row["primaryReading"]
                and bool(row["newArticle"]) == (name in new_words)
                and row["entryIds"] and set(row["entryIds"]) <= families.keys()
                and any(lexical_pair(families[i], meta["word"], meta["reading"])
                        for i in row["entryIds"]), f"Support identity/restrictions mismatch: {name}")
        require(f"(../kanji/{c}.md)" in (root / name).read_text(encoding="utf-8")
                and f"(../{name})" in (root / f"kanji/{c}.md").read_text(encoding="utf-8"),
                f"Missing reciprocal link: {c} / {name}")
    candidates = json.loads((folder / "baseline-word-candidates.json").read_text(encoding="utf-8"))
    activated = {(r["kanji"], r["article"]) for r in candidates if r["kanji"] in members}
    require(activated <= pairs, "Activated baseline pair missing from mappings")
    decisions = ledger["readingDispositions"]
    identities = [(r["kanji"], r["kind"], r["reading"]) for r in decisions]
    expected = [(c, kind, reading) for c in members
                for kind, field in (("on", "onyomi"), ("kun", "kunyomi"))
                for reading in source[c]["metadata"][field]]
    require(identities == expected, "Full reading dispositions/order differ from source")
    projections = ledger["curatedProjection"]
    require([r["kanji"] for r in projections] == members, "Curated membership/order differs")
    offered = 0
    for c, projection in zip(members, projections):
        meta = metadata(root, f"kanji/{c}.md")
        for field in ("kanji", "strokes", "radical", "radicalNumber", "onyomi", "kunyomi"):
            require(meta[field] == source[c]["metadata"][field], f"Source metadata changed: {c}")
        require(meta["jlpt"] == 1 and "jlpt-n1" in meta["tags"]
                and f"grade-{source[c]['metadata']['grade']}" in meta["tags"],
                f"Level/grade changed: {c}")
        strokes = json.loads((root / f"strokes/{c}.json").read_text(encoding="utf-8"))
        require(strokes["kanji"] == c and strokes["sourceRevision"] == KVG_REVISION
                and strokes["strokeCount"] == len(strokes["strokes"]) == meta["strokes"],
                f"Stroke identity/count/revision mismatch: {c}")
        body = (root / f"kanji/{c}.md").read_text(encoding="utf-8")
        table = body.split("## Readings\n", 1)[1].split("## Common words", 1)[0]
        for row in (r for r in decisions if r["kanji"] == c):
            require(type(row["selected"]) is bool and row["reason"].strip()
                    and set(row["entryIds"]) <= families.keys(), f"Invalid reading decision: {c}")
            lines = [line for line in table.splitlines()
                     if line.startswith(f"| {row['reading']} |")]
            require(len(lines) == 1, f"Missing/duplicate reading row: {c} {row['reading']}")
            if row.get("sourceOnly"):
                require(not row["selected"] and "source-only" in lines[0],
                        f"Source-only reading unqualified/offered: {c}")
            if row["selected"]:
                require(row["entryIds"] and (c, row["article"]) in pairs
                        and f"(../{row['article']})" in lines[0],
                        f"Selected reading lacks mapped table support: {c}")
        for kind, field, key in (("on", "onyomi", "onKeys"), ("kun", "kunyomi", "kunKeys")):
            selected = quiz_readings(meta, field)
            quiz_field = "quiz" + field[0].upper() + field[1:]
            require(meta[quiz_field] == projection[quiz_field]
                    == [r["reading"] for r in decisions
                        if r["kanji"] == c and r["kind"] == kind and r["selected"]],
                    f"Curated subset differs from decisions: {c}")
            keys = offered_keys(selected)
            require(keys == projection[key], f"Offered key ledger mismatch: {c}")
            offered += len(keys)
        quiz = ledger["quizAudit"][c]
        require(meta["title"] == quiz["title"] and meta["distractors"] == quiz["distractors"]
                and len(set(meta["distractors"])) == 3
                and quiz["labels"] == [metadata(root, f"kanji/{d}.md")["title"]
                                       for d in meta["distractors"]], f"Quiz labels differ: {c}")
    for row in ledger["wordQuizAudit"]["directExclusions"]:
        require(metadata(root, f"words/{row['word']}.md")["quiz_exclusions"] == row["exclude"],
                "Word exclusion ledger mismatch")
    return {"batch": batch, "baseCommit": commit, "draftKanji": len(members),
            "newWords": len(new_words), "changedReusedArticles": len(changes),
            "requiredReciprocalPairs": len(pairs), "activatedBaselinePairs": len(activated),
            "readingDispositions": len(decisions), "curatedOfferedKeys": offered,
            "sourceOnlyOfferedKeys": 0, "dictionaryFamilies": len(families),
            "exactBaseRuntimePreservedOutsideRecordedChanges": True,
            "manifestFresh": True, "contentVersion": current["contentVersion"],
            "limits": "Mechanical draft audit, not lexical-allocation/naturalness verification, independent review, native/phone acceptance or publication."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", required=True)
    args = parser.parse_args()
    print(json.dumps(audit(ROOT, args.batch), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
