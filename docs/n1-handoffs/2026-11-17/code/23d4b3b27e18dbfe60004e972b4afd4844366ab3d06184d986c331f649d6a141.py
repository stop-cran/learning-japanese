"""Freeze actual full app tool outputs and admit one already-prepared confirmation."""
import datetime
import json
import re
import sys
from pathlib import Path

from common import freeze_json, require, write_frozen
from confirm_b132 import OUT, ROOT, admit


def main(family, status_path, roster_path):
    require(family in ("claude", "gpt"), "Unknown reviewer family")
    status_path, roster_path = Path(status_path), Path(roster_path)
    timestamps = []
    for path in (status_path, roster_path):
        match = re.fullmatch(r"([0-9]{13})-copilot-tool-output-[0-9a-f]+\.txt", path.name)
        require(match, "Use actual app-saved tool output")
        timestamps.append(int(match[1]) / 1000)
    observed = datetime.datetime.fromtimestamp(min(timestamps), datetime.timezone.utc)
    status = json.loads(status_path.read_bytes())
    roster_text = roster_path.read_text(encoding="utf-8")
    roster = json.loads(roster_text[roster_text.index("["):])
    output = ROOT / ("confirmation-" + family + "002-admission-input")
    require(not output.exists(), "Preserve previous admission input")
    status_ref = freeze_json(output / "status.json", status)
    roster_ref = freeze_json(output / "roster.json", roster)
    write_frozen(output / "original-roster-output.txt", roster_path.read_bytes())
    request_path = output / "request.json"
    freeze_json(request_path, {
        "statusPath": status_ref["path"], "rosterPath": roster_ref["path"],
        "observedAt": observed.isoformat(),
    })
    admit(OUT / ("N1-B132-" + family.upper() + "-CONFIRM-002-preflight.json"), request_path)


if __name__ == "__main__":
    main(*sys.argv[1:])
