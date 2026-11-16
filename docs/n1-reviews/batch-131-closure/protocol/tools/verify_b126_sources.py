"""Verify B126's signed dictionary selections and both complete baseline scans."""
import gzip
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_module, require, sha, start_guard
from confirm_v2 import clean

BASE = "ea9e1e364da4f3421a05d2a9706e5dcf44f0d797"
MEMBER = "\u5098"
DISTRACTORS = ["\u91d1", "\u5168", "\u5408"]
KEYWORDS = {
    "umbrella", "umbrellas", "parasol", "parasols", "canopy", "awning",
    "shelter", "shade", "cover", "protection",
}
STOPWORDS = {"a", "an", "the", "of", "or", "and", "like", "something"}
EXPANSION = {"caps", "hats", "shapes", "covering", "covers", "sunshade"}
HERE = WS / "scratch-126" / "review"
PREFIX = "docs/n1-sources/batch-126/"
VERIFIER_PATH = WS / "scratch-124" / "review" / "verify-source-records.py"
VERIFIER_SHA = "21842b6d2d6040d2deb4a9f8c6d15f2c28c17386a443da52780a7ef7cc169c62"
FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"


class HashedReader:
    def __init__(self, stream, guard):
        self.stream, self.guard = stream, guard
        self.digest = hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        data = self.stream.read(size)
        self.digest.update(data)
        return data


def tokens(values):
    return set(re.findall("[a-z]+", " ".join(values).lower()))


def single_headword_glosses(raw):
    entries = [
        entry for entry in ET.fromstring(raw).findall("entry")
        if any(node.text == MEMBER for node in entry.findall("k_ele/keb"))
    ]
    require(entries, "No complete single-headword JMdict family")
    return ([entry.findtext("ent_seq") for entry in entries],
            [node.text or "" for entry in entries for node in entry.findall("sense/gloss")])


def scan_baseline(stream, cards, guard):
    meanings = {}
    iterator = ET.iterparse(stream, events=("start", "end"))
    _, root = next(iterator)
    for event, node in iterator:
        if event != "end" or node.tag != "character":
            continue
        literal = node.findtext("literal")
        if literal in cards:
            require(literal not in meanings, "Duplicate baseline dictionary character")
            meanings[literal] = [
                value.text or "" for value in node.findall("reading_meaning/rmgroup/meaning")
                if value.get("m_lang") in (None, "en")
            ]
        node.clear()
        root.clear()
        guard.check()
    require(set(meanings) == set(cards), "Missing baseline dictionary records")
    return [{**cards[char], "meanings": meanings[char]} for char in sorted(cards)]


def matched_rows(rows, keywords):
    return [
        {**row, "matchedWords": sorted(keywords & tokens([row["title"], *row["meanings"]]))}
        for row in rows
    ]


def verify_scans(original, expanded, rows, source_meanings, jm_raw, original_sha):
    first = matched_rows(rows, KEYWORDS)
    require(
        original["baseCommit"] == BASE and original["newKanji"] == MEMBER
        and original["newSourceMeanings"] == source_meanings
        and original["newTitle"] == "umbrella; parasol"
        and original["literalGlossTokens"] == sorted(tokens(source_meanings))
        and original["expandedSemanticKeywords"] == sorted(KEYWORDS)
        and original["caseFoldAndTokenPattern"] == "[a-z]+",
        "Original scan source or token policy differs",
    )
    identities, glosses = single_headword_glosses(jm_raw)
    expanded_tokens = (tokens(glosses) - STOPWORDS) | KEYWORDS | EXPANSION
    second = matched_rows(rows, expanded_tokens)
    require(
        expanded["baseCommit"] == BASE and expanded["newKanji"] == MEMBER
        and expanded["extends"] == {"file": "baseline-gloss-scan.json", "sha256": original_sha}
        and expanded["singleCharacterJmdictEntries"] == identities
        and expanded["allSingleCharacterJmdictGlosses"] == glosses
        and expanded["sourceMeanings"] == source_meanings
        and expanded["omittedFunctionTokens"] == sorted(STOPWORDS)
        and expanded["scanTokens"] == sorted(expanded_tokens),
        "Expanded scan source or token policy differs",
    )
    for recorded, actual in ((original, first), (expanded, second)):
        require(
            recorded["scannedBaselineCards"] == len(rows)
            and recorded["rows"] == actual
            and recorded["matches"] == [row["kanji"] for row in actual if row["matchedWords"]],
            "Recorded baseline scan does not reproduce",
        )
    return {"baselineCards": len(rows), "originalMatches": original["matches"],
            "expandedMatches": expanded["matches"], "expandedTokens": sorted(expanded_tokens)}


