"""Verify B125's six exact source selections and reproduce its baseline scan."""
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_module, require, sha, start_guard
from confirm_v2 import clean

BASE = "419aafb53d6488f67817f325e0e63ad51651780a"
CANDIDATE = "483bb066e68faf354779f7d5fc73c4594605cdd7"
HERE = WS / "scratch-125" / "review"
PREFIX = "docs/n1-sources/batch-125/"
SUPPLEMENT = "docs/n1-sources/batch-125-supplement/"
FALLBACK = "docs/n1-sources/batch-125-fallback/"
MEMBER = "\u4fb5"
COMPARISONS = set("\u5192\u5bb3\u5bdd\u6383\u6483\u653b\u72af\u9032")
FALLBACKS = set("\u4eba\u4f11\u4f55\u5165\u51fa\u53e3\u5973\u65e5\u6708\u7537\u8cb7")
QUERIES = {"\u5192\u3059", "\u5bb3\u3059\u308b", "\u5bdd\u308b", "\u6383\u304f",
           "\u6483\u3064", "\u653b\u3081\u308b", "\u72af\u3059", "\u9032\u3080", "\u9032\u5165"}
VERIFIER_PATH = WS / "scratch-124" / "review" / "verify-source-records.py"
VERIFIER_SHA = "21842b6d2d6040d2deb4a9f8c6d15f2c28c17386a443da52780a7ef7cc169c62"


class HashedReader:
    def __init__(self, stream, guard):
        self.stream, self.guard = stream, guard
        self.digest = hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        data = self.stream.read(size)
        self.digest.update(data)
        return data


def words(values):
    return set(re.findall("[a-z]+", " ".join(values).lower()))


def scan_records(stream, titles, target_meanings, guard):
    target_words = words(target_meanings)
    seen, matches = set(), {}
    iterator = ET.iterparse(stream, events=("start", "end"))
    _, root = next(iterator)
    for event, node in iterator:
        if event != "end" or node.tag != "character":
            continue
        literal = node.findtext("literal")
        if literal in titles:
            require(literal not in seen, "Duplicate baseline dictionary character")
            seen.add(literal)
            meanings = [value.text or "" for value in node.findall("reading_meaning/rmgroup/meaning")
                        if value.get("m_lang") in (None, "en")]
            title_hits = sorted(target_words & words([titles[literal]]))
            meaning_hits = sorted(target_words & words(meanings))
            if title_hits or meaning_hits:
                matches[literal] = {
                    "title": titles[literal], "path": f"kanji/{literal}.md",
                    "kanjidicMeanings": meanings, "meaningHits": meaning_hits, "titleHits": title_hits,
                }
        node.clear()
        root.clear()
        guard.check()
    return {
        "targetGlossWords": sorted(target_words), "scannedCards": len(titles),
        "matches": matches, "missingRecords": sorted(set(titles) - seen),
    }


