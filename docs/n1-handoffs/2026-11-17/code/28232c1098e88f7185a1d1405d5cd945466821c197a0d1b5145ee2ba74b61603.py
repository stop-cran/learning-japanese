"""Record delivery of I, the contributor-only child of confirmed integrated M.

Unlike the linear B134 recorder, original review/manifest/accounting values remain
historical; activeReviewedSnapshot/integrationReview select M. Modeled on B130 v2,
with explicit frozen plan, pre/post integration-closure gates and exact file inventory.
Only the explicit record CLI writes receipt artifacts/ledger and drafts an issue request;
it never signs, commits, pushes, or posts. Subsequent receipt CI/ZIP/equality are required.

Usage: PLAN I CI_RUN_ID ZIP_RECEIPT NARRATIVE PRE_CLOSURE_GATES COMMITTED_CLOSURE_GATES NEW_OUT
"""
import json
import sys
from pathlib import Path

import b134_integrated_v1 as contract
import deliver_b134_integration_v1 as delivery
from common import freeze_json, frozen, json_bytes, require, sha, start_guard, write_frozen
from record_b117_publication_v3 import validate_delivery
from record_b130_publication import comment_body, load_narrative
from verify_b134_packet import RUNNER
from verify_b134_sources import Git


def record(plan_path, commit, run_id, zip_path, narrative_path, pre_gates, committed_gates, out):
    require(run_id.isdigit(), "Use numeric CI run ID")
    plan, plan_raw = contract.load_plan(Path(plan_path))
    output = delivery.new_output(out)
    target = contract.REPO / contract.PUBLICATION
    require(not target.exists(), "Preserve existing receipt attempt")
    narrative = load_narrative(Path(narrative_path))
    guard, _ = start_guard("B134 integrated publication recorder")
    try:
        git = Git(contract.REPO, RUNNER, guard)
        delivery.clean(git, commit)
        context = contract.verify_closure(git, plan, commit)
        contract.plan_gates(git, plan)
        delivery.remote_head(git, commit)
        remote = delivery.remote_commit(git, commit)
        manifest = contract.blob(git, commit, "manifest.json")
        ci_raw = delivery.api(git, "run", "view", run_id, "--repo", delivery.REPOSITORY, "--json",
                              "databaseId,headSha,status,conclusion,url,workflowName,jobs,createdAt,updatedAt")
        ci = json.loads(ci_raw)
        require(ci["databaseId"] == int(run_id) and ci["workflowName"] == "Validate content",
                "Wrong CI workflow/run")
        zip_raw = frozen(zip_path)
        archive = json.loads(zip_raw)
        validate_delivery(commit, manifest, ci, archive)
        from run_b134_integration_gates_v1 import tree_digest
        gates, gate_refs = {}, {}
        for mode, path, head in (("closure", pre_gates, plan["merge"]),
                                 ("committed-closure", committed_gates, commit)):
            ref = {"path": str(Path(path).resolve()), "sha256": sha(frozen(path))}
            raw = delivery.closure_gate(ref, mode, plan, head, manifest)
            require(json.loads(raw)["treeInventorySha256"] == tree_digest(contract.tree(git, commit)),
                    "Closure gates describe another tree")
            gates[mode] = raw
            gate_refs[mode] = ref
        old_raw = contract.blob(git, commit, contract.PROGRESS)
        ledger = json.loads(old_raw)
        require((contract.REPO / contract.PROGRESS).read_bytes() == old_raw, "Ledger differs from signed blob")
        index = json.loads(contract.blob(git, commit, "docs/n1-sources/source-index.json"))
        pending = {row["kanji"] for row in index if row["statusAtFreeze"] == "pending"}
        present = {Path(p).stem for p in contract.runtime_entries(json.loads(manifest)) if p.startswith("kanji/")}
        require(len(pending) == 1228 and len(pending & present) == 272 and "\u7d2b" in pending & present,
                "Published pending-source membership differs")
        counts = {"delivered": 272, "n1Additions": 266, "n2Placements": 6, "remaining": 956}
        limits = list(dict.fromkeys([*ledger["limits"], *context["integrationLimits"],
                                    "This verifies only this integrated published runtime, not the remaining N1 set.",
                                    "The contributor-only receipt still needs CI, exact ZIP and served-tree equality."]))
        # All checks and a second remote observation precede any repository writes.
        delivery.clean(git, commit)
        delivery.remote_head(git, commit)
        files = {".gitattributes": b"* -text\n", "ci-run.json": ci_raw, "zip-receipt.json": zip_raw}
        for mode, raw in gates.items():
            files[f"gates/{mode}/summary.json"] = raw
            for name in contract.ORDER:
                for suffix in ("json", "log"):
                    files[f"gates/{mode}/{name}.{suffix}"] = frozen(
                        Path(gate_refs[mode]["path"]).parent / f"{name}.{suffix}")
        proof = {
            "schemaVersion": 1, "batch": 134, "status": delivery.STATUS,
            "publishedCommit": commit, "publishedCommitUrl": remote["html_url"],
            "base": contract.BASE, "initialSnapshot": "ba80afffc20a72d31be68b355b6f90aab36a5726",
            "reviewedSnapshot": contract.REVIEWED, "activeReviewedSnapshot": plan["merge"],
            "signedOriginalClosure": plan["signedClosure"], "incoming": contract.INCOMING,
            "planSha256": sha(plan_raw), "context": context,
            "ci": {"runId": ci["databaseId"], "url": ci["url"], "sha256": sha(ci_raw)},
            "archive": {"zipSha256": archive["sha256"], "receiptSha256": sha(zip_raw),
                        "verifiedRuntimeHashes": archive["verifiedRuntimeHashes"],
                        "contentVersion": archive["contentVersion"]},
            "sourceAccounting": {**counts, "overallN1TaskComplete": False},
            "limits": limits, "recordedFileSha256": {name: sha(raw) for name, raw in files.items()},
            "gateRefs": gate_refs,
            "recorderSha256": sha(frozen(Path(__file__))),
        }
        # Build the sole allowed publication ledger delta without overwriting historical review keys.
        published = json.loads(old_raw)
        published.update(status=delivery.STATUS, published=["\u7d2b"], runtimePublished=True, limits=limits)
        published["accounting"].update(publishedPendingRecordsWithCards=272, publishedN1Additions=266, undelivered=956)
        published["publication"] = {
            "commit": commit, "url": remote["html_url"],
            "receipt": "../n1-reviews/batch-134-integration-publication-001/provenance.json"}
        delivery.published_ledger(ledger, published, commit, proof)
        output.mkdir()
        write_frozen(output / "previous-progress.json", old_raw)
        for name, raw in files.items():
            write_frozen(target / name, raw)
        freeze_json(target / "provenance.json", proof)
        path = contract.REPO / contract.PROGRESS
        path.chmod(0o644)
        path.write_bytes(json_bytes(published))
        require(path.read_bytes() == json_bytes(published), "Ledger readback failed")
        path.chmod(0o444)
        body = comment_body(134, ["\u7d2b"], commit, remote["html_url"], ci["url"], archive, counts, narrative)
        body += (f"\n\nConcurrent main `{contract.INCOMING}` is preserved by the signed merge "
                 f"`{plan['merge']}`; both integration-impact confirmations and the original review "
                 "remain snapshot-specific. Incoming counter-language correctness is not newly certified.")
        freeze_json(output / "issue60-request.json", {
            "body": body, "publishedCommit": commit, "planSha256": sha(plan_raw)})
        freeze_json(output / "record.json", {
            "status": "RECEIPT_WRITTEN_NOT_SIGNED", "publishedCommit": commit,
            "planSha256": sha(plan_raw), "provenanceSha256": sha(frozen(target / "provenance.json")),
            "previousLedgerSha256": sha(old_raw), "updatedLedgerSha256": sha(frozen(path)),
            "publicationAccepted": False, "limits": "Receipt signature/push, CI/ZIP/equality and issue checkpoint remain."})
    finally:
        require(not guard.finish()["breach"], "Recorder RAM breach")


if __name__ == "__main__":
    require(len(sys.argv) == 9, __doc__)
    record(*sys.argv[1:])
