"""Reproduce the signed B131 reconciliation's finite source selection."""
import ast
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from verify_b126_sources import HashedReader
from verify_b129_revision_sources import INPUTS, selection, verify_stream
from verify_b131_payload import BASE, REPO, RUNNER
from verify_b131_revision_runtime_001 import PARENT, ROOT
from verify_b131_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

PREFIX = "docs/n1-sources/batch-131-reconciliation/"
ORIGINAL = "docs/n1-sources/batch-131/"
COMPARISONS = set("\u6c37\u51cd\u9152\u51b4\u6dbc\u4e45\u5bb3\u67af\u6bba\u5352"
                  "\u63f4\u5faa\u756a\u58eb\u8ecd\u9001\u62b5")
PACKET = WS / "review-packets" / "batch-131-1359b467-compact-001"
PACKET_SHA = "454c924ce460d050d31eedca225b9553d42790a0060df474088e38c7ca049b39"
HELPERS = {
    "verify_b126_sources.py": "6fc5f09b2c4ed04de40f9aec2502b2e560c3b577a836b1ae7f59f587e83b20e3",
    "verify_b129_revision_sources.py": "0a0b097d50fea71e5efde646d82f0a84e089bede29fa986d3ed545520245dd34",
    "verify_reconciliation_sources.py": "761688d05d89807478c002e3022749cc6b1cbd9ab4cb18b0805b4c19761ce7e6",
}


def exact_words(producer):
    nodes = [node.value for node in ast.parse(producer).body if isinstance(node, ast.Assign)
             and any(isinstance(target, ast.Name) and target.id == "WORDS" for target in node.targets)]
    require(len(nodes) == 1, "Missing or duplicate exact-word definition")
    node = nodes[0]
    require(isinstance(node, ast.Call) and not node.args and not node.keywords
            and isinstance(node.func, ast.Attribute) and node.func.attr == "split"
            and isinstance(node.func.value, ast.Constant)
            and isinstance(node.func.value.value, str), "Inspect changed exact-word producer")
    words = node.func.value.value.split()
    require(words and len(words) == len(set(words)), "Invalid exact-word inventory")
    return words


def source_selections(receipt, membership, xml, producer, comparisons):
    require(set(comparisons) == COMPARISONS, "Finite comparison scope differs")
    exact = sorted(COMPARISONS | set(exact_words(producer)))
    identities = sorted({identity for raw in comparisons.values()
                         for identity in re.findall(r"\b\d{7}\b", raw.decode("utf-8"))})
    require(receipt["parent"] == PARENT and receipt["publishedBase"] == BASE
            and receipt["producerSha256"] == sha(producer)
            and receipt["predicates"] == {
                "exactSpellings": exact, "entryIdsFromCompleteComparisonCards": identities},
            "Source selector provenance differs")
    queries = {f"{kind}:{value}": [] for kind, values in
               (("exact-spelling", exact), ("entry-id", identities)) for value in values}
    for identity, predicates in membership.items():
        require(re.fullmatch(r"\d{7}", identity) and isinstance(predicates, list)
                and predicates and len(predicates) == len(set(predicates))
                and set(predicates) <= set(queries), "Invalid record-to-query membership")
        for predicate in predicates:
            queries[predicate].append(identity)
    require(receipt["queryCountsIncludingAbsences"] == {q: len(ids) for q, ids in queries.items()},
            "Query counts or explicit absences differ")

    def remap(query):
        return query.replace("entry-id:", "entry-id-cited-by-actual-comparison:", 1)

    jmdict = {
        "queries": {remap(q): ids for q, ids in queries.items()},
        "recordPredicates": {identity: [remap(q) for q in predicates]
                             for identity, predicates in membership.items()},
        "zeroMatches": [remap(q) for q, ids in queries.items() if not ids],
    }
    characters = sorted(COMPARISONS | set("\u885b\u971c"))
    kanjidic = {
        "queries": {"literal:" + char: [char] for char in characters},
        "recordPredicates": {char: ["literal:" + char] for char in characters},
        "zeroMatches": [],
    }
    require(set(receipt["outputs"]) == set(xml) == {
        "jmdict-families.xml", "kanjidic2-records.xml"}, "Unexpected source outputs")
    selected = {}
    for kind, name, tag, key, mapping in (
        ("jmdict", "jmdict-families.xml", "entry", "ent_seq", jmdict),
        ("kanjidic2", "kanjidic2-records.xml", "character", "literal", kanjidic),
    ):
        root = ET.fromstring(xml[name])
        require(root.tag == ("JMdict" if kind == "jmdict" else "kanjidic2")
                and all(child.tag == tag for child in root), "Invalid selected XML container")
        selected[kind] = selection(xml[name], mapping, tag, key, receipt["outputs"][name])
    require(set(selected["jmdict"]["expected"]) == set(membership)
            and len(membership) == receipt["completeFamilies"]
            and len(selected["kanjidic2"]["expected"]) == receipt["completeCharacterRecords"],
            "Selected record counts or membership differ")
    return selected


