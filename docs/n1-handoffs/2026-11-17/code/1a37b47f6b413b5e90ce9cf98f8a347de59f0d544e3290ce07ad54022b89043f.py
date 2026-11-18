"""Derive explicit integration successors without altering earlier protocol programs."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, write_frozen
from verify_b130_integration_runtime import ROOT

TOOLS = Path(__file__).parent


def replace_once(text, old, new):
    require(text.count(old) == 1, "Integration derivation anchor changed")
    return text.replace(old, new)


def main():
    outputs = []
    text = frozen(TOOLS / "confirm_b130_followup_v3.py",
                  "41d23ec4ab7e5dc63ead708957da2554efa77f900c01fdb52bb288ab6c4137cf").decode()
    text = text.replace("b130_followup_admission_v2", "b130_integration_admission")
    text = text.replace("b130_followup_lineage_v2", "b130_integration_lineage")
    text = replace_once(
        text,
        'sources = [(f"previous-confirmation/{Path(prior[\'report\'][\'path\']).name}", previous, None),\n'
        '               (f"initial-report/{Path(initial[\'report\'][\'path\']).name}", original, None)]',
        'sources = [(f"previous-confirmation/{Path(prior[\'report\'][\'path\']).name}", previous, None)]',
    )
    text = replace_once(text, '    return text\n\n\ndef verify_prior',
                        '    text += ("\\nINTEGRATION-IMPACT FOLLOW-UP\\n"\n'
                        '             "Check whether the actual integration delta changes or invalidates your own "\n'
                        '             "earlier B130 conclusions. The complete incoming article and counter, "\n'
                        '             "current scoped cards/supports, own response/mapping and neutral mechanical "\n'
                        '             "evidence are supplied. N1 content and earlier evidence are byte-preserved. "\n'
                        '             "Do not transfer acceptance automatically or assert an independent linguistic "\n'
                        '             "audit of the unrelated counter fix. Its impact on this N1 review is in scope. "\n'
                        '             "The initial report, complete original corpus, comparison-card universe and "\n'
                        '             "old source collections are not reread in this bounded followup; do not claim "\n'
                        '             "otherwise. Your own prior accepted report and retained uncompacted context "\n'
                        '             "remain the basis. Preserve every prior limit, including unresolved lexical "\n'
                        '             "allocation, guarded quiz consequence, latent readings and native/device limits.\\n")\n'
                        '    return text\n\n\ndef verify_prior')
    text = replace_once(text, '"basis": spec["basis"], "prior": spec["prior"],',
                        '"basis": spec["basis"], "capacityObservation": spec["capacityObservation"], '
                        '"prior": spec["prior"],')
    outputs.append(write_frozen(TOOLS / "confirm_b130_integration.py", text.encode()))
    text = frozen(TOOLS / "b130_followup_admission_v2.py",
                  "30223ccd6753d310871aa88f1328c42d9b4890cd193014813dd6cd1e09693d78").decode()
    text = replace_once(text,
                        "from b130_followup_lineage_v2 import require_followup_preflight",
                        "from b130_integration_lineage import require_followup_preflight, verify_capacity")
    text = replace_once(text, '    guard, _ = start_guard(record["run"])',
                        '    capacity = verify_capacity(record, config, raw)\n'
                        '    guard, _ = start_guard(record["run"])')
    text = replace_once(text, '"scopeTool": {"path": str(scope_path), "sha256": SCOPE_SHA},',
                        '"scopeTool": {"path": str(scope_path), "sha256": SCOPE_SHA},\n'
                        '        "capacityEvidence": capacity,')
    outputs.append(write_frozen(TOOLS / "b130_integration_admission.py", text.encode()))
    print(json.dumps(freeze_json(ROOT / "integration-protocol-derivation-001.json", {
        "outputs": outputs,
        "changes": "Explicit accepted-prior integration lineage; omit rereading the unchanged initial "
                   "report with disclosure; bind current capacity observation and enforce it before "
                   "admission. Original audit, finalizer, report grammar, serial/resource gates and "
                   "all earlier programs remain unchanged. No reviewer launched.",
    })))


if __name__ == "__main__":
    main()
