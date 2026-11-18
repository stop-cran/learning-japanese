"""Verify B130's observed reconciliation selections against complete dictionaries.

The CLI accepts only a clean owner-signed successor. The same source verifier can
check immutable observed copies during preparation, without candidate acceptance.
"""
import ast
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from prepare_b129_source_facts import literal_assignment
from verify_b126_sources import HashedReader
from verify_b129_revision_sources import INPUTS, selection, verify_stream
from verify_b130_payload import BASE, MEMBERS, REPO, RUNNER
from verify_b130_revision_runtime_v2 import PARENT, PREFIX, ROOT
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

OBSERVATION = ROOT / "revision-source-observation-001"
OBSERVATION_SHA = "08dc273b1d3764ebd4f016e20eb9d41e6ad8c0c05fe3b989670cea9bdcf93060"
NAMES = ("source-receipt.json", "query-membership.json", "jmdict-families.xml",
         "kanjidic2-records.xml", "reconcile_sources_b130.py")
HELPERS = {
    "verify_b129_revision_sources.py": "0a0b097d50fea71e5efde646d82f0a84e089bede29fa986d3ed545520245dd34",
    "verify_reconciliation_sources.py": "761688d05d89807478c002e3022749cc6b1cbd9ab4cb18b0805b4c19761ce7e6",
    "verify_b126_sources.py": "6fc5f09b2c4ed04de40f9aec2502b2e560c3b577a836b1ae7f59f587e83b20e3",
    "prepare_b129_source_facts.py": "a1f850826848325b2566c859353f424c8476fb6de05225cd1a79476722a989ea",
    "verify_b130_sources.py": "222518f71e16878a49dbff51ecaa94ee2d9f6f471b8d9a5fa4fb9bd4b6d0a22b",
    "verify_b130_payload.py": "f5d3791ae3b1ae301617ee90ab3625cb60aab9631724441200df22cca8ee2551",
    "verify_b130_revision_runtime_v2.py": "b10c35de0cf0b96c681ac138ba270d962a9a00d5ae42314dfc3f46b91d8827be",
}


def recover_selectors(producer):
    comparisons = literal_assignment(producer, "COMPARISONS")
    require(isinstance(comparisons, str) and len(comparisons) == len(set(comparisons)),
            "Comparison literals differ")
    nodes = [node.value for node in ast.parse(producer).body if isinstance(node, ast.Assign)
             and any(isinstance(target, ast.Name) and target.id == "EXACT" for target in node.targets)]
    expected_left = ast.parse("set(COMPARISONS)", mode="eval").body
    require(len(nodes) == 1 and isinstance(nodes[0], ast.BinOp)
            and isinstance(nodes[0].op, ast.BitOr)
            and ast.dump(nodes[0].left) == ast.dump(expected_left),
            "Re-inspect the changed exact-spelling producer")
    extra = ast.literal_eval(nodes[0].right)
    require(isinstance(extra, set) and all(isinstance(value, str) and value for value in extra),
            "Invalid extra exact-spelling selectors")
    return sorted(set(comparisons) | extra), sorted(set(comparisons) | set(MEMBERS))


def selections(receipt, membership, xml, producer):
    spellings, characters = recover_selectors(producer)
    selectors = receipt["selectors"]
    require(receipt["parent"] == PARENT and receipt["publishedBase"] == BASE
            and selectors["exactSpellings"] == spellings
            and selectors["characterLiterals"] == characters
            and set(receipt["outputs"]) == {"jmdict-families.xml", "kanjidic2-records.xml"}
            and receipt["producerSha256"] == sha(producer),
            "Source receipt does not describe the executed selection")
    queries = {"exact-spelling:" + value: [] for value in spellings}
    for identity, predicates in membership.items():
        require(isinstance(identity, str) and identity and isinstance(predicates, list)
                and predicates and predicates == sorted(set(predicates))
                and set(predicates) <= set(queries), "Invalid per-family predicate inventory")
        for predicate in predicates:
            queries[predicate].append(identity)
    require(selectors["queryCountsIncludingZero"] == {q: len(ids) for q, ids in queries.items()},
            "Exact query counts or zero matches differ")
    jmdict = {"queries": queries, "recordPredicates": membership,
              "zeroMatches": [q for q, ids in queries.items() if not ids]}
    kanjidic = {
        "queries": {"literal:" + char: [char] for char in characters},
        "recordPredicates": {char: ["literal:" + char] for char in characters},
        "zeroMatches": [],
    }
    result = {}
    for kind, name, tag, key, mapping in (
        ("jmdict", "jmdict-families.xml", "entry", "ent_seq", jmdict),
        ("kanjidic2", "kanjidic2-records.xml", "character", "literal", kanjidic),
    ):
        parsed = ET.fromstring(xml[name])
        require(parsed.tag == ("JMdict" if kind == "jmdict" else "kanjidic2")
                and all(child.tag == tag for child in parsed),
                "Unexpected extracted XML container or record")
        claim = receipt["outputs"][name]
        require(claim["source"] == kind and claim["completeCanonicalEquality"] is True,
                "Missing complete-source declaration")
        result[kind] = selection(xml[name], mapping, tag, key, claim)
    require(set(result["jmdict"]["expected"]) == set(membership),
            "Per-family membership and selected XML differ")
    return result


