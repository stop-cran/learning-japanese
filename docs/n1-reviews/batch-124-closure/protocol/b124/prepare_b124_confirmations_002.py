"""Build isolated held-confirmation followups after the signed response correction."""
import copy
import json
import re
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, json_bytes, load_batch, require, sha, write_frozen
from confirm_v2 import clean
from confirm_v3 import build_followup
from prepare_b124_confirmations import REVIEWERS, additional
from verify_b124_reconciliation_002 import COMPARISONS, PREFIX, PREVIOUS_PREFIX, SELECTION

REVIEW = WS / "scratch-124" / "review"
RUNTIME_PROOF_SHA = "d914e5e63ab5e576aae26104276b8bb7b1fad1b81656923d48b510a522594dc2"
DOCUMENTATION_PROOF_SHA = "cbd96e89ff2b970672eca3b8316f970b80fe9692f3c396d689950a1340ead591"
DOCUMENTATION_CANDIDATE = "beba46248ea0da6faa1c34b64f5c700565be5b23"
PRIORS = {
    "claude": ("CONFIRMED", ["Q1", "Q5"],
               "587370ad871542d9282db9ee8b76f8a25933dc126c526d6a59dcffb5b156e11d"),
    "gpt": ("UNVERIFIED", ["Q1", "Q3", "Q4", "Q5", "Q7", "Q8", "Q10", "Q11", "Q16"],
            "d889c8687cdadc5a843c18e401a82e17af1e88f0a16ee3bcdaab1ff02faa2aa5"),
}


def neutralize(name, original):
    value = copy.deepcopy(original)
    if name == "source-receipt.json":
        del value["confirmationBindings"]
        removed = ["/confirmationBindings"]
    elif name == "dispositions.json":
        del value["confirmationStatus"]
        removed = ["/confirmationStatus"]
    elif name == "selection-005.json":
        keys = ("reviewResponses", "rawConfirmationVerdicts", "reviewEvidenceAccepted", "confirmationAccepted")
        for key in keys:
            del value["reconciliation"][key]
        removed = [f"/reconciliation/{key}" for key in keys]
    else:
        raise ValueError("Unknown neutral source")
    return value, removed


