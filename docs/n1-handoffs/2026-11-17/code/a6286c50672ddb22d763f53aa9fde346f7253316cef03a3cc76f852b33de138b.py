"""Validate and archive excluded initial reviews without accepting their findings."""
import json
from pathlib import Path

from common import frozen, require, sha


def require_context_hold(held, mechanics, structure, context, batch, candidate):
    same_binding = lambda key: all(held[key][part] == mechanics[key][part]
                                   for part in ("path", "sha256"))
    require(batch == 130 and held["batch"] == batch and held["candidate"] == candidate
            and held["status"] == "HOLD_CONTEXT_COMPACTED" and mechanics["status"] == "HOLD"
            and held["reviewAccepted"] is False and held["finalAcceptance"] is False
            and held["run"] == mechanics["run"] and held["session"] == mechanics["session"]
            and mechanics["candidate"] == candidate
            and all(same_binding(key) for key in ("structure", "context", "finalAudit"))
            and structure["status"] == "PASS" and structure["errors"] == []
            and structure["overall"] == held["rawVerdict"]
            and context["status"] == "FAIL" and len(context["errors"]) == 1
            and [event["type"] for event in context["compactions"]]
                == ["session.compaction_start", "session.compaction_complete"]
            and context["errors"][0].startswith("Context compaction occurred:")
            and len(mechanics["problems"]) == 1
            and mechanics["problems"][0] == "context " + context["errors"][0]
            and mechanics["evidenceCheck"] is None,
            "Excluded initial is not its recorded context-held execution")


def archive_excluded(paths, batch, candidate, accepted_runs, copy, binding, dump, chain,
                     audit_support, records):
    excluded = []
    for path in paths:
        path = Path(path)
        held = json.loads(frozen(path))
        read = lambda item: json.loads(frozen(item["path"], item["sha256"]))
        mechanics, structure, context = (read(held[key]) for key in ("final", "structure", "context"))
        require_context_hold(held, mechanics, structure, context, batch, candidate)
        run = held["run"]
        require(run not in accepted_runs and run not in {item["run"] for item in excluded},
                "An excluded run cannot also be accepted or duplicated")
        audit = read(held["finalAudit"])
        require(audit["eventsSha256"] == context["eventsSha256"],
                "Held audit/context describe different logs")
        prefix = f"excluded-initials/{run}"
        copy(path, f"{prefix}/hold.json")
        for field in ("report", "final", "structure", "context"):
            binding(held[field], f"{prefix}/{field}.{'md' if field == 'report' else 'json'}")
        dump(f"{prefix}/audit-summary.json",
             audit_support.bounded_audit(Path(held["finalAudit"]["path"])))
        for suffix in ("phase1", "launch", "admission"):
            copy(records / f"{run}-{suffix}.json", f"{prefix}/{suffix}.json")
        launch = json.loads(frozen(records / f"{run}-launch.json"))
        require(launch["session"] == held["session"], "Excluded launch identity differs")
        config_path = records / "prompts" / f"audit-config-{run}.json"
        config = json.loads(frozen(config_path))
        require(config["run"] == run and config["report"] == held["report"]["path"],
                "Excluded config/report mismatch")
        for item in config["files"]:
            frozen(item["path"], item["sha256"])
        copy(config_path, f"{prefix}/config.json")
        for field in ("prompt", "kickoff"):
            copy(Path(config[field]), f"{prefix}/{field}.txt")
        chains = [chain(Path(config["coreManifest"]), f"{prefix}/chain"),
                  chain(records / f"{run}-extension.json", f"{prefix}/extension")]
        copy(records / f"{run}-phase2-message.txt", f"{prefix}/phase2-message.txt")
        excluded.append({"run": run, "session": held["session"], "snapshot": candidate,
                         "status": held["status"], "rawVerdict": held["rawVerdict"],
                         "reviewAccepted": False, "finalAcceptance": False,
                         "holdSha256": sha(frozen(path)), "chains": chains,
                         "eventsSha256": context["eventsSha256"]})
    return excluded
