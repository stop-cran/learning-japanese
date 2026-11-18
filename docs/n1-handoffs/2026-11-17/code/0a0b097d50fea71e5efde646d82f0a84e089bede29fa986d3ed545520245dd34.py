"""Re-stream the three observed B129 correction selections against pinned dictionaries.

The observed selector maps are pinned, not accepted as a signed handoff. Full execution
requires the signed successor and does not establish linguistic or gate acceptance.
"""
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard
from verify_b126_sources import HashedReader
from verify_b129_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER
from verify_reconciliation_sources import element_value

PARENT = "7c662b37c647a9b300278abe2e3079fe57f09f83"
REPO = WS / "b129-worktree"
REVIEW = WS / "scratch-129" / "review"
PREFIX = "docs/n1-sources/batch-129-reconciliation/"
RUNNER = {
    "path": str(REVIEW / "guarded-test-v3.py"),
    "sha256": "9326cabd53fb1ac18417dcc1f39d4316af8f1b0a945bf7523a9e73a7044a6848",
}
PINS = {
    "jmdict-query-membership.json": "363baf203a3155142f849068f1298c3e7ab56226c6c77684d9afcfc99f10a268",
    "kanjidic2-query-membership.json": "d71095847817504a452c3e51a7439b57691ba5b580d41eac0624bf837c46d221",
    "supplement-query-membership.json": "d50691408c146a4fb38f973914e06a24b3e2c44a1dd67aca5ea3efa00db51ff1",
    "complete-source-receipt.json": "652ea75f87c132629cdf2b9837b38d728051f7061f8ac00b8f8f6e255ddae60d",
    "supplement-source-receipt.json": "c6bb63f948c68fd4aa43fff8ae04fe8ec328ad2f5eae61d27c1d28e5bcc8ef49",
}
HELPERS = {
    "verify_b126_sources.py": "6fc5f09b2c4ed04de40f9aec2502b2e560c3b577a836b1ae7f59f587e83b20e3",
    "verify_b129_sources.py": "9fb0aa1b179679638865582eed251f2c4fd4c9a84707f56099383808b18d0b33",
    "verify_reconciliation_sources.py": "761688d05d89807478c002e3022749cc6b1cbd9ab4cb18b0805b4c19761ce7e6",
}
INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz",
               "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
               "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4",
               "entry", "ent_seq"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz",
                  "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed",
                  "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8",
                  "character", "literal"),
}
SELECTORS = {
    "entry": {"exact-spelling", "exact-reading", "entry-id-cited-by-actual-comparison"},
    "character": {"literal"},
}


def selection(raw, membership, tag, key, declared=None):
    queries = membership["queries"]
    require(isinstance(queries, dict) and queries, "Empty selector map")
    for query, identities in queries.items():
        kind, separator, value = query.partition(":")
        require(separator and value and kind in SELECTORS[tag], f"Unsupported selector: {query}")
        require(isinstance(identities, list) and all(isinstance(i, str) and i for i in identities)
                and len(identities) == len(set(identities)), f"Invalid selector membership: {query}")
    nodes = ET.fromstring(raw).findall(tag)
    identities = [node.findtext(key) for node in nodes]
    require(all(identities) and len(identities) == len(set(identities)),
            "Duplicate or missing selected identity")
    expected = {identity: element_value(node) for identity, node in zip(identities, nodes)}
    if declared is not None:
        canonical = {
            identity: sha(ET.canonicalize(ET.tostring(node, encoding="unicode"),
                                          strip_text=True).encode("utf-8"))
            for identity, node in zip(identities, nodes)
        }
        require(declared["sha256"] == sha(raw) and declared["bytes"] == len(raw)
                and declared["canonicalRecordHashes"] == canonical,
                "Selected XML differs from its receipt")
    return {"queries": queries, "expected": expected, "membership": membership,
            "rawSha256": sha(raw)}


def hits(node, tag, key, queries):
    values = ({"literal": {node.findtext(key)}} if tag == "character" else {
        "exact-spelling": {n.text for n in node.findall("k_ele/keb")},
        "exact-reading": {n.text for n in node.findall("r_ele/reb")},
        "entry-id-cited-by-actual-comparison": {node.findtext(key)},
    })
    return [q for q in queries if q.split(":", 1)[1] in values[q.split(":", 1)[0]]]


