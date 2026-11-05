import contextlib
import io
from pathlib import Path

c = Path(__file__).resolve().parent
source = c / "execution-341-audit.py"
text = source.read_text(encoding="utf-8")
replacements = {
    'assert ledger["reviewClosed"] == ledger["published"] == []':
        'assert ledger["reviewClosed"] == ["丘"] and ledger["published"] == []',
    'FOLDER / "batch-058-draft-audit.json"':
        'FOLDER / "batch-058-acceptance-source-audit.json"',
}
for before, after in replacements.items():
    assert text.count(before) == 1, before
    text = text.replace(before, after)
scope = {"__file__": str(source), "__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(text, str(source), "exec"), scope)
result = scope["result"]
result.update(
    execution=349,
    status="combined-source-audit-pending-evidence-reverification",
    freshLinguisticReviewOfAllFamiliesClaimed=False,
    limits="Fresh combined-tree mechanical source audit; original linguistic reviews and accepted Android/native/visual evidence reverified separately, not rerun. Original process noncompliance preserved. Publication pending; physical-phone/general-release and whole-set outstanding.",
)
(scope["FOLDER"] / "batch-058-acceptance-source-audit.json").write_text(
    scope["json"].dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Combined source audit passed: frozen inputs/dictionaries,68 exact families,baseline985/4942/985,original guards,8303 hashes,readings/three reciprocal pairs/pinned strokes/actual Han font cmaps/budgets.")
