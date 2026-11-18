"""Prepare isolated confirmations of the verified B120 pushing-character correction."""
import copy
import json
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha
from confirm_v2 import binding, clean

CANDIDATE = "356375e1d340573dc76e4f61826dfb9af9640bdd"
REVIEW = WS / "scratch-120" / "review"
HERE = REVIEW / "confirm"
SOURCE = "docs/n1-sources/batch-120/reconciliation-002/"


def prepare():
    config = load_batch(120)
    clean(config, CANDIDATE)
    proof_path = REVIEW / "correction-verification-002.json"
    proof = json.loads(frozen(proof_path, "88a542059a06883178567265c6cc20c1504ce1e9edce1163395e5a29e982c87c"))
    require(proof["candidate"] == CANDIDATE and proof["status"] == "PASS" and not proof["memory"]["breach"],
            "Correction is not verified")
    selected = HERE / "correction-002-neutral"
    selected.mkdir(exist_ok=False)
    erratum = {
        **proof["sourceSummaryErratum"], "candidate": CANDIDATE,
        "sourceSummarySha256": proof["newEvidenceSha256"][SOURCE + "pair-dispositions.md"],
        "completeXml": {"path": SOURCE + "jmdict-records.xml",
                        "sha256": proof["newEvidenceSha256"][SOURCE + "jmdict-records.xml"]},
        "preservation": "The signed source summary and complete XML remain unchanged. "
                        "This explicit correction is to be preserved with the closure.",
    }
    freeze_json(selected / "source-summary-erratum.json", erratum)
    neutral = {key: proof[key] for key in (
        "status", "batch", "candidate", "prior", "base", "manifestSha256", "contentVersion",
        "runtimeEntries", "boundedDelta", "completeSourceCopies", "gates", "summary", "gateRunner",
        "signature", "scope", "memory")}
    neutral["sourceProofSha256"] = sha(frozen(proof_path))
    freeze_json(selected / "revision-verification.json", neutral)
    shared = [
        {**binding(path), "source": f"coordinator/correction-002/{path.name}"}
        for path in sorted(selected.iterdir())
    ]
    gates = WS / "scratch-120" / "author-gates-002"
    gate_sources = [
        {**binding(gates / f"{item['gate']}.log"), "source": f"gates-correction-002/{item['gate']}.log"}
        for item in proof["gates"]
    ]
    gate_sources.append({**binding(gates / "summary.json"), "source": "gates-correction-002/summary.json"})
    new_sources = [
        "kanji/\u62bc.md",
        *[SOURCE + name for name in ("jmdict-records.xml", "kanjidic2-records.xml", "receipt.json",
                                     "pair-dispositions.md", "changed-file-inventory.md")],
    ]
    claude = json.loads(frozen(HERE / "N1-B120-CLAUDE-001-CONFIRM-001-spec.json",
                               "c5cb9018923dfd162ab211e738a28bb0d8e988b83e00c26272ffbd4fce3e5a3b"))
    claude.update(candidate=CANDIDATE, run="N1-B120-CLAUDE-001-CONFIRM-002")
    claude["revisedSources"].extend([*new_sources, SOURCE + "author-response-claude.md"])
    claude["additionalSources"] = [
        {**item, "source": item["source"].split(" (", 1)[0]}
        for item in claude["additionalSources"]
        if not item["source"].startswith("gates-committed-revision/")
    ]
    claude["additionalSources"].extend([
        *shared, *gate_sources,
        {**binding(WS / "reports-120" / "N1-B120-CLAUDE-001-CONFIRM-001.md"),
         "source": "held-report/N1-B120-CLAUDE-001-CONFIRM-001.md"},
    ])
    require("gpt" not in json.dumps(claude).lower(), "Peer selection in Claude dossier")
    gpt = {
        "batch": 120, "candidate": CANDIDATE, "run": "N1-B120-GPT-001-CONFIRM-002",
        "family": "gpt", "session": "524dc618-ae8f-4474-b698-6896a0507aed",
        "basis": "accepted-confirmation", "priorVerdict": "CONFIRMED", "openClaimIds": [],
        "acceptance": binding(REVIEW / "N1-B120-GPT-001-acceptance.json"),
        "prior": binding(HERE / "N1-B120-GPT-001-CONFIRM-001-acceptance.json"),
        "revisedSources": ["kanji/\u902e.md", "words/\u902e\u6355.md", *new_sources,
                           SOURCE + "author-response-gpt.md"],
        "originalSources": ["evidence/external-snapshots/01-extract.txt"],
        "additionalSources": copy.deepcopy([*shared, *gate_sources]),
    }
    require("claude" not in json.dumps(gpt).lower(), "Peer selection in GPT dossier")
    for spec in (claude, gpt):
        for path in spec["revisedSources"]:
            git(config, "show", f"{CANDIDATE}:{path}")
        for item in spec["additionalSources"]:
            frozen(Path(item["path"]), item["sha256"])
        require(all(" (" not in item["source"] for item in spec["additionalSources"]),
                "Annotated source identifier")
        print(freeze_json(HERE / f"{spec['run']}-spec.json", spec))


if __name__ == "__main__":
    prepare()
