"""Derive an explicit evidence-only follow-up without changing the frozen renderer."""
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen

SOURCE = TOOLS / "confirm_followup.py"
SOURCE_SHA = "c08acedfd7322ddd9b16bf3a4b4314085bebcf664c8513ab71fc348e4c389c15"
OUTPUT = TOOLS / "confirm_followup_evidence_v1.py"
HELPER = '''
def selected_revision_diff(config, candidate, spec):
    evidence_only = spec.get("evidenceOnly", False)
    require(type(evidence_only) is bool, "evidenceOnly must be an explicit boolean")
    if not evidence_only:
        return revision_diff(config, candidate)
    names = [p for p in git(config, "diff", "--name-only", "--no-renames", "-z",
                           config["candidate"], candidate).decode("utf-8").split("\\0") if p]
    require(names and all(p.startswith("docs/") for p in names),
            "Evidence-only follow-up requires a nonempty documentation-only delta")
    runtime = git(config, "diff", "--no-color", config["candidate"], candidate,
                  "--", ".", ":(exclude)docs")
    require(not runtime, "Evidence-only follow-up changed runtime or manifest bytes")
    note = (
        "# Evidence-only revision; no runtime patch\\n"
        f"Prior candidate: {config['candidate']}\\n"
        f"Current candidate: {candidate}\\n"
        "The complete Git delta contains only contributor documentation. All runtime "
        "and manifest bytes are unchanged. Selected neutral evidence and the current "
        "family's response are supplied separately; other-family responses are not "
        "included. This is a delta observation, not confirmation or publication "
        "acceptance.\\n"
    ).encode("utf-8")
    return note, names

'''


def derive(raw):
    text = raw.decode("utf-8")
    changes = [
        ('RUN = r"N1-B{batch}-[A-Z0-9-]+-CONFIRM-(\\d{{3}})"',
         HELPER + 'RUN = r"N1-B{batch}-[A-Z0-9-]+-CONFIRM-(\\d{{3}})"'),
        ('delta, omitted = revision_diff(dict(config, candidate=prior["candidate"]), spec["candidate"])',
         'delta, omitted = selected_revision_diff(dict(config, candidate=prior["candidate"]), '
         'spec["candidate"], spec)'),
        ('    prompt = prompt_text.encode("utf-8")',
         '    if spec.get("evidenceOnly", False):\n'
         '        prompt_text += ("\\nEVIDENCE-ONLY FOLLOW-UP\\n"\n'
         '                        "The supplied fix.patch is an explicit no-runtime-change note, "\n'
         '                        "not a fabricated patch. Git verified a nonempty documentation-only "\n'
         '                        "successor with byte-identical runtime and manifest. Evaluate the "\n'
         '                        "new source/scope disposition; unchanged teaching does not by itself "\n'
         '                        "resolve a held source claim. Preserve the exact prior verdict and "\n'
         '                        "all limits, and assess the current snapshot independently.\\n")\n'
         '    prompt = prompt_text.encode("utf-8")'),
        ('              "diffScope": "Delta from the prior confirmation\'s candidate, excluding generated manifest and "\n'
         '                           "contributor docs. Responses and neutral evidence are explicitly selected in the spec.",',
         '              "evidenceOnly": spec.get("evidenceOnly", False),\n'
         '              "diffScope": ("Verified documentation-only delta; runtime and manifest unchanged. "\n'
         '                            "Neutral evidence and own-family response selected explicitly."\n'
         '                            if spec.get("evidenceOnly", False) else\n'
         '                            "Delta from the prior confirmation\'s candidate, excluding generated manifest and "\n'
         '                            "contributor docs. Responses and neutral evidence are explicitly selected in the spec."),'),
    ]
    newline = "\r\n" if b"\r\n" in raw else "\n"
    changes = [(old.replace("\n", newline), new.replace("\n", newline)) for old, new in changes]
    for old, new in changes:
        require(text.count(old) == 1, "Frozen follow-up derivation anchor changed")
        text = text.replace(old, new)
    reverse = text
    for old, new in reversed(changes):
        require(reverse.count(new) == 1, "Ambiguous reverse derivation")
        reverse = reverse.replace(new, old)
    require(reverse.encode("utf-8") == raw, "Derivation changed unrelated source")
    compile(text, str(OUTPUT), "exec")
    return text.encode("utf-8")


def main():
    original = frozen(SOURCE, SOURCE_SHA)
    derived = derive(original)
    output = write_frozen(OUTPUT, derived)
    print(freeze_json(TOOLS / "b125-evidence-followup-derivation.json", {
        "source": {"path": str(SOURCE), "sha256": sha(original)},
        "output": output,
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "reverseExact": True,
        "scope": "Opt-in documentation-only successor; all prior lineage, isolation, "
                 "signed clean snapshot, context, audit and substantive acceptance gates unchanged.",
        "packetsPrepared": False,
    }))


if __name__ == "__main__":
    main()
