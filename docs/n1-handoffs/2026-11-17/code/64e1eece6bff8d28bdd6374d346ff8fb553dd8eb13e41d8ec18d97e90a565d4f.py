"""Verify prepared evidence, freeze only owned artifacts, and publish a local handoff."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE / "selected-runtime-003"), r"C:\Users\stop-\n1-kanji-workspace\review-tools"]
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

REVIEW = HERE.parent
PACKETS = [REVIEW / f"revision-confirmation-claude-{i:03d}" for i in range(1, 4)]
PACKETS += [REVIEW / f"revision-confirmation-gpt-{i:03d}" for i in range(1, 3)]
EXECUTIONS = [REVIEW / f"confirmation-prep-test-{i:03d}" for i in range(1, 12)]
EXECUTIONS += [REVIEW / f"confirmation-runtime-stage-{i:03d}" for i in range(1, 4)]
EXECUTIONS += [REVIEW / f"revision-confirmation-claude-prepare-{i:03d}" for i in range(1, 4)]
EXECUTIONS += [REVIEW / f"revision-confirmation-gpt-prepare-{i:03d}" for i in range(1, 3)]
EXECUTIONS += [REVIEW / f"revision-confirmation-readiness-{i:03d}" for i in range(1, 3)]
EXECUTIONS += [REVIEW / name for name in (
    "confirmation-producers-retention-001", "confirmation-actual-request-build-001",
    "confirmation-continuation-v2-tests-001", "confirmation-lossless-json-measurement-001")]

guard, _ = start_guard("B134 freeze runnable revision-only handoff")
try:
    ready = json.loads(frozen(HERE / "actual-readiness-v2.json",
                             "fe29dac42925ff0263dd19d425d030085520cdd49423f1098ef051c2cdbb371f"))
    require(ready["status"] == "PASS_PREPARATION_ONLY" and ready["actualReviewerAdmission"] is False
            and all(row["forecast"] <= row["limit"] and not row["reviewAccepted"]
                    for row in ready["runs"].values()), "Actual prepared readiness differs")
    for folder in (REVIEW / "confirmation-prep-test-011",
                   REVIEW / "confirmation-continuation-v2-tests-001",
                   REVIEW / "revision-confirmation-claude-prepare-003",
                   REVIEW / "revision-confirmation-gpt-prepare-002",
                   REVIEW / "revision-confirmation-readiness-002"):
        result = json.loads((folder / "receipt.json").read_bytes())
        require(result["exitCode"] == result["childExitCodeAfterCleanup"] == 0
                and result["cleanupError"] is None and not result["memory"]["breach"]
                and result["memory"]["freeRamBeforeBytes"] > 2 * 1024**3
                and result["memory"]["minimumObservedFreeRamBytes"] >= 1024**3
                and result["runnerSha256"] == "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"
                and result["guardSha256"] == "46c721d63970e352a2c5c9d21c5d67b216e88a160b0966e65e2e407c0cb41c84"
                and result["logSha256"] == sha((folder / "output.log").read_bytes()),
                "Selected guarded execution evidence differs")
    tools = {}
    for name in ("b134_revision_confirmation_v2.py", "b134_revision_proofs_v1.py"):
        canonical = WS / "review-tools" / name
        selected = HERE / "selected-runtime-003" / name
        require(canonical.read_bytes() == frozen(selected), "Canonical tool differs from tested runtime")
        canonical.chmod(0o444)
        tools[str(canonical)] = sha(frozen(canonical))
    predecessor = WS / "review-tools" / "b134_integration_confirmation_v1.py"
    require(sha(predecessor.read_bytes()) == "4070171ab891062859a5df1e07d7f6ab76732c66832db353e08aacf271a45f61",
            "Preserved v1 source changed")
    predecessor.chmod(0o444)
    tools[str(predecessor)] = sha(frozen(predecessor))
    dependencies = {}
    active = {}
    for family, row in ready["runs"].items():
        preflight = json.loads(frozen(row["preflight"]["path"], row["preflight"]["sha256"]))
        config = json.loads(frozen(preflight["config"]["path"], preflight["config"]["sha256"]))
        require(not Path(config["report"]).exists(), "Actual reviewer report exists before handoff")
        for item in config["files"]:
            dependencies[item["path"]] = sha(frozen(item["path"], item["sha256"]))
        active[family] = {key: row[key] for key in ("run", "session", "candidate", "preflight", "chain",
                         "scopeProof", "gateProof", "sources", "segments", "dossierUtf8ByteBound",
                         "lastAcceptedInputTokens", "forecast", "limit", "kickoffPath", "kickoffText")}
        active[family]["config"] = preflight["config"]
        active[family]["prompt"] = {"path": config["prompt"], "sha256": sha(frozen(config["prompt"]))}
        active[family]["kickoff"] = {"path": config["kickoff"], "sha256": sha(frozen(config["kickoff"]))}
    freeze_json(HERE / "dependency-index.json", dependencies)
    freeze_json(HERE / "active-artifacts.json", active)
    files = set()
    for root in [HERE, *PACKETS, *EXECUTIONS]:
        require(root.parent == REVIEW or root == HERE, "Owned artifact root escaped")
        if root.exists():
            for path in root.rglob("*"):
                if path.is_file():
                    require(path.resolve().is_relative_to(root.resolve()), "Owned artifact traverses elsewhere")
                    files.add(path)
    inventory = {**tools}
    for path in sorted(files):
        require(path.name not in ("HANDOFF.txt", "frozen-files.json"), "Handoff already exists")
        path.chmod(0o444)
        inventory[str(path)] = sha(frozen(path))
        guard.check()
    inventory_ref = freeze_json(HERE / "frozen-files.json", inventory)
    body = frozen(HERE / "handoff-body.txt").decode()
    body += "\n\nACTIVE ACTUAL ARTIFACTS / EXACT KICKOFF STRINGS:\n" + json.dumps(active, ensure_ascii=False, indent=2)
    body += "\n\nFULL FROZEN FILE INVENTORY:\n"
    body += "\n".join(digest + "  " + path for path, digest in sorted(inventory.items())) + "\n"
    body += "\nInventory JSON: " + json.dumps(inventory_ref) + "\n"
    handoff = write_frozen(HERE / "HANDOFF.txt", body.encode())
finally:
    memory = guard.finish()
require(not memory["breach"], "Handoff freeze RAM breach")
print(json.dumps({"handoff": handoff, "inventory": inventory_ref, "files": len(inventory),
                  "actualReviewerAdmission": False, "memory": memory}))
