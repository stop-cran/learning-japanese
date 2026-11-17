"""Freeze a test candidate in a NEW directory; this is not a readiness assertion."""
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import require, write_frozen

root = Path(__file__).resolve().parent
target = Path(sys.argv[1]).resolve()
require(target.parent == root.parent and not target.exists(), "Use a new direct review runtime")
target.mkdir()
print(write_frozen(target / "b134_authorized_confirmation_v1.py",
                   (root / "b134_authorized_confirmation_v1.py").read_bytes()))
