"""Run a frozen shared review tool with B127's bounded Git subprocess helper."""
import json
import runpy
import sys
from pathlib import Path

import common
import verify_b127_sources as sources


def main():
    common.require(len(sys.argv) >= 2, "Usage: run_b127_tool.py TOOL.py [ARGS]")
    path = Path(sys.argv[1]).resolve()
    common.require(path.parent == common.TOOLS and path.suffix == ".py", "Tool must be in review-tools")
    raw = common.frozen(path)
    original_start = common.start_guard

    def start_guard(label):
        guard, resource = original_start(label)
        sources.ACTIVE_GUARD = guard
        return guard, resource

    def git(config, *args):
        return sources.git(*args, repo=Path(config["repo"]))

    common.start_guard = start_guard
    common.git = git
    print(json.dumps({"tool": str(path), "sha256": common.sha(raw),
                      "adapterSha256": common.sha(Path(__file__).read_bytes()),
                      "gitHelperSha256": common.sha(common.frozen(Path(sources.__file__)))}), flush=True)
    sys.argv = [str(path), *sys.argv[2:]]
    try:
        runpy.run_path(str(path), run_name="__main__")
    finally:
        sources.ACTIVE_GUARD = None


if __name__ == "__main__":
    main()
