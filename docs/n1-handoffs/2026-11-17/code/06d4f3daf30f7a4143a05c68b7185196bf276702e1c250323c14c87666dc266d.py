"""Extend B129 closure for its disclosed first-confirmation replacement."""
import json
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, review_dir, sha, write_frozen
from prepare_b129_initial_replacement import FAILED_RUN, verify_replacement

ORIGINAL = {"reviewerOrigin": "original", "replacementFor": None,
            "originalSession": None}


def confirmation_origin(spec, mechanics, launch, accepted, original, config, records,
                        kind, previous):
    require(spec["session"] == mechanics["session"], "Audited reviewer differs")
    if not any(key in spec for key in ("replayedFrom", "unavailable", "originalSession")):
        require(spec["session"] == launch["session"]
                and accepted.get("reviewerOrigin", "original") == "original",
                "Confirmation changed reviewer")
        return dict(ORIGINAL)
    require(kind == "final" and config["batch"] == 129 and spec["family"] == "claude"
            and previous is None and "prior" not in spec,
            "Only the first final Claude replacement is supported")
    verify_replacement(spec, config, original, launch, records)
    require(accepted.get("reviewerOrigin") == "fresh-context-replacement"
            and accepted.get("replacesUnavailable") == FAILED_RUN
            and accepted.get("originalSession") == launch["session"],
            "Acceptance must disclose replacement identity")
    return {"reviewerOrigin": "fresh-context-replacement", "replacementFor": FAILED_RUN,
            "originalSession": launch["session"]}


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
        raw = json.dumps(audit.get(key, []), ensure_ascii=False, sort_keys=True).encode("utf-8")
        result[key + "Count"] = len(audit.get(key, []))
        result[key + "Sha256"] = sha(raw)
    result["rawCompletionMessage"] = audit["messages"]
    return result


def replace_exact(text, substitutions):
    changed = text
    for before, after in substitutions:
        require(changed.count(before) == 1, "Ambiguous closure anchor: " + before)
        changed = changed.replace(before, after)
    restored = changed
    for before, after in reversed(substitutions):
        require(restored.count(after) == 1, "Ambiguous reverse closure anchor")
        restored = restored.replace(after, before)
    require(restored == text, "Closure derivation is not reversible")
    return changed


