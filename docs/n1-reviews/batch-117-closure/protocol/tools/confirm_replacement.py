"""Reconstruct a same-family confirmation after the original context exhausted.

No context/audit/structure gate is relaxed. The failed run is bound as unavailable
history, never supplied as teaching evidence or attributed to the replacement.
"""
import json
import re
import sys
from pathlib import Path

from common import (COORDINATOR, WS, at_commit, freeze_json, frozen, git, load_batch,
                    load_module, require, review_dir, start_guard, verify_packet, write_frozen)
from confirm_v2 import admit, binding, clean, final, revision_diff


def require_replacement(spec, initial, launch, held, context, prior):
    require(spec["session"] != spec["originalSession"] == launch["session"] == held["session"]
            and spec["family"] == held["family"] == prior["family"],
            "Replacement must identify the unavailable original and the same family")
    require(initial.get("reviewAccepted") is True
            and held["candidate"] == spec["candidate"]
            and held["confirmationAccepted"] is False and held["reviewEvidenceAccepted"] is False
            and held["status"] == "HELD_CONTEXT_COMPACTION"
            and context["status"] == "FAIL" and context["compactions"],
            "No audited context-exhaustion basis for a replacement")
    require(prior["session"] == spec["originalSession"]
            and prior["reviewEvidenceAccepted"] is True and prior["confirmationAccepted"] is False,
            "Earlier substantive confirmation lineage differs")


def replacement_prompt(text):
    replacements = (
        ("confirmation of your own accepted B117 initial review",
         "same-family replacement confirmation of the accepted B117 initial review"),
        ("Your own initial report:", "Original reviewer's initial report:"),
        ("your own unchanged initial report", "the original reviewer's unchanged initial report"),
        ("Read your own full report", "Read the original reviewer's full report"),
        ("including changes not requested by you", "including changes not requested in the source reports"),
    )
    for old, new in replacements:
        require(text.count(old) == 1, f"Unexpected frozen renderer wording: {old}")
        text = text.replace(old, new)
    return text + (
        "\nREPLACEMENT IDENTITY AND SCOPE\n"
        "You are a fresh same-family reviewer, not the author of the historical reports. "
        "The original context is unavailable. Do not claim retained firsthand context. "
        "All conclusions must be established from the complete source records read in this chain. "
        "The Dispositions IDs refer to the initial report only. Also independently address every "
        "finding and consequential limit of the separately supplied earlier substantive confirmation "
        "and both author responses in your Basis, Findings or Limits, citing their distinct source paths. "
        "The unusable context-exhausted run and its conclusions are not supplied. "
        "Missing evidence must remain UNVERIFIED, not inferred from an old verdict.\n"
    )


