"""Freeze separate same-reviewer confirmation specs from the signed correction."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_batch, require, sha
from confirm_v2 import clean


def prepare(candidate, proof_path):
    config = load_batch(118)
    clean(config, candidate)
    proof = json.loads(frozen(proof_path))
    require(proof["candidate"] == candidate and proof["status"] == "PASS", "Revision proof mismatch")
    records = WS / "scratch-118" / "review"
    reconciliation = records / "reconciliation-001"
    gates = WS / "scratch-118" / "author-gates-reconciliation-001"
    source = lambda path, label: {"path": str(path), "sha256": sha(frozen(path)), "source": label}
    common = [
        source(reconciliation / name, f"scratch-118/review/reconciliation-001/{name}")
        for name in ("pair-dispositions.json", "source-extraction.json", "changed-file-inventory.json")
    ]
    common += [
        source(path, f"scratch-118/review/reconciliation-001/comparison-cards/{path.name}")
        for path in sorted((reconciliation / "comparison-cards").glob("*.md"))
    ]
    sections = WS / "scratch-118" / "neutral-source-sections-001"
    common += [source(path, f"scratch-118/neutral-source-sections-001/{path.name}")
               for path in sorted(sections.iterdir()) if path.is_file()]
    common += [source(proof_path, "coordinator/revision-verification.json")]
    for item in proof["gates"]:
        name = f"{item['gate']}.log"
        common.append(source(gates / name, f"gates/{name}"))
    require(len(common) == len({entry["source"] for entry in common}), "Duplicate selected source")
    for family, initial_number, session in (
        ("claude", "002", "fcb92754-e5d2-42a6-b2ba-d42c6ef2d1dc"),
        ("gpt", "001", "25ca142b-ae23-4c30-a774-70432ab9acb9"),
    ):
        initial = f"N1-B118-{family.upper()}-{initial_number}"
        run = f"{initial}-CONFIRM-001"
        acceptance_path = records / f"{initial}-acceptance.json"
        acceptance = json.loads(frozen(acceptance_path))
        require(acceptance["reviewAccepted"] and acceptance["run"] == initial,
                "Initial review not accepted")
        response = f"author-response-{family}-{initial_number}.md"
        spec = {
            "batch": 118, "candidate": candidate, "run": run, "family": family, "session": session,
            "acceptance": {"path": str(acceptance_path), "sha256": sha(frozen(acceptance_path))},
            "revisedSources": ["kanji/析.md", "words/分析.md",
                               "docs/n1-sources/batch-118/reconciliation-001/kanjidic2-records.xml"],
            "originalSources": ["repo/docs/content-format.md", "evidence/kanjidic2-records.xml",
                                "evidence/jmdict-families.xml", "evidence/external-snapshots/01-extract.txt"],
            "additionalSources": [
                source(reconciliation / response, f"scratch-118/review/reconciliation-001/{response}"),
                *common,
            ],
        }
        print(json.dumps(freeze_json(records / "confirm" / f"{run}-spec.json", spec)))


if __name__ == "__main__":
    prepare(sys.argv[1], Path(sys.argv[2]))
