import difflib
import hashlib
import json
import shutil
from pathlib import Path

C = Path(__file__).resolve().parent
R = C.parent / "learning-japanese"
folder = R / "docs/n1-reviews/batch-083-native-corrected"
old = R / "docs/n1-reviews/batch-083-native/N1Batch083NativeTest.kt"
new = folder / "N1Batch083CorrectedNativeTest.kt"
diff = folder / "fixture-from-original-083.diff"
verification = C / "batch-083-corrected-native-fixture-verification.json"
evidence = R / "docs/n1-sources/execution-577.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


v = load(verification)
assert sha(old) == v["priorHarnessSha256"]
assert sha(new) == v["fixtureSha256"]
assert sha(diff) == v["fixtureDiffSha256"]
diff.write_text("".join(difflib.unified_diff(
    old.read_text(encoding="utf-8").splitlines(keepends=True),
    new.read_text(encoding="utf-8").splitlines(keepends=True),
    fromfile=old.relative_to(R).as_posix(), tofile=new.relative_to(R).as_posix(), n=0)), encoding="utf-8")
v["fixtureDiffSha256"] = sha(diff)
v["fixtureDiffContext"] = 0
save(verification, v)
e = load(evidence)
e["fixtureVerification"] = v
for item in e["provenance"]:
    if item["source"] == str(verification):
        target = R / item["archive"]
        shutil.copyfile(verification, target)
        item["sha256"] = sha(target)
target = folder / "preparation-receipts" / Path(__file__).name
assert not target.exists()
shutil.copyfile(__file__, target)
e["provenance"].append({"source": str(Path(__file__)), "archive": target.relative_to(R).as_posix(),
                        "sha256": sha(target)})
e["diagnostics"].append(
    "Initial staged diff-check rejected unified-diff blank context lines as trailing whitespace before any signing call. "
    "Regenerated only the diagnostic fixture diff with zero context; valid delta and all assertions/source/APK/archive "
    "bytes unchanged, verification/provenance refreshed. No signing hang or build/test failure."
)
save(evidence, e)
print("Zero-context diagnostic diff regenerated; fixture/APKs/archive unchanged.")
