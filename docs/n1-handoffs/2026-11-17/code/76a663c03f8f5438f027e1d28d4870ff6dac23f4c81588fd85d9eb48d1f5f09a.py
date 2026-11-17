"""Verify the signed S1 correction, full selected sources and actual execution evidence."""
import datetime
import difflib
import gzip
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import (CHECKS, WS, freeze_json, frozen, git, load_batch, load_module,
                    require, sha, start_guard)
from confirm_v2 import clean
from verify_b123_revision_v2 import runtime
from verify_b124_reconciliation import HashReader
from verify_b125_reconciliation_001 import XML_HASHES
from verify_b125_reconciliation_002 import FINGERPRINT, RUNNER_SHA, frontmatter, listed, receipt, visible

PARENT = "dbca5192a4308dc6e8d954af37775e0fcd1986ea"
PREFIX = "docs/n1-sources/batch-125-reconciliation-003/"
COMPARISONS = set("低短小容劣汚美貧")
WORDS = {"低い", "短い", "小さい", "劣る", "汚い", "美しい", "貧しい"}
ADDED = list("低短小容")
OLD = list("犯冒害攻撃入損痛討略戦患病毒破触違突徹凌占")
INVENTORY_SHA = "ee0ae6331d6fa12b8403f7527bbd59f89beb1b97e6ef3483e88f5941fef0d08d"
REPORTS = {
    "claude": "ce0cbf16a6b0c4248faedbe5df78f119296ca49cb055606ff5950602883c7679",
    "gpt": "0415392277549cc1f6a0592b6f2047ae659d6bb6ea370dd78d39206efa3e856d",
}


def inventory_row(character, raw, parse):
    fm, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
    require(fm and fm["kanji"] == character, "Inventory card identity differs")
    return {
        "kanji": character, "title": fm["title"], "onyomi": fm.get("onyomi", []),
        "kunyomi": fm.get("kunyomi", []), "quizOnyomi": fm.get("quizOnyomi"),
        "quizKunyomi": fm.get("quizKunyomi"), "tags": fm.get("tags", []), "sha256": sha(raw),
    }


def verify_inventory(inventory, actual, key):
    require(inventory["parent"] == PARENT and inventory["count"] == len(actual)
            and len(inventory["cards"]) == len(actual)
            and len({row["kanji"] for row in inventory["cards"]}) == len(actual)
            and {row["kanji"]: row for row in inventory["cards"]} == actual,
            "Complete parent inventory fields, membership or hashes differ")
    for row in actual.values():
        for base, practice in (("onyomi", "quizOnyomi"), ("kunyomi", "quizKunyomi")):
            offered = row[base] if row[practice] is None else row[practice]
            require(all(key(reading) != "みにくい" for reading in [*row[base], *offered]),
                    "The external exact reading key is present in current metadata/practice")


