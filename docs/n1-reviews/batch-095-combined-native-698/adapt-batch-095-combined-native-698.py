"""Adapt committed, inspected child wrappers without changing their safety checks."""
import importlib.util
from pathlib import Path

C = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("prepare698", C / "prepare-batch-095-combined-native-698.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
R = m.R


def replace(text, old, new, count=1):
    assert text.count(old) == count, (old, text.count(old))
    return text.replace(old, new)


compile_prior = R / "docs" / "n1-reviews" / "batch-095-native" / "preparation-receipts" / "run-693-native-compile.ps1"
text = compile_prior.read_text(encoding="utf-8-sig")
for old, new, count in [
    ("49dac17d-7012-48cb-b241-ce67cb94bf4e", m.L.name, 1),
    ("preflight-693", "preflight-698", 2),
    ("$p.checkpoint -ne 692", "$p.checkpoint -ne 697", 1),
    ("batch-095-native-preparation-in-progress", "batch-095-combined-native-import-in-progress", 1),
    ("batch-095-native-fixture-verification.json", "batch-095-combined-native-698-verification.json", 1),
    ("N1Batch095NativeTest.kt", m.FIXTURE.name, 1),
    ("n1-batch-095-native-test.apk", "n1-batch-095-combined-698-test.apk", 1),
    ("n1-batch-095-native-app.apk", "n1-batch-095-combined-698-app.apk", 1),
]:
    text = replace(text, old, new, count)
target = C / "run-698-native-compile.ps1"
if target.exists():
    assert target.read_text(encoding="utf-8") == text
else:
    target.write_text(text, encoding="utf-8")

native_prior = R / "docs" / "n1-reviews" / "batch-095-native" / "execution-694" / "receipts" / "run-694-native.ps1"
text = native_prior.read_text(encoding="utf-8-sig")
for old, new, count in [
    ("6538b1ef-d7d4-465b-bd47-d66aa8a6ea9f", m.L.name, 1),
    ("694", "698", 5),
    ('"$content\\docs\\n1-sources\\execution-693.json"', '"$control\\batch-095-combined-native-698-compiled.json"', 1),
    ("95be0577bea120a757bccd190625499b01e94a63", m.HEAD, 1),
    ("$checkpoint.checkpoint -ne 693", "$checkpoint.checkpoint -ne 697", 1),
    ("batch-095-native-execution-in-progress", "batch-095-combined-native-import-in-progress", 1),
    ("io.github.stopcran.kanji.ui.N1Batch095GlyphTest,io.github.stopcran.kanji.ui.N1Batch095ArticleTest",
     "io.github.stopcran.kanji.ui.N1Batch095CombinedImport698Test", 1),
    ("$result.terminalSuccessCases -eq 2", "$result.terminalSuccessCases -eq 1", 1),
    (r"OK \(2 tests\)", r"OK \(1 test\)", 1),
]:
    text = replace(text, old, new, count)
text = replace(text, "'^n1-095-[\\p{L}\\p{N}-]+\\.(png|json|txt)$'", "'^n1-095-combined-import-698\\.json$'")
assert "File]::Open" not in text and "runner.lock" not in text
target = C / "run-698-native.ps1"
assert not target.exists()
target.write_text(text, encoding="utf-8")
print("Adapted inspected child wrappers; checkpoint, signed heads, wholly-clean trees, frozen hashes and parent ancestry retained.")
