from pathlib import Path

source = Path(__file__).with_name("archive-batch-050-visual.py")
text = source.read_text(encoding="utf-8").replace("batch-050-", "batch-053-")
text = text.replace("== 12", "== 21").replace('"imagePayloadsVerified": 12', '"imagePayloadsVerified": 21')
text = text.replace("12 actual resized PNG", "21 actual resized PNG")
exec(compile(text, str(source), "exec"))