def main(handoff_path):
    handoff_raw = frozen(handoff_path)
    handoff = json.loads(handoff_raw)
    config = load_batch(125)
    candidate = handoff["candidate"]
    require(handoff["parent"] == PARENT, "Handoff parent differs")
    clean(config, candidate)
    meta = git(config, "show", "-s", "--format=%P%n%G?|%GF|%ae|%ce%n%cI%n%B", candidate).decode().splitlines()
    require(meta[:2] == [PARENT, f"G|{FINGERPRINT}|stop-cran@list.ru|stop-cran@list.ru"]
            and "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in meta,
            "Signature, parent, identities or trailer differ")
    committed_at = datetime.datetime.fromisoformat(meta[2])
    blob = lambda rev, path: git(config, "show", f"{rev}:{path}")
    current = lambda path: blob(candidate, path)
    repo, scratch, lean = Path(config["repo"]), WS / "scratch-125", WS / "lean"
    scripts = scratch / "reconciliation-003-scripts"
    guard, _ = start_guard("B125 S1 independent verification")
    try:
        changed = {tuple(line.split("\t", 1)) for line in git(
            config, "diff", "--no-renames", "--name-status", PARENT, candidate).decode().splitlines()}
        expected = {("M" if path in ("kanji/侵.md", "manifest.json") else "A", path)
                    for path in handoff["changedFiles"]}
        require(changed == expected and len(changed) == 11, "Exact additive changed-file inventory differs")
        for path, digest in handoff["changedFiles"].items():
            require(sha(current(path)) == digest, f"Signed bytes differ from handoff: {path}")
        old_card, card = blob(PARENT, "kanji/侵.md"), current("kanji/侵.md")
        before, after = frontmatter(old_card.decode()), frontmatter(card.decode())
        require(before.keys() == after.keys()
                and all(before[k] == after[k] for k in before if k != "quiz_exclusions")
                and listed(before["quiz_exclusions"]) == OLD
                and listed(after["quiz_exclusions"]) == OLD + ADDED,
                "Frozen metadata or prior exclusions changed")
        old_lines, new_lines = old_card.decode().splitlines(), card.decode().splitlines()
        ops = [op for op in difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False).get_opcodes()
               if op[0] != "equal"]
        require(len(ops) == 2 and ops[0][0] == "replace" and ops[0][2] - ops[0][1] == 1
                and old_lines[ops[0][1]].startswith("quiz_exclusions:")
                and ops[1][0] == "insert" and ops[1][4] - ops[1][3] == 1
                and all(f"[{char}]({char}.md)" in new_lines[ops[1][3]] for char in ADDED)
                and "does not imply" in new_lines[ops[1][3]], "Runtime prose delta differs")
        manifest_raw = current("manifest.json")
        manifest = json.loads(manifest_raw)
        before_runtime, after_runtime = runtime(json.loads(blob(PARENT, "manifest.json"))), runtime(manifest)
        require(len(after_runtime) == 8712 and before_runtime.keys() == after_runtime.keys()
                and {p for p in after_runtime if before_runtime[p] != after_runtime[p]} == {"kanji/侵.md"}
                and sha(card.replace(b"\r\n", b"\n")) == after_runtime["kanji/侵.md"]
                and sha(manifest_raw) == handoff["manifestSha256"]
                and manifest["contentVersion"] == handoff["contentVersion"], "Runtime/manifest binding differs")
        for path in ("words/侵入.md", "strokes/侵.json", *(f"kanji/{c}.md" for c in COMPARISONS)):
            require(current(path) == blob(PARENT, path), f"Unrelated runtime changed: {path}")

        source_raw = current(PREFIX + "source-receipt.json")
        source = json.loads(source_raw)
        require(source["parent"] == PARENT
                and source["priorSourceReceiptSha256"] == sha(current(
                    "docs/n1-sources/batch-125-reconciliation-002/source-receipt.json"))
                and source["priorDispositionSha256"] == sha(current(
                    "docs/n1-sources/batch-125-reconciliation-002/dispositions.json")),
                "Previous source/disposition binding differs")
        capture = scratch / "reconciliation-002-source-captures-001" / "shin.html"
        capture_raw = frozen(capture, "710735ff84146a52d67432006836576b54e3bf4b329daadd86ec46dc447252e4")
        require(source["kanjiPedia"]["localCaptureSha256"] == sha(capture_raw)
                and source["kanjiPedia"]["url"] == "https://www.kanjipedia.jp/kanji/0003603100"
                and "②みにくい。背が低くて容姿がみすぼらしい。" in visible(capture_raw),
                "Actual positive character-source capture differs")
        selector_path = scratch / "reconciliation-003-sources-001" / "source-receipt.json"
        selector_raw = selector_path.read_bytes()
        selectors = json.loads(selector_raw)
        require(sha(selector_raw) == source["selectedRecords"]["selectorReceiptSha256"]
                == "2520134d212dfc25a68d49774611ee936776b9eab879ff04ba584ab6a59434ea",
                "Selected source receipt differs")
        source_tool_path = WS / "scratch-124" / "review" / "verify-source-records.py"
        frozen(source_tool_path, "21842b6d2d6040d2deb4a9f8c6d15f2c28c17386a443da52780a7ef7cc169c62")
        source_tool = load_module("b125_s1_source_verifier", source_tool_path)
        source_records = []
        for kind, (filename, compressed_sha, tag, identity) in source_tool.INPUTS.items():
            raw = current(PREFIX + f"{kind}-records.xml")
            expected_records = source_tool.records(raw, tag, identity)
            queries = WORDS if kind == "jmdict" else COMPARISONS
            index = {query: [] for query in queries}
            for node in ET.fromstring(raw).findall(tag):
                keys = {e.text for e in node.findall("k_ele/keb")} if kind == "jmdict" else {node.findtext("literal")}
                for query in queries & keys:
                    index[query].append(node.findtext(identity))
            selected = selectors["selections"][kind]
            require(selected["exactSelectors"] == index and all(index.values())
                    and selected["recordCount"] == len(expected_records) == (7 if kind == "jmdict" else 8)
                    and selected["outputSha256"] == source["selectedRecords"][f"{kind}-records.xml"] == sha(raw)
                    and selected["compressedSha256"] == compressed_sha, "Selected record inventory differs")
            source_path = WS / "control" / "inputs" / filename
            digest = hashlib.sha256()
            with source_path.open("rb") as stream:
                while chunk := stream.read(1024 * 1024):
                    digest.update(chunk)
                    guard.check()
            require(digest.hexdigest() == compressed_sha, "Compressed dictionary changed")
            with gzip.open(source_path, "rb") as stream:
                reader = HashReader(stream, guard)
                found = source_tool.verify_stream(reader, tag, identity, [{
                    "name": kind, "mode": "exact", "queries": queries, "expected": expected_records,
                }], guard)[0]
                while reader.read(1024 * 1024):
                    pass
            require(reader.digest.hexdigest() == XML_HASHES[kind], "Decompressed dictionary changed")
            source_records.append({"kind": kind, "identities": found, "queries": sorted(queries),
                                   "outputSha256": sha(raw), "compressedSha256": compressed_sha,
                                   "decompressedSha256": reader.digest.hexdigest()})

        sys.path.insert(0, str(lean))
        from n1lib import parse
        from reading_options import key
        inventory_path = scratch / "reconciliation-003-inventory-002" / "card-inventory.json"
        inventory_raw = inventory_path.read_bytes()
        inventory = json.loads(inventory_raw)
        require(sha(inventory_raw) == source["parentInventory"]["sha256"] == INVENTORY_SHA,
                "Retained second inventory differs")
        paths = git(config, "ls-tree", "-r", "--name-only", "-z", PARENT, "kanji").decode().split("\0")
        paths = [path for path in paths if path.endswith(".md")]
        actual = {}
        for path in paths:
            character = Path(path).stem
            actual[character] = inventory_row(character, blob(PARENT, path), parse)
            guard.check()
        require(len(actual) == 1245, "Unexpected complete parent card count")
        verify_inventory(inventory, actual, key)

        evidence_commands = {
            "reconciliation-003-inventory-002/inventory.json": [
                str(scripts / "inventory.py"), str(inventory_path)],
            "reconciliation-003-sources-001/sources.json": [
                str(scripts / "extract.py"), str(scratch / "reconciliation-003-sources-001")],
            "reconciliation-003-reading-001/reading.json": [str(scripts / "reading-model.py")],
            "reconciliation-003-author-integrity-002/integrity.json": [str(scripts / "integrity.py")],
            "reconciliation-003-committed-integrity-001/integrity.json": [str(scripts / "integrity.py")],
        }
        evidence = {}
        for name, command in evidence_commands.items():
            record, log = receipt(scratch / name, handoff["evidenceReceipts"][name], command, repo)
            evidence[name] = {"receiptSha256": sha((scratch / name).read_bytes()), "logSha256": sha(log)}
            if name.endswith("integrity.json"):
                check = json.loads(log)
                require(check["head"] == (candidate if "committed" in name else PARENT)
                        and check["parentInventoryCardsVerified"] == 1245
                        and check["additionalGuards"] == ADDED, "Integrity log snapshot differs")
            if name.endswith("reading.json"):
                require(sha(log) == source["readingModelLogSha256"], "Explicit reading evidence differs")
                replay = subprocess.check_output([sys.executable, "-B", str(scripts / "reading-model.py")], cwd=repo)
                require(replay == log, "Explicit-source bounded reading replay differs")
        require(sha((scratch / source["meaningModelLog"].split("/", 1)[1]).read_bytes())
                == source["meaningModelLogSha256"], "Meaning model evidence differs")

        commands = {
            "lint": [str(lean / "n1_batch_tool.py"), "lint", "--base", config["base"], "--no-jmdict", "侵"],
            "quiz-safety": [str(lean / "quiz_safety.py"), "侵"],
            "linkplan": [str(lean / "n1_linkplan.py"), "verify", config["base"], "侵"],
            "reading-exposure": [str(scripts / "reading.py")],
            "validate": [str(repo / "tools" / "validate.py")],
            "manifest": [str(repo / "tools" / "build_manifest.py")],
            "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
            "budget": [str(repo / "tools" / "check_content_budget.py")],
            "vocabulary": [str(repo / "tools" / "grammar_vocabulary.py"), "check"],
            "manifest-rebuild": [str(repo / "tools" / "build_manifest.py")],
        }
        driver_sha = sha((scripts / "gates.py").read_bytes())
        require(sha((WS / "scratch-124" / "run-reconciliation-002-checks.py").read_bytes()) == RUNNER_SHA
                and (scripts / "reading.py").read_bytes() == (scratch / "reading.py").read_bytes(),
                "Pinned runner or isolated reading script changed")
        gates, latest = {}, None
        for mode, bindings in handoff["gateSets"].items():
            directory = scratch / bindings["directory"]
            summary_raw = (directory / "summary.json").read_bytes()
            summary = json.loads(summary_raw)
            require(sha(summary_raw) == bindings["summary"] and summary["batch"] == 125
                    and summary["reconciliation"] == 3 and summary["status"] == "PASS"
                    and summary["mode"] == mode and summary["publishedBase"] == config["base"]
                    and summary["parent"] == PARENT and summary["head"] == (PARENT if mode == "author" else candidate)
                    and summary["checks"] == list(commands) and set(commands) == set(CHECKS)
                    and summary["manifestSha256"] == handoff["manifestSha256"]
                    and summary["runnerSha256"] == driver_sha and summary["boundedRunnerSha256"] == RUNNER_SHA,
                    "Gate summary differs from signed handoff")
            gates[mode] = []
            for name, command in commands.items():
                record, log = receipt(directory / f"{name}.json", bindings[name], command, repo)
                started = datetime.datetime.fromisoformat(record["startedAt"])
                completed = datetime.datetime.fromisoformat(record["completedAt"])
                require(record["gate"] == name and (latest is None or started >= latest)
                        and (completed <= committed_at if mode == "author" else started >= committed_at),
                        "Gate order or commit-time attribution differs")
                latest = completed
                if name == "unittest":
                    require(re.search(rb"(?m)^Ran 431 tests in [0-9.]+s\r?\n\r?\nOK\r?$", log),
                            "Expected host test result is missing")
                if name == "manifest-rebuild":
                    require(record["manifestReproducible"] is True
                            and record["manifestSha256"] == handoff["manifestSha256"], "Manifest rebuild differs")
                gates[mode].append({"gate": name, "receiptSha256": bindings[name], "logSha256": sha(log)})

        responses = {}
        for family, report_sha in REPORTS.items():
            report = WS / "reports-125" / f"N1-B125-{family.upper()}-CONFIRM-001.md"
            require(sha(frozen(report)) == report_sha, "Raw earlier confirmation changed")
            raw = current(PREFIX + f"{family}-response-003.md")
            other = "gpt" if family == "claude" else "claude"
            require(not re.search(rf"\b{other}\b", raw.decode(), re.I) and report_sha in raw.decode()
                    and (family != "claude" or "UNVERIFIED" not in raw.decode()), "Family response isolation differs")
            responses[family] = sha(raw)
        progress = json.loads(current("docs/n1-sources/batch-125-progress-004.json"))
        selection = json.loads(current("docs/n1-sources/batch-125/selection-004.json"))
        require(progress["parent"] == selection["parent"] == PARENT
                and progress["membership"] == ["侵"] and progress["sourceRows"] == [48]
                and progress["reviewClosed"] == progress["published"] == []
                and progress["runtimePublished"] is False
                and progress["accounting"] == {"frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 254,
                                               "publishedN1Additions": 248, "n2Placements": 6,
                                               "undelivered": 974, "overallN1TaskComplete": False}
                and selection["s1AddedDirectGuards"] == ADDED
                and selection["requiredReciprocalPairs"] == [["侵入", "侵"]]
                and selection["distractors"] == ["寝", "進", "掃"], "Selection or delivery accounting changed")
        clean(config, candidate)
        proof = {
            "batch": 125, "status": "PASS", "candidate": candidate, "parent": PARENT,
            "originalCandidate": config["candidate"],
            "signature": {"status": "G", "fingerprint": FINGERPRINT, "signer": "stop-cran@list.ru"},
            "handoffSha256": sha(handoff_raw), "changedFiles": handoff["changedFiles"],
            "sourceReceiptSha256": sha(source_raw), "dispositionsSha256": sha(current(PREFIX + "disposition.md")),
            "sourceRecords": source_records, "parentInventorySha256": INVENTORY_SHA, "parentInventoryCards": 1245,
            "externalReadingKey": "みにくい", "exactMetadataAndPracticeMatches": [],
            "explicitReadingReplayByteIdentical": True, "additionalGuards": ADDED,
            "unrelatedRuntimeAndFrozenMetadataPreserved": True, "runtimeChanged": ["kanji/侵.md"],
            "runtimeEntries": 8712, "manifestSha256": sha(manifest_raw), "contentVersion": manifest["contentVersion"],
            "gateSets": handoff["gateSets"], "gates": gates, "evidenceReceipts": evidence, "responses": responses,
            "reviewAccepted": False, "confirmationAccepted": False,
            "limits": "Independent bytes, exact complete source records, current inventory and bounded host model only. "
                      "No usage-frequency inference, arbitrary/future pool, multi-borrow, native/device, semantic "
                      "confirmation or publication acceptance. Failed inventory001 remains excluded.",
        }
        print(freeze_json(scratch / "review" / "reconciliation-003-independent-proof.json", proof))
    finally:
        require(not guard.finish()["breach"], "Independent verification breached RAM guard")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
