"""Verify the frozen final handoff and bind independently reproduced proofs."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

ROOT = WS / "scratch-134" / "review"
PREP = ROOT / "neutral-preparation-001"
HERE = PREP / "projected-successor-001"
MANIFEST_SHA = "6810a95659092a5e119a21dfa29412d540354edb1405c5b46b060cb3872d9dbb"
FINAL_SHA = "08ca555e19656801105ffe781fca72bc59ee62bc8899aa60cdc4ab6989317a15"
HANDOFF_SHA = "117aaf90e0c07d9ebb4a0dde025fd94b1bf6f3b998acbb26791c666da2dda49f"
RUNNER_SHA = "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"


def load(path, digest=None):
    return json.loads(frozen(path, digest))


def verify_receipt(path, digest, exit_code):
    row = load(path, digest)
    frozen(Path(path).parent / "output.log", row["logSha256"])
    require(row["runnerSha256"] == RUNNER_SHA and row["guardSha256"] == GUARD_SHA
            and row["exitCode"] == row["childExitCodeAfterCleanup"] == exit_code
            and row["cleanupError"] is None and not row["memory"]["breach"]
            and row["waitTimeoutSeconds"] <= .1 and row["cleanupTimeoutSecondsPerStage"] <= 10,
            "Execution receipt integrity, outcome or resource bound differs")
    return row


def main():
    guard, _ = start_guard("B134 independent final preparation verification")
    try:
        manifest_path = PREP / "PREPARATION-SHA256SUMS-001.json"
        manifest = load(manifest_path, MANIFEST_SHA)
        final = load(HERE / "final-static-verification-001.json", FINAL_SHA)
        frozen(HERE / "COORDINATOR-HANDOFF-001.txt", HANDOFF_SHA)
        actual = {p.relative_to(PREP).as_posix() for p in PREP.rglob("*") if p.is_file()}
        require(len(manifest) == 3181 and actual == set(manifest) | {
            "PREPARATION-SHA256SUMS-001.json", "projected-successor-001/final-static-verification-001.json"},
            "Preparation inventory changed")
        for name, digest in manifest.items():
            path = PREP / name
            require(path.resolve().is_relative_to(PREP.resolve()), "Unsafe preparation member")
            frozen(path, digest)
            guard.check()
        require(final["candidate"] == "ba80afffc20a72d31be68b355b6f90aab36a5726"
                and final["base"] == "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
                and final["status"] == "PASS_FINAL_FROZEN_NEUTRAL_PREPARATION_NOT_REVIEW_ADMISSION"
                and final["preparationManifestSha256"] == MANIFEST_SHA
                and final["handoffSha256"] == HANDOFF_SHA and not final["memory"]["breach"],
                "Final preparation identity differs")
        capacity_path = ROOT / "independent-capacity-verification-001.json"
        capacity = load(capacity_path, "9c01cbff4a5344dd1030c35233142effdccb1e125dafd5d32a7f9c8f611c7971")
        source_path = ROOT / "independent-neutral-source-verification-001.json"
        source = load(source_path, "e0ed11a6d6f63cc6ed53d1ee5aa4c6722862c28004226bbf4041220b0790f167")
        require(source["reproducedProof"]["sha256"] == sha(frozen(HERE / "complete-verification-001.json"))
                and capacity["packetManifestSha256"] == sha(frozen(HERE / "packet" / "SHA256SUMS.json"))
                and capacity["capacitySha256"] == sha(frozen(HERE / "capacity-measurement-001.json")),
                "Independent evidence no longer binds final inputs")
        executions = load(HERE / "execution-bindings-001.json")["executions"]
        require(len(executions) == 26 and len({row["path"] for row in executions}) == 26,
                "Execution inventory differs")
        for row in executions:
            receipt = verify_receipt(row["path"], row["sha256"], row["exitCode"])
            require(row["command"] == receipt["command"] and row["logSha256"] == receipt["logSha256"]
                    and row["interpretation"] == (
                        "PASS" if row["exitCode"] == 0 else "PRESERVED_FAILED_ATTEMPT_NOT_A_PASS"),
                    "Execution interpretation differs")
        controller = load(HERE / "controller-validation-001.json")
        positive = controller["positive"]
        require(positive["controllerActions"] == ["admit", "launch-observation", "phase1", "final", "accept"]
                and positive["syntheticOnly"] and positive["realChildStructureCheckerExercised"]
                and positive["reportExclusiveCreateReadback"] == "PASS"
                and positive["finalNegativeControls"] == 4, "Incomplete synthetic lifecycle")
        require([row["action"] for row in controller["wrapperRejections"]]
                == ["admit", "launch", "phase1", "final", "accept"], "Missing wrapper rejection")
        for row in controller["wrapperRejections"]:
            require(row["exitCode"] == 1, "Wrapper accepted absent observations")
            verify_receipt(row["receipt"]["path"], row["receipt"]["sha256"], 1)
        optional = load(HERE / "optional-validation-001.json")
        require(optional["testsRun"] == 6 and len(optional["individualUnits"]) == 62,
                "Optional-unit controls incomplete")
        hold = load(HERE / "readiness-and-hold-validation-001.json")
        require(hold["noPartialOutputs"] and hold["E10PassE11Reject"]
                and len(hold["reportReadinessNegativeControls"]) == 3
                and hold["actualPacketProofWrongHashRejected"], "Readiness/HOLD controls incomplete")
        preflight = load(HERE / "audit-configs-001" / "preflight.json")
        require(preflight["order"] == ["claude", "gpt"], "Reviewer order differs")
        for family, spec in preflight["runs"].items():
            frozen(spec["prompt"]["path"], spec["prompt"]["sha256"])
            require(frozen(spec["kickoff"]["path"], spec["kickoff"]["sha256"]).decode() == spec["kickoffText"],
                    "Kickoff differs")
            config = load(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"])
            for binding in config["files"]:
                frozen(binding["path"], binding["sha256"])
            require(spec["startupEstimate"] == final["estimates"][family]
                    and spec["startupEstimate"]["estimatedUpper"] == capacity["selected"]["firstPassingTrial"]["startupPeak"]
                    and not Path(spec["report"]).exists() and not any(Path(spec["report"]).parent.iterdir())
                    and not (HERE / (spec["run"] + "-launch.json")).exists(), "Run readiness differs")
        verify_receipt(ROOT / "neutral-final-static-execution-001" / "receipt.json",
                       "1e1a7d4de2e4186f391ccfe6b213181e4d34b650996b2785c10601f425c67c3a", 0)
        result = {
            "status": "PASS_FINAL_PREPARATION_NOT_REVIEW_ADMISSION",
            "candidate": final["candidate"], "base": final["base"],
            "preparationManifestSha256": MANIFEST_SHA, "handoffSha256": HANDOFF_SHA,
            "staticVerificationSha256": FINAL_SHA, "staticFilesVerified": len(manifest),
            "executionReceiptsVerified": len(executions) + 1,
            "capacityProof": {"path": str(capacity_path), "sha256": sha(frozen(capacity_path))},
            "sourceProof": {"path": str(source_path), "sha256": sha(frozen(source_path))},
            "startupForecast": capacity["selected"]["firstPassingTrial"]["startupPeak"],
            "caps": capacity["selected"]["firstPassingTrial"]["caps"],
            "limits": "Actual serial admission, two-family reviews and claim adjudication remain; no teaching or delivery acceptance.",
        }
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Final preparation verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(ROOT / "independent-preparation-final-verification-001.json", result)))


if __name__ == "__main__":
    main()
