"""Bind complete dictionary extractions and comparison articles to a signed revision."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, git, load_batch, require, sha, start_guard
from confirm_v2 import clean


def element_value(element):
    return (element.tag, tuple(sorted(element.attrib.items())), (element.text or "").strip(),
            tuple((element_value(child), (child.tail or "").strip()) for child in element))


def verify(candidate, output):
    config = load_batch(117)
    clean(config, candidate)
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    index_raw = blob("docs/n1-sources/batch-117/reconciliation-001/source-evidence-index.json")
    index = json.loads(index_raw)
    require(index["baseline"] == config["base"]
            and index["reviewedCandidateParent"] == config["candidate"], "Source ancestry mismatch")
    known_inputs = {
        "KANJIDIC2": ("n1-planning-kanjidic2.xml.gz",
                     "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed",
                     "kanjidic2", "character", "literal", "completeRecords", "characters"),
        "JMdict": ("n1-implementation-JMdict_e.gz",
                   "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
                   "jmdict", "entry", "ent_seq", "completeEntries", "entryIds"),
    }
    guard, _ = start_guard("B117 signed source verification")
    records = []
    try:
        for source, (filename, digest, field, tag, key, count_field, keys_field) in known_inputs.items():
            raw_path = WS / "control" / "inputs" / filename
            require(index["pinnedInputs"][source]["sha256"] == digest
                    and Path(index["pinnedInputs"][source]["path"]) == raw_path,
                    f"Unexpected pinned input: {source}")
            computed = hashlib.sha256()
            with raw_path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    computed.update(chunk)
                    guard.check()
            require(computed.hexdigest() == digest, f"Changed raw source: {source}")
            extracted = blob(index[field]["path"])
            require(sha(extracted) == index[field]["sha256"], f"Changed extraction: {source}")
            entries = ET.fromstring(extracted).findall(tag)
            expected = {item.findtext(key): element_value(item) for item in entries}
            require(len(expected) == len(entries) == index[field][count_field]
                    and set(expected) == set(index[field][keys_field]),
                    f"Extraction membership mismatch: {source}")
            found = set()
            with gzip.open(raw_path, "rb") as stream:
                for event, item in ET.iterparse(stream, events=("end",)):
                    if item.tag != tag:
                        continue
                    identifier = item.findtext(key)
                    if identifier in expected:
                        require(identifier not in found and element_value(item) == expected[identifier],
                                f"Incomplete or altered {source} record: {identifier}")
                        found.add(identifier)
                    item.clear()
                    guard.check()
            require(found == set(expected), f"Missing source records: {source}")
            records.append({"source": source, "inputSha256": digest,
                            "extractionSha256": sha(extracted), "completeRecordsVerified": len(found)})
        for character, record in index["comparisonCards"].items():
            require(record["baselinePath"] == f"kanji/{character}.md",
                    f"Wrong comparison identity: {character}")
            copied = blob(record["path"])
            original = git(config, "show", f"{config['base']}:{record['baselinePath']}")
            require(copied == original and sha(copied) == record["sha256"]
                    and len(copied) == record["bytes"], f"Changed comparison article: {character}")
            guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Source verification RAM guard breached")
    result = {
        "batch": 117, "candidate": candidate, "status": "PASS",
        "sourceEvidenceIndexSha256": sha(index_raw), "dictionaryRecords": records,
        "comparisonCardsVerified": len(index["comparisonCards"]), "baseline": config["base"],
        "memory": memory, "publicationAccepted": False,
        "limits": "Complete parsed records verified against pinned dictionary inputs; comparison articles "
                  "are byte-exact baseline copies. This is provenance verification, not linguistic review.",
    }
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]))
