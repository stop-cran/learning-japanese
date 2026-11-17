"""Build the evidence-bound B134 resolution and closure request after both fresh reviews.

build_b134_resolution.py FRESH_INPUT_JSON NEW_OUTPUT_DIRECTORY

FRESH_INPUT_JSON is coordinator-authored after both fresh reviews are accepted and
adjudicated. Its fields are exactly:
  reviews           closure review items (spec, preflight, final, launch, phase1,
                    extension), Claude then GPT, passed unchanged to close_b134.py;
  adjudications     {fresh run: accepted coordinator adjudication ref};
  evidence          extra archived coordinator evidence (archivePath, path, sha256);
  protectedSources  extra local-only texts (path, sha256) for the leakage scan;
  dispositions      one decision per fresh claim (run, id, status, reason,
                    evidence as archive paths);
  limits            fresh-review limitations appended to the fixed B134 limits.

The original 29 dispositions are converted from the frozen coordinator map; their
local-only captures are cited through the archived binding verification. The output
is not closure: close_b134.py dry/real remains the authoritative validator.
"""
import json
import sys
from pathlib import Path

from b132_closure_records import archive_path
from b134_review_history import MODE
from close_b134 import ORIGINAL, ORIGINAL_SHA, PROOFS, REVIEWED, ROOT, read_review
from common import WS, freeze_json, frozen, json_bytes, require, sha, write_frozen
from run_b134_closure_checks import BATCH, CANDIDATE

ORIGINAL_RUNS = ("N1-B134-CLAUDE-001", "N1-B134-GPT-001")
FIXED_EVIDENCE = {
    "verification/coordinator-original-dispositions.json": (
        "coordinator-disposition-bindings-001/coordinator-dispositions.json",
        "e317783a7c579ca13ff7d3cbe9f8a4940b6dc7cce3ae0eed791c8625dcb92b13"),
    "verification/coordinator-original-bindings.json": (
        "coordinator-disposition-bindings-001/verification.json",
        "d4eee7728c8cd3570096621ef38ffe68dd9ffda0346ddf6b068b38bc509ad9ac"),
    "verification/coordinator-source-checks.json": (
        "coordinator-source-checks-captures-001/coordinator-source-checks.json",
        "e044047ebe19a8f64865c462fc1e51187d3f77dad85344c4b20baa4b16511843"),
    "verification/coordinator-source-bindings.json": (
        "coordinator-source-checks-captures-001/verification.json",
        "0d6e2c85dcde9bbbc49c4176a649bf1bf6c359b5f2c78354752586b4c099d7fb"),
    "verification/navy-capture-index.json": (
        "reconciliation-captures-001/index.json",
        "18a06c432531ccf700d3042b75319c6e3ec4909edd51ce094477c5881a7337a0"),
}
BINDINGS = "verification/coordinator-original-bindings.json"
DRAFT = "verification/coordinator-original-dispositions.json"
KEY_ARCHIVE = {
    "claudeAdjudication": ("reviews/N1-B134-CLAUDE-001/adjudication.json",),
    "gptAdjudication": ("reviews/N1-B134-GPT-001/adjudication.json",),
    "sourceProof": ("verification/reconciliation-sources.json",),
    "gateProof": ("verification/reconciliation-gates.json",),
    "partialChecks001": ("verification/coordinator-source-bindings.json",
                         "verification/coordinator-source-checks.json"),
    "navyCaptures": ("verification/navy-capture-index.json",),
}
LOCAL_ONLY_KEYS = {"purpleNativeCapture", "threadReadback", "fiberReadback",
                   "hallReadback", "wrapReadback"}
