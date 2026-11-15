"""Verify the signed third correction against its complete pinned source families."""
import gzip
import re
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard, verify_packet
from confirm_v2 import clean
from verify_reconciliation_sources import element_value

PARENT = "1c2fc20527c935306d241ad7bf8d68b27c12140a"
ROOT = "docs/n1-sources/batch-117/reconciliation-003"
INPUTS = {
    "KANJIDIC2": ("n1-planning-kanjidic2.xml.gz",
                 "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed",
                 "kanjidic2", "character", "literal", "completeRecords"),
    "JMdict": ("n1-implementation-JMdict_e.gz",
               "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
               "jmdict", "entry", "ent_seq", "completeEntries"),
}


def verify(candidate, output):
    config = load_batch(117)
    clean(config, candidate)
    require(git(config, "rev-parse", f"{candidate}^").decode().strip() == PARENT,
            "Correction has another parent")
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    index_raw = blob(f"{ROOT}/source-evidence-index.json")
    index = json.loads(index_raw)
    require(index["batch"] == 117 and index["parent"] == PARENT, "Index ancestry differs")
    correction = json.loads(blob(f"{ROOT}/correction-receipt.json"))
    require(correction["sourceEvidence"]["indexSha256"] == sha(index_raw), "Receipt index differs")
    require(correction["batch"] == 117 and correction["parent"] == PARENT, "Receipt ancestry differs")
    added = correction["addedGuards"]
    declined = correction["declinedComparisons"]
    sources_expected = set(added) | {pair.split("/")[0] for pair in declined}
    counterparts_expected = {c for values in added.values() for c in values} | {
        pair.split("/")[1] for pair in declined}
    card_citations = set()
    for record in index["comparisonCards"].values():
        card_citations |= set(re.findall(r"(?<!\d)\d{7}(?!\d)", blob(record["path"]).decode("utf-8")))
    guard, _ = start_guard("B117 round-3 signed sources")
    dictionaries = []
    try:
        packet, packet_sums, _ = verify_packet(config, guard)
        for path in git(config, "ls-tree", "-r", "--name-only", PARENT, "--",
                        "docs/n1-sources/batch-117").decode().splitlines():
            require(blob(path) == git(config, "show", f"{PARENT}:{path}"),
                    f"Previous source evidence changed: {path}")
            guard.check()
        for source, (filename, digest, field, tag, key, count_field) in INPUTS.items():
            raw_path = WS / "control" / "inputs" / filename
            require(index["pinnedInputs"][source] == {"path": str(raw_path), "sha256": digest},
                    f"Unexpected pinned input: {source}")
            computed = hashlib.sha256()
            with raw_path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    computed.update(chunk)
                    guard.check()
            require(computed.hexdigest() == digest, f"Pinned source changed: {source}")
            extracted = blob(index[field]["path"])
            require(sha(extracted) == index[field]["sha256"], f"Extraction hash differs: {source}")
            entries = ET.fromstring(extracted).findall(tag)
            expected = {item.findtext(key): element_value(item) for item in entries}
            require(len(expected) == len(entries) == index[field][count_field],
                    f"Duplicate or missing extracted records: {source}")
            if source == "KANJIDIC2":
                require(set(expected) == set(index[field]["characters"])
                        == set(index["comparisonCards"]) == counterparts_expected,
                        "Character membership differs")
            queries = index["jmdict"]["exactWrittenQueries"] if source == "JMdict" else {}
            actual_queries = {query: set() for query in queries}
            found = set()
            with gzip.open(raw_path, "rb") as stream:
                for _, element in ET.iterparse(stream, events=("end",)):
                    if element.tag != tag:
                        continue
                    identity = element.findtext(key)
                    if identity in expected:
                        require(identity not in found and element_value(element) == expected[identity],
                                f"Incomplete or altered record: {source}/{identity}")
                        found.add(identity)
                    if queries:
                        for spelling in element.findall("k_ele/keb"):
                            if spelling.text in actual_queries:
                                actual_queries[spelling.text].add(identity)
                    element.clear()
                    guard.check()
            require(found == set(expected), f"Source record absent: {source}")
            if queries:
                cited = set(index["jmdict"]["counterpartCardCitedIds"])
                require(cited == card_citations, "Counterpart-cited JMdict IDs differ from the cards")
                require(set(expected) == set(index["jmdict"]["entryIds"]), "JMdict entry list differs")
                require(all(actual_queries[q] == set(ids) for q, ids in queries.items())
                        and set(expected) == set().union(*actual_queries.values()) | cited,
                        "Incomplete exact-written JMdict family")
            dictionaries.append({"source": source, "inputSha256": digest,
                                 "extractionSha256": sha(extracted), "completeRecordsVerified": len(found),
                                 "exactWrittenQueriesVerified": len(queries)})
        for character, record in index["comparisonCards"].items():
            require(record["commit"] == PARENT and record["baselinePath"] == f"kanji/{character}.md",
                    f"Wrong counterpart identity: {character}")
            copied = blob(record["path"])
            require(copied == git(config, "show", f"{PARENT}:{record['baselinePath']}")
                    == blob(record["baselinePath"]) and sha(copied) == record["sha256"]
                    and len(copied) == record["bytes"], f"Counterpart differs: {character}")
            guard.check()
        for item in index["existingTargetSourceRecords"]:
            existing = blob(item["path"])
            require(existing == git(config, "show", f"{PARENT}:{item['path']}")
                    and sha(existing) == item["sha256"], f"Existing target record differs: {item['path']}")
        require({item["source"] for item in index["characterSources"]} == sources_expected
                and len(index["characterSources"]) == len(sources_expected),
                "Character-source coverage differs")
        for source in index["characterSources"]:
            for field in ("extract", "response"):
                item = source[field]
                path = Path(item["path"])
                relative = path.relative_to(packet).as_posix()
                require(packet_sums[relative] == item["sha256"]
                        and len(frozen(path, item["sha256"])) == item["bytes"],
                        f"Character source differs: {source['source']}/{field}")
        changed = git(config, "diff", "--name-only", "--no-renames", "-z", PARENT,
                      candidate).decode().strip("\0").split("\0")
        runtime = {path for path in changed if not path.startswith(ROOT + "/")}
        require(runtime == {f"kanji/{c}.md" for c in added} | {"manifest.json"},
                "Correction changes unrelated files")
        for character, guards in added.items():
            path = f"kanji/{character}.md"
            line = lambda rev: next(l for l in git(config, "show", f"{rev}:{path}").decode("utf-8")
                                    .splitlines() if l.startswith("quiz_exclusions:"))
            before, after = line(PARENT), line(candidate)
            require(after == before[:-1] + "".join(f", {g}" for g in guards) + "]",
                    f"Guard change is not an exact append: {character}")
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source verification RAM guard breached")
    result = {"batch": 117, "candidate": candidate, "parent": PARENT, "status": "PASS",
              "sourceEvidenceIndex": f"{ROOT}/source-evidence-index.json",
              "sourceEvidenceIndexSha256": sha(index_raw), "dictionaryRecords": dictionaries,
              "comparisonCardsVerified": len(index["comparisonCards"]),
              "characterSourcesVerified": len(index["characterSources"]),
              "existingTargetRecordsVerified": len(index["existingTargetSourceRecords"]),
              "counterpartCardCitedIdsVerified": sorted(card_citations),
              "guardAppendsVerified": added, "declinedComparisons": declined,
              "priorSourceEvidencePreserved": True, "scopeVerified": sorted(runtime),
              "memory": memory, "publicationAccepted": False,
              "tool": {"path": str(Path(__file__).resolve()), "sha256": sha(Path(__file__).read_bytes())},
              "limits": "Complete parsed source families and byte-exact comparison articles, not linguistic approval."}
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]))
