"""Derive closure tools for the actual third correction and six-run review history."""
import ast
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen

NEW = "f2d2ddf87a0f1a721920241a88a61e28a98fa6f2"
OLD = "dbca5192a4308dc6e8d954af37775e0fcd1986ea"
PROOF = "b0429c6363d34443b3d7bc9e3d385c2b22d6c0ea40c8fc4a49f2306e15687ff5"
PINS = {
    "finalize_b125.py": "6b83f36b3107896c2719e5d961c4cb705bcfb163319f49f05591cb0d628e47e2",
    "prepare_b125_publication_tools.py": "4118b69f80c0a9494f445e70d1a3cc51ec6c90107d42672c7240de6dfb73500c",
    "run-checks-closure-001.py": "1205ec2cc196ca9bfb8859307024163508d718833ce03a672da49fb2cc8b9773",
}


def derive(source, output, transform):
    raw = frozen(source, PINS[source.name])
    text = raw.decode("utf-8").replace("\r\n", "\n")
    original = text
    changes = []

    def sub(old, new):
        nonlocal text
        require(text.count(old) == 1, f"Unexpected derivation anchor: {old[:90]}")
        text = text.replace(old, new)
        changes.append((old, new))

    def function(name, replacement):
        node = next(node for node in ast.parse(text).body if isinstance(node, ast.FunctionDef) and node.name == name)
        sub(ast.get_source_segment(text, node), replacement)

    transform(sub, function)
    reverse = text
    for old, new in reversed(changes):
        require(reverse.count(new) == 1, "Ambiguous reverse derivation")
        reverse = reverse.replace(new, old)
    require(reverse == original, "Unrelated source changed")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    require(original.replace("\n", newline).encode("utf-8") == raw, "Mixed source line endings")
    derived = text.replace("\n", newline).encode("utf-8")
    compile(derived, str(output), "exec")
    return {"source": {"path": str(source), "sha256": sha(raw)},
            "output": write_frozen(output, derived), "reverseExact": True, "changes": len(changes)}


