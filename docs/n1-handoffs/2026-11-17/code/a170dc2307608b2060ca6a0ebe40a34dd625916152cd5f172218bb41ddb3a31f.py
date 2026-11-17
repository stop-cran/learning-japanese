"""Correct the deferred-font binding before executing any packet builder."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, r"C:\Users\stop-\n1-kanji-workspace\review-tools")
from common import frozen, require, sha, write_frozen, freeze_json

source = HERE / "tools" / "packet-builder-b134-001.py"
raw = frozen(source)
before = '        require(sha(font_raw) == facts["strokeFontEvidenceSha256"], "Signed font evidence changed")'
after = ('        # Bytes come from the signed candidate; separate finite verification gates admission.\n'
         '        require(json.loads(font_raw)["members"][0]["character"] == MEMBERS[0],\n'
         '                "Signed bounded font scope differs")')
require(before in raw.decode(), "Missing correction anchor")
text = raw.decode().replace(before, after)
binding = write_frozen(HERE / "tools" / "packet-builder-b134-002.py", text.encode())
freeze_json(HERE / "packet-builder-correction-002.json", {
    "source": {"path": str(source), "sha256": sha(raw)}, "output": binding,
    "reason": "source-facts-002 has no font digest field; signed font blob remains exact, with actual finite proof required separately."})