def prepare():
    extra_protocol = (
        '"b129_closure_revision.py", "test_b129_closure_revision.py", '
        '"close_b129_v2.py", "archive_b129_chains.py", "verify_b129_archive_v2.py", '
        '"prepare_b129_initial_replacement.py", "prepare_b129_initial_replacement_v2.py", '
        '"confirm_b129_context_replacement.py"'
    )
    identity = '''            origin = confirmation_origin(
                spec, mechanics, launch, accepted, original, config, records, kind, previous)
            if origin["reviewerOrigin"] == "fresh-context-replacement":
                failure = read(Path(spec["unavailable"]["path"]), spec["unavailable"]["sha256"])
                held_prefix = f"held-runs/{failure['run']}"
                binding(spec["unavailable"], f"{held_prefix}/failure.json")
                binding(spec["replayedFrom"], f"{held_prefix}/spec.json")
                binding(failure["context"], f"{held_prefix}/context.json")
                held_audit = read(Path(failure["audit"]["path"]), failure["audit"]["sha256"])
                dump(f"{held_prefix}/audit-summary.json",
                     bounded_void(held_audit, failure["audit"]["sha256"]))
                for suffix in ("preflight", "admission", "config"):
                    copy(records / "confirm" / f"{failure['run']}-{suffix}.json",
                         f"{held_prefix}/{suffix}.json")
                held_config = read(records / "confirm" / f"{failure['run']}-config.json")
                for field in ("prompt", "kickoff"):
                    copy(Path(held_config[field]), f"{held_prefix}/{field}.txt")
                held_chains = [chain(Path(held_config["chainManifest"]), f"{held_prefix}/chain")]
                excluded_confirmations.append({
                    "run": failure["run"], "session": failure["session"],
                    "candidate": failure["candidate"], "status": failure["status"],
                    "reviewEvidenceAccepted": False, "confirmationAccepted": False,
                    "reportWritten": False, "linguisticVerdict": None, "chains": held_chains,
                    "auditSha256": failure["audit"]["sha256"],
                })'''
    substitutions = [
        ("from archive_b124_chains_v2 import prepare as prepare_public_chain",
         "from archive_b129_chains import prepare as prepare_public_chain\n"
         "from b129_closure_revision import ORIGINAL, bounded_void, confirmation_origin"),
        ("    contents, lineage = {}, []",
         "    contents, lineage, excluded_confirmations = {}, [], []"),
        ('        prefix = f"runs/{run}"',
         '        prefix = f"runs/{run}"\n        origin = dict(ORIGINAL)'),
        ('            require(spec["session"] == mechanics["session"] == launch["session"],\n'
         '                    "Confirmation changed reviewer")', identity),
        ('                        "role": kind, "priorRun": previous if confirmation else None,',
         '                        "role": kind, **origin, "priorRun": previous if confirmation else None,'),
        ('"test_b129_external_sources.py"):', '"test_b129_external_sources.py", ' + extra_protocol + '):'),
        ('"reviewLineage": lineage, "excludedInitialRuns": excluded,',
         '"reviewLineage": lineage, "excludedInitialRuns": excluded,\n'
         '            "excludedConfirmationRuns": excluded_confirmations,'),
        ('"the original reviewer, its own report, the actual runtime delta and "',
         '"the original reviewer where available; the explicitly attributed Claude replacement "\n'
         '                            "uses the unchanged original report, actual runtime delta and "'),
        ('"neither accepted nor unaccepted earlier snapshots are final acceptance of this revision.",',
         '"neither accepted nor unaccepted earlier snapshots are final acceptance of this revision. "\n'
         '                            "The executed compacted first confirmation remains VOID, reportless "\n'
         '                            "and excluded from teaching evidence and acceptance.",'),
    ]
    sources = [
        ("close_b129.py", "close_b129_v2.py",
         "a3f8e53f30f29c3e80c2f846e869a70f363641d4554771d7157ba8d02d004f51", substitutions),
        ("archive_b124_chains_v2.py", "archive_b129_chains.py", None, [
            ('    return (source.startswith("evidence/external-snapshots/")\n'
             '            and source != "evidence/external-snapshots/manifest.json")',
             '    return ((source.startswith("evidence/external-snapshots/")\n'
             '             and source != "evidence/external-snapshots/manifest.json")\n'
             '            or source.startswith(("external-reconciliation/", "original-source-sections/")))'),
        ]),
        ("verify_b129_archive.py", "verify_b129_archive_v2.py", None, [
            ("from archive_b124_chains_v2 import is_local_only_source",
             "from archive_b129_chains import is_local_only_source"),
            ('        for review in provenance["reviewLineage"]:',
             '        for review in (provenance["reviewLineage"]\n'
             '                       + provenance["excludedConfirmationRuns"]):'),
            ('"Verifies the actual closure files and known external-snapshot labels. "',
             '"Verifies actual accepted and held closure chains, including B129 complete-source labels. "'),
        ]),
    ]
    derivations = []
    for old, new, digest, edits in sources:
        raw = frozen(TOOLS / old, digest)
        text = raw.decode("utf-8")
        newline = "\r\n" if "\r\n" in text else "\n"
        edits = [(before.replace("\n", newline), after.replace("\n", newline))
                 for before, after in edits]
        result = replace_exact(text, edits).encode("utf-8")
        compile(result, new, "exec")
        derivations.append({
            "source": {"path": str(TOOLS / old), "sha256": sha(raw)},
            "output": write_frozen(TOOLS / new, result), "reverseExact": True,
            "substitutions": [{"before": before, "after": after} for before, after in edits],
        })
    print(json.dumps(freeze_json(review_dir(129) / "closure-v2-derivation.json", {
        "derivations": derivations,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "Tool preparation only; final acceptance is still required. Original tools, "
                  "executed VOID context, reports and sources are not rewritten. Complete external "
                  "articles remain local, including all co-located material.",
    })))


if __name__ == "__main__":
    prepare()
