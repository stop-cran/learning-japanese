"""Derive explicit initial-selection support while preserving the existing closure gates."""
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen

HERE = Path(__file__).resolve().parent


def derive():
    source = HERE / "close.py"
    original = frozen(source)
    newline = "\r\n" if b"\r\n" in original else "\n"
    text = original.decode("utf-8").replace("\r\n", "\n")
    edits = [
        ("from confirm_v3 import run_number\n",
         "from confirm_v3 import run_number\nfrom closure_initials import archive_excluded\n"),
        ("def archive(batch, candidate, final_runs, intermediate_runs=()):",
         "def archive(batch, candidate, final_runs, intermediate_runs=(), *, preflight_path,\n"
         "            excluded_initials=(), confirmation_protocol=()):"),
        ('originals = read(records / "prompts" / "preflight.json")["runs"]',
         'originals = read(preflight_path)["runs"]\n'
         '    require(set(originals) == {"claude", "gpt"}, "Exactly two initial families required")'),
        ('        for path in sorted((records / "confirm").glob("*-superseded.json")):',
         '        excluded = archive_excluded(excluded_initials, batch, config["candidate"],\n'
         '                                    {item["run"] for item in lineage}, copy, binding, dump,\n'
         '                                    chain, audit_support, records)\n'
         '        copy(preflight_path, "protocol/selected-initial-preflight.json")\n'
         '        for path in sorted((records / "confirm").glob("*-superseded.json")):'),
        ('                     "tooling-preflight.json", "tooling-tests.txt",\n'
         '                     "tooling-v2-derivation.json", "tooling-v2.patch", "tooling-v2-tests.txt"):',
         '                     "tooling-preflight.json", "tooling-tests.txt", *confirmation_protocol):'),
        ('                     "confirm_v3.py", "test_confirm_v3.py", "close.py", "test_close.py"):',
         '                     "confirm_v3.py", "test_confirm_v3.py", "close.py", "test_close.py",\n'
         '                     "close_selected.py", "closure_initials.py", "test_closure_initials.py",\n'
         '                     "derive_close_selected.py", "close-selected-derivation.json"):'),
        ('            "reviewLineage": lineage,',
         '            "reviewLineage": lineage, "excludedInitialRuns": excluded,'),
        ('    batch, candidate, *runs = sys.argv[1:]\n'
         '    finals = [run for run in runs if not run.startswith("+")]\n'
         '    archive(int(batch), candidate, finals, tuple(run[1:] for run in runs if run.startswith("+")))',
         '    spec = read(Path(sys.argv[1]))\n'
         '    archive(spec["batch"], spec["candidate"], spec["finalRuns"],\n'
         '            tuple(spec.get("intermediateRuns", [])), preflight_path=Path(spec["preflight"]),\n'
         '            excluded_initials=tuple(Path(p) for p in spec.get("excludedInitials", [])),\n'
         '            confirmation_protocol=tuple(spec.get("confirmationProtocol", [])))'),
    ]
    for before, after in edits:
        require(text.count(before) == 1, f"Closure derivation anchor changed: {before!r}")
        text = text.replace(before, after)
    reverse = text
    for before, after in reversed(edits):
        require(reverse.count(after) == 1, "Closure reverse anchor changed")
        reverse = reverse.replace(after, before)
    require(reverse.replace("\n", newline).encode("utf-8") == original,
            "Closure reverse delta is not exact")
    compile(text, "close_selected.py", "exec")
    output = write_frozen(HERE / "close_selected.py", text.replace("\n", newline).encode("utf-8"))
    print(freeze_json(HERE / "close-selected-derivation.json", {
        "source": {"path": str(source), "sha256": sha(original)}, "output": output,
        "reverseExact": True, "replacements": len(edits),
        "scope": "Explicit initial preflight, preserved excluded structure-hold evidence, "
                 "and explicit optional follow-up protocol artifacts. Acceptance gates unchanged.",
    }))


if __name__ == "__main__":
    derive()
