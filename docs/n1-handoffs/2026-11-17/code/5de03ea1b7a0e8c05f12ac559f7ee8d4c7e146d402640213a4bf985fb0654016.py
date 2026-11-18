"""Prepare isolated original-reviewer confirmations for the verified B123 revision."""
import json
import re
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha
from confirm_v2 import build, clean

CANDIDATE = "047970a055903c0337d73823288695938648dd1d"
REVIEW = WS / "scratch-123" / "review"
PREFIX = "docs/n1-sources/batch-123/"
REVIEWERS = {
    "claude": ("44df27a1-5cbd-4398-b3ed-499809381a33",
               "769bfa775266f4a8e35a13594deddd6f684821f616db70639057d35d0c2aee1a",
               "06258f394a124d7b1801e035585ba243d5c5ec2f77703c47ab1e0e12e1d568ee"),
    "gpt": ("fbf6d07e-124a-4cf8-b339-5060f515e0b9",
            "7d0c8131fe458bbcbf10fb8f5558c5be1d14859892a57bf8425c181d94315408",
            "9bffe08c6d746e46dbf38737c0ce29aaa57c8cbe8b32dfc9c246d34576c8f34f"),
}
PROOFS = {
    "coordinator-reconciliation-verification-001.json":
        "7bd65759c91939c536dfb03a00ff461fcbc30a0f293b5ddb78d7fb0f404f3f20",
    "coordinator-reconciliation-selection-001.json":
        "25de95031769bf33c53ffe8c9f3a0c9b05d2d0198c90f455797ab611c2b9f742",
    "coordinator-reconciliation-verification-002.json":
        "c7a9b6721556e4db4d7619d4f677a75957c834c6ce31cc03d40b8ce86ea11713",
    "coordinator-reconciliation-selection-002.json":
        "e6242f59ed47fed5a58a5af2a1260616cea3bdc158fb2f3a84776ae29bf9ae43",
}


def additional(path, source, digest=None):
    raw = frozen(path, digest)
    return {"path": str(path), "sha256": sha(raw), "source": source}


