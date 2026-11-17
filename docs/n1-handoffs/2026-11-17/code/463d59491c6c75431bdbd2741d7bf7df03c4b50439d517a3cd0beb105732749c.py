"""Preserve real context-held, premature and coordinator-phase2-mismatch initials without accepting any."""
import json
from pathlib import Path

from b130_excluded_initials_v2 import archive_excluded as archive_earlier
from common import frozen, require, sha


STATUS = "VOID_COORDINATOR_PHASE2_MESSAGE_MISMATCH"
SUFFIX = "\nMissing entries: none"
GAP = "Tool call during the phase gap"
BREACHES = [GAP, "Extension read before phase 2 or out of order"] * 9 + [
    GAP, "Report write before complete required coverage, or a repeated write",
    GAP, "Invalid report readback", GAP, "Invalid completion message or premature completion",
    "Incomplete two-phase execution"]


def require_mismatch_hold(held, phase, final, audit, context, structure, events_raw, phase2, batch, candidate):
    same = lambda a, b: a["path"] == b["path"] and a["sha256"] == b["sha256"]
    users = [(i, event["data"]["content"]) for i, event in
             enumerate(json.loads(line) for line in events_raw.decode("utf-8").splitlines())
             if event.get("type") == "user.message"]
    delivered = users[1] if len(users) == 2 else (None, "")
    require(batch == 130 and held["batch"] == batch and held["run"] == "N1-B130-CLAUDE-003"
            and held["candidate"] == phase["candidate"] == final["candidate"] == candidate
            and held["session"] == phase["session"] == final["session"] == audit["session"]
            and held["status"] == STATUS and held["reviewAccepted"] is False and held["finalAcceptance"] is False
            and phase["run"] == final["run"] == held["run"]
            and phase["status"] == "PHASE1_READY" and phase["readyForPhase2"] is True and not phase["breaches"]
            and phase["coreRead"] == phase["coreRequired"] == 87
            and final["status"] == "HOLD" and same(final["finalAudit"], held["audit"])
            and same(final["context"], held["context"]) and same(final["structure"], held["structure"])
            and held["preflight"]["sha256"] == phase["preflightSha256"] == final["preflightSha256"]
            and audit["status"] == "VOID" and audit["breaches"] == BREACHES
            and audit["coreRead"] == audit["coreRequired"] == 87
            and audit["extensionRead"] == audit["extensionRequired"] == 9
            and audit["writes"] == audit["readbacks"] == 1 and audit["fetches"] == 0
            and audit["unexpectedUserMessages"] == 1 and audit["reviewerIdle"] and len(audit["messages"]) == 2
            and held["events"]["sha256"] == audit["eventsSha256"] == context["eventsSha256"]
            and context["status"] == "PASS" and context["errors"] == context["compactions"] == []
            and structure["status"] == "PASS" and structure["errors"] == []
            and delivered[0] == held["deliveredPhase2"]["eventIndex"]
            and sha(delivered[1].encode("utf-8")) == held["deliveredPhase2"]["sha256"]
            and held["deliveredPhase2"]["missingSuffix"] == SUFFIX and phase2 == delivered[1] + SUFFIX,
            "Excluded initial is not its recorded coordinator phase2-mismatch execution")


def archive_excluded(paths, batch, candidate, accepted_runs, copy, binding, dump, chain,
                     audit_support, records):
    excluded = []
    for path in paths:
        path = Path(path)
        held = json.loads(frozen(path))
        disallowed = set(accepted_runs) | {item["run"] for item in excluded}
        if held["status"] != STATUS:
            excluded.extend(archive_earlier([path], batch, candidate, disallowed, copy, binding, dump,
                                            chain, audit_support, records))
            continue
        read = lambda item: json.loads(frozen(item["path"], item["sha256"]))
        phase, final, audit, context, structure = (
            read(held[key]) for key in ("phase1", "final", "audit", "context", "structure"))
        events_raw = frozen(held["events"]["path"], held["events"]["sha256"])
        phase2 = frozen(held["phase2Message"]["path"], held["phase2Message"]["sha256"]).decode("utf-8")
        require_mismatch_hold(held, phase, final, audit, context, structure, events_raw, phase2, batch, candidate)
        run = held["run"]
        require(run not in disallowed, "An excluded run cannot also be accepted or duplicated")
        require(Path(held["phase2Message"]["path"]) == records / f"{run}-phase2-message.txt"
                and not (records / f"{run}-acceptance.json").exists(), "Mismatch run advanced or moved")
        frozen(held["report"]["path"], held["report"]["sha256"])
        preflight = read(held["preflight"])
        spec = preflight["runs"]["claude"]
        require(held["preflight"]["path"] == phase["preflight"] == final["preflight"]
                and Path(held["audit"]["path"]).parent.parent == Path(phase["auditDir"]).parent,
                "Excluded preflight or audit location differs")
        config_path = Path(spec["auditConfig"])
        config = json.loads(frozen(config_path))
        require(spec["run"] == config["run"] == run and config["report"] == spec["report"] == held["report"]["path"],
                "Excluded config/report mismatch")
        for item in config["files"]:
            frozen(item["path"], item["sha256"])
        launch = json.loads(frozen(records / f"{run}-launch.json"))
        require(launch["session"] == held["session"] and launch["run"] == run, "Excluded launch identity differs")
        prefix = f"excluded-initials/{run}"
        copy(path, f"{prefix}/hold.json")
        binding(held["report"], f"{prefix}/report.md")
        for key in ("phase1", "final", "structure", "context", "preflight"):
            binding(held[key], f"{prefix}/{key}.json")
        binding(held["phase2Message"], f"{prefix}/phase2-message.txt")
        for key, item in held["failureExecution"].items():
            binding(item, f"{prefix}/failed-execution/{key}")
        dump(f"{prefix}/audit-summary.json", audit_support.bounded_audit(Path(held["audit"]["path"])))
        for suffix in ("launch", "admission", "extension-preflight"):
            copy(records / f"{run}-{suffix}.json", f"{prefix}/{suffix}.json")
        copy(config_path, f"{prefix}/config.json")
        for field in ("prompt", "kickoff"):
            copy(Path(config[field]), f"{prefix}/{field}.txt")
        chains = [chain(Path(config["coreManifest"]), f"{prefix}/chain"),
                  chain(records / f"{run}-extension.json", f"{prefix}/extension")]
        excluded.append({
            "run": run, "session": held["session"], "snapshot": candidate, "status": held["status"],
            "rawVerdict": structure["overall"], "reviewAccepted": False, "finalAcceptance": False,
            "holdSha256": sha(frozen(path)), "eventsSha256": held["events"]["sha256"], "chains": chains,
            "limits": "Coordinator delivered only the first line of the frozen phase2 message, so the final "
                      "audit is VOID. The raw verdict and report are preserved but quarantined, not accepted.",
        })
    return excluded
