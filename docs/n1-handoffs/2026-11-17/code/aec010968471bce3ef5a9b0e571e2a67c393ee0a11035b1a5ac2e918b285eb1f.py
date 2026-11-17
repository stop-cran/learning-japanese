"""Verify the immutable first correction while its two remaining holds are revised."""
import datetime
import gzip
import hashlib
import json
import re
import xml.etree.ElementTree as ET

from common import GUARD_SHA, WS, freeze_json, frozen, git, load_batch, load_module, require, sha, start_guard
from verify_b123_revision_v2 import runtime
from verify_b124_reconciliation import HashReader

CANDIDATE = "49d0b00d438969b157e739360f8639c6a9b0d950"
PREFIX = "docs/n1-sources/batch-125-reconciliation/"
COMPARISONS = set("損略戦凌患病毒破占触違突徹討痛")
SUMMARY_HASHES = {
    "author": "c1a1c21839aedf8d1164a03e8bd6e08c2aa47416d61dc190a359d0d861f57bb8",
    "committed": "e7ef5fb4006bd8d65c26c0e954e60f234f9b9aa23f7347350e51b76eed65f274",
}
XML_HASHES = {
    "jmdict": "107079c692f2e49c08d45da1da227b7e021298f247d16578b44dfaa2ec9002c4",
    "kanjidic2": "9a000ef112b4bad8f1e6e3ca1f8e9f73ed84c93a5eae93dadfa1513081dc5db8",
}


