"""Freeze a test runtime copy without changing any delivery/old-review tool."""
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import require, write_frozen

source = Path(__file__).resolve().parent
target = Path(sys.argv[1]).resolve()
require(target.parent == source.parent and not target.exists(), "Use a NEW direct review runtime")
target.mkdir()
print(write_frozen(target / "b134_integration_followup_v1.py",
                   (source / "b134_integration_followup_v1.py").read_bytes()))
