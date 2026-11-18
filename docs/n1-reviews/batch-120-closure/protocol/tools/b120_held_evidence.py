"""Preserve B120's structurally held confirmation outside accepted review lineage."""
import gzip
import json
from pathlib import Path

from common import WS, frozen, json_bytes, load_module, require, sha

RUN = "N1-B120-CLAUDE-001-CONFIRM-001"
SNAPSHOT = "c986ae49e844c08afc294d9381c7e486f2c9315d"
SESSION = "ca852871-ca27-4e1f-a8f9-892839b0eada"
HOLD_SHA = "7da89802ae417ff0c5e58e792a8f5b936875985532600c1996bd95e272d4fdd5"
ERROR = ("Optional O1: citation source 'coordinator/pair-dispositions-neutral.md' "
         "is not in the reviewer's chain")
HERE = WS / "scratch-120" / "review" / "confirm"


def verify_lineage(provenance, candidate):
    initial = "8637cccb25507a1123559041ebba5401203de2db"
    prior_gpt = "N1-B120-GPT-001-CONFIRM-001"
    final_runs = {f"N1-B120-{family}-001-CONFIRM-002" for family in ("CLAUDE", "GPT")}
    require(candidate not in (SNAPSHOT, initial)
            and provenance["reviewedSnapshot"] == candidate
            and provenance["initialSnapshot"] == initial
            and provenance["publication"] == "PENDING"
            and not provenance["excludedInitialRuns"]
            and provenance["intermediateRuns"] == [prior_gpt]
            and set(provenance["finalRuns"]) == final_runs, "Unexpected B120 closure selection")
    rows = provenance["reviewLineage"]
    expected_runs = final_runs | {"N1-B120-CLAUDE-001", "N1-B120-GPT-001", prior_gpt}
    require(len(rows) == 5 and {row["run"] for row in rows} == expected_runs
            and RUN not in expected_runs, "Held report must remain outside accepted lineage")
    for row in rows:
        family = "claude" if "CLAUDE" in row["run"] else "gpt"
        session = SESSION if family == "claude" else "524dc618-ae8f-4474-b698-6896a0507aed"
        is_final = row["run"] in final_runs
        is_initial = "-CONFIRM-" not in row["run"]
        require(row["family"] == family and row["session"] == session
                and row["role"] == ("final" if is_final else "initial" if is_initial else "intermediate")
                and row["snapshot"] == (candidate if is_final else initial if is_initial else SNAPSHOT)
                and row["rawVerdict"] == ("UNVERIFIED" if is_initial else "CONFIRMED")
                and row["finalAcceptance"] is is_final
                and row["confirmationAcceptedOnSnapshot"] is (not is_initial)
                and row["priorRun"] == (prior_gpt if is_final and family == "gpt" else None),
                f"Wrong snapshot-specific B120 acceptance: {row['run']}")


def verify_hold(hold, mechanics, audit, context, structure):
    require(hold["run"] == mechanics["run"] == RUN
            and hold["candidate"] == mechanics["candidate"] == SNAPSHOT
            and hold["session"] == mechanics["session"] == SESSION
            and hold["family"] == "claude", "Held run identity changed")
    require(hold["status"] == "HELD_STRUCTURE" and mechanics["status"] == "HOLD"
            and hold["rawVerdict"] == mechanics["confirmation"] == "UNVERIFIED"
            and all(hold[key] is False for key in
                    ("reviewEvidenceAccepted", "confirmationAccepted", "publicationAccepted")),
            "Held history must not become accepted evidence")
    require(all(hold[key] == mechanics[key] for key in ("report", "audit", "context", "structure")),
            "Held record does not bind the mechanical result")
    require(structure["status"] == "FAIL" and structure["errors"] == [ERROR]
            and structure["confirmation"] == "UNVERIFIED"
            and hold["openClaimIds"] == ["O1/L1"], "Unexpected structural hold")
    require(audit["final"] and audit["reviewerIdle"] and not audit["recordIncomplete"]
            and not audit["breaches"] and not audit["unexpectedUserMessages"]
            and audit["chainRead"] == audit["chainRequired"] == 35
            and audit["writes"] == audit["readbacks"] == 1 and audit["readbackVerified"]
            and audit["fetches"] == 0 and audit["messages"] == ["UNVERIFIED"]
            and audit["actualResponseModels"] == ["claude-opus-5-5"],
            "Held execution record changed")
    require(context["status"] == "PASS" and not context["compactions"]
            and context["eventsSha256"] == audit["eventsSha256"], "Held context changed")


