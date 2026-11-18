"""Resolve the two documented historical producer bases without rewriting receipts."""
from pathlib import Path

from common import TOOLS, WS, require


def resolve_binding(path):
    path = Path(path)
    if path.is_absolute():
        return path, None
    parts = path.parts
    if parts[:4] == ("..", "scratch-117", "review", "confirm"):
        base, rule = TOOLS, "legacy-confirmation-producer-review-tools"
        tail = parts[1:]
    elif parts[:3] == ("scratch-117", "review", "confirm"):
        base, rule = WS, "workspace-confirmation-producer"
        tail = parts
    else:
        raise ValueError(f"Unrecorded relative binding base: {path}")
    require(".." not in tail and "." not in tail, "Unsafe relative binding")
    resolved = (base / path).resolve()
    require(resolved.is_relative_to(WS / "scratch-117" / "review" / "confirm"),
            "Binding escaped the confirmation archive")
    return resolved, rule
