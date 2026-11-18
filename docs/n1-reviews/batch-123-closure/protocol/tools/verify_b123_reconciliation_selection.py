"""Verify B123's declared exact-query and explicit-ID supplemental selections."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_b123_revision_v2 import INPUTS, SOURCE
from verify_reconciliation_sources import element_value


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def unique_strings(values, label):
    require(isinstance(values, list)
            and all(isinstance(value, str) and value.strip() for value in values)
            and len(values) == len(set(values)), f"Invalid {label}")
    return set(values)


def verify_selection(stream, tag, key, queries, explicit_ids, expected, guard):
    selected, hits = [], {query: [] for query in queries}
    parser = ET.iterparse(stream, events=("start", "end"))
    _, root = next(parser)
    for event, node in parser:
        if event != "end" or node.tag != tag:
            continue
        identity = node.findtext(key)
        written = ({identity} if tag == "character"
                   else {item.text for item in node.findall("k_ele/keb") if item.text})
        matched = queries & written
        if matched or identity in explicit_ids:
            require(identity not in selected, f"Duplicate input identity: {identity}")
            require(identity in expected, f"Missing selected record: {identity}")
            require(element_value(node) == expected[identity],
                    f"Incomplete or altered selected record: {identity}")
            selected.append(identity)
            for query in matched:
                hits[query].append(identity)
        node.clear()
        root.clear()
        guard.check()
    require(set(selected) == set(expected), "Unexpected or missing output membership")
    require(explicit_ids <= set(selected), "Explicit entry ID missing from input")
    return selected, {query: hits[query] for query in sorted(hits)}


def main(candidate, receipt_sha, output):
    config = load_batch(123)
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P", candidate).decode().strip()
            == config["candidate"], "Reconciliation is not the direct initial child")
    blob = lambda path: git(config, "show", f"{candidate}:{SOURCE}{path}")
    raw_receipt = blob("query-manifest.json")
    require(sha(raw_receipt) == receipt_sha, "Signed query manifest changed")
    receipt = json.loads(raw_receipt, object_pairs_hook=unique_object)
    require(str(receipt["batch"]) == "123" and receipt["baseline"] == config["base"]
            and receipt["initialCandidate"] == config["candidate"],
            "Query manifest has different batch or ancestry")
    memory = receipt["memory"]
    require(receipt["admissionFreeBytes"] > 2 * 1024**3
            and memory["freeRamBeforeBytes"] > 2 * 1024**3
            and memory["minimumObservedFreeRamBytes"] >= 1024**3
            and memory["abortThresholdBytes"] == 1024**3
            and memory["samplingIntervalSeconds"] == 0.25 and not memory["breach"],
            "Source collector resource contract failed")
    literals = unique_strings(receipt["kanjidic2ExactLiterals"], "literal queries")
    queries = unique_strings(receipt["jmdictExactWrittenQueries"], "written queries")
    explicit_ids = unique_strings(receipt["jmdictExplicitEntryIds"], "explicit IDs")
    require(literals == set("範標紀鏡様格形本倣像囲限境界広方度道計測量坂理師象儀"),
            "Required supplemental character set differs")
    require({"1205270", "1438050", "1956840", "2713240"} <= explicit_ids,
            "Required complete entry selection missing")
    expected_files = {f"comparison-cards/{literal}.md" for literal in literals - {"範"}}
    expected_files |= {f"{kind}-records.xml" for kind in INPUTS}
    require(set(receipt["files"]) == expected_files, "Source file inventory differs")
    guard, _ = start_guard("B123 supplemental exact selection")
    selections, copies = [], {}
    try:
        for path, binding in receipt["files"].items():
            raw = blob(path)
            require(sha(raw) == binding["sha256"] and len(raw) == binding["bytes"],
                    f"Signed source file binding differs: {path}")
            if path.startswith("comparison-cards/"):
                article = f"kanji/{Path(path).stem}.md"
                require(raw == git(config, "show", f"{config['base']}:{article}")
                        == git(config, "show", f"{config['candidate']}:{article}")
                        == git(config, "show", f"{candidate}:{article}"),
                        f"Comparison card differs from frozen teaching: {article}")
                copies[article] = sha(raw)
            guard.check()
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
            expected = {identity: element_value(node) for identity, node in zip(identities, nodes)}
            selected_queries = literals if kind == "kanjidic2" else queries
            selected_ids = set() if kind == "kanjidic2" else explicit_ids
            with gzip.open(source, "rb") as stream:
                found, hits = verify_selection(stream, tag, key, selected_queries,
                                               selected_ids, expected, guard)
            require(found == identities, f"Source-order membership differs: {kind}")
            selections.append({
                "source": kind, "inputSha256": digest, "outputSha256": sha(raw),
                "mode": "exact-literal" if kind == "kanjidic2" else "exact-keb-or-ent_seq",
                "queries": sorted(selected_queries), "explicitEntryIds": sorted(selected_ids),
                "members": found, "completeRecordsVerified": len(found), "queryMatches": hits,
                "queriesWithoutMatches": [query for query, matches in hits.items() if not matches],
            })
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Supplemental selection verification RAM breach")
    print(json.dumps(freeze_json(Path(output), {
        "batch": 123, "status": "PASS", "candidate": candidate, "base": config["base"],
        "initialCandidate": config["candidate"], "queryManifestSha256": receipt_sha,
        "selections": selections, "comparisonCards": copies, "memory": memory,
        "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Exact declared selection completeness and full record preservation, not "
                  "linguistic sufficiency, exhaustive query discovery or publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: CANDIDATE_SHA QUERY_MANIFEST_SHA NEW_PROOF")
    main(*sys.argv[1:])
