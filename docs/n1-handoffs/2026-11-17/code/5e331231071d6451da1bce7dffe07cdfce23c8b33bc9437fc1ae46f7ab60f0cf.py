"""Verify the bounded direct-pair correction after B119 CONFIRM-001."""
import difflib
import json
import sys
from pathlib import Path

from common import WS, freeze_json, frozen, git, load_batch, require, sha, start_guard
from confirm_v2 import binding, clean
from verify_b119_revision import parse, verify_gates

PRIOR = "14662814559b9cb969bcb5768643748758cefffe"
PROOF_SHA = "978eff583554f9778a5e30ae14dc55db34f39f6e75d398ea8b1490a43fc92ddb"
SUPPLEMENT_SHA = "28163cdcfe8462baa49284c4a55294f828d3b7e1ddcb3f2c75b44f09b9472e83"
PREFIX = "docs/n1-sources/batch-119/reconciliation-003/"


def verify_pair_change(before, after):
    old, old_body = parse(before)
    new, new_body = parse(after)
    require({k: v for k, v in old.items() if k != "quiz_exclusions"}
            == {k: v for k, v in new.items() if k != "quiz_exclusions"},
            "Preserved metadata changed")
    require("丸" not in old["quiz_exclusions"]
            and new["quiz_exclusions"] == [*old["quiz_exclusions"], "丸"],
            "The only exclusion change must append the direct 丸 pair")
    changes = [(a, b, c, d) for tag, a, b, c, d in difflib.SequenceMatcher(
        a=old_body.splitlines(), b=new_body.splitlines(), autojunk=False).get_opcodes()
        if tag != "equal"]
    if changes:
        require(len(changes) == 1, "More than one comparison passage changed")
        a, b, c, d = changes[0]
        old_lines, new_lines = old_body.splitlines(), new_body.splitlines()
        require(b - a <= 1 and d - c == 1
                and old_lines.index("## Notes") < a < len(old_lines) - 1
                and "[丸](丸.md)" in new_lines[c]
                and (a == b or "[円](円.md)" in old_lines[a]),
                "Change extends beyond the qualified 円/丸 comparison")
    return {"addedGuard": "丸", "changedBodyPassages": len(changes)}


def verify(candidate, gates, output):
    config = load_batch(119)
    clean(config, candidate)
    require(git(config, "show", "-s", "--format=%P", candidate).decode().strip() == PRIOR,
            "Follow-up must directly descend from the prior confirmation snapshot")
    records = WS / "scratch-119" / "review"
    proof_path = records / "revision-verification-002.json"
    supplement_path = records / "revision-supplement-verification-002.json"
    previous = json.loads(frozen(proof_path, PROOF_SHA))
    supplemental = json.loads(frozen(supplement_path, SUPPLEMENT_SHA))
    require(previous["candidate"] == supplemental["candidate"] == PRIOR
            and previous["status"] == supplemental["status"] == "PASS"
            and not previous["memory"]["breach"] and not supplemental["memory"]["breach"],
            "Prior verified evidence differs")
    guard, _ = start_guard("B119 bounded follow-up verification")
    try:
        changes = git(config, "diff", "--name-status", "--no-renames", PRIOR, candidate
                      ).decode().splitlines()
        docs = []
        runtime_changes = set()
        for line in changes:
            status, path = line.split("\t")
            if path.startswith(PREFIX):
                require(status == "A", "Existing reconciliation evidence was modified")
                docs.append(path)
            else:
                require(status == "M" and path in ("kanji/妥.md", "manifest.json"),
                        f"Unexpected correction: {line}")
                runtime_changes.add(path)
        require(runtime_changes == {"kanji/妥.md", "manifest.json"} and docs,
                "Missing correction or source evidence")
        blob = lambda revision, path: git(config, "show", f"{revision}:{path}")
        card = blob(candidate, "kanji/妥.md")
        pair = verify_pair_change(blob(PRIOR, "kanji/妥.md").decode(), card.decode())
        raw_manifest = blob(candidate, "manifest.json")
        manifest, old_manifest = json.loads(raw_manifest), json.loads(blob(PRIOR, "manifest.json"))
        runtime = lambda value: {p: h for entries in value.values() if isinstance(entries, dict)
                                 for p, h in entries.items()}
        current, old = runtime(manifest), runtime(old_manifest)
        require(current.keys() == old.keys()
                and {p for p in old if current[p] != old[p]} == {"kanji/妥.md"}
                and current["kanji/妥.md"] == sha(card), "Unexpected runtime manifest delta")
        receipts = verify_gates(gates, raw_manifest, config, guard)
        evidence = {}
        for path in docs:
            raw = blob(candidate, path)
            require(frozen(Path(config["repo"]) / path) == raw,
                    f"New evidence differs from its signed blob: {path}")
            evidence[path] = sha(raw)
            guard.check()
        result = {
            **previous, "candidate": candidate, "prior": PRIOR,
            "manifestSha256": sha(raw_manifest), "contentVersion": manifest["contentVersion"],
            "runtimeEntries": len(current), "gates": receipts,
            "priorVerification": binding(proof_path), "priorSupplement": binding(supplement_path),
            "boundedDelta": pair, "newEvidenceSha256": evidence,
            "oldEvidencePreserved": True,
            "verificationScope": "Signed direct-child delta, exact metadata and old-source "
                                 "preservation, single direct guard and bounded passage, "
                                 "runtime hashes and ten fresh gates. Semantic adjudication "
                                 "and final publication remain separate.",
        }
    finally:
        memory = guard.finish()
    require(not memory["breach"], "Follow-up RAM guard breached")
    result["memory"] = memory
    print(json.dumps(freeze_json(output, result)))


if __name__ == "__main__":
    verify(sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]))
