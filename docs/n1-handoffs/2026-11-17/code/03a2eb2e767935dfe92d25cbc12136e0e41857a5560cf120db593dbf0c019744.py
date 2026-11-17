"""Preserve closure134 while permitting its exact config-pinned tool inputs.

The original reader remains unchanged for review data. Only the nineteen external
producer files shared by the two frozen reviewer inventories are additionally
readable, and only with the inventory's exact supplied hash.
"""
import json
import sys
from pathlib import Path

from common import WS, frozen, require, sha

SOURCE = Path(__file__).with_name("close_b134.py")
SOURCE_SHA = "23a637e2489b378565aa0308de9ce0d13441beebb3e2ade0fb134a6a0fb88b2f"
frozen(SOURCE, SOURCE_SHA)
import close_b134 as original

ROOT = original.ROOT
CONFIG_ROOT = ROOT / "fresh-independent-002" / "lifecycle-011" / "audit-configs-020"
CONFIGS = {
    "claude": "05688385b07d0b00a9a98077014a26aae23a6e06713c7ddb29e78855a3d12d22",
    "gpt": "387f8763fd7514704baaa1fe2c8b7a7fcbd39ac28917ba06600d79e670308571",
}
original_reader = original.read_review


def external_inputs():
    inventories = []
    for family, digest in CONFIGS.items():
        config = json.loads(frozen(CONFIG_ROOT / ("audit-" + family + "-fresh-003.json"), digest))
        external = {}
        for item in config["files"]:
            path = Path(item["path"]).resolve()
            if not path.is_relative_to(ROOT):
                require(path.parent == (WS / "review-tools").resolve()
                        and path not in external, "Unexpected external producer input")
                external[path] = item["sha256"]
        inventories.append(external)
    require(len(inventories[0]) == 19 and inventories[0] == inventories[1],
            "The frozen reviewer inventories disagree about external producers")
    return inventories[0]


EXTERNAL = external_inputs()


def read_review(path, digest=None):
    path = Path(path).resolve()
    if path.is_relative_to(ROOT):
        return original_reader(path, digest)
    require(path in EXTERNAL and digest == EXTERNAL[path],
            "External review input is not exactly bound by both frozen configs")
    return frozen(path, digest)


def main(mode, request_path, output):
    raw = frozen(Path(__file__))
    request = json.loads(read_review(request_path))
    require(any(item["archivePath"] == "protocol/close_b134_v2.py"
                and item["sha256"] == sha(raw)
                and read_review(item["path"], item["sha256"]) == raw
                for item in request["evidence"]),
            "Closure must retain this scope-repair producer")
    original.read_review = read_review
    try:
        original.main(mode, request_path, output)
    finally:
        original.read_review = original_reader


if __name__ == "__main__":
    require(len(sys.argv) == 4, "close_b134_v2.py dry|real REQUEST_JSON OUTPUT")
    main(sys.argv[1], Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve())
