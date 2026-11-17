"""Assemble an additive integration closure from real accepted confirmations."""
import copy
import json
import sys
from pathlib import Path

import b134_integrated_v2 as contract
from common import freeze_json, json_bytes, require, sha, start_guard, write_frozen
from verify_b134_packet import RUNNER
from verify_b134_sources import Git


def assemble(plan, plan_raw, previous, manifest, confirmations, evidence):
    files = {
        ".gitattributes": b"* -text\n",
        "previous-progress.json": previous,
        "plan.json": plan_raw,
        **evidence,
    }
    require(len(files) == len(evidence) + 3, "Evidence overwrites reserved archive paths")
    runs = []
    for family in ("claude", "gpt"):
        value = confirmations[family]
        runs.append(value["run"])
        for key in ("acceptance", "report", "final", "adjudication"):
            name = f"runs/{value['run']}/{key}.{'md' if key == 'report' else 'json'}"
            require(name not in files, "Duplicate confirmation evidence")
            files[name] = value[key]
    limits = [
        "Integration-impact confirmation only, not a fresh whole-corpus review "
        "or independent certification of the unrelated counter correction.",
        "All earlier N1 verdicts, coordinator decisions, source qualifications, "
        "51 Notes warnings and native/device/custom-pool limits remain intact.",
        "Both incoming content blobs are preserved exactly; the manifest is "
        "regenerated. No N1 teaching, source record or prior review is changed.",
        "Publication and exact served-archive checks remain outstanding; this "
        "integration closure grants no delivery credit.",
    ]
    runtime = {
        "manifestSha256": sha(manifest),
        "contentVersion": json.loads(manifest)["contentVersion"],
        "runtimeEntries": len(contract.runtime_entries(json.loads(manifest))),
    }
    require(runtime["runtimeEntries"] == 8747, "Unexpected runtime membership")
    provenance = {
        "batch": 134, "reviewedSnapshot": plan["merge"],
        "previousReviewedSnapshot": contract.REVIEWED,
        "parents": [plan["signedClosure"], contract.INCOMING],
        "runtimeCandidate": runtime, "finalRuns": runs,
        "publication": "PENDING", "deliveryCredit": 0, "limits": limits,
        "recordedFileSha256": {name: sha(raw) for name, raw in sorted(files.items())},
    }
    files["provenance.json"] = json_bytes(provenance)
    files["validation-provenance.json"] = json_bytes({
        "candidate": plan["merge"],
        "reviewClosureSha256": sha(files["provenance.json"]),
        "planSha256": sha(plan_raw),
        "recordedFileSha256": {},
        "scope": "Exact accepted evidence, original/merge gates, object "
                 "preservation and additive ledger checks; no publication acceptance.",
    })
    ledger = copy.deepcopy(json.loads(previous))
    require(not contract.EXTENSION_KEYS & set(ledger), "Integration already recorded")
    ledger.update(
        activeReviewedSnapshot=plan["merge"],
        integrationReview={
            "reviewedSnapshot": plan["merge"],
            "previousReviewedSnapshot": contract.REVIEWED,
            "parents": provenance["parents"],
            "status": "closed-with-disclosed-limits",
            "runtimeCandidate": runtime, "finalRuns": runs,
            "closurePath": contract.INTEGRATION.rstrip("/"),
            "closureProvenanceSha256": sha(files["provenance.json"]),
            "validationProvenanceSha256": sha(files["validation-provenance.json"]),
            "limits": limits,
        },
    )
    contract.closure_data(plan, json.loads(previous), ledger, files, manifest, confirmations)
    return files, json_bytes(ledger)


def main(mode, plan_path, output, preservation):
    require(mode in ("dry", "real"), "Use dry or real")
    require(output.parent == contract.REVIEW and not output.exists(), "Use a new review output")
    plan, plan_raw = contract.load_plan(plan_path)
    guard, _ = start_guard("B134 actual integration closure assembly")
    try:
        git = Git(contract.REPO, RUNNER, guard)

        def clean():
            require(git("rev-parse", "HEAD").decode().strip() == plan["merge"]
                    and not git("status", "--porcelain=v1", "--untracked-files=all"),
                    "Assembly requires the unchanged clean signed merge")

        clean()
        contract.merge(git, plan["signedClosure"], plan["merge"])
        contract.plan_gates(git, plan)
        confirmations = contract.accepted(plan)
        previous = contract.blob(git, plan["merge"], contract.PROGRESS)
        manifest = contract.blob(git, plan["merge"], "manifest.json")
        evidence = {"protocol/assemble-b134-integration.py": Path(__file__).read_bytes()}
        for group in ("originalGates", "mergeGates"):
            for name, ref in plan[group].items():
                evidence[f"verification/{group}/{name}.json"] = contract.read_ref(ref)
        evidence["protocol/tool-inventory.json"] = contract.read_ref(plan["toolInventory"])
        evidence["verification/preservation.json"] = contract.read_ref(preservation)
        kept = json.loads(evidence["verification/preservation.json"])
        require(kept["status"] == "PASS_MERGED_PRESERVATION_ONLY" and kept["candidate"] == plan["merge"]
                and kept["closure"] == plan["signedClosure"] and kept["incoming"] == contract.INCOMING
                and kept["reviewedSnapshot"] == contract.REVIEWED and not kept["memory"]["breach"],
                "Preservation verification does not bind this merge")
        files, ledger = assemble(plan, plan_raw, previous, manifest, confirmations, evidence)
        before = contract.tree(git, plan["merge"])
        staged = dict(before)
        staged[contract.PROGRESS] = ("100644", "blob", "prospective-progress")
        for name in files:
            path = contract.INTEGRATION + name
            require(path not in before, "Archive path already tracked")
            staged[path] = ("100644", "blob", "prospective-archive")

        def read(name):
            if name == contract.PROGRESS:
                return ledger
            if name.startswith(contract.INTEGRATION):
                return files[name[len(contract.INTEGRATION):]]
            return contract.blob(git, plan["merge"], name)

        contract.verify_closure(git, plan, plan["merge"], signed=False, staged=staged, read=read)
        clean()
        destination = (output / "archive" if mode == "dry"
                       else contract.REPO / contract.INTEGRATION)
        require(not destination.exists(), "Preserve existing integration archive")
        for name, raw in sorted(files.items()):
            write_frozen(destination / name, raw)
            guard.check()
        write_frozen(output / "expected-progress.json", ledger)
        if mode == "real":
            path = contract.REPO / contract.PROGRESS
            require(path.read_bytes() == previous, "Ledger changed before replacement")
            path.chmod(0o644)
            path.write_bytes(ledger)
            path.chmod(0o444)
            require(path.read_bytes() == ledger, "Ledger readback differs")
        result = {
            "status": "PASS_ADDITIVE_INTEGRATION_ASSEMBLY",
            "mode": mode, "merge": plan["merge"], "planSha256": sha(plan_raw),
            "archiveFiles": len(files), "ledgerSha256": sha(ledger),
            "closureSha256": sha(files["provenance.json"]),
            "publicationAccepted": False, "deliveryCredit": 0,
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Integration assembly RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(output / "assembly.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 6, "assemble-b134-integration-v2.py dry|real PLAN NEW_REVIEW_OUTPUT "
                                "PRESERVATION_JSON PRESERVATION_SHA256")
    main(sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(),
         {"path": str(Path(sys.argv[4]).resolve()), "sha256": sys.argv[5]})
