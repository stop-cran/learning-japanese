"""Bind the actual signed B124 correction, exact source selections and both gate runs."""
import gzip
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, load_module, require, sha, start_guard
from confirm_v2 import clean
from verify_b123_revision_v2 import SIGNER, runtime

REVIEW = WS / "scratch-124" / "review"
CANDIDATE = "fa394d237e28df96319495a003718cc9c880a069"
CARD, WORD, STROKES = "kanji/裕.md", "words/余裕.md", "strokes/裕.json"
PREFIX = "docs/n1-sources/batch-124-reconciliation/"
PROGRESS = "docs/n1-sources/batch-124-progress-003.json"
COMPARISONS = set("福多栄資宝貨余剰冗満悠楽金充足濃広")
EXTRA_DOCS = {PROGRESS, "docs/n1-sources/batch-124/selection-004.json",
              "docs/n1-sources/batch-124/author-audit-003.json"}
RUNNER_SHA = "1c6878b4830f8301cdfd1fd9382c4a8117692f085f9abe2e208f92a069e08612"
SOURCE_TOOL_SHA = "21842b6d2d6040d2deb4a9f8c6d15f2c28c17386a443da52780a7ef7cc169c62"
CONTRACT_TOOL_SHA = "1c626c4f2e49d5761d53926c70b5891ea00b63fc7a06383aeb7d5a076772a270"
XML_HASHES = {
    "jmdict": "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4",
    "kanjidic2": "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8",
}


def check_metadata(original, revised):
    require({k: v for k, v in original.items() if k != "quiz_exclusions"}
            == {k: v for k, v in revised.items() if k != "quiz_exclusions"},
            "Preserved metadata changed")
    old, new = original["quiz_exclusions"], revised["quiz_exclusions"]
    require(new[:len(old)] == old and len(new) == len(set(new))
            and set(new) - set(old) == set("多楽広"), "Required or original guards differ")


def check_summary(summary, config, mode, manifest_sha):
    require(summary["batch"] == "124" and summary["reconciliation"] == 1
            and summary["status"] == "PASS" and summary["mode"] == mode
            and summary["publishedBase"] == config["base"]
            and summary["reconciliationParent"] == config["candidate"]
            and summary["startingHead"] == (CANDIDATE if mode == "committed" else config["candidate"])
            and len(summary["checks"]) == len(CHECKS) and set(summary["checks"]) == set(CHECKS)
            and summary["manifestSha256"] == manifest_sha and summary["runnerSha256"] == RUNNER_SHA,
            "Gate summary belongs to another mode, revision or manifest")


def check_query_index(metadata, raw, queries):
    entries = ET.fromstring(raw).findall("entry")
    by_id = {entry.findtext("ent_seq"): sorted(
        {node.text for node in entry.findall("k_ele/keb")} & queries) for entry in entries}
    index = {query: sorted(identity for identity, matched in by_id.items() if query in matched)
             for query in queries}
    require(metadata["recordSelectors"] == by_id
            and metadata["matchedEntryIdsByQuery"] == index
            and metadata["unmatchedExactQueries"] == sorted(q for q, ids in index.items() if not ids),
            "Declared exact-query membership differs")


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard = stream, guard
        self.digest = hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        raw = self.stream.read(size)
        self.digest.update(raw)
        return raw


