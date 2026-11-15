"""Prepare isolated original-family confirmations of the verified B124 correction."""
import copy
import json
import re
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, write_frozen
from confirm_v2 import build, clean
from verify_b124_reconciliation import CANDIDATE, COMPARISONS, PREFIX

REVIEW = WS / "scratch-124" / "review"
VERIFICATION_SHA = "4a2622178667f86cb0c6a80b4e1e2cedde2846d2d34511b84c828f09c24edcc0"
REVIEWERS = {
    "claude": ("a917da6c-69eb-4637-b35c-fd163682be12",
               "213a41ce1c0e6eec0b4a8e13c484cc25dac8bee300dbe690b7e9ced5835974f1"),
    "gpt": ("9b629a17-7dc2-4a85-a8d4-fc0cc70c507d",
            "05e4a48d8b9abb12c06a0aca46778a0adfe56da41a67231dd6b304d6ea2d0f5c"),
}


def neutralize(name, original):
    value = copy.deepcopy(original)
    if name == "source-receipt.json":
        del value["immutableInputs"]
        del value["reviewReportBindings"]
        removed = ["/immutableInputs", "/reviewReportBindings"]
    elif name == "selection.json":
        for row in value["claimInventory"]:
            del row["reviewRows"]
        removed = ["/claimInventory/*/reviewRows"]
    elif name == "dispositions.json":
        del value["sourceBindings"]["reviewReports"]
        removed = ["/sourceBindings/reviewReports"]
    else:
        raise ValueError("Unknown neutral source")
    return value, removed


def additional(path, source):
    return {"path": str(path), "source": source, "sha256": sha(frozen(path))}


