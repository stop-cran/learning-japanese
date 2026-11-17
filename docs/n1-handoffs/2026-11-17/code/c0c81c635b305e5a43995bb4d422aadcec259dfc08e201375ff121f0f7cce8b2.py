"""Prepare B118 CONFIRM-003 follow-up specs for the reconciliation-002 descendant.

Earlier preparers stay unchanged. Exact HTML section slices keep their bytes; line-based review
copies append one LF under source-display-003 with reversible provenance.
"""
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, load_batch, require, sha, write_frozen
from confirm_v2 import clean

REVIEWED = ["研", "断", "絶", "折", "究", "査", "調", "察", "考", "討", "論", "批"]
REPO = "docs/n1-sources/batch-118/reconciliation-002/"
FAMILIES = (
    ("claude", "N1-B118-CLAUDE-002", "fcb92754-e5d2-42a6-b2ba-d42c6ef2d1dc",
     "992bcd8a552a7e5f9d735b03b8566457a19aa6e2d3f4cfafe7fecfb509f51077",
     {"basis": "accepted-confirmation", "priorVerdict": "CONFIRMED", "openClaimIds": []}),
    ("gpt", "N1-B118-GPT-001", "25ca142b-ae23-4c30-a774-70432ab9acb9",
     "eb980ecf310bf2c87bca39dfc33e6d3e06e294be824bfa786e2978fd5c8982cd",
     {"basis": "confirmation", "priorVerdict": "NEEDS FIX", "openClaimIds": ["F1", "L2"]}),
)


def prepare(candidate, proof_path):
    config = load_batch(118)
    clean(config, candidate)
    proof = json.loads(frozen(proof_path))
    require(proof["candidate"] == candidate and proof["status"] == "PASS"
            and proof["prior"] == "fa2f64f2472cf9ef10b8ac5f48db14dcaa248cd2", "Revision proof mismatch")
    records = WS / "scratch-118" / "review"
    handoff = records / "reconciliation-002"
    gates = WS / "scratch-118" / "author-gates-reconciliation-002"
    displays = records / "confirm" / "source-display-003"
    source = lambda path, label: {"path": str(path), "sha256": sha(frozen(path)), "source": label}
    label = lambda path: "scratch-118/" + path.relative_to(WS / "scratch-118").as_posix()
    common = [source(handoff / name, label(handoff / name)) for name in (
        "author-response-gpt-001-confirm-002.md", "changed-file-inventory.json", "target-source-receipt.json")]
    common += [source(handoff / "comparison-cards" / f"{c}.md", label(handoff / "comparison-cards" / f"{c}.md"))
               for c in ["析", *REVIEWED]]
    derivatives = []
    for name in ["析-daijisen", *REVIEWED]:
        html = handoff / "sections" / f"{name}.html"
        raw = frozen(html)
        require(not raw.endswith(b"\n"), f"Unexpected terminal LF: {html}")
        derived = displays / f"{name}.html.txt"
        output = write_frozen(derived, raw + b"\n")
        require(frozen(derived)[:-1] == raw, "Display normalization is not reversible")
        common.append(source(derived, f"source-display-003/{name}.html.txt"))
        derivatives.append({"original": {"path": str(html), "source": label(html), "sha256": sha(raw)},
                            "display": output, "operation": "Append one LF for the line-based review chain.",
                            "reverseExact": True, "originalModified": False})
        text = handoff / "sections" / f"{name}.txt"
        common.append(source(text, label(text)))
    provenance = displays / "derivation.json"
    freeze_json(provenance, {"derivatives": derivatives,
                             "reason": "Exact HTML slices lack a terminal newline. No content changes. "
                                       "The exact slices remain authoritative; .txt files are author "
                                       "markup-stripped derivatives."})
    common.append(source(provenance, "source-display-003/derivation.json"))
    common.append(source(proof_path, "coordinator/revision-verification-002.json"))
    for item in proof["gates"]:
        name = f"{item['gate']}.log"
        common.append(source(gates / name, f"gates-reconciliation-002/{name}"))
    for family, initial, session, prior_sha, basis in FAMILIES:
        prior_path = records / "confirm" / f"{initial}-CONFIRM-002-acceptance.json"
        prior = json.loads(frozen(prior_path, prior_sha))
        require(prior["candidate"] == proof["prior"] and prior["session"] == session, "Prior binding differs")
        acceptance_path = records / f"{initial}-acceptance.json"
        own = []
        if family == "gpt":
            adjudication = records / "confirm" / f"{initial}-CONFIRM-002-adjudication.json"
            own.append(source(adjudication, f"coordinator/{adjudication.name}"))
        additional = [*own, *common]
        require(len(additional) == len({entry["source"] for entry in additional}), "Duplicate selected source")
        run = f"{initial}-CONFIRM-003"
        spec = {
            "batch": 118, "candidate": candidate, "run": run, "family": family, "session": session,
            "acceptance": {"path": str(acceptance_path), "sha256": sha(frozen(acceptance_path))},
            "prior": {"path": str(prior_path), "sha256": prior_sha}, **basis,
            "revisedSources": ["kanji/析.md", "words/分析.md", REPO + "README.md",
                               REPO + "pair-dispositions.json", REPO + "source-receipt.json",
                               "docs/n1-sources/batch-118/reconciliation-001/kanjidic2-records.xml"],
            "originalSources": ["repo/docs/content-format.md", "evidence/kanjidic2-records.xml",
                                "evidence/jmdict-families.xml", "evidence/external-snapshots/01-extract.txt"],
            "additionalSources": additional,
        }
        print(json.dumps(freeze_json(records / "confirm" / f"{run}-spec.json", spec)))


if __name__ == "__main__":
    prepare(sys.argv[1], Path(sys.argv[2]))
