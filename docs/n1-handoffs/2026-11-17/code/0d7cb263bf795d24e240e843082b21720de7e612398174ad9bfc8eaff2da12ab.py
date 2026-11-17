"""Generate the report-placement successor, preserving original Windows file bytes."""
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, sha, write_frozen


def main():
    source = TOOLS / "close_b132_reconciled.py"
    destination = TOOLS / "close_b132_reconciled_v2.py"
    raw = frozen(source)
    text = raw.decode("utf-8").replace("\r\n", "\n")
    changes = [
        (
            "def main(mode, output):\n"
            "    require(mode in (\"dry\", \"real\") and not output.exists()\n"
            "            and not output.with_name(output.name + \"-report.json\").exists(), \"Preserve closure attempt\")",
            "def closure_report_path(mode, output):\n"
            "    return (HERE / \"reconciled-closure-real-report-001.json\" if mode == \"real\"\n"
            "            else output.with_name(output.name + \"-report.json\"))\n\n\n"
            "def main(mode, output):\n"
            "    report_path = closure_report_path(mode, output)\n"
            "    require(mode in (\"dry\", \"real\") and not output.exists()\n"
            "            and not report_path.exists(), \"Preserve closure attempt\")"
        ),
        (
            'for name in ("close_b132_reconciled.py", "b132_confirmation_records.py", "confirm_b132.py",',
            'for name in ("close_b132_reconciled.py", "close_b132_reconciled_v2.py",\n'
            '                     "b132_confirmation_records.py", "confirm_b132.py",'
        ),
        (
            'freeze_json(output.with_name(output.name + "-report.json"), report)',
            'freeze_json(report_path, report)'
        ),
    ]
    for index, (before, after) in enumerate(changes, 1):
        if text.count(before) != 1:
            raise ValueError(f"Expected unique preserved-builder replacement {index}")
        text = text.replace(before, after)
    result = write_frozen(destination, text.encode("utf-8"))
    print(freeze_json(WS / "scratch-132" / "review" / "reconciled-closure-successor-002.json", {
        "source": str(source), "sourceSha256": sha(raw), "result": result,
        "change": "Real execution report goes to scratch,not a sibling outside the permitted closure subtree. "
                  "Both original and actual successor builders are archived. All acceptance/retention checks unchanged. "
                  "Generated Python uses LF; original raw-byte source hash is retained.",
        "producer": str(Path(__file__)), "producerSha256": sha(frozen(Path(__file__))),
    }))


if __name__ == "__main__":
    main()
