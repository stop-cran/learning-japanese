"""Admit an initial N1 review without reserving unrelated app sessions.

Usage: python -B scoped_admission.py BATCH claude|gpt STATUS_JSON [PREFLIGHT]

This replaces only step_v2.py's admission action. All remaining lifecycle
actions, frozen review inputs, review order and RAM thresholds are unchanged.
Earlier admissions and scripts remain historical and must not be rewritten.
"""
import datetime
import json
import sys
from pathlib import Path

from common import (
    COORDINATOR, GUARD, GUARD_SHA, freeze_json, frozen, load_batch,
    load_module, require, review_dir, sha, write_frozen,
)

REPOSITORY = "stop-cran/learning-japanese"
POLICY = "n1-scope-serial-v1"
FLOOR = 2 * 1024 ** 3


def assess_status(status, session_name, free_ram):
    sessions = status.get("sessions")
    require(isinstance(sessions, list), "Missing full sessions snapshot")
    require(status.get("summary", {}).get("total") == len(sessions),
            "Session snapshot is incomplete")
    ids = [s.get("id") for s in sessions]
    require(all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids),
            "Session IDs are missing or duplicated")
    require(COORDINATOR in ids, "Coordinator absent from full snapshot")

    owned = {COORDINATOR}
    while True:
        descendants = {
            s["id"] for s in sessions
            if s.get("creator_session_id") in owned
            or s.get("coordinating_creator_session_id") in owned
        }
        if descendants <= owned:
            break
        owned.update(descendants)
    scoped = owned | {
        s["id"] for s in sessions if s.get("project_repo") == REPOSITORY
    }
    active = [
        {"id": s["id"], "name": s.get("name"),
         "activity": s.get("activity"), "is_running": s.get("is_running")}
        for s in sessions
        if (s.get("activity") or {}).get("status") != "idle" or s.get("is_running")
    ]
    blockers = [s for s in active if s["id"] in scoped and s["id"] != COORDINATOR]
    unrelated = [s for s in active if s["id"] not in scoped]
    duplicate = any((s.get("name") or "").strip() == session_name for s in sessions)
    return {
        "policy": POLICY,
        "scope": {
            "coordinator": COORDINATOR,
            "repository": REPOSITORY,
            "sessionIds": sorted(scoped),
            "rule": "Coordinator descendants and sessions in the N1 content repository",
        },
        "freeRamBytes": free_ram,
        "startupFloorMet": free_ram > FLOOR,
        "activeSessions": active,
        "blockingSessions": blockers,
        "unrelatedActiveSessions": unrelated,
        "otherBusySession": bool(blockers),
        "sessionNamedForThisRunExists": duplicate,
        "statusAllowsAdmission": free_ram > FLOOR and not blockers and not duplicate,
        "note": (
            "Full snapshot retained without filtering. Unrelated isolated work is not "
            "a machine-wide reservation. One N1 batch/writer/reviewer, frozen inputs, "
            "actual shared-resource exclusivity and RAM guards remain required. "
            "This observation is not a reservation or content/publication approval."
        ),
    }


def main(batch, key, snapshot, preflight=None):
    config = load_batch(batch)
    records = review_dir(batch)
    preflight_path = Path(preflight) if preflight else records / "prompts" / "preflight.json"
    require(preflight_path.parent == records / "prompts", "Preflight must be a frozen prompts record")
    specification = json.loads(frozen(preflight_path))
    spec = specification["runs"][key]
    run = spec["run"]
    audit_config = json.loads(frozen(spec["auditConfig"]))
    for item in audit_config["files"]:
        frozen(item["path"], item["sha256"])
    frozen(spec["prompt"], spec["promptSha256"])
    order = specification["order"]
    for earlier in order[:order.index(key)]:
        prior = json.loads(frozen(records / f"{specification['runs'][earlier]['run']}-acceptance.json"))
        require(prior["reviewAccepted"] is True and prior["candidate"] == config["candidate"],
                f"Earlier {earlier} run not accepted")

    raw = Path(snapshot).read_bytes()
    require(sha(GUARD.read_bytes()) == GUARD_SHA, "RAM guard changed")
    resource = load_module("n1_ram_guard_scoped_admit", GUARD)
    assessment = assess_status(json.loads(raw), spec["launch"]["sessionName"], resource.available_ram())
    absent = {
        "report": not Path(spec["report"]).exists(),
        "extension": not (records / f"{run}-extension.json").exists(),
        "auditDirectory": not (records / run).exists(),
        "admission": not (records / f"{run}-admission.json").exists(),
        "admissionStatus": not (records / f"{run}-admission-status.json").exists(),
        "launch": not (records / f"{run}-launch.json").exists(),
    }
    tool = Path(__file__).resolve()
    record = {
        "run": run, "batch": config["batch"], "candidate": config["candidate"],
        "createdAt": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "preflight": str(preflight_path), "preflightSha256": sha(preflight_path.read_bytes()),
        "tool": {"path": str(tool), "sha256": sha(tool.read_bytes())},
        "launch": spec["launch"], "kickoff": spec["kickoffText"],
        **assessment, "absent": absent,
        "admitted": assessment["statusAllowsAdmission"] and all(absent.values()),
    }
    if not record["admitted"]:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        raise SystemExit("Admission refused")
    record["statusSnapshot"] = write_frozen(records / f"{run}-admission-status.json", raw)
    written = freeze_json(records / f"{run}-admission.json", record)
    print(json.dumps(written, ensure_ascii=False))


if __name__ == "__main__":
    require(4 <= len(sys.argv) <= 5, __doc__)
    main(*sys.argv[1:])
