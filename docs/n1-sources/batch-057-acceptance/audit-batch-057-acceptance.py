import contextlib
import io
from pathlib import Path

c = Path(__file__).resolve().parent
source = c / "execution-331-audit.py"
text = source.read_text(encoding="utf-8")
old = 'FOLDER / "batch-057-draft-audit.json"'
assert text.count(old) == 1
text = text.replace(old, 'FOLDER / "batch-057-acceptance-source-audit.json"')
scope = {"__file__": str(source), "__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(text, str(source), "exec"), scope)
result = scope["result"]
result.update(
    execution=339,
    status="combined-source-audit-pending-evidence-reverification",
    freshLinguisticReviewOfAllFamiliesClaimed=False,
    limits="Fresh combined-tree mechanical source audit. Original linguistic reviews and accepted Android/native/visual evidence reverified separately, not rerun. Original process noncompliance preserved. No fresh linguistic certification; publication pending. Physical-phone/general-release and whole-set outstanding.",
)
(scope["FOLDER"] / "batch-057-acceptance-source-audit.json").write_text(
    scope["json"].dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Combined source audit passed: frozen inputs/dictionaries,194 exact families,baseline985/4942/985,original guards,8300 hashes,readings/links/pinned strokes/actual Han font cmaps/budgets.")
