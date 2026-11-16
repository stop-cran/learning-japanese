import sys
from pathlib import Path

AUTHOR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTHOR))
from b129_common import BASE, CHARS, GUARD_SHA, REPO, ROOT, git, normalized, sha, start_guard, stop_child, write

HERE = Path(__file__).resolve().parent
PACKET = REPO / "docs" / "n1-sources" / "batch-129-reconciliation"
ORIGINAL_PACKET = REPO / "docs" / "n1-sources" / "batch-129"
PARENT = "7c662b37c647a9b300278abe2e3079fe57f09f83"
PAIRS = {
    "絹": list("絡索緒線結括"),
    "虹": list("輪円光批劾議談撃騒動罪圧抗反曲器盆盤容缶対抵"),
}
assert sum(map(len, PAIRS.values())) == 28
