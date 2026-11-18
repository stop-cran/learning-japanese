"""Bind coordinator revision002 scope/gate proofs, without rerunning their checks.

No producer execution, signing, tree/index writes or semantic acceptance. The exact
two producer scripts are pinned; supplied immutable proof copies and signed Git
objects must agree. Actual proof hashes are parameters, never forecast placeholders.
"""
import json
from pathlib import Path

import b134_integrated_v1 as base
from common import WS, frozen, require, sha
from verify_b134_gates import memory_ok

PRODUCERS = {
    "scope": (Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\verify-b134-revision002.py"),
              "328b5281659b6dd9f049cf05cc8219fe56843aa952f315c1e7bb4d331ba17b6b"),
    "gates": (Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\verify-b134-revision002-gates.py"),
              "a30355caeb0f948c2460fc4c274eed0f81bef505c5a01917e5422d9a4fdd8a1c"),
}
CARD = "kanji/\u7d2b.md"


def read(item):
    return frozen(item["path"], item["sha256"])


def verify(git, candidate, scope_ref, gate_ref):
    for path, digest in PRODUCERS.values():
        frozen(path, digest)
    scope_raw, gate_raw = read(scope_ref), read(gate_ref)
    scope, gates = json.loads(scope_raw), json.loads(gate_raw)
    require(scope["batch"] == gates["batch"] == 134 and scope["status"] == gates["status"] == "PASS"
            and scope["reviewed"] == base.REVIEWED and scope["commit"] == gates["candidate"] == candidate
            and scope["lineageDepth"] == 1 and scope["verifierSha256"] == PRODUCERS["scope"][1]
            and gates["verifierSha256"] == PRODUCERS["gates"][1] and gates["sourceProof"] == scope_ref,
            "Missing actual descendant scope/gate producer binding")
    memory_ok(scope["memory"]); memory_ok(gates["memory"])
    base.identity(git, candidate, [base.REVIEWED])
    before, after = base.tree(git, base.REVIEWED), base.tree(git, candidate)
    require(before.keys() <= after.keys(), "Coordinator-proven revision removed objects")
    changed = {p: sha(base.blob(git, candidate, p)) for p in after if before.get(p) != after[p]}
    require(changed == scope["signedFiles"]
            and {p for p in before if before[p] != after[p]} == {CARD, "manifest.json"}
            and scope["card"]["priorExclusions"] == 56 and scope["card"]["exclusions"] == 58
            and sorted(after.keys() - before.keys()) == scope["evidencePaths"],
            "Actual revision objects differ from the coordinator scope proof")
    for path, item in scope["bindings"].items():
        require(path.startswith("snapshot/") and path[9:] in changed
                and sha(read(item)) == changed[path[9:]], "Scope signed snapshot binding differs")
    require(set(scope["bindings"]) == {"snapshot/" + p for p in changed}, "Scope snapshot inventory incomplete")
    manifest_sha = changed["manifest.json"]
    require(gates["manifestSha256"] == manifest_sha and set(gates["groups"]) == {"working", "committed"},
            "Actual revision gate groups or manifest differs")
    evidence = {name: read(item) for name, item in gates["evidence"].items()}
    expected_names = {"scope-proof.json"} | {
        f"{mode}/{name}.{suffix}" for mode in ("working", "committed")
        for name in base.ORDER for suffix in ("json", "log")} | {
        f"{mode}/summary.json" for mode in ("working", "committed")}
    require(set(evidence) == expected_names and evidence["scope-proof.json"] == scope_raw,
            "Actual gate proof lost immutable captured evidence")
    for mode, group in gates["groups"].items():
        summary_raw = evidence[mode + "/summary.json"]
        summary = json.loads(summary_raw)
        require(group["summarySha256"] == sha(summary_raw) and group["quizWarnings"] == 51
                and group["latentReadingPairs"] == 1 and summary["mode"] == mode
                and summary["head"] == (base.REVIEWED if mode == "working" else candidate)
                and summary["manifestSha256"] == manifest_sha and summary["checks"] == base.ORDER
                and [row["gate"] for row in group["gates"]] == base.ORDER,
                "Actual cumulative gate summary binding differs")
        for row in group["gates"]:
            name = row["gate"]
            for suffix, key in (("json", "receiptSha256"), ("log", "logSha256")):
                require(sha(evidence[f"{mode}/{name}.{suffix}"]) == summary["logs"][name][key] == row[key],
                        "Captured actual gate bytes differ")
    return {"status": "BOUND_ACTUAL_COORDINATOR_REVISION_PROOFS_ONLY", "candidate": candidate,
            "priorSnapshot": base.REVIEWED, "scopeProof": scope_ref, "gateProof": gate_ref,
            "manifestSha256": manifest_sha, "runtimeEntries": scope["manifest"]["runtimeEntries"],
            "scopeProducerSha256": PRODUCERS["scope"][1], "gateProducerSha256": PRODUCERS["gates"][1],
            "semanticAcceptance": False, "publicationAccepted": False}
