from pathlib import Path

source = Path(__file__).with_name("archive-batch-050-visual.py")
text = source.read_text(encoding="utf-8").replace("batch-050-", "batch-054-")
text = text.replace("== 12", "== 18").replace('"imagePayloadsVerified": 12', '"imagePayloadsVerified": 18')
text = text.replace("12 actual resized PNG", "18 actual resized PNG")
exec(compile(text, str(source), "exec"))