def main():
    config = load_batch(124)
    clean(config, CANDIDATE)
    proof_path = REVIEW / "coordinator-reconciliation-verification-001.json"
    proof = json.loads(frozen(proof_path, VERIFICATION_SHA))
    require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE
            and not proof["memory"]["breach"], "Signed correction verification held")
    recovery_path = REVIEW / "confirm" / "tooling-preflight-recovery-001.json"
    recovery = json.loads(frozen(recovery_path,
                                "c21693f20db0cbeefc2ac01a924a98fc1fdb29863f8a353605ab7ebd4eb742e2"))
    require(recovery["status"] == "PASS_PREPARATION_ONLY" and recovery["testCount"] == 21,
            "Confirmation tooling recovery missing")
    for item in recovery["productionOutputs"]:
        frozen(item["path"], item["sha256"])
    blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
    neutral_dir = REVIEW / "reconciliation-001-neutral"
    require(not neutral_dir.exists(), "Preserve existing neutral sources")
    shared, derivatives = [], []
    for name in ("source-receipt.json", "selection.json", "dispositions.json"):
        original_raw = blob(PREFIX + name)
        require(sha(original_raw) == proof["signedArtifacts"][PREFIX + name], "Verified source changed")
        value, removed = neutralize(name, json.loads(original_raw))
        value["_reviewIsolation"] = {
            "originalSignedPath": PREFIX + name, "originalSha256": sha(original_raw),
            "removedJsonPointers": removed,
            "scope": "Only cross-report provenance removed; substantive statements and source selectors unchanged.",
        }
        path = neutral_dir / name
        derivative = write_frozen(path, json_bytes(value))
        derivatives.append({"inputSha256": sha(original_raw), "output": derivative, "removed": removed})
        shared.append(additional(path, f"neutral-author-evidence/{name}"))
    summary = {key: proof[key] for key in (
        "batch", "candidate", "initial", "base", "manifestSha256", "contentVersion", "runtimeEntries",
        "sourceReceiptSha256", "sourceRecords", "runner", "gateSets",
        "metadataStrokesSupportAndHistoricalEvidencePreserved",
        "sourceMembersPublishedBeforeBatch", "sourceMembersInCandidate",
    )}
    summary.update(status="PASS_MECHANICAL_ONLY", semanticAcceptance=False,
                   sourceProofSha256=VERIFICATION_SHA,
                   limits="Verified signed bytes, complete source selections and host gates only; "
                          "the author dispositions remain proposals for independent evaluation.")
    summary_path = neutral_dir / "verification-summary.json"
    freeze_json(summary_path, summary)
    shared.append(additional(summary_path, "verification/signed-correction-summary.json"))
    gate_dir = Path(proof["gateSets"]["committed"]["directory"])
    for name in ("summary.json", *(f"{gate}.log" for gate in CHECKS)):
        shared.append(additional(gate_dir / name, f"committed-checks/{name}"))
    revised = ["kanji/裕.md", "words/余裕.md", PREFIX + "jmdict-records.xml",
               PREFIX + "kanjidic2-records.xml",
               "docs/n1-sources/batch-124/jmdict-selected-records.xml"]
    revised += [PREFIX + f"comparison-cards/{char}.md" for char in sorted(COMPARISONS)]
    originals = [f"repo/kanji/{char}.md" for char in sorted(set("厚富豊財容補複"))]
    originals += ["evidence/external-snapshots/01-extract.txt",
                  "evidence/external-snapshots/manifest.json", "evidence/shape-evidence.json"]
    for raw in [*(blob(path) for path in revised), *(frozen(item["path"]) for item in shared)]:
        require(not re.search(r"\bclaude\b|\bgpt\b|NEEDS FIX|CONFIRMED",
                              raw.decode("utf-8"), re.I), "Cross-review material in shared evidence")
    dispositions = json.loads(blob(PREFIX + "dispositions.json"))["dispositions"]
    require({row["id"] for row in dispositions} == {*(f"Q{i}" for i in range(1, 17)), "F1-広"}
            and {row["candidate"] for row in dispositions if row["decision"] == "direct-guard"}
            == set("多楽広"), "Finite disposition inventory changed")
    freeze_json(REVIEW / "reconciliation-001-source-adjudication.json", {
        "batch": 124, "candidate": CANDIDATE, "status": "READY_FOR_INDEPENDENT_CONFIRMATIONS",
        "verificationSha256": VERIFICATION_SHA, "neutralDerivatives": derivatives,
        "implementedDirectPairs": ["多", "楽", "広"],
        "sourceBasis": "多い explicitly includes large quantity/much; 楽 has a separate economically "
                       "comfortable sense; 広い is spacious and matches the roominess taught on 裕. "
                       "The name-list correction is present without changing quiz readings.",
        "unacceptedNoGuardProposals": [row["id"] for row in dispositions if row["decision"] == "no-new-guard"],
        "limits": "The 14 no-new-guard proposals are not coordinator-confirmed clean decisions. "
                  "Each original family must evaluate the full selected evidence and actual delta. "
                  "No source-completeness proof settles semantic equivalence, and neither initial "
                  "acceptance nor this preparation approves publication.",
    })
    for family, (session, acceptance_sha) in REVIEWERS.items():
        run = f"N1-B124-{family.upper()}-CONFIRM-001"
        acceptance = REVIEW / f"N1-B124-{family.upper()}-001-acceptance.json"
        frozen(acceptance, acceptance_sha)
        response_path = neutral_dir / f"response-{family}.md"
        response = blob(PREFIX + f"{family}-response.md")
        require(sha(response) == proof["signedArtifacts"][PREFIX + f"{family}-response.md"],
                "Signed author response changed")
        write_frozen(response_path, response)
        spec = {
            "batch": 124, "run": run, "family": family, "candidate": CANDIDATE, "session": session,
            "acceptance": {"path": str(acceptance), "sha256": acceptance_sha},
            "revisedSources": revised, "originalSources": originals,
            "additionalSources": [additional(response_path, "author-response/current.md"), *shared],
        }
        path = REVIEW / "confirm" / f"{run}-spec.json"
        freeze_json(path, spec)
        build(path)
    print(json.dumps({"runsPrepared": ["N1-B124-CLAUDE-CONFIRM-001", "N1-B124-GPT-CONFIRM-001"],
                      "reviewersLaunched": False, "candidate": CANDIDATE}))


if __name__ == "__main__":
    main()
