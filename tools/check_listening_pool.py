"""Read-only N5/N4 pool feasibility; candidate mode never establishes runtime readiness."""
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
PROFILES = {
    BLUEPRINT: (GROUPS, MIN_MS, MAX_MS, 5),
    "n4-section-v1": ((("task-based", 8, 16), ("key-point", 7, 14),
                       ("verbal-expression", 5, 10), ("quick-response", 8, 16)), 31 * 60_000, 39 * 60_000, 4),
}


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


def analyze(documents: list[dict], legacy_exposures: set[str] | None = None,
            *, profile: str = BLUEPRINT, unpublished_candidate: bool = False) -> dict:
    """Check declared package metadata; check_root additionally verifies actual files."""
    if profile not in PROFILES:
        raise ValueError(f"Unsupported diagnostic profile: {profile}")
    profile_groups, minimum_ms, maximum_ms, level = PROFILES[profile]
    legacy_exposures = legacy_exposures or set()
    included, excluded, errors = [], [], []
    identities, exposures = set(), {}
    for document in documents:
        identifier = document.get("id") if isinstance(document, dict) else None
        ready = tasks.validate_document(document, f"listening-tasks/{identifier}.json")
        if identifier in identities:
            raise ValueError(f"Duplicate task ID: {identifier}")
        identities.add(identifier)
        if document.get("blueprint") != profile:
            excluded.append({"id": identifier, "reason": "not assigned to this blueprint"})
        elif not ready and not (unpublished_candidate and document.get("media") is not None):
            excluded.append({"id": identifier, "reason": "missing complete media" if unpublished_candidate else
                             "missing complete media or exact-output approval"})
        else:
            included.append(document)
            exposure = document["exposureId"]
            if exposure in exposures:
                errors.append(f"Shared pool exposure identity: {exposures[exposure]} and {identifier} ({exposure})")
            if exposure in legacy_exposures:
                errors.append(f"Pool task {identifier} reuses legacy story identity {exposure}")
            exposures[exposure] = identifier
    if level == 4:
        other_stories = {document["exposureId"] for document in documents if document["jlpt"] != level}
        for document in included:
            if document["exposureId"] in other_stories:
                errors.append(f"N4 pool task {document['id']} reuses another level's story identity")
    groups = []
    status = "candidate" if unpublished_candidate else "approved"
    for kind, selected, minimum in profile_groups:
        members = sorted((document for document in included if document["taskType"] == kind), key=lambda d: d["id"])
        scored = [document for document in members if document["usage"] == "scored"]
        examples = [document for document in members if document["usage"] == "example"]
        if len(scored) < minimum:
            errors.append(f"{kind}: {len(scored)} {status} scored tasks; at least {minimum} required")
        if not examples:
            errors.append(f"{kind}: no independent {status} worked example")
        duration = None
        if len(scored) >= selected and examples:
            scored_ms = sorted(item_duration_ms(document) for document in scored)
            example_ms = [item_duration_ms(document) for document in examples]
            duration = {"shortest": sum(scored_ms[:selected]) + min(example_ms),
                        "longest": sum(scored_ms[-selected:]) + max(example_ms)}
        groups.append({
            "taskType": kind, "selectedScoredCount": selected, f"minimum{status.title()}ScoredCount": minimum,
            f"{status}ScoredIds": [document["id"] for document in scored],
            f"{status}ExampleIds": [document["id"] for document in examples],
            "durationMs": duration, "instructionVariants": instruction_variants(members),
        })
    duration = None
    if all(group["durationMs"] is not None for group in groups):
        duration = {bound: sum(group["durationMs"][bound] for group in groups) for bound in ("shortest", "longest")}
        if duration["shortest"] < minimum_ms:
            errors.append(f"Shortest permitted form is {duration['shortest']} ms; minimum is {minimum_ms} ms")
        if duration["longest"] > maximum_ms:
            errors.append(f"Longest permitted form is {duration['longest']} ms; maximum is {maximum_ms} ms")
    report = {
        "blueprint": profile, "jlpt": level, "checksPassed": not errors, "groups": groups, "excluded": excluded,
        "mode": "unpublished-candidate" if unpublished_candidate else "approved-runtime",
        "durationMs": duration, "requiredDurationMs": {"minimum": minimum_ms, "maximum": maximum_ms}, "errors": errors,
        "notCovered": [
            "Semantic story independence and equivalent generic instructions require editorial review.",
            "Actual listening, native/physical-phone acceptance and spending authorization are separate gates.",
            "Run check_content_budget.py for complete-archive headroom.",
            "Runtime preflight must check the learner's exposure, cooldown, accessibility and permitted form timing.",
        ],
    }
    if unpublished_candidate:
        report.update(publicationReady=False, scoringReady=False,
                      readiness="NOT ESTABLISHED: candidate feasibility does not grant approval or publication/scoring readiness.")
    return report


def check_root(root: Path, *, profile: str = BLUEPRINT, unpublished_candidate: bool = False) -> dict:
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
    report = analyze(documents, {path.stem for path in (root / "listening").glob("*.json")},
                     profile=profile, unpublished_candidate=unpublished_candidate)
    report["contentVersion"] = manifest["contentVersion"]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--profile", choices=PROFILES, default=BLUEPRINT)
    parser.add_argument("--unpublished-candidate", action="store_true",
                        help="Check complete private media without requiring/granting runtime approval; never scoring/publication readiness")
    args = parser.parse_args(argv)
    try:
        report = check_root(args.root, profile=args.profile, unpublished_candidate=args.unpublished_candidate)
    except (ValueError, OSError) as exc:
        report = {"blueprint": args.profile, "checksPassed": False, "errors": [str(exc)]}
        if args.unpublished_candidate:
            report.update(mode="unpublished-candidate", publicationReady=False, scoringReady=False,
                          readiness="NOT ESTABLISHED: invalid unpublished candidate.")
    print(json.dumps(report, indent=2))
    return 0 if report["checksPassed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