def verify_stream(stream, tag, key, selections, guard):
    observed = [{q: [] for q in item["queries"]} for item in selections]
    seen = [set() for _ in selections]
    parser = ET.iterparse(stream, events=("start", "end"))
    _, root = next(parser)
    for event, node in parser:
        if event != "end" or node.tag != tag:
            continue
        identity = node.findtext(key)
        for item, found, identities in zip(selections, observed, seen):
            matched = hits(node, tag, key, item["queries"])
            if not matched:
                continue
            require(identity not in identities, "Duplicate identity in original dictionary")
            require(identity in item["expected"], f"Missing applicable family: {identity}")
            require(element_value(node) == item["expected"][identity],
                    f"Incomplete or altered record: {identity}")
            identities.add(identity)
            for query in matched:
                found[query].append(identity)
        node.clear()
        root.clear()
        guard.check()
    result = []
    for item, found, identities in zip(selections, observed, seen):
        require(identities == set(item["expected"]), "Unexpected extracted family")
        require(found == item["queries"], "Selector membership differs from original dictionary")
        inverse = {identity: [q for q, ids in found.items() if identity in ids]
                   for identity in sorted(identities)}
        require(inverse == item["membership"]["recordPredicates"],
                "Record-to-selector mapping differs")
        require([q for q, ids in found.items() if not ids] == item["membership"]["zeroMatches"],
                "Zero-match selectors differ")
        result.append({"identities": sorted(identities), "queries": found,
                       "zeroMatches": item["membership"]["zeroMatches"],
                       "outputSha256": item["rawSha256"]})
    return result


def verify(blob, guard):
    documents, bindings = {}, {}
    for name, digest in PINS.items():
        raw = blob(PREFIX + name)
        require(sha(raw) == digest, f"Observed source contract changed: {name}")
        documents[name], bindings[name] = json.loads(raw), digest
    receipt = documents["complete-source-receipt.json"]
    require(receipt["parent"] == PARENT, "Correction source receipt targets another parent")
    snapshot = json.loads(blob("docs/n1-source-snapshot.json"))
    results = {}
    for kind, (filename, compressed, decompressed, tag, key) in INPUTS.items():
        specs = [(receipt["sources"][kind], documents[f"{kind}-query-membership.json"])]
        if kind == "jmdict":
            specs.append((documents["supplement-source-receipt.json"],
                          documents["supplement-query-membership.json"]))
        selections, output_names = [], []
        for claim, membership in specs:
            source, output = claim["input"], claim["output"]
            require(Path(source["path"]) == WS / "control" / "inputs" / filename
                    and source["compressedSha256"] == compressed
                    and source["decompressedSha256"] == decompressed
                    and claim["completeCanonicalEquality"] is True,
                    f"Wrong source declaration: {kind}")
            name = output["path"]
            require(name in {f"{kind}-complete-records.xml", "jmdict-supplement-complete-records.xml"},
                    "Unexpected correction XML path")
            raw = blob(PREFIX + name)
            selections.append(selection(raw, membership, tag, key, output))
            output_names.append(name)
            bindings[name] = sha(raw)
        require(snapshot["inputs"][filename]["sha256"] == compressed
                and snapshot[kind]["xmlSha256"] == decompressed, "Frozen source snapshot differs")
        path = WS / "control" / "inputs" / filename
        with path.open("rb") as stream:
            reader = HashedReader(stream, guard)
            while reader.read(65536):
                pass
        require(reader.digest.hexdigest() == compressed, f"Compressed dictionary differs: {kind}")
        with gzip.open(path, "rb") as stream:
            reader = HashedReader(stream, guard)
            verified = verify_stream(reader, tag, key, selections, guard)
            while reader.read(65536):
                pass
        require(reader.digest.hexdigest() == decompressed, f"Decompressed dictionary differs: {kind}")
        results[kind] = {"compressedSha256": compressed, "decompressedSha256": decompressed,
                         "selections": dict(zip(output_names, verified))}
    return results, bindings


def main(candidate, output):
    require(re.fullmatch(r"[0-9a-f]{40}", candidate), "Full successor commit SHA required")
    output = Path(output).resolve()
    require(output.parent == REVIEW and not output.exists(), "Use a new B129 review proof path")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    guard, _ = start_guard("B129 correction complete source verification")
    git = Git(REPO, RUNNER, guard)

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == candidate
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed successor checkout changed")

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN, "Wrong origin")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", candidate).decode().strip()
                == f"{PARENT}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Wrong successor signature/identity")
        require(TRAILER in git("show", "-s", "--format=%B", candidate), "Missing trailer")

        def blob(path):
            raw = git("show", f"{candidate}:{path}")
            require((REPO / path).read_bytes() == raw, f"Worktree differs from signed blob: {path}")
            return raw

        require(blob("docs/n1-source-snapshot.json")
                == git("show", f"{PARENT}:docs/n1-source-snapshot.json"), "Source snapshot changed")
        results, bindings = verify(blob, guard)
        clean()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source verification RAM guard breached")
    print(json.dumps(freeze_json(output, {
        "batch": 129, "status": "PASS_COMPLETE_SOURCES_ONLY", "candidate": candidate,
        "parent": PARENT, "results": results, "signedBindings": bindings, "memory": memory,
        "producerSha256": sha(frozen(Path(__file__))),
        "helpers": HELPERS, "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Exact complete dictionary records and declared selectors only. Pair semantics, "
                  "external captures, preservation, gate execution and confirmations remain required.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: verify_b129_revision_sources.py CANDIDATE NEW_OUTPUT")
    main(*sys.argv[1:])
