"""Prepare B134's closure checks without modifying or accepting the reviewed tree."""
import json

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

TOOLS = WS / "review-tools"
HERE = WS / "scratch-134"
REPO = WS / "b134-worktree"
CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
SOURCES = {
    "run_b133_closure_checks.py": "9e3c87bb4e0a899990dde66ea9c1c760bcd1d222977842ed5721b15daa19224f",
    "test_run_b133_closure_checks.py": "35b26b3c4282ecb598cb7b163b0d60eaa951e4850e06a3e2c8585ab9a55bda2f",
}


def main():
    helper = TOOLS / "prepare_b133_closure_checks.py"
    frozen(helper, "37ed22cf9b70e94f9a4a6f4772c3accf3dbdda1e395e707a911f8b5d35f5d7c2")
    derive = load_module("b134_closure_derivation", helper).derive
    guard, _ = start_guard("B134 closure-gate preparation only")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Frozen candidate changed")
        helpers = {}
        for name in ("common_134.py", "run_134_gates.py", "check_reading_134.py", "bounded_launch_134.py"):
            signed = git("show", f"{CANDIDATE}:docs/n1-sources/batch-134/producers/{name}")
            require((HERE / name).read_bytes() == signed, "Signed gate helper differs: " + name)
            helpers[name] = sha(signed)
        changes = [
            ("B133", "B134"), ("b133", "b134"), ("_133", "_134"),
            ("scratch-133", "scratch-134"), ("BATCH = 133", "BATCH = 134"),
            ("6858fcfb069cc56a195c3f6ed938f92f657fe96b", BASE),
            ("ad047ace020579f81bde250ac948b9a4cb597887", CANDIDATE),
            ('MEMBERS = ["\\u7434", "\\u925b", "\\u6edd"]', 'MEMBERS = ["\\u7d2b"]'),
            ("Derived from run_b132_closure_checks.py.", "Derived from run_b133_closure_checks.py."),
        ]
        outputs = {}
        for source, replacements in (
                ("run_b133_closure_checks.py", changes),
                ("test_run_b133_closure_checks.py", [("b133", "b134")])):
            derived, applied = derive(frozen(TOOLS / source, SOURCES[source]), replacements)
            destination = TOOLS / source.replace("b133", "b134")
            outputs[destination.name] = {
                **write_frozen(destination, derived), "source": source,
                "sourceSha256": SOURCES[source], "replacements": applied,
            }
        require(not git("status", "--porcelain=v1", "--untracked-files=all"), "Preparation changed candidate")
        result = {
            "status": "PREPARED_NOT_EXECUTED", "candidate": CANDIDATE, "base": BASE,
            "outputs": outputs, "signedGateHelpers": helpers,
            "limits": "Focused controls required. No closure constructed, gate run, review accepted or teaching changed.",
        }
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Closure preparation RAM breach")
    result["memory"] = memory
    print(json.dumps(freeze_json(HERE / "review" / "closure-checks-preparation-001.json", result)))


if __name__ == "__main__":
    main()
