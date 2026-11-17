"""Preserve the unadmitted failed build and correct its negated authorship phrase."""
import json

from common import WS, freeze_json, frozen, require, sha
from confirm_b133_fresh_v2 import OUT, validate_spec

RUN = "N1-B133-CLAUDE-CONFIRM-003"
ROOT = WS / "scratch-133" / "review"
FAILED = ROOT / "claude003-build-failed-001"


def main():
    receipt = json.loads((ROOT / "claude003-build-run-001" / "receipt.json").read_bytes())
    log = (ROOT / "claude003-build-run-001" / "output.log").read_bytes()
    require(receipt["exitCode"] == 1 and receipt["logSha256"] == sha(log)
            and b"Historical authorship remains misattributed" in log, "Wrong failed attempt")
    require(not FAILED.exists() and not (OUT / (RUN + "-preflight.json")).exists()
            and not (OUT / (RUN + "-admission.json")).exists()
            and not (WS / "reports-133" / (RUN + ".md")).exists(), "Already prepared or admitted")
    sources = [
        OUT / (RUN + "-spec.json"), OUT / (RUN + "-chain.json"), OUT / RUN,
        WS / "review-chains" / RUN.lower(),
    ]
    require(all(path.exists() for path in sources), "Incomplete failed attempt")
    old = frozen(sources[0])
    spec = json.loads(old)
    before = "not your own firsthand review"
    require(spec["basisText"].count(before) == 1, "Unexpected attribution wording")
    spec["basisText"] = spec["basisText"].replace(before, "not firsthand work by this session")
    require("your own" not in spec["basisText"].lower(), "Ambiguous authorship remains")
    validate_spec(spec)
    inventory = []
    FAILED.mkdir()
    for index, source in enumerate(sources):
        destination = FAILED / (str(index) + "-" + source.name)
        paths = sorted(source.rglob("*")) if source.is_dir() else [source]
        for path in paths:
            if path.is_file():
                target = destination / path.relative_to(source) if source.is_dir() else destination
                inventory.append({"originalPath": str(path), "retainedPath": str(target),
                                  "sha256": sha(frozen(path))})
        source.rename(destination)
    for row in inventory:
        frozen(row["retainedPath"], row["sha256"])
    corrected = freeze_json(OUT / (RUN + "-spec.json"), spec)
    print(json.dumps(freeze_json(FAILED / "preservation.json", {
        "status": "FAILED_UNADMITTED_BUILD_PRESERVED",
        "reason": "The strict historical-attribution guard rejects the substring 'your own' even "
                  "when negated. Only that negated phrase changed; no source or scope was removed.",
        "originalSpecSha256": sha(old), "correctedSpec": corrected,
        "files": inventory, "reviewLaunched": False,
    })))


if __name__ == "__main__":
    main()
