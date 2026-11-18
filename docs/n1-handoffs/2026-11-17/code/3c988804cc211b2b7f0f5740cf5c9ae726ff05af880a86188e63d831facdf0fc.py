"""Freeze the unchanged capacity calculation using both exact-core 011 meter audits."""
import json
import sys
from pathlib import Path

import b134_token_meter as meter
from common import WS, freeze_json, frozen, require, sha, start_guard, write_frozen

ROOT = WS / "scratch-134" / "review"
CORE_SHA = "49db3ba57325e7913a533b3b11b7ad810e6085123474327b037a6de7c7c31719"
PREPARATION = ROOT / "token-meter-011-preparation-002" / "preparation.json"
PREPARATION_SHA = "af7d4568f464f853f77bd7975539e4ee69d36aa3cd45b83a9db0f894e87c3909"
SESSIONS = {
    "claude": "439ba40b-5cb0-4669-a3c8-de1e385dc321",
    "gpt": "00039869-7c08-4e94-8224-a5d4fd673a60",
}


def main(output):
    require(output.parent == ROOT and not output.exists(), "Use a new direct review output")
    guard, _ = start_guard("B134 measured capacity 011")
    try:
        preparation_raw = frozen(PREPARATION, PREPARATION_SHA)
        measurements, bindings = [], {}
        for family, session in SESSIONS.items():
            _, spec, _ = meter.load_preparation(PREPARATION, family)
            path = ROOT / f"meter-011-{family}-final-001" / "audit.json"
            raw = frozen(path)
            record = json.loads(raw)
            require(record["session"] == session and record["family"] == family
                    and spec["core"]["sha256"] == CORE_SHA
                    and record["producerSha256"] == sha(Path(meter.__file__).read_bytes()),
                    "Audit belongs to a different meter or executable")
            for key in ("events", "admission"):
                ref = record[key]
                frozen(ref["path"], ref["sha256"])
            admission = json.loads(frozen(record["admission"]["path"]))
            require(admission["preparation"]["sha256"] == sha(preparation_raw),
                    "Audit admission belongs to another preparation")
            measurements.append(record)
            bindings[family] = {"path": str(path), "sha256": sha(raw)}
            guard.check()
        verification_path = ROOT / "successor-011-verification-001" / "verification.json"
        verification_raw = frozen(
            verification_path, "7ad06c861b4af2b2f722e54e6e200531919fb6cad6f8cd81541ea2d291571577")
        verification = json.loads(verification_raw)
        require(verification["coreManifestSha256"] == CORE_SHA
                and verification["retainedPredecessorFiles"] == 1461,
                "Lossless successor verification differs")
        bounds_path = ROOT / "fresh-independent-002" / "projected-successor-008" / "capacity-measurement-002.json"
        bounds_raw = frozen(bounds_path)
        bounds = json.loads(bounds_raw)
        require(bounds["candidate"] == "355cccb840d22e7313e79f234eb93d1367e00352",
                "Article bounds belong to another candidate")
        result = meter.measured_forecasts(measurements, CORE_SHA, bounds["trials"])
        result.update(
            measurements=bindings,
            preparation={"path": str(PREPARATION), "sha256": sha(preparation_raw)},
            articleBounds={"path": str(bounds_path), "sha256": sha(bounds_raw)},
            losslessVerification={"path": str(verification_path), "sha256": sha(verification_raw)},
        )
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Measured capacity RAM breach")
    result["memory"] = memory
    result["producer"] = write_frozen(output / "producer.py", Path(__file__).read_bytes())
    print(json.dumps(freeze_json(output / "capacity.json", result)))


if __name__ == "__main__":
    require(len(sys.argv) == 2, "b134_measured_capacity_011.py NEW_OUTPUT_DIRECTORY")
    main(Path(sys.argv[1]).resolve())
