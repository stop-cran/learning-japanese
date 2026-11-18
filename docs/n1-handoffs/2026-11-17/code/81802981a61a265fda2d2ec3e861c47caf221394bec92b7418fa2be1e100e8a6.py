"""Derive cc374-pinned v2 integration tools from the frozen v1 tools with counted substitutions."""
import hashlib
import json
import sys
from pathlib import Path

TOOLS = Path(r"C:\Users\stop-\n1-kanji-workspace\review-tools")
PREP = Path(r"C:\Users\stop-\n1-kanji-workspace\scratch-134\review\integration-prep-001")
OUT = Path(sys.argv[1])
SOURCES = {
    "b134_integration.py": "18949ffa",
    "b134_integrated_v1.py": "b493c63d5d2d3c24968d0cb957dd715fd9396135aafa7781d61810867016ee86",
    "run_b134_integration_gates_v1.py": "188d3dde386d84b205097de7a2691c3b19bcfc5547f9900182aa276cfaa142bc",
    "verify_b134_integration_closure_v1.py": "17101ab9971f662bfb8ed90fa54d9de82ad32ae73143e90fab33ee9910289581",
    "deliver_b134_integration_v1.py": "7df5c4480716db8e0d94ae5bb0e60d4653fe1c53da64abfbde02043c81985d45",
    "record_b134_integration_publication_v1.py": "28232c1098e88f7185a1d1405d5cd945466821c197a0d1b5145ee2ba74b61603",
}
OLD = "355cccb840d22e7313e79f234eb93d1367e00352"
NEW = "cc374051efa75199212a87c9abf08d7391419055"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def sub(text, old, new, count):
    found = text.count(old)
    assert found == count, (old, found, count)
    return text.replace(old, new)


CRLF = {}


def read(name):
    raw = (TOOLS / name).read_bytes()
    assert sha(raw).startswith(SOURCES[name]), name
    text = raw.decode("utf-8")
    CRLF[name.replace("_v1.py", "_v2.py").replace("integration.py", "integration_v2.py")] = "\r\n" in text
    assert ("\r\n" in text) == (text.count("\n") == text.count("\r\n")), name
    return text.replace("\r\n", "\n")


results = {}
text = read("b134_integration.py")
text = sub(text, '"""Verify the concurrent signed school-label change and its later B134 merge.\n',
           '"""Verify the concurrent signed school-label change and its later B134 merge.\n\n'
           'v2 of b134_integration.py: identical checks; REVIEWED is the revision-confirmed snapshot\n'
           'cc374051 (owner-signed authorized descendant of 355cccb) instead of 355cccb.\n', 1)
text = sub(text, "b134_integration.py incoming", "b134_integration_v2.py incoming", 1)
text = sub(text, "b134_integration.py merged", "b134_integration_v2.py merged", 1)
text = sub(text, f'REVIEWED = "{OLD}"', f'REVIEWED = "{NEW}"', 1)
text = sub(text, '"limits": "Exact signed object/manifest preservation only. Frozen B134 reviews remain on "\n'
                 '                  "355cccb. Combined-tree host gates',
           '"limits": "Exact signed object/manifest preservation only. Frozen B134 reviews and authorized "\n'
           '                  "confirmations remain on cc374051 (revision-confirmed descendant of 355cccb). "\n'
           '                  "Combined-tree host gates', 1)
assert "355cccb840" not in text
results["b134_integration_v2.py"] = text

text = read("b134_integrated_v1.py")
text = sub(text, '"""B134 integration contracts; unlike linear B134, C->M->I retains incoming main.\n',
           '"""B134 integration contracts; unlike linear B134, C->M->I retains incoming main.\n\n'
           'v2 of b134_integrated_v1.py: REVIEWED comes from b134_integration_v2 (cc374051) and the\n'
           'original ledger is validated by b134_revision_progress; all other contracts are unchanged.\n', 1)
text = sub(text, "from b134_closure_progress import validate_progress",
           "from b134_revision_progress import validate_progress", 1)
text = sub(text, "from b134_integration import", "from b134_integration_v2 import", 1)
text = sub(text, '         "record_b134_integration_publication_v1.py")',
           '         "record_b134_integration_publication_v1.py", "b134_integration_v2.py",\n'
           '         "b134_revision_progress.py")', 1)
text = sub(text, "_v1", "_v2", 8)
text = sub(text, "v2 of b134_integrated_v2.py", "v2 of b134_integrated_v1.py", 1)
results["b134_integrated_v2.py"] = text

for name, count in (("run_b134_integration_gates_v1.py", 1), ("verify_b134_integration_closure_v1.py", 1),
                    ("deliver_b134_integration_v1.py", 4), ("record_b134_integration_publication_v1.py", 3)):
    results[name.replace("_v1.py", "_v2.py")] = sub(read(name), "_v1", "_v2", count)

for name, value in results.items():
    lines = [line for line in value.splitlines() if "v1" in line and "--porcelain=v1" not in line
             and "_v1.py:" not in line and "of b134_integrated_v1.py" not in line]
    assert not lines, (name, lines)

test = (PREP / "test-integration.py").read_text(encoding="utf-8")
test_count = test.count("_v1")
test = test.replace("_v1", "_v2")
results_test = test

OUT.mkdir()
inventory = {}
for name, value in results.items():
    target = TOOLS / name
    assert not target.exists(), name
    raw = (value.replace("\n", "\r\n") if CRLF[name] else value).encode("utf-8")
    target.write_bytes(raw)
    inventory[name] = sha(raw)
for name in ("b134_revision_progress.py",):
    inventory[name] = sha((TOOLS / name).read_bytes())
(OUT / "test-integration-v2.py").write_text(results_test, encoding="utf-8", newline="\n")
(OUT / "tool-inventory.json").write_text(json.dumps({"files": inventory}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"testV1Replacements": test_count, "files": inventory}, indent=2))
