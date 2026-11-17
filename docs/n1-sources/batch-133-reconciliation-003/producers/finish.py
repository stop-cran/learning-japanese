import json
import os
import stat
import sys
from datetime import datetime, timezone
from pathlib import Path

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT.parent))
from common_133 import REPO, git, sha, start_guard, write
from notes import PARENT, REL


def load(path):
    return json.loads(path.read_bytes())


def binding(path):
    return {"path": str(path), "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}


def main():
    current_outer = OUT.parent / "review" / "teaching3-freeze-001"
    guard = start_guard()
    try:
        revision = load(OUT / "revision.json")
        head = git("rev-parse", "HEAD").decode().strip()
        assert head == revision["revision"] and git("rev-parse", "HEAD^@").decode().split() == [PARENT]
        git("verify-commit", "HEAD")
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
        for directory in ("author-gates-001", "committed-gates-001", "packaged-preservation-001", "committed-preservation-001"):
            assert load(OUT / directory / "summary.json")["status"] == "PASS"
        assert load(OUT / "committed-preservation-001" / "summary.json")["unchangedRuntimeEntries"] == 8744
        reading = (OUT / "committed-gates-001" / "reading-exposure.log").read_text(encoding="utf-8")
        assert "0 production hit(s)" in reading and "0 padded-session hit(s)" in reading and "1 latent collision(s)" in reading
        copied = []
        for directory in sorted((OUT.parent / "review").glob("teaching3-*")):
            if directory == current_outer:
                continue
            receipt = directory / "receipt.json"
            expected_exit = 1 if directory.name == "teaching3-prepare-001" else 0
            assert load(receipt)["exitCode"] == expected_exit
            assert load(receipt)["memory"]["breach"] is None
            for path in sorted(directory.iterdir()):
                guard.check()
                if path.is_file():
                    destination = OUT / "guarded-runs" / directory.name / path.name
                    write(destination, path.read_bytes())
                    assert path.read_bytes() == destination.read_bytes()
                    os.chmod(path, stat.S_IREAD)
                    copied.append(binding(path))
        for path in sorted((REPO / REL).rglob("*")):
            guard.check()
            if path.is_file():
                os.chmod(path, stat.S_IREAD)
                assert path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
        packet_inventory = REPO / REL / "inventory.json"
        assert sha(packet_inventory.read_bytes()) == revision["reconciliationInventorySha256"]
        handoff = {
            **revision, "status": "PASS_SIGNED_LOCAL_HANDOFF",
            "gateSummary": binding(OUT / "committed-gates-001" / "summary.json"),
            "authorGateSummary": binding(OUT / "author-gates-001" / "summary.json"),
            "preservationSummary": binding(OUT / "committed-preservation-001" / "summary.json"),
            "preservationWrapperBinding": binding(OUT / "committed-preservation-001" / "wrapper-binding.json"),
            "reconciliationInventory": binding(packet_inventory),
            "sourceBindings": binding(OUT / "source-bindings.json"),
            "preservedPreparationFailure": load(OUT / "source-bindings.json")["preparationFailure"],
            "addedExclusions": {"滝": ["酒"]}, "retainedExclusion": ["滝", "液"],
            "correctedGloss": "The abbreviation is たきすい, a named sake sold in Edo, not waterfall-water readings たきみず/ろうすい; both faulty glosses superseded only in the new teaching snapshot.",
            "runtimeEntries": 8745, "unchangedRuntimeEntries": 8744,
            "fullOrderedTenGatesPassedBeforeAndAfterSigning": True,
            "earlierEvidenceAndAllOtherTrackedPathsUnchanged": True,
            "externalCompletedRunCopies": copied,
            "finalOuterRunner": {
                "directory": str(current_outer), "outsideLocalInventory": True,
                "files": ["output.log", "receipt.json"],
                "reason": "Final running launcher's files cannot be self-inventoried/finalized while its child runs; hash and set ReadOnly after launcher completion, reporting separately."
            },
            "warnings": [
                "One preexisting latent うるおす/湿 reading relation remains; not drawable in modeled production/Starter pools, including one-holder borrowing.",
                "Bounded host/static checks are not arbitrary/custom or multiple-borrow-pool, Kotlin/native/device, rendering, whole-set or publication acceptance.",
                "Earlier original/fresh-context reviewer verdicts remain preserved. New cumulative-delta confirmation remains coordinator-owned; this is not review closure.",
                "No refetch: frozen coordinator capture/extraction reproduced byte-for-byte; full captures/sections remain local, bounded attributable excerpts and bindings committed.",
                "Initial pre-edit source preparation failed on CRLF-vs-LF literals; original producer/output/receipt preserved. A separate verified successor normalized runtime text only; no gate failure or source rewrite."
            ],
            "published": {"delivered": 268, "total": 1228, "remaining": 960, "publication": False},
            "noPushNoReviewersNoNewAgentsNoNextBatch": True
        }
        write(OUT / "handoff.json", handoff)
        assert not git("status", "--porcelain=v1", "--untracked-files=all")
    finally:
        write(OUT / "finish-memory.json", guard.finish())
    inventory = {}
    for path in sorted(OUT.rglob("*")):
        if path.is_file():
            os.chmod(path, stat.S_IREAD)
            inventory[str(path.relative_to(OUT))] = {
                "sha256": sha(path.read_bytes()), "bytes": path.stat().st_size, "readOnly": True
            }
    write(OUT / "inventory.json", {
        "files": inventory, "selfExcluded": True,
        "createdAfterAllOtherOutputsReadOnlyAt": datetime.now(timezone.utc).isoformat(),
        "finalOuterRunnerOutsideInventory": str(current_outer)
    })
    os.chmod(OUT / "inventory.json", stat.S_IREAD)
    actual = {str(path.relative_to(OUT)) for path in OUT.rglob("*") if path.is_file()}
    assert actual == set(inventory) | {"inventory.json"}
    for relative, info in inventory.items():
        path = OUT / relative
        assert path.stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
        assert sha(path.read_bytes()) == info["sha256"] and path.stat().st_size == info["bytes"]
    assert (OUT / "inventory.json").stat().st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
    print(json.dumps({
        "status": "PASS_FROZEN_HANDOFF", "revision": head, "parent": PARENT,
        "gateSummary": handoff["gateSummary"], "preservationSummary": handoff["preservationSummary"],
        "reconciliationInventory": handoff["reconciliationInventory"],
        "localInventory": binding(OUT / "inventory.json"), "localFrozenFiles": len(inventory) + 1,
        "finalOuterRunnerOutsideInventory": str(current_outer)
    }))


if __name__ == "__main__":
    main()
