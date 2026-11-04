from pathlib import Path

template = Path(__file__).with_name("audit-batch-053-draft.py")
source = template.read_text(encoding="utf-8")
for old, new in [
    ('"execution": 290', '"execution": 296'),
    ('"status": "local-unreviewed-draft"', '"status": "combined-source-audit-pending-evidence-reverification"'),
    ("batch-053-draft-audit.json", "batch-053-acceptance-source-audit.json"),
    ("Mechanical LOCAL UNREVIEWED draft audit only. Independent two-family review, reconciliation, Android/native/visual/current-main/publication gates pending.",
     "Fresh combined-tree mechanical source audit only; accepted textual/Android/native/visual evidence is reverified separately, not rerun. Publication pending."),
]:
    assert old in source
    source = source.replace(old, new)
exec(compile(source, str(__file__), "exec"))
