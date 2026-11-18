"""Prepare isolated, bounded follow-ups after the held nine-pair correction."""
import json
import re
import sys
from pathlib import Path

from common import CHECKS, WS, freeze_json, frozen, git, load_batch, require, sha
from confirm_followup import build_followup
from confirm_v2 import binding, clean
from prepare_b123_confirmations_001 import REVIEWERS
from verify_b123_revision_v4 import CAPTURE_SHA, OPTIONAL, PARENT, PREFIX, REQUIRED

REVIEW = WS / "scratch-123" / "review"
PRIOR_ACCEPTANCES = {
    "claude": "451f12e971abdec7e32f4f1bd2e857a134225416cee7afb58edc965c79db5ca0",
    "gpt": "a24f56ea0caa01def1aa4924731cec2328f607645787af5cd16ac252d9989cae",
}


def check_isolation(raw, family=None):
    text = raw.decode("utf-8")
    denied = ("gpt",) if family == "claude" else ("claude",) if family == "gpt" else ("claude", "gpt")
    require(not any(re.search(name, text, re.I) for name in denied),
            "Another reviewer's identity or report occurs in selected evidence")
    require(raw.endswith(b"\n"), "Selected evidence lacks chain line framing")


def prepare(candidate):
    config = load_batch(123)
    clean(config, candidate)
    proof_path = REVIEW / "coordinator-reconciliation-verification-003.json"
    adjudication_path = REVIEW / "reconciliation-003-source-adjudication.json"
    proof = json.loads(frozen(proof_path))
    adjudication = json.loads(frozen(adjudication_path))
    require(proof["status"] == "PASS" and proof["candidate"] == candidate
            and proof["parent"] == PARENT and not proof["memory"]["breach"]
            and proof["newCapture"]["sha256"] == CAPTURE_SHA,
            "Signed follow-up proof differs")
    require(adjudication["candidate"] == candidate
            and adjudication["status"] == "READY_FOR_INDEPENDENT_CONFIRMATIONS"
            and adjudication["openClaimIds"] == []
            and set(adjudication["pairDecisions"]) == {f"Q{i}" for i in range(1, 10)},
            "Source adjudication incomplete")
    names = git(config, "ls-tree", "-r", "--name-only", candidate, "--", PREFIX).decode().splitlines()
    require(set(names) == set(proof["signedSourceArtifacts"]), "Signed source inventory differs")
    revised = ["kanji/\u7bc4.md", *[f"kanji/{c}.md" for c in sorted(set(REQUIRED) | OPTIONAL)], *names]
    revised += [
        "docs/n1-sources/batch-123/reconciliation-001/kanjidic2-records.xml",
        "docs/n1-sources/batch-123/reconciliation-001/jmdict-records.xml",
    ]
    for path in revised:
        raw = git(config, "show", f"{candidate}:{path}")
        check_isolation(raw)
        if path in proof["signedSourceArtifacts"]:
            require(sha(raw) == proof["signedSourceArtifacts"][path], "Verified source changed")

    def source(path, label, expected=None):
        raw = frozen(path, expected)
        check_isolation(raw)
        return {**binding(path), "source": label}

    shared = [source(proof_path, "coordinator/revision-verification-003.json"),
              source(adjudication_path, "coordinator/source-adjudication-003.json")]
    reference_path = REVIEW / "followup-003-han-source-reference.json"
    reference = json.loads(frozen(reference_path))
    original = frozen(reference["originalExtract"]["path"], reference["originalExtract"]["sha256"])
    lines = original.decode("utf-8").splitlines()
    require(sum(len(item["text"]) for item in reference["quotes"]) <= 80,
            "Overlong prior-source quotation")
    for item in reference["quotes"]:
        first, last = item["lines"]
        require(1 <= first <= last <= len(lines)
                and item["text"] in "\n".join(lines[first - 1:last]), "Prior-source quote differs")
    shared.append(source(reference_path, "source-references/han.json"))
    gates = Path(proof["gateSummary"]["path"]).parent
    shared.append(source(gates / "summary.json", "committed-checks/summary.json",
                         proof["gateSummary"]["sha256"]))
    require([item["gate"] for item in proof["gates"]] == list(CHECKS), "Missing gates")
    for item in proof["gates"]:
        name = f"{item['gate']}.log"
        shared.append(source(gates / name, f"committed-checks/{name}", item["logSha256"]))
    specifications = []
    for family, (session, initial_sha, _) in REVIEWERS.items():
        initial = REVIEW / f"N1-B123-{family.upper()}-001-acceptance.json"
        prior = REVIEW / "confirm" / f"N1-B123-{family.upper()}-CONFIRM-002-acceptance.json"
        frozen(initial, initial_sha)
        frozen(prior, PRIOR_ACCEPTANCES[family])
        response = WS / "scratch-123" / "reconciliation-003" / f"author-response-{family}-003.md"
        check_isolation(frozen(response), family)
        run = f"N1-B123-{family.upper()}-CONFIRM-003"
        spec = {
            "batch": 123, "candidate": candidate, "run": run, "family": family, "session": session,
            "basis": "accepted-confirmation" if family == "claude" else "held-confirmation",
            "priorVerdict": "CONFIRMED" if family == "claude" else "UNVERIFIED",
            "openClaimIds": [] if family == "claude" else [f"Q{i}" for i in range(1, 10)],
            "acceptance": binding(initial), "prior": binding(prior),
            "revisedSources": revised,
            "originalSources": [],
            "additionalSources": [{**binding(response), "source": "author-response/current.md"}, *shared],
        }
        specifications.append((REVIEW / "confirm" / f"{run}-spec.json", spec))
    for path, spec in specifications:
        print(json.dumps(freeze_json(path, spec)))
        build_followup(path)


if __name__ == "__main__":
    prepare(sys.argv[1])