def build(spec_path):
    spec = json.loads(frozen(spec_path))
    config = load_batch(spec["batch"])
    records, run = review_dir(spec["batch"]), spec["run"]
    out = records / "confirm"
    require(re.fullmatch(rf"N1-B{spec['batch']}-[A-Z0-9-]+-CONFIRM-\d{{3}}", run), "Invalid run")
    require(spec["family"] in ("claude", "gpt"), "Unknown family")
    clean(config, spec["candidate"])
    read = lambda item: json.loads(frozen(Path(item["path"]), item["sha256"]))
    initial, held, prior = (read(spec[key]) for key in ("acceptance", "unavailable", "prior"))
    launch_path = records / f"{initial['run']}-launch.json"
    launch = json.loads(frozen(launch_path))
    context = read(held["context"])
    require_replacement(spec, initial, launch, held, context, prior)
    require(initial["candidate"] == config["candidate"], "Initial snapshot differs")
    held_final, prior_final = read(held["final"]), read(prior["final"])
    require(held_final["status"] == "HOLD" and held_final["context"] == held["context"]
            and held_final["candidate"] == spec["candidate"], "Held mechanics differ")
    require(prior_final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and prior_final["report"] == prior["report"], "Substantive prior mechanics differ")
    git(config, "merge-base", "--is-ancestor", prior["candidate"], spec["candidate"])
    original = frozen(Path(initial["report"]["path"]), initial["report"]["sha256"])
    previous = frozen(Path(prior["report"]["path"]), prior["report"]["sha256"])
    ids = re.findall(r"(?m)^### ([FO]\d+):", original.decode("utf-8").replace("\r\n", "\n"))
    require(len(ids) == len(set(ids)), "Duplicate original dispositions")
    report = WS / f"reports-{spec['batch']}" / f"{run}.md"
    require(not report.exists(), "Report destination exists")
    sources = [(f"initial-report/{Path(initial['report']['path']).name}", original, None),
               (f"previous-confirmation/{Path(prior['report']['path']).name}", previous, None)]
    bindings = [binding(spec_path), spec["acceptance"], spec["unavailable"], spec["prior"],
                initial["report"], prior["report"], held["context"], held["final"], binding(launch_path)]
    delta, omitted = revision_diff(config, spec["candidate"])
    bindings.append(write_frozen(out / f"{run}-fix.patch", delta))
    sources.append(("diffs/fix.patch", delta, None))
    revised = dict(config, candidate=spec["candidate"])
    guard, _ = start_guard(run)
    try:
        packet, sums, _ = verify_packet(config, guard)
        for path in spec["revisedSources"]:
            data = at_commit(revised, path)
            bindings.append(write_frozen(out / run / "snapshot" / Path(path), data))
            sources.append((f"snapshot/{path}", data, None))
        for path in spec["originalSources"]:
            require(path in sums, f"Unbound original source: {path}")
            data = frozen(packet / Path(path), sums[path])
            bindings.append(binding(packet / Path(path)))
            sources.append((f"original-packet/{path}", data, None))
        for item in spec["additionalSources"]:
            data = frozen(Path(item["path"]), item["sha256"])
            bindings.append({"path": item["path"], "sha256": item["sha256"]})
            sources.append((item["source"], data, None))
        require(len(sources) == len({s[0] for s in sources}), "Duplicate source")
        chain_module = load_module("n1_replacement_chain", records / "review_chain.py")
        chain_path = out / f"{run}-chain.json"
        chain = chain_module.build_chain(sources, WS / "review-chains" / run.lower(), chain_path, guard, run)
    finally:
        require(not guard.finish()["breach"], "RAM guard breached")
    renderer = load_module("n1_replacement_renderer", out / "renderer.py")
    prompt_path, kickoff_path = out / f"{run}-prompt.txt", out / f"{run}-kickoff.txt"
    prompt = renderer.render_prompt({**spec, "scope": config["members"], "dispositionIds": ids},
                                    {"candidate": spec["candidate"], "freeze": config["candidate"],
                                     "originalReport": initial["report"]["path"], "report": str(report)},
                                    chain, prompt_path)
    bindings.append(write_frozen(prompt_path, replacement_prompt(prompt).encode("utf-8")))
    kickoff = (f"Read {prompt_path} using one view call with forceReadLargeFiles: true and no view_range, "
               "then follow its instructions. No other tool call may precede that read.").encode("ascii")
    bindings.extend([write_frozen(kickoff_path, kickoff), binding(chain_path)])
    bindings.extend(binding(out / name) for name in ("renderer.py", "audit-confirm.py", "check-confirm-structure.py"))
    bindings.extend(binding(path) for path in (Path(__file__), Path(__file__).with_name("confirm_v2.py"),
                                              records / "review_chain.py", records / "check-run-context.py"))
    audit_config = {"run": run, "prompt": str(prompt_path), "kickoff": str(kickoff_path), "report": str(report),
                    "coordinator": COORDINATOR, "expectedFamily": spec["family"], "chainManifest": str(chain_path),
                    "completionContract": "entire-message-enum-v1", "reportStructureContract": "confirm-structure-v1",
                    "dispositionIds": ids, "maxWebFetches": 0, "files": bindings}
    result = {"run": run, "batch": spec["batch"], "session": spec["session"], "candidate": spec["candidate"],
              "originalSession": spec["originalSession"], "replacementReason": "audited-context-compaction",
              "priorRun": prior["run"], "unavailable": spec["unavailable"],
              "config": freeze_json(out / f"{run}-config.json", audit_config),
              "kickoff": binding(kickoff_path), "chain": binding(chain_path),
              "segments": len(chain["segments"]), "sourceCount": len(sources),
              "dispositionIds": ids, "diffOmittedPaths": omitted, "preparedOnly": True}
    print(json.dumps(freeze_json(out / f"{run}-preflight.json", result)))


if __name__ == "__main__":
    action, *args = sys.argv[1:]
    if action == "build":
        build(Path(args[0]))
    elif action == "admit":
        admit(Path(args[0]), Path(args[1]))
    elif action == "final":
        final(Path(args[0]))
    else:
        raise SystemExit("build <spec> | admit <preflight> <status> | final <preflight>")
