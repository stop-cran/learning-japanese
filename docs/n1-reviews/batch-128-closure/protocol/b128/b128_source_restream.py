"""Independently re-stream B128's complete dictionary records with keb and reb selectors."""
import gzip
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WS, freeze_json, git, require, sha, start_guard
from verify_b124_reconciliation import HashReader
from verify_reconciliation_sources import element_value

PREFIX = "docs/n1-sources/batch-128-reconciliation/"
READING = "ほとり"
READING_KEY = "reading=" + READING
RULE = ("Any exact k_ele/keb match, or r_ele/reb=ほとり; "
        "include entire matching family without sense filtering.")
LITERALS = list("刃声差房案横鋭響鳴危在郊騒叫咲唇")
INPUTS = {
    "jmdict": ("n1-implementation-JMdict_e.gz",
               "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
               "entry", "ent_seq", "jmdict-complete-records.xml"),
    "kanjidic2": ("n1-planning-kanjidic2.xml.gz",
                  "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed",
                  "character", "literal", "kanjidic2-complete-records.xml"),
}


def records(raw, tag, key):
    nodes = ET.fromstring(raw).findall(tag)
    values = {node.findtext(key): element_value(node) for node in nodes}
    require(len(values) == len(nodes) and None not in values and "" not in values,
            "Duplicate or missing dictionary identity")
    return values


def matches(node, kind, queries):
    if kind == "kanjidic2":
        literal = node.findtext("literal")
        return [literal] if literal in queries else []
    kebs = {item.text for item in node.findall("k_ele/keb") if item.text}
    rebs = {item.text for item in node.findall("r_ele/reb") if item.text}
    found = sorted(kebs & (queries - {READING_KEY}))
    return found + ([READING_KEY] if READING_KEY in queries and READING in rebs else [])


def stream_records(stream, kind, tag, key, queries, expected, guard):
    observed = {query: [] for query in queries}
    seen = set()
    parser = ET.iterparse(stream, events=("start", "end"))
    _, root = next(parser)
    for event, node in parser:
        if event != "end" or node.tag != tag:
            continue
        hits = matches(node, kind, queries)
        if hits:
            identity = node.findtext(key)
            require(identity not in seen, f"Duplicate identity in pinned dictionary: {identity}")
            require(identity in expected, f"Missing applicable family: {kind}/{identity}")
            require(element_value(node) == expected[identity],
                    f"Incomplete or altered record: {kind}/{identity}")
            seen.add(identity)
            for query in hits:
                observed[query].append(identity)
        node.clear()
        root.clear()
        guard.check()
    require(seen == set(expected), f"Unexpected extracted record: {kind}")
    return {query: sorted(ids) for query, ids in observed.items()}, sorted(seen)


def verify(blob, guard, inputs_dir=None, pinned=None):
    inputs_dir = Path(inputs_dir or WS / "control" / "inputs")
    pinned = pinned or INPUTS
    selector = json.loads(blob(PREFIX + "selector-membership.json"))
    declared = json.loads(blob(PREFIX + "source-verification-002.json"))
    snapshot = json.loads(blob("docs/n1-source-snapshot.json"))
    require(selector["selectorRule"] == RULE and selector["allMatchingFamiliesIncluded"] is True
            and selector["kanjidic2LiteralSelectors"] == LITERALS, "Selector contract differs")
    keb_or_reb = selector["exactKebOrRebQueries"]
    require(READING_KEY in keb_or_reb and all(keb_or_reb), "Reading selector or query missing")
    results = {}
    for kind, (filename, compressed_sha, tag, key, output) in pinned.items():
        raw = blob(PREFIX + output)
        expected = records(raw, tag, key)
        claim = declared[kind]
        require(sha(raw) == claim["extractedSha256"] and claim["completeRecords"] == len(expected)
                and sorted(expected) == claim["canonicalIdentities"]
                and claim["allSelectorsAndCanonicalRecordsMatchOriginal"] is True,
                f"Extracted records differ from declaration: {kind}")
        queries = set(keb_or_reb) if kind == "jmdict" else set(LITERALS)
        if kind == "jmdict":
            require(set(expected) == {i for ids in keb_or_reb.values() for i in ids},
                    "Extracted JMdict families differ from selector union")
        source = inputs_dir / filename
        with source.open("rb") as stream:
            reader = HashReader(stream, guard)
            while reader.read(1024 * 1024):
                pass
        require(reader.digest.hexdigest() == compressed_sha == claim["compressedSha256"]
                == snapshot["inputs"][filename]["sha256"], f"Compressed source differs: {kind}")
        with gzip.open(source, "rb") as stream:
            reader = HashReader(stream, guard)
            observed, identities = stream_records(reader, kind, tag, key, queries, expected, guard)
            while reader.read(1024 * 1024):
                pass
        decompressed = reader.digest.hexdigest()
        require(decompressed == claim["decompressedXmlSha256"] == snapshot[kind]["xmlSha256"],
                f"Decompressed source differs: {kind}")
        if kind == "jmdict":
            require(observed == {q: sorted(ids) for q, ids in keb_or_reb.items()},
                    "Exact keb/reb selector membership differs")
        else:
            require(all(observed[c] == [c] for c in LITERALS), "Character selector membership differs")
        results[kind] = {"identities": identities, "membership": observed, "outputSha256": sha(raw),
                         "compressedSha256": compressed_sha, "decompressedSha256": decompressed}
    return results


def main():
    require(len(sys.argv) == 4 and sys.argv[1] in {"--index", "--commit"},
            "Usage: b128_source_restream.py --index|--commit REV OUTPUT.json")
    mode, revision, output = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    require(not output.exists(), "Preserve existing re-stream evidence")
    config = {"repo": str(WS / "b128-worktree")}
    if mode == "--index":
        require(revision == "staged", "Index mode requires REV=staged")
        prefix = ":"
        head = git(config, "rev-parse", "HEAD").decode().strip()
    else:
        head = git(config, "rev-parse", f"{revision}^{{commit}}").decode().strip()
        require(head == revision, "Commit mode requires a full commit SHA")
        prefix = f"{revision}:"
    blob = lambda path: git(config, "show", prefix + path)
    guard, _ = start_guard("B128 complete dictionary re-stream")
    try:
        results = verify(blob, guard)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Re-stream RAM guard breached")
    print(json.dumps(freeze_json(output, {
        "batch": 128, "status": "PASS", "mode": mode, "revision": revision, "head": head,
        "rule": RULE, "results": results, "memory": memory,
        "toolSha256": sha(Path(__file__).read_bytes())})))


if __name__ == "__main__":
    main()
