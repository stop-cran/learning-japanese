"""Specialize the preserved B133 closure builder for the actual three-revision history."""
from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen
from derive_b133_closure_recorders_v2 import replace

HISTORY = '''
        for family, run, snapshot in (
            ("claude", "N1-B133-CLAUDE-CONFIRM-001", "110b4ffb6af078eb2adb00645db4c9e0bd6db188"),
            ("gpt", "N1-B133-GPT-CONFIRM-002", "d7d6cff92afe8220c16a5daa76f1c3f00a2bef30"),
        ):
            entry, retained, chain = confirmation_entry(files, family, run, snapshot)
            entries.append(entry)
            local.extend(retained)
            retention[run] = chain
        nonaccepted = []
        for run, name, digest in (
            ("N1-B133-GPT-CONFIRM-001", "gpt-confirm-001-adjudication-001.json",
             "987fb5f9a0a9f884ea229d11b0318bc36893cd3162e0567ae1bb09c21ec4efdc"),
            ("N1-B133-CLAUDE-CONFIRM-002", "claude-confirm-002-adjudication-001.json",
             "8bba057dd162f4e32c8fa6e0c9243692643dc312fd2e4d2d8548ae1fe2ccf326"),
        ):
            entry, retained, chain = unaccepted_entry(files, run, REVIEW / name, digest)
            nonaccepted.append(entry)
            local.extend(retained)
            retention[run] = chain
'''

FRESH = '''
    if "originalSession" in record:
        entry.update(
            reviewerOrigin="fresh-context-replacement", originalSession=record["originalSession"],
            replacementReason=record["replacementReason"],
        )
        ref = record["contextObservation"]
        entry["contextObservation"] = put(
            files, prefix + "origin-observation.json", frozen(ref["path"], ref["sha256"]))
        prior_prefix = "reviews/N1-B133-CLAUDE-CONFIRM-002/"
        entry["priorFinal"] = {"path": prior_prefix + "final.json",
                               "sha256": sha(files[prior_prefix + "final.json"])}
        name = prior_prefix + "adjudication-summary.json"
        entry["priorAdjudication"] = {
            "path": name, "sha256": sha(files[name]),
            "originalSha256": json.loads(files[name])["originalAdjudicationSha256"],
        }
'''


