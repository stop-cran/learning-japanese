"""Specialize the prior full served-tree and owner-checkpoint verifier for actual B133."""
from common import TOOLS, WS, freeze_json, frozen, sha, write_frozen


def main():
    original = frozen(TOOLS / "finish_b132_delivery.py")
    raw = original
    for before, after in (
        (b"b132", b"b133"), (b"B132", b"B133"), (b"batch-132", b"batch-133"),
        (b"902d6021214aaf28f8bdf41b9920b0d76a79b83c", b"c12af4c508ba7d2f82d92d86569b83e8ad4204f1"),
        (b"8739", b"8745"), (b"adbf488f76c55cc2", b"a4afe85384bc1452"),
        (b"268", b"271"), (b"262", b"265"), (b"960", b"957"),
        (b'["\\u5893"]', b'["\\u7434", "\\u925b", "\\u6edd"]'),
    ):
        raw = raw.replace(before, after)
    compile(raw, "finish_b133_delivery.py", "exec")
    print(freeze_json(WS / "scratch-133" / "review" / "finish-tool-001.json", {
        "originalSha256": sha(original),
        "successor": write_frozen(TOOLS / "finish_b133_delivery.py", raw),
        "scope": "Only actual batch, publication commit, manifest version, runtime and source-accounting "
                 "constants changed. Full served-entry equality, signature/lineage, CI, checkpoint "
                 "deduplication and owner/readback validation remain required.",
    }))


if __name__ == "__main__":
    main()
