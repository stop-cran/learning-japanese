"""GPT004 identity-only protocol, existing-source bindings, predecessor and filesystem readiness."""
import json

from b131_review_v4_common import (
    CORE, HERE, IMMUTABLE_BINDINGS, POLICY, PRIOR, RUNS, accepted_prerequisite, frozen, require, sha)
from b131_preflight_003 import validate_report_destination
from b131_preflight_002 import normalize_prompt, verify_chain, verify_subset as verify_original_subset
from b131_capacity_003 import PROFILES, validate_capacity_config, verify_neutral_telemetry, verify_policy


def neutral_inputs():
    preflight = json.loads(frozen(PRIOR / "prompts" / "preflight-compact-003.json",
        "7813a4f972672ed099d1b26628249820d647b6bd2a8ad2c7dccaac507e0f19a0"))
    return preflight["runs"]["claude"]


def derive_prompt(spec):
    old = neutral_inputs()
    raw = frozen(old["prompt"], old["promptSha256"])
    for before, after in ((old["prompt"], spec["prompt"]), (old["report"], spec["report"]),
                          (old["run"], spec["run"])):
        raw = raw.replace(before.encode("utf-8"), after.encode("utf-8"))
    return raw


def verify_prompt_identity(spec):
    require(frozen(spec["prompt"], spec["promptSha256"]) == derive_prompt(spec),
            "GPT004 prompt differs beyond the three exact neutral identity/path substitutions")
    old = neutral_inputs()
    expected = old["kickoffText"].replace(old["prompt"], spec["prompt"])
    require(frozen(spec["kickoff"]).decode("ascii") == spec["kickoffText"] == expected,
            "GPT004 kickoff differs beyond bootstrap path")
    return {"status": "PASS_IDENTITY_ONLY", "sourcePromptSha256": old["promptSha256"],
            "permittedChanges": ["exact prompt path", "exact report path", "exact run ID"]}


def verify_prerequisite(preflight):
    expected = accepted_prerequisite()
    require(preflight["sequentialPrerequisite"] == expected, "Accepted Claude003 prerequisite binding differs")
    return expected


def verify_subset(guard, initial=False):
    for path, digest in IMMUTABLE_BINDINGS:
        frozen(path, digest)
        guard.check()
    frozen(HERE / "review_chain.py", IMMUTABLE_BINDINGS[3][1])
    frozen(HERE / "core-chain-compact-002.json", IMMUTABLE_BINDINGS[2][1])
    verify_neutral_telemetry()
    verify_policy()
    return verify_original_subset(guard, initial=initial)


def verify_protocol(preflight):
    require(preflight["order"] == ["gpt"] and list(preflight["runs"]) == ["gpt"],
            "Only the fresh GPT004 attempt is preparable; accepted Claude003 must not rerun")
    verify_prerequisite(preflight)
    spec = preflight["runs"]["gpt"]
    require(spec["run"] == RUNS[0] and spec["launch"] == {
        "mode": "interactive", "model": PROFILES["gpt"]["selectedModel"], "contextTier": "long_context",
        "freshSession": True, "sessionName": "B131 GPT independent review004"}, "Fresh GPT004 identity differs")
    proof = validate_report_destination(spec)
    identity = verify_prompt_identity(spec)
    config = json.loads(frozen(spec["auditConfig"]))
    for binding in config["files"]:
        frozen(binding["path"], binding["sha256"])
    validate_capacity_config(config)
    require(config["run"] == spec["run"] and config["report"] == spec["report"]
            and config["expectedFamily"] == "gpt" and config["coreManifest"] == str(CORE)
            and config["capacityForecastSha256"] == IMMUTABLE_BINDINGS[4][1]
            and config["maxWebFetches"] == 0
            and preflight["capacityPolicySha256"] == sha(frozen(POLICY)), "Fresh004 bindings differ")
    return {"status": "PASS_IDENTITY_BOUND_GPT004", "identity": identity, "reportDestinations": [proof]}


def path_inventory(preflight):
    spec = preflight["runs"]["gpt"]
    chain = json.loads(frozen(CORE, IMMUTABLE_BINDINGS[2][1]))
    for segment in chain["segments"]:
        frozen(segment["path"], segment["sha256"])
    verify_prompt_identity(spec)
    directory = HERE / "chains" / ("b131-" + spec["run"] + "-extension-004")
    return {"bootstrap": spec["prompt"], "coreManifest": str(CORE), "coreSegments": len(chain["segments"]),
            "report": validate_report_destination(spec), "extensionDirectory": str(directory),
            "extensionManifest": str(HERE / (spec["run"] + "-extension.json")),
            "phase2Message": str(HERE / (spec["run"] + "-phase2-message.txt")),
            "extensionOwner": "prepare_chain_b131_004.py; all sources/SHAs/costs gated before chain/message creation",
            "reportReadback": "Same report path; sole reviewer create after complete reads, then exact full readback",
            "auditOutput": str(HERE / spec["run"]),
            "auditOwner": "audit-review.py creates its own timestamped audit directory before snapshots",
            "futureEvents": "Fresh app session only; validated after future launch, not claimed to exist now"}
