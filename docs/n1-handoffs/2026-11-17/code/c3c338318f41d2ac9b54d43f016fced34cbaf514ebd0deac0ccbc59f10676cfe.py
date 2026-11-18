"""Preserve the failed prefix attempt and derive the correct signed source prefix."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import frozen, require, sha, write_frozen, freeze_json
source = HERE / "tools" / "packet-builder-b134-002.py"
raw = frozen(source)
require('PREFIX = "docs/n1-sources/batch-133/"' in raw.decode(), "Prefix anchor differs")
text = raw.decode().replace("batch-133/", "batch-134/")
binding = write_frozen(HERE / "tools" / "packet-builder-b134-003.py", text.encode())
freeze_json(HERE / "packet-prefix-correction-003.json", {
    "source": {"path": str(source), "sha256": sha(raw)}, "output": binding,
    "reason": "Failed attempt retained. Correct source path batch-133 to batch-134; no packet had been written."})
