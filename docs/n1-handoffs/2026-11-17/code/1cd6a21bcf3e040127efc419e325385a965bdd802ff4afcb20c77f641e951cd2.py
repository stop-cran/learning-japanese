"""Disclose a fresh-context B133 confirmation instead of overfilling the original Claude reviewer.

observe   measures the actual original-session telemetry and freezes the lower-bound capacity refusal.
derive    writes confirm_b133_fresh.py from the frozen confirm_b133_v2.py; only spec validation, build,
          render and final change, every other engine function stays AST-identical.
"""
import ast
import json
import sys
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen

ENGINE = TOOLS / "confirm_b133_v2.py"
FAMILY = "claude"
PLANNED_RUN = "N1-B133-CLAUDE-CONFIRM-002"
CANDIDATE_002 = "d7d6cff92afe8220c16a5daa76f1c3f00a2bef30"
REASON = "pre-admission-context-capacity"


def root():
    from confirm_b133_v2 import ROOT
    return ROOT


def observation_path():
    return root() / "confirmation-capacity-observation-002.json"


def binding(path, digest=None):
    return {"path": str(path), "sha256": sha(frozen(path, digest))}


def observe():
    from confirm_b133_v2 import DRIFT_ALLOWANCE, OUT, REPORT_ALLOWANCE, STARTUP_GATE, context, initial
    from admit_b133_source_reconciliation import INITIALS
    from b133_capacity import PROFILES
    out = observation_path()
    require(not out.exists(), "Preserve the existing observation")
    original = INITIALS[FAMILY]["session"]
    raw = (Path.home() / ".copilot" / "session-state" / original / "events.jsonl").read_bytes()
    observed = context(raw, FAMILY)
    require(observed["compactions"] == [] and observed["lastInputTokens"], "Unusable original telemetry")
    refs, report, _ = initial(FAMILY, original)
    gate = min(STARTUP_GATE, PROFILES[FAMILY]["maxPromptTokens"])
    lower = observed["lastInputTokens"] + len(report) + DRIFT_ALLOWANCE + REPORT_ALLOWANCE
    require(lower >= gate, "Original reviewer may still fit; do not replace it")
    previous = OUT / "N1-B133-CLAUDE-CONFIRM-001-preflight.json"
    previous_record = json.loads(frozen(previous))
    prefix = write_frozen(root() / "confirmation-capacity-observation-002" / "original-events.jsonl", raw)
    print(json.dumps(freeze_json(out, {
        "batch": 133, "family": FAMILY, "originalSession": original, "plannedRun": PLANNED_RUN,
        "candidate": CANDIDATE_002, "status": "NOT_ADMITTED_CONTEXT_RISK", "events": prefix,
        "telemetry": observed,
        "lowerBound": {
            "lastInputTokens": observed["lastInputTokens"], "initialReport": refs["report"],
            "initialReportTokens": len(report), "driftAllowance": DRIFT_ALLOWANCE,
            "reportAllowance": REPORT_ALLOWANCE, "peakLowerBound": lower, "gate": gate,
            "method": "The controller always adds the original initial report to the chain and counts it at "
                      "one token per byte. That source plus the unchanged reserves already reaches the gate, "
                      "before the prompt, cumulative fix.patch, snapshot cards and every additional source.",
        },
        "reference": {"confirm001Preflight": binding(previous),
                      "confirm001ChainTokens": previous_record["capacity"]["estimatedChainTokens"],
                      "confirm001PromptBytes": previous_record["capacity"]["promptBytes"]},
        "decision": "Do not admit CONFIRM-002 into the original Claude session. Use one new same-family "
                    "session created by the original reviewer without model or context overrides, with "
                    "fully disclosed historical attribution and an informed complete chain.",
        "producer": binding(Path(__file__)),
    })))


def fresh_origin(spec):
    from admit_b133_source_reconciliation import INITIALS
    family = spec["family"]
    observation = json.loads(frozen(observation_path(), spec["contextObservation"]["sha256"]))
    require(spec["contextObservation"] == binding(observation_path())
            and observation["status"] == "NOT_ADMITTED_CONTEXT_RISK" and observation["family"] == family
            and observation["originalSession"] == spec["originalSession"] == INITIALS[family]["session"]
            and observation["plannedRun"] == spec["run"] and observation["candidate"] == spec["candidate"]
            and isinstance(spec["session"], str) and spec["session"] != spec["originalSession"]
            and observation["lowerBound"]["peakLowerBound"] >= observation["lowerBound"]["gate"],
            "Fresh-context origin is not the observed capacity replacement")
    return True


def fresh_bindings(spec):
    return [spec["contextObservation"], binding(Path(__file__))]


