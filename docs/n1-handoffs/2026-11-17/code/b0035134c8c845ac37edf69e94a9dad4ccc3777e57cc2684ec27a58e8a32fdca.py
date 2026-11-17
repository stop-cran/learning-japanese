"""Prepare isolated original-reviewer confirmations from verified signed evidence."""
import json
import re
import sys
from pathlib import Path

from common import freeze_json, frozen, json_bytes, load_batch, require, sha, start_guard, write_frozen
from confirm_b127 import build, clean
from b129_revision_pairs import EXTERNAL_SHA, JM_FILES, NOOSE_EXTERNAL_SHA, ORIGINAL
from verify_b129_revision_runtime import PARENT, PREFIX, REVIEW
from verify_b129_sources import Git

REVIEWERS = {
    "claude": ("6b850696-09e6-4774-b35a-09d67befffe6",
               "b2316f51a590da62c6216387985e2034b004602799cc12b74c1200a681e3d02f", "CLEAN"),
    "gpt": ("8d91db13-ecbb-4d48-8888-78c682edec78",
            "40ef4cd6a3f625705609538b25e2ca5f68ed57f4e21addaffb84c4ddfd3ebaa7", "NEEDS FIX"),
}
FAMILY = {"claude": re.compile(r"claude|anthropic|opus|sonnet|haiku", re.I),
          "gpt": re.compile(r"\bgpt|openai|codex", re.I)}
VERDICTS = re.compile(r"\bCLEAN\b|NEEDS FIX|\bCONFIRMED\b|\bUNVERIFIED\b")
TOOLING_SHA = "b97dafc9d1634c9dbe46271c74075c0d9e163e2e67eed48125ce8ed089ff1d22"
OUTPUT = REVIEW / "confirmation-001-neutral"


def neutral(raw):
    text = raw.decode("utf-8")
    return not any(pattern.search(text) for pattern in FAMILY.values()) and not VERDICTS.search(text)


def isolated(family, raw):
    text = raw.decode("utf-8")
    return {name for name, pattern in FAMILY.items() if pattern.search(text)} == {family}


def derivative(raw, label, before, after):
    text = raw.decode("utf-8")
    require(text.count(before) == 1 and after not in text, "Unexpected attribution to neutralize")
    value = json.loads(text.replace(before, after))
    value["confirmationDerivative"] = {
        "signedPath": PREFIX + label, "signedSha256": sha(raw),
        "change": "Removed one other-family name from the shape/lexical distinction; retained the "
                  "complete argument, disagreement, all pair decisions and source evidence.",
    }
    return json_bytes(value)


def neutral_pairs(raw):
    result = derivative(raw, "pair-dispositions.json",
                        "Preserve Claude's narrower shape-versus-lexical distinction.",
                        "Preserve the narrower shape-versus-lexical distinction.")
    require(neutral(result), "Shared pair table leaks review provenance")
    return result


def response(family, raw):
    if family == "gpt":
        raw = derivative(raw, "reviewer-response-gpt.json",
                         "Preserved Claude's lexical/shape distinction",
                         "Preserved the lexical/shape distinction")
    require(isolated(family, raw), f"Response is not isolated: {family}")
    return raw


def additional(path, source):
    return {"path": str(path), "sha256": sha(frozen(path)), "source": source}


