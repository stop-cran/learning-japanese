"""Build family-isolated confirmations for the verified signed B127 successor."""
import copy
import json
import re
from pathlib import Path

from common import (CHECKS, TOOLS, WS, freeze_json, frozen, git, json_bytes, load_batch,
                    require, sha, start_guard, write_frozen)
from confirm_b127 import build, clean
from finalize_b127 import check_proof
from verify_b127_reconciliation import ADDED_GUARDS, CARD, CANDIDATE, MEMBER, OTHERS, PREFIX

REVIEW = WS / "scratch-127" / "review"
PROOF_SHA = "6d63b9a10b3059a2a39ab7481e17a76ae628afc2255c7e5f0128d241cac1d6cb"
TOOLING_SHA = "25ac6ceb9d32b458735cb71d52f38b4f37f0aac870df52de4008333c1073b86f"
REVIEWERS = {
    "claude": ("b1e90345-f8f3-4c8d-b776-09eb8d299ba9",
               "919d75a822715a6e51009a9e077f49a9ea251a297ea6bbab46b2245793623e22"),
    "gpt": ("3d1c4b40-90b0-466d-a565-32a96db5281c",
            "accc68fa089f6d702d3fc3bddd163e786caff27da74cdc78dec3559f81063800"),
}
PROVENANCE = re.compile(r"\bclaude\b|\bgpt\b|\bCLEAN\b|NEEDS FIX|CONFIRMED", re.I)


def shared_is_neutral(raw):
    return not PROVENANCE.search(raw.decode("utf-8"))


def response_is_isolated(family, raw):
    other = {"claude": "gpt", "gpt": "claude"}[family]
    return not re.search(rf"\b{other}\b", raw.decode("utf-8"), re.I)


def neutral_receipt(receipt):
    result = copy.deepcopy(receipt)
    del result["admissionBindings"]
    result["derivation"] = {
        "originalSignedPath": PREFIX + "source-receipt.json",
        "originalSha256": sha(json_bytes(receipt)),
        "onlyOmittedTopLevelKey": "admissionBindings",
        "reason": "Contains family-specific report/adjudication identities. All dictionary selectors, "
                  "complete records, source input hashes and local capture bindings are unchanged.",
    }
    return result


def additional(path, source):
    return {"path": str(path), "source": source, "sha256": sha(frozen(path))}


