"""Prepare isolated original-reviewer chains from the verified B130 successor."""
import json
import re
import sys
from pathlib import Path

from b129_confirmation_presentation import canonical, compact_xml
from b130_compact_common import verify_packet
from common import freeze_json, frozen, json_bytes, load_batch, require, sha, start_guard, write_frozen
from confirm_b130_compact import build, clean
from verify_b130_payload import REPO, RUNNER
from verify_b130_revision_runtime_v3 import INITIAL_SHA, MEMBERS, PARENT, PREFIX, ROOT
from verify_b130_sources import Git

REVIEWERS = {"claude": "b6bd4627-73cc-452b-9a56-2b9407c9a0cf",
             "gpt": "827ecfff-5750-4a20-baa7-7f0952d31ca1"}
HELPERS = {
    "confirm_b130_compact.py": "f18dd4515b7ea2f351f9064f69edc299db67c23507c2f697715b04ea4121bdf3",
    "b129_confirmation_presentation.py": "3e6021a6d64bb2d969c7b8cb40fa029caa70077d380840bfc1d12543921493f1",
}
PROOF_SHA = "3b05ee5d043bdf081ef30ec818cc46a4e16f9bacd472e5266b6a69b048871df1"
OUTPUT = ROOT / "confirmation-001-neutral"
FAMILIES = {"claude": re.compile(r"\b(?:claude|anthropic|opus|sonnet|haiku)\b", re.I),
            "gpt": re.compile(r"\b(?:gpt|openai|codex)\b", re.I)}


def neutral(raw):
    return not any(pattern.search(raw.decode("utf-8")) for pattern in FAMILIES.values())


def pair_lines(raw):
    value = json.loads(raw)
    header = {key: item for key, item in value.items() if key != "rows"}
    lines = [header, *value["rows"]]
    result = ("\n".join(json.dumps(item, ensure_ascii=False, separators=(",", ":")) for item in lines) + "\n").encode()
    parsed = [json.loads(line) for line in result.splitlines()]
    require({**parsed[0], "rows": parsed[1:]} == value, "Pair information lost during presentation")
    return result


def additional(path, source):
    return {"path": str(path), "sha256": sha(frozen(path)), "source": source}


