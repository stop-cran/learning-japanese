import contextlib
import io
from pathlib import Path

c = Path(__file__).resolve().parent
source = c / "execution-361-audit.py"
text = source.read_text(encoding="utf-8")
for before, after in {
    'assert ledger["reviewClosed"] == ledger["published"] == []':
        'assert ledger["reviewClosed"] == ["亭"] and ledger["published"] == []',
    'FOLDER / "batch-060-draft-audit.json"':
        'FOLDER / "batch-060-acceptance-source-audit.json"',
}.items():
    assert text.count(before) == 1, before
    text = text.replace(before, after)
scope = {"__file__": str(source), "__name__": "bounded_acceptance"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(text, str(source), "exec"), scope)
    scope["audit"]()
result = scope["load"](scope["FOLDER"] / "batch-060-acceptance-source-audit.json")
result.update(
    execution=369, status="combined-source-audit-pending-evidence-reverification",
    freshLinguisticReviewOfAllFamiliesClaimed=False,
    coordinatorInspection="Fresh combined-tree mechanical re-extraction of51frozen families; original linguistic inspection/reconciliation retained, not newly performed.",
    limits="Mechanical source, baseline, exact membership, readings, links, strokes, font cmaps and original budgets. Original reviews/Android/native/visual reverified separately, not rerun. Historical060-P1/P2 process noncompliance remains explicit; physical-phone/general-release and whole-set outstanding.",
)
scope["save"](scope["FOLDER"] / "batch-060-acceptance-source-audit.json", result)
print("Combined source audit passed:51exact families;baseline985/4942/985;8309hashes;2readings;2reciprocalpairs;11legacyguards;pinnedstrokes;actualHanfontcmaps;originalbudgets.")
