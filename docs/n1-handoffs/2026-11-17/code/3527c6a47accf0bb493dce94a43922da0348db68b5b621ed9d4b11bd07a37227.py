"""Derive fresh-context B133 confirmation acceptance and collection from the frozen originals.

Only reviewer identity changes: the confirmation session must differ from, and explicitly disclose,
the original accepted reviewer and the frozen capacity observation. Every other binding is unchanged.
"""
import json
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen

RECORDS = (
    "b133_confirmation_records.py", "b133_fresh_confirmation_records.py",
    "408838d3ce1bcecc98b58195eba56907c52ecbcea897e3990a114b224c642598", [
        ("from common import json_bytes, require, sha\n",
         "from common import json_bytes, require, sha\n"
         "from b133_fresh_confirmation import REASON, fresh_origin\n"),
        ('    require(spec["family"] == initial_spec["family"] and spec["session"] == initial_spec["session"],\n'
         '            "Confirmation must use the original accepted reviewer")\n',
         '    require(spec["family"] == initial_spec["family"]\n'
         '            and spec["reviewerOrigin"] == "fresh-context-replacement"\n'
         '            and spec["originalSession"] == initial_spec["session"] != spec["session"],\n'
         '            "Fresh confirmation must disclose the original accepted reviewer")\n'),
        ('    preflight = checked_json(spec["preflight"], read)\n',
         '    preflight = checked_json(spec["preflight"], read)\n'
         '    observation = checked_json(preflight["contextObservation"], read)\n'
         '    require(fresh_origin({"family": spec["family"], "run": spec["run"], "session": spec["session"],\n'
         '                          "candidate": spec["snapshot"], "originalSession": spec["originalSession"],\n'
         '                          "contextObservation": preflight["contextObservation"]})\n'
         '            and observation["originalSession"] == spec["originalSession"]\n'
         '            and all(record["originalSession"] == spec["originalSession"]\n'
         '                    and record["replacementReason"] == REASON for record in (preflight, final))\n'
         '            and acceptance["reviewerOrigin"] == spec["reviewerOrigin"]\n'
         '            and acceptance["originalSession"] == spec["originalSession"]\n'
         '            and acceptance["replacementReason"] == REASON\n'
         '            and acceptance["contextObservation"] == preflight["contextObservation"],\n'
         '            "Fresh-context origin is not disclosed throughout")\n'),
        ('        "auditConfig": preflight["config"], "initialAcceptance": initial_refs["acceptance"],\n',
         '        "auditConfig": preflight["config"], "initialAcceptance": initial_refs["acceptance"],\n'
         '        "contextObservation": preflight["contextObservation"],\n'),
    ])
ACCEPT = (
    "accept_b133_confirmation.py", "accept_b133_fresh_confirmation.py",
    "f6ec9ce8d9415b878743864661807de04842c6f9e38594f6b29c88ebd1836f0d", [
        ('"""Persist an independently authored B133 confirmation adjudication only after all real bindings pass."""',
         '"""Persist a fresh-context B133 confirmation adjudication only after all real bindings pass."""'),
        ("from b133_confirmation_records import collect_confirmation\n",
         "from b133_fresh_confirmation import REASON\n"
         "from b133_fresh_confirmation_records import collect_confirmation\n"),
        ('    session = INITIALS[family]["session"]\n', '    original = INITIALS[family]["session"]\n'),
        ('    require(preflight["session"] == final["session"] == session and final["candidate"] == candidate,\n'
         '            "Confirmation identity differs")\n',
         '    session = preflight["session"]\n'
         '    require(final["session"] == session != original and final["candidate"] == candidate\n'
         '            and preflight["originalSession"] == final["originalSession"] == original\n'
         '            and preflight["replacementReason"] == final["replacementReason"] == REASON,\n'
         '            "Fresh confirmation identity differs")\n'),
        ('        "run": run, "batch": 133, "candidate": candidate, "session": session,\n',
         '        "run": run, "batch": 133, "candidate": candidate, "session": session,\n'
         '        "reviewerOrigin": "fresh-context-replacement", "originalSession": original,\n'
         '        "replacementReason": REASON, "contextObservation": preflight["contextObservation"],\n'),
        ('        "acceptanceLimit": "One original reviewer\'s bounded confirmation, not publication or whole-set acceptance.",\n',
         '        "acceptanceLimit": "One same-family fresh-context bounded confirmation, attributed separately from "\n'
         '                           "the original reviewer; not publication or whole-set acceptance.",\n'),
        ('        "family": family, "role": "confirmation", "run": run, "session": session,\n',
         '        "family": family, "role": "confirmation", "run": run, "session": session,\n'
         '        "reviewerOrigin": "fresh-context-replacement", "originalSession": original,\n'),
        ('    require(len(sys.argv) == 3, "accept_b133_confirmation.py RUN DRAFT")\n',
         '    require(len(sys.argv) == 3, "accept_b133_fresh_confirmation.py RUN DRAFT")\n'),
    ])


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


def main():
    out = TOOLS.parent / "scratch-133" / "review" / "fresh-acceptance-tooling-001.json"
    require(not out.exists(), "Preserve the existing preparation")
    derivations = []
    for old, new, digest, edits in (RECORDS, ACCEPT):
        target = TOOLS / new
        require(not target.exists(), "Preserve derived tool " + new)
        text = frozen(TOOLS / old, digest).decode("utf-8")
        newline = "\r\n" if "\r\n" in text else "\n"
        edits = [(a.replace("\n", newline), b.replace("\n", newline)) for a, b in edits]
        result = replace_exact(text, edits).encode("utf-8")
        compile(result, new, "exec")
        derivations.append({"source": {"path": str(TOOLS / old), "sha256": digest},
                            "output": write_frozen(target, result), "reverseExact": True,
                            "substitutions": len(edits)})
    print(json.dumps(freeze_json(out, {
        "batch": 133, "derivations": derivations,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "scope": "Fresh-context reviewer identity, disclosed original session, replacement reason and frozen "
                 "capacity observation only. Report, adjudication, audit, chain, config, admission, event "
                 "prefix/slice and delivery-age bindings are unchanged.",
        "confirmationAccepted": False, "publicationAccepted": False,
    })))


if __name__ == "__main__":
    main()
