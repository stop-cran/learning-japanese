"""Derive B134 publication checks from the previously used B133 recorder."""
import json
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, start_guard, write_frozen
from run_b134_closure_checks import BASE, HERE, REPO, lineage
from verify_b134_packet import RUNNER
from verify_b134_sources import Git

SOURCE = "record_b133_publication_v2.py"
SOURCE_SHA = "72b0506bb65342b4bc88ffdf3f79c353416b8bc251023465f1dcdcd1e6f15f36"
REVIEWED = "355cccb840d22e7313e79f234eb93d1367e00352"


def derive(raw):
    text = raw.decode("utf-8")
    require(text.count("def validate_reviews(") == text.count("def validate_gate(") == 1,
            "Publication source layout differs")
    start = text.index("def validate_reviews(")
    end = text.index("def validate_gate(")
    text = text[:start] + text[end:]
    old = "from b133_closure_origins import validate_final_identity, validate_history"
    new = (
        "from b134_closure_progress import validate_archived_resolution, validate_progress\n"
        "from b134_initial_records import INITIALS, actual_initial"
    )
    require(text.count(old) == 1, "Publication import differs")
    text = text.replace(old, new)
    old = 'from record_b130_publication import comment_body, delivery_accounting, load_narrative'
    require(text.count(old) == 1, "Accounting import differs")
    text = text.replace(old, 'from record_b130_publication import comment_body, load_narrative')
    text = text.replace("b133", "b134").replace("B133", "B134")
    old = (
        '                == sorted([*inventory, "provenance.json"]), "Closure tree differs from inventory")\n'
        '        source_index = '
    )
    new = (
        '                == sorted([*inventory, "provenance.json"]), "Closure tree differs from inventory")\n'
        '        original_claims = {}\n'
        '        for family in INITIALS:\n'
        '            _, refs, _, claims = actual_initial(family)\n'
        '            report = refs["report"]\n'
        '            original_claims[family] = {\n'
        '                "report": frozen(report["path"], report["sha256"]),\n'
        '                "reportSha256": report["sha256"], "claims": claims,\n'
        '            }\n'
        '        validate_archived_resolution(\n'
        '            closure, lambda name, digest: frozen(closure_path / name, digest), original_claims)\n'
        '        source_index = '
    )
    require(text.count(old) == 1, "Publication inventory boundary differs")
    text = text.replace(old, new)
    require("b133" not in text and "B133" not in text, "Stale B133 identity")
    compile(text, "record_b134_publication.py", "exec")
    return text.encode("utf-8")


def main(output):
    require(output.parent == HERE / "review" and not output.exists(),
            "Use a new direct review output directory")
    target = TOOLS / "record_b134_publication.py"
    require(not target.exists(), "Preserve the existing recorder")
    guard, _ = start_guard("B134 publication-recorder preparation")
    try:
        git = Git(REPO, RUNNER, guard)
        require(git("rev-parse", "HEAD").decode().strip() == REVIEWED
                and not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Reviewed worktree differs")
        lineage(git, REVIEWED)
        source = frozen(TOOLS / SOURCE, SOURCE_SHA)
        result = derive(source)
        binding = write_frozen(target, result)
        require(not git("status", "--porcelain=v1", "--untracked-files=all"),
                "Preparation changed teaching worktree")
    finally:
        memory = guard.finish()
        require(not memory["breach"], "Recorder preparation RAM breach")
    print(json.dumps(freeze_json(output / "preparation.json", {
        "status": "PREPARED_NOT_EXECUTED", "base": BASE, "reviewedSnapshot": REVIEWED,
        "source": {"path": str(TOOLS / SOURCE), "sha256": SOURCE_SHA},
        "recorder": binding, "producerSha256": sha(Path(__file__).read_bytes()), "memory": memory,
        "changes": [
            "B134 signed identity, paths and unchanged host-gate order.",
            "B134 fresh-review history and uncredited 271/957 baseline ledger.",
            "Recheck the archive-bound resolution against all actual original review obligations.",
        ],
        "limits": "No closure, gate, CI, ZIP, teaching or publication acceptance. No remote writes.",
    })))


if __name__ == "__main__":
    import sys
    require(len(sys.argv) == 2, "prepare_b134_publication_recorder.py NEW_OUTPUT_DIRECTORY")
    main(Path(sys.argv[1]).resolve())
