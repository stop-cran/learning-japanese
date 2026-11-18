"""Reproduce the held preparation's byte proof without rewriting its frozen results."""
import json
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-133" / "review"
HERE = ROOT / "neutral-preparation-003"
sys.path.insert(0, str(WS / "review-tools"))
from common import freeze_json, frozen, require, sha, start_guard

MANIFEST_SHA = "d80374b3cf50876d418869821ebf02fcb115cccf0654e560c429e99f86e0e263"
FINAL_SHA = "82a3979a196dcde2f95af29f5211050594fe69c753b036b53f432a08e024388d"
HANDOFF_SHA = "a00efba0b4aca64a1e7b4ef6972999eee12a112f25e042f36b215269e76081d0"
BRIEF = Path(r"C:\Users\stop-\.copilot\session-state\2451b10d-02a9-46ab-82d5-d90993f0cb8b\files\b133-review-preparation-004-brief.txt")
BRIEF_SHA = "921cf0ce01f23beb58c181cffb56b317389b91d4bd6eb119a3bfbc227f455b2e"


def main():
    guard, _ = start_guard("B133 coordinator held-preparation verification")
    try:
        manifest = json.loads(frozen(HERE / "PREPARATION-SHA256SUMS-001.json", MANIFEST_SHA))
        require(len(manifest) == 1554, "Unexpected preparation inventory")
        require({p.relative_to(HERE).as_posix() for p in HERE.rglob("*") if p.is_file()}
                == set(manifest) | {"PREPARATION-SHA256SUMS-001.json", "final-static-verification-001.json"},
                "Unexpected final preparation file")
        for name, digest in manifest.items():
            path = HERE / name
            require(path.resolve().is_relative_to(HERE.resolve()), "Unsafe manifest path")
            frozen(path, digest)
            guard.check()
        final = json.loads(frozen(HERE / "final-static-verification-001.json", FINAL_SHA))
        frozen(HERE / "COORDINATOR-HANDOFF-001.txt", HANDOFF_SHA)
        frozen(BRIEF, BRIEF_SHA)
        require(final["status"] == "PASS_FROZEN_COMPLETE_NEUTRAL_PREPARATION_CAPACITY_HOLD"
                and final["actualReviewersLaunched"] == 0, "Held preparation status differs")
        reference = json.loads(frozen(HERE / "complete-verification-001.json"))
        producer = HERE / "tools" / "verify-b133-neutral-complete-002.py"
        namespace = {"__name__": "coordinator_reproduction", "__file__": str(producer)}
        exec(compile(frozen(producer).decode(), str(producer), "exec"), namespace)
        reproduced = []

        def compare_only(path, result):
            require(path == HERE / "complete-verification-001.json" and result == reference,
                    "Independent complete byte proof did not reproduce")
            reproduced.append(result)
            return {"status": result["status"], "reproducedExactly": True}

        namespace["freeze_json"] = compare_only
        namespace["main"]()
        require(len(reproduced) == 1, "Missing reproduced proof")
        receipts = json.loads(frozen(HERE / "execution-bindings-001.json"))
        verified_receipts = []
        for item in receipts["successfulExecutions"].values():
            path = Path(item["path"])
            receipt = json.loads(frozen(path, item["sha256"]))
            frozen(path.parent / "output.log", receipt["logSha256"])
            require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 0
                    and not receipt["memory"]["breach"] and receipt["cleanupError"] is None,
                    "Failed successful-execution receipt")
            verified_receipts.append(str(path))
        controls = json.loads(frozen(HERE / "controller-validation-001.json"))
        require(controls["positive"]["syntheticOnly"] is True
                and controls["positive"]["finalNegativeControls"] == 4, "Synthetic control scope differs")
        for row in controls["wrapperRejections"]:
            receipt = json.loads(frozen(row["receipt"]["path"], row["receipt"]["sha256"]))
            log = frozen(Path(row["receipt"]["path"]).parent / "output.log", receipt["logSha256"])
            require(row["exitCode"] == receipt["exitCode"] == 1
                    and b"Startup capacity estimate failed" in log, "Wrong wrapper rejection")
        for family in ("claude", "gpt"):
            item = final["startup"][family]
            require(item["status"] == "HOLD_ESTIMATE" and item["estimatedUpper"] > item["limit"] == 700000,
                    "Held forecast admitted")
        for item in final["readiness"]:
            require(not Path(item["report"]).exists() and not any(Path(item["parent"]).iterdir()),
                    "Actual report destination no longer empty")
        result = {
            "status": "PASS_REPRODUCED_003_HOLD_NOT_REVIEW_ADMISSION",
            "candidate": reference["candidate"], "base": reference["base"],
            "staticFilesVerified": len(manifest), "packetFiles": reference["packetFiles"],
            "counts": reference["counts"], "completeByteProofReproducedExactly": True,
            "manifestSha256": MANIFEST_SHA, "finalStaticVerificationSha256": FINAL_SHA,
            "handoffSha256": HANDOFF_SHA, "successfulExecutionReceipts": verified_receipts,
            "wrapperRejectionsVerified": len(controls["wrapperRejections"]),
            "nextBriefSha256": BRIEF_SHA,
            "limits": "Accepts 003 only as preserved held preparation. No semantic review, reviewer admission or publication.",
        }
        print(json.dumps(freeze_json(ROOT / "coordinator-preparation003-verification-001.json", result)))
    finally:
        require(not guard.finish()["breach"], "Coordinator verification RAM breach")


if __name__ == "__main__":
    main()
