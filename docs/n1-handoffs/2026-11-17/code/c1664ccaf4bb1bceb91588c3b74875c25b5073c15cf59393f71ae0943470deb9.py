"""Adapt only synthetic optional-unit and forecast controls from the accepted precedent."""
import sys
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
HERE = ROOT / "neutral-preparation-001" / "projected-successor-001"
OLD = WS / "scratch-133" / "review" / "neutral-preparation-004" / "successor-002"
sys.path.insert(0, str(WS / "review-tools"))
from common import frozen, require, sha, write_frozen, freeze_json

source = OLD / "tools" / "test-optional004.py"
raw = frozen(source)
text = raw.decode().replace("\r\n", "\n")
for before, after in (
    (str(OLD), str(HERE)), ("scratch-133", "scratch-134"),
    ('ROOT / "neutral-preparation-004" / "successor-002"',
     'ROOT / "neutral-preparation-001" / "projected-successor-001"'),
    ("b133", "b134"), ("B133", "B134"), ("protocol-003", "protocol-001"),
    ("audit-configs-003", "audit-configs-001"),
    ("final-test-synthetic-protocol-b134-002.py", "test-synthetic-protocol-b134-001.py"),
    ('len(costs), 86', 'len(costs), 62'), ("K:琴", "K:紫"),
    ('{"D": 10, "E": 5}', '{"D": 25, "E": 10}'),
):
    text = text.replace(before, after)
binding = write_frozen(HERE / "tools" / "test-optional-b134-001.py", text.encode())
freeze_json(HERE / "optional-controls-derivation-001.json", {
    "source": {"path": str(source), "sha256": sha(raw)}, "output": binding,
    "changes": "B134 roots, 62 actual units, synthetic target fixture and measured D25/E10 caps only."})
