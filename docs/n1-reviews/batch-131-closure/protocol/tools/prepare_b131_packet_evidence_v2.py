"""Correct the coordinator's expanded font assumption to the inspected producer scope."""
import json
from pathlib import Path

from common import WS, freeze_json, frozen, require, sha, start_guard

TOOLS = Path(__file__).resolve().parent
HERE = WS / "scratch-131" / "review"
frozen(TOOLS / "prepare_b131_source_verifier.py",
       "1c49464972263d673822b45a3445d293f439c3c03cc00ed3e1ab974e7f1544a5")
from prepare_b131_source_verifier import derive


def main():
    require(not (HERE / "packet-evidence-recovery-001.json").exists()
            and not (TOOLS / "verify_b131_packet_evidence_v2.py").exists(), "Preserve recovery artifacts")
    failed_raw = frozen(HERE / "packet-verification-execution-001" / "receipt.json")
    failed = json.loads(failed_raw)
    log = frozen(HERE / "packet-verification-execution-001" / "output.log", failed["logSha256"])
    require(failed["exitCode"] == 1
            and b"ValueError: Finite taught/comparison Han or code-point inventory differs" in log,
            "Unexpected predecessor failure")
    guard, _ = start_guard("B131 finite font-scope correction")
    try:
        derived = derive(
            "verify_b131_packet_evidence.py",
            "b7de738bc79f8d879d81f2b47f288ab9d4b0d6e376c7f947d48688c6c2df8e56",
            "verify_b131_packet_evidence_v2.py", [
                ('HERE / "packet-verification-001"', 'HERE / "packet-verification-002"'),
                ('            comparisons[char] = metadata["title"], sha(raw)\n'
                 '            teaching.append(raw.decode("utf-8"))\n',
                 '            comparisons[char] = (metadata["title"], sha(raw))\n'),
                ('                and set(re.findall("[\\u3400-\\u4dbf\\u4e00-\\u9fff]", "\\n".join(teaching))) <= chars,\n',
                 '                and (set(re.findall("[\\u3400-\\u9fff]", "\\n".join(teaching)))\n'
                 '                     | set(comparisons) | set("\\u5f73\\u4e8d\\u97cb\\u884c\\u7f8a\\u96e8\\u76f8\\u6728\\u76ee")) == chars,\n'),
                ('        points = fonts["codePoints"]\n',
                 '        require(fonts["producerSha256"] == signed[PREFIX + "producers/font_final_b131.py"]\n'
                 '                and fonts["initialGenerationEvidenceSha256"] == signed[PREFIX + "stroke-font-evidence.json"],\n'
                 '                "Font producer or initial generation binding differs")\n'
                 '        points = fonts["codePoints"]\n'),
                ('"fontMissingCodePoints": missing, "memory": memory,',
                 '"fontMissingCodePoints": missing,\n'
                 '        "fontScope": "All Han in the three new cards, all comparison identifiers and explicit "\n'
                 '                     "mnemonic/radical components; not every legacy comparison article body.",\n'
                 '        "memory": memory,'),
            ])
        guard.check()
    finally:
        memory = guard.finish()
    require(not memory["breach"], "RAM breach")
    print(json.dumps(freeze_json(HERE / "packet-evidence-recovery-001.json", {
        "status": "PREPARATION_ONLY", "derivation": derived, "failedReceiptSha256": sha(failed_raw),
        "producerSha256": sha(frozen(Path(__file__))), "memory": memory,
        "qualification": "The predecessor incorrectly demanded font coverage evidence for all Han "
                         "throughout 179 legacy article bodies. The actual signed producer probes all "
                         "Han in the new cards, the 179 comparison identifiers and explicit components. "
                         "V2 exactly reproduces that finite set and records its limits; no author "
                         "evidence or teaching changed, and rendered fallback remains unverified.",
    })))


if __name__ == "__main__":
    main()
