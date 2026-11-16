"""Verify exact partial outputs, then finish the failed prompt derivation."""
import ast
import json
from pathlib import Path

from common import TOOLS, WS, freeze_json, frozen, require, sha, write_frozen


def main():
    root = WS / "scratch-130" / "review"
    producer = TOOLS / "prepare_b130_compact_review.py"
    original_producer = frozen(producer)
    receipt_raw = (root / "compact-review-preparation-001" / "receipt.json").read_bytes()
    receipt = json.loads(receipt_raw)
    require(receipt["exitCode"] == 1 and not receipt["memory"]["breach"]
            and receipt["logSha256"] == sha((root / "compact-review-preparation-001" / "output.log").read_bytes()),
            "Expected preparation failure differs")
    packet_path = root / "compact-review-packet-preflight-001.json"
    packet = json.loads(frozen(packet_path))
    require(packet["status"] == "PASS_PRESENTATION_ONLY", "Partial packet proof absent")
    manifest = json.loads(frozen(packet["packetManifest"]["path"], packet["packetManifest"]["sha256"]))
    for path, digest in manifest.items():
        frozen(Path(packet["packet"]) / path, digest)
    module = ast.parse(original_producer)
    main_node = next(node for node in module.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    calls = [
        node.value for node in main_node.body
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name) and node.value.func.id == "derive"
    ]
    require(len(calls) == 4, "Expected four explicit derivations")
    records = []
    for call in calls:
        source, target, changes = map(ast.literal_eval, call.args)
        if target == "build-prompts-b130-compact.py":
            require(changes[-1] == ('"preflight.json"', '"preflight-compact-001.json"'),
                    "Failed replacement differs")
            changes[-1] = (
                'freeze_json(prompts / "preflight.json", record)',
                'freeze_json(prompts / "preflight-compact-001.json", record)',
            )
        raw = frozen(TOOLS / source)
        original_lines = raw.decode("utf-8").splitlines(keepends=True)
        endings = ["\r\n" if line.endswith("\r\n") else "\n" if line.endswith("\n") else ""
                   for line in original_lines]
        text = raw.decode("utf-8").replace("\r\n", "\n")
        applied = []
        for before, after in changes:
            count = text.count(before)
            require(count > 0, "Missing derivation anchor: " + before)
            text = text.replace(before, after)
            applied.append({"before": before, "after": after, "count": count})
        reverse = text
        for change in reversed(applied):
            require(reverse.count(change["after"]) == change["count"],
                    "Ambiguous reverse derivation: " + change["after"])
            reverse = reverse.replace(change["after"], change["before"])
        lines = reverse.splitlines(keepends=True)
        require(len(lines) == len(endings), "Restored line count differs")
        restored = "".join(line.removesuffix("\n") + ending for line, ending in zip(lines, endings))
        require(restored.encode("utf-8") == raw, "Nonreversible derivation")
        derived = text.encode("utf-8")
        compile(derived, target, "exec")
        path = TOOLS / target
        reused = path.exists()
        if reused:
            require(frozen(path) == derived, "Partial output differs")
            output = {"path": str(path), "sha256": sha(derived), "bytes": len(derived)}
        else:
            output = write_frozen(path, derived)
        records.append({
            "source": {"path": str(TOOLS / source), "sha256": sha(raw)},
            "output": output, "changes": applied, "sourceLineEndings": endings,
            "byteReversible": True, "reusedExactPartialOutput": reused,
        })
    print(freeze_json(root / "compact-review-tooling-derivation-002.json", {
        "batch": 130, "status": "PREPARATION_ONLY",
        "packetProof": {"path": str(packet_path), "sha256": sha(frozen(packet_path))},
        "originalProducer": {"path": str(producer), "sha256": sha(original_producer)},
        "producer": {"path": str(Path(__file__)), "sha256": sha(frozen(Path(__file__)))},
        "failureReceiptSha256": sha(receipt_raw), "derivations": records,
        "repair": "The last broad preflight filename replacement collided in reverse with an "
                  "earlier inserted preflight guard. Use its unique freeze_json call anchor. "
                  "Existing packet, hold and three generated tools were verified/reused unchanged.",
        "limits": "No reviewer launched or accepted; original context failure is preserved. "
                  "Replacement prompts, admission and actual context auditing remain required.",
    }))


if __name__ == "__main__":
    main()
