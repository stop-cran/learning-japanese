from pathlib import Path

source = Path(__file__).with_name("archive-batch-050-visual.py")
text = source.read_text(encoding="utf-8").replace("batch-050-", "batch-052-")
text = text.replace("== 12", "== 16").replace('"imagePayloadsVerified": 12', '"imagePayloadsVerified": 16')
text = text.replace("12 actual resized PNG", "16 actual resized PNG")
exec(compile(text, str(source), "exec"))
