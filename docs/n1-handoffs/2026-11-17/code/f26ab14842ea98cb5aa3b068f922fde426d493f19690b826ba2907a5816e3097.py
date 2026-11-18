"""Strict full-roster resource admission for one future serial B131 reviewer."""
import json
from datetime import datetime, timezone
from pathlib import Path

from b131_review_v4_common import (BASE, CANDIDATE, COORDINATOR, GUARD, HERE,
                                     PROOFS, RECORDS, REPO, RUNNER, freeze_json,
                                     frozen, load_module, require, sha, start_guard,
                                     write_frozen)
from verify_b131_sources import FINGERPRINT, Git, OWNER


def validate_roster(status, roster, session_name, now, observed):
    rows = status["sessions"]
    require(isinstance(rows, list) and isinstance(roster, list) and rows,
            "Full nonempty status/roster arrays required")
    ids, roster_ids = [r["id"] for r in rows], [r["id"] for r in roster]
    require(len(ids) == len(set(ids)) == status["summary"]["total"] == len(roster_ids)
            and len(roster_ids) == len(set(roster_ids)) and set(ids) == set(roster_ids),
            "Full app snapshots differ, duplicate IDs, or filtered rows")
    age = (now - observed).total_seconds()
    require(0 <= age < 120, "Admission snapshots must be fresh, not future-dated")
    require(all(row["id"] == COORDINATOR or
                (row["activity"]["status"] == "idle" and not row.get("is_running", False))
                for row in rows), "Another session is active or unknown")
    require(not any(row["name"].strip() == session_name for row in rows),
            "Duplicate reviewer session exists")
    return len(rows)


def observe(argument, config, spec, record):
    from b131_preflight_004 import validate_report_destination
    report_readiness = validate_report_destination(spec)
    from b131_review_v4_common import DEFAULT_PREFLIGHT
    from b131_preflight_004 import verify_prerequisite
    verify_prerequisite(json.loads(frozen(DEFAULT_PREFLIGHT)))
    request_path = Path(argument)
    request_raw = request_path.read_bytes()
    request = json.loads(request_raw)
    require(set(request) == {"statusPath", "rosterPath", "observedAt"},
            "Admission request must name full status/roster snapshots and observedAt")
    status_raw, roster_raw = (Path(request[k]).read_bytes() for k in ("statusPath", "rosterPath"))
    status = json.loads(status_raw)
    roster = json.loads(roster_raw[roster_raw.index(b"["):])
    observed = datetime.fromisoformat(request["observedAt"])
    require(observed.tzinfo is not None, "Observation timestamp needs an explicit timezone")
    count = validate_roster(status, roster, spec["launch"]["sessionName"],
                            datetime.now(timezone.utc), observed)
    report = Path(spec["report"])
    run = spec["run"]
    absent = {"report": not report.exists(), "extension": not (HERE / f"{run}-extension.json").exists(),
              "auditDirectory": not (HERE / run).exists(), "launch": not (HERE / f"{run}-launch.json").exists()}
    require(all(absent.values()), "Existing reviewer artifacts must be preserved")
    guard, _ = start_guard("B131 future reviewer admission")
    git = Git(REPO, RUNNER, guard)
    try:
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Signed candidate checkout differs")
        require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
                == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Candidate identity differs")
        for name, digest in PROOFS.items():
            proof = json.loads(frozen(RECORDS / name, digest))
            require(proof["candidate"] == CANDIDATE and proof["base"] == BASE
                    and proof["status"] == "PASS" and not proof["memory"]["breach"], "Candidate proof differs")
        from b131_review_v4_common import verify_packet
        verify_packet(config, guard)
        from b131_preflight_004 import verify_subset
        from b131_review_v4_common import FORECAST
        from b131_capacity_003 import load_forecast
        verify_subset(guard, initial=True)
        capacity = load_forecast()
        record.update(capacityForecastSha256=sha(frozen(FORECAST)),
                      chosenCaps=capacity['chosenCaps'],
                      projectedWorstCasePeak=capacity['projectedWorstCasePeak'])
        bindings = {
            "request": write_frozen(HERE / f"{run}-admission-request.json", request_raw),
            "status": write_frozen(HERE / f"{run}-admission-status.json", status_raw),
            "roster": write_frozen(HERE / f"{run}-admission-roster.txt", roster_raw)}
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Admission RAM breach")
    resource = load_module("b131_admit_ram", GUARD)
    free = resource.available_ram()
    require(free > 2 * 1024**3, "Reviewer startup RAM floor no longer met")
    report_readiness = validate_report_destination(spec)
    record['reportDestination'] = report_readiness
    record.update(status="ADMITTED_REVIEWER_STARTUP_ONLY", admitted=True,
                  freeRamBytes=free, memory=memory, sessionCount=count, snapshots=bindings,
                  observedAt=request["observedAt"], absent=absent, launch=spec["launch"],
                  kickoff=spec["kickoffText"],
                  note="Fresh observation, not a reservation, completed review or publication permission.")
    return record
