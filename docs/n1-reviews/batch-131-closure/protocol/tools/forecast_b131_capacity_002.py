"""Freeze a reproducible capacity/cap choice; never admit or launch a reviewer."""
import json

from b131_review_v2_common import (
    CALIBRATION, CALIBRATION_SHA, FORECAST, HERE, PACKET,
    freeze_json, frozen, load_batch, require, sha, start_guard, verify_packet)
from b131_capacity_002 import compute_forecast


def main():
    require(not FORECAST.exists(), "Preserve frozen capacity forecast")
    guard, _ = start_guard("B131 compact-002 conservative capacity forecast")
    try:
        _, sums, packet_sha = verify_packet(load_batch(131), guard)
        chain_path = HERE / "core-chain-compact-002.json"
        chain_raw = frozen(chain_path)
        calibration = json.loads(frozen(CALIBRATION, CALIBRATION_SHA))
        reference = json.loads(frozen(PACKET / "eligibility-reference.json"))
        catalog = json.loads(frozen(PACKET / "evidence/jmdict-extension-index.json"))["characters"]
        computed = compute_forecast(json.loads(chain_raw), calibration, sums, reference, catalog)
        computed.update(packetManifestSha256=packet_sha, chainManifestSha256=sha(chain_raw),
                        calibration={"path": str(CALIBRATION), "sha256": CALIBRATION_SHA})
        computed["memory"] = guard.finish()
        require(not computed["memory"]["breach"], "Forecast RAM breach")
        binding = freeze_json(FORECAST, computed)
        print(json.dumps({"record": binding, "status": computed["status"], "core": computed["coreTokens"],
                          "caps": computed["chosenCaps"], "peak": computed["projectedWorstCasePeak"],
                          "trials": [{"D": row["D"], "peak": row["projectedWorstCasePeak"]}
                                     for row in computed["trials"]]}))
        return 0 if computed["chosenCaps"] else 1
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    raise SystemExit(main())
