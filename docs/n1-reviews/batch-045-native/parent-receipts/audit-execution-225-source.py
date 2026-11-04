from pathlib import Path

control = Path(__file__).resolve().parent
source = (control / "audit-batch-045-draft.py").read_text(encoding="utf-8")
for before, after in (
    ('execution": 220', 'execution": 225'),
    ("execution=220", "execution=225"),
    ("execution-220-", "execution-225-"),
    ('source = raw.decode("utf-8")', 'source = raw.decode("utf-8").replace("save(folder /", "save(control /")'),
    ('scope["save"](scope["folder"] / "batch-045-draft-audit.json", result)',
     'scope["save"](control / "execution-225-source-audit.json", result)'),
):
    assert before in source, before
    source = source.replace(before, after)
exec(compile(source, str(__file__), "exec"))
