"""Read-only static feasibility gate for n5-section-v1, not listening approval."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_manifest import build_manifest
import validate_listening_tasks as tasks

BLUEPRINT = "n5-section-v1"
# Order, selected scored count, minimum approved scored pool.
GROUPS = (("task-based", 7, 8), ("key-point", 6, 7), ("verbal-expression", 5, 6), ("quick-response", 6, 7))
MIN_MS, MAX_MS = 26 * 60_000, 34 * 60_000


def item_duration_ms(document: dict) -> int:
    example = document["usage"] == "example"
    stages = document["stages"] if example else document["stages"][1:]
    audio = sum(document["media"]["audio"][stage["id"]]["durationMs"] for stage in stages)
    preview = 0 if document["taskType"] == "quick-response" else 5_000
    answer = 10_000 if example or document["taskType"] in ("verbal-expression", "quick-response") else 15_000
    return audio + preview + answer + (10_000 if example else 0)


def instruction_variants(documents: list[dict]) -> list[dict]:
    variants = {}
    for document in documents:
        turns = {turn["id"]: turn for turn in document["turns"]}
        selected = [turns[identifier] for identifier in document["stages"][0]["turns"]]
        wording = {
            "text": [turn["text"] for turn in selected],
            "spokenText": [turn.get("spokenText", turn["text"]) for turn in selected],
            "translation": [turn["translation"] for turn in selected],
        }
        key = tasks.canonical_hash(wording)
        variants.setdefault(key, {**wording, "taskIds": []})["taskIds"].append(document["id"])
    return list(variants.values())


def analyze(documents: list[dict], legacy_exposures: set[str] | None = None) -> dict:
    """Check declared package metadata; check_root additionally verifies actual files."""
    legacy_exposures = legacy_exposures or set()
    approved, excluded, errors = [], [], []
    identities, exposures = set(), {}
    for document in documents:
        identifier = document.get("id") if isinstance(document, dict) else None
        ready = tasks.validate_document(document, f"listening-tasks/{identifier}.json")
        if identifier in identities:
            raise ValueError(f"Duplicate task ID: {identifier}")
        identities.add(identifier)
        if document.get("blueprint") != BLUEPRINT:
            excluded.append({"id": identifier, "reason": "not assigned to this blueprint"})
        elif not ready:
            excluded.append({"id": identifier, "reason": "missing complete media or exact-output approval"})
        else:
            approved.append(document)
            exposure = document["exposureId"]
            if exposure in exposures:
                errors.append(f"Shared pool exposure identity: {exposures[exposure]} and {identifier} ({exposure})")
            if exposure in legacy_exposures:
                errors.append(f"Pool task {identifier} reuses legacy story identity {exposure}")
            exposures[exposure] = identifier
    groups = []
    for kind, selected, minimum in GROUPS:
        members = sorted((document for document in approved if document["taskType"] == kind), key=lambda d: d["id"])
        scored = [document for document in members if document["usage"] == "scored"]
        examples = [document for document in members if document["usage"] == "example"]
        if len(scored) < minimum:
            errors.append(f"{kind}: {len(scored)} approved scored tasks; at least {minimum} required")
        if not examples:
            errors.append(f"{kind}: no independent approved worked example")
        duration = None
        if len(scored) >= selected and examples:
            scored_ms = sorted(item_duration_ms(document) for document in scored)
            example_ms = [item_duration_ms(document) for document in examples]
            duration = {"shortest": sum(scored_ms[:selected]) + min(example_ms),
                        "longest": sum(scored_ms[-selected:]) + max(example_ms)}
        groups.append({
            "taskType": kind, "selectedScoredCount": selected, "minimumApprovedScoredCount": minimum,
            "approvedScoredIds": [document["id"] for document in scored],
            "approvedExampleIds": [document["id"] for document in examples],
            "durationMs": duration, "instructionVariants": instruction_variants(members),
        })
    duration = None
    if all(group["durationMs"] is not None for group in groups):
        duration = {bound: sum(group["durationMs"][bound] for group in groups) for bound in ("shortest", "longest")}
        if duration["shortest"] < MIN_MS:
            errors.append(f"Shortest permitted form is {duration['shortest']} ms; minimum is {MIN_MS} ms")
        if duration["longest"] > MAX_MS:
            errors.append(f"Longest permitted form is {duration['longest']} ms; maximum is {MAX_MS} ms")
    return {
        "blueprint": BLUEPRINT, "checksPassed": not errors, "groups": groups, "excluded": excluded,
        "durationMs": duration, "requiredDurationMs": {"minimum": MIN_MS, "maximum": MAX_MS}, "errors": errors,
        "notCovered": [
            "Semantic story independence and equivalent generic instructions require editorial review.",
            "Actual listening, native/physical-phone acceptance and spending authorization are separate gates.",
            "Run check_content_budget.py for complete-archive headroom.",
            "F must check the learner's exposure, cooldown, accessibility and exact selected form.",
        ],
    }


def check_root(root: Path) -> dict:
    names = {path.name for path in root.iterdir()}
    for folder in ("listening-tasks", "task-audio", "task-images"):
        if (root / folder).exists() and folder not in names:
            raise ValueError(f"Incorrect folder casing: {folder}")
    errors = []
    tasks.check_listening_tasks(lambda path, message: errors.append(f"{path.name}: {message}"), root)
    if errors:
        raise ValueError("\n".join(errors))
    manifest_path = root / "manifest.json"
    if manifest_path.is_symlink():
        raise ValueError("Manifest must not be a symlink")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest != build_manifest(root):
        raise ValueError("Manifest is stale or malformed; run tools/build_manifest.py before checking the pool")
    documents = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((root / "listening-tasks").glob("*.json"))]
    report = analyze(documents, {path.stem for path in (root / "listening").glob("*.json")})
    report["contentVersion"] = manifest["contentVersion"]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args(argv)
    try:
        report = check_root(args.root)
    except (ValueError, OSError) as exc:
        report = {"blueprint": BLUEPRINT, "checksPassed": False, "errors": [str(exc)]}
    print(json.dumps(report, indent=2))
    return 0 if report["checksPassed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
