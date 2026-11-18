"""Tighten B133 publication retention after the preserved dry-run overlap failure."""
from common import TOOLS, WS, freeze_json, frozen, sha, write_frozen
from derive_b133_closure_recorders_v2 import replace


def main():
    original = frozen(TOOLS / "close_b133_v2.py")
    raw = replace(original, "from b133_closure_history import unaccepted_entry",
                  "from b133_closure_history import unaccepted_entry\n"
                  "from b133_closure_retention import retain_overlapping_chains")
    raw = replace(raw, '    "close_b133.py", "close_b133_v2.py", "test_b133_closure_v2.py",',
                  '    "close_b133.py", "close_b133_v2.py", "close_b133_v3.py",\n'
                  '    "b133_closure_retention.py", "test_b133_closure_retention.py", "test_b133_closure_v2.py",')
    raw = replace(raw, "        uuids, leaks = publication_findings(files, windows, allowed, guard)",
                  "        adjustments = retain_overlapping_chains(files, windows, allowed, guard, retention)\n"
                  '        put(files, "verification/chain-retention-adjustments.json", json_bytes(adjustments))\n'
                  "        uuids, leaks = publication_findings(files, windows, allowed, guard)")
    raw = replace(raw,
                  "            for family, claim, status, reason in RESOLUTION\n        ],",
                  "            for family, claim, status, reason in RESOLUTION\n"
                  "        ] + [\n"
                  '            {"run": "N1-B133-CLAUDE-CONFIRM-003", "id": identity, "status": "fixed",\n'
                  '             "reason": reason, "evidence": [*evidence, adjudications["claude"], adjudications["gpt"]]}\n'
                  "            for identity, reason in (\n"
                  '                ("historical-gloss", "The mistaken waterfall-water interpretation of the "\n'
                  '                 "specified historical compound reading is corrected to an Edo sake name; "\n'
                  '                 "earlier contrary review and coordinator assertions are withdrawn."),\n'
                  '                ("sake-precaution", "A separate direct alcohol/sake precaution and explicitly "\n'
                  '                 "historical Note were added, without modern synonymy or reading changes."),\n'
                  "            )\n        ],")
    raw = replace(raw, '"closure-real-report-002.json"', '"closure-real-report-003.json"')
    compile(raw, "close_b133_v3.py", "exec")
    successor = write_frozen(TOOLS / "close_b133_v3.py", raw)
    print(freeze_json(WS / "scratch-133" / "review" / "closure-v3-derivation.json", {
        "originalSha256": sha(original), "successor": successor,
        "preservedDryRun": "scratch-133/closure-v2-dry-001-report.json",
        "scope": "Stricter local-only chain retention. Reports, manifests, reviewer inputs and all "
                 "publication checks remain unchanged; non-chain overlap and unknown identities still fail.",
    }))


if __name__ == "__main__":
    main()
