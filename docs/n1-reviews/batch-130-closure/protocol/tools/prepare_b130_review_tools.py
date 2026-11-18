"""Derive B130's neutral contract and packet builder without changing predecessors."""
import json
from pathlib import Path

from common import freeze_json, frozen, require, sha, write_frozen

ROOT = Path(__file__).resolve().parent
HERE = ROOT.parent / "scratch-130" / "review"


def derive(source_name, target_name, changes):
    raw = frozen(ROOT / source_name)
    original_lines = raw.decode("utf-8").splitlines(keepends=True)
    endings = ["\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
               for line in original_lines]
    text = raw.decode("utf-8").replace("\r\n", "\n")
    applied = []
    for before, after in changes:
        require(text.count(before) > 0, "Missing derivation anchor: " + before[:90])
        count = text.count(before)
        text = text.replace(before, after)
        applied.append({"before": before, "after": after, "count": count})
    reverse = text
    for change in reversed(applied):
        require(reverse.count(change["after"]) == change["count"], "Ambiguous reverse derivation")
        reverse = reverse.replace(change["after"], change["before"])
    restored_lines = reverse.splitlines(keepends=True)
    require(len(restored_lines) == len(endings), "Reverse line count differs")
    restored = "".join(line.removesuffix("\n") + ending for line, ending in zip(restored_lines, endings))
    require(restored.encode("utf-8") == raw, "Nonreversible tool derivation")
    compile(text, target_name, "exec")
    return {"source": {"path": str(ROOT / source_name), "sha256": sha(raw)},
            "output": write_frozen(ROOT / target_name, text.encode("utf-8")),
            "changes": applied, "sourceLineEndings": endings, "byteReversible": True}


def main():
    original = frozen(ROOT / "prepare_b129_review_contract.py").decode("utf-8").replace("\r\n", "\n")
    old_joyo = original[original.index("JOYO_ROWS = {"):original.index("\n\n\ndef query_index")]
    new_joyo = "JOYO_ROWS = " + json.dumps({
        "\u5840": ["136", "\u5840\uff08 \ufa39\uff09\n\u30d8\u30a4 \u5840\uff0c\u677f\u5840"],
        "\u62cd": ["125", "\u62cd\n\u30cf\u30af \u62cd\u624b\uff0c\u62cd\u8eca\uff0c\u4e00\u62cd\n\u30d2\u30e7\u30a6 \u62cd\u5b50"],
        "\u8017": ["147", "\u8017\n\u30e2\u30a6 \u6d88\u8017 \u300c\u30e2\u30a6\u300d\u306f\uff0c\u6163\u7528\u97f3\u3002\n\u30b3\u30a6 \u5fc3\u795e\u8017\u5f31"],
    }, ensure_ascii=True, indent=4)
    contract = derive("prepare_b129_review_contract.py", "prepare_b130_review_contract.py", [
        ("B129", "B130"), ("b129", "b130"), ('"batch": 129', '"batch": 130'),
        ('proof["batch"] == 129', 'proof["batch"] == 130'),
        (old_joyo, new_joyo),
        ('from b130_source_schema import verify_scan\n',
         'from b130_source_schema import verify_scan\n'
         'from b130_signed_evidence import FINAL_VERIFIER_SHA, RESIDUAL, verify_final_proof\n'),
        ('             "baselineGitBytesSha256": row["baselineBytesSha256"],',
         '             "baselineWorkingBytesSha256": row["baselineWorkingBytesSha256"],\n'
         '             "baselineNormalizedSha256": row["baselineNormalizedSha256"],'),
        ('    candidate = source_proof["candidate"]\n',
         '    candidate = source_proof["candidate"]\n'
         '    final_binding = evidence["finalSourceProof"]\n'
         '    final_proof = json.loads(frozen(final_binding["path"], final_binding["sha256"]))\n'
         '    verify_final_proof(final_proof, source_sha, candidate)\n'
         '    frozen(Path(__file__).with_name("verify_b130_final_sources.py"), FINAL_VERIFIER_SHA)\n'
         '    final_facts = json.loads(frozen(final_proof["facts"]["path"], final_proof["facts"]["sha256"]))\n'),
        ('            and evidence["findings"] == [], "Candidate evidence remains unresolved")',
         '            and evidence["finalSourceProof"]["sha256"] == final_binding["sha256"],\n'
         '            "Candidate evidence remains unresolved")'),
        ('                                   if record["input"] == "n1-implementation-JMdict_e.gz"], "entry", "ent_seq")',
         '                                   if record["input"] == "n1-implementation-JMdict_e.gz"]\n'
         '                                  + [source(RESIDUAL)], "entry", "ent_seq")'),
        ('len(jm) == 252', 'len(jm) == 519'),
        ('for directory in ("scans-003", "scans-004"):', 'for directory in ("scans-002",):'),
        ('query_index(jm, facts["jmdictSelections"])',
         'query_index(jm, [{"mode": "union", "queries": final_facts["queries"]}])'),
        ('len(pending & before) == 258', 'len(pending & before) == 261'),
        ('len(pending & after) == 261', 'len(pending & after) == 264'),
        ('len(after) == 1251', 'len(after) == 1254'),
        ('"expectedKanji": 1251', '"expectedKanji": 1254'),
        ('"sourceMembersPublishedBeforeBatch": 258', '"sourceMembersPublishedBeforeBatch": 261'),
        ('"sourceMembersInCandidate": 261', '"sourceMembersInCandidate": 264'),
        ('"dictionaryVerification": {"path": source_path, "sha256": source_sha},',
         '"dictionaryVerification": {"path": source_path, "sha256": source_sha},\n'
         '        "finalDictionaryVerification": final_binding,'),
    ])
    packet = derive("build-packet-b129.py", "build-packet-b130.py", [
        ("build-packet-b129.py", "build-packet-b130.py"),
        ("b129_external_sources.py", "b130_external_sources.py"),
        ("from b129_external_sources import", "from b130_external_sources import"),
    ])
    print(freeze_json(HERE / "review-tool-derivation.json", {
        "contract": contract, "packet": packet,
        "producerSha256": sha(Path(__file__).read_bytes()),
        "limits": "Neutral review preparation only; signed execution and packet validation still required.",
    }))


if __name__ == "__main__":
    main()
