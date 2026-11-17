"""Correct cumulative guard accounting without rewriting the reviewed receipt."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent
original = frozen(HERE / "verify_b119_followup.py",
                  "5e331231071d6451da1bce7dffe07cdfce23c8b33bc9437fc1ae46f7ab60f0cf")
anchor = '            "boundedDelta": pair, "newEvidenceSha256": evidence,\n'
replacement = anchor + (
    '            "addedGuards": {\n'
    '                character: sorted(set(parse(blob(candidate, f"kanji/{character}.md").decode())[0]\n'
    '                                      ["quiz_exclusions"])\n'
    '                                  - set(parse(blob(config["candidate"], f"kanji/{character}.md").decode())[0]\n'
    '                                        ["quiz_exclusions"]))\n'
    '                for character in config["members"]},\n'
    '            "verifierTool": binding(Path(__file__)),\n'
    '            "supersedes": binding(records / "revision-verification-003.json"),\n'
    '            "correction": "The earlier addedGuards field was inherited from the prior proof; "\n'
    '                          "this receipt recomputes cumulative guards from the actual signed cards. "\n'
    '                          "The earlier boundedDelta and runtime/card verification were correct.",\n'
)
text = original.decode()
newline = "\r\n" if "\r\n" in text else "\n"
anchor = anchor.replace("\n", newline)
replacement = replacement.replace("\n", newline)
require(text.count(anchor) == 1, "Correction anchor changed")
updated = text.replace(anchor, replacement, 1)
require(updated.replace(replacement, anchor, 1).encode() == original, "Reverse delta differs")
compile(updated, "verify_b119_followup_v2.py", "exec")
result = write_frozen(HERE / "verify_b119_followup_v2.py", updated.encode())
out = WS / "scratch-119" / "review" / "confirm"
write_frozen(out / "verify_b119_followup_v2.py", updated.encode())
write_frozen(out / "derive_b119_followup_verifier_v2.py", frozen(Path(__file__)))
print(json.dumps(freeze_json(out / "guard-inventory-tool-correction.json", {
    "originalSha256": sha(original), "correctedTool": result, "reverseExact": True,
    "reason": "Claude CONFIRM-002 L2 identified inherited addedGuards omitting the new 丸 guard.",
    "reviewedInputPreserved": True,
})))
