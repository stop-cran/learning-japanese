"""Generate narrow immutable follow-up/closure derivatives; existing gates stay unchanged."""
import ast
import json
import subprocess
import sys
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "scratch-117" / "review" / "confirm"


def derive(source, destination, edits):
    original = frozen(ROOT / source)
    text = original.decode("utf-8")
    newline = "\r\n" if "\r\n" in text else "\n"
    applied = []
    for old, new in edits:
        if old not in text:
            old = old.replace("\n", newline)
        new = new.replace("\n", newline)
        require(text.count(old) == 1, f"Unexpected derivation anchor in {source}: {old}")
        text = text.replace(old, new, 1)
        applied.append((old, new))
    compile(text, destination, "exec")
    reversed_text = text
    for old, new in reversed(applied):
        require(reversed_text.count(new) == 1, f"Ambiguous reverse delta in {source}")
        reversed_text = reversed_text.replace(new, old, 1)
    require(reversed_text.encode("utf-8") == original, "Derivation cannot be exactly reversed")
    return {"source": {"path": str(ROOT / source), "sha256": sha(original)},
            "output": write_frozen(ROOT / destination, text.encode("utf-8")),
            "reverseExact": True, "edits": [{"before": a, "after": b} for a, b in applied]}


derivations = [
    derive("confirm_v3.py", "confirm_v4.py", [
        ('from confirm_v2 import admit, binding, clean, final, revision_diff',
         'from confirm_v2 import admit, binding, clean, final, revision_diff\n'
         'from replacement_lineage import require_followup_identity'),
        ('    require(launch["session"] == spec["session"], "Follow-up changes the original reviewer")',
         '    require_followup_identity(spec, initial, launch, records)'),
        ('    bindings = [binding(spec_path), spec["acceptance"], spec["prior"], prior["report"], initial["report"]]',
         '    bindings = [binding(spec_path), spec["acceptance"], spec["prior"], prior["report"], initial["report"]]\n'
         '    if "reviewerOrigin" in spec:\n'
         '        bindings.append(spec["reviewerOrigin"])\n'
         '    bindings.append(binding(Path(__file__).with_name("replacement_lineage.py")))'),
        ('    prompt = renderer.render_prompt(renderer_spec, packet_info, chain, prompt_path).encode("utf-8")',
         '    prompt_text = renderer.render_prompt(renderer_spec, packet_info, chain, prompt_path)\n'
         '    if "reviewerOrigin" in spec:\n'
         '        prompt_text += ("\\nCONTINUING REPLACEMENT IDENTITY\\n"\n'
         '                        "You are continuing your own prior replacement confirmation. The original "\n'
         '                        "initial report was written by another reviewer of the same family; do not "\n'
         '                        "claim firsthand authorship of it or retained context from that session. "\n'
         '                        "Your own previous confirmation and its consequential open claims are the "\n'
         '                        "basis for this bounded follow-up. Preserve all prior limits.\\n")\n'
         '    prompt = prompt_text.encode("utf-8")'),
    ]),
    derive("close_v2.py", "close_v3.py", [
        ('from confirm_v3 import run_number',
         'from confirm_v3 import run_number\nfrom replacement_lineage import require_followup_identity'),
        ('def require_identity(spec, session, original, launch, held=None, context=None, prior=None):',
         'def require_identity(spec, session, original, launch, held=None, context=None, prior=None, records=None):'),
        ('    else:\n        require(spec["session"] == launch["session"], "Confirmation changed reviewer without provenance")',
         '    elif "reviewerOrigin" in spec:\n'
         '        require(records is not None, "Continuing replacement lacks archived records")\n'
         '        require_followup_identity(spec, original, launch, records)\n'
         '    else:\n        require(spec["session"] == launch["session"], "Confirmation changed reviewer without provenance")'),
        ('                require_identity(spec, mechanics["session"], original, launch)',
         '                require_identity(spec, mechanics["session"], original, launch, records=records)'),
        ('                     "closure-v2-derivation.json", "closure-v2-tests.txt"):',
         '                     "closure-v2-derivation.json", "closure-v2-tests.txt",\n'
         '                     "replacement-continuation-derivation.json", "replacement-continuation-tests.txt"):'),
        ('                     "confirm_replacement.py", "test_confirm_replacement.py", "close_v2.py", "test_close_v2.py"):',
         '                     "confirm_replacement.py", "test_confirm_replacement.py", "close_v2.py", "test_close_v2.py",\n'
         '                     "confirm_v4.py", "close_v3.py", "replacement_lineage.py",\n'
         '                     "test_replacement_lineage.py", "derive_replacement_continuation.py"):'),
        ('                        "replacementFor": replacement_for, "finalAcceptance": kind == "final",',
         '                        "replacementFor": replacement_for,\n'
         '                        "reviewerOrigin": spec.get("reviewerOrigin") if confirmation else None,\n'
         '                        "finalAcceptance": kind == "final",'),
    ]),
]
for name in ("confirm_v4.py", "close_v3.py"):
    module = ast.parse(frozen(ROOT / name).decode("utf-8"))
    require(not any(isinstance(n, (ast.Global, ast.Nonlocal)) for n in ast.walk(module)),
            "Derivation added mutable module hooks")
done = subprocess.run([sys.executable, "-B", "-m", "unittest", "-q",
                       "test_replacement_lineage", "test_confirm_v3", "test_close_v2",
                       "test_confirm_replacement", "test_close"], cwd=ROOT, capture_output=True)
tests = write_frozen(OUT / "replacement-continuation-tests.txt", done.stdout + done.stderr)
require(done.returncode == 0, (done.stdout + done.stderr).decode("utf-8"))
print(json.dumps(freeze_json(OUT / "replacement-continuation-derivation.json", {
    "reason": "Continue a mechanically valid but substantively held fresh replacement with its own context; archive its intermediate and final identity without attributing it to the original reviewer.",
    "derivations": derivations, "tests": tests, "exitCode": done.returncode,
    "unchangedGates": ["confirm_v2.admit", "confirm_v2.final", "audit-confirm.py",
                       "check-confirm-structure.py", "check-run-context.py"],
    "helper": {"path": str(ROOT / "replacement_lineage.py"),
               "sha256": sha(frozen(ROOT / "replacement_lineage.py"))},
})))
