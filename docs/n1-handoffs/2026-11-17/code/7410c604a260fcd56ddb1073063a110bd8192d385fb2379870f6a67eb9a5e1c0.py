"""Verify the second B124 correction and byte-exact reuse of its complete source packet."""
import json
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, load_module, require, sha, start_guard
from confirm_v2 import clean
from verify_b124_reconciliation import (
    CANDIDATE as PARENT, CARD, COMPARISONS, CONTRACT_TOOL_SHA, PREFIX as PREVIOUS_PREFIX,
    SIGNER, STROKES, WORD,
)
from verify_b123_revision_v2 import runtime
from n1lib import parse

REVIEW = WS / "scratch-124" / "review"
PREFIX = "docs/n1-sources/batch-124-reconciliation-002/"
PROGRESS = "docs/n1-sources/batch-124-progress-004.json"
SELECTION = "docs/n1-sources/batch-124/selection-005.json"
AUDIT = "docs/n1-sources/batch-124/author-audit-004.json"
SOURCE_NAMES = {"source-receipt.json", "dispositions.json", "dispositions.md",
                "claude-response.md", "gpt-response.md"}
ADDED = list("\u798f\u6804\u8cc7\u5b9d\u4f59\u5270\u6e80\u60a0\u6fc3")
RETAINED = list("\u539a\u5bcc\u8c4a\u8ca1\u591a\u697d\u5e83")
OPEN_IDS = ["Q1", "Q3", "Q4", "Q5", "Q7", "Q8", "Q10", "Q11", "Q16"]
FIRST_PROOF_SHA = "4a2622178667f86cb0c6a80b4e1e2cedde2846d2d34511b84c828f09c24edcc0"
RUNNER_SHA = "ecccdbaa897600e9842865d335ab4b73a5d51b33c64c250f2c3ae60d715ba299"


def check_card(old_raw, new_raw):
    old_text, new_text = (raw.decode("utf-8").replace("\r\n", "\n") for raw in (old_raw, new_raw))
    old, old_body = parse(old_text)
    new, new_body = parse(new_text)
    require({k: v for k, v in old.items() if k != "quiz_exclusions"}
            == {k: v for k, v in new.items() if k != "quiz_exclusions"},
            "Preserved title, reading, distractor or other metadata changed")
    require(old["quiz_exclusions"] == RETAINED and new["quiz_exclusions"] == RETAINED + ADDED,
            "Expected exactly seven retained and nine appended direct guards")
    before, after = old_body.splitlines(), new_body.splitlines()
    added = [line for line in after if line not in before]
    require(len(added) == 1 and added[0].startswith("- Sources record ")
            and [line for line in after if line != added[0]] == before,
            "Existing card body or reading/source paragraph changed")
    require("conservatively" in added[0] and "do not assert synonymy" in added[0]
            and "compound" in added[0] and "\u88d5 is not taught as rich-flavored" in added[0],
            "Conservative scope or compound/flavor qualification missing")
    return new


def check_summary(summary, config, candidate, mode, manifest_sha):
    require(summary["batch"] == "124" and summary["reconciliation"] == 2
            and summary["status"] == "PASS" and summary["mode"] == mode
            and summary["publishedBase"] == config["base"]
            and summary["reconciliationParent"] == PARENT
            and summary["startingHead"] == (candidate if mode == "committed" else PARENT)
            and len(summary["checks"]) == len(CHECKS) and set(summary["checks"]) == set(CHECKS)
            and summary["manifestSha256"] == manifest_sha and summary["runnerSha256"] == RUNNER_SHA,
            "Gate summary belongs to another mode, revision or manifest")


