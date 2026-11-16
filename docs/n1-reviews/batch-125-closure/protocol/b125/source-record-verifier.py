"""Verify B124's complete selected dictionary records against the pinned inputs."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import WS, freeze_json, git, require, sha, start_guard
from confirm_v2 import clean
from verify_reconciliation_sources import element_value

BASE = "2655539b587c1ab57e64ab74a97cddaf81bb81c6"
MEMBER = "裕"
COMPARISONS = set('富豊容補複満余')
QUERIES = {'余る', '余分', '余猶', '余裕', '富', '富む', '富裕', '裕福', '豊', '豊か', '豊作', '豊富'}
INPUTS = {
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz",
                 "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed",
                 "character", "literal"),
    "jmdict": ("n1-implementation-JMdict_e.gz",
              "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
              "entry", "ent_seq"),
}
HERE = Path(__file__).resolve().parent
PREFIX = "docs/n1-sources/batch-124/"


def records(raw, tag, key):
    nodes = ET.fromstring(raw).findall(tag)
    values = {node.findtext(key): element_value(node) for node in nodes}
    require(len(values) == len(nodes) and None not in values and "" not in values,
            "Duplicate or missing dictionary identity")
    return values


def verify_stream(stream, tag, key, selections, guard):
    for selection in selections:
        require(selection["mode"] in {"contains-member", "contains-any", "exact"},
                f"Unsupported selection mode: {selection['mode']}")
        if selection["mode"] == "contains-any":
            require(selection["queries"] and all(selection["queries"]),
                    "Contains-any selection requires nonempty queries")
    found = [set() for _ in selections]
    parser = ET.iterparse(stream, events=("start", "end"))
    _, root = next(parser)
    for event, node in parser:
        if event != "end" or node.tag != tag:
            continue
        identity = node.findtext(key)
        keys = ({identity} if tag == "character"
                else {item.text for item in node.findall("k_ele/keb") if item.text})
        for selection, seen in zip(selections, found):
            selected = (any(MEMBER in item for item in keys)
                        if selection["mode"] == "contains-member"
                        else any(query in item for query in selection["queries"] for item in keys)
                        if selection["mode"] == "contains-any"
                        else bool(keys & selection["queries"]))
            if selected:
                require(identity not in seen, "Duplicate identity in pinned dictionary")
                require(identity in selection["expected"],
                        f"Missing applicable family: {selection['name']}/{identity}")
                require(element_value(node) == selection["expected"][identity],
                        f"Incomplete or altered record: {selection['name']}/{identity}")
                seen.add(identity)
        node.clear()
        root.clear()
        guard.check()
    for selection, seen in zip(selections, found):
        require(seen == set(selection["expected"]),
                f"Unexpected or missing extracted record: {selection['name']}")
    return [sorted(seen) for seen in found]


def main(candidate):
    output = HERE / "source-selection-verification-001.json"
    require(not output.exists(), "Preserve existing source verification")
    config = {"repo": str(WS / "b124-worktree"), "candidate": candidate, "base": BASE}
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P", candidate).decode().strip() == BASE,
            "B124 candidate must be a direct child of its published base")
    require(git(config, "show", "-s", "--format=%GF", candidate).decode().strip()
            == "D4C9A275A218AF747B787AFA9D94B9D311BD26A7", "Signing fingerprint differs")
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    snapshot_raw = blob("docs/n1-source-snapshot.json")
    require(snapshot_raw == git(config, "show", f"{BASE}:docs/n1-source-snapshot.json"),
            "Pinned source definitions changed")
    snapshot = json.loads(snapshot_raw)
    guard, _ = start_guard("B124 complete dictionary membership verification")
    results = []
    try:
        for kind, (filename, expected_sha, tag, key) in INPUTS.items():
            source = WS / "control" / "inputs" / filename
            digest = hashlib.sha256()
            with source.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
                    guard.check()
            require(digest.hexdigest() == expected_sha == snapshot["inputs"][filename]["sha256"],
                    f"Pinned input changed: {filename}")
            selections = []
            labels = ("selected", "comparison")
            for label in labels:
                name = f"{kind}-{label}-records.xml"
                raw = blob(PREFIX + name)
                exact = {"selected": {MEMBER}, "comparison": COMPARISONS}[label] \
                    if kind == "kanjidic2" else QUERIES
                mode = "contains-member" if kind == "jmdict" and label == "selected" else "exact"
                selections.append({"name": name, "sha256": sha(raw), "mode": mode,
                                   "queries": exact, "expected": records(raw, tag, key)})
            name = f"comparison-supplement-001/{kind}-records.xml"
            raw = blob(PREFIX + name)
            selections.append({
                "name": name, "sha256": sha(raw),
                "mode": "contains-any" if kind == "jmdict" else "exact",
                "queries": {"厚", "財"}, "expected": records(raw, tag, key),
            })
            with gzip.open(source, "rb") as stream:
                identities = verify_stream(stream, tag, key, selections, guard)
            for selection, matched in zip(selections, identities):
                results.append({
                    "path": PREFIX + selection["name"], "sha256": selection["sha256"],
                    "input": filename, "inputSha256": expected_sha, "mode": selection["mode"],
                    "queries": ([MEMBER] if selection["mode"] == "contains-member"
                                else sorted(selection["queries"])),
                    "completeMatchingRecords": len(matched), "identities": matched,
                })
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source verification RAM guard breached")
    print(json.dumps(freeze_json(output, {
        "batch": 124, "candidate": candidate, "base": BASE, "status": "PASS",
        "snapshotSha256": sha(snapshot_raw), "sourceRecords": results, "memory": memory,
        "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Complete pinned records and exact selection membership, including all readings, "
                  "spellings, restrictions and senses. Not a linguistic, gate, review or publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: python -B verify-source-records.py CANDIDATE_SHA")
    main(sys.argv[1])
