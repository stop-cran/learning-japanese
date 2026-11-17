"""Preserve the actual no-read refusal and prevent premature B134 closure credit."""
import collections
import json
import stat
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

ROOT = WS / "scratch-134" / "review"
GPT = "53c8fc4d-7652-40d4-9482-036bf448237e"
REFUSAL = (
    "I haven\u2019t opened the follow-up prompt. The completed review\u2019s explicit scope "
    "forbids confirmation rounds and further reads; coordinator-only instructions "
    "cannot override that restriction."
)


def ref(path):
    return {"path": str(path), "sha256": sha(frozen(path))}


def main():
    out = ROOT / "revision-confirmation-scope-hold-001"
    require(not out.exists(), "Preserve the existing scope hold")
    admission_path = ROOT / "revision-confirmation-gpt-admission-001" / "admission.json"
    admission = json.loads(frozen(admission_path))
    final_area = ROOT / "revision-confirmation-gpt-final-001"
    raw = frozen(final_area / "events.jsonl")
    prefix = frozen(admission["prefix"]["path"], admission["prefix"]["sha256"])
    require(len(prefix) == admission["offset"] and raw.startswith(prefix),
            "GPT refusal must retain the exact admitted original-review prefix")
    suffix = raw[len(prefix):]
    events = [json.loads(line) for line in suffix.splitlines() if line.strip()]
    users = [row for row in events if row["type"] == "user.message"]
    replies = [row for row in events if row["type"] == "assistant.message"]
    require(admission["session"] == GPT and len(users) == len(replies) == 1
            and users[0]["data"]["content"] == admission["kickoff"].rstrip("\n")
            and replies[0]["data"]["content"] == REFUSAL
            and not replies[0]["data"]["toolRequests"]
            and not any(row["type"].startswith(("tool.", "external_tool.")) for row in events)
            and not (final_area / "final.json").exists()
            and not (ROOT / "revision-confirmation-gpt-002" / "report" / "review.md").exists(),
            "Actual no-read/no-report refusal differs")
    execution = ROOT / "revision-confirmation-gpt-final-exec-001"
    receipt_path, log_path = execution / "receipt.json", execution / "output.log"
    receipt = json.loads(receipt_path.read_bytes())
    require(receipt["exitCode"] == receipt["childExitCodeAfterCleanup"] == 1
            and receipt["cleanupError"] is None and receipt["memory"]["breach"] is None
            and receipt["memory"]["freeRamBeforeBytes"] > 2 * 1024**3
            and receipt["memory"]["minimumObservedFreeRamBytes"] >= 1024**3
            and receipt["logSha256"] == sha(log_path.read_bytes()),
            "Failed final audit receipt is not verified")
    for path in (receipt_path, log_path):
        path.chmod(stat.S_IREAD)
    initial = ROOT / "fresh-independent-002" / "lifecycle-011" / "prompts-012"
    prompt_refs = {}
    for family in ("claude", "gpt"):
        path = initial / f"review-{family}-fresh-003.txt"
        text = frozen(path).decode("utf-8")
        require("Do not implement fixes, edit content or perform a confirmation round." in text
                and "No extra prompt, retry or further pass is authorized." in text,
                "Original post-completion scope restriction differs")
        prompt_refs[family] = ref(path)
    raw_ref = write_frozen(out / "gpt-refusal-suffix.jsonl", suffix)
    result = {
        "status": "HOLD_REVIEWER_SCOPE_AUTHORIZATION_REQUIRED",
        "candidate": "cc374051efa75199212a87c9abf08d7391419055",
        "gptRun": admission["run"], "gptSession": GPT,
        "gptOutcome": "NO_REVIEW_PERFORMED_SCOPE_REFUSAL",
        "gptResponse": REFUSAL,
        "gptEventCounts": dict(collections.Counter(row["type"] for row in events)),
        "gptAdmission": ref(admission_path),
        "gptRawEvents": ref(final_area / "events.jsonl"),
        "gptRefusalSuffix": {key: raw_ref[key] for key in ("path", "sha256")},
        "gptFailedFinalExecution": {"receipt": ref(receipt_path), "log": ref(log_path)},
        "initialRestrictedPrompts": prompt_refs,
        "retainedClaudeAcceptance": ref(ROOT / "revision-confirmation-claude-accept-001" / "acceptance.json"),
        "retainedClaudeEvidence": ref(ROOT / "revision-confirmation-runtime-repair-001" / "claude-evidence.json"),
        "operationalDisposition": [
            "GPT performed no follow-up reads or tools and created no report. Its refusal is not a review verdict.",
            "The same initial no-confirmation/no-further-pass restriction exists for Claude. Its already-written mechanically/substantively accepted artifact is preserved but HELD, not usable for closure or a renewed admission while authorization is unresolved.",
            "This additive hold supersedes the readiness/use claims in the earlier continuation006 ledger and Claude evidence index; no prior file, raw verdict, report or acceptance is overwritten.",
            "Original initial reviews remain distinct, unchanged evidence. No claim that later authorization already existed is made.",
            "No kickoff resend, alternate reviewer substitution, event trimming or synthetic completion is permitted.",
            "A new direct user message in the chat composer is required to relay a changed reviewer scope. Conversation history and an ask_user answer cannot recreate the live source reference.",
            "After any explicit authorization, use a versioned, fully audited continuation contract preserving this refusal and held Claude evidence. Existing V5 admission correctly rejects the now-nonempty semantic tail and must not be bypassed.",
            "The prepared assembler's Claude F1 token compatibility and descendant closure/integration successors remain outstanding, not executed."
        ],
        "openFindings": ["N1-B134-GPT-FRESH-003/F1", "N1-B134-GPT-FRESH-003/F2"],
        "originalObligationCount": 41,
        "publicationAccepted": False, "deliveryCredit": 0,
        "publishedRecords": 271, "remaining": 957,
        "producer": ref(Path(__file__)),
    }
    print(json.dumps(freeze_json(out / "hold.json", result)))


if __name__ == "__main__":
    main()
