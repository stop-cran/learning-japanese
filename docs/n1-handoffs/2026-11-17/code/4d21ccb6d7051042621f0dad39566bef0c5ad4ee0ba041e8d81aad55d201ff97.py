"""Generate complete new-file/dependency inventories and freeze verified preparation."""
import ast
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOOLS = Path(r"C:\Users\stop-\n1-kanji-workspace\review-tools")
sys.path.insert(0, str(TOOLS))
from common import freeze_json, frozen, sha, write_frozen

NAMES = ("b134_integrated_v1.py", "run_b134_integration_gates_v1.py",
         "verify_b134_integration_closure_v1.py", "deliver_b134_integration_v1.py",
         "record_b134_integration_publication_v1.py")
new = {name: sha((TOOLS / name).read_bytes()) for name in NAMES}
pending, dependencies = list(NAMES), {}
while pending:
    name = pending.pop()
    if name in dependencies:
        continue
    path = TOOLS / name
    raw = path.read_bytes()
    dependencies[name] = sha(raw)
    for node in ast.walk(ast.parse(raw, filename=name)):
        names = ([alias.name for alias in node.names] if isinstance(node, ast.Import)
                 else [node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
        for module in names:
            candidate = module.split(".")[0] + ".py"
            if (TOOLS / candidate).is_file() and candidate not in dependencies:
                pending.append(candidate)
for name in NAMES:
    (TOOLS / name).chmod(0o444)
freeze_json(ROOT / "tool-inventory.json", {"files": new})
freeze_json(ROOT / "dependency-inventory.json", {
    "files": {name: digest for name, digest in dependencies.items() if name not in NAMES},
    "limits": "Existing files are hash-bound, never modified or chmodded by preparation."})
for number in range(1, 5):
    original = ROOT.parent / f"integration-prep-test-{number:03d}"
    receipt_raw = (original / "receipt.json").read_bytes()
    receipt = json.loads(receipt_raw)
    log = (original / "output.log").read_bytes()
    if receipt["logSha256"] != sha(log) or receipt["memory"]["breach"] or receipt["cleanupError"]:
        raise ValueError("Invalid guarded receipt")
    if number == 4 and receipt["exitCode"] != 0:
        raise ValueError("Final controls failed")
    for filename, raw in (("receipt.json", receipt_raw), ("output.log", log)):
        write_frozen(ROOT / "test-receipts" / original.name / filename, raw)
        (original / filename).chmod(0o444)
files = {}
for path in ROOT.rglob("*"):
    if path.is_file():
        path.chmod(0o444)
        files[path.relative_to(ROOT).as_posix()] = sha(frozen(path))
inventory = freeze_json(ROOT / "inventory.json", {"status": "FROZEN_PREPARATION_ONLY", "files": files, "tools": new})
import importlib.util
spec = importlib.util.spec_from_file_location("verify_b134_integration_preparation", ROOT / "verify-preparation.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.main()
print(json.dumps({"inventory": inventory, "handoffSha256": sha(frozen(ROOT / "HANDOFF.txt")),
                  "toolInventorySha256": sha(frozen(ROOT / "tool-inventory.json")),
                  "dependencyInventorySha256": sha(frozen(ROOT / "dependency-inventory.json")),
                  "scratchFiles": len(files), "existingDependencyFiles": len(dependencies) - len(new)}))
