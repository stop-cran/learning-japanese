"""B131-only immutable paths and checks for neutral independent-review preparation."""
import json
from pathlib import Path

from common import (CHECKS, COORDINATOR, GUARD, GUARD_SHA, SIGNER, SNAP, TOOLS, WS,
                    freeze_json, frozen, json_bytes, load_module, readonly, require,
                    sha, start_guard, word, write_frozen)

CANDIDATE = "1359b467e0edee8822c665614d6ca57e42785c4d"
BASE = "cb0f5581bdda84f7e673225c19126c85e242e57b"
SOURCE_BASE = "6da1184b82b60553f9b65c57f53289c779f96f7c"
MEMBERS = ["\u885b", "\u7f8a", "\u971c"]
REPO = WS / "b131-worktree"
RECORDS = WS / "scratch-131" / "review"
HERE = RECORDS / "preparation-001"
PACKET = WS / "review-packets" / "batch-131-1359b467-compact-001"
RUNNER = {"path": str(RECORDS / "guarded-test-v3.py"),
          "sha256": "da78564efadb90ac4c174dbf13e375327b611bc5e0fc77913c8b85c22c1aaf6b"}
PROOFS = {
    "source-verification-001.json": "99a7a9a11c213280ddae0110fceec9599a7d4d47451e1b3fb1ae6a9e2ab6ac33",
    "source-union-verification-001.json": "1735390e50f8768da2cdf264b8157dc19a31e690970cd689b4fc9077e97677f5",
    "payload-verification-001.json": "dc3f1068362350bd81fdc8ec94e20b32589b0fdcdb25248a911e4817ffb068d6",
    "gate-verification-002/verification.json": "82fbf0d68e879e0371e9226ac322c81c2e13118fdbd5711e7901bef79f155751",
    "packet-verification-002/verification.json": "cefe31cf4020dcad2601bafff5446451c73cda86b451f34b54da7683a8167c89",
}


def review_dir(batch):
    require(int(batch) == 131, "This tooling is limited to B131")
    return HERE


def load_batch(batch):
    value = json.loads(frozen(review_dir(batch) / "batch.json"))
    require(value["batch"] == 131 and value["candidate"] == CANDIDATE
            and value["base"] == BASE and value["sourceBase"] == SOURCE_BASE
            and value["members"] == MEMBERS and value["repo"] == str(REPO),
            "B131 candidate configuration changed")
    value["configSha256"] = sha(frozen(HERE / "batch.json"))
    return value


def packet_dir(config):
    require(config["batch"] == 131 and config["candidate"] == CANDIDATE, "Packet identity differs")
    return PACKET


def verify_packet(config, guard=None):
    root = packet_dir(config)
    raw = frozen(root / "SHA256SUMS.json")
    sums = json.loads(raw)
    for relative, expected in sums.items():
        path = root / relative
        require(path.resolve().is_relative_to(root.resolve()), "Unsafe packet path")
        frozen(path, expected)
        if guard:
            guard.check()
    require(sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
            == sorted([*sums, "SHA256SUMS.json"]), "Unlisted packet file")
    return root, sums, sha(raw)
