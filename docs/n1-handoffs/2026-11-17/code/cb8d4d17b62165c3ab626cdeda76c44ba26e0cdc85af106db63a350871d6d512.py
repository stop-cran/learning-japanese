"""Verify exact repair routing without executing lifecycle actions; freeze package."""
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import freeze_json, frozen, load_module, require, sha, write_frozen

for path in ROOT.iterdir():
    if path.is_file():
        path.chmod(0o444)
adapter = load_module("b134_test_final_repair_controller", ROOT / "controller-entry.py")
calls = []
fake = SimpleNamespace(child=lambda *args: calls.append(args) or (0, "synthetic", "synthetic"))
with patch.object(adapter, "load_module", return_value=fake):
    controller = adapter.load_controller()
    controller.child(adapter.ORIGINAL / "check-report-structure-b134-014.py", "--test")
    controller.child("unrelated-pinned-child.py", "--other")
require(calls == [(ROOT / "checker-entry.py", "--test"), ("unrelated-pinned-child.py", "--other")],
        "Controller did not redirect only the exact old checker")
freeze_json(ROOT / "controller-routing.json", {
    "status": "PASS", "checkerOnlyRedirected": True, "otherChildrenUnchanged": True,
    "controllerSha256": sha(frozen(ROOT / "controller-entry.py")),
    "checkerSha256": sha(frozen(ROOT / "checker-entry.py")),
    "noLifecycleActionExecuted": True})
test = ROOT.parent / "report-checker-repair-test-001"
for name in ("receipt.json", "output.log"):
    raw = (test / name).read_bytes()
    write_frozen(ROOT / "test-receipts" / name, raw)
    (test / name).chmod(0o444)
receipt = json.loads(frozen(ROOT / "test-receipts" / "receipt.json"))
require(receipt["exitCode"] == 0 and not receipt["memory"]["breach"]
        and receipt["logSha256"] == sha(frozen(ROOT / "test-receipts" / "output.log")),
        "Guarded report-checker test failed")
files = {}
for path in ROOT.rglob("*"):
    if path.is_file():
        path.chmod(0o444)
        files[path.relative_to(ROOT).as_posix()] = sha(frozen(path))
print(json.dumps(freeze_json(ROOT / "inventory.json", {"status": "FROZEN", "files": files})))
