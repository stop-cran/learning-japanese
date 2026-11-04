from pathlib import Path

control = Path(__file__).resolve().parent
source = (control / "audit-batch-043-draft.py").read_text(encoding="utf-8")
before = 'source = raw.decode("utf-8")'
assert before in source
source = source.replace(before, 'source = raw.decode("utf-8").replace("save(folder /", "save(control /")')
for before, after in (
    ('execution": 202', 'execution": 207'),
    ("execution=202", "execution=207"),
    ("execution-202-", "execution-207-"),
):
    source = source.replace(before, after)
before = 'scope["save"](scope["folder"] / "batch-043-draft-audit.json", result)'
assert before in source
source = source.replace(before, 'scope["save"](control / "execution-207-source-audit.json", result)')
exec(compile(source, str(__file__), "exec"))
