import json
import re

from common import WS, frozen, require
from confirm_v2 import preflight

root = WS / "scratch-125" / "review" / "confirm"
results = []
for family, other in (("CLAUDE", "gpt"), ("GPT", "claude")):
    prepared, config = preflight(root / f"N1-B125-{family}-CONFIRM-002-preflight.json")
    chain = json.loads(frozen(config["chainManifest"]))
    for segment in chain["segments"]:
        raw = frozen(segment["path"], segment["sha256"])
        require(not re.search(rf"\b{other}\b", raw.decode("utf-8"), re.I),
                f"Other-family token in {family} segment {segment['index']}")
    results.append({"family": family, "segments": len(chain["segments"]), "crossFamilyToken": False})
print(json.dumps(results))