def check_dispositions(value, titles, source_receipt, old_dispositions):
    rows = value["dispositions"]
    prior = {row["id"]: row for row in old_dispositions["dispositions"]}
    require(len(rows) == 17 and {row["id"] for row in rows} == set(prior)
            and {row["candidate"] for row in rows} == COMPARISONS,
            "Disposition inventory differs")
    require(value["target"] == {"kanji": "\u88d5", "displayedLabel": titles["\u88d5"],
                               "sourceRow": 986, "postReconciliationGuards": RETAINED + ADDED},
            "Disposition target scope or guards differ")
    require(value["supersededPriorJudgments"]["supersededClaims"] == OPEN_IDS,
            "Superseded claims differ")
    selectors = source_receipt["dictionaryInputs"]["jmdict"]["recordSelectors"]
    for row in rows:
        char, evidence = row["candidate"], row["evidence"]
        expected = ("conservative-direct-guard" if char in ADDED else
                    "direct-guard-retained" if char in RETAINED else "no-new-guard-retained")
        require(row["candidateLabel"] == titles[char] and row["decision"] == expected
                and row["previousDecision"] == prior[row["id"]]["decision"]
                and row["reviewFinding"] is False, f"Pair attribution, label or decision differs: {char}")
        require(evidence["kanjidic2Character"] == char
                and len(evidence["jmdictEntries"]) == len(set(evidence["jmdictEntries"]))
                and set(evidence["jmdictEntries"]) == set(evidence["selectors"]),
                f"Pair record inventory differs: {char}")
        for identity, queries in evidence["selectors"].items():
            require(identity in selectors and queries and len(queries) == len(set(queries))
                    and set(queries) <= set(selectors[identity]), f"Unsupported exact selector: {char}/{identity}")
        status = "guard added" if char in ADDED else "guard retained" if char in RETAINED else "no guard"
        require(row["endpointStatus"] == {"\u88d5": status, char: "no inverse guard"}
                and row["\u88d5PromptToCandidate"] and row["candidatePromptTo\u88d5"],
                f"Direct endpoint disposition missing: {char}")


