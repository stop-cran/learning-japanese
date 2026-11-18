"""Isolated compact-002 preparation paths; no held review records are inputs."""
import json
from pathlib import Path

from common import (CHECKS, COORDINATOR, GUARD, GUARD_SHA, SNAP, TOOLS, WS, freeze_json,
                    frozen, json_bytes, load_module, require, sha, start_guard, write_frozen)
from b131_neutral_common_001 import BASE, CANDIDATE, MEMBERS, PROOFS, RECORDS, REPO, RUNNER, SOURCE_BASE

OLD_HERE = RECORDS / "preparation-001"
OLD_PACKET = WS / "review-packets" / "batch-131-1359b467-compact-001"
OLD_PACKET_SHA = "454c924ce460d050d31eedca225b9553d42790a0060df474088e38c7ca049b39"
CONTRACT_SHA = "94c879183f0e012cf5c6ff64189dc5fb92a2b8e310cc9c58dde263b83e3f532d"
CALIBRATION = RECORDS / "capacity" / "claude001-calibration-001.json"
CALIBRATION_SHA = "aca593742a9191eec34aa7b8774b4042789bdf7d0025fcfe0d06896b0a3041da"
HERE = RECORDS / "preparation-002"
PACKET = WS / "review-packets" / "batch-131-1359b467-compact-002"
FORECAST = HERE / "capacity-forecast-compact-002.json"
RUNS = ("N1-B131-CLAUDE-002", "N1-B131-GPT-002")


def review_dir(batch):
    require(int(batch) == 131, "Compact-002 is B131-only")
    return HERE


def packet_dir(config):
    require(config["batch"] == 131 and config["candidate"] == CANDIDATE, "Packet identity differs")
    return PACKET


def load_batch(batch):
    value = json.loads(frozen(review_dir(batch) / "batch.json"))
    require(value["candidate"] == CANDIDATE and value["base"] == BASE and value["members"] == MEMBERS
            and value["repo"] == str(REPO), "Candidate configuration differs")
    value["configSha256"] = sha(frozen(HERE / "batch.json"))
    return value


def verify_packet(config, guard=None):
    raw = frozen(packet_dir(config) / "SHA256SUMS.json")
    require(sha(raw) == config["packetManifestSha256"], "Packet manifest changed")
    sums = json.loads(raw)
    for relative, digest in sums.items():
        path = PACKET / relative
        require(path.resolve().is_relative_to(PACKET.resolve()), "Unsafe packet member")
        frozen(path, digest)
        if guard:
            guard.check()
    require(sorted(p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file())
            == sorted([*sums, "SHA256SUMS.json"]), "Packet has unlisted members")
    return PACKET, sums, sha(raw)


def verify_inputs(guard):
    raw = frozen(OLD_PACKET / "SHA256SUMS.json", OLD_PACKET_SHA)
    sums = json.loads(raw)
    require(sorted(p.relative_to(OLD_PACKET).as_posix() for p in OLD_PACKET.rglob("*") if p.is_file())
            == sorted([*sums, "SHA256SUMS.json"]), "Original packet members changed")
    for name, digest in sums.items():
        frozen(OLD_PACKET / name, digest)
        guard.check()
    contract_raw = frozen(OLD_HERE / "source-contract.json", CONTRACT_SHA)
    contract = json.loads(contract_raw)
    for binding in contract["files"].values():
        frozen(binding["path"], binding["sha256"])
        guard.check()
    calibration_raw = frozen(CALIBRATION, CALIBRATION_SHA)
    calibration = json.loads(calibration_raw)
    frozen(calibration["coreChain"], calibration["coreChainSha256"])
    from verify_b131_sources import FINGERPRINT, Git, OWNER
    git = Git(REPO, RUNNER, guard)
    require(git("rev-parse", "HEAD").decode().strip() == CANDIDATE
            and not git("status", "--porcelain=v1", "--untracked-files=all"),
            "Candidate is not the unchanged clean checkout")
    require(git("show", "-s", "--format=%P|%G?|%GF|%ae|%ce", CANDIDATE).decode().strip()
            == f"{BASE}|G|{FINGERPRINT}|{OWNER}|{OWNER}", "Signed candidate identity changed")
    return sums, calibration
