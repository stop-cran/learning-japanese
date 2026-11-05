import contextlib
import io
from pathlib import Path

c = Path(__file__).resolve().parent
source = c / "execution-351-audit.py"
text = source.read_text(encoding="utf-8")
for before, after in {
    'assert ledger["reviewClosed"] == ledger["published"] == []':
        'assert ledger["reviewClosed"] == ["享"] and ledger["published"] == []',
    'FOLDER / "batch-059-draft-audit.json"':
        'FOLDER / "batch-059-acceptance-source-audit.json"',
}.items():
    assert text.count(before) == 1, before
    text = text.replace(before, after)
scope = {"__file__": str(source), "__name__": "__main__"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(text, str(source), "exec"), scope)
result = scope["result"]
result.update(
    execution=359, status="combined-source-audit-pending-evidence-reverification",
    freshLinguisticReviewOfAllFamiliesClaimed=False,
    coordinatorInspection="Fresh combined-tree mechanical re-extraction of54frozen families; original linguistic inspection/reconciliation retained, not newly performed.",
    limits="Mechanical source, baseline, exact membership, readings, links, strokes, font cmaps and original budgets. Original reviews/Android/native/visual reverified separately, not rerun. Historical confirmation noncompliance remains explicit; physical-phone/general-release and whole-set outstanding.",
)
(scope["FOLDER"] / "batch-059-acceptance-source-audit.json").write_text(
    scope["json"].dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("Combined source audit passed:54exact families;baseline985/4942/985;8306hashes;3readings;2reciprocalpairs;11wordguards;pinnedstrokes;actualHanfontcmaps;originalbudgets.")
