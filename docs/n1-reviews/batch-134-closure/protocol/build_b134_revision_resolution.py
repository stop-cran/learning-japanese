"""Build a descendant closure request without changing the original355 builder."""
import copy
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, load_module, require, sha, start_guard, write_frozen

SOURCE = Path(__file__).with_name("build_b134_resolution.py")
SOURCE_SHA = "4996208cd0084fa20fe08da332cc39567ffc0a14a6af5f89dac96674b027cd45"
HISTORY = Path(__file__).with_name("b134_revision_history.py")
HISTORY_SHA = "3fb4c7f222d055794303223a0abb1d43afea6af84ab5b6d95bb836aa7e728eac"
INPUT_SHA = "b0a0a521ee1a9260143838d0bda56e33125a6eef2c5c4b60b787eb76aab00c09"
frozen(SOURCE, SOURCE_SHA)
frozen(HISTORY, HISTORY_SHA)
base = load_module("b134_revision_resolution_pinned_base", SOURCE)
history = load_module("b134_revision_resolution_pinned_history", HISTORY)
ROOT = base.ROOT


def build_resolution(original, original_adjudications, fresh_adjudications, fresh,
                     inventory, confirmation_adjudications):
    require(len(original) == 29 and len(fresh) == 12
            and set(fresh_adjudications) == {
                "N1-B134-CLAUDE-FRESH-003", "N1-B134-GPT-FRESH-003"},
            "Retain exactly the original29 and FRESH003 twelve obligations")
    require(set(confirmation_adjudications) == {"claude", "gpt"},
            "Both actual authorized confirmation adjudications are required")
    added = {}
    for family, item in confirmation_adjudications.items():
        run = item["run"]
        require(re.fullmatch("N1-B134-" + family.upper() + r"-REVISION-\d{3}", run)
                and run not in added and run not in fresh_adjudications
                and item["ref"]["sha256"] ==
                inventory.get("confirmations/" + run + "/adjudication.json"),
                "Confirmation adjudication is misattributed or unarchived")
        added[run] = item["ref"]["sha256"]
    result = base.build_resolution(original, original_adjudications, fresh_adjudications, fresh, inventory)
    require(len(result["dispositions"]) == 41, "A claim was lost during resolution assembly")
    result.update(mode=history.MODE, reviewedSnapshot=history.REVISED, priorReviewedSnapshot=history.PRIOR)
    result["adjudicationSha256"].update(added)
    require(len(result["adjudicationSha256"]) == 6, "Expected six separately bound review roles")
    return result