def main(candidate):
    require(re.fullmatch("[0-9a-f]{40}", candidate), "A full candidate SHA is required")
    output = HERE / "source-selection-verification-001.json"
    require(not output.exists(), "Preserve existing source verification")
    frozen(VERIFIER_PATH, VERIFIER_SHA)
    verifier = load_module("b126_pinned_source_verifier", VERIFIER_PATH)
    verifier.MEMBER = MEMBER
    config = {"repo": str(WS / "b126-worktree"), "candidate": candidate, "base": BASE}
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P|%GF", candidate).decode().strip()
            == BASE + "|" + FINGERPRINT, "Candidate parent or signer differs")
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    snapshot_raw = blob("docs/n1-source-snapshot.json")
    require(snapshot_raw == git(config, "show", f"{BASE}:docs/n1-source-snapshot.json"),
            "Pinned source definitions changed")
    snapshot = json.loads(snapshot_raw)
    index_raw = blob("docs/n1-sources/source-index.json")
    require(index_raw == git(config, "show", f"{BASE}:docs/n1-sources/source-index.json"),
            "Frozen source index changed")
    row = next(item for item in json.loads(index_raw) if item["kanji"] == MEMBER)
    require(row == json.loads(blob(PREFIX + "source-row.json"))
            and row["sourceRow"] == 70 and row["statusAtFreeze"] == "pending", "Wrong frozen member")
    scan_raw, expanded_raw = (blob(PREFIX + name) for name in
                              ("baseline-gloss-scan.json", "baseline-gloss-scan-002.json"))
    original, expanded = json.loads(scan_raw), json.loads(expanded_raw)
    specs = {
        "jmdict": [("jmdict-selected-records.xml", "contains-member", {MEMBER})],
        "kanjidic2": [
            ("kanjidic2-selected-records.xml", "exact", {MEMBER}),
            ("kanjidic2-comparison-records.xml", "exact", set(DISTRACTORS) | set(original["matches"])),
            ("kanjidic2-expanded-comparison-records.xml", "exact", set(expanded["matches"])),
        ],
    }
    guard, _ = start_guard("B126 complete sources and baseline scans")
    results, inputs = [], {}
    try:
        for kind, (filename, compressed_sha, tag, key) in verifier.INPUTS.items():
            path = WS / "control" / "inputs" / filename
            with path.open("rb") as stream:
                reader = HashedReader(stream, guard)
                while reader.read(1024 * 1024):
                    pass
            require(reader.digest.hexdigest() == compressed_sha == snapshot["inputs"][filename]["sha256"],
                    f"Changed compressed source: {kind}")
            selections = []
            for name, mode, queries in specs[kind]:
                raw = blob(PREFIX + name)
                selections.append({"name": PREFIX + name, "sha256": sha(raw), "mode": mode,
                                   "queries": queries, "expected": verifier.records(raw, tag, key)})
            with gzip.open(path, "rb") as stream:
                reader = HashedReader(stream, guard)
                identities = verifier.verify_stream(reader, tag, key, selections, guard)
            require(reader.digest.hexdigest() == snapshot[kind]["xmlSha256"],
                    f"Changed decompressed source: {kind}")
            inputs[kind] = {"filename": filename, "compressedSha256": compressed_sha,
                            "decompressedXmlSha256": reader.digest.hexdigest()}
            for selection, matched in zip(selections, identities):
                results.append({"path": selection["name"], "sha256": selection["sha256"],
                                "input": filename, "inputSha256": compressed_sha,
                                "mode": selection["mode"], "queries": sorted(selection["queries"]),
                                "completeMatchingRecords": len(matched), "identities": matched})

        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        baseline = json.loads(git(config, "show", f"{BASE}:manifest.json"))["files"]
        tree = git(config, "ls-tree", "-rz", BASE, "--", "kanji").decode("utf-8")
        cards = {}
        for entry in tree.split("\0"):
            if not entry:
                continue
            header, name = entry.split("\t", 1)
            mode, kind, identity = header.split(" ")
            require(mode == "100644" and kind == "blob" and name.endswith(".md"),
                    "Unexpected baseline kanji tree entry")
            raw = (Path(config["repo"]) / Path(name)).read_bytes()
            require(hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() == identity
                    and sha(raw.replace(b"\r\n", b"\n")) == baseline[name],
                    f"Baseline bytes differ from signed Git tree: {name}")
            metadata, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
            require(metadata is not None, f"Baseline metadata missing: {name}")
            char = Path(name).stem
            cards[char] = {"kanji": char, "path": name, "baselineRawSha256": sha(raw),
                           "title": metadata["title"]}
            guard.check()
        require(len(cards) == 1245 and MEMBER not in cards, "Baseline membership differs")
        with gzip.open(WS / "control" / "inputs" / verifier.INPUTS["kanjidic2"][0], "rb") as stream:
            reader = HashedReader(stream, guard)
            rows = scan_baseline(reader, cards, guard)
        require(reader.digest.hexdigest() == inputs["kanjidic2"]["decompressedXmlSha256"],
                "Baseline scan source changed")
        scan_proof = verify_scans(original, expanded, rows, row["metadata"]["meanings"],
                                  blob(PREFIX + "jmdict-selected-records.xml"), sha(scan_raw))
        comparison_cards = set(DISTRACTORS) | set(original["matches"]) | set(expanded["matches"])
        for char in comparison_cards:
            require(blob(PREFIX + f"comparison-cards/{char}.md")
                    == git(config, "show", f"{BASE}:kanji/{char}.md"), "Comparison card is not its base copy")
            guard.check()
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source verification RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 126, "candidate": candidate, "base": BASE, "status": "PASS",
        "snapshotSha256": sha(snapshot_raw), "inputs": inputs, "sourceRecords": results,
        "reproducedScans": scan_proof, "originalScanSha256": sha(scan_raw),
        "expandedScanSha256": sha(expanded_raw), "comparisonCards": sorted(comparison_cards),
        "memory": memory, "verifierSha256": sha(Path(__file__).read_bytes()),
        "reusedVerifier": {"path": str(VERIFIER_PATH), "sha256": VERIFIER_SHA},
        "limits": "Complete pinned records, selectors and actual baseline token scans. "
                  "Token matches are not synonym adjudication, exhaustive linguistic coverage, "
                  "reading-pool safety or publication/native/device acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: python -B verify_b126_sources.py CANDIDATE_SHA")
    main(sys.argv[1])
