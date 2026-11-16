"""Bind real B132 review records before assembling a publication closure.

No run identities or verdicts are supplied by this module. The eventual closure
builder must provide the frozen accepted artifacts and independently adjudicated
resolution record. Passing these checks is not substantive review acceptance.
"""
import json
import re
from pathlib import PurePosixPath

from common import require, sha
from record_b132_publication import validate_progress, validate_reviews
from run_b132_closure_checks import BASE, BATCH, CANDIDATE, MEMBERS

MECHANICAL_STATUS = "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
REFERENCE_FIELDS = ("report", "final", "acceptance", "adjudication", "context", "structure")
UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
SHA256 = re.compile(r"[0-9a-f]{64}")


def archive_path(name):
    require(isinstance(name, str) and name and "\\" not in name and ":" not in name,
            "Use a canonical relative archive path")
    path = PurePosixPath(name)
    require(path.parts and not path.is_absolute() and ".." not in path.parts
            and path.as_posix() == name and name != "provenance.json",
            "Unsafe or reserved archive path")
    return name


def same_ref(left, right, label):
    require(left["path"] == right["path"] and left["sha256"] == right["sha256"],
            f"{label} binding differs")


def checked_json(ref, read):
    require(isinstance(ref["sha256"], str) and SHA256.fullmatch(ref["sha256"]),
            "Expected an exact SHA-256 reference")
    raw = read(ref["path"], ref["sha256"])
    require(sha(raw) == ref["sha256"], "Reader returned bytes outside the frozen binding")
    value = json.loads(raw)
    require(isinstance(value, dict), "Expected an object record")
    return value


def validate_record(spec, acceptance, final, audit, context, structure, adjudication, preflight):
    run, role, snapshot, session = (spec[name] for name in ("run", "role", "snapshot", "session"))
    require(spec["family"] in ("claude", "gpt") and role in ("initial", "confirmation")
            and UUID.fullmatch(session), "Invalid review role, family or session")
    require(re.fullmatch(r"N1-B132-(?:CLAUDE|GPT)-(?:CONFIRM-)?[0-9]{3}", run),
            "Unexpected B132 run identifier")
    require(run.startswith("N1-B132-" + spec["family"].upper() + "-")
            and ("-CONFIRM-" in run) == (role == "confirmation"), "Run identity differs from role/family")
    key = "verdict" if role == "initial" else "confirmation"
    allowed = ("CLEAN", "NEEDS FIX", "UNVERIFIED") if role == "initial" else ("CONFIRMED",)
    require(spec[key] in allowed, "Unexpected accepted review status")
    for label, record in (("acceptance", acceptance), ("final", final)):
        require(record["run"] == run and record["candidate"] == snapshot,
                f"{label} run or snapshot differs")
    require(acceptance["reviewAccepted"] is True and acceptance[key] == spec[key],
            "Review has not been accepted")
    require(final["status"] == MECHANICAL_STATUS and final["session"] == session,
            "Final mechanical record differs")
    require(adjudication["run"] == run, "Adjudication run differs")
    require(audit["final"] is True and audit["reviewerIdle"] is True
            and audit["recordIncomplete"] is False and audit["breaches"] == []
            and audit["unexpectedUserMessages"] == [] and audit["fetches"] == 0
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"] is True
            and audit["session"] == session, "Final review audit is incomplete or breached")
    models = audit["actualResponseModels"]
    require(isinstance(models, list) and models
            and all(isinstance(model, str) and model.startswith(spec["family"] + "-") for model in models),
            "Observed response models do not match the review family")
    reads = ("core", "extension") if role == "initial" else ("chain",)
    for name in reads:
        require(type(audit[f"{name}Read"]) is int and type(audit[f"{name}Required"]) is int
                and audit[f"{name}Required"] > 0
                and audit[f"{name}Read"] == audit[f"{name}Required"],
                f"Incomplete {name} read coverage")
    require(context["status"] == "PASS" and context["compactions"] == []
            and context["eventsSha256"] == audit["eventsSha256"],
            "Context/compaction audit differs")
    require(structure["status"] == "PASS"
            and structure["overall" if role == "initial" else "confirmation"] == spec[key],
            "Report structure or status differs")
    require(preflight["candidate"] == snapshot, "Preflight describes another snapshot")
    if role == "initial":
        require(adjudication["candidate"] == snapshot and adjudication["claimsAdjudicated"] is True
                and adjudication["verdict"] == spec[key]
                and acceptance["acceptedFindings"] == adjudication["acceptedFindings"],
                "Initial substantive adjudication differs")
        same_ref(acceptance["report"], adjudication["report"], "Adjudicated report")
        same_ref(acceptance["final"], adjudication["final"], "Adjudicated mechanical final")
        require(preflight["runs"][spec["family"]]["run"] == run
                and preflight["runs"][spec["family"]]["report"] == acceptance["report"]["path"],
                "Initial preflight run or report differs")
    else:
        require(preflight["run"] == run and preflight["session"] == session
                and isinstance(adjudication["dispositions"], dict), "Confirmation bindings differ")
        same_ref(acceptance["report"], final["report"], "Confirmation report")
        require(final["confirmation"] == spec[key], "Final confirmation differs")


