"""Freeze separate original-reviewer confirmation inputs for B122."""
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, load_batch, require, sha
from confirm_v2 import clean

CANDIDATE = "4659f3a2e44ac01dc2e1a455db2fee300496b080"
REVIEW = WS / "scratch-122" / "review"
SOURCE = "docs/n1-sources/batch-122-reconciliation/"
FAMILIES = {
    "claude": (
        "6d8d06fa-17cc-4ddc-a197-2307998499d4",
        "6fc74d09fe013972631a4b8459aeff6a4f50905bc16addef19f09aeaa7a148d4",
        "cbfde1dc9c55355d530e285b5cc47920f9d210afed74ae563eac49275060f9c8",
    ),
    "gpt": (
        "c47c8f02-a9a5-4df1-a263-bd526aff1dc8",
        "de10e8df97c726337cd1c903a723cfd1f4b8d9b33b82e8593b7d86afaf42c562",
        "ec3fa825a5bf41759af17072f44bbf34cc59750924fe20949a32759fa4d9685f",
    ),
}


def additional(path, source, expected=None):
    raw = frozen(path, expected)
    return {"path": str(path), "sha256": sha(raw), "source": source}


def main():
    clean(load_batch(122), CANDIDATE)
    shared = [
        additional(REVIEW / "coordinator-reconciliation-verification-002.json",
                   "checks/signed-revision-verification.json",
                   "ff04d8bd487315f769a572c75e0fbeafa50f3aaf76b18408c2fe96b84c16214a"),
        additional(REVIEW / "coordinator-reconciliation-selection-001.json",
                   "checks/complete-selection-verification.json",
                   "164e412f4397d9e95e1cfd83968c4f1e09382fc30e0f5ec66fc0557605224dd9"),
    ]
    gates = WS / "scratch-122" / "reconciliation-committed-gates-001"
    shared.extend(additional(gates / f"{name}.log", f"checks/{name}.txt")
                  for name in CHECKS)
    revised = [
        "kanji/悠.md", "words/悠々.md",
        *(SOURCE + name for name in (
            "neutral-kanjidic2.xml", "neutral-jmdict.xml",
            "additional-kanjidic2.xml", "additional-jmdict.xml", "dispositions.md")),
    ]
    original = [
        "evidence/kanjidic2-records.xml", "evidence/jmdict-families.xml",
        "evidence/external-snapshots/01-extract.txt", "evidence/joyo-rows.json",
        "repo/docs/content-format.md",
        *(f"repo/kanji/{character}.md" for character in "易簡単慢常延幅優遊娯余快伸続凪息側後達"),
    ]
    records = []
    for family, (session, acceptance_sha, response_sha) in FAMILIES.items():
        run = f"N1-B122-{family.upper()}-001"
        acceptance = REVIEW / f"{run}-acceptance.json"
        frozen(acceptance, acceptance_sha)
        response = additional(WS / "scratch-122" / f"{family}-reconciliation-response.md",
                              "author-response/response.md", response_sha)
        raw_response = frozen(Path(response["path"])).decode("utf-8")
        other = "GPT" if family == "claude" else "CLAUDE"
        require(f"N1-B122-{other}" not in raw_response, "Cross-review response contamination")
        spec = {
            "batch": 122, "run": run + "-CONFIRM-001", "family": family,
            "candidate": CANDIDATE, "session": session,
            "acceptance": {"path": str(acceptance), "sha256": acceptance_sha},
            "revisedSources": revised, "originalSources": original,
            "additionalSources": [response, *shared],
        }
        records.append(freeze_json(REVIEW / "confirm" / f"{spec['run']}-spec.json", spec))
    freeze_json(REVIEW / "confirm" / "specification-preparation.json", {
        "batch": 122, "candidate": CANDIDATE, "specifications": records,
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "scope": "Each reviewer gets only its own original report and response. Shared sources "
                 "are the actual signed revision, neutral dispositions, complete dictionaries, "
                 "unchanged comparison cards and fresh host-gate evidence.",
        "preparedOnly": True,
    })


if __name__ == "__main__":
    main()
