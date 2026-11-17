"""Verify the signed reading repair, complete sources and unchanged four-pool model."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import (WS, freeze_json, frozen, git, load_batch, load_module, require, sha,
                    start_guard, verify_packet)
from confirm_v2 import clean
from finalize_b117_v3 import require_prior_sources
from verify_reconciliation_sources import element_value

PARENT = "5100ec3e8580ba03e6e6dcaa378cb92492f1d13f"
ROOT = "docs/n1-sources/batch-117/reconciliation-004"
POOLS = {"N1 stack", "All stack", "Starter+target", "Starter+target+由"}
CHOICES = ["銀", "語", "休"]
INPUTS = {
    "KANJIDIC2": ("n1-planning-kanjidic2.xml.gz",
                 "af0a499d62ac4413c614adcca360e2306490c3f64fccb3510fc7caa15f901bed",
                 "kanjidic2", "character", "literal", "completeRecords"),
    "JMdict": ("n1-implementation-JMdict_e.gz",
               "2dbbfe0b1214911766bbc128a0935618b925be917e7d1c50f3536a89b0e8786d",
               "jmdict", "entry", "ent_seq", "completeEntries"),
}


def require_focused(result):
    require(result["status"] == "PASS" and result["parent"] == PARENT
            and result["failedPools"] == [] and set(result["pools"]) == POOLS,
            "Focused check is incomplete or failed")
    old = result["parentPositiveControl"]
    require(old["yuiReachable"] and old["curatedCards"] == []
            and {str(k): v for k, v in old["deficits"].items()} == {"3": 1}
            and old["seededWitness"]["seed"] == 1
            and "ゆい" in old["seededWitness"]["wrongOptions"],
            "Parent positive control is missing")
    metadata = result["currentTargetMetadata"]
    require(metadata["distractors"] == CHOICES and metadata["onyomi"] == ["イ"]
            and metadata["kunyomi"] == [] and metadata["quizOnyomi"] == ["イ"]
            and metadata["quizKunyomi"] == [] and "ゆい" not in metadata["quiz_exclusions"],
            "Focused check changed the question or hid the attested reading")
    for name, row in result["pools"].items():
        require(row["curatedCards"] == CHOICES and row["outcomes"] == 1
                and {str(k): v for k, v in row["deficits"].items()} == {"0": 1}
                and set(row["reachable"]) == {"ぎん", "ご", "きゅう"} and not row["fallback"]
                and row["yuiReachable"] is False and row["seededWitness"] is None
                and row["seedRange"] == [0, 999] and row["seedsChecked"] == 1000
                and set(row["sampledWrongOptions"]) == {"ぎん", "ご", "きゅう"}
                and row["invalidSampleSeeds"] == [], f"Pool is not repaired: {name}")


def verify(candidate, gates, output):
    config = load_batch(117)
    clean(config, candidate)
    require(git(config, "rev-parse", f"{candidate}^").decode().strip() == PARENT,
            "Round-4 parent changed")
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    raw_index = blob(f"{ROOT}/source-evidence-index.json")
    index = json.loads(raw_index)
    receipt = json.loads(blob(f"{ROOT}/correction-receipt.json"))
    require(index["batch"] == receipt["batch"] == 117 and index["parent"] == receipt["parent"] == PARENT
            and receipt["sourceEvidence"]["indexSha256"] == sha(raw_index)
            and receipt["distractors"] == {"before": ["録", "催", "集"], "after": CHOICES},
            "Round-4 source/receipt binding differs")
    require((WS / receipt["validation"]["directory"]).resolve() == gates.resolve(),
            "Signed receipt names another gate directory")
    guard, _ = start_guard("B117 signed round-4 sources and focused regression")
    records = []
    try:
        packet, sums, _ = verify_packet(config, guard)
        source_root = "docs/n1-sources/batch-117"
        preserved = require_prior_sources(*[
            git(config, "ls-tree", "-r", "-z", rev, "--", source_root) for rev in (PARENT, candidate)])
        for source, (filename, digest, field, tag, key, count_field) in INPUTS.items():
            raw_path = WS / "control" / "inputs" / filename
            require(index["pinnedInputs"][source] == {"path": str(raw_path), "sha256": digest},
                    f"Unexpected pinned dictionary: {source}")
            hasher = hashlib.sha256()
            with raw_path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    hasher.update(chunk)
                    guard.check()
            require(hasher.hexdigest() == digest, f"Dictionary changed: {source}")
            extracted = blob(index[field]["path"])
            require(sha(extracted) == index[field]["sha256"], f"Extraction changed: {source}")
            entries = ET.fromstring(extracted).findall(tag)
            expected = {item.findtext(key): element_value(item) for item in entries}
            require(len(expected) == len(entries) == index[field][count_field],
                    f"Duplicate or missing extraction: {source}")
            if source == "KANJIDIC2":
                require(set(expected) == set(index[field]["characters"]) == set(CHOICES + ["維", "由"]),
                        "Character record membership differs")
            queries = index[field]["exactWrittenQueries"] if source == "JMdict" else {}
            actual_queries = {query: set() for query in queries}
            found = set()
            with gzip.open(raw_path, "rb") as stream:
                for _, element in ET.iterparse(stream, events=("end",)):
                    if element.tag != tag:
                        continue
                    identity = element.findtext(key)
                    if identity in expected:
                        require(identity not in found and element_value(element) == expected[identity],
                                f"Incomplete source record: {source}/{identity}")
                        found.add(identity)
                    for spelling in element.findall("k_ele/keb"):
                        if spelling.text in actual_queries:
                            actual_queries[spelling.text].add(identity)
                    element.clear()
                    guard.check()
            require(found == set(expected), f"Source records absent: {source}")
            if source == "JMdict":
                require(queries and all(actual_queries[q] == set(ids) for q, ids in queries.items())
                        and set(expected) == set().union(*actual_queries.values()),
                        "Incomplete exact-written dictionary families")
            records.append({"source": source, "inputSha256": digest, "extractionSha256": sha(extracted),
                            "completeRecordsVerified": len(found), "exactWrittenQueriesVerified": len(queries)})
        require(set(index["comparisonCards"]) == set(CHOICES), "Wrong comparison cards")
        for character, item in index["comparisonCards"].items():
            require(item["commit"] == PARENT and item["baselinePath"] == f"kanji/{character}.md",
                    "Wrong comparison identity")
            copied = blob(item["path"])
            require(copied == git(config, "show", f"{PARENT}:{item['baselinePath']}")
                    == blob(item["baselinePath"]) and sha(copied) == item["sha256"]
                    and len(copied) == item["bytes"], f"Comparison changed: {character}")
        require(len(index["characterSources"]) == 1 and index["characterSources"][0]["source"] == "維",
                "Wrong character source")
        for field in ("extract", "response"):
            item = index["characterSources"][0][field]
            path = Path(item["path"])
            require(sums[path.relative_to(packet).as_posix()] == item["sha256"]
                    and len(frozen(path, item["sha256"])) == item["bytes"], "Character source changed")
        require(set(index["models"]) == {"n1lib.py", "reading_options.py", "reading_exposure.py"},
                "Wrong model snapshots")
        for name, item in index["models"].items():
            live = Path(item["origin"]).read_bytes()
            require(item["origin"] == str(WS / "lean" / name)
                    and item["snapshot"] == f"{ROOT}/model-snapshots/{name}"
                    and blob(item["snapshot"]) == live and sha(live) == item["sha256"]
                    and len(blob(item["snapshot"])) == item["bytes"], f"Model changed: {name}")
        changed = git(config, "diff", "--name-only", "--no-renames", "-z", PARENT, candidate)
        runtime = {p for p in changed.decode().strip("\0").split("\0") if not p.startswith(ROOT + "/")}
        require(runtime == {"kanji/維.md", "manifest.json"}, "Unrelated runtime correction")
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        old = git(config, "show", f"{PARENT}:kanji/維.md").decode().replace("\r\n", "\n")
        current = blob("kanji/維.md").decode().replace("\r\n", "\n")
        old_fm, _ = parse(old)
        new_fm, _ = parse(current)
        require(new_fm == {**old_fm, "distractors": CHOICES}, "Unrelated frontmatter change")
        require(old.split("## Notes\n")[0].replace("distractors: [録, 催, 集]", "distractors: [銀, 語, 休]")
                == current.split("## Notes\n")[0], "Non-Notes prose changed")
        require(old.split("\nMetadata:")[1] == current.split("\nMetadata:")[1], "Source citation changed")
        check_path = WS / receipt["validation"]["focusedCheck"]["path"]
        check_sha = receipt["validation"]["focusedCheck"]["sha256"]
        check_copy = gates / check_path.name
        require(check_path.read_bytes() == frozen(check_copy, check_sha), "Live check differs from frozen copy")
        suite = json.loads(frozen(gates / "suite-summary.json"))
        author_raw = frozen(gates / "focused-check.json")
        require(suite["status"] == "PASS" and suite["parent"] == PARENT
                and suite["originalTenCommandsUnchanged"] is True and suite["focusedExitCode"] == 0
                and suite["focusedCheckSha256"] == check_sha
                and suite["focusedResultSha256"] == sha(author_raw)
                and suite["focusedLogSha256"] == sha(frozen(gates / "focused-check.log"))
                and suite["originalTenSummarySha256"] == sha(frozen(gates / "summary.json")),
                "Focused execution receipt changed")
        author = json.loads(author_raw)
        require_focused(author)
        require(not author["memory"]["breach"], "Author focused RAM check failed")
        check = load_module("b117_round4_focused_recheck", check_path)
        actual = json.loads(json.dumps(check.main(None)))
        require_focused(actual)
        require(actual == {k: v for k, v in author.items()
                           if k not in {"startedAt", "completedAt", "memory"}},
                "Independent focused regression differs from author's result")
        require(check_path.read_bytes() == frozen(check_copy, check_sha), "Live check changed during execution")
        for item in index["models"].values():
            require(sha(Path(item["origin"]).read_bytes()) == item["sha256"],
                    "Live model changed during execution")
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Round-4 source/model RAM check failed")
    result = {
        "batch": 117, "candidate": candidate, "parent": PARENT, "status": "PASS",
        "sourceEvidenceIndex": f"{ROOT}/source-evidence-index.json",
        "sourceEvidenceIndexSha256": sha(raw_index), "dictionaryRecords": records,
        "comparisonCardsVerified": 3, "characterSourcesVerified": 1,
        "modelSnapshotsVerified": {name: item["sha256"] for name, item in index["models"].items()},
        "priorSourceEvidencePreserved": True, "priorSourceEntriesPreserved": preserved,
        "scopeVerified": sorted(runtime), "focusedCheck": actual,
        "focusedTool": {"path": str(check_copy.resolve()), "sha256": check_sha},
        "focusedExecutionPath": str(check_path),
        "focusedAuthorResultSha256": sha(author_raw),
        "manifestSha256": sha(blob("manifest.json")), "targetSha256": sha(blob("kanji/維.md")),
        "memory": memory, "publicationAccepted": False,
        "tool": {"path": str(Path(__file__).resolve()), "sha256": sha(Path(__file__).read_bytes())},
        "limits": "Complete parsed sources and four-pool host model, not linguistic/native/publication approval.",
    }
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
