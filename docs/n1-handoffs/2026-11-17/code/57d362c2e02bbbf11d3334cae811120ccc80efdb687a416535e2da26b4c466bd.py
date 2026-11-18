"""Derive the corrected-snapshot closure tools while preserving the prepared versions."""
import ast
from pathlib import Path

from common import WS, freeze_json, frozen, require, write_frozen
from confirm_v2 import binding

HERE = Path(__file__).resolve().parent
source = HERE / "finalize_b120.py"
original = frozen(source, "37f83774330174b27f68a45a54cb35a73397544406cc34a0b7a2fa2cc7848d0e").decode()
text = original.replace("\r\n", "\n")
deltas = []


def replace(old, new, label):
    global text
    require(text.count(old) == 1, f"Changed finalizer anchor: {label}")
    text = text.replace(old, new)
    deltas.append({"label": label, "before": old, "after": new})


replace('CANDIDATE = "c986ae49e844c08afc294d9381c7e486f2c9315d"',
        'CANDIDATE = "356375e1d340573dc76e4f61826dfb9af9640bdd"\n'
        'RECONCILED = "c986ae49e844c08afc294d9381c7e486f2c9315d"',
        "signed candidate and preserved parent")
replace("000daca2adf350a897a99027de9fda6e310bc18fce6897b69b5e79d10e1a2f29",
        "33d2f6ca0ec078404966ec9a9780967bbe2624685b4eda1a0e26f8d91613deb8", "manifest")
replace("985b89011351ab99143beaa14de30c7ac8f5be6c47239b1f3a8a6de63e904810",
        "e9f7a3b2e73f241a03b98ff8e77e5985033365c492f5e40294f2f0987e9d1042", "gate summary")
replace('GATES = WS / "scratch-120" / "committed-revision-gates-001"',
        'GATES = WS / "scratch-120" / "author-gates-002"', "committed gates")
replace("from pathlib import Path", "from pathlib import Path\n"
        "from b120_held_evidence import collect as collect_held, verify_lineage", "held history support")
node = next(node for node in ast.parse(text).body
            if isinstance(node, ast.FunctionDef) and node.name == "verify_closure")
replace(ast.get_source_segment(text, node),
        "def verify_closure(provenance):\n    verify_lineage(provenance, CANDIDATE)",
        "two final confirmations and passing-only predecessor lineage")
replace('git(config, "show", "-s", "--format=%P", CANDIDATE).decode().strip() == INITIAL',
        'git(config, "show", "-s", "--format=%P", CANDIDATE).decode().strip() == RECONCILED',
        "preserved signed reconciliation")
replace('summary["startingHead"] == CANDIDATE and summary["base"] == config["base"]\n'
        '                and summary["status"] == "PASS" and summary["cleanBeforeAndAfter"]',
        'summary["candidate"] == CANDIDATE and summary["startingHead"] == RECONCILED\n'
        '                and summary["base"] == config["base"] and summary["status"] == "PASS"\n'
        '                and summary["committedManifestSha256"] == MANIFEST_SHA',
        "actual hash-pinned author runner summary schema")
