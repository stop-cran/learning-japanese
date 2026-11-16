"""Bind B127's signed correction, complete selections, preserved bytes and gates."""
import datetime
import gzip
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import (CHECKS, GUARD_SHA, WS, freeze_json, frozen, git, load_batch,
                    load_module, require, sha, start_guard)
from verify_b123_revision_v2 import check_gate, runtime
from verify_b124_reconciliation import HashReader
from verify_b127_sources import FINGERPRINT, VERIFIER, VERIFIER_SHA, RUNNER_SHA

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

CANDIDATE = "6541c81fa9d58f25849562f19ab7b04282f392e3"
SCRATCH = WS / "scratch-127"
REVIEW = SCRATCH / "review"
PREFIX = "docs/n1-sources/batch-127-reconciliation/"
MEMBER = "\u5009"
CARD = f"kanji/{MEMBER}.md"
OTHERS = "\u56f2\u4fdd\u9810\u5bb9\u7559\u5b58\u6301\u5fd9\u901f\u6b7b\u5ef6\u6b62\u505c"
OLD_GUARDS = list("\u5eab\u8535\u5e9c\u5ba4\u53ce\u8caf\u6025\u7a81\u4ea1\u7f6e\u5165")
ADDED_GUARDS = [char for char in OTHERS if char != "\u5b58"]
HANDOFF_SHA = "17686ef80ee57d91b73384f7a2a855e86d5baa4d1213c6ec8d5d64c1219429fe"
DRIVER_SHA = "e03dc3f51da7873b86e0b640e3e0d34356360d8f441eba9a8b282355358451e6"
SERIAL_SHA = "ec62cbf2a03b012b8cdba50cacd925e9eb3816d9f3978eaae3cd65a14343856d"
COMMON_SHA = "a13ff0ddc995e636cf0eeba8153179e364422bf496093d14c0c14480cd057b2e"
SOURCE_SHA = "24cc550390a6b1d49f62bd9e349d7a05049745c0a7ff36a43cb9afe45504c133"
PAIRS_SHA = "1891e64fb601767584b51d5330a08a289126663279c90cd2179260ae04128185"
MANIFEST_SHA = "8b668da6ed7c88eff76542878fe1044f5b48b58ba8343b30566a7d1d39ed44a7"


def metadata(raw):
    result, _ = parse(raw.decode("utf-8").replace("\r\n", "\n"))
    require(result is not None, "Missing card metadata")
    return result


def check_metadata(old, new):
    require({k: v for k, v in old.items() if k != "quiz_exclusions"}
            == {k: v for k, v in new.items() if k != "quiz_exclusions"},
            "Non-exclusion metadata changed")
    require(old["quiz_exclusions"] == OLD_GUARDS
            and new["quiz_exclusions"] == OLD_GUARDS + ADDED_GUARDS
            and len(set(new["quiz_exclusions"])) == 23
            and new["distractors"] == list("\u91d1\u5168\u5408")
            and not set(new["distractors"]) & set(new["quiz_exclusions"]),
            "Original/required guards or curated options changed")


def check_claims(table, receipt, old, new, comparison_cards):
    claims = table["claims"]
    require(len(claims) == 13
            and [row["id"] for row in claims] == [f"Q{i}" for i in range(1, 14)]
            and [row["pair"] for row in claims] == [[MEMBER, char] for char in OTHERS]
            and table["unguardedOpenClaimIds"] == [], "Finite claim inventory differs")
    for row in claims:
        other = row["pair"][1]
        card = comparison_cards[other]
        before = {MEMBER: other in old["quiz_exclusions"],
                  other: MEMBER in card.get("quiz_exclusions", [])}
        after = {MEMBER: other in new["quiz_exclusions"], other: before[other]}
        require(row["otherTitle"] == card["title"]
                and row["declaredEndpointStatus"] == {
                    "parent": before, "revision": after,
                    "effectiveSymmetricGuard": any(after.values())},
                f"Wrong displayed title or declaring endpoint: {row['id']}")
        expected = ("distinct-with-positive-source-support" if row["id"] == "Q6"
                    else "source-supported-direct-guard" if row["id"] in {"Q8", "Q12", "Q13"}
                    else "conservative-direct-guard")
        require(row["disposition"] == expected
                and len(row["directions"]) == 2 and all(row["directions"].values())
                and row["strongestPlausibleOverlap"] and row["citations"]
                and row["remainingUncertainty"], f"Incomplete disposition: {row['id']}")
        binding = row["recordBindings"]
        require(binding["character"] == {
                    "file": "kanjidic2-comparison-records.xml", "literal": other}
                and binding["completeWordFamilies"] == {
                    "file": "jmdict-comparison-records.xml",
                    "entryIds": receipt["selectors"][row["id"]]["entryIds"]},
                f"Wrong complete source family: {row['id']}")


