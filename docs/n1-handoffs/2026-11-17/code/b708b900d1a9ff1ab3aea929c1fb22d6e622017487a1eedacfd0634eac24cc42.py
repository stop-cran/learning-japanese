"""Verify the final 004 handoff using the independent projection/capacity checks."""
import argparse
import importlib.util
import json
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-133" / "review"
OUTER = ROOT / "neutral-preparation-004"
HERE = OUTER / "successor-002"
sys.path.insert(0, str(WS / "review-tools"))
from common import freeze_json, frozen, require, sha, start_guard

MANIFEST_SHA = "5bf2c26716a5019f7c96978afb7f54d59b874a93352cd9494d0a17e6024bfdcd"
HANDOFF_SHA = "8c425594070f253ef914bfd0df053057657d79293d8689f7fc09faa9004fa02f"
FINAL_SHA = "09e35d5986deb8a712a34c126c0e5e48b8d6d282fe7ddea9fd56eb173c977775"
RUNNER_SHA = "03260517d250b9d8071e2e70ec76fdb3ffda906d4f947e4a049375ebb249e5eb"
GUARD_SHA = "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"


def load(path, digest=None):
    return json.loads(frozen(path, digest))


def receipt_check(binding, success):
    path = Path(binding["path"])
    receipt = load(path, binding["sha256"])
    frozen(path.parent / "output.log", receipt["logSha256"])
    require(receipt["runnerSha256"] == RUNNER_SHA
            and receipt["guardSha256"] == GUARD_SHA
            and receipt["cleanupError"] is None
            and not receipt["memory"]["breach"]
            and receipt["waitTimeoutSeconds"] <= .1
            and receipt["cleanupTimeoutSecondsPerStage"] <= 10
            and (receipt["exitCode"] == 0) == success,
            "Execution receipt integrity/outcome differs")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    guard, _ = start_guard("B133 coordinator final 004 verification")
    try:
        helper = WS / "review-tools" / "verify_b133_preparation004.py"
        frozen(helper, "013f909475870ad87ddfa830c3d7322d9ea35383501fab41853e481e95f2f48f")
        spec = importlib.util.spec_from_file_location("independent004", helper)
        independent = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(independent)
        manifest_path = HERE / "PREPARATION-SHA256SUMS-004.json"
        final_path = HERE / "final-static-verification-004.json"
        manifest = load(manifest_path, MANIFEST_SHA)
        final = load(final_path, FINAL_SHA)
        frozen(HERE / "COORDINATOR-HANDOFF-004.txt", HANDOFF_SHA)
        require(Path(manifest["base"]) == OUTER and len(manifest["files"]) == 3493,
                "Unexpected manifest root/count")
        actual = {str(p.relative_to(OUTER)) for p in OUTER.rglob("*") if p.is_file()}
        require(actual == set(manifest["files"]) | {
            str(manifest_path.relative_to(OUTER)), str(final_path.relative_to(OUTER))},
            "Final inventory changed")
        for name, digest in manifest["files"].items():
            path = OUTER / name
            require(path.resolve().is_relative_to(OUTER), "Unsafe static path")
            frozen(path, digest)
            guard.check()
        require(final["candidate"] == "ad047ace020579f81bde250ac948b9a4cb597887"
                and final["base"] == "6858fcfb069cc56a195c3f6ed938f92f657fe96b"
                and final["status"] == "PASS_IMMUTABLE_PREPARATION_FORECAST_NOT_REVIEWER_ADMISSION"
                and final["actualReviewerArtifacts"] == "ABSENT"
                and final["manifestSha256"] == MANIFEST_SHA
                and final["handoffSha256"] == HANDOFF_SHA
                and not final["memory"]["breach"],
                "Final preparation identity/status differs")
        sums = load(HERE / "packet" / "SHA256SUMS.json")
        files = {name: frozen(HERE / "packet" / name, digest) for name, digest in sums.items()}
        old_sums = load(independent.OLD / "packet" / "SHA256SUMS.json")
        require(set(old_sums) <= set(files), "Original source removed")
        require({name for name, digest in old_sums.items() if sha(files[name]) != digest}
                == {"REVIEW.md", "packet.json"}, "Unapproved original source modification")
        independent.check_projection(files)
        measured = independent.check_capacity(
            files, load(HERE / "core-chain-001.json"), load(HERE / "capacity-measurement-001.json"))
        independent.reproduce(HERE / "tools" / "verify004-full-derived.py",
                              HERE / "complete-verification-001.json")
        preflight = load(HERE / "audit-configs-004" / "preflight.json", final["preflightSha256"])
        require(preflight["order"] == ["claude", "gpt"], "Reviewer order differs")
        disclosure = frozen(HERE / "DISCLOSURE-001.txt")
        prompts = {}
        for family, item in preflight["runs"].items():
            prompt = frozen(item["prompt"]["path"], item["prompt"]["sha256"])
            require(prompt.count(disclosure) == files["REVIEW.md"].count(disclosure) == 1
                    and item["startupEstimate"]["estimatedUpper"] == measured["startupUpper"]
                    and item["startupEstimate"]["status"] == "PASS_ESTIMATE"
                    and not Path(item["report"]).exists()
                    and not any(Path(item["report"]).parent.iterdir()),
                    "Prompt, forecast or report destination differs")
            require(frozen(item["kickoff"]["path"], item["kickoff"]["sha256"])
                    == item["kickoffText"].encode("ascii"), "Exact kickoff differs")
            prompts[family] = prompt.decode()
        require(prompts["claude"].replace("CLAUDE", "GPT").replace("-claude-", "-gpt-")
                == prompts["gpt"], "Prompts differ beyond identity")
        executions = load(HERE / "execution-bindings-001.json")["executions"]
        require(len(executions) == 17, "Incomplete execution inventory")
        for row in executions:
            require(row["outcome"] in ("PASS", "PRESERVED_FAILURE"), "Unknown execution outcome")
            receipt_check(row["receipt"], row["outcome"] == "PASS")
        controller = load(HERE / "controller-validation-003.json")
        require(controller["positive"]["controllerActions"]
                == ["admit", "launch-observation", "phase1", "final", "accept"]
                and controller["positive"]["syntheticOnly"] is True
                and controller["positive"]["realChildStructureCheckerExercised"] is True
                and controller["positive"]["reportExclusiveCreateReadback"] == "PASS"
                and controller["positive"]["finalNegativeControls"] == 4,
                "Incomplete synthetic lifecycle")
        require([row["action"] for row in controller["wrapperRejections"]]
                == ["admit", "launch", "phase1", "final", "accept"], "Missing wrapper rejection")
        for row in controller["wrapperRejections"]:
            require(row["exitCode"] == 1, "Wrapper did not reject missing observations")
            receipt_check(row["receipt"], False)
        receipt_check({
            "path": str(ROOT / "neutral004-final-static-verification-execution-001" / "receipt.json"),
            "sha256": "582e90fb5c40e742865914b15cdafc9c87cb221347929cbbde7978708ea9b266"}, True)
        result = {
            "status": "PASS_REPRODUCED_004_FINAL_PREPARATION_NOT_REVIEW_ACCEPTANCE",
            "candidate": final["candidate"], "base": final["base"],
            "staticFilesVerified": len(manifest["files"]), "packetFiles": len(sums),
            "manifestSha256": MANIFEST_SHA, "handoffSha256": HANDOFF_SHA,
            "finalStaticVerificationSha256": FINAL_SHA,
            "completeByteProofReproducedExactly": True,
            "capacityIndependentRecomputation": measured,
            "boundExecutionReceiptsVerified": 23,
            "limits": "Mechanical preparation only. Actual serial admission, two-family reviews, reconciliation and publication remain required.",
        }
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Coordinator verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(args.output, result)))


if __name__ == "__main__":
    main()