def main():
    output = HERE / "source-selection-verification-001.json"
    require(not output.exists(), "Preserve existing source verification")
    frozen(VERIFIER_PATH, VERIFIER_SHA)
    verifier = load_module("b125_pinned_source_verifier", VERIFIER_PATH)
    verifier.MEMBER = MEMBER
    config = {"repo": str(WS / "b125-worktree"), "candidate": CANDIDATE, "base": BASE}
    clean(config, CANDIDATE)
    blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
    snapshot_raw = blob("docs/n1-source-snapshot.json")
    require(snapshot_raw == git(config, "show", f"{BASE}:docs/n1-source-snapshot.json"),
            "Source definitions changed")
    snapshot = json.loads(snapshot_raw)
    specs = {
        "jmdict": [
            (PREFIX + "jmdict-selected-records.xml", "contains-member", {MEMBER}),
            (SUPPLEMENT + "jmdict-records.xml", "exact", QUERIES),
        ],
        "kanjidic2": [
            (PREFIX + "kanjidic2-selected-records.xml", "exact", {MEMBER}),
            (PREFIX + "kanjidic2-comparison-records.xml", "exact", set()),
            (SUPPLEMENT + "kanjidic2-records.xml", "exact", COMPARISONS),
            (FALLBACK + "kanjidic2-records.xml", "exact", FALLBACKS),
        ],
    }
    guard, _ = start_guard("B125 complete source and corpus-scan verification")
    results, input_results = [], {}
    try:
        for kind, (filename, compressed_sha, tag, key) in verifier.INPUTS.items():
            path = WS / "control" / "inputs" / filename
            with path.open("rb") as stream:
                reader = HashedReader(stream, guard)
                while reader.read(1024 * 1024):
                    pass
            require(reader.digest.hexdigest() == compressed_sha
                    == snapshot["inputs"][filename]["sha256"], f"Changed source: {kind}")
            selections = []
            for relative, mode, queries in specs[kind]:
                raw = blob(relative)
                selections.append({
                    "name": relative, "sha256": sha(raw), "mode": mode, "queries": queries,
                    "expected": verifier.records(raw, tag, key),
                })
            with gzip.open(path, "rb") as stream:
                reader = HashedReader(stream, guard)
                identities = verifier.verify_stream(reader, tag, key, selections, guard)
            require(reader.digest.hexdigest() == snapshot[kind]["xmlSha256"],
                    f"Decompressed source hash differs: {kind}")
            input_results[kind] = {
                "filename": filename, "compressedSha256": compressed_sha,
                "decompressedXmlSha256": reader.digest.hexdigest(),
            }
            for selection, matched in zip(selections, identities):
                results.append({
                    "path": selection["name"], "sha256": selection["sha256"],
                    "input": filename, "inputSha256": compressed_sha,
                    "mode": selection["mode"], "queries": sorted(selection["queries"]),
                    "completeMatchingRecords": len(matched), "identities": matched,
                })

        baseline = json.loads(git(config, "show", f"{BASE}:manifest.json"))
        titles = {}
        import sys
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        for name, digest in baseline["files"].items():
            if not name.startswith("kanji/"):
                continue
            raw = (Path(config["repo"]) / Path(name)).read_bytes().replace(b"\r\n", b"\n")
            require(sha(raw) == digest, f"Baseline card differs: {name}")
            metadata, _ = parse(raw.decode("utf-8"))
            require(metadata is not None, f"Baseline card lacks metadata: {name}")
            titles[Path(name).stem] = metadata["title"]
        row = json.loads(blob(PREFIX + "source-row.json"))
        with gzip.open(WS / "control" / "inputs" / verifier.INPUTS["kanjidic2"][0], "rb") as stream:
            scan = scan_records(stream, titles, row["metadata"]["meanings"], guard)
        original = json.loads(blob(PREFIX + "comparison-scan.json"))
        require(original["baseCommit"] == BASE and original["target"] == MEMBER
                and all(original[key] == value for key, value in scan.items()),
                "Recorded baseline gloss scan does not reproduce")
        require(scan["scannedCards"] == 1244 and not scan["missingRecords"],
                "Incomplete baseline gloss scan")
        clean(config, CANDIDATE)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source verification RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 125, "candidate": CANDIDATE, "base": BASE, "status": "PASS",
        "snapshotSha256": sha(snapshot_raw), "inputs": input_results,
        "sourceRecords": results, "reproducedScan": scan,
        "scanSha256": sha(blob(PREFIX + "comparison-scan.json")), "memory": memory,
        "verifierSha256": sha(Path(__file__).read_bytes()),
        "reusedVerifier": {"path": str(VERIFIER_PATH), "sha256": VERIFIER_SHA},
        "limits": "Complete pinned records and exact selectors, including empty gloss-word results. "
                  "Not an exhaustive synonym search, linguistic review or publication acceptance.",
    })))


if __name__ == "__main__":
    main()
