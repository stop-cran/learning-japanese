import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from recon_common import BASE, HERE, PACKET, PARENT, REPO, SCRATCH, git, sha, start_guard, stop_child, write

FINGERPRINT = "D4C9A275A218AF747B787AFA9D94B9D311BD26A7"
TRAILER = "Co-authored-by: Copilot App <223556219+Copilot@users.noreply.github.com>"


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ("stage", "sign", "handoff"):
        raise SystemExit("usage: finish_reconciliation.py stage|sign|handoff NEW_DIRECTORY")
    mode, out = sys.argv[1], Path(sys.argv[2]).resolve()
    assert out.parent == SCRATCH and not out.exists()
    out.mkdir()
    guard = start_guard()
    process = None
    try:
        owner_name = git("show", "-s", "--format=%an", PARENT).decode("utf-8").strip()
        identity = {k: git("config", k).decode("utf-8").strip() for k in ("user.name", "user.email", "user.signingkey", "commit.gpgsign")}
        assert identity == {"user.name": owner_name, "user.email": "stop-cran@list.ru", "user.signingkey": FINGERPRINT, "commit.gpgsign": "true"}
        inventory = json.loads((PACKET / "packet-files.json").read_text(encoding="utf-8"))
        for path, info in inventory["files"].items():
            guard.check()
            assert sha((PACKET / path).read_bytes()) == info["sha256"], path
        assert {p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()} == set(inventory["files"]) | {"packet-files.json"}
        if mode in ("stage", "sign"):
            assert git("rev-parse", "HEAD").decode().strip() == PARENT
        if mode == "stage":
            paths = ["kanji/唇.md", "manifest.json", "docs/n1-authoring-notes.md", "docs/n1-sources/batch-128-progress-reconciliation-001.json"]
            paths += [p.relative_to(REPO).as_posix() for p in PACKET.rglob("*") if p.is_file()]
            git("add", "--sparse", "--", *paths)
            actual = set(git("diff", "--cached", "--name-only", "--no-renames", "-z").decode("utf-8").rstrip("\0").split("\0"))
            assert actual == set(paths)
            blobs = {}
            for entry in git("ls-files", "--stage", "-z", "--", *paths).decode("utf-8").rstrip("\0").split("\0"):
                guard.check()
                meta, path = entry.split("\t", 1)
                _, blob, stage = meta.split()
                raw = (REPO / path).read_bytes()
                assert stage == "0" and blob == hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest(), path
                blobs[path] = {"gitBlob": blob, "rawSha256": sha(raw)}
            assert len(blobs) == len(paths)
            git("-c", "core.whitespace=blank-at-eol,blank-at-eof,space-before-tab,cr-at-eol", "diff", "--cached", "--check")
            write(out / "index-verification.json", {"files": blobs, "allStagedBytesEqualWorkspace": True, "exactScope": True})
            result = {"mode": mode, "files": len(blobs), "allStagedBytesEqualWorkspace": True}
        else:
            if mode == "sign":
                assert not git("diff", "--name-only")
                gates = json.loads((SCRATCH / "reconciliation-author-gates-001" / "summary.json").read_text(encoding="utf-8"))
                preservation = json.loads((SCRATCH / "reconciliation-preservation-author-001" / "summary.json").read_text(encoding="utf-8"))
                assert gates["status"] == preservation["status"] == "PASS"
                assert gates["manifestSha256"] == preservation["manifestSha256"] == sha((REPO / "manifest.json").read_bytes())
                args = ["git", "commit", "--quiet", "-S" + FINGERPRINT,
                        "-m", "Reconcile B128 direct meaning choices",
                        "-m", "Add direct conservative blossom, qualified-edge and outer-area guards on 唇. Preserve complete narrow sources, two-direction Q1-Q15 dispositions, isolated responses and prior evidence. No publication or new membership.",
                        "-m", TRAILER]
            else:
                head = git("rev-parse", "HEAD").decode().strip()
                assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
                assert not git("status", "--porcelain=v1", "--untracked-files=all")
                args = ["git", "verify-commit", "--raw", head]
            log = out / "operation.log"
            with log.open("xb") as stream:
                process = subprocess.Popen(args, cwd=REPO, stdout=stream, stderr=subprocess.STDOUT)
                deadline = time.monotonic() + 30
                while True:
                    try:
                        code = process.wait(timeout=0.1)
                        break
                    except subprocess.TimeoutExpired:
                        guard.check()
                        if time.monotonic() >= deadline:
                            raise TimeoutError("Deadline reached. Preserve staged state and yield; do not retry or bypass owner signing.")
                guard.check()
            assert code == 0, log.read_text(encoding="utf-8")
            head = git("rev-parse", "HEAD").decode().strip()
            assert git("rev-parse", "HEAD^@").decode().split() == [PARENT]
            assert not git("status", "--porcelain=v1", "--untracked-files=all")
            signature = git("show", "-s", "--format=%H%n%P%n%an%n%ae%n%cn%n%ce%n%G?%n%GF%n%GP%n%B", head).decode("utf-8")
            lines = signature.splitlines()
            assert lines[:6] == [head, PARENT, owner_name, "stop-cran@list.ru", owner_name, "stop-cran@list.ru"]
            assert lines[6] in ("G", "U") and FINGERPRINT in lines[7:9] and TRAILER in signature
            write(out / "identity-signature.log", signature.encode("utf-8"))
            result = {"mode": mode, "successor": head, "parent": PARENT, "publishedBase": BASE, "clean": True,
                      "author": owner_name + " <stop-cran@list.ru>", "committer": owner_name + " <stop-cran@list.ru>",
                      "signatureStatus": lines[6], "signingFingerprint": lines[7], "primaryFingerprint": lines[8],
                      "signatureEvidence": str(out / "identity-signature.log")}
            if mode == "handoff":
                gates_path = SCRATCH / "reconciliation-committed-gates-001" / "summary.json"
                preserve_path = SCRATCH / "reconciliation-preservation-committed-001" / "summary.json"
                gates = json.loads(gates_path.read_text(encoding="utf-8"))
                preservation = json.loads(preserve_path.read_text(encoding="utf-8"))
                assert gates["status"] == preservation["status"] == "PASS"
                assert gates["startingHead"] == preservation["head"] == head
                assert gates["manifestSha256"] == preservation["manifestSha256"] == sha(git("show", "HEAD:manifest.json"))
                result.update({
                    "worktree": str(REPO), "membership": [{"kanji": "唇", "sourceRow": 159}],
                    "runtimeChangesFromParent": ["kanji/唇.md", "manifest.json"],
                    "supportWordAndGeometryRawBytesPreserved": True,
                    "addedDirectGuards": ["咲", "刃", "郊"], "totalDirectGuards": 17,
                    "authorGates": {"directory": str(SCRATCH / "reconciliation-author-gates-001"), "summarySha256": sha((SCRATCH / "reconciliation-author-gates-001" / "summary.json").read_bytes())},
                    "committedGates": {"directory": str(gates_path.parent), "summarySha256": sha(gates_path.read_bytes()), "checks": gates["checks"]},
                    "preservation": {"directory": str(preserve_path.parent), "summarySha256": sha(preserve_path.read_bytes()), "runtimeCount": preservation["manifestMappedRuntimeEntries"], "unchangedFromParent": preservation["parentRuntimeEntriesUnchanged"]},
                    "packet": str(PACKET), "packetInventorySha256": sha((PACKET / "packet-files.json").read_bytes()),
                    "bindings": {name: {"path": str(PACKET / name), "sha256": sha((PACKET / name).read_bytes())} for name in (
                        "pair-dispositions.json", "source-receipt.json", "source-receipt-002.json", "selector-membership.json",
                        "source-verification-002.json", "response-a.md", "response-b.md", "preserved-history.json",
                        "author-evidence.json", "packet-files.json")},
                    "manifestSha256": gates["manifestSha256"], "contentVersion": preservation["contentVersion"],
                    "noOpenUnguardedClaims": True,
                    "limits": ["Historical scope remains disclosed and directly guarded for Q1/Q12; no universal synonymy.",
                               "Two latent hypothetical reading-pool collisions; zero modeled production/restricted-Starter hits.",
                               "No arbitrary/custom-pool, multiple-borrow, Kotlin/native/device or older-APK acceptance.",
                               "脣 bundled-cmap gap and actual fallback rendering remain untested; pilot vocabulary only.",
                               "No reviewer contact, push, publication, new cards or new batch."],
                    "publishedAccountingUnchanged": {"delivered": 257, "remaining": 971, "localDrafts": 1},
                })
        write(out / ("handoff.json" if mode == "handoff" else "result.json"), result)
        print(json.dumps(result, ensure_ascii=False))
    finally:
        active_error = sys.exc_info()[1]
        cleanup_error = None
        try:
            stop_child(process)
        except (OSError, subprocess.TimeoutExpired) as error:
            cleanup_error = error
        write(out / "execution-receipt.json", {
            "mode": mode, "memory": guard.finish(), "childPid": process.pid if process else None,
            "childExitCode": process.returncode if process else None, "waitTimeoutSeconds": 0.1,
            "cleanupTimeoutSecondsPerStage": 10, "activeError": str(active_error) if active_error is not None else None,
            "cleanupError": str(cleanup_error) if cleanup_error is not None else None,
            "producerSha256": sha(Path(__file__).read_bytes()),
        })
        if cleanup_error is not None:
            if active_error is None:
                raise cleanup_error
            active_error.add_note(f"Child cleanup also failed: {cleanup_error}")


if __name__ == "__main__":
    main()