def main():
    config = load_batch(125)
    blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
    previous = lambda path: git(config, "show", f"{config['candidate']}:{path}")
    receipt_raw = blob(PREFIX + "source-receipt.json")
    require(sha(receipt_raw) == "b7a96deea5a41555e14eb7ae71585d6c94dbf20bbe8038be3579e76b4ce1bbd7",
            "Source receipt differs from handoff")
    receipt = json.loads(receipt_raw)
    dispositions_raw = blob(PREFIX + "dispositions.json")
    require(sha(dispositions_raw) == "db59648976ec2f8f54e526c4b90929c7168006b3200e564d5d0da3712ae649b6",
            "Disposition snapshot differs")
    dispositions = json.loads(dispositions_raw)["dispositions"]
    require({row["other"] for row in dispositions} == COMPARISONS and len(dispositions) == 15
            and {row["id"] for row in dispositions if row["status"] == "open"} == {"Q4", "Q9"},
            "Finite comparison inventory or remaining holds differ")
    tool_path = WS / "scratch-124" / "review" / "verify-source-records.py"
    frozen(tool_path, "21842b6d2d6040d2deb4a9f8c6d15f2c28c17386a443da52780a7ef7cc169c62")
    source_tool = load_module("b125_reconciliation_001_complete_sources", tool_path)
    guard, _ = start_guard("B125 first correction immutable source and gate verification")
    try:
        for path, digest in receipt["files"].items():
            require(sha(blob(PREFIX + path)) == digest, f"Source bytes differ: {path}")
        require(len(receipt["files"]) == 20, "Unexpected source inventory")
        for character in COMPARISONS:
            path = f"kanji/{character}.md"
            require(blob(PREFIX + f"comparison-cards/{character}.md") == blob(path) == previous(path),
                    f"Comparison card changed: {character}")
        sources = []
        for kind, (filename, compressed, tag, key) in source_tool.INPUTS.items():
            metadata = receipt["selections"][kind]
            raw = blob(PREFIX + f"{kind}-records.xml")
            expected = source_tool.records(raw, tag, key)
            queries = ({query for values in receipt["queriesByDisposition"].values() for query in values}
                       if kind == "jmdict" else COMPARISONS)
            index = {query: [] for query in queries}
            for node in ET.fromstring(raw).findall(tag):
                keys = ({element.text for element in node.findall("k_ele/keb")}
                        if kind == "jmdict" else {node.findtext("literal")})
                for query in keys & queries:
                    index[query].append(node.findtext(key))
            require(metadata["matchingIdsByExactSelector"] == index
                    and metadata["unmatchedSelectors"] == sorted(q for q, ids in index.items() if not ids)
                    and metadata["recordCount"] == len(expected) == (62 if kind == "jmdict" else 15)
                    and metadata["outputSha256"] == sha(raw)
                    and metadata["compressedSha256"] == compressed
                    and metadata["decompressedXmlSha256"] == XML_HASHES[kind],
                    f"{kind} declared membership or input bindings differ")
            path = WS / "control" / "inputs" / filename
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    guard.check()
                    digest.update(chunk)
            require(digest.hexdigest() == compressed, f"{kind} compressed input changed")
            with gzip.open(path, "rb") as stream:
                reader = HashReader(stream, guard)
                found = source_tool.verify_stream(reader, tag, key, [{
                    "name": kind, "mode": "exact", "queries": queries, "expected": expected,
                }], guard)[0]
                while reader.read(1024 * 1024):
                    pass
            require(reader.digest.hexdigest() == XML_HASHES[kind], f"{kind} decompressed input changed")
            sources.append({"kind": kind, "identities": found, "queries": sorted(queries),
                            "outputSha256": sha(raw), "compressedSha256": compressed})
        manifest_raw = blob("manifest.json")
        manifest_sha = sha(manifest_raw)
        require(manifest_sha == "d0c0ed77434a2cdf67bbdb7d47a81b0934e3af7e24bb4d28ae79ae8d54d2b8e3",
                "Manifest differs from handoff")
        current, initial = runtime(json.loads(manifest_raw)), runtime(json.loads(previous("manifest.json")))
        require(current.keys() == initial.keys() and len(current) == 8712
                and {path for path in initial if current[path] != initial[path]} == {"kanji/侵.md"},
                "Runtime scope changed")
        for path in ("words/侵入.md", "strokes/侵.json"):
            require(blob(path) == previous(path), f"Preserved runtime bytes changed: {path}")
        repo, lean, scratch = WS / "b125-worktree", WS / "lean", WS / "scratch-125"
        commands = {
            "lint": [str(lean / "n1_batch_tool.py"), "lint", "--base", config["base"], "--no-jmdict", "侵"],
            "quiz-safety": [str(lean / "quiz_safety.py"), "侵"],
            "linkplan": [str(lean / "n1_linkplan.py"), "verify", config["base"], "侵"],
            "reading-exposure": [str(scratch / "reading.py")],
            "validate": [str(repo / "tools" / "validate.py")],
            "manifest": [str(repo / "tools" / "build_manifest.py")],
            "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
            "budget": [str(repo / "tools" / "check_content_budget.py")],
            "vocabulary": [str(repo / "tools" / "grammar_vocabulary.py"), "check"],
            "manifest-rebuild": [str(repo / "tools" / "build_manifest.py")],
        }
        driver_sha = "077b33ed341ae7a5417d676feafeb3b262edabe300b21fced3cfe6ac38036c9a"
        runner_sha = "ecccdbaa897600e9842865d335ab4b73a5d51b33c64c250f2c3ae60d715ba299"
        require(sha((scratch / "reconciliation-001-gates.py").read_bytes()) == driver_sha
                and sha((WS / "scratch-124" / "run-reconciliation-002-checks.py").read_bytes()) == runner_sha,
                "Executed gate producer changed")
        gates, latest = {}, None
        for mode, summary_sha in SUMMARY_HASHES.items():
            directory = scratch / f"reconciliation-001-{mode}-gates-001"
            summary_raw = (directory / "summary.json").read_bytes()
            summary = json.loads(summary_raw)
            require(sha(summary_raw) == summary_sha and summary["status"] == "PASS"
                    and summary["batch"] == 125 and summary["reconciliation"] == 1
                    and summary["mode"] == mode and summary["publishedBase"] == config["base"]
                    and summary["parent"] == config["candidate"]
                    and summary["head"] == (config["candidate"] if mode == "author" else CANDIDATE)
                    and summary["checks"] == list(commands) and summary["manifestSha256"] == manifest_sha
                    and summary["runnerSha256"] == driver_sha and summary["boundedRunnerSha256"] == runner_sha,
                    f"{mode} summary binding differs")
            gates[mode] = []
            for name, arguments in commands.items():
                raw = (directory / f"{name}.json").read_bytes()
                record = json.loads(raw)
                log = (directory / f"{name}.log").read_bytes()
                started = datetime.datetime.fromisoformat(record["startedAt"])
                completed = datetime.datetime.fromisoformat(record["completedAt"])
                require(record["gate"] == name and record["command"][1:] == ["-B", *arguments]
                        and record["cwd"] == str(repo) and record["exitCode"] == 0
                        and record["childExitCodeAfterCleanup"] == 0 and record["waitTimeoutSeconds"] <= 1
                        and record["runnerSha256"] == runner_sha and record["guardSha256"] == GUARD_SHA
                        and record["logSha256"] == sha(log) and record["logBytes"] == len(log)
                        and record["memory"]["breach"] is None
                        and record["memory"]["freeRamBeforeBytes"] > 2 * 1024**3
                        and record["memory"]["minimumObservedFreeRamBytes"] >= 1024**3
                        and completed >= started and (latest is None or started >= latest),
                        f"{mode}/{name}: command, execution, ordering, log or resource binding differs")
                latest = completed
                if name == "unittest":
                    require(re.search(rb"(?m)^Ran 431 tests in [0-9.]+s\r?\n\r?\nOK\r?$", log),
                            "Expected test run did not pass")
                if name == "manifest-rebuild":
                    require(record["manifestReproducible"] is True
                            and record["manifestSha256"] == manifest_sha, "Manifest was not reproduced")
                gates[mode].append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
                guard.check()
        print(freeze_json(scratch / "review" / "reconciliation-001-independent-proof.json", {
            "batch": 125, "candidate": CANDIDATE, "parent": config["candidate"], "status": "PASS",
            "sourceReceiptSha256": sha(receipt_raw), "dispositionsSha256": sha(dispositions_raw),
            "sources": sources, "gates": gates, "runtimeEntries": len(current),
            "manifestSha256": manifest_sha, "openClaimIds": ["Q4", "Q9"],
            "reviewAccepted": False, "confirmationAccepted": False,
            "limits": "Immutable Git snapshot and original execution receipts only; current checkout may "
                      "be advancing in the author session. Full selected records and all twenty gate "
                      "receipts are verified, not semantic harmlessness, final review or publication.",
        }))
    finally:
        require(not guard.finish()["breach"], "Independent verification RAM guard breached")


if __name__ == "__main__":
    main()
