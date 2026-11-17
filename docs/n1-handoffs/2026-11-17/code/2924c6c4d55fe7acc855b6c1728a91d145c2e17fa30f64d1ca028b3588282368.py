"""Reused survey originals are hash-bound, not falsely claimed ReadOnly."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import frozen, require, sha, write_frozen, freeze_json
source = HERE / "tools" / "packet-builder-b134-003.py"
raw = frozen(source)
text = raw.decode().replace('"complete-record-trial"', '"complete-record-trial-002"')
before = ('            raw = frozen(item["localRawCapture"], item["rawSha256"])\n'
          '            text_raw = frozen(Path(item["localRawCapture"]).with_suffix(".txt"), item["textSha256"])')
after = ('            raw = Path(item["localRawCapture"]).read_bytes()\n'
         '            text_raw = Path(item["localRawCapture"]).with_suffix(".txt").read_bytes()')
require(before in text, "Capture anchor differs")
binding = write_frozen(HERE / "tools" / "packet-builder-b134-004.py", text.replace(before, after).encode())
freeze_json(HERE / "packet-capture-correction-004.json", {
    "source": {"path": str(source), "sha256": sha(raw)}, "output": binding,
    "reason": "B132 raw survey files are writable. Validate exact signed raw/text hashes and freeze copies, without modifying original attributes. Preserve incomplete trial."})
