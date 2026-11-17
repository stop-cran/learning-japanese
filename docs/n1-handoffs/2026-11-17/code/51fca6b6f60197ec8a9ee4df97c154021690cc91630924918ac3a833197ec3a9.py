"""Adapt the actual signed new-member pair rationale schema; preserve v2."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen

ROOT = Path(__file__).resolve().parent
HERE = ROOT.parent / "scratch-130" / "review"
derivation = json.loads(frozen(HERE / "evidence-v2-derivation.json",
                              "495819f20f139b021678f82223739faa134b19b0ffd6657b87f8d84cd7a7d9db"))
source = frozen(ROOT / "verify_b130_evidence_v2.py", derivation["output"]["sha256"])
old = b'and all(item["decision"] in DECISIONS and item["bothDirections"] is True for item in items),'
new = b'and all(item["decision"] in DECISIONS and isinstance(item["bothDirections"], str) and item["bothDirections"].strip() for item in items),'
require(source.count(old) == 1, "New-member pair schema anchor changed")
output = source.replace(old, new)
require(output.replace(new, old) == source, "Pair-schema derivation is not reversible")
compile(output, "verify_b130_evidence_v3.py", "exec")
result = write_frozen(ROOT / "verify_b130_evidence_v3.py", output)
print(freeze_json(HERE / "evidence-v3-derivation.json", {
    "source": derivation["output"], "output": result, "byteReversible": True,
    "change": "The signed new-member pairs carry a nonempty explanatory bothDirections string, not a boolean. "
              "Require that actual schema without interpreting the rationale as linguistic acceptance.",
    "producerSha256": sha(Path(__file__).read_bytes()),
}))
