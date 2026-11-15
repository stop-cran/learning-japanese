"""Verify the additive C1 follow-up while retaining B123's first-revision proof."""
import json
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import clean
from verify_b123_revision_v2 import (CARD, SIGNER, STROKES, WORD, check_gate,
                                    check_metadata, check_runtime, check_summary, verify_sources)

sys.path.insert(0, str(WS / "lean"))
from n1lib import parse

PARENT = "65f04ca52a310d517ecb05fb17434cb4f41a118d"
PREFIX = "docs/n1-sources/batch-123/reconciliation-002/"
PRIOR_PROOF = WS / "scratch-123" / "review" / "coordinator-reconciliation-verification-001.json"
PRIOR_SHA = "7bd65759c91939c536dfb03a00ff461fcbc30a0f293b5ddb78d7fb0f404f3f20"


def check_followup_metadata(before, after):
    check_metadata(before, after)
    require(after["quiz_exclusions"] == [*before["quiz_exclusions"], "普"],
            "Follow-up must append only the focused 普 guard")


def check_delta(changes):
    sources = []
    runtime = set()
    for line in changes.splitlines():
        status, path = line.split("\t")
        require((status == "M" and path in (CARD, "manifest.json"))
                or (status == "A" and path.startswith(PREFIX)),
                f"Unexpected or non-additive follow-up delta: {line}")
        if status == "A":
            sources.append(path)
        else:
            runtime.add(path)
    require(runtime == {CARD, "manifest.json"} and sources, "Incomplete follow-up delta")
    return sources


def verify(candidate, gates, runner, output):
    config = load_batch(123)
    prior = json.loads(frozen(PRIOR_PROOF, PRIOR_SHA))
    require(prior["status"] == "PASS" and prior["candidate"] == PARENT
            and prior["initial"] == config["candidate"] and prior["base"] == config["base"],
            "First-revision proof binding differs")
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P", candidate).decode().strip() == PARENT,
            "Expected a non-rewriting direct child of the first reconciliation")
    require(git(config, "show", "-s", "--format=%P", PARENT).decode().strip() == config["candidate"],
            "First-revision ancestry differs")
    identity = git(config, "show", "-s", "--format=%GF%n%B", candidate).decode("utf-8").splitlines()
    require(identity[0] == SIGNER
            and "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>" in identity,
            "Signing fingerprint or trailer differs")
    runner_sha = sha(frozen(runner))
    guard, _ = start_guard("B123 focused signed follow-up verification")
    try:
        blob = lambda commit, path: git(config, "show", f"{commit}:{path}")
        raw_manifest = blob(candidate, "manifest.json")
        manifest = json.loads(raw_manifest)
        current = check_runtime(json.loads(blob(config["base"], "manifest.json")), manifest)
        require(len(current) == prior["runtimeEntries"] == 8708, "Runtime membership differs")
        before, _ = parse(blob(PARENT, CARD).decode("utf-8").replace("\r\n", "\n"))
        after, _ = parse(blob(candidate, CARD).decode("utf-8").replace("\r\n", "\n"))
        check_followup_metadata(before, after)
        for character in [*after["distractors"], *after["quiz_exclusions"]]:
            require(f"kanji/{character}.md" in current, f"Unresolved counterpart: {character}")
        for path in (STROKES, WORD):
            require(blob(candidate, path) == blob(PARENT, path), f"Preserved runtime changed: {path}")
        for path in (CARD, STROKES, WORD):
            require(sha(blob(candidate, path).replace(b"\r\n", b"\n")) == current[path],
                    f"Manifest hash differs: {path}")
        delta = git(config, "diff", "--name-status", "--no-renames", PARENT, candidate).decode("utf-8")
        source_paths = check_delta(delta)
        source_proof = verify_sources(config, candidate, source_paths, guard)
        summary_raw = frozen(gates / "summary.json")
        summary = json.loads(summary_raw)
        check_summary(summary, {**config, "candidate": PARENT}, candidate,
                      sha(raw_manifest), runner_sha)
        if "requiredParent" in summary:
            require(summary["requiredParent"] == PARENT, "Runner summary parent differs")
        receipts = []
        for name in CHECKS:
            raw, log = frozen(gates / f"{name}.json"), frozen(gates / f"{name}.log")
            check_gate(json.loads(raw), log, name, sha(raw_manifest), config["repo"], runner_sha)
            receipts.append({"gate": name, "receiptSha256": sha(raw), "logSha256": sha(log)})
            guard.check()
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Follow-up verification RAM breach")
    print(json.dumps(freeze_json(output, {
        "batch": 123, "status": "PASS", "candidate": candidate, "parent": PARENT,
        "initial": config["candidate"], "base": config["base"],
        "priorRevisionProof": {"path": str(PRIOR_PROOF), "sha256": PRIOR_SHA},
        "manifestSha256": sha(raw_manifest), "contentVersion": manifest["contentVersion"],
        "runtimeEntries": len(current), "newGuard": "普", "changedPathsFromParent": delta.splitlines(),
        "sourceProof": source_proof, "gates": receipts,
        "gateSummary": {"path": str(gates / "summary.json"), "sha256": sha(summary_raw)},
        "runner": {"path": str(runner), "sha256": runner_sha},
        "signature": {"fingerprint": SIGNER, "ownerVerified": True}, "worktreeClean": True,
        "firstRevisionTeachingAndSourcesPreservedExceptFocusedCardAndManifest": True,
        "sourceMembersPublishedBeforeBatch": 252, "sourceMembersInCandidate": 253,
        "memory": memory, "linguisticAcceptance": False, "publicationAccepted": False,
        "limits": "Signed additive C1 delta and complete newly selected records verified. "
                  "Exact new query selection and source-based reviewer confirmations remain separate.",
    })))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
