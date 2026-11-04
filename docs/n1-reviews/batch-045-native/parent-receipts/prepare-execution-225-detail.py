import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops

control = Path(__file__).resolve().parent
source = control / "artifacts" / "batch-045-parent-native-attempt-1" / "n1-045-font-pairs.png"
target = control / "artifacts" / "batch-045-visual-detail.png"
original = Image.open(source)
expected = original.crop((40, 200, 330, 325)).resize((1160, 500), Image.Resampling.NEAREST)
assert ImageChops.difference(expected.convert("RGB"), Image.open(target).convert("RGB")).getbbox() is None
record = {
    "source": str(source), "sourceSha256": hashlib.sha256(source.read_bytes()).hexdigest(),
    "sourceDimensions": list(original.size), "target": str(target),
    "targetSha256": hashlib.sha256(target.read_bytes()).hexdigest(),
    "crop": [40, 200, 330, 325], "resize": [1160, 500],
    "resample": "NEAREST", "derivationPixelEqualityVerified": True,
    "scope": "Source-pixel enlargement only; no redrawn glyphs, phone or normal-size interaction claim.",
}
path = control / "batch-045-visual-detail-derivation.json"
assert not path.exists()
path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
launcher = (control / "run-batch-045-visual.ps1").read_text(encoding="utf-8")
launcher = launcher.replace("batch-045-visual-claude", "batch-045-visual-detail-claude")
launcher = launcher.replace("batch-045-visual-prompt.txt", "batch-045-visual-detail-prompt.txt")
path = control / "run-batch-045-visual-detail.ps1"
assert not path.exists()
path.write_text(launcher, encoding="utf-8")
print("Verified exact source-pixel derivation; prepared sole-original-reviewer narrow followup.")