def main():
    original = frozen(TOOLS / "close_b133.py")
    # Bind the actual preserved adjudication, not an abbreviation transcribed from a checkpoint.
    history = HISTORY.replace(
        "987fb5f9a0a9f884ea229d11b0318bc36893cd3162e0567ae1bb09c21ec4efdc",
        sha(frozen(WS / "scratch-133" / "review" / "gpt-confirm-001-adjudication-001.json")))
    replacements = [
        ("from b133_closure_records import", "from b133_closure_records_v2 import"),
        ("from b133_confirmation_records import collect_confirmation",
         "from b133_confirmation_records import collect_confirmation\n"
         "from b133_fresh_confirmation_records_v2 import collect_confirmation as collect_fresh_confirmation\n"
         "from b133_closure_history import unaccepted_entry"),
        ("from record_b133_publication import", "from record_b133_publication_v2 import"),
        ('REVISION = "110b4ffb6af078eb2adb00645db4c9e0bd6db188"',
         'REVISION = "b1acf155fb8c7e1066a5c3baf88ae98ab92c29ac"'),
        ('"teaching-revision-verification-002"', '"teaching-revision-verification-004"'),
        ("0a95d56399cc78df0e7fd3fd9b2e0359267f5c4d564a1da39ab3079e00982d9c",
         "8a88b67f4e609885fd14b739442ae72ecad9476d2f19040c535c9f468ab6a90e"),
        ('    (SOURCE_ROOT / "readback", (".txt",)),',
         '    (SOURCE_ROOT / "readback", (".txt",)),\n'
         '    (HERE / "teaching-reconciliation-002" / "source-sections", (".txt",)),\n'
         '    (HERE / "teaching-reconciliation-003" / "source-sections", (".txt",)),\n'
         '    (REVIEW / "claude-confirm-002-adjudication-sources-001", (".txt", ".html")),'),
        ('"close_b133.py", "test_close_b133.py", "b133_closure_records.py", "b133_confirmation_records.py",',
         '"close_b133.py", "close_b133_v2.py", "test_b133_closure_v2.py",\n'
         '    "b133_closure_records.py", "b133_closure_records_v2.py", "b133_confirmation_records.py",\n'
         '    "b133_closure_history.py", "b133_closure_origins.py", "record_b133_publication_v2.py",\n'
         '    "b133_fresh_confirmation_records_v2.py", "b133_fresh_confirmation_v2.py",\n'
         '    "confirm_b133_fresh_v2.py", "accept_b133_fresh_confirmation_v2.py",'),
        ('"verify_b133_teaching_revision_v2.py", "archive_b129_chains.py", "common.py",',
         '"verify_b133_teaching_revision_v2.py", "verify_b133_teaching_revision_v3.py",\n'
         '    "verify_b133_teaching_revision_v4.py", "archive_b129_chains.py", "common.py",'),
        ('"Two independent same-snapshot initial textual reviews plus both original-reviewer delta "\n'
         '    "confirmations of the owner-signed reconciliation, not exhaustive linguistic certification.",',
         '"Two independent same-snapshot initial textual reviews, original GPT final confirmation and "\n'
         '    "disclosed same-family fresh-context Claude final confirmation. Original Claude context "\n'
         '    "could not fit the unchanged gate; its initial and first confirmation remain historical. "\n'
         '    "This is not equal fresh-read depth or exhaustive linguistic certification.",'),
        ('"disclosed retained distinction, not a nineteenth comparison.",',
         '"separately disclosed retained distinction, outside the nineteen direct pair decisions.",'),
        ('"Initial CLEAN and UNVERIFIED reports remain unchanged. Eleven qualified direct precautions and seven "\n'
         '    "retained distinctions resolve the original claims only in the owner-signed revised snapshot.",',
         '"All initial and intermediate reports remain unchanged, including both UNVERIFIED confirmations. "\n'
         '    "Thirteen qualified direct precautions, six retained distinctions and the corrected historical "\n'
         '    "sake-name abbreviation apply only to the final signed snapshot. Earlier waterfall-water "\n'
         '    "interpretations in GPT CONFIRM-002 and coordinator adjudications are withdrawn, not erased.",'),
        ('"滝 sound/terrain/water family: 声, 激 and 険 precautions added; 液 retained "\n'
         '                           "as a superordinate category already guarded by 水."',
         '"滝 sound/terrain/water family: 声, 激, 険 and 液 precautions added. The liquid "\n'
         '                           "precaution has direct flow/drink grounds, not a third-card argument; "\n'
         '                           "the erroneous historical abbreviation gloss was corrected."'),
        ('def confirmation_entry(files, family):\n'
         '    run = "N1-B133-" + family.upper() + "-CONFIRM-001"',
         'def confirmation_entry(files, family, run=None, candidate=REVISION):\n'
         '    run = run or "N1-B133-" + family.upper() + "-CONFIRM-003"'),
        ('require(record["candidate"] == REVISION and record["teachingChange"] is True, "Confirmation snapshot differs")',
         'require(record["candidate"] == candidate and record["teachingChange"] is True, "Confirmation snapshot differs")'),
        ('"family": family, "role": "confirmation", "run": run, "session": INITIALS[family]["session"],\n'
         '        "snapshot": REVISION, "confirmation": "CONFIRMED",',
         '"family": family, "role": "confirmation", "run": run, "session": record["session"],\n'
         '        "snapshot": candidate, "confirmation": "CONFIRMED",'),
        ('    refs, derivatives, _ = collect_confirmation(spec, initial_binding(family), frozen)',
         '    if "originalSession" in record:\n'
         '        spec.update(reviewerOrigin="fresh-context-replacement", originalSession=record["originalSession"])\n'
         '        refs, derivatives, _ = collect_fresh_confirmation(spec, initial_binding(family), frozen)\n'
         '    else:\n'
         '        refs, derivatives, _ = collect_confirmation(spec, initial_binding(family), frozen)'),
        ('    entry["reviewAccepted"] = True\n', '    entry["reviewAccepted"] = True\n' + FRESH),
        ('        for family in INITIALS:\n            entry, retained, chain = confirmation_entry(files, family)',
         history + '\n        for family in INITIALS:\n            entry, retained, chain = confirmation_entry(files, family)'),
        ('"reviewLineage": entries, "finalRuns": [entry["run"] for entry in entries[2:]],',
         '"reviewLineage": entries, "finalRuns": ["N1-B133-CLAUDE-CONFIRM-003", "N1-B133-GPT-CONFIRM-003"],\n'
         '            "intermediateRuns": ["N1-B133-CLAUDE-CONFIRM-001", "N1-B133-GPT-CONFIRM-002"],\n'
         '            "nonAcceptedReviews": nonaccepted,'),
        ('"closure-real-report-001.json"', '"closure-real-report-002.json"'),
    ]
    raw = original
    for old, new in replacements:
        raw = replace(raw, old, new)
    # These two plain-language occurrences have the same exact replacement.
    before = b"confirmed by both original reviewers"
    after = b"confirmed by the final original GPT and disclosed fresh Claude reviewers"
    count = raw.count(before)
    require(count == 2, "Unexpected final-review attribution count")
    raw = raw.replace(before, after)
    restored = raw.replace(after, before)
    for old, new in reversed(replacements):
        restored = replace(restored, new, old)
    require(restored == original, "Closure derivation not reversible")
    compile(raw, "close_b133_v2.py", "exec")
    result = write_frozen(TOOLS / "close_b133_v2.py", raw)
    print(freeze_json(WS / "scratch-133" / "review" / "closure-v2-derivation.json", {
        "originalSha256": sha(original), "successor": result,
        "scope": "Final reconciliation-003, all intermediate and held reviews, disclosed fresh Claude "
                 "origin, corrected thirteen/six accounting and expanded local-only source protection.",
    }))


if __name__ == "__main__":
    main()
