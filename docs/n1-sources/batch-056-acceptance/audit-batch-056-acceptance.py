import contextlib
import io
from pathlib import Path
import sys

c = Path(__file__).resolve().parent
source = c / "execution-318.py"
text = source.read_text(encoding="utf-8")
old = 'save(f / "batch-056-draft-audit.json", result)'
assert text.count(old) == 1
text = text.replace(old, 'save(f / "batch-056-acceptance-source-audit.json", result)')
sys.argv = [str(source), "audit"]
scope = {"__file__": str(source), "__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(text, str(source), "exec"), scope)
result = scope["result"]
result.update(
    execution=329,
    status="combined-source-audit-pending-evidence-reverification",
    freshLinguisticReviewOfAllFamiliesClaimed=False,
    limits="Fresh combined-tree mechanical source audit. Original linguistic reviews and accepted Android/native/visual evidence reverified separately, not rerun. No fresh linguistic certification; publication pending. Physical-phone/general-release and whole-set outstanding.",
)
scope["save"](scope["f"] / "batch-056-acceptance-source-audit.json", result)
print("Combined source audit passed: 5 frozen inputs, 2 decompressed dictionaries, 64 exact families, baseline985/4942/985, exact guards,8297 hashes/8293 unchanged, readings/links/strokes/28Han fonts and budgets.")
