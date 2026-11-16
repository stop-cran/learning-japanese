"""Specialize the historical gate's reading inventory without weakening its checks."""
import ast
from pathlib import Path

from common import TOOLS, freeze_json, frozen, require, sha, write_frozen
from verify_b127_reconciliation import REVIEW


def main():
    source = TOOLS / "verify_b127_reconciliation_v3.py"
    original = frozen(source, "f4c1cb5e8f73da6200dfcd9bc1e981c28279a3a4b75615e2b3dd592f8526ecd3")
    helper_path = TOOLS / "verify_b123_revision_v2.py"
    helper_raw = frozen(helper_path)
    helper_text = helper_raw.decode()
    node = next(node for node in ast.parse(helper_text).body
                if isinstance(node, ast.FunctionDef) and node.name == "check_gate")
    selected = ast.get_source_segment(helper_text, node)
    old_readings = r'("\u7bc4", "\u30cf\u30f3", "\u306e\u308a", "\u3059\u3059\u3080")'
    new_readings = (
        r'("\u5009", "\u30bd\u30a6", "\u304f\u3089", "\u306b\u308f\u304b", '
        r'"\u307b\u308d\u3076", "\u3082\u308d\u3057", "\u304a\u3055\u3081\u308b", "\u3072\u3068\u3084")'
    )
    require(selected.count(old_readings) == 1, "Historical reading gate changed")
    specialized = selected.replace(old_readings, new_readings)
    require(specialized.replace(new_readings, old_readings) == selected, "Gate derivation not reversible")
    before = b"from verify_b123_revision_v2 import check_gate, runtime"
    after = ("from verify_b123_revision_v2 import runtime\n\n" + specialized + "\n").encode()
    require(original.count(before) == 1, "Historical import changed")
    derived = original.replace(before, after)
    require(derived.replace(after, before) == original, "Verifier derivation not reversible")
    compile(derived, "verify_b127_reconciliation_v4.py", "exec")
    target = write_frozen(TOOLS / "verify_b127_reconciliation_v4.py", derived)
    print(freeze_json(REVIEW / "reconciliation-verifier-v4-derivation.json", {
        "source": {"path": str(source), "sha256": sha(original)}, "output": target,
        "gateSource": {"path": str(helper_path), "sha256": sha(helper_raw)},
        "oldReadings": old_readings, "newReadings": new_readings, "reverseExact": True,
        "reason": "The reused B123 gate embeds B123's readings. Its complete receipt/log/resource "
                  "checks are retained, but reading exposure must cover B127's target, frozen "
                  "readings and five explicitly supplied supplemental alternatives.",
        "producerSha256": sha(Path(__file__).read_bytes()),
    }))


if __name__ == "__main__":
    main()
