"""Bind accepted B134 initials without rewriting their different claim schemas."""
import json
import re
import sys
from pathlib import Path

from b132_closure_records import UUID, checked_json
from common import WS, freeze_json, frozen, json_bytes, require, sha, write_frozen
from run_b134_closure_checks import CANDIDATE

MECHANICAL_STATUS = "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
P = WS / "scratch-134" / "review" / "neutral-preparation-001" / "projected-successor-001"
PREFLIGHT = {
    "path": str(P / "audit-configs-001" / "preflight.json"),
    "sha256": "c155d397d284665b758985ed89d0fe08882970a6bb8224fadb2169620b6a0254",
}
INITIALS = {
    "claude": {
        "session": "3847f453-7c80-4ede-88d3-6771cca5f794",
        "verdict": "UNVERIFIED",
        "acceptance": "5a4f00680af86b0e59ebcf3033ca952791382f023d499906d303082f297ecef3",
        "final": "65d9c8584b0fbdadc227a7c7c087ef2ebe6c0f7cb3b0fbfb9ed2bb3f99ae79c8",
    },
    "gpt": {
        "session": "8950c746-d7a4-42fb-8db1-3b4ef664144a",
        "verdict": "NEEDS FIX",
        "acceptance": "79f73957d10912872d2d750a6d6452d801f602e6fd75f249f4d676cfe5682778",
        "final": "38d15336c17faf928578a153942b068e6c8e9a2f6e42e793b479905fe1d4b55b",
    },
}
CLAIM_ID = re.compile(r"(?:(?:CLAUDE|GPT)-)?[CDEFOQL][1-9]\d*")


def ids(values, field):
    require(isinstance(values, list)
            and all(isinstance(value, str) and CLAIM_ID.fullmatch(value) for value in values),
            "Invalid claim inventory: " + field)
    require(len(values) == len(set(values)), "Duplicate claim identity: " + field)
    return list(values)


def normalize_claims(adjudication, family):
    accepted = adjudication["acceptedFindings"]
    require(isinstance(accepted, list), "Missing accepted-findings inventory")
    if accepted and all(isinstance(item, dict) for item in accepted):
        require(all(all(isinstance(item.get(key), str) and item[key].strip()
                        for key in ("id", "disposition", "reason", "coordinatorSeverity"))
                    for item in accepted), "Incomplete accepted-finding object")
        accepted = [item["id"] for item in accepted]
    open_ids = ids(adjudication["openClaimIds"], "openClaimIds")
    if "coordinatorClaimIds" in adjudication:
        coordinator = ids(adjudication["coordinatorClaimIds"], "coordinatorClaimIds")
    else:
        require(family == "gpt" and {"CLAUDE-C1", "CLAUDE-C2"} <= set(open_ids),
                "Missing explicit coordinator-claim inventory")
        coordinator = []
    return {
        "acceptedFindings": ids(accepted, "acceptedFindings"),
        "openClaimIds": open_ids,
        "coordinatorClaimIds": coordinator,
    }


def disposition_ids(report, claims):
    report_ids = re.findall(r"(?m)^### ([FO]\d+):", report.decode("utf-8"))
    ids(report_ids, "original report")
    values = [*report_ids]
    for field in ("acceptedFindings", "openClaimIds", "coordinatorClaimIds"):
        values.extend(ids(claims[field], field))
    return list(dict.fromkeys(values))


