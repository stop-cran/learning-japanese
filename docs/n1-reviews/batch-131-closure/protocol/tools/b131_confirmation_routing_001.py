"""Bind B131 confirmations to the two accepted, separately namespaced initials."""
import datetime
import json
import math
import uuid
from pathlib import Path

from common import COORDINATOR, TOOLS, WS, frozen, load_module, require, sha

ROOT = WS / "scratch-131" / "review"
PARENT = "1359b467e0edee8822c665614d6ca57e42785c4d"
INITIALS = {
    "claude": {
        "directory": "preparation-003", "run": "N1-B131-CLAUDE-003",
        "session": "95cb8d22-f976-4ed5-bb62-0a3a52ff2931",
        "acceptanceSha256": "1ed83db9be063f5f80e5d36df3a928e7fd9a8a3353c94b59d0c7fc99adb129e8",
        "checkerSha256": "9902553a73d0099940517730b2c8a06f1082951a530ca32d0c26efd116326bb4",
    },
    "gpt": {
        "directory": "preparation-004", "run": "N1-B131-GPT-004",
        "session": "ebb78462-3199-4b4f-9afc-18103f010fc9",
        "acceptanceSha256": "40e0a72e7feedd8918fea6ca90b56d3d4652688d7dfc5cfe4888e6d613244537",
        "checkerSha256": "2e1073e46ea1f7dcd7a322e223de0e98fd35b03c94a7416b3caba70e6f3c1d86",
    },
}
CHAIN_PATH = ROOT / "preparation-003" / "review_chain.py"
CHAIN_SHA = "2e4184500af5f4361d996a3568ed4f6abf2f3999f80556fa07ac3e22782d12ae"
CAPACITY_PATH = TOOLS / "b131_capacity_003.py"
CAPACITY_SHA = "0ddf6f1e51e7cd6542ffa9b672f6d31f4dc03bae888a3e1bde9ad6e772e65a61"


def profile(family):
    require(family in INITIALS, "Unknown B131 confirmation family")
    return INITIALS[family]


def initial_directory(family):
    return ROOT / profile(family)["directory"]


def checker_path(family):
    return initial_directory(family) / "check-run-context.py"


def check_lineage(spec, accepted, launch, config):
    expected = profile(spec["family"])
    acceptance = initial_directory(spec["family"]) / (expected["run"] + "-acceptance.json")
    require(spec["batch"] == config["batch"] == 131
            and spec["acceptance"] == {
                "path": str(acceptance), "sha256": expected["acceptanceSha256"]}
            and accepted["run"] == launch["run"] == expected["run"]
            and accepted["reviewAccepted"] is True
            and accepted["candidate"] == launch["candidate"] == config["candidate"] == PARENT
            and spec["session"] == launch["session"] == expected["session"],
            "Confirmation differs from its accepted original reviewer or frozen snapshot")


def initial_launch(spec, accepted, config):
    expected = profile(spec["family"])
    frozen(spec["acceptance"]["path"], expected["acceptanceSha256"])
    path = initial_directory(spec["family"]) / (expected["run"] + "-launch.json")
    launch = json.loads(frozen(path))
    check_lineage(spec, accepted, launch, config)
    for key in ("final", "adjudication", "report"):
        frozen(accepted[key]["path"], accepted[key]["sha256"])
    return launch


def binding(path, digest=None):
    return {"path": str(path), "sha256": sha(frozen(path, digest))}


def routing_bindings(family):
    expected = profile(family)
    return [
        binding(Path(__file__)),
        binding(CHAIN_PATH, CHAIN_SHA),
        binding(checker_path(family), expected["checkerSha256"]),
        binding(CAPACITY_PATH, CAPACITY_SHA),
        binding(initial_directory(family) / (expected["run"] + "-launch.json")),
        binding(ROOT / "preparation-003" / "batch.json"),
    ]


