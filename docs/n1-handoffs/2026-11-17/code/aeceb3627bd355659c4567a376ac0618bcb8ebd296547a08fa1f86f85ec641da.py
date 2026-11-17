"""Seal independently written GPT003 decisions against actual execution/source bytes."""
import json
import re
import subprocess
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha

ROOT = WS / "scratch-134" / "review"
LIFE = ROOT / "fresh-independent-002" / "lifecycle-011"
PACKET = ROOT / "fresh-independent-002" / "projected-successor-011" / "packet"
REPO = WS / "b134-worktree"
RUN = "N1-B134-GPT-FRESH-003"
CANDIDATE = "355cccb840d22e7313e79f234eb93d1367e00352"


def main():
    output = ROOT / "gpt-fresh003-adjudication-001"
    require(not output.exists(), "Preserve existing adjudication")
    draft = json.loads(Path(__file__).with_name(
        "b134-gpt-fresh003-substantive-draft.json").read_bytes())
    final_raw = frozen(LIFE / (RUN + "-final.json"),
                       "8e4e01d64bf411917d1438e2f306ae272a0625867168c40e7541f59a9a3071df")
    final = json.loads(final_raw)
    report = frozen(final["report"]["path"], draft["reportSha256"])
    audit = json.loads(frozen(final["audit"]["path"], final["audit"]["sha256"]))
    require(final["candidate"] == draft["candidate"] == CANDIDATE
            and final["run"] == draft["run"] == RUN
            and final["status"] == "MECHANICAL_PASS_REQUIRES_SUBSTANTIVE_ADJUDICATION"
            and final["problems"] == [] and final["structure"]["status"] == "PASS"
            and final["structure"]["overall"] == draft["verdict"]
            and final["report"]["sha256"] == draft["reportSha256"], "Final identity differs")
    require(audit["breaches"] == [] and audit["reviewerIdle"] is True
            and audit["status"] == "FINAL_AUDIT_NEEDS_CLAIM_CHECK"
            and audit["coreRead"] == audit["coreRequired"] == 64
            and audit["extensionRead"] == audit["extensionRequired"] == 6
            and audit["writes"] == audit["readbacks"] == 1
            and audit["readbackVerified"] is True and audit["fetches"] == 0
            and audit["unexpectedUserMessages"] == 0 and not audit["recordIncomplete"]
            and audit["capacityTelemetry"]["status"] == "PASS"
            and audit["capacityTelemetry"]["compactions"] == []
            and audit["actualResponseModels"] == ["gpt-6.1-sol"], "Execution audit differs")
    require(re.findall(r"(?m)^### ([FO]\d+):", report.decode("utf-8")) == ["F1", "F2"]
            and {row["id"] for row in draft["decisions"]}
            == {"F1", "F2", *draft["coordinatorClaimIds"]}, "Claim accounting differs")
    bindings = []
    for relative in (
        "kanji/紫.md", "kanji/濃.md", "kanji/食.md", "kanji/衣.md", "kanji/服.md",
        "kanji/花.md", "kanji/列.md", "kanji/殿.md", "kanji/赤.md",
        "docs/content-format.md", "docs/n1-sources/batch-134-reconciliation-001/dispositions.md",
    ):
        raw = subprocess.check_output(
            ["git", "--no-pager", "show", CANDIDATE + ":" + relative], cwd=REPO)
        require((REPO / relative).read_bytes() == raw, "Current source changed: " + relative)
        bindings.append({"repositoryPath": relative, "snapshot": CANDIDATE, "sha256": sha(raw)})
    inventory = json.loads(frozen(PACKET / "SHA256SUMS.json",
                                 "adeac0009e52039a57fd3121a45f0e91eb697a6f35b131db0517922f3d1b540c"))
    sources = []
    for name in ("evidence/external-snapshots/01-extract.txt",
                 "evidence/external-snapshots/02-extract.txt",
                 "evidence/jmdict-families.compact-xml-v1.txt"):
        raw = frozen(PACKET / name, inventory[name])
        sources.append({"source": name, "path": str(PACKET / name),
                        "sha256": sha(raw), "lines": len(raw.decode("utf-8").splitlines()),
                        "redistribution": "Native captures remain local; cite hash and paraphrase only."})
    draft.update(claimsAdjudicated=True, finalSha256=sha(final_raw),
                 signedSourceBindings=bindings, sourceBindings=sources)
    draft["claimChecks"].insert(0, {
        "claim": "Actual reviewed model, read coverage, report bytes and context capacity.",
        "evidence": "Final " + sha(final_raw) + "; audit " + final["audit"]["sha256"]
                    + "; actual gpt-6.1-sol;64/64 core,6/6 extension,one write/readback;"
                    + "peak input " + str(audit["capacityTelemetry"]["actualPeakInputTokens"])
                    + ";zero compaction/fetches/unexpected messages.",
        "disposition": "Mechanical review evidence passes; no semantic acceptance follows solely "
                       "from the clean audit. The raw NEEDS FIX result is preserved.",
    })
    print(json.dumps(freeze_json(output / "adjudication.json", draft)))


if __name__ == "__main__":
    main()