def main(documentation_proof_path):
    config = load_batch(124)
    doc_raw = frozen(documentation_proof_path, DOCUMENTATION_PROOF_SHA)
    doc = json.loads(doc_raw)
    runtime = json.loads(frozen(REVIEW / "coordinator-reconciliation-verification-002.json", RUNTIME_PROOF_SHA))
    candidate = doc["candidate"]
    require(doc["status"] == "PASS" and doc["parent"] == runtime["candidate"]
            and candidate == DOCUMENTATION_CANDIDATE and doc["newStandardGateSetsRun"] is False
            and doc["runtimeAndPriorEvidenceUnchanged"] is True and not doc["memory"]["breach"],
            "Documentation correction has not been independently verified")
    clean(config, candidate)
    blob = lambda path: git(config, "show", f"{candidate}:{path}")
    neutral = REVIEW / "reconciliation-002-neutral"
    require(not neutral.exists(), "Preserve existing second-round sources")
    derivatives, shared = [], []
    for name, signed_path in (
        ("source-receipt.json", PREFIX + "source-receipt.json"),
        ("dispositions.json", PREFIX + "dispositions.json"),
        ("selection-005.json", SELECTION),
    ):
        raw = blob(signed_path)
        require(sha(raw) == runtime["signedArtifacts"][signed_path], "Verified signed source changed")
        value, removed = neutralize(name, json.loads(raw))
        value["_reviewIsolation"] = {
            "originalSignedPath": signed_path, "originalSha256": sha(raw),
            "removedJsonPointers": removed,
            "scope": "Only cross-report provenance removed; all substantive pair claims and selectors preserved.",
        }
        path = neutral / name
        output = write_frozen(path, json_bytes(value))
        derivatives.append({"inputSha256": sha(raw), "output": output, "removed": removed})
        shared.append(additional(path, f"neutral-author-evidence/{name}"))
    for name in ("source-receipt.json", "selection.json"):
        shared.append(additional(REVIEW / "reconciliation-001-neutral" / name,
                                 f"reused-source-contract/{name}"))
    summary = {key: runtime[key] for key in (
        "batch", "initial", "base", "manifestSha256", "contentVersion", "runtimeEntries",
        "sourceReceiptSha256", "sourceRecords", "runner", "gateSets",
        "metadataStrokesSupportAndHistoricalEvidencePreserved",
        "sourceMembersPublishedBeforeBatch", "sourceMembersInCandidate",
    )}
    summary.update(
        candidate=candidate, runtimeGateSnapshot=runtime["candidate"], status="PASS_MECHANICAL_ONLY",
        semanticAcceptance=False, sourceProofSha256=RUNTIME_PROOF_SHA,
        documentationProofSha256=sha(doc_raw), documentationOnlySuccessorVerified=True,
        limits="The runtime gate logs retain their actual snapshot identity. The later signed successor "
               "only adds isolated response-attribution documents; runtime and prior sources are byte-identical. "
               "Mechanical checks are not semantic, confirmation, device or publication acceptance.",
    )
    summary_path = neutral / "verification-summary.json"
    freeze_json(summary_path, summary)
    shared.append(additional(summary_path, "verification/signed-correction-summary.json"))
    gates = Path(runtime["gateSets"]["committed"]["directory"])
    for name in ("summary.json", *(f"{gate}.log" for gate in CHECKS)):
        shared.append(additional(gates / name, f"committed-checks/{name}"))
    revised = [
        "kanji/\u88d5.md", "words/\u4f59\u88d5.md", PREVIOUS_PREFIX + "jmdict-records.xml",
        PREVIOUS_PREFIX + "kanjidic2-records.xml", "docs/n1-sources/batch-124/jmdict-selected-records.xml",
        *(PREVIOUS_PREFIX + f"comparison-cards/{char}.md" for char in sorted(COMPARISONS)),
    ]
    originals = [f"repo/kanji/{char}.md" for char in sorted(set("\u539a\u5bcc\u8c4a\u8ca1\u5bb9\u88dc\u8907"))]
    originals += ["evidence/external-snapshots/01-extract.txt",
                  "evidence/external-snapshots/manifest.json", "evidence/shape-evidence.json"]
    for raw in [*(blob(path) for path in revised), *(frozen(item["path"]) for item in shared)]:
        require(not re.search(r"\bclaude\b|\bgpt\b|NEEDS FIX|CONFIRMED",
                              raw.decode("utf-8"), re.I), "Cross-review material in shared evidence")
    freeze_json(REVIEW / "reconciliation-002-confirmation-preparation.json", {
        "batch": 124, "candidate": candidate, "runtimeGateSnapshot": runtime["candidate"],
        "status": "READY_FOR_INDEPENDENT_CONFIRMATIONS", "semanticAcceptance": False,
        "documentationProofSha256": sha(doc_raw), "runtimeProofSha256": RUNTIME_PROOF_SHA,
        "neutralDerivatives": derivatives,
        "limits": "Conservative quiz exclusions resolve the author's uncertainty without claiming "
                  "universal synonymy. Original-family substantive confirmation is still required.",
    })
    for family, (session, initial_sha) in REVIEWERS.items():
        run = f"N1-B124-{family.upper()}-CONFIRM-002"
        prior_verdict, open_ids, prior_sha = PRIORS[family]
        prior_path = REVIEW / "confirm" / f"N1-B124-{family.upper()}-CONFIRM-001-acceptance.json"
        initial_path = REVIEW / f"N1-B124-{family.upper()}-001-acceptance.json"
        frozen(prior_path, prior_sha)
        frozen(initial_path, initial_sha)
        names = ["claude-response-002.md", "response-correction-001.json"] if family == "claude" else ["gpt-response.md"]
        family_sources = []
        for name in names:
            raw = blob(PREFIX + name)
            hashes = doc["signedArtifacts"] if family == "claude" else runtime["signedArtifacts"]
            require(sha(raw) == hashes[PREFIX + name], "Verified family response changed")
            require(not re.search(r"\bgpt\b" if family == "claude" else r"\bclaude\b",
                                  raw.decode("utf-8"), re.I), "Response contains the other family")
            path = neutral / f"{family}-{name}"
            write_frozen(path, raw)
            family_sources.append(additional(path, f"author-response/{name}"))
        spec = {
            "batch": 124, "run": run, "family": family, "candidate": candidate, "session": session,
            "acceptance": {"path": str(initial_path), "sha256": initial_sha},
            "basis": "held-confirmation", "prior": {"path": str(prior_path), "sha256": prior_sha},
            "priorVerdict": prior_verdict, "openClaimIds": open_ids,
            "revisedSources": revised, "originalSources": originals,
            "additionalSources": [*family_sources, *shared],
        }
        path = REVIEW / "confirm" / f"{run}-spec.json"
        freeze_json(path, spec)
        build_followup(path)
    print(json.dumps({"candidate": candidate, "preparedOnly": True, "reviewersLaunched": False}))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
