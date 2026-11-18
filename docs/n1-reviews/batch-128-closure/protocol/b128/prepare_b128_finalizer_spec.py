"""Bind B128's completed reconciliation and confirmation support for closure."""
import json
from pathlib import Path

from common import GUARD_SHA, TOOLS, WS, freeze_json, frozen, require, sha, start_guard

ROOT = WS / "scratch-128" / "review"
CANDIDATE = "7b3fd5c13c20f4b456723abe3de0ac42c4390bd4"
FAILED = {
    "reconciliation-verifier-v2-derivation-execution-001",
    "reconciliation-verifier-v2-tests-001",
}
EXECUTIONS = (
    "blocked-resume-preflight-001",
    "blocked-resume-tests-001",
    "restream-staged-execution-001",
    "lifecycle-tooling-execution-001",
    "reconciliation-verifier-v2-derivation-execution-001",
    "reconciliation-verifier-v2-derivation-execution-002",
    "reconciliation-verifier-v2-tests-001",
    "reconciliation-verifier-v3-derivation-execution-001",
    "reconciliation-verifier-v3-tests-001",
    "reconciliation-verification-001",
    "confirmation-preparation-execution-001",
    "confirmation-claude-admission-execution-001",
    "confirmation-claude-final-execution-001",
    "confirmation-claude-acceptance-execution-001",
    "confirmation-gpt-admission-execution-001",
    "confirmation-gpt-final-execution-001",
    "confirmation-gpt-acceptance-execution-001",
    "closure-archive-001",
    "closure-archive-verification-execution-001",
)


def main():
    guard, _ = start_guard("B128 finalizer support")
    try:
        items = []

        def add(path, name, digest=None):
            items.append({
                "path": str(path), "sha256": sha(frozen(path, digest)), "archivePath": name,
            })
            guard.check()

        for name in (
            "derive_b128_reconciliation_v2.py", "derive_b128_reconciliation_v3.py",
            "verify_b128_reconciliation_v2.py", "verify_b128_reconciliation_v3.py",
            "test_verify_b128_reconciliation.py", "test_verify_b128_reconciliation_v2.py",
            "test_verify_b128_reconciliation_v3.py", "test_prepare_b128_confirmations.py",
            "b128_source_restream.py", "test_b128_source_restream.py",
            "run_b128_closure_checks.py", "prepare_b128_publication_tools.py",
            Path(__file__).name,
        ):
            add(TOOLS / name, "protocol/b128/" + name)
        for name in (
            "reconciliation-verifier-v2-derivation.json",
            "reconciliation-verifier-v3-derivation.json",
            "confirmation-001-preparation.json", "lifecycle-tooling-preflight.json",
            "restream-staged-001.json", "reconciliation-001-staged-preflight-003.json",
            "closure-spec-001.json",
        ):
            add(ROOT / name, "verification/tooling/" + name)
        for name in ("guarded-test-v3.py", "test-guarded-test-v3.py", "guarded-runner-derivation.json"):
            add(ROOT / name, "protocol/b128/" + name)
        add(ROOT / "reconciliation-verifier-v2-derivation-execution-001" / "producer.py",
            "protocol/b128/failed-v2-derivation-producer.py")
        handoff = WS / "scratch-128" / "reconciliation-handoff-001"
        for name in (
            "handoff.json", "resume-evidence.json", "resume-memory.json",
            "execution-receipt.json", "identity-signature.log", "operation.log",
        ):
            add(handoff / name, "verification/handoff/" + name)
        supplements = json.loads(frozen(handoff / "resume-evidence.json"))
        require(supplements["successor"] == CANDIDATE, "Recovery describes another candidate")
        for relative, binding in supplements["bindings"].items():
            if relative != "reconciliation-handoff-001/handoff.json":
                add(Path(binding["path"]), "verification/recovery/" + relative, binding["sha256"])
        for name in EXECUTIONS:
            directory = ROOT / name
            receipt_raw = (directory / "receipt.json").read_bytes()
            receipt = json.loads(receipt_raw)
            log = (directory / "output.log").read_bytes()
            require(sha(log) == receipt["logSha256"], "Execution log changed: " + name)
            require(receipt["guardSha256"] == GUARD_SHA
                    and receipt["childExitCodeAfterCleanup"] == receipt["exitCode"]
                    and receipt["cleanupError"] is None
                    and not receipt["memory"]["breach"], "Execution provenance failed: " + name)
            require(receipt["exitCode"] == (1 if name in FAILED else 0),
                    "Unexpected execution result: " + name)
            for filename, raw in (("receipt.json", receipt_raw), ("output.log", log)):
                path = directory / filename
                require(path.read_bytes() == raw, "Execution changed during capture")
                path.chmod(0o444)
                add(path, "verification/executions/" + name + "/" + filename, sha(raw))
        require(len({item["archivePath"] for item in items}) == len(items), "Duplicate archive path")
        proof = ROOT / "reconciliation-001-independent-proof.json"
        proof_sha = "3418480c542a8e92540f89b695837814e989a3e793933561f1cecfdd02ab234b"
        frozen(proof, proof_sha)
        archive = ROOT / "closure-archive-verification-001.json"
        archive_raw = frozen(archive)
        require(json.loads(archive_raw)["candidate"] == CANDIDATE
                and json.loads(archive_raw)["status"] == "PASS", "Archive is not verified")
        print(freeze_json(ROOT / "finalizer-support-001.json", {
            "candidate": CANDIDATE, "supportingArtifacts": items,
            "captureScope": "Completed execution receipts/logs frozen after hash checks, not "
                            "execution-time immutability. Both failed predecessors remain failures.",
            "published": False,
        }))
        print(freeze_json(ROOT / "finalizer-spec-001.json", {
            "candidate": CANDIDATE,
            "verification": {"path": str(proof), "sha256": proof_sha},
            "archiveVerification": {"path": str(archive), "sha256": sha(archive_raw)},
            "supportingArtifacts": items,
        }))
    finally:
        require(not guard.finish()["breach"], "Finalizer preparation RAM breach")


if __name__ == "__main__":
    main()
