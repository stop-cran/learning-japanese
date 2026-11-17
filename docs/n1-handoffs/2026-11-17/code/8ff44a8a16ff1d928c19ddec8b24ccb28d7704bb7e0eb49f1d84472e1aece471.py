"""Bind the post-signing recovery supplements without changing the frozen v1."""
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen
from verify_b128_reconciliation import REVIEW


RESUME_CHECK = '''
def check_resume(directory, candidate):
    expected = {"handoff.json", "identity-signature.log", "operation.log",
                "execution-receipt.json", "resume-evidence.json", "resume-memory.json"}
    require({path.name for path in directory.iterdir()} == expected, "Handoff directory differs")
    evidence_raw = pin(directory / "resume-evidence.json",
                       "2c66492989abb6380444bd4c378ea06680730eab867cecfdc93b6a1366ad0c93")
    memory_raw = pin(directory / "resume-memory.json",
                     "041250032fdb852bbf840db872c71153f2dad61df3bee11672dc8bc741de6ca9")
    evidence = json.loads(evidence_raw)
    require(evidence["successor"] == candidate and evidence["authorizedRetryCount"] == 1
            and evidence["originalFailedAttemptPreserved"] is True
            and evidence["finalClean"] is True and memory_ok(json.loads(memory_raw)),
            "Recovery supplement scope or RAM evidence differs")
    names = {"reconciliation-sign-001/execution-receipt.json",
             "reconciliation-sign-002/result.json", "reconciliation-sign-002/execution-receipt.json",
             "reconciliation-retry-preflight-001.json", "reconciliation-stage-001/index-verification.json",
             "reconciliation-handoff-001/handoff.json"}
    require(set(evidence["bindings"]) == names, "Recovery binding inventory differs")
    bound = {}
    for name, item in evidence["bindings"].items():
        path = SCRATCH / name
        require(Path(item["path"]) == path, "Recovery binding path differs")
        bound[name] = json.loads(pin(path, item["sha256"]))
    result = bound["reconciliation-sign-002/result.json"]
    require(result["mode"] == "sign" and result["successor"] == candidate
            and result["parent"] == PARENT and result["publishedBase"] == BASE
            and result["clean"] is True and result["signatureStatus"] == "G"
            and result["signingFingerprint"] == result["primaryFingerprint"] == FINGERPRINT,
            "Recovery signed result differs")
    for attempt in ("001", "002"):
        receipt = bound[f"reconciliation-sign-{attempt}/execution-receipt.json"]
        require(receipt["mode"] == "sign" and memory_ok(receipt["memory"])
                and receipt["waitTimeoutSeconds"] == 0.1
                and receipt["cleanupTimeoutSecondsPerStage"] == 10
                and receipt["cleanupError"] is None
                and receipt["producerSha256"] == PRODUCER_SHAS["finish_reconciliation.py"],
                "Recovery signing execution differs")
        if attempt == "002":
            require(receipt["childExitCode"] == 0 and receipt["activeError"] is None,
                    "Signing retry did not succeed")
        else:
            require(receipt["childExitCode"] == 1
                    and receipt["activeError"].startswith("Deadline reached."),
                    "Original signing failure was relabeled")
    require(evidence["budgetLog"].encode("utf-8") == pin(COMMITTED_GATES / "budget.log"),
            "Recovery budget differs from committed gate")
    return {"evidenceSha256": sha(evidence_raw), "memorySha256": sha(memory_raw),
            "bindings": evidence["bindings"], "authorizedRetryCount": 1,
            "originalFailedAttemptPreserved": True}


'''


def main():
    source = TOOLS / "verify_b128_reconciliation.py"
    original = frozen(source, "c79bb4d0e1967e91640ef89100ec8cec32c8c02f6f5c24e41d384d40ef85a248")
    replacements = [
        ("def check_handoff(handoff, handoff_path, candidate, owner, repo, config):",
         RESUME_CHECK + "def check_handoff(handoff, handoff_path, candidate, owner, repo, config):"),
        ('    require({path.name for path in directory.iterdir()}\n'
         '            == {"handoff.json", "identity-signature.log", "operation.log", "execution-receipt.json"},\n'
         '            "Handoff directory differs")',
         '    resume = check_resume(directory, candidate)'),
        ('            and len(handoff["limits"]) == 5 and all(handoff["limits"]), "Handoff fields differ")',
         '            and len(handoff["limits"]) == 5 and all(handoff["limits"]), "Handoff fields differ")\n'
         '    return resume'),
        ('        check_handoff(handoff, handoff_path, candidate, owner, repo, config)',
         '        resume = check_handoff(handoff, handoff_path, candidate, owner, repo, config)'),
        ('        "handoffSha256": handoff_sha, "addedDirectGuards": ADDED_GUARDS, "totalDirectGuards": 17,',
         '        "handoffSha256": handoff_sha, "addedDirectGuards": ADDED_GUARDS, "totalDirectGuards": 17,\n'
         '        "resumeEvidence": resume,'),
    ]
    require(original.count(b"\r\n") == original.count(b"\n"), "Frozen verifier line endings changed")
    replacements = [(before.replace("\n", "\r\n"), after.replace("\n", "\r\n"))
                    for before, after in replacements]
    derived = original.decode("utf-8")
    for before, after in replacements:
        require(derived.count(before) == 1, "Frozen verifier replacement is ambiguous")
        derived = derived.replace(before, after)
    restored = derived
    for before, after in reversed(replacements):
        require(restored.count(after) == 1, "Verifier reversal is ambiguous")
        restored = restored.replace(after, before)
    require(restored.encode("utf-8") == original, "Verifier derivation is not exactly reversible")
    compile(derived, "verify_b128_reconciliation_v2.py", "exec")
    target = write_frozen(TOOLS / "verify_b128_reconciliation_v2.py", derived.encode("utf-8"))
    print(freeze_json(REVIEW / "reconciliation-verifier-v2-derivation.json", {
        "source": {"path": str(source), "sha256": sha(original)}, "output": target,
        "reverseExact": True,
        "reason": "The author added two recovery supplements after v1 was frozen. Require their exact "
                  "six-file directory, pinned bytes, successful single signing retry, preserved original "
                  "timeout, complete bindings, committed budget and unchanged RAM limits. All v1 "
                  "handoff, source, signature, content, gate and preservation checks remain unchanged.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    }))


if __name__ == "__main__":
    main()
