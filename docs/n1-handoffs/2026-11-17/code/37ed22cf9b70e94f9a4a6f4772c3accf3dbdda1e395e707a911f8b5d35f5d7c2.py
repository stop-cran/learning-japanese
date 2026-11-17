"""Specialize the existing closure gate wrapper without executing or accepting a closure."""
import ast
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen
from verify_b133_packet import RUNNER
from verify_b133_sources import Git

TOOLS = WS / "review-tools"
HERE = WS / "scratch-133"
REPO = WS / "b133-worktree"
CANDIDATE = "ad047ace020579f81bde250ac948b9a4cb597887"
BASE = "6858fcfb069cc56a195c3f6ed938f92f657fe96b"
SOURCES = {
    "run_b132_closure_checks.py": "3a1d3f79e85c89096a9d8ecbb89baed6d77fc22f5745f3d8e42432e2d6e2d301",
    "test_run_b132_closure_checks.py": "07cc5e04c83477353e84bd632f18170e0ca230b7c75a440445efd54b38b2ab10",
}


def derive(raw, changes):
    text = raw.decode("utf-8")
    applied = []
    for before, after in changes:
        require(before in text, "Missing derivation anchor: " + before)
        applied.append((before, after, text.count(before)))
        text = text.replace(before, after)
    inverse = text
    for before, after, count in reversed(applied):
        require(inverse.count(after) == count, "Ambiguous reverse derivation: " + after)
        inverse = inverse.replace(after, before)
    require(inverse.encode() == raw, "Derivation is not byte-reversible")
    ast.parse(text)
    return text.encode(), applied


def main():
    guard, _ = start_guard("B133 closure-gate preparation only")
    git = Git(REPO, RUNNER, guard)
    try:
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Candidate is no longer clean and unchanged")
        helpers = {}
        for name in ("common_133.py", "run_133_gates.py", "check_reading_133.py", "bounded_launch_133.py"):
            signed = git("show", f"{CANDIDATE}:docs/n1-sources/batch-133/producers/{name}")
            require((HERE / name).read_bytes() == signed, "Actual signed gate helper differs: " + name)
            helpers[name] = sha(signed)
        common = [("B132", "B133"), ("b132", "b133")]
        changes = common + [
            ("_132", "_133"), ("scratch-132", "scratch-133"), ("BATCH = 132", "BATCH = 133"),
            ("2375ab9add0cc5d569c8ea35d229b82813fd8557", BASE),
            ("2e618b38ae5b420f7a1fe6783268093348367c51", CANDIDATE),
            ('MEMBERS = ["\\u5893"]', 'MEMBERS = ["\\u7434", "\\u925b", "\\u6edd"]'),
            ('"check_reading_133.py")', '"check_reading_133.py", "bounded_launch_133.py")'),
            ("Derived from run_b131_closure_checks.py.", "Derived from run_b132_closure_checks.py."),
        ]
        outputs = {}
        for source_name, replacements in (
                ("run_b132_closure_checks.py", changes),
                ("test_run_b132_closure_checks.py", [("b132", "b133")])):
            raw = frozen(TOOLS / source_name, SOURCES[source_name])
            derived, applied = derive(raw, replacements)
            destination = TOOLS / source_name.replace("b132", "b133")
            outputs[destination.name] = {
                **write_frozen(destination, derived),
                "source": source_name, "sourceSha256": SOURCES[source_name],
                "replacements": applied,
            }
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Preparation changed candidate")
        print(json.dumps(freeze_json(HERE / "review" / "closure-checks-preparation-001.json", {
            "status": "PREPARED_NOT_EXECUTED", "candidate": CANDIDATE, "base": BASE,
            "outputs": outputs, "signedGateHelpers": helpers,
            "scope": "B133 wrapper additionally binds its signed bounded launcher before invoking the unchanged ten serial gates.",
            "limits": "Focused controls still required. No closure constructed, gate run, review accepted or teaching changed.",
        })))
    finally:
        require(not guard.finish()["breach"], "Preparation RAM breach")


if __name__ == "__main__":
    main()
