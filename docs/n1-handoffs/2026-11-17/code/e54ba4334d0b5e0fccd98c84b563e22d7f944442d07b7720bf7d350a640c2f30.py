"""Verify the additive signed response correction without relabeling earlier runtime gates."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from finalize_b124 import RESPONSE_PATHS, RUNTIME_PROOF_SHA, SIGNER

REVIEW = WS / "scratch-124" / "review"
PARENT = "be2aaeac504be19860a9a69de499d8202863bde9"
PREFIX = "docs/n1-sources/batch-124-reconciliation-002/"
REPORT_SHA = "8ab76aad27740967930beeae21050bbf2f54909aa67287e515722d5a9c958034"
ACCEPTANCE_SHA = "587370ad871542d9282db9ee8b76f8a25933dc126c526d6a59dcffb5b156e11d"
HANDOFF = WS / "scratch-124" / "response-correction-001-handoff.json"
R2_HANDOFF_SHA = "2e716aaa9955e2084b8366c5868da1c90c35f7ae031605ccdd8465d3eed1dc39"
BRIEF_SHA = "7eecd94344e719290b0c5723585b2d8fa497294f0548df1929e499e4a5d68037"
ADMISSION_SHA = "89876216164719d479652c18a69118e9edc2a5948441061c919ae2d5aac0821c"
CLOSED = {"reviewerContacted": False, "push": False, "published": False}


def check_handoff(value, candidate, base, blob, prior, tree, addendum):
    commit = value["commit"]
    require(commit["sha"] == candidate and commit["parent"] == PARENT and commit["publishedBase"] == base
            and commit["signatureVerified"] is True and commit["signingKeyFingerprint"] == SIGNER
            and commit["worktreeClean"] is True and commit["push"] is False and commit["amended"] is False,
            "Handoff commit identity differs")
    inventory = value["fileInventory"]
    require(inventory["count"] == 2 and set(inventory["exactPaths"]) == RESPONSE_PATHS
            and len(inventory["files"]) == 2
            and {item["path"] for item in inventory["files"]} == RESPONSE_PATHS
            and all(item["sha256"] == sha(blob(item["path"])) and item["bytes"] == len(blob(item["path"]))
                    for item in inventory["files"]), "Handoff inventory differs")
    require(value["correctionBindings"]["addendum"]["bindings"] == addendum, "Handoff addendum copy differs")
    history = value["preservedHistory"]
    require(history["verifiedR2Proof"]["sha256"] == RUNTIME_PROOF_SHA
            and history["priorR2Handoff"]["sha256"] == R2_HANDOFF_SHA
            and history["priorR2Handoff"]["candidate"] == PARENT
            and history["assignmentBrief"]["sha256"] == BRIEF_SHA
            and history["freshAdmission"]["sha256"] == ADMISSION_SHA, "Handoff history binding differs")
    for item in history["unchangedSourceAndRuntimeFiles"]:
        require(item["sameAsSignedParent"] is True
                and sha(blob(item["path"])) == sha(prior(item["path"])) == item["sha256"],
                f"Handoff preserved-file claim differs: {item['path']}")
    trees = value["runtimeByteEquality"]["trees"]
    require(set(trees) == {"kanji", "strokes", "words"}, "Handoff runtime tree set differs")
    for name, item in trees.items():
        require(item["byteIdentical"] is True
                and item["gitTree"] == item["parentGitTree"] == tree(candidate, name) == tree(PARENT, name),
                f"Handoff runtime tree claim differs: {name}")
    gates = value["newGateRuns"]
    require(gates["authoring"] == [] and gates["committed"] == [] and gates["priorR2RunsReusedAsEvidence"] is False
            and value["publication"] == CLOSED, "Handoff gate or publication attribution differs")


def check_delta(changes):
    require(len(changes) == 2 and {path for status, path in changes if status == "A"} == RESPONSE_PATHS,
            "The response correction must add exactly two documents and preserve every earlier file")


def check_addendum(value, blob, proof):
    require(value["signedParent"]["commit"] == PARENT
            and value["signedParent"]["verifiedParent"] == proof["parent"]
            and value["signedParent"]["signingKeyFingerprint"] == SIGNER, "Response parent differs")
    for key, name in (("original", "claude-response.md"), ("corrected", "claude-response-002.md")):
        item = value["responses"][key]
        require(item["path"] == PREFIX + name and item["sha256"] == sha(blob(item["path"])),
                f"Response binding differs: {key}")
    require(value["responses"]["original"]["preservedVerbatim"] is True, "Original response not preserved")
    binding = value["confirmationBinding"]
    require(binding["report"]["sha256"] == REPORT_SHA
            and binding["heldAcceptance"]["sha256"] == ACCEPTANCE_SHA,
            "Correction is bound to another report or acceptance")
    for item in binding.values():
        frozen(item["path"], item["sha256"])
    acceptance = json.loads(frozen(binding["heldAcceptance"]["path"], ACCEPTANCE_SHA))
    for key in ("reviewEvidenceAccepted", "confirmationAccepted", "acceptedNewFindings", "openClaimIds"):
        require(binding["heldAcceptance"][key] == acceptance[key], "Held acceptance was relabeled")
    require(binding["heldAcceptance"]["rawVerdict"] == acceptance["verdict"] == "CONFIRMED"
            and acceptance["confirmationAccepted"] is False, "Raw optional judgment was relabeled")
    for item in value["historicalBindingsUnchanged"].values():
        require(sha(blob(item["path"])) == item["sha256"], "Historical document binding differs")
    supersession = value["responseReferenceSupersession"]
    location, pointer = supersession["activeReferenceLocation"].split("#")
    require(location == "docs/n1-sources/batch-124/selection-005.json"
            and pointer == "reconciliation.reviewResponses.claude"
            and sha(blob(location)) == supersession["activeReferenceFileSha256"]
            and supersession["historicalResponseSha256"] == value["responses"]["original"]["sha256"]
            and supersession["successorResponseSha256"] == value["responses"]["corrected"]["sha256"],
            "Active response supersession changed unrelated provenance")
    runtime = value["unchangedRuntimeManifest"]
    require(runtime["path"] == "manifest.json"
            and runtime["sha256"] == sha(blob("manifest.json")) == proof["manifestSha256"]
            and runtime["contentVersion"] == proof["contentVersion"]
            and runtime["runtimeKanjiCardPath"] == "kanji/\u88d5.md"
            and runtime["runtimeKanjiCardSha256"] == sha(blob("kanji/\u88d5.md")),
            "Documentation addendum claims different runtime bytes")
    boundary = value["changeBoundary"]
    require(set(boundary["repositoryFilesAdded"]) == RESPONSE_PATHS
            and all(boundary[key] is False for key in (
                "runtimeChanged", "sourceRecordsChanged", "querySetChanged", "rawVerdictChanged",
                "progressCountChanged", "publicationStateChanged", "otherFamilyIncluded"))
            and value["gateRuns"]["newStandardGateSetsRun"] is False
            and value["publication"] == CLOSED,
            "Documentation scope or gate/publication attribution differs")


def verify(candidate, handoff_sha):
    config = load_batch(124)
    handoff = json.loads(frozen(HANDOFF, handoff_sha))
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P", candidate).decode().strip() == PARENT,
            "Documentation correction is not a direct successor")
    require(git(config, "show", "-s", "--format=%G?|%GF|%ae|%ce", candidate).decode().strip()
            == f"G|{SIGNER}|stop-cran@list.ru|stop-cran@list.ru", "Owner signature differs")
    require(b"Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"
            in git(config, "show", "-s", "--format=%B", candidate), "Co-author trailer missing")
    runtime_path = REVIEW / "coordinator-reconciliation-verification-002.json"
    proof = json.loads(frozen(runtime_path, RUNTIME_PROOF_SHA))
    require(proof["status"] == "PASS" and proof["candidate"] == PARENT and not proof["memory"]["breach"],
            "Runtime proof differs")
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    prior = lambda path: git(config, "show", f"{PARENT}:{path}")
    guard, _ = start_guard("B124 signed response attribution correction")
    try:
        changes = [line.split("\t") for line in git(
            config, "diff", "--name-status", "--no-renames", PARENT, candidate
        ).decode("utf-8").splitlines()]
        check_delta(changes)
        for path in ("manifest.json", "kanji/\u88d5.md", "words/\u4f59\u88d5.md", "strokes/\u88d5.json",
                     *proof["signedArtifacts"]):
            require(blob(path) == prior(path), f"Preserved source/runtime bytes changed: {path}")
            guard.check()
        addendum = json.loads(blob(PREFIX + "response-correction-001.json"))
        check_addendum(addendum, blob, proof)
        tree = lambda rev, name: git(config, "rev-parse", f"{rev}:{name}").decode().strip()
        check_handoff(handoff, candidate, config["base"], blob, prior, tree, addendum)
        response = blob(PREFIX + "claude-response-002.md").decode("utf-8")
        require(REPORT_SHA in response and "## Historical initial-report dispositions" in response
                and "## First confirmation's local O1" in response
                and "## First confirmation's local O2" in response
                and "not relabeled" in response and "earlier table" in response
                and "gpt" not in response.lower()
                and "initial report's optional acceptance" not in response,
                "Corrected response attribution or family isolation differs")
        clean(config, candidate)
        result = {
            "batch": 124, "status": "PASS", "candidate": candidate, "parent": PARENT,
            "initial": config["candidate"], "base": config["base"],
            "changedPaths": changes, "runtimeAndPriorEvidenceUnchanged": True,
            "runtimeProofSha256": RUNTIME_PROOF_SHA, "manifestSha256": proof["manifestSha256"],
            "contentVersion": proof["contentVersion"],
            "signedArtifacts": {path: sha(blob(path)) for path in sorted(RESPONSE_PATHS)},
            "signature": {"fingerprint": SIGNER, "ownerVerified": True}, "worktreeClean": True,
            "authorHandoff": {"path": str(HANDOFF), "sha256": handoff_sha},
            "newStandardGateSetsRun": False,
            "limits": "Exact additive documents, signature, attribution bindings and complete prior-tree preservation. "
                      "Earlier runtime gates remain attributed to be2aaeac, not this documentation-only successor. "
                      "No new semantic, confirmation, device or publication acceptance.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Documentation verification RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(REVIEW / "coordinator-response-correction-verification-001.json", result)))


if __name__ == "__main__":
    verify(sys.argv[1], sys.argv[2])