def main(candidate, proof_sha):
    from verify_b129_revision_runtime import REPO, RUNNER
    config = load_batch(129)
    require(config["candidate"] == PARENT and not OUTPUT.exists(), "Wrong original snapshot or existing output")
    proof_path = REVIEW / "revision-evidence-proof-001" / "verification.json"
    proof = json.loads(frozen(proof_path, proof_sha))
    require(proof["status"] == "PASS_MECHANICAL_ONLY" and proof["candidate"] == candidate
            and proof["parent"] == PARENT and proof["pairProof"]["pairCount"] == 28
            and proof["pairProof"]["externalCaptureCount"] == 29
            and not proof["reviewAccepted"] and not proof["publicationAccepted"],
            "Signed correction has not passed mechanical admission")
    tooling = json.loads(frozen(REVIEW / "confirm" / "tooling-preflight.json", TOOLING_SHA))
    require(tooling["batch"] == 129 and tooling["exitCode"] == 0
            and tooling["status"] == "PASS_PREPARATION_ONLY", "Confirmation tooling is not ready")
    for row in tooling["derivations"]:
        frozen(row["output"]["path"], row["output"]["sha256"])
    for field in ("output", "helper"):
        row = tooling["engineDerivation"][field]
        frozen(row["path"], row["sha256"])
    guard, _ = start_guard("B129 original-reviewer confirmation preparation")
    git = Git(REPO, RUNNER, guard)
    try:
        clean(config, candidate)
        blob = lambda path: git("show", f"{candidate}:{path}")
        sys.path.insert(0, str(REPO.parent / "lean"))
        from n1lib import parse
        cards = set(config["members"])
        for character in config["members"]:
            metadata, _ = parse(blob(f"kanji/{character}.md").decode("utf-8").replace("\r\n", "\n"))
            cards.update(metadata["quiz_exclusions"])
            cards.update(metadata["distractors"])
        table_raw = blob(PREFIX + "pair-dispositions.json")
        cards.update(row["pair"][1] for row in json.loads(table_raw)["rows"])
        revised = [f"kanji/{character}.md" for character in sorted(cards)]
        revised += ["words/\u8309\u8389\u82b1.md", "words/\u7d79.md", "words/\u8679.md"]
        revised += [*JM_FILES, ORIGINAL + "kanjidic2-target-records.xml",
                    PREFIX + "kanjidic2-complete-records.xml"]
        revised += [PREFIX + name for name in (
            "jmdict-query-membership.json", "kanjidic2-query-membership.json",
            "supplement-query-membership.json", "complete-source-receipt.json",
            "supplement-source-receipt.json", "noose-source-receipt.json",
            "source-discrepancies-and-limits.json", "claim-source-readset.json",
        )]
        for path in revised:
            require(neutral(blob(path)), f"Review provenance in shared source: {path}")
        originals = [f"evidence/external-snapshots/{number:02d}-extract.txt" for number in range(1, 8)]
        originals.append("evidence/external-snapshots/manifest.json")
        summary = {key: proof[key] for key in (
            "batch", "candidate", "parent", "base", "signature", "runtimeEntries", "runtimeChanged",
            "manifestSha256", "contentVersion", "inventorySha256", "preservedInheritedFiles",
            "teachingInsertions", "absentComparison",
        )}
        summary.update(
            status="PASS_MECHANICAL_ONLY", proofSha256=proof_sha, semanticAcceptance=False,
            finitePairs=proof["pairProof"]["pairCount"], addedGuards=proof["pairProof"]["addedGuards"],
            noncollisionPairs=proof["pairProof"]["noncollisionPairs"], externalCaptures=29,
            completeRecordUnion=proof["pairProof"]["completeFamilyUnionCount"],
            limits="Signed runtime and contributor preservation, source membership and all ten serial "
                   "host gates passed. Author dispositions require independent semantic assessment. "
                   "Historical ambiguity, six latent reading collisions, one-additional-holder risks, "
                   "unread source images, native/device and arbitrary-pool limits remain.")
        require(neutral(json_bytes(summary)), "Shared verification summary leaks provenance")
        shared = []
        for name, data, source in (
            ("verification.json", json_bytes(summary), "verification/signed-correction-summary.json"),
            ("pair-dispositions.json", neutral_pairs(table_raw), "evidence/reconciliation/pair-dispositions.json"),
        ):
            path = OUTPUT / name
            write_frozen(path, data)
            shared.append(additional(path, source))
        external = json.loads(frozen(REVIEW / "reconciliation-external-001" / "manifest.json", EXTERNAL_SHA))
        extra = json.loads(frozen(REVIEW / "reconciliation-noose-external-001" / "manifest.json",
                                  NOOSE_EXTERNAL_SHA))
        for index, capture in enumerate([*external["captures"], extra], 1):
            binding = capture["outputs"]["complete-extract.txt"]
            require(neutral(frozen(binding["path"], binding["sha256"])), "External extract leaks provenance")
            shared.append(additional(Path(binding["path"]), f"external-reconciliation/{index:02d}-complete.txt"))
        committed = proof["gateSets"]["committed"]
        gate_files = ["summary.json", *[row["gate"] + ".log" for row in committed["gates"]]]
        for name in gate_files:
            captured = proof["capturedEvidence"]["committed-gates/" + name]
            require(neutral(frozen(captured["path"], captured["sha256"])), "Gate output leaks provenance")
            shared.append(additional(Path(captured["path"]), "committed-checks/" + name))
        prepared = []
        for family, (session, acceptance_sha, verdict) in REVIEWERS.items():
            initial = f"N1-B129-{family.upper()}-001"
            run = f"N1-B129-{family.upper()}-CONFIRM-001"
            acceptance_path = REVIEW / f"{initial}-acceptance.json"
            accepted = json.loads(frozen(acceptance_path, acceptance_sha))
            launch = json.loads(frozen(REVIEW / f"{initial}-launch.json"))
            require(accepted["candidate"] == PARENT and accepted["reviewAccepted"] is True
                    and accepted["verdict"] == verdict and launch["session"] == session,
                    "Original reviewer identity or accepted verdict differs")
            frozen(accepted["report"]["path"], accepted["report"]["sha256"])
            response_path = OUTPUT / f"response-{family}.json"
            write_frozen(response_path, response(family, blob(PREFIX + f"reviewer-response-{family}.json")))
            spec = {
                "batch": 129, "run": run, "family": family, "candidate": candidate, "session": session,
                "acceptance": {"path": str(acceptance_path), "sha256": acceptance_sha},
                "revisedSources": revised, "originalSources": originals,
                "additionalSources": [additional(response_path, "author-response/current.json"), *shared],
            }
            spec_path = REVIEW / "confirm" / f"{run}-spec.json"
            freeze_json(spec_path, spec)
            build(spec_path)
            prepared.append(run)
            guard.check()
        clean(config, candidate)
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Confirmation preparation RAM guard breached")
    print(json.dumps(freeze_json(REVIEW / "confirmation-001-preparation.json", {
        "batch": 129, "candidate": candidate, "proofSha256": proof_sha, "runsPrepared": prepared,
        "revisedSources": revised, "originalSources": originals, "sharedSources": shared,
        "memory": memory, "reviewersLaunched": False, "producerSha256": sha(Path(__file__).read_bytes()),
        "isolation": "Each chain has only its owning family's original report and response. The exact "
                     "signed originals are preserved; explicit derivatives remove one other-family "
                     "name, never a disposition, disagreement, source or uncertainty.",
        "limits": "Preparation only. No semantic confirmation, publication or delivery credit.",
    })))


if __name__ == "__main__":
    require(len(sys.argv) == 3, "Usage: prepare_b129_confirmations.py CANDIDATE PROOF_SHA")
    main(*sys.argv[1:])
