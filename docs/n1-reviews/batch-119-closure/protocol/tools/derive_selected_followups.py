"""Preserve accepted prior snapshots in the selected-initial review pipeline."""
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent


def derive_file(source_name, output_name, edits):
    source = HERE / source_name
    original = frozen(source)
    newline = "\r\n" if b"\r\n" in original else "\n"
    text = original.decode("utf-8").replace("\r\n", "\n")
    for before, after in edits:
        require(text.count(before) == 1, f"Changed derivation anchor: {before!r}")
        text = text.replace(before, after)
    reverse = text
    for before, after in reversed(edits):
        require(reverse.count(after) == 1, f"Changed reverse anchor: {after!r}")
        reverse = reverse.replace(after, before)
    require(reverse.replace("\n", newline).encode("utf-8") == original, "Nonreversible derivation")
    compile(text, output_name, "exec")
    return {
        "source": {"path": str(source), "sha256": sha(original)},
        "output": write_frozen(HERE / output_name, text.replace("\n", newline).encode("utf-8")),
        "reverseExact": True, "replacements": len(edits),
    }


def derive():
    confirmations = derive_file("confirm_v5.py", "confirm_followup.py", [
        ('old = "accepted B117 adjudicated previous confirmation"',
         'old = f"accepted B{spec[\'batch\']} adjudicated previous confirmation"'),
        ('text = text.replace(old, "accepted B117 previous confirmation")',
         'text = text.replace(old, f"accepted B{spec[\'batch\']} previous confirmation")'),
    ])
    closure = derive_file("close_selected.py", "close_selected_v2.py", [
        ("from closure_initials import archive_excluded\n",
         "from closure_initials import archive_excluded\n"
         "from close_v4 import require_historical_confirmation\n"),
        ('        require_intermediate(accepted, candidate)\n'
         '        require(accepted["family"] in ("claude", "gpt"), "Unknown intermediate family")',
         '        require_historical_confirmation(accepted, candidate)\n'
         '        require(accepted["family"] in ("claude", "gpt"), "Unknown intermediate family")'),
        ('        elif kind == "intermediate":\n'
         '            require_intermediate(accepted, candidate)',
         '        elif kind == "intermediate":\n'
         '            require_historical_confirmation(accepted, candidate)'),
        ('                        "finalAcceptance": kind == "final", "report": report, "chains": chains,',
         '                        "confirmationAcceptedOnSnapshot": accepted.get("confirmationAccepted", False),\n'
         '                        "finalAcceptance": kind == "final", "report": report, "chains": chains,'),
        ('                     "derive_close_selected.py", "close-selected-derivation.json"):',
         '                     "derive_close_selected.py", "close-selected-derivation.json",\n'
         '                     "confirm_v5.py", "confirm_followup.py", "replacement_lineage.py",\n'
         '                     "confirm_replacement.py", "close_v4.py", "close_selected_v2.py",\n'
         '                     "derive_selected_followups.py", "selected-followups-derivation.json",\n'
         '                     "test_selected_followups.py"):'),
        ('                            "confirmations are preserved with their raw verdicts and are not final acceptances.",',
         '                            "confirmations retain their raw verdicts and snapshot-specific acceptance; "\n'
         '                            "neither accepted nor unaccepted earlier snapshots are final acceptance of this revision.",'),
    ])
    tests = derive_file("test_accepted_followup.py", "test_selected_followups.py", [
        ("from close_v4 import require_historical_confirmation",
         "from close_selected_v2 import require_historical_confirmation"),
        ("from confirm_v5 import render_followup_prompt, require_prior_state",
         "from confirm_followup import render_followup_prompt, require_prior_state"),
        ('self.spec = {"basis": "accepted-confirmation", "priorVerdict": "CONFIRMED", "openClaimIds": []}',
         'self.spec = {"batch": 118, "basis": "accepted-confirmation", "priorVerdict": "CONFIRMED", "openClaimIds": []}'),
        ('return "Perform ONE read-only confirmation of your own accepted B117 adjudicated previous confirmation."',
         'return f"Perform ONE read-only confirmation of your own accepted B{spec[\'batch\']} adjudicated previous confirmation."'),
        ('self.assertIn("accepted B117 previous confirmation", text)',
         'self.assertIn("accepted B118 previous confirmation", text)\n'
         '        second = render_followup_prompt(SimpleNamespace(render_prompt=render),\n'
         '                                        {**self.spec, "batch": 119}, {}, {}, None)\n'
         '        self.assertIn("accepted B119 previous confirmation", second)'),
    ])
    print(freeze_json(HERE / "selected-followups-derivation.json", {
        "derivations": [confirmations, closure, tests],
        "tool": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "scope": "Batch-aware accepted-confirmation prompt anchor; unchanged historical-acceptance "
                 "gate reused from close_v4 with explicit selected initial runs and preserved "
                 "excluded initial evidence. Snapshot-specific acceptance is recorded separately "
                 "from final acceptance. Original files remain byte-exact.",
    }))


if __name__ == "__main__":
    derive()
