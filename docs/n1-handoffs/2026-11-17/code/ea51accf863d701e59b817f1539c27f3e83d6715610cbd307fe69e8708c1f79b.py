"""Prepare isolated, bounded integration-impact followups without contacting reviewers."""
import json
from pathlib import Path

from b130_context_confirmation import binding
from b130_integration_lineage import ACCEPTANCE_SHA, PREVIOUS, PRIOR_CANDIDATE, RUNS, check_capacity
from common import freeze_json, frozen, json_bytes, load_batch, require, sha, start_guard, write_frozen
from confirm_b130_integration import build_followup, clean
from prepare_b130_claude004 import select_complete
from prepare_b130_confirmations import FAMILIES, additional, neutral
from verify_b130_integration_evidence import BUNDLE, CANDIDATE, MANIFEST
from verify_b130_integration_runtime import BASE, CLOSURE, INCOMING, ROOT
from verify_b130_payload import REPO, RUNNER
from verify_b130_revision_runtime_v3 import PREFIX
from verify_b130_sources import Git

OUTPUT = ROOT / "integration-confirmation-001-neutral"
PROOF_SHA = "ea21d87422c1af22703ae09d39c1a51747fe127db12a52293538e55a42836ffa"
CAPACITY_SHA = "e65fd1162980b71d2c1670098e96b32f7451462efaefa2e62bdf600dab390c26"