def main():
    config = load_batch(123)
    clean(config, CANDIDATE)
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse
    blob = lambda path: git(config, "show", f"{CANDIDATE}:{path}")
    card, _ = parse(blob("kanji/\u7bc4.md").decode("utf-8").replace("\r\n", "\n"))
    pair = json.loads(blob(PREFIX + "reconciliation-002/pair-disposition.json"))
    require(pair["pair"] == ["\u7bc4", "\u666e"] and pair["decision"] == "guard"
            and pair["declarationEndpoint"] == "\u7bc4"
            and card["quiz_exclusions"][-1] == "\u666e", "Focused pair is not resolved")
    neutral = json.loads(blob(PREFIX + "reconciliation-001/pair-dispositions.json"))
    remaining = [row["pair"][1] for row in neutral["pairs"] if row["decision"] == "no-new-guard"]
    require(set(remaining) == set("\u672c\u50cf\u56f2\u65b9\u5ea6\u8a08\u6e2c\u91cf\u7406"),
            "Residual disposition scope changed")
    shared = [additional(REVIEW / name, f"verification/{name}", digest)
              for name, digest in PROOFS.items()]
    for item in shared:
        require(json.loads(frozen(item["path"]))["status"] == "PASS", "Verification held")
    names = git(config, "ls-tree", "-r", "--name-only", CANDIDATE, "--", PREFIX).decode().splitlines()
    supplement = [p for p in names if p.startswith(PREFIX + "reconciliation-")]
    require(len(supplement) == 36, "Unexpected additive packet inventory")
    revised = ["kanji/\u7bc4.md", "words/\u7bc4\u56f2.md", *supplement]
    revised += [PREFIX + name for name in (
        "jmdict-comparison-records.xml", "jmdict-selected-records.xml",
        "kanjidic2-comparison-records.xml", "kanjidic2-selected-records.xml")]
    copied = {Path(p).stem for p in supplement if "/comparison-cards/" in p}
    copied.add("\u666e")
    counterparts = set(card["quiz_exclusions"]) | set(card["distractors"]) | set(remaining)
    original = [f"repo/kanji/{character}.md" for character in sorted(counterparts - copied)]
    original += ["evidence/external-snapshots/01-extract.txt",
                 "evidence/external-snapshots/manifest.json",
                 "evidence/source-metadata.json", "evidence/shape-evidence.json"]
    captures_path = REVIEW / "reconciliation-source-captures-001" / "provenance.json"
    captures = json.loads(frozen(captures_path,
                                "85e90221700ae4efbe43b37b12cd8bb290ceeff4a68c35ad04e7b07365f62500"))
    shared.append(additional(captures_path, "external-sources/tool-return-provenance.json"))
    for item in captures["sources"]:
        shared.append(additional(Path(item["content"]["path"]), item["sourceLabel"],
                                 item["content"]["sha256"]))
    extracts_path = REVIEW / "reconciliation-character-extracts-001" / "provenance.json"
    extracts = json.loads(frozen(extracts_path,
                                "be42f106ab062c1952e5e1cb588637c3dcc1422d8553c5c14deb30f11a97cf84"))
    shared.append(additional(extracts_path, "external-sources/retained-section-provenance.json"))
    for item in extracts["sources"]:
        output = item["output"]
        shared.append(additional(Path(output["path"]), "external-sources/" +
                                 Path(output["path"]).name, output["sha256"]))
    gates = WS / "scratch-123" / "reconciliation-002" / "committed-gates-001"
    for name in [*(f"{gate}.log" for gate in CHECKS), "summary.json"]:
        shared.append(additional(gates / name, f"committed-checks/{name}"))
    for path in revised:
        require(not re.search(r"claude|gpt|NEEDS FIX|CONFIRMED", blob(path).decode("utf-8"), re.I),
                f"Reviewer-specific material in shared source: {path}")
    for item in shared:
        require(not re.search(r"author-response-|initial-claude|initial-gpt",
                              frozen(item["path"]).decode("utf-8"), re.I),
                f"Cross-review binding in shared material: {item['path']}")
    specs = []
    for family, (session, acceptance_sha, response_sha) in REVIEWERS.items():
        run = f"N1-B123-{family.upper()}-CONFIRM-001"
        acceptance = REVIEW / f"N1-B123-{family.upper()}-001-acceptance.json"
        frozen(acceptance, acceptance_sha)
        response = WS / "scratch-123" / "reconciliation-002" / f"author-response-{family}-002.md"
        spec = {"batch": 123, "run": run, "family": family, "candidate": CANDIDATE,
                "session": session, "acceptance": {"path": str(acceptance), "sha256": acceptance_sha},
                "revisedSources": revised, "originalSources": original,
                "additionalSources": [
                    additional(response, "author-response/current.md", response_sha), *shared]}
        specs.append((REVIEW / "confirm" / f"{run}-spec.json", spec))
    print(json.dumps(freeze_json(REVIEW / "reconciliation-002-source-adjudication.json", {
        "batch": 123, "candidate": CANDIDATE, "status": "READY_FOR_INDEPENDENT_CONFIRMATIONS",
        "resolvedCoordinatorFinding": {
            "id": "C1", "pair": pair["pair"],
            "basis": "Direct pair now declared on the scoped card. The unchanged complete Daijisen "
                     "character entry attests the widespread branch; actual comparison title and "
                     "complete KANJIDIC2 record support the overlap. JMdict kana/rare-form "
                     "restrictions are retained. No universal/model equivalence is asserted.",
        },
        "remainingNoNewGuardPairs": remaining,
        "limits": "These remain bounded, source-based hypotheses for both independent reviewers. "
                  "This is not confirmation acceptance, whole-set/native or publication acceptance.",
        "sourceIsolation": "Only each reviewer's own report and current response; shared sources "
                           "contain no report, acceptance, adjudication or response inventory.",
    })))
    for path, spec in specs:
        print(json.dumps(freeze_json(path, spec)))
        build(path)


if __name__ == "__main__":
    main()
