"""Verify the second reconciliation's signed packet and actual successful retry."""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

import b130_delta_gates as gates
from b130_context_confirmation import binding
from b130_delta_pairs import check_responses, check_table
from b130_followup_closure_history import PREVIOUS
from b130_signed_evidence import verify_reading_keys
from common import GUARD_SHA, TOOLS, WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from finalize_b130 import PROOF_SHA, ROOT
from verify_b130_payload import BASE, REPO, RUNNER
from verify_b130_revision_runtime_v3 import MEMBERS, PREFIX
from verify_b130_sources import FINGERPRINT, Git, ORIGIN, OWNER, TRAILER

CANDIDATE = "1ac4053c5da955c3afaafc1e879e63a98ee42526"
RUNTIME_SHA = "3455b584d0a3571d18bfc7cb302ad2e83abf985ffb366dc602ded59fad443ca2"
REUSE_SHA = "94d454b6ff92c774874a7ea092e9f6fbbab4be052e4a1139c0888030404b6ccb"
FAILED = ROOT.parent / "reconciliation-002-committed-gates-001"
FAILED_SHA = "adc8debabe900876b223be665380eb4d196984059e2d2e6ad090342eb47a5dac"
ORIGINAL = "docs/n1-sources/batch-130/"


def check_failed(files):
    require(set(files) == {"admission.json", *(f"{name}.{suffix}" for name in
            ("lint", "quiz-safety", "linkplan", "reading-exposure", "validate")
            for suffix in ("json", "log"))}, "Aborted gate directory was completed or rewritten")
    raw = files["validate.json"]
    row = json.loads(raw)
    require(sha(raw) == FAILED_SHA and row["gate"] == "validate"
            and row["exitCode"] is None and row["childExitCodeAfterCleanup"] == 1
            and row["cleanupError"] is None and row["memory"]["breach"] == row["activeError"]
            and row["memory"]["minimumObservedFreeRamBytes"] == 1040928768
            and row["logSha256"] == sha(files["validate.log"])
            and row["logBytes"] == len(files["validate.log"]) == 0,
            "Aborted validation was relabelled or lost")
    return row


