"""Render one fresh attempt-numbered rerun of a batch's frozen initial-review prompt (clean path only).

The new prompt must equal the frozen attempt-001 prompt for the same family except the exact run-identity
substitutions (run id, prompt path and report path). Nothing from earlier attempts is supplied.
Usage: python -B build-prompts-v3.py <batch> <claude|gpt> <attempt>
Writes prompts/initial-<key>-<NNN>.txt, kickoff, audit config and prompts/preflight-<key>-<NNN>.json.
"""
import copy
import datetime
import json
import sys
from pathlib import Path

from common import TOOLS, freeze_json, frozen, json_bytes, load_batch, require, review_dir, sha, verify_packet, write_frozen

BUILDER_V2 = "build-prompts-v2.py"


def identity_pairs(n, label, key, attempt):
    new = f"{attempt:03d}"
    return [(f"N1-B{n}-{label}-001", f"N1-B{n}-{label}-{new}"),
            (f"initial-{key}-001", f"initial-{key}-{new}")]


def substitute(data, pairs):
    counts = []
    for old, new in pairs:
        old_b, new_b = old.encode("utf-8"), new.encode("utf-8")
        require(new_b not in data, f"Attempt identity {new!r} already present in the source")
        counts.append({"from": old, "to": new, "count": data.count(old_b)})
        data = data.replace(old_b, new_b)
    return data, counts


def reverse(data, pairs):
    for old, new in reversed(pairs):
        data = data.replace(new.encode("utf-8"), old.encode("utf-8"))
    return data


def derive(original_spec, original_audit, original_prompt, original_kickoff, n, key, attempt, prompts):
    label = original_spec["run"].split("-")[2]
    pairs = identity_pairs(n, label, key, attempt)
    prompt, prompt_counts = substitute(original_prompt, pairs)
    kickoff, kickoff_counts = substitute(original_kickoff, pairs)
    require(all(c["count"] > 0 for c in prompt_counts) and kickoff_counts[1]["count"] == 1,
            "Expected every identity token in the frozen prompt and one prompt path in the kickoff")
    require(reverse(prompt, pairs) == original_prompt and reverse(kickoff, pairs) == original_kickoff,
            "Attempt prompt differs from the frozen prompt beyond run identity")
    new = f"{attempt:03d}"
    run = pairs[0][1]
    prompt_path = prompts / f"initial-{key}-{new}.txt"
    kickoff_path = prompts / f"kickoff-{key}-{new}.txt"
    report = Path(original_spec["report"]).with_name(f"initial-{key}-{new}.md")
    require(str(prompt_path) in prompt.decode("utf-8") and str(report) in prompt.decode("utf-8")
            and str(prompt_path) in kickoff.decode("ascii"), "Rendered paths do not match the attempt files")
    audit = copy.deepcopy(original_audit)
    old_files = {original_spec["prompt"], original_spec["kickoff"]}
    audit.update(run=run, kickoff=str(kickoff_path), prompt=str(prompt_path), report=str(report))
    audit["files"] = [f for f in original_audit["files"] if f["path"] not in old_files] + [
        {"path": str(prompt_path), "sha256": sha(prompt)}, {"path": str(kickoff_path), "sha256": sha(kickoff)}]
    spec = copy.deepcopy(original_spec)
    spec.update(run=run, prompt=str(prompt_path), promptSha256=sha(prompt), kickoff=str(kickoff_path),
                kickoffText=kickoff.decode("ascii"), auditConfig=str(prompts / f"audit-config-{run}.json"),
                report=str(report))
    spec["launch"]["sessionName"] = original_spec["launch"]["sessionName"].replace(" 001", f" {new}")
    require(spec["launch"]["sessionName"] != original_spec["launch"]["sessionName"], "Session name unchanged")
    return {"prompt": (prompt_path, prompt), "kickoff": (kickoff_path, kickoff),
            "audit": (prompts / f"audit-config-{run}.json", json_bytes(audit)), "spec": spec,
            "counts": {"prompt": prompt_counts, "kickoff": kickoff_counts}, "report": report}


def main(batch, key, attempt):
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
    hold = json.loads(frozen(records / f"{previous}-structure-hold.json"))
    require(hold["status"] == "HOLD_STRUCTURE_FAILED" and hold["reviewAccepted"] is False
            and hold["candidate"] == config["candidate"], "Rerun requires a frozen mechanical structure hold")
    _, _, packet_sha = verify_packet(config)
    require(packet_sha == base["packetManifestSha256"]
            and sha(frozen(records / "core-chain.json")) == base["coreChainSha256"], "Packet or chain changed")
    template = frozen(prompts / "template.txt", base["template"]["templateSha256"])
    original = base["runs"][key]
    original_prompt = frozen(original["prompt"], original["promptSha256"])
    original_kickoff = frozen(original["kickoff"])
    require(original_kickoff.decode("ascii") == original["kickoffText"], "Frozen kickoff changed")
    original_audit = json.loads(frozen(original["auditConfig"]))
    derived = derive(original, original_audit, original_prompt, original_kickoff, n, key, attempt, prompts)
    require(not derived["report"].exists(), "Attempt report already exists")
    for name in ("prompt", "kickoff", "audit"):
        require(not derived[name][0].exists(), f"Attempt {name} already exists")
    outputs = {name: write_frozen(*derived[name]) for name in ("prompt", "kickoff", "audit")}
    record = copy.deepcopy(base)
    record["runs"][key] = derived["spec"]
    record.update(createdAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  basePreflight={"path": str(base_path), "sha256": sha(base_raw)},
                  attempt={"family": key, "number": attempt, "supersedesRun": previous,
                           "hold": {"path": str(records / f"{previous}-structure-hold.json"),
                                    "sha256": sha(frozen(records / f"{previous}-structure-hold.json"))},
                           "identitySubstitutions": derived["counts"], "templateSha256": sha(template),
                           "reverseEqualsFrozenAttempt001": True, "outputs": outputs},
                  builder={"path": str(TOOLS / "build-prompts-v3.py"),
                           "sha256": sha((TOOLS / "build-prompts-v3.py").read_bytes()),
                           "baseBuilder": str(TOOLS / BUILDER_V2)})
    record["blindness"] += (" Fresh clean-path attempt: no earlier report, hold, verdict, finding or "
                            "structure error is supplied to the new reviewer.")
    print(json.dumps(freeze_json(prompts / f"preflight-{key}-{attempt:03d}.json", record), ensure_ascii=False))


if __name__ == "__main__":
    if len(sys.argv) != 4 or sys.argv[2] not in ("claude", "gpt"):
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
