"""Bind the revision verifier to the author's actual committed-gate schema."""
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent
SOURCE_SHA = "27b972fd0f7a2df2ef897616f87054cec3d5ab880ee7bacc9ade830ce9a7a67e"
OLD = '''        require(summary["status"] == "PASS" and summary["base"] == config["base"]
                and summary["startingHead"] == candidate and set(summary["checks"]) == set(CHECKS)
                and len(summary["checks"]) == len(CHECKS)
                and summary["manifestSha256"] == sha(raw_manifest) and summary["manifestReproducible"],
                "Gate summary is not for the exact committed revision")
'''
NEW = '''        check_summary(summary, config, candidate, sha(raw_manifest))
'''
HELPER = '''
def check_summary(summary, config, candidate, manifest_sha):
    require(summary["status"] == "PASS" and summary["mode"] == "committed"
            and summary["base"] == config["base"] and summary["parent"] == config["candidate"]
            and summary["head"] == candidate and set(summary["checks"]) == set(CHECKS)
            and len(summary["checks"]) == len(CHECKS)
            and summary["manifestSha256"] == manifest_sha and summary["manifestReproducible"],
            "Gate summary is not for the exact committed revision")


'''


def main():
    source = HERE / "verify_b121_revision.py"
    original_raw = frozen(source, SOURCE_SHA)
    original = original_raw.decode("utf-8").replace("\r\n", "\n")
    require(original.replace("\n", "\r\n").encode("utf-8") == original_raw,
            "Expected uniform original CRLF endings")
    require(original.count(OLD) == 1 and original.count("def verify(candidate, gates, output):") == 1,
            "Original verifier differs")
    derived = original.replace(OLD, NEW).replace(
        "def verify(candidate, gates, output):", HELPER + "def verify(candidate, gates, output):"
    )
    require(derived.replace(HELPER, "").replace(NEW, OLD) == original, "Reverse delta differs")
    compile(derived, "verify_b121_revision_v2.py", "exec")
    output = write_frozen(HERE / "verify_b121_revision_v2.py",
                          derived.replace("\n", "\r\n").encode("utf-8"))
    freeze_json(WS / "scratch-121" / "review" / "revision-verifier-v2-derivation.json", {
        "source": {"path": str(source), "sha256": SOURCE_SHA},
        "output": output,
        "reverseExact": True,
        "reason": "The actual run-gates.py summary uses head, not the prepared startingHead key. "
                  "Require committed mode and the exact parent as well; do not rewrite receipts.",
        "producer": {"path": str(Path(__file__)), "sha256": sha(Path(__file__).read_bytes())},
        "publicationAccepted": False,
    })


if __name__ == "__main__":
    main()
