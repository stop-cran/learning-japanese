"""Prepare batch N's core chain or a run's mechanically selected extension; never launches a reviewer.

Core:      python -B prepare-chain.py <batch>
Extension: python -B prepare-chain.py <batch> --run <run> --reply <phase1-list> --phase1-audit <audit.json>
"""
import argparse
import json
import sys
from pathlib import Path

from b130_compact_common import SNAP, CHECKS, WS, TOOLS, freeze_json, frozen, load_batch, require, review_dir, sha, start_guard, \
    verify_packet, write_frozen


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("batch", type=int)
    parser.add_argument("--run")
    parser.add_argument("--reply", type=Path)
    parser.add_argument("--phase1-audit", type=Path)
    args = parser.parse_args(argv)
    if bool(args.reply) != bool(args.run) or bool(args.reply) != bool(args.phase1_audit):
        parser.error("Extension preparation requires --run, --reply and --phase1-audit together")
    if args.run and not args.run.replace("-", "").isalnum():
        parser.error("Run identifier must contain letters, digits or hyphens only")
    records = review_dir(args.batch)
    sys.path.insert(0, str(records))
    from review_chain import build_chain, validate_selection
    config = load_batch(args.batch)
    n = config["batch"]
    guard, _ = start_guard("Chain preparation")
    try:
        packet_root, sums, packet_sha = verify_packet(config, guard)
        reference = json.loads((packet_root / "eligibility-reference.json").read_bytes())
        packet = json.loads((packet_root / "packet.json").read_bytes())
        members = packet["newKanji"]
        sources, missing = [], []

        def add(relative, last=None, display=None):
            data = (packet_root / Path(relative)).read_bytes()
            require(sha(data) == sums[relative], relative)
            sources.append((display or relative, data, last))

        if args.reply:
            reply_bytes = frozen(args.reply)
            phase1_bytes = frozen(args.phase1_audit)
            phase1 = json.loads(phase1_bytes)
            require(phase1["status"] == "PHASE1_READY" and phase1["breaches"] == [], "Phase 1 audit not ready")
            require(phase1["phase1ListSha256"] == sha(reply_bytes), "Reply differs from the audited phase-1 list")
            selection = validate_selection(reply_bytes.decode("utf-8"), reference)
            if not selection["valid"]:
                freeze_json(records / f"{args.run}-extension-void.json", {
                    "status": "VOID", "run": args.run, "extensionBuilt": False,
                    "replySha256": sha(reply_bytes), "errors": selection["errors"],
                    "quarantine": "No observations may become review evidence, reconciliation input or later hints.",
                })
                raise ValueError("Invalid list; no extension created")
            for entry in selection["entries"]:
                relative = f"repo/kanji/{entry['character']}.md"
                if relative not in sums:
                    missing.append(entry["requestLine"])
                else:
                    add(relative, display=f"{relative} [{entry['label']}]")
            directory = WS / "review-chains" / f"b{n}-{args.run}-extension"
            manifest_path = records / f"{args.run}-extension.json"
            message_path = records / f"{args.run}-phase2-message.txt"
            preflight = records / f"{args.run}-extension-preflight.json"
            label = f"B{n} {args.run} extension"
        else:
            for relative in ("REVIEW.md", "packet.json", "rubric/copilot-instructions.md",
                             "rubric/content-structure.instructions.md"):
                add(relative)
            add("repo/docs/content-format.md", config.get("contentFormatLines", 139))
            add("repo/docs/jlpt-levels.md")
            for folder in ("kanji/{}.md", "strokes/{}.json"):
                for c in members:
                    add("snapshot/" + folder.format(c))
            add("diffs/existing.diff")
            for relative in packet["modifiedExisting"]:
                add(f"snapshot/{relative}")
            for relative in packet["supportingUnchanged"]:
                add(f"repo/{relative}")
            for name in CHECKS:
                add(f"checks/{name}.txt")
            add("evidence/xml-presentation.json")
            for name in ("source-metadata.json", "kanjidic2-records.xml", "jmdict-families.xml",
                         "dictionary-index.json", "joyo-rows.json", "shape-evidence.json",
                         "provenance.json", "title-index.txt"):
                add(f"evidence/{name}")
            for c in dict.fromkeys(c for row in reference["cards"] for c in row["distractors"]):
                add(f"repo/kanji/{c}.md")
            snapshots = json.loads((packet_root / f"{SNAP}/manifest.json").read_bytes())
            add(f"{SNAP}/manifest.json")
            for item in snapshots["snapshots"]:
                if item["status"] == "SUPPLIED":
                    add(item["extract"]["path"])
            directory = WS / "review-chains" / f"b{n}-initial-compact-001"
            manifest_path = records / "core-chain-compact-001.json"
            message_path = None
            preflight = records / "core-chain-compact-001-preflight.json"
            label = f"B{n} required core"
        for path in (directory, manifest_path, preflight, *(p for p in [message_path] if p)):
            require(not path.exists(), f"Preserve existing output: {path}")
        chain = build_chain(sources, directory, manifest_path, guard, label)
        guard.check()
        if message_path:
            message = chain["segments"][0]["path"] + "\n" + (
                "Missing entries:\n" + "\n".join(missing) if missing else "Missing entries: none")
            write_frozen(message_path, message.encode("utf-8"))
        memory = guard.finish()
    except (Exception, KeyboardInterrupt):
        guard.finish()
        raise
    record = {
        "batch": n, "packetManifestSha256": packet_sha, "chainManifest": str(manifest_path),
        "chainManifestSha256": sha(manifest_path.read_bytes()), "firstSegment": chain["segments"][0]["path"],
        "segments": len(chain["segments"]), "sources": len(chain["sources"]), "missingVerbatim": missing,
        "builder": {"path": str(TOOLS / "prepare-chain-b130-compact.py"), "sha256": sha((TOOLS / "prepare-chain-b130-compact.py").read_bytes())},
        "memory": memory,
    }
    if args.reply:
        record.update(run=args.run, replySha256=sha(reply_bytes), phase1AuditSha256=sha(phase1_bytes),
                      phase2Message=str(message_path), phase2MessageSha256=sha(message_path.read_bytes()))
    freeze_json(preflight, record)
    print(json.dumps(record, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
