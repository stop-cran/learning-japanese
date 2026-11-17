"""Render one fresh clean-path initial-review attempt after a frozen VOID quarantine of the previous attempt.

Identical to build-prompts-v3.py (whose derive() is reused unchanged) except for the predecessor gate:
v3 accepts only a frozen HOLD_STRUCTURE_FAILED record; v4 accepts only a frozen quarantine whose status is a
VOID, with no review or publication acceptance, the same candidate, still-matching report/final hashes, and a
frozen authorization record bound to that quarantine. Nothing from earlier attempts is supplied.
Usage: python -B build-prompts-v4.py <batch> <claude|gpt> <attempt> <quarantine.json> <authorization.json>
Writes prompts/initial-<key>-<NNN>.txt, kickoff, audit config and prompts/preflight-<key>-<NNN>.json.
"""
import copy
import datetime
import json
import sys
from pathlib import Path

from common import TOOLS, freeze_json, frozen, load_batch, load_module, require, review_dir, sha, verify_packet, \
    write_frozen

V3 = TOOLS / "build-prompts-v3.py"
v3 = load_module("build_prompts_v3_for_v4", V3)


def check_predecessor(quarantine, authorization, quarantine_sha, candidate, previous, key, attempt):
    require(quarantine.get("run") == previous, "Quarantine is not for the immediately preceding attempt")
    require(str(quarantine.get("status", "")).startswith("VOID_"), "Predecessor is not a frozen VOID")
    require(quarantine.get("reviewAccepted") is False and quarantine.get("publicationAccepted") is False,
            "VOID predecessor must have no review or publication acceptance")
    require(quarantine.get("candidate") == candidate, "Quarantine candidate differs from the batch candidate")
    bound = authorization.get("predecessor") or {}
    require(bound.get("run") == previous and bound.get("sha256") == quarantine_sha,
            "Authorization is not bound to this exact quarantine")
    require(authorization.get("family") == key and authorization.get("attempt") == attempt
            and authorization.get("candidate") == candidate, "Authorization scope differs from this attempt")
    require(authorization.get("userAuthorization"), "Authorization record lacks user provenance")


def main(batch, key, attempt, quarantine_path, authorization_path):
    attempt = int(attempt)
    require(2 <= attempt <= 3, "Clean-path reruns are limited to attempts 002 and 003")
    config = load_batch(batch)
    n, records = config["batch"], review_dir(batch)
    prompts = records / "prompts"
    base_path = prompts / "preflight.json"
    base_raw = frozen(base_path)
    base = json.loads(base_raw)
    require(key in base["runs"], "Unknown run family")
    previous = base["runs"][key]["run"].replace("-001", f"-{attempt - 1:03d}")
    quarantine_path, authorization_path = Path(quarantine_path), Path(authorization_path)
    require(quarantine_path == records / f"{previous}-quarantine.json", "Quarantine must be the batch record")
    require(authorization_path.parent == records, "Authorization must be a batch review record")
    quarantine_raw, authorization_raw = frozen(quarantine_path), frozen(authorization_path)
    quarantine = json.loads(quarantine_raw)
    check_predecessor(quarantine, json.loads(authorization_raw), sha(quarantine_raw), config["candidate"],
                      previous, key, attempt)
    for name in ("report", "final"):
        frozen(quarantine[name]["path"], quarantine[name]["sha256"])
    _, _, packet_sha = verify_packet(config)
    require(packet_sha == base["packetManifestSha256"]
            and sha(frozen(records / "core-chain.json")) == base["coreChainSha256"], "Packet or chain changed")
    template = frozen(prompts / "template.txt", base["template"]["templateSha256"])
    original = base["runs"][key]
    original_prompt = frozen(original["prompt"], original["promptSha256"])
    original_kickoff = frozen(original["kickoff"])
    require(original_kickoff.decode("ascii") == original["kickoffText"], "Frozen kickoff changed")
    original_audit = json.loads(frozen(original["auditConfig"]))
    derived = v3.derive(original, original_audit, original_prompt, original_kickoff, n, key, attempt, prompts)
    require(not derived["report"].exists(), "Attempt report already exists")
    for name in ("prompt", "kickoff", "audit"):
        require(not derived[name][0].exists(), f"Attempt {name} already exists")
    outputs = {name: write_frozen(*derived[name]) for name in ("prompt", "kickoff", "audit")}
    record = copy.deepcopy(base)
    record["runs"][key] = derived["spec"]
    record.update(createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  basePreflight={"path": str(base_path), "sha256": sha(base_raw)},
                  attempt={"family": key, "number": attempt, "supersedesRun": previous,
                           "predecessorVoid": {"path": str(quarantine_path), "sha256": sha(quarantine_raw),
                                               "status": quarantine["status"]},
                           "authorization": {"path": str(authorization_path), "sha256": sha(authorization_raw)},
                           "identitySubstitutions": derived["counts"], "templateSha256": sha(template),
                           "reverseEqualsFrozenAttempt001": True, "outputs": outputs},
                  builder={"path": str(TOOLS / "build-prompts-v4.py"),
                           "sha256": sha((TOOLS / "build-prompts-v4.py").read_bytes()),
                           "derivationFrom": {"path": str(V3), "sha256": sha(V3.read_bytes())}})
    record["blindness"] += (" Fresh clean-path attempt after a VOID: no earlier report, quarantine, verdict, "
                            "finding, observation or failure detail is supplied to the new reviewer.")
    print(json.dumps(freeze_json(prompts / f"preflight-{key}-{attempt:03d}.json", record), ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 6 or sys.argv[2] not in ("claude", "gpt"):
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
