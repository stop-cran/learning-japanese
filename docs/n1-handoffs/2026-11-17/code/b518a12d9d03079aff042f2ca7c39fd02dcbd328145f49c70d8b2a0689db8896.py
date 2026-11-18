"""Prepare isolated same-reviewer dossiers from B121's verified signed revision."""
import json
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha
from confirm_v2 import binding, build, clean
from verify_b121_revision_v2 import CARD

CANDIDATE = "b7369b9502f7f5c14a4f2081fe9e6a0e2b276e42"
PREFIX = "docs/n1-sources/batch-121/reconciliation-001/"
REVIEW = WS / "scratch-121" / "review"
GATES = WS / "scratch-121" / "reconciliation-committed-gates-001"
REVIEWERS = (
    ("claude", "N1-B121-CLAUDE-002", "d8f38620-f2e5-4071-bff7-6a66dfeb6cbe"),
    ("gpt", "N1-B121-GPT-001", "833a5222-0567-4746-92b9-d275f5c72342"),
)


def main():
    config = load_batch(121)
    clean(config, CANDIDATE)
    proof_path = REVIEW / "coordinator-revision-verification-001.json"
    proof = json.loads(frozen(proof_path, "a7b2aa81f1451024846b45dbb38d45efff6b8de3fc10d020b740e407a710deca"))
    require(proof["status"] == "PASS" and proof["candidate"] == CANDIDATE
            and not proof["linguisticAcceptance"] and not proof["publicationAccepted"],
            "Missing exact revision verification")
    source_bindings_raw = git(config, "show", f"{CANDIDATE}:{PREFIX}source-bindings.json")
    source_bindings = json.loads(source_bindings_raw)
    require(sha(source_bindings_raw) == "59ddeccfbcf45528a94b657b511f2a93b0ecd90f10bebff1b6d2fd0e2ad803d9",
            "Author source binding changed")
    for name, item in source_bindings["files"].items():
        raw = git(config, "show", f"{CANDIDATE}:{PREFIX}{name}")
        require(len(raw) == item["bytes"] and sha(raw) == item["sha256"], f"Source binding differs: {name}")
    inventory_raw = git(config, "show", f"{CANDIDATE}:{PREFIX}changed-file-inventory.json")
    require(sha(inventory_raw) == "337dd23cdb7662f365479f2be379e19d580c3cd9a8fff4401f869c8ec9605ea7",
            "Author inventory changed")
    inventory = json.loads(inventory_raw)
    for start, fields in (
        (config["base"], ("runtime", "contributor")),
        (config["candidate"], ("parentToCandidateRuntime", "parentToCandidateContributor")),
    ):
        actual = git(config, "diff", "--name-only", "-z", start, CANDIDATE).decode("utf-8").strip("\0").split("\0")
        require(sorted(actual) == sorted(path for field in fields for path in inventory[field]),
                "Exact changed-file inventory differs")
    from n1lib import parse
    metadata, _ = parse(git(config, "show", f"{CANDIDATE}:{CARD}").decode("utf-8").replace("\r\n", "\n"))
    counterparts = sorted(set(metadata["distractors"] + metadata["quiz_exclusions"]))
    revised = [CARD, "words/\u9053\u5fb3.md", *(f"kanji/{char}.md" for char in counterparts)]
    revised += [PREFIX + name for name in (
        "disposition.md", "changed-file-inventory.json", "source-bindings.json",
        "jmdict-records.xml", "kanjidic2-records.xml",
        "starter-jmdict-records.xml", "starter-kanjidic2-records.xml",
        "roads-jmdict-records.xml", "roads-kanjidic2-records.xml",
    )]
    original = [
        "rubric/content-structure.instructions.md",
        "evidence/provenance.json", "evidence/shape-evidence.json", "evidence/joyo-rows.json",
        "evidence/external-snapshots/01-extract.txt",
        "evidence/kanjidic2-records.xml", "evidence/jmdict-families.xml",
    ]
    additional = [
        {**binding(proof_path), "source": "coordinator/revision-verification-001.json"},
    ]
    for name in [*(f"{check}.log" for check in CHECKS), "summary.json"]:
        additional.append({**binding(GATES / name), "source": f"gates-committed-revision/{name}"})
    for family, initial, session in REVIEWERS:
        run = initial + "-CONFIRM-001"
        spec = {
            "batch": 121, "candidate": CANDIDATE, "run": run, "family": family, "session": session,
            "basis": "initial", "acceptance": binding(REVIEW / f"{initial}-acceptance.json"),
            "revisedSources": [*revised, PREFIX + f"author-response-{family}.md"],
            "originalSources": original, "additionalSources": additional,
        }
        forbidden = (f"author-response-{'gpt' if family == 'claude' else 'claude'}.md",
                     "held-initial-disposition.md")
        require(not any(name in path for name in forbidden for path in spec["revisedSources"]),
                "Other-reviewer or held observations in dossier")
        spec_path = REVIEW / "confirm" / f"{run}-spec.json"
        freeze_json(spec_path, spec)
        build(spec_path)
    freeze_json(REVIEW / "confirmation-preparation-001.json", {
        "candidate": CANDIDATE, "sourceBindingSha256": sha(source_bindings_raw),
        "inventorySha256": sha(inventory_raw), "sourceBindingsAndInventoryVerified": True,
        "counterparts": counterparts, "originalReportsUnchanged": True,
        "reviewers": [{"family": family, "run": initial + "-CONFIRM-001", "session": session}
                      for family, initial, session in REVIEWERS],
        "isolation": "Only the matching original report and author response. Shared source dispositions, "
                     "actual cards and complete selected records; no other report or held observations.",
        "preparedOnly": True, "publicationAccepted": False,
    })


if __name__ == "__main__":
    main()
