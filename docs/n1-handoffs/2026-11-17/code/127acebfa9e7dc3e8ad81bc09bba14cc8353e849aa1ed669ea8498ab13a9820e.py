"""Verify the frozen final preparation without admitting or launching reviewers."""
import ast
import json
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
PREP = ROOT / "neutral-preparation-001"
HERE = PREP / "projected-successor-001"
sys.path.insert(0, str(HERE / "protocol-001"))
from b134_common import frozen, require, sha, freeze_json, start_guard, verify_packet, validate_report_destination, REPO, CANDIDATE, BASE
from b134_capacity import load_forecast, startup_bound
from verify_b134_sources import Git, FINGERPRINT, OWNER


def main():
    guard, _ = start_guard("B134 final immutable preparation verification")
    try:
        manifest = json.loads(frozen(PREP / "PREPARATION-SHA256SUMS-001.json"))
        actual = {p.relative_to(PREP).as_posix() for p in PREP.rglob("*") if p.is_file()}
        require(actual == set(manifest) | {"PREPARATION-SHA256SUMS-001.json"},
                "Preparation inventory changed after freeze")
        for name, digest in manifest.items():
            frozen(PREP / name, digest)
            if name.endswith(".py"):
                ast.parse(frozen(PREP / name), filename=str(PREP / name))
            guard.check()
        sums = verify_packet(guard)
        preflight = json.loads(frozen(HERE / "audit-configs-001" / "preflight.json"))
        forecast = load_forecast()
        require(preflight["order"] == ["claude", "gpt"] and forecast["chosenCaps"] == {"D": 25, "E": 10},
                "Final order/caps differ")
        estimates = {}
        for family, spec in preflight["runs"].items():
            validate_report_destination(spec)
            cfg = json.loads(frozen(spec["auditConfig"]["path"], spec["auditConfig"]["sha256"]))
            for row in cfg["files"]:
                frozen(row["path"], row["sha256"])
            estimates[family] = startup_bound(forecast, family, len(frozen(cfg["prompt"])))
            require(estimates[family]["estimatedUpper"] == 625929
                    and estimates[family]["status"] == "PASS_ESTIMATE", "Actual final forecast differs")
            for suffix in ("-launch.json", "-phase1.json", "-extension.json", "-final.json", "-acceptance.json"):
                require(not (HERE / (spec["run"] + suffix)).exists(), "Live reviewer artifact present")
        executions = json.loads(frozen(HERE / "execution-bindings-001.json"))
        for row in executions["executions"]:
            receipt = json.loads(frozen(row["path"], row["sha256"]))
            frozen(Path(row["path"]).parent / "output.log", row["logSha256"])
            require(not receipt["memory"]["breach"] and receipt["cleanupError"] is None, "Execution resource breach")
        runner = {"path": str(ROOT / "guarded-test-v3.py"),
                  "sha256": "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"}
        git = Git(REPO, runner, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Clean signed snapshot changed")
        result = {"status": "PASS_FINAL_FROZEN_NEUTRAL_PREPARATION_NOT_REVIEW_ADMISSION",
                  "candidate": CANDIDATE, "base": BASE, "preparationFiles": len(manifest),
                  "packetFiles": len(sums), "estimates": estimates,
                  "preparationManifestSha256": sha(frozen(PREP / "PREPARATION-SHA256SUMS-001.json")),
                  "handoffSha256": sha(frozen(HERE / "COORDINATOR-HANDOFF-001.txt")),
                  "limits": "Actual observation/model/context gates and claim adjudication remain; no reviewer launched."}
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Final static verification RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(HERE / "final-static-verification-001.json", result)))


if __name__ == "__main__":
    main()