def verify():
    config = load_batch(124)
    clean(config, CANDIDATE)
    require(git(config, "show", "-s", "--format=%P", CANDIDATE).decode().strip() == config["candidate"],
            "Correction is not a direct child of the initial candidate")
    require(git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
            == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Owner signature differs")
    require(b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
            in git(config, "show", "-s", "--format=%B", CANDIDATE), "Co-author trailer missing")
    frozen(REVIEW / "verify-source-records.py", SOURCE_TOOL_SHA)
    frozen(REVIEW / "prepare-source-contract.py", CONTRACT_TOOL_SHA)
    source_tool = load_module("b124_complete_source_selection", REVIEW / "verify-source-records.py")
    contract = load_module("b124_initial_contract", REVIEW / "prepare-source-contract.py")
    from n1lib import parse

    blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
    previous = lambda path: git(config, "show", f"{config['candidate']}:{path}")
    handoff_raw = frozen(WS / "scratch-124" / "reconciliation-001-handoff.json")
    handoff = json.loads(handoff_raw)
    require(handoff["commit"]["sha"] == CANDIDATE and handoff["commit"]["parent"] == config["candidate"],
            "Author handoff is for another revision")
    guard, _ = start_guard("B124 signed correction verification")
    try:
        changes = [line.split("\t") for line in git(
            config, "diff", "--name-status", "--no-renames", config["candidate"], CANDIDATE
        ).decode("utf-8").splitlines()]
        require(len(changes) == handoff["fileInventory"]["count"] == 30
                and sorted(path for _, path in changes) == sorted(handoff["fileInventory"]["commitPaths"]),
                "Signed file inventory differs")
        for status, path in changes:
            require((status == "M" and path in (CARD, "manifest.json"))
                    or (status == "A" and (path.startswith(PREFIX) or path in EXTRA_DOCS)),
                    f"Unexpected or non-additive delta: {status} {path}")
        manifest_raw = blob("manifest.json")
        manifest_sha = sha(manifest_raw)
        manifest = json.loads(manifest_raw)
        current, initial = runtime(manifest), runtime(json.loads(previous("manifest.json")))
        baseline = runtime(json.loads(git(config, "show", f"{config['base']}:manifest.json")))
        require(current.keys() == initial.keys() and len(current) == 8710
                and {path for path in initial if current[path] != initial[path]} == {CARD},
                "Unrelated runtime manifest change")
        require(set(current) - set(baseline) == {CARD, STROKES} and set(baseline) <= set(current)
                and {path for path in baseline if baseline[path] != current[path]} == {WORD},
                "Published runtime baseline differs")
        for path in (WORD, STROKES):
            require(blob(path) == previous(path), f"Preserved runtime bytes changed: {path}")
        for path in (CARD, WORD, STROKES):
            require(sha(blob(path).replace(b"\r\n", b"\n")) == current[path], "Runtime hash differs")
        original, _ = parse(previous(CARD).decode("utf-8").replace("\r\n", "\n"))
        revised, _ = parse(blob(CARD).decode("utf-8").replace("\r\n", "\n"))
        check_metadata(original, revised)
        require("omits のり and ゆ" in blob(CARD).decode("utf-8"), "Name-list correction missing")
        receipt_raw = blob(PREFIX + "source-receipt.json")
        require(sha(receipt_raw) == handoff["sourceEvidence"]["sourceReceiptSha256"], "Source receipt differs")
        receipt = json.loads(receipt_raw)
        selection_raw = blob(PREFIX + "selection.json")
        selection = json.loads(selection_raw)
        require(sha(selection_raw) == receipt["selectionSha256"]
                and selection["candidateParent"] == receipt["candidateParent"] == config["candidate"]
                and selection["publishedBase"] == receipt["publishedBase"] == config["base"]
                and selection["membership"] == [{"kanji": "裕", "sourceRow": 986}]
                and selection["requiredReciprocalPairs"] == [["余裕", "裕"]]
                and set(selection["comparisonCards"]) == COMPARISONS,
                "Source selection scope differs")
        for name, item in receipt["files"].items():
            raw = blob(PREFIX + name)
            require(sha(raw) == item["sha256"] and len(raw) == item["bytes"], f"Source artifact differs: {name}")
        for character, digest in receipt["comparisonCardSha256AtParent"].items():
            path = f"kanji/{character}.md"
            require(blob(PREFIX + f"comparison-cards/{character}.md") == blob(path) == previous(path)
                    and sha(blob(path)) == digest, f"Comparison card changed: {character}")
        require(set(receipt["comparisonCardSha256AtParent"]) == COMPARISONS, "Comparison inventory differs")
        for item in receipt["immutableInputs"].values():
            frozen(item["path"], item["sha256"])
        sources = []
        for kind, (filename, compressed_sha, tag, key) in source_tool.INPUTS.items():
            metadata = receipt["dictionaryInputs"][kind]
            raw = blob(PREFIX + f"{kind}-records.xml")
            expected = source_tool.records(raw, tag, key)
            require(sha(raw) == metadata["extractedSha256"] and len(raw) == metadata["extractedBytes"]
                    and len(expected) == metadata["recordCount"]
                    and sorted(expected) == sorted(metadata["completeRecordIdentities"]),
                    f"Extracted {kind} record inventory differs")
            queries = set(metadata["exactWrittenFormQueries"]) if kind == "jmdict" else {"裕", *COMPARISONS}
            if kind == "jmdict":
                require(queries == {q for values in selection["exactJmdictQueriesByClaim"].values() for q in values},
                        "Claim selector union differs")
                check_query_index(metadata, raw, queries)
            else:
                require(set(metadata["recordSelectors"]["characters"]) == queries, "Character selectors differ")
            source = WS / "control" / "inputs" / filename
            require(str(source) == metadata["sourcePath"]
                    and metadata["compressedSha256"] == compressed_sha
                    and metadata["decompressedXmlSha256"] == XML_HASHES[kind], "Dictionary pin differs")
            digest = hashlib.sha256()
            with source.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
                    guard.check()
            require(digest.hexdigest() == compressed_sha, "Compressed dictionary changed")
            with gzip.open(source, "rb") as stream:
                reader = HashReader(stream, guard)
                found = source_tool.verify_stream(reader, tag, key, [
                    {"name": kind, "mode": "exact", "queries": queries, "expected": expected}
                ], guard)[0]
                while reader.read(1024 * 1024):
                    pass
            require(reader.digest.hexdigest() == XML_HASHES[kind], "Decompressed dictionary changed")
            sources.append({"kind": kind, "queries": sorted(queries), "identities": found,
                            "completeRecords": len(found), "extractedSha256": sha(raw),
                            "compressedSha256": compressed_sha, "decompressedSha256": XML_HASHES[kind]})
        runner = WS / "scratch-124" / "run-reconciliation-checks.py"
        frozen(runner, RUNNER_SHA)
        gate_sets = {}
        for mode in ("author", "committed"):
            declared = handoff["gates"][mode]
            directory = Path(declared["directory"])
            require(directory.parent == WS / "scratch-124", "Gates outside this batch")
            summary_raw = frozen(directory / "summary.json", declared["summarySha256"])
            check_summary(json.loads(summary_raw), config, mode, manifest_sha)
            for item in declared["gates"]:
                frozen(item["receiptPath"], item["receiptSha256"])
                frozen(item["logPath"], item["logSha256"])
            verified = contract.gate_bindings(directory, config, manifest_sha, RUNNER_SHA, guard)
            require(verified == [{k: item[k] for k in ("gate", "receiptSha256", "logSha256")}
                                 for name in CHECKS for item in declared["gates"] if item["gate"] == name],
                    "Handoff gate receipts differ")
            require(b"Ran 431 tests" in frozen(directory / "unittest.log"), "Expected unit run missing")
            gate_sets[mode] = {"directory": str(directory), "summarySha256": sha(summary_raw), "gates": verified}
        for item in handoff["preservedHistory"]["verifiedUnchangedFromParent"]:
            require(blob(item["path"]) == previous(item["path"])
                    and sha(blob(item["path"])) == item["sha256"], "Historical evidence changed")
        progress_raw = blob(PROGRESS)
        progress = json.loads(progress_raw)
        require(sha(progress_raw) == handoff["progress"]["sha256"]
                and not progress["runtimePublished"] and progress["published"] == progress["reviewClosed"] == []
                and progress["accounting"]["publishedPendingRecordsWithCards"] == 253
                and progress["accounting"]["undelivered"] == 975
                and progress["accounting"]["overallN1TaskComplete"] is False
                and progress["runtimeCandidate"]["manifestSha256"] == manifest_sha == handoff["manifest"]["sha256"],
                "Unpublished accounting or manifest binding differs")
        pending = {row["kanji"] for row in json.loads(blob("docs/n1-sources/source-index.json"))
                   if row["statusAtFreeze"] == "pending"}
        count = lambda entries: len(pending & {Path(p).stem for p in entries if p.startswith("kanji/")})
        require(len(pending) == 1228 and count(baseline) == 253 and count(current) == 254, "Frozen progress differs")
        clean(config, CANDIDATE)
        result = {"batch": 124, "status": "PASS", "candidate": CANDIDATE, "initial": config["candidate"],
                  "base": config["base"], "handoffSha256": sha(handoff_raw), "manifestSha256": manifest_sha,
                  "contentVersion": manifest["contentVersion"], "runtimeEntries": len(current),
                  "changedPaths": changes, "sourceReceiptSha256": sha(receipt_raw), "sourceRecords": sources,
                  "signedArtifacts": {path: sha(blob(path)) for _, path in changes if path.startswith("docs/")},
                  "runner": {"path": str(runner), "sha256": RUNNER_SHA}, "gateSets": gate_sets,
                  "metadataStrokesSupportAndHistoricalEvidencePreserved": True,
                  "sourceMembersPublishedBeforeBatch": 253, "sourceMembersInCandidate": 254,
                  "signature": {"fingerprint": SIGNER, "ownerVerified": True}, "worktreeClean": True,
                  "limits": "Exact signed bytes, complete selections and both host gate sets only. "
                            "No semantic, confirmation, device or publication acceptance."}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Correction verification RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(REVIEW / "coordinator-reconciliation-verification-001.json", result)))


if __name__ == "__main__":
    verify()