def main(handoff_path, handoff_sha, output_path):
    handoff_path, output = Path(handoff_path).resolve(), Path(output_path).resolve()
    require(output.parent == ROOT and not output.exists(), "Use a new direct review evidence directory")
    handoff_raw = handoff_path.read_bytes()
    require(sha(handoff_raw) == handoff_sha, "Reported handoff bytes differ")
    handoff = json.loads(handoff_raw)
    require(handoff["status"] == "AUTHOR-VERIFICATION-COMPLETE-UNPUBLISHED-AWAITING-TWO-INDEPENDENT-CONFIRMATIONS"
            and handoff["candidate"] == CANDIDATE and handoff["parent"] == PREVIOUS
            and handoff["publishedBase"] == BASE and handoff["clean"] is True,
            "Incomplete or different signed handoff")
    runtime_path, reuse_path = ROOT / "delta-runtime-proof-001.json", ROOT / "delta-source-reuse-proof-001.json"
    runtime = json.loads(frozen(runtime_path, RUNTIME_SHA))
    reuse = json.loads(frozen(reuse_path, REUSE_SHA))
    require(runtime["status"] == "PASS_RUNTIME_ONLY" and reuse["status"] == "PASS_SOURCE_REUSE_ONLY"
            and runtime["candidate"] == reuse["candidate"] == CANDIDATE
            and runtime["parent"] == reuse["parent"] == PREVIOUS
            and all(item["reviewAccepted"] is False and item["publicationAccepted"] is False
                    and gates.memory_ok(item["memory"]) for item in (runtime, reuse)),
            "Independent proofs differ")
    previous_proof = json.loads(frozen(ROOT / "revision-evidence-001" / "verification.json", PROOF_SHA))
    guard, _ = start_guard("B130 second signed evidence verification")
    git = Git(REPO, RUNNER, guard)
    cache, captured = {}, {}

    def clean():
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed successor checkout changed")

    def blob(path, revision=CANDIDATE):
        key = (revision, path)
        if key not in cache:
            cache[key] = git("show", f"{revision}:{path}")
        raw = cache[key]
        if revision == CANDIDATE:
            require((REPO / path).read_bytes() == raw, "Checkout differs: " + path)
        guard.check()
        return raw

    def source(name):
        return blob(PREFIX + name)

    try:
        clean()
        require(git("remote", "get-url", "origin").decode().strip() == ORIGIN
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{PREVIOUS}|G|{FINGERPRINT}|{OWNER}|{OWNER}"
                and TRAILER in git("show", "-s", "--format=%B", CANDIDATE), "Signed identity differs")
        changes = runtime["changedPaths"]
        require(len(changes) == handoff["exactChangedFiles"]["count"] == 42, "Unexpected delta count")
        for path, digest in runtime["signedArtifacts"].items():
            require(sha(blob(path)) == digest, "Signed delta differs")
        changed_raw = Path(handoff["exactChangedFiles"]["path"]).read_bytes()
        require(sha(changed_raw) == handoff["exactChangedFiles"]["sha256"], "Handoff inventory changed")
        changed = json.loads(changed_raw)
        require(changed["candidate"] == CANDIDATE and changed["parent"] == PREVIOUS
                and changed["count"] == len(set(changed["files"])) == 42
                and set(changed["files"]) == set(changes)
                and changed["committedBlobSha256"] == runtime["signedArtifacts"],
                "Handoff inventory contradicts independent signed proof")
        inventory_raw = source("evidence-inventory-003.json")
        inventory = json.loads(inventory_raw)
        prior_inventory_raw = source("evidence-inventory-002.json")
        prior_inventory = json.loads(prior_inventory_raw)
        prior_files = {**prior_inventory["files"], "evidence-inventory-002.json": sha(prior_inventory_raw)}
        require(inventory["parent"] == PREVIOUS and inventory["selfExcluded"] is True
                and len(inventory["files"]) == 141 and len(prior_files) == 104
                and inventory["previousInventory"] == {
                    "path": "evidence-inventory-002.json", "sha256": sha(prior_inventory_raw)}
                and all(inventory["files"].get(name) == digest for name, digest in prior_files.items())
                and sha(inventory_raw) == handoff["packetInventory"]["sha256"],
                "Prior or active evidence inventory differs")
        names = [PREFIX + name for name in inventory["files"]]
        for path, (_, raw) in zip(names, git.objects([f"{CANDIDATE}:{name}" for name in names])):
            cache[(CANDIDATE, path)] = raw
            require(sha(blob(path)) == inventory["files"][path[len(PREFIX):]], "Packet hash differs")
        actual_paths = set(git("ls-tree", "-r", "--name-only", CANDIDATE, "--", PREFIX).decode().splitlines())
        require(actual_paths == set(names) | {PREFIX + "evidence-inventory-003.json"}
                and {path for path in changes if path.startswith(PREFIX)}
                == actual_paths - {PREFIX + name for name in prior_files},
                "New packet membership or additive delta differs")
        require(not git("diff", "--name-only", PREVIOUS, CANDIDATE, "--", ORIGINAL)
                and len(git("ls-tree", "-r", "--name-only", CANDIDATE, "--", ORIGINAL).splitlines()) == 307,
                "Original packet was changed")
        sys.path.insert(0, str(WS / "lean"))
        from n1lib import parse
        metadata = {char: parse(blob(f"kanji/{char}.md").decode("utf-8").replace("\r\n", "\n"))[0]
                    for char in MEMBERS}
        table_raw = source("pair-dispositions-002.json")
        pair_proof = check_table(source("pair-dispositions-001.json"), json.loads(table_raw),
                                 metadata, json.loads(source("source-receipt.json")))
        pair_proof["pairTableSha256"] = sha(table_raw)
        pair_proof["responses"] = check_responses(source, table_raw)
        source_reuse = json.loads(source("source-reuse-002.json"))
        for name, digest in source_reuse["files"].items():
            require(sha(source(name)) == digest, "Declared source reuse differs")
        receipt = json.loads(source("source-receipt.json"))
        family_hashes = receipt["outputs"]["jmdict-families.xml"]["canonicalRecordHashes"]
        require(source_reuse["parent"] == PREVIOUS
                and source_reuse["completeFamiliesRead"] == {
                    identity: family_hashes[identity] for identity in ("1238610", "1408810")},
                "Decisive complete-family hashes differ")
        tool_bindings = json.loads(source("second-002-tool-bindings.json"))
        original_bindings = json.loads(source("tool-bindings.json"))
        require(tool_bindings["parent"] == PREVIOUS
                and tool_bindings["originalImplementationBindings"] == {
                    "path": "tool-bindings.json", "sha256": sha(source("tool-bindings.json"))}
                and original_bindings["guardSha256"] == GUARD_SHA, "Original gate identity differs")
        for name, digest in tool_bindings["newProducers"].items():
            require(sha(source("producers/" + name)) == digest
                    and (ROOT.parent / name).read_bytes() == source("producers/" + name),
                    "New executed producer differs")
        for name, item in original_bindings["dependencies"].items():
            require(sha(blob(ORIGINAL + "producers/" + name)) == item["sha256"]
                    and (ROOT.parent / name).read_bytes() == blob(ORIGINAL + "producers/" + name),
                    "Original implementation dependency differs")
        for name, digest in original_bindings["leanTools"].items():
            require(sha((WS / "lean" / name).read_bytes()) == digest, "Lean tool differs")
        for name, group in handoff["localSourceGatePreservationAndSigningReceipts"].items():
            directory = Path(group["directory"])
            require(directory == ROOT.parent / name
                    and {path.name for path in directory.iterdir()} == set(group["files"]),
                    "Handoff directory inventory differs")
            for filename, digest in group["files"].items():
                raw = (directory / filename).read_bytes()
                require(sha(raw) == digest, "Handoff execution hash differs")
                captured[f"{name}/{filename}"] = raw
        gate_sets = {}
        for mode, name in (("author", "reconciliation-002-author-gates-001"),
                           ("committed", "reconciliation-002-committed-gates-002")):
            record, files = gates.verify(
                ROOT.parent / name, mode, CANDIDATE, runtime["manifestSha256"],
                tool_bindings["newProducers"]["run_b130_second_gates.py"],
                original_bindings["dependencies"]["run_b130_gates.py"]["sha256"],
                original_bindings["dependencies"]["b130_common.py"]["sha256"], guard)
            require(all(captured[f"{name}/{filename}"] == raw for filename, raw in files.items()),
                    "Gate files changed while being checked")
            if mode == "author":
                require(all(source(f"author-evidence/second-002/{name}/{filename}") == raw
                            for filename, raw in files.items()), "Signed author execution copy differs")
            gate_sets[mode] = record
            warnings = [line for line in files["quiz-safety.log"].decode("utf-8").splitlines()
                        if line.startswith("WARN")]
            require(warnings == previous_proof["retainedQuizSafetyWarnings"], "Warnings changed")
            unit = files["unittest.log"].decode("utf-8")
            require(re.search(r"(?m)^Ran 431 tests in .+\r?$", unit)
                    and re.search(r"(?m)^OK\r?$", unit), "Full host tests differ")
            keys = json.loads(blob(ORIGINAL + "reading-keys.json"))["testedKeys"]
            verify_reading_keys(blob(ORIGINAL + "producers/check_reading_b130.py"),
                                blob(ORIGINAL + "reading-keys.json"), files["reading-exposure.log"], keys)
        failure_files = {path.name: path.read_bytes() for path in FAILED.iterdir()}
        require(all(captured[f"{FAILED.name}/{name}"] == raw for name, raw in failure_files.items()),
                "Aborted evidence changed after handoff hash verification")
        failed = check_failed(failure_files)
        captured.update({FAILED.name + "/" + name: raw for name, raw in failure_files.items()})
        require(datetime.fromisoformat(gate_sets["committed"]["firstStartedAt"])
                > datetime.fromisoformat(failed["completedAt"])
                > datetime.fromisoformat(gate_sets["author"]["lastCompletedAt"]),
                "Retry did not follow the preserved aborted attempt")
        for mode, name in (("author", "reconciliation-002-author-preserve-001"),
                           ("committed", "reconciliation-002-committed-preserve-001")):
            preservation = json.loads(captured[f"{name}/summary.json"])
            require(preservation["status"] == "PASS" and preservation["mode"] == mode
                    and preservation["parent"] == PREVIOUS and preservation["publishedBase"] == BASE
                    and preservation["head"] == (PREVIOUS if mode == "author" else CANDIDATE)
                    and set(preservation["exactChangedFileInventory"]) == set(changes)
                    and preservation["runtimeHashesChecked"] == 8730
                    and preservation["otherRuntimeManifestEntriesUnchanged"] == 8729
                    and preservation["allOtherParentTrackedBlobsPreserved"] is True
                    and preservation["earlierNotesRawBytesPreserved"] is True
                    and preservation["originalPacketFilesChecked"] == 307
                    and preservation["oldReconciliationInventoryFilesChecked"] == 104
                    and preservation["manifestSha256"] == runtime["manifestSha256"]
                    and preservation["packetInventorySha256"] == sha(inventory_raw)
                    and gates.memory_ok(json.loads(captured[f"{name}/memory.json"])),
                    "Preservation evidence differs")
        progress = json.loads(blob("docs/n1-sources/batch-130-progress-reconciliation-003.json"))
        require(progress["parent"] == PREVIOUS and progress["publishedBase"] == BASE
                and progress["status"] == "unpublished-author-proposal-awaiting-two-independent-confirmations"
                and (progress["publishedDelivered"], progress["undelivered"], progress["frozenTotal"],
                     progress["localUnpublishedDrafts"], progress["deliveryCredit"]) == (261, 967, 1228, 3, 0)
                and progress["lexicalAllocationResolved"] is False
                and progress["historicalOriginalQuestionsPreserved"] == 24
                and progress["counts"] == pair_proof["counts"] and progress["unprotectedAuthorQuizHolds"] == []
                and progress["manifestSha256"] == runtime["manifestSha256"]
                and progress["contentVersion"] == runtime["contentVersion"]
                and progress["quizSafetyWarnings"] == warnings, "Premature or different author progress")
        require(handoff_path.read_bytes() == handoff_raw, "Handoff changed during verification")
        clean()
        captures = {name: write_frozen(output / "captured" / name, raw)
                    for name, raw in captured.items()}
        captures["author-handoff.json"] = write_frozen(output / "captured" / "author-handoff.json", handoff_raw)
        captures["changed-files.json"] = write_frozen(output / "captured" / "changed-files.json", changed_raw)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Signed delta evidence RAM guard breached")
    print(json.dumps(freeze_json(output / "verification.json", {
        "batch": 130, "status": "PASS_SECOND_RECONCILIATION_BINDINGS_ONLY",
        "candidate": CANDIDATE, "parent": PREVIOUS, "base": BASE,
        "proofs": {"runtime": binding(runtime_path), "sourceReuse": binding(reuse_path)},
        "previousEvidenceProof": binding(ROOT / "revision-evidence-001" / "verification.json"),
        "handoffSha256": handoff_sha, "changedFileCount": 42, "originalPacketFiles": 307,
        "priorEvidencePreserved": True, "pairBindings": pair_proof, "gateSets": gate_sets,
        "preservedAbortedGate": {"receiptSha256": FAILED_SHA, "attempt": FAILED.name,
                                "result": "RESOURCE_ABORT_NOT_SUCCESS"},
        "captureImmutability": "Source files are checked against the exact final handoff hashes, "
                               "then captured read-only now. No historical read-only state is inferred.",
        "retainedQuizSafetyWarnings": warnings, "capturedExecutionFiles": captures,
        "producer": binding(__file__),
        "helpers": [binding(TOOLS / name) for name in ("b130_delta_pairs.py", "b130_delta_gates.py")],
        "memory": memory, "reviewAccepted": False, "publicationAccepted": False,
        "limits": "Exact signed packet, source reuse, pair/history metadata, unchanged ten commands "
                  "and successful serial retry. Failed001 remains failed. Semantic dispositions and "
                  "both isolated confirmations remain required; no native/device/publication acceptance.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 4, "Usage: verify_b130_delta_evidence.py HANDOFF SHA256 NEW_OUTPUT_DIRECTORY")
    main(*sys.argv[1:])