def verify(source, guard):
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    observation = json.loads(frozen(OBSERVATION / "observation.json", OBSERVATION_SHA))
    documents = {}
    for name in NAMES:
        expected = observation["files"][name]["sha256"]
        frozen(OBSERVATION / name, expected)
        documents[name] = source(name)
        require(sha(documents[name]) == expected,
                "Observed source contract changed; inspect a successor: " + name)
    receipt = json.loads(documents["source-receipt.json"])
    membership = json.loads(documents["query-membership.json"])
    require(sha(documents["query-membership.json"]) == receipt["membershipSha256"],
            "Membership receipt differs")
    selected = selections(receipt, membership, documents, documents["reconcile_sources_b130.py"])
    results = {}
    for kind, (filename, compressed, decompressed, tag, key) in INPUTS.items():
        declared = receipt["inputs"][kind]
        require(declared["filename"] == filename and declared["compressedSha256"] == compressed
                and declared["decompressedSha256"] == decompressed,
                "Wrong pinned dictionary input")
        path = WS / "control" / "inputs" / filename
        with path.open("rb") as stream:
            reader = HashedReader(stream, guard)
            while reader.read(65536):
                pass
        require(reader.digest.hexdigest() == compressed, "Compressed dictionary differs: " + kind)
        with gzip.open(path, "rb") as stream:
            reader = HashedReader(stream, guard)
            verified = verify_stream(reader, tag, key, [selected[kind]], guard)[0]
            while reader.read(65536):
                pass
        require(reader.digest.hexdigest() == decompressed, "Complete dictionary differs: " + kind)
        results[kind] = {"compressedSha256": compressed, "decompressedSha256": decompressed,
                         **verified}
    return results, {name: sha(raw) for name, raw in documents.items()}


def main(candidate, producer_relative, output):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate) and candidate != PARENT,
            "Full signed successor SHA required")
    require(producer_relative.startswith(PREFIX) and producer_relative.endswith(".py")
            and "\\" not in producer_relative
            and all(part not in ("", ".", "..") for part in producer_relative.split("/")),
            "Use the actual repository-relative signed reconciliation producer")
    output = Path(output).resolve()
    require(output.parent == ROOT and not output.exists(), "Use a new B130 review proof path")
    guard, _ = start_guard("B130 reconciliation complete source verification")
    git = Git(REPO, RUNNER, guard)

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed successor checkout changed")

    def blob(path, revision=candidate):
        raw = git("show", f"{revision}:{path}")
        if revision == candidate:
            require((REPO / path).read_bytes() == raw, "Worktree differs from signed blob: " + path)
        return raw

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", candidate),
                "Wrong signature, parent, owner or trailer")
        snapshot_raw = blob("docs/n1-source-snapshot.json")
        require(snapshot_raw == blob("docs/n1-source-snapshot.json", PARENT),
                "Pinned source snapshot changed")
        snapshot = json.loads(snapshot_raw)
        for kind, (filename, compressed, decompressed, _, _) in INPUTS.items():
            require(snapshot["inputs"][filename]["sha256"] == compressed
                    and snapshot[kind]["xmlSha256"] == decompressed, "Source snapshot differs")
        path_for = lambda name: producer_relative if name == "reconcile_sources_b130.py" else PREFIX + name
        results, bindings = verify(lambda name: blob(path_for(name)), guard)
        receipt = json.loads(blob(PREFIX + "source-receipt.json"))
        for character, item in receipt["comparisonCards"].items():
            require(len(character) == 1 and item["path"] == f"comparison-cards/{character}.md",
                    "Invalid comparison path")
            raw = blob(PREFIX + item["path"])
            require(sha(raw) == item["sha256"]
                    and raw == blob(f"kanji/{character}.md", PARENT)
                    and raw == blob(f"kanji/{character}.md"), "Comparison copy changed")
            bindings[item["path"]] = sha(raw)
            guard.check()
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Reconciliation source RAM guard breached")
    print(json.dumps(freeze_json(output, {
        "batch": 130, "status": "PASS_COMPLETE_SOURCES_ONLY", "candidate": candidate,
        "parent": PARENT, "base": BASE, "results": results, "signedBindings": bindings,
        "signedProducer": producer_relative, "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))), "helpers": HELPERS,
        "observedContractSha256": OBSERVATION_SHA,
        "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Complete source records, exact/zero selectors and comparison bytes only. "
                  "Semantic dispositions, external captures, author gates and final confirmations "
                  "still require separate verification. This proof does not close any question.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: verify_b130_revision_sources.py SHA SIGNED_PRODUCER NEW_OUTPUT")
    main(*sys.argv[1:])