def verify_sources(receipt, blob, guard):
    frozen(VERIFIER, VERIFIER_SHA)
    verifier = load_module("b127_complete_reconciliation_sources", VERIFIER)
    snapshot = json.loads(blob("docs/n1-source-snapshot.json"))
    queries = {q for item in receipt["selectors"].values() for q in item["exactKebQueries"]}
    results = []
    for kind, (filename, compressed_sha, tag, key) in verifier.INPUTS.items():
        raw = blob(PREFIX + f"{kind}-comparison-records.xml")
        declared = receipt["outputs"][f"{kind}-comparison-records.xml"]
        nodes = ET.fromstring(raw).findall(tag)
        expected = verifier.records(raw, tag, key)
        canonical = {node.findtext(key): sha(ET.canonicalize(
            ET.tostring(node, encoding="unicode"), strip_text=True).encode()) for node in nodes}
        require(sha(raw) == declared["sha256"] and len(raw) == declared["bytes"]
                and canonical == declared["canonicalCompleteRecordHashes"]
                and len(expected) == (55 if kind == "jmdict" else 14),
                f"Extracted record hashes or count differ: {kind}")
        exact = queries if kind == "jmdict" else set(MEMBER + OTHERS)
        if kind == "jmdict":
            index = {query: [node.findtext(key) for node in nodes
                             if query in {item.text for item in node.findall("k_ele/keb")}]
                     for query in queries}
            require(index == receipt["exactQueryMembership"]
                    and sorted(q for q, ids in index.items() if not ids) == receipt["zeroMatchQueries"],
                    "Exact selector membership differs")
            for qid, char in zip((f"Q{i}" for i in range(1, 14)), OTHERS):
                item = receipt["selectors"][qid]
                require(item["character"] == char and item["entryIds"]
                        == sorted({eid for query in item["exactKebQueries"] for eid in index[query]}),
                        f"Per-claim source union differs: {qid}")
        else:
            require(receipt["kanjidicSelector"] == sorted(exact), "Character selector differs")
        source = WS / "control" / "inputs" / filename
        with source.open("rb") as stream:
            reader = HashReader(stream, guard)
            while reader.read(65536):
                pass
        require(reader.digest.hexdigest() == compressed_sha == snapshot["inputs"][filename]["sha256"],
                f"Compressed source differs: {kind}")
        with gzip.open(source, "rb") as stream:
            reader = HashReader(stream, guard)
            found = verifier.verify_stream(reader, tag, key, [{
                "name": kind, "mode": "exact", "queries": exact, "expected": expected,
            }], guard)[0]
            while reader.read(65536):
                pass
        require(reader.digest.hexdigest() == snapshot[kind]["xmlSha256"]
                and receipt["dictionaryInputs"][kind] == {
                    "filename": filename, "compressedSha256": compressed_sha,
                    "decompressedSha256": reader.digest.hexdigest()},
                f"Decompressed source differs: {kind}")
        results.append({"kind": kind, "identities": found, "queries": sorted(exact),
                        "outputSha256": sha(raw), "compressedSha256": compressed_sha,
                        "decompressedSha256": reader.digest.hexdigest()})
    return results


