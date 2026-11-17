"""Verify the exact, complete dictionary selection for the focused B123 follow-up."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_b123_reconciliation_selection import unique_object, unique_strings, verify_selection
from verify_b123_revision_v2 import INPUTS
from verify_b123_revision_v3 import PARENT, PREFIX
from verify_reconciliation_sources import element_value


def check_queries(receipt):
    literals = unique_strings(receipt["kanjidic2ExactLiterals"], "literal queries")
    queries = unique_strings(receipt["jmdictExactWrittenQueries"], "written queries")
    require(literals == {"\u666e"} and queries == {"\u666e\u304f", "\u666e\u53ca", "\u904d\u304f"},
            "Focused query set differs")
    require("jmdictExplicitEntryIds" not in receipt, "Unexpected explicit-ID selection")
    require(set(receipt["files"]) == {"comparison-\u666e.md", "jmdict-records.xml",
                                     "kanjidic2-records.xml"}, "Focused source inventory differs")
    return literals, queries


def verify(candidate, receipt_sha, output):
    config = load_batch(123)
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P", candidate).decode().strip() == PARENT,
            "Focused revision is not the expected direct child")
    blob = lambda path: git(config, "show", f"{candidate}:{PREFIX}{path}")
    raw_receipt = blob("query-manifest.json")
    require(sha(raw_receipt) == receipt_sha, "Signed query manifest changed")
    receipt = json.loads(raw_receipt, object_pairs_hook=unique_object)
    require(str(receipt["batch"]) == "123" and receipt["baseline"] == config["base"]
            and receipt["initialCandidate"] == config["candidate"]
            and receipt["immediateParent"] == PARENT, "Query manifest ancestry differs")
    memory = receipt["memory"]
    require(receipt["admissionFreeBytes"] > 2 * 1024**3
            and memory["freeRamBeforeBytes"] > 2 * 1024**3
            and memory["minimumObservedFreeRamBytes"] >= 1024**3
            and memory["abortThresholdBytes"] == 1024**3
            and memory["samplingIntervalSeconds"] == 0.25 and not memory["breach"],
            "Source collector resource contract failed")
    literals, queries = check_queries(receipt)
    guard, _ = start_guard("B123 focused exact source selection")
    selections = []
    try:
        for path, item in receipt["files"].items():
            raw = blob(path)
            require(sha(raw) == item["sha256"] and len(raw) == item["bytes"],
                    f"Signed source binding differs: {path}")
        copy = blob("comparison-\u666e.md")
        for commit in (config["base"], config["candidate"], PARENT, candidate):
            require(copy == git(config, "show", f"{commit}:kanji/\u666e.md"),
                    "Comparison card changed between bound snapshots")
        for kind, (filename, digest, tag, key) in INPUTS.items():
            source = WS / "control" / "inputs" / filename
            declaration = receipt["sources"][kind]
            require(declaration["input"] == str(source)
                    and declaration["inputSha256"] == digest
                    and declaration["output"] == f"{kind}-records.xml",
                    f"Dictionary provenance differs: {kind}")
            calculated = hashlib.sha256()
            with source.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    calculated.update(chunk)
                    guard.check()
            require(calculated.hexdigest() == digest, f"Pinned input changed: {kind}")
            raw = blob(declaration["output"])
            root = ET.fromstring(raw)
            require(root.tag.lower() == kind, f"Unexpected dictionary root: {kind}")
            nodes = root.findall(tag)
            identities = [node.findtext(key) for node in nodes]
            unique_strings(identities, f"{kind} output identities")
            require(identities == declaration["members"], f"Declared members differ: {kind}")
            expected_ids = ["\u666e"] if kind == "kanjidic2" else ["1497100", "1497110"]
            require(identities == expected_ids, "Focused source members differ")
            expected = {identity: element_value(node) for identity, node in zip(identities, nodes)}
            selected_queries = literals if kind == "kanjidic2" else queries
            with gzip.open(source, "rb") as stream:
                found, hits = verify_selection(stream, tag, key, selected_queries, set(),
                                               expected, guard)
            require(found == identities and all(hits.values()),
                    f"Source-order membership or query coverage differs: {kind}")
            selections.append({"source": kind, "inputSha256": digest, "outputSha256": sha(raw),
                               "members": found, "queryMatches": hits,
                               "completeRecordsVerified": len(found)})
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Focused selection RAM breach")
    print(json.dumps(freeze_json(Path(output), {
        "batch": 123, "status": "PASS", "candidate": candidate, "parent": PARENT,
        "queryManifestSha256": receipt_sha, "selections": selections,
        "comparisonCardSha256": sha(copy), "memory": memory,
        "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Exact query membership, full records and comparison bytes only; "
                  "not linguistic sufficiency, exhaustive discovery or publication acceptance.",
    })))


if __name__ == "__main__":
    verify(*sys.argv[1:])
