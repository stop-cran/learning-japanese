from pathlib import Path

template = Path(__file__).with_name("audit-batch-055-draft.py")
source = template.read_text(encoding="utf-8")
for old, new in [
    ('"execution": 308', '"execution": 315'),
    ('"status": "local-unreviewed-runtime-draft"',
     '"status": "combined-source-audit-pending-evidence-reverification"'),
    ('batch-055-draft-audit.json', 'batch-055-acceptance-source-audit.json'),
    ('"freshLinguisticReviewOfAllFamiliesClaimed": True',
     '"freshLinguisticReviewOfAllFamiliesClaimed": False'),
    ("Mechanical LOCAL UNREVIEWED draft audit with separate coordinator source inspections, not independent linguistic certification. Two-family review, reconciliation, fresh Android/native/visual/current-main/publication gates pending. No phone/general-release/whole-set acceptance.",
     "Fresh combined-tree mechanical source audit. Original linguistic reviews and accepted Android/native/visual evidence reverified separately, not rerun. No fresh linguistic certification. Publication pending; no phone/general-release/whole-set acceptance."),
]:
    assert old in source, old
    source = source.replace(old, new)
exec(compile(source, str(__file__), "exec"))