def main(candidate):
    require(not OUTPUT.exists(), "Preserve an existing confirmation preparation")
    for name, digest in HELPERS.items():
        frozen(Path(__file__).with_name(name), digest)
    proof = json.loads(frozen(ROOT / "revision-evidence-001" / "verification.json", PROOF_SHA))
    require(proof["status"] == "PASS_SIGNED_RECONCILIATION_BINDINGS_ONLY"
            and proof["candidate"] == candidate and proof["parent"] == PARENT
            and proof["pairBindings"]["pairCount"] == 28
            and not proof["reviewAccepted"] and not proof["publicationAccepted"],
            "Signed reconciliation has not passed mechanical verification")
    tooling = json.loads(frozen(ROOT / "confirm" / "tooling-preflight.json",
                                "4716ffc27334041e6dac47189b6574c7bcc2a1a6947b740df0f2dbe19d778d29"))
    require(tooling["exitCode"] == 0 and tooling["status"] == "PASS_PREPARATION_ONLY",
            "Confirmation protocol tooling is not ready")
    for row in tooling["derivations"]:
        frozen(row["output"]["path"], row["output"]["sha256"])
    config = load_batch(130)
    require(config["candidate"] == PARENT, "Wrong original review snapshot")
    guard, _ = start_guard("B130 isolated original-reviewer confirmation preparation")
    git = Git(REPO, RUNNER, guard)
    try:
        clean(config, candidate)
        packet, sums, _ = verify_packet(config, guard)
        blob = lambda path: git("show", f"{candidate}:{path}")
        table_raw = blob(PREFIX + "pair-dispositions-001.json")
        table = json.loads(table_raw)
        sys.path.insert(0, str(REPO.parent / "lean"))
        from n1lib import parse
        cards = set(MEMBERS) | {row["pair"][1] for row in table["rows"]}
        for character in MEMBERS:
            metadata, _ = parse(blob(f"kanji/{character}.md").decode("utf-8").replace("\r\n", "\n"))
            cards.update(metadata["distractors"])
        revised = [f"kanji/{character}.md" for character in sorted(cards)]
        revised += ["words/\u5840.md", "words/\u62cd\u624b.md", "words/\u6d88\u8017.md"]
        revised += [PREFIX + name for name in ("source-receipt.json", "query-membership.json",
                                               "external-capture-bindings.json", "authored-source-analysis-001.json")]
        for path in revised:
            require(neutral(blob(path)), "Review-family provenance in a shared signed source: " + path)
        originals = ["evidence/jmdict-families.xml", "evidence/xml-presentation.json",
                     "evidence/external-snapshots/manifest.json"]
        originals += [f"evidence/external-snapshots/{number:02d}-extract.txt" for number in range(1, 8)]
        for name in originals:
            require(neutral(frozen(packet / name, sums[name])), "Review provenance in original shared evidence")
        shared, presentations = [], {}
        for name in ("jmdict-families.xml", "kanjidic2-records.xml", "pair-dispositions-001.json"):
            raw = blob(PREFIX + name)
            data = pair_lines(raw) if name.endswith(".json") else compact_xml(raw)
            presented = name.replace(".json", ".jsonl")
            require(neutral(data), "Shared presentation leaks review-family provenance")
            path = OUTPUT / presented
            write_frozen(path, data)
            shared.append(additional(path, "evidence/reconciliation/" + presented))
            presentations[presented] = {
                "signedSource": PREFIX + name, "signedSha256": sha(raw), "presentedSha256": sha(data),
                "completeInfosetOrObjectPreserved": True,
                "canonicalSha256": None if name.endswith(".json") else sha(canonical(raw).encode()),
            }
        disclosure = {
            "method": "Complete XML canonical infosets with indentation removed and one record per line. "
                      "Complete pair-table header then one whole row per line; exact JSON roundtrip verified. "
                      "No fields, source meanings, languages, restrictions, decisions or qualifications removed.",
            "files": presentations,
            "scope": "All 28 finite reconciliation pairs, their 99 complete families and 31 complete characters. "
                     "The original 519 complete JMdict families, seven complete external extracts, three new "
                     "complete external-body extracts, actual counterpart/curated cards and supports are supplied. "
                     "The original 192-character collection and other unchanged comparison cards are not reread "
                     "in this bounded delta confirmation. No whole-card re-review of comparison articles.",
        }
        runtime = json.loads(frozen(proof["proofs"]["runtime"]["path"], proof["proofs"]["runtime"]["sha256"]))
        summary = {
            "batch": 130, "candidate": candidate, "parent": PARENT, "base": proof["base"],
            "status": "SIGNED_MECHANICAL_CHECKS_ONLY", "proofSha256": PROOF_SHA,
            "runtimeEntries": runtime["runtimeEntries"], "runtimeChanged": runtime["runtimeChanged"],
            "manifestSha256": runtime["manifestSha256"], "contentVersion": runtime["contentVersion"],
            "finitePairs": 28, "pairDecisionCounts": table["counts"],
            "addedGuards": {char: runtime["cardMetadata"][char]["addedGuards"] for char in MEMBERS},
            "declaredOpenQuizHolds": table["openQuizHolds"], "semanticAcceptance": False,
            "limits": "Author dispositions are hypotheses, not accepted linguistic conclusions. A guarded "
                      "precaution does not establish synonymy or resolve historical glyph/spelling allocation. "
                      "All ten author and committed host checks passed with 83 retained nonfatal warnings. "
                      "Zero tested production/padded hits does not remove two latent readings or establish "
                      "arbitrary/custom/multiple-borrow pools, Kotlin/native/device, font fallback or older APK behavior.",
        }
        for name, value in (("presentation.json", disclosure), ("verification.json", summary)):
            require(neutral(json_bytes(value)), "Neutral metadata contains a review family")
            freeze_json(OUTPUT / name, value)
            shared.append(additional(OUTPUT / name, "verification/" + name))
        external = json.loads(frozen(proof["proofs"]["external"]["path"], proof["proofs"]["external"]["sha256"]))
        for index, capture in enumerate(external["captures"], 1):
            item = capture["outputs"]["complete-extract.txt"]
            require(neutral(frozen(item["path"], item["sha256"])), "External extract leaks provenance")
            shared.append(additional(Path(item["path"]), f"external-reconciliation/{index:02d}-complete.txt"))
        for name in ("summary.json", *[row["gate"] + ".log" for row in proof["gateSets"]["committed"]["gates"]]):
            item = proof["capturedExecutionFiles"]["reconciliation-committed-gates-001/" + name]
            require(neutral(frozen(item["path"], item["sha256"])), "Committed check contains review attribution")
            shared.append(additional(Path(item["path"]), "committed-checks/" + name))
        prepared = []
        for family, session in REVIEWERS.items():
            initial = f"N1-B130-{family.upper()}-004"
            run = f"N1-B130-{family.upper()}-CONFIRM-001"
            acceptance_path = ROOT / (initial + "-acceptance.json")
            accepted = json.loads(frozen(acceptance_path, INITIAL_SHA[family]))
            launch = json.loads(frozen(ROOT / (initial + "-launch.json")))
            require(accepted["candidate"] == PARENT and accepted["reviewAccepted"] is True
                    and accepted["verdict"] == "NEEDS FIX" and launch["session"] == session,
                    "Wrong accepted original reviewer")
            own = [PREFIX + f"responses/{family}-response-001.md",
                   PREFIX + f"responses/{family}-mapping-001.json"]
            opposite = "gpt" if family == "claude" else "claude"
            require(all(not FAMILIES[opposite].search(blob(path).decode("utf-8")) for path in own),
                    "Family response is not isolated")
            spec = {"batch": 130, "run": run, "family": family, "candidate": candidate, "session": session,
                    "acceptance": {"path": str(acceptance_path), "sha256": INITIAL_SHA[family]},
                    "revisedSources": [*revised, *own], "originalSources": originals,
                    "additionalSources": shared}
            spec_path = ROOT / "confirm" / (run + "-spec.json")
            freeze_json(spec_path, spec)
            build(spec_path)
            chain = json.loads(frozen(ROOT / "confirm" / (run + "-chain.json")))
            prepared.append({"run": run, "session": session, "segments": len(chain["segments"]),
                             "chainBytes": sum(row["bytes"] for row in chain["segments"])})
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Confirmation preparation RAM guard breached")
    print(json.dumps(freeze_json(ROOT / "confirmation-001-preparation.json", {
        "batch": 130, "candidate": candidate, "status": "PREPARED_NOT_ADMITTED",
        "proofSha256": PROOF_SHA, "runs": prepared, "sharedSources": shared,
        "revisedSharedSources": revised, "originalSources": originals, "presentations": presentations,
        "memory": memory, "reviewersLaunched": False, "producerSha256": sha(frozen(Path(__file__))),
        "isolation": "Only each recipient's original accepted report and own author response/mapping. "
                     "The other response, combined handoff/progress/inventory/producers and excluded reviews "
                     "are never claim evidence. All 24 historical questions remain in their owner's mapping. "
                     "No source refetch, semantic acceptance, publication or delivery credit.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: prepare_b130_confirmations.py CANDIDATE")
    main(sys.argv[1])
