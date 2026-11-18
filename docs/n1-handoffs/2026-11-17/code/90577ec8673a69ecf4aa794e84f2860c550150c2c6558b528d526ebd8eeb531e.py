"""Material immutable-subset handoff only; explicitly not reviewer/protocol readiness."""
import json
from b131_review_v2_common import (
    FORECAST, HERE, PACKET, freeze_json, frozen, require, sha, start_guard)
from b131_preflight_002 import verify_subset


def main():
    guard, _ = start_guard("B131 compact-002 immutable-subset verification")
    try:
        result = verify_subset(guard, initial=True)
        paths = [PACKET / "SHA256SUMS.json", HERE / "packet-build-002.json",
                 HERE / "derivation-verification-002.json",
                 PACKET / "evidence/kanjidic2-review-projection.xml",
                 PACKET / "evidence/jmdict-review-core.xml",
                 PACKET / "evidence/title-index-delta.txt",
                 PACKET / "evidence/jmdict-extension-index.json",
                 HERE / "core-chain-compact-002.json", FORECAST]
        result["files"] = [{"path": str(path), "sha256": sha(frozen(path)),
                            "bytes": path.stat().st_size} for path in paths]
        result["remaining"] = "Prompts, new audit/lifecycle configs and focused rejection tests are NOT READY."
        result["limits"] = (
            "Preparation only. No reviewer admitted/launched. No teaching edits, commits, pushes or publication. "
            "JMdict615 core records249780 record-line bytes plus19 framing bytes=249799. "
            "Original compact-001 filenames/bytes retained except required REVIEW.md/packet.json replacements. "
            "Separate immutable complete remainder-record files support future independently selected exact-keb evidence.")
        result["memory"] = guard.finish()
        require(not result["memory"]["breach"], "Subset verification RAM breach")
        binding = freeze_json(HERE / "partial-handoff-002.json", result)
        print(json.dumps({"handoff": binding, **result}, ensure_ascii=False))
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise


if __name__ == "__main__":
    main()
