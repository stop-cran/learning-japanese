"""Fresh path readiness, actual directory write probes and unchanged evidence verification."""
import json
import os
import stat
import uuid
from pathlib import Path

from b131_review_v3_common import (
    CORE, DEFAULT_PREFLIGHT, FORECAST, HERE, IMMUTABLE_BINDINGS, RUNS,
    frozen, require, sha)
from b131_preflight_002 import normalize_prompt, verify_chain, verify_subset as verify_evidence_subset


def validate_report_destination(spec):
    report = Path(spec["report"])
    parent = report.parent
    require(report.is_absolute(), "Report destination must be absolute")
    require(parent.exists(), "Missing report parent: " + str(parent))
    require(parent.is_dir(), "Report parent is not a directory: " + str(parent))
    require(not report.exists(), "Report already present: " + str(report))
    info = parent.stat()
    require(bool(info.st_mode & stat.S_IWRITE)
            and not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_READONLY
            and os.access(parent, os.W_OK), "Report parent is not writable or is ReadOnly: " + str(parent))
    require(not any(parent.iterdir()), "Fresh report parent must be empty: " + str(parent))
    probe = parent / (".b131-path-probe-" + uuid.uuid4().hex)
    created = False
    try:
        with probe.open("xb") as stream:
            created = True
            stream.write(b"B131 report-parent exclusive-create/readback/delete probe\n")
        require(probe.read_bytes() == b"B131 report-parent exclusive-create/readback/delete probe\n",
                "Report parent write/readback probe differs")
    finally:
        if created:
            probe.unlink()
    require(not any(parent.iterdir()) and not report.exists(), "Report destination changed during preflight")
    return {"report": str(report), "parent": str(parent), "exists": True, "isDirectory": True,
            "directoryReadOnly": False, "empty": True, "reportAbsent": True,
            "exclusiveCreateReadbackDelete": "PASS"}


def verify_subset(guard, initial=False):
    for path, digest in IMMUTABLE_BINDINGS:
        frozen(path, digest)
        guard.check()
    frozen(HERE / "review_chain.py", IMMUTABLE_BINDINGS[3][1])
    frozen(HERE / "core-chain-compact-002.json", IMMUTABLE_BINDINGS[2][1])
    return verify_evidence_subset(guard, initial=initial)


def verify_protocol(preflight):
    require(preflight["order"] == ["claude", "gpt"], "Family order differs")
    prompts, kickoffs, proofs = [], [], []
    for family, spec in preflight["runs"].items():
        proofs.append(validate_report_destination(spec))
        require(spec["run"] in RUNS and spec["run"] == "N1-B131-" + family.upper() + "-003",
                "Not a fresh003 run")
        config = json.loads(frozen(spec["auditConfig"]))
        for binding in config["files"]:
            frozen(binding["path"], binding["sha256"])
        require(config["run"] == spec["run"] and config["report"] == spec["report"]
                and config["expectedFamily"] == family and config["coreManifest"] == str(CORE)
                and config["capacityForecastSha256"] == IMMUTABLE_BINDINGS[4][1]
                and config["maxWebFetches"] == 0, "Fresh run/evidence bindings differ")
        prompts.append(frozen(spec["prompt"], spec["promptSha256"]))
        kickoff = frozen(spec["kickoff"])
        require(kickoff.decode("ascii") == spec["kickoffText"], "Kickoff differs")
        require(spec["prompt"].encode() in kickoff and spec["report"].encode() in prompts[-1],
                "Bootstrap/report path is absent from delivered instructions")
        kickoffs.append(kickoff)
    require(normalize_prompt(prompts[0]) == normalize_prompt(prompts[1]), "Prompt pair differs beyond identity")
    require(normalize_prompt(kickoffs[0]) == normalize_prompt(kickoffs[1]), "Kickoff pair differs beyond identity")
    return {"status": "PASS_PAIRED_PROTOCOL", "runs": [spec["run"] for spec in preflight["runs"].values()],
            "reportDestinations": proofs}


def path_inventory(preflight):
    chain = json.loads(frozen(CORE, IMMUTABLE_BINDINGS[2][1]))
    for segment in chain["segments"]:
        frozen(segment["path"], segment["sha256"])
    records = []
    for spec in preflight["runs"].values():
        frozen(spec["prompt"], spec["promptSha256"])
        frozen(spec["kickoff"])
        require(chain["segments"][0]["path"].encode() in frozen(spec["prompt"]),
                "Prompt core entry point differs")
        parent = validate_report_destination(spec)
        records.append({
            "run": spec["run"], "bootstrap": {"path": spec["prompt"], "state": "exists frozen/readable"},
            "core": {"manifest": str(CORE), "segments": len(chain["segments"]), "state": "all exist frozen/readable"},
            "reportCreate": parent,
            "extension": {
                "directory": str(HERE / "chains" / ("b131-" + spec["run"] + "-extension-002")),
                "manifest": str(HERE / (spec["run"] + "-extension.json")),
                "message": str(HERE / (spec["run"] + "-phase2-message.txt")),
                "owner": "prepare_chain_b131_003.py -> build_chain/write_frozen",
                "state": "created and SHA/coverage/capacity-verified before any phase2 message is exposed",
                "noLaunchNeeded": True},
            "reportReadback": {"path": spec["report"], "owner": "reviewer's sole create after all reads",
                               "state": "same already-writable parent; auditor requires exact complete readback"},
            "auditOutput": {"directory": str(HERE / spec["run"]),
                            "owner": "audit-review.py root.mkdir(parents=True) before snapshot writes"},
            "futureSessionEvents": {"owner": "future app-created fresh session; not accessed in preparation",
                                     "state": "validated by lifecycle launch/phase1/final, not claimed to exist now"}})
    return records
