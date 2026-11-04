from pathlib import Path

control = Path(__file__).resolve().parent
source = (control / "audit-batch-044-draft.py").read_text(encoding="utf-8")
before = 'source = raw.decode("utf-8")'
assert before in source
source = source.replace(before, 'source = raw.decode("utf-8").replace("save(folder /", "save(control /")')
for before, after in (
    ('execution": 211', 'execution": 216'),
    ("execution=211", "execution=216"),
    ("execution-211-", "execution-216-"),
    ('assert not result["exactWordChoiceLabels"]', 'assert len(result["exactWordChoiceLabels"]) == 1'),
    ('scope["save"](scope["folder"] / "batch-044-draft-audit.json", result)',
     'scope["save"](control / "execution-216-source-audit.json", result)'),
):
    assert before in source, before
    source = source.replace(before, after)
exec(compile(source, str(__file__), "exec"))
