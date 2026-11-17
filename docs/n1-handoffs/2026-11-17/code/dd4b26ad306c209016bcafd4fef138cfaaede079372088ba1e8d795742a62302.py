"""Derive B126 receipt/checkpoint verifiers from the frozen B122 publication tools."""
import json
import re
import sys
from pathlib import Path

from close_b126 import CANDIDATE, bounded_git, verify_archive
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from prepare_b122_publication_tools import replace
from prepare_b123_publication_tools import PINS


def main(published):
    require(re.fullmatch(r"[0-9a-f]{40}", published), "Full publication SHA required")
    guard, _ = start_guard("B126 publication tooling preparation")
    try:
        git = bounded_git(guard)
        require(git("rev-parse", "HEAD").decode().strip() == published
                and not git("status", "--porcelain=v1", "--untracked-files=all")
                and git("show", "-s", "--format=%P", published).decode().strip() == CANDIDATE,
                "Publication must be the clean direct closure child")
        manifest = git("show", f"{published}:manifest.json")
        require(manifest == git("show", f"{CANDIDATE}:manifest.json")
                and json.loads(manifest)["contentVersion"] == "54646f3d85c21fd3",
                "Reviewed manifest differs")
        verify_archive()
        substitutions = {
            "18ec8c757b0faae846ddec5317c37089cfbbae67": published,
            "e0787399ec3babfa": "54646f3d85c21fd3",
            "B122": "B126", "batch-122": "batch-126", "load_batch(122)": "load_batch(126)",
            "8706": "8714", "252": "256", "246": "250", "976": "972",
            r"\u60a0": r"\u5098",
        }
        records = []
        for name, digest in PINS.items():
            source = WS / "scratch-122" / name
            original = frozen(source, digest).decode("utf-8")
            selected = {old: new for old, new in substitutions.items() if old in original}
            derived = replace(original, selected)
            require(replace(derived, {new: old for old, new in selected.items()}) == original,
                    "Derivation is not byte-reversible")
            compile(derived, name, "exec")
            records.append({"source": {"path": str(source), "sha256": digest},
                            "output": write_frozen(WS / "scratch-126" / name, derived.encode("utf-8")),
                            "substitutions": selected, "reverseExact": True})
        print(freeze_json(WS / "scratch-126" / "publication-tools-preflight.json", {
            "batch": 126, "publishedCommit": published,
            "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
            "derivations": records,
            "limits": "Preparation only; receipt CI, exact ZIP/tree equality and owner checkpoint remain required."}))
    finally:
        require(not guard.finish()["breach"], "Publication-tool preparation RAM breach")


if __name__ == "__main__":
    main(sys.argv[1])
