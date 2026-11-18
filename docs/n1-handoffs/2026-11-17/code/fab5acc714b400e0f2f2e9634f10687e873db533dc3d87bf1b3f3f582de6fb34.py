"""Prepare minimal, isolated original-reviewer follow-ups for the direct 丸 pair."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, write_frozen
from confirm_v2 import binding, clean
from verify_b119_followup import PRIOR


def prepare(candidate):
    config = load_batch(119)
    clean(config, candidate)
    records = WS / "scratch-119" / "review"
    handoff, out = records / "reconciliation-003", records / "confirm"
    proof_path = records / "revision-verification-003.json"
    proof = json.loads(frozen(proof_path))
    source_proof_path = records / "revision-source-verification-003.json"
    source_proof = json.loads(frozen(source_proof_path))
    require(proof["candidate"] == source_proof["candidate"] == candidate
            and proof["status"] == source_proof["status"] == "PASS" and proof["prior"] == PRIOR,
            "Follow-up verification mismatch")
    selected_dir = out / "followup-source-display-001"
    selected_dir.mkdir(exist_ok=False)
    derivatives = []
    for name, tag, key, wanted in (
        ("jmdict-records.xml", "entry", "ent_seq", {"1604230"}),
        ("kanjidic2-records.xml", "character", "literal", {"妥", "丸", "円"}),
    ):
        path = f"docs/n1-sources/batch-119/reconciliation-002/{name}"
        raw = git(config, "show", f"{candidate}:{path}")
        pattern = f"<{tag}>.*?</{tag}>".encode()
        selected = [(ET.fromstring(item).findtext(key), item)
                    for item in re.findall(pattern, raw, re.S)
                    if ET.fromstring(item).findtext(key) in wanted]
        require(len(selected) == len(wanted) and {k for k, _ in selected} == wanted,
                "Complete selected source records missing")
        wrapper = "JMdict" if tag == "entry" else "kanjidic2"
        display = (f"<{wrapper}>\n".encode() + b"\n".join(item for _, item in selected)
                   + f"\n</{wrapper}>\n".encode())
        saved = write_frozen(selected_dir / name, display)
        derivatives.append({
            "sourcePath": path, "sourceSha256": sha(raw), "snapshot": candidate,
            "display": saved, "method": "Byte-exact complete XML element slices in a new root wrapper.",
            "records": {key: sha(item) for key, item in selected},
        })
    require(derivatives[0]["records"]["1604230"] == source_proof["completeEntrySha256"],
            "Displayed entry differs from the verified complete element")
    freeze_json(selected_dir / "derivation.json", derivatives)
    source = lambda path, label: {**binding(path), "source": label}
    common = [source(path, f"followup-source-display-001/{path.name}")
              for path in sorted(selected_dir.iterdir())]
    common += [source(proof_path, "coordinator/revision-verification-003.json"),
               source(source_proof_path, "coordinator/revision-source-verification-003.json")]
    gates = WS / "scratch-119" / "reconciliation-gates-003"
    for item in proof["gates"]:
        path = gates / f"{item['gate']}.log"
        require(sha(frozen(path)) == item["logSha256"], "Gate log changed")
        common.append(source(path, f"gates-reconciliation-003/{path.name}"))
    for family, session in (("claude", "eacaa258-4687-4272-aea1-ed8a32bc18cc"),
                            ("gpt", "4f722d54-37d8-4727-9e14-9c05283a2913")):
        initial = f"N1-B119-{family.upper()}-001"
        prior = out / f"{initial}-CONFIRM-001-acceptance.json"
        own = handoff / f"author-response-{family}-001.md"
        spec = {
            "batch": 119, "candidate": candidate, "run": f"{initial}-CONFIRM-002",
            "family": family, "session": session,
            "basis": "accepted-confirmation" if family == "claude" else "confirmation",
            "priorVerdict": "CONFIRMED" if family == "claude" else "NEEDS FIX",
            "openClaimIds": [] if family == "claude" else ["F1"],
            "acceptance": binding(records / f"{initial}-acceptance.json"), "prior": binding(prior),
            "revisedSources": [
                "kanji/妥.md", "kanji/循.md", "kanji/丸.md", "kanji/円.md",
                "docs/n1-sources/batch-119/reconciliation-003/source-bindings.json",
                "docs/n1-sources/batch-119/reconciliation-003/pair-dispositions.json",
            ],
            "originalSources": ["evidence/external-snapshots/01-extract.txt"],
            "additionalSources": [
                source(own, f"scratch-119/review/reconciliation-003/{own.name}"), *common,
            ],
        }
        print(json.dumps(freeze_json(out / f"{initial}-CONFIRM-002-spec.json", spec)))


if __name__ == "__main__":
    prepare(sys.argv[1])