def main(runtime_path, output):
    runtime_path, output = Path(runtime_path).resolve(), Path(output).resolve()
    require(runtime_path.parent == output.parent == ROOT and not output.exists(),
            "Use frozen runtime proof and a new direct B131 review output")
    runtime_raw = frozen(runtime_path)
    runtime = json.loads(runtime_raw)
    candidate = runtime["candidate"]
    require(runtime["status"] == "PASS_RUNTIME_ONLY" and runtime["parent"] == PARENT
            and not runtime["reviewAccepted"] and not runtime["publicationAccepted"],
            "Runtime proof does not bind an unaccepted successor")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    guard, _ = start_guard("B131 complete reconciliation source verification")
    git = Git(REPO, RUNNER, guard)
    bindings = {}

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed successor checkout changed")

    def blob(path, revision=candidate):
        raw = git("show", f"{revision}:{path}")
        if revision == candidate:
            require((REPO / path).read_bytes() == raw, "Checkout differs from signed blob: " + path)
            if path in runtime["signedArtifacts"]:
                require(sha(raw) == runtime["signedArtifacts"][path], "Runtime proof binding differs")
            bindings[path] = sha(raw)
        return raw

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", candidate),
                "Successor identity or parent differs")
        snapshot_raw = blob("docs/n1-source-snapshot.json")
        require(snapshot_raw == blob("docs/n1-source-snapshot.json", PARENT),
                "Pinned source snapshot changed")
        snapshot = json.loads(snapshot_raw)
        receipt = json.loads(blob(PREFIX + "source-receipt.json"))
        membership = json.loads(blob(PREFIX + "query-membership.json"))
        producer = blob(PREFIX + "producers/r131_sources.py")
        comparisons = {}
        for char in sorted(COMPARISONS):
            raw = blob(PREFIX + f"comparison-cards/{char}.md")
            require(raw == blob(f"kanji/{char}.md", PARENT) == blob(f"kanji/{char}.md"),
                    "Comparison card differs from original and current snapshot")
            comparisons[char] = raw
            guard.check()
        xml = {name: blob(PREFIX + name) for name in
               ("jmdict-families.xml", "kanjidic2-records.xml")}
        selected = source_selections(receipt, membership, xml, producer, comparisons)
        results = {}
        for kind, (filename, compressed, decompressed, tag, key) in INPUTS.items():
            require(receipt["inputs"][kind] == [filename, compressed, decompressed, tag]
                    and snapshot["inputs"][filename]["sha256"] == compressed
                    and snapshot[kind]["xmlSha256"] == decompressed, "Pinned input binding differs")
            path = WS / "control" / "inputs" / filename
            with path.open("rb") as stream:
                reader = HashedReader(stream, guard)
                while reader.read(65536):
                    pass
            require(reader.digest.hexdigest() == compressed, "Compressed dictionary differs")
            with gzip.open(path, "rb") as stream:
                reader = HashedReader(stream, guard)
                verified = verify_stream(reader, tag, key, [selected[kind]], guard)[0]
                while reader.read(65536):
                    pass
            require(reader.digest.hexdigest() == decompressed, "Decompressed dictionary differs")
            results[kind] = verified
        for name, digest in receipt["originalSourceReuseBindings"].items():
            require(Path(name).name == name and sha(blob(ORIGINAL + name)) == digest
                    and blob(ORIGINAL + name) == blob(ORIGINAL + name, PARENT),
                    "Reused original source evidence changed")
        sums = json.loads(frozen(PACKET / "SHA256SUMS.json", PACKET_SHA))
        external = json.loads(blob(PREFIX + "external-source-bindings.json"))
        manifest_path = "evidence/external-snapshots/manifest.json"
        manifest_raw = frozen(PACKET / manifest_path, external["manifestSha256"])
        manifest = json.loads(manifest_raw)
        require(Path(external["frozenRoot"]) == PACKET
                and external["snapshots"] == [s for s in manifest["snapshots"] if s["index"] in (1, 5, 6)]
                and len(external["snapshots"]) == 3
                and external["extractionMethod"] == manifest["extractionMethod"],
                "External reuse selection differs")
        external_files = {}
        for item in external["snapshots"]:
            for field in ("response", "extract"):
                record = item[field]
                require(record["path"] in sums and sums[record["path"]] == record["sha256"],
                        "External capture is not in the accepted packet")
                external_files[record["path"]] = sha(frozen(PACKET / record["path"], record["sha256"]))
        require(sums[manifest_path] == sha(manifest_raw), "External manifest packet binding differs")
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source verification RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 131, "status": "PASS_COMPLETE_SOURCES_ONLY", "candidate": candidate,
        "parent": PARENT, "base": BASE, "runtimeProof": {
            "path": str(runtime_path), "sha256": sha(runtime_raw)},
        "results": results, "signedBindings": bindings, "externalFrozenFiles": external_files,
        "memory": memory, "helpers": HELPERS, "producerSha256": sha(frozen(Path(__file__))),
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Complete finite selections, explicit absences, exact comparison copies and "
                  "original external captures only. Mechanical seven-digit references can include "
                  "collateral identifiers; record availability is not lexical support. Pair claims, "
                  "gate evidence, isolated responses and both confirmations remain separate.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: verify_b131_revision_sources_001.py RUNTIME_PROOF NEW_OUTPUT")
    main(*sys.argv[1:])