STATUSES = ("resolved", "withdrawn", "optional")
FIXED_LIMITS = [
    "Fresh independent reviews plus coordinator reconciliation; the original reviewers did "
    "not confirm the fixes and their UNVERIFIED / NEEDS FIX verdicts remain unchanged.",
    "Kanji-only scope: the \u7d2b card keeps 56 quiz exclusions, curated distractors "
    "\u53e4/\u53f3/\u5ddd and kun reading [\u3080\u3089\u3055\u304d].",
    "The mnemonic is invented and non-etymological.",
    "Historical \u30c4\u30c4\u30e0 scope is unresolved; the latent \u7d2b/\u5305 reading "
    "collision is retained as a documented limitation.",
    "\u5b57\u901a gives 11 strokes versus 12 in KANJIDIC2/KanjiVG; the discrepancy is "
    "retained, not resolved.",
    "51 expected notes warnings and 11 pre-existing fallback cards remain.",
    "\u8308 (U+8308) is absent from all three checked font cmaps; no rendered-fallback "
    "acceptance.",
    "No Kotlin, native, device, phone or whole-set acceptance; publication remains pending "
    "until the signed closure is pushed and its CI passes.",
]


def fixed_inputs():
    """Return fixed request evidence, archive inventory and protected local texts."""
    index = json.loads(read_review(ORIGINAL / "index.json", ORIGINAL_SHA))
    inventory = dict(index["recordedFileSha256"])
    for label, (_, digest) in PROOFS.items():
        inventory["verification/" + label + ".json"] = digest
    evidence, raws = [], {}
    for name, (relative, digest) in FIXED_EVIDENCE.items():
        path = ROOT / relative
        raws[name] = read_review(path, digest)
        require(inventory.setdefault(name, digest) == digest, "Fixed evidence collides: " + name)
        evidence.append({"archivePath": name, "path": str(path), "sha256": digest})
    protected = []
    for name in (BINDINGS, "verification/coordinator-source-bindings.json"):
        for key, ref in json.loads(raws[name])["captures"].items():
            if key.endswith(("Readback", "NativeCapture")):
                protected.append({"path": ref["path"], "sha256": ref["sha256"]})
    for capture in json.loads(raws["verification/navy-capture-index.json"])["captures"]:
        protected.append({"path": capture["text"]["path"], "sha256": capture["text"]["sha256"]})
    for ref in protected:
        path = Path(ref["path"]).resolve()
        require(path.is_relative_to(WS), "Protected source escaped N1 workspace")
        frozen(path, ref["sha256"])
    return index, evidence, inventory, protected, raws


def original_dispositions(index, inventory, raws):
    draft = json.loads(raws[DRAFT])
    bindings = json.loads(raws[BINDINGS])
    require(draft["reviewedSnapshot"] == REVIEWED and draft["initialSnapshot"] == CANDIDATE
            and bindings["status"] == "PASS_BINDINGS_NOT_FINAL_CLOSURE"
            and bindings["candidate"] == REVIEWED
            and bindings["dispositions"]["sha256"] == sha(raws[DRAFT]),
            "Original disposition bindings differ")
    for key, ref in draft["evidence"].items():
        captured = bindings["captures"][key]
        require(captured["sha256"] == captured["original"]["sha256"] == ref["sha256"],
                "Bound original evidence differs: " + key)
        if key in KEY_ARCHIVE:
            require(inventory[KEY_ARCHIVE[key][0]] == ref["sha256"],
                    "Archived evidence differs from its original: " + key)
        else:
            require(key in LOCAL_ONLY_KEYS, "Unmapped original evidence: " + key)
    checks = {(row["run"], row["id"]): row["cardPredicates"] for row in bindings["checks"]}
    result = []
    for row in draft["dispositions"]:
        identity = (row["run"], row["id"])
        require(row["run"] in ORIGINAL_RUNS and checks.get(identity) == len(row["predicates"])
                and row["status"] in STATUSES and row["reason"].strip(),
                "Unchecked original disposition")
        paths = [path for key in row["evidenceKeys"] for path in KEY_ARCHIVE.get(key, (BINDINGS,))]
        paths = list(dict.fromkeys([*paths, DRAFT, BINDINGS]))
        result.append({
            "run": row["run"], "id": row["id"], "status": row["status"], "reason": row["reason"],
            "evidence": [{"path": path, "sha256": inventory[path]} for path in paths],
            "originalEvidenceKeys": row["evidenceKeys"], "cardPredicates": row["predicates"],
        })
    require(len(result) == len({(row["run"], row["id"]) for row in result}) == 29,
            "Expected 29 distinct original obligations")
    lineage = {entry["run"]: entry["adjudication"]["sha256"] for entry in index["reviewLineage"]}
    require(set(lineage) == set(ORIGINAL_RUNS), "Original lineage differs")
    return result, lineage


