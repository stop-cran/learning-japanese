"""Exercise the actual frozen structure checker through the repaired child boundary."""
import json
import os
from pathlib import Path

from b131_review_v3_common import HERE, RECORDS, TOOLS, freeze_json, frozen, require, sha, write_frozen
from b131_lifecycle_process_005 import python


def main():
    root = RECORDS / "preparation003-lifecycle006-controls-001"
    root.mkdir(exist_ok=False)
    run = "N1-B131-CLAUDE-003"
    spec = json.loads(frozen(HERE / "prompts" / "preflight-compact-003.json"))["runs"]["claude"]
    config = json.loads(frozen(spec["auditConfig"]))
    phase1 = json.loads(frozen(HERE / f"{run}-phase1.json"))
    report = Path(spec["report"])
    report_raw = frozen(report, "a3034b4c4c6f1b58ce97e9765b3e0f01248f7d30b82116b594ab5bc2cb666011")
    checker = HERE / "check-report-structure.py"
    frozen(checker, "3ccb51f9f5636e99a65fd16400a4317afb026f4e373a83c11dba6925440121e3")
    audit = HERE / run / "audit-20261116T190040302546" / "audit.json"
    common_args = [
        "--core-manifest", config["coreManifest"], "--extension", HERE / f"{run}-extension.json",
        "--reference", config["reference"], "--phase1-list", Path(phase1["auditDir"]) / "phase1-list.txt",
        "--phase2-message", HERE / f"{run}-phase2-message.txt", "--audit", audit, "--run", run,
    ]
    # An empty inherited path reproduces the original host condition.
    os.environ.pop("PYTHONPATH", None)
    code, stdout, stderr = python(checker, "--report", report, *common_args)
    positive = json.loads(stdout)
    require(code == 0 and positive["status"] == "PASS" and not positive["errors"],
            f"Real structure check failed: {stdout}\n{stderr}")
    negative_path = root / "invalid-extra-section.md"
    write_frozen(negative_path, report_raw + b"\n## Unexpected section\ninvalid\n")
    code, stdout, stderr = python(checker, "--report", negative_path, *common_args)
    negative = json.loads(stdout)
    require(code == 1 and negative["status"] == "FAIL" and negative["errors"],
            f"Invalid structure was accepted: {stdout}\n{stderr}")
    require(frozen(report) == report_raw, "Actual reviewer report changed")
    require((HERE / f"{run}-context.json").is_file(), "Preserved initial context is missing")
    proof = {
        "status": "PASS",
        "realReport": {"path": str(report), "sha256": sha(report_raw)},
        "positive": positive,
        "negative": negative,
        "checks": ["empty-parent-PYTHONPATH import succeeds", "actual report passes unchanged checker",
                   "extra H2 is rejected", "actual report unchanged", "prior partial context retained"],
        "limits": "Tool integration and structure only; not substantive report or publication acceptance.",
    }
    print(json.dumps(freeze_json(root / "result.json", proof)))


if __name__ == "__main__":
    main()