def verify_gates(handoff, config, guard):
    repo = Path(config["repo"])
    lean = WS / "lean"
    commands = {
        "lint": [str(lean / "n1_batch_tool.py"), "lint", "--base", config["candidate"], "--no-jmdict", MEMBER],
        "quiz-safety": [str(lean / "quiz_safety.py"), MEMBER],
        "linkplan": [str(lean / "n1_linkplan.py"), "verify", config["candidate"], MEMBER],
        "reading-exposure": [str(SCRATCH / "check_reading_b127.py")],
        "validate": [str(repo / "tools" / "validate.py")],
        "manifest": [str(repo / "tools" / "build_manifest.py")],
        "unittest": ["-m", "unittest", "discover", "-s", "tools", "-p", "test_*.py"],
        "budget": [str(repo / "tools" / "check_content_budget.py")],
        "vocabulary": [str(repo / "tools" / "grammar_vocabulary.py"), "check"],
        "manifest-rebuild": [str(repo / "tools" / "build_manifest.py")],
    }
    for name, digest in (("reconcile_gates_b127.py", DRIVER_SHA),
                         ("run_b127_gates.py", SERIAL_SHA), ("b127_common.py", COMMON_SHA)):
        require(sha((SCRATCH / name).read_bytes()) == digest, f"Gate producer changed: {name}")
    gate_sets, latest = {}, None
    for mode in ("author", "committed"):
        binding = handoff["bindings"][mode + "Gates"]
        directory = SCRATCH / f"reconciliation-{mode}-gates-001"
        require(Path(binding["directory"]) == directory, "Gate directory differs")
        summary = json.loads(frozen(directory / "summary.json", binding["summarySha256"]))
        head = config["candidate"] if mode == "author" else CANDIDATE
        require(summary["batch"] == "127" and summary["revision"] == "reconciliation-001"
                and summary["status"] == "PASS" and summary["mode"] == mode
                and summary["parent"] == config["candidate"] and summary["startingHead"] == head
                and summary["publishedBase"] == config["base"]
                and summary["checks"] == list(commands) and summary["commands"] == commands
                and summary["runnerSha256"] == DRIVER_SHA
                and summary["reusedSerialRunGateSha256"] == SERIAL_SHA
                and summary["commonHelperSha256"] == COMMON_SHA
                and summary["guardSha256"] == GUARD_SHA and summary["serial"] is True
                and summary["waitTimeoutSeconds"] == 0.1
                and summary["cleanupTimeoutSecondsPerStage"] == 10
                and summary["manifestSha256"] == MANIFEST_SHA
                and not summary["finalMemory"]["breach"], f"Wrong gate summary: {mode}")
        rows = []
        for name, arguments in commands.items():
            declared = summary["logs"][name]
            raw = frozen(directory / f"{name}.json", declared["receiptSha256"])
            record = json.loads(raw)
            log = frozen(directory / f"{name}.log", declared["logSha256"])
            check_gate(record, log, name, MANIFEST_SHA, str(repo), SERIAL_SHA)
            require(record["command"][1:] == ["-B", *arguments]
                    and record["commonHelperSha256"] == COMMON_SHA
                    and record["cleanupTimeoutSecondsPerStage"] == 10
                    and record["cleanupError"] is None and record["activeError"] is None,
                    f"Gate command or cleanup differs: {mode}/{name}")
            started = datetime.datetime.fromisoformat(record["startedAt"])
            finished = datetime.datetime.fromisoformat(record["completedAt"])
            require(finished >= started and (latest is None or started >= latest),
                    "Gate executions overlap or are out of order")
            latest = finished
            if name == "unittest":
                require(re.search(rb"(?m)^Ran 431 tests in [0-9.]+s\r?\n\r?\nOK\r?$", log),
                        "Expected 431 tests did not pass")
            rows.append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
            guard.check()
        require({row["gate"] for row in rows} == set(CHECKS), "Missing gate")
        gate_sets[mode] = {"directory": str(directory), "summarySha256": binding["summarySha256"],
                           "head": head, "gates": rows}
    directory = REVIEW / "reconciliation-published-base-linkplan-001"
    raw, log = (directory / "receipt.json").read_bytes(), (directory / "output.log").read_bytes()
    extra = json.loads(raw)
    require(extra["command"][1:] == ["-B", r"..\lean\n1_linkplan.py", "verify", config["base"], MEMBER]
            and extra["cwd"] == str(repo) and extra["exitCode"] == extra["childExitCodeAfterCleanup"] == 0
            and extra["runnerSha256"] == RUNNER_SHA and extra["guardSha256"] == GUARD_SHA
            and extra["waitTimeoutSeconds"] == 0.1 and extra["cleanupError"] is None
            and not extra["memory"]["breach"] and extra["logSha256"] == sha(log)
            and log.decode().strip() == "changed word files: 1; expected pairs: 1; added link pairs: 1; "
            "total added links: 1; declared remark edits: 0; problems: 0",
            "Published-base reciprocal-link supplement failed")
    for path in (directory / "receipt.json", directory / "output.log"):
        path.chmod(0o444)
    return gate_sets, {"directory": str(directory), "receiptSha256": sha(raw), "logSha256": sha(log),
                       "reason": "Author delta gates use the reviewed parent (zero new pairs); "
                                 "this supplement verifies the original one-pair published-base obligation."}


