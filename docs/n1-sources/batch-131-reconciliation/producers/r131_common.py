from b131_common import (
    GUARD_SHA, REPO, ROOT, git, normalized, sha, start_guard, stop_child, write,
    HERE as SCRIPTS,
)

HERE = SCRIPTS / "reconciliation-001"
PACKET = REPO / "docs" / "n1-sources" / "batch-131-reconciliation"
ORIGINAL = REPO / "docs" / "n1-sources" / "batch-131"
PARENT = "1359b467e0edee8822c665614d6ca57e42785c4d"
BASE = "cb0f5581bdda84f7e673225c19126c85e242e57b"
CHARS = ["衛", "羊", "霜"]
COMPARISONS = list("氷凍酒冴涼久害枯殺卒援循番士軍送抵")
FROZEN = ROOT / "review-packets" / "batch-131-1359b467-compact-001"
