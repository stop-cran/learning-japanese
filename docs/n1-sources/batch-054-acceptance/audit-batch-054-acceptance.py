from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parent.parent / "learning-japanese"
sys.path.insert(0, str(root / "tools"))
import audit_n1_batch

main = "dfd87ba949dc41493c800411675c44d782482c46"
main_changes = {f"kanji/{c}.md" for c in "九四回度"}
original_delta = audit_n1_batch.runtime_delta


def integrated_delta(before, after, additions, changed):
    assert not changed & main_changes
    for name in main_changes:
        expected = subprocess.check_output(["git", "show", f"{main}:{name}"], cwd=root)
        assert (root / name).read_bytes() == expected, name
    original_delta(before, after, additions, changed | main_changes)


audit_n1_batch.runtime_delta = integrated_delta

template = Path(__file__).with_name("audit-batch-054-draft.py")
source = template.read_text(encoding="utf-8")
for old, new in [
    ('"execution": 299', '"execution": 305'),
    ('"status": "local-unreviewed-runtime-draft"', '"status": "combined-source-audit-pending-evidence-reverification"'),
    ("batch-054-draft-audit.json", "batch-054-acceptance-source-audit.json"),
    ('assert manifest[section][name] == expected, name',
     'assert manifest[section][name] == (json.loads(committed(main, "manifest.json"))[section][name] if name in main_changes else expected), name'),
    ("Mechanical LOCAL UNREVIEWED draft audit. Two-family review, reconciliation, fresh Android/native/visual/current-main/publication gates pending. No phone/general-release/whole-set acceptance.",
     "Fresh combined-tree mechanical source audit only. Accepted textual/Android/native/visual evidence reverified separately, not rerun. Publication pending; no phone/general-release/whole-set acceptance."),
]:
    assert old in source
    source = source.replace(old, new)
source = source.replace('"changedReusedRuntimePayloads": [],',
                        '"changedReusedRuntimePayloads": [], "upstreamOnlyRuntimeChanges": sorted(main_changes), "upstreamCommit": main,')
source = source.replace('"baseRuntimePayloadHashesPreserved": preserved,',
                        '"baseRuntimePayloadsAccountedFor": preserved, "baseRuntimeHashesUnchanged": preserved - len(main_changes),')
source = source.replace('batch = audit(R, "054")',
                        'batch = audit(R, "054")\nbatch["upstreamOnlyRuntimeChanges"] = sorted(main_changes)\nbatch["preservationBoundary"] = "Exact base runtime preserved except recorded batch additions and four byte-identical upstream-only articles; no changed teaching conflict."')
exec(compile(source, str(__file__), "exec"))