addition = '''
        correction_path = REVIEW / "correction-verification-002.json"
        correction_raw = frozen(correction_path,
            "88a542059a06883178567265c6cc20c1504ce1e9edce1163395e5a29e982c87c")
        correction = json.loads(correction_raw)
        require(correction["status"] == "PASS" and correction["candidate"] == CANDIDATE
                and correction["prior"] == RECONCILED and not correction["memory"]["breach"]
                and correction["summary"]["sha256"] == SUMMARY_SHA, "Correction proof changed")
        for path, digest in correction["newEvidenceSha256"].items():
            require(sha(blob(CANDIDATE, path)) == digest, f"Correction source changed: {path}")
        artifacts["verification/correction-verification-002.json"] = correction_raw
        for path in sorted((REVIEW / "confirm" / "correction-002-neutral").iterdir()):
            if path.is_file():
                artifacts[f"verification/correction-002/{path.name}"] = frozen(path)
        erratum = artifacts["verification/correction-002/source-summary-erratum.json"]
        erratum_data = json.loads(erratum)
        require(erratum_data["candidate"] == CANDIDATE
                and sha(blob(CANDIDATE, erratum_data["path"])) == erratum_data["sourceSummarySha256"]
                and sha(blob(CANDIDATE, erratum_data["completeXml"]["path"]))
                == erratum_data["completeXml"]["sha256"], "Source erratum binding differs")
        held_files, held_record = collect_held(guard)
        require(not artifacts.keys() & held_files.keys(), "Held artifact collision")
        artifacts.update(held_files)
        for name in ("finalize_b120_v2.py", "derive_b120_finalizer_v2.py",
                     "b120-finalizer-v2-derivation.json", "b120_held_evidence.py",
                     "test_b120_held_evidence.py", "verify_b120_correction.py",
                     "verify_b120_correction_v2.py", "test_verify_b120_correction_v2.py",
                     "b120-correction-v2-derivation.json", "prepare_b120_confirmations_002.py"):
            artifacts[f"protocol/tools/{name}"] = frozen(Path(__file__).with_name(name))
        artifacts["protocol/run-reconciliation-002-checks.py"] = frozen(
            WS / "scratch-120" / "run-reconciliation-002-checks.py",
            "cc10b400cc2c1c2b7ca26acfa120c4d4e336c071b930cbbee9b01654e1f1f68a")
'''
replace("        for name, raw in artifacts.items():\n            write_frozen(closure / name, raw)",
        addition.lstrip("\n") + "\n        for name, raw in artifacts.items():\n"
        "            write_frozen(closure / name, raw)\n"
        '        write_frozen(repo / "docs" / "n1-sources" / "batch-120" / "reconciliation-002"\n'
        '                     / "source-summary-erratum.json", erratum)',
        "archive held report as unaccepted history and persist explicit source erratum")
replace('"remainingConsequentialClaims": [], "historicalReportsPreserved": True,',
        '"remainingConsequentialClaims": [], "historicalReportsPreserved": True,\n'
        '                       "heldConfirmations": [held_record],', "disclose held report")
replace('"reconciliation": "batch-120/reconciliation-001/bindings.json"}',
        '"reconciliation": "batch-120/reconciliation-001/bindings.json",\n'
        '                               "correction": "batch-120/reconciliation-002/bindings.json",\n'
        '                               "sourceSummaryErratum": "batch-120/reconciliation-002/source-summary-erratum.json",\n'
        '                               "sourceSummaryErratumSha256": sha(erratum)}',
        "source correction provenance")
replace('"recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()}, "publication": "PENDING"}',
        '"recordedFileSha256": {name: sha(raw) for name, raw in artifacts.items()},\n'
        '            "heldConfirmations": [held_record], "publication": "PENDING"}',
        "held archive in validation provenance")
reversed_text = text
for delta in reversed(deltas):
    require(reversed_text.count(delta["after"]) == 1, "Ambiguous reverse transformation")
    reversed_text = reversed_text.replace(delta["after"], delta["before"])
require(reversed_text == original.replace("\r\n", "\n"), "Finalizer reverse proof failed")
compile(text, "finalize_b120_v2.py", "exec")
finalizer = write_frozen(HERE / "finalize_b120_v2.py", text.encode())

runner_source = WS / "scratch-120" / "run-checks-closure-001.py"
runner = frozen(runner_source, "9b49b4f4cac4d98d748b94c4300d6fc75bd95dfa6021c8b72efabbc0ff593822")
runner_changes = [
    (b"from finalize_b120 import", b"from finalize_b120_v2 import"),
    (b"3adf43a5a3390868ae387652026c781e21de9df59382b04bbbcc28a8a93b98c6",
     b"cc10b400cc2c1c2b7ca26acfa120c4d4e336c071b930cbbee9b01654e1f1f68a"),
    (b"run-committed-revision-checks.py", b"run-reconciliation-002-checks.py"),
]
derived = runner
for before, after in runner_changes:
    require(derived.count(before) == 1, "Closure runner anchor changed")
    derived = derived.replace(before, after)
compile(derived, "run-checks-closure-002.py", "exec")
gate_runner = write_frozen(WS / "scratch-120" / "run-checks-closure-002.py", derived)
print(freeze_json(HERE / "b120-finalizer-v2-derivation.json", {
    "source": binding(source), "runnerSource": binding(runner_source),
    "finalizer": finalizer, "closureRunner": gate_runner, "reverseExactNormalizedSource": True,
    "changes": deltas,
    "limit": "Preparation only. The tools require both accepted CONFIRM-002 reports on the corrected snapshot.",
}))
