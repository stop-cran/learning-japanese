"""Freeze the final B134 fresh-independent preparation handoff."""
import json
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
FINAL = ROOT / "fresh-independent-002" / "projected-successor-007"
PROTOCOL = FINAL / "protocol-002"
sys.path.insert(0, str(WS / "review-tools"))
from common import require, sha, write_frozen


def bound(path):
    raw = path.read_bytes()
    return {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}


def main():
    capacity_path = FINAL / "capacity-measurement-001.json"
    completeness_path = FINAL / "source-completeness-verification-002.json"
    packet_proof_path = ROOT / "packet-verification-001" / "verification.json"
    capacity = json.loads(capacity_path.read_text(encoding="utf-8"))
    completeness = json.loads(completeness_path.read_text(encoding="utf-8"))
    packet_proof = json.loads(packet_proof_path.read_text(encoding="utf-8"))
    test_receipt = ROOT / "fresh-002-test-007" / "receipt.json"
    verify_receipt = ROOT / "fresh-002-verify-002" / "receipt.json"
    require(completeness["status"] == "PASS_COMPLETE_SOURCE_AND_PACKET_INTEGRITY"
            and capacity["decision"] == "HOLD_ESTIMATE"
            and packet_proof["status"] == "PASS",
            "Final proof, packet proof, or capacity decision differs")
    require(sha(packet_proof_path.read_bytes())
            == "fb95e655419fe9ecc0465ac565fb309397fb8843c22362b08cf5a1feda4d478a",
            "Coordinator packet proof is not the bound proof")
    require(json.loads(test_receipt.read_text(encoding="utf-8"))["exitCode"] == 0
            and json.loads(verify_receipt.read_text(encoding="utf-8"))["exitCode"] == 0,
            "Guarded test or verifier receipt did not pass")
    tiers = []
    for full, projected in zip(capacity["completeRecordTrial"]["trials"], capacity["trials"]):
        require(full["caps"] == projected["caps"], "Capacity tier ordering differs")
        tiers.append({
            "caps": full["caps"],
            "completeRecordStartupForecast": full["startupForecast"],
            "completeRecordExcess": full["excess"],
            "projectedStartupForecast": projected["startupForecast"],
            "projectedExcess": projected["excess"],
            "outcome": projected["outcome"],
        })
    files = {
        "packetInventory": FINAL / "packet" / "SHA256SUMS.json",
        "coreManifest": FINAL / "fresh-independent-core-001.json",
        "capacity": capacity_path,
        "sourceCompletenessProof": completeness_path,
        "coordinatorPacketProof": packet_proof_path,
        "protocol": PROTOCOL / "PROTOCOL.txt",
        "protocolController": PROTOCOL / "fresh-review-protocol-002.py",
        "protocolTests": PROTOCOL / "test-fresh-review-protocol-002.py",
        "claudeAuditConfig": PROTOCOL / "audit-claude-002.json",
        "gptAuditConfig": PROTOCOL / "audit-gpt-002.json",
        "initialPrompt": FINAL / "prompts-002" / "initial-review-002.txt",
        "kickoffPrompt": FINAL / "prompts-002" / "kickoff-fresh-review-002.txt",
        "sourceVerifier": WS / "scratch-134" / "review" / "fresh-independent-002" / "tools"
                         / "verify_fresh_independent_002.py",
        "testReceipt": test_receipt,
        "verificationReceipt": verify_receipt,
    }
    handoff = {
        "status": "PREPARED_NOT_ADMITTED",
        "candidate": completeness["candidate"],
        "parent": completeness["base"],
        "reviewerAdmission": "HOLD_ESTIMATE; no reviewer launched and no core delivered",
        "files": {name: bound(path) for name, path in files.items()},
        "packetProofAssertions": {
            "signedInventoryFiles": 215,
            "originalJmdict": 399, "supplementalJmdict": 194,
            "canonicalEqualJmdictOverlaps": 71, "uniqueJmdictFamilies": 522,
            "originalKanjidic2": 59, "supplementalKanjidic2": 37,
            "canonicalEqualKanjidic2Overlaps": 11, "uniqueKanjidic2Records": 85,
            "targetDictionaryEntries": 115, "comparisonReadbacks": 53,
            "readbackJmdictEntries": 227, "finiteBaselinePairs": 53, "newPairs": 0,
            "localHistoryFiles": 227, "authorGateFiles": 44,
            "externalCaptures": 2, "boundedExcerpts": 6,
            "fontCodePoints": 74, "missingInAllThreeFonts": "U+8308",
            "progressAccounting": {"credited": 271, "remaining": 957},
            "assertedBy": packet_proof["verifierSha256"],
        },
        "sourceCompleteness": completeness,
        "selectionProvenance": {
            "originalPredicates": 182, "originalZeroMatches": 6,
            "supplementalPredicates": 140, "supplementalZeroMatches": 5,
            "indexedPredicates": 322, "supplementalMembershipRows": 194,
        },
        "core": {
            "sources": completeness["coreChain"]["sources"],
            "segments": completeness["coreChain"]["segments"],
            "bytes": completeness["coreChain"]["totalSegmentBytes"],
            "candidateArticles": completeness["candidateArticleCount"],
            "excludedCounterparts": 56,
        },
        "capacity": {
            "startupGate": capacity["startupGate"],
            "bootstrapAllowance": capacity["bootstrapTokens"],
            "reportAllowance": capacity["reportTokens"],
            "optionalAllowance": capacity["optionalUnitAllowance"],
            "largestOptionalUnitForecastTokens": capacity["largestOptionalUnitTokens"],
            "completeRecordCoreTokens": capacity["completeRecordTrial"]["coreTokens"],
            "projectedCoreTokens": capacity["coreTokens"],
            "tiers": tiers,
            "chosenCaps": None,
            "forecastsAreTokenMeasurements": False,
        },
        "reviewerProfiles": {
            "claude": {"selectedModel": "claude-opus-5.5", "contextTier": "long_context",
                       "maxPromptTokens": 952000, "prePhase2Gate": 740000},
            "gpt": {"selectedModel": "gpt-6.1-sol", "contextTier": "long_context",
                    "maxPromptTokens": 922000, "prePhase2Gate": 710000},
            "admissionRequires": ["actual selectedModel", "explicit contextTier",
                                  "exact maxPromptTokens telemetry", "zero compaction",
                                  "one prompt-only bootstrap read and wait"],
        },
        "changesFromB133Precedent": [
            "Kept serial two-phase D/E/optional selection and the exact existing cap order.",
            "Merged original and supplemental dictionaries only after full-record canonical equality.",
            "Added complete-record-first measurement and only the prescribed KANJIDIC2 field projection.",
            "Bound the revised candidate, complete source/index evidence, 56 exclusions, and packet proof.",
            "Added prompt-only bootstrap admission against actual runtime telemetry and a persisted event-hash record.",
            "Reused the existing B134 two-phase audit mechanics; no other source reduction or cap was introduced.",
        ],
        "commands": {
            "focusedTests": (
                'python -B "C:\\Users\\stop-\\n1-kanji-workspace\\scratch-134\\review\\guarded-test-v3.py" '
                '"C:\\Users\\stop-\\n1-kanji-workspace\\scratch-134\\review\\fresh-002-test-007" '
                'python -B "C:\\Users\\stop-\\n1-kanji-workspace\\scratch-134\\review\\fresh-independent-002\\'
                'projected-successor-007\\protocol-002\\test-fresh-review-protocol-002.py"'
            ),
            "sourceCompleteness": (
                'python -B "C:\\Users\\stop-\\n1-kanji-workspace\\scratch-134\\review\\guarded-test-v3.py" '
                '"C:\\Users\\stop-\\n1-kanji-workspace\\scratch-134\\review\\fresh-002-verify-002" '
                'python -B "C:\\Users\\stop-\\n1-kanji-workspace\\scratch-134\\review\\fresh-independent-002\\'
                'tools\\verify_fresh_independent_002.py"'
            ),
            "bootstrap": (
                'python -B "C:\\Users\\stop-\\n1-kanji-workspace\\scratch-134\\review\\fresh-independent-002\\'
                'projected-successor-007\\protocol-002\\fresh-review-protocol-002.py" bootstrap '
                '--family <claude|gpt> --events "<actual-session-events.jsonl>" '
                '--config "<matching-frozen-audit-config.json>" --output "<new-bootstrap-record.json>"'
            ),
            "authorizeCore": (
                'python -B "C:\\Users\\stop-\\n1-kanji-workspace\\scratch-134\\review\\fresh-independent-002\\'
                'projected-successor-007\\protocol-002\\fresh-review-protocol-002.py" authorize-core '
                '--bootstrap "<PASS_BOOTSTRAP_WAIT.json>" --events "<same-actual-session-events.jsonl>"'
            ),
        },
        "limitations": [
            "Every allowed D/E cap exceeds the 700000 startup gate, even after the prescribed KD projection.",
            "HOLD_ESTIMATE forbids prompt-to-core evidence delivery; bootstrap readiness is not core admission.",
            "No reviewer was launched, no teaching was edited, and no semantic verdict or acceptance is claimed.",
            "Forecasts are conservative estimates, not actual token usage; a future changed packet needs a new measurement and proof.",
            "Coordinator owns the independent fresh-review admission and actual live-session telemetry checks.",
        ],
    }
    output = FINAL / "preparation-handoff-002.json"
    print(json.dumps(write_frozen(output, (json.dumps(handoff, ensure_ascii=False, indent=2) + "\n").encode()),
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
