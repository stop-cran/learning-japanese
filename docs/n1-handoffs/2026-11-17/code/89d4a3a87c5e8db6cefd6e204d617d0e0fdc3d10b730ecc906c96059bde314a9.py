"""Immutable B134 lifecycle-012 paths and shared integrity checks."""
import json
import os
import stat
import sys
import uuid
from pathlib import Path

WS = Path(r"C:\Users\stop-\n1-kanji-workspace")
ROOT = WS / "scratch-134" / "review"
HERE = ROOT / "fresh-independent-002" / "lifecycle-011"
PROTOCOL = HERE / "protocol-012"
PACKET_ROOT = ROOT / "fresh-independent-002" / "projected-successor-011"
PACKET = PACKET_ROOT / "packet"
CORE = PACKET_ROOT / "fresh-independent-core-001.json"
CORE_SOURCES = PACKET_ROOT / "core-sources-011.json"
FROZEN_CORE = PACKET_ROOT / "frozen-core-011.json"
CAPACITY = ROOT / "meter-011-capacity-001" / "capacity.json"
ARTICLE_BOUNDS = ROOT / "fresh-independent-002" / "projected-successor-008" / "capacity-measurement-002.json"
PREPARATION = ROOT / "token-meter-011-preparation-002" / "preparation.json"
METER_AUDITS = {
    "claude": ROOT / "meter-011-claude-final-001" / "audit.json",
    "gpt": ROOT / "meter-011-gpt-final-001" / "audit.json",
}
LOSSLESS_VERIFICATION = ROOT / "successor-011-verification-001" / "verification.json"
REPO = WS / "b134-worktree"
COORDINATOR = "2451b10d-02a9-46ab-82d5-d90993f0cb8b"
PUBLISHED = "e17cb97c53ca4e3193dae5e11b52ba517fe86e76"
BASE = "ba80afffc20a72d31be68b355b6f90aab36a5726"
CANDIDATE = "355cccb840d22e7313e79f234eb93d1367e00352"

SUMS_SHA = "adeac0009e52039a57fd3121a45f0e91eb697a6f35b131db0517922f3d1b540c"
CORE_SHA = "49db3ba57325e7913a533b3b11b7ad810e6085123474327b037a6de7c7c31719"
CORE_SOURCES_SHA = "4c7cd5d0d52066fb44e762d8891bc942c8135a687c5d64b153a9f06ee59f0fe4"
FROZEN_CORE_SHA = "5ffe2892ad0cbc64fe118e3c5f34c44556ba44e1f13aaae0a80e9be05059b68c"
CAPACITY_SHA = "3aec7dc4d2701303145c8bfddbb698e2c180065c2298d115ae5b23b249a020d9"
ARTICLE_BOUNDS_SHA = "417f0b6f0834129eb6c0a1754279db97c1f78f1e4be99b651fa97db307c278c2"
PREPARATION_SHA = "af7d4568f464f853f77bd7975539e4ee69d36aa3cd45b83a9db0f894e87c3909"
LOSSLESS_SHA = "7ad06c861b4af2b2f722e54e6e200531919fb6cad6f8cd81541ea2d291571577"
METER_SHA = {
    "claude": "bedab1ae4f9121529a5f2309cf2a0e406b20a835291862f2b099262bd07533aa",
    "gpt": "5162bcc404d35b90a90d9ce75d50667e00dc40effc8549915003c06732e6ed42",
}
PROOFS = {
    "source-completeness-verification-008.json": {
        "path": str(ROOT / "fresh-independent-002" / "projected-successor-008"
                    / "source-completeness-verification-008.json"),
        "sha256": "acf95bca98d386bff469a413491e0f4ac9f6a4f1b322892f5a5b5a0c17efb989",
    },
    "reconciliation-verification-001/verification.json": {
        "path": str(ROOT / "reconciliation-verification-001" / "verification.json"),
        "sha256": "7ea9e7dde1989b5d1eb71bed3b5789ab77f4e3713277591b4841eeb2b0295da1",
    },
    "reconciliation-gate-verification-001/verification.json": {
        "path": str(ROOT / "reconciliation-gate-verification-001" / "verification.json"),
        "sha256": "7b0e846ede88b4a5350df16b58df0c4461e4ba83fc0208f006d65c3951170787",
    },
    "packet-verification-001/verification.json": {
        "path": str(ROOT / "packet-verification-001" / "verification.json"),
        "sha256": "fb95e655419fe9ecc0465ac565fb309397fb8843c22362b08cf5a1feda4d478a",
    },
}
RUNNER = ROOT / "guarded-test-v3.py"
RUNNER_SHA = "52d7b2a997aa707358556d7cbb0fa621e4383df45bf67c84b52bd729a52ad283"

sys.path.insert(0, str(WS / "review-tools"))
from common import freeze_json, frozen, require, sha, start_guard, write_frozen