def collect(guard):
    contents = {}
    prefix = f"held-runs/{RUN}"

    def resolve(path):
        path = Path(path)
        return path if path.is_absolute() else WS / path

    def put(name, raw):
        require(not name.endswith(".jsonl") and name not in contents, "Invalid held archive path")
        contents[name] = raw

    def copy(path, name, expected=None):
        raw = frozen(resolve(path), expected)
        put(f"{prefix}/{name}", raw)
        guard.check()
        return raw

    def ref(item, name):
        return copy(item["path"], name, item["sha256"])

    hold = json.loads(copy(HERE / f"{RUN}-structure-hold.json", "structure-hold.json", HOLD_SHA))
    mechanics = json.loads(ref(hold["final"], "final.json"))
    audit_raw = frozen(resolve(hold["audit"]["path"]), hold["audit"]["sha256"])
    audit = json.loads(audit_raw)
    context = json.loads(ref(hold["context"], "context.json"))
    structure = json.loads(ref(hold["structure"], "structure.json"))
    verify_hold(hold, mechanics, audit, context, structure)
    ref(hold["report"], "report.md")
    ref(hold["tool"], "record-structure-hold.py")
    support = load_module("b120_held_bounded_audit", WS / "scratch-115" / "assemble-closure.py")
    put(f"{prefix}/audit-summary.json",
        json_bytes(support.bounded_audit(resolve(hold["audit"]["path"]))))
    spec = json.loads(copy(HERE / f"{RUN}-spec.json", "spec.json"))
    preflight = json.loads(copy(HERE / f"{RUN}-preflight.json", "preflight.json"))
    admission = json.loads(copy(HERE / f"{RUN}-admission.json", "admission.json"))
    require(spec["session"] == preflight["session"] == admission["session"] == SESSION
            and spec["candidate"] == preflight["candidate"] == admission["candidate"] == SNAPSHOT
            and spec["run"] == preflight["run"] == admission["run"] == RUN
            and preflight["config"] == admission["config"], "Held preparation differs")
    config = json.loads(ref(preflight["config"], "config.json"))
    require(config["run"] == RUN and config["maxWebFetches"] == 0, "Held config differs")
    for item in config["files"]:
        frozen(resolve(item["path"]), item["sha256"])
        guard.check()
    for name in ("prompt", "kickoff"):
        copy(config[name], f"{name}.txt")
    chain_raw = frozen(resolve(preflight["chain"]["path"]), preflight["chain"]["sha256"])
    require(resolve(config["chainManifest"]) == resolve(preflight["chain"]["path"]),
            "Held chain binding differs")
    chain = json.loads(chain_raw)
    put(f"{prefix}/chain/manifest.json", chain_raw)
    require(len(chain["segments"]) == 35, "Held chain count changed")
    for segment in chain["segments"]:
        raw = frozen(resolve(segment["path"]), segment["sha256"])
        packed = gzip.compress(raw, mtime=0)
        require(gzip.decompress(packed) == raw, "Held chain compression differed")
        put(f"{prefix}/chain/{Path(segment['path']).name}.gz", packed)
        guard.check()
    record = {
        "run": RUN, "family": "claude", "session": SESSION, "snapshot": SNAPSHOT,
        "rawVerdict": "UNVERIFIED", "status": "HELD_STRUCTURE",
        "reviewEvidenceAccepted": False, "confirmationAccepted": False,
        "includedInAcceptedLineage": False, "finalAcceptance": False,
        "hold": {"path": f"{prefix}/structure-hold.json", "sha256": HOLD_SHA},
        "report": {"path": f"{prefix}/report.md", "sha256": hold["report"]["sha256"]},
        "eventsSha256": audit["eventsSha256"],
        "preservation": "Byte-exact report and failure records, lossless delivered chain, "
                        "bounded execution summary. No raw event payloads or implied acceptance.",
    }
    put("held-runs/index.json", json_bytes([record]))
    return contents, record