def verify():
    config = load_batch(124)
    handoff_path = WS / "scratch-124" / "reconciliation-002-handoff.json"
    handoff_raw = frozen(handoff_path)
    handoff = json.loads(handoff_raw)
    candidate = handoff["commit"]["sha"]
    clean(config, candidate)
    require(handoff["commit"]["parent"] == PARENT
            and git(config, "show", "-s", "--format=%P", candidate).decode().strip() == PARENT,
            "Expected a direct child of the first correction")
    require(git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce", candidate).decode().strip()
            == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Owner signature differs")
    require(b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
            in git(config, "show", "-s", "--format=%B", candidate), "Co-author trailer missing")
    first_path = REVIEW / "coordinator-reconciliation-verification-001.json"
    first = json.loads(frozen(first_path, FIRST_PROOF_SHA))
    require(first["status"] == "PASS" and first["candidate"] == PARENT
            and first["initial"] == config["candidate"] and first["base"] == config["base"]
            and not first["memory"]["breach"], "Prior complete-source proof differs")
    contract_path = REVIEW / "prepare-source-contract.py"
    frozen(contract_path, CONTRACT_TOOL_SHA)
    contract = load_module("b124_second_correction_contract", contract_path)
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    previous = lambda path: git(config, "show", f"{PARENT}:{path}")
    guard, _ = start_guard("B124 second signed correction verification")
    try:
        changes = [line.split("\t") for line in git(
            config, "diff", "--name-status", "--no-renames", PARENT, candidate
        ).decode("utf-8").splitlines()]
        expected = {CARD: "M", "manifest.json": "M", PROGRESS: "A", SELECTION: "A", AUDIT: "A",
                    **{PREFIX + name: "A" for name in SOURCE_NAMES}}
        inventory = handoff["fileInventory"]["files"]
        require(len(changes) == len(expected) == handoff["fileInventory"]["count"] == len(inventory)
                and {path: status for status, path in changes} == expected
                and sorted(expected) == sorted(item["path"] for item in inventory),
                "Signed file inventory or additive scope differs")
        for item in inventory:
            raw = blob(item["path"])
            require(sha(raw) == item["sha256"] and len(raw) == item["bytes"], "Handoff file bytes differ")
        metadata = check_card(previous(CARD), blob(CARD))
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
        for path, digest in first["signedArtifacts"].items():
            require(sha(blob(path)) == digest and blob(path) == previous(path),
                    f"Earlier signed source evidence changed: {path}")
            guard.check()
        old_receipt = json.loads(blob(PREVIOUS_PREFIX + "source-receipt.json"))
        source_raw = blob(PREFIX + "source-receipt.json")
        receipt = json.loads(source_raw)
        require(receipt["candidateParent"] == PARENT and receipt["publishedBase"] == config["base"]
                and receipt["noAdditionalQueriesOrFetches"] is True
                and sha(source_raw) == handoff["sourceProvenance"]["receiptSha256"]
                and receipt == handoff["sourceProvenance"]["receipt"],
                "New source receipt scope or handoff binding differs")
        reuse = receipt["reusedSourceContract"]
        require(reuse["path"] == "../batch-124-reconciliation/source-receipt.json"
                and reuse["sha256"] == sha(blob(PREVIOUS_PREFIX + "source-receipt.json")),
                "Reused receipt binding differs")
        for kind in ("jmdict", "kanjidic2"):
            old = old_receipt["dictionaryInputs"][kind]
            declared = reuse[kind]
            require(declared["recordsPath"] == f"../batch-124-reconciliation/{kind}-records.xml"
                    and declared["recordsSha256"] == old["extractedSha256"]
                    == sha(blob(PREVIOUS_PREFIX + f"{kind}-records.xml"))
                    and declared["compressedSha256"] == old["compressedSha256"]
                    and declared["decompressedXmlSha256"] == old["decompressedXmlSha256"],
                    f"Reused complete {kind} bytes or dictionary pins differ")
        require(reuse["jmdict"]["completeRecordCount"] == 48
                and reuse["jmdict"]["exactWrittenFormQueryCount"] == 45
                and reuse["jmdict"]["unmatchedExactQueries"] == 0
                and reuse["kanjidic2"]["completeCharacterCount"] == 18,
                "Complete source contract was weakened")
        copies = reuse["comparisonCardCopies"]["sha256AtParent"]
        require(copies == old_receipt["comparisonCardSha256AtParent"], "Comparison source inventory differs")
        titles = {"\u88d5": metadata["title"]}
        for char, digest in copies.items():
            raw = blob(f"kanji/{char}.md")
            require(sha(raw) == digest and raw == previous(f"kanji/{char}.md")
                    == blob(PREVIOUS_PREFIX + f"comparison-cards/{char}.md"),
                    f"Reused comparison card changed: {char}")
            titles[char] = parse(raw.decode("utf-8").replace("\r\n", "\n"))[0]["title"]
        supplemental = receipt["supplementalTargetSource"]
        frozen(supplemental["capturePath"], supplemental["captureSha256"])
        frozen(supplemental["receiptPath"], supplemental["receiptSha256"])
        bindings = receipt["confirmationBindings"]
        for name in ("coordinatorBrief", "authorAdmission"):
            frozen(bindings[name]["path"], bindings[name]["sha256"])
        for family in ("claude", "gpt"):
            item = bindings[family]
            for key in ("report", "acceptance", "final", "adjudication"):
                frozen(item[key + "Path"], item[key + "Sha256"])
            accepted = json.loads(frozen(item["acceptancePath"], item["acceptanceSha256"]))
            require(item["rawVerdict"] == accepted["verdict"]
                    and item["accepted"] is accepted["confirmationAccepted"] is False
                    and item["openClaimIds"] == accepted["openClaimIds"]
                    and item["acceptedNewFindings"] == accepted["acceptedNewFindings"] == [],
                    "Held confirmation was relabeled")
        dispositions_raw = blob(PREFIX + "dispositions.json")
        dispositions = json.loads(dispositions_raw)
        check_dispositions(dispositions, titles, old_receipt,
                           json.loads(blob(PREVIOUS_PREFIX + "dispositions.json")))
        selection = json.loads(blob(SELECTION))
        require(selection["membership"] == [{"kanji": "\u88d5", "sourceRow": 986}]
                and selection["requiredReciprocalPairs"] == [["\u4f59\u88d5", "\u88d5"]]
                and selection["directMeaningGuards"] == RETAINED + ADDED
                and selection["distractors"] == metadata["distractors"]
                and set(selection["comparisonCards"]) == COMPARISONS,
                "Selection membership or quiz metadata differs")
        selected = selection["reconciliation"]
        for key, name in (("sourceReceiptSha256", "source-receipt.json"),
                          ("dispositionsSha256", "dispositions.json"),
                          ("dispositionsMarkdownSha256", "dispositions.md")):
            require(selected[key] == sha(blob(PREFIX + name)), "Selection evidence binding differs")
        for family in ("claude", "gpt"):
            require(selected["reviewResponses"][family]["sha256"] == sha(blob(PREFIX + f"{family}-response.md")),
                    "Family response binding differs")
        runner = WS / "scratch-124" / "run-reconciliation-002-checks.py"
        frozen(runner, RUNNER_SHA)
        gate_sets = {}
        for mode, key in (("author", "authoringGates"), ("committed", "committedGates")):
            declared = handoff["verification"][key]
            directory = WS / declared["directory"]
            require(directory.parent == WS / "scratch-124", "Gates outside this batch")
            summary_raw = frozen(directory / "summary.json", declared["summarySha256"])
            check_summary(json.loads(summary_raw), config, candidate, mode, manifest_sha)
            for item in declared["checks"]:
                frozen(WS / item["receiptPath"], item["receiptSha256"])
                frozen(WS / item["logPath"], item["logSha256"])
            verified = contract.gate_bindings(directory, config, manifest_sha, RUNNER_SHA, guard)
            require(verified == [{"gate": item["name"], "receiptSha256": item["receiptSha256"],
                                  "logSha256": item["logSha256"]}
                                 for name in CHECKS for item in declared["checks"] if item["name"] == name],
                    "Handoff gate receipts differ")
            require(b"Ran 431 tests" in frozen(directory / "unittest.log"), "Expected unit run missing")
            gate_sets[mode] = {"directory": str(directory), "summarySha256": sha(summary_raw), "gates": verified}
        progress_raw = blob(PROGRESS)
        progress = json.loads(progress_raw)
        require(progress["published"] == progress["reviewClosed"] == []
                and progress["runtimePublished"] is False
                and progress["accounting"]["publishedPendingRecordsWithCards"] == 253
                and progress["accounting"]["undelivered"] == 975
                and progress["accounting"]["overallN1TaskComplete"] is False
                and progress["runtimeCandidate"]["manifestSha256"] == manifest_sha
                == handoff["verification"]["manifestSha256"], "Unpublished accounting or manifest differs")
        history = handoff["preservedHistory"]
        frozen(WS / history["priorHandoffPath"], history["priorHandoffSha256"])
        for key, path in (
            ("priorProgress003Sha256", "docs/n1-sources/batch-124-progress-003.json"),
            ("priorSelection004Sha256", "docs/n1-sources/batch-124/selection-004.json"),
            ("priorAudit003Sha256", "docs/n1-sources/batch-124/author-audit-003.json"),
        ):
            require(blob(path) == previous(path) and sha(blob(path)) == history[key], "Historical evidence changed")
        clean(config, candidate)
        result = {
            "batch": 124, "status": "PASS", "candidate": candidate, "parent": PARENT,
            "initial": config["candidate"], "base": config["base"],
            "handoffSha256": sha(handoff_raw), "manifestSha256": manifest_sha,
            "contentVersion": manifest["contentVersion"], "runtimeEntries": len(current),
            "changedPaths": changes, "sourceReceiptSha256": sha(source_raw),
            "reusedCompleteSourceProof": {"path": str(first_path), "sha256": FIRST_PROOF_SHA},
            "sourceRecords": first["sourceRecords"],
            "signedArtifacts": {path: sha(blob(path)) for _, path in changes if path.startswith("docs/")},
            "runner": {"path": str(runner), "sha256": RUNNER_SHA}, "gateSets": gate_sets,
            "metadataStrokesSupportAndHistoricalEvidencePreserved": True,
            "sourceMembersPublishedBeforeBatch": 253, "sourceMembersInCandidate": 254,
            "signature": {"fingerprint": SIGNER, "ownerVerified": True}, "worktreeClean": True,
            "outstandingDocumentationCorrection": handoff["postSigningCoordinatorCorrection"],
            "limits": "Exact signed bytes and reuse of previously verified complete selections, plus both "
                      "new host gate sets only. No semantic, confirmation, device or publication acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Second correction verification RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(REVIEW / "coordinator-reconciliation-verification-002.json", result)))


if __name__ == "__main__":
    verify()