def main(input_path, output):
    require(output.parent == ROOT and not output.exists(), "Use a new direct review output directory")
    fresh = json.loads(base.read_review(input_path))
    require(set(fresh) == {"reviews", "adjudications", "evidence", "protectedSources",
                           "dispositions", "revision", "limits", "assemblyMemory"}
            and fresh["assemblyMemory"]["breach"] is None,
            "Expected the complete verified descendant input schema")
    reviews, revision = fresh["reviews"], fresh["revision"]
    require([item["spec"]["family"] for item in reviews] == ["claude", "gpt"]
            and revision["candidate"] == history.REVISED and revision["priorSnapshot"] == history.PRIOR
            and set(revision["confirmations"]) == {"claude", "gpt"}
            and revision["confirmations"]["claude"]["sha256"] != history.HELD_CLAUDE_SHA,
            "Wrong descendant input or held pre-authorization acceptance")
    validator_refs = [item for item in fresh["evidence"]
                      if item["archivePath"] == "protocol/assemble-b134-revision-input-v2.py"]
    require(len(validator_refs) == 1 and validator_refs[0]["sha256"] == INPUT_SHA,
            "Expected the exact tested descendant input validator")
    base.read_review(validator_refs[0]["path"], INPUT_SHA)
    validator = load_module("b134_actual_revision_input_validator", validator_refs[0]["path"])
    guard, _ = start_guard("B134 descendant resolution assembly")
    try:
        index, evidence, inventory, protected, raws = base.fixed_inputs()
        validated, confirmations, tokens = [], {}, {}
        for family, review in zip(("claude", "gpt"), reviews, strict=True):
            collection = json.loads(base.read_review(
                ROOT / (family + "-fresh003-collector-001") / "review-input.json",
                validator.COLLECTIONS[family]))
            run = review["spec"]["run"]
            require(review == collection["review"]
                    and fresh["adjudications"][run] == collection["adjudication"],
                    "The complete original FRESH003 review bindings changed")
            original = json.loads(validator.read_ref(collection["adjudication"]))
            accepted = json.loads(validator.read_ref(revision["confirmations"][family]))
            final = json.loads(validator.read_ref(accepted["final"]))
            decision = json.loads(validator.read_ref(accepted["adjudication"]))
            validator.read_ref(accepted["report"])
            frozen(accepted["producer"]["path"], accepted["producer"]["sha256"])
            validated.extend(validator.confirmation_dispositions(
                family, collection, original, accepted, final, decision))
            confirmations[family] = {"run": accepted["run"], "ref": accepted["adjudication"]}
            tokens[accepted["run"]] = decision["dispositions"]
            inventory["reviews/" + run + "/adjudication.json"] = collection["adjudication"]["sha256"]
            guard.check()
        require(validated == fresh["dispositions"] and tokens == revision["literalDispositionTokens"],
                "Claim statuses, reasons or literal confirmation tokens changed after assembly")
        require(set(fresh["adjudications"]) == {item["spec"]["run"] for item in reviews},
                "Extra original adjudications")
        for item in fresh["evidence"]:
            name = base.archive_path(item["archivePath"])
            require(not name.startswith("reviews/") and name not in inventory,
                    "Descendant evidence collides with unchanged history")
            base.read_review(item["path"], item["sha256"])
            inventory[name] = item["sha256"]
            evidence.append({key: item[key] for key in ("archivePath", "path", "sha256")})
        for key, digest in history.PROOFS.items():
            source_ref = revision["scopeProof" if key == "scope" else "gateProof"]
            require(source_ref["sha256"] == digest, "Wrong signed revision proof")
            validator.read_ref(source_ref)
            name = "verification/revision-" + key + ".json"
            require(name not in inventory, "Duplicate revision proof")
            inventory[name] = digest
            evidence.append({"archivePath": name, **source_ref})
        hold_path = ROOT / "revision-confirmation-scope-hold-001" / "hold.json"
        base.read_review(hold_path, history.HOLD_SHA)
        hold_ref = {"path": str(hold_path), "sha256": history.HOLD_SHA}
        evidence.append({"archivePath": "history/revision-scope-hold.json", **hold_ref})
        inventory["history/revision-scope-hold.json"] = history.HOLD_SHA
        for item in fresh["protectedSources"]:
            path = Path(item["path"]).resolve()
            require(path.is_relative_to(base.WS), "Protected source escaped N1 workspace")
            frozen(path, item["sha256"])
            protected.append({"path": str(path), "sha256": item["sha256"]})
        require(isinstance(fresh["limits"], list) and fresh["limits"]
                and all(isinstance(text, str) and text.strip() for text in fresh["limits"]),
                "Explicit descendant limits are required")
        original, lineage = base.original_dispositions(index, inventory, raws)
        resolution = build_resolution(original, lineage, fresh["adjudications"],
                                      fresh["dispositions"], inventory, confirmations)
        for path, digest in ((SOURCE, SOURCE_SHA), (HISTORY, HISTORY_SHA), (Path(__file__), None)):
            raw = frozen(path, digest)
            name = "protocol/" + path.name
            if name in inventory:
                require(inventory[name] == sha(raw), "A retained producer has different bytes")
                continue
            saved = write_frozen(output / path.name, raw)
            inventory[name] = saved["sha256"]
            evidence.append({"archivePath": name,
                             **{key: saved[key] for key in ("path", "sha256")}})
        require(len(evidence) == len({item["archivePath"] for item in evidence}),
                "Duplicate descendant archive evidence")
        resolution_ref = freeze_json(output / "resolution.json", resolution)
        request = {
            "reviews": reviews,
            "revision": {**copy.deepcopy(revision), "scopeHold": hold_ref},
            "resolution": {key: resolution_ref[key] for key in ("path", "sha256")},
            "evidence": evidence, "protectedSources": protected,
            "limits": [
                "Both original and FRESH003 raw verdicts remain unchanged; authorized same-FRESH003 "
                "descendant confirmations are separate roles, not original001 reviewer confirmations.",
                "Current correction cc374 retains58 exclusions; the prior355 snapshot had56. "
                "Readings, curated distractors and support article remain unchanged.",
                *base.FIXED_LIMITS[2:], *fresh["limits"],
            ],
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Descendant resolution assembly RAM breach")
    print(json.dumps({"resolution": resolution_ref,
                      "request": freeze_json(output / "closure-request.json", request),
                      "memory": freeze_json(output / "assembly-memory.json", memory),
                      "dispositions": 41, "limits": "Resolution only; actual execution collection and closure remain required."}))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "build_b134_revision_resolution.py FRESH_INPUT NEW_REVIEW_OUTPUT")
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