def main():
    require(not OUTPUT.exists(), "Preserve existing integration preparation")
    derivation = json.loads(frozen(ROOT / "integration-protocol-derivation-001.json",
                                   "9d9de8dacf74b0cb18a259546fd6344c59919f409e80bdbe80f33c6c56968bba"))
    for item in derivation["outputs"]:
        frozen(item["path"], item["sha256"])
    proof = json.loads(frozen(ROOT / "integration-evidence-001.json", PROOF_SHA))
    require(proof["status"] == "PASS_INTEGRATION_BINDINGS_ONLY" and proof["candidate"] == CANDIDATE
            and proof["manifestSha256"] == MANIFEST
            and proof["reviewAccepted"] is False and proof["publicationAccepted"] is False,
            "Integrated evidence has not passed independent mechanical verification")
    runtime = json.loads(frozen(proof["runtimeProof"]["path"], proof["runtimeProof"]["sha256"]))
    capacity_path = ROOT / "integration-capacity-observation-001.json"
    capacity = json.loads(frozen(capacity_path, CAPACITY_SHA))
    config = load_batch(130)
    guard, _ = start_guard("B130 bounded integration confirmation preparation")
    git = Git(REPO, RUNNER, guard)
    try:
        clean(config, CANDIDATE)
        blob = lambda path: git("show", f"{CANDIDATE}:{path}")
        revised = [f"kanji/{char}.md" for char in ("\u5840", "\u62cd", "\u8017", "\u97ff")]
        revised += ["words/\u5840.md", "words/\u62cd\u624b.md", "words/\u6d88\u8017.md",
                    "articles/numbers-and-counters.md", "counters/age.json"]
        for path in revised:
            require(neutral(blob(path)), "Review-family attribution in shared source")
        raw = blob(PREFIX + "jmdict-families.xml")
        require(raw == git("show", f"{PRIOR_CANDIDATE}:{PREFIX}jmdict-families.xml"),
                "Existing decisive source collection changed")
        selected, selection = select_complete(raw, "entry", "ent_seq", ("1238610", "1408810"))
        require(neutral(selected), "Selected full source records contain review attribution")
        selected_path = OUTPUT / "jmdict-families.xml"
        write_frozen(selected_path, selected)
        shared = [additional(selected_path, "reused-sources/jmdict-families.xml")]
        summary = {
            "batch": 130, "candidate": CANDIDATE, "parents": [CLOSURE, INCOMING],
            "previousN1Snapshot": PRIOR_CANDIDATE, "publishedBase": BASE,
            "status": "INDEPENDENT_MECHANICAL_VERIFICATION_ONLY", "proofSha256": PROOF_SHA,
            "runtimeProofSha256": proof["runtimeProof"]["sha256"],
            "trackedPaths": runtime["trackedPaths"], "otherTrackedBlobsAndModesUnchanged": 40294,
            "runtimeEntries": 8730, "otherRuntimeHashesUnchanged": 8728,
            "runtimeChanged": runtime["runtimeChanged"], "manifestSha256": MANIFEST,
            "contentVersion": "3df59f6cf1dee0f2", "incomingContentsByteEqualToSecondParent": True,
            "generatedManifestByteReproducible": True,
            "unchangedN1": "Every N1 card/support/metadata/practice/exclusion, source/review/progress artifact "
                           "and earlier Notes remains byte-identical to the first parent. That parent's "
                           "contributor-only closure preserved the earlier N1 snapshot.",
            "gateSets": {mode: {
                "summarySha256": facts["summarySha256"],
                "gates": [{key: row[key] for key in ("gate", "receiptSha256", "logSha256")}
                          for row in facts["gates"]],
                "actualHostTests": 431, "unchangedCommandsAndSerialOrder": True,
                "resourceAndImmediateChildCleanupVerified": True,
            } for mode, facts in proof["gateSets"].items()},
            "notesWarnings": {"count": 83, "unchanged": True,
                              "exactListSha256": sha(json_bytes(proof["retainedQuizSafetyWarnings"]))},
            "sourceReuse": {"signedSource": PREFIX + "jmdict-families.xml",
                           "signedSourceSha256": sha(raw), "presentedSha256": sha(selected),
                           **selection, "newQueriesOrFetches": 0},
            "scope": "Integration-impact followup, not a new whole-card/source-universe review. The complete "
                     "incoming article and counter and current scoped cards/supports are presented. Only the "
                     "two complete decisive dictionary families are reread, not the remaining97 families, "
                     "original519-family collection, full character collections, comparison-card universe "
                     "or pair tables. All unchanged evidence remains preserved; no new lexical allocation "
                     "claim is made. Actual full gate logs/receipts were independently checked; their bindings "
                     "and results are supplied here, not a claim that the reader reread or reran those logs.",
            "limits": "Effect/impression lexical allocation remains unresolved; the quiz consequence remains "
                      "protected by the existing precaution. Rare/image/old-dictionary allocations and unread "
                      "index limits remain. Host evidence stays bounded to the established N1/All/Starter-plus-one "
                      "cases, with latent readings retained; no arbitrary/custom/multiple-borrow/Kotlin/native/"
                      "device/font-rendering/old-APK/served-ZIP acceptance. Incoming counter-language correctness "
                      "is not newly certified by these mechanical checks.",
            "reviewAccepted": False, "publicationAccepted": False, "deliveryCredit": 0,
        }
        require(neutral(json_bytes(summary)), "Shared integration proof contains review-family attribution")
        freeze_json(OUTPUT / "verification.json", summary)
        shared.append(additional(OUTPUT / "verification.json", "verification/integration.json"))
        runs = []
        for family in ("claude", "gpt"):
            previous = json.loads(frozen(ROOT / "confirm" / f"{PREVIOUS[family]}-spec.json"))
            own = [PREFIX + f"responses/{family}-response-002.md",
                   PREFIX + f"responses/{family}-mapping-002.json"]
            opposite = "gpt" if family == "claude" else "claude"
            require(all(not FAMILIES[opposite].search(blob(path).decode()) for path in own),
                    "Own response/mapping exposes the other family")
            spec = {key: previous[key] for key in
                    ("batch", "family", "session", "originalSession", "acceptance", "reviewerOrigin")}
            if family == "claude":
                spec["preparedOnlyPriorRun"] = previous["preparedOnlyPriorRun"]
            spec.update({
                "run": RUNS[family], "candidate": CANDIDATE, "basis": "accepted-confirmation",
                "priorVerdict": "CONFIRMED", "openClaimIds": [],
                "prior": {"path": str(ROOT / "confirm" / f"{PREVIOUS[family]}-acceptance.json"),
                          "sha256": ACCEPTANCE_SHA[family]},
                "capacityObservation": {"path": str(capacity_path), "sha256": CAPACITY_SHA},
                "revisedSources": [*revised, *own], "originalSources": [], "additionalSources": shared,
            })
            spec_path = ROOT / "confirm" / f"{RUNS[family]}-spec.json"
            freeze_json(spec_path, spec)
            build_followup(spec_path)
            chain = json.loads(frozen(ROOT / "confirm" / f"{RUNS[family]}-chain.json"))
            chain_bytes = sum(row["bytes"] for row in chain["segments"])
            observed = next(row for row in capacity["reviewers"] if row["family"] == family)
            checked = check_capacity(capacity, family, spec["session"], observed["eventsSha256"], chain_bytes)
            runs.append({"run": spec["run"], "session": spec["session"], "spec": binding(spec_path),
                         "segments": len(chain["segments"]), "chainBytes": chain_bytes,
                         "capacityPreflightOnly": checked})
        clean(config, CANDIDATE)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Integration preparation RAM guard breached")
    print(json.dumps(freeze_json(ROOT / "integration-confirmation-preparation-001.json", {
        "status": "PREPARED_NOT_ADMITTED", "candidate": CANDIDATE, "runs": runs,
        "sharedSources": shared, "revisedSharedSources": revised, "sourceSelection": selection,
        "proofSha256": PROOF_SHA, "capacityObservationSha256": CAPACITY_SHA,
        "producer": binding(__file__), "memory": memory, "reviewersLaunched": False,
        "isolation": "Only each recipient's own last accepted report and isolated response/mapping, actual "
                     "runtime delta, current relevant content and neutral evidence. No combined handoff, "
                     "inventory, opposite-family report/verdict or initial report reread.",
    })))


if __name__ == "__main__":
    main()
