import gzip
import hashlib
import json
import shutil
from pathlib import Path

CONTROL = Path(__file__).resolve().parent
ROOT = CONTROL.parent / "learning-japanese"
folder = ROOT / "docs" / "n1-reviews" / "batch-078-native"
prior = folder / "preparation-attempt-1"
assert not prior.exists()
fixture = folder / "N1Batch078NativeTest.kt"
assert hashlib.sha256(fixture.read_bytes()).hexdigest() == "060f1a8fca3ea32507058e47080034c6a8bfad446545ef981822831c728e1c7a"
items = list(folder.iterdir())
prior.mkdir()
for source in items:
    shutil.move(str(source), str(prior / source.name))
source_record = ROOT / "docs" / "n1-sources" / "execution-525.json"
shutil.copyfile(source_record, prior / "execution-525-initial-record.json")
shutil.copyfile(CONTROL / "batch-078-native-fixture-verification.json",
                prior / "fixture-verification.json")
raw = prior / "compile.txt"
(prior / "compile-raw.txt.gz").write_bytes(gzip.compress(raw.read_bytes(), mtime=0))
assert gzip.decompress((prior / "compile-raw.txt.gz").read_bytes()) == raw.read_bytes()
raw.write_text("\n".join(line.rstrip() for line in raw.read_text().splitlines()) + "\n", encoding="utf-8")
apk = CONTROL / "artifacts" / "n1-batch-078-native-test.apk"
target = CONTROL / "artifacts" / "n1-batch-078-native-test-attempt-1.apk"
assert not target.exists()
assert hashlib.sha256(apk.read_bytes()).hexdigest() == "4dc6f6cc18f1cfc5b3f118c2b987674635ebe6b4398d2ace8f4027b5391f6848"
apk.rename(target)
print("Initial successful but unexecuted compilation preserved; production Markdown nested-list projection correction required.")
