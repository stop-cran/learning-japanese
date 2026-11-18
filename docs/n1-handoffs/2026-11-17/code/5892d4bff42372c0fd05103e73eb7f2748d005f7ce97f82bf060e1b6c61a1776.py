"""Derive the established one-phase auditor and report contract for B132 confirmation."""
import ast
import json
import subprocess
import sys

from common import WS, freeze_json, frozen, load_module, require, sha, start_guard, write_frozen
from run_b132_closure_checks import REPO, HERE
from verify_b132_packet import RUNNER
from verify_b132_sources import Git

OUT = HERE / "review" / "confirmation-001"
SOURCE = WS / "scratch-116" / "confirm"
PINS = {
    "audit-confirm.py": "c6ec99949ef19057f432c052df3293184c3866e65ba7387e148a39505a3b2c9e",
    "check-confirm-structure.py": "ad3a204757e872e54b81745a028d040e4510ce551046a63ec6b70fcb0bddd31d",
    "test-audit-confirm.py": "21619257f2cbfd446a0f36a1f526c38d77dc0f98909f5e1fa8c4eaa4879537d9",
    "test-confirm-structure.py": "cb98ae269f1fa55689d107ada23a49677e81937f67fff030421179fbe5aafddb",
    "prepare-confirmation-v9.py": "ae0efcc5624c73bb9bd2a3e37131a572b771d2070bb868745aecff67dc321af5",
}


def replace_once(text, old, new, changes):
    require(text.count(old) == 1, "Unexpected confirmation source for: " + old)
    changes.append((old, new))
    return text.replace(old, new)


def main():
    require(not OUT.exists(), "Preserve the previous engine preparation")
    guard, _ = start_guard("B132 confirmation-engine preparation")
    try:
        OUT.mkdir()
        derivations = []
        for name, digest in PINS.items():
            original = frozen(SOURCE / name, digest)
            text = original.decode("utf-8")
            changes = []
            if name == "prepare-confirmation-v9.py":
                text = "\n\n".join(ast.get_source_segment(text, node) for node in ast.parse(text).body
                                   if isinstance(node, ast.FunctionDef)
                                   and node.name in ("skeleton", "render_prompt", "self_test")) + "\n"
                name = "renderer.py"
            selected = text
            text = text.replace("B116", "B132")
            if name == "audit-confirm.py":
                text = replace_once(text, "sys.path.insert(0, str(HERE.parent))",
                                    "sys.path.insert(0, str(HERE.parent / 'neutral-preparation-002' / 'protocol-001'))",
                                    changes)
            if name == "check-confirm-structure.py":
                text = replace_once(text, "([FO][1-9]\\d?)", "([FOQ][1-9]\\d?)", changes)
                text = replace_once(text, 'if confirmation == "CONFIRMED" and (defect or open_items):',
                                    'if confirmation == "CONFIRMED" and (defect or open_items or "UNVERIFIED" in facets.values()):',
                                    changes)
                text = replace_once(text, "and no NEEDS FIX facet", "and no NEEDS FIX or UNVERIFIED facet", changes)
            if name == "renderer.py":
                text = replace_once(text, "using new evidence and the actual revision.",
                                    "using new evidence and the actual signed snapshot.", changes)
                text = replace_once(text, "Actual revised commit: {commit}",
                                    "Actual confirmation snapshot: {commit}", changes)
                text = replace_once(text, "the actual revised snapshot and diff,",
                                    "the actual signed snapshot and verified change/no-change record,", changes)
            reverse = text
            for old, new in reversed(changes):
                require(reverse.count(new) == 1, "Ambiguous reverse derivation")
                reverse = reverse.replace(new, old)
            require(reverse.replace("B132", "B116") == selected, "Unexpected derivation delta")
            prefix = ""
            if name == "renderer.py":
                prefix = ("import re\nfrom pathlib import Path\n"
                          "from common import COORDINATOR, require, load_module as load\n"
                          "HERE = Path(__file__).resolve().parent\n\n")
            raw = (prefix + text).encode("utf-8")
            compile(raw, name, "exec")
            derivations.append({
                "source": {"path": str(SOURCE / ("prepare-confirmation-v9.py" if name == "renderer.py" else name)),
                           "sha256": digest},
                "output": write_frozen(OUT / name, raw), "reverseExact": True,
                "selectedDeltas": ["B116 -> B132", *[{"old": old, "new": new} for old, new in changes]],
                "selection": "skeleton/render_prompt/self_test functions" if prefix else "whole file",
            })
        load_module("b132_confirmation_renderer", OUT / "renderer.py").self_test()
        command = ("import sys,unittest;sys.path.insert(0," + repr(str(OUT)) + ");"
                   "unittest.main(module=None,argv=['unittest','test-audit-confirm',"
                   "'test-confirm-structure','test_b132_confirmation_engine'])")
        process = subprocess.Popen([sys.executable, "-B", "-c", command], cwd=REPO,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = Git(REPO, RUNNER, guard).wait(process)
        log = write_frozen(OUT / "tooling-tests.txt", stdout + stderr)
        require(process.returncode == 0, (stdout + stderr).decode("utf-8", "replace"))
        result = {
            "batch": 132, "status": "ENGINE_PREPARED_NOT_REVIEW_ADMISSION",
            "derivations": derivations, "tests": log, "exitCode": process.returncode,
            "limits": "No source dossier, reviewer admission, confirmation or content acceptance.",
        }
        print((stdout + stderr).decode("utf-8", "replace"))
        print(json.dumps(freeze_json(OUT / "engine-preparation.json", result)))
    finally:
        require(not guard.finish()["breach"], "Confirmation preparation RAM breach")


if __name__ == "__main__":
    main()