def build_resolution(original, original_adjudications, fresh_adjudications, fresh, inventory):
    require(len(fresh_adjudications) == 2 and not set(fresh_adjudications) & set(ORIGINAL_RUNS),
            "Two fresh adjudications are required")
    seen = {(row["run"], row["id"]) for row in original}
    dispositions = list(original)
    for row in fresh:
        require(set(row) == {"run", "id", "status", "reason", "evidence"}
                and row["run"] in fresh_adjudications and isinstance(row["id"], str)
                and row["id"].strip() and (row["run"], row["id"]) not in seen
                and row["status"] in STATUSES
                and isinstance(row["reason"], str) and row["reason"].strip()
                and isinstance(row["evidence"], list) and row["evidence"],
                "Invalid, duplicate or unresolved fresh disposition")
        refs = []
        for path in dict.fromkeys(row["evidence"]):
            archive_path(path)
            require(path in inventory, "Fresh disposition cites unarchived evidence: " + path)
            refs.append({"path": path, "sha256": inventory[path]})
        seen.add((row["run"], row["id"]))
        dispositions.append({**row, "evidence": refs})
    return {
        "batch": BATCH, "initialSnapshot": CANDIDATE, "reviewedSnapshot": REVIEWED, "mode": MODE,
        "originalReviewerConfirmation": False,
        "adjudicationSha256": {**original_adjudications,
                               **{run: ref["sha256"] for run, ref in fresh_adjudications.items()}},
        "remainingActionableFindings": [], "remainingConsequentialClaims": [],
        "dispositions": dispositions,
    }


def main(input_path, output):
    require(output.parent == ROOT and not output.exists(), "Use a new direct review output directory")
    fresh = json.loads(read_review(input_path))
    require(set(fresh) == {"reviews", "adjudications", "evidence", "protectedSources",
                           "dispositions", "limits"}, "Unexpected fresh input fields")
    reviews = fresh["reviews"]
    require(isinstance(reviews, list) and [item["spec"]["family"] for item in reviews]
            == ["claude", "gpt"], "Both serial fresh reviews are required")
    runs = [item["spec"]["run"] for item in reviews]
    require(set(fresh["adjudications"]) == set(runs), "Fresh adjudications differ from the reviews")
    index, evidence, inventory, protected, raws = fixed_inputs()
    for run, ref in fresh["adjudications"].items():
        read_review(ref["path"], ref["sha256"])
        inventory["reviews/" + run + "/adjudication.json"] = ref["sha256"]
    for ref in fresh["evidence"]:
        name = archive_path(ref["archivePath"])
        require(not name.startswith("reviews/") and name not in inventory,
                "Fresh evidence collides with archived history: " + name)
        read_review(ref["path"], ref["sha256"])
        inventory[name] = ref["sha256"]
        evidence.append({key: ref[key] for key in ("archivePath", "path", "sha256")})
    for ref in fresh["protectedSources"]:
        path = Path(ref["path"]).resolve()
        require(path.is_relative_to(WS), "Protected source escaped N1 workspace")
        frozen(path, ref["sha256"])
        protected.append({"path": ref["path"], "sha256": ref["sha256"]})
    require(isinstance(fresh["limits"], list) and fresh["limits"]
            and all(isinstance(value, str) and value.strip() for value in fresh["limits"]),
            "Fresh-review limitations are required")
    original, lineage = original_dispositions(index, inventory, raws)
    resolution = build_resolution(original, lineage, fresh["adjudications"],
                                  fresh["dispositions"], inventory)
    resolution_ref = write_frozen(output / "resolution.json", json_bytes(resolution))
    request = {
        "reviews": reviews,
        "resolution": {"path": resolution_ref["path"], "sha256": resolution_ref["sha256"]},
        "evidence": evidence, "protectedSources": protected,
        "limits": [*FIXED_LIMITS, *fresh["limits"]],
    }
    print(json.dumps({"resolution": resolution_ref,
                      "request": freeze_json(output / "closure-request.json", request),
                      "dispositions": len(resolution["dispositions"])}))


if __name__ == "__main__":
    require(len(sys.argv) == 3, __doc__)
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
