import difflib
import json
import re
import subprocess
from pathlib import Path
from recon_common import *


def capture_git(args, guard):
    command = ["git", "-c", "core.quotepath=false", *args]
    child = subprocess.Popen(command, cwd=REPO, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        while True:
            try:
                stdout, stderr = child.communicate(timeout=0.1)
                break
            except subprocess.TimeoutExpired:
                guard.check()
        return {"command": command, "exitCode": child.returncode,
                "stdout": stdout.decode("utf8"), "stderr": stderr.decode("utf8"),
                "stdoutSha256": sha(stdout), "stderrSha256": sha(stderr)}
    finally:
        stop_child(child)


def check_patch_whitespace(guard):
    rel = "docs/n1-sources/batch-129-reconciliation/teaching-diff.patch"
    patch = (REPO / rel).read_bytes()
    expected_patch = []
    for ch in ("絹", "虹"):
        path = f"kanji/{ch}.md"
        before = git("show", f"{PARENT}:{path}").replace(b"\r\n", b"\n").decode()
        after = normalized(REPO / path)
        expected_patch.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                                  fromfile=PARENT + ":" + path, tofile="candidate:" + path))
    assert patch == "".join(expected_patch).encode()
    full = capture_git(["-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check"], guard)
    pattern = re.compile(re.escape(rel) + r":(\d+): trailing whitespace\.\n\+ \n")
    matches = list(pattern.finditer(full["stdout"]))
    assert full["exitCode"] == 2 and full["stderr"] == ""
    assert len(matches) == 4 and "".join(m.group() for m in matches) == full["stdout"]
    lines = patch.splitlines()
    for match in matches:
        assert lines[int(match.group(1)) - 1] == b" ", "Only a unified-diff blank-context marker is accepted"
    rest = capture_git(["-c", "core.whitespace=cr-at-eol", "diff", "--cached", "--check",
                        "--", ".", ":(exclude)" + rel], guard)
    assert rest["exitCode"] == 0 and rest["stdout"] == "" and rest["stderr"] == ""
    return {"fullCheck": full, "allOtherStagedFilesCheck": rest,
            "acceptedPatchLines": [int(m.group(1)) for m in matches],
            "patchSha256": sha(patch),
            "disposition": "Exactly four 0x20 blank-context delimiter lines in a byte-regenerated unified diff are accepted as patch syntax, not removed or fixed. All other staged paths pass; no global whitespace check/configuration is disabled."}


