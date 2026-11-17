"""Same-reviewer deltas after either an accepted or an unaccepted confirmation.

confirm_v2 stays unchanged and still prepares first confirmations. This module adds only
build_followup: the prior confirmation report is the reviewer's basis, and the runtime diff is
the delta from the prior confirmation's candidate to the new signed revision.
"""
import json
import re
import sys
from pathlib import Path

from common import (COORDINATOR, WS, at_commit, freeze_json, frozen, git, load_batch, load_module,
                    require, review_dir, start_guard, write_frozen)
from b130_compact_common import verify_packet
from confirm_b130_fresh_context import binding, clean, final, revision_diff
from b130_followup_admission import admit
from b130_followup_lineage import require_followup_identity

RUN = r"N1-B{batch}-[A-Z0-9-]+-CONFIRM-(\d{{3}})"


def run_number(batch, run):
    match = re.fullmatch(RUN.format(batch=batch), run)
    require(match, f"Invalid run: {run}")
    return int(match[1])


def normalized(raw):
    return raw.decode("utf-8").replace("\r\n", "\n")


def require_prior_state(spec, prior, findings):
    require(prior.get("reviewEvidenceAccepted") is True, "Prior evidence is not accepted")
    if spec["basis"] == "accepted-confirmation":
        require(prior.get("confirmationAccepted") is True and prior["verdict"] == "CONFIRMED"
                and spec.get("priorVerdict") == "CONFIRMED"
                and prior.get("openClaimIds") == spec.get("openClaimIds") == []
                and not findings and prior["acceptedNewFindings"] == [],
                "Accepted basis relabels the prior verdict or leaves open claims")
    else:
        require(prior.get("confirmationAccepted") is False,
                "Unaccepted basis cannot relabel an accepted prior snapshot")
        if spec["basis"] == "confirmation":
            require(prior["verdict"] == "NEEDS FIX" and findings,
                    "Confirmation basis needs an accepted NEEDS FIX")
        else:
            require(spec["basis"] == "held-confirmation" and spec.get("priorVerdict") == prior["verdict"]
                    and spec.get("openClaimIds") == prior["openClaimIds"] and prior["openClaimIds"],
                    "Held basis relabels the prior verdict or open claims")


def render_followup_prompt(renderer, spec, packet, chain, prompt_path):
    accepted = spec["basis"] == "accepted-confirmation"
    rendered_spec = {**spec, "basis": "confirmation"} if accepted else spec
    text = renderer.render_prompt(rendered_spec, packet, chain, prompt_path)
    if accepted:
        old = f"accepted B{spec['batch']} adjudicated previous confirmation"
        require(text.count(old) == 1, "Accepted-follow-up renderer anchor changed")
        text = text.replace(old, f"accepted B{spec['batch']} previous confirmation")
        text += (
            "\nACCEPTED SNAPSHOT FOLLOW-UP\n"
            "Your prior CONFIRMED report remains accepted on its earlier snapshot. It has no "
            "open finding. This assignment checks only the subsequent actual delta and its "
            "new source/check evidence; it does not relabel that earlier acceptance as held "
            "or transfer it automatically to the new snapshot. Preserve all prior limits.\n"
        )
    return text


