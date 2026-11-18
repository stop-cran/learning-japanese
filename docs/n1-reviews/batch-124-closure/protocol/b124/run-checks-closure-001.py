"""Run the existing B124 host gates on its contributor-only review closure."""
import json
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import CHECKS, freeze_json, frozen, git, load_batch, load_module, require, sha
from confirm_v2 import clean
from finalize_b124 import check_documentation, check_history, check_proofs

HERE = Path(__file__).resolve().parent


def main(commit, output):
    config = load_batch(124)
    clean(config, commit)
    closure = Path(config["repo"]) / "docs" / "n1-reviews" / "batch-124-closure"
    provenance = json.loads(frozen(closure / "provenance.json"))
    candidate = provenance["reviewedSnapshot"]
    require(git(config, "show", "-s", "--format=%P", commit).decode().strip() == candidate,
            "Closure must be a direct child of the confirmed successor")
    changed = git(config, "diff", "--name-only", candidate, commit).decode().splitlines()
    require(changed and all(path.startswith("docs/") for path in changed),
            "Closure changed non-contributor content")
    manifest = git(config, "show", f"{commit}:manifest.json")
    require(manifest == git(config, "show", f"{candidate}:manifest.json"), "Closure manifest changed")
    first, current = [
        json.loads(frozen(closure / "verification" / f"reconciliation-{index:03}.json"))
        for index in (1, 2)
    ]
    documentation = json.loads(frozen(closure / "verification" / "response-correction-001.json"))
    check_history(provenance, candidate, config)
    check_proofs(first, current, current["candidate"], config)
    check_documentation(documentation, candidate, current, config)
    for path, digest in provenance["recordedFileSha256"].items():
        frozen(closure / path, digest)
    validation = json.loads(frozen(closure / "validation-provenance.json"))
    require(validation["candidate"] == candidate
            and validation["reviewClosureSha256"] == sha(frozen(closure / "provenance.json")),
            "Validation describes another closure")
    for path, digest in validation["recordedFileSha256"].items():
        frozen(closure / path, digest)
    runner_path = Path(current["runner"]["path"])
    frozen(runner_path, current["runner"]["sha256"])
    runner = load_module("b124_runtime_closure_gates", runner_path)
    require(set(runner.CHECKS) == set(CHECKS), "Runtime gate inventory differs")
    output = Path(output).resolve()
    require(output.parent == HERE and not output.exists(), "Use a new direct scratch-124 output")
    output.mkdir()
    manifest_sha = None
    for name in CHECKS:
        manifest_sha = runner.run_gate(name, output, manifest_sha)
    require(manifest_sha == sha(manifest), "Gates changed the confirmed manifest")
    clean(config, commit)
    summary = {
        "batch": 124, "status": "PASS", "base": config["base"], "candidateHead": commit,
        "reviewedSnapshot": candidate, "runtimeGateBasis": current["candidate"],
        "checks": list(CHECKS), "manifestSha256": manifest_sha, "manifestReproducible": True,
        "runnerSha256": current["runner"]["sha256"],
        "closureRunnerSha256": sha(frozen(Path(__file__))),
        "limits": "Host gates only; no arbitrary-pool, native/device or publication acceptance.",
    }
    freeze_json(output / "summary.json", summary)
    for path in output.iterdir():
        if path.is_file():
            path.chmod(0o444)
    print(json.dumps(summary))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