def collect_record(spec, read):
    """read(path, sha256) must require a ReadOnly input; return exact source refs."""
    acceptance = checked_json(spec["acceptance"], read)
    final = checked_json(acceptance["final"], read)
    audit_ref = final["finalAudit"] if spec["role"] == "initial" else final["audit"]
    audit = checked_json(audit_ref, read)
    context = checked_json(final["context"], read)
    structure = checked_json(final["structure"], read)
    adjudication = checked_json(acceptance["adjudication"], read)
    preflight_ref = ({"path": final["preflight"], "sha256": final["preflightSha256"]}
                     if spec["role"] == "initial" else spec["preflight"])
    preflight = checked_json(preflight_ref, read)
    validate_record(spec, acceptance, final, audit, context, structure, adjudication, preflight)
    report = acceptance["report"]
    require(sha(read(report["path"], report["sha256"])) == report["sha256"],
            "Report content differs")
    refs = {
        "acceptance": spec["acceptance"], "final": acceptance["final"],
        "adjudication": acceptance["adjudication"], "report": report,
        "context": final["context"], "structure": final["structure"],
        "preflight": preflight_ref, "audit": audit_ref,
    }
    return refs, adjudication


def validate_resolution(resolution, lineage, reviewed, inventory):
    require(resolution["batch"] == BATCH and resolution["initialSnapshot"] == CANDIDATE
            and resolution["reviewedSnapshot"] == reviewed
            and resolution["remainingActionableFindings"] == []
            and resolution["remainingConsequentialClaims"] == [],
            "Resolution has the wrong snapshot or outstanding work")
    expected = {entry["run"]: entry["adjudication"]["sha256"] for entry in lineage}
    require(resolution["adjudicationSha256"] == expected,
            "Resolution does not bind every accepted adjudication")
    require(isinstance(resolution["dispositions"], list), "Missing claim dispositions")
    ids = set()
    for item in resolution["dispositions"]:
        identity = (item["run"], item["id"])
        require(item["run"] in expected and isinstance(item["id"], str) and item["id"]
                and identity not in ids, "Invalid or duplicate claim disposition")
        require(item["status"] in ("fixed", "source-backed-no-change", "excluded-from-delivered-teaching")
                and isinstance(item["reason"], str) and item["reason"].strip()
                and isinstance(item["evidence"], list) and item["evidence"],
                "Unresolved or unsupported claim disposition")
        for ref in item["evidence"]:
            archive_path(ref["path"])
            require(SHA256.fullmatch(ref["sha256"]) and inventory.get(ref["path"]) == ref["sha256"],
                    "Disposition evidence is not bound to the closure inventory")
        ids.add(identity)
    required = {(entry["run"], claim) for entry in lineage if entry["role"] == "initial"
                for claim in [*entry["acceptedFindings"], *entry["openClaimIds"],
                              *entry["coordinatorClaimIds"]]}
    require(required <= ids, "An accepted finding or consequential claim lacks a disposition")


def closed_progress(original, closure_raw, manifest, resolution):
    closure = json.loads(closure_raw)
    reviewed = closure["reviewedSnapshot"]
    validate_reviews(closure, reviewed)
    validate_resolution(resolution, closure["reviewLineage"], reviewed, closure["recordedFileSha256"])
    require(original["batch"] == BATCH and original["members"] == MEMBERS
            and original["base"] == BASE and original["sourceRows"] == [197]
            and original["status"] == "local-unreviewed-author-candidate"
            and original["publishedDelivered"] == 267 and original["undelivered"] == 961
            and original["deliveryNotIncremented"] is True, "Unexpected original B132 ledger")
    require(closure["limits"] and all(isinstance(item, str) and item for item in closure["limits"]),
            "Explicit review/acceptance limits are required")
    value = {
        "batch": BATCH, "base": BASE, "governingIssue": 60,
        "status": "textual-review-closed-publication-pending",
        "members": MEMBERS, "sourceRows": original["sourceRows"], "supports": original["supports"],
        "initialSnapshot": CANDIDATE, "reviewedSnapshot": reviewed,
        "reviewClosed": MEMBERS, "published": [], "runtimePublished": False,
        "manifestSha256": sha(manifest), "contentVersion": json.loads(manifest)["contentVersion"],
        "accounting": {
            "frozenPendingRecords": 1228, "publishedPendingRecordsWithCards": 267,
            "publishedN1Additions": 261, "n2Placements": 6, "undelivered": 961,
            "reviewClosedPendingRecordsWithCards": 268, "localUnreviewedDrafts": 0,
            "notStarted": 960, "overallN1TaskComplete": False,
        },
        "review": {
            "status": "closed-with-disclosed-limits", "finalRuns": closure["finalRuns"],
            "closure": "../n1-reviews/batch-132-closure/provenance.json",
            "closureProvenanceSha256": sha(closure_raw), "historicalReportsPreserved": True,
            "remainingActionableFindings": [], "remainingConsequentialClaims": [],
        },
        "originalAuthorProgress": "../n1-reviews/batch-132-closure/verification/original-progress.json",
        "originalAuthorWarnings": original["warnings"],
        "publicationGates": ["Owner-signed publication", "CI", "Exact served ZIP/runtime equality"],
        "limits": closure["limits"],
    }
    validate_progress(value, reviewed, manifest, closure_raw)
    return value
