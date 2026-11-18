"""Preserve a failed audit whose unexpected-user-message field is a count."""
import json
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, review_dir, sha, write_frozen
from b129_closure_revision import replace_exact


def bounded_void(audit, expected_sha):
    require(audit["status"] == "VOID" and audit["reviewerIdle"]
            and audit["writes"] == audit["readbacks"] == 0
            and audit["messages"] == ["UNVERIFIED"], "Unexpected failed execution")
    fields = ("session", "eventsSha256", "eventsBytes", "eventsCount", "sliceSha256",
              "sliceBytes", "offset", "prefixSha256", "status", "actualResponseModels",
              "reviewerIdle", "recordIncomplete", "chainRead", "chainRequired",
              "writes", "readbacks", "readbackVerified", "fetches")
    result = {key: audit[key] for key in fields if key in audit}
    result.update(originalAuditSha256=expected_sha, rawExecutionPayloadsRemainLocal=True,
                  reviewEvidenceAccepted=False, confirmationAccepted=False)
    for key in ("breaches", "notes", "unexpectedUserMessages"):
        value = audit.get(key, [])
        require(isinstance(value, list) or type(value) is int and value >= 0,
                "Unsupported audit count: " + key)
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True).encode("utf-8")
        result[key + "Count"] = value if type(value) is int else len(value)
        result[key + "Sha256"] = sha(raw)
    result["rawCompletionMessage"] = audit["messages"]
    return result


def prepare():
    source = TOOLS / "close_b129_v2.py"
    raw = frozen(source)
    text = raw.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    edits = [
        ("from b129_closure_revision import ORIGINAL, bounded_void, confirmation_origin",
         "from b129_closure_revision import ORIGINAL, confirmation_origin\n"
         "from b129_closure_void import bounded_void"),
        ('"confirm_b129_context_replacement.py"):',
         '"confirm_b129_context_replacement.py", "close_b129_v3.py", '
         '"b129_closure_void.py", "test_b129_closure_void.py"):'),
    ]
    edits = [(before.replace("\n", newline), after.replace("\n", newline)) for before, after in edits]
    derived = replace_exact(text, edits).encode("utf-8")
    compile(derived, "close_b129_v3.py", "exec")
    print(freeze_json(review_dir(129) / "closure-v3-derivation.json", {
        "source": {"path": str(source), "sha256": sha(raw)},
        "output": write_frozen(TOOLS / "close_b129_v3.py", derived), "reverseExact": True,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "scope": "Preserve actual audit count fields without treating integers as lists. "
                 "V2 was never executed to produce closure. No acceptance or review rule changed.",
    }))


if __name__ == "__main__":
    prepare()