def main():
    config = load_batch(127)
    guard, _ = start_guard("B127 isolated confirmation preparation")
    try:
        clean(config, CANDIDATE)
        proof = json.loads(frozen(REVIEW / "reconciliation-001-independent-proof.json", PROOF_SHA))
        check_proof(proof, CANDIDATE, config)
        tooling = json.loads(frozen(REVIEW / "confirm" / "tooling-preflight-recovery-001.json", TOOLING_SHA))
        require(tooling["status"] == "PASS_PREPARATION_ONLY" and tooling["exitCode"] == 0,
                "Confirmation tooling is not ready")
        for item in tooling["derivations"]:
            frozen(item["output"]["path"], item["output"]["sha256"])
        for field in ("output", "helper"):
            item = tooling["engineDerivation"][field]
            frozen(item["path"], item["sha256"])
        blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
        receipt_raw = blob(PREFIX + "source-receipt.json")
        receipt = json.loads(receipt_raw)
        require(sha(receipt_raw) == proof["sourceReceiptSha256"]
                and receipt_raw == json_bytes(receipt), "Source receipt serialization differs")
        neutral_source = neutral_receipt(receipt)
        require({key: value for key, value in neutral_source.items() if key != "derivation"}
                == {key: value for key, value in receipt.items() if key != "admissionBindings"},
                "Neutral derivative changed source evidence")
        summary = {key: proof[key] for key in (
            "batch", "candidate", "parent", "base", "signature", "runtimeChanged", "runtimeEntries",
            "manifestSha256", "contentVersion", "sourceReceiptSha256", "dispositionsSha256",
            "sources", "gateSets", "publishedBaseLinkplan", "addedDirectGuards", "conservativeGuardIds",
            "distinctClaimIds", "unguardedOpenClaimIds")}
        summary.update(
            status="PASS_MECHANICAL_ONLY", sourceProofSha256=PROOF_SHA, semanticAcceptance=False,
            limits="Signed bytes, complete dictionary selections and host gates only. The finite "
                   "author dispositions require independent evaluation; conservative guards retain "
                   "linguistic uncertainty. No native/device, arbitrary-pool or publication acceptance.")
        from verify_b127_reconciliation import OLD_GUARDS
        comparisons = sorted(set(OTHERS) | set(OLD_GUARDS) | set("\u91d1\u5168\u5408\u4eba\u53e3"))
        revised = [CARD, f"words/{MEMBER}\u5eab.md"]
        revised += [f"kanji/{char}.md" for char in comparisons]
        original_prefix = "docs/n1-sources/batch-127/"
        revised += [original_prefix + name for name in (
            "jmdict-selected-records.xml", "kanjidic2-selected-records.xml",
            "kanjidic2-expanded-comparison-records.xml")]
        revised += [PREFIX + name for name in (
            "pair-dispositions.json", "jmdict-comparison-records.xml",
            "kanjidic2-comparison-records.xml", "external-source-summary.json")]
        originals = [f"evidence/external-snapshots/{i:02d}-extract.txt" for i in range(1, 4)]
        originals += ["evidence/external-snapshots/manifest.json"]
        responses = {family: blob(PREFIX + family + "-author-response.md") for family in REVIEWERS}
        for family, raw in responses.items():
            require(sha(raw) == proof["responses"][family] and response_is_isolated(family, raw),
                    f"Family response changed or leaked: {family}")
        for path in revised:
            require(shared_is_neutral(blob(path)), f"Family provenance in shared input: {path}")
            guard.check()
        require(shared_is_neutral(json_bytes(summary)) and shared_is_neutral(json_bytes(neutral_source)),
                "Neutral summary or source receipt leaks review provenance")
        neutral = REVIEW / "confirmation-001-neutral"
        require(not neutral.exists(), "Preserve existing neutral inputs")
        summary_path, receipt_path = neutral / "verification-summary.json", neutral / "source-receipt.json"
        freeze_json(summary_path, summary)
        freeze_json(receipt_path, neutral_source)
        shared = [additional(summary_path, "verification/signed-correction-summary.json"),
                  additional(receipt_path, "evidence/reconciliation/source-receipt.json")]
        committed = proof["gateSets"]["committed"]
        directory = Path(committed["directory"])
        frozen(directory / "summary.json", committed["summarySha256"])
        shared.append(additional(directory / "summary.json", "committed-checks/summary.json"))
        rows = {row["gate"]: row for row in committed["gates"]}
        require(set(rows) == set(CHECKS), "Committed gate set differs")
        for name in CHECKS:
            path = directory / f"{name}.log"
            frozen(path, rows[name]["logSha256"])
            shared.append(additional(path, f"committed-checks/{name}.log"))
        supplement = proof["publishedBaseLinkplan"]
        for filename, key in (("receipt.json", "receiptSha256"), ("output.log", "logSha256")):
            path = Path(supplement["directory"]) / filename
            frozen(path, supplement[key])
            shared.append(additional(path, f"committed-checks/published-base-linkplan/{filename}"))
        for item in shared:
            require(shared_is_neutral(frozen(item["path"])), f"Shared input leaks: {item['source']}")
        prepared = []
        for family, (session, acceptance_sha) in REVIEWERS.items():
            initial = f"N1-B127-{family.upper()}-001"
            run = f"N1-B127-{family.upper()}-CONFIRM-001"
            acceptance_path = REVIEW / f"{initial}-acceptance.json"
            accepted = json.loads(frozen(acceptance_path, acceptance_sha))
            require(accepted["run"] == initial and accepted["reviewAccepted"] is True,
                    "Original review is not accepted")
            response_path = neutral / f"response-{family}.md"
            write_frozen(response_path, responses[family])
            spec = {
                "batch": 127, "run": run, "family": family, "candidate": CANDIDATE, "session": session,
                "acceptance": {"path": str(acceptance_path), "sha256": acceptance_sha},
                "revisedSources": revised, "originalSources": originals,
                "additionalSources": [additional(response_path, "author-response/current.md"), *shared],
            }
            path = REVIEW / "confirm" / f"{run}-spec.json"
            freeze_json(path, spec)
            build(path)
            prepared.append(run)
        result = {
            "batch": 127, "candidate": CANDIDATE, "runsPrepared": prepared,
            "verificationSha256": PROOF_SHA, "neutralReceiptSha256": sha(json_bytes(neutral_source)),
            "implementedDirectPairs": ADDED_GUARDS, "unguardedOpenFinitePairs": [],
            "sourceDistinctPair": "\u5b58", "reviewersLaunched": False,
            "isolation": "Only the owning family's unchanged report and response are present in its "
                         "chain. Shared evidence is neutral; the complete original source receipt "
                         "is preserved signed, with only admissionBindings omitted in the derivative.",
            "limits": "Readiness only, not semantic or publication acceptance. External extracts and "
                      "mixed read-chain segments remain local.",
            "producerSha256": sha(Path(__file__).read_bytes()),
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Confirmation preparation RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(REVIEW / "confirmation-001-preparation.json", result)))


if __name__ == "__main__":
    main()
