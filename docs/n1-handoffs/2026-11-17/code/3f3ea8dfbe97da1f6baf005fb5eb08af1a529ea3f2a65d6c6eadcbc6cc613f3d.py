"""Immutable B134 paths and shared integrity checks."""
import json
import os
import stat
import sys
import uuid
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
HERE = ROOT / "neutral-preparation-001" / "projected-successor-001"
PROTOCOL = HERE / "protocol-001"
PACKET = HERE / "packet"
FORECAST = HERE / "capacity-measurement-001.json"
CORE = HERE / "core-chain-001.json"
REPO = WS / "b134-worktree"
COORDINATOR = "2451b10d-02a9-46ab-82d5-d90993f0cb8b"
CANDIDATE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
BASE = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
SUMS_SHA = "12cabfd9f51797c02f77c9513ad5ae6fe7f57aeceb6d180bf3cf24baf6c5c13e"
CORE_SHA = "82cb9c2c46e60357dbd8b61a59e6ff6204232622482fc35a7075f465a9fe436f"
FORECAST_SHA = "9701f4014bf22d9a26f609bc1be936d9fd3c34e5d45e13af11a44ef81cbc6928"
sys.path.insert(0, str(WS / "review-tools"))
from common import freeze_json, frozen, require, sha, start_guard, write_frozen


def verify_packet(guard=None):
    sums = json.loads(frozen(PACKET / "SHA256SUMS.json", SUMS_SHA))
    require({p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()}
            == set(sums) | {"SHA256SUMS.json"}, "Packet file inventory differs")
    for name, digest in sums.items():
        path = PACKET / name
        require(path.resolve().is_relative_to(PACKET.resolve()), "Unsafe packet member")
        frozen(path, digest)
        if guard:
            guard.check()
    return sums


def validate_report_destination(spec):
    report = Path(spec["report"])
    parent = report.parent
    require(report.is_absolute() and parent.is_dir() and not report.exists(), "Report path unavailable")
    info = parent.stat()
    require(bool(info.st_mode & stat.S_IWRITE)
            and not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_READONLY
            and os.access(parent, os.W_OK) and not any(parent.iterdir()), "Report directory not empty/writable")
    probe = parent / (".b134-readiness-" + uuid.uuid4().hex)
    made = False
    try:
        with probe.open("xb") as stream:
            made = True
            stream.write(b"B134 report path readiness\n")
        require(probe.read_bytes() == b"B134 report path readiness\n", "Report readback failed")
    finally:
        if made:
            probe.unlink()
    require(not report.exists() and not any(parent.iterdir()), "Report path changed during probe")
    return {"report": str(report), "parent": str(parent), "exclusiveCreateReadbackDelete": "PASS"}
