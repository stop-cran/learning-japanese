"""Freeze the focused source finding and admit the original B123 author."""
import datetime
import json
import sys
from pathlib import Path

from common import (WS, freeze_json, frozen, git, load_batch, load_module, require,
                    sha, start_guard, write_frozen)
from confirm_v2 import clean
from scoped_admission import assess_status

CANDIDATE = "65f04ca52a310d517ecb05fb17434cb4f41a118d"
AUTHOR = "3fb8a285-ebf3-456e-89ed-5e4b77b0f0a1"
REVIEW = WS / "scratch-123" / "review"


def main(status_path):
    config = load_batch(123)
    clean(config, CANDIDATE)
    proofs = []
    for name, digest in (
        ("coordinator-reconciliation-verification-001.json",
         "7bd65759c91939c536dfb03a00ff461fcbc30a0f293b5ddb78d7fb0f404f3f20"),
        ("coordinator-reconciliation-selection-001.json",
         "25de95031769bf33c53ffe8c9f3a0c9b05d2d0198c90f455797ab611c2b9f742"),
    ):
        raw = frozen(REVIEW / name, digest)
        proof = json.loads(raw)
        require(proof["candidate"] == CANDIDATE and proof["status"] == "PASS",
                "Reconciliation verification not accepted mechanically")
        proofs.append({"path": str(REVIEW / name), "sha256": digest})
    for family in ("CLAUDE", "GPT"):
        prior = json.loads(frozen(REVIEW / f"N1-B123-{family}-001-acceptance.json"))
        require(prior["reviewAccepted"] and prior["candidate"] == config["candidate"],
                "Initial review evidence not accepted")
    sys.path.insert(0, str(WS / "lean"))
    from n1lib import parse
    card = git(config, "show", f"{CANDIDATE}:kanji/範.md")
    comparison = git(config, "show", f"{CANDIDATE}:kanji/普.md")
    current, _ = parse(card.decode("utf-8").replace("\r\n", "\n"))
    other, _ = parse(comparison.decode("utf-8").replace("\r\n", "\n"))
    packet = WS / "review-packets" / "batch-123-3bda01ae"
    sums = json.loads(frozen(packet / "SHA256SUMS.json"))
    source_path = "evidence/external-snapshots/01-extract.txt"
    source = frozen(packet / source_path, sums[source_path])
    require(comparison == frozen(packet / "repo" / "kanji" / "普.md",
                                 sums["repo/kanji/普.md"]), "Comparison snapshot changed")
    require(other["title"] == "universal; widespread" and "普" not in current["quiz_exclusions"]
            and "範" not in other.get("quiz_exclusions", []), "Focused pair state differs")
    require("広く行き渡る" in source.decode("utf-8")
            and "widespread sense" in card.decode("utf-8"), "Widespread source or delta missing")
    finding = freeze_json(REVIEW / "reconciliation-001-source-adjudication.json", {
        "batch": 123, "candidate": CANDIDATE, "mechanicalProofs": proofs,
        "status": "NEEDS_FOCUSED_AUTHOR_CORRECTION_BEFORE_CONFIRMATION",
        "findings": [{
            "id": "C1", "pair": ["範", "普"], "confidence": "high",
            "evidence": [
                {"path": "kanji/範.md", "line": 51, "sha256": sha(card)},
                {"path": "kanji/普.md", "lines": [3, 20], "sha256": sha(comparison)},
                {"path": str(packet / source_path), "line": 21, "sha256": sha(source)},
            ],
            "reason": "The newly foregrounded, independently attested widespread branch admits "
                      "the counterpart's displayed widespread label. Neither endpoint excludes "
                      "the direct pair; an exclusion with 広 is not transitive.",
            "requiredChange": "Add a direct 普 guard and source-backed neutral pair disposition.",
        }],
        "remainingNoNewGuardPairs": list("本像囲方度計測量理"),
        "limits": "Those nine pair decisions remain hypotheses for source-based independent "
                  "confirmation, not closed harmlessness claims. No review or publication acceptance.",
    })
    brief = REVIEW / "b123-reconciliation-002-brief.txt"
    brief.chmod(0o444)
    brief_binding = {"path": str(brief), "sha256": sha(frozen(brief))}
    source_status = Path(status_path)
    now = datetime.datetime.now(datetime.timezone.utc)
    require(abs(now.timestamp() - source_status.stat().st_mtime) < 180, "Status snapshot stale")
    status_raw = source_status.read_bytes()
    guard, resource = start_guard("B123 focused author admission")
    assessment = assess_status(json.loads(status_raw), "", resource.available_ram())
    memory = guard.finish()
    require(not memory["breach"] and assessment["startupFloorMet"]
            and not assessment["blockingSessions"], json.dumps(assessment, ensure_ascii=False))
    status = json.loads(status_raw)
    author = [item for item in status["sessions"] if item["id"] == AUTHOR]
    require(len(author) == 1 and author[0]["activity"]["status"] == "idle"
            and not author[0].get("awaiting_user_input"), "Original author not ready")
    clean(config, CANDIDATE)
    frozen(Path(__file__).with_name("scoped_admission.py"),
           "e40e5107ef31e3040c0b212786dbce0f680b1d718b3cdbb7bb9a086aeaea7df8")
    Path(__file__).chmod(0o444)
    print(json.dumps(freeze_json(REVIEW / "b123-reconciliation-002-admission.json", {
        "batch": 123, "candidate": CANDIDATE, "author": AUTHOR,
        "brief": brief_binding, "finding": finding,
        "status": write_frozen(REVIEW / "b123-reconciliation-002-admission-status.json", status_raw),
        "assessment": assessment, "memory": memory, "admittedAt": now.isoformat(),
        "producerSha256": sha(Path(__file__).read_bytes()),
        "scope": "One original-author follow-up; no confirmation, publication or additional batch.",
    })))
    print(json.dumps(brief_binding))


if __name__ == "__main__":
    main(sys.argv[1])
