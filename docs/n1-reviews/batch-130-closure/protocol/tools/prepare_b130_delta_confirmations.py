"""Prepare bounded same-fresh-reviewer confirmations from the verified signed delta."""
import json
from pathlib import Path

from b129_confirmation_presentation import canonical, compact_xml
from b130_context_confirmation import binding
from b130_followup_closure_history import FINALS, HISTORICAL, PREVIOUS
from b130_followup_lineage import PRIOR_SHA
from common import TOOLS, freeze_json, frozen, json_bytes, load_batch, require, sha, start_guard, write_frozen
from confirm_b130_followup_v2 import build_followup, clean
from prepare_b130_confirmations import FAMILIES, additional, neutral, pair_lines
from verify_b130_delta_evidence import CANDIDATE, ROOT
from verify_b130_payload import REPO, RUNNER
from verify_b130_revision_runtime_v3 import PREFIX
from verify_b130_sources import Git

PROOF_SHA = "0288e16198420c4e8b8b14a109ce6af2ac7cf4b8572468639b923aa59affa5a9"
OUTPUT = ROOT / "confirmation-003-neutral"


def main():
    require(not OUTPUT.exists(), "Preserve existing confirmation preparation")
    proof = json.loads(frozen(ROOT / "delta-evidence-001" / "verification.json", PROOF_SHA))
    require(proof["candidate"] == CANDIDATE and proof["parent"] == PREVIOUS
            and proof["status"] == "PASS_SECOND_RECONCILIATION_BINDINGS_ONLY"
            and proof["reviewAccepted"] is False and proof["publicationAccepted"] is False,
            "Signed follow-up has not passed independent mechanical verification")
    runtime = json.loads(frozen(proof["proofs"]["runtime"]["path"], proof["proofs"]["runtime"]["sha256"]))
    config = load_batch(130)
    guard, _ = start_guard("B130 bounded follow-up confirmation preparation")
    git = Git(REPO, RUNNER, guard)
    try:
        clean(config, CANDIDATE)
        blob = lambda path: git("show", f"{CANDIDATE}:{path}")
        revised = [f"kanji/{char}.md" for char in ("塀", "拍", "耗", "響")]
        revised += ["words/塀.md", "words/拍手.md", "words/消耗.md"]
        revised += [PREFIX + name for name in (
            "source-reuse-002.json", "source-receipt.json", "query-membership.json")]
        for name in revised:
            require(neutral(blob(name)), "Review-family attribution in shared source")
        shared, presentations = [], {}
        for name in ("jmdict-families.xml", "kanjidic2-records.xml",
                     "pair-dispositions-001.json", "pair-dispositions-002.json"):
            raw = blob(PREFIX + name)
            data = pair_lines(raw) if name.endswith(".json") else compact_xml(raw)
            presented = name.replace(".json", ".jsonl")
            require(neutral(data), "Shared presentation names a review family")
            path = OUTPUT / presented
            write_frozen(path, data)
            shared.append(additional(path, "evidence/reconciliation/" + presented))
            presentations[presented] = {
                "signedSource": PREFIX + name, "signedSha256": sha(raw), "presentedSha256": sha(data),
                "completeInfosetOrObjectPreserved": True,
                "canonicalSha256": None if name.endswith(".json") else sha(canonical(raw).encode()),
            }
        disclosure = {
            "method": "Complete XML canonical infosets with indentation removed and one record per line; "
                      "complete pair headers followed by complete rows with exact JSON roundtrip. "
                      "No meanings, languages, restrictions, decisions or qualifications removed.",
            "files": presentations,
            "scope": "Only the new direct precaution and qualified Notes on 拍, with exact diff from the "
                     "prior confirmation snapshot. The three scoped cards, their three support articles "
                     "and complete actual 響 card are supplied, along with all99 complete reconciliation "
                     "families,31 complete character records and both28-row tables. Other unchanged "
                     "comparison/curated cards, the original519-family collection, external captures "
                     "and original192-character collection are NOT reread in this bounded follow-up. "
                     "Prior limits remain; this is not a fresh full-card or whole-index review.",
        }
        summary = {
            "batch": 130, "candidate": CANDIDATE, "parent": PREVIOUS, "base": proof["base"],
            "status": "SIGNED_MECHANICAL_CHECKS_ONLY", "proofSha256": PROOF_SHA,
            "runtimeEntries": runtime["runtimeEntries"], "runtimeChanged": runtime["runtimeChanged"],
            "manifestSha256": runtime["manifestSha256"], "contentVersion": runtime["contentVersion"],
            "addedGuards": {"拍": ["響"]}, "finitePairs": 28,
            "pairDecisionCounts": proof["pairBindings"]["counts"],
            "declaredOpenQuizHolds": [], "semanticAcceptance": False,
            "sourceReuse": "Existing complete records and comparisons are byte-identical to the earlier "
                           "independently verified source proof. No new dictionary scan or fetch.",
            "checks": "All ten author checks and all ten committed checks passed. The first committed "
                      "attempt aborted for RAM during validate and remains an abort; complete retry002 "
                      "passed.83 exact nonfatal warnings and both latent readings remain.",
            "limits": "Precaution protects the unresolved effect/impression region, not ordinary synonymy "
                      "or lexical allocation. Host checks do not establish arbitrary/custom/multiple-borrow "
                      "pools, Kotlin/native/device, font rendering or old-APK behavior. No delivery credit.",
        }
        for name, value in (("presentation.json", disclosure), ("verification.json", summary)):
            require(neutral(json_bytes(value)), "Neutral metadata contains a review family")
            freeze_json(OUTPUT / name, value)
            shared.append(additional(OUTPUT / name, "verification/" + name))
        for name in ("summary.json", *[row["gate"] + ".log" for row in proof["gateSets"]["committed"]["gates"]]):
            item = proof["capturedExecutionFiles"]["reconciliation-002-committed-gates-002/" + name]
            require(neutral(frozen(item["path"], item["sha256"])), "Check output contains review attribution")
            shared.append(additional(Path(item["path"]), "committed-checks/" + name))
        runs = []
        for family in ("claude", "gpt"):
            origin_path = ROOT / "confirm" / f"{HISTORICAL[family]}-spec.json"
            origin = json.loads(frozen(origin_path))
            prior_path = ROOT / "confirm" / f"{HISTORICAL[family]}-acceptance.json"
            prior = json.loads(frozen(prior_path, PRIOR_SHA[family]))
            own = [PREFIX + f"responses/{family}-response-002.md",
                   PREFIX + f"responses/{family}-mapping-002.json"]
            opposite = "gpt" if family == "claude" else "claude"
            require(all(not FAMILIES[opposite].search(blob(path).decode("utf-8")) for path in own),
                    "Family response is not isolated")
            spec = {
                "batch": 130, "run": FINALS[family], "family": family, "candidate": CANDIDATE,
                "session": origin["session"], "originalSession": origin["originalSession"],
                "acceptance": origin["acceptance"], "reviewerOrigin": binding(origin_path),
                "prior": {"path": str(prior_path), "sha256": PRIOR_SHA[family]},
                "basis": "accepted-confirmation" if family == "claude" else "held-confirmation",
                "priorVerdict": prior["verdict"], "openClaimIds": prior["openClaimIds"],
                "revisedSources": [*revised, *own], "originalSources": [], "additionalSources": shared,
            }
            spec_path = ROOT / "confirm" / f"{FINALS[family]}-spec.json"
            freeze_json(spec_path, spec)
            build_followup(spec_path)
            chain = json.loads(frozen(ROOT / "confirm" / f"{FINALS[family]}-chain.json"))
            runs.append({"run": spec["run"], "session": spec["session"],
                         "segments": len(chain["segments"]),
                         "chainBytes": sum(row["bytes"] for row in chain["segments"]),
                         "spec": binding(spec_path)})
        clean(config, CANDIDATE)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Confirmation preparation RAM guard breached")
    print(json.dumps(freeze_json(ROOT / "confirmation-003-preparation.json", {
        "batch": 130, "candidate": CANDIDATE, "status": "PREPARED_NOT_ADMITTED",
        "proofSha256": PROOF_SHA, "runs": runs, "sharedSources": shared,
        "revisedSharedSources": revised, "originalSources": [], "presentations": presentations,
        "memory": memory, "reviewersLaunched": False, "producer": binding(__file__),
        "isolation": "Each reader gets its own prior confirmation and original same-family initial report, "
                     "own-family response/mapping, actual delta and neutral complete source/check evidence. "
                     "No other-family report, combined handoff, author inventory/producers or excluded review.",
    })))


if __name__ == "__main__":
    main()