def main():
    config = load_batch(127)
    repo = Path(config["repo"])
    output = REVIEW / "reconciliation-001-independent-proof.json"
    require(not output.exists(), "Preserve existing proof")
    handoff = json.loads(frozen(SCRATCH / "reconciliation-handoff-001" / "handoff.json", HANDOFF_SHA))
    guard, _ = start_guard("B127 signed reconciliation verification")
    blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
    previous = lambda path: git(config, "show", f"{config['candidate']}:{path}")
    try:
        require(git(config, "rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git(config, "status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is not a clean HEAD")
        require(git(config, "show", "-s", "--format=%P|%G?|%GF|%GP|%ae|%ce", CANDIDATE).decode().strip()
                == f"{config['candidate']}|G|{FINGERPRINT}|{FINGERPRINT}|stop-cran@list.ru|stop-cran@list.ru",
                "Wrong direct parent or owner signature")
        git(config, "verify-commit", CANDIDATE)
        require(b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
                in git(config, "show", "-s", "--format=%B", CANDIDATE), "Missing co-author trailer")
        require(handoff["candidate"] == CANDIDATE and handoff["parent"] == config["candidate"]
                and handoff["publishedBase"] == config["base"], "Handoff lineage differs")
        inventory = json.loads(frozen(SCRATCH / "reconciliation-handoff-001" / "changed-files.json",
                                     handoff["changedFileInventory"]["sha256"]))
        names = git(config, "diff", "--name-only", "--no-renames", "-z",
                    config["candidate"], CANDIDATE).decode().strip("\0").split("\0")
        expected = [item["path"] for item in inventory["files"]]
        require(names == expected and len(set(names)) == 66
                and all(path.startswith(PREFIX) or path in {
                    CARD, "manifest.json", "docs/n1-authoring-notes.md",
                    "docs/n1-sources/batch-127-progress-002.json"} for path in names),
                "Unexpected changed-file inventory")
        signed_artifacts = {}
        for item in inventory["files"]:
            raw = blob(item["path"])
            require(sha(raw) == item["sha256"] and len(raw) == item["bytes"]
                    and (repo / item["path"]).read_bytes() == raw, f"Signed bytes differ: {item['path']}")
            signed_artifacts[item["path"]] = sha(raw)
            guard.check()
        old, new = metadata(previous(CARD)), metadata(blob(CARD))
        check_metadata(old, new)
        manifest = json.loads(blob("manifest.json"))
        before, after = runtime(json.loads(previous("manifest.json"))), runtime(manifest)
        require(sha(blob("manifest.json")) == MANIFEST_SHA
                and manifest["contentVersion"] == "b6f11a69505108f7"
                and before.keys() == after.keys() and len(after) == 8716
                and [path for path in after if before[path] != after[path]] == [CARD]
                and after[CARD] == sha(blob(CARD).replace(b"\r\n", b"\n")), "Runtime delta differs")
        for path in (f"words/{MEMBER}\u5eab.md", f"strokes/{MEMBER}.json"):
            require(blob(path) == previous(path), f"Preserved runtime bytes changed: {path}")
        notes = previous("docs/n1-authoring-notes.md")
        revised_notes = blob("docs/n1-authoring-notes.md")
        require(notes in revised_notes and len(revised_notes) > len(notes), "Historical notes changed")
        history = json.loads(blob(PREFIX + "preserved-history.json"))
        require(history["parent"] == config["candidate"] and len(history["files"]) == 189
                and not set(history["files"]) & set(names), "Historical files changed")
        for path, item in history["files"].items():
            raw = (repo / path).read_bytes()
            require(sha(raw) == item["sha256"] and len(raw) == item["bytes"], f"History differs: {path}")
            guard.check()
        packet = json.loads(blob(PREFIX + "packet-files.json"))
        require(len(packet["files"]) == 61
                and set(names) & {PREFIX + name for name in packet["files"]} ==
                {PREFIX + name for name in packet["files"]}, "Packet inventory differs")
        for name, item in packet["files"].items():
            raw = (repo / PREFIX / name).read_bytes()
            require(sha(raw) == item["sha256"] and len(raw) == item["bytes"], f"Packet differs: {name}")
        receipt_raw, pairs_raw = blob(PREFIX + "source-receipt.json"), blob(PREFIX + "pair-dispositions.json")
        require(sha(receipt_raw) == SOURCE_SHA and sha(pairs_raw) == PAIRS_SHA, "Signed source binding differs")
        receipt, pairs = json.loads(receipt_raw), json.loads(pairs_raw)
        sources = verify_sources(receipt, blob, guard)
        comparisons = {}
        for char in MEMBER + OTHERS:
            copied = blob(PREFIX + f"comparison-cards/{char}.md")
            require(copied == previous(f"kanji/{char}.md"), f"Comparison snapshot differs: {char}")
            if char != MEMBER:
                require(copied == blob(f"kanji/{char}.md"), f"Comparison endpoint changed: {char}")
                comparisons[char] = metadata(copied)
                row = next(row for row in pairs["claims"] if row["pair"][1] == char)
                require(row["recordBindings"]["comparisonCard"] == {
                    "file": f"comparison-cards/{char}.md", "sha256": sha(copied)},
                    f"Comparison binding differs: {char}")
        check_claims(pairs, receipt, old, new, comparisons)
        for field in ("admissionBindings", "reusedImmutableEvidence", "reusedExternalSnapshots"):
            for item in receipt[field].values():
                raw = Path(item["path"]).read_bytes()
                require(sha(raw) == item["sha256"] and len(raw) == item["bytes"],
                        f"Reused evidence changed: {item['path']}")
                guard.check()
        responses = {}
        for family, other in (("claude", "gpt"), ("gpt", "claude")):
            raw = blob(PREFIX + family + "-author-response.md")
            require(sha(raw) == handoff["bindings"][family + "Response"]["sha256"]
                    and not re.search(rf"\b{other}\b", raw.decode(), re.I), "Cross-family response")
            responses[family] = sha(raw)
        gate_sets, linkplan = verify_gates(handoff, config, guard)
        require(not git(config, "status", "--porcelain=v1", "--untracked-files=all"), "Worktree changed")
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Verification RAM guard breached")
    proof = {
        "batch": 127, "status": "PASS", "candidate": CANDIDATE,
        "parent": config["candidate"], "base": config["base"],
        "signature": {"fingerprint": FINGERPRINT, "ownerVerified": True}, "worktreeClean": True,
        "runtimeChanged": [CARD], "runtimeEntries": len(after), "preservedRuntimeAndHistory": True,
        "manifestSha256": MANIFEST_SHA, "contentVersion": manifest["contentVersion"],
        "changedFiles": names, "signedArtifacts": signed_artifacts,
        "sourceReceiptSha256": SOURCE_SHA, "dispositionsSha256": PAIRS_SHA,
        "sources": sources, "responses": responses, "gateSets": gate_sets,
        "publishedBaseLinkplan": linkplan, "memory": memory, "handoffSha256": HANDOFF_SHA,
        "addedDirectGuards": ADDED_GUARDS, "conservativeGuardIds": pairs["conservativeGuardClaimIds"],
        "distinctClaimIds": ["Q6"], "unguardedOpenClaimIds": [],
        "reviewAccepted": False, "confirmationAccepted": False,
        "verifierSha256": sha(Path(__file__).read_bytes()),
        "limits": "Signed bytes, complete source selections and twenty bound host gates, plus the "
                  "published-base reciprocal pair, are verified. Author semantic dispositions still "
                  "require independent original-family confirmation; conservative guards retain "
                  "linguistic uncertainty. Not native/device, arbitrary-pool or publication acceptance.",
    }
    print(json.dumps(freeze_json(output, proof)))


if __name__ == "__main__":
    main()