def check_context(events, family):
    path = checker_path(family)
    frozen(path, profile(family)["checkerSha256"])
    checker = load_module("b131_confirm_context_" + family, path)
    raw = Path(events).read_bytes()
    result = checker.check(events)
    frozen(CAPACITY_PATH, CAPACITY_SHA)
    capacity = load_module("b131_confirm_capacity", CAPACITY_PATH)
    exact = capacity.telemetry(
        [json.loads(line) for line in raw.decode("utf-8").splitlines()],
        capacity.load_forecast(), family)
    require(result["eventsSha256"] == sha(raw), "Context events changed during inspection")
    return {**result, "status": "PASS" if result["status"] == exact["status"] == "PASS" else "FAIL",
            "family": family, "checker": binding(path), "exactProfile": exact}


def capacity_check(context, chain):
    require(context["status"] == "PASS", "Original reviewer context is not accepted")
    last = context["exactProfile"]["lastInputTokens"]
    require(type(last) is int and last >= 0 and chain["segments"], "Missing actual capacity inputs")
    total = sum(row["bytes"] for row in chain["segments"])
    require(total > 0, "Empty confirmation chain")
    # Includes the rendered headers; use the conservative dictionary coefficient for every byte.
    incremental = math.ceil(total * 0.65 * 1.10)
    peak = last + 7000 + incremental + 30000
    require(peak <= 700000, f"Original reviewer confirmation would exceed capacity: {peak} > 700000")
    return {"status": "PASS_PRE_CONFIRMATION_CAPACITY", "lastInputTokens": last,
            "chainBytes": total, "projectedChainTokens": incremental,
            "currentOffset": 7000, "reportAllowance": 30000, "gate": 700000,
            "projectedPeak": peak, "coefficient": "0.65 tokens/byte * 1.10; all rendered chain bytes"}


def report_destination(path):
    path = Path(path)
    require(path.parent == WS / "reports-131" and not path.exists(),
            "Unexpected or existing B131 confirmation report")
    path.parent.mkdir(parents=True, exist_ok=True)
    probe = path.parent / (".b131-confirmation-probe-" + uuid.uuid4().hex)
    try:
        with probe.open("xb") as stream:
            stream.write(b"B131 report destination probe\n")
        require(probe.read_bytes() == b"B131 report destination probe\n", "Report probe differs")
    finally:
        if probe.exists():
            probe.unlink()
    return {"parent": str(path.parent), "writeReadDeleteProbe": True, "reportAbsent": not path.exists()}


def check_roster(status, roster, session, observed, now):
    rows = status["sessions"]
    ids, other_ids = [row["id"] for row in rows], [row["id"] for row in roster]
    require(rows and len(ids) == len(set(ids)) == status["summary"]["total"]
            and len(other_ids) == len(set(other_ids)) == len(ids) and set(ids) == set(other_ids),
            "Full status and roster differ or contain duplicates")
    require(observed.tzinfo is not None and 0 <= (now - observed).total_seconds() < 120,
            "Confirmation status/roster snapshots expired or are future-dated")
    require(all(row["id"] == COORDINATOR or (
        row["activity"]["status"] == "idle" and not row.get("is_running", False)) for row in rows),
        "Another session is active or unknown")
    matches = [row for row in rows if row["id"] == session]
    require(len(matches) == 1, "Original reviewer missing from full snapshot")
    reviewer = matches[0]
    require(not reviewer.get("awaiting_user_input") and not reviewer.get("awaiting_plan_approval")
            and sum(row["name"] == reviewer["name"] for row in rows) == 1,
            "Original reviewer is blocked or ambiguously named")


def admission_snapshot(path, session):
    raw = Path(path).read_bytes()
    request = json.loads(raw)
    require(set(request) == {"statusPath", "rosterPath", "observedAt"}, "Invalid confirmation admission request")
    status_raw, roster_raw = (Path(request[key]).read_bytes() for key in ("statusPath", "rosterPath"))
    status = json.loads(status_raw)
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    check_roster(status, roster, session, datetime.datetime.fromisoformat(request["observedAt"]),
                 datetime.datetime.now(datetime.timezone.utc))
    return status_raw, roster_raw, raw
