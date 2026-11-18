"""Preserve the refused packet and adapt newline-less tool text for chain display."""
import copy
import json
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, write_frozen
from confirm_v2 import build, clean
from prepare_b123_confirmations_001 import CANDIDATE, REVIEW, REVIEWERS, additional


def main():
    config = load_batch(123)
    clean(config, CANDIDATE)
    previous = REVIEW / "confirm" / "N1-B123-CLAUDE-CONFIRM-001-spec.json"
    spec = json.loads(frozen(previous,
                            "a6ad83aa8da3ef62319fedba222a47d0870fd177718ce2baf37029cd115e13c5"))
    adaptations = []
    for item in spec["additionalSources"]:
        raw = frozen(item["path"], item["sha256"])
        if raw.endswith(b"\n"):
            continue
        require(item["source"].startswith("external-sources/")
                and item["source"].endswith("-tool-result.txt"), "Unexpected newline-less input")
        original = {"path": item["path"], "sha256": item["sha256"], "bytes": len(raw)}
        output = write_frozen(REVIEW / "confirmation-tool-text-001" /
                              Path(item["path"]).name, raw + b"\n")
        require(frozen(output["path"])[:-1] == raw, "Display adaptation changed source text")
        item["path"], item["sha256"] = output["path"], output["sha256"]
        adaptations.append({"sourceLabel": item["source"], "original": original,
                            "display": output, "soleChange": "Append one final LF for chain framing."})
    require(adaptations, "Expected the recorded chain framing incompatibility")
    provenance = freeze_json(REVIEW / "confirmation-tool-text-001" / "provenance.json", {
        "status": "DISPLAY_ADAPTATION_ONLY", "files": adaptations,
        "limits": "Original tool returns and capture provenance remain byte-identical. These "
                  "display copies append one LF only; no content, truncation notice or "
                  "source boundary is removed or rewritten. This does not complete truncated pages.",
    })
    spec["additionalSources"].append(additional(Path(provenance["path"]),
                                               "external-sources/display-adaptation.json",
                                               provenance["sha256"]))
    for path in spec["revisedSources"]:
        require(git(config, "show", f"{CANDIDATE}:{path}").endswith(b"\n"),
                f"Revised source lacks chain framing: {path}")
    packet = WS / "review-packets" / "batch-123-3bda01ae"
    for path in spec["originalSources"]:
        require(frozen(packet / path).endswith(b"\n"), f"Original source lacks framing: {path}")
    for item in spec["additionalSources"]:
        require(frozen(item["path"], item["sha256"]).endswith(b"\n"),
                "Additional source lacks framing")
    for family, (session, acceptance_sha, response_sha) in REVIEWERS.items():
        current = copy.deepcopy(spec)
        run = f"N1-B123-{family.upper()}-CONFIRM-002"
        current.update(run=run, family=family, session=session)
        current["acceptance"] = {
            "path": str(REVIEW / f"N1-B123-{family.upper()}-001-acceptance.json"),
            "sha256": acceptance_sha}
        response = WS / "scratch-123" / "reconciliation-002" / f"author-response-{family}-002.md"
        current["additionalSources"][0] = additional(response, "author-response/current.md", response_sha)
        path = REVIEW / "confirm" / f"{run}-spec.json"
        print(json.dumps(freeze_json(path, current)))
        build(path)
    print(json.dumps(freeze_json(REVIEW / "confirmation-preparation-recovery-001.json", {
        "failedAttempt": "confirmation-preparation-001",
        "cause": "Six retained web_fetch returns have no final LF; the unchanged chain "
                 "builder requires a line-terminated source.",
        "preserved": "All first-attempt artifacts, original tool bytes, producer and failure receipt.",
        "adaptation": provenance, "runs": [
            "N1-B123-CLAUDE-CONFIRM-002", "N1-B123-GPT-CONFIRM-002"],
        "reviewersLaunched": False,
    })))


if __name__ == "__main__":
    main()