def collect_initial_record(spec, preflight_ref, final_ref, read):
    family, run, session = (spec[name] for name in ("family", "run", "session"))
    require(family in INITIALS and spec["role"] == "initial"
            and spec["snapshot"] == CANDIDATE and UUID.fullmatch(session)
            and session == INITIALS[family]["session"]
            and run == "N1-B134-" + family.upper() + "-001",
            "Invalid original-review identity")
    acceptance = checked_json(spec["acceptance"], read)
    final = checked_json(final_ref, read)
    preflight = checked_json(preflight_ref, read)
    launch = preflight["runs"][family]
    config = checked_json(launch["auditConfig"], read)
    adjudication = checked_json(acceptance["adjudication"], read)
    audit = checked_json(final["audit"], read)
    for label, record in (("acceptance", acceptance), ("final", final), ("adjudication", adjudication)):
        require(record["run"] == run and record["candidate"] == CANDIDATE,
                label + " identifies another review")
    require(acceptance["reviewAccepted"] is True and acceptance["verdict"] == spec["verdict"]
            and acceptance["finalSha256"] == final_ref["sha256"],
            "Unaccepted or unbound initial review")
    require(final["session"] == session and final["status"] == MECHANICAL_STATUS
            and final["problems"] == [], "Mechanical final is incomplete")
    report = final["report"]
    require(config["candidate"] == preflight["candidate"] == CANDIDATE
            and launch["run"] == config["run"] == run and config["expectedFamily"] == family
            and config["report"] == launch["report"] == report["path"],
            "Report, preflight or audit configuration differs")
    report_raw = read(report["path"], report["sha256"])
    require(sha(report_raw) == report["sha256"] == acceptance["reportSha256"]
            == adjudication["reportSha256"]
            and adjudication["finalSha256"] == final_ref["sha256"],
            "Report/adjudication hash binding differs")
    require(adjudication["claimsAdjudicated"] is True and adjudication["verdict"] == spec["verdict"]
            and isinstance(adjudication["claimChecks"], list) and adjudication["claimChecks"]
            and all(isinstance(item, dict)
                    and all(isinstance(item.get(key), str) and item[key].strip()
                            for key in ("claim", "evidence", "disposition"))
                    for item in adjudication["claimChecks"]), "Substantive adjudication is missing")
    require(audit["run"] == run and audit["session"] == session and audit["final"] is True
            and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK" and audit["bootstrapVerified"] is True
            and audit["reviewerIdle"] is True and audit["recordIncomplete"] is False
            and audit["breaches"] == [] and type(audit["unexpectedUserMessages"]) is int
            and audit["unexpectedUserMessages"] == audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"] is True
            and len(audit["messages"]) == 2 and audit["messages"][-1].strip() == spec["verdict"],
            "Incomplete or breached execution audit")
    for name in ("core", "extension"):
        require(type(audit[f"{name}Required"]) is int and audit[f"{name}Required"] > 0
                and type(audit[f"{name}Read"]) is int
                and audit[f"{name}Read"] == audit[f"{name}Required"], "Incomplete read coverage")
    models, telemetry = audit["actualResponseModels"], audit["capacityTelemetry"]
    require(models and all(isinstance(model, str) and model.startswith(family + "-") for model in models)
            and telemetry["status"] == "PASS" and telemetry["errors"] == []
            and telemetry["compactions"] == [] and telemetry["family"] == family,
            "Observed family/context telemetry differs")
    structure = final["structure"]
    require(structure["status"] == "PASS" and structure["overall"] == spec["verdict"]
            == INITIALS[family]["verdict"], "Structure or verdict differs")
    claims = normalize_claims(adjudication, family)
    disposition_ids(report_raw, claims)
    fields = ("run", "session", "eventsSha256", "eventsBytes", "status", "breaches",
              "bootstrapVerified", "actualResponseModels", "reviewerIdle", "recordIncomplete",
              "coreRead", "coreRequired", "extensionRead", "extensionRequired",
              "writes", "readbacks", "readbackVerified", "reportBinding", "fetches")
    summary = {field: audit[field] for field in fields}
    summary.update(originalAuditSha256=final["audit"]["sha256"], rawExecutionPayloadsRemainLocal=True,
                   representation="Bounded derivative; raw calls, messages and events remain local.")
    refs = {
        "acceptance": spec["acceptance"], "final": final_ref, "report": report,
        "adjudication": acceptance["adjudication"], "audit": final["audit"],
        "preflight": preflight_ref, "auditConfig": launch["auditConfig"],
    }
    derivatives = {
        "audit-summary": json_bytes(summary),
        "context": json_bytes({"status": "PASS", "eventsSha256": audit["eventsSha256"],
                              "originalAuditSha256": final["audit"]["sha256"],
                              "capacityTelemetry": telemetry}),
        "structure": json_bytes({"originalFinalSha256": final_ref["sha256"], "structure": structure}),
        "claims": json_bytes({"originalAdjudication": acceptance["adjudication"], **claims,
                             "representation": "Identity-only normalization; original unchanged."}),
    }
    return refs, derivatives, claims


def actual_initial(family):
    known = INITIALS[family]
    run = "N1-B134-" + family.upper() + "-001"
    spec = {
        "family": family, "run": run, "role": "initial", "session": known["session"],
        "snapshot": CANDIDATE, "verdict": known["verdict"],
        "acceptance": {"path": str(P / (run + "-acceptance.json")), "sha256": known["acceptance"]},
    }
    final = {"path": str(P / (run + "-final.json")), "sha256": known["final"]}
    refs, derivatives, claims = collect_initial_record(spec, PREFLIGHT, final, frozen)
    return spec, refs, derivatives, claims


def main(output):
    root = WS / "scratch-134" / "review"
    require(output.parent == root and not output.exists(), "Use a new direct review output directory")
    collected = {family: actual_initial(family) for family in INITIALS}
    result = {"batch": 134, "candidate": CANDIDATE, "status": "BOUND_INITIALS_NOT_CONFIRMATION",
              "toolSha256": sha(frozen(Path(__file__))), "initials": {}}
    for family, (spec, refs, derivatives, claims) in collected.items():
        result["initials"][family] = {
            "spec": spec, "refs": refs, "claims": claims,
            "dispositionIds": disposition_ids(frozen(refs["report"]["path"], refs["report"]["sha256"]), claims),
            "derivatives": {
                name: write_frozen(output / family / (name + ".json"), raw)
                for name, raw in derivatives.items()
            },
        }
    print(json.dumps(freeze_json(output / "index.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "b134_initial_records.py NEW_OUTPUT_DIRECTORY")
    main(Path(sys.argv[1]).resolve())