PROMPT_ONLY_EVENT_TYPES = (
    "session.start", "session.permissions_changed", "session.info", "session.warning",
    "hook.start", "hook.end", "hook.start", "hook.end", "hook.start", "hook.end",
    "user.message", "system.message", "assistant.turn_start", "session.usage_record",
    "assistant.message", "tool.execution_start", "hook.start", "hook.end",
    "hook.start", "hook.end", "tool.execution_complete", "assistant.turn_end",
    "assistant.turn_start", "session.usage_record", "assistant.message", "assistant.turn_end",
    "hook.start", "hook.end", "session.usage_checkpoint",
)
PROMPT_ONLY_HOOK_TYPES = (
    "sessionStart", "userPromptSubmitted", "userPromptTransformed",
    "preToolUse", "postToolUse", "agentStop",
)


def validate_prompt_only_event_shape(events):
    """Allow only the observed host bootstrap envelope around one prompt-only view turn."""
    require(tuple(event.get("type") for event in events) == PROMPT_ONLY_EVENT_TYPES,
            "Bootstrap event snapshot contains unrecognized or extra activity")
    hooks = [event for event in events if event.get("type") in {"hook.start", "hook.end"}]
    starts = [event for event in hooks if event["type"] == "hook.start"]
    ends = [event for event in hooks if event["type"] == "hook.end"]
    require(len(starts) == len(ends) == len(PROMPT_ONLY_HOOK_TYPES),
            "Bootstrap hook envelope count differs")
    for index, expected in enumerate(PROMPT_ONLY_HOOK_TYPES):
        start = starts[index].get("data", {})
        end = ends[index].get("data", {})
        require(start.get("hookType") == end.get("hookType") == expected
                and start.get("hookInvocationId")
                and start.get("hookInvocationId") == end.get("hookInvocationId")
                and end.get("success") is True,
                "Bootstrap hook envelope is not a successful matched pair")
    turns = [event.get("data", {}).get("turnId") for event in events
             if event.get("type") in {"assistant.turn_start", "assistant.turn_end"}]
    require(turns == ["0", "0", "1", "1"], "Bootstrap turn boundary differs")


def verify_packet(guard=None):
    sums_raw = frozen(PACKET / "SHA256SUMS.json", SUMS_SHA)
    sums = json.loads(sums_raw)
    actual = {p.relative_to(PACKET).as_posix() for p in PACKET.rglob("*") if p.is_file()}
    require(actual == set(sums) | {"SHA256SUMS.json"}, "Packet file inventory differs")
    require(len(sums) == 1507, "Frozen packet source count differs")
    for name, digest in sums.items():
        path = PACKET / Path(name)
        require(path.resolve().is_relative_to(PACKET.resolve()), "Unsafe packet member")
        frozen(path, digest)
        if guard:
            guard.check()
    return sums


def verify_core(guard=None):
    core_raw = frozen(CORE, CORE_SHA)
    core = json.loads(core_raw)
    source_index = json.loads(frozen(CORE_SOURCES, CORE_SOURCES_SHA))
    frozen(FROZEN_CORE, FROZEN_CORE_SHA)
    proof = json.loads(frozen(LOSSLESS_VERIFICATION, LOSSLESS_SHA))
    require(len(core["sources"]) == len(set(row["source"] for row in core["sources"])) == 90
            and len(core["segments"]) == 64
            and core["segments"][0]["index"] == 1
            and core["segments"][-1]["index"] == 64,
            "Frozen successor-011 core inventory differs")
    require(core["sources"] and core["sources"][0]["source"] == "REVIEW.md"
            and core["sources"][1]["source"] == "evidence/lossless-core-representation-guide.md"
            and source_index["sources"] == [row["source"] for row in core["sources"]],
            "Core source order or representation guide differs")
    require(not any("author-response" in row["source"].lower()
                    or "report" in row["source"].lower()
                    and ("initial-" in row["source"].lower() or "fresh-" in row["source"].lower())
                    for row in core["sources"]),
            "Prior reviewer or author-response material entered the core")
    chain_root = PACKET_ROOT / "chains" / "fresh-independent-core-001"
    total_bytes = 0
    for index, row in enumerate(core["segments"], 1):
        path = Path(row["path"])
        require(path.resolve().is_relative_to(chain_root.resolve())
                and row["index"] == index and row["bytes"] < 16000,
                "Unsafe or reordered core segment")
        raw = frozen(path, row["sha256"])
        require(len(raw) == row["bytes"] and raw.endswith(b"\n"), "Core segment size differs")
        total_bytes += len(raw)
        if guard:
            guard.check()
    require(total_bytes == proof["chainBytes"] == 815589
            and proof["coreManifestSha256"] == CORE_SHA
            and proof["coreSources"] == 90 and proof["segments"] == 64
            and proof["payloadBytes"] == 773285,
            "Successor-011 lossless proof differs")
    return core


def validate_report_destination(spec):
    report = Path(spec["report"])
    parent = report.parent
    require(report.is_absolute() and parent.is_dir() and not report.exists(),
            "Report path unavailable")
    info = parent.stat()
    require(bool(info.st_mode & stat.S_IWRITE)
            and not getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_READONLY
            and os.access(parent, os.W_OK) and not any(parent.iterdir()),
            "Report directory not empty/writable")
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
    require(not report.exists() and not any(parent.iterdir()),
            "Report path changed during readiness probe")
    return {"report": str(report), "parent": str(parent),
            "exclusiveCreateReadbackDelete": "PASS"}
