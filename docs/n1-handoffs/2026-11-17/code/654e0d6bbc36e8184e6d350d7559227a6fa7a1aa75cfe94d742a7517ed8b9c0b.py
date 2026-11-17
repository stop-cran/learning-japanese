"""Freeze the B134 lossless-successor builders, verifier, executions and o200k projection (continuation-tools-005)."""
import json
import shutil
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

R = WS / "scratch-134" / "review"
OUT = R / "continuation-tools-005"
TOOLS = ["build_b134_successor_009.py", "build_b134_successor_010.py", "build_b134_successor_011.py",
         "verify_b134_successor_011.py", "freeze_b134_successor_011.py"]
EXECUTIONS = ["successor-009-build-execution-001", "successor-010-build-execution-001",
              "successor-011-build-execution-001", "successor-011-verification-execution-001"]
SUCC = R / "fresh-independent-002"
PINS = {
    "codecFreeze004": (R / "continuation-tools-004" / "index.json",
                       "274bedd21e6d2fa754b90f9cd350dbacb651f52ebe6e283434420d7e15f977b8"),
    "frozenCore009": (SUCC / "projected-successor-009" / "frozen-core-009.json", None),
    "frozenCore010": (SUCC / "projected-successor-010" / "frozen-core-010.json",
                      "266bef4a1c2e0047e0b267c53ee234604d2c88c5000eac037cd73f7585574390"),
    "frozenCore011": (SUCC / "projected-successor-011" / "frozen-core-011.json",
                      "5ffe2892ad0cbc64fe118e3c5f34c44556ba44e1f13aaae0a80e9be05059b68c"),
    "packetSums011": (SUCC / "projected-successor-011" / "packet" / "SHA256SUMS.json",
                      "adeac0009e52039a57fd3121a45f0e91eb697a6f35b131db0517922f3d1b540c"),
    "core011": (SUCC / "projected-successor-011" / "fresh-independent-core-001.json",
                "49db3ba57325e7913a533b3b11b7ad810e6085123474327b037a6de7c7c31719"),
    "verification011": (R / "successor-011-verification-001" / "verification.json",
                        "7ad06c861b4af2b2f722e54e6e200531919fb6cad6f8cd81541ea2d291571577"),
}


def main():
    require(not OUT.exists(), "continuation-tools-005 already exists")
    pins = {}
    for key, (path, expected) in PINS.items():
        raw = frozen(path, expected)
        pins[key] = {"path": str(path), "sha256": sha(raw), "bytes": len(raw)}
    files = {}
    for name in TOOLS:
        source = WS / "review-tools" / name
        ref = write_frozen(OUT / "tools" / name, source.read_bytes())
        files[name] = dict(ref, sourcePath=str(source))
    executions = {}
    for name in EXECUTIONS:
        receipt = json.loads(frozen(R / name / "receipt.json"))
        require(receipt["exitCode"] == 0 and receipt["memory"]["breach"] is None, "Execution did not pass: " + name)
        executions[name] = {item.name: write_frozen(OUT / "executions" / name / item.name, item.read_bytes())
                            for item in sorted((R / name).iterdir())}
    index = {
        "status": "LOSSLESS_SUCCESSOR_011_BUILT_VERIFIED_PROJECTED_NOT_MEASURED_NOT_REVIEW_ADMISSION",
        "files": files, "executions": executions, "pins": pins,
        "intermediates": {
            "009": "XML-only lossless encoding; frozen and preserved; never metered.",
            "010": "DEFECTIVE: its reading-guide example reused real ent_seq 1013030 with invented content "
                   "(fabricated record); preserved, never metered or used for review.",
            "011": "Candidate: 010 representation with the guide example derived verbatim from real record "
                   "473 (ent_seq 1554300) of the packet; independently verified lossless.",
        },
        "o200kProjection": {
            "method": "011 o200k chain tokens x measured 008 Claude segment-growth/o200k ratio (1.4653), "
                      "plus 620 non-segment growth; forecast = ceil(growth*1.1)+12000; total = forecast + "
                      "article forecast + 130000 reserves.",
            "o200k008": 321955, "o200k011": 253881, "projectedClaudeGrowth": 372634, "coreForecast": 421898,
            "tiers": {"25/10": [707293, "HOLD"], "20/10": [685696, "PASS"], "15/10": [663654, "PASS"],
                      "10/10": [640791, "PASS"], "10/5": [626175, "PASS"]},
            "limits": "Projection only; actual Claude and GPT meters on 011 decide admission.",
        },
        "reviewerAdmitted": False, "published": False,
    }
    print(json.dumps(freeze_json(OUT / "index.json", index)))


if __name__ == "__main__":
    main()
