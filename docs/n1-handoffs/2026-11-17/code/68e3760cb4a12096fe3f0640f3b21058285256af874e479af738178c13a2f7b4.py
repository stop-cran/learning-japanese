"""Prepare isolated same-reviewer dossiers for the two-commit B119 correction."""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_batch, require, sha, write_frozen
from confirm_v2 import clean
from verify_b119_revision import INTERMEDIATE, SUPPORT


def prepare(candidate, proof_path, gates):
    config = load_batch(119)
    clean(config, candidate)
    proof = json.loads(frozen(proof_path))
    require(proof["candidate"] == candidate and proof["status"] == "PASS"
            and proof["prior"] == INTERMEDIATE, "Revision proof mismatch")
    records = WS / "scratch-119" / "review"
    supplement_path = records / "revision-supplement-verification-002.json"
    supplement = json.loads(frozen(supplement_path))
    require(supplement["candidate"] == candidate and supplement["status"] == "PASS",
            "Supplementary verification mismatch")
    handoff = records / "reconciliation-002"
    old_handoff = records / "reconciliation-001"
    out = records / "confirm"
    source = lambda path, label: {"path": str(path), "sha256": sha(frozen(path)), "source": label}
    label = lambda path: "scratch-119/" + path.relative_to(WS / "scratch-119").as_posix()
    common = [source(handoff / name, label(handoff / name)) for name in (
        "source-extraction.json", "pair-dispositions.json", "changed-file-inventory.json",
        "source-index-rows.json")]
    common += [source(path, label(path)) for path in sorted((handoff / "comparison-cards").glob("*.md"))]
    extraction = json.loads(frozen(handoff / "source-extraction.json"))
    require({Path(item["path"]).stem for item in common if "/comparison-cards/" in item["source"]}
            == set(extraction["comparisonCardSha256"]), "Comparison dossier is incomplete")
    membership = handoff / "n1-kanji-source-20261102.json"
    raw = frozen(membership, extraction["community"]["sha256"])
    display = out / "source-display-001" / "n1-kanji-source-20261102.json.txt"
    displayed = raw if raw.endswith(b"\n") else raw + b"\n"
    display_binding = write_frozen(display, displayed)
    derivation = out / "source-display-001" / "derivation.json"
    freeze_json(derivation, {
        "original": source(membership, label(membership)), "display": display_binding,
        "operation": "Preserve bytes; append one LF only if absent for the line-based chain.",
        "appendedLF": displayed != raw, "reverseExact": displayed[:len(raw)] == raw,
        "originalModified": False,
    })
    common += [source(display, "source-display-001/n1-kanji-source-20261102.json.txt"),
               source(derivation, "source-display-001/derivation.json"),
               source(old_handoff / "font-audit.json", label(old_handoff / "font-audit.json")),
               source(supplement_path, "coordinator/revision-supplement-verification-002.json"),
               source(proof_path, "coordinator/revision-verification-002.json")]
    for item in proof["gates"]:
        name = f"{item['gate']}.log"
        require(sha(frozen(gates / name)) == item["logSha256"], "Gate log differs from revision proof")
        common.append(source(gates / name, f"gates-reconciliation-002/{name}"))
    require(len(common) == len({item["source"] for item in common}), "Duplicate neutral source")
    for family, session in (
        ("claude", "eacaa258-4687-4272-aea1-ed8a32bc18cc"),
        ("gpt", "4f722d54-37d8-4727-9e14-9c05283a2913"),
    ):
        initial = f"N1-B119-{family.upper()}-001"
        acceptance_path = records / f"{initial}-acceptance.json"
        acceptance = json.loads(frozen(acceptance_path))
        require(acceptance["reviewAccepted"] and acceptance["run"] == initial,
                "Initial evidence not accepted")
        response_name = f"author-response-{family}-001.md"
        own = [source(directory / response_name, label(directory / response_name))
               for directory in (old_handoff, handoff)]
        run = f"{initial}-CONFIRM-001"
        spec = {
            "batch": 119, "candidate": candidate, "run": run, "family": family, "session": session,
            "acceptance": {"path": str(acceptance_path), "sha256": sha(frozen(acceptance_path))},
            "revisedSources": [
                *(f"kanji/{c}.md" for c in SUPPORT), *(f"words/{w}.md" for w in SUPPORT.values()),
                "docs/n1-sources/batch-119/reconciliation-002/kanjidic2-records.xml",
                "docs/n1-sources/batch-119/reconciliation-002/jmdict-records.xml",
                "docs/n1-sources/batch-119/reconciliation-002/jmdict-recurrence-records.xml",
            ],
            "originalSources": [
                "rubric/content-structure.instructions.md", "repo/docs/content-format.md",
                "repo/docs/jlpt-levels.md", "evidence/provenance.json", "evidence/shape-evidence.json",
                "evidence/joyo-rows.json", "evidence/external-snapshots/01-extract.txt",
                "evidence/external-snapshots/02-extract.txt",
            ],
            "additionalSources": [*own, *common],
        }
        print(json.dumps(freeze_json(out / f"{run}-spec.json", spec)))


if __name__ == "__main__":
    prepare(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