def finalizer(sub, function):
    sub('"""Close B125\'s two corrections while preserving the excluded protocol-VOID run."""',
        '"""Close all three B125 corrections and preserve accepted, held and protocol-VOID history."""')
    sub('from closure_quarantine_v2 import STATUS',
        'from closure_quarantine_v2 import STATUS\n'
        'from b125_followup_lineage import check_history as check_followup_history\n'
        'from finalize_b125 import check_proofs as check_first_two')
    sub(f'CANDIDATE = "{OLD}"', f'SECOND = "{OLD}"\nCANDIDATE = "{NEW}"')
    sub('    2: "ab5977465cacf873bd565e2761a1bafbdfcc1d044c8bf7ae06a7f214660e196d",',
        '    2: "ab5977465cacf873bd565e2761a1bafbdfcc1d044c8bf7ae06a7f214660e196d",\n'
        f'    3: "{PROOF}",')
    sub('FINALS = {family: f"N1-B125-{family.upper()}-CONFIRM-001" for family in INITIALS}',
        'FINALS = {family: f"N1-B125-{family.upper()}-CONFIRM-002" for family in INITIALS}')
    function("check_history", '''def check_history(provenance, config):
    check_followup_history(provenance, config, CANDIDATE)''')
    function("check_proofs", '''def check_proofs(first, second, current, config):
    check_first_two(first, second, config)
    require(current["candidate"] == CANDIDATE and current["parent"] == SECOND
            and current["originalCandidate"] == config["candidate"]
            and current["status"] == "PASS" and current["batch"] == 125
            and current["runtimeEntries"] == 8712
            and current["signature"] == second["signature"]
            and current["additionalGuards"] == list("\\u4f4e\\u77ed\\u5c0f\\u5bb9")
            and current["unrelatedRuntimeAndFrozenMetadataPreserved"] is True
            and current["runtimeChanged"] == ["kanji/\\u4fb5.md"]
            and current["parentInventoryCards"] == 1245
            and current["exactMetadataAndPracticeMatches"] == []
            and current["explicitReadingReplayByteIdentical"] is True
            and current["reviewAccepted"] is False and current["confirmationAccepted"] is False
            and set(current["gates"]) == {"author", "committed"},
            "Signed S1 source/inventory/runtime proof differs")
    for gates in current["gates"].values():
        require(len(gates) == len(CHECKS) and {row["gate"] for row in gates} == set(CHECKS),
                "Incomplete S1 correction gate inventory")''')
    sub('"intermediateRuns": [], "closure":', '"intermediateRuns": provenance["intermediateRuns"], "closure":')
    sub('"original-reviewer confirmations on the second signed correction. GPT001 is "',
        '"original-reviewer second confirmations on the third signed correction; both first "\n'
        '                    "confirmations retain their accepted/held historical states. GPT001 is "')
    sub('ledger["correctionSources"] = ["batch-125-reconciliation/", "batch-125-reconciliation-002/"]',
        'ledger["correctionSources"] = ["batch-125-reconciliation/", "batch-125-reconciliation-002/",\n'
        '                                   "batch-125-reconciliation-003/"]')
    sub('"Fifteen added direct guards conservatively protect broad-English choices, not universal "',
        '"Nineteen added direct guards conservatively protect broad-English choices, not universal "')
    sub('"All raw reports and limits remain; GPT001 and historical open Q4/Q9 evidence are not relabelled.",',
        '"All raw reports and limits remain; GPT001 and historical Q4/Q9 and S1 holds are not relabelled.",\n'
        '        "The positive appearance-source branch is scoped against current titles/readings; ordinary "\n'
        '        "frequency, arbitrary/future pools and multi-borrow safety are not established.",')
    sub('first, current = [json.loads(proof_raw[number]) for number in (1, 2)]',
        'first, second, current = [json.loads(proof_raw[number]) for number in (1, 2, 3)]')
    sub('    check_proofs(first, current, config)', '    check_proofs(first, second, current, config)')
    sub('len(archive["chains"]) == 8', 'len(archive["chains"]) == 10')
    sub('((FIRST, config["candidate"]), (CANDIDATE, FIRST))',
        '((FIRST, config["candidate"]), (SECOND, FIRST), (CANDIDATE, SECOND))')
    sub('"verification/reconciliation-002.json": proof_raw[2],',
        '"verification/reconciliation-002.json": proof_raw[2],\n'
        '        "verification/reconciliation-003.json": proof_raw[3],\n'
        '        "verification/s1-parent-inventory.json": frozen(\n'
        '            WS / "scratch-125" / "reconciliation-003-inventory-002" / "card-inventory.json",\n'
        '            current["parentInventorySha256"]),')
    sub('for number, proof in ((1, first), (2, current)):',
        'for number, proof in ((1, first), (2, second), (3, current)):')
    sub('directory = WS / "scratch-125" / f"reconciliation-{number:03}-{mode}-gates-001"',
        'directory = WS / "scratch-125" / (proof["gateSets"][mode]["directory"] if number == 3\n'
        '                                               else f"reconciliation-{number:03}-{mode}-gates-001")')
    sub('for name in ("finalize_b125.py", "test_finalize_b125.py", "verify_b125_reconciliation_001.py",',
        'for name in ("finalize_b125_v2.py", "test_finalize_b125_v2.py", "prepare_b125_finalizer_v2.py",\n'
        '                     "b125_followup_lineage.py", "test_b125_followup_lineage.py",\n'
        '                     "verify_b125_reconciliation_003.py", "test_verify_b125_reconciliation_003.py",\n'
        '                     "prepare_b125_confirmations_002.py", "test_prepare_b125_confirmations_002.py",\n'
        '                     "finalize_b125.py", "test_finalize_b125.py", "verify_b125_reconciliation_001.py",')
    sub('        for name in ("reconciliation-001-gates.py", "reconciliation-002-gates.py"):',
        '        for relative, binding in current["evidenceReceipts"].items():\n'
        '            source = WS / "scratch-125" / relative\n'
        '            prefix = "evidence/s1/" + relative.removesuffix(".json")\n'
        '            artifacts[prefix + ".json"] = frozen(source, binding["receiptSha256"])\n'
        '            artifacts[prefix + ".log"] = frozen(source.with_suffix(".log"), binding["logSha256"])\n'
        '        for source in sorted((WS / "scratch-125" / "reconciliation-003-scripts").glob("*.py")):\n'
        '            artifacts["protocol/b125/reconciliation-003/" + source.name] = frozen(source)\n'
        '        for name in ("reconciliation-001-gates.py", "reconciliation-002-gates.py"):')


def downstream(sub, function):
    sub('from finalize_b125 import CANDIDATE, check_history, check_proofs',
        'from finalize_b125_v2 import CANDIDATE, check_history, check_proofs')
    sub('first, current = [json.loads(frozen(closure / "verification" / f"reconciliation-{n:03}.json"))\n'
        '                      for n in (1, 2)]',
        'first, second, current = [json.loads(frozen(closure / "verification" / f"reconciliation-{n:03}.json"))\n'
        '                              for n in (1, 2, 3)]')
    sub('    check_proofs(first, current, config)', '    check_proofs(first, second, current, config)')


def runner(sub, function):
    downstream(sub, function)
    sub('HERE / "reconciliation-002-committed-gates-001"', 'HERE / "reconciliation-003-committed-gates-001"')


def main():
    records = [
        derive(TOOLS / "finalize_b125.py", TOOLS / "finalize_b125_v2.py", finalizer),
        derive(TOOLS / "prepare_b125_publication_tools.py", TOOLS / "prepare_b125_publication_tools_v2.py", downstream),
        derive(WS / "scratch-125" / "run-checks-closure-001.py",
               WS / "scratch-125" / "run-checks-closure-002.py", runner),
    ]
    print(freeze_json(TOOLS / "b125-finalizer-v2-derivation.json", {
        "candidate": NEW, "proofSha256": PROOF, "derivations": records,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "limits": "Prepared tools only; no closure, acceptance, commit or publication is performed.",
    }))


if __name__ == "__main__":
    main()