def replacement_prompt(text):
    substitutions = (
        ("confirmation of your own adjudicated B133 initial report with open claims",
         "same-family fresh-context confirmation of the original reviewer's adjudicated B133 initial report "
         "with open claims"),
        ("Your own initial report:", "Original reviewer's initial report:"),
        ("The chain contains your own unchanged initial report",
         "The chain contains the original reviewer's unchanged initial report"),
        ("Read your own full report", "Read the original reviewer's full report"),
        ("including changes not requested by you", "including changes not requested in the original report"),
    )
    for before, after in substitutions:
        require(text.count(before) == 1, "Unexpected attribution wording: " + before)
        text = text.replace(before, after)
    require("your own" not in text.lower(), "Historical authorship remains misattributed")
    return text + (
        "\nFRESH CONTEXT AND HISTORICAL ATTRIBUTION\n"
        "You are a new same-family reviewer, not the author of the initial report or of the earlier "
        "same-family confirmation. Both remain accepted historical evidence with their own limits. The "
        "original session's retained context is too large to receive this complete chain within the "
        "unchanged capacity gate, so this confirmation was never admitted there; that is not a failed or "
        "withheld review. This is informed bounded confirmation, not a new blind initial review or a claim "
        "that you retain the original reviewer's firsthand context. Read the entire chain and independently "
        "assess the actual cumulative changes and every supplied disposition within the stated scope, "
        "including each qualified precaution and its Note. Earlier confirmations are evidence to check, not "
        "conclusions to inherit. No missing or consequential uncertain claim can support CONFIRMED. All "
        "source, access, context, reporting, isolation and final-audit requirements remain unchanged. No "
        "publication or delivery credit is authorized.\n"
    )


ANCHORS = (
    ("from b133_confirmation_records import disposition_ids\n",
     "from b133_confirmation_records import disposition_ids\n"
     "from b133_fresh_confirmation import REASON, fresh_bindings, fresh_origin, replacement_prompt\n"),
    ('"additionalSources", "basis", "priorVerdict", "basisText"}',
     '"additionalSources", "basis", "priorVerdict", "basisText", "originalSession",\n'
     '               "contextObservation"}'),
    ('    require(family in INITIALS and INITIALS[family]["session"] == spec["session"],\n'
     '            "Confirmation must use its original reviewer")\n',
     '    require(family in INITIALS and fresh_origin(spec),\n'
     '            "Fresh confirmation must disclose its original reviewer")\n'),
    ('    refs, original, ids = initial(family, spec["session"])\n',
     '    refs, original, ids = initial(family, spec["originalSession"])\n'),
    ('    for ref in ({"path": str(spec_path), "sha256": sha(spec_raw)}, *refs.values()):\n',
     '    for ref in ({"path": str(spec_path), "sha256": sha(spec_raw)}, *refs.values(), *fresh_bindings(spec)):\n'),
    ('            "batch": 133, "run": run, "session": spec["session"], "candidate": candidate,\n',
     '            "originalSession": spec["originalSession"], "replacementReason": REASON,\n'
     '            "contextObservation": spec["contextObservation"],\n'
     '            "batch": 133, "run": run, "session": spec["session"], "candidate": candidate,\n'),
    ('    text = renderer.render_prompt({**spec, "dispositionIds": ids}, packet, chain, prompt_path)\n',
     '    text = replacement_prompt(renderer.render_prompt({**spec, "dispositionIds": ids}, packet, chain,\n'
     '                                                     prompt_path))\n'),
    ('            "run": run, "batch": 133, "candidate": record["candidate"], "session": record["session"],\n',
     '            "run": run, "batch": 133, "candidate": record["candidate"], "session": record["session"],\n'
     '            "originalSession": record["originalSession"], "replacementReason": record["replacementReason"],\n'),
)
CHANGED = {"validate_spec", "build", "render", "final"}


def functions(text):
    return {node.name: ast.dump(node) for node in ast.parse(text).body
            if isinstance(node, ast.FunctionDef) and node.name not in CHANGED}


def derive_text(text):
    original = text.replace("\r\n", "\n")
    result = original
    for before, after in ANCHORS:
        require(result.count(before) == 1, "Unexpected confirmation engine anchor: " + before[:60])
        result = result.replace(before, after)
    require(functions(original) == functions(result), "Access/admission/final-audit mechanics changed")
    return result


def derive():
    out = TOOLS / "confirm_b133_fresh.py"
    require(not out.exists(), "Preserve the derived controller")
    derived = derive_text(frozen(ENGINE).decode("utf-8"))
    compile(derived, out.name, "exec")
    output = write_frozen(out, derived.encode("utf-8"))
    print(json.dumps(freeze_json(root() / "fresh-confirmation-tooling-002.json", {
        "source": binding(ENGINE), "output": output, "producer": binding(Path(__file__)),
        "capacityObservation": binding(observation_path()), "reviewerLaunched": False,
        "scope": "Only spec origin validation, initial-report lineage, fresh bindings, preflight/final "
                 "origin fields and historical attribution differ; all other engine functions are AST-identical.",
    })))


if __name__ == "__main__":
    action = sys.argv[1:]
    if action == ["observe"]:
        sys.path.insert(0, str(Path(__file__).parent))
        observe()
    elif action == ["derive"]:
        derive()
    else:
        raise SystemExit("observe | derive")