def main():
    guard = start_guard()
    try:
        assert git("rev-parse", "HEAD").decode().strip() == PARENT
        initial = HERE / "signing-attempt-001.json"
        attempt = json.loads(initial.read_text(encoding="utf8"))
        assert attempt["exitCode"] is None and attempt["stalled"] is False
        assert not (HERE / "staging-001.json").exists()
        sign_source = (HERE / "sign.py").read_text(encoding="utf8")
        assert sign_source.index('git("-c", "core.whitespace=cr-at-eol"') < sign_source.index("process = subprocess.Popen(command")
        check = check_patch_whitespace(guard)
        write(HERE / "preflight-whitespace-001.json", check)
        inventory001 = PACKET / "evidence-inventory-001.json"
        old = json.loads(inventory001.read_text(encoding="utf8"))
        for path, digest in old["files"].items():
            assert sha((PACKET / path).read_bytes()) == digest
        structural = HERE / "author-preservation-001" / "summary.json"
        hashes = HERE / "author-preservation-001" / "runtime-hashes.json"
        write(PACKET / "pre-sign-whitespace-revision-002.json", {
            "parent": PARENT, "preservedInventory001Sha256": sha(inventory001.read_bytes()),
            "failure": {"path": str(initial), "sha256": sha(initial.read_bytes()),
                        "phase": "Pre-sign staged whitespace check, before staging receipt and before commit/GPG subprocess.",
                        "commitOrGpgProcessLaunched": False, "exitCodeField": attempt["exitCode"],
                        "initialSignerSha256": sha((HERE / "sign.py").read_bytes()),
                        "trace": "sign.py:36 -> b129_common.py:81 RuntimeError; git diff --cached --check exited2. Its stdout was not retained by the old helper, so the exact readonly check is captured separately rather than pretending the empty signer stdout was the diagnostic."},
            "whitespace": check,
            "unchangedStructuralProof": {"path": str(structural), "summarySha256": sha(structural.read_bytes()),
                                          "runtimeHashesPath": str(hashes), "runtimeHashesSha256": sha(hashes.read_bytes())},
            "payloadDisposition": "No learner, manifest, original-source, original-inventory or failed-attempt bytes changed. Only additive contributor evidence and explicit bounded patch-syntax acceptance were added.",
            "signingPolicy": "No actual GPG attempt has occurred. The resumed preflight may launch one actual owner-signing operation; on a popup stall preserve staged work and yield without retry or bypass.",
            "finalBinding": {"inventory": "evidence-inventory-002.json",
                              "changedPaths": "changed-file-inventory-002.json",
                              "validationPlan": "validation-plan-002.json"},
        })
        producer_hashes = {}
        for name in ("recover_preflight.py", "preserve_final.py", "sign_final.py"):
            path = HERE / name
            compile(path.read_text(encoding="utf8"), str(path), "exec")
            raw = path.read_bytes()
            write(PACKET / "producers" / name, raw)
            producer_hashes[name] = sha(raw)
        write(PACKET / "validation-plan-002.json", {
            "supersedesForFinalBinding": "validation-plan.json",
            "unchangedTenGateRunnerSha256": sha((HERE / "run_gates.py").read_bytes()),
            "sameSerialTenGateCommands": "validation-plan.json",
            "authorDirectories": [str(HERE / "author-gates-002"), str(HERE / "author-preservation-002")],
            "committedDirectories": [str(HERE / "committed-gates-001"), str(HERE / "committed-preservation-001")],
            "preservationProducer": "producers/preserve_final.py",
            "preservation": "Recheck all8724 current raw/runtime hashes and all9 manifest groups, unchanged original180 packet blobs and every file of both inventories. Exact equality to the initial complete structural proof carries forward ordered metadata/body/wrapper/source-canonical checks without claiming changed sources were re-read.",
            "signingProducer": "producers/sign_final.py", "producerHashes": producer_hashes,
            "preSignAcceptance": "pre-sign-whitespace-revision-002.json",
            "allEarlierPacketsLogsAndAttemptsPreserved": True,
            "snapshotBinding": "Final external handoff binds the actual serial gate/preservation/signing receipts, new final inventory and exact signed snapshot. No prospective check is claimed passed here.",
        })
        prefix = str(PACKET.relative_to(REPO)).replace("\\", "/") + "/"
        paths = {str(p.relative_to(REPO)).replace("\\", "/") for p in PACKET.rglob("*") if p.is_file()}
        paths.update({"kanji/絹.md", "kanji/虹.md", "manifest.json",
                      prefix + "changed-file-inventory-002.json", prefix + "evidence-inventory-002.json"})
        write(PACKET / "changed-file-inventory-002.json", {
            "supersedesForFinalBinding": "changed-file-inventory.json", "parent": PARENT,
            "paths": sorted(paths), "modifiedInheritedPaths": ["kanji/絹.md", "kanji/虹.md", "manifest.json"],
            "scope": "All other paths are additive reconciliation packet files. Old path inventory and every source/report/scan/failed attempt preserved.",
        })
        files = {str(p.relative_to(PACKET)).replace("\\", "/"): sha(p.read_bytes()) for p in sorted(PACKET.rglob("*")) if p.is_file()}
        write(PACKET / "evidence-inventory-002.json", {
            "packet": "batch-129-reconciliation-001", "parent": PARENT,
            "selfExcluded": "evidence-inventory-002.json",
            "supersedesForFinalBinding": "evidence-inventory-001.json",
            "files": files,
        })
        print("Preserved pre-GPG failure and all initial packet bytes; new final inventory:",
              sha((PACKET / "evidence-inventory-002.json").read_bytes()), "other files", len(files))
    finally:
        write(HERE / "recover-preflight-memory-001.json", guard.finish())


if __name__ == "__main__":
    main()