def verify_prior(spec, config, records):
    """Return (initial acceptance, prior acceptance, prior report bytes) after lineage checks."""
    initial = json.loads(frozen(Path(spec["acceptance"]["path"]), spec["acceptance"]["sha256"]))
    require(initial.get("reviewAccepted") is True and initial["candidate"] == config["candidate"],
            "Initial review is not accepted on the freeze")
    launch = json.loads(frozen(records / f"{initial['run']}-launch.json"))
    require_followup_identity(spec, initial, launch, records)
    prior = json.loads(frozen(Path(spec["prior"]["path"]), spec["prior"]["sha256"]))
    require(prior["family"] == spec["family"] and prior["session"] == spec["session"],
            "Prior confirmation belongs to another reviewer")
    require(run_number(spec["batch"], prior["run"]) < run_number(spec["batch"], spec["run"]),
            "Follow-up must use a later run number")
    prior_spec = json.loads(frozen(records / "confirm" / f"{prior['run']}-spec.json"))
    require(prior_spec["acceptance"] == spec["acceptance"] and prior_spec["session"] == spec["session"],
            "Prior confirmation has another initial lineage")
    mechanics = json.loads(frozen(Path(prior["final"]["path"]), prior["final"]["sha256"]))
    require(mechanics["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and mechanics["run"] == prior["run"] and mechanics["candidate"] == prior["candidate"]
            and mechanics["confirmation"] == prior["verdict"] and mechanics["report"] == prior["report"],
            "Prior mechanics contradict its adjudication")
    frozen(Path(prior["adjudication"]["path"]), prior["adjudication"]["sha256"])
    report = frozen(Path(prior["report"]["path"]), prior["report"]["sha256"])
    findings = re.findall(r"(?m)^### (F\d+):", normalized(report))
    require(set(findings) == set(prior["acceptedNewFindings"]), "Prior report has unaccepted findings")
    require_prior_state(spec, prior, findings)
    require(prior["candidate"] != spec["candidate"], "Follow-up repeats the prior candidate")
    git(config, "merge-base", "--is-ancestor", prior["candidate"], spec["candidate"])
    return initial, prior, report


def build_followup(spec_path):
    spec = json.loads(frozen(spec_path))
    config = load_batch(spec["batch"])
    records = review_dir(spec["batch"])
    out = records / "confirm"
    run = spec["run"]
    run_number(spec["batch"], run)
    require(spec["family"] in ("claude", "gpt"), "Unknown family")
    clean(config, spec["candidate"])
    initial, prior, previous = verify_prior(spec, config, records)
    ids = re.findall(r"(?m)^### ([FO]\d+):", normalized(previous))
    require(len(ids) == len(set(ids)), "Duplicate prior dispositions")
    report = WS / f"reports-{spec['batch']}" / f"{run}.md"
    require(not report.exists(), "Report destination already exists")
    original = frozen(Path(initial["report"]["path"]), initial["report"]["sha256"])
    sources = [(f"previous-confirmation/{Path(prior['report']['path']).name}", previous, None),
               (f"initial-report/{Path(initial['report']['path']).name}", original, None)]
    bindings = [binding(spec_path), spec["acceptance"], spec["prior"], prior["report"], initial["report"]]
    if "reviewerOrigin" in spec:
        bindings.append(spec["reviewerOrigin"])
    bindings.append(binding(Path(__file__).with_name("b130_followup_lineage.py")))
    delta, omitted = revision_diff(dict(config, candidate=prior["candidate"]), spec["candidate"])
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
            require(path in sums, f"Unbound original source {path}")
            data = frozen(packet / Path(path), sums[path])
            bindings.append(binding(packet / Path(path)))
            sources.append((f"original-packet/{path}", data, None))
        for item in spec["additionalSources"]:
            data = frozen(Path(item["path"]), item["sha256"])
            bindings.append({"path": item["path"], "sha256": item["sha256"]})
            sources.append((item["source"], data, None))
        require(len(sources) == len({s[0] for s in sources}), "Duplicate source")
        chain_module = load_module("n1_confirm_chain", records / "review_chain.py")
        chain_path = out / f"{run}-chain.json"
        chain = chain_module.build_chain(sources, WS / "review-chains" / run.lower(), chain_path, guard, run)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM guard breached")
    renderer = load_module("n1_confirm_renderer", out / "renderer.py")
    prompt_path, kickoff_path = out / f"{run}-prompt.txt", out / f"{run}-kickoff.txt"
    renderer_spec = {**spec, "scope": config["members"], "dispositionIds": ids}
    packet_info = {"candidate": spec["candidate"], "freeze": prior["candidate"],
                   "originalReport": prior["report"]["path"], "report": str(report)}
    prompt_text = render_followup_prompt(renderer, renderer_spec, packet_info, chain, prompt_path)
    if "reviewerOrigin" in spec:
        prompt_text += ("\nCONTINUING FRESH-REVIEWER IDENTITY\n"
                        "You are continuing your own prior fresh-context confirmation. The original "
                        "initial report was written by another reviewer of the same family; do not "
                        "claim firsthand authorship of it or retained context from that session. "
                        "Your own previous confirmation and the actual subsequent delta are the "
                        "basis for this bounded follow-up. Preserve all prior limits.\n")
    if spec["basis"] == "held-confirmation":
        prompt_text = prompt_text.replace("recorded a gloss-overlap scan",
                                          "retained the original D18 effect-allocation question").replace(
            "and to each scan decision", "and to the proposed precaution")
    prompt = prompt_text.encode("utf-8")
    kickoff = (f"Read {prompt_path} using one view call with forceReadLargeFiles: true and no view_range, "
               "then follow its instructions. No other tool call may precede that read.").encode("ascii")
    bindings.extend([write_frozen(prompt_path, prompt), write_frozen(kickoff_path, kickoff), binding(chain_path)])
    bindings.extend(binding(out / name) for name in ("renderer.py", "audit-confirm.py", "check-confirm-structure.py"))
    bindings.extend(binding(path) for path in (Path(__file__), Path(__file__).with_name("confirm_b130_fresh_context.py"),
                                              records / "review_chain.py", records / "check-run-context.py"))
    audit_config = {"run": run, "prompt": str(prompt_path), "kickoff": str(kickoff_path), "report": str(report),
                    "coordinator": COORDINATOR, "expectedFamily": spec["family"], "chainManifest": str(chain_path),
                    "completionContract": "entire-message-enum-v1", "reportStructureContract": "confirm-structure-v1",
                    "dispositionIds": ids, "maxWebFetches": 0, "files": bindings}
    config_binding = freeze_json(out / f"{run}-config.json", audit_config)
    result = {"originalSession": spec["originalSession"], "reviewerOrigin": spec["reviewerOrigin"],
              "run": run, "batch": spec["batch"], "session": spec["session"], "candidate": spec["candidate"],
              "basis": spec["basis"], "prior": spec["prior"], "priorRun": prior["run"],
              "diffBase": prior["candidate"], "config": config_binding, "kickoff": binding(kickoff_path),
              "chain": binding(chain_path), "segments": len(chain["segments"]), "sourceCount": len(sources),
              "dispositionIds": ids, "diffOmittedPaths": omitted,
              "diffScope": "Delta from the prior confirmation's candidate, excluding generated manifest and "
                           "contributor docs. Responses and neutral evidence are explicitly selected in the spec.",
              "memory": memory, "preparedOnly": True}
    print(json.dumps(freeze_json(out / f"{run}-preflight.json", result)))


if __name__ == "__main__":
    action, *args = sys.argv[1:]
    if action == "build":
        build_followup(Path(args[0]))
    elif action == "admit":
        admit(Path(args[0]), Path(args[1]))
    elif action == "final":
        final(Path(args[0]))
    else:
        raise SystemExit("build <follow-up spec> | admit <preflight> <status> | final <preflight>")
