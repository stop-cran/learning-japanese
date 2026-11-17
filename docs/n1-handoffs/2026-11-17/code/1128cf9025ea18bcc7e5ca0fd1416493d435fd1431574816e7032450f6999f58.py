"""Derive the B133 fresh-context continuation controller, collector and acceptor from frozen originals.

Each successor only imports b133_fresh_confirmation_v2 instead of b133_fresh_confirmation (and the
acceptor the derived collector); the controller additionally passes the spec to replacement_prompt so the
CONFIRM-003 continuation carries truthful attribution. Every other function is AST-identical and every
derivation is exactly reversible.
"""
import ast
import json
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen

FIRST = "from b133_fresh_confirmation import "
SECOND = "from b133_fresh_confirmation_v2 import "
DERIVATIONS = (
    ("confirm_b133_fresh.py", "confirm_b133_fresh_v2.py",
     "b39f0c79a2814b07b2ed2504112370773446512af560bc845115a42b1dc2d26e", {"render"}, [
         (FIRST + "REASON, fresh_bindings, fresh_origin, replacement_prompt\n",
          SECOND + "REASON, fresh_bindings, fresh_origin, replacement_prompt\n"),
         ("                                                     prompt_path))\n",
          "                                                     prompt_path), spec)\n"),
     ]),
    ("b133_fresh_confirmation_records.py", "b133_fresh_confirmation_records_v2.py",
     "7e0c562e5e2a66e03bf3333b28b396e9f6f689745353187c7c7addfa0477bf25", set(), [
         (FIRST + "REASON, fresh_origin\n", SECOND + "REASON, fresh_origin\n"),
     ]),
    ("accept_b133_fresh_confirmation.py", "accept_b133_fresh_confirmation_v2.py",
     "1fc16c4182a4c270998b5b08a8d927e6c195bcf4ed6e1d5153cdb1d6868866dc", set(), [
         (FIRST + "REASON\n", SECOND + "REASON\n"),
         ("from b133_fresh_confirmation_records import collect_confirmation\n",
          "from b133_fresh_confirmation_records_v2 import collect_confirmation\n"),
         ('"accept_b133_fresh_confirmation.py RUN DRAFT"', '"accept_b133_fresh_confirmation_v2.py RUN DRAFT"'),
     ]),
)


def replace_exact(text, substitutions):
    changed = text
    for before, after in substitutions:
        require(changed.count(before) == 1, "Ambiguous anchor: " + before[:70])
        changed = changed.replace(before, after)
    restored = changed
    for before, after in reversed(substitutions):
        require(restored.count(after) == 1, "Ambiguous reverse anchor: " + after[:70])
        restored = restored.replace(after, before)
    require(restored == text, "Derivation is not reversible")
    return changed


def functions(text, changed):
    return {node.name: ast.dump(node) for node in ast.parse(text).body
            if isinstance(node, ast.FunctionDef) and node.name not in changed}


def main():
    out = TOOLS.parent / "scratch-133" / "review" / "fresh-continuation-tooling-001.json"
    require(not out.exists(), "Preserve the existing preparation")
    module = TOOLS / "b133_fresh_confirmation_v2.py"
    derivations = []
    for old, new, digest, changed, edits in DERIVATIONS:
        target = TOOLS / new
        require(not target.exists(), "Preserve derived tool " + new)
        text = frozen(TOOLS / old, digest).decode("utf-8")
        newline = "\r\n" if "\r\n" in text else "\n"
        require(text.count(newline) == text.count("\n") and text.count("\r") == text.count("\r\n"),
                "Mixed newline convention: " + old)
        result = replace_exact(text, [(before.replace("\n", newline), after.replace("\n", newline))
                                      for before, after in edits])
        require(functions(text, changed) == functions(result, changed)
                and set(functions(text, set())) == set(functions(result, set())),
                "Functions outside the declared change differ: " + new)
        compile(result, new, "exec")
        derivations.append({"source": {"path": str(TOOLS / old), "sha256": digest},
                            "output": write_frozen(target, result.encode("utf-8")), "reverseExact": True,
                            "newline": "CRLF" if newline == "\r\n" else "LF",
                            "substitutions": len(edits), "changedFunctions": sorted(changed)})
    print(json.dumps(freeze_json(out, {
        "batch": 133, "derivations": derivations,
        "module": {"path": str(module), "sha256": sha(frozen(module))},
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "scope": "CONFIRM-003 continuation of the disclosed fresh-context Claude reviewer only: same session, "
                 "same capacity observation and original session, bound to its frozen CONFIRM-002 final and "
                 "adjudication; truthful continuation attribution. Report, adjudication, audit, chain, config, "
                 "admission, event prefix/slice and delivery-age bindings are unchanged.",
        "reviewerLaunched": False, "confirmationAccepted": False, "publicationAccepted": False,
    })))


if __name__ == "__main__":
    main()
